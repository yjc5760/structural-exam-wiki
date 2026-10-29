# -*- coding: utf-8 -*-
"""重新內嵌圖解：python3 refresh_figs.py ../../lecture-SS-U1-3.html
依 SVG 的 aria-label（「圖N-M …」）比對講義中同名的內嵌 SVG 並整段替換。
修改圖時：改 gen_figs.py → python3 gen_figs.py → python3 refresh_figs.py <講義>。"""
import sys, os, re, glob
here = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1]
html = open(path, encoding="utf-8").read()
n = 0
for f in sorted(glob.glob(os.path.join(here, "fig-*.svg"))):
    svg = open(f, encoding="utf-8").read()
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S).replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")  # 去除外部工具附加的中繼資料
    tag = re.search(r'aria-label="(圖\d+-\d+)', svg).group(1)
    pat = re.compile(r'<svg\b[^>]*aria-label="' + re.escape(tag) + r'[ "].*?</svg>', re.S)
    html, k = pat.subn(lambda m: svg, html)
    assert k == 1, (tag, k)
    n += k
open(path, "w", encoding="utf-8").write(html)
print(f"replaced {n} figures in {path}")
