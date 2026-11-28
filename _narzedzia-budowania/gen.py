import re, sys, pathlib
root = pathlib.Path('/home/user/madry-portfel')
tpl = (root/'artykuly/brutto-netto-rodzaje-umow.html').read_text()
head_end = tpl.index('<main>')
foot_start = tpl.index('<footer>')
BASE = 'https://bartuniadev.github.io/madry-portfel/'

def build(slug, title, desc, cat_name, cat_id, icon, hero_label, body, related, sources=None):
    import extras_share
    body = body + extras_share.share_html('https://bartuniadev.github.io/madry-portfel/artykuly/'+slug+'.html', title) + sources_html(sources)
    title = title.replace('"', '\u201d'); desc = desc.replace('"', '\u201d')
    h = tpl[:head_end]
    old_t = 'Brutto vs netto i rodzaje umów — jak czytać ofertę pracy'
    old_d = 'Umowa o pracę, zlecenie czy B2B — dlaczego ta sama kwota brutto oznacza zupełnie inne pieniądze na koncie. Jak porównywać oferty pracy, żeby się nie przeliczyć.'
    h = h.replace(old_t, title).replace(old_d, desc)
    h = h.replace('brutto-netto-rodzaje-umow.html', slug + '.html')
    h = h.replace('"Zacznij tutaj"', '"%s"' % cat_name).replace('index.html#zacznij-tutaj', 'index.html#' + cat_id)
    import re as _re
    _m = _re.search(r'Opublikowano (\d+) listopada 2026', body)
    _d = '2026-11-%02d' % int(_m.group(1)) if _m else '2026-11-15'
    _MON = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12}
    _u = _re.search(r'Zaktualizowano (\d+) (\w+) (\d{4})', body)
    _dm = '%s-%02d-%02d' % (_u.group(3), _MON[_u.group(2)], int(_u.group(1))) if _u and _u.group(2) in _MON else _d
    h = h.replace('"datePublished": "2026-09-21"', '"datePublished": "%s"' % _d).replace('"dateModified": "2026-09-21"', '"dateModified": "%s"' % _dm)
    hero = f'''  <div class="hero-graphic">
    <svg viewBox="0 0 720 160" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{hero_label}">
      <defs>
        <linearGradient id="heroBg" x1="0" y1="0" x2="720" y2="160" gradientUnits="userSpaceOnUse">
          <stop offset="0" stop-color="#eef7f0"/>
          <stop offset="1" stop-color="#d7ecdc"/>
        </linearGradient>
        <radialGradient id="heroGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/>
          <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <rect width="720" height="160" fill="url(#heroBg)"/>
      <circle cx="360" cy="80" r="68" fill="url(#heroGlow)"/>
      <g opacity="0.5">
        <circle cx="88" cy="34" r="12" fill="none" stroke="#1f7a4d" stroke-width="2"/>
        <circle cx="118" cy="126" r="5" fill="#e0a63f"/>
        <circle cx="636" cy="118" r="9" fill="none" stroke="#1f7a4d" stroke-width="2"/>
        <circle cx="602" cy="32" r="4" fill="#e0a63f"/>
      </g>
      <g class="hero-icon" transform="translate(316,20) scale(4.2)" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" color="#145c39">
        {icon}
      </g>
    </svg>
  </div>
'''
    icon_svg = f'<svg class="topic-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{icon}</svg>'
    main = f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="../index.html">Artykuły</a> <span aria-hidden="true">/</span> <a href="../index.html#{cat_id}">{cat_name}</a> <span aria-hidden="true">/</span> <span aria-current="page">{title}</span></nav>
  <div class="article-header">
    <div class="icon-badge lg">{icon_svg}</div>
    <h1>{title}</h1>
  </div>
{hero}
{body}
  <section class="related-articles reveal">
    <h2>Powiązane artykuły</h2>
    <ul class="article-list">
{related}    </ul>
  </section>
</main>

'''
    (root/'artykuly'/(slug+'.html')).write_text(h + main + tpl[foot_start:])

def sources_html(sources):
    if not sources: return ''
    items = ''.join('      <li><a href="%s" rel="noopener">%s</a> — %s</li>\n' % (u,t,d) for u,t,d in sources)
    return ('''
  <section class="sources">
    <h2>Źródła i przydatne strony</h2>
    <ul>
''' + items + '''    </ul>
    <p class="sources-note">Kwoty, limity i adresy sprawdzone w listopadzie 2026 r. Przepisy się zmieniają — w razie rozbieżności wiążące są informacje na stronach urzędowych.</p>
  </section>
''')

def related_from(slugs):
    out = ''
    for s in slugs:
        t = (root/'artykuly'/(s+'.html')).read_text()
        m = re.search(r'<div class="icon-badge lg">(<svg.*?</svg>)</div>\s*<h1>(.*?)</h1>', t, re.S)
        d = re.search(r'<meta name="description" content="(.*?)">', t).group(1)
        out += f'''    <li>
      <div class="icon-badge">{m.group(1)}</div>
      <div class="article-body">
        <a href="{s}.html">{m.group(2)}</a>
        <p>{d}</p>
      </div>
    </li>
'''
    return out

sys.modules[__name__].__dict__.update(build=build, related_from=related_from, sources_html=sources_html)
