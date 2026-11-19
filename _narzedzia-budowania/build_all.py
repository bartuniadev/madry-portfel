import sys, os
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S); import gen
rd=lambda n: open(S+'/'+n).read()
SRC = {
 'ulga': ('https://www.podatki.gov.pl/ulgi-i-odliczenia/ulga-dla-mlodych-pit-dla-osob-do-26-lat','Ulga dla młodych — podatki.gov.pl','oficjalny opis zwolnienia, limitu i rodzajów przychodów objętych ulgą'),
 'knf': ('https://www.knf.gov.pl/dla_konsumenta/ostrzezenia_publiczne','Lista ostrzeżeń publicznych KNF','podmioty, wobec których nadzór złożył zawiadomienie o podejrzeniu przestępstwa'),
 'rf': ('https://rf.gov.pl/dla-klientow/czy-rzecznik-moze-ci-pomoc/','Rzecznik Finansowy','bezpłatna pomoc w sporze z bankiem, firmą pożyczkową lub ubezpieczycielem'),
 'podatki': ('https://www.podatki.gov.pl/','Serwis podatki.gov.pl','usługa Twój e-PIT, formularze i aktualne terminy'),
 'bik': ('https://www.bik.pl/','Biuro Informacji Kredytowej','sprawdzenie własnej historii kredytowej'),
 'pesel': ('https://www.gov.pl/web/gov/zastrzez-swoj-numer-pesel-lub-cofnij-zastrzezenie','Zastrzeż swój numer PESEL — gov.pl','bezpłatna usługa online, dostępna też w aplikacji mObywatel'),
 'npp': ('https://www.gov.pl/web/nieodplatna-pomoc','Nieodpłatna pomoc prawna i poradnictwo obywatelskie','zapisy na bezpłatną poradę, także dla osób zadłużonych'),
 'obl': ('https://www.obligacjeskarbowe.pl/oferta-obligacji/','Aktualna oferta obligacji — obligacjeskarbowe.pl','oprocentowanie i listy emisyjne bieżących serii'),
}
ICON = {
 'pit':'<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="9" y1="12" x2="15" y2="12"/><path d="M9.5 16h5"/>',
 'obl':'<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M3 9h2M19 15h2M3 15h2M19 9h2"/>',
 'etf':'<path d="M12 3 L21 8 L12 13 L3 8 Z"/><path d="M3 12 L12 17 L21 12"/><path d="M3 16 L12 21 L21 16"/>',
 'debt':'<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
 'lock':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/><circle cx="12" cy="16" r="1"/>',
 'bolt':'<polygon points="13 2 4 14 11 14 10 22 20 9 13 9 13 2"/>',
}
CAT = {'dlugi':'Kredyty i długi','mieszkanie':'Mieszkanie i samochód','kariera':'Kariera i dochody','oszczedzanie':'Oszczędzanie i bezpieczeństwo','inwestowanie':'Emerytura i inwestowanie','budzet':'Budżet i wydatki','zacznij-tutaj':'Zacznij tutaj'}
ARTICLES = [
 dict(slug='zwrot-podatku-pit-dla-mlodych', title='Zwrot podatku i pierwszy PIT — co musisz wiedzieć przed 26. urodzinami i po nich',
  desc='Jak działa roczne rozliczenie PIT, skąd bierze się zwrot podatku albo dopłata, co zmienia ulga dla młodych i rok 26. urodzin oraz jak krok po kroku sprawdzić Twój e-PIT.',
  cat='kariera', icon='pit', hero='Ilustracja paragonu podatkowego — rozliczenie PIT', body='pit.html',
  related=['brutto-netto-rodzaje-umow','ike-ikze-emerytura','negocjacje-podwyzka-zmiana-pracy'],
  sources=[SRC['ulga'],('https://www.podatki.gov.pl/aktualnosci/kas-przypomina-zasady-rocznego-rozliczenia-pit-osob-do-26-roku-zycia','KAS: zasady rocznego rozliczenia PIT osób do 26. roku życia','kiedy trzeba złożyć zeznanie, a kiedy nie'),SRC['podatki']]),
 dict(slug='obligacje-skarbowe-dla-poczatkujacych', title='Obligacje skarbowe dla początkujących — jak chronić oszczędności przed inflacją',
  desc='Czym są obligacje skarbowe, czym różnią się serie OTS, TOS, COI i EDO, jak działa indeksacja inflacją, wcześniejszy wykup i podatek Belki — prosto, dla osób, które dopiero zaczynają oszczędzać.',
  cat='oszczedzanie', icon='obl', hero='Ilustracja obligacji skarbowej', body='obl.html',
  related=['konta-oszczednosciowe','poduszka-finansowa','ike-ikze-emerytura'],
  sources=[SRC['obl'],('https://www.obligacjeskarbowe.pl/faq/','Pytania i odpowiedzi — obligacjeskarbowe.pl','zasady przedterminowego wykupu, opłaty i zamiana obligacji')]),
 dict(slug='etf-dla-poczatkujacych', title='ETF-y dla początkujących — jak kupić cały rynek jedną transakcją',
  desc='Czym jest ETF, dlaczego opłaty mają tak duże znaczenie, co oznaczają TER, Acc i UCITS, jak krok po kroku kupić pierwszy fundusz indeksowy i jak rozliczyć podatek.',
  cat='inwestowanie', icon='etf', hero='Ilustracja warstw — koszyk wielu spółek w jednym funduszu', body='etf.html',
  related=['jak-zaczac-inwestowac','ike-ikze-emerytura','obligacje-skarbowe-dla-poczatkujacych'],
  sources=[('https://www.gpw.pl/etfy','ETF-y notowane na GPW','aktualna lista funduszy dostępnych na warszawskiej giełdzie'),SRC['knf'],('https://www.podatki.gov.pl/','Serwis podatki.gov.pl','formularz PIT-38 i zasady rozliczania zysków kapitałowych')]),
 dict(slug='jak-wyjsc-z-dlugow', title='Jak wyjść z długów — lawina, kula śnieżna i plan na pierwszy wieczór',
  desc='Plan wychodzenia z długów krok po kroku: spis zobowiązań, metoda lawiny i kuli śnieżnej na liczbach, rozmowa z wierzycielem, konsolidacja i bezpłatna pomoc dla zadłużonych.',
  cat='dlugi', icon='debt', hero='Ilustracja ogniw łańcucha — wychodzenie z długów', body='dlugi.html',
  related=['bnpl-raty-pulapki','karta-kredytowa-historia-kredytowa','budzet-50-30-20'],
  sources=[SRC['npp'],SRC['rf'],('https://www.knf.gov.pl/dla_konsumenta/gdzie_szukac_pomocy_w_przypadku_sporu_z_instytucja_finansowa','KNF: gdzie szukać pomocy w sporze z instytucją finansową','przegląd instytucji, do których możesz się zwrócić'),SRC['bik']]),
 dict(slug='oszustwa-finansowe-jak-sie-chronic', title='Oszustwa finansowe — 6 schematów, na które łapią się nawet ostrożni',
  desc='Fałszywe SMS-y, telefon z „banku", BLIK na znajomego, fałszywe inwestycje i oferty pracy. Jak rozpoznać oszustwo, jak się zabezpieczyć i co zrobić w pierwszych minutach po utracie pieniędzy.',
  cat='oszczedzanie', icon='lock', hero='Ilustracja kłódki — bezpieczeństwo pieniędzy', body='oszustwa.html',
  related=['karta-kredytowa-historia-kredytowa','poduszka-finansowa','bnpl-raty-pulapki'],
  sources=[SRC['pesel'],('https://www.gov.pl/web/baza-wiedzy/dostales-niepokojacy-sms-albo-email-zglos-go-do-cert-polska-csirt-nask','Jak zgłosić podejrzany SMS lub e-mail do CERT Polska','numer 8080 i pozostałe kanały zgłoszeń'),('https://incydent.cert.pl/','Formularz zgłoszenia incydentu — CERT Polska','zgłaszanie fałszywych stron i prób wyłudzeń'),SRC['knf'],SRC['rf']]),
 dict(slug='dorabianie-po-godzinach', title='Jak dorobić do pensji legalnie — zlecenie, dzieło, działalność nierejestrowana i podatki',
  desc='Zlecenie, umowa o dzieło, działalność nierejestrowana czy sprzedaż własnych rzeczy — jak legalnie dorabiać do etatu, ile zostaje po podatku i kiedy opłaca się założyć firmę.',
  cat='kariera', icon='bolt', hero='Ilustracja błyskawicy — dodatkowe źródło dochodu', body='dorabianie.html',
  related=['negocjacje-podwyzka-zmiana-pracy','zwrot-podatku-pit-dla-mlodych','brutto-netto-rodzaje-umow'],
  sources=[('https://www.biznes.gov.pl/pl/portal/00115','Działalność nierejestrowana — biznes.gov.pl','warunki, aktualny limit przychodu i obowiązki'),('https://zielonalinia.gov.pl/dzialalnosc-nierejestrowa-co-warto-wiedziec/','Działalność nierejestrowa: co warto wiedzieć — Zielona Linia','praktyczne omówienie zasad przez centrum informacyjne służb zatrudnienia'),SRC['ulga']]),
]
