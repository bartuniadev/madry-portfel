import re,glob,os,json,sys
os.chdir('/home/user/madry-portfel')
s=open('index.html').read(); m=open('sitemap.xml').read(); bad=[]
badge='<span class="badge-new">Nowość</span>'
if len(sys.argv)>1:
    s=s.replace(badge,'')
    for slug in sys.argv[1:]:
        i=s.index(f'href="artykuly/{slug}.html">'); j=s.index('</a>',i); s=s[:j]+badge+s[j:]
    open('index.html','w').write(s)
for f in glob.glob('*.html')+glob.glob('*/*.html'):
    if f.startswith('_'): continue
    t=open(f).read()
    for h in re.findall(r'(?:href|src)="([^"#]+)',t):
        if h.startswith(('http','mailto')): continue
        p=('/home/user/madry-portfel/'+h[len('/madry-portfel/'):]) if h.startswith('/madry-portfel/') else os.path.normpath(os.path.join(os.path.dirname(f),h))
        if not os.path.exists(p): bad.append((f,h))
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
        try: json.loads(blk)
        except Exception: bad.append((f,'jsonld'))
    for mm in re.finditer(r'<meta [^>]*content="([^"]*)"([^>]*)>',t):
        if mm.group(2).strip(): bad.append((f,'meta'))
    if f not in ('google054b00c069a6f4cf.html','404.html','polityka-prywatnosci.html') and f.replace('\\','/') not in m and not f.startswith('google'): bad.append((f,'not in sitemap'))
for a in glob.glob('artykuly/*.html'):
    if a not in s: bad.append((a,'not on home'))
    if 'class="sources"' not in open(a).read(): bad.append((a,'no sources'))
print(bad or 'all checks ok','| articles',len(glob.glob('artykuly/*.html')),'| counts',re.findall(r'category-count">\((\d+)\)',s),'| sitemap',m.count('<loc>'),'| badges',s.count(badge))
# share images must point to the page's own image
for f in glob.glob('artykuly/*.html'):
    slug=os.path.basename(f)[:-5]; t=open(f).read()
    for m_ in re.findall(r'(?:og:image" content|twitter:image" content|"image": )"([^"]+)"',t):
        if not m_.endswith(f'/assets/og/{slug}.jpg'): print('OG MISMATCH',f,m_[-40:])
