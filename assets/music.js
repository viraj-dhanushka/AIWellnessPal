/* Gentle background music for aiwellnesspal.com.
 *
 * Music is on by default: the ♪ button shows as active and playback is tried as
 * soon as the page loads. Most browsers block sound until the visitor interacts,
 * so if that attempt is refused the track starts (softly, with a fade-in) on the
 * first click, tap or key press. Turning it off with the ♪ button is remembered
 * in localStorage. Playing the
 * YouTube demo fades the music out and keeps it paused. The position carries
 * across pages via sessionStorage. Nothing is downloaded until playback starts.
 */
(function () {
  var SRC = '/assets/audio/i-give-you-today.m4a';
  var VOLUME = 0.18;
  var OFF_KEY = 'aiwp-music-off';
  var TIME_KEY = 'aiwp-music-time';

  function get(store, k) { try { return window[store].getItem(k); } catch (e) { return null; } }
  function set(store, k, v) { try { window[store].setItem(k, v); } catch (e) {} }
  function del(store, k) { try { window[store].removeItem(k); } catch (e) {} }

  var audio = null, fadeTimer = null, heldForVideo = false, started = false;
  var btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'music-toggle';
  btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M9 18.5a3 3 0 1 1-2-2.83V5.8l12-2.3v12a3 3 0 1 1-2-2.83V7.06L9 8.6v9.9z"/></svg>';
  document.body.appendChild(btn);

  function playing() { return audio && !audio.paused; }
  // "On" = playing, or enabled and waiting for the browser to allow sound.
  function enabled() { return get('localStorage', OFF_KEY) !== '1' && !heldForVideo; }
  function render() {
    var on = playing() || (enabled() && !audio) || (enabled() && audio && audio.paused && !started);
    btn.classList.toggle('on', on);
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btn.setAttribute('aria-label', on ? 'Pause background music' : 'Play background music');
    btn.title = on ? 'Pause music' : 'Play music';
  }

  function fadeTo(target, ms, done) {
    clearInterval(fadeTimer);
    var start = audio.volume, steps = Math.max(1, Math.round(ms / 50)), i = 0;
    fadeTimer = setInterval(function () {
      i++;
      audio.volume = Math.max(0, Math.min(1, start + (target - start) * (i / steps)));
      if (i >= steps) { clearInterval(fadeTimer); if (done) done(); }
    }, 50);
  }

  function start() {
    if (!audio) {
      audio = new Audio(SRC);
      audio.loop = true;
      audio.preload = 'auto';
      var t = parseFloat(get('sessionStorage', TIME_KEY));
      if (t > 0) audio.currentTime = t;
      audio.addEventListener('play', render);
      audio.addEventListener('pause', render);
    }
    audio.volume = 0;
    var p = audio.play();
    if (p && p.then) {
      p.then(function () { started = true; removeFirst(); fadeTo(VOLUME, 2000); render(); })
       .catch(function () { render(); });   // blocked: wait for the first gesture
    } else { started = true; fadeTo(VOLUME, 2000); }
  }

  function stop(fadeMs) {
    if (!playing()) return;
    fadeTo(0, fadeMs, function () { audio.pause(); });
  }

  // First interaction anywhere starts the music (if the visitor hasn't turned it off).
  function firstGesture(e) {
    if (e.target.closest && (e.target.closest('.music-toggle') || e.target.closest('#video'))) return;
    removeFirst();
    if (get('localStorage', OFF_KEY) !== '1' && !heldForVideo) start();
  }
  function removeFirst() {
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.removeEventListener(ev, firstGesture, true); });
  }
  ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { document.addEventListener(ev, firstGesture, true); });

  // The ♪ button: play / pause, remembered for next visits.
  btn.addEventListener('click', function () {
    removeFirst();
    if (playing() || enabled()) { stop(400); set('localStorage', OFF_KEY, '1'); render(); }
    else { heldForVideo = false; del('localStorage', OFF_KEY); start(); }
  });

  // Playing the YouTube demo pauses the music so the video has full attention.
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#video button')) {
      heldForVideo = true;
      removeFirst();
      stop(600);
      render();
    }
  }, true);

  // Keep the position when moving between pages.
  window.addEventListener('pagehide', function () {
    if (audio) set('sessionStorage', TIME_KEY, String(audio.currentTime || 0));
  });

  render();
  // Try to start right away (allowed in some browsers, e.g. sites the visitor engages with).
  if (enabled()) start();
})();
