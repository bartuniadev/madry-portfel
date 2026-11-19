# Unifies publisher/author structured data across the site (idempotent):
# one Organization with PNG logo, publishing principles and the open-source repo;
# Article.isAccessibleForFree; AboutPage/WebPage data for the about and methodology pages.
import glob, json, os, re

ROOT = '/home/user/madry-portfel/'
BASE = 'https://bartuniadev.github.io/madry-portfel/'
ORG_ID = BASE + '#organization'
ORG = {
    "@type": "Organization", "@id": ORG_ID, "name": "Mądry Portfel", "url": BASE,
    "logo": {"@type": "ImageObject", "url": BASE + "assets/logo-512.png", "width": 512, "height": 512},
    "sameAs": ["https://github.com/bartuniadev/madry-portfel"],
    "publishingPrinciples": BASE + "jak-powstaja-tresci.html",
}
AUTHOR = {"@type": "Organization", "@id": ORG_ID, "name": "Mądry Portfel", "url": BASE}
PAGES = {
    'o-nas.html': {"@context": "https://schema.org", "@type": "AboutPage", "name": "O nas — Mądry Portfel", "url": BASE + "o-nas.html", "inLanguage": "pl-PL", "about": ORG, "publisher": ORG},
    'jak-powstaja-tresci.html': {"@context": "https://schema.org", "@type": "WebPage", "name": "Jak powstają treści i skąd bierzemy dane", "url": BASE + "jak-powstaja-tresci.html", "inLanguage": "pl-PL", "about": {"@id": ORG_ID}, "publisher": ORG},
}


def fix_node(n):
    t = n.get('@type')
    if t == 'Organization' and n.get('name') == 'Mądry Portfel':
        n.clear(); n.update(json.loads(json.dumps(ORG)))
        return
    if isinstance(n.get('publisher'), dict) and n['publisher'].get('name', 'Mądry Portfel') == 'Mądry Portfel':
        n['publisher'] = json.loads(json.dumps(ORG))
    if isinstance(n.get('author'), dict) and n['author'].get('@type') == 'Organization' and n['author'].get('name') == 'Mądry Portfel':
        n['author'] = dict(AUTHOR)
    if t == 'Article':
        n['isAccessibleForFree'] = True
    if t == 'WebSite':
        n['publisher'] = {"@id": ORG_ID}
        n.setdefault('inLanguage', 'pl-PL')


changed = 0
for f in glob.glob(ROOT + '*.html') + glob.glob(ROOT + '*/*.html'):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith('_') or os.path.basename(f).startswith('google'):
        continue
    s = open(f).read()
    orig = s

    def repl(m):
        raw = m.group(1)
        try:
            d = json.loads(raw)
        except Exception:
            return m.group(0)
        before = json.dumps(d, ensure_ascii=False, sort_keys=True)
        for n in d.get('@graph', [d]):
            if isinstance(n, dict):
                fix_node(n)
        if json.dumps(d, ensure_ascii=False, sort_keys=True) == before:
            return m.group(0)
        return '<script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n</script>'

    s = re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', repl, s, flags=re.S)
    if rel in PAGES and 'application/ld+json' not in s:
        s = s.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(PAGES[rel], ensure_ascii=False, indent=2) + '\n</script>\n</head>', 1)
    if s != orig:
        open(f, 'w').write(s)
        changed += 1
print('structured data updated in', changed, 'pages')
