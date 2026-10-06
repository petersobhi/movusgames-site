"""Write the site's content pages: one per game, the guides, How it works and
the FAQ, plus the sitemap.

The site still has no build step at serve time — this writes plain HTML that
is committed, exactly as `make-images.py` writes plain images. It exists so
that twenty pages share one header, one footer and one set of head tags
rather than twenty hand-edited copies that drift.

    python3 tools/build-pages.py

Every page lives in its own folder as `index.html`, so its address has no
extension (`/games/move-rush/`), and every asset is linked from the root.

**Numbers on these pages come from the app, not from marketing.** The
intensity of each game is its `Workout.met` value; the calorie figure is the
app's own formula, (MET − 1) × resting metabolism (Mifflin–St Jeor), for a
stated reference adult. Change a MET in the app and change it here.
"""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://movusgames.com"
CSS = "/style.css?v=5"
TODAY = datetime.date.today().isoformat()

# --------------------------------------------------------------- reference
# A 35-year-old, 170cm, 70kg adult, with the sex constant at the midpoint of
# Mifflin–St Jeor's two (the app's own fallback for "not specified").
REF_RMR_PER_MIN = (10 * 70 + 6.25 * 170 - 5 * 35 - 78) / 1440


def kcal10(met):
    return round((met - 1) * REF_RMR_PER_MIN * 10)


# ------------------------------------------------------------------- games
GAMES = [
    dict(slug="move-rush", id="runner", name="Move Rush", shot="body", card="runner",
         met=8.5, accent="#ff8a3d",
         title="Move Rush — an endless runner you play by running",
         short="An endless runner through a dusk city. Step left and right to change lane, jump the barriers, squat under the gantries.",
         lede="An endless runner through a toy city at dusk, played with your whole body. Step across to change lanes, jump the red barriers, squat under the blue gantries — and keep going as the street speeds up.",
         moves=[("Step left or right", "One step across your room moves the runner one lane. The camera reads where your body is standing, not a swipe."),
                ("Jump", "Both feet off the floor clears a red barrier — and the arcs of coins that sit over them."),
                ("Squat", "Get low to slide under a blue gantry. The runner folds the moment you do.")],
         works="Legs and glutes from every squat and jump, calves from the landings, and your heart rate from never quite stopping.",
         tips=["Stand in the middle of your space before the run starts — that is the centre lane.",
               "A step, not a lean: move your feet so your whole body travels.",
               "Coins high in an arc need a jump. Time it over the barrier and you get both.",
               "You have six hearts. A crash costs one and gives you a moment to recover."],
         faq=[("Do I need a treadmill or to run on the spot?", "No. The street runs by itself; you only move to change lane, jump or squat. Most players end up bouncing on their toes anyway."),
              ("How much space does Move Rush need?", "About two metres side to side so you can step a lane each way, and two to three metres back from the phone so your whole body is in frame."),
              ("Is there a two-player mode?", "Not yet. Two-player is held back until it has been tested properly with two people in front of one camera.")]),
    dict(slug="penalty-hero", id="keeper", name="Penalty Hero", shot="keeper", card="keeper",
         met=6.0, accent="#bc76f5",
         title="Penalty Hero — a goalkeeper game you play with your hands",
         short="Stand in goal and save penalties with your own hands. Reach high, reach wide, get low — every save is a real dive.",
         lede="You are the goalkeeper. Penalties come in high, wide and low, and you save them with your own hands — reach for the top corner, throw an arm out to the side, get down for the low ones. The crowd lets you know how you did.",
         moves=[("Reach", "Throw a hand at the ball. Your keeper's glove goes exactly where yours does."),
                ("Go low", "Reach down, or step across so the ball is straight at you."),
                ("Step across", "Move your body to cover the side the striker is aiming for.")],
         works="Shoulders and arms from the reaches, legs and core from getting low and moving across the goal in short, explosive bursts.",
         tips=["Watch the striker, not the ball's first metre — the run-up gives the side away.",
               "A straight arm reaches further than a bent one.",
               "Balls aimed at your body are saved by standing in the way.",
               "Shots get faster as you go; three goals and the match is over."],
         faq=[("Do I need to dive on the floor?", "No. A save is judged on where your hands are, so reaching and stepping is enough. Nobody needs to land on a living-room floor."),
              ("Can I save with my feet?", "No — hands only. Feet are the first thing a camera loses in a normal room, so a save that depended on them would be luck."),
              ("Is it good exercise?", "It is intermittent: short, explosive reaches with a breath between shots. About %d kcal in ten minutes for a 70 kg adult.")]),
    dict(slug="swim", id="swim", name="Swim", shot="swim", card="swim",
         met=6.8, accent="#4dd1f2",
         title="Swim — a front-crawl race you swim standing up",
         short="Race three lanes to the wall with a real front-crawl stroke. Reach over, pull through, and keep the rhythm.",
         lede="A swimming race you do standing in your living room. Swim front crawl with your arms — reach over, catch, pull through — and race three swimmers to the wall. Rhythm wins: alternate arms and keep the stroke long.",
         moves=[("Reach over", "Bring one arm over your head and forward, like the recovery of a real stroke."),
                ("Pull through", "Sweep it down past your hip. The game reads the fall of each hand, not its height."),
                ("Alternate", "Left, right, left. Two strokes on the same arm count for half.")],
         works="Shoulders, upper back and arms through a full range of motion, with your core holding you steady — the arms of front crawl without the water.",
         tips=["Long strokes beat fast ones: flailing earns nothing.",
               "Keep a steady beat — the game counts your stroke rate and rewards rhythm.",
               "Stand side-on to nothing: face the phone squarely so it can see both arms.",
               "Finish strong — the last length is where places change."],
         faq=[("Does it work if I can't swim?", "Yes. It reads the arm movement of front crawl; there is no water and nothing to learn except the rhythm."),
              ("Is it hard on the shoulders?", "It takes your arms through a full overhead range for the length of a race. Go at your own pace and stop if anything hurts."),
              ("How long is a race?", "Under a minute for a quick swimmer — long enough to feel it, short enough to go again.")]),
    dict(slug="slash", id="slash", name="Slash", shot="slash", card="slash",
         met=7.8, accent="#f257c4",
         title="Slash — cut flying fruit with your hands",
         short="Your hands are blades. Swipe through fruit thrown over a rooftop at sunset — and leave the bombs alone.",
         lede="Fruit flies up over a city rooftop and your hands are the blades. Swipe through it in mid-air, chain cuts for combos, and keep your hands off the bombs. Both hands, all the time.",
         moves=[("Swipe", "Move a hand fast through a fruit to cut it. Either hand, any direction."),
                ("Combo", "Cut several in one sweep for a bigger score."),
                ("Avoid", "A bomb costs a life. Pull your hands away when one goes up.")],
         works="Continuous two-arm swinging works your shoulders and arms, and twisting to reach works your core. It is one of the most intense games in the app.",
         tips=["Use both hands — one per side of the screen.",
               "Big sweeping cuts score combos; small flicks miss.",
               "Watch the top of the arc: that is where fruit is slowest.",
               "You can play it standing close, or even sitting, as long as your hands are in frame."],
         faq=[("Can I play Slash sitting down?", "Yes. Slash only reads your hands, so it works seated as long as the camera can see them."),
              ("What happens if I hit a bomb?", "You lose a life. You have six."),
              ("Is it a good workout?", "Yes — continuous arm work at a high rate. About %d kcal in ten minutes for a 70 kg adult.")]),
    dict(slug="squat-rush", id="squats", name="Squat Rush", shot="squats", card="squats",
         met=8.0, accent="#9adb3e",
         title="Squat Rush — dodge balls by squatting",
         short="Three machines fire balls at your head. Squat under every one. A leg workout that does not feel like one.",
         lede="Three pitching machines in a park take aim at you, and the only way out of the way is down. Squat under every ball, come back up, and keep your three hearts as the volleys speed up.",
         moves=[("Squat", "Bend your knees and get low until the ball passes. Hold it long enough to clear it."),
                ("Stand", "Come back up between balls — every one is a full repetition."),
                ("Watch the lamps", "A machine lights up before it fires, so you know which one is next.")],
         works="Quads, glutes and hamstrings with every squat, and your heart rate from the pace. It is a bodyweight squat workout in disguise.",
         tips=["Push your hips back as you squat, like sitting into a chair.",
               "Keep your chest up so the camera reads your height clearly.",
               "Two machines can fire at once — the lamps tell you.",
               "Squat for every ball, even the ones you think will miss."],
         faq=[("How many squats is a game?", "It depends how long you last — the app counts every one and shows the total at the end."),
              ("Is it suitable for beginners?", "Yes. Squat as deep as is comfortable; the game only needs your head to get under the ball."),
              ("How many calories does it burn?", "About %d kcal in ten minutes for a 70 kg adult — repeated bodyweight squats add up fast.")]),
    dict(slug="boxing", id="boxing", name="Boxing", shot="boxing", card="boxing",
         met=7.8, accent="#f24d57",
         title="Boxing — a first-person fight you throw real punches in",
         short="First-person boxing. Throw real punches, slip his jab, and land the counter. A new opponent every fight.",
         lede="A first-person fight in a floodlit ring. Your fists are on screen, and they go where yours go — throw real punches, lean out of the way of his, duck the high ones, and come back over the top. Every fight is a new opponent.",
         moves=[("Punch", "Throw straight punches with either hand. A clean shot to the head does the most damage."),
                ("Lean", "Lean away when he winds up — his shoulder tells you which side the punch is coming from."),
                ("Duck", "Get under the high punches.")],
         works="Shoulders, arms and core from punching, and legs from slipping and ducking — the shape of a real pad session.",
         tips=["Keep your hands up between punches — it is faster to throw from a guard.",
               "Watch his wind-up: it shows the side the punch is coming from.",
               "Punch when he is open, right after he throws.",
               "Snap the punch back. A punch lands when your fist stops."],
         faq=[("Do I need gloves or a bag?", "No. Your hands are read by the camera; there is nothing to hit but the air."),
              ("Is the opponent the same every time?", "No — every fight deals a new opponent with a different look and kit."),
              ("How hard is it as a workout?", "About %d kcal in ten minutes for a 70 kg adult, with your arms working the whole round.")]),
]

for g in GAMES:
    g["kcal"] = kcal10(g["met"])
    g["faq"] = [(q, a % g["kcal"] if "%d" in a else a) for q, a in g["faq"]]

# ------------------------------------------------------------------ guides
GUIDES = [
    dict(slug="home-workout-games",
         title="Home workout games you play with your body",
         h1="Home workout games you play with your whole body",
         desc="How camera-controlled fitness games work, what they are good for, and how to get a real workout out of them at home with no equipment.",
         body="""
<p class="lede">The best home workout is the one you actually do. Games that read your
body through a camera turn exercise into something you play — and because the
controller is your body, every move counts.</p>

<h2>What is a body-controlled game?</h2>
<p>A body-controlled game uses a camera to read your posture and movement and turns
it into input. Instead of pressing a button to jump, you jump. Instead of swiping to
change lane, you step across your room. Movus does this with the iPhone's front
camera: the phone sits a few metres away and reads where your body, hands and feet
are many times a second.</p>

<h2>Why games work better than routines for many people</h2>
<ul>
  <li><b>Attention goes on the goal, not the effort.</b> You squat because a ball is
      coming, not because a timer says so.</li>
  <li><b>Short sessions are natural.</b> A run or a match lasts one to three minutes,
      which is easy to fit in and easy to repeat.</li>
  <li><b>Progress is visible.</b> Scores, streaks and personal bests make it obvious
      when you are getting better.</li>
</ul>

<h2>What each kind of game works</h2>
<table>
  <tr><th>Game</th><th>Main movement</th><th>Mostly works</th></tr>
  <tr><td><a href="/games/move-rush/">Move Rush</a></td><td>Jumps, squats, side-steps</td><td>Legs, cardio</td></tr>
  <tr><td><a href="/games/squat-rush/">Squat Rush</a></td><td>Repeated squats</td><td>Quads, glutes</td></tr>
  <tr><td><a href="/games/boxing/">Boxing</a></td><td>Punches, leans, ducks</td><td>Shoulders, arms, core</td></tr>
  <tr><td><a href="/games/slash/">Slash</a></td><td>Two-arm swipes</td><td>Shoulders, arms</td></tr>
  <tr><td><a href="/games/swim/">Swim</a></td><td>Front-crawl arm strokes</td><td>Shoulders, upper back</td></tr>
  <tr><td><a href="/games/penalty-hero/">Penalty Hero</a></td><td>Reaches and steps</td><td>Arms, legs, reaction</td></tr>
</table>

<h2>Building a session</h2>
<p>A simple way to get a balanced 15–20 minutes: start with a lighter game to warm
up (<a href="/games/penalty-hero/">Penalty Hero</a> or <a href="/games/swim/">Swim</a>),
then two or three rounds of something harder (<a href="/games/move-rush/">Move Rush</a>,
<a href="/games/squat-rush/">Squat Rush</a>, <a href="/games/boxing/">Boxing</a>), and
finish with an arm game like <a href="/games/slash/">Slash</a>. Movus totals calories,
minutes and reps on its Progress page as you go.</p>

<h2>What you need</h2>
<ul>
  <li>An iPhone running iOS 17 or later.</li>
  <li>Somewhere to stand it up at about waist height.</li>
  <li>Two to three metres of clear floor in front of it.</li>
</ul>
<p>See <a href="/guides/set-up-iphone-for-motion-games/">how to set up your phone</a> for
the details that make tracking reliable.</p>
"""),
    dict(slug="set-up-iphone-for-motion-games",
         title="How to set up your iPhone for motion-controlled games",
         h1="How to set up your iPhone for motion-controlled games",
         desc="Where to put the phone, how far to stand, and how to light the room so a camera-based game reads your body reliably.",
         body="""
<p class="lede">Almost every tracking problem in a camera game comes down to three
things: where the phone is, how far away you stand, and the light. Get those right
and the game reads you every time.</p>

<h2>1. Put the phone at waist height or above</h2>
<p>Stand it against a wall, on a shelf, or propped on the edge of a table, in
landscape. The camera needs to look at you, not up at you: flat on the floor it sees
mostly ceiling and your legs. Tilting it back slightly is fine.</p>

<h2>2. Stand two to three metres back</h2>
<p>The game needs your whole body in frame — head to at least the knees. In Movus
the calibration screen shows your live outline and turns green when you are in the
right place. If it asks you to step back, your body is too big in the picture; if
it asks you to come closer, it is too small.</p>
<p>Hand games like <a href="/games/slash/">Slash</a> are more forgiving: they only
need your hands and shoulders, so you can stand closer or even sit.</p>

<h2>3. Light the front of you, not the back</h2>
<ul>
  <li>Turn on the room light. Evening light from one lamp is often not enough.</li>
  <li>Avoid a bright window behind you — the camera exposes for the window and you
      become a silhouette.</li>
  <li>Plain clothes that contrast with the wall behind you help.</li>
</ul>

<h2>4. Keep the space clear</h2>
<p>Leave room to swing your arms and step to each side. Move anything you could hit,
and make sure pets and other people are out of frame — the camera follows one person.</p>

<h2>Troubleshooting</h2>
<table>
  <tr><th>What happens</th><th>Usually means</th><th>Try</th></tr>
  <tr><td>"Step back"</td><td>Too close</td><td>Move back half a metre</td></tr>
  <tr><td>"Show your hands"</td><td>Hands out of frame</td><td>Raise the phone or step back</td></tr>
  <tr><td>Moves read late</td><td>Low light or Low Power Mode</td><td>Turn a light on; switch Low Power Mode off</td></tr>
  <tr><td>"Where did you go?"</td><td>You left the frame</td><td>Step back into the outline</td></tr>
</table>
<p>More help is on the <a href="/support.html">support page</a>.</p>
"""),
    dict(slug="calories-burned-exercise-games",
         title="How many calories do exercise games burn?",
         h1="How many calories do exercise games burn?",
         desc="An honest look at calories in active video games: how they are estimated, what changes the number, and typical figures for each Movus game.",
         body="""
<p class="lede">Exercise games can be a genuine workout — but the number on screen is
only as good as the method behind it. Here is how Movus estimates it, and what you
can expect from each game.</p>

<h2>How the estimate works</h2>
<p>Every activity has a <b>MET</b> value: how many times your resting metabolism it
takes. Running is high, sitting is 1. Movus gives each game a MET based on the
Compendium of Physical Activities and on what the game actually asks of your body.</p>
<p>It then estimates your resting metabolism from your height, weight, age and sex
using the <b>Mifflin–St Jeor</b> equation, and counts only the <b>active</b> part —
(MET − 1) × resting rate × minutes. That is the same thing Apple Health calls
active energy, so the two agree.</p>

<h2>Typical figures</h2>
<p>For a 35-year-old, 170 cm, 70 kg adult, ten minutes of continuous play:</p>
<table>
  <tr><th>Game</th><th>Intensity (MET)</th><th>Active kcal / 10 min</th></tr>
__TABLE__
</table>
<p>A heavier or more muscular person burns more for the same game; a lighter person
burns less. Movus uses your own numbers from Apple Health if you allow it.</p>

<h2>What makes the real number higher or lower</h2>
<ul>
  <li><b>How much you move.</b> A round you barely moved in burns less, and Movus
      logs the movements it actually read.</li>
  <li><b>Rest between rounds.</b> The table assumes continuous play.</li>
  <li><b>Depth and range.</b> Deeper squats and bigger arm strokes cost more.</li>
</ul>

<h2>Is it enough to count as exercise?</h2>
<p>Most adults are advised to get around 150 minutes of moderate activity a week.
Activities above about 6 MET count as vigorous, and most Movus games are in that
range when played continuously. Fifteen to twenty minutes a day of play adds up.</p>
"""),
    dict(slug="exercise-games-for-kids-and-families",
         title="Active games for kids and families at home",
         h1="Active games for kids and families at home",
         desc="Camera-controlled games that get children and families moving indoors — with no controllers to fight over and no accounts to set up.",
         body="""
<p class="lede">When it is raining, dark early, or just too cold to go out, a game that
needs you to jump, duck and dodge gets the whole house moving — and there is no
controller to share.</p>

<h2>Why body games suit families</h2>
<ul>
  <li><b>No controller to learn.</b> Children already know how to jump and squat.
      Each game shows a short animation of the move it wants.</li>
  <li><b>Easy turn-taking.</b> Rounds last a minute or two, so everyone gets a go.</li>
  <li><b>Visible scores.</b> Personal bests make it a friendly competition.</li>
</ul>

<h2>Good first games</h2>
<ul>
  <li><a href="/games/squat-rush/">Squat Rush</a> — one simple move, instantly funny.</li>
  <li><a href="/games/slash/">Slash</a> — just your hands; works for small children and seated players.</li>
  <li><a href="/games/move-rush/">Move Rush</a> — the classic endless runner, with real jumping.</li>
</ul>

<h2>Safety first</h2>
<ul>
  <li>Clear the space and keep younger children and pets out of the play area.</li>
  <li>Play on a non-slip floor in trainers or bare feet, not socks.</li>
  <li>Stand the phone where it cannot be knocked over.</li>
</ul>

<h2>Privacy for families</h2>
<p>Movus has no account, never asks for a name and never records or uploads camera
frames — every frame is read on the phone and discarded. Read more in
<a href="/guides/is-camera-fitness-private/">is camera-based fitness private?</a></p>
"""),
    dict(slug="no-equipment-cardio-at-home",
         title="No-equipment cardio at home that doesn't feel like cardio",
         h1="No-equipment cardio at home that doesn't feel like cardio",
         desc="Jumping, squatting, dodging and punching: how to get your heart rate up at home with nothing but floor space and a phone.",
         body="""
<p class="lede">Cardio does not need a treadmill. Jumps, squats, side-steps and punches,
done continuously, raise your heart rate as well as most machines — the hard part is
keeping going. Games solve that part.</p>

<h2>The movements that do the work</h2>
<ul>
  <li><b>Jumps</b> — the quickest way to raise your heart rate.</li>
  <li><b>Squats</b> — big muscles, big demand.</li>
  <li><b>Lateral steps</b> — work the legs in a direction most routines ignore.</li>
  <li><b>Punches and arm swings</b> — upper-body cardio with no impact on the joints.</li>
</ul>

<h2>A 15-minute no-equipment session</h2>
<ol>
  <li><b>Warm up, 3 min</b> — <a href="/games/swim/">Swim</a>: long arm strokes.</li>
  <li><b>Legs, 5 min</b> — <a href="/games/move-rush/">Move Rush</a> and <a href="/games/squat-rush/">Squat Rush</a>, alternating rounds.</li>
  <li><b>Upper body, 5 min</b> — <a href="/games/boxing/">Boxing</a> and <a href="/games/slash/">Slash</a>.</li>
  <li><b>Cool down, 2 min</b> — <a href="/games/penalty-hero/">Penalty Hero</a> at an easy pace, then stretch.</li>
</ol>

<h2>Low-impact options</h2>
<p>If jumping is not for you, Slash, Boxing and Swim need no jumping at all, and Slash
can be played sitting down.</p>
"""),
    dict(slug="is-camera-fitness-private",
         title="Is camera-based fitness private?",
         h1="Is camera-based fitness private?",
         desc="What happens to camera frames in a motion-controlled fitness app, what to look for, and exactly what Movus does and does not do.",
         body="""
<p class="lede">A game that watches you has to be worth trusting. Here is what to ask of
any camera fitness app — and the answers for Movus.</p>

<h2>The questions to ask</h2>
<ul>
  <li><b>Is the video processed on the phone or sent to a server?</b></li>
  <li><b>Is anything recorded or saved?</b></li>
  <li><b>Does it need an account?</b></li>
  <li><b>What data does it collect, and can you turn it off?</b></li>
</ul>

<h2>The answers for Movus</h2>
<ul>
  <li><b>On the phone.</b> Every frame is read by Apple's on-device body tracking and
      discarded. There is no server that receives video.</li>
  <li><b>Nothing recorded.</b> No video, no photos, no still frames are written or sent.</li>
  <li><b>No account.</b> Movus never asks for a name or an email.</li>
  <li><b>Anonymous usage, switchable.</b> Which game, how long and how many movements —
      aggregates only, never images or body data — with one switch in Settings to stop it.</li>
</ul>

<h2>The camera light</h2>
<p>When a game is running, iOS shows its camera indicator. Movus closes the camera
whenever you leave a game, so the indicator goes off on the home screen.</p>

<p>The full details are in the <a href="/privacy.html">privacy policy</a>.</p>
"""),
]

# -------------------------------------------------------------------- shell


def picture(stem, w, h, sizes, alt, widths=(700, 1000, 1400), lazy=True, eager_hi=False):
    av = ", ".join(f"/img/{stem}-{x}.avif {x}w" for x in widths)
    wb = ", ".join(f"/img/{stem}-{x}.webp {x}w" for x in widths)
    extra = ' fetchpriority="high"' if eager_hi else (' loading="lazy"' if lazy else "")
    return (f'<picture><source type="image/avif" sizes="{sizes}" srcset="{av}">'
            f'<source type="image/webp" sizes="{sizes}" srcset="{wb}">'
            f'<img sizes="{sizes}" decoding="async" src="/img/{stem}.jpg"{extra} '
            f'width="{w}" height="{h}" alt="{alt}"></picture>')


def card_pic(card, alt):
    return picture(f"card-{card}", 330, 402, "(max-width: 560px) 45vw, 240px", alt,
                   widths=(400, 550, 700))


def shot_pic(shot, alt, hero=False):
    return picture(f"shot-{shot}", 1400, 644, "(max-width: 900px) 92vw, 560px", alt,
                   lazy=not hero, eager_hi=hero)


HEADER = """<header class="site">
  <div class="wrap">
    <a class="brand" href="/"><picture><source type="image/avif" sizes="32px" srcset="/img/icon-96.avif 96w, /img/icon-192.avif 192w"><source type="image/webp" sizes="32px" srcset="/img/icon-96.webp 96w, /img/icon-192.webp 192w"><img sizes="32px" decoding="async" src="/img/icon-96.png" width="32" height="32" alt=""></picture><span>MOVUS</span></a>
    <nav class="site">
      <a href="/games/">Games</a>
      <a href="/how-it-works/">How it works</a>
      <a href="/guides/">Guides</a>
      <a class="keep" href="/support.html">Support</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="site">
  <div class="wrap">
    <div>© 2026 Movus</div>
    <nav>
      <a href="/games/">Games</a>
      <a href="/how-it-works/">How it works</a>
      <a href="/guides/">Guides</a>
      <a href="/faq/">FAQ</a>
      <a href="/privacy.html">Privacy</a>
      <a href="/support.html">Support</a>
    </nav>
  </div>
</footer>"""


def page(path, title, desc, body, schema, image="/img/og.jpg"):
    url = f"{SITE}{path}"
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0716">
<link rel="canonical" href="{url}">
<link rel="icon" href="/img/favicon-64.png" sizes="64x64">
<link rel="apple-touch-icon" href="/img/icon-180.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Movus">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}{image}">
<link rel="preload" href="/fonts/outfit-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{CSS}">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": schema}, indent=1)}
</script>
</head>
<body>

{HEADER}

{body}

{FOOTER}

</body>
</html>
"""
    out = os.path.join(ROOT, path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(html)
    return path


def crumbs(items):
    links = " <span>/</span> ".join(
        f'<a href="{p}">{n}</a>' if p else f"<span aria-current=\"page\">{n}</span>"
        for n, p in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb">{links}</nav>'


def crumb_schema(items, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n,
         "item": f"{SITE}{p or path}"} for i, (n, p) in enumerate(items)]}


def faq_html(qs):
    return "\n".join(f'<details class="qa"><summary>{q}</summary><p>{a}</p></details>'
                     for q, a in qs)


def faq_schema(qs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}


APP_REF = {"@type": "MobileApplication", "@id": f"{SITE}/#app", "name": "Movus",
           "operatingSystem": "iOS 17.0 or later", "applicationCategory": "GameApplication"}

# -------------------------------------------------------------------- build
written = []

# Game pages
for i, g in enumerate(GAMES):
    path = f"/games/{g['slug']}/"
    others = [o for o in GAMES if o is not g]
    trail = [("Home", "/"), ("Games", "/games/"), (g["name"], None)]
    moves = "\n".join(f'<div class="step"><h3>{m}</h3><p>{d}</p></div>' for m, d in g["moves"])
    tips = "\n".join(f"<li>{t}</li>" for t in g["tips"])
    related = "\n".join(
        f'<a class="game" href="/games/{o["slug"]}/">{card_pic(o["card"], o["name"])}<b>{o["name"]}</b></a>'
        for o in others[:4])
    body = f"""<main>
<div class="hero game-hero">
  <div class="wrap">
    <div>
      {crumbs(trail)}
      <p class="eyebrow">A Movus game</p>
      <h1>{g['name']}</h1>
      <p class="lede">{g['lede']}</p>
      <dl class="stats">
        <div><dt>Intensity</dt><dd>{g['met']} <small>MET</small></dd></div>
        <div><dt>Active energy</dt><dd>≈{g['kcal']} <small>kcal / 10 min*</small></dd></div>
        <div><dt>Controller</dt><dd>Your body</dd></div>
      </dl>
    </div>
    <div class="device">{shot_pic(g['shot'], g['name'] + ' in Movus, as seen from across the room.', hero=True)}</div>
  </div>
</div>

<section>
  <div class="wrap">
    <p class="kicker">How to play</p>
    <h2>The moves it reads.</h2>
    <div class="steps">
{moves}
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap split">
    <div>
      <p class="kicker">The workout</p>
      <h2>What {g['name']} works.</h2>
      <p class="section-lede" style="margin-bottom:0">{g['works']}</p>
      <p class="meta" style="margin-top:20px">*For a 35-year-old, 170 cm, 70 kg adult playing
      continuously. The app uses your own height, weight and age. <a href="/guides/calories-burned-exercise-games/">How it is calculated</a>.</p>
    </div>
    <div>
      <p class="kicker">Tips</p>
      <ul class="facts">
{tips}
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap prose">
    <p class="kicker">Questions</p>
    <h2>{g['name']} FAQ</h2>
{faq_html(g['faq'])}
    <p style="margin-top:28px">Setting up for the first time? Read <a href="/guides/set-up-iphone-for-motion-games/">how to set up your iPhone</a>.</p>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <p class="kicker">More games</p>
    <h2>Keep moving.</h2>
    <div class="games">
{related}
    </div>
  </div>
</section>
</main>"""
    schema = [crumb_schema(trail, path), faq_schema(g["faq"]),
              {"@type": "VideoGame", "name": f"{g['name']} (Movus)", "url": f"{SITE}{path}",
               "description": g["short"], "image": f"{SITE}/img/shot-{g['shot']}.jpg",
               "gamePlatform": "iPhone", "playMode": "SinglePlayer",
               "genre": ["Fitness", "Exergame"], "isPartOf": APP_REF}]
    written.append(page(path, f"{g['title']} | Movus", g["short"], body, schema,
                        image=f"/img/shot-{g['shot']}.jpg"))

# Games index
cards = "\n".join(
    f'''<a class="game-row" href="/games/{g["slug"]}/">
  <div class="thumb">{card_pic(g["card"], g["name"])}</div>
  <div><h2>{g["name"]}</h2><p>{g["short"]}</p>
  <p class="meta">{g["met"]} MET · ≈{g["kcal"]} kcal per 10 min</p></div>
</a>''' for g in GAMES)
trail = [("Home", "/"), ("Games", None)]
written.append(page("/games/", "The games — six fitness games you play with your body | Movus",
    "Move Rush, Penalty Hero, Swim, Slash, Squat Rush and Boxing: six iPhone games controlled by your body through the front camera.",
    f"""<main>
<div class="wrap"><div class="doc wide">
  {crumbs(trail)}
  <h1>Six games, one controller.</h1>
  <p class="lede">Each Movus game asks your body for something different — a step, a
  squat, a punch, a stroke. Pick by what you want to work, or just by what looks fun.</p>
  <div class="game-list">
{cards}
  </div>
</div></div>
</main>""",
    [crumb_schema(trail, "/games/"),
     {"@type": "ItemList", "itemListElement": [
         {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/games/{g['slug']}/",
          "name": g["name"]} for i, g in enumerate(GAMES)]}]))

# Guides
table = "\n".join(f'  <tr><td><a href="/games/{g["slug"]}/">{g["name"]}</a></td>'
                  f'<td>{g["met"]}</td><td>≈{g["kcal"]}</td></tr>'
                  for g in sorted(GAMES, key=lambda g: -g["met"]))
for gd in GUIDES:
    path = f"/guides/{gd['slug']}/"
    trail = [("Home", "/"), ("Guides", "/guides/"), (gd["h1"], None)]
    others = "\n".join(f'<li><a href="/guides/{o["slug"]}/">{o["h1"]}</a></li>'
                       for o in GUIDES if o is not gd)
    body = gd["body"].replace("__TABLE__", table)
    written.append(page(path, f"{gd['title']} | Movus", gd["desc"], f"""<main>
<div class="wrap"><article class="doc">
  {crumbs(trail)}
  <h1>{gd['h1']}</h1>
  <p class="meta">Movus guides · Updated {TODAY}</p>
{body}
  <aside class="more">
    <h2>More guides</h2>
    <ul>
{others}
    </ul>
  </aside>
</article></div>
</main>""", [crumb_schema(trail, path),
             {"@type": "Article", "headline": gd["h1"], "description": gd["desc"],
              "dateModified": TODAY, "author": {"@type": "Organization", "name": "Movus"},
              "publisher": {"@id": f"{SITE}/#org"}, "mainEntityOfPage": f"{SITE}{path}",
              "image": f"{SITE}/img/og.jpg"}]))

trail = [("Home", "/"), ("Guides", None)]
items = "\n".join(f'<a class="guide" href="/guides/{g["slug"]}/"><h2>{g["h1"]}</h2><p>{g["desc"]}</p></a>'
                  for g in GUIDES)
written.append(page("/guides/", "Guides — home workouts, setup and active games | Movus",
    "Guides to body-controlled fitness games: setting up your iPhone, home cardio with no equipment, calories, family play and camera privacy.",
    f"""<main>
<div class="wrap"><div class="doc wide">
  {crumbs(trail)}
  <h1>Guides</h1>
  <p class="lede">Getting the most out of games you play with your body — from setting up
  the phone to building a real workout.</p>
  <div class="guide-list">
{items}
  </div>
</div></div>
</main>""", [crumb_schema(trail, "/guides/")]))

# How it works
trail = [("Home", "/"), ("How it works", None)]
written.append(page("/how-it-works/", "How Movus works — camera body tracking on iPhone | Movus",
    "How Movus reads your movement with the iPhone front camera, on the device, with nothing recorded — and how to set up for reliable tracking.",
    f"""<main>
<div class="wrap"><article class="doc">
  {crumbs(trail)}
  <h1>How Movus works</h1>
  <p class="lede">Movus turns the iPhone's front camera into a controller. It reads where
  your body, hands and feet are, many times a second, and each game turns that into a move.</p>

  <h2>Body tracking, on the phone</h2>
  <p>Each camera frame goes through Apple's on-device body-pose detection, which finds
  your joints — shoulders, elbows, wrists, hips, knees. Movus measures everything
  against <b>your own calibrated pose</b>, so a step means the same thing for a tall
  adult and a child, near the phone or further away. The frame is then discarded:
  nothing is recorded and nothing leaves the phone.</p>

  <h2>Calibration</h2>
  <p>When a game starts, the calibration screen shows your live outline. Stand where it
  asks; it turns green when your body is framed and steady, and the game begins. If
  you step out of frame mid-game, it pauses and asks <i>where did you go?</i> — come
  back into the outline and a short countdown resumes play.</p>

  <h2>What each game reads</h2>
  <table>
    <tr><th>Signal</th><th>Used by</th></tr>
    <tr><td>Where you stand (left / centre / right)</td><td><a href="/games/move-rush/">Move Rush</a></td></tr>
    <tr><td>Crouch and jump</td><td><a href="/games/move-rush/">Move Rush</a>, <a href="/games/squat-rush/">Squat Rush</a>, <a href="/games/boxing/">Boxing</a></td></tr>
    <tr><td>Hand positions</td><td><a href="/games/slash/">Slash</a>, <a href="/games/penalty-hero/">Penalty Hero</a>, <a href="/games/boxing/">Boxing</a></td></tr>
    <tr><td>Arm strokes</td><td><a href="/games/swim/">Swim</a></td></tr>
    <tr><td>Upper-body lean</td><td><a href="/games/boxing/">Boxing</a></td></tr>
  </table>

  <h2>Setting up</h2>
  <ul>
    <li>Phone in landscape, at about waist height or above.</li>
    <li>Two to three metres back, whole body in frame.</li>
    <li>A lit room, without a bright window behind you.</li>
  </ul>
  <p>The full walkthrough is in <a href="/guides/set-up-iphone-for-motion-games/">how to set up your iPhone</a>.</p>

  <h2>Calories and Apple Health</h2>
  <p>Movus estimates active energy from each game's intensity and your own body, and can
  save every session to Apple Health as a workout. See
  <a href="/guides/calories-burned-exercise-games/">how the calories are calculated</a>.</p>

  <h2>Privacy</h2>
  <p>No account, no recording, no upload. Anonymous usage counts can be switched off in
  Settings. Read <a href="/guides/is-camera-fitness-private/">is camera fitness private?</a>
  and the <a href="/privacy.html">privacy policy</a>.</p>
</article></div>
</main>""", [crumb_schema(trail, "/how-it-works/"),
             {"@type": "HowTo", "name": "Set up Movus for body tracking",
              "step": [{"@type": "HowToStep", "text": t} for t in [
                  "Stand the iPhone in landscape at about waist height or above.",
                  "Step two to three metres back so your whole body is in frame.",
                  "Turn on a room light and avoid a bright window behind you.",
                  "Hold still on the calibration screen until it turns green."]]}]))

# FAQ
FAQ = [
    ("What is Movus?", "Movus is a collection of fitness games for iPhone that you control with your body. The front camera reads your movement, so you play by running, jumping, squatting, punching and swimming — no buttons and nothing to wear."),
    ("What do I need to play?", "An iPhone running iOS 17 or later, somewhere to stand it at about waist height, and two to three metres of clear space."),
    ("Does Movus record video of me?", "No. Every camera frame is processed on the phone and discarded. Nothing is recorded, saved or uploaded."),
    ("Do I need an account?", "No. Movus never asks for a name, an email or a sign-in."),
    ("Which games are included?", "Six: Move Rush, Penalty Hero, Swim, Slash, Squat Rush and Boxing."),
    ("Can children play?", "Yes. The games use natural movements, and there is no account or chat. Clear the space and supervise younger children."),
    ("Can I play sitting down?", "Slash reads only your hands, so it works seated. The other games need you standing."),
    ("How are calories calculated?", "From each game's intensity (a MET value) and your resting metabolism from the Mifflin–St Jeor equation, counting only active energy — the same measure Apple Health uses."),
    ("Does it work with Apple Health?", "Yes, if you turn it on in Settings: each game is saved as a workout with its active energy."),
    ("Why isn't the game reading my moves?", "Usually the phone is too low, you are too close, or the room is too dark. See the setup guide or the support page."),
    ("Is there a multiplayer mode?", "Not yet. Two-player modes are being tested and will come in a later version."),
    ("When is Movus available?", "Movus is coming to the App Store for iPhone."),
]
trail = [("Home", "/"), ("FAQ", None)]
written.append(page("/faq/", "Frequently asked questions | Movus",
    "Answers about Movus: what you need, privacy and the camera, calories, Apple Health, playing with kids and setup.",
    f"""<main>
<div class="wrap"><article class="doc">
  {crumbs(trail)}
  <h1>Frequently asked questions</h1>
{faq_html(FAQ)}
  <p style="margin-top:28px">Still stuck? The <a href="/support.html">support page</a> covers setup problems in detail.</p>
</article></div>
</main>""", [crumb_schema(trail, "/faq/"), faq_schema(FAQ)]))

# Sitemap
urls = ["/"] + written + ["/privacy.html", "/support.html"]
def prio(u):
    return "1.0" if u == "/" else "0.9" if u.startswith("/games/") else "0.7" if u.startswith("/guides/") or u in ("/how-it-works/", "/faq/") else "0.4"
entries = "\n".join(
    f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio(u)}</priority>\n  </url>"
    for u in urls)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(
    f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')
print(f"{len(written)} pages, {len(urls)} sitemap entries")
