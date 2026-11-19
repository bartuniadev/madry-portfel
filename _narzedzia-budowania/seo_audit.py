import sys, re, html, os
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
from seo_map import SEO
root='/home/user/madry-portfel/'
def norm(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).lower()
def stems(kw):
    out=[]
    for w in re.findall(r'[\wąćęłńóśźż/%+-]+', kw.lower()):
        if w.isdigit() or len(w)<=2: continue
        if len(w)<=3: out.append(w); continue
        out.append(w[:max(4,len(w)-2)])
    return out
def has(text,kw): return all(s in text for s in stems(kw))
miss={'h1':[],'intro':[],'h2':[]}
for k,(kw,sec,ti,de) in SEO.items():
    if not k.startswith('artykuly/'): continue
    t=open(root+k+'.html').read()
    h1=norm(re.search(r'<h1>(.*?)</h1>',t,re.S).group(1))
    m=re.search(r'<p class="meta">.*?</p>(.*?)<h2',t,re.S)
    intro=norm(m.group(1)) if m else ''
    h2=' | '.join(norm(x) for x in re.findall(r'<h2>(.*?)</h2>',t,re.S) if 'Powiązane' not in x and 'Źródła' not in x)
    if not has(h1,kw): miss['h1'].append((k[9:],kw))
    if not has(intro,kw): miss['intro'].append((k[9:],kw))
    if not any(has(h2,s) for s in [kw]+sec): miss['h2'].append((k[9:],kw))
for key,v in miss.items():
    print(f'--- brak frazy w {key}: {len(v)}')
    for x in v: print('   ',x)
