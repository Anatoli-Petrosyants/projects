# Portfolio — Anatoli Petrosyants

Static portfolio site for an iOS developer, hosted on GitHub Pages.
No frameworks, no npm, no build toolchain — plain HTML, CSS and vanilla JavaScript,
generated from two JSON files by a small Python script.

**Live site:** https://anatoli-petrosyants.github.io/projects/

## Structure

```
data/site.json          Bio, stats, skills, experience, education, links
data/projects.json      One entry per App Store app
build.py                Generator: JSON + templates -> HTML
assets/css/style.css    Single stylesheet (dark by default, light theme supported)
assets/js/main.js       Theme toggle, scroll reveal, contact-form mailto builder
assets/img/icons/       512px App Store icons, used on cards
assets/img/apps/        Screenshot collages, used on project pages
assets/files/           CV (PDF)
index.html              Generated
contact.html            Generated
404.html                Generated
projects/*.html         Generated, one per app
sitemap.xml robots.txt  Generated
```

Everything at the repo root except `data/`, `build.py` and `assets/` is generated
output. It is committed on purpose — GitHub Pages serves the files directly and
never runs the build.

## Editing

Change content in `data/site.json` or `data/projects.json`, then regenerate:

```sh
python3 build.py
```

Do not hand-edit the generated `.html` files; the next build overwrites them.
Layout and markup changes belong in the template functions inside `build.py`,
styling in `assets/css/style.css`.

### Adding a new app

1. Add an object to `data/projects.json`.
2. Drop a 512px icon at `assets/img/icons/<slug>.jpg` and a screenshot image at
   `assets/img/apps/<slug>.png`. App Store metadata and the icon URL come from
   `https://itunes.apple.com/lookup?id=<appStoreId>&country=us`.
3. Run `python3 build.py`.

## Local preview

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploying

Push to `main`. In the repository settings, under **Pages**, set the source to
**Deploy from a branch**, branch `main`, folder `/ (root)`.

`.nojekyll` is present so GitHub Pages serves the files as-is instead of running
them through Jekyll.

If the repository is ever renamed or moved to a custom domain, update `baseUrl`
in `data/site.json` and rebuild — it drives the canonical URLs, Open Graph tags
and the sitemap. All in-page links are relative, so they keep working either way.

## Contact form

The form on `contact.html` does not post anywhere. It validates the input and
opens a pre-filled `mailto:` draft in the visitor's mail client. That keeps the
site fully static with no third-party form service. To switch to a hosted
endpoint later (Formspree, Web3Forms), give the `<form>` a real `action` and drop
the `data-mailto-form` attribute that `assets/js/main.js` hooks into.
