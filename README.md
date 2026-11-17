# Mądry Portfel — blog o finansach dla młodych na starcie kariery zawodowej

Statyczna strona (czysty HTML/CSS, zero build-toola) gotowa do darmowego hostingu na GitHub Pages.

## Struktura
- `index.html` — strona główna: wyszukiwarka poradników, odnośniki do kategorii i lista artykułów w siedmiu kategoriach
- `artykuly/` — 70 wpisów; każdy ma sekcję „Źródła i przydatne strony" z linkami do stron urzędowych
- `narzedzia/` — 4 kalkulatory działające w przeglądarce (bez zależności, do pobrania i użycia offline): brutto–netto, budżet 50/30/20, procent składany, spłata długów
- `slownik.html` — słownik 76 pojęć finansowych z odesłaniami do artykułów i kalkulatorów
- `pytania.html` — 34 najczęstsze pytania z krótkimi odpowiedziami (dane strukturalne FAQ)
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

| Co | Wartość 2026 | Gdzie występuje |
|---|---|---|
| Minimalne wynagrodzenie | 4806 zł brutto | `narzedzia/kalkulator-brutto-netto.html`, `artykuly/ubezpieczenia-na-starcie.html` (kara za brak OC) |
| Limit działalności nierejestrowanej | 10 813,50 zł na kwartał | `artykuly/dorabianie-po-godzinach.html` |
| Limit ulgi dla młodych, kwota wolna, próg podatkowy | 85 528 zł / 30 000 zł / 120 000 zł | `artykuly/zwrot-podatku-pit-dla-mlodych.html`, `artykuly/dorabianie-po-godzinach.html`, kalkulator brutto–netto |
| Składki i koszty uzyskania przychodu | 13,71% / 9% / 250 zł | kalkulator brutto–netto |
| Opłaty za przedterminowy wykup obligacji | 0,50–3 zł | `artykuly/obligacje-skarbowe-dla-poczatkujacych.html` |
| Opłaty przy zakupie auta | PCC 2%, rejestracja ok. 160 zł | `artykuly/pierwszy-samochod-ile-kosztuje.html` |

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
