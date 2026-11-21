# Generates share blocks (idempotent), feed.xml and llms.txt from the current site files.
import re, glob, html, json, os
# apply SEO metadata first, so feed.xml and llms.txt read final descriptions
import subprocess as _sp0, sys as _sys0, os as _os0
_sp0.run([_sys0.executable, _os0.path.join(_os0.path.dirname(_os0.path.abspath(__file__)),'apply_seo.py')], check=True, stdout=_sp0.DEVNULL)
from urllib.parse import quote
from email.utils import format_datetime
from datetime import datetime, timezone
root='/home/user/madry-portfel/'; BASE='https://bartuniadev.github.io/madry-portfel/'
os.chdir(root)

def share_html(url, title):
    u=quote(url, safe=''); t=quote(title, safe='')
    return f'''  <div class="share" data-url="{url}" data-title="{html.escape(title)}">
    <p class="share-title">Przyda się komuś? Podeślij ten poradnik</p>
    <div class="share-links">
      <button type="button" data-share-native hidden>Udostępnij</button>
      <button type="button" data-share-copy>Kopiuj link</button>
      <a href="https://wa.me/?text={t}%20{u}" rel="noopener" target="_blank">WhatsApp</a>
      <a href="https://www.facebook.com/sharer/sharer.php?u={u}" rel="noopener" target="_blank">Facebook</a>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url={u}" rel="noopener" target="_blank">LinkedIn</a>
      <a href="https://twitter.com/intent/tweet?url={u}&amp;text={t}" rel="noopener" target="_blank">X</a>
    </div>
    <p class="share-note" aria-live="polite"></p>
  </div>

'''

arts=[]
for f in sorted(glob.glob('artykuly/*.html')):
    t=open(f).read()
    title=html.unescape(re.search(r'<h1>(.*?)</h1>',t,re.S).group(1).strip())
    desc=html.unescape(re.search(r'<meta name="description" content="([^"]*)">',t).group(1))
    date=re.search(r'"datePublished": "([0-9-]+)"',t).group(1)
    cat=html.unescape(re.search(r'<a href="\.\./index\.html#[a-z-]+">([^<]+)</a>',t).group(1))
    url=BASE+f
    arts.append(dict(f=f,title=title,desc=desc,date=date,cat=cat,url=url))
    # share block + script (idempotent)
    if 'class="share"' not in t:
        anchor='  <section class="sources">' if '<section class="sources">' in t else '  <section class="related-articles'
        t=t.replace(anchor, share_html(url,title)+anchor,1)
    if 'assets/share.js' not in t:
        t=t.replace('<script defer src="../assets/stats.js"></script>\n','<script defer src="../assets/stats.js"></script>\n<script defer src="../assets/share.js"></script>\n',1)
    open(f,'w').write(t)

# RSS feed (newest first)
arts_sorted=sorted(arts,key=lambda a:(a['date'],a['f']),reverse=True)
def rfc(d): return format_datetime(datetime.strptime(d,'%Y-%m-%d').replace(hour=8,tzinfo=timezone.utc))
items=''.join(f'''  <item>
    <title>{html.escape(a["title"])}</title>
    <link>{a["url"]}</link>
    <guid isPermaLink="true">{a["url"]}</guid>
    <pubDate>{rfc(a["date"])}</pubDate>
    <category>{html.escape(a["cat"])}</category>
    <description>{html.escape(a["desc"])}</description>
  </item>
''' for a in arts_sorted)
feed=f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Mądry Portfel — finanse dla młodych na starcie kariery</title>
  <link>{BASE}</link>
  <atom:link href="{BASE}feed.xml" rel="self" type="application/rss+xml"/>
  <description>Poradniki o pensji, podatkach, oszczędzaniu, kredytach i inwestowaniu dla osób, które dopiero zaczynają zarabiać.</description>
  <language>pl-PL</language>
  <lastBuildDate>{rfc(arts_sorted[0]["date"])}</lastBuildDate>
{items}</channel>
</rss>
'''
open('feed.xml','w').write(feed)

# llms.txt grouped like the homepage
s=open('index.html').read()
by={a['f']:a for a in arts}
out=['# Mądry Portfel','',
 '> Darmowy serwis edukacyjny o finansach osobistych w Polsce dla młodych osób na starcie kariery: pensja i podatki (PIT, ulga dla młodych), budżet, oszczędzanie, kredyty i długi, mieszkanie, inwestowanie i emerytura (IKE, IKZE, PPK, ETF, obligacje skarbowe), prawa pracownika. Kwoty i limity według stanu na 2026 r., z linkami do źródeł urzędowych przy każdym artykule.','',
 'Treści mają charakter edukacyjny i nie są doradztwem finansowym. Serwis nie sprzedaje produktów finansowych, nie wyświetla reklam i nie używa plików cookies.','']
for sec in re.finditer(r'<section class="category-section reveal" id="([a-z-]+)">\s*<h[23] class="category-title">([^<]+)<span',s):
    cid,cname=sec.group(1),sec.group(2).strip()
    block=s[sec.end():s.index('</section>',sec.end())]
    links=re.findall(r'href="(artykuly/[^"]+\.html)"',block)
    out.append(f'## {cname}'); out.append('')
    for l in links:
        a=by[l]; out.append(f'- [{a["title"]}]({a["url"]}): {a["desc"]}')
    out.append('')
out += ['## Kalkulatory','',
 f'- [Czy dobrze zarabiam?]({BASE}narzedzia/czy-dobrze-zarabiam.html): pensja brutto lub netto na tle rozkładu wynagrodzeń GUS (maj 2026) — jaki procent pracujących zarabia mniej.',
 f'- [Kalkulator wynagrodzeń brutto–netto 2026 i 2027]({BASE}narzedzia/kalkulator-brutto-netto.html): umowa o pracę, ulga dla młodych, PIT-2, PPK, wypłata w każdym miesiącu roku z progiem podatkowym i limitem składek ZUS.',
 f'- [Kalkulator budżetu 50/30/20]({BASE}narzedzia/kalkulator-budzetu.html): podział dochodu netto na potrzeby, zachcianki i oszczędności.',
 f'- [Kalkulator procentu składanego]({BASE}narzedzia/kalkulator-procentu-skladanego.html): wpłaty miesięczne, podatek Belki, wartość po inflacji.',
 f'- [Kalkulator spłaty długów]({BASE}narzedzia/kalkulator-splaty-dlugow.html): porównanie metody lawiny i kuli śnieżnej.',
 f'- [Kalkulator OKI]({BASE}narzedzia/kalkulator-oki.html): osobiste konto inwestycyjne (od 2027 r.) w porównaniu ze zwykłym rachunkiem i IKE — podatek Belki kontra podatek od aktywów.',
 f'- [Kalkulator umowy zlecenia]({BASE}narzedzia/kalkulator-umowy-zlecenia.html): ile na rękę ze zlecenia dla studenta do 26 lat, przy jedynej pracy i obok etatu; minimalna stawka godzinowa 2026 i 2027.',
 f'- [Kalkulator lokaty]({BASE}narzedzia/kalkulator-lokaty.html): zysk z lokaty i konta oszczędnościowego po podatku Belki i inflacji, z odnawianiem lokaty.',
 f'- [Kalkulator kredytu]({BASE}narzedzia/kalkulator-kredytu.html): rata równa i malejąca, odsetki, RRSO z prowizją i efekt nadpłat.',
 f'- [Kalkulator poduszki finansowej]({BASE}narzedzia/kalkulator-poduszki-finansowej.html): ile odłożyć na czarną godzinę (3–6+ miesięcy niezbędnych wydatków) i w jakim czasie.',
 f'- [Kalkulator inflacji]({BASE}narzedzia/kalkulator-inflacji.html): ile dziś trzeba mieć, żeby kupić to samo co w danym roku, według średniorocznej inflacji GUS od 2000 r.',
 f'- [Kalkulator urlopu]({BASE}narzedzia/kalkulator-urlopu.html): ile dni urlopu wypoczynkowego przysługuje (20 lub 26 dni, staż ze szkołą), urlop przy pierwszej pracy i zmianie pracy, niepełny etat, ekwiwalent za niewykorzystany urlop.',
 f'- [Porównanie ofert pracy]({BASE}narzedzia/porownanie-ofert-pracy.html): dwie oferty obok siebie — netto na etacie lub zleceniu, PPK, benefity, koszt i czas dojazdu, bezpłatny urlop na zleceniu; która jest realnie warta więcej.',
 f'- [Podział kosztów w związku]({BASE}narzedzia/kalkulator-podzialu-kosztow.html): po równo, proporcjonalnie do dochodów lub równe kieszonkowe — wkład na wspólne konto i co zostaje każdemu.','',
 '## Ile na rękę — popularne kwoty','',
 *[f'- [{g} zł brutto ile netto]({BASE}wynagrodzenia/{g}-brutto-ile-netto.html): wyliczenie netto na umowie o pracę i zleceniu, koszt pracodawcy, pozycja na tle zarobków GUS.' for g in [5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,11000,12000,13000,14000,15000,16000,18000,20000]],
 *[f'- [{n} zł netto ile brutto]({BASE}wynagrodzenia/{n}-netto-ile-brutto.html): ile brutto potrzeba, żeby dostać tę kwotę na rękę na umowie o pracę i zleceniu.' for n in [4000,4500,5000,5500,6000,6500,7000,7500,8000,9000,10000,12000]],'',
 '## Pomocnicze','',
 f'- [Najczęstsze pytania o finanse]({BASE}pytania.html): krótkie odpowiedzi z odesłaniem do poradników.',
 f'- [Słownik pojęć finansowych]({BASE}slownik.html): definicje ponad 75 pojęć, od brutto i netto po RRSO i ETF.',
 f'- [Jak powstają treści]({BASE}jak-powstaja-tresci.html): źródła danych, sposób liczenia kalkulatorów, coroczne aktualizacje i zgłaszanie błędów.',
 f'- [O serwisie]({BASE}o-nas.html): zasady redakcyjne i kontakt.','']
open('llms.txt','w').write('\n'.join(out))
print('articles',len(arts),'| feed items',feed.count('<item>'),'| llms lines',len(out))

# Per-page share images (og:image / twitter:image / JSON-LD image) — always point to the page's own image
pages={}
for f in glob.glob('artykuly/*.html')+glob.glob('narzedzia/kalkulator-*.html'):
    pages[f]=os.path.basename(f)[:-5]
pages.update({'narzedzia/index.html':'narzedzia','pytania.html':'pytania','slownik.html':'slownik'})
IMG_RE=r'https://bartuniadev\.github\.io/madry-portfel/(?:og-image\.png|assets/og/[a-z0-9-]+\.jpg)'
n=0
for f,slug in pages.items():
    img=f'assets/og/{slug}.jpg'
    if not os.path.exists(img): continue
    t=open(f).read(); o=t
    t=re.sub(r'(<meta property="og:image" content=")'+IMG_RE+'"', r'\g<1>'+BASE+img+'"', t)
    t=re.sub(r'(<meta name="twitter:image" content=")'+IMG_RE+'"', r'\g<1>'+BASE+img+'"', t)
    t=re.sub(r'("image": ")'+IMG_RE+'"', r'\g<1>'+BASE+img+'"', t)
    if 'og:image:width' not in t:
        t=re.sub(r'(<meta property="og:image" content="[^"]+">\n)', r'\1<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n', t, count=1)
    if t!=o: open(f,'w').write(t); n+=1
print('og images wired:', n)

# SEO titles/descriptions/keywords — must run after every rebuild
import subprocess as _sp, sys as _sys
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'apply_seo.py')], check=True)
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'fix_related.py')], check=True)
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'add_toc.py')], check=True)
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'add_author.py')], check=True)
_sp.run([_sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)),'enrich_ld.py')], check=True)
