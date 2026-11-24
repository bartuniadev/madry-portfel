# Builds two hidden (noindex) pages for Instagram:
#  linki.html     — "link in bio" page with buttons to the most useful tools and articles
#  instagram.html — the owner's launch plan: profile setup, highlight covers, 2-week posting
#                   calendar (carousels + Reels) with captions to copy, story ideas and tips.
# Assets: karuzele/*.png (carousels), ig/*.png and ig/reel-*.mp4 next to this script.
import html, json, os, re, shutil
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/madry-portfel/'
BASE = 'https://bartuniadev.github.io/madry-portfel/'
K, IG = S + '/karuzele/', S + '/ig/'
md = open(K + 'opisy-postow.md').read()


def ig_caption(prefix):
    i = md.index('## ' + prefix)
    j = md.find('\n## ', i + 3)
    block = md[i:j if j > 0 else len(md)]
    m = re.search(r'### Instagram\n((?:>.*\n?)+)', block)
    return '\n'.join(l[2:] if l.startswith('> ') else '' for l in m.group(1).rstrip('\n').split('\n')).strip()


# --- assets
os.makedirs(ROOT + 'pliki/instagram', exist_ok=True)
os.makedirs(ROOT + 'pliki/karuzele', exist_ok=True)
Image.open(IG + 'profilowe.png').convert('RGB').save(ROOT + 'pliki/instagram/profilowe.jpg', quality=92)
HL = ['kalkulatory', 'pensja', 'kalendarz', 'oszczedzanie', 'podatki']
for k in HL:
    Image.open(IG + f'wyroznione-{k}.png').convert('RGB').save(ROOT + f'pliki/instagram/wyroznione-{k}.jpg', quality=90)
REELS = ['weekendy', 'niedziele', 'godziny', 'l4']
for r in REELS:
    shutil.copy(IG + f'reel-{r}.mp4', ROOT + f'pliki/instagram/reel-{r}.mp4')


def carousel(sid):
    out, n = [], 1
    while os.path.exists(K + f'{sid}-{n}.png'):
        dst = f'pliki/karuzele/{sid}-{n}.jpg'
        Image.open(K + f'{sid}-{n}.png').convert('RGB').save(ROOT + dst, quality=88, optimize=True, progressive=True)
        out.append(dst)
        n += 1
    return out


REEL_CAP = {
    'weekendy': '28 dni wolnego za 11 dni urlopu — tak rozłóż wolne w 2027 🗓️ Zapisz i wyślij osobie, z którą planujesz wyjazdy. Pełny kalendarz — link w bio.\n\n#długiweekend #urlop #dniwolne2027 #podróże #praca',
    'niedziele': 'Grudzień w sklepach: niedziele handlowe 6, 13 i 20 grudnia, a od 24 do 27 grudnia duże sklepy zamknięte 🛒 Zapisz, żeby nie zapomnieć. Wszystkie daty na 2027 — link w bio.\n\n#niedzielahandlowa #święta #zakupy #wigilia #grudzień',
    'godziny': 'Ile godzin pracujesz na nowy smartfon? 📱 Przy 7000 zł brutto to 213 godzin. Policz swoje rzeczy — link w bio.\n\n#oszczędzanie #pieniądze #finanseosobiste #świadomezakupy',
    'l4': 'Ile naprawdę dostaniesz na L4? Na rękę tracisz mniej, niż myślisz 👀 Kalkulator L4 — link w bio.\n\n#L4 #praca #wynagrodzenie #prawopracy',
}
# (date, kind, id, title, note)
PLAN = [
    ('śr 25.11', 'post', 'start', 'Cześć, tu Mądry Portfel', 'Pierwszy post — przypnij go na górze profilu.'),
    ('czw 26.11', 'post', 'godziny', 'Ile godzin pracy kosztuje smartfon', ''),
    ('pt 27.11', 'reel', 'weekendy', 'Reel: 28 dni wolnego za 11 dni urlopu', 'Dodaj modną muzykę z biblioteki Instagrama.'),
    ('sob 28.11', 'post', 'niedziele', 'Niedziele handlowe w grudniu', ''),
    ('nd 29.11', 'post', 'zarobki', 'Czy dobrze zarabiasz? Mediana GUS', 'Przypnij jako drugi.'),
    ('wt 1.12', 'reel', 'l4', 'Reel: ile dostaniesz na L4', ''),
    ('czw 3.12', 'post', 'premia', 'Premia świąteczna — ile zostanie', ''),
    ('sob 5.12', 'reel', 'niedziele', 'Reel: kiedy sklepy są otwarte', 'Dzień przed niedzielą handlową 6 grudnia.'),
    ('wt 8.12', 'post', 'l4', 'Ile dostaniesz na L4', ''),
    ('czw 10.12', 'post', 'urlop', 'Masz 20 czy 26 dni urlopu?', ''),
    ('sob 12.12', 'reel', 'godziny', 'Reel: ile godzin pracujesz na smartfon', ''),
    ('od 20.12', 'post', 'zmiany2027', 'Zmiany w finansach od 1 stycznia 2027', 'Między 20 grudnia a 10 stycznia.'),
]
CAP_PREFIX = {'start': 'Karuzela 6', 'godziny': 'Karuzela 7', 'l4': 'Karuzela 8', 'urlop': 'Karuzela 9',
              'zarobki': 'Karuzela 1', 'zmiany2027': 'Karuzela 2', 'premia': 'Karuzela 3', 'weekendy': 'Karuzela 4', 'niedziele': 'Karuzela 5'}

e = lambda s: html.escape(s, quote=True)
items = []
for k, (date, kind, sid, title, note) in enumerate(PLAN):
    if kind == 'post':
        imgs = carousel(sid)
        cap = ig_caption(CAP_PREFIX[sid])
        thumbs = ''.join(f'<a href="{p}" target="_blank" rel="noopener"><img src="{p}" alt="Slajd {i + 1}" width="96" height="120" loading="lazy"></a>' for i, p in enumerate(imgs))
        media = f'''<div class="thumbs">{thumbs}</div>
      <div class="row"><button type="button" class="btn primary share-files" data-files='{json.dumps(imgs)}' data-type="image/jpeg" data-title="{e(title)}">Udostępnij zdjęcia do Instagrama</button></div>'''
    else:
        cap = REEL_CAP[sid]
        v = f'pliki/instagram/reel-{sid}.mp4'
        media = f'''<video src="{v}" controls playsinline muted preload="metadata" width="180" height="320"></video>
      <div class="row"><button type="button" class="btn primary share-files" data-files='{json.dumps([v])}' data-type="video/mp4" data-title="{e(title)}">Udostępnij film do Instagrama</button> <a class="btn" href="{v}" download>Pobierz MP4</a></div>'''
    items.append(f'''  <section class="kit-card">
    <p class="when"><strong>{e(date)}</strong> · {"Karuzela" if kind == "post" else "Reel"}{" · " + e(note) if note else ""}</p>
    <h3>{e(title)}</h3>
      {media}
    <div class="cap">
      <div class="cap-head"><strong>Opis</strong><button type="button" class="copy" data-copy="p-{k}">Kopiuj</button></div>
      <textarea id="p-{k}" readonly rows="6">{e(cap)}</textarea>
    </div>
  </section>
''')

BIO = 'Finanse na starcie kariery 💸\nPensja, podatki, oszczędzanie — konkretnie\n17 darmowych kalkulatorów, 0 reklam\n👇 Kalkulatory i poradniki'
NAME = 'Mądry Portfel | Finanse'
LINK = BASE + 'linki.html'
STORIES = [
    ('Quiz', 'Naklejka „Quiz”: „Ile procent Polaków zarabia mniej niż 7550 zł brutto?” — 25% / 50% / 75%. Poprawna: 50% (to mediana). W kolejnej relacji naklejka z linkiem do „Czy dobrze zarabiam?”.'),
    ('Ankieta', 'Naklejka „Ankieta”: „Kawa na mieście codziennie?” Tak / Nie. Następna relacja: „Rok takiej kawy to 123 godziny pracy” + link do „Ile zarabiam na godzinę?”.'),
    ('Twój wynik', 'Zrób swoją grafikę w „Czy dobrze zarabiam?” albo „Ile zarabiam na godzinę?” (przycisk „Grafika do relacji”), dodaj naklejkę z linkiem i napisz „A Wy?”.'),
    ('Odliczanie', 'Naklejka „Odliczanie” do niedzieli handlowej 6 grudnia — kto ją kliknie, dostanie przypomnienie. Link do listy niedziel handlowych.'),
    ('Pytania', 'Naklejka „Pytania”: „Zapytaj o pensję, podatki albo urlop — odpowiem w relacjach”. Odpowiedzi to gotowe pomysły na kolejne posty.'),
    ('Repost', 'Po każdym nowym poście udostępnij go w relacji z dopiskiem „Nowy post 👆” — to najprostszy sposób, żeby obserwujący go zobaczyli.'),
]

tpl = open(ROOT + 'o-nas.html').read()
head0 = tpl[:tpl.index('<main>')]
foot0 = tpl[tpl.index('</main>') + len('</main>'):]


def page(title, main, extra_css='', script=''):
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head0)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', h, flags=re.S)
    h = re.sub(r'<meta (property="og:[^"]+"|name="twitter:[^"]+"|name="description") content="[^"]*">\n?', '', h)
    h = re.sub(r'<link rel="canonical"[^>]*>\n?', '', h)
    h = h.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n<style>\n' + extra_css + '</style>\n</head>', 1)
    return h + main + foot0.replace('</body>', script + '</body>', 1)


KIT_CSS = open(ROOT + 'udostepnij.html').read().split('<style>\n', 1)[1].split('</style>', 1)[0]
COPY_JS = re.search(r'<script>\n\(function\(\)\{\n  function flash.*?</script>\n', open(ROOT + 'udostepnij.html').read(), re.S).group(0)
COPY_JS = COPY_JS.replace("new File([bl], p.split('/').pop(), {type: 'image/jpeg'})", "new File([bl], p.split('/').pop(), {type: b.getAttribute('data-type') || 'image/jpeg'})")

hl_html = ''.join(f'<a href="pliki/instagram/wyroznione-{k}.jpg" target="_blank" rel="noopener"><img src="pliki/instagram/wyroznione-{k}.jpg" alt="Okładka: {k}" width="68" height="120" loading="lazy"></a>' for k in HL)
main = f'''<main>
  <h1>Start na Instagramie</h1>
  <p class="lead">Wszystko do założenia profilu i pierwszych dwóch tygodni publikacji: grafiki, filmy i opisy do skopiowania. Ta strona jest tylko dla Ciebie — nie ma jej w menu ani w wyszukiwarkach.</p>

  <section class="kit-step">
    <h2>1. Załóż profil (10 minut)</h2>
    <ol>
      <li><strong>Nazwa użytkownika</strong> — sprawdź, która jest wolna: <code>madry.portfel</code>, <code>madryportfel</code> albo <code>madry_portfel</code>.</li>
      <li><strong>Imię i nazwisko</strong> (to pole jest wyszukiwane): <button type="button" class="copy" data-copy-text="{e(NAME)}">Kopiuj: {e(NAME)}</button></li>
      <li><strong>Bio</strong>: <textarea id="bio" readonly rows="4">{e(BIO)}</textarea> <button type="button" class="copy" data-copy="bio">Kopiuj bio</button></li>
      <li><strong>Link w bio</strong> — strona z najważniejszymi kalkulatorami: <button type="button" class="copy" data-copy-text="{LINK}">Kopiuj link</button> (<a href="linki.html">zobacz, jak wygląda</a>)</li>
      <li><strong>Zdjęcie profilowe</strong>: <a href="pliki/instagram/profilowe.jpg" target="_blank" rel="noopener"><img class="avatar" src="pliki/instagram/profilowe.jpg" alt="Zdjęcie profilowe" width="72" height="72"></a> — przytrzymaj i zapisz.</li>
      <li>W ustawieniach przełącz na <strong>konto profesjonalne → Twórca</strong> (za darmo) — zobaczysz statystyki zasięgów.</li>
      <li><strong>Okładki wyróżnionych relacji</strong> (Kalkulatory, Pensja, Kalendarz, Oszczędzanie, Podatki):<div class="thumbs hl">{hl_html}</div></li>
    </ol>
  </section>

  <section class="kit-step">
    <h2>2. Plan na dwa tygodnie</h2>
    <p>Publikuj wieczorem, między 19 a 21. Pod każdym postem odpowiadaj na komentarze przez pierwszą godzinę — to najmocniej podbija zasięg. Do Reelsów dodaj modną muzykę z biblioteki Instagrama (pliki są bez dźwięku).</p>
  </section>
{''.join(items)}
  <section class="kit-step">
    <h2>3. Relacje — pomysły na codzień</h2>
    <ul>
{''.join(f'      <li><strong>{e(t)}:</strong> {e(d)}</li>{chr(10)}' for t, d in STORIES)}    </ul>
  </section>
</main>'''
EXTRA_CSS = KIT_CSS + '''.avatar{width:72px;height:72px;border-radius:50%;vertical-align:middle}
.thumbs.hl img{width:68px;height:120px}
.thumbs img{width:96px;height:120px}
video{display:block;border-radius:12px;background:#000;margin:6px 0}
#bio{width:100%;font:inherit;font-size:.9rem;padding:10px;border:1px solid var(--border);border-radius:10px;background:var(--bg);margin:6px 0}
'''
open(ROOT + 'instagram.html', 'w').write(page('Start na Instagramie | Mądry Portfel', main, EXTRA_CSS, COPY_JS))

# --- link in bio
LINKS = [
    ('narzedzia/czy-dobrze-zarabiam.html', 'Czy dobrze zarabiam?', 'Twoja pensja na tle Polaków — dane GUS'),
    ('narzedzia/ile-zarabiam-na-godzine.html', 'Ile zarabiam na godzinę?', 'I ile godzin pracy kosztuje smartfon czy czynsz'),
    ('artykuly/niedziele-handlowe-2026-2027.html', 'Niedziele handlowe 2026 i 2027', 'Najbliższa niedziela handlowa i pełna lista'),
    ('artykuly/dni-wolne-od-pracy-2027.html', 'Dni wolne 2027 i długie weekendy', '28 dni wolnego za 11 dni urlopu'),
    ('narzedzia/kalkulator-l4.html', 'Kalkulator L4', 'Ile dostaniesz na zwolnieniu'),
    ('narzedzia/kalkulator-urlopu.html', 'Kalkulator urlopu', '20 czy 26 dni i ekwiwalent'),
    ('narzedzia/kalkulator-brutto-netto.html', 'Kalkulator brutto–netto 2027', 'Ile na rękę w każdym miesiącu'),
    ('artykuly/premia-swiateczna-bony-ile-netto.html', 'Premia świąteczna ile netto', 'Tabela 500–5000 zł i bony z ZFŚS'),
    ('artykuly/zmiany-w-finansach-2027.html', 'Zmiany od 1 stycznia 2027', 'Płaca minimalna, IKE, IKZE, OKI'),
]
LINK_CSS = '''.lb{max-width:520px;margin:0 auto;text-align:center}
.lb .av{width:96px;height:96px;border-radius:50%;margin:8px auto 10px;display:block}
.lb h1{font-size:1.7rem;margin:0}
.lb .lead{font-size:1rem;margin:6px 0 22px}
.lb a.lk{display:block;text-align:left;text-decoration:none;color:var(--text);background:var(--card);border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:10px 0;transition:border-color .2s,transform .2s}
.lb a.lk:hover{border-color:var(--accent);transform:translateY(-2px)}
.lb a.lk strong{display:block;color:var(--accent-dark);font-size:1.02rem}
.lb a.lk span{font-size:.86rem;color:var(--muted)}
.lb .more{display:flex;gap:10px;justify-content:center;margin:18px 0 0;flex-wrap:wrap}
.lb .more a{font-weight:600;text-decoration:none}
'''
lmain = f'''<main>
  <div class="lb">
    <img class="av" src="pliki/instagram/profilowe.jpg" alt="" width="96" height="96">
    <h1>Mądry Portfel</h1>
    <p class="lead">Finanse na starcie kariery — kalkulatory i poradniki bez reklam.</p>
{''.join(f'    <a class="lk" href="{u}"><strong>{e(t)}</strong><span>{e(d)}</span></a>{chr(10)}' for u, t, d in LINKS)}    <p class="more"><a href="narzedzia/index.html">Wszystkie kalkulatory →</a> <a href="index.html#poradniki">Wszystkie poradniki →</a></p>
  </div>
</main>'''
open(ROOT + 'linki.html', 'w').write(page('Mądry Portfel — linki', lmain, LINK_CSS))
print('instagram.html + linki.html written;', len(PLAN), 'plan items')
