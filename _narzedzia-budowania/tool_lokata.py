import sys; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool
main_inner = '''    <div class="type-toggle" role="radiogroup" aria-label="Rodzaj produktu">
      <label><input type="radio" name="kind" id="kDep" value="dep" checked><span>Lokata</span></label>
      <label><input type="radio" name="kind" id="kAcc" value="acc"><span>Konto oszczędnościowe (kapitalizacja co miesiąc)</span></label>
    </div>
    <div class="split-controls two">
      <div class="field">
        <label for="amount">Kwota (zł)</label>
        <input type="number" id="amount" inputmode="decimal" value="10000" min="0" step="1000">
      </div>
      <div class="field">
        <label for="rate">Oprocentowanie roczne (%)</label>
        <input type="number" id="rate" inputmode="decimal" value="5" min="0" max="30" step="0.1">
      </div>
      <div class="field" id="termField">
        <label for="term">Okres lokaty (miesiące)</label>
        <input type="number" id="term" inputmode="numeric" value="3" min="1" max="120" step="1">
      </div>
      <div class="field">
        <label for="years">Jak długo oszczędzasz (lata)</label>
        <input type="number" id="years" inputmode="decimal" value="1" min="0.25" max="30" step="0.25">
        <span class="hint" id="renewHint">Lokata odnawia się na ten sam okres, z doliczonymi odsetkami.</span>
      </div>
      <div class="field">
        <label for="infl">Zakładana inflacja (%)</label>
        <input type="number" id="infl" inputmode="decimal" value="3" min="0" max="30" step="0.1">
      </div>
      <div class="field check">
        <label><input type="checkbox" id="belka" checked> Odlicz podatek Belki (19%)</label>
        <span class="hint">Odznacz dla lokaty w IKE lub na OKI (w granicach zwolnienia).</span>
      </div>
    </div>

    <div class="presets">
      <button type="button" class="preset-btn" data-p="dep,3">Lokata 3-miesięczna</button>
      <button type="button" class="preset-btn" data-p="dep,6">Lokata 6-miesięczna</button>
      <button type="button" class="preset-btn" data-p="dep,12">Lokata roczna</button>
      <button type="button" class="preset-btn" data-p="acc,1">Konto oszczędnościowe</button>
    </div>

    <div class="net-box">
      <span class="label">Zysk na czysto</span>
      <span class="net-amount" id="net">0 zł</span>
      <span class="pct" id="netPct"></span>
    </div>

    <table class="breakdown">
      <tbody>
        <tr><td>Odsetki przed podatkiem</td><td id="rGross">0 zł</td></tr>
        <tr><td>Podatek Belki (19%)</td><td id="rTax">0 zł</td></tr>
        <tr class="total"><td>Odsetki na czysto</td><td id="rNet">0 zł</td></tr>
      </tbody>
    </table>

    <div class="results-grid">
      <div class="result-card needs">
        <span class="label">Kwota na koniec</span>
        <span class="amount" id="final">0 zł</span>
        <span class="pct" id="finalNote"></span>
      </div>
      <div class="result-card">
        <span class="label">Oprocentowanie netto</span>
        <span class="amount" id="effRate">0%</span>
        <span class="pct">w skali roku, po podatku</span>
      </div>
      <div class="result-card savings">
        <span class="label">Realnie, po inflacji</span>
        <span class="amount" id="real">0 zł</span>
        <span class="pct" id="realNote"></span>
      </div>
    </div>

    <p class="sum-warning" id="warn" hidden></p>'''
trust = ('odsetki liczone jako oprocentowanie roczne × liczba miesięcy / 12 (banki liczą dokładnie w dniach, więc wynik może różnić się o kilka groszy). '
 'Podatek Belki 19% pobierany jest przy każdej kapitalizacji — na koniec każdego okresu lokaty albo co miesiąc na koncie oszczędnościowym. '
 'Przy odnawianiu zakładamy to samo oprocentowanie przez cały czas — w rzeczywistości banki je zmieniają, a promocyjne stawki często dotyczą tylko nowych środków i limitowanej kwoty. '
 'Depozyty w bankach chroni Bankowy Fundusz Gwarancyjny do równowartości 100 000 euro na osobę w jednym banku.')
more = ('<a href="../artykuly/konta-oszczednosciowe.html">Konta oszczędnościowe i lokaty — jak wybrać →</a><br>'
        '<a href="../artykuly/podatek-belki-jak-dziala.html">Podatek Belki — jak działa →</a><br>'
        '<a href="kalkulator-oki.html">Kalkulator OKI — oszczędzanie bez podatku Belki →</a>')
script = r'''  function $(id){ return document.getElementById(id); }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2,useGrouping:'always'}).format(n) + ' zł'; }
  function pct(n){ return new Intl.NumberFormat('pl-PL',{minimumFractionDigits:2,maximumFractionDigits:2}).format(n) + '%'; }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function num(id, d){ var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : d; }

  function recalc(){
    var K = num('amount', 0), r = num('rate', 0) / 100, infl = num('infl', 0) / 100;
    var acc = $('kAcc').checked, belka = $('belka').checked;
    $('termField').hidden = acc;
    $('renewHint').textContent = acc ? 'Odsetki dopisywane co miesiąc i dalej oprocentowane.' : 'Lokata odnawia się na ten sam okres, z doliczonymi odsetkami.';
    var term = acc ? 1 : Math.max(1, Math.round(num('term', 1)));
    var months = Math.max(term, Math.round(num('years', 1) * 12));
    var periods = Math.max(1, Math.floor(months / term));
    var bal = K, gross = 0, tax = 0;
    for (var p = 0; p < periods; p++){
      var i = r2(bal * r * term / 12);
      var t = belka ? r2(i * 0.19) : 0;
      gross += i; tax += t; bal = r2(bal + i - t);
    }
    var net = r2(gross - tax), totalMonths = periods * term, yrs = totalMonths / 12;
    var eff = K > 0 ? (Math.pow(bal / K, 1 / yrs) - 1) * 100 : 0;
    var real = bal / Math.pow(1 + infl, yrs);

    $('net').textContent = fmt(net);
    $('netPct').textContent = 'po ' + (totalMonths < 12 ? totalMonths + ' mies.' : (yrs % 1 === 0 ? yrs + (yrs === 1 ? ' roku' : ' latach') : totalMonths + ' mies.'));
    $('rGross').textContent = fmt(gross);
    $('rTax').textContent = belka ? '− ' + fmt(tax) : '0,00 zł (bez podatku)';
    $('rNet').textContent = fmt(net);
    $('final').textContent = fmt(bal);
    $('finalNote').textContent = acc ? 'kapitalizacja co miesiąc' : periods + (periods === 1 ? ' lokata' : ' lokat po ' + term + ' mies.');
    $('effRate').textContent = pct(eff);
    $('real').textContent = fmt(real);
    var realGain = real - K;
    $('realNote').textContent = realGain >= 0 ? 'zyskujesz realnie ' + fmt(realGain) : 'tracisz realnie ' + fmt(-realGain) + ' — inflacja zjada zysk';

    var w = [];
    if (months % term !== 0 && !acc) w.push('Okres oszczędzania nie dzieli się równo na lokaty ' + term + '-miesięczne — liczymy ' + periods + ' pełne okresy (' + totalMonths + ' mies.). Zerwanie lokaty przed terminem zwykle oznacza utratę odsetek.');
    if (K > 400000) w.push('Gwarancja BFG obejmuje do 100 000 euro na osobę w jednym banku — przy większej kwocie rozważ podział między banki.');
    $('warn').hidden = w.length === 0; $('warn').textContent = w.join(' ');
  }
  ['amount','rate','term','years','infl','belka','kDep','kAcc'].forEach(function(id){
    $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc);
  });
  document.querySelectorAll('.preset-btn').forEach(function(btn){
    btn.addEventListener('click', function(){
      var p = btn.getAttribute('data-p').split(',');
      $(p[0] === 'acc' ? 'kAcc' : 'kDep').checked = true; $('term').value = p[1]; recalc();
    });
  });
  recalc();'''
n = make_tool.build('kalkulator-lokaty',
  'Kalkulator lokaty — zysk po podatku Belki i inflacji',
  'Kalkulator lokaty i konta oszczędnościowego: ile zarobisz na czysto po podatku Belki, ile przy odnawianiu lokaty i czy wygrywasz z inflacją. Bez rejestracji.',
  'Kalkulator lokaty', 'kalkulator lokaty, ile zarobię na lokacie, kalkulator konta oszczędnościowego, lokata podatek Belki',
  'Kalkulator lokaty', 'Kalkulator lokaty i konta oszczędnościowego',
  'Ile zarobisz na lokacie lub koncie oszczędnościowym na czysto — po podatku Belki, przy odnawianiu lokaty i po uwzględnieniu inflacji. Liczy się w Twojej przeglądarce.',
  main_inner, trust, more, script)
print('lokata', n)
