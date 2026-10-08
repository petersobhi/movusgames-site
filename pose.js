/* The figure in the hero viewfinder.
 *
 * It is not a stock illustration: the proportions below are the same
 * Drillis & Contini segment table the app's own test harness is built from
 * (`MoveGame/Dev/PoseBody.swift`), as fractions of stature, and the limbs are
 * placed the same way the rig places them — a *direction and a reach*, with
 * the middle joint solved by the law of cosines — so an arm cannot stretch
 * and the elbow always lands where a real one would.
 *
 * The poses it cycles through are the signals the detector actually reads:
 * a step across, a crouch, a jump, a reach, a planted lean. The readout
 * underneath names each one the way the game does.
 *
 * ~4KB, no dependencies, one rAF loop that stops when off-screen. */
(function () {
  'use strict';

  var cv = document.getElementById('finder');
  if (!cv || !cv.getContext) return;
  var ctx = cv.getContext('2d');
  var out = document.getElementById('finder-move');

  /* Fractions of stature — PoseBody.swift */
  var B = {
    torso: 0.288, upperArm: 0.186, foreArm: 0.146,
    thigh: 0.245, shank: 0.246,
    halfShoulder: 0.129, halfHip: 0.0955, neckToNose: 0.118
  };

  /* Angles are measured from straight down, positive toward screen-right, so
     aim = (sin a, cos a) with y pointing down the canvas. `r` is reach as a
     fraction of full extension — exactly cos(fold / 2). */
  var POSES = [
    { name: 'Tracking',      hip: [0, 0],        tilt: 0,
      arms: [[-0.27, 0.96], [0.27, 0.96]], legs: [[-0.07, 0.99], [0.07, 0.99]] },

    { name: 'Step · left',   hip: [-0.085, 0],   tilt: -0.05,
      arms: [[-0.34, 0.93], [0.26, 0.95]], legs: [[-0.20, 0.97], [0.16, 0.96]] },

    { name: 'Crouch',        hip: [0, 0.120],    tilt: 0.16,
      arms: [[-0.70, 0.78], [0.70, 0.78]], legs: [[-0.17, 0.79], [0.17, 0.79]] },

    { name: 'Jump',          hip: [0, -0.165],   tilt: -0.03,
      arms: [[-2.60, 0.95], [2.60, 0.95]], legs: [[-0.10, 0.88], [0.10, 0.88]] },

    { name: 'Reach',         hip: [0, 0.005],    tilt: 0,
      arms: [[-2.78, 0.98], [2.78, 0.98]], legs: [[-0.06, 0.99], [0.06, 0.99]] },

    { name: 'Step · right',  hip: [0.085, 0],    tilt: 0.05,
      arms: [[-0.26, 0.95], [0.34, 0.93]], legs: [[-0.16, 0.96], [0.20, 0.97]] },

    /* The one move that separates a lean from a step: shoulders over, hips
       where they were. `PoseStream.tilt` is the shoulder line against the hip
       line, which is why this pose moves the torso and not the feet. */
    { name: 'Lean · left',   hip: [-0.012, 0],   tilt: -0.30,
      arms: [[-0.40, 0.95], [0.08, 0.96]], legs: [[-0.07, 0.99], [0.07, 0.99]] }
  ];

  var HOLD = 1150, MOVE = 620;          /* ms: still, then travelling */
  var STEP = HOLD + MOVE;

  function ease(t) { return t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2; }
  function mix(a, b, t) { return a + (b - a) * t; }

  /* Two bones from a direction and a reach. The far joint lands exactly
     `reach × length` along `aim`, so the limb keeps its length whatever the
     pose asks for — the property the app's own harness was rebuilt to get. */
  function limb(ox, oy, ang, reach, upper, lower, bend) {
    var total = upper + lower;
    var d = Math.max(0.05, Math.min(reach, 0.999)) * total;
    var ux = Math.sin(ang), uy = Math.cos(ang);
    var ex = ox + ux * d, ey = oy + uy * d;
    var a = (d * d + upper * upper - lower * lower) / (2 * d);
    var h = Math.sqrt(Math.max(0, upper * upper - a * a));
    return {
      mid: [ox + ux * a - uy * h * bend, oy + uy * a + ux * h * bend],
      end: [ex, ey]
    };
  }

  function build(p) {
    var hx = p.hip[0], hy = p.hip[1];
    var st = Math.sin(p.tilt), ct = Math.cos(p.tilt);

    /* The torso is a rigid bar from the hip centre, tilted; the shoulder line
       is square to it. */
    var nx = hx + st * B.torso, ny = hy - ct * B.torso;
    var sx = ct * B.halfShoulder, sy = st * B.halfShoulder;

    var sh = [[nx - sx, ny - sy], [nx + sx, ny + sy]];
    var hp = [[hx - B.halfHip, hy], [hx + B.halfHip, hy]];

    var arms = [0, 1].map(function (i) {
      return limb(sh[i][0], sh[i][1], p.arms[i][0], p.arms[i][1],
                  B.upperArm, B.foreArm, i ? 1 : -1);
    });
    var legs = [0, 1].map(function (i) {
      return limb(hp[i][0], hp[i][1], p.legs[i][0], p.legs[i][1],
                  B.thigh, B.shank, i ? -1 : 1);
    });

    return {
      nose: [nx + st * B.neckToNose, ny - ct * B.neckToNose],
      neck: [nx, ny], hipC: [hx, hy], sh: sh, hp: hp, arms: arms, legs: legs
    };
  }

  /* Blending two poses blends their *inputs* — angle, reach, hip, tilt — and
     then solves, rather than blending solved joint positions. A lerp between
     two solved skeletons shortens every limb through the middle of the move,
     which reads as the body deflating. */
  function blend(a, b, t) {
    return {
      name: t < 0.5 ? a.name : b.name,
      hip: [mix(a.hip[0], b.hip[0], t), mix(a.hip[1], b.hip[1], t)],
      tilt: mix(a.tilt, b.tilt, t),
      arms: [0, 1].map(function (i) {
        return [mix(a.arms[i][0], b.arms[i][0], t), mix(a.arms[i][1], b.arms[i][1], t)];
      }),
      legs: [0, 1].map(function (i) {
        return [mix(a.legs[i][0], b.legs[i][0], t), mix(a.legs[i][1], b.legs[i][1], t)];
      })
    };
  }

  var dpr = 1, W = 0, H = 0;
  function size() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = cv.getBoundingClientRect();
    W = r.width; H = r.height;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function draw(p) {
    var f = build(p);
    /* Stature spans 0.72 of the panel; the hips sit at a fixed height so a
       jump visibly leaves the ground and a crouch visibly sinks toward it. */
    var S = H * 0.72, cx = W / 2, cy = H * 0.63;
    function P(q) { return [cx + q[0] * S, cy + q[1] * S]; }

    ctx.clearRect(0, 0, W, H);

    /* The ground the figure stands on, so a jump and a crouch have something
       to be measured against. */
    var gy = cy + 0.005 * S;
    var g = ctx.createLinearGradient(cx - S * 0.5, 0, cx + S * 0.5, 0);
    g.addColorStop(0, 'rgba(43,184,240,0)');
    g.addColorStop(0.5, 'rgba(43,184,240,.28)');
    g.addColorStop(1, 'rgba(43,184,240,0)');
    ctx.strokeStyle = g; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(cx - S * 0.5, gy); ctx.lineTo(cx + S * 0.5, gy); ctx.stroke();

    var bone = Math.max(3, S * 0.021);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.shadowColor = 'rgba(43,184,240,.55)';
    ctx.shadowBlur = bone * 2.4;
    ctx.strokeStyle = '#dff3fd';
    ctx.lineWidth = bone;

    function line(a, b) {
      var u = P(a), v = P(b);
      ctx.beginPath(); ctx.moveTo(u[0], u[1]); ctx.lineTo(v[0], v[1]); ctx.stroke();
    }

    /* spine, shoulder line, hip line */
    line(f.hipC, f.neck);
    line(f.sh[0], f.sh[1]);
    line(f.hp[0], f.hp[1]);
    for (var i = 0; i < 2; i++) {
      line(f.sh[i], f.arms[i].mid); line(f.arms[i].mid, f.arms[i].end);
      line(f.hp[i], f.legs[i].mid); line(f.legs[i].mid, f.legs[i].end);
    }

    /* head */
    var hd = P(f.nose), rr = S * 0.058;
    ctx.beginPath(); ctx.arc(hd[0], hd[1], rr, 0, Math.PI * 2); ctx.stroke();

    /* joints, the way the app's own overlay draws them */
    ctx.shadowBlur = 0;
    ctx.fillStyle = '#2bb8f0';
    var dots = [f.neck, f.hipC, f.sh[0], f.sh[1], f.hp[0], f.hp[1],
                f.arms[0].mid, f.arms[1].mid, f.arms[0].end, f.arms[1].end,
                f.legs[0].mid, f.legs[1].mid, f.legs[0].end, f.legs[1].end];
    for (var k = 0; k < dots.length; k++) {
      var d = P(dots[k]);
      ctx.beginPath(); ctx.arc(d[0], d[1], bone * 0.62, 0, Math.PI * 2); ctx.fill();
    }
  }

  var t0 = null, shown = '', running = false, raf = 0;

  function frame(now) {
    if (!running) return;
    if (t0 === null) t0 = now;
    var e = now - t0;
    var i = Math.floor(e / STEP) % POSES.length;
    var into = e % STEP;
    var p;
    if (into < HOLD) {
      p = POSES[i];
    } else {
      p = blend(POSES[i], POSES[(i + 1) % POSES.length], ease((into - HOLD) / MOVE));
    }
    draw(p);
    if (out && p.name !== shown) { shown = p.name; out.textContent = p.name; }
    raf = requestAnimationFrame(frame);
  }

  function start() { if (!running) { running = true; raf = requestAnimationFrame(frame); } }
  function stop()  { running = false; cancelAnimationFrame(raf); }

  size();
  window.addEventListener('resize', function () { size(); draw(POSES[0]); }, { passive: true });

  /* A still figure for anyone who has asked the system not to animate, and
     for a tab nobody is looking at. */
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    draw(POSES[0]);
    if (out) out.textContent = POSES[0].name;
    return;
  }

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      es[0].isIntersecting ? start() : stop();
    }, { threshold: 0.05 }).observe(cv);
  } else { start(); }

  document.addEventListener('visibilitychange', function () {
    document.hidden ? stop() : start();
  });
})();
