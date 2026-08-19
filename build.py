#!/usr/bin/env python3
"""Static site generator for the portfolio.

Reads data/site.json + data/projects.json, writes index.html, contact.html,
projects/<slug>.html, 404.html, sitemap.xml and robots.txt.

No third-party dependencies. Run:  python3 build.py
"""

import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
PROJECT_DIR = ROOT / "projects"

SITE = json.loads((DATA / "site.json").read_text(encoding="utf-8"))
PROJECTS = json.loads((DATA / "projects.json").read_text(encoding="utf-8"))

BASE_URL = SITE["baseUrl"].rstrip("/")


def e(value):
    """Escape a value for HTML text/attribute context."""
    return html.escape(str(value), quote=True)


# --------------------------------------------------------------------------
# inline icons
# --------------------------------------------------------------------------

ICONS = {
    "appstore": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.36 12.9c-.02-2.3 1.88-3.4 1.96-3.45-1.07-1.56-2.73-1.78-3.32-1.8-1.41-.14-2.76.83-3.48.83-.72 0-1.83-.81-3.01-.79-1.55.02-2.98.9-3.78 2.29-1.61 2.79-.41 6.92 1.16 9.18.77 1.11 1.68 2.35 2.88 2.31 1.16-.05 1.6-.75 3-.75s1.79.75 3.01.72c1.24-.02 2.03-1.13 2.79-2.24.88-1.28 1.24-2.53 1.26-2.6-.03-.01-2.42-.93-2.44-3.7zM14.1 5.2c.64-.78 1.07-1.86.95-2.94-.92.04-2.03.61-2.69 1.38-.59.69-1.11 1.79-.97 2.84 1.03.08 2.07-.52 2.71-1.28z"/></svg>',
    "download": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.07 1.4-2.07 2.85V21H9z"/></svg>',
    "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5C5.37.5 0 5.87 0 12.5c0 5.3 3.44 9.8 8.2 11.39.6.11.82-.26.82-.58v-2.2c-3.34.72-4.04-1.42-4.04-1.42-.55-1.4-1.34-1.77-1.34-1.77-1.09-.75.08-.73.08-.73 1.2.09 1.84 1.24 1.84 1.24 1.07 1.84 2.8 1.31 3.49 1 .1-.78.42-1.31.76-1.61-2.67-.3-5.47-1.34-5.47-5.96 0-1.32.47-2.39 1.24-3.23-.13-.3-.54-1.52.11-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6.01 0c2.29-1.55 3.3-1.23 3.3-1.23.65 1.66.24 2.88.12 3.18.77.84 1.23 1.91 1.23 3.23 0 4.63-2.8 5.65-5.48 5.95.43.37.81 1.1.81 2.22v3.29c0 .32.22.7.83.58A12.01 12.01 0 0 0 24 12.5C24 5.87 18.63.5 12 .5z"/></svg>',
    "upwork": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.56 5.9c-1.9 0-3.4 1.24-4 3.23-.93-1.4-1.63-3.1-2.04-4.53H9.47v5.5c0 1.09-.88 1.98-1.97 1.98a1.98 1.98 0 0 1-1.98-1.98V4.6H2.47v5.5A5 5 0 0 0 7.5 15.1a5 5 0 0 0 5-5.01v-.92c.4.83.9 1.7 1.5 2.47l-1.28 6.02h3.1l.92-4.36c.81.52 1.74.83 2.82.83 2.3 0 4.18-1.88 4.18-4.2 0-2.3-1.88-4.03-4.18-4.03zm0 5.68c-.87 0-1.74-.37-2.44-.97l.21-.85v-.02c.15-.9.65-2.4 2.23-2.4 1.18 0 2.14.96 2.14 2.14 0 1.16-.96 2.1-2.14 2.1z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.4 2.1L8.1 9.9a16 16 0 0 0 6 6l1.4-1.3a2 2 0 0 1 2.1-.5c.9.4 1.8.6 2.7.8a2 2 0 0 1 1.7 2z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.6 2 2.2 6.4 2.2 11.84c0 1.74.46 3.44 1.32 4.94L2 22l5.36-1.4a9.8 9.8 0 0 0 4.68 1.2h.01c5.43 0 9.84-4.4 9.84-9.84 0-2.63-1.02-5.1-2.88-6.96A9.78 9.78 0 0 0 12.04 2zm0 17.98h-.01a8.2 8.2 0 0 1-4.16-1.14l-.3-.18-3.1.81.83-3.02-.2-.31a8.13 8.13 0 0 1-1.25-4.3c0-4.51 3.68-8.18 8.2-8.18 2.19 0 4.24.85 5.79 2.4a8.13 8.13 0 0 1 2.4 5.79c0 4.52-3.68 8.13-8.2 8.13zm4.5-6.09c-.25-.13-1.46-.72-1.68-.8-.23-.08-.39-.13-.55.12-.17.25-.64.8-.78.97-.14.16-.29.18-.53.06-.25-.12-1.04-.38-1.98-1.22-.73-.65-1.23-1.46-1.37-1.7-.14-.25-.02-.38.11-.5.11-.11.25-.29.37-.44.13-.14.17-.25.25-.41.09-.17.04-.31-.02-.44-.06-.12-.55-1.34-.76-1.83-.2-.48-.4-.42-.55-.42h-.47c-.16 0-.42.06-.64.31-.22.25-.84.82-.84 2s.86 2.32.98 2.48c.12.17 1.7 2.6 4.12 3.64.58.25 1.03.4 1.38.51.58.19 1.1.16 1.52.1.46-.07 1.46-.6 1.66-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.29z"/></svg>',
    "telegram": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.7 19.4c-.24 1.07-.88 1.33-1.78.83l-4.92-3.63-2.37 2.29c-.26.26-.48.48-.99.48l.36-5.02L18.1 6.2c.4-.35-.08-.55-.62-.2L6.2 13.14 1.35 11.6c-1.06-.33-1.08-1.06.22-1.57L20.53 2.7c.88-.33 1.65.2 1.37 1.6z"/></svg>',
    "arrow-left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>',
    "sun": '<svg class="icon-sun" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "moon": '<svg class="icon-moon" viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
}


# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------

NAV = [
    ("index.html", "Home", False),
    ("index.html#work", "Work", False),
    ("index.html#experience", "Experience", True),
    ("contact.html", "Contact", False),
]


def head(title, description, prefix, canonical, og_image="assets/img/profile.jpg"):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="author" content="{e(SITE['name'])}">
<link rel="canonical" href="{e(BASE_URL)}/{e(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(BASE_URL)}/{e(canonical)}">
<meta property="og:image" content="{e(BASE_URL)}/{e(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}assets/img/profile-sm.jpg">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
<script>
  (function () {{
    try {{
      var t = localStorage.getItem("theme");
      if (t === "light" || t === "dark") document.documentElement.setAttribute("data-theme", t);
    }} catch (e) {{}}
  }})();
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""


def header(prefix, current):
    links = []
    for href, label, optional in NAV:
        target = prefix + href
        aria = ' aria-current="page"' if href == current else ""
        klass = ' class="is-optional"' if optional else ""
        links.append(f'<a href="{target}"{aria}{klass}>{e(label)}</a>')

    return f"""<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="nav__brand" href="{prefix}index.html">
        <img src="{prefix}assets/img/profile-sm.jpg" alt="" width="28" height="28">
        <span>{e(SITE['name'])}</span>
      </a>
      <div class="nav__links">
        {''.join(links)}
        <a href="{prefix}{e(SITE['links']['cv'])}" class="is-optional" download>CV</a>
      </div>
      <button class="theme-toggle" type="button" aria-label="Toggle colour theme">
        {ICONS['sun']}{ICONS['moon']}
      </button>
    </nav>
  </div>
</header>
"""


def footer(prefix, fab=True):
    links = SITE["links"]
    fab_html = ""
    if fab:
        fab_html = (
            f'<a class="fab" href="{prefix}contact.html" aria-label="Get in touch">'
            f"{ICONS['mail']}<span>Get in touch</span></a>\n"
        )
    return fab_html + f"""<footer class="site-footer">
  <div class="wrap">
    <span>&copy; 2026 {e(SITE['name'])}. Built as static HTML, hosted on GitHub Pages.</span>
    <span class="footer-links">
      <a href="mailto:{e(SITE['email'])}">Email</a>
      <a href="tel:{e(SITE['phone'])}">{e(SITE["phoneDisplay"])}</a>
      <a href="{e(links['linkedin'])}" rel="noopener" target="_blank">LinkedIn</a>
      <a href="{e(links['github'])}" rel="noopener" target="_blank">GitHub</a>
      <a href="{e(links['upwork'])}" rel="noopener" target="_blank">Upwork</a>
      <a href="{prefix}{e(links['cv'])}" download>CV</a>
    </span>
  </div>
</footer>
<script src="{prefix}assets/js/main.js" defer></script>
</body>
</html>
"""


def person_schema():
    payload = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": SITE["name"],
        "jobTitle": SITE["role"],
        "email": "mailto:" + SITE["email"],
        "telephone": SITE["phone"],
        "url": BASE_URL + "/",
        "image": BASE_URL + "/assets/img/profile.jpg",
        "sameAs": [SITE["links"]["linkedin"], SITE["links"]["github"], SITE["links"]["upwork"]],
        "knowsAbout": ["iOS development", "Swift", "SwiftUI", "The Composable Architecture"],
    }
    return '<script type="application/ld+json">%s</script>' % json.dumps(payload)


# --------------------------------------------------------------------------
# fragments
# --------------------------------------------------------------------------

def app_card(project, prefix):
    badge = ""
    if project["ownership"] == "own":
        badge = '<span class="badge">My app</span>'
    meta = [f"{e(project['genre'])}", f"★ {e(project['rating'])} ({e(project['ratingCount'])})"]
    return f"""<a class="app-card" href="{prefix}projects/{e(project['slug'])}.html">
  <img class="app-card__icon" src="{prefix}assets/img/icons/{e(project['slug'])}.jpg"
       alt="{e(project['name'])} app icon" width="60" height="60" loading="lazy">
  <span class="app-card__body">
    <span class="app-card__name">{e(project['name'])}{badge}</span>
    <span class="app-card__tag">{e(project['tagline'])}</span>
    <span class="app-card__meta">{'<span>' + '</span><span>'.join(meta) + '</span>'}</span>
  </span>
</a>"""


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def build_index():
    stats = "".join(
        f'<div class="stat"><div class="stat__value">{e(s["value"])}</div>'
        f'<div class="stat__label">{e(s["label"])}</div></div>'
        for s in SITE["stats"]
    )

    cards = "\n".join(app_card(p, "") for p in PROJECTS)

    jobs = []
    for job in SITE["experience"]:
        points = "".join(f"<li>{e(p)}</li>" for p in job["points"])
        link = ""
        if job.get("project"):
            link = (f' · <a href="projects/{e(job["project"])}.html">view the app</a>')
        jobs.append(f"""<article class="job">
  <div class="job__period">{e(job['period'])}</div>
  <div>
    <h3 class="job__title">{e(job['title'])}</h3>
    <p class="job__company">{e(job['company'])}{link}</p>
    <ul>{points}</ul>
  </div>
</article>""")

    skill_rows = []
    for label, values in SITE["skills"].items():
        chips = "".join('<span class="chip">%s</span>' % e(v) for v in values)
        skill_rows.append(
            '<div class="skill-row"><div class="skill-row__label">%s</div>'
            '<div class="chips">%s</div></div>' % (e(label), chips)
        )
    skills = "".join(skill_rows)

    education = "".join(
        f'<div class="card"><h3>{e(ed["school"])}</h3>'
        f'<p class="muted">{e(ed["degree"])}</p>'
        f'<p class="muted" style="font-size:.88rem">{e(ed["period"])}</p></div>'
        for ed in SITE["education"]
    )

    body = f"""{header('', 'index.html')}
<main id="main">

  <section class="hero">
    <div class="wrap hero__grid">
      <div>
        <p class="hero__role">{e(SITE['role'])}</p>
        <h1>Apps that feel<br>native, because<br>they are.</h1>
        <p class="lead">{e(SITE['tagline'])}</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="#work">See the work</a>
          <a class="btn btn--ghost" href="{e(SITE['links']['cv'])}" download>{ICONS['download']}Download CV</a>
          <a class="btn btn--ghost" href="{e(SITE['links']['github'])}" rel="noopener" target="_blank">{ICONS['github']}GitHub</a>
        </div>
      </div>
      <img class="hero__photo" src="assets/img/profile.jpg"
           alt="Portrait of {e(SITE['name'])}" width="900" height="900">
    </div>
  </section>

  <section class="wrap" style="padding-bottom:clamp(28px,4vw,48px)">
    <div class="stats reveal">{stats}</div>
  </section>

  <section class="section" id="work">
    <div class="wrap">
      <p class="eyebrow">Selected work</p>
      <h2>Shipped to the App Store</h2>
      <p class="lead" style="margin-bottom:36px">
        Apps I built or led, from fitness and social/dating platforms used by millions to tools I designed and shipped on my own.
      </p>
      <div class="app-grid reveal">
{cards}
      </div>
    </div>
  </section>

  <section class="section" id="skills">
    <div class="wrap">
      <p class="eyebrow">Toolkit</p>
      <h2>What I work with</h2>
      <div style="margin-top:28px">{skills}</div>
    </div>
  </section>

  <section class="section" id="experience">
    <div class="wrap">
      <p class="eyebrow">Experience</p>
      <h2>Fourteen years of iOS</h2>
      <div class="timeline" style="margin-top:32px">
        {''.join(jobs)}
      </div>
    </div>
  </section>

  <section class="section" id="about">
    <div class="wrap">
      <p class="eyebrow">Education</p>
      <h2>Beyond the day job</h2>
      <div class="cards" style="margin-top:28px">
        {education}
        <div class="card">
          <h3>Off the keyboard</h3>
          <p class="muted">{e(SITE['hobbies'])}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="contact">
    <div class="wrap">
      <p class="eyebrow">Open to work</p>
      <h2>Let's build something great.</h2>
      <p class="lead" style="margin-bottom:28px">
        Available for iOS contract and full-time roles. The fastest way to reach me is email.
      </p>
      <div class="hero__actions" style="margin-top:0">
        <a class="btn btn--primary" href="contact.html">{ICONS['mail']}Contact me</a>
        <a class="btn btn--ghost" href="{e(SITE['links']['whatsapp'])}" rel="noopener" target="_blank">{ICONS['whatsapp']}WhatsApp</a>
        <a class="btn btn--ghost" href="{e(SITE['links']['telegram'])}" rel="noopener" target="_blank">{ICONS['telegram']}Telegram</a>
        <a class="btn btn--ghost" href="{e(SITE['links']['linkedin'])}" rel="noopener" target="_blank">{ICONS['linkedin']}LinkedIn</a>
        <a class="btn btn--ghost" href="{e(SITE['links']['upwork'])}" rel="noopener" target="_blank">{ICONS['upwork']}Upwork</a>
      </div>
    </div>
  </section>

</main>
{person_schema()}
{footer('')}"""

    page = head(
        f"{SITE['name']} · {SITE['role']}",
        SITE["tagline"],
        "",
        "index.html",
    ) + body
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def build_project(index, project):
    prefix = "../"
    slug = project["slug"]

    facts = [
        ("Role", project["role"]),
        ("Category", project["genre"]),
        ("App Store rating", f"★ {project['rating']} · {project['ratingCount']} ratings"),
        ("On the store since", project["released"]),
        ("Published by", project["seller"]),
    ]
    if project.get("period"):
        facts.insert(1, ("Worked on", project["period"]))

    facts_html = "".join(
        f'<div class="fact"><div class="fact__label">{e(label)}</div>'
        f'<div class="fact__value">{e(value)}</div></div>'
        for label, value in facts
    )

    about = "".join(f"<p>{e(p)}</p>" for p in project["about"])
    contributions = "".join(f"<li>{e(c)}</li>" for c in project["contributions"])
    tech = "".join(f'<span class="chip">{e(t)}</span>' for t in project["tech"])
    badge = '<span class="badge">My app</span>' if project["ownership"] == "own" else \
            '<span class="badge badge--neutral">Client work</span>'

    prev_project = PROJECTS[index - 1]
    next_project = PROJECTS[(index + 1) % len(PROJECTS)]

    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": project["name"],
        "operatingSystem": "iOS",
        "applicationCategory": "MobileApplication",
        "url": project["appStoreUrl"],
        "author": {"@type": "Person", "name": SITE["name"]},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": project["rating"],
            "ratingCount": project["ratingCount"].replace(",", ""),
        },
    })

    body = f"""{header(prefix, '')}
<main id="main">
  <section class="section" style="padding-bottom:0">
    <div class="wrap">
      <a class="back-link" href="{prefix}index.html#work">{ICONS['arrow-left']}All work</a>

      <div class="project-hero">
        <img class="project-hero__icon" src="{prefix}assets/img/icons/{e(slug)}.jpg"
             alt="{e(project['name'])} app icon" width="96" height="96">
        <div class="project-hero__body">
          <p class="eyebrow" style="margin-bottom:10px">{badge}</p>
          <h1>{e(project['name'])}</h1>
          <p class="lead">{e(project['tagline'])}</p>
          <div class="hero__actions">
            <a class="btn btn--primary" href="{e(project['appStoreUrl'])}" rel="noopener" target="_blank">
              {ICONS['appstore']}View on the App Store
            </a>
          </div>
        </div>
      </div>

      <div class="facts reveal">{facts_html}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <img class="shot reveal" src="{prefix}assets/img/apps/{e(slug)}.png"
           alt="{e(project['name'])} app screenshots" loading="lazy">
    </div>
  </section>

  <section class="section">
    <div class="wrap" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:48px">
      <div>
        <p class="eyebrow">About the app</p>
        <div class="prose">{about}</div>
      </div>
      <div>
        <p class="eyebrow">What I did</p>
        <ul class="bullets">{contributions}</ul>
        <p class="eyebrow" style="margin-top:32px">Tech</p>
        <div class="chips">{tech}</div>
      </div>
    </div>
  </section>

  <section class="wrap" style="padding-bottom:64px">
    <div class="project-nav">
      <a href="{e(prev_project['slug'])}.html">&larr; {e(prev_project['name'])}</a>
      <a href="{e(next_project['slug'])}.html">{e(next_project['name'])} &rarr;</a>
    </div>
  </section>
</main>
<script type="application/ld+json">{schema}</script>
{footer(prefix)}"""

    page = head(
        f"{project['name']} · {SITE['name']}",
        project["tagline"],
        prefix,
        f"projects/{slug}.html",
        og_image=f"assets/img/apps/{slug}.png",
    ) + body

    PROJECT_DIR.mkdir(exist_ok=True)
    (PROJECT_DIR / f"{slug}.html").write_text(page, encoding="utf-8")


def build_contact():
    links = SITE["links"]
    contact_rows = [
        (ICONS["mail"], "Email", SITE["email"], f"mailto:{SITE['email']}", False),
        (ICONS["phone"], "Phone", SITE["phoneDisplay"], f"tel:{SITE['phone']}", False),
        (ICONS["whatsapp"], "WhatsApp", SITE["phoneDisplay"], links["whatsapp"], True),
        (ICONS["telegram"], "Telegram", SITE["phoneDisplay"], links["telegram"], True),
        (ICONS["linkedin"], "LinkedIn", "in/anatoli-petrosyants", links["linkedin"], True),
        (ICONS["upwork"], "Upwork", "Hire me for contract work", links["upwork"], True),
        (ICONS["github"], "GitHub", "Anatoli-Petrosyants", links["github"], True),
        (ICONS["download"], "Curriculum vitae", "PDF, one page", links["cv"], False),
    ]
    rows = "".join(
        f'<a class="contact-link" href="{e(href)}"'
        + (' rel="noopener" target="_blank"' if external else "")
        + f'>{icon}<span><strong>{e(label)}</strong><small>{e(value)}</small></span></a>'
        for icon, label, value, href, external in contact_rows
    )

    body = f"""{header('', 'contact.html')}
<main id="main">
  <section class="section">
    <div class="wrap">
      <p class="eyebrow">Contact</p>
      <h2>Tell me about the project.</h2>
      <p class="lead" style="margin-bottom:44px">
        Open to iOS contract work and full-time roles. Fill this in and it opens a
        pre-written email in your mail app. Nothing is sent to a third-party server.
        Prefer to message? WhatsApp and Telegram are on the right.
      </p>

      <div class="contact-grid">
        <form data-mailto-form="{e(SITE['email'])}" novalidate>
          <div class="field">
            <label for="name">Your name</label>
            <input id="name" name="name" type="text" autocomplete="name" required>
            <span class="error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="email">Your email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
            <span class="error" aria-live="polite"></span>
          </div>
          <div class="field">
            <label for="message">Message</label>
            <textarea id="message" name="message" rows="7" required></textarea>
            <span class="error" aria-live="polite"></span>
          </div>
          <button class="btn btn--primary" type="submit">{ICONS['mail']}Open email draft</button>
          <p class="form-note" data-form-status aria-live="polite">
            No mail app? Write to <a href="mailto:{e(SITE['email'])}">{e(SITE['email'])}</a> directly.
          </p>
        </form>

        <div>
          <p class="eyebrow">Elsewhere</p>
          <div class="contact-links">{rows}</div>
        </div>
      </div>
    </div>
  </section>
</main>
{footer('', fab=False)}"""

    page = head(
        f"Contact · {SITE['name']}",
        f"Get in touch with {SITE['name']}, {SITE['role'].lower()} open to contract and full-time work.",
        "",
        "contact.html",
    ) + body
    (ROOT / "contact.html").write_text(page, encoding="utf-8")


def build_404():
    body = f"""{header('', '')}
<main id="main">
  <section class="section" style="text-align:center">
    <div class="wrap">
      <p class="eyebrow">404</p>
      <h2>This page does not exist.</h2>
      <p class="lead" style="margin:16px auto 32px">
        The link is broken or the page moved. The work is all one click away.
      </p>
      <a class="btn btn--primary" href="{e(BASE_URL)}/index.html">Back to home</a>
    </div>
  </section>
</main>
{footer('')}"""
    page = head(f"Page not found · {SITE['name']}", "Page not found.", "", "404.html") + body
    (ROOT / "404.html").write_text(page, encoding="utf-8")


def build_sitemap():
    urls = ["index.html", "contact.html"] + [f"projects/{p['slug']}.html" for p in PROJECTS]
    entries = "".join(f"  <url><loc>{BASE_URL}/{u}</loc></url>\n" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8"
    )


def main():
    build_index()
    build_contact()
    for index, project in enumerate(PROJECTS):
        build_project(index, project)
    build_404()
    build_sitemap()
    print(f"built: index.html, contact.html, 404.html, {len(PROJECTS)} project pages, sitemap.xml, robots.txt")


if __name__ == "__main__":
    sys.exit(main())
