# usage: python add_index.py  (reads entries from stdin as python list of dicts)
import sys, re, os, ast
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
import build_all as B
try:
    import build_more as M; B.ICON.update(M.ICON)
except ImportError: pass
root='/home/user/madry-portfel/'
entries=ast.literal_eval(sys.stdin.read())
s=open(root+'index.html').read(); m=open(root+'sitemap.xml').read()
for e in entries:
    if f'artykuly/{e["slug"]}.html"' in s: continue
    html=f'''      <li>
        <div class="icon-badge"><svg class="topic-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{B.ICON[e["icon"]]}</svg></div>
        <div class="article-body">
          <a href="artykuly/{e["slug"]}.html">{e["title"]}<span class="badge-new">Nowość</span></a>
          <p>{e["desc"]}</p>
        </div>
      </li>
'''
    i=s.index(f'id="{e["cat"]}"')
    mm=re.compile(r'<span class="category-count">\((\d+)\)</span>').search(s,i)
    s=s[:mm.start()]+f'<span class="category-count">({int(mm.group(1))+1})</span>'+s[mm.end():]
    j=s.index('<ul class="article-list">\n',i)+len('<ul class="article-list">\n')
    if e.get('last'):
        j=s.index('    </ul>',j)
    s=s[:j]+html+s[j:]
    m=m.replace('</urlset>',f'  <url><loc>https://bartuniadev.github.io/madry-portfel/artykuly/{e["slug"]}.html</loc><lastmod>2026-11-16</lastmod></url>\n</urlset>')
open(root+'index.html','w').write(s); open(root+'sitemap.xml','w').write(m)
print('index updated')
