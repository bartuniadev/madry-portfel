import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <div class="type-toggle" role="radiogroup" aria-label="Rok">
      <label><input type="radio" name="year" id="y2026" value="2026" checked><span>2026</span></label>
      <label><input type="radio" name="year" id="y2027" value="2027"><span>2027</span></label>
    </div>
    <div class="field">
      <label for="gross">Kwota brutto z umowy zlecenia (zł miesięcznie)</label>
      <input type="number" id="gross" inputmode="decimal" value="3000" min="0" step="100">
    </div>
    <div class="split-controls two">
      <div class="field">
        <label for="rate">Stawka za godzinę (opcjonalnie)</label>
        <input type="number" id="rate" inputmode="decimal" placeholder="np. 32,30" min="0" step="0.1">
      </div>
      <div class="field">
        <label for="hours">Liczba godzin w miesiącu</label>
        <input type="number" id="hours" inputmode="numeric" placeholder="np. 80" min="0" step="1">
        <span class="hint">Wpisz stawkę i godziny — kwotę brutto policzymy sami.</span>
      </div>
    </div>

    <p class="field-title" id="statusLabel">Twoja sytuacja</p>
    <div class="type-toggle" role="radiogroup" aria-labelledby="statusLabel">
      <label><input type="radio" name="status" id="sStudent" value="student"><span>Student lub uczeń do 26 lat</span></label>
      <label><input type="radio" name="status" id="sOnly" value="only" checked><span>Zlecenie to moja jedyna praca</span></label>
      <label><input type="radio" name="status" id="sJob" value="job"><span>Mam też etat (co najmniej płaca minimalna)</span></label>
    </div>

    <div class="checks">
      <div class="field check" id="youngField">
        <label><input type="checkbox" id="young"> Nie mam jeszcze 26 lat (ulga dla młodych, PIT-0)</label>
      </div>
      <div class="field check" id="sickField">
        <label><input type="checkbox" id="sick" checked> Dobrowolne ubezpieczenie chorobowe (2,45%)</label>
      </div>
      <div class="field check" id="pit2Field">
        <label><input type="checkbox" id="pit2"> Złożyłem PIT-2 u tego zleceniodawcy (300 zł)</label>
      </div>
    </div>

    <div class="net-box">
      <span class="label">Na rękę z umowy zlecenia</span>
      <span class="net-amount" id="net">0 zł</span>
      <span class="pct" id="netPct"></span>
    </div>

    <table class="breakdown">
      <tbody>
        <tr><td>Składki społeczne (emerytalna, rentowa<span id="sickTxt">, chorobowa</span>)</td><td id="rZus">0 zł</td></tr>
        <tr><td>Składka zdrowotna (9%)</td><td id="rHealth">0 zł</td></tr>
        <tr><td>Koszty uzyskania przychodu (20%) — obniżają podatek</td><td id="rKup">0 zł</td></tr>
        <tr><td>Zaliczka na podatek dochodowy</td><td id="rTax">0 zł</td></tr>
        <tr class="total"><td>Wypłata netto</td><td id="rNet">0 zł</td></tr>
      </tbody>
    </table>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Netto za godzinę</span>
        <span class="amount" id="netHour">—</span>
        <span class="pct" id="netHourNote">wpisz liczbę godzin</span>
      </div>
      <div class="result-card">
        <span class="label">Netto rocznie</span>
        <span class="amount" id="netYear">0 zł</span>
        <span class="pct">12 × ta sama kwota</span>
      </div>
      <div class="result-card savings">
        <span class="label">Koszt zleceniodawcy (ok.)</span>
        <span class="amount" id="cost">0 zł</span>
        <span class="pct">ze składkami po jego stronie</span>
      </div>
    </div>

    <p class="sum-warning" id="warn" hidden></p>'''

trust = ('umowa zlecenia z zleceniodawcą, który nie jest Twoim pracodawcą. <strong>Student lub uczeń do 26 lat</strong> — bez składek ZUS i zdrowotnej, a dzięki uldze dla młodych bez podatku (do 85 528 zł przychodu rocznie). '
 '<strong>Jedyna praca</strong> — składki społeczne 9,76% + 1,5% (+ 2,45% chorobowa, jeśli ją wybierzesz) i zdrowotna 9%. '
 '<strong>Etat u innego pracodawcy</strong> z wynagrodzeniem co najmniej minimalnym — ze zlecenia tylko składka zdrowotna 9%. '
 'Koszty uzyskania przychodu 20% (od kwoty po składkach społecznych), zaliczka 12%, pomniejszona o 300 zł, jeśli złożyłeś PIT-2 u tego zleceniodawcy. '
 'Przy umowach do 200 zł brutto miesięcznie podatek pobiera się ryczałtem, więc wynik może się nieznacznie różnić. Minimalna stawka godzinowa: 31,40 zł w 2026 r. i 32,30 zł w 2027 r.')

more = ('<a href="../artykuly/dorabianie-po-godzinach.html">Jak dorobić do pensji legalnie →</a><br>'
        '<a href="../artykuly/brutto-netto-rodzaje-umow.html">Brutto, netto i rodzaje umów →</a><br>'
        '<a href="kalkulator-brutto-netto.html">Kalkulator brutto–netto dla umowy o pracę →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(n) + ' zł'; }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  var MIN_RATE = {2026: 31.40, 2027: 32.30}, MIN_WAGE = {2026: 4806, 2027: 4950};

  function fromHours(){
    var rate = parseFloat($('rate').value), h = parseFloat($('hours').value);
    if (isFinite(rate) && rate > 0 && isFinite(h) && h > 0) $('gross').value = r2(rate * h);
  }

  function recalc(){
    var gross = parseFloat($('gross').value); if (!isFinite(gross) || gross < 0) gross = 0;
    var year = $('y2027').checked ? 2027 : 2026;
    var status = $('sStudent').checked ? 'student' : ($('sJob').checked ? 'job' : 'only');
    $('youngField').hidden = status === 'student';
    $('sickField').hidden = status !== 'only';
    var young = status === 'student' || $('young').checked;
    $('pit2Field').hidden = young;
    var sick = status === 'only' && $('sick').checked;

    var social = 0, health = 0;
    if (status === 'only'){
      social = r2(gross * 0.0976) + r2(gross * 0.015) + (sick ? r2(gross * 0.0245) : 0);
      social = r2(social);
    }
    if (status !== 'student') health = r2((gross - social) * 0.09);
    var kup = r2((gross - social) * 0.2);
    var tax = 0;
    if (!young){
      var base = Math.max(0, Math.round(gross - social - kup));
      tax = Math.max(0, Math.round(base * 0.12 - ($('pit2').checked ? 300 : 0)));
    }
    var net = Math.max(0, r2(gross - social - health - tax));
    var cost = gross;
    if (status === 'only'){
      cost = gross * (1 + 0.0976 + 0.065 + 0.0167 + 0.001 + (gross >= MIN_WAGE[year] ? 0.0245 : 0));
    }

    $('sickTxt').hidden = !sick;
    $('net').textContent = fmt(net);
    $('netPct').textContent = gross > 0 ? Math.round(net / gross * 100) + '% kwoty brutto' : '';
    $('rZus').textContent = status === 'only' ? '− ' + fmt(social) : '0,00 zł (nie dotyczy)';
    $('rHealth').textContent = status === 'student' ? '0,00 zł (nie dotyczy)' : '− ' + fmt(health);
    $('rKup').textContent = young ? '—' : fmt(kup);
    $('rTax').textContent = young ? '0,00 zł (ulga dla młodych)' : '− ' + fmt(tax);
    $('rNet').textContent = fmt(net);
    $('netYear').textContent = fmt(net * 12);
    $('cost').textContent = fmt(cost);
    var h = parseFloat($('hours').value);
    if (isFinite(h) && h > 0){ $('netHour').textContent = fmt(net / h); $('netHourNote').textContent = 'przy ' + h + ' godz. w miesiącu'; }
    else { $('netHour').textContent = '—'; $('netHourNote').textContent = 'wpisz liczbę godzin'; }

    var w = [], rate = parseFloat($('rate').value);
    if (!(isFinite(rate) && rate > 0) && isFinite(h) && h > 0) rate = gross / h;
    if (isFinite(rate) && rate > 0 && rate + 0.001 < MIN_RATE[year])
      w.push('Stawka ' + fmt(rate) + ' za godzinę jest niższa od minimalnej stawki godzinowej w ' + year + ' r. (' + fmt(MIN_RATE[year]) + ' brutto). Zleceniodawca musi zapłacić co najmniej tyle.');
    if (young && gross * 12 > 85528)
      w.push('Przy tej kwocie roczny przychód przekroczy limit ulgi dla młodych (85 528 zł) — od tego momentu zleceniodawca zacznie pobierać zaliczki na podatek.');
    if (status === 'student')
      w.push('Status studenta kończy się z dniem ukończenia studiów (obrony) lub skreślenia z listy studentów, a zwolnienie z ZUS — także w dniu 26. urodzin.');
    $('warn').hidden = w.length === 0; $('warn').textContent = w.join(' ');
  }

  ['rate','hours'].forEach(function(id){ $(id).addEventListener('input', function(){ fromHours(); recalc(); }); });
  ['gross','young','sick','pit2','y2026','y2027','sStudent','sOnly','sJob'].forEach(function(id){
    $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc);
  });
  if (new Date() >= new Date(2027, 0, 1)) $('y2027').checked = true;
  recalc();'''

css = '''  .field-title{font-size:0.88rem;color:var(--text-2);font-weight:600;margin:4px 0 8px;}
  .checks{display:grid;grid-template-columns:repeat(2,1fr);gap:4px 16px;margin:0 0 6px;}
  .checks .field{margin-bottom:10px;}
  @media (max-width:560px){.checks{grid-template-columns:1fr;}}
'''
n = make_tool.build('kalkulator-umowy-zlecenia',
  'Kalkulator umowy zlecenia 2027 i 2026 — ile na rękę',
  'Kalkulator umowy zlecenia 2026 i 2027: ile na rękę dla studenta do 26 lat, przy jedynej pracy i przy etacie. Składki, podatek, stawka godzinowa.',
  'Kalkulator umowy zlecenia', 'kalkulator umowy zlecenia, umowa zlecenie ile na rękę, zlecenie student kalkulator, minimalna stawka godzinowa 2027',
  'Kalkulator umowy zlecenia', 'Kalkulator umowy zlecenia 2027 i 2026',
  'Ile zostanie na rękę z umowy zlecenia — dla studenta do 26 lat, gdy zlecenie to Twoja jedyna praca i gdy masz też etat. Z kontrolą minimalnej stawki godzinowej. Liczy się w Twojej przeglądarce.',
  main_inner, trust, more, script, css)
print('zlecenie', n)
