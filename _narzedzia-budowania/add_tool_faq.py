# Adds a visible FAQ section and FAQPage structured data to selected calculator pages (idempotent).
import json, html, re
ROOT = '/home/user/madry-portfel/narzedzia/'
FAQ = {
    'kalkulator-brutto-netto': [
        ('Ile na rękę z 6000 zł brutto w 2027 roku?', 'Na umowie o pracę ok. 4420,43 zł (z PIT-2, bez PPK, dla osoby powyżej 26 lat). Z PPK zostaje 4289,43 zł, a osobie do 26 lat z ulgą dla młodych — 4711,43 zł.'),
        ('Ile brutto, żeby mieć 5000 zł na rękę?', 'Na umowie o pracę ok. 6850,14 zł brutto (z PIT-2, bez PPK). Swój wariant policzysz, przełączając kalkulator na „Netto → brutto”.'),
        ('Czy w 2027 roku zmienia się sposób liczenia pensji?', 'Składki, koszty uzyskania przychodu i kwota zmniejszająca podatek zostają bez zmian. Rośnie płaca minimalna — do 4950 zł brutto. Nowa skala PIT (próg 130 000 zł i stawka 24%) czeka na decyzję prezydenta i dotyczyłaby tylko dochodów powyżej 120 000 zł rocznie.'),
        ('Dlaczego pod koniec roku wypłata może być niższa?', 'Gdy dochód od początku roku przekroczy 120 000 zł, nadwyżka jest opodatkowana stawką 32%. U osób do 26 lat wypłata spada po przekroczeniu limitu ulgi dla młodych (85 528 zł przychodu). Wypłata rośnie za to po przekroczeniu rocznego limitu składek emerytalnej i rentowej.'),
    ],
    'czy-dobrze-zarabiam': [
        ('Ile wynosi mediana wynagrodzeń w Polsce?', 'Według GUS w maju 2026 r. mediana wynosiła 7550,32 zł brutto, czyli ok. 5477 zł na rękę. Połowa pracujących zarabia mniej, połowa więcej.'),
        ('Ile procent Polaków zarabia mniej niż średnia krajowa?', 'Ok. 65%. Przeciętne wynagrodzenie (9178,16 zł w maju 2026 r.) jest wyższe od mediany, bo podnoszą je najwyższe pensje.'),
        ('Od jakiej pensji jestem w 10% najlepiej zarabiających?', 'Od 14 239 zł brutto miesięcznie (dane GUS za maj 2026 r.), czyli ok. 10 037 zł na rękę na umowie o pracę.'),
        ('Ile zarabia 10% najmniej zarabiających?', 'Co najwyżej 4806 zł brutto — tyle, ile wynosiła płaca minimalna w 2026 r.'),
    ],
    'kalkulator-inflacji': [
        ('Ile jest dziś warte 100 zł z 2020 roku?', 'Żeby w 2025 r. kupić to samo, co w 2020 r. za 100 zł, trzeba było mieć ok. 143,76 zł — ceny wzrosły w tym czasie o 43,8% (dane GUS).'),
        ('Jaka była inflacja w 2025 roku?', 'Średnioroczna inflacja w 2025 r. wyniosła 3,6% — tyle samo co w 2024 r. Najwyższa w ostatnich latach była w 2022 r. (14,4%) i 2023 r. (11,4%).'),
        ('Ile straciły pieniądze trzymane w gotówce od 2015 roku?', '100 zł odłożone w 2015 r. bez oprocentowania miało w 2025 r. siłę nabywczą ok. 63,84 zł, bo ceny wzrosły o 56,6%.'),
    ],
    'kalkulator-umowy-zlecenia': [
        ('Ile na rękę z umowy zlecenia 3000 zł brutto?', 'Gdy zlecenie jest jedyną pracą (ze składką chorobową) — 2106,72 zł. Gdy masz też etat z co najmniej płacą minimalną — 2442 zł. Student do 26 lat dostaje całe 3000 zł.'),
        ('Jaka jest minimalna stawka godzinowa w 2027 roku?', '32,30 zł brutto za godzinę (w 2026 r. — 31,40 zł). Zleceniodawca musi ją wypłacić niezależnie od tego, jak opisano wynagrodzenie w umowie.'),
        ('Czy student płaci ZUS od umowy zlecenia?', 'Nie — student lub uczeń do 26. urodzin nie płaci od zlecenia składek ZUS ani zdrowotnej, a ulga dla młodych zwalnia go z podatku do 85 528 zł przychodu rocznie.'),
    ],
}
CSS = '''  .tool-faq{margin-top:30px;}
  .tool-faq h2{font-size:1.25rem;margin:0 0 6px;}
  .tool-faq details{border-top:1px solid var(--border);padding:12px 2px;}
  .tool-faq summary{cursor:pointer;font-weight:600;}
  .tool-faq summary:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  .tool-faq p{color:var(--text-2);margin:8px 0 0;max-width:65ch;}
'''
for slug, qa in FAQ.items():
    p = ROOT + slug + '.html'
    s = open(p).read()
    if 'class="tool-faq"' in s:
        print('skip', slug)
        continue
    sec = '  <section class="tool-faq" aria-labelledby="faqTitle">\n    <h2 id="faqTitle">Najczęstsze pytania</h2>\n' + ''.join(
        f'    <details>\n      <summary>{html.escape(q)}</summary>\n      <p>{html.escape(a)}</p>\n    </details>\n' for q, a in qa) + '  </section>\n\n'
    anchor = '  <div class="trust">'
    assert s.count(anchor) == 1, slug
    s = s.replace(anchor, sec + anchor, 1)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    s = s.replace('</head>', '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>\n</head>', 1)
    s = s.replace('</style>', CSS + '</style>', 1)
    open(p, 'w').write(s)
    print('faq added', slug, len(qa))
