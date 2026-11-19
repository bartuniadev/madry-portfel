# Generates wynagrodzenia/<kwota>-brutto-ile-netto.html — one page per popular salary amount.
import math, json, html, re, os
from urllib.parse import quote

ROOT = '/home/user/madry-portfel/'
BASE = 'https://bartuniadev.github.io/madry-portfel/'
AMOUNTS = [5000, 5500, 6000, 6500, 7000, 7500, 8000, 9000, 10000, 12000, 15000]
TODAY = '2026-11-19'
MED, D1, D9 = 7550.32, 4806.0, 14239.0
SU = math.log(D9 / MED) / 1.2815516
SD = math.log(MED / D1) / 1.2815516
YOUNG = 85528


def r2(x):
    return round(x + 1e-9, 2)


def etat(g, ppk=False, pit2=True, young=False, kup=250):
    zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245))
    h = r2((g - zus) * 0.09)
    ppkO = r2(g * 0.02) if ppk else 0
    ppkE = r2(g * 0.015) if ppk else 0
    tax = 0
    if not young:
        base = max(0, round(g - zus - kup + ppkE))
        tax = max(0, round(base * 0.12 - (300 if pit2 else 0)))
    return dict(zus=zus, health=h, tax=tax, ppk=ppkO, net=r2(g - zus - h - tax - ppkO))


def year_sim(g):
    """Standard case (PIT-2, no PPK, KUP 250): 12 months with the 120 000 zł threshold."""
    zus = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245))
    h = r2((g - zus) * 0.09)
    base = max(0, round(g - zus - 250))
    cum, nets, cross = 0, [], None
    for m in range(12):
        lo = max(0, min(base, 120000 - cum))
        hi = base - lo
        tax = max(0, round(lo * 0.12 + hi * 0.32 - 300))
        if hi > 0 and cross is None:
            cross = m + 1
        cum += base
        nets.append(r2(g - zus - h - tax))
    return nets, cross


def zlecenie(g, mode):
    if mode == 'student':
        return g
    if mode == 'only':
        soc = r2(r2(g * 0.0976) + r2(g * 0.015) + r2(g * 0.0245))
    else:
        soc = 0
    h = r2((g - soc) * 0.09)
    kup = r2((g - soc) * 0.2)
    tax = max(0, round(round(g - soc - kup) * 0.12))
    return r2(g - soc - h - tax)


def pct(g):
    z = math.log(g / MED) / (SU if g >= MED else SD)
    return 0.5 * (1 + math.erf(z / math.sqrt(2))) * 100


def zl(n, dec=2):
    s = f'{n:,.{dec}f}'.replace(',', ' ').replace('.', ',')
    return s.replace(' ', '\u00a0') + '\u00a0zł'


def zl0(n):
    return zl(round(n), 0)


MONTHS_GEN = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']
MONTHS_LOC = ['styczniu', 'lutym', 'marcu', 'kwietniu', 'maju', 'czerwcu', 'lipcu', 'sierpniu', 'wrześniu', 'październiku', 'listopadzie', 'grudniu']


def share_html(url, title):
    t = quote(title + ' ' + url)
    u = quote(url, safe='')
    return f'''  <div class="share" data-url="{url}" data-title="{html.escape(title)}">
    <p class="share-title">Przyda się komuś? Podeślij to wyliczenie</p>
    <div class="share-links">
      <button type="button" data-share-native hidden>Udostępnij</button>
      <button type="button" data-share-copy>Kopiuj link</button>
      <a href="https://wa.me/?text={t}" rel="noopener" target="_blank">WhatsApp</a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={u}" rel="noopener" target="_blank">Facebook</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener" target="_blank">LinkedIn</a>
      <a href="https://twitter.com/intent/tweet?url={u}&amp;text={quote(title)}" rel="noopener" target="_blank">X</a>
    </div>
    <p class="share-note" aria-live="polite"></p>
  </div>
'''


def page(g):
    slug = f'{g}-brutto-ile-netto'
    url = BASE + f'wynagrodzenia/{slug}.html'
    std = etat(g)
    ppk = etat(g, ppk=True)
    young = etat(g, young=True)
    nopit2 = etat(g, pit2=False)
    commute = etat(g, kup=300)
    nets, cross = year_sim(g)
    year_net = sum(nets)
    z_only, z_job, z_stud = zlecenie(g, 'only'), zlecenie(g, 'job'), zlecenie(g, 'student')
    cost = r2(g * 1.2048)
    p = pct(g)
    n = std['net']
    gs = f'{g:,}'.replace(',', '\u00a0')
    title = f'{gs} zł brutto ile netto w 2027? To {zl0(n)} na rękę'
    seo_title = f'{g} brutto ile netto 2027? {round(n)} zł na rękę'
    desc = (f'{gs} zł brutto to w 2027 r. ok. {zl0(n)} netto na umowie o pracę (PIT-2, bez PPK). '
            f'Z PPK {zl0(ppk["net"])}, do 26 lat {zl0(young["net"])}. Zlecenie, koszt pracodawcy i budżet.')
    young_cross = math.ceil(YOUNG / g) if g * 12 > YOUNG else None
    stud_note = (f' do {MONTHS_GEN[young_cross - 1]}, potem po przekroczeniu limitu ulgi dla młodych (85\u00a0528 zł rocznie) pobierana jest zaliczka na podatek' if young_cross else '')

    rows = [
        ('Standard: PIT-2, bez PPK', std['net']),
        ('Z PPK (2% + 1,5% pracodawcy)', ppk['net']),
        ('Do 26 lat (ulga dla młodych), bez PPK', young['net']),
        ('Bez złożonego PIT-2', nopit2['net']),
        ('Dojazd z innej miejscowości (koszty 300 zł)', commute['net']),
    ]
    table = '\n'.join(f'      <tr><td>{html.escape(a)}</td><td><strong>{zl(b)}</strong></td></tr>' for a, b in rows)
    b50, b30, b20 = n * .5, n * .3, n * .2

    notes = []
    if young_cross:
        notes.append(f'<li><strong>Do 26 lat:</strong> przy {gs} zł brutto limit ulgi dla młodych (85\u00a0528 zł przychodu rocznie) skończy się w {MONTHS_LOC[young_cross - 1]} — od tego miesiąca wypłata spadnie do ok. {zl0(std["net"])}.</li>')
    if cross:
        notes.append(f'<li><strong>Próg podatkowy:</strong> w {MONTHS_LOC[cross - 1]} dochód od początku roku przekroczy 120\u00a0000 zł i nadwyżka będzie opodatkowana stawką 32% — wtedy na rękę zostaje ok. {zl0(nets[-1])} miesięcznie.</li>')
    notes_html = ('  <ul>\n    ' + '\n    '.join(notes) + '\n  </ul>\n') if notes else ''

    above = 'więcej' if g >= MED else 'mniej'
    diff = abs(g - MED)
    others = ' · '.join((f'<strong>{a:,}'.replace(',', '\u00a0') + ' zł</strong>') if a == g else f'<a href="{a}-brutto-ile-netto.html">' + f'{a:,}'.replace(',', '\u00a0') + ' zł</a>' for a in AMOUNTS)

    faq = [
        (f'Ile to netto {gs} zł brutto?', f'Na umowie o pracę w 2027 r. {gs} zł brutto to ok. {zl0(n)} na rękę (z PIT-2, bez PPK, dla osoby powyżej 26 lat). Z PPK ok. {zl0(ppk["net"])}.'),
        (f'Ile netto z {gs} zł brutto na umowie zlecenia?', f'Gdy zlecenie jest jedyną pracą i płacisz składkę chorobową — ok. {zl0(z_only)}. Gdy masz też etat z co najmniej płacą minimalną — ok. {zl0(z_job)}. Student do 26 lat dostaje całe {zl0(z_stud)}{stud_note}.'),
        (f'Ile netto z {gs} zł brutto dla osoby do 26 lat?', f'Ok. {zl0(young["net"])} na umowie o pracę — dzięki uldze dla młodych nie ma zaliczki na podatek, ale składki ZUS i zdrowotna są pobierane normalnie.'),
        (f'Ile pracodawcę kosztuje {gs} zł brutto?', f'Ok. {zl0(cost)} miesięcznie — do pensji dolicza składki emerytalną, rentową, wypadkową oraz na Fundusz Pracy i FGŚP.'),
    ]
    faq_html = '\n'.join(f'  <details class="faq">\n    <summary>{html.escape(q)}</summary>\n    <p>{html.escape(a)}</p>\n  </details>' for q, a in faq)

    body = f'''  <p class="meta">Wyliczenie · zasady na 2027 r. (te same co w 2026 r.) · Aktualizacja 19 listopada 2026</p>

  <p class="tldr"><strong>W skrócie:</strong> {gs} zł brutto to w 2027 r. <strong>{zl(n)} netto</strong> na umowie o pracę (z PIT-2, bez PPK). Z PPK zostaje {zl(ppk['net'])}, a osobie do 26 lat — {zl(young['net'])}. Pracodawcę ta pensja kosztuje ok. {zl0(cost)} miesięcznie.</p>

  <h2>{gs} zł brutto ile netto — umowa o pracę</h2>
  <table>
    <thead><tr><th>Wariant</th><th>Na rękę miesięcznie</th></tr></thead>
    <tbody>
{table}
    </tbody>
  </table>
  <p>Inny wariant policzysz w <a href="../narzedzia/kalkulator-brutto-netto.html">kalkulatorze brutto–netto 2027</a> — pokazuje też wypłatę w każdym miesiącu roku.</p>
{notes_html}
  <h2>Na co idzie różnica między brutto a netto</h2>
  <ul>
    <li><strong>Składki społeczne:</strong> {zl(std['zus'])} (emerytalna, rentowa i chorobowa — 13,71% brutto).</li>
    <li><strong>Składka zdrowotna:</strong> {zl(std['health'])} (9% od kwoty po składkach społecznych).</li>
    <li><strong>Zaliczka na podatek:</strong> {zl(std['tax'], 0)} (12% od dochodu po kosztach 250 zł, minus 300 zł kwoty zmniejszającej).</li>
  </ul>
  <p>Rocznie na rękę: <strong>{zl0(year_net)}</strong>. Pracodawca płaci łącznie ok. {zl0(cost)} miesięcznie, czyli {zl0(cost * 12)} rocznie. Każdą pozycję z paska wyjaśniamy w tekście <a href="../artykuly/pasek-wynagrodzenia-jak-czytac.html">jak czytać pasek wynagrodzenia</a>.</p>

  <h2>{gs} zł brutto na umowie zlecenia</h2>
  <table>
    <thead><tr><th>Sytuacja</th><th>Na rękę</th></tr></thead>
    <tbody>
      <tr><td>Zlecenie to jedyna praca (ze składką chorobową)</td><td><strong>{zl(z_only)}</strong></td></tr>
      <tr><td>Masz też etat z co najmniej płacą minimalną</td><td><strong>{zl(z_job)}</strong></td></tr>
      <tr><td>Student lub uczeń do 26 lat{'*' if young_cross else ''}</td><td><strong>{zl(z_stud)}</strong></td></tr>
    </tbody>
  </table>
{'  <p><small>* Do ' + MONTHS_GEN[young_cross - 1] + ' — później roczny przychód przekroczy limit ulgi dla młodych (85\u00a0528 zł) i zleceniodawca zacznie pobierać zaliczkę na podatek.</small></p>' + chr(10) if young_cross else ''}  <p>Na zleceniu nie masz płatnego urlopu ani okresu wypowiedzenia — porównując oferty, licz to w cenie. Swój wariant sprawdzisz w <a href="../narzedzia/kalkulator-umowy-zlecenia.html">kalkulatorze umowy zlecenia</a>, a porównanie z B2B — w tekście <a href="../artykuly/b2b-czy-etat-porownanie.html">B2B czy etat</a>.</p>

  <h2>Czy {gs} zł brutto to dobra pensja?</h2>
  <p>Według danych GUS za maj 2026 r. połowa pracujących zarabiała mniej niż 7550 zł brutto (mediana). {gs} zł brutto to o {zl0(diff)} {above} niż mediana — zarabiasz więcej niż <strong>ok. {round(p)}% pracujących</strong> w Polsce. Dokładną pozycję i wykres zobaczysz w kalkulatorze <a href="../narzedzia/czy-dobrze-zarabiam.html">Czy dobrze zarabiam?</a>, a omówienie danych — w artykule o <a href="../artykuly/mediana-wynagrodzen-ile-zarabiaja-polacy.html">medianie wynagrodzeń</a>.</p>

  <h2>Budżet przy {zl0(n)} na rękę</h2>
  <p>Według prostej zasady <a href="../artykuly/budzet-50-30-20.html">50/30/20</a>:</p>
  <ul>
    <li><strong>{zl0(b50)}</strong> na potrzeby — mieszkanie, rachunki, jedzenie, dojazdy,</li>
    <li><strong>{zl0(b30)}</strong> na przyjemności,</li>
    <li><strong>{zl0(b20)}</strong> na oszczędności i spłatę długów.</li>
  </ul>
  <p>Przy samodzielnym wynajmie warto, żeby czynsz z opłatami nie przekraczał ok. 30–35% pensji netto — tu ok. {zl0(n * .30)}–{zl0(n * .35)}. Ile odłożyć na start, policzysz w <a href="../narzedzia/kalkulator-poduszki-finansowej.html">kalkulatorze poduszki finansowej</a>.</p>

  <h2>Najczęstsze pytania</h2>
{faq_html}

  <h2>Inne kwoty</h2>
  <p class="amounts-nav">{others}</p>
  <p>Wszystkie kwoty w jednym miejscu: <a href="../artykuly/ile-na-reke-tabela-brutto-netto.html">tabela brutto–netto od 4950 do 20 000 zł</a>.</p>

  <p><em>Treść ma charakter edukacyjny. Wyliczenia według zasad obowiązujących w listopadzie 2026 r. (skala PIT 12% do 120 000 zł dochodu, kwota zmniejszająca 300 zł miesięcznie); w 2027 r. zasady liczenia pensji są takie same, chyba że wejdzie w życie nowa skala podatkowa (dotyczy dochodów powyżej 120 000 zł rocznie). Rzeczywista wypłata może różnić się o kilka złotych przez zaokrąglenia i dodatki.</em></p>
'''
    body = re.sub(r'(\d) (\d{3})(?!\d)', '\\1\u00a0\\2', body)

    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": title.replace('\u00a0', ' '), "description": desc.replace('\u00a0', ' '), "inLanguage": "pl-PL",
         "datePublished": TODAY, "dateModified": TODAY, "mainEntityOfPage": url, "image": BASE + f'assets/og/{slug}.jpg',
         "author": {"@type": "Organization", "name": "Mądry Portfel", "url": BASE}, "publisher": {"@type": "Organization", "name": "Mądry Portfel", "url": BASE},
         "keywords": f'{g} brutto ile netto, {g} brutto na rękę 2027, {g} brutto ile netto zlecenie, {g} brutto do 26 lat'},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Mądry Portfel", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Ile na rękę — tabela", "item": BASE + 'artykuly/ile-na-reke-tabela-brutto-netto.html'},
            {"@type": "ListItem", "position": 3, "name": f'{g} zł brutto ile netto', "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q.replace('\u00a0', ' '), "acceptedAnswer": {"@type": "Answer", "text": a.replace('\u00a0', ' ')}} for q, a in faq]},
    ]}
    e = lambda s: html.escape(s.replace('\u00a0', ' '), quote=True)
    head = f'''<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(seo_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="stylesheet" href="../style.css">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="../assets/fonts/fonts.css">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Mądry Portfel">
<meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{e(seo_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og/{slug}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(seo_title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{BASE}assets/og/{slug}.jpg">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
</script>
<link rel="alternate" type="application/rss+xml" title="Mądry Portfel — nowe poradniki" href="{BASE}feed.xml">
</head>
'''
    tpl = open(ROOT + 'artykuly/ile-na-reke-tabela-brutto-netto.html').read()
    header = tpl[tpl.index('<body>'):tpl.index('<main>')]
    footer = tpl[tpl.index('</main>') + len('</main>'):]
    icon = re.search(r'<div class="icon-badge lg">.*?</div>', tpl, re.S).group(0)
    main = f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="../index.html">Artykuły</a> <span aria-hidden="true">/</span> <a href="../artykuly/ile-na-reke-tabela-brutto-netto.html">Ile na rękę</a> <span aria-hidden="true">/</span> <span aria-current="page">{gs} zł brutto</span></nav>
  <div class="article-header">
    {icon}
    <h1>{html.escape(title)}</h1>
  </div>

{body}
{share_html(url, title.replace(chr(160), ' '))}
  <section class="sources">
    <h2>Jak liczymy i źródła</h2>
    <ul>
      <li><a href="https://www.zus.pl/" rel="noopener">Zakład Ubezpieczeń Społecznych</a> — stopy składek na ubezpieczenia społeczne</li>
      <li><a href="https://www.podatki.gov.pl/" rel="noopener">Serwis podatki.gov.pl</a> — skala podatkowa, kwota zmniejszająca podatek, ulga dla młodych</li>
      <li><a href="https://stat.gov.pl/obszary-tematyczne/rynek-pracy/pracujacy-zatrudnieni-wynagrodzenia-koszty-pracy/" rel="noopener">GUS — wynagrodzenia</a> — rozkład wynagrodzeń (maj 2026 r.)</li>
    </ul>
    <p class="sources-note">Wyliczenia sprawdzone w listopadzie 2026 r. Przepisy się zmieniają — w razie rozbieżności wiążące są informacje na stronach urzędowych.</p>
  </section>
</main>'''
    os.makedirs(ROOT + 'wynagrodzenia', exist_ok=True)
    open(ROOT + f'wynagrodzenia/{slug}.html', 'w').write(head + header + main + footer)
    return slug, title, n, len(seo_title), len(desc)


if __name__ == '__main__':
    for g in AMOUNTS:
        print(page(g))
