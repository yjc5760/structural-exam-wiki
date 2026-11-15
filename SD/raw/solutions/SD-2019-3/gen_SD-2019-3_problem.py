#!/usr/bin/env python3
"""SD-2019-3：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
只重繪左圖（兩層構架）；右圖反應譜為曲線圖，不重繪（重繪等於自己編數據）。
幾何逐項對應題目正本 SD-2019-3-problem.md §4 判讀清單（註解中的 #n）。
用法：python3 gen_SD-2019-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2019-3"
H, BW, T = 2.6, 4.0, 0.3
def slab(cv, y):
    cv.polygon([(0, y - T/2), (BW, y - T/2), (BW, y + T/2), (0, y + T/2)], "#E4E7EC", C["member"], 2.0)
def fig1():
    cv = fit(560, 420, (-1.0, 8.6), (-1.6, 6.0), L=20, R=20, T=20, B=20)
    ground(cv, (-0.6, 0), (BW + 0.6, 0))
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt")
    for y, ul in ((H, "u_{1}"), (2*H, "u_{2}")):
        slab(cv, y); cv.text((BW/2, y - 0.6), "m = 5×10⁴ kg", 14, C["text"])           # #4
        cv.arrow((BW, y), (BW + 1.4, y), C["deform"], 2.4, 9, dash="6 4"); cv.math((BW + 1.4, y), ul, 15, C["deform"], "start", dx=6)   # #3
    cv.text((BW/2, -0.9), "φ_{1} = {0.5, 1.0}（依 u_{1}、u_{2}）；週期 1.0 s", 14, C["text"])   # #2 #3
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "φ1 分量依 u1（二樓）、u2（屋頂）排列；兩層質量相同")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
