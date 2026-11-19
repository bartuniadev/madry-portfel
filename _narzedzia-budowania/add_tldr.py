# Inserts "W skrócie" boxes (p.tldr) after the meta line: into source bodies for generated
# articles (rebuild afterwards) and directly into the page for hand-written (legacy) articles.
import os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import build_all as B, build_more as M
ROOT = '/home/user/madry-portfel/'
TLDR = {
 'black-friday-jak-nie-dac-sie-nabic': 'Black Friday 2026: kupuj tylko z listy przygotowanej przed wyprzedażą i porównuj cenę z najniższą ceną z 30 dni przed obniżką — sklep musi ją podać przy każdej promocji. Przy ratach „0%” sprawdzaj RRSO i całkowitą kwotę do zapłaty, a zakupy w internecie możesz zwrócić w ciągu 14 dni.',
 'budzet-50-30-20': 'Budżet domowy metodą 50/30/20: 50% dochodu netto na potrzeby (mieszkanie, rachunki, jedzenie, dojazdy), 30% na wydatki uznaniowe i 20% na oszczędności oraz nadpłatę długów. Proporcje możesz dopasować do swojej sytuacji — ważne, żeby część na oszczędności przelewać od razu po wypłacie.',
 'chwilowki-ile-naprawde-kosztuja': 'Chwilówki kosztują więcej, niż sugeruje reklama: 100 zł opłat za pożyczenie 2000 zł na 30 dni to 5% miesięcznie, a w skali roku RRSO rzędu kilkudziesięciu procent. Najdroższe jest przedłużanie terminu — dług główny nie maleje, a opłaty rosną.',
 'emerytura-z-zus-ile-realnie-dostaniesz': 'Emerytura z ZUS dla dzisiejszych 20- i 30-latków będzie stanowić wyraźnie mniejszą część ostatniej pensji niż u obecnych emerytów — prognozy mówią o ok. jednej czwartej do jednej trzeciej. Różnicę możesz uzupełnić sam: PPK z dopłatą pracodawcy, IKE lub IKZE i regularne inwestowanie.',
 'ike-ikze-emerytura': 'IKE czy IKZE? IKZE daje ulgę od razu — wpłaty (do 12 039,60 zł w 2027 r.) odliczasz od dochodu w PIT, a przy wypłacie po 65. roku życia płacisz 10% ryczałtu. IKE (limit 30 099 zł w 2027 r.) nie daje ulgi przy wpłacie, ale zyski są bez podatku przy wypłacie po 60. roku życia. Można mieć oba.',
 'ile-odkladac-na-emeryture': 'Ile odkładać na emeryturę? Zaczynając przed trzydziestką — ok. 10% dochodu netto (wliczając PPK), po trzydziestce ok. 15%, a po czterdziestce 20% lub więcej. Im wcześniej zaczniesz, tym mniejsza miesięczna kwota wystarczy, bo dłużej pracuje procent składany.',
 'inflacja-a-twoje-pieniadze': 'Oszczędności a inflacja: pieniądze bez oprocentowania co roku tracą realną wartość — przy inflacji 5% za 10 000 zł po roku kupisz tyle, co dziś za ok. 9 500 zł. Poduszkę trzymaj na koncie oszczędnościowym, pieniądze na kilka lat w obligacjach indeksowanych inflacją, a na kilkanaście lat — częściowo w funduszach akcji.',
 'karta-kredytowa-historia-kredytowa': 'Karta kredytowa nic nie kosztuje, jeśli co miesiąc spłacasz całe zadłużenie w okresie bezodsetkowym (zwykle ok. 50–56 dni). Spłacana w terminie buduje historię kredytową w BIK, która pomaga później przy kredycie hipotecznym; płacenie tylko „minimalnej raty” uruchamia wysokie odsetki.',
 'konto-bankowe-jak-wybrac': 'Darmowe konto bankowe to takie, które nic nie kosztuje przy Twoim sposobie korzystania: sprawdź w cenniku opłatę za kartę, bankomaty, przelewy natychmiastowe, przewalutowanie i warunek wpływu pensji. Pieniądze w banku chroni BFG do równowartości 100 000 euro na osobę w jednym banku.',
 'kredyt-hipoteczny-dla-poczatkujacych': 'Kredyt hipoteczny: bank zwykle wymaga 20% wkładu własnego (część banków — 10% z dodatkowym zabezpieczeniem), a do tego potrzebujesz kilku procent ceny na notariusza, podatki i opłaty. Bezpieczna rata to wyraźnie mniej niż maksymalna zdolność kredytowa — licz też całkowity koszt odsetek przez 25–30 lat.',
 'obligacje-skarbowe-dla-poczatkujacych': 'Obligacje skarbowe kosztują 100 zł za sztukę i są jednym z najbezpieczniejszych miejsc na oszczędności w złotych. Na kilka lat najczęściej wybiera się obligacje indeksowane inflacją (COI na 4 lata, EDO na 10 lat), na krótszy termin — stałoprocentowe; przy wcześniejszym wykupie płacisz niewielką opłatę.',
 'oc-dla-mlodego-kierowcy': 'OC dla młodego kierowcy jest drogie, bo ubezpieczyciel nie zna Twojej historii — ale różnica między najtańszą a najdroższą ofertą bywa wielokrotna. Porównuj kilka ofert, pamiętaj, że moc i pojemność silnika podnoszą składkę, a współwłasność z rodzicem rozważ ze świadomością, że szkoda obciąży też jego zniżki.',
 'pasek-wynagrodzenia-jak-czytac': 'Pasek wynagrodzenia pokazuje, dokąd idzie różnica między brutto a netto: składki społeczne (13,71% brutto), składka zdrowotna (9%), zaliczka na podatek i ewentualnie PPK. Sprawdź na nim, czy pracodawca uwzględnił PIT-2 (300 zł mniej zaliczki miesięcznie), ulgę dla młodych i właściwe koszty dojazdu.',
 'pierwsza-pensja': 'Pierwsza pensja: zanim zaczniesz wydawać, ustaw przelew na oszczędności w dniu wypłaty — co najmniej 10–20% — a resztę podziel na stałe koszty (ok. 50%) i wydatki dla przyjemności. Sprawdź też pasek wynagrodzenia, PIT-2 i PPK oraz zacznij budować bufor na niespodzianki.',
 'plan-na-pierwszy-rok-pracy': 'Pierwsza praca a finanse — plan na 12 miesięcy: najpierw sprawdź umowę i pasek, zdecyduj o PPK i zapisuj wydatki, potem ułóż budżet i zbuduj poduszkę finansową, a pod koniec roku zajmij się IKE lub IKZE i pierwszym PIT. Stałe zlecenie na oszczędności — choćby 5–10% pensji — ustaw już po pierwszej wypłacie.',
 'podatek-belki-jak-dziala': 'Podatek Belki to 19% od odsetek, dywidend i zysków z inwestycji — bez kwoty wolnej i bez odliczania inflacji. Legalnie zapłacisz mniej, oszczędzając na IKE, IKZE, w PPK i na koncie OKI (od 2027 r.) oraz rozliczając straty z zyskami w PIT-38.',
 'poduszka-finansowa': 'Poduszka finansowa to 3–6 miesięcy niezbędnych wydatków (nie całej pensji) na koncie, z którego wypłacisz pieniądze w jeden dzień. Zacznij od 1000 zł bufora, potem odłóż równowartość jednego miesiąca wydatków, a dopiero później dochodź do pełnej kwoty.',
 'ppk-pracownicze-plany-kapitalowe': 'PPK czy warto? W większości przypadków tak: do Twojej wpłaty 2% pensji pracodawca dokłada 1,5%, a państwo — wpłatę powitalną i coroczne dopłaty. Rezygnację rozważ, gdy spłacasz drogi dług albo nie masz jeszcze żadnego bufora na nagłe wydatki.',
 'rozmowa-o-pieniadzach-w-rekrutacji': 'Oczekiwania finansowe na rozmowie o pracę: pracodawca musi podać wynagrodzenie lub widełki w ogłoszeniu albo przed rozmową i nie może pytać o Twoje dotychczasowe zarobki. Przygotuj jedną kwotę brutto opartą na stawkach rynkowych i dopytaj, czy widełki dotyczą umowy o pracę, czy B2B.',
 'rrso-jak-czytac-oferte-pozyczki': 'RRSO to jedna liczba, która łączy odsetki, prowizję i inne obowiązkowe koszty kredytu — to ona, a nie „oprocentowanie 0%” z reklamy, pozwala porównać oferty. Drugą liczbą do porównania jest całkowita kwota do zapłaty; od umowy kredytu konsumenckiego możesz odstąpić w ciągu 14 dni.',
 'subskrypcje-i-stale-oplaty': 'Stałe opłaty i subskrypcje rosną bez Twojej decyzji — przegląd historii konta z 12 miesięcy zwykle znajduje kilkaset złotych rocznie do odzyskania. Anuluj to, czego nie używasz od 30 dni, zmniejsz pakiety ponad potrzeby i zapisz daty końca umów, żeby negocjować przed odnowieniem.',
 'umowa-najmu-na-co-uwazac': 'Umowa najmu mieszkania: zanim zapłacisz kaucję, sprawdź w księdze wieczystej, czy wynajmujący ma prawo do lokalu, i płać tylko na konto osoby z umowy. W umowie pilnuj wysokości kaucji i zasad jej zwrotu, podwyżek, okresu wypowiedzenia oraz protokołu stanu mieszkania z odczytem liczników.',
 'umowa-o-prace-jak-czytac': 'Umowa o pracę: przed podpisaniem sprawdź rodzaj umowy, miejsce pracy, wymiar etatu i przede wszystkim składniki wynagrodzenia — co jest pensją zasadniczą, a co premią uznaniową. Okres próbny trwa najwyżej 3 miesiące, a w ciągu 7 dni od rozpoczęcia pracy pracodawca przekazuje informację o warunkach zatrudnienia.',
 'utrata-pracy-plan-finansowy': 'Utrata pracy: sprawdź, co Ci się należy — okres wypowiedzenia (od 2 tygodni do 3 miesięcy, zależnie od stażu), ekwiwalent za niewykorzystany urlop, a przy zwolnieniu z przyczyn leżących po stronie firmy zatrudniającej co najmniej 20 osób — także odprawę. W pierwszym tygodniu przejdź na budżet awaryjny i nie podpisuj porozumienia stron od ręki.',
 'wspolne-finanse-w-zwiazku': 'Wspólne finanse w związku działają zwykle w jednym z trzech modeli: wspólne konto na wszystko, osobne konta albo model mieszany — osobne pensje i wspólne konto na stałe koszty. Zacznijcie od rozmowy o dochodach, długach i kwocie, którą każde może wydać bez pytania; koszty można dzielić po równo lub proporcjonalnie do zarobków.',
 'wyprowadzka-od-rodzicow-ile-kosztuje': 'Wyprowadzka od rodziców: na start potrzebujesz zwykle kaucji i pierwszego czynszu (razem równowartość 2–3 miesięcznych opłat) oraz pieniędzy na przeprowadzkę i wyposażenie, a co miesiąc — na czynsz, media, jedzenie i dojazdy. Przez trzy miesiące przed wyprowadzką odkładaj kwotę przyszłych opłat — sprawdzisz, czy budżet jest realny.',
 'zmiana-pracy-lista-kontrolna': 'Zmiana pracy to najskuteczniejszy sposób na podwyżkę, ale przed wypowiedzeniem sprawdź, co możesz stracić: premię wypłacaną tylko zatrudnionym, niewykorzystany urlop, zobowiązania z umowy szkoleniowej i zakaz konkurencji. Po pierwszej wypłacie u nowego pracodawcy podnieś stałe zlecenie na oszczędności o połowę różnicy netto.',
}


def nb(t):
    t = re.sub(r'(\d) (\d{3})(?!\d)', '\\1\u00a0\\2', t)
    return re.sub(r'(\d) (zł|%|euro|dni|lat|miesięcy|miesiące)', '\\1\u00a0\\2', t)


bodies = {a['slug']: a['body'] for a in B.ARTICLES + M.ARTICLES}
done_body, done_legacy = [], []
for slug, text in TLDR.items():
    p = (S + '/' + bodies[slug]) if slug in bodies else (ROOT + f'artykuly/{slug}.html')
    s = open(p).read()
    if 'class="tldr"' in s:
        continue
    m = re.search(r'<p class="meta">.*?</p>', s, re.S)
    assert m, slug
    box = f'\n\n  <p class="tldr"><strong>W skrócie:</strong> {nb(text)}</p>'
    s = s[:m.end()] + box + s[m.end():]
    open(p, 'w').write(s)
    (done_body if slug in bodies else done_legacy).append(slug)
# zwrot podatku: convert the existing summary paragraph into the box
p = S + '/' + bodies['zwrot-podatku-pit-dla-mlodych']
s = open(p).read()
if 'class="tldr"' not in s:
    m = re.search(r'<div class="card">\s*<p><strong>W skrócie:</strong>(.*?)</p>\s*</div>', s, re.S)
    if m:
        s = s[:m.start()] + '<p class="tldr"><strong>W skrócie:</strong>' + m.group(1) + '</p>' + s[m.end():]
        open(p, 'w').write(s)
        done_body.append('zwrot-podatku-pit-dla-mlodych')
print('bodies:', len(done_body), 'legacy:', len(done_legacy))
print(' '.join(done_body))
