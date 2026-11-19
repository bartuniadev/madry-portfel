import json, re, html
root='/home/user/madry-portfel/'
A='artykuly/'
T=[
("800 plus","Świadczenie wychowawcze: 800 zł miesięcznie na każde dziecko do 18. roku życia, niezależnie od dochodu rodziny.",A+"dziecko-a-finanse.html","Dziecko a finanse"),
("B2B (samozatrudnienie)","Współpraca z firmą w ramach własnej działalności gospodarczej zamiast umowy o pracę. Wyższa kwota na fakturze, ale bez płatnego urlopu, chorobowego i kodeksowej ochrony.",A+"b2b-czy-etat-porownanie.html","B2B czy etat"),
("DCC (dynamiczne przeliczenie waluty)","Propozycja terminala lub bankomatu za granicą, by rozliczyć transakcję w złotych. Zwykle oznacza gorszy kurs — lepiej wybrać walutę lokalną.",A+"podroze-taniej-budzet-urlopu.html","Podróże taniej"),
("Okres próbny","Pierwsza umowa o pracę zawierana na maksymalnie 3 miesiące, z krótszym okresem wypowiedzenia.",A+"umowa-o-prace-jak-czytac.html","Umowa o pracę — jak ją czytać"),
("Ulga na start","Zwolnienie nowego przedsiębiorcy ze składek na ubezpieczenia społeczne przez pierwsze 6 miesięcy działalności; płaci się tylko składkę zdrowotną.",A+"b2b-czy-etat-porownanie.html","B2B czy etat"),
("Umowa szkoleniowa („lojalka”)","Umowa, w której pracodawca finansuje szkolenie, a pracownik zobowiązuje się przepracować określony czas (maksymalnie 3 lata) lub zwrócić koszty.",A+"umowa-o-prace-jak-czytac.html","Umowa o pracę — jak ją czytać"),
("Zakaz konkurencji","Zobowiązanie do niepodejmowania działalności konkurencyjnej wobec pracodawcy. Po ustaniu zatrudnienia wymaga odszkodowania — co najmniej 25% wynagrodzenia za odpowiedni okres.",A+"umowa-o-prace-jak-czytac.html","Umowa o pracę — jak ją czytać"),
("Zasiłek macierzyński","Świadczenie z ZUS za czas urlopu macierzyńskiego i rodzicielskiego: 81,5% podstawy przez cały okres albo 100%, a potem 70% — zależnie od złożonego wniosku.",A+"dziecko-a-finanse.html","Dziecko a finanse"),
("Bessa","Dłuższy okres spadków na giełdzie — umownie o 20% lub więcej od szczytu. Normalna, powtarzająca się część inwestowania w akcje.",A+"hossa-bessa-jak-nie-panikowac.html","Hossa, bessa i panika"),
("Chwilówka","Krótkoterminowa pożyczka pozabankowa, zwykle na 30–60 dni. Jej koszt tkwi głównie w prowizjach i opłatach za przedłużenie terminu.",A+"chwilowki-ile-naprawde-kosztuja.html","Chwilówki — ile naprawdę kosztują"),
("Hossa","Dłuższy okres wzrostów na giełdzie. Sprzyja nadmiernemu optymizmowi i podejmowaniu większego ryzyka, niż wynika z planu.",A+"hossa-bessa-jak-nie-panikowac.html","Hossa, bessa i panika"),
("Klasa aktywów","Grupa inwestycji o podobnym źródle zysku i ryzyku: gotówka i depozyty, obligacje, akcje, nieruchomości, surowce.",A+"klasy-aktywow-akcje-obligacje-fundusze.html","Klasy aktywów"),
("Komornik sądowy","Funkcjonariusz publiczny wykonujący orzeczenia sądów; jako jedyny może przymusowo zająć część wynagrodzenia lub rachunek dłużnika — w granicach ustawowych limitów.",A+"windykacja-i-komornik-twoje-prawa.html","Windykacja i komornik"),
("Księga wieczysta","Publiczny rejestr stanu prawnego nieruchomości: opisuje lokal, właściciela, obciążenia i hipoteki. Sprawdza się ją przed każdym zakupem mieszkania.",A+"kupno-mieszkania-rynek-pierwotny-i-wtorny.html","Kupno mieszkania krok po kroku"),
("Przedawnienie długu","Upływ terminu (zwykle 3 lub 6 lat), po którym wierzyciel nie może skutecznie dochodzić roszczenia przed sądem, jeśli dłużnik podniesie zarzut przedawnienia.",A+"windykacja-i-komornik-twoje-prawa.html","Windykacja i komornik"),
("Rachunek maklerski","Konto do kupowania i przechowywania akcji, obligacji i funduszy ETF; odpowiednik rachunku bankowego dla papierów wartościowych.",A+"rachunek-maklerski-pierwsze-zlecenie.html","Rachunek maklerski"),
("Uwierzytelnianie dwuskładnikowe (2FA)","Logowanie wymagające oprócz hasła drugiego elementu — kodu z aplikacji, SMS-a lub klucza sprzętowego. Chroni konto nawet po wycieku hasła.",A+"bezpieczenstwo-cyfrowe-finansow.html","Bezpieczeństwo cyfrowe finansów"),
("Widełki płacowe","Przedział wynagrodzenia przewidziany na danym stanowisku; pracodawca ma obowiązek poinformować o nim kandydata.",A+"rozmowa-o-pieniadzach-w-rekrutacji.html","Oczekiwania finansowe na rozmowie o pracę"),
("Zadatek","Kwota wpłacana przy umowie przedwstępnej: przepada, gdy wycofa się kupujący, a wraca w podwójnej wysokości, gdy wycofa się sprzedający. Zaliczka po prostu podlega zwrotowi.",A+"kupno-mieszkania-rynek-pierwotny-i-wtorny.html","Kupno mieszkania krok po kroku"),
("Zlecenie z limitem ceny","Zlecenie giełdowe, w którym określasz maksymalną cenę kupna (lub minimalną sprzedaży); chroni przed transakcją po nieoczekiwanym kursie.",A+"rachunek-maklerski-pierwsze-zlecenie.html","Rachunek maklerski"),
("Akumulujący (fundusz)","Fundusz, który nie wypłaca dywidend, tylko sam je reinwestuje. Zysk rośnie wewnątrz funduszu, a podatek pojawia się dopiero przy sprzedaży jednostek.",A+"etf-dla-poczatkujacych.html","ETF-y dla początkujących"),
("BFG (Bankowy Fundusz Gwarancyjny)","Instytucja gwarantująca depozyty w bankach i SKOK-ach do równowartości 100 000 euro na osobę w jednej instytucji. Nie obejmuje inwestycji, np. funduszy czy akcji.",A+"konto-bankowe-jak-wybrac.html","Konto bankowe — jak wybrać"),
("BIK (Biuro Informacji Kredytowej)","Baza danych o kredytach, kartach i pożyczkach oraz o tym, czy były spłacane w terminie. Banki sprawdzają ją przed udzieleniem kredytu.",A+"karta-kredytowa-historia-kredytowa.html","Karta kredytowa i historia kredytowa"),
("BLIK","Polski system płatności mobilnych oparty na sześciocyfrowych kodach z aplikacji banku. Kod podany innej osobie pozwala jej wypłacić lub wydać Twoje pieniądze — stąd popularność oszustw „na BLIK-a”.",A+"oszustwa-finansowe-jak-sie-chronic.html","Oszustwa finansowe"),
("BNPL (kup teraz, zapłać później)","Odroczona płatność lub raty oferowane przy zakupach w internecie. Formalnie to kredyt: opóźnienie oznacza opłaty i wpis w historii kredytowej.",A+"bnpl-raty-pulapki.html","Pułapki rat i płatności odroczonych"),
("Brutto i netto","Brutto to wynagrodzenie przed potrąceniami; netto („na rękę”) to kwota po odjęciu składek i zaliczki na podatek.","narzedzia/kalkulator-brutto-netto.html","Kalkulator brutto–netto"),
("Budżet 50/30/20","Prosta metoda podziału dochodu: ok. 50% na potrzeby, 30% na zachcianki, 20% na oszczędności i spłatę długów.",A+"budzet-50-30-20.html","Budżet metodą 50/30/20"),
("Chargeback","Procedura reklamacji transakcji kartą: bank może cofnąć płatność, gdy towar nie dotarł lub sprzedawca nie oddaje pieniędzy.",A+"prawa-konsumenta-zwrot-reklamacja.html","Prawa konsumenta"),
("Darowizna","Nieodpłatne przekazanie pieniędzy lub rzeczy. W najbliższej rodzinie zwolniona z podatku po spełnieniu warunków formalnych.",A+"darowizny-i-pozyczki-w-rodzinie.html","Darowizny i pożyczki w rodzinie"),
("Działalność nierejestrowana","Drobna działalność zarobkowa bez zakładania firmy, dozwolona do kwartalnego limitu przychodu (w 2026 r. 10 813,50 zł). Bez składek ZUS; dochód rozlicza się w rocznym zeznaniu.",A+"dorabianie-po-godzinach.html","Dorabianie po godzinach"),
("Dywersyfikacja","Rozłożenie pieniędzy na wiele różnych aktywów, tak aby kłopoty jednego z nich nie zniszczyły całości oszczędności.",A+"jak-zaczac-inwestowac.html","Jak zacząć inwestować"),
("Dywidenda","Część zysku spółki wypłacana jej akcjonariuszom. Podlega 19% podatkowi od zysków kapitałowych.",A+"podatek-belki-jak-dziala.html","Podatek Belki"),
("EKUZ","Europejska Karta Ubezpieczenia Zdrowotnego — bezpłatny dokument dający dostęp do publicznej opieki zdrowotnej w krajach UE na zasadach obowiązujących miejscowych. Nie zastępuje polisy podróżnej.",A+"ubezpieczenia-na-starcie.html","Ubezpieczenia na starcie"),
("ETF","Fundusz inwestycyjny notowany na giełdzie, który odwzorowuje wybrany indeks (np. kilka tysięcy spółek z całego świata). Kupuje się go jak akcję, przez rachunek maklerski.",A+"etf-dla-poczatkujacych.html","ETF-y dla początkujących"),
("Franszyza i udział własny","Zapisy w polisie określające próg, poniżej którego ubezpieczyciel nie wypłaca odszkodowania, lub część szkody, którą zawsze pokrywasz sam.",A+"ubezpieczenia-na-starcie.html","Ubezpieczenia na starcie"),
("IKE (Indywidualne Konto Emerytalne)","Konto do długoterminowego oszczędzania z rocznym limitem wpłat. Zyski są zwolnione z podatku Belki przy wypłacie po 60. roku życia.",A+"ike-ikze-emerytura.html","IKE i IKZE"),
("IKZE (Indywidualne Konto Zabezpieczenia Emerytalnego)","Konto emerytalne, na które wpłaty odlicza się od dochodu w rocznym zeznaniu. Przy wypłacie po 65. roku życia płaci się zryczałtowany podatek 10%.",A+"ike-ikze-emerytura.html","IKE i IKZE"),
("Inflacja","Wzrost ogólnego poziomu cen, czyli spadek siły nabywczej pieniądza. Przy inflacji 5% za tę samą kwotę kupisz po roku o ok. 5% mniej.",A+"inflacja-a-twoje-pieniadze.html","Inflacja a Twoje pieniądze"),
("Kapitalizacja odsetek","Doliczanie naliczonych odsetek do kapitału, dzięki czemu w kolejnym okresie odsetki liczą się od większej kwoty.","narzedzia/kalkulator-procentu-skladanego.html","Kalkulator procentu składanego"),
("Kaucja","Zabezpieczenie wpłacane wynajmującemu przy najmie mieszkania; podlega zwrotowi po zakończeniu umowy, po potrąceniu ewentualnych należności.",A+"umowa-najmu-na-co-uwazac.html","Umowa najmu mieszkania"),
("Koszty uzyskania przychodu","Zryczałtowana kwota (przy umowie o pracę standardowo 250 zł miesięcznie), o którą obniża się podstawę obliczenia podatku.",A+"pasek-wynagrodzenia-jak-czytac.html","Pasek wynagrodzenia"),
("Kula śnieżna","Metoda spłaty długów, w której nadpłacasz najpierw zobowiązanie o najmniejszej kwocie, a każdą zwolnioną ratę dokładasz do następnego.","narzedzia/kalkulator-splaty-dlugow.html","Kalkulator spłaty długów"),
("Kwota wolna od podatku","Część rocznego dochodu, od której nie płaci się PIT — 30 000 zł w skali podatkowej. W praktyce działa jako kwota zmniejszająca podatek (3 600 zł rocznie).",A+"zwrot-podatku-pit-dla-mlodych.html","Zwrot podatku i pierwszy PIT"),
("Lawina","Metoda spłaty długów, w której nadpłacasz najpierw zobowiązanie o najwyższym oprocentowaniu. Matematycznie najtańsza.",A+"jak-wyjsc-z-dlugow.html","Jak wyjść z długów"),
("Lokata","Umowa z bankiem na przechowanie pieniędzy przez określony czas w zamian za z góry ustalone odsetki. Zerwanie przed terminem zwykle oznacza ich utratę.",A+"konta-oszczednosciowe.html","Konto oszczędnościowe"),
("Marża kredytu","Stała część oprocentowania kredytu, będąca zarobkiem banku. Do marży dolicza się zmienny wskaźnik referencyjny.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
("Najem okazjonalny","Rodzaj umowy najmu wymagający od najemcy notarialnego oświadczenia o poddaniu się egzekucji i wskazania lokalu, do którego się wyprowadzi.",A+"umowa-najmu-na-co-uwazac.html","Umowa najmu mieszkania"),
("Obligacje skarbowe","Papiery wartościowe emitowane przez Skarb Państwa — pożyczka udzielana państwu w zamian za odsetki. Serie indeksowane inflacją chronią siłę nabywczą oszczędności.",A+"obligacje-skarbowe-dla-poczatkujacych.html","Obligacje skarbowe dla początkujących"),
("OC w życiu prywatnym","Ubezpieczenie pokrywające szkody wyrządzone niechcący innym osobom, np. zalanie sąsiada czy potrącenie pieszego na rowerze.",A+"ubezpieczenia-na-starcie.html","Ubezpieczenia na starcie"),
("Odprawa","Świadczenie pieniężne przy zwolnieniu z przyczyn niedotyczących pracownika (u pracodawców zatrudniających co najmniej 20 osób): od jednej do trzech miesięcznych pensji, zależnie od stażu.",A+"utrata-pracy-plan-finansowy.html","Utrata pracy — plan finansowy"),
("OKI (Osobiste Konto Inwestycyjne)","Osobiste konto inwestycyjne dostępne od 1 stycznia 2027 r. Zyski na nim nie są objęte podatkiem Belki, a od średniej wartości aktywów ponad 100 000 zł płaci się podatek od aktywów (0,85% w 2027 r.).",A+"osobiste-konto-inwestycyjne-oki.html","OKI — jak działa"),
("Płaca minimalna (minimalne wynagrodzenie)","Najniższe wynagrodzenie za pełny etat, ustalane co roku przez rząd: 4806 zł brutto w 2026 r. i 4950 zł brutto w 2027 r. Na zleceniu obowiązuje minimalna stawka godzinowa (32,30 zł w 2027 r.).",A+"placa-minimalna-2027-netto.html","Płaca minimalna 2027 netto"),
("Okres wypowiedzenia","Czas między złożeniem wypowiedzenia umowy o pracę a jej rozwiązaniem: 2 tygodnie, 1 miesiąc lub 3 miesiące, zależnie od stażu u pracodawcy.",A+"prawa-pracownika-w-liczbach.html","Prawa pracownika w liczbach"),
("PCC (podatek od czynności cywilnoprawnych)","Podatek płacony m.in. przy zakupie samochodu od osoby prywatnej (2%) i przy pożyczce od osoby spoza najbliższej rodziny (0,5%). Deklarację PCC-3 składa się w ciągu 14 dni.",A+"pierwszy-samochod-ile-kosztuje.html","Pierwszy samochód"),
("PIT-2","Oświadczenie składane pracodawcy, dzięki któremu co miesiąc pomniejsza on zaliczkę na podatek o 300 zł.",A+"pasek-wynagrodzenia-jak-czytac.html","Pasek wynagrodzenia"),
("PIT-11","Informacja o dochodach i pobranych zaliczkach, którą pracodawca przekazuje pracownikowi do końca lutego. Podstawa rocznego zeznania.",A+"zwrot-podatku-pit-dla-mlodych.html","Zwrot podatku i pierwszy PIT"),
("PIT-38","Roczne zeznanie, w którym rozlicza się zyski i straty ze sprzedaży akcji, funduszy, ETF-ów i kryptowalut.",A+"podatek-belki-jak-dziala.html","Podatek Belki"),
("Podatek Belki","Potoczna nazwa 19-procentowego podatku od zysków kapitałowych: odsetek z lokat i obligacji, dywidend oraz zysków ze sprzedaży inwestycji.",A+"podatek-belki-jak-dziala.html","Podatek Belki"),
("Poduszka finansowa","Rezerwa pieniędzy na nieprzewidziane sytuacje, zwykle równowartość 3–6 miesięcy niezbędnych wydatków, trzymana w łatwo dostępnym miejscu.",A+"poduszka-finansowa.html","Poduszka finansowa"),
("POLSTR","Nowy wskaźnik referencyjny stopy procentowej, który stopniowo zastępuje WIBOR w oprocentowaniu kredytów.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
("PPK (Pracownicze Plany Kapitałowe)","Program długoterminowego oszczędzania, w którym do wpłat pracownika dokładają się pracodawca i państwo.",A+"ppk-pracownicze-plany-kapitalowe.html","PPK — czy warto zostać"),
("Procent składany","Mechanizm, w którym zysk z poprzednich okresów sam zaczyna przynosić zysk. Im dłuższy czas, tym większa część wyniku pochodzi z odsetek od odsetek.","narzedzia/kalkulator-procentu-skladanego.html","Kalkulator procentu składanego"),
("Próg podatkowy","Granica rocznego dochodu (120 000 zł), powyżej której nadwyżka jest opodatkowana stawką 32% zamiast 12%.",A+"zwrot-podatku-pit-dla-mlodych.html","Zwrot podatku i pierwszy PIT"),
("Reklamacja (niezgodność towaru z umową)","Uprawnienie konsumenta wobec sprzedawcy przez dwa lata od zakupu: żądanie naprawy, wymiany, obniżenia ceny lub zwrotu pieniędzy za wadliwy towar.",A+"prawa-konsumenta-zwrot-reklamacja.html","Prawa konsumenta"),
("RRSO","Rzeczywista roczna stopa oprocentowania — jedna liczba łącząca odsetki, prowizję i pozostałe koszty kredytu. Służy do porównywania ofert o tej samej kwocie i okresie.",A+"rrso-jak-czytac-oferte-pozyczki.html","RRSO i prawdziwy koszt kredytu"),
("SD-Z2","Zgłoszenie darowizny lub spadku od najbliższej rodziny, składane w urzędzie skarbowym w ciągu 6 miesięcy; warunek zwolnienia z podatku powyżej ustawowego progu.",A+"darowizny-i-pozyczki-w-rodzinie.html","Darowizny i pożyczki w rodzinie"),
("Składki ZUS","Obowiązkowe składki na ubezpieczenia społeczne (emerytalne, rentowe, chorobowe, wypadkowe) oraz zdrowotne, potrącane z wynagrodzenia i opłacane przez pracodawcę.",A+"pasek-wynagrodzenia-jak-czytac.html","Pasek wynagrodzenia"),
("Stopa procentowa NBP","Podstawowa cena pieniądza ustalana przez bank centralny. Wpływa na oprocentowanie kredytów, lokat i limit maksymalnych odsetek.",A+"inflacja-a-twoje-pieniadze.html","Inflacja a Twoje pieniądze"),
("Stopa zastąpienia","Relacja emerytury do ostatniego wynagrodzenia. Dla dzisiejszych dwudziesto- i trzydziestolatków prognozowana jest wyraźnie niżej niż dla obecnych emerytów.",A+"emerytura-z-zus-ile-realnie-dostaniesz.html","Emerytura z ZUS"),
("TER","Całkowity roczny koszt funduszu wyrażony w procentach jego aktywów; jest na bieżąco wliczany w cenę jednostki.",A+"etf-dla-poczatkujacych.html","ETF-y dla początkujących"),
("Ulga dla młodych (PIT-0)","Zwolnienie z podatku dochodowego dla osób do 26. roku życia — obejmuje przychody z pracy i zlecenia do 85 528 zł rocznie.",A+"zwrot-podatku-pit-dla-mlodych.html","Zwrot podatku i pierwszy PIT"),
("WIBOR","Wskaźnik referencyjny, na którym przez lata opierało się oprocentowanie kredytów w złotych; zastępowany przez POLSTR.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
("Wkład własny","Część ceny nieruchomości, którą kupujący pokrywa z własnych pieniędzy; banki wymagają zwykle 10–20%.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
("Wynagrodzenie chorobowe","Świadczenie za czas zwolnienia lekarskiego — co do zasady 80% wynagrodzenia; przez pierwsze 33 dni w roku wypłaca je pracodawca, potem ZUS jako zasiłek.",A+"prawa-pracownika-w-liczbach.html","Prawa pracownika w liczbach"),
("Zaliczka na podatek","Miesięczna kwota podatku dochodowego potrącana z wynagrodzenia przez pracodawcę; ostatecznie rozliczana w rocznym zeznaniu.",A+"pasek-wynagrodzenia-jak-czytac.html","Pasek wynagrodzenia"),
("Zastrzeżenie numeru PESEL","Bezpłatna usługa, po której włączeniu banki i firmy pożyczkowe nie powinny udzielić kredytu na Twoje dane. Zastrzeżenie cofa się na czas własnych formalności.",A+"oszustwa-finansowe-jak-sie-chronic.html","Oszustwa finansowe"),
("Zdolność kredytowa","Ocena banku, czy i jaką kwotę kredytu jesteś w stanie spłacić — na podstawie dochodów, wydatków, zobowiązań i historii kredytowej.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
]
import locale, os
def key(t):
    order="0123456789aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
    return [order.index(c) if c in order else -1 for c in t[0].lower() if c.isalnum() or c==' ']
T.sort(key=key)
for _,_,href,_ in T: assert os.path.exists(root+href), href
tpl=open(root+'o-nas.html').read()
head=tpl[:tpl.index('<main>')]
d_old=re.search(r'<meta name="description" content="([^"]*)">',head).group(1)
d_new='Słownik pojęć finansowych Mądrego Portfela: ponad 50 haseł — od brutto i netto, przez RRSO i ETF, po podatek Belki — wyjaśnionych prostym językiem, z odesłaniem do poradników.'
head=head.replace('O nas | Mądry Portfel','Słownik pojęć finansowych | Mądry Portfel').replace(d_old,d_new).replace('madry-portfel/o-nas.html','madry-portfel/slownik.html')
ld={"@context":"https://schema.org","@type":"DefinedTermSet","name":"Słownik pojęć finansowych — Mądry Portfel","url":"https://bartuniadev.github.io/madry-portfel/slownik.html","inLanguage":"pl-PL",
    "hasDefinedTerm":[{"@type":"DefinedTerm","name":t,"description":d} for t,d,_,_ in T]}
head=head.replace('</head>','<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=1)+'\n</script>\n</head>')
letters=[]; body=''
for t,d,href,lt in T:
    L=t[0].upper()
    if L not in letters:
        if letters: body+='  </dl>\n'
        letters.append(L); body+=f'  <h2 class="gl-letter" id="litera-{len(letters)}">{L}</h2>\n  <dl class="glossary">\n'
    body+=f'    <dt>{html.escape(t,quote=False)}</dt>\n    <dd>{html.escape(d,quote=False)} <a href="{href}">{html.escape(lt,quote=False)} →</a></dd>\n'
body+='  </dl>\n'
index=' '.join(f'<a href="#litera-{i+1}">{L}</a>' for i,L in enumerate(letters))
main=f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="index.html">Mądry Portfel</a> <span aria-hidden="true">/</span> <span aria-current="page">Słownik</span></nav>
  <h1>Słownik pojęć finansowych</h1>
  <p class="lead">{len(T)} haseł, które pojawiają się w ofertach pracy, umowach z bankiem i na pasku wynagrodzenia — wyjaśnione prostym językiem. Przy każdym znajdziesz odesłanie do poradnika lub kalkulatora, w którym temat jest rozwinięty.</p>
  <p class="gl-index" aria-label="Indeks alfabetyczny">{index}</p>

{body}
  <p><em>Definicje mają charakter edukacyjny i są celowo uproszczone. Kwoty i limity podano według stanu na listopad 2026 r.</em></p>
</main>

'''
head=head.replace('<a href="slownik.html">Słownik</a>','<a href="slownik.html" aria-current="page">Słownik</a>')
open(root+'slownik.html','w').write(head+main+tpl[tpl.index('<footer>'):])
print('terms',len(T),'letters',''.join(letters))
