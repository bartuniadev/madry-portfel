# Mądry Portfel — blog o finansach dla młodych na starcie kariery zawodowej

Statyczna strona (czysty HTML/CSS, zero build-toola) gotowa do darmowego hostingu na GitHub Pages.

## Struktura
- `index.html` — strona główna z listą artykułów
- `artykuly/` — poszczególne wpisy
- `o-nas.html`, `polityka-prywatnosci.html` — strony wymagane m.in. do AdSense
- `robots.txt`, `sitemap.xml` — SEO (podmień `TWOJA-DOMENA-LUB-GITHUB-IO` na realny adres po wdrożeniu)

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
