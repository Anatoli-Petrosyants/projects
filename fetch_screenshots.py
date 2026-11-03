#!/usr/bin/env python3
"""Download per-app App Store screenshots and preview videos.

Screenshots land in assets/img/shots/<slug>/; an App Preview video, when the
store listing has one, lands in assets/video/<slug>.mp4 with its poster frame
beside it as assets/video/<slug>.jpg.

The home grid and social cards use the single wide collage in
assets/img/apps/<slug>.jpg; the project page gallery uses the individual
screenshots this script pulls from the public iTunes lookup API, so they stay
in sync with whatever is live on the App Store.

    python3 fetch_screenshots.py            # every project
    python3 fetch_screenshots.py ctrltv     # one slug

Re-run it after shipping new store screenshots, then run build.py.

The lookup API has no field for preview videos, so those are read out of the
public apps.apple.com listing page, which embeds the HLS playlist URL. ffmpeg
remuxes the best variant into a single MP4 (no re-encode); without ffmpeg on
PATH the video step is skipped and any existing file is left alone.
"""

import gzip
import json
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
PROJECTS = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
SHOT_DIR = ROOT / "assets" / "img" / "shots"
VIDEO_DIR = ROOT / "assets" / "video"

# mzstatic serves any size from the same base path; 540px wide covers a 2x
# render of the ~270px gallery card without bloating the repo.
WIDTH = 540
LOOKUP = "https://itunes.apple.com/lookup?id=%s&country=us"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch(url):
    request = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def app_id(project):
    match = re.search(r"/id(\d+)", project["appStoreUrl"])
    if not match:
        raise ValueError("no App Store id in %s" % project["appStoreUrl"])
    return match.group(1)


def resize(url):
    """Swap the trailing size segment of an mzstatic thumb URL for ours."""
    return url.rsplit("/", 1)[0] + "/%dx0w.jpg" % WIDTH


def listing_url(project):
    """The store page for the app, in the storefront its appStoreUrl names."""
    match = re.search(r"apps\.apple\.com/([a-z]{2})/", project["appStoreUrl"])
    country = match.group(1) if match else "us"
    return "https://apps.apple.com/%s/app/id%s" % (country, app_id(project))


# The first App Preview on the page is the iPhone one: the listing orders the
# iPhone media shelf before iPad, and the poster template sits next to it.
VIDEO_RE = re.compile(
    r'"video":\{"\$kind":"Video","videoUrl":"([^"]+\.m3u8)",'
    r'"preview":\{[^{}]*?"template":"([^"]+)"'
)


def best_variant(master_url):
    """The highest-bandwidth video playlist and the audio playlist it pairs with."""
    master = fetch(master_url).decode("utf-8")
    audio = dict(re.findall(r'TYPE=AUDIO,[^\n]*?GROUP-ID="([^"]+)"[^\n]*?URI="([^"]+)"', master))
    best = None
    for attrs, uri in re.findall(r"#EXT-X-STREAM-INF:([^\n]+)\n(\S+)", master):
        bandwidth = int(re.search(r"(?<![-_A-Z])BANDWIDTH=(\d+)", attrs).group(1))
        group = re.search(r'AUDIO="([^"]+)"', attrs)
        if best is None or bandwidth > best[0]:
            best = (bandwidth, uri, audio.get(group.group(1)) if group else None)
    return best[1], best[2]


def fetch_video(project):
    slug = project["slug"]
    page = fetch(listing_url(project))
    # apps.apple.com sometimes gzips even when the request did not offer it
    if page[:2] == b"\x1f\x8b":
        page = gzip.decompress(page)
    html = page.decode("utf-8", "replace")
    match = VIDEO_RE.search(html)
    video, poster = VIDEO_DIR / ("%s.mp4" % slug), VIDEO_DIR / ("%s.jpg" % slug)
    if not match:
        # the preview was taken down on the store: take it down here too
        for stale in (video, poster):
            if stale.exists():
                stale.unlink()
        return None
    if not shutil.which("ffmpeg"):
        print("!! %-15s has a preview video but ffmpeg is not installed" % slug)
        return None

    playlist, template = match.group(1), match.group(2)
    video_url, audio_url = best_variant(playlist)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    command = ["ffmpeg", "-loglevel", "error", "-y", "-i", video_url]
    if audio_url:
        command += ["-i", audio_url, "-map", "0:v:0", "-map", "1:a:0"]
    # faststart moves the index to the front so playback starts before the
    # whole file has downloaded
    command += ["-c", "copy", "-movflags", "+faststart", str(video)]
    subprocess.run(command, check=True)
    poster.write_bytes(fetch(template.replace("{w}x{h}{c}.{f}", "%dx0w.jpg" % WIDTH)))
    return video


def main(slugs):
    for project in PROJECTS:
        slug = project["slug"]
        if slugs and slug not in slugs:
            continue

        payload = json.loads(fetch(LOOKUP % app_id(project)))
        if not payload["resultCount"]:
            print("!! %-15s no App Store result" % slug)
            continue

        shots = payload["results"][0].get("screenshotUrls") or []
        if not shots:
            print("!! %-15s no screenshots" % slug)
            continue

        out = SHOT_DIR / slug
        out.mkdir(parents=True, exist_ok=True)
        for stale in out.glob("*.jpg"):
            stale.unlink()

        for number, url in enumerate(shots, start=1):
            path = out / ("%02d.jpg" % number)
            path.write_bytes(fetch(resize(url)))
        video = fetch_video(project)
        print("   %-15s %d screenshots%s" % (slug, len(shots), ", preview video" if video else ""))


if __name__ == "__main__":
    main(set(sys.argv[1:]))
