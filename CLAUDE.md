# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static portfolio site for an iOS developer, served by GitHub Pages on the
custom domain `https://anatolipetrosyants.dev/`. Plain HTML/CSS/JS — no npm,
no bundler, no framework, no runtime dependencies. Python 3 stdlib only.

## Commands

```sh
python3 build.py                 # regenerate all HTML from data/*.json
python3 fetch_screenshots.py     # refresh assets/img/shots/<slug>/ from the App Store
python3 -m http.server 8000      # local preview at http://localhost:8000
```

There is no test suite, linter or CI. The only correctness check that matters is
that `build.py` runs clean and no local link 404s.

## Architecture

The critical thing to understand: **the HTML files are build output, committed to
the repo.** GitHub Pages serves files verbatim and never runs `build.py`, so
generated HTML must be regenerated and committed alongside any data or template
change. Editing `index.html`, `contact.html`, `404.html` or `projects/*.html`
directly is always wrong — the next `python3 build.py` silently overwrites it.

Three layers:

1. **`data/site.json`** — everything about the person: bio, `stats`, `skills`
   (an ordered map of category to tag list), `experience`, `education`,
   `experiments`, social `links`, and `baseUrl`.
2. **`data/projects.json`** — an array of App Store apps, ordered as they appear
   in the home grid. Each entry's `slug` is the contract that ties four things
   together: the page path `projects/<slug>.html`, the icon
   `assets/img/icons/<slug>.jpg`, the wide collage `assets/img/apps/<slug>.jpg`
   and the per-screen gallery folder `assets/img/shots/<slug>/`.
   Rename a slug and all four must move.
3. **`build.py`** — templates as Python functions. `head()`, `header()`,
   `footer()` build shared chrome; `build_index()`, `build_project()`,
   `build_contact_redirect()`, `build_404()` build pages; `build_sitemap()` writes
   `sitemap.xml` and `robots.txt`.

### Path prefixes

Every link in the site is relative, so the site works both at a repo subpath and
at a domain root. Template functions take a `prefix` argument that is `""` for
root-level pages and `"../"` for pages in `projects/`. Any new markup that
references an asset must thread that prefix through, or the project pages break
while the home page keeps working — an easy failure to miss.

`baseUrl` in `site.json` is the single source of truth for the domain. It drives
the generated `CNAME` file that GitHub Pages reads, plus every absolute URL that
has to be absolute: `<link rel="canonical">`, Open Graph and Twitter tags,
JSON-LD and the sitemap. Changing it and rebuilding is all a domain move takes.

The home page's canonical is the bare domain, so `head()` is called with an empty
`canonical` and the nav links to `./` rather than `index.html` — two URL forms for
the same page is exactly what the canonical is there to prevent. `link()` handles
that resolution; use it instead of concatenating a prefix onto a nav href.

### Python version constraint

The local interpreter is Python 3.9. Nested same-quote f-strings and backslashes
inside f-string expressions are syntax errors there. Build long HTML fragments in
an explicit loop with `%`-formatting rather than cramming a `"".join(...)`
comprehension into an f-string.

Everything user-facing goes through `e()` (an `html.escape` wrapper) before it
lands in markup.

### SEO invariants

These are easy to break silently, so check them after touching `head()` or the
page builders:

- Every page has a unique `<title>` and `<meta name="description">`.
- `404.html` and the `contact.html` redirect stub are the only noindexed pages.
- Every `<img>` carries `width` and `height`. Project screenshots get theirs from
  `image_size()`, which parses PNG and JPEG headers directly — without them the
  page reflows as images load and Cumulative Layout Shift suffers.
- The hero portrait is the LCP element: it is preloaded and marked
  `fetchpriority="high"`, and must not be given `loading="lazy"`.
- JSON-LD goes through `ld()`. The home page emits `Person`, `WebSite` and an
  `ItemList`; project pages emit `SoftwareApplication` and a `BreadcrumbList`.
  Validate changes at https://validator.schema.org/.

### Styling

One stylesheet, `assets/css/style.css`, driven by CSS custom properties on
`:root`. Dark is the default palette; light is defined twice — once under
`html[data-theme="light"]` for the explicit toggle and once under
`@media (prefers-color-scheme: light)` scoped to `html:not([data-theme="dark"])`
so the system preference applies only when the user has not chosen. Adding a
color means adding it to all three blocks. A blocking inline script in `head()`
reads `localStorage.theme` before first paint to avoid a flash.

### JavaScript

`assets/js/main.js` is one IIFE, no modules, loaded with `defer`. It does three
things: theme toggle, `IntersectionObserver` scroll reveal for `.reveal`
elements, and the contact form. The form is wired by the `data-mailto-form`
attribute whose value is the destination address; it validates client-side and
then sets `window.location.href` to a `mailto:` URL. Nothing is posted to a
server — that is deliberate, since GitHub Pages is static-only.

## Content sourcing

App metadata (rating, rating count, category, release year, minimum iOS version,
icon artwork) comes from the public iTunes lookup API and should be refreshed
from there rather than typed by hand:

```sh
curl -s "https://itunes.apple.com/lookup?id=<appStoreId>&country=us"
```

Icons are downloaded from the `artworkUrl512` field in that response.

Project pages show a horizontal screenshot gallery built from
`assets/img/shots/<slug>/NN.jpg`, one file per App Store screenshot in store
order. `fetch_screenshots.py` writes those: it reads the App Store id out of
each project's `appStoreUrl`, pulls `screenshotUrls` from the same lookup API
and re-requests each image at 540px wide (the mzstatic thumb URL takes any
`<width>x0w.jpg` suffix). It wipes the folder first, so removing a screenshot on
the App Store removes it from the site. `build.py` reads whatever files are
there — delete the folder and the page falls back to the single wide collage.

The collage in `assets/img/apps/<slug>.jpg` is still the `og:image` for the
project page, since a wide image is what a social card wants.

Screenshot collages are resized to 1400px wide and then converted to JPEG, which
cut them from roughly 1 MB each to 250 KB with no visible loss — the source PNGs
carried an alpha channel that was fully opaque:

```sh
sips -Z 1400 source.png --out tmp.png
sips -s format jpeg -s formatOptions 82 tmp.png --out assets/img/apps/<slug>.jpg
```

There is no WebP encoder on this machine (`sips` cannot write it, and `cwebp` and
ImageMagick are not installed), so JPEG is the smallest format available without
adding a dependency.

## Deployment

Push to `main`; GitHub Pages is configured to deploy from the branch root.
`.nojekyll` at the root stops Jekyll from processing the output, and `CNAME`
points the custom domain at it. HTTPS is mandatory rather than optional here: the
`.dev` TLD is on the HSTS preload list, so the site will not load over plain HTTP.
