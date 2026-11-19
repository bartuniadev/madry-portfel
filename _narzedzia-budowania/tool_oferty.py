import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_tool


def offer(k, label, gross, kind, ppk, benefit, commute, minutes):
    sel = lambda v, t: f'<option value="{v}"{" selected" if v == kind else ""}>{t}</option>'
    return f'''      <fieldset class="offer">
        <legend>{label}</legend>
        <div class="field"><label for="g{k}">Wynagrodzenie brutto miesięcznie (zł)</label><input type="number" id="g{k}" inputmode="decimal" value="{gross}" min="0" step="100"></div>
        <div class="field"><label for="t{k}">Rodzaj umowy</label><select id="t{k}">{sel("etat", "Umowa o pracę")}{sel("zlec", "Zlecenie (jedyna praca)")}{sel("stud", "Zlecenie — student do 26 l.")}</select></div>
        <div class="field check" id="ppkF{k}"><label><input type="checkbox" id="p{k}"{" checked" if ppk else ""}> W PPK (2% + 1,5% od pracodawcy)</label></div>
        <div class="field"><label for="b{k}">Benefity — ile byś za nie zapłacił sam (zł/mies.)</label><input type="number" id="b{k}" inputmode="decimal" value="{benefit}" min="0" step="10"><span class="hint">Np. pakiet medyczny, karta sportowa, lunch. Licz tylko te, z których skorzystasz.</span></div>
        <div class="field"><label for="c{k}">Koszt dojazdu miesięcznie (zł)</label><input type="number" id="c{k}" inputmode="decimal" value="{commute}" min="0" step="10"></div>
        <div class="field"><label for="m{k}">Dojazd w obie strony dziennie (minuty)</label><input type="number" id="m{k}" inputmode="numeric" value="{minutes}" min="0" step="5"><span class="hint">Liczony dla dni w biurze.</span></div>
        <div class="field"><label for="d{k}">Dni w biurze w tygodniu</label><input type="number" id="d{k}" inputmode="numeric" value="{5 if k == 'A' else 2}" min="0" max="5" step="1"></div>
      </fieldset>'''


main_inner = f'''    <div class="checks">
      <div class="field check"><label><input type="checkbox" id="young"> Nie mam jeszcze 26 lat (ulga dla młodych)</label></div>
    </div>
    <div class="offers">
{offer("A", "Oferta A", 7000, "etat", True, 150, 180, 80)}
{offer("B", "Oferta B", 7200, "zlec", False, 0, 80, 40)}
    </div>

    <div class="verdict" id="verdict" aria-live="polite"></div>

    <div class="tbl-wrap">
    <table class="data-table cmp">
      <caption>Kwoty miesięcznie. Wartość urlopu na zleceniu: 20 dni wolnego rocznie bez wynagrodzenia.</caption>
      <thead><tr><th scope="col"></th><th scope="col">Oferta A</th><th scope="col">Oferta B</th></tr></thead>
      <tbody id="rows"></tbody>
    </table>
    </div>
    <p class="sum-warning" id="warn" hidden></p>'''

trust = ('<strong>Netto</strong> liczymy tak jak w kalkulatorach brutto–netto i zlecenia (2026/2027: składki 13,71% na etacie i 11,26% na zleceniu, zdrowotna 9%, koszty 250 zł na etacie i 20% na zleceniu, podatek 12%, ulga dla młodych do 85 528 zł rocznie). <strong>Na zleceniu</strong> zakładamy, że to Twoja jedyna praca, nie płacisz dobrowolnej składki chorobowej i złożyłeś PIT-2 u zleceniodawcy (tak jak na etacie); student do 26 lat nie płaci składek ani podatku. '
         '<strong>PPK pracodawcy</strong> (1,5% brutto) doliczamy jako Twoje pieniądze odkładane na przyszłość — możesz je pominąć, patrząc na wiersz „Na rękę”. '
         '<strong>Urlop:</strong> na etacie przysługuje 20 dni płatnego urlopu (26 przy stażu od 10 lat, wliczając szkołę); na zleceniu zakładamy, że weźmiesz tyle samo wolnego, ale bez wynagrodzenia — to średnio 20/252 rocznej pensji. '
         'Nie uwzględniamy chorobowego, okresu wypowiedzenia ani premii — opisujemy je w artykułach poniżej. Przy B2B wynik byłby inny — patrz porównanie B2B i etatu.')

more = ('<a href="../artykuly/benefity-pozaplacowe-ile-sa-warte.html">Benefity pracownicze — ile są warte →</a><br>'
        '<a href="../artykuly/zmiana-pracy-lista-kontrolna.html">Zmiana pracy — lista kontrolna →</a><br>'
        '<a href="../artykuly/b2b-czy-etat-porownanie.html">B2B czy etat — porównanie →</a>')

script = r'''  function $(id){ return document.getElementById(id); }
  function r2(x){ return Math.round((x + Number.EPSILON) * 100) / 100; }
  function fmt(n){ return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n)) + ' zł'; }
  function num(id){ var v = parseFloat($(id).value); return isFinite(v) && v >= 0 ? v : 0; }
  var YOUNG = 85528, LEAVE = 20 / 252;

  function netEtat(g, ppk, young){
    var zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245)), h = r2((g - zus) * 0.09);
    var own = ppk ? r2(g * 0.02) : 0, emp = ppk ? r2(g * 0.015) : 0, tax = 0;
    var exempt = young && g * 12 <= YOUNG;
    if (!exempt) tax = Math.max(0, Math.round(Math.max(0, Math.round(g - zus - 250 + emp)) * 0.12 - 300));
    return {net: r2(g - zus - h - tax - own), emp: emp, own: own};
  }
  function netZlec(g, young, student){
    var zus = student ? 0 : r2(r2(g * 0.0976) + r2(g * 0.015)), h = student ? 0 : r2((g - zus) * 0.09), kup = r2((g - zus) * 0.2);
    var tax = (young && g * 12 <= YOUNG) ? 0 : Math.max(0, Math.round(Math.round(g - zus - kup) * 0.12 - 300));
    return r2(g - zus - h - tax);
  }
  function calc(k, young){
    var g = num('g' + k), t = $('t' + k).value, ppk = t === 'etat' && $('p' + k).checked;
    $('ppkF' + k).hidden = t !== 'etat';
    var net, emp = 0;
    if (t === 'etat'){ var e = netEtat(g, ppk, young); net = e.net; emp = e.emp; }
    else net = netZlec(g, young, t === 'stud');
    var leave = t === 'etat' ? 0 : net * LEAVE;
    var ben = num('b' + k), com = num('c' + k);
    var hours = num('m' + k) / 60 * Math.min(5, num('d' + k)) * 4.33;
    var total = net - leave + ben - com + emp;
    return {t: t, g: g, net: net, leave: leave, ben: ben, com: com, emp: emp, total: total, hours: hours};
  }
  var TYPE = {etat: "Etat", zlec: "Zlecenie", stud: "Zlecenie (student)"};
  function recalc(){
    var young = $('young').checked;
    var studA = $('tA').value === 'stud', studB = $('tB').value === 'stud';
    var a = calc('A', young || studA), b = calc('B', young || studB);
    var row = function(lbl, x, y, cls){ return '<tr' + (cls ? ' class="' + cls + '"' : '') + '><th scope="row">' + lbl + '</th><td>' + x + '</td><td>' + y + '</td></tr>'; };
    var sign = function(v, minus){ return v ? (minus ? '− ' : '+ ') + fmt(v) : '—'; };
    $('rows').innerHTML =
      row('Umowa', TYPE[a.t], TYPE[b.t]) +
      row('Brutto', fmt(a.g), fmt(b.g)) +
      row('Na rękę', fmt(a.net), fmt(b.net), 'em') +
      row('Bezpłatny urlop (zlecenie)', sign(a.leave, true), sign(b.leave, true)) +
      row('Benefity', sign(a.ben), sign(b.ben)) +
      row('Dojazd', sign(a.com, true), sign(b.com, true)) +
      row('PPK od pracodawcy', sign(a.emp), sign(b.emp)) +
      row('Realna wartość miesięcznie', fmt(a.total), fmt(b.total), 'total') +
      row('Czas dojazdu miesięcznie', Math.round(a.hours) + ' godz.', Math.round(b.hours) + ' godz.');
    var d = a.total - b.total, v = $('verdict');
    if (Math.abs(d) < 1) v.textContent = 'Obie oferty są warte praktycznie tyle samo — decydują inne rzeczy: stabilność, rozwój, zespół.';
    else {
      var better = d > 0 ? 'A' : 'B';
      var hrs = Math.round(d > 0 ? a.hours - b.hours : b.hours - a.hours);
      v.textContent = 'Oferta ' + better + ' jest realnie warta o ' + fmt(Math.abs(d)) + ' miesięcznie więcej (' + fmt(Math.abs(d) * 12) + ' rocznie)' +
        (hrs > 0 ? ', ale zabiera ' + hrs + ' godz. więcej na dojazdy w miesiącu.' : hrs < 0 ? ' i do tego oszczędza ' + (-hrs) + ' godz. dojazdów w miesiącu.' : '.');
    }
    var w = [];
    if ((a.t !== 'etat') || (b.t !== 'etat')) w.push('Na zleceniu nie masz płatnego chorobowego (chyba że opłacasz dobrowolną składkę chorobową), okresu wypowiedzenia ani ochrony z Kodeksu pracy — to też ma swoją cenę.');
    if ((young && (a.g * 12 > YOUNG || b.g * 12 > YOUNG)) || (studA && a.g * 12 > YOUNG) || (studB && b.g * 12 > YOUNG)) w.push('Przy pensji powyżej ok. 7127 zł brutto miesięcznie limit ulgi dla młodych (85 528 zł rocznie) skończy się przed końcem roku — od tego miesiąca pobierany jest podatek. Liczymy wtedy wariant z podatkiem.');
    $('warn').hidden = !w.length; $('warn').textContent = w.join(' ');
  }
  ['young','gA','tA','pA','bA','cA','mA','dA','gB','tB','pB','bB','cB','mB','dB'].forEach(function(id){ $(id).addEventListener('input', recalc); $(id).addEventListener('change', recalc); });
  recalc();'''

css = '''  .checks{margin:0 0 6px;}
  .offers{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;}
  @media (max-width:640px){.offers{grid-template-columns:1fr;}}
  fieldset.offer{border:1px solid var(--border);border-radius:10px;padding:12px 14px 2px;margin:0;min-width:0;background:var(--bg);}
  fieldset.offer legend{font-weight:700;padding:0 6px;color:var(--green);}
  fieldset.offer .field input{font-size:1.05rem;padding:9px 10px;}
  fieldset.offer select{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:9px 10px;font-size:1rem;font-family:inherit;min-height:44px;}
  fieldset.offer select:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  .cmp th[scope="row"]{text-align:left;font-weight:500;color:var(--text-2);white-space:normal;}
  .cmp tr.em td{font-weight:700;}
  .cmp tr.total th,.cmp tr.total td{font-weight:700;color:var(--green);border-top:2px solid var(--green);}
'''
print('oferty', make_tool.build('porownanie-ofert-pracy',
    'Porównanie ofert pracy — kalkulator realnej wartości',
    'Porównaj dwie oferty pracy: netto na etacie i zleceniu, PPK, benefity, koszt i czas dojazdu oraz bezpłatny urlop na zleceniu. Która oferta jest realnie warta więcej.',
    'Porównanie ofert pracy', 'porównanie ofert pracy, która oferta pracy lepsza, etat czy zlecenie kalkulator, kalkulator oferty pracy',
    'Porównanie ofert pracy', 'Porównanie ofert pracy — która jest realnie warta więcej',
    'Wyższe brutto nie zawsze oznacza lepszą ofertę. Wpisz dwie propozycje — policzę netto na etacie lub zleceniu, PPK, benefity, dojazdy i bezpłatny urlop na zleceniu, i pokażę, która jest realnie warta więcej. Liczy się w Twojej przeglądarce.',
    main_inner, trust, more, script, css))
