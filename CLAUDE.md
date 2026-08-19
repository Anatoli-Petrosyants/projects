# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A static portfolio site for an iOS developer, served by GitHub Pages at
`https://anatoli-petrosyants.github.io/projects/`. Plain HTML/CSS/JS — no npm,
no bundler, no framework, no runtime dependencies. Python 3 stdlib only.

## Commands

```sh
python3 build.py                 # regenerate all HTML from data/*.json
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
   in the home grid. Each entry's `slug` is the contract that ties three things
   together: the page path `projects/<slug>.html`, the icon
   `assets/img/icons/<slug>.jpg`, and the screenshot `assets/img/apps/<slug>.png`.
   Rename a slug and all three must move.
3. **`build.py`** — templates as Python functions. `head()`, `header()`,
   `footer()` build shared chrome; `build_index()`, `build_project()`,
   `build_contact()`, `build_404()` build pages; `build_sitemap()` writes
   `sitemap.xml` and `robots.txt`.

### Path prefixes

Every link in the site is relative, so the site works both at a repo subpath and
at a domain root. Template functions take a `prefix` argument that is `""` for
root-level pages and `"../"` for pages in `projects/`. Any new markup that
references an asset must thread that prefix through, or the project pages break
while the home page keeps working — an easy failure to miss.

`baseUrl` in `site.json` is used only for absolute URLs that must be absolute:
`<link rel="canonical">`, Open Graph tags, JSON-LD and the sitemap. Change it if
the repo is renamed or a custom domain is added.

### Python version constraint

The local interpreter is Python 3.9. Nested same-quote f-strings and backslashes
inside f-string expressions are syntax errors there. Build long HTML fragments in
an explicit loop with `%`-formatting rather than cramming a `"".join(...)`
comprehension into an f-string.

Everything user-facing goes through `e()` (an `html.escape` wrapper) before it
lands in markup.

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
Screenshot collages are resized locally with `sips -Z 1400`.

## Deployment

Push to `main`; GitHub Pages is configured to deploy from the branch root.
`.nojekyll` at the root stops Jekyll from processing the output.
