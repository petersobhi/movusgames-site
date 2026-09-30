"""Rebuild the site's images from the app repo's own screenshots.

The site has no build step and it does have a hundred and thirty image files,
which until now were made by hand — so the first re-shoot after a graphics
pass had no recipe to follow and the question "where did shot-body come from"
had no answer in either repo. This is that answer, and it is the whole of it:

  shot-<name>   <- Tools/AppStore/screenshots/iphone-6.9/<NN>-<name>.png
  card-<game>   <- MoveGame/Resources/CardArt/cardart-<v>-<game>-574x700.png

Every image ships as AVIF and WebP at three widths with a JPEG last resort,
because `index.html` offers all three in a <picture> with a srcset. Nothing
here is cropped: the App Store screenshot and the hub card are already
composed, and a second crop is a second place for the composition to drift.

    python3 tools/make-images.py                # everything
    python3 tools/make-images.py shot-body card-runner

Needs Pillow 11.3+, which writes AVIF without a plugin.
"""
import os, re, sys, glob
from PIL import Image

APP = os.path.expanduser("~/Work/MoveGame")
IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")

# The nine App Store screenshots, by the name the site calls them.
SHOTS = {"body": "01-body", "hub": "02-hub", "keeper": "03-keeper",
         "swim": "04-swim", "slash": "05-slash", "boxing": "06-boxing",
         "squats": "07-squats", "progress": "08-progress",
         "privacy": "09-privacy"}

CARDS = ["runner", "keeper", "swim", "slash", "boxing", "squats",
         "dance", "downhill", "hula", "skyfall"]

# Widths, and the quality each format is carrying. Measured against what was
# already in `img/` rather than chosen: a 1400px AVIF lands within a couple of
# KB of the 40.7KB the hand-made one was, so a regenerated file does not
# quietly change the page weight the performance pass measured.
SHOT_WIDTHS, CARD_WIDTHS = (700, 1000, 1400), (400, 550, 700)
AVIF_Q, WEBP_Q, JPEG_Q = 55, 78, 82


def card_source(game):
    v = sorted(glob.glob(f"{APP}/MoveGame/Resources/CardArt/cardart-v*-{game}-574x700.png"))
    if not v:
        return None
    # Highest artVersion, numerically — v9 must not beat v17.
    return max(v, key=lambda p: int(re.search(r"cardart-v(\d+)-", p).group(1)))


def emit(src, stem, widths, jpeg_width):
    im = Image.open(src).convert("RGB")
    for w in widths:
        h = round(im.height * w / im.width)
        r = im.resize((w, h), Image.LANCZOS)
        r.save(f"{IMG}/{stem}-{w}.avif", quality=AVIF_Q)
        r.save(f"{IMG}/{stem}-{w}.webp", quality=WEBP_Q, method=6)
    jh = round(im.height * jpeg_width / im.width)
    im.resize((jpeg_width, jh), Image.LANCZOS).save(
        f"{IMG}/{stem}.jpg", quality=JPEG_Q, optimize=True, progressive=True)
    total = sum(os.path.getsize(f"{IMG}/{stem}-{w}.{e}")
                for w in widths for e in ("avif", "webp"))
    print(f"  {stem:16} {im.width}x{im.height} -> "
          f"{total // 1024}KB in {len(widths) * 2} files + jpeg")


def main(only):
    jobs = {}
    for name, shot in SHOTS.items():
        jobs[f"shot-{name}"] = (
            f"{APP}/Tools/AppStore/screenshots/iphone-6.9/{shot}.png",
            SHOT_WIDTHS, 1400)
    for game in CARDS:
        jobs[f"card-{game}"] = (card_source(game), CARD_WIDTHS, 330)

    wanted = {k: v for k, v in jobs.items() if not only or k in only}
    if only:
        unknown = set(only) - set(jobs)
        if unknown:
            raise SystemExit(f"unknown: {', '.join(sorted(unknown))}\n"
                             f"known: {', '.join(sorted(jobs))}")
    missing = [k for k, (s, _, _) in wanted.items() if not s or not os.path.exists(s)]
    if missing:
        raise SystemExit("no source for: " + ", ".join(sorted(missing)))
    for stem, (src, widths, jw) in sorted(wanted.items()):
        emit(src, stem, widths, jw)


if __name__ == "__main__":
    main(set(sys.argv[1:]))
