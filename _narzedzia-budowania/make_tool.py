# Builds a calculator page in narzedzia/ from the compound-interest calculator template.
# usage (import): make_tool.build(slug, title, desc, app_name, keywords, crumb, main_html, script_js, extra_css='')
import re
ROOT = '/home/user/madry-portfel/'
TPL = ROOT + 'narzedzia/kalkulator-procentu-skladanego.html'

COMMON_CSS = '''  .type-toggle{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px;}
  .type-toggle label{position:relative;cursor:pointer;}
  .type-toggle input{position:absolute;opacity:0;width:1px;height:1px;}
  .type-toggle span{display:block;padding:8px 14px;border-radius:999px;border:1px solid var(--border);font-size:0.88rem;color:var(--text-2);background:var(--bg);}
  .type-toggle input:checked + span{background:var(--green);border-color:var(--green);color:#08130d;font-weight:700;}
  .type-toggle input:focus-visible + span{outline:2px solid var(--green);outline-offset:2px;}
  .net-box{display:flex;flex-direction:column;gap:2px;margin:10px 0 16px;padding:16px 18px;background:var(--bg);border:1px solid var(--green);border-radius:10px;}
  .net-box .label{font-size:0.85rem;color:var(--text-2);}
  .net-box .pct{font-size:0.8rem;color:var(--text-2);}
  .net-amount{font-family:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;font-weight:700;font-size:clamp(1.7rem,7vw,2.3rem);color:var(--green);font-variant-numeric:tabular-nums;}
  .breakdown{width:100%;border-collapse:collapse;margin:0 0 20px;font-size:0.92rem;}
  .breakdown td{padding:9px 4px;border-bottom:1px solid var(--border);}
  .breakdown td:last-child{text-align:right;white-space:nowrap;font-family:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;font-variant-numeric:tabular-nums;}
  .breakdown tr.total td{border-bottom:0;font-weight:700;color:var(--green);}
  .verdict{margin:4px 0 18px;padding:14px 16px;border:1px solid var(--green);border-radius:10px;background:var(--bg);font-size:0.95rem;}
  .verdict.worse{border-color:var(--gold);}
  details.tbl{margin:18px 0 0;border:1px solid var(--border);border-radius:9px;background:var(--bg);}
  details.tbl summary{cursor:pointer;padding:12px 14px;font-weight:600;font-size:0.92rem;}
  details.tbl summary:focus-visible{outline:2px solid var(--green);outline-offset:2px;}
  .tbl-wrap{overflow-x:auto;}
  .data-table{width:100%;border-collapse:collapse;font-size:0.85rem;}
  .data-table th,.data-table td{padding:7px 6px;border-top:1px solid var(--border);text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums;}
  .data-table th{color:var(--text-2);font-weight:600;font-size:0.78rem;}
  .data-table th:first-child,.data-table td:first-child{text-align:left;}
  .data-table caption{caption-side:bottom;text-align:left;padding:8px 10px 10px;font-size:0.75rem;color:var(--text-2);}
  @media (max-width:380px){.data-table th,.data-table td{padding:7px 4px;font-size:0.78rem;}}
  .more-link{line-height:2.2;}
  [hidden]{display:none !important;}
'''


def build(slug, title, desc, app_name, keywords, crumb, h1, lead, main_inner, trust, more_links, script_js, extra_css=''):
    src = open(TPL).read()
    head_end = src.index('<style>')
    style_end = src.index('</style>') + len('</style>')
    main_start = src.index('<main>')
    footer_start = src.index('<footer>')
    script_start = src.index('<script>\n', footer_start)
    head = src[:head_end]
    style = src[head_end:style_end]
    between = src[style_end:main_start]
    footer = src[footer_start:script_start]

    head = head.replace('kalkulator-procentu-skladanego.html', slug + '.html').replace(
        'assets/og/kalkulator-procentu-skladanego.jpg', 'assets/og/' + slug + '.jpg')
    head = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', head)
    for a in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
        head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + desc, head)
    for a in ['property="og:title"', 'name="twitter:title"']:
        head = re.sub(r'(<meta ' + a + r' content=")[^"]*', lambda m: m.group(1) + title, head)
    head = head.replace('"name": "Kalkulator procentu składanego"', '"name": "' + app_name + '"')
    head = re.sub(r'"description": "[^"]*"', '"description": "' + desc + '"', head)
    head = re.sub(r'"keywords": "[^"]*"', '"keywords": "' + keywords + '"', head)
    assert 'procentu' not in head
    style = style.replace('</style>', COMMON_CSS + extra_css + '</style>')

    main = f'''<main>
  <nav class="breadcrumb-dark" aria-label="Okruszki"><a href="../index.html">Mądry Portfel</a> <span aria-hidden="true">/</span> <a href="index.html">Narzędzia</a> <span aria-hidden="true">/</span> <span aria-current="page">{crumb}</span></nav>
  <span class="pill">0 kont · 0 maila · 0 ciasteczek</span>
  <h1>{h1}</h1>
  <p class="lead">{lead}</p>

  <div class="calc-card">
{main_inner}
  </div>

  <div class="trust">
    <p><strong>Jak to liczymy:</strong> {trust}</p>
    <a class="download-btn" href="{slug}.html" download="{slug}-madry-portfel.html">Pobierz i używaj offline (HTML)</a>
    <p class="microcopy">To zwykła strona HTML bez makr i bez ciasteczek. <a href="https://github.com/bartuniadev/madry-portfel/blob/master/narzedzia/{slug}.html">Zobacz kod źródłowy na GitHub</a>.</p>
  </div>

  <p class="more-link">{more_links}</p>
</main>

'''
    script = '<script>\n' + script_js + '\n</script>\n<script defer src="../assets/stats.js"></script>\n</body>\n</html>\n'
    out = head + style + between + main + footer + script
    open(ROOT + 'narzedzia/' + slug + '.html', 'w').write(out)
    return len(out)
