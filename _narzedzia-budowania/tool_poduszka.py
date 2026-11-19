import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <p class="field-title">Niezbędne wydatki miesięcznie — to, co musisz zapłacić nawet bez pracy</p>
    <div class="split-controls two">
      <div class="field"><label for="eHome">Czynsz lub rata kredytu</label><input type="number" id="eHome" inputmode="decimal" value="1800" min="0" step="50"></div>
      <div class="field"><label for="eBills">Rachunki i telefon</label><input type="number" id="eBills" inputmode="decimal" value="350" min="0" step="10"></div>
      <div class="field"><label for="eFood">Jedzenie i chemia</label><input type="number" id="eFood" inputmode="decimal" value="1000" min="0" step="50"></div>
      <div class="field"><label for="eTrans">Transport</label><input type="number" id="eTrans" inputmode="decimal" value="300" min="0" step="50"></div>
      <div class="field"><label for="eDebt">Raty i inne zobowiązania</label><input type="number" id="eDebt" inputmode="decimal" value="0" min="0" step="50"></div>
      <div class="field"><label for="eOther">Inne niezbędne (leki, ubezpieczenia)</label><input type="number" id="eOther" inputmode="decimal" value="150" min="0" step="50"></div>
    </div>

    <p class="field-title" id="sitLabel">Twoja sytuacja</p>
    <div class="type-toggle" role="radiogroup" aria-labelledby="sitLabel">
      <label><input type="radio" name="sit" id="sitDual" value="3"><span>Etat, dwie pensje w domu</span></label>
      <label><input type="radio" name="sit" id="sitSingle" value="4" checked><span>Etat, jedna pensja</span></label>
      <label><input type="radio" name="sit" id="sitIrr" value="6"><span>B2B, zlecenia lub nieregularne dochody</span></label>
    </div>
    <div class="checks">
      <div class="field check"><label><input type="checkbox" id="kids"> Mam dzieci lub osoby na utrzymaniu (+1 miesiąc)</label></div>
      <div class="field check"><label><input type="checkbox" id="mortgage"> Spłacam kredyt hipoteczny (+1 miesiąc)</label></div>
    </div>

    <div class="split-controls two">
      <div class="field"><label for="have">Ile już masz odłożone (zł)</label><input type="number" id="have" inputmode="decimal" value="2000" min="0" step="500"></div>
      <div class="field"><label for="monthly">Ile możesz odkładać miesięcznie (zł)</label><input type="number" id="monthly" inputmode="decimal" value="600" min="0" step="50"></div>
    </div>

    <div class="net-box">
      <span class="label">Twoja poduszka finansowa</span>
      <span class="net-amount" id="target">0 zł</span>
      <span class="pct" id="targetNote"></span>
    </div>

    <div class="progress" role="img" id="progWrap" aria-label="Postęp"><i id="prog"></i></div>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Brakuje</span>
        <span class="amount" id="missing">0 zł</span>
        <span class="pct" id="missingNote"></span>
      </div>
      <div class="result-card needs">
        <span class="label">Uzbierasz za</span>
        <span class="amount" id="time">—</span>
        <span class="pct" id="timeNote"></span>
      </div>
      <div class="result-card savings">
        <span class="label">Żeby zdążyć w rok</span>
        <span class="amount" id="perYear">0 zł</span>
        <span class="pct">odkładaj miesięcznie</span>
      </div>
    </div>

    <div class="verdict" id="verdict" aria-live="polite"></div>'''
trust = ('poduszka finansowa to pieniądze na utratę pracy, chorobę albo nagły duży wydatek — liczymy ją jako wielokrotność niezbędnych wydatków, nie całej pensji. '
 'Punkt wyjścia: 3 miesiące przy dwóch pensjach na etacie, 4 przy jednej, 6 przy nieregularnych dochodach; doliczamy po miesiącu przy osobach na utrzymaniu i kredycie hipotecznym. '
 'Na start warto mieć choćby 1000–2000 zł na drobne awarie. Poduszkę trzymaj tam, skąd wypłacisz ją w jeden dzień bez straty: na koncie oszczędnościowym lub krótkiej lokacie, nie w akcjach. '
 'Czas uzbierania nie uwzględnia odsetek.')
more = ('<a href="../artykuly/poduszka-finansowa.html">Poduszka finansowa — ile odłożyć i jak zacząć →</a><br>'
        '<a href="kalkulator-lokaty.html">Kalkulator lokaty — gdzie trzymać poduszkę →</a><br>'
        '<a href="../artykuly/kolejnosc-finansowych-priorytetow.html">Kolejność finansowych priorytetów →</a>')
script = r'''  function $(id){ return document.getElementById(id); }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function num(id){ var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : 0; }
  var MONTHS = ['styczniu','lutym','marcu','kwietniu','maju','czerwcu','lipcu','sierpniu','wrześniu','październiku','listopadzie','grudniu'];
  function recalc(){
    var exp = num('eHome') + num('eBills') + num('eFood') + num('eTrans') + num('eDebt') + num('eOther');
    var sit = document.querySelector('input[name="sit"]:checked');
    var months = (sit ? +sit.value : 4) + ($('kids').checked ? 1 : 0) + ($('mortgage').checked ? 1 : 0);
    var target = exp * months, have = num('have'), monthly = num('monthly');
    var missing = Math.max(0, target - have), pct = target > 0 ? Math.min(100, have / target * 100) : 0;
    $('target').textContent = fmt(target);
    $('targetNote').textContent = months + ' × niezbędne wydatki (' + fmt(exp) + ' miesięcznie)';
    $('prog').style.width = pct + '%';
    $('progWrap').setAttribute('aria-label', 'Masz ' + Math.round(pct) + '% poduszki');
    $('missing').textContent = fmt(missing);
    $('missingNote').textContent = 'masz ' + Math.round(pct) + '% celu';
    $('perYear').textContent = fmt(missing / 12);
    var v = $('verdict');
    if (missing <= 0){
      $('time').textContent = 'gotowe'; $('timeNote').textContent = 'poduszka jest pełna';
      v.textContent = 'Masz pełną poduszkę. Kolejne oszczędności możesz kierować na cele długoterminowe — np. IKE, IKZE lub OKI.';
      return;
    }
    if (monthly <= 0){
      $('time').textContent = '—'; $('timeNote').textContent = 'wpisz, ile odkładasz';
      v.textContent = 'Zacznij od stałego przelewu w dniu wypłaty — nawet 100 zł miesięcznie to 1200 zł w rok.';
      return;
    }
    var n = Math.ceil(missing / monthly), d = new Date(); d.setMonth(d.getMonth() + n);
    function mies(k){ return k === 1 ? 'miesiąc' : (k % 10 >= 2 && k % 10 <= 4 && (k % 100 < 12 || k % 100 > 14)) ? 'miesiące' : 'miesięcy'; }
    function lata(y){ if (y % 1 !== 0) return String(y).replace('.', ',') + ' roku'; return y + (y === 1 ? ' rok' : (y % 10 >= 2 && y % 10 <= 4 && (y % 100 < 12 || y % 100 > 14)) ? ' lata' : ' lat'); }
    $('time').textContent = n <= 24 ? n + ' ' + mies(n) : lata(Math.round(n / 12 * 10) / 10);
    $('timeNote').textContent = 'w ' + MONTHS[d.getMonth()] + ' ' + d.getFullYear();
    var first = have < 1000 ? ' Najpierw uzbieraj 1000–2000 zł na drobne awarie — przy ' + fmt(monthly) + ' miesięcznie to ' + Math.max(1, Math.ceil((Math.min(2000, target) - have) / monthly)) + ' mies.' : '';
    v.textContent = (n > 36 ? 'To długo — spróbuj odkładać więcej albo obniżyć niezbędne wydatki. ' : 'Ustaw stały przelew na konto oszczędnościowe w dniu wypłaty, żeby się udało.') + first;
  }
  ['eHome','eBills','eFood','eTrans','eDebt','eOther','have','monthly','kids','mortgage','sitDual','sitSingle','sitIrr'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  recalc();'''
css = '''  .field-title{font-size:0.88rem;color:var(--text-2);font-weight:600;margin:6px 0 10px;}
  .checks{display:grid;grid-template-columns:repeat(2,1fr);gap:4px 16px;margin:0 0 6px;}
  .checks .field{margin-bottom:10px;}
  @media (max-width:560px){.checks{grid-template-columns:1fr;}}
  .progress{height:12px;border-radius:999px;background:var(--bg);border:1px solid var(--border);overflow:hidden;margin:0 0 18px;}
  .progress i{display:block;height:100%;background:var(--green);border-radius:999px;transition:width .2s ease;}
'''
print('poduszka', make_tool.build('kalkulator-poduszki-finansowej',
  'Kalkulator poduszki finansowej — ile odłożyć',
  'Kalkulator poduszki finansowej: ile pieniędzy odłożyć na czarną godzinę przy Twoich wydatkach i sytuacji zawodowej i za ile miesięcy ją uzbierasz.',
  'Kalkulator poduszki finansowej', 'kalkulator poduszki finansowej, ile odłożyć na czarną godzinę, fundusz awaryjny, poduszka finansowa ile',
  'Kalkulator poduszki finansowej', 'Kalkulator poduszki finansowej',
  'Ile pieniędzy odłożyć na czarną godzinę? Wpisz niezbędne wydatki i swoją sytuację — policzę cel poduszki finansowej i za ile miesięcy ją uzbierasz. Liczy się w Twojej przeglądarce.',
  main_inner, trust, more, script, css))
