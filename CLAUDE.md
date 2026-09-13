# noahschouela.com

Quarto site for https://noahschouela.com, published by GitHub Pages from
`docs/`. Migrated from WordPress.com on 2026-09-13.

## The loop

```bash
# edit the .qmd sources, then
quarto render
```

**Never hand-edit `docs/`.** It is build output *and* it is tracked in git,
because GitHub Pages serves from it — so it must be committed alongside the
sources, but `quarto render` overwrites it wholesale. Sources are:

| File | Page |
|---|---|
| `index.qmd` | About (`/`) |
| `research/index.qmd` | Research |
| `cv/index.qmd` | CV |
| `styles.css` | all |
| `_quarto.yml` | site config, PT Sans font link |

`tidy-urls.py` runs post-render: rewrites the sitemap to directory URLs and
adds canonical tags. Leave it alone unless URLs change.

## Previewing

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory docs
```

**Caveat that will waste your time otherwise:** Python's `http.server` sends
`Last-Modified` and answers `304 Not Modified`, so the browser serves stale CSS
and edits appear not to have landed. Hard-reload, or use a handler that deletes
`If-Modified-Since` and `If-None-Match` from the *request* — suppressing the
response header does not work, because `SimpleHTTPRequestHandler` decides the
304 inside `send_head()` before any response header is written.

To check layout, screenshot rather than reason about CSS:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=6000 \
  --window-size=1440,1400 --screenshot=out.png http://localhost:8000/
```

## Design

Carried over from the previous WordPress site (Hever theme) so the migration is
not a visible break: **PT Sans** throughout, links **#1279BE**, headshot with a
20px radius, "Welcome!" as the home heading. Keep new work consistent with that.

## Things that look wrong but are not

- **`main.content.page-full { grid-column: screen-start / screen-end }`** in
  `styles.css` is load-bearing. On `page-layout: full`, Quarto puts
  `.column-body` on `<main>`, pinning it to the grid track
  `minmax(500px, calc(850px - 3em))` ~= 802px. A grid track is a hard cap that
  `max-width` cannot lift. Removing this rule silently re-narrows the CV page.
- **`body-classes` in page YAML is silently ignored** by this Quarto version —
  it renders `<body class="nav-fixed">` regardless. Target Quarto's own
  `page-full` / `column-page` classes instead.
- **The Pearson Institute is deliberately unlinked** in `index.qmd`:
  `thepearsoninstitute.org` does not resolve and the Harris path 404s.

## Images

Any replacement headshot must have its EXIF orientation checked and baked in.
The 2026 candidate was encoded landscape and relied on EXIF orientation 8 to
display upright; link-preview scrapers ignore that and would have shown it
sideways. Resize, bake the rotation into the pixels, strip EXIF, keep it under
~150KB. The live file is already clean.

## Updating the CV

Two repos. Source lives in the **private** `career-docs` repo:

1. Edit `~/Documents/Technical/GitHub/career-docs/academic-cv/cv_schouela.qmd`
2. `quarto render` there
3. Copy the PDF into `assets/` here under a new dated filename
4. Update the link and the "Last updated" line in `cv/index.qmd`
5. `quarto render` here

Never copy CV *sources* into this repo — it is public, and the retired
`cv.tex` in `career-docs` history carries a former address and phone number.

## Conventions

- **Noah makes all commits and pushes.** Stage the work and hand over a commit
  message; `git commit` and `git push` are denied in settings.
- `_private/` is gitignored and holds DNS rollback values and migration notes.
  This repo is public — nothing sensitive outside `_private/`.
