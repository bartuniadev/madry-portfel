import sys, os, importlib
S=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,S)
import gen, build_all as B
extra = []
if os.path.exists(S+'/build_more.py'):
    import build_more; extra = build_more.ARTICLES; B.ICON.update(getattr(build_more,'ICON',{}))
arts = B.ARTICLES + extra
only = set(sys.argv[1:])
# two passes so related_from can read articles generated in this run
for _ in range(2):
    for a in arts:
        if only and a['slug'] not in only: continue
        try: rel = gen.related_from(a['related'])
        except FileNotFoundError: rel = ''
        gen.build(a['slug'], a['title'], a['desc'], B.CAT[a['cat']], a['cat'], B.ICON[a['icon']], a['hero'], B.rd(a['body']), rel, a.get('sources'))
print('built', len(arts) if not only else len(only))
