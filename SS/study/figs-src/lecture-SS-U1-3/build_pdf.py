# -*- coding: utf-8 -*-
"""Chromium 列印 PDF：python3 build_pdf.py <src.html（須位於 study/ 以取用 assets/katex）> <out.pdf> "<頁尾文字>" """
import sys, re, os, asyncio
from playwright.async_api import async_playwright
SRC, PDF, FOOT = sys.argv[1], sys.argv[2], sys.argv[3]
doc = open(SRC, encoding="utf-8").read()
doc = re.sub(r"<nav>.*?</nav>", "", doc, flags=re.S)
doc = (doc.replace("<details>", '<div class="det">').replace("</details>", "</div>")
          .replace("<summary>", '<p class="sum">').replace("</summary>", "</p>"))
doc = doc.replace("</head>", """<style>
@page{size:A4;margin:14mm 13mm 16mm 13mm}
html,body{background:#fff!important;font-family:"Microsoft JhengHei","Noto Sans CJK TC",sans-serif;font-size:10.2pt;line-height:1.62}
main{max-width:none;padding:0}
header{padding:20px 22px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
header h1{font-size:19pt}header .sub{font-size:10pt}header .meta{font-size:8.5pt}
*{-webkit-print-color-adjust:exact;print-color-adjust:exact}
section{margin-bottom:20px}
h2{font-size:14pt;margin:20px 0 10px;break-after:avoid}
h3{font-size:11.6pt;margin:15px 0 6px;break-after:avoid}
h4{font-size:10.6pt;break-after:avoid}
table{font-size:8.9pt}th,td{padding:4px 6px}
tr{break-inside:avoid}
.fig,.why,.trap,.tens,.comp,.box,.lead{break-inside:avoid}
.fig{padding:10px 8px 6px;margin:12px 0}.fig .cap{font-size:8.6pt}
.why,.trap,.tens,.comp,.lead{padding:9px 13px;margin:11px 0;font-size:9.8pt}
.det{background:#fff;border:1px solid #dfe6ea;border-radius:8px;padding:8px 12px;margin:8px 0;break-inside:avoid}
.sum{font-weight:600;color:#1565c0;margin:0 0 4px}
.det p{border-left:3px solid #e0e0e0;padding-left:10px;color:#455a64;font-size:9.6pt}
footer{font-size:8.5pt;padding:14px}
</style></head>""")
tmp = os.path.join(os.path.dirname(os.path.abspath(SRC)), "_print_tmp.html")
open(tmp, "w", encoding="utf-8").write(doc)


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        await pg.goto("file://" + tmp)
        await pg.wait_for_function("document.querySelectorAll('.katex').length > 50", timeout=30000)
        await pg.wait_for_timeout(800)
        await pg.pdf(path=PDF, format="A4", print_background=True, display_header_footer=True,
                     header_template="<span></span>",
                     footer_template=f'<div style="width:100%;text-align:center;font-size:8px;color:#78909c;font-family:Noto Sans CJK TC">{FOOT}　<span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                     margin=dict(top="14mm", bottom="16mm", left="13mm", right="13mm"))
        await b.close()
asyncio.run(main())
os.remove(tmp)
print("PDF ->", PDF)
