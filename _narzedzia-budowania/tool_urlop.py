import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool

MONTHS = ['styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień']


def month_opts(sel):
    return ''.join(f'<option value="{i + 1}"{" selected" if i + 1 == sel else ""}>{m}</option>' for i, m in enumerate(MONTHS))


main_inner = f'''    <p class="field-title">Twój staż pracy</p>
    <div class="field"><label for="edu">Najwyżej ukończona szkoła</label><select id="edu">
      <option value="0">Podstawowa / bez średniej</option>
      <option value="3">Branżowa I st. / zawodowa (3 lata)</option>
      <option value="4">Liceum (4 lata)</option>
      <option value="5">Technikum / branżowa II st. (5 lat)</option>
      <option value="6">Szkoła policealna (6 lat)</option>
      <option value="8" selected>Studia wyższe (8 lat)</option>
    </select><span class="hint">Studia to licencjat, inżynier lub magister. Liczy się jedna, najkorzystniejsza szkoła — okresy nauki się nie sumują.</span></div>
    <div class="split-controls two">
      <div class="field"><label for="wy">Okres pracy — lata</label><input type="number" id="wy" inputmode="numeric" value="1" min="0" max="50" step="1"></div>
      <div class="field"><label for="wm">i miesiące</label><input type="number" id="wm" inputmode="numeric" value="6" min="0" max="11" step="1"></div>
    </div>
    <p class="hint">Wszystkie umowy o pracę, a od 2026 r. także udokumentowane umowy zlecenia i działalność gospodarcza (okresy pokrywające się liczą się raz). Pracę w trakcie nauki wliczasz zamiast szkoły tylko wtedy, gdy to korzystniejsze.</p>

    <div class="field"><label for="fte">Wymiar etatu</label><select id="fte">
      <option value="1" selected>Pełny etat</option><option value="0.8">4/5 etatu</option><option value="0.75">3/4 etatu</option><option value="0.5">1/2 etatu</option><option value="0.25">1/4 etatu</option>
    </select></div>

    <p class="field-title" id="sitLabel">Twoja sytuacja w tym roku</p>
    <div class="type-toggle" role="radiogroup" aria-labelledby="sitLabel">
      <label><input type="radio" name="sit" value="full" checked><span>Cały rok u tego pracodawcy</span></label>
      <label><input type="radio" name="sit" value="first"><span>Pierwsza praca w życiu</span></label>
      <label><input type="radio" name="sit" value="part"><span>Zmiana pracy w trakcie roku</span></label>
    </div>
    <div class="split-controls two" id="months" hidden>
      <div class="field"><label for="ms">Miesiąc rozpoczęcia pracy u tego pracodawcy</label><select id="ms">{month_opts(3)}</select></div>
      <div class="field" id="meF"><label for="me">Miesiąc zakończenia (grudzień, jeśli pracujesz dłużej)</label><select id="me">{month_opts(12)}</select></div>
    </div>

    <div class="net-box">
      <span class="label" id="resLabel">Urlop w tym roku</span>
      <span class="net-amount" id="days">0 dni</span>
      <span class="pct" id="daysNote"></span>
    </div>

    <div class="results-grid">
      <div class="result-card">
        <span class="label">Staż do urlopu</span>
        <span class="amount" id="staz">—</span>
        <span class="pct" id="stazNote"></span>
      </div>
      <div class="result-card needs">
        <span class="label">Wymiar roczny</span>
        <span class="amount" id="annual">—</span>
        <span class="pct" id="annualNote"></span>
      </div>
      <div class="result-card savings">
        <span class="label">Do 26 dni urlopu</span>
        <span class="amount" id="to26">—</span>
        <span class="pct" id="to26Note"></span>
      </div>
    </div>
    <div class="verdict" id="verdict" aria-live="polite"></div>

    <h2 class="tool-sub" id="ekw">Ekwiwalent za niewykorzystany urlop</h2>
    <p class="hint">Należy się, gdy umowa się kończy, a urlop nie został wykorzystany. Wpisz pensję brutto (stałe składniki) i liczbę niewykorzystanych dni.</p>
    <div class="split-controls two">
      <div class="field"><label for="sal">Wynagrodzenie brutto miesięcznie (zł)</label><input type="number" id="sal" inputmode="decimal" value="6000" min="0" step="100"></div>
      <div class="field"><label for="left">Niewykorzystane dni urlopu</label><input type="number" id="left" inputmode="decimal" value="5" min="0" max="80" step="1"></div>
    </div>
    <div class="results-grid">
      <div class="result-card">
        <span class="label">Ekwiwalent brutto</span>
        <span class="amount" id="eqG">0 zł</span>
        <span class="pct" id="eqRate"></span>
      </div>
      <div class="result-card savings">
        <span class="label">Ok. na rękę</span>
        <span class="amount" id="eqN">0 zł</span>
        <span class="pct">gdy jest wypłacony razem z ostatnią pensją</span>
      </div>
    </div>'''

trust = ('<strong>Wymiar urlopu</strong> (art. 154 Kodeksu pracy): 20 dni przy stażu poniżej 10 lat, 26 dni od 10 lat. Do stażu wlicza się ukończona szkoła (art. 155): szkoła branżowa I stopnia do 3 lat, technikum lub szkoła branżowa II stopnia do 5, liceum 4, szkoła policealna 6, studia wyższe 8 lat. '
         'Od 2026 r. wlicza się też okresy zleceń i działalności gospodarczej — po udokumentowaniu zaświadczeniem z ZUS. '
         '<strong>Niepełny etat:</strong> wymiar proporcjonalny, niepełny dzień zaokrąglony w górę; dzień urlopu to 8 godzin. '
         '<strong>Pierwsza praca:</strong> 1/12 rocznego wymiaru po każdym przepracowanym miesiącu (art. 153) — zakładamy rozpoczęcie pierwszego dnia miesiąca. '
         '<strong>Zmiana pracy:</strong> urlop proporcjonalny do miesięcy zatrudnienia w roku, niepełny miesiąc i niepełny dzień zaokrąglone w górę; gdy stara i nowa praca przypadają w tym samym miesiącu, zaokrągla poprzedni pracodawca. '
         '<strong>Ekwiwalent:</strong> pensja ÷ współczynnik 20,92 (2026 i 2027 r., pomniejszony proporcjonalnie przy niepełnym etacie) × liczba dni; na rękę liczymy jak dodatek do pensji na umowie o pracę (składki, zdrowotna, podatek 12% z PIT-2, bez PPK).')

more = ('<a href="../artykuly/dni-wolne-od-pracy-2027.html">Dni wolne od pracy 2027 i długie weekendy →</a><br>'
        '<a href="../artykuly/prawa-pracownika-w-liczbach.html">Prawa pracownika w liczbach →</a><br>'
        '<a href="../artykuly/zmiana-pracy-lista-kontrolna.html">Zmiana pracy — lista kontrolna →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function dec(n, d){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:d || 1}).format(n); }
  function godz(n){ return n + ' ' + plural(n, 'godzina', 'godziny', 'godzin'); }
  function num(id, max){ var v = parseFloat($(id).value); if (!isFinite(v) || v < 0) v = 0; return max != null ? Math.min(v, max) : v; }
  function plural(n, one, few, many){ var a = Math.abs(n) % 100, b = a % 10; if (n === 1) return one; if (b >= 2 && b <= 4 && (a < 12 || a > 14)) return few; return many; }
  function dni(n){ return n === 1 ? 'dzień' : 'dni'; }
  function ym(totalM){ var y = Math.floor(totalM / 12), m = totalM % 12, out = [];
    if (y) out.push(y + ' ' + plural(y, 'rok', 'lata', 'lat'));
    if (m) out.push(m + ' mies.');
    return out.length ? out.join(' ') : '0 mies.'; }
  var COEF = 20.92;
  function netEtat(g){
    var zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245)), h = r2((g - zus) * 0.09);
    var tax = Math.max(0, Math.round(Math.max(0, Math.round(g - zus - 250)) * 0.12 - 300));
    return g - zus - h - tax;
  }
  function sit(){ var r = document.querySelector('input[name="sit"]:checked'); return r ? r.value : 'full'; }

  function recalc(){
    var edu = parseInt($('edu').value, 10), workM = Math.round(num('wy', 60)) * 12 + Math.round(num('wm', 11));
    var fte = parseFloat($('fte').value), s = sit();
    var stazM = edu * 12 + workM;
    var base = stazM >= 120 ? 26 : 20;
    var annual = Math.ceil(base * fte - 1e-9);
    $('staz').textContent = ym(stazM);
    $('stazNote').textContent = edu ? 'w tym ' + edu + ' ' + plural(edu, 'rok', 'lata', 'lat') + ' za szkołę' : 'bez okresu nauki';
    $('annual').textContent = annual + ' ' + dni(annual);
    $('annualNote').textContent = fte < 1 ? 'z ' + base + ' dni dla pełnego etatu' : (base === 26 ? 'staż co najmniej 10 lat' : 'staż poniżej 10 lat');
    if (stazM >= 120){ $('to26').textContent = 'masz już'; $('to26Note').textContent = 'prawo do 26 dni'; }
    else { $('to26').textContent = ym(120 - stazM); $('to26Note').textContent = 'stażu brakuje'; }

    $('months').hidden = s === 'full';
    $('meF').hidden = s !== 'part';
    var ms = parseInt($('ms').value, 10), me = parseInt($('me').value, 10), days, note, label, v = '';
    if (s === 'full'){
      days = annual; label = 'Urlop w tym roku';
      note = godz(annual * 8) + (fte < 1 ? ' (dzień urlopu = 8 godzin)' : '');
      v = 'Masz ' + annual + ' ' + dni(annual) + ' urlopu, w tym 4 dni urlopu na żądanie. Niewykorzystany urlop przechodzi na kolejny rok — trzeba go wykorzystać do 30 września.';
    } else if (s === 'first'){
      var mm = 13 - ms, acc = base * fte * mm / 12;
      days = acc; label = 'Urlop do końca roku';
      note = 'po ' + dec(base * fte / 12, 2) + ' dnia za każdy z ' + mm + ' ' + plural(mm, 'miesiąca', 'miesięcy', 'miesięcy') + ' (ok. ' + Math.round(acc * 8) + ' godz.)';
      v = 'W pierwszej pracy urlop nabywasz z dołu: po każdym przepracowanym miesiącu 1/12 rocznego wymiaru. Od 1 stycznia przyszłego roku masz od razu pełne ' + annual + ' ' + dni(annual) + '.';
      if (stazM >= 120) v += ' Uwaga: przy pierwszej pracy staż zwykle wynika tylko ze szkoły — sprawdź wpisany okres pracy.';
    } else {
      if (me < ms) me = ms;
      var mp = me - ms + 1, prop = Math.min(annual, Math.ceil(annual * mp / 12 - 1e-9));
      days = prop; label = 'Urlop u tego pracodawcy';
      note = mp + ' ' + plural(mp, 'miesiąc', 'miesiące', 'miesięcy') + ' z 12 · ' + godz(prop * 8);
      v = 'U tego pracodawcy przysługuje Ci ' + prop + ' ' + dni(prop) + ' urlopu (proporcjonalnie do ' + mp + ' ' + plural(mp, 'miesiąca', 'miesięcy', 'miesięcy') + '). U poprzedniego lub następnego pracodawcy dostaniesz urlop za pozostałe miesiące roku. Jeśli u poprzedniego wykorzystałeś więcej, niż wynikało z proporcji, tu dostaniesz odpowiednio mniej.';
    }
    $('resLabel').textContent = label;
    var whole = Math.abs(days - Math.round(days)) < 1e-9;
    $('days').textContent = (s === 'first' ? 'ok. ' + dec(days) : days) + ' ' + (whole ? dni(Math.round(days)) : 'dnia');
    $('daysNote').textContent = note;
    $('verdict').textContent = v;

    var sal = num('sal'), left = num('left', 80), daily = sal / (COEF * fte);
    var eq = r2(daily * left);
    $('eqG').textContent = fmt(eq);
    $('eqRate').textContent = left ? fmt(daily) + ' za dzień (' + dec(daily / 8) + ' zł/godz.)' : '';
    $('eqN').textContent = fmt(Math.max(0, netEtat(sal + eq) - netEtat(sal)));
  }
  ['edu','wy','wm','fte','ms','me','sal','left'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  document.querySelectorAll('input[name="sit"]').forEach(function(r){ r.addEventListener('change', recalc); });
  recalc();'''

css = '''  #edu,#fte,#ms,#me{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 10px;font-size:1rem;font-family:inherit;min-height:44px;}
  #edu:focus-visible,#fte:focus-visible,#ms:focus-visible,#me:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  .tool-sub{font-size:1.15rem;margin:26px 0 6px;}
  p.hint{margin:-4px 0 14px;font-size:.85rem;color:var(--text-2);line-height:1.5;}
'''
print('urlop', make_tool.build('kalkulator-urlopu',
    'Kalkulator urlopu 2027 — ile dni urlopu i ekwiwalent',
    'Ile dni urlopu Ci przysługuje: staż ze szkołą, 20 czy 26 dni, pierwsza praca, zmiana pracy w trakcie roku, niepełny etat. Plus ekwiwalent za niewykorzystany urlop.',
    'Kalkulator urlopu wypoczynkowego', 'kalkulator urlopu, ile dni urlopu, urlop proporcjonalny, ekwiwalent za urlop, urlop po studiach',
    'Kalkulator urlopu', 'Kalkulator urlopu — ile dni urlopu Ci przysługuje',
    'Sprawdź, ile dni urlopu wypoczynkowego masz w tym roku: ze stażem liczonym razem ze szkołą, przy pierwszej pracy, zmianie pracy w trakcie roku i na niepełnym etacie. Na końcu policzysz ekwiwalent za niewykorzystany urlop. Wszystko liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, css))
