# Sync "Powiązane artykuły" cards with each target article's current H1 and meta description.
import re, glob, html, os
ROOT = '/home/user/madry-portfel/artykuly/'
info = {}
for f in glob.glob(ROOT + '*.html'):
    s = open(f).read()
    h1 = re.search(r'<h1>(.*?)</h1>', s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    info[os.path.basename(f)] = (re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else None,
                                 html.unescape(d.group(1)) if d else None)
changed = 0
card = re.compile(r'(<a href="([a-z0-9-]+\.html)">)(.*?)(</a>\s*<p>)(.*?)(</p>)', re.S)
for f in sorted(glob.glob(ROOT + '*.html')):
    s = open(f).read()
    i = s.find('<h2>Powiązane artykuły</h2>')
    if i < 0:
        continue
    j = s.find('</ul>', i)
    blk = s[i:j]
    def fix(m):
        t = info.get(m.group(2))
        if not t or not t[0] or not t[1]:
            return m.group(0)
        return m.group(1) + html.escape(t[0], quote=False) + m.group(4) + html.escape(t[1], quote=False) + m.group(6)
    nb = card.sub(fix, blk)
    if nb != blk:
        open(f, 'w').write(s[:i] + nb + s[j:])
        changed += 1
print('related cards synced in', changed, 'articles')
