import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <div class="type-toggle" role="radiogroup" aria-label="Rodzaj rat">
      <label><input type="radio" name="kind" id="kEq" value="eq" checked><span>Raty równe</span></label>
      <label><input type="radio" name="kind" id="kDec" value="dec"><span>Raty malejące</span></label>
    </div>
    <div class="split-controls two">
      <div class="field">
        <label for="amount">Kwota kredytu (zł)</label>
        <input type="number" id="amount" inputmode="decimal" value="400000" min="0" step="10000">
      </div>
      <div class="field">
        <label for="rate">Oprocentowanie roczne (%)</label>
        <input type="number" id="rate" inputmode="decimal" value="7" min="0" max="30" step="0.05">
        <span class="hint">Marża banku + wskaźnik (np. WIBOR/WIRON) albo stała stopa.</span>
      </div>
      <div class="field">
        <label for="years">Okres spłaty (lata)</label>
        <input type="number" id="years" inputmode="numeric" value="25" min="1" max="35" step="1">
      </div>
      <div class="field">
        <label for="fee">Prowizja (% kwoty)</label>
        <input type="number" id="fee" inputmode="decimal" value="0" min="0" max="20" step="0.1">
      </div>
      <div class="field">
        <label for="over">Nadpłata co miesiąc (zł)</label>
        <input type="number" id="over" inputmode="decimal" value="0" min="0" step="100">
        <span class="hint">Nadpłata skraca okres spłaty.</span>
      </div>
    </div>

    <div class="presets">
      <button type="button" class="preset-btn" data-p="400000,7,25,0">Hipoteka 400 000 zł / 25 lat</button>
      <button type="button" class="preset-btn" data-p="30000,12,5,3">Gotówkowy 30 000 zł / 5 lat</button>
      <button type="button" class="preset-btn" data-p="60000,9,7,2">Samochód 60 000 zł / 7 lat</button>
    </div>

    <div class="net-box">
      <span class="label" id="rataLabel">Miesięczna rata</span>
      <span class="net-amount" id="rata">0 zł</span>
      <span class="pct" id="rataNote"></span>
    </div>

    <div class="results-grid">
      <div class="result-card savings">
        <span class="label">Odsetki łącznie</span>
        <span class="amount" id="interest">0 zł</span>
        <span class="pct" id="interestNote"></span>
      </div>
      <div class="result-card">
        <span class="label">Do oddania łącznie</span>
        <span class="amount" id="total">0 zł</span>
        <span class="pct">kapitał + odsetki + prowizja</span>
      </div>
      <div class="result-card needs">
        <span class="label">RRSO (ok.)</span>
        <span class="amount" id="rrso">0%</span>
        <span class="pct">z prowizją, bez ubezpieczeń</span>
      </div>
    </div>

    <div class="verdict" id="verdict" aria-live="polite"></div>

    <details class="tbl">
      <summary>Harmonogram spłaty rok po roku</summary>
      <div class="tbl-wrap">
      <table class="data-table">
        <caption>Kwoty w złotych, zaokrąglone. Z uwzględnieniem nadpłat.</caption>
        <thead><tr><th scope="col">Rok</th><th scope="col">Wpłacone</th><th scope="col">Odsetki</th><th scope="col">Zostało</th></tr></thead>
        <tbody id="schedule"></tbody>
      </table>
      </div>
    </details>

    <p class="sum-warning" id="warn" hidden></p>'''
trust = ('oprocentowanie stałe przez cały okres (przy zmiennej stopie rata zmieni się razem z WIBOR/WIRON), odsetki naliczane co miesiąc od pozostałego kapitału. '
 '<strong>Raty równe</strong> — co miesiąc ta sama kwota; <strong>malejące</strong> — stała część kapitałowa i malejące odsetki. '
 'Nadpłata co miesiąc w całości zmniejsza kapitał i skraca okres. Od nadpłaty kredytu hipotecznego bank może pobrać opłatę tylko w pierwszych 3 latach (do 3% nadpłacanej kwoty). '
 'RRSO liczymy z harmonogramu bez nadpłat, z prowizją pobraną z góry. Nie uwzględniamy ubezpieczeń, wyceny nieruchomości ani opłat za prowadzenie konta — sprawdź je w formularzu informacyjnym banku.')
more = ('<a href="../artykuly/kredyt-hipoteczny-dla-poczatkujacych.html">Kredyt hipoteczny dla początkujących →</a><br>'
        '<a href="../artykuly/rrso-jak-czytac-oferte-pozyczki.html">RRSO — jak czytać ofertę pożyczki →</a><br>'
        '<a href="kalkulator-splaty-dlugow.html">Kalkulator spłaty długów — lawina i kula śnieżna →</a>')
script = r'''  function $(id){ return document.getElementById(id); }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(n) + ' zł'; }
  function fmt0(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)); }
  function pct(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2}).format(n) + '%'; }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function num(id, d){ var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : d; }

  /* harmonogram miesięczny; zwraca listę płatności i odsetki */
  function schedule(K, r, n, dec, over){
    var i = r / 12, bal = K, rows = [], annuity = i > 0 ? K * i / (1 - Math.pow(1 + i, -n)) : K / n, capPart = K / n;
    for (var m = 1; m <= n && bal > 0.005; m++){
      var interest = r2(bal * i);
      var principal = dec ? capPart : annuity - interest;
      principal = Math.min(bal, principal);
      var extra = Math.min(bal - principal, over);
      bal = r2(bal - principal - extra);
      rows.push({pay: r2(principal + interest), extra: extra, interest: interest, bal: bal});
    }
    return rows;
  }
  /* RRSO: roczna stopa, przy której wartość bieżąca rat = kwota wypłacona (kwota − prowizja) */
  function rrso(paid, payments){
    var lo = 0, hi = 2;
    for (var k = 0; k < 80; k++){
      var mid = (lo + hi) / 2, pv = 0;
      for (var m = 0; m < payments.length; m++) pv += payments[m] / Math.pow(1 + mid, (m + 1) / 12);
      if (pv > paid) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2 * 100;
  }

  function recalc(){
    var K = num('amount', 0), r = num('rate', 0) / 100, years = Math.max(1, Math.min(35, Math.round(num('years', 1))));
    var n = years * 12, dec = $('kDec').checked, fee = K * num('fee', 0) / 100, over = num('over', 0);
    if (K <= 0){ return; }
    var base = schedule(K, r, n, dec, 0), plan = over > 0 ? schedule(K, r, n, dec, over) : base;
    var alt = schedule(K, r, n, !dec, 0);
    var sum = function(rows, k){ return rows.reduce(function(a, x){ return a + x[k]; }, 0); };
    var intBase = sum(base, 'interest'), intPlan = sum(plan, 'interest'), intAlt = sum(alt, 'interest');

    $('rataLabel').textContent = dec ? 'Pierwsza rata (raty malejące)' : 'Miesięczna rata';
    $('rata').textContent = fmt(base[0].pay);
    $('rataNote').textContent = dec ? 'ostatnia rata: ' + fmt(base[base.length - 1].pay) : (over > 0 ? '+ nadpłata ' + fmt(over) + ' miesięcznie' : n + ' rat');
    $('interest').textContent = fmt(intPlan);
    $('interestNote').textContent = over > 0 ? 'bez nadpłat: ' + fmt(intBase) : (dec ? 'przy ratach równych: ' + fmt(intAlt) : 'przy ratach malejących: ' + fmt(intAlt));
    $('total').textContent = fmt(K + intPlan + fee);
    $('rrso').textContent = pct(rrso(K - fee, base.map(function(x){ return x.pay; })));

    var v = $('verdict');
    if (over > 0){
      var saved = intBase - intPlan, months = base.length - plan.length;
      v.textContent = 'Nadpłacając ' + fmt(over) + ' miesięcznie, spłacisz kredyt o ' + Math.floor(months / 12) + ' lat i ' + (months % 12) + ' mies. szybciej i oszczędzisz ' + fmt(saved) + ' na odsetkach.';
    } else if (!dec){
      v.textContent = 'Raty malejące kosztowałyby ' + fmt(intAlt) + ' odsetek, czyli o ' + fmt(intBase - intAlt) + ' mniej — ale pierwsza rata byłaby wyższa: ' + fmt(alt[0].pay) + '.';
    } else {
      v.textContent = 'Przy ratach równych zapłaciłbyś ' + fmt(intAlt - intBase) + ' więcej odsetek, ale rata byłaby stała: ' + fmt(alt[0].pay) + '.';
    }

    var body = '', y = 0, paid = 0, ints = 0;
    plan.forEach(function(x, m){
      paid += x.pay + x.extra; ints += x.interest;
      if ((m + 1) % 12 === 0 || m === plan.length - 1){
        y++; body += '<tr><td>' + y + '</td><td>' + fmt0(paid) + '</td><td>' + fmt0(ints) + '</td><td>' + fmt0(x.bal) + '</td></tr>';
        paid = 0; ints = 0;
      }
    });
    $('schedule').innerHTML = body;

    var w = [];
    if (r > 0.25) w.push('Oprocentowanie powyżej 25% rocznie to sygnał ostrzegawczy — sprawdź, czy oferta nie przekracza ustawowych limitów odsetek i kosztów pozaodsetkowych.');
    $('warn').hidden = w.length === 0; $('warn').textContent = w.join(' ');
  }
  ['amount','rate','years','fee','over','kEq','kDec'].forEach(function(id){
    $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc);
  });
  document.querySelectorAll('.preset-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var p = btn.getAttribute('data-p').split(',');
      $('amount').value = p[0]; $('rate').value = p[1]; $('years').value = p[2]; $('fee').value = p[3]; $('over').value = 0; recalc();
    });
  });
  recalc();'''
n = make_tool.build('kalkulator-kredytu',
  'Kalkulator kredytu — rata, odsetki, nadpłata i RRSO',
  'Kalkulator kredytu hipotecznego i gotówkowego: rata równa i malejąca, odsetki łącznie, RRSO z prowizją i ile oszczędzisz na nadpłacie. Bez rejestracji.',
  'Kalkulator kredytu', 'kalkulator kredytu, kalkulator raty kredytu, kalkulator kredytu hipotecznego, kalkulator nadpłaty kredytu, raty równe czy malejące',
  'Kalkulator kredytu', 'Kalkulator kredytu: rata, odsetki i nadpłata',
  'Policz ratę kredytu hipotecznego lub gotówkowego, odsetki za cały okres i RRSO z prowizją. Porównaj raty równe i malejące i sprawdź, ile oszczędzisz, nadpłacając co miesiąc. Liczy się w Twojej przeglądarce.',
  main_inner, trust, more, script)
print('kredyt', n)
