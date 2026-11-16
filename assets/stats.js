/*
 * Mądry Portfel — anonimowe statystyki odwiedzin i informacja o prywatności.
 *
 * Statystyki: GoatCounter (https://www.goatcounter.com) — bez plików cookies,
 * bez profilowania. Licznik działa tylko na opublikowanej stronie (nie w kopii
 * pobranej na dysk), nie działa, gdy przeglądarka wysyła sygnał Global Privacy
 * Control lub Do Not Track, ani gdy użytkownik wyłączył liczenie na stronie
 * polityki prywatności.
 *
 * Aby zmienić konto statystyk, podmień GOATCOUNTER_CODE (kod z goatcounter.com).
 */
(function () {
  var GOATCOUNTER_CODE = 'madryportfel';
  var LIVE_HOST = 'bartuniadev.github.io';
  var KEY_NO_STATS = 'mp-no-stats';
  var KEY_NOTICE = 'mp-notice';

  function get(key) {
    try { return window.localStorage.getItem(key); } catch (e) { return null; }
  }
  function set(key, value) {
    try {
      if (value === null) window.localStorage.removeItem(key);
      else window.localStorage.setItem(key, value);
      return true;
    } catch (e) { return false; }
  }

  function privacySignal() {
    return navigator.globalPrivacyControl === true ||
      navigator.doNotTrack === '1' || window.doNotTrack === '1';
  }

  function statsAllowed() {
    return location.hostname === LIVE_HOST && !!GOATCOUNTER_CODE &&
      get(KEY_NO_STATS) !== '1' && !privacySignal();
  }

  function loadCounter() {
    if (!statsAllowed()) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://gc.zgo.at/count.js';
    s.setAttribute('data-goatcounter', 'https://' + GOATCOUNTER_CODE + '.goatcounter.com/count');
    document.head.appendChild(s);
  }

  function policyHref() {
    if (location.hostname === LIVE_HOST) return '/madry-portfel/polityka-prywatnosci.html';
    var path = location.pathname;
    var inSub = /\/(artykuly|narzedzia)\//.test(path);
    return (inSub ? '../' : '') + 'polityka-prywatnosci.html';
  }

  function showNotice() {
    if (get(KEY_NOTICE) === '1') return;
    if (/polityka-prywatnosci\.html$/.test(location.pathname)) return;
    var bar = document.createElement('div');
    bar.setAttribute('role', 'region');
    bar.setAttribute('aria-label', 'Informacja o prywatności');
    bar.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:50;max-width:720px;margin:0 auto;' +
      'display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;padding:14px 16px;border-radius:12px;' +
      'background:#16211c;color:#e9f1ec;font:14px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;' +
      'box-shadow:0 10px 30px rgba(0,0,0,.25)';
    var text = document.createElement('p');
    text.style.cssText = 'margin:0;flex:1 1 320px';
    text.innerHTML = 'Ta strona <strong>nie używa plików cookies</strong>. Odwiedziny liczymy anonimowo, ' +
      'bez profilowania i bez reklam. <a href="' + policyHref() + '" style="color:#7fe3b0">Polityka prywatności</a>';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.textContent = 'Rozumiem';
    btn.style.cssText = 'font:inherit;font-weight:700;padding:9px 18px;border:0;border-radius:8px;' +
      'background:#3ad889;color:#08130d;cursor:pointer';
    btn.addEventListener('click', function () {
      set(KEY_NOTICE, '1');
      bar.parentNode.removeChild(bar);
    });
    bar.appendChild(text);
    bar.appendChild(btn);
    document.body.appendChild(bar);
  }

  /* Przełącznik „nie licz moich odwiedzin” na stronie polityki prywatności. */
  function wireOptOut() {
    var box = document.getElementById('stats-optout');
    if (!box) return;
    var status = document.getElementById('stats-status');
    function render() {
      var off = get(KEY_NO_STATS) === '1';
      box.checked = off;
      if (!status) return;
      if (off) status.textContent = 'Twoje odwiedziny nie są liczone w tej przeglądarce.';
      else if (privacySignal()) status.textContent = 'Twoja przeglądarka wysyła sygnał prywatności (GPC lub Do Not Track) — Twoje odwiedziny nie są liczone.';
      else status.textContent = 'Twoje odwiedziny są liczone anonimowo.';
    }
    box.addEventListener('change', function () {
      if (!set(KEY_NO_STATS, box.checked ? '1' : null)) {
        status.textContent = 'Nie udało się zapisać ustawienia — przeglądarka blokuje pamięć strony.';
        return;
      }
      render();
    });
    render();
  }

  function init() {
    loadCounter();
    showNotice();
    wireOptOut();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
