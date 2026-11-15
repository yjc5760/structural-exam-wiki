#!/usr/bin/env python3
"""SD-2016-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2016-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2016-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2016-1"
H, BW = 2.4, 3.6           # 樓高、跨度考卷未給，示意
P0, T1, TD = 2.4e5, 0.1, 0.2   # #4 外力歷時
def fig1():
    cv = fit(820, 380, (-1.8, 15.6), (-1.2, 6.4), L=20, R=20, T=20, B=20)
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt")
    ground(cv, (-0.6, 0), (BW + 0.6, 0))                                            # #7
    for y, ml, kl, vl in ((H, "2m", "2k", "v_{1}"), (2*H, "m", "k", "v_{2}")):      # #2 #3
        cv.polygon([(0, y - 0.18), (BW, y - 0.18), (BW, y + 0.18), (0, y + 0.18)], "#C9CED6", C["member"], 1.8)
        cv.math((BW/2, y), ml, 16, C["text"], dy=-22)
        cv.math((BW, y - H/2), kl, 16, C["text"], "start", dx=10)
        cv.arrow((BW + 0.2, y), (BW + 1.5, y), C["deform"], 2.2, 9, dash="5 4"); cv.math((BW + 1.5, y), vl, 15, C["deform"], "start", dx=6)
    cv.arrow((-1.6, 2*H), (-0.02, 2*H), C["load"], 3.0, 10); cv.math((-1.2, 2*H), "p(t)", 15, C["load"], dy=-16)   # #1 只作用在頂層
    # 外力歷時（考卷給的三角形脈衝，非讀圖數據）
    ox, sx, sy = 8.0, 30.0, 4.0/P0
    cv.arrow((ox, 0), (ox + TD*sx + 1.2, 0), C["muted"], 1.6, 8); cv.arrow((ox, 0), (ox, 5.2), C["muted"], 1.6, 8)
    cv.polygon([(ox, 0), (ox + T1*sx, P0*sy), (ox + TD*sx, 0)], C["fill_t"], C["load"], 2.2)
    cv.line((ox, P0*sy), (ox + T1*sx, P0*sy), C["dim"], 1, dash="3 3")
    cv.text((ox, P0*sy), "2.4×10^{5}", 13, C["text"], "end", dx=-6)
    for t in (T1, TD): cv.text((ox + t*sx, 0), f"{t:g}", 13, C["text"], dy=16)
    cv.text((ox, 5.2), "p(t)  N", 13, C["text"], "start", dx=8); cv.text((ox + TD*sx + 1.2, 0), "t (s)", 13, C["text"], "start", dx=4)
    cv.text_px(410, 366, "m = 2×10^{3} kg，k = 10^{5} N/m；外力只作用在頂層樓版", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "底層 2m／2k、頂層 m／k；p(t) 只作用在頂層；三角形脈衝 0.2 s、峰值在 0.1 s")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
