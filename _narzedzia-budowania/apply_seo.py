# Applies the keyword map: <title>, meta/OG/Twitter title+description, JSON-LD description+keywords.
import sys, re, html, os, json
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
from seo_map import SEO
root='/home/user/madry-portfel/'
def esc(s): return html.escape(s, quote=True)
changed=0
for k,(kw,sec,ti,de) in SEO.items():
    f=root+k+'.html'; t=open(f).read(); o=t
    t=re.sub(r'<title>.*?</title>', '<title>'+esc(ti)+'</title>', t, count=1, flags=re.S)
    for attr,val in [('name="description"',de),('property="og:description"',de),('name="twitter:description"',de),('property="og:title"',ti),('name="twitter:title"',ti)]:
        t=re.sub(r'(<meta '+attr+r' content=")[^"]*(")', lambda m: m.group(1)+esc(val)+m.group(2), t, count=1)
    kws=', '.join([kw]+sec)
    def fix_ld(m):
        try: d=json.loads(m.group(1))
        except Exception: return m.group(0)
        nodes=d.get('@graph',[d])
        touched=False
        for n in nodes:
            if n.get('@type') in ('Article','WebApplication'):
                n['description']=de; n['keywords']=kws; touched=True
        if not touched: return m.group(0)
        return '<script type="application/ld+json">\n'+json.dumps(d,ensure_ascii=False,indent=2)+'\n</script>'
    t=re.sub(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', fix_ld, t, flags=re.S)
    if t!=o: open(f,'w').write(t); changed+=1
print('seo applied to', changed, 'pages')
