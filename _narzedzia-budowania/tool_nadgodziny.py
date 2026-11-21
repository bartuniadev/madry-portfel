import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool

HOURS = {2026: [160, 160, 176, 168, 160, 168, 184, 160, 176, 176, 160, 160],
         2027: [152, 160, 176, 176, 144, 176, 176, 176, 176, 168, 160, 168]}
MONTHS = ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień']
opts = ''.join(f'<option value="{y}-{i}"{" selected" if (y, i) == (2026, 10) else ""}>{m} {y} — {HOURS[y][i]} godz.</option>'
               for y in (2026, 2027) for i, m in enumerate(MONTHS))

main_inner = f'''    <div class="split-controls two">
      <div class="field"><label for="g">Pensja brutto miesięcznie (zł)</label><input type="number" id="g" inputmode="decimal" value="7000" min="0" step="100"></div>
      <div class="field"><label for="m">Miesiąc (wymiar czasu pracy)</label><select id="m">{opts}</select></div>
    </div>
    <div class="split-controls two">
      <div class="field"><label for="h50">Nadgodziny z dodatkiem 50%</label><input type="number" id="h50" inputmode="decimal" value="10" min="0" max="200" step="1"><span class="hint">Zwykłe dni robocze — zostajesz dłużej po pracy.</span></div>
      <div class="field"><label for="h100">Nadgodziny z dodatkiem 100%</label><input type="number" id="h100" inputmode="decimal" value="0" min="0" max="200" step="1"><span class="hint">W nocy, w niedziele i święta wolne od pracy oraz w dniu wolnym za pracę w niedzielę lub święto.</span></div>
    </div>

    <div class="net-box">
      <span class="label">Za nadgodziny dostaniesz na rękę</span>
      <span class="net-amount" id="net">0 zł</span>
      <span class="pct" id="netNote"></span>
    </div>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Stawka godzinowa</span>
        <span class="amount" id="rate">0 zł</span>
        <span class="pct" id="rateNote"></span>
      </div>
      <div class="result-card needs">
        <span class="label">Nadgodziny brutto</span>
        <span class="amount" id="gross">0 zł</span>
        <span class="pct" id="grossNote"></span>
      </div>
      <div class="result-card savings">
        <span class="label">Wypłata w tym miesiącu</span>
        <span class="amount" id="total">0 zł</span>
        <span class="pct" id="totalNote"></span>
      </div>
    </div>
    <div class="verdict" id="verdict" aria-live="polite"></div>
    <p class="sum-warning" id="warn" hidden></p>'''

trust = ('<strong>Stawka godzinowa</strong> to pensja miesięczna podzielona przez wymiar czasu pracy w danym miesiącu (od 144 godzin w maju 2027 r. do 184 w lipcu 2026 r.) — dlatego ta sama nadgodzina jest warta różnie w różnych miesiącach. '
         '<strong>Za każdą nadgodzinę</strong> dostajesz zwykłe wynagrodzenie i dodatek (art. 151¹ Kodeksu pracy): 50% w zwykłe dni, 100% w nocy, w niedziele i święta wolne od pracy, w dniu wolnym za pracę w niedzielę lub święto oraz za przekroczenie przeciętnej tygodniowej normy. '
         'Zakładamy, że nadgodziny wykraczają poza miesięczny wymiar i nie odbierasz za nie wolnego — jeśli pracodawca da Ci czas wolny, dodatek nie przysługuje. '
         '<strong>Na rękę</strong> liczymy jak dodatek do pensji na umowie o pracę (składki, zdrowotna, podatek 12% z PIT-2, bez PPK). '
         'Limit to co do zasady 150 nadgodzin w roku, chyba że układ zbiorowy, regulamin lub umowa przewiduje inny.')

more = ('<a href="../artykuly/prawa-pracownika-w-liczbach.html">Prawa pracownika w liczbach — urlop, L4, nadgodziny →</a><br>'
        '<a href="../artykuly/dni-wolne-od-pracy-2027.html">Wymiar czasu pracy i dni wolne 2027 →</a><br>'
        '<a href="kalkulator-brutto-netto.html">Kalkulator brutto–netto 2026 i 2027 →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(r2(n)) + ' zł'; }
  function fmt0(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function num(id, max){ var v = parseFloat($(id).value); if (!isFinite(v) || v < 0) v = 0; return max != null ? Math.min(v, max) : v; }
  function ndg(n){ var a = Math.abs(n) % 100, b = a % 10; return n + ' ' + (n === 1 ? 'nadgodzina' : (n % 1 === 0 && b >= 2 && b <= 4 && (a < 12 || a > 14)) ? 'nadgodziny' : 'nadgodzin'); }
  var HOURS = ''' + str(HOURS).replace(' ', '').replace("2026", '"2026"').replace("2027", '"2027"') + r''';
  var MONTHS = ['styczniu','lutym','marcu','kwietniu','maju','czerwcu','lipcu','sierpniu','wrześniu','październiku','listopadzie','grudniu'];
  function netEtat(g){
    var zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245)), h = r2((g - zus) * 0.09);
    var tax = Math.max(0, Math.round(Math.max(0, Math.round(g - zus - 250)) * 0.12 - 300));
    return g - zus - h - tax;
  }
  function recalc(){
    var g = num('g'), sel = $('m').value.split('-'), y = sel[0], mi = parseInt(sel[1], 10), wym = HOURS[y][mi];
    var h50 = num('h50', 200), h100 = num('h100', 200);
    var rate = g / wym, ot = r2(h50 * rate * 1.5 + h100 * rate * 2);
    var netOt = Math.max(0, netEtat(g + ot) - netEtat(g));
    $('net').textContent = fmt(netOt);
    $('netNote').textContent = (h50 + h100) ? 'z ' + fmt(ot) + ' brutto' : 'wpisz liczbę nadgodzin';
    $('rate').textContent = fmt(rate);
    $('rateNote').textContent = fmt(g) + ' ÷ ' + wym + ' godz. w ' + MONTHS[mi];
    $('gross').textContent = fmt(ot);
    $('grossNote').textContent = (h50 ? h50 + ' × ' + fmt(rate * 1.5) : '') + (h50 && h100 ? ' + ' : '') + (h100 ? h100 + ' × ' + fmt(rate * 2) : '');
    $('total').textContent = fmt0(netEtat(g + ot));
    $('totalNote').textContent = 'na rękę, zamiast ' + fmt0(netEtat(g));
    var hrs = h50 + h100;
    $('verdict').textContent = hrs ? ndg(hrs) + ' w ' + MONTHS[mi] + ' ' + y + ' r. to ' + fmt0(netOt) + ' więcej na rękę — średnio ' + fmt(netOt / hrs) + ' za godzinę.' : '';
    var w = [];
    if (hrs > 150) w.push('Ponad 150 nadgodzin to więcej niż roczny limit z Kodeksu pracy (chyba że Twój układ zbiorowy, regulamin lub umowa przewiduje wyższy).');
    else if (hrs * 12 > 150) w.push('Przy takiej liczbie nadgodzin co miesiąc przekroczysz roczny limit 150 godzin po ok. ' + Math.floor(150 / hrs) + ' miesiącach.');
    $('warn').hidden = !w.length; $('warn').textContent = w.join(' ');
  }
  ['g','m','h50','h100'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  (function(){ var n = new Date(), k = n.getFullYear() + '-' + n.getMonth(); if ($('m').querySelector('option[value="' + k + '"]')) $('m').value = k; })();
  recalc();'''

css = '''  #m{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 10px;font-size:1rem;font-family:inherit;min-height:44px;}
  #m:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
'''
print('nadgodziny', make_tool.build('kalkulator-nadgodzin',
    'Kalkulator nadgodzin 2026 i 2027 — ile za nadgodziny',
    'Kalkulator nadgodzin: stawka godzinowa z wymiaru czasu pracy w danym miesiącu, dodatek 50% lub 100%, nadgodziny brutto i na rękę. Wymiar dla 2026 i 2027 r.',
    'Kalkulator nadgodzin', 'kalkulator nadgodzin, ile za nadgodziny, dodatek za nadgodziny 50% 100%, nadgodziny na rękę, stawka godzinowa',
    'Kalkulator nadgodzin', 'Kalkulator nadgodzin — ile dostaniesz za nadgodziny',
    'Wpisz pensję, miesiąc i liczbę nadgodzin — policzę stawkę godzinową z wymiaru czasu pracy, dodatek 50% lub 100% i to, ile z tego zostanie Ci na rękę. Wymiar godzin dla każdego miesiąca 2026 i 2027 r. Liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, css))
