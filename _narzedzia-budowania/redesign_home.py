# Homepage top section: hero with search and a mini net-salary calculator, popular tools grid,
# "Na czasie" features, salary chips, then the (unchanged) category lists. Idempotent: replaces
# everything between <main class="home-main"> and the first category section.
import json, os, re

S = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/madry-portfel/'
icons = {}
for li in open(ROOT + 'narzedzia/index.html').read().split('<li>')[1:]:
    m = re.search(r'href="([a-z0-9-]+)\.html"', li)
    sv = re.search(r'(<svg.*?</svg>)', li, re.S)
    if m and sv:
        icons[m.group(1)] = sv.group(1)
home = open(ROOT + 'index.html').read()
art_icons = {}
for li in home.split('<li>')[1:]:
    m = re.search(r'href="artykuly/([a-z0-9-]+)\.html"', li)
    sv = re.search(r'(<svg.*?</svg>)', li, re.S)
    if m and sv:
        art_icons[m.group(1)] = sv.group(1)
n_tools = len(icons)
n_arts = len(re.findall(r'<a href="artykuly/[a-z0-9-]+\.html"', home.split('<section class="category-section', 1)[1]))


def net(g):
    r2 = lambda x: round(x + 1e-9, 2)
    zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245))
    h = r2((g - zus) * 0.09)
    tax = max(0, round(max(0, round(g - zus - 250)) * 0.12 - 300))
    return g - zus - h - tax, zus, h, tax


G = 7000
N, Z, H, T = net(G)
pl = lambda x: f'{round(x):,}'.replace(',', ' ') + ' zł'
pct = lambda x: f'{x / G * 100:.1f}%'

TOOLS = [
    ('czy-dobrze-zarabiam', 'Czy dobrze zarabiam?', 'Twoja pensja na tle Polaków — dane GUS', True),
    ('kalkulator-brutto-netto', 'Brutto–netto 2026 i 2027', 'Wypłata w każdym miesiącu, PIT-2, PPK, ulga dla młodych', False),
    ('kalkulator-urlopu', 'Kalkulator urlopu', '20 czy 26 dni, zmiana pracy i ekwiwalent', False),
    ('porownanie-ofert-pracy', 'Porównanie ofert pracy', 'Netto, benefity i dojazdy — która jest warta więcej', False),
    ('kalkulator-budzetu', 'Budżet 50/30/20', 'Podział wypłaty na potrzeby, zachcianki i oszczędności', False),
    ('kalkulator-procentu-skladanego', 'Procent składany', 'Ile urosną regularne oszczędności po latach', False),
]
MORE = [('kalkulator-umowy-zlecenia', 'Umowa zlecenia'), ('kalkulator-oki', 'OKI'), ('kalkulator-lokaty', 'Lokata'),
        ('kalkulator-kredytu', 'Rata kredytu'), ('kalkulator-poduszki-finansowej', 'Poduszka finansowa'),
        ('kalkulator-podzialu-kosztow', 'Podział kosztów dla par'), ('kalkulator-inflacji', 'Inflacja'),
        ('kalkulator-splaty-dlugow', 'Spłata długów'), ('kalkulator-l4', 'L4 — chorobowe'), ('kalkulator-nadgodzin', 'Nadgodziny')]
FEATURES = [
    ('dni-wolne-od-pracy-2027', 'Kalendarz', 'Dni wolne od pracy 2027 i długie weekendy', '10 dni wolnego za 4 dni urlopu — gotowy plan na cały rok.'),
    ('zmiany-w-finansach-2027', 'Od 1 stycznia', 'Zmiany w finansach 2027', 'Płaca minimalna 4950 zł, nowe limity IKE i IKZE, konto OKI bez podatku Belki.'),
    ('ile-na-reke-tabela-brutto-netto', 'Pensja', 'Ile na rękę w 2027 — tabela', 'Netto dla pensji od płacy minimalnej do 20 000 zł brutto.'),
]
for slug, *_ in FEATURES:
    assert slug in art_icons, slug


def tool_card(slug, title, desc, featured):
    cls = 'tool-card featured' if featured else 'tool-card'
    return (f'      <a class="{cls}" href="narzedzia/{slug}.html">\n'
            f'        <span class="tc-icon">{icons[slug]}</span>\n'
            f'        <span class="tc-title">{title}</span>\n'
            f'        <span class="tc-desc">{desc}</span>\n'
            f'      </a>\n')


def feature(slug, eyebrow, title, desc):
    return (f'      <a class="feature-card" href="artykuly/{slug}.html">\n'
            f'        <span class="fc-top"><span class="fc-icon">{art_icons[slug]}</span><span class="fc-eyebrow">{eyebrow}</span></span>\n'
            f'        <span class="fc-title">{title}</span>\n'
            f'        <span class="fc-desc">{desc}</span>\n'
            f'      </a>\n')


chips_g = ' '.join(f'<a href="wynagrodzenia/{g}-brutto-ile-netto.html">{g:,}'.replace(',', ' ') + ' zł</a>' for g in [5000, 6000, 7000, 8000, 10000, 12000])
chips_n = ' '.join(f'<a href="wynagrodzenia/{g}-netto-ile-brutto.html">{g:,}'.replace(',', ' ') + ' zł</a>' for g in [4000, 5000, 6000, 8000])

top = f'''<main class="home-main">
  <section class="home-hero">
    <div class="hh-copy">
      <p class="hh-eyebrow">Bez reklam · bez kont · bez ciasteczek</p>
      <h1>Finanse osobiste dla młodych — <span class="hh-accent">policzone</span> i wyjaśnione</h1>
      <p class="lead">Pierwsza pensja, podatki, budżet, oszczędzanie i inwestowanie. {n_arts} poradników ze źródłami urzędowymi i {n_tools} kalkulatorów, które liczą w Twojej przeglądarce.</p>
      <div class="finder">
        <label class="visually-hidden" for="q">Szukaj poradnika</label>
        <input type="search" id="q" placeholder="Szukaj: PIT, urlop, najem, ETF…" autocomplete="off">
        <p class="finder-empty" id="qEmpty" hidden>Nic nie znaleziono. Spróbuj innego słowa albo zajrzyj do <a href="slownik.html">słownika</a> lub <a href="pytania.html">najczęstszych pytań</a>.</p>
      </div>
      <p class="hh-popular"><span>Popularne:</span> <a href="artykuly/pit-za-2026-jak-rozliczyc.html">PIT za 2026</a> <a href="artykuly/dni-wolne-od-pracy-2027.html">Dni wolne 2027</a> <a href="artykuly/ike-ikze-emerytura.html">IKE i IKZE</a> <a href="artykuly/plan-na-pierwszy-rok-pracy.html">Pierwsza praca</a></p>
    </div>
    <aside class="hh-calc" aria-labelledby="hcTitle">
      <p class="hc-eyebrow">Umowa o pracę · 2026 i 2027</p>
      <h2 id="hcTitle">Ile na rękę?</h2>
      <label for="hcG">Pensja brutto miesięcznie</label>
      <div class="hc-input"><input id="hcG" type="number" inputmode="decimal" value="{G}" min="0" max="100000" step="100"><span aria-hidden="true">zł</span></div>
      <p class="hc-out" aria-live="polite"><span>Na rękę</span> <strong id="hcN">{pl(N)}</strong></p>
      <div class="hc-bar" aria-hidden="true"><i class="b-net" id="hbN" style="width:{pct(N)}"></i><i class="b-zus" id="hbZ" style="width:{pct(Z)}"></i><i class="b-hea" id="hbH" style="width:{pct(H)}"></i><i class="b-tax" id="hbT" style="width:{pct(T)}"></i></div>
      <ul class="hc-legend">
        <li><i class="b-zus"></i>ZUS <span id="hcZ">{pl(Z)}</span></li>
        <li><i class="b-hea"></i>Zdrowotna <span id="hcH">{pl(H)}</span></li>
        <li><i class="b-tax"></i>Podatek <span id="hcT">{pl(T)}</span></li>
      </ul>
      <p class="hc-note">Z PIT-2, bez PPK. Ulga dla młodych, PPK i próg podatkowy — w <a id="hcLink" href="narzedzia/kalkulator-brutto-netto.html">pełnym kalkulatorze brutto–netto&nbsp;→</a></p>
    </aside>
  </section>

  <section class="home-block" aria-labelledby="hTools">
    <div class="hb-head"><h2 id="hTools">Najpopularniejsze kalkulatory</h2><a href="narzedzia/index.html">Wszystkie {n_tools}&nbsp;→</a></div>
    <div class="tool-grid">
{''.join(tool_card(*t) for t in TOOLS)}    </div>
    <p class="more-tools"><span>Także:</span> {' '.join(f'<a href="narzedzia/{s}.html">{t}</a>' for s, t in MORE)} <a href="pliki/budzet-domowy-madry-portfel.xlsx" download>Arkusz budżetu (.xlsx)</a></p>
  </section>

  <section class="home-block" aria-labelledby="hNow">
    <div class="hb-head"><h2 id="hNow">Na czasie</h2><a href="artykuly/koniec-roku-finanse-lista.html">Lista na koniec roku&nbsp;→</a></div>
    <div class="feature-grid">
{''.join(feature(*f) for f in FEATURES)}    </div>
  </section>

  <section class="home-block salary-strip" aria-labelledby="hSal">
    <h2 id="hSal" class="visually-hidden">Ile na rękę — popularne kwoty</h2>
    <p><span>Ile na rękę z pensji brutto:</span> {chips_g}</p>
    <p><span>Ile brutto, żeby mieć na rękę:</span> {chips_n}</p>
  </section>

  <div class="hb-head articles-head"><h2 id="poradniki">Poradniki</h2><a href="pytania.html">Najczęstsze pytania&nbsp;→</a></div>
'''

a = home.index('<main class="home-main">')
b = home.index('  <nav class="cat-chips"')
home = home[:a] + top + home[b:]

script = '''<script>
(function(){
  var q=document.getElementById('q'); if(!q) return;
  var main=document.querySelector('.home-main'), empty=document.getElementById('qEmpty');
  var norm=function(t){return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/ł/g,'l');};
  var items=[].slice.call(document.querySelectorAll('.category-section .article-list li')).map(function(li){return {li:li,text:norm(li.textContent)};});
  [].forEach.call(document.querySelectorAll('.category-section'),function(sec){
    var n=sec.querySelectorAll('.article-list li').length; if(n<=8) return;
    sec.classList.add('collapsed');
    var btn=document.createElement('button'); btn.type='button'; btn.className='show-all';
    btn.textContent='Pokaż wszystkie ('+n+')'; btn.setAttribute('aria-expanded','false');
    btn.addEventListener('click',function(){var open=sec.classList.toggle('collapsed')===false; btn.setAttribute('aria-expanded',open?'true':'false'); btn.textContent=open?'Zwiń':'Pokaż wszystkie ('+n+')';});
    sec.appendChild(btn);
  });
  q.addEventListener('input',function(){
    var words=norm(q.value).split(/\\s+/).filter(Boolean).map(function(w){return w.length>=6?w.slice(0,-2):w.length>=4?w.slice(0,-1):w;}), shown=0;
    main.classList.toggle('searching',words.length>0);
    items.forEach(function(it){var ok=words.every(function(w){return it.text.indexOf(w)>-1;}); it.li.hidden=!ok; if(ok) shown++;});
    [].forEach.call(document.querySelectorAll('.category-section'),function(sec){sec.hidden=!sec.querySelector('li:not([hidden])'); sec.classList.add('is-visible');});
    empty.hidden=shown>0;
  });
  q.addEventListener('keydown',function(e){ if(e.key==='Enter'){ var h=document.getElementById('poradniki'); if(h) h.scrollIntoView({block:'start'}); } });
  var g=document.getElementById('hcG'); if(!g) return;
  var r2=function(x){return Math.round((x+Number.EPSILON)*100)/100;};
  var fmt=function(n){return new Intl.NumberFormat('pl-PL',{maximumFractionDigits:0,useGrouping:'always'}).format(Math.round(n))+'\\u00a0zł';};
  g.addEventListener('input',function(){
    var v=parseFloat(g.value); if(!isFinite(v)||v<0) v=0; v=Math.min(v,100000);
    var z=r2(r2(v*0.0976)+r2(v*0.015)+r2(v*0.0245)), h=r2((v-z)*0.09), t=Math.max(0,Math.round(Math.max(0,Math.round(v-z-250))*0.12-300)), n=v-z-h-t;
    document.getElementById('hcN').textContent=fmt(n); document.getElementById('hcZ').textContent=fmt(z);
    document.getElementById('hcH').textContent=fmt(h); document.getElementById('hcT').textContent=fmt(t);
    var w=function(id,x){document.getElementById(id).style.width=(v?x/v*100:0)+'%';}; w('hbN',n); w('hbZ',z); w('hbH',h); w('hbT',t);
    document.getElementById('hcLink').href='narzedzia/kalkulator-brutto-netto.html?brutto='+v+'&ppk=0';
  });
})();
</script>'''
home = re.sub(r'<script>\n\(function\(\)\{\n  var q=document\.getElementById\(\'q\'\).*?</script>', lambda m: script, home, count=1, flags=re.S)
assert 'hcG' in home and "classList.toggle('searching'" in home
open(ROOT + 'index.html', 'w').write(home)
print('home redesigned:', n_arts, 'articles,', n_tools, 'tools, net', round(N, 2))
