import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool

main_inner = '''    <div class="split-controls two">
      <div class="field"><label for="g">Pensja brutto miesięcznie (zł)</label><input type="number" id="g" inputmode="decimal" value="7000" min="0" step="100"><span class="hint">Przy zmiennej pensji — średnia z ostatnich 12 miesięcy.</span></div>
      <div class="field"><label for="d">Dni na L4 w tym miesiącu</label><input type="number" id="d" inputmode="numeric" value="10" min="0" max="31" step="1"><span class="hint">Liczą się wszystkie dni kalendarzowe, także weekendy.</span></div>
    </div>

    <p class="field-title" id="rateLabel">Rodzaj zwolnienia</p>
    <div class="type-toggle" role="radiogroup" aria-labelledby="rateLabel">
      <label><input type="radio" name="rate" value="0.8" checked><span>Zwykłe L4 — 80%</span></label>
      <label><input type="radio" name="rate" value="1"><span>Ciąża lub wypadek w drodze do pracy — 100%</span></label>
    </div>

    <div class="net-box">
      <span class="label">Wypłata za ten miesiąc</span>
      <span class="net-amount" id="net">0 zł</span>
      <span class="pct" id="netNote"></span>
    </div>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Chorobowe brutto</span>
        <span class="amount" id="sick">0 zł</span>
        <span class="pct" id="sickNote"></span>
      </div>
      <div class="result-card needs">
        <span class="label">Pensja za dni w pracy</span>
        <span class="amount" id="work">0 zł</span>
        <span class="pct" id="workNote"></span>
      </div>
      <div class="result-card savings">
        <span class="label" id="lossLbl">Tracisz przez L4</span>
        <span class="amount" id="loss">0 zł</span>
        <span class="pct" id="lossNote"></span>
      </div>
    </div>
    <div class="verdict" id="verdict" aria-live="polite"></div>'''

trust = ('<strong>Podstawa</strong> chorobowego to przeciętna pensja brutto z ostatnich 12 miesięcy pomniejszona o 13,71% (Twoje składki emerytalna, rentowa i chorobowa). '
         'Za każdy dzień zwolnienia dostajesz 1/30 z 80% podstawy (100% w ciąży, po wypadku w drodze do pracy lub z pracy i przy badaniach dawcy). '
         'Pensję za ten miesiąc pomniejsza się o 1/30 za każdy dzień choroby. '
         '<strong>Od chorobowego</strong> nie płaci się składek emerytalnej, rentowej i chorobowej — tylko zdrowotną 9% i zaliczkę na podatek; wypłatę liczymy jak na umowie o pracę z PIT-2, bez PPK. '
         'Przez pierwsze 33 dni choroby w roku (14 dni po 50. roku życia) płaci pracodawca, potem ZUS wypłaca zasiłek w tej samej wysokości. '
         'Gdy większość miesiąca jesteś na L4, kadry mogą liczyć pensję za przepracowane dni godzinowo — wtedy wynik różni się o kilkadziesiąt złotych.')

more = ('<a href="../artykuly/prawa-pracownika-w-liczbach.html">Prawa pracownika w liczbach — urlop, L4, nadgodziny →</a><br>'
        '<a href="../artykuly/poduszka-finansowa.html">Poduszka finansowa — na wypadek choroby →</a><br>'
        '<a href="kalkulator-brutto-netto.html">Kalkulator brutto–netto 2026 i 2027 →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(r2(n)) + ' zł'; }
  function fmt0(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function num(id, max){ var v = parseFloat($(id).value); if (!isFinite(v) || v < 0) v = 0; return max != null ? Math.min(v, max) : v; }
  function dni(n){ return n === 1 ? 'dzień' : 'dni'; }
  /* wypłata w miesiącu: pensja za dni w pracy + wynagrodzenie chorobowe */
  function month(work, sick){
    var zus = r2(r2(work * 0.0976) + r2(work * 0.015) + r2(work * 0.0245));
    var h = r2((work - zus + sick) * 0.09);
    var tax = Math.max(0, Math.round(Math.max(0, Math.round(work - zus + sick - 250)) * 0.12 - 300));
    return {net: r2(work - zus + sick - h - tax), zus: zus, h: h, tax: tax};
  }
  function recalc(){
    var g = num('g'), d = Math.round(num('d', 31));
    var rate = parseFloat(document.querySelector('input[name="rate"]:checked').value);
    var base = r2(g * (1 - 0.1371)), daily = r2(base * rate / 30), sick = r2(daily * d);
    var work = d >= 30 ? 0 : r2(g - g / 30 * d);
    var m = month(work, sick), normal = month(g, 0);
    var loss = normal.net - m.net;
    $('net').textContent = fmt(m.net);
    $('netNote').textContent = 'zwykle ' + fmt(normal.net) + ' na rękę';
    $('sick').textContent = fmt(sick);
    $('sickNote').textContent = d ? fmt(daily) + ' za każdy dzień' : 'bez zwolnienia';
    $('work').textContent = fmt(work);
    $('workNote').textContent = d >= 30 ? 'cały miesiąc na L4' : 'pensja minus ' + d + '/30';
    var gain = loss < -0.5;
    $('lossLbl').textContent = gain ? 'Różnica' : 'Tracisz przez L4';
    $('loss').textContent = gain ? '+ ' + fmt0(-loss) : fmt0(Math.max(0, loss));
    $('lossNote').textContent = gain ? 'więcej niż zwykle — bez składek ZUS' : (d && g ? 'ok. ' + fmt0(Math.max(0, loss) / d) + ' za dzień L4' : '');
    var v = '';
    if (d && g){
      v = d + ' ' + dni(d) + ' na L4 ' + (rate === 1 ? '(100%)' : '(80%)') + (loss < -0.5 ? ' to ok. ' + fmt0(-loss) + ' więcej na rękę niż w zwykłym miesiącu. ' : ' to ok. ' + fmt0(Math.max(0, loss)) + ' mniej na rękę niż w zwykłym miesiącu. ');
      v += rate === 1 ? 'Przy 100% wypłata jest zbliżona do zwykłej, bo od chorobowego nie płaci się składek emerytalnej, rentowej i chorobowej.' : 'Na rękę tracisz mniej, niż sugeruje „80%”, bo od chorobowego nie płaci się składek emerytalnej, rentowej i chorobowej.';
      if (d > 14) v += ' Jeśli masz ponad 50 lat, po 14 dniach w roku zasiłek wypłaca już ZUS — w tej samej wysokości.';
    }
    $('verdict').textContent = v;
  }
  ['g','d'].forEach(function(id){ $(id).addEventListener('input', recalc); });
  document.querySelectorAll('input[name="rate"]').forEach(function(r){ r.addEventListener('change', recalc); });
  recalc();'''

print('l4', make_tool.build('kalkulator-l4',
    'Kalkulator L4 2026 i 2027 — ile dostanę na zwolnieniu',
    'Ile dostanę na L4? Policz chorobowe 80% lub 100%, pensję za dni w pracy i wypłatę na rękę w miesiącu ze zwolnieniem lekarskim — i ile tracisz za każdy dzień.',
    'Kalkulator L4 — wynagrodzenie chorobowe', 'kalkulator L4, ile dostanę na L4, wynagrodzenie chorobowe, zasiłek chorobowy kalkulator, chorobowe 80%',
    'Kalkulator L4', 'Kalkulator L4 — ile dostanę na zwolnieniu lekarskim',
    'Wpisz pensję i liczbę dni zwolnienia — policzę wynagrodzenie chorobowe, pensję za dni w pracy i wypłatę na rękę w miesiącu z L4. Zobaczysz też, ile kosztuje Cię każdy dzień choroby. Wszystko liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, ''))
