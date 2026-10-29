#!/usr/bin/env python3
"""static.html -> A4 PDF（MathJax→SVG + WeasyPrint）

用法:  python3 build_pdf.py <out.pdf> [work_dir] [頁尾文字]

前置:  pip install weasyprint --break-system-packages
       npm install mathjax-full --prefix /tmp/mj
       （沙盒無 Chromium，playwright 下載也會失敗，這是唯一可行路徑）

輸入為 prerender.py 產生的 <work_dir>/static.html。
"""
import re, json, subprocess, sys, os, html as htmllib

PDF = sys.argv[1]
WORK = sys.argv[2] if len(sys.argv) > 2 else '/tmp/pdfw'
FOOT = sys.argv[3] if len(sys.argv) > 3 else '公式 給／背分界　'
SRC = os.path.join(WORK, 'static.html')
HERE = os.path.dirname(os.path.abspath(__file__))

src = open(SRC, encoding='utf-8').read()

# --- 1. 抽數學式（保護 svg/style/script 區塊不被誤抓）---
PROTECT = re.compile(r'(<svg\b.*?</svg>|<style\b.*?</style>|<script\b.*?</script>)', re.S | re.I)
parts = PROTECT.split(src)
items = []


def stash(tex, display):
    # 關鍵：TeX 內的 < > & 在 HTML 原始碼中被跳脫過，不還原會被 MathJax 當成
    # 對齊字元而產生 merror，PDF 上顯示為一整塊黑方框
    items.append({'tex': htmllib.unescape(tex.strip()), 'display': display})
    return '\x00MJ%d\x00' % (len(items) - 1)


for i in range(0, len(parts), 2):
    parts[i] = re.sub(r'\$\$(.+?)\$\$', lambda m: stash(m.group(1), True), parts[i], flags=re.S)
    parts[i] = re.sub(r'\\\((.+?)\\\)', lambda m: stash(m.group(1), False), parts[i], flags=re.S)

json.dump(items, open(WORK + '/math_in.json', 'w'), ensure_ascii=False)
subprocess.run(['node', os.path.join(HERE, 'tex2svg.js'),
                WORK + '/math_in.json', WORK + '/math_out.json'], check=True)
rendered = json.load(open(WORK + '/math_out.json'))

# merror = TeX 語法錯，PDF 上會變成黑方框 —— 早點爆掉比印出來才發現好
if any('merror' in r for r in rendered):
    bad = [items[i]['tex'] for i, r in enumerate(rendered) if 'merror' in r]
    raise SystemExit('TeX 錯誤，請修正後重跑：' + repr(bad))

doc = ''.join(parts)
doc = re.sub(r'\x00MJ(\d+)\x00',
             lambda m: ('<div class="mjd">%s</div>' if items[int(m.group(1))]['display']
                        else '<span class="mji">%s</span>') % rendered[int(m.group(1))], doc)

# --- 2. 列印樣式 ---
doc = doc.replace('</head>', '''<style>
@page{size:A4;margin:14mm 12mm 15mm 12mm;
 @bottom-center{content:"''' + FOOT + '''" counter(page) " / " counter(pages);
 font-family:"Noto Sans CJK TC";font-size:8.2pt;color:#78909c}}
html,body{background:#fff!important;font-family:"Noto Sans CJK TC",sans-serif;font-size:9.8pt;line-height:1.58}
main{max-width:none;padding:0}
header{padding:16px 18px;border-radius:0}
header h1{font-size:16pt;line-height:1.35}header p{font-size:8.4pt}
section{margin-bottom:16px}
h2{font-size:13pt;margin:16px 0 8px;break-after:avoid}
h3{font-size:11pt;margin:14px 0 6px;break-after:avoid}
h3.grph{background:#eceff1;border-left:5px solid #1565c0;padding:5px 10px;border-radius:5px;
  color:#1565c0;margin:16px 0 9px;break-after:avoid}
p{margin:6px 0}p.lead{font-size:9.4pt}
.kpis{gap:8px}.kpi{padding:9px}.kpi .n{font-size:1.5em}.kpi .l{font-size:7.6pt}
.legend{gap:8px}.lg{padding:9px 11px;break-inside:avoid}.lg h4{font-size:9.4pt}.lg p{font-size:8pt}
.lg h4::before{content:"■　"}
.lg.must h4::before{color:#c62828}.lg.half h4::before{color:#ef6c00}.lg.give h4::before{color:#2e7d32}
.cards{gap:9px}
.fc{padding:10px 13px;break-inside:avoid;box-shadow:none}
.fc .top{margin-bottom:3px}.fc .nm{font-size:10pt}
.tag{font-size:7.4pt;padding:1px 8px;border:1px solid currentColor}
.fc .eq{padding:4px 9px;margin:4px 0}
.fc .meta{font-size:8.7pt;margin:4px 0 0;line-height:1.5}
.fc .ev{font-size:7.8pt;margin-top:6px;padding-top:5px}
.fc .ev .yr{padding:0 4px;margin:1px 1px 1px 0}
.fc .ev .never{color:#c62828;font-weight:700}
.note,.warn{padding:9px 13px;margin:10px 0;font-size:9pt;break-inside:avoid}
.tw{overflow:visible;border:none;background:none}
table{font-size:7.5pt;min-width:0!important;width:100%;table-layout:fixed}
th,td{padding:2.4px 3px;border-bottom:1px solid #e0e6ea;word-break:break-word}
th{position:static;font-size:7pt;line-height:1.2;text-align:center;background:#eceff1}
th:first-child,th:last-child{text-align:left}
thead{display:table-header-group}tr{break-inside:avoid}
tr.hl{background:#f2f7fc}
td.qq{font-size:7.1pt}td.rm{font-size:7pt;line-height:1.32}
td .y{font-size:8.5pt}
.ynote{font-size:7pt;color:#78909c}
.mjd{text-align:center;margin:5px 0;break-inside:avoid}
.mjd svg{max-width:100%;max-height:56px}
.mji svg{vertical-align:-0.22em;max-height:15px}
mjx-container{display:inline-block}
th .mjd,td .mjd{margin:0}th .mjd svg{max-height:20px}
footer{font-size:7.6pt;padding:10px 0 0;border-top:1px solid #e0e6ea;margin-top:14px}
#matrix{break-before:page}
#strategy{break-before:page}
</style></head>''')

open(WORK + '/print.html', 'w', encoding='utf-8').write(doc)
from weasyprint import HTML
HTML(filename=WORK + '/print.html', base_url=WORK).write_pdf(PDF)
print('PDF -> %s | math items: %d' % (PDF, len(items)))
