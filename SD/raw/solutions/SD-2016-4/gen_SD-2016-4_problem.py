#!/usr/bin/env python3
"""SD-2016-4：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2016-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2016-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2016-4"
H, BW = 2.2, 3.6           # 樓高、跨度考卷未給，示意
def fig1():
    cv = fit(520, 470, (-2.0, 7.0), (-2.0, 7.4), L=20, R=20, T=20, B=20)
    for x in (0, BW): cv.line((x, 0), (x, 3*H), C["member"], 2.4, cap="butt")
    ground(cv, (-0.6, 0), (BW + 0.6, 0))                                             # #8
    for j, (ml, vl) in enumerate((("m", "v_{1}"), ("m", "v_{2}"), ("m/2", "v_{3}"))):  # #2 #4
        y = (j + 1)*H
        cv.polygon([(0, y - 0.16), (BW, y - 0.16), (BW, y + 0.16), (0, y + 0.16)], "#C9CED6", C["member"], 1.6)
        cv.math((BW/2, y), ml, 16, C["text"], dy=-20)
        cv.math((0, y - H/2), "k", 16, C["text"], "end", dx=-10)                         # #3
        cv.arrow((BW + 0.2, y), (BW + 1.4, y), C["deform"], 2.2, 9, dash="5 4"); cv.math((BW + 1.4, y), vl, 15, C["deform"], "start", dx=6)
    cv.double_arrow((0.6, -1.0), (3.0, -1.0), C["load"], 2.2, 9); cv.text((1.8, -1.6), "地表加速度", 13, C["load"])
    cv.text_px(260, 455, "k = 1.15×10^{6} N/m（各層總勁度），m = 5×10^{3} kg", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "頂層質量是 m/2；三層勁度都是 k；自由度由下往上 v1、v2、v3")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
