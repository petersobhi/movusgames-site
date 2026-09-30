# movusgames.com

The public site for Movus. Three static pages, no build step, no dependencies.

- `index.html`   — landing page
- `privacy.html` — the App Store **Privacy Policy URL** (mandatory)
- `support.html` — the App Store **Support URL** (mandatory)
- `CNAME`        — the custom domain, for GitHub Pages

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
