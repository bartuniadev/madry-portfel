# Adds a visible FAQ section and FAQPage structured data to selected calculator pages (idempotent).
import json, html, re
ROOT = '/home/user/madry-portfel/narzedzia/'
FAQ = {
    'kalkulator-brutto-netto': [
        ('Ile na rękę z 6000 zł brutto w 2027 roku?', 'Na umowie o pracę ok. 4420,43 zł (z PIT-2, bez PPK, dla osoby powyżej 26 lat). Z PPK zostaje 4289,43 zł, a osobie do 26 lat z ulgą dla młodych — 4711,43 zł.'),
        ('Ile brutto, żeby mieć 5000 zł na rękę?', 'Na umowie o pracę ok. 6850,14 zł brutto (z PIT-2, bez PPK). Swój wariant policzysz, przełączając kalkulator na „Netto → brutto”.'),
        ('Czy w 2027 roku zmienia się sposób liczenia pensji?', 'Nie. Składki, koszty uzyskania przychodu, kwota zmniejszająca podatek i skala PIT (12% do 120 000 zł, 32% powyżej) zostają bez zmian — prezydent zawetował 27 listopada 2026 r. ustawę podnoszącą próg do 130 000 zł. Rośnie płaca minimalna — do 4950 zł brutto.'),
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
    'kalkulator-l4': [
        ('Ile dostanę na L4 przy pensji 7000 zł brutto?', 'Za każdy dzień zwolnienia 161,07 zł brutto chorobowego (80%). Przy 10 dniach L4 wypłata za miesiąc wyniesie ok. 4783 zł na rękę zamiast 5102 zł, czyli ok. 318 zł mniej (umowa o pracę, PIT-2, bez PPK).'),
        ('Ile płatne jest L4?', 'Co do zasady 80% podstawy, czyli przeciętnej pensji brutto z ostatnich 12 miesięcy pomniejszonej o 13,71% składek. 100% przysługuje m.in. w ciąży, po wypadku w drodze do pracy lub z pracy i przy badaniach dawcy.'),
        ('Kto płaci za L4 — pracodawca czy ZUS?', 'Przez pierwsze 33 dni choroby w roku kalendarzowym płaci pracodawca (wynagrodzenie chorobowe), a osobom po 50. roku życia — przez 14 dni. Potem zasiłek chorobowy wypłaca ZUS, w tej samej wysokości.'),
        ('Czy od L4 płaci się podatek i ZUS?', 'Od wynagrodzenia chorobowego i zasiłku nie płaci się składek emerytalnej, rentowej i chorobowej. Pobierana jest tylko składka zdrowotna 9% i zaliczka na podatek — dlatego na rękę tracisz mniej, niż sugeruje 80%.'),
    ],
    'kalkulator-nadgodzin': [
        ('Ile dostanę za 10 nadgodzin przy pensji 7000 zł brutto?', 'W listopadzie 2026 r. (160 godzin pracy) stawka godzinowa to 43,75 zł, więc 10 nadgodzin z dodatkiem 50% to 656,25 zł brutto, czyli ok. 447 zł na rękę.'),
        ('Kiedy dodatek za nadgodziny wynosi 100%?', 'Za nadgodziny w nocy, w niedziele i święta, które nie są dla Ciebie dniami pracy, w dniu wolnym udzielonym za pracę w niedzielę lub święto oraz za przekroczenie przeciętnej tygodniowej normy czasu pracy. W pozostałych przypadkach dodatek wynosi 50%.'),
        ('Ile nadgodzin można mieć w roku?', 'Co do zasady 150 godzin w roku kalendarzowym. Układ zbiorowy, regulamin pracy lub umowa o pracę mogą ustalić inny limit.'),
        ('Czy zamiast pieniędzy mogę dostać wolne za nadgodziny?', 'Tak. Na Twój wniosek pracodawca może dać czas wolny w tym samym wymiarze (godzina za godzinę), a z własnej inicjatywy — w wymiarze o połowę wyższym. Wtedy dodatek za nadgodziny nie przysługuje.'),
    ],
    'kalkulator-urlopu': [
        ('Ile dni urlopu po studiach?', 'Ukończone studia wliczają się do stażu jako 8 lat, więc absolwent ma 20 dni urlopu, a 26 dni — po 2 latach pracy. Od 2026 r. do stażu wliczają się też udokumentowane umowy zlecenia i działalność gospodarcza.'),
        ('Ile wynosi ekwiwalent za 5 dni urlopu przy pensji 6000 zł?', 'Ok. 1434 zł brutto (6000 zł ÷ 20,92 × 5 dni), czyli ok. 977 zł na rękę, gdy jest wypłacony razem z ostatnią pensją.'),
        ('Ile urlopu przy zmianie pracy w trakcie roku?', 'U każdego pracodawcy proporcjonalnie do miesięcy zatrudnienia w danym roku. Np. przy 20 dniach i pracy od marca do grudnia (10 miesięcy) — 17 dni (20 × 10/12, zaokrąglone w górę).'),
        ('Do kiedy trzeba wykorzystać zaległy urlop?', 'Do 30 września następnego roku — urlop z 2026 r. trzeba wykorzystać do 30 września 2027 r.'),
    ],
    'ile-zarabiam-na-godzine': [
        ('Ile zarabiam na godzinę przy 7000 zł brutto?', 'Na umowie o pracę ok. 30,49 zł na rękę za godzinę (5101,67 zł netto ÷ 167,3 godziny pracy w miesiącu przy pełnym etacie), czyli ok. 0,51 zł na minutę. Brutto to ok. 41,83 zł za godzinę.'),
        ('Ile zarabiam na godzinę przy płacy minimalnej?', 'W 2026 r. (4806 zł brutto) ok. 21,55 zł na rękę za godzinę, a w 2027 r. (4950 zł brutto) ok. 22,14 zł — przy pełnym etacie, z PIT-2 i bez PPK.'),
        ('Ile godzin pracy jest w miesiącu?', 'Przy pełnym etacie średnio 167,3 godziny — w 2026 i 2027 r. to 2008 godzin rocznie. W konkretnych miesiącach od 144 godzin (maj 2027) do 184 godzin (lipiec 2026).'),
        ('Co to jest realna stawka godzinowa?', 'To pensja na rękę podzielona przez czas pracy razem z dojazdami. Przy 7000 zł brutto i godzinie dojazdów dziennie spada z 30,49 zł do ok. 27,10 zł za godzinę.'),
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
