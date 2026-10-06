# movusgames.com

The public site for Movus. Static pages, no build step at serve time, no
dependencies.

- `index.html`   — landing page
- `privacy.html` — the App Store **Privacy Policy URL** (mandatory)
- `support.html` — the App Store **Support URL** (mandatory)
- `CNAME`        — the custom domain, for GitHub Pages
- `games/`, `guides/`, `how-it-works/`, `faq/` and `sitemap.xml` — **written
  by `python3 tools/build-pages.py`**, which holds their content and shares one
  header, footer and head across them. Edit the script, run it, commit the
  output. Game numbers (MET, kcal per 10 min) come from the app's
  `Workout.met` and its calorie formula; keep them in step.
- `img/` — written by `python3 tools/make-images.py` from the app repo's App
  Store screenshots and card art.

Source of truth lives in the app repo under `site/`; this repo is the
deployment. Copy the folder over and push.

## Changing the stylesheet

`style.css` is served with `Cache-Control: max-age=14400` and the pages that
reference it with `max-age=600`, so a browser picks up new **HTML** after ten
minutes and keeps the old **CSS** for up to four hours. New page, old
stylesheet — which renders as an unstyled document with a dark background,
and is exactly what the owner saw the first time this site was redesigned.

**So the link carries a version: `style.css?v=N`. Bump N in all three pages
whenever `style.css` changes.** A different URL cannot be answered from a
cache that has never seen it, which is the only fix that does not depend on
anybody purging anything.

Images do not need this — every one of them is a new filename.
