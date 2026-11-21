# Narzędzia do budowania strony

Ten katalog nie jest publikowany na stronie (GitHub Pages pomija katalogi zaczynające się od `_`). Są tu skrypty, którymi generowane są artykuły, kalkulatory i dodatki, oraz teksty źródłowe artykułów.

## Jak użyć
Skrypty zakładają, że teksty artykułów leżą w tym samym folderze co skrypty. Najprościej:

```bash
mkdir -p /tmp/mp && cp _narzedzia-budowania/*.py _narzedzia-budowania/*.js _narzedzia-budowania/og_template.html _narzedzia-budowania/tresci/*.html /tmp/mp/
cd /home/user/madry-portfel
python3 /tmp/mp/run_build.py <slug>        # przebuduj artykuł(y) z treści
python3 /tmp/mp/extras.py                  # udostępnianie, feed.xml, llms.txt, SEO, karty „Powiązane”
python3 /tmp/mp/check.py                   # kontrola linków, mapy witryny, danych strukturalnych
python3 /tmp/mp/seo_audit.py               # frazy kluczowe w H1, wstępie i H2
```

## Najważniejsze pliki
- `build_all.py`, `build_more.py` — lista artykułów (tytuł, opis, kategoria, ikona, plik treści, powiązane, źródła).
- `gen.py` — szablon strony artykułu; `run_build.py` — budowanie wybranych artykułów.
- `add_index.py` — dodaje artykuł na stronę główną i do mapy witryny.
- `extras.py` — bloki „Udostępnij”, `feed.xml`, `llms.txt`; uruchamia `apply_seo.py` i `fix_related.py`.
- `seo_map.py` — frazy kluczowe, tytuły i opisy meta dla każdej strony.
- `make_tool.py` + `tool_*.py` — generatory kalkulatorów w `narzedzia/`.
- `gen_wyn.py` — strony „X zł brutto ile netto” w `wynagrodzenia/`; `gen_wyn_net.py` — strony „X zł netto ile brutto”.
- `add_tool_faq.py` — sekcje „Najczęstsze pytania” (z danymi FAQPage) w 4 kalkulatorach; uruchom ponownie po przebudowie kalkulatora skryptem `tool_*.py`.
- `add_author.py` — strona „O autorze”, podpis pod artykułami i autor (Person) w danych strukturalnych; działa, gdy obok skryptu leży `author.json` (`{"name": "…", "bio": ["…"], "role": "…"}`), bez niego nic nie robi.
- `redesign_home.py` + `home2.css` — górna część strony głównej (hasło, wyszukiwarka, mini-kalkulator „Ile na rękę?”, karty kalkulatorów, „Na czasie”, kwoty netto) i zwijanie kategorii. Uruchom po dodaniu kalkulatora lub artykułu, żeby odświeżyć liczniki; `home2.css` to końcowa część `style.css`.
- `add_toc.py`, `enrich_ld.py` — spis treści w artykułach, wspólne dane wydawcy i dane FAQPage z sekcji „Najczęstsze pytania” w artykułach; uruchamiane przez `extras.py`.
- `og_template.html` + `og_render.js` — grafiki 1200×630 do udostępniania (Playwright).
- `karuzele/` — slajdy 1080×1350 do mediów społecznościowych.
- `tresci/` — treść artykułów (HTML bez nagłówka i stopki).

Uwaga: po zmianie treści artykułu edytuj plik w `tresci/`, a nie gotową stronę w `artykuly/` — przebudowa nadpisuje gotowe strony. Wyjątkiem jest 14 starszych artykułów pisanych ręcznie (nie ma ich w `build_all.py`/`build_more.py`) — te edytuje się bezpośrednio w `artykuly/`.
