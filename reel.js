/* The hero reel: the app's AppBackground rule, on a page. The glow behind the
   phone and the highlighted name follow whichever game is playing, and a name
   jumps to its game. Times are the cuts in img/reel.mp4 (tools/make-reel.sh). */
(function () {
  var v = document.getElementById('reel'), hero = document.getElementById('hero');
  if (!v || !hero) return;
  var pills = [].slice.call(document.querySelectorAll('.reel-games button'));
  var tints = { runner: '#ff7a38', boxing: '#f24d57', swim: '#4dd1f2', slash: '#b47af5', keeper: '#2fc46d', squats: '#9adb3d' };
  var shown = 0;
  function show(i) {
    if (i === shown) return;
    pills[shown].classList.remove('on');
    pills[i].classList.add('on');
    shown = i;
    hero.style.setProperty('--tint', tints[pills[i].className.split(' ')[0].slice(2)]);
  }
  v.addEventListener('timeupdate', function () {
    var i = pills.length - 1;
    while (i > 0 && v.currentTime < +pills[i].dataset.at) i--;
    show(i);
  });
  pills.forEach(function (p, i) {
    p.addEventListener('click', function () {
      v.currentTime = +p.dataset.at + .05;
      show(i);
      v.play();
    });
  });
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) v.pause();
})();
