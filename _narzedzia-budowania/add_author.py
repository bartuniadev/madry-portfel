# Author byline + "O autorze" page, driven by author.json next to this script:
#   {"name": "...", "bio": ["zdanie 1", "zdanie 2"], "role": "autor i redaktor"}
# Without author.json the script does nothing. Idempotent.
import glob, html, json, os, re, sys

S = os.path.dirname(os.path.abspath(__file__))
ROOT = '/home/user/madry-portfel/'
BASE = 'https://bartuniadev.github.io/madry-portfel/'
CFG = os.path.join(S, 'author.json')
if not os.path.exists(CFG):
    print('author: no author.json, skipped')
    sys.exit(0)
cfg = json.load(open(CFG))
NAME = cfg['name'].strip()
ROLE = cfg.get('role', 'autor i redaktor').strip()
BIO = [b.strip() for b in cfg.get('bio', []) if b.strip()]
PERSON = {"@type": "Person", "@id": BASE + "o-autorze.html#autor", "name": NAME, "url": BASE + "o-autorze.html",
          "worksFor": {"@id": BASE + "#organization"}}

# 1) the author page, built from the About page template
tpl = open(ROOT + 'o-nas.html').read()
head = tpl[:tpl.index('<main>')]
foot = tpl[tpl.index('</main>') + len('</main>'):]
title = f'O autorze — {NAME} | Mądry Portfel'
desc = f'{NAME} — {ROLE} Mądrego Portfela: kim jest, jak pisze o finansach osobistych dla młodych i jak sprawdza dane w źródłach urzędowych.'[:160]
e = lambda s: html.escape(s, quote=True)
head = re.sub(r'<title>.*?</title>', '<title>' + e(title) + '</title>', head)
for a in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
    head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + e(desc), head)
for a in ['property="og:title"', 'name="twitter:title"']:
    head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + e(title), head)
head = head.replace('madry-portfel/o-nas.html', 'madry-portfel/o-autorze.html')
head = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', '', head, flags=re.S)
ld = {"@context": "https://schema.org", "@type": "ProfilePage", "url": BASE + "o-autorze.html", "inLanguage": "pl-PL",
      "mainEntity": dict(PERSON, description=' '.join(BIO))}
head = head.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
bio_html = ''.join(f'  <p>{html.escape(b)}</p>\n' for b in BIO)
main = f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="index.html">Mądry Portfel</a> <span aria-hidden="true">/</span> <span aria-current="page">O autorze</span></nav>
  <h1>{html.escape(NAME)} — {html.escape(ROLE)}</h1>
{bio_html}
  <h2>Jak pracuję</h2>
  <ul>
    <li>Każdy tekst opieram na źródłach urzędowych (podatki.gov.pl, ZUS, GUS, Dziennik Ustaw) i podaję je przy artykule.</li>
    <li>Przy pisaniu i wyliczeniach korzystam z narzędzi AI, ale kwoty, limity i terminy sprawdzam w źródłach, zanim trafią na stronę.</li>
    <li>Nie sprzedaję produktów finansowych i nie biorę pieniędzy za polecanie banków czy funduszy.</li>
  </ul>
  <p>Szczegóły: <a href="jak-powstaja-tresci.html">jak powstają treści i skąd bierzemy dane</a>. Znalazłeś błąd? <a href="https://github.com/bartuniadev/madry-portfel/issues" rel="noopener">Zgłoś go</a> albo napisz na adres ze strony <a href="o-nas.html">O nas</a>.</p>
</main>'''
open(ROOT + 'o-autorze.html', 'w').write(head + main + foot)

# 2) byline under the meta line + Person author in structured data (articles and salary pages)
changed = 0
for f in glob.glob(ROOT + 'artykuly/*.html') + glob.glob(ROOT + 'wynagrodzenia/*.html'):
    s = open(f).read()
    o = s
    byline = f'<p class="byline">Autor: <a href="../o-autorze.html">{html.escape(NAME)}</a> · dane sprawdzone w źródłach urzędowych · <a href="../jak-powstaja-tresci.html">jak powstają treści</a></p>'
    s = re.sub(r'\n  <p class="byline">.*?</p>', '', s)
    m = re.search(r'<p class="meta">.*?</p>', s, re.S)
    if m:
        s = s[:m.end()] + '\n  ' + byline + s[m.end():]

    def fix(mm):
        try:
            d = json.loads(mm.group(1))
        except Exception:
            return mm.group(0)
        hit = False
        for n in d.get('@graph', [d]):
            if isinstance(n, dict) and n.get('@type') == 'Article':
                n['author'] = dict(PERSON); hit = True
        if not hit:
            return mm.group(0)
        return '<script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n</script>'
    s = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', fix, s, flags=re.S)
    if s != o:
        open(f, 'w').write(s); changed += 1

# 3) sitemap entry
sm = open(ROOT + 'sitemap.xml').read()
if 'o-autorze.html' not in sm:
    sm = sm.replace('</urlset>', f'  <url><loc>{BASE}o-autorze.html</loc><lastmod>2026-11-19</lastmod></url>\n</urlset>')
    open(ROOT + 'sitemap.xml', 'w').write(sm)
print('author: page written, bylines in', changed, 'pages')
