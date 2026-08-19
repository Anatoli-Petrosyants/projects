#!/usr/bin/env python3
"""Download per-app App Store screenshots into assets/img/shots/<slug>/.

The home grid and social cards use the single wide collage in
assets/img/apps/<slug>.jpg; the project page gallery uses the individual
screenshots this script pulls from the public iTunes lookup API, so they stay
in sync with whatever is live on the App Store.

    python3 fetch_screenshots.py            # every project
    python3 fetch_screenshots.py ctrltv     # one slug

Re-run it after shipping new store screenshots, then run build.py.
"""

import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
PROJECTS = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
SHOT_DIR = ROOT / "assets" / "img" / "shots"

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
        print("   %-15s %d screenshots" % (slug, len(shots)))


if __name__ == "__main__":
    main(set(sys.argv[1:]))
