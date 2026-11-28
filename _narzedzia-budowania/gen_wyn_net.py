# Generates wynagrodzenia/<kwota>-netto-ile-brutto.html — how much gross you need for a given take-home pay.
import os, sys, re, json, html, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_wyn as G

NETS = [4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 9000, 10000, 12000]


def solve(fn, target):
    lo, hi = 0.0, 300000.0
    for _ in range(80):
        m = (lo + hi) / 2
        if fn(m) < target:
            lo = m
        else:
            hi = m
    g = math.ceil(hi * 100) / 100
    k = 0
    while fn(g) < target and k < 1000:
        g = round(g + 0.01, 2)
        k += 1
    return g


def page(n):
    slug = f'{n}-netto-ile-brutto'
    url = G.BASE + f'wynagrodzenia/{slug}.html'
    ns = f'{n:,}'.replace(',', '\u00a0')
    g_std = solve(lambda g: G.etat(g)['net'], n)
    g_ppk = solve(lambda g: G.etat(g, ppk=True)['net'], n)
    g_young = solve(lambda g: G.etat(g, young=True)['net'], n)
    g_nopit2 = solve(lambda g: G.etat(g, pit2=False)['net'], n)
    z_only = solve(lambda g: G.zlecenie(g, 'only'), n)
    z_job = solve(lambda g: G.zlecenie(g, 'job'), n)
    cost = G.r2(g_std * 1.2048)
    p = G.pct(g_std)
    gs0 = G.zl0(g_std)
    title = f'Ile brutto, żeby mieć {ns} zł netto? Ok. {gs0} w 2027'
    seo_title = f'{n} netto ile brutto 2027? Ok. {round(g_std)} zł brutto'
    desc = (f'Żeby dostać {ns} zł na rękę na umowie o pracę w 2027 r., potrzebujesz ok. {gs0} brutto (PIT-2, bez PPK). '
            f'Z PPK {G.zl0(g_ppk)}, do 26 lat {G.zl0(g_young)}, zlecenie.')
    rows = [
        ('Standard: PIT-2, bez PPK', g_std),
        ('Z PPK (2% + 1,5% pracodawcy)', g_ppk),
        ('Do 26 lat (ulga dla młodych), bez PPK', g_young),
        ('Bez złożonego PIT-2', g_nopit2),
    ]
    table = '\n'.join(f'      <tr><td>{html.escape(a)}</td><td><strong>{G.zl(b)}</strong></td></tr>' for a, b in rows)
    young_cross = math.ceil(G.YOUNG / g_young) if g_young * 12 > G.YOUNG else None
    young_note = (f'<p><small>Przy uldze dla młodych kwota dotyczy miesięcy przed wyczerpaniem limitu 85\u00a0528 zł przychodu rocznie — przy {G.zl0(g_young)} brutto stanie się to w {G.MONTHS_LOC[young_cross - 1]}; potem pobierana jest zaliczka na podatek i do tych samych {ns} zł netto potrzeba ok. {gs0} brutto.</small></p>\n' if young_cross else '')
    nets, cross = G.year_sim(g_std)
    if cross:
        young_note += (f'<p><small>Uwaga: przy {G.zl0(g_std)} brutto w {G.MONTHS_LOC[cross - 1]} dochód od początku roku przekroczy próg 120\u00a0000 zł i nadwyżka będzie opodatkowana stawką 32% — od tego miesiąca na rękę zostanie ok. {G.zl0(nets[-1])}. Żeby przez cały rok dostawać średnio {ns} zł netto, potrzeba więcej brutto; dokładnie policzysz to w kalkulatorze.</small></p>\n')
    nearest = min(G.AMOUNTS, key=lambda a: abs(a - g_std))
    nears = f'{nearest:,}'.replace(',', '\u00a0')
    others = ' · '.join((f'<strong>{x:,}'.replace(',', '\u00a0') + ' zł netto</strong>') if x == n else f'<a href="{x}-netto-ile-brutto.html">' + f'{x:,}'.replace(',', '\u00a0') + ' zł netto</a>' for x in NETS)
    ask = math.ceil(g_std / 100) * 100
    faq = [
        (f'Ile brutto to {ns} zł netto?', f'Na umowie o pracę w 2027 r. — ok. {gs0} brutto (z PIT-2, bez PPK, osoba powyżej 26 lat). Z PPK potrzeba ok. {G.zl0(g_ppk)} brutto.'),
        (f'Ile brutto, żeby mieć {ns} zł netto na zleceniu?', f'Gdy zlecenie jest jedyną pracą (ze składką chorobową) — ok. {G.zl0(z_only)} brutto. Gdy masz też etat z co najmniej płacą minimalną — ok. {G.zl0(z_job)} brutto. Student do 26 lat potrzebuje {ns} zł brutto.'),
        (f'Ile pracodawcę kosztuje {ns} zł netto?', f'Ok. {G.zl0(cost)} miesięcznie: {gs0} brutto plus składki płacone przez pracodawcę.'),
    ]
    faq_html = '\n'.join(f'  <details class="faq">\n    <summary>{html.escape(q)}</summary>\n    <p>{html.escape(a)}</p>\n  </details>' for q, a in faq)
    above = 'więcej' if g_std >= G.MED else 'mniej'

    body = f'''  <p class="meta">Wyliczenie · zasady na 2027 r. (te same co w 2026 r.) · Aktualizacja 19 listopada 2026</p>

  <p class="tldr"><strong>W skrócie:</strong> żeby dostać <strong>{ns} zł na rękę</strong> na umowie o pracę w 2027 r., potrzebujesz ok. <strong>{G.zl(g_std)} brutto</strong> (z PIT-2, bez PPK). Z PPK — {G.zl(g_ppk)}, a osoba do 26 lat — {G.zl(g_young)}. Pracodawcę kosztuje to ok. {G.zl0(cost)} miesięcznie.</p>

  <h2>{ns} zł netto ile brutto — umowa o pracę</h2>
  <table>
    <thead><tr><th>Wariant</th><th>Potrzebne brutto</th></tr></thead>
    <tbody>
{table}
    </tbody>
  </table>
{young_note}  <p>Inną kwotę albo swój wariant (PPK, dojazdy, rok 2026 lub 2027) policzysz w <a href="../narzedzia/kalkulator-brutto-netto.html?netto={n}&amp;rok=2027&amp;ppk=0">kalkulatorze brutto–netto</a> — otworzy się od razu z tą kwotą w trybie „Netto → brutto”.</p>

  <h2>Ile brutto na umowie zlecenia</h2>
  <table>
    <thead><tr><th>Sytuacja</th><th>Potrzebne brutto</th></tr></thead>
    <tbody>
      <tr><td>Zlecenie to jedyna praca (ze składką chorobową)</td><td><strong>{G.zl(z_only)}</strong></td></tr>
      <tr><td>Masz też etat z co najmniej płacą minimalną</td><td><strong>{G.zl(z_job)}</strong></td></tr>
      <tr><td>Student lub uczeń do 26 lat</td><td><strong>{G.zl(n)}</strong></td></tr>
    </tbody>
  </table>
  <p>Swój wariant sprawdzisz w <a href="../narzedzia/kalkulator-umowy-zlecenia.html">kalkulatorze umowy zlecenia</a>.</p>

  <h2>Jak podać oczekiwania finansowe na rozmowie</h2>
  <ul>
    <li><strong>Mów w brutto miesięcznie</strong> — tak liczą pracodawcy i tak podaje się widełki w ogłoszeniach. Chcesz {ns} zł na rękę? Na etacie podaj co najmniej ok. <strong>{G.zl0(ask)} brutto</strong>.</li>
    <li><strong>Zapytaj o PPK i benefity</strong> — przy PPK do tej samej kwoty na rękę potrzeba ok. {G.zl0(g_ppk - g_std)} brutto więcej, ale dopłata pracodawcy trafia na Twoje konto.</li>
    <li><strong>Przy zleceniu i B2B przeliczaj inaczej</strong> — brak płatnego urlopu i chorobowego to realny koszt; patrz: <a href="../artykuly/b2b-czy-etat-porownanie.html">B2B czy etat</a>.</li>
  </ul>
  <p>Więcej o rozmowie o pieniądzach: <a href="../artykuly/rozmowa-o-pieniadzach-w-rekrutacji.html">oczekiwania finansowe w rekrutacji</a> i <a href="../artykuly/negocjacje-podwyzka-zmiana-pracy.html">jak negocjować podwyżkę</a>.</p>

  <h2>Czy {ns} zł netto to dużo?</h2>
  <p>{gs0} brutto to o {G.zl0(abs(g_std - G.MED))} {above} niż mediana płac w Polsce (7550 zł brutto według GUS za maj 2026 r.) — więcej zarabia ok. {round(100 - p)}% pracujących, mniej — ok. {round(p)}%. Pełne wyliczenie dla zbliżonej pensji: <a href="{nearest}-brutto-ile-netto.html">{nears} zł brutto ile netto</a>; swoją pozycję sprawdzisz w kalkulatorze <a href="../narzedzia/czy-dobrze-zarabiam.html">Czy dobrze zarabiam?</a>.</p>

  <h2>Najczęstsze pytania</h2>
{faq_html}

  <h2>Inne kwoty netto</h2>
  <p class="amounts-nav">{others}</p>
  <p>Odwrotnie — od brutto do netto: <a href="../artykuly/ile-na-reke-tabela-brutto-netto.html">tabela brutto–netto od 4950 do 20 000 zł</a>.</p>

  <p><em>Treść ma charakter edukacyjny. Wyliczenia według zasad obowiązujących w listopadzie 2026 r. (skala PIT 12% do 120 000 zł dochodu, kwota zmniejszająca 300 zł miesięcznie, koszty uzyskania przychodu 250 zł); w 2027 r. zasady liczenia pensji są takie same — prezydent zawetował 27 listopada 2026 r. zmianę skali PIT. Rzeczywista wypłata może różnić się o kilka złotych przez zaokrąglenia.</em></p>
'''
    body = re.sub(r'(\d) (\d{3})(?!\d)', '\\1\u00a0\\2', body)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title.replace('\u00a0', ' '), "description": desc.replace('\u00a0', ' '), "inLanguage": "pl-PL",
         "datePublished": G.TODAY, "dateModified": G.TODAY, "mainEntityOfPage": url, "image": G.BASE + f'assets/og/{slug}.jpg',
         "author": {"@type": "Organization", "name": "Mądry Portfel", "url": G.BASE}, "publisher": {"@type": "Organization", "name": "Mądry Portfel", "url": G.BASE},
         "keywords": f'{n} netto ile brutto, ile brutto żeby mieć {n} netto, {n} na rękę ile brutto 2027'},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mądry Portfel", "item": G.BASE},
            {"@type": "ListItem", "position": 2, "name": "Ile na rękę — tabela", "item": G.BASE + 'artykuly/ile-na-reke-tabela-brutto-netto.html'},
            {"@type": "ListItem", "position": 3, "name": f'{n} zł netto ile brutto', "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q.replace('\u00a0', ' '), "acceptedAnswer": {"@type": "Answer", "text": a.replace('\u00a0', ' ')}} for q, a in faq]},
    ]}
    e = lambda s: html.escape(s.replace('\u00a0', ' '), quote=True)
    tpl = open(G.ROOT + f'wynagrodzenia/6000-brutto-ile-netto.html').read()
    head = tpl[:tpl.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>' + e(seo_title) + '</title>', head)
    for a in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + e(desc), head)
    for a in ['property="og:title"', 'name="twitter:title"']:
        head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + e(seo_title), head)
    head = head.replace('wynagrodzenia/6000-brutto-ile-netto.html', f'wynagrodzenia/{slug}.html').replace('assets/og/6000-brutto-ile-netto.jpg', f'assets/og/{slug}.jpg')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>', head, flags=re.S)
    assert '6000-brutto' not in head
    rest = tpl[tpl.index('</head>'):tpl.index('<main>')]
    footer = tpl[tpl.index('</main>') + len('</main>'):]
    icon = re.search(r'<div class="icon-badge lg">.*?</div>', tpl, re.S).group(0)
    share = G.share_html(url, title.replace('\u00a0', ' '))
    sources = tpl[tpl.index('  <section class="sources">'):tpl.index('</main>')]
    main = f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="../index.html">Artykuły</a> <span aria-hidden="true">/</span> <a href="../artykuly/ile-na-reke-tabela-brutto-netto.html">Ile na rękę</a> <span aria-hidden="true">/</span> <span aria-current="page">{ns} zł netto</span></nav>
  <div class="article-header">
    {icon}
    <h1>{html.escape(title)}</h1>
  </div>

{body}
{share}
{sources}</main>'''
    open(G.ROOT + f'wynagrodzenia/{slug}.html', 'w').write(head + rest + main + footer)
    return slug, g_std, len(seo_title), len(desc)


if __name__ == '__main__':
    for n in NETS:
        print(page(n))
