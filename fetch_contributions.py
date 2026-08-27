#!/usr/bin/env python3
"""Snapshot the GitHub contribution graph into data/contributions.json.

GitHub has no public REST endpoint for the calendar (the GraphQL one needs a
token), but the profile page loads it from an unauthenticated HTML fragment at
/users/<login>/contributions. This script parses that fragment into the day
grid build.py renders, so the site keeps its no-runtime-dependency rule: the
heatmap is baked into index.html at build time, not fetched in the browser.

    python3 fetch_contributions.py                  # login from data/site.json
    python3 fetch_contributions.py some-other-user

Re-run it whenever the graph should be refreshed, then run build.py and commit
both data/contributions.json and the regenerated index.html.
"""

import datetime
import html
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
SITE = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
OUT = DATA / "contributions.json"

GRAPH = "https://github.com/users/%s/contributions"
UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "X-Requested-With": "XMLHttpRequest",
}

DAY_RE = re.compile(
    r'<td[^>]*\bdata-date="(\d{4}-\d{2}-\d{2})"[^>]*'
    r'\bid="contribution-day-component-(\d+)-(\d+)"[^>]*'
    r'\bdata-level="(\d+)"',
)
TOOLTIP_RE = re.compile(
    r'<tool-tip[^>]*\bfor="contribution-day-component-(\d+)-(\d+)"[^>]*>(.*?)</tool-tip>',
    re.S,
)
MONTH_RE = re.compile(
    r'<td class="ContributionCalendar-label"[^>]*colspan="(\d+)"[^>]*>.*?'
    r'aria-hidden="true"[^>]*>([^<]+)</span>',
    re.S,
)
TOTAL_RE = re.compile(
    r'id="js-contribution-activity-description"[^>]*>\s*([\d,]+)\s*\n?\s*contributions',
)
RANGE_RE = re.compile(r'data-(from|to)="(\d{4}-\d{2}-\d{2})')
COUNT_RE = re.compile(r"^([\d,]+)\s+contribution")


def login():
    """The GitHub username, taken from the profile URL in site.json."""
    url = SITE["links"]["github"].rstrip("/")
    return url.rsplit("/", 1)[-1]


def fetch(url):
    request = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def counts(markup):
    """Map (row, column) to a contribution count, read out of the tooltips.

    The cell itself only carries data-level (0-4, the colour bucket); the exact
    number lives in the tool-tip element that describes it.
    """
    found = {}
    for row, column, text in TOOLTIP_RE.findall(markup):
        label = html.unescape(re.sub(r"<[^>]+>", "", text)).strip()
        match = COUNT_RE.match(label)
        found[(int(row), int(column))] = (
            int(match.group(1).replace(",", "")) if match else 0
        )
    return found


def parse(markup):
    total = TOTAL_RE.search(markup)
    if not total:
        raise ValueError("no contribution total in the response")

    span = dict(RANGE_RE.findall(markup))
    counted = counts(markup)

    days = {}
    columns = 0
    for date, row, column, level in DAY_RE.findall(markup):
        row, column = int(row), int(column)
        columns = max(columns, column + 1)
        days[(row, column)] = {
            "date": date,
            "level": int(level),
            "count": counted.get((row, column), 0),
        }
    if not days:
        raise ValueError("no day cells in the response")

    # Column-major, one list per week, None where the first and last weeks run
    # past the range GitHub returned.
    weeks = [[days.get((row, column)) for row in range(7)] for column in range(columns)]
    months = [
        {"label": label.strip(), "weeks": int(colspan)}
        for colspan, label in MONTH_RE.findall(markup)
    ]

    return {
        "user": None,
        "total": int(total.group(1).replace(",", "")),
        "from": span.get("from", ""),
        "to": span.get("to", ""),
        "fetched": datetime.date.today().isoformat(),
        "months": months,
        "weeks": weeks,
    }


def main(argv):
    user = argv[0] if argv else login()
    graph = parse(fetch(GRAPH % user))
    graph["user"] = user

    OUT.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(
        "   %s  %d contributions  %s to %s  (%d weeks)"
        % (user, graph["total"], graph["from"], graph["to"], len(graph["weeks"]))
    )


if __name__ == "__main__":
    main(sys.argv[1:])
