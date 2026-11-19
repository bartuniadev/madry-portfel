import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <div class="type-toggle" role="radiogroup" aria-label="Rodzaj kwoty">
      <label><input type="radio" name="kind" id="kGross" value="gross" checked><span>Kwota brutto</span></label>
      <label><input type="radio" name="kind" id="kNet" value="net"><span>Kwota na rękę (netto)</span></label>
    </div>
    <div class="field">
      <label for="amount" id="amountLbl">Twoje wynagrodzenie brutto miesięcznie (zł)</label>
      <input type="number" id="amount" inputmode="decimal" value="7000" min="0" step="100">
    </div>
    <div class="presets">
      <button type="button" class="preset-btn" data-v="4950">Płaca minimalna 2027</button>
      <button type="button" class="preset-btn" data-v="7550">Mediana</button>
      <button type="button" class="preset-btn" data-v="9178">Średnia</button>
      <button type="button" class="preset-btn" data-v="14239">Top 10%</button>
    </div>

    <div class="net-box">
      <span class="label">Zarabiasz więcej niż</span>
      <span class="net-amount" id="pct">0%</span>
      <span class="pct" id="pctNote"></span>
    </div>

    <svg id="chart" class="dist-chart" viewBox="0 0 640 270" role="img" aria-label="Rozkład wynagrodzeń w Polsce i Twoja pozycja"></svg>
    <p class="chart-note">Przerywane linie: 10% pracujących zarabia mniej niż 4,8 tys. zł brutto, połowa — mniej niż 7,6 tys. zł, 90% — mniej niż 14,2 tys. zł. Zielone pole to osoby, które zarabiają mniej od Ciebie.</p>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Mediana w Polsce</span>
        <span class="amount">7 550 zł</span>
        <span class="pct">brutto · ok. 5 477 zł netto</span>
      </div>
      <div class="result-card needs">
        <span class="label" id="medLbl">Do mediany</span>
        <span class="amount" id="medDiff">0 zł</span>
        <span class="pct">brutto miesięcznie</span>
      </div>
      <div class="result-card savings">
        <span class="label" id="topLbl">Do najlepiej zarabiających 10%</span>
        <span class="amount" id="topDiff">0 zł</span>
        <span class="pct">próg: 14 239 zł brutto</span>
      </div>
    </div>

    <div class="share-row">
      <button type="button" class="download-btn" id="shareBtn">Udostępnij wynik</button>
      <span class="hint" id="shareStatus" aria-live="polite"></span>
    </div>
    <p class="sum-warning" id="warn" hidden></p>'''
trust = ('dane GUS o rozkładzie wynagrodzeń w gospodarce narodowej w maju 2026 r.: 10% osób zarabiało co najwyżej 4806 zł brutto, połowa — co najwyżej 7550,32 zł (mediana), a 10% najlepiej zarabiających — co najmniej 14 239 zł; przeciętne wynagrodzenie wyniosło 9178,16 zł. '
 'Między tymi punktami wynik szacujemy z rozkładu logarytmiczno-normalnego dopasowanego do danych GUS, więc to przybliżenie z dokładnością do kilku punktów procentowych. '
 'Kwotę netto przeliczamy na brutto dla umowy o pracę (z PIT-2, bez PPK, osoba powyżej 26 lat). Porównanie dotyczy pensji z jednego miesiąca, bez premii rocznych. '
 'Źródło: <a href="https://stat.gov.pl/obszary-tematyczne/rynek-pracy/pracujacy-zatrudnieni-wynagrodzenia-koszty-pracy/">GUS — wynagrodzenia</a>.')
more = ('<a href="../artykuly/mediana-wynagrodzen-ile-zarabiaja-polacy.html">Mediana wynagrodzeń 2026 — ile naprawdę zarabiają Polacy →</a><br>'
        '<a href="../artykuly/negocjacje-podwyzka-zmiana-pracy.html">Jak negocjować podwyżkę →</a><br>'
        '<a href="kalkulator-brutto-netto.html">Kalkulator brutto–netto →</a>')
script = r'''  function $(id){ return document.getElementById(id); }
  var MED = 7550.32, D1 = 4806, D9 = 14239, AVG = 9178.16, Z90 = 1.2815516;
  var SU = Math.log(D9 / MED) / Z90, SD = Math.log(MED / D1) / Z90;
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function erf(x){ var s = x < 0 ? -1 : 1; x = Math.abs(x); var t = 1 / (1 + 0.3275911 * x);
    var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return s * y; }
  function pctOf(x){ if (x <= 0) return 0; var z = Math.log(x / MED) / (x >= MED ? SU : SD); return 50 * (1 + erf(z / Math.SQRT2)); }
  function dens(x){ var s = x >= MED ? SU : SD, z = Math.log(x / MED) / s; return Math.exp(-z * z / 2) / x; }
  function net(g){ var zus = r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245); zus = r2(zus); var h = r2((g - zus) * 0.09);
    var tax = Math.max(0, Math.round(Math.max(0, Math.round(g - zus - 250)) * 0.12 - 300)); return r2(g - zus - h - tax); }
  function grossFromNet(n){ var lo = 0, hi = 200000; for (var i = 0; i < 60; i++){ var m = (lo + hi) / 2; if (net(m) < n) lo = m; else hi = m; } return (lo + hi) / 2; }

  function drawChart(g){
    var W = 640, H = 270, L = 14, R = 14, T = 34, B = 66, x0 = 2000, x1 = 24000;
    var sx = function(x){ return L + (Math.min(Math.max(x, x0), x1) - x0) / (x1 - x0) * (W - L - R); };
    var maxD = 0, pts = [];
    for (var x = x0; x <= x1; x += 100){ var d = dens(x); pts.push([x, d]); if (d > maxD) maxD = d; }
    var sy = function(d){ return H - B - d / maxD * (H - B - T); };
    var line = pts.map(function(p, i){ return (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join(' ');
    var area = 'M' + sx(x0) + ' ' + (H - B) + ' ' + line.replace(/^M/, 'L') + ' L' + sx(x1) + ' ' + (H - B) + ' Z';
    var gx = sx(g), fill = pts.filter(function(p){ return p[0] <= g; });
    var under = fill.length ? 'M' + sx(x0) + ' ' + (H - B) + ' ' + fill.map(function(p){ return 'L' + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join(' ') + ' L' + gx.toFixed(1) + ' ' + sy(dens(Math.max(g, x0))).toFixed(1) + ' L' + gx.toFixed(1) + ' ' + (H - B) + ' Z' : '';
    var marks = [[D1, '4,8 tys.'], [MED, '7,6 tys.'], [D9, '14,2 tys.']];
    var svg = '<path d="' + area + '" fill="rgba(147,164,154,0.16)" stroke="none"/>' +
      (under ? '<path d="' + under + '" fill="rgba(58,216,137,0.35)" stroke="none"/>' : '') +
      '<path d="' + line + '" fill="none" stroke="#93a49a" stroke-width="2"/>' +
      '<line x1="' + L + '" y1="' + (H - B) + '" x2="' + (W - R) + '" y2="' + (H - B) + '" stroke="#2b362f" stroke-width="1"/>';
    marks.forEach(function(m, i){ var x = sx(m[0]);
      svg += '<line x1="' + x + '" y1="' + T + '" x2="' + x + '" y2="' + (H - B) + '" stroke="#5c6a62" stroke-dasharray="3 4"/>' +
        '<text x="' + x + '" y="' + (H - B + 26 + (i === 1 ? 28 : 0)) + '" fill="#93a49a" font-size="22" text-anchor="middle">' + m[1] + '</text>'; });
    var ty = T - 10, anchor = gx > W - 150 ? 'end' : gx < 150 ? 'start' : 'middle';
    svg += '<line x1="' + gx + '" y1="' + (T + 4) + '" x2="' + gx + '" y2="' + (H - B) + '" stroke="#f2c14e" stroke-width="3"/>' +
      '<text x="' + (anchor === 'end' ? gx - 6 : anchor === 'start' ? gx + 6 : gx) + '" y="' + ty + '" fill="#f2c14e" font-size="24" font-weight="700" text-anchor="' + anchor + '">Ty</text>';
    $('chart').innerHTML = svg;
  }

  var last = null;
  function recalc(){
    var isNet = $('kNet').checked, v = parseFloat($('amount').value);
    $('amountLbl').textContent = isNet ? 'Twoje wynagrodzenie na rękę miesięcznie (zł)' : 'Twoje wynagrodzenie brutto miesięcznie (zł)';
    if (!isFinite(v) || v <= 0){ $('pct').textContent = '—'; $('pctNote').textContent = 'Wpisz kwotę.'; return; }
    var g = isNet ? grossFromNet(v) : v, n = isNet ? v : net(v), p = pctOf(g);
    var pr = p < 1 ? '<1' : p > 99 ? '>99' : Math.round(p);
    $('pct').textContent = pr + '%';
    $('pctNote').textContent = 'pracujących w Polsce · ' + (isNet ? 'Na rękę ' + fmt(n) + ' to ok. ' + fmt(g) + ' brutto' : fmt(g) + ' brutto to ok. ' + fmt(n) + ' na rękę') + ' · dane GUS, maj 2026';
    $('medLbl').textContent = g >= MED ? 'Ponad medianą o' : 'Do mediany brakuje';
    $('medDiff').textContent = fmt(Math.abs(g - MED));
    $('topLbl').textContent = g >= D9 ? 'Jesteś w najlepiej zarabiających 10%' : 'Do najlepiej zarabiających 10%';
    $('topDiff').textContent = g >= D9 ? '✓' : fmt(D9 - g);
    drawChart(g);
    var w = [];
    if (g < 4806) w.push('To mniej niż płaca minimalna za pełny etat (4806 zł brutto w 2026 r., 4950 zł w 2027 r.) — taka kwota dotyczy niepełnego etatu.');
    if (g >= MED && g < AVG) w.push('Ciekawostka: zarabiasz więcej niż połowa pracujących, a mimo to mniej niż „średnia krajowa” (9178 zł). Średnią zawyżają najwyższe pensje — mniej niż średnią zarabia ok. 65% osób.');
    $('warn').hidden = !w.length; $('warn').textContent = w.join(' ');
    last = {p: pr, g: g};
  }
  $('shareBtn').addEventListener('click', function(){
    if (!last) return;
    var url = 'https://bartuniadev.github.io/madry-portfel/narzedzia/czy-dobrze-zarabiam.html';
    var text = 'Zarabiam więcej niż ' + last.p + '% pracujących w Polsce (dane GUS). Sprawdź, gdzie jesteś Ty:';
    var st = $('shareStatus');
    if (navigator.share){ navigator.share({title: 'Czy dobrze zarabiam?', text: text, url: url}).catch(function(){}); return; }
    var full = text + ' ' + url;
    if (navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(full).then(function(){ st.textContent = 'Skopiowano — wklej znajomym lub w social media.'; }, function(){ st.textContent = full; });
    } else st.textContent = full;
  });
  ['amount','kGross','kNet'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  document.querySelectorAll('.preset-btn').forEach(function(b){ b.addEventListener('click', function(){ $('kGross').checked = true; $('amount').value = b.getAttribute('data-v'); recalc(); }); });
  recalc();'''
css = '''  .dist-chart{width:100%;height:auto;display:block;margin:4px 0 6px;font-family:system-ui,sans-serif;}
  .chart-note{font-size:0.8rem;color:var(--text-2);margin:0 0 16px;}
  .share-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:18px;}
  .share-row .download-btn{border:0;cursor:pointer;font-family:inherit;}
  .share-row .hint{font-size:0.82rem;color:var(--text-2);overflow-wrap:anywhere;}
  .sum-warning{margin-top:16px;}
'''
print('zarobki', make_tool.build('czy-dobrze-zarabiam',
  'Czy dobrze zarabiam? Twoja pensja na tle Polaków',
  'Czy dobrze zarabiam? Wpisz pensję brutto lub netto i sprawdź, ile procent Polaków zarabia mniej od Ciebie — według najnowszych danych GUS o rozkładzie wynagrodzeń.',
  'Czy dobrze zarabiam? Pensja na tle Polaków', 'czy dobrze zarabiam, ile zarabiają Polacy, mediana wynagrodzeń 2026, zarobki na tle Polaków',
  'Czy dobrze zarabiam?', 'Czy dobrze zarabiam? Twoja pensja na tle Polaków',
  'Wpisz swoją pensję i sprawdź, ile procent pracujących w Polsce zarabia mniej od Ciebie — na podstawie najnowszych danych GUS o rozkładzie wynagrodzeń. Nic nie jest wysyłane: liczy się w Twojej przeglądarce.',
  main_inner, trust, more, script, css))
