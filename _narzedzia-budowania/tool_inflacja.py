import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool

years_opts = ''.join(f'<option value="{y}"{" selected" if y == 2015 else ""}>{y}</option>' for y in range(2000, 2026))
end_opts = ''.join(f'<option value="{y}"{" selected" if y == 2025 else ""}>{y}</option>' for y in range(2001, 2026)) + '<option value="2026">2026 (szacunek)</option>'

main_inner = f'''    <div class="split-controls">
      <div class="field">
        <label for="amount">Kwota (zł)</label>
        <input type="number" id="amount" inputmode="decimal" value="100" min="0" step="10">
      </div>
      <div class="field">
        <label for="from">Z roku</label>
        <select id="from">{years_opts}</select>
      </div>
      <div class="field">
        <label for="to">Do roku</label>
        <select id="to">{end_opts}</select>
      </div>
    </div>
    <div class="presets">
      <button type="button" class="preset-btn" data-f="2020" data-t="2025">Od pandemii (2020)</button>
      <button type="button" class="preset-btn" data-f="2015" data-t="2025">10 lat</button>
      <button type="button" class="preset-btn" data-f="2004" data-t="2025">Od wejścia do UE</button>
    </div>

    <div class="net-box">
      <span class="label" id="eqLabel">Tyle trzeba mieć dziś, żeby kupić to samo</span>
      <span class="net-amount" id="eq">0 zł</span>
      <span class="pct" id="eqNote"></span>
    </div>

    <svg id="chart" class="infl-chart" viewBox="0 0 640 260" role="img" aria-label="Wzrost cen rok po roku"></svg>

    <div class="results-grid">
      <div class="result-card savings">
        <span class="label">Ceny wzrosły łącznie o</span>
        <span class="amount" id="total">0%</span>
        <span class="pct" id="avg"></span>
      </div>
      <div class="result-card">
        <span class="label">Pieniądze trzymane w szufladzie</span>
        <span class="amount" id="real">0 zł</span>
        <span class="pct" id="realNote">tyle są dziś realnie warte</span>
      </div>
      <div class="result-card needs">
        <span class="label">Najwyższa inflacja w okresie</span>
        <span class="amount" id="peak">—</span>
        <span class="pct" id="peakNote"></span>
      </div>
    </div>

    <div class="share-row">
      <button type="button" class="download-btn" id="shareBtn">Udostępnij wynik</button>
      <span class="hint" id="shareStatus" aria-live="polite"></span>
    </div>
    <p class="sum-warning" id="warn" hidden></p>'''

trust = ('średnioroczne wskaźniki cen towarów i usług konsumpcyjnych GUS (inflacja CPI) za lata 2001–2025 — np. 14,4% w 2022 r., 11,4% w 2023 r. i 3,6% w 2024 i 2025 r. '
         'Kwotę mnożymy przez wzrost cen w kolejnych latach. Rok 2026 to szacunek na podstawie ostatniego odczytu (październik 2026 r.: 3,5% rok do roku) — pełny wynik GUS poda w styczniu 2027 r. '
         'Inflacja to średnia dla koszyka zakupów — Twoje wydatki mogły drożeć szybciej lub wolniej. '
         'Źródło: <a href="https://stat.gov.pl/obszary-tematyczne/ceny-handel/wskazniki-cen/wskazniki-cen-towarow-i-uslug-konsumpcyjnych-pot-inflacja-/roczne-wskazniki-cen-towarow-i-uslug-konsumpcyjnych/">GUS — roczne wskaźniki cen</a>.')

more = ('<a href="../artykuly/inflacja-a-twoje-pieniadze.html">Inflacja a Twoje pieniądze — jak się chronić →</a><br>'
        '<a href="../artykuly/obligacje-skarbowe-dla-poczatkujacych.html">Obligacje indeksowane inflacją →</a><br>'
        '<a href="kalkulator-lokaty.html">Kalkulator lokaty — zysk po inflacji →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  /* średnioroczne wskaźniki CPI GUS (rok poprzedni = 100), 2026 — szacunek */
  var CPI = {2001:105.5,2002:101.9,2003:100.8,2004:103.5,2005:102.1,2006:101.0,2007:102.5,2008:104.2,2009:103.5,2010:102.6,
    2011:104.3,2012:103.7,2013:100.9,2014:100.0,2015:99.1,2016:99.4,2017:102.0,2018:101.6,2019:102.3,2020:103.4,
    2021:105.1,2022:114.4,2023:111.4,2024:103.6,2025:103.6,2026:103.5};
  function fmt(n, d){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:d||0,maximumFractionDigits:d||0,useGrouping:'always'}).format(n) + ' zł'; }
  function pc(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:1}).format(n) + '%'; }
  var last = null;
  function draw(from, to){
    var W = 640, H = 260, L = 50, R = 14, T = 18, B = 34, pts = [], lvl = 100;
    pts.push([from, 100]);
    for (var y = from + 1; y <= to; y++){ lvl *= CPI[y] / 100; pts.push([y, lvl]); }
    var maxV = Math.max.apply(null, pts.map(function(p){ return p[1]; })), minV = Math.min(100, Math.min.apply(null, pts.map(function(p){ return p[1]; })));
    var top = Math.ceil(maxV / 10) * 10, bot = Math.floor(minV / 10) * 10;
    var sx = function(y){ return L + (to === from ? 0 : (y - from) / (to - from) * (W - L - R)); };
    var sy = function(v){ return T + (top - v) / (top - bot || 1) * (H - T - B); };
    var g = '';
    var step = (top - bot) > 100 ? 50 : (top - bot) > 40 ? 20 : 10;
    for (var v = bot; v <= top; v += step){ g += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + sy(v) + '" y2="' + sy(v) + '" stroke="#2b362f"/>' +
      '<text x="' + (L - 8) + '" y="' + (sy(v) + 6) + '" fill="#93a49a" font-size="17" text-anchor="end">' + v + '</text>'; }
    var line = pts.map(function(p, i){ return (i ? 'L' : 'M') + sx(p[0]).toFixed(1) + ' ' + sy(p[1]).toFixed(1); }).join(' ');
    var area = line + ' L' + sx(to) + ' ' + (H - B) + ' L' + sx(from) + ' ' + (H - B) + ' Z';
    var span = to - from, every = span > 16 ? 5 : span > 8 ? 2 : 1, labels = '';
    var ticks = [];
    for (var t = from; t <= to; t += every) ticks.push(t);
    if (ticks[ticks.length - 1] !== to){ if (to - ticks[ticks.length - 1] < every * 0.6 && ticks.length > 1) ticks.pop(); ticks.push(to); }
    ticks.forEach(function(t, i){ var anchor = i === 0 ? 'start' : i === ticks.length - 1 ? 'end' : 'middle';
      labels += '<text x="' + sx(t) + '" y="' + (H - 8) + '" fill="#93a49a" font-size="17" text-anchor="' + anchor + '">' + (t === 2026 ? '2026*' : t) + '</text>'; });
    var end = pts[pts.length - 1];
    $('chart').innerHTML = g + '<path d="' + area + '" fill="rgba(242,193,78,0.16)"/>' + '<path d="' + line + '" fill="none" stroke="#f2c14e" stroke-width="3.5" stroke-linejoin="round"/>' +
      '<circle cx="' + sx(end[0]) + '" cy="' + sy(end[1]) + '" r="6" fill="#f2c14e"/>' + labels;
  }
  function recalc(){
    var a = parseFloat($('amount').value), from = +$('from').value, to = +$('to').value;
    if (!isFinite(a) || a < 0) a = 0;
    var w = [];
    Array.prototype.forEach.call($('to').options, function(o){ o.disabled = +o.value <= from; });
    if (to <= from){ to = Math.min(2025, from + 1); if (to <= from) to = 2026; $('to').value = String(to); }
    var f = 1, peak = 0, peakY = null;
    for (var y = from + 1; y <= to; y++){ f *= CPI[y] / 100; if (CPI[y] - 100 > peak){ peak = CPI[y] - 100; peakY = y; } }
    var eq = a * f, real = a / f, n = to - from, avg = (Math.pow(f, 1 / n) - 1) * 100;
    $('eqLabel').textContent = 'Tyle trzeba mieć w ' + (to === 2026 ? '2026 r.' : to + ' r.') + ', żeby kupić to, co w ' + from + ' r. za ' + fmt(a);
    $('eq').textContent = fmt(eq, eq < 1000 ? 2 : 0);
    $('eqNote').textContent = fmt(a) + ' z ' + from + ' r. to w ' + to + ' r. ok. ' + fmt(eq) + (to === 2026 ? ' (2026 — szacunek)' : '');
    $('total').textContent = '+' + pc((f - 1) * 100);
    $('avg').textContent = 'średnio ' + pc(avg) + ' rocznie przez ' + n + (n === 1 ? ' rok' : (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14)) ? ' lata' : ' lat');
    $('real').textContent = fmt(real, real < 1000 ? 2 : 0);
    $('realNote').textContent = 'siła nabywcza ' + fmt(a) + ' trzymanych bez oprocentowania od ' + from + ' r.';
    $('peak').textContent = peakY ? pc(peak) : '—';
    $('peakNote').textContent = peakY ? 'w ' + peakY + ' r.' : '';
    if (to === 2026) w.push('Rok 2026 jest szacunkiem — GUS poda średnią inflację za cały rok w styczniu 2027 r.');
    $('warn').hidden = !w.length; $('warn').textContent = w.join(' ');
    draw(from, to);
    last = {a: a, from: from, to: to, eq: eq};
  }
  $('shareBtn').addEventListener('click', function(){
    if (!last) return;
    var url = 'https://bartuniadev.github.io/madry-portfel/narzedzia/kalkulator-inflacji.html';
    var text = fmt(last.a) + ' z ' + last.from + ' r. to w ' + last.to + ' r. aż ' + fmt(last.eq) + ' — tyle trzeba mieć, żeby kupić to samo (dane GUS). Sprawdź swoją kwotę:';
    var st = $('shareStatus');
    if (navigator.share){ navigator.share({title: 'Kalkulator inflacji', text: text, url: url}).catch(function(){}); return; }
    var full = text + ' ' + url;
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(full).then(function(){ st.textContent = 'Skopiowano — wklej znajomym.'; }, function(){ st.textContent = full; });
    else st.textContent = full;
  });
  ['amount','from','to'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  document.querySelectorAll('.preset-btn').forEach(function(b){ b.addEventListener('click', function(){ $('from').value = b.getAttribute('data-f'); $('to').value = b.getAttribute('data-t'); recalc(); }); });
  recalc();'''

css = '''  .split-controls .field{min-width:0;}
  .split-controls select{width:100%;min-width:0;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 10px;font-size:1.05rem;font-family:inherit;min-height:46px;}
  .split-controls select:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  .infl-chart{width:100%;height:auto;display:block;margin:4px 0 16px;font-family:system-ui,sans-serif;}
  .share-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:18px;}
  .share-row .download-btn{border:0;cursor:pointer;font-family:inherit;}
  .share-row .hint{font-size:0.82rem;color:var(--text-2);overflow-wrap:anywhere;}
  .sum-warning{margin-top:16px;}
  @media (max-width:480px){.split-controls{grid-template-columns:1fr 1fr;} .split-controls .field:first-child{grid-column:1 / -1;}}
'''
print('inflacja', make_tool.build('kalkulator-inflacji',
    'Kalkulator inflacji — ile są warte pieniądze z lat',
    'Kalkulator inflacji GUS: ile dziś trzeba mieć, żeby kupić to samo co za 100 zł w 2015 czy 2020 r., ile straciły oszczędności i jak rosły ceny od 2000 r.',
    'Kalkulator inflacji', 'kalkulator inflacji, ile warte są pieniądze, inflacja od 2015, siła nabywcza pieniądza',
    'Kalkulator inflacji', 'Kalkulator inflacji — ile są warte Twoje pieniądze',
    'Ile dziś trzeba mieć, żeby kupić to, co kiedyś za 100 zł? Wybierz lata — policzę wzrost cen według oficjalnych danych GUS i to, ile straciły pieniądze trzymane bez oprocentowania. Liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, css))
