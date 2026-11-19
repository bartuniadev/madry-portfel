import json, re, html, os
root='/home/user/madry-portfel/'; A='artykuly/'; N='narzedzia/'
G=[
("Pensja i podatki",[
 ("Ile dostanę na rękę z kwoty brutto?","Na umowie o pracę w pierwszym progu podatkowym zostaje ok. 71–75% kwoty brutto: z 6 000 zł brutto to ok. 4 420 zł netto (bez PPK). Osoby do 26. roku życia dostają więcej dzięki uldze dla młodych.",N+"kalkulator-brutto-netto.html","Kalkulator brutto–netto"),
 ("Czy przed 26. rokiem życia płacę podatek dochodowy?","Od przychodów z umowy o pracę i zlecenia do 85 528 zł rocznie — nie. Składki ZUS i zdrowotna są jednak pobierane normalnie (wyjątkiem jest zlecenie studenta).",A+"zwrot-podatku-pit-dla-mlodych.html","Zwrot podatku i pierwszy PIT"),
 ("Do kiedy trzeba rozliczyć PIT?","Do 30 kwietnia za poprzedni rok. Gotowe zeznanie czeka w usłudze Twój e-PIT od 15 lutego; zwrot przy rozliczeniu elektronicznym przychodzi w ciągu 45 dni.",A+"pit-za-2026-jak-rozliczyc.html","Jak rozliczyć PIT za 2026"),
 ("Ile wynosi płaca minimalna w 2027 roku i ile to na rękę?","Od 1 stycznia 2027 r. to 4950 zł brutto za pełny etat, czyli ok. 3704 zł netto na umowie o pracę (z PIT-2, bez PPK). Na zleceniu minimalna stawka wynosi 32,30 zł brutto za godzinę.",A+"placa-minimalna-2027-netto.html","Płaca minimalna 2027 netto"),
 ("Co to jest PIT-2 i czy muszę go składać?","To oświadczenie, dzięki któremu pracodawca co miesiąc pomniejsza zaliczkę na podatek o 300 zł. Bez niego dostajesz niższą wypłatę, a nadpłata wraca dopiero po rocznym rozliczeniu.",A+"pasek-wynagrodzenia-jak-czytac.html","Pasek wynagrodzenia"),
 ("Czy B2B opłaca się bardziej niż etat?","Przy tym samym koszcie dla firmy — głównie w okresie ulg na start. Na stałe kontrakt ma sens, gdy kwota na fakturze jest wyższa od pensji brutto o ok. 30–40%, bo sam pokrywasz urlop, chorobowe i księgowość.",A+"b2b-czy-etat-porownanie.html","B2B czy etat"),
 ("Czy mogę legalnie dorabiać bez zakładania firmy?","Tak — na zleceniu, umowie o dzieło albo w ramach działalności nierejestrowanej, jeśli przychód nie przekracza 10 813,50 zł na kwartał (2026 r.; w 2027 r. 11 137,50 zł). Dochód wykazujesz w rocznym zeznaniu.",A+"dorabianie-po-godzinach.html","Dorabianie po godzinach"),
]),
("Budżet i oszczędzanie",[
 ("Ile powinienem odkładać z pensji?","Na start 5–10% dochodu netto, docelowo ok. 20% (z czego ok. 10% na emeryturę, wliczając PPK). Ważniejsza od kwoty jest automatyzacja: przelew dzień po wypłacie.",A+"automatyzacja-oszczedzania.html","Automatyzacja oszczędzania"),
 ("Ile powinna wynosić poduszka finansowa?","Równowartość 3–6 miesięcy niezbędnych wydatków. Bliżej trzech przy stabilnym etacie, bliżej sześciu przy B2B, zleceniu lub jednej pensji w gospodarstwie.",A+"poduszka-finansowa.html","Poduszka finansowa"),
 ("Gdzie trzymać poduszkę finansową?","Tam, skąd wypłacisz ją w jeden dzień bez straty: na koncie oszczędnościowym, ewentualnie częściowo na krótkich lokatach. Nie w akcjach i nie w długoterminowych obligacjach.",A+"gdzie-trzymac-pieniadze-na-rok-trzy-piec-lat.html","Gdzie trzymać pieniądze"),
 ("Najpierw spłacać długi czy oszczędzać?","Najpierw mały bufor (1 000–2 000 zł), potem drogie długi, dopiero później pełna poduszka i inwestowanie. PPK z dopłatą pracodawcy warto mieć od początku.",A+"kolejnosc-finansowych-priorytetow.html","Kolejność finansowych priorytetów"),
 ("Czy pieniądze w banku są bezpieczne?","Depozyty w bankach i SKOK-ach chroni Bankowy Fundusz Gwarancyjny do równowartości 100 000 euro na osobę w jednej instytucji. Gwarancja nie obejmuje funduszy, akcji ani kryptowalut.",A+"konto-bankowe-jak-wybrac.html","Konto bankowe — jak wybrać"),
 ("Jak chronić oszczędności przed inflacją?","Poduszkę trzymaj na oprocentowanym koncie, akceptując niewielką stratę jako cenę dostępności. Pieniądze na kilka lat — w obligacjach indeksowanych inflacją; na kilkanaście — częściowo w szerokich funduszach akcji.",A+"inflacja-a-twoje-pieniadze.html","Inflacja a Twoje pieniądze"),
]),
("Kredyty i długi",[
 ("Co to jest RRSO?","Rzeczywista roczna stopa oprocentowania — jedna liczba łącząca odsetki, prowizję i pozostałe koszty kredytu. To ona, a nie „oprocentowanie 0%” z reklamy, pozwala porównać dwie oferty.",A+"rrso-jak-czytac-oferte-pozyczki.html","RRSO i prawdziwy koszt kredytu"),
 ("Lawina czy kula śnieżna — która metoda spłaty długów jest lepsza?","Lawina (od najdroższego długu) jest matematycznie najtańsza, kula śnieżna (od najmniejszego) daje szybsze efekty. Różnica bywa niewielka — najwięcej zyskujesz, mając jakikolwiek plan zamiast płacenia samych minimalnych rat.",N+"kalkulator-splaty-dlugow.html","Kalkulator spłaty długów"),
 ("Czy mogę zwrócić pożyczkę zaraz po jej wzięciu?","Tak. Od umowy kredytu konsumenckiego możesz odstąpić w ciągu 14 dni bez podawania przyczyny, a spłacić wcześniej — w dowolnym momencie, z proporcjonalnym obniżeniem kosztów.",A+"rrso-jak-czytac-oferte-pozyczki.html","RRSO i prawdziwy koszt kredytu"),
 ("Czy firma windykacyjna może zająć moje konto?","Nie. Zajęcia może dokonać wyłącznie komornik sądowy na podstawie orzeczenia sądu. Windykator może dzwonić, pisać i proponować ugodę.",A+"windykacja-i-komornik-twoje-prawa.html","Windykacja i komornik"),
 ("Ile wkładu własnego potrzeba na kredyt hipoteczny?","Standardowo 20% wartości nieruchomości; część banków akceptuje 10% przy dodatkowym zabezpieczeniu. Do tego kilka procent ceny na koszty transakcji i nienaruszona poduszka finansowa.",A+"kredyt-hipoteczny-dla-poczatkujacych.html","Kredyt hipoteczny dla początkujących"),
]),
("Inwestowanie i emerytura",[
 ("Od jakiej kwoty można zacząć inwestować?","Obligacje skarbowe kosztują 100 zł za sztukę, a jednostki wielu funduszy ETF — kilkadziesiąt do kilkuset złotych. Przy małych kwotach pilnuj prowizji minimalnej u brokera.",A+"rachunek-maklerski-pierwsze-zlecenie.html","Rachunek maklerski"),
 ("Co to jest ETF?","Fundusz notowany na giełdzie, który odwzorowuje indeks — np. kilka tysięcy spółek z całego świata. Kupujesz go jedną transakcją, a roczny koszt to zwykle ułamek procenta.",A+"etf-dla-poczatkujacych.html","ETF-y dla początkujących"),
 ("Czy warto zostać w PPK?","W większości przypadków tak: do Twoich 2% pensji pracodawca dokłada 1,5%, a państwo — dopłaty. To pieniądze, których w inny sposób nie dostaniesz.",A+"ppk-pracownicze-plany-kapitalowe.html","PPK — czy warto zostać"),
 ("IKE czy IKZE — co wybrać?","IKE zwalnia zyski z podatku przy wypłacie po 60. roku życia; IKZE daje odliczenie wpłat od dochodu co roku, a przy wypłacie 10% ryczałtu. Można mieć oba.",A+"ike-ikze-emerytura.html","IKE i IKZE"),
 ("Co to jest OKI i czy warto je założyć?","Osobiste konto inwestycyjne działa od 2027 r.: zyski na nim nie są objęte podatkiem Belki, a wpłacać i wypłacać można bez limitów. Podatek od aktywów (0,85% rocznie) płaci się dopiero od średniej wartości ponad 100 000 zł, więc dla większości początkujących OKI oznacza inwestowanie bez podatku.",A+"osobiste-konto-inwestycyjne-oki.html","OKI — jak działa"),
 ("Ile odkładać na emeryturę?","Orientacyjnie ok. 10% dochodu netto przy starcie przed trzydziestką (wliczając PPK), 15% po trzydziestce i 20% po czterdziestce. Im wcześniej zaczniesz, tym mniejsza kwota wystarczy.",A+"ile-odkladac-na-emeryture.html","Ile odkładać na emeryturę"),
 ("Co zrobić, gdy moje inwestycje spadają?","Jeśli nie zmienił się Twój cel ani termin — nic, poza dalszymi regularnymi wpłatami. Sprzedaż w dołku zamienia przejściowy spadek wyceny w trwałą stratę.",A+"hossa-bessa-jak-nie-panikowac.html","Hossa, bessa i panika"),
 ("Ile wynosi podatek od zysków z oszczędności i inwestycji?","19% (tzw. podatek Belki) — od odsetek, dywidend i zysków ze sprzedaży. Można go ograniczyć, korzystając z IKE, IKZE i PPK.",A+"podatek-belki-jak-dziala.html","Podatek Belki"),
]),
("Mieszkanie, zakupy, bezpieczeństwo",[
 ("Ile może wynosić kaucja przy wynajmie mieszkania?","Maksymalnie dwunastokrotność miesięcznego czynszu przy zwykłym najmie i sześciokrotność przy najmie okazjonalnym; w praktyce jeden–dwa czynsze. Zwrot następuje w ciągu miesiąca od opróżnienia lokalu.",A+"umowa-najmu-na-co-uwazac.html","Umowa najmu mieszkania"),
 ("Czy mogę zwrócić towar kupiony w sklepie stacjonarnym?","Tylko jeśli sklep na to pozwala — to jego dobra wola. Ustawowe 14 dni na zwrot bez podania przyczyny dotyczy zakupów przez internet i poza lokalem przedsiębiorstwa.",A+"prawa-konsumenta-zwrot-reklamacja.html","Prawa konsumenta"),
 ("Jak długo mogę reklamować wadliwy produkt?","Sprzedawca odpowiada za zgodność towaru z umową przez dwa lata od wydania. Na odpowiedź ma 14 dni — brak odpowiedzi oznacza uznanie reklamacji.",A+"prawa-konsumenta-zwrot-reklamacja.html","Prawa konsumenta"),
 ("Jak zastrzec numer PESEL?","Bezpłatnie w aplikacji mObywatel, na gov.pl albo w urzędzie gminy. Zastrzeżenie działa od razu; cofasz je na czas własnych formalności kredytowych.",A+"oszustwa-finansowe-jak-sie-chronic.html","Oszustwa finansowe"),
 ("Co zrobić, gdy podałem dane oszustowi albo kliknąłem w fałszywy link?","Natychmiast zadzwoń do banku (numer z karty), zablokuj dostęp i kartę, zmień hasła z innego urządzenia, zgłoś sprawę na policję i do CERT Polska.",A+"oszustwa-finansowe-jak-sie-chronic.html","Oszustwa finansowe"),
 ("Które ubezpieczenia warto mieć na początku?","OC w życiu prywatnym, ubezpieczenie rzeczy i odpowiedzialności najemcy oraz polisę podróżną przy wyjazdach. Ubezpieczenie telefonu czy „przedłużoną gwarancję” zwykle można odpuścić.",A+"ubezpieczenia-na-starcie.html","Ubezpieczenia na starcie"),
]),
("Praca",[
 ("Ile dni urlopu mi przysługuje?","20 dni przy stażu poniżej 10 lat i 26 dni powyżej; do stażu wlicza się naukę (studia wyższe to 8 lat). Zaległy urlop trzeba wykorzystać do 30 września następnego roku.",A+"prawa-pracownika-w-liczbach.html","Prawa pracownika w liczbach"),
 ("Ile dostanę na zwolnieniu lekarskim?","Co do zasady 80% wynagrodzenia (100% m.in. w ciąży i po wypadku w drodze do pracy). Nowy pracownik nabywa to prawo zwykle po 30 dniach ubezpieczenia.",A+"prawa-pracownika-w-liczbach.html","Prawa pracownika w liczbach"),
 ("Czy pracodawca może zapytać, ile zarabiam w obecnej pracy?","Nie. Od końca 2025 r. pracodawca nie może pytać kandydata o dotychczasowe zarobki i ma obowiązek poinformować o proponowanym wynagrodzeniu lub jego przedziale.",A+"rozmowa-o-pieniadzach-w-rekrutacji.html","Oczekiwania finansowe na rozmowie o pracę"),
 ("Jaki mam okres wypowiedzenia?","Przy umowie na czas nieokreślony i określony: 2 tygodnie (staż u pracodawcy poniżej 6 miesięcy), 1 miesiąc (co najmniej 6 miesięcy) lub 3 miesiące (co najmniej 3 lata).",A+"zmiana-pracy-lista-kontrolna.html","Zmiana pracy — lista kontrolna"),
]),
]
for _,qs in G:
    for q,a,href,lt in qs: assert os.path.exists(root+href), href
tpl=open(root+'o-nas.html').read()
head=tpl[:tpl.index('<main>')]
d_old=re.search(r'<meta name="description" content="([^"]*)">',head).group(1)
total=sum(len(qs) for _,qs in G)
d_new='Najczęstsze pytania o pieniądze na starcie kariery — pensja i podatki, oszczędzanie, kredyty, inwestowanie, mieszkanie i prawa pracownika. Krótkie odpowiedzi z odesłaniem do poradników.'
head=head.replace('O nas | Mądry Portfel','Najczęstsze pytania o finanse | Mądry Portfel').replace(d_old,d_new).replace('madry-portfel/o-nas.html','madry-portfel/pytania.html')
ld={"@context":"https://schema.org","@type":"FAQPage","inLanguage":"pl-PL","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for _,qs in G for q,a,_,_ in qs]}
head=head.replace('</head>','<script type="application/ld+json">\n'+json.dumps(ld,ensure_ascii=False,indent=1)+'\n</script>\n</head>')
body=''; toc=[]
for i,(g,qs) in enumerate(G):
    toc.append(f'<a href="#grupa-{i+1}">{g}</a>')
    body+=f'  <h2 class="gl-letter" id="grupa-{i+1}">{g}</h2>\n'
    for q,a,href,lt in qs:
        body+=f'  <details class="faq">\n    <summary>{html.escape(q,quote=False)}</summary>\n    <p>{html.escape(a,quote=False)} <a href="{href}">{html.escape(lt,quote=False)} →</a></p>\n  </details>\n'
main=f'''<main>
  <nav class="breadcrumb" aria-label="Okruszki"><a href="index.html">Mądry Portfel</a> <span aria-hidden="true">/</span> <span aria-current="page">Najczęstsze pytania</span></nav>
  <h1>Najczęstsze pytania</h1>
  <p class="lead">{total} pytań, które słyszymy najczęściej — z krótką odpowiedzią i odesłaniem do poradnika lub kalkulatora, w którym temat jest rozwinięty. Nie znasz jakiegoś pojęcia? Zajrzyj do <a href="slownik.html">słownika</a>.</p>
  <nav class="cat-chips" aria-label="Grupy pytań">{''.join(toc)}</nav>

{body}
  <p><em>Odpowiedzi mają charakter edukacyjny i są celowo skrócone. Kwoty i terminy podano według stanu na listopad 2026 r. — szczegóły i zastrzeżenia znajdziesz w podlinkowanych poradnikach.</em></p>
</main>

'''
open(root+'pytania.html','w').write(head+main+tpl[tpl.index('<footer>'):])
print('faq',total)
