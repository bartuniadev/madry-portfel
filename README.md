# Mądry Portfel — finanse osobiste i kalkulatory dla młodych

**Strona: https://bartuniadev.github.io/madry-portfel/**

Darmowe poradniki i kalkulatory finansowe dla osób, które dopiero zaczynają zarabiać — bez reklam, bez kont i bez ciasteczek. Każdy tekst ma źródła urzędowe.

Najczęściej używane:
- [Kalkulator brutto–netto 2027 (w obie strony)](https://bartuniadev.github.io/madry-portfel/narzedzia/kalkulator-brutto-netto.html)
- [Czy dobrze zarabiam? — Twoja pensja na tle Polaków (dane GUS)](https://bartuniadev.github.io/madry-portfel/narzedzia/czy-dobrze-zarabiam.html)
- [Ile na rękę w 2027 — tabela brutto–netto](https://bartuniadev.github.io/madry-portfel/artykuly/ile-na-reke-tabela-brutto-netto.html)
- [Zmiany w finansach od 1 stycznia 2027](https://bartuniadev.github.io/madry-portfel/artykuly/zmiany-w-finansach-2027.html)
- [Porównanie ofert pracy — etat czy zlecenie, benefity, dojazdy](https://bartuniadev.github.io/madry-portfel/narzedzia/porownanie-ofert-pracy.html)
- [Kalkulator inflacji (GUS od 2000 r.)](https://bartuniadev.github.io/madry-portfel/narzedzia/kalkulator-inflacji.html)
- [Wszystkie kalkulatory](https://bartuniadev.github.io/madry-portfel/narzedzia/index.html)

---

Statyczna strona (czysty HTML/CSS, zero build-toola) na GitHub Pages. Skrypty generujące artykuły, kalkulatory i dodatki są w `_narzedzia-budowania/`.

## Struktura
- `index.html` — strona główna: wyszukiwarka poradników, odnośniki do kategorii i lista artykułów w siedmiu kategoriach
- `artykuly/` — 78 wpisów; każdy ma sekcję „Źródła i przydatne strony" z linkami do stron urzędowych
- `narzedzia/` — 13 kalkulatorów działających w przeglądarce (bez zależności, do pobrania i użycia offline): czy dobrze zarabiam (rozkład płac GUS), brutto–netto 2026/2027 (z wypłatą w każdym miesiącu), umowa zlecenia, porównanie dwóch ofert pracy (netto, benefity, dojazdy), inflacja (CPI GUS od 2000 r.), lokata, kredyt (raty, RRSO, nadpłata), OKI, poduszka finansowa, podział kosztów dla par, budżet 50/30/20, procent składany, spłata długów
- `wynagrodzenia/` — strony „X zł brutto ile netto” dla 11 popularnych kwot (5000–15 000 zł) i „X zł netto ile brutto” dla 6 kwot (4000–10 000 zł): etat, zlecenie, koszt pracodawcy, pozycja na tle płac GUS, budżet, FAQ
- `slownik.html` — słownik 77 pojęć finansowych z odesłaniami do artykułów i kalkulatorów
- `pytania.html` — 36 najczęstszych pytań z krótkimi odpowiedziami (dane strukturalne FAQ)
- `pliki/budzet-domowy-madry-portfel.xlsx` — darmowy arkusz budżetu domowego (miesiąc 50/30/20, rok, cele) do pobrania bez maila; generowany skryptem z formułami.
- `o-nas.html`, `polityka-prywatnosci.html` — strony wymagane m.in. do AdSense
- `style.css`, `assets/` — style, fonty, skrypt animacji (`reveal.js`) oraz statystyk i komunikatu o prywatności (`stats.js`)
- `404.html` — strona błędu dla nieistniejących adresów (GitHub Pages używa jej automatycznie)
- `robots.txt`, `sitemap.xml` — SEO

## Statystyki odwiedzin i prywatność
- Odwiedziny liczy **GoatCounter** — bez plików cookies i bez profilowania. Kod licznika jest w `assets/stats.js` (stała `GOATCOUNTER_CODE`, obecnie `madryportfel`); skrypt jest dołączony do każdej strony.
- **Żeby statystyki zaczęły się zbierać, załóż konto na goatcounter.com z kodem strony `madryportfel`** (albo z innym kodem i podmień stałą w `assets/stats.js`). Panel będzie pod adresem `https://madryportfel.goatcounter.com`.
- Licznik działa tylko na opublikowanej stronie (nie w pobranych kalkulatorach), respektuje sygnały Global Privacy Control / Do Not Track i można go wyłączyć na stronie polityki prywatności.
- Komunikat o prywatności wyświetla się raz; po kliknięciu „Rozumiem” zapisuje w localStorage klucz `mp-notice`.
- Jeśli kiedyś dodasz reklamy (AdSense) lub inne narzędzia używające cookies, trzeba będzie wdrożyć baner zgody i zaktualizować `polityka-prywatnosci.html`.

## Widoczność w wyszukiwarkach i AI
- `sitemap.xml` — zgłoszona w Google Search Console (71 adresów; bez polityki prywatności, która ma `noindex`).
- `feed.xml` — kanał RSS z nowymi poradnikami (link w nagłówku każdej strony).
- `llms.txt` — opis serwisu i lista poradników dla asystentów AI.
- `8e2e70638e5f6d82df0618f5c750c046.txt` — klucz IndexNow; po publikacji nowych treści zgłoś adresy do Binga i innych wyszukiwarek przez `https://api.indexnow.org/IndexNow` (host `bartuniadev.github.io`, `keyLocation` wskazujący ten plik).
- `_seo/slowa-kluczowe.csv` — mapa słów kluczowych: fraza główna, frazy dodatkowe, tytuł SEO, opis meta i H1 dla każdej strony (folder z podkreślnikiem nie jest publikowany przez GitHub Pages). Fraza główna występuje w tytule, opisie, H1, ramce „W skrócie”/wstępie i co najmniej jednym H2.
- `assets/og/*.jpg` — grafiki 1200×630 wyświetlane przy udostępnianiu linków (Facebook, LinkedIn, WhatsApp, X); `assets/share.js` obsługuje przyciski „Udostępnij” i „Kopiuj link” pod artykułami.

## Coroczny przegląd — liczby, które się zmieniają
Część treści zawiera kwoty obowiązujące w konkretnym roku (stan: listopad 2026). Na początku każdego roku sprawdź i zaktualizuj:

| Co | 2026 | 2027 | Gdzie występuje |
|---|---|---|---|
| Minimalne wynagrodzenie / stawka godzinowa | 4806 zł / 31,40 zł | 4950 zł / 32,30 zł | kalkulator brutto–netto (`YEARS`), `artykuly/placa-minimalna-2027-netto.html`, `artykuly/zmiany-w-finansach-2027.html`, `artykuly/prawa-pracownika-w-liczbach.html`, `artykuly/ile-na-reke-tabela-brutto-netto.html`, `artykuly/ubezpieczenia-na-starcie.html` (kara za brak OC) |
| Limit działalności nierejestrowanej (kwartał) | 10 813,50 zł | 11 137,50 zł | `artykuly/dorabianie-po-godzinach.html`, `pytania.html` |
| Kwota wolna od zajęcia na koncie | 3604,50 zł | 3712,50 zł | `artykuly/windykacja-i-komornik-twoje-prawa.html` |
| Limit IKE / IKZE | 28 260 / 11 304 zł | 30 099 / 12 039,60 zł | `artykuly/ike-ikze-emerytura.html`, `artykuly/koniec-roku-finanse-lista.html`, kalkulator OKI (`IKE_LIMIT`) |
| Roczny limit podstawy składek emerytalnej i rentowej | 282 600 zł | ok. 300 990 zł (z projektu budżetu — potwierdź w styczniu) | kalkulator brutto–netto (`YEARS.cap`) |
| Podatek od aktywów OKI / kwota zwolniona | — | 0,85% / 100 000 zł (w tym 25 000 zł oszczędności) | kalkulator OKI, `artykuly/osobiste-konto-inwestycyjne-oki.html` |
| Skala PIT | 12% do 120 000 zł, 32% powyżej | czeka na decyzję prezydenta (12% / 24% / 32%, progi 130 i 150 tys. zł) | kalkulator brutto–netto (pole „Nowa skala”), `artykuly/zmiany-w-finansach-2027.html`, `artykuly/ile-na-reke-tabela-brutto-netto.html` |
| Rozkład płac GUS (mediana, decyle) | — | maj 2026: D1 4806 zł, mediana 7550,32 zł, D9 14 239 zł | `narzedzia/czy-dobrze-zarabiam.html` (MED, D1, D9), `artykuly/mediana-wynagrodzen-ile-zarabiaja-polacy.html`, strony w `wynagrodzenia/` |
| Inflacja średnioroczna (CPI GUS) | 2025: 3,6% | 2026: szacunek 3,5% — w styczniu 2027 wpisz wynik GUS | `narzedzia/kalkulator-inflacji.html` (obiekt `CPI`) |
| Limit ulgi dla młodych, kwota wolna | 85 528 zł / 30 000 zł | bez zmian | `artykuly/zwrot-podatku-pit-dla-mlodych.html`, kalkulator brutto–netto |
| Składki i koszty uzyskania przychodu | 13,71% / 9% / 250 zł | bez zmian | kalkulator brutto–netto |
| Opłaty za przedterminowy wykup obligacji | 0,50–3 zł | sprawdź | `artykuly/obligacje-skarbowe-dla-poczatkujacych.html` |
| Opłaty przy zakupie auta | PCC 2%, rejestracja ok. 160 zł | sprawdź | `artykuly/pierwszy-samochod-ile-kosztuje.html` |

Kalkulator brutto–netto sam przełącza się na rok 2027 od 1 stycznia 2027 r. (wg daty w przeglądarce). Na rok 2028 dopisz nowy wpis w obiekcie `YEARS` i przycisk roku.

Przy każdej zmianie treści zaktualizuj też `lastmod` w `sitemap.xml` oraz `dateModified` w danych strukturalnych artykułu.

## Jak wystawić stronę za darmo (GitHub Pages)

1. Załóż konto na github.com (jeśli jeszcze nie masz).
2. Utwórz nowe, **publiczne** repozytorium, np. `madry-portfel`.
3. W tym folderze:
   ```
   git init
   git add .
   git commit -m "Pierwsza wersja bloga"
   git branch -M main
   git remote add origin https://github.com/TWOJ-LOGIN/madry-portfel.git
   git push -u origin main
   ```
4. W ustawieniach repozytorium: **Settings → Pages → Source: Deploy from branch → main / (root)**.
5. Po kilku minutach strona będzie dostępna pod `https://TWOJ-LOGIN.github.io/madry-portfel/`.
6. Podmień `TWOJA-DOMENA-LUB-GITHUB-IO` w `robots.txt` i `sitemap.xml` na ten realny adres.

Własna domena (np. `.pl`) to koszt (zwykle kilkadziesiąt zł/rok) — na start nie jest potrzebna, subdomena `github.io` działa i jest indeksowana przez Google.

## Następne kroki (w kolejności, która realnie działa)

1. **Zarejestruj się w Google Search Console** i dodaj adres strony + `sitemap.xml`, żeby Google w ogóle zaczął indeksować treść.
2. **Pisz regularnie** — 2 nowe artykuły tygodniowo robią więcej niż 10 na start i potem cisza. Wyszukiwarki premiują świeżość i regularność.
3. **Google AdSense** — zgłoś stronę dopiero gdy będzie miała ok. 15–20 solidnych artykułów i realny (choćby mały) ruch. Zgłoszenia z pustą stroną są odrzucane. Wymaga: polityki prywatności (jest), realnych treści (są), i strony "O nas" (jest).
4. **Programy partnerskie (afiliacja) w finansach PL** — do zbadania i wybrania samodzielnie, bo warunki i dostępność zmieniają się często:
   - sieci afiliacyjne ogólne działające w Polsce: Awin, Rakuten Advertising, Adtraction — mają w ofercie też produkty finansowe,
   - porównywarki finansowe z własnym programem partnerskim (np. typu Rankomat, Totalmoney, Comperia) — sprawdź aktualne warunki na ich stronach,
   - programy partnerskie pojedynczych fintechów/domów maklerskich — część z nich prowadzi własne programy poleceń, warto sprawdzić bezpośrednio na ich stronach.
   - **Ważne:** rejestracja w programie afiliacyjnym dla produktów finansowych zwykle wymaga podania danych do rozliczeń (czasem działalności gospodarczej) — to musisz zrobić samodzielnie, jako właściciel strony.
5. Po uzyskaniu pierwszych linków partnerskich — wstaw je w miejscach oznaczonych `<!-- TODO -->` w artykułach i zamień treść boksu `.disclosure` tak, by dokładnie opisywał, z czego korzystasz.

## Ważne zastrzeżenie

To nie jest "ustaw i zapomnij". Realny dochód z takiej strony (reklamy + afiliacja) zwykle pojawia się po miesiącach regularnego publikowania i budowania ruchu z wyszukiwarki — pierwsze tygodnie to praca bez przychodu. Traktuj to jako projekt na wiele miesięcy, nie jednorazowe wdrożenie.
