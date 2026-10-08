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
- `pose.js` — the tracked figure in the home page's viewfinder. Its
  proportions are the same Drillis & Contini segment table the app's own
  harness uses (`MoveGame/Dev/PoseBody.swift`) and its limbs are placed the
  same way the rig places them, from a direction and a reach, so the figure
  on the site is literally the body the detector is tested against. The
  poses it cycles are the signals the detector reads. It is the only
  animation on the site; keep it that way.

Source of truth lives in the app repo under `site/`; this repo is the
deployment. Copy the folder over and push.

## The design

`style.css` opens with the plan — colour, type, layout and motion — and the
short version is: **one ground, one accent, three type voices, and no cards.**
The sheet it replaced spent crimson, cyan and gold on decoration and then had
no colour left to point with, and every section was the same
kicker → heading → three-rounded-cards block, which is what the owner meant
by "AI slop". If you add a section, give it a shape the page does not already
have.

Numbers, specs and labels are set in monospace. That is not a texture: this
product makes measured claims, so its data is set as data.

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
