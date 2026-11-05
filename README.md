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

This repo is the source of truth and the deployment: pushing to `main`
publishes it through GitHub Pages.

## The page's job is the App Store, and it looks like the app

The site should look like the thing you are about to download. `style.css` is the
app's design system on a web page: its values are read off `DesignSystem.swift`,
`Components.swift` and `GameTile` in the app repo, night theme. Outfit only, uppercase
Black for titles, its game tiles, chips, panels and backdrop.

Keep the home page short: headline, badge and the reel; the six tiles; three steps; the
badge again.

- **The one button is Apple's "Download on the App Store" badge**, hotlinked as their
  marketing toolbox serves it. Never recolour or reshape it. Every page has it in the header
  and the closing panel, plus iOS Safari's Smart App Banner (`apple-itunes-app`). On a
  computer a QR code stands beside the big one.
- The link is `https://apps.apple.com/app/id6808390249`, with no country in it, so Apple
  sends each visitor to their own storefront. It is `APP` in `tools/build-pages.py`, and
  written out by hand in `index.html`, `privacy.html`, `support.html` and `404.html`.
  Change them together, and if the URL ever changes, regenerate the QR code.
- **The hero is real footage from the store build**: `img/reel.mp4`, recipe and warnings in
  `tools/make-reel.sh`. `reel.js` makes the phone's glow and the highlighted name follow it.
  Re-record it when a game changes, and do not show a character the store build does not have.
- There is no analytics on this site. App Store Connect's App Analytics lists it under the
  **Web Referrer** source, which is why these links open in the same tab and never carry
  `rel=noreferrer`.

## Changing the stylesheet

`style.css` is served with `Cache-Control: max-age=14400` and the pages that
reference it with `max-age=600`, so a browser picks up new **HTML** after ten
minutes and keeps the old **CSS** for up to four hours. New page, old
stylesheet — which renders as an unstyled document with a dark background,
and is exactly what the owner saw the first time this site was redesigned.

**So the link carries a version: `style.css?v=N`. Bump N in `index.html`,
`privacy.html`, `support.html`, `404.html` and `CSS` in `tools/build-pages.py`
whenever `style.css` changes.** A different URL cannot be answered from a
cache that has never seen it, which is the only fix that does not depend on
anybody purging anything.

Images do not need this — every one of them is a new filename.
