import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <div class="split-controls two">
      <div class="field">
        <label for="incA">Dochód netto osoby 1 (zł miesięcznie)</label>
        <input type="number" id="incA" inputmode="decimal" value="7000" min="0" step="100">
      </div>
      <div class="field">
        <label for="incB">Dochód netto osoby 2 (zł miesięcznie)</label>
        <input type="number" id="incB" inputmode="decimal" value="4500" min="0" step="100">
      </div>
    </div>
    <p class="field-title">Wspólne koszty miesięcznie</p>
    <div class="split-controls two">
      <div class="field"><label for="cHome">Czynsz lub rata kredytu</label><input type="number" id="cHome" inputmode="decimal" value="2400" min="0" step="50"></div>
      <div class="field"><label for="cBills">Rachunki: prąd, gaz, internet, telefon</label><input type="number" id="cBills" inputmode="decimal" value="450" min="0" step="10"></div>
      <div class="field"><label for="cFood">Jedzenie i chemia</label><input type="number" id="cFood" inputmode="decimal" value="1600" min="0" step="50"></div>
      <div class="field"><label for="cOther">Inne wspólne: auto, wyjścia, zwierzę</label><input type="number" id="cOther" inputmode="decimal" value="600" min="0" step="50"></div>
      <div class="field"><label for="cSave">Wspólne oszczędzanie</label><input type="number" id="cSave" inputmode="decimal" value="1000" min="0" step="100"><span class="hint">Np. poduszka, wakacje, wkład własny.</span></div>
    </div>

    <div class="net-box">
      <span class="label">Wspólny budżet miesięcznie</span>
      <span class="net-amount" id="total">0 zł</span>
      <span class="pct" id="totalNote"></span>
    </div>

    <div class="methods" id="methods"></div>
    <p class="cmp-note">Wkład — przelew na wspólne konto co miesiąc. Zostaje — pieniądze tylko dla siebie po opłaceniu wspólnych kosztów.</p>

    <div class="verdict" id="verdict" aria-live="polite"></div>
    <p class="sum-warning" id="warn" hidden></p>'''
trust = ('trzy najczęstsze sposoby dzielenia wspólnych kosztów. <strong>Po równo</strong> — każde wpłaca połowę. '
 '<strong>Proporcjonalnie do dochodów</strong> — każde wpłaca taki sam procent swojej pensji, więc osoba zarabiająca więcej dokłada więcej. '
 '<strong>Równe kieszonkowe</strong> — po opłaceniu wspólnych kosztów obojgu zostaje tyle samo pieniędzy dla siebie. '
 'Żaden sposób nie jest jedynym słusznym — ważne, żeby oboje go rozumieli i akceptowali. Najlepiej działa wspólne konto na stałe koszty i osobne konta na wydatki własne.')
more = ('<a href="../artykuly/wspolne-finanse-w-zwiazku.html">Wspólne finanse w związku — jak się dogadać →</a><br>'
        '<a href="kalkulator-budzetu.html">Kalkulator budżetu 50/30/20 →</a><br>'
        '<a href="../artykuly/ile-kosztuje-wesele.html">Ile kosztuje wesele →</a>')
script = r'''  function $(id){ return document.getElementById(id); }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function num(id){ var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : 0; }
  function recalc(){
    var a = num('incA'), b = num('incB');
    var total = num('cHome') + num('cBills') + num('cFood') + num('cOther') + num('cSave');
    var inc = a + b;
    $('total').textContent = fmt(total);
    $('totalNote').textContent = inc > 0 ? Math.round(total / inc * 100) + '% Waszych łącznych dochodów (' + fmt(inc) + ')' : '';
    var shA = inc > 0 ? a / inc : 0.5;
    var m = [
      {name: 'Po równo (50/50)', ca: total / 2, cb: total / 2},
      {name: 'Proporcjonalnie (' + Math.round(shA * 100) + '/' + (100 - Math.round(shA * 100)) + ')', ca: total * shA, cb: total * (1 - shA), best: true},
      {name: 'Równe kieszonkowe', ca: a - (inc - total) / 2, cb: b - (inc - total) / 2}
    ];
    $('methods').innerHTML = m.map(function(x){
      var la = a - x.ca, lb = b - x.cb;
      var cell = function(lbl, v){ return '<div><span>' + lbl + '</span><b' + (v < 0 ? ' class="neg"' : '') + '>' + fmt(v) + '</b></div>'; };
      return '<section class="method' + (x.best ? ' best' : '') + '"><h2>' + x.name + (x.best ? ' <em>najczęstszy wybór</em>' : '') + '</h2><div class="mgrid">' +
        cell('Wkład osoby 1', x.ca) + cell('Wkład osoby 2', x.cb) + cell('Zostaje osobie 1', la) + cell('Zostaje osobie 2', lb) + '</div></section>';
    }).join('');
    var eq = m[0], pr = m[1];
    var v = $('verdict');
    if (inc <= 0) v.textContent = 'Wpiszcie dochody, żeby porównać sposoby podziału.';
    else if (Math.abs(a - b) < 1) v.textContent = 'Zarabiacie tyle samo, więc wszystkie trzy sposoby dają ten sam wynik: każde wpłaca ' + fmt(total / 2) + '.';
    else {
      var richer = a > b ? '1' : '2', poorer = a > b ? '2' : '1';
      var leftEqP = (a > b ? b - eq.cb : a - eq.ca), leftPrP = (a > b ? b - pr.cb : a - pr.ca);
      v.textContent = 'Przy podziale po równo osobie ' + poorer + ' zostaje ' + fmt(leftEqP) + ' dla siebie, a przy proporcjonalnym — ' + fmt(leftPrP) + '. Proporcjonalny podział to najczęstszy kompromis: osoba ' + richer + ' dokłada więcej, ale nadal ma więcej dla siebie.';
    }
    var w = [];
    if (total > inc && inc > 0) w.push('Wspólne koszty są wyższe niż Wasze łączne dochody — żaden podział tego nie rozwiąże. Zacznijcie od przeglądu wydatków.');
    else if (m.some(function(x){ return a - x.ca < 0 || b - x.cb < 0; })) w.push('Przy niektórych sposobach jednej osobie nie wystarcza na wkład (kwoty na czerwono) — ten wariant odpada.');
    $('warn').hidden = !w.length; $('warn').textContent = w.join(' ');
  }
  ['incA','incB','cHome','cBills','cFood','cOther','cSave'].forEach(function(id){ $(id).addEventListener('input', recalc); });
  recalc();'''
css = '''  .field-title{font-size:0.88rem;color:var(--text-2);font-weight:600;margin:6px 0 10px;}
  .methods{display:grid;gap:10px;margin-bottom:8px;}
  .method{background:var(--bg);border:1px solid var(--border);border-radius:10px;padding:12px 14px;}
  .method.best{border-color:var(--green);}
  .method h2{margin:0 0 8px;font-size:0.95rem;line-height:1.3;}
  .method h2 em{font-style:normal;font-size:0.72rem;font-weight:700;color:#08130d;background:var(--green);border-radius:999px;padding:2px 8px;margin-left:6px;vertical-align:1px;}
  .mgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;}
  .mgrid span{display:block;font-size:0.72rem;color:var(--text-2);}
  .mgrid b{font-family:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;font-size:0.98rem;}
  .mgrid b.neg{color:#ff8f7a;}
  @media (max-width:560px){.mgrid{grid-template-columns:1fr 1fr;}}
  .cmp-note{font-size:0.8rem;color:var(--text-2);margin:0 0 14px;}
'''
print('para', make_tool.build('kalkulator-podzialu-kosztow',
  'Podział kosztów w związku — kalkulator dla par',
  'Kalkulator podziału kosztów w związku: po równo, proporcjonalnie do zarobków czy równe kieszonkowe. Ile każde wpłaca na wspólne konto i ile zostaje dla siebie.',
  'Kalkulator podziału kosztów w związku', 'podział kosztów w związku, jak dzielić rachunki w związku, wspólne konto dla par, kalkulator dla par',
  'Podział kosztów w związku', 'Podział kosztów w związku — kalkulator dla par',
  'Po równo, proporcjonalnie do zarobków czy tak, żeby obojgu zostawało tyle samo? Wpiszcie dochody i wspólne koszty — zobaczycie, ile każde z Was przelewa na wspólne konto i ile zostaje dla siebie. Liczy się w przeglądarce, nic nie jest wysyłane.',
  main_inner, trust, more, script, css))
