# Adds ids to article H2 headings and a collapsible "W tym artykule" table of contents
# (after the "W skrócie" box, or after the meta line). Idempotent: rebuilds the TOC each run.
import glob, re, html, unicodedata

ROOT = '/home/user/madry-portfel/'
MIN_H2 = 4


def slugify(t):
    t = unicodedata.normalize('NFKD', t.replace('ł', 'l').replace('Ł', 'L'))
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:60].rstrip('-') or 'sekcja'


def text(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


changed = 0
for f in sorted(glob.glob(ROOT + 'artykuly/*.html') + glob.glob(ROOT + 'wynagrodzenia/*.html')):
    s = open(f).read()
    orig = s
    s = re.sub(r'\n*  <details class="toc">.*?</details>\n*', '\n\n', s, flags=re.S)
    start = s.find('<p class="meta">')
    end_candidates = [i for i in (s.find('<div class="share"'), s.find('<section class="sources"')) if i > 0]
    if start < 0 or not end_candidates:
        continue
    end = min(end_candidates)
    body = s[start:end]
    used, items = set(), []

    def add_id(m):
        attrs, inner = m.group(1) or '', m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        if idm:
            hid = idm.group(1)
        else:
            base = slugify(text(inner)); hid = base; k = 2
            while hid in used:
                hid = f'{base}-{k}'; k += 1
        used.add(hid)
        items.append((hid, text(inner)))
        return f'<h2{attrs if idm else attrs + f" id=\"{hid}\""}>{inner}</h2>'

    body2 = re.sub(r'<h2([^>]*)>(.*?)</h2>', add_id, body, flags=re.S)
    if len(items) >= MIN_H2:
        toc = ('  <details class="toc">\n    <summary>W tym artykule ({})</summary>\n    <ol>\n'.format(len(items)) +
               ''.join(f'      <li><a href="#{h}">{html.escape(t, quote=False)}</a></li>\n' for h, t in items) + '    </ol>\n  </details>\n')
        anchor = re.search(r'<p class="tldr">.*?</p>\n', body2, re.S) or re.search(r'<p class="meta">.*?</p>\n', body2, re.S)
        body2 = body2[:anchor.end()] + '\n' + toc + body2[anchor.end():]
    s = s[:start] + body2 + s[end:]
    if s != orig:
        open(f, 'w').write(s)
        changed += 1
print('toc updated in', changed, 'pages')
