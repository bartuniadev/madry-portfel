import html, re

def nb(t):
    t = re.sub(r'(\d) (\d{3})(?!\d)', '\\1\u00a0\\2', t)
    return re.sub(r'(\d) (zł|%|r\.)', '\\1\u00a0\\2', t)
OUT = __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '/'
LOGO = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><polyline points="7.5 13.5 10.5 10.5 13 12.5 16.5 8.5"/><polyline points="14 8.5 16.5 8.5 16.5 11"/></svg>'
SETS = {
    'zarobki': [
        ('hook', {'eyebrow': 'Dane GUS · maj 2026', 'title': 'Połowa Polaków zarabia mniej niż <em>7550 zł</em> brutto', 'sub': 'Sprawdź, gdzie jest Twoja pensja →'}),
        ('stat', {'eyebrow': 'Mediana a średnia', 'big': '65%', 'title': 'pracujących zarabia mniej niż „średnia krajowa”', 'sub': 'Średnią (9178 zł) zawyżają najwyższe pensje. Typową pensję lepiej pokazuje mediana: 7550 zł.'}),
        ('stat', {'eyebrow': 'Najmniej i najwięcej', 'big': '4806 zł', 'title': 'tyle co najwyżej zarabia 10% najmniej zarabiających', 'sub': 'A 10% najlepiej zarabiających dostaje co najmniej 14 239 zł brutto miesięcznie.'}),
        ('table', {'eyebrow': 'Ile to na rękę?', 'title': 'Progi płac w Polsce — brutto i netto',
                   'rows': [('10% zarabia do', '4806 zł', '3606 zł'), ('Mediana', '7550 zł', '5477 zł'), ('Średnia', '9178 zł', '6587 zł'), ('Top 10% od', '14 239 zł', '10 037 zł')],
                   'note': 'Umowa o pracę, PIT-2, bez PPK, osoba powyżej 26 lat.'}),
        ('cta', {'eyebrow': 'Za darmo · bez rejestracji', 'title': 'Ile procent Polaków zarabia mniej od Ciebie?', 'sub': 'Wpisz pensję w kalkulatorze „Czy dobrze zarabiam?” — wynik w 10 sekund.', 'link': 'bartuniadev.github.io/madry-portfel'}),
    ],
    'premia': [
        ('hook', {'eyebrow': 'Grudzień 2026', 'title': 'Premia świąteczna: ile z niej <em>naprawdę</em> zostanie?', 'sub': 'Przesuń, zanim wydasz ją w głowie →'}),
        ('table', {'eyebrow': 'Ile to na rękę?', 'title': 'Premia brutto i netto na umowie o pracę',
                   'rows': [('500 zł', '341 zł', '393 zł'), ('1000 zł', '681 zł', '785 zł'), ('2000 zł', '1363 zł', '1570 zł'), ('5000 zł', '3408 zł', '3926 zł')],
                   'note': 'Bez PPK. Do 26 lat — z ulgą dla młodych.', 'cols': ('Premia brutto', 'Na rękę', 'Do 26 lat')}),
        ('stat', {'eyebrow': 'Fundusz socjalny', 'big': '1000 zł', 'title': 'tyle rocznie z ZFŚS dostaniesz bez podatku', 'sub': 'Liczą się wszystkie świadczenia z funduszu w roku — paczka, bon, dopłata do wczasów.'}),
        ('stat', {'eyebrow': 'Sprytny ruch', 'big': 'IKZE', 'title': 'wpłata do 31 grudnia obniży podatek za 2026 rok', 'sub': 'Odzyskasz część podatku pobranego od premii w przyszłorocznym PIT.'}),
        ('cta', {'eyebrow': 'Za darmo · bez rejestracji', 'title': 'Policz swoją premię i pensję', 'sub': 'Tabela premii, zasady ZFŚS i kalkulator brutto–netto 2027.', 'link': 'bartuniadev.github.io/madry-portfel'}),
    ],
    'zmiany2027': [
        ('hook', {'eyebrow': 'Od 1 stycznia 2027', 'title': '5 zmian w Twoim portfelu od <em>nowego roku</em>', 'sub': 'Przesuń, żeby zobaczyć →'}),
        ('stat', {'eyebrow': '1 · Płaca minimalna', 'big': '4950 zł', 'title': 'brutto za pełny etat — ok. 3704 zł na rękę', 'sub': 'Na umowie zlecenia minimum to 32,30 zł brutto za godzinę.'}),
        ('stat', {'eyebrow': '2 · Konta emerytalne', 'big': '30 099 zł', 'title': 'tyle wpłacisz na IKE w 2027 roku', 'sub': 'Na IKZE — 12 039,60 zł, a wpłaty odliczysz od podatku.'}),
        ('stat', {'eyebrow': '3 · Nowe konto OKI', 'big': 'bez Belki', 'title': 'zyski na osobistym koncie inwestycyjnym bez 19% podatku', 'sub': 'Podatek 0,85% rocznie płaci się dopiero od majątku powyżej 100 000 zł.'}),
        ('stat', {'eyebrow': '4 · Dorabianie bez firmy', 'big': '11 137,50 zł', 'title': 'limit przychodu działalności nierejestrowanej na kwartał', 'sub': '225% płacy minimalnej — w 2026 r. było 10 813,50 zł.'}),
        ('stat', {'eyebrow': '5 · Konto a komornik', 'big': '3712,50 zł', 'title': 'miesięcznie na koncie jest wolne od zajęcia', 'sub': 'To 75% płacy minimalnej — tej kwoty komornik nie może zająć.'}),
        ('cta', {'eyebrow': 'Wszystkie zmiany i kalkulatory', 'title': 'Policz swoją pensję na 2027 rok', 'sub': 'Kalkulator brutto–netto 2027, kalkulator OKI i pełna lista zmian — za darmo, bez rejestracji.', 'link': 'bartuniadev.github.io/madry-portfel'}),
    ],
    'weekendy': [
        ('hook', {'eyebrow': 'Kalendarz 2027', 'title': '28 dni wolnego za <em>11 dni</em> urlopu', 'sub': 'Zapisz, zanim ktoś z zespołu zajmie te terminy →'}),
        ('table', {'eyebrow': 'Gdzie wziąć urlop', 'title': 'Najlepsze długie weekendy 2027',
                   'rows': [('1–10 stycznia', '4 dni', '10 dni'), ('27–30 maja', '1 dzień', '4 dni'), ('11–14 listopada', '1 dzień', '4 dni'), ('24.12–2.01.2028', '5 dni', '10 dni')],
                   'note': 'Urlop: 4–5 i 7–8 stycznia, 28 maja, 12 listopada, 27–31 grudnia.', 'cols': ('Wolne', 'Urlop', 'Razem')}),
        ('stat', {'eyebrow': 'Święta w sobotę', 'big': '2 dni', 'title': 'dodatkowego wolnego za 1 maja i 25 grudnia', 'sub': 'Oba święta wypadają w sobotę, więc pracodawca musi wyznaczyć Ci za każde inny dzień wolny.'}),
        ('stat', {'eyebrow': 'Długie weekendy za darmo', 'big': '5 razy', 'title': 'trzy dni wolnego pod rząd bez urlopu', 'sub': 'Nowy Rok (1–3.01), Wielkanoc (27⁠–⁠29.03), majówka (1–3.05), Wszystkich Świętych (30.10⁠–⁠1.11) i święta (24–26.12).'}),
        ('stat', {'eyebrow': 'Wymiar czasu pracy', 'big': '251 dni', 'title': 'pracy w 2027 roku — razem 2008 godzin', 'sub': 'Najkrótszy miesiąc to maj: 18 dni i 144 godziny.'}),
        ('cta', {'eyebrow': 'Pełny kalendarz za darmo', 'title': 'Ile dni urlopu masz w 2027?', 'sub': 'Kalendarz świąt, plan długich weekendów i kalkulator urlopu — bez rejestracji.', 'link': 'bartuniadev.github.io/madry-portfel'}),
    ],
    'niedziele': [
        ('hook', {'eyebrow': 'Grudzień 2026', 'title': '3 niedziele handlowe i <em>4 dni</em> bez sklepów', 'sub': 'Zapisz, zanim zaczniesz świąteczne zakupy →'}),
        ('table', {'eyebrow': 'Kiedy sklepy są otwarte', 'title': 'Niedziele handlowe przed świętami',
                   'rows': [('6 grudnia', 'niedziela', 'otwarte'), ('13 grudnia', 'niedziela', 'otwarte'), ('20 grudnia', 'niedziela', 'otwarte'), ('24–27 grudnia', 'czw–nd', 'zamknięte')],
                   'note': 'Wigilia jest dniem wolnym od pracy od 2025 r.', 'cols': ('Data', 'Dzień', 'Sklepy')}),
        ('stat', {'eyebrow': 'Cały 2027 rok', 'big': '8 niedziel', 'title': 'handlowych: 31.01, 21.03, 25.04, 27.06, 29.08 i 5, 12, 19.12', 'sub': 'Zawsze ostatnia niedziela stycznia, kwietnia, czerwca i sierpnia, niedziela przed Wielkanocą i trzy przed Wigilią.'}),
        ('cta', {'eyebrow': 'Licznik dni i pełna lista', 'title': 'Kiedy najbliższa niedziela handlowa?', 'sub': 'Sprawdzisz w kalendarzu niedziel handlowych 2026 i 2027 — z poradami, jak nie przepłacić przed świętami.', 'link': 'bartuniadev.github.io/madry-portfel'}),
    ],
}
CSS = '''
@import url("file:///home/user/madry-portfel/assets/fonts/fonts.css");
*{box-sizing:border-box} body{margin:0;background:#ddd}
.slide{width:1080px;height:1350px;position:relative;overflow:hidden;background:#faf9f6;color:#14261c;font-family:"Inter",system-ui,sans-serif;display:flex;flex-direction:column;padding:96px 92px 80px}
.slide.dark{background:#14261c;color:#f3f1ea}
.bg{position:absolute;inset:0;background:radial-gradient(900px 700px at 110% 105%, #cfe8d8 0%, rgba(207,232,216,0) 60%);pointer-events:none}
.dark .bg{background:radial-gradient(900px 700px at 110% 105%, rgba(58,216,137,.25) 0%, rgba(58,216,137,0) 60%)}
.eyebrow{position:relative;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:30px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:#1f7a4d}
.dark .eyebrow{color:#7fe3b0}
.body{position:relative;flex:1;display:flex;flex-direction:column;justify-content:center;gap:34px}
h1,h2,.sub{text-wrap:balance}
h1{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:96px;line-height:1.04;margin:0;letter-spacing:-.015em}
h1 em{font-style:normal;color:#7fe3b0}
h2{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:62px;line-height:1.12;margin:0}
.big{font-family:"Fraunces",Georgia,serif;font-weight:600;font-size:150px;line-height:1;color:#1f7a4d;letter-spacing:-.02em}
.sub{font-size:40px;line-height:1.4;color:#4d5d55;max-width:880px}
.dark .sub{color:#c9d3cd}
table{border-collapse:collapse;width:100%;font-size:42px}
th{font-size:28px;text-transform:uppercase;letter-spacing:.06em;color:#6b7a72;text-align:right;padding:0 0 18px;font-weight:600}
th:first-child{text-align:left}
td{padding:26px 0;border-top:2px solid #d9e3dc;text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
td:first-child{text-align:left;font-weight:500}
tr.hl td{color:#1f7a4d}
.note{font-size:30px;color:#6b7a72}
.link{display:inline-block;font-size:40px;font-weight:700;background:#3ad889;color:#08130d;border-radius:18px;padding:22px 32px;align-self:flex-start}
.foot{position:relative;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:16px;font-family:"Fraunces",Georgia,serif;font-size:42px;color:#145c39;font-weight:500}
.dark .brand{color:#f3f1ea}
.brand svg{width:48px;height:48px;color:#1f7a4d}
.dark .brand svg{color:#7fe3b0}
.count{font-size:30px;color:#6b7a72;font-variant-numeric:tabular-nums}
.dark .count{color:#9fb0a7}
'''


def slide(kind, d, i, n):
    d = {k: (nb(v) if isinstance(v, str) else [tuple(nb(x) for x in r) for r in v] if isinstance(v, list) else v) for k, v in d.items()}
    dark = kind in ('hook', 'cta')
    e = '<div class="eyebrow">' + html.escape(d['eyebrow']) + '</div>'
    if kind == 'hook':
        b = '<h1>' + d['title'] + '</h1><div class="sub">' + html.escape(d['sub']) + '</div>'
    elif kind == 'stat':
        b = '<div class="big">' + html.escape(d['big']) + '</div><h2>' + html.escape(d['title']) + '</h2><div class="sub">' + html.escape(d['sub']) + '</div>'
    elif kind == 'table':
        rows = ''.join('<tr' + (' class="hl"' if r[0] in ('Mediana', '1000 zł') else '') + '><td>' + html.escape(r[0]) + '</td><td>' + html.escape(r[1]) + '</td><td>' + html.escape(r[2]) + '</td></tr>' for r in d['rows'])
        b = '<h2>' + html.escape(d['title']) + '</h2><table><thead><tr>' + ''.join('<th>' + html.escape(c) + '</th>' for c in d.get('cols', ('Próg', 'Brutto', 'Na rękę'))) + '</tr></thead><tbody>' + rows + '</tbody></table><div class="note">' + html.escape(d['note']) + '</div>'
    else:
        b = '<h1 style="font-size:88px">' + html.escape(d['title']) + '</h1><div class="sub">' + html.escape(d['sub']) + '</div><div class="link">' + html.escape(d['link']) + '</div>'
    return ('<section class="slide' + (' dark' if dark else '') + '"><div class="bg"></div>' + e + '<div class="body">' + b +
            '</div><div class="foot"><div class="brand">' + LOGO + 'Mądry Portfel</div><div class="count">' + str(i) + ' / ' + str(n) + '</div></div></section>')


for name, slides in SETS.items():
    doc = ('<!doctype html><html lang="pl"><head><meta charset="utf-8"><style>' + CSS + '</style></head><body>' +
           ''.join(slide(k, d, i + 1, len(slides)) for i, (k, d) in enumerate(slides)) + '</body></html>')
    open(OUT + name + '.html', 'w').write(doc)
print('ok')
