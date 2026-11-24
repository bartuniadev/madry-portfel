# Builds udostepnij.html — a hidden (noindex) promotion kit for the site owner:
# Google/Bing submission steps, a ready message for friends, carousel images to download/share
# and post captions with copy buttons. Reads karuzele/opisy-postow.md and karuzele/*.png next to this script.
import html, json, os, re, sys
from urllib.parse import quote
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/madry-portfel/'
BASE = 'https://bartuniadev.github.io/madry-portfel/'
KDIR = S + '/karuzele/'

SETS = [  # (id, md heading prefix, title, when, article path)
    ('niedziele', 'Karuzela 5', 'Niedziele handlowe — 3 niedziele i 4 dni bez sklepów', 'Najlepiej 28 listopada – 5 grudnia, przypomnienie 18–19 grudnia', 'artykuly/niedziele-handlowe-2026-2027.html'),
    ('weekendy', 'Karuzela 4', 'Długie weekendy 2027 — 28 dni wolnego za 11 dni urlopu', 'Teraz i do połowy grudnia, powtórka na początku stycznia', 'artykuly/dni-wolne-od-pracy-2027.html'),
    ('zarobki', 'Karuzela 1', 'Czy dobrze zarabiasz? Mediana płac GUS', 'W dowolnym momencie — temat „zawsze na czasie”', 'narzedzia/czy-dobrze-zarabiam.html'),
    ('premia', 'Karuzela 3', 'Premia świąteczna — ile z niej zostanie', '1–15 grudnia', 'artykuly/premia-swiateczna-bony-ile-netto.html'),
    ('zmiany2027', 'Karuzela 2', 'Zmiany w finansach od 1 stycznia 2027', '20 grudnia – 10 stycznia', 'artykuly/zmiany-w-finansach-2027.html'),
]

md = open(KDIR + 'opisy-postow.md').read()


def captions(prefix):
    i = md.index('## ' + prefix)
    j = md.find('\n## ', i + 3)
    block = md[i:j if j > 0 else len(md)]
    out = []
    for m in re.finditer(r'### ([^\n]+)\n((?:>.*\n?)+)', block):
        name = m.group(1).split('(')[0].strip()
        text = '\n'.join(l[2:] if l.startswith('> ') else '' for l in m.group(2).rstrip('\n').split('\n'))
        out.append((name, text.strip()))
    return out


os.makedirs(ROOT + 'pliki/karuzele', exist_ok=True)
cards = []
for sid, prefix, title, when, path in SETS:
    imgs = []
    n = 1
    while os.path.exists(KDIR + f'{sid}-{n}.png'):
        dst = f'pliki/karuzele/{sid}-{n}.jpg'
        Image.open(KDIR + f'{sid}-{n}.png').convert('RGB').save(ROOT + dst, quality=88, optimize=True, progressive=True)
        imgs.append(dst)
        n += 1
    url = BASE + path
    caps = captions(prefix)
    thumbs = ''.join(f'<a href="{p}" target="_blank" rel="noopener"><img src="{p}" alt="Slajd {k + 1}" width="108" height="135" loading="lazy"></a>' for k, p in enumerate(imgs))
    cap_html = ''.join(
        f'''      <div class="cap">
        <div class="cap-head"><strong>{html.escape(name)}</strong><button type="button" class="copy" data-copy="c-{sid}-{k}">Kopiuj</button></div>
        <textarea id="c-{sid}-{k}" readonly rows="6">{html.escape(text)}</textarea>
      </div>
''' for k, (name, text) in enumerate(caps))
    share = (f'<a class="btn" href="https://www.facebook.com/sharer/sharer.php?u={quote(url, safe="")}" target="_blank" rel="noopener">Facebook</a>'
             f'<a class="btn" href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url, safe="")}" target="_blank" rel="noopener">LinkedIn</a>'
             f'<a class="btn" href="https://wa.me/?text={quote(title + " " + url, safe="")}" target="_blank" rel="noopener">WhatsApp</a>'
             f'<a class="btn" href="https://twitter.com/intent/tweet?text={quote(title, safe="")}&amp;url={quote(url, safe="")}" target="_blank" rel="noopener">X</a>')
    cards.append(f'''  <section class="kit-card" id="{sid}">
    <h3>{html.escape(title)}</h3>
    <p class="when">Kiedy: {html.escape(when)}</p>
    <div class="thumbs">{thumbs}</div>
    <div class="row">
      <button type="button" class="btn primary share-files" data-files='{json.dumps(imgs)}' data-title="{html.escape(title)}">Udostępnij zdjęcia (Instagram, Facebook…)</button>
      <span class="hint">Na komputerze: kliknij miniaturę i zapisz obraz.</span>
    </div>
{cap_html}    <div class="row"><span class="lbl">Link do artykułu:</span> {share} <button type="button" class="btn copy" data-copy-text="{url}">Kopiuj link</button></div>
  </section>
''')

EXTRA = [
    ('Wykop — mikroblog', 'Po godzinach zrobiłem darmową stronę z kalkulatorami dla osób na starcie kariery: ile na rękę w 2027, L4, nadgodziny, urlop i ekwiwalent, porównanie dwóch ofert pracy, a do tego „Czy dobrze zarabiam?” — wpisujesz pensję i widzisz, ile procent pracujących zarabia mniej (dane GUS).\n\nBez reklam, bez rejestracji, wszystko liczy się w przeglądarce, kod jest otwarty na GitHubie. Szukam uwag: co liczy źle, czego brakuje?\n\n' + BASE + '\n\n#finanse #pieniadze #praca #oszczedzanie #programowanie'),
    ('Reddit (np. r/Polska — najpierw sprawdź zasady subreddita o autopromocji)', 'Tytuł: Zrobiłem darmowe kalkulatory finansowe bez reklam — ile na rękę 2027, L4, nadgodziny, urlop. Szukam uwag\n\nTreść: Cześć! Po godzinach zrobiłem stronę dla osób, które zaczynają pracę: kalkulator brutto–netto na 2027, L4, nadgodziny (z wymiarem godzin na każdy miesiąc), urlop i ekwiwalent, porównanie ofert pracy i „Czy dobrze zarabiam?” na danych GUS. Bez reklam i rejestracji, kod na GitHubie. Jeśli coś liczy inaczej niż Wasz pasek wypłaty — dajcie znać, poprawię.\n\n' + BASE),
    ('Mail do redakcji (Bankier, Money.pl, Business Insider, Infor, portale regionalne)', 'Temat: Darmowe narzędzie: ile procent Polaków zarabia mniej od Ciebie (dane GUS 2026)\n\nDzień dobry,\n\nprowadzę niezależny, niekomercyjny serwis Mądry Portfel z kalkulatorami finansowymi dla osób na starcie kariery. Jeden z nich — „Czy dobrze zarabiam?” — na podstawie rozkładu wynagrodzeń GUS z maja 2026 r. pokazuje, ile procent pracujących zarabia mniej niż wpisana pensja. Przykład: 7550 zł brutto (mediana) to połowa pracujących, a mniej niż „średnią krajową” (9178 zł) zarabia ok. 65% osób.\n\nNa stronie są też kalkulatory na 2027 r.: brutto–netto, L4, nadgodziny i urlop, a także kalendarz dni wolnych i niedziel handlowych. Wszystko bez reklam i rejestracji, z metodologią i źródłami. Jeśli przyda się Państwu do materiału — można z niego korzystać i linkować bez ograniczeń.\n\n' + BASE + 'narzedzia/czy-dobrze-zarabiam.html\n\nPozdrawiam'),
    ('Gdzie szukać grup na Facebooku', 'Wpisz w wyszukiwarce grup: „oszczędzanie”, „finanse osobiste”, „praca + Twoje miasto”, „studenci + Twoja uczelnia”, „mamy + Twoje miasto”, „pierwsza praca”. Wybierz grupy aktywne (posty z ostatnich dni), przeczytaj regulamin i wrzucaj po jednym poście dziennie — najlepiej karuzelę albo pytanie z linkiem, nie sam link.'),
]

msg = ('Hej! Zrobiłem stronę z darmowymi kalkulatorami finansowymi — ile na rękę z pensji, L4, nadgodziny, urlop i czy dobrze zarabiasz na tle Polaków. '
       'Bez reklam i bez rejestracji. Rzucisz okiem i powiesz, co poprawić? ' + BASE)

tpl = open(ROOT + 'o-nas.html').read()
head = tpl[:tpl.index('<main>')]
foot = tpl[tpl.index('</main>') + len('</main>'):]
head = re.sub(r'<title>.*?</title>', '<title>Pakiet do udostępniania | Mądry Portfel</title>', head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
head = re.sub(r'<meta (property="og:[^"]+"|name="twitter:[^"]+"|name="description") content="[^"]*">\n?', '', head)
head = re.sub(r'<link rel="canonical"[^>]*>\n?', '', head)
head = head.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n<style>\n' + '''.kit-step{margin:28px 0;padding:20px 22px;border:1px solid var(--border);border-radius:16px;background:var(--card)}
.kit-step h2{margin:0 0 8px;font-size:1.3rem}
.kit-step ol{padding-left:1.2em}.kit-step li{margin:6px 0}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0}
.btn{display:inline-block;font:inherit;font-size:.9rem;font-weight:600;text-decoration:none;cursor:pointer;color:var(--accent-dark);background:var(--bg);border:1px solid var(--border);border-radius:999px;padding:8px 14px}
.btn:hover{border-color:var(--accent);background:#eef7f0}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:var(--accent-dark)}
.copy{font:inherit;font-size:.85rem;font-weight:600;cursor:pointer;color:var(--accent-dark);background:#eef7f0;border:1px solid #cfe5d6;border-radius:999px;padding:5px 12px}
.copy.done{background:var(--accent);color:#fff;border-color:var(--accent)}
.kit-card{margin:22px 0;padding:20px 22px;border:1px solid var(--border);border-radius:16px;background:var(--card)}
.kit-card h3{margin:0;font-size:1.2rem}
.when{margin:4px 0 12px;color:var(--muted);font-size:.9rem}
.thumbs{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px}
.thumbs img{width:108px;height:135px;object-fit:cover;border-radius:8px;border:1px solid var(--border);display:block}
.cap{margin:12px 0}.cap-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.cap textarea{width:100%;font:inherit;font-size:.88rem;line-height:1.5;padding:10px 12px;border:1px solid var(--border);border-radius:10px;background:var(--bg);color:var(--text);resize:vertical}
.lbl{font-size:.88rem;color:var(--muted)}
.hint{font-size:.82rem;color:var(--muted)}
.msg{width:100%;font:inherit;font-size:.95rem;padding:12px;border:1px solid var(--border);border-radius:10px;background:var(--bg)}
''' + '</style>\n</head>', 1)

main = f'''<main>
  <h1>Pakiet do udostępniania</h1>
  <p class="lead">Ta strona jest dla Ciebie — nie ma jej w menu ani w wyszukiwarkach. Trzy kroki, każdy zajmuje kilka minut, a razem dają stronie pierwszych czytelników. <strong>Zaczynasz na Instagramie?</strong> Gotowy plan startu z grafikami, Reelsami i opisami: <a href="instagram.html">Start na Instagramie →</a></p>

  <section class="kit-step">
    <h2>1. Zgłoś stronę do Google i Bing (5 minut, raz)</h2>
    <ol>
      <li><a class="btn primary" href="https://search.google.com/search-console" target="_blank" rel="noopener">Otwórz Google Search Console</a> → <strong>Dodaj usługę</strong> → <strong>Prefiks URL</strong> i wklej adres: <button type="button" class="copy" data-copy-text="{BASE}">Kopiuj adres strony</button></li>
      <li>Weryfikacja: wybierz <strong>Plik HTML</strong> i kliknij <strong>Weryfikuj</strong> (plik jest już na stronie). Jeśli Google każe pobrać inny plik — wyślij mi jego nazwę.</li>
      <li>W menu <strong>Mapy witryn</strong> wpisz <code>sitemap.xml</code> <button type="button" class="copy" data-copy-text="sitemap.xml">Kopiuj</button> i kliknij <strong>Prześlij</strong>.</li>
      <li>W <strong>Sprawdzaniu adresu URL</strong> wklej adres strony głównej i kliknij <strong>Poproś o zindeksowanie</strong>.</li>
      <li><a class="btn" href="https://www.bing.com/webmasters" target="_blank" rel="noopener">Otwórz Bing Webmaster Tools</a> → <strong>Importuj z Google Search Console</strong> (Bing zasila też DuckDuckGo i Ecosię).</li>
    </ol>
  </section>

  <section class="kit-step">
    <h2>2. Wyślij link 10 znajomym (2 minuty)</h2>
    <p>Pierwsze wejścia i pierwsze uwagi najszybciej dadzą znajomi. Gotowa wiadomość:</p>
    <textarea class="msg" id="friendMsg" readonly rows="4">{html.escape(msg)}</textarea>
    <div class="row">
      <a class="btn primary" href="https://wa.me/?text={quote(msg, safe="")}" target="_blank" rel="noopener">WhatsApp</a>
      <a class="btn" href="fb-messenger://share?link={quote(BASE, safe="")}">Messenger</a>
      <a class="btn" href="sms:&amp;body={quote(msg, safe="")}">SMS</a>
      <a class="btn" href="https://www.facebook.com/sharer/sharer.php?u={quote(BASE, safe="")}" target="_blank" rel="noopener">Facebook</a>
      <button type="button" class="copy" data-copy="friendMsg">Kopiuj wiadomość</button>
    </div>
  </section>

  <section class="kit-step">
    <h2>3. Wrzuć karuzelę (5 minut na post)</h2>
    <p>Na telefonie przycisk <strong>Udostępnij zdjęcia</strong> otwiera menu udostępniania — wybierz Instagram albo Facebook, a potem wklej skopiowany opis. Jeden post w danej grupie, z treścią (nie sam link), i napisz wprost, że to Twoja strona. Odpowiadaj na komentarze — to najbardziej podbija zasięg.</p>
  </section>

{''.join(cards)}
  <section class="kit-step">
    <h2>4. Pokaż stronę tam, gdzie są ludzie</h2>
    <p>Jedna wzmianka w dużym portalu albo popularny wpis na Wykopie potrafi dać tysiące wejść. Napisz wprost, że to Twój projekt, i poproś o uwagi — to działa lepiej niż reklama.</p>
    <p><strong>Grafiki do relacji:</strong> w kalkulatorach <a href="narzedzia/czy-dobrze-zarabiam.html">„Czy dobrze zarabiam?”</a> i <a href="narzedzia/ile-zarabiam-na-godzine.html">„Ile zarabiam na godzinę?”</a> jest przycisk „Grafika do relacji” — wrzuć swój wynik („Zarabiam więcej niż X% Polaków”, „Smartfon kosztuje mnie 213 godzin pracy”) na Instagram z naklejką z linkiem i poproś znajomych, żeby sprawdzili swój.</p>
{''.join(f'''    <div class="cap">
      <div class="cap-head"><strong>{html.escape(n)}</strong><button type="button" class="copy" data-copy="x-{k}">Kopiuj</button></div>
      <textarea id="x-{k}" readonly rows="7">{html.escape(t)}</textarea>
    </div>
''' for k, (n, t) in enumerate(EXTRA))}  </section>
</main>'''

script = '''<script>
(function(){
  function flash(b){ var t = b.textContent; b.classList.add('done'); b.textContent = 'Skopiowano'; setTimeout(function(){ b.classList.remove('done'); b.textContent = t; }, 1600); }
  function copy(text, b){
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function(){ flash(b); }, function(){ fallback(text, b); });
    else fallback(text, b);
  }
  function fallback(text, b){ var t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); flash(b); } catch (e) {} t.remove(); }
  document.querySelectorAll('[data-copy]').forEach(function(b){ b.addEventListener('click', function(){ copy(document.getElementById(b.getAttribute('data-copy')).value, b); }); });
  document.querySelectorAll('[data-copy-text]').forEach(function(b){ b.addEventListener('click', function(){ copy(b.getAttribute('data-copy-text'), b); }); });
  document.querySelectorAll('.share-files').forEach(function(b){
    b.addEventListener('click', function(){
      var paths = JSON.parse(b.getAttribute('data-files'));
      Promise.all(paths.map(function(p){ return fetch(p).then(function(r){ return r.blob(); }).then(function(bl){ return new File([bl], p.split('/').pop(), {type: 'image/jpeg'}); }); }))
        .then(function(files){
          if (navigator.canShare && navigator.canShare({files: files})) return navigator.share({files: files, title: b.getAttribute('data-title')});
          window.open(paths[0], '_blank');
        }).catch(function(){});
    });
  });
})();
</script>
'''
foot = foot.replace('</body>', script + '</body>', 1)
open(ROOT + 'udostepnij.html', 'w').write(head + main + foot)
print('kit:', len(cards), 'carousels,', sum(1 for _ in os.listdir(ROOT + 'pliki/karuzele')), 'images')
