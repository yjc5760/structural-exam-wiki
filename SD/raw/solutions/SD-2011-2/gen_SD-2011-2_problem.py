#!/usr/bin/env python3
"""SD-2011-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2011-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2011-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2011-2"
Lw, A0 = 6.0, 0.35          # 路面波長、振幅：符號題，比例示意（#5）
def fig1():
    cv = fit(620, 470, (-3.6, 4.4), (-1.6, 5.4), L=20, R=20, T=20, B=20)
    # 路面 u_g(x) = u_g0 sin(2πx/L)（#5）
    xs = [-3.4 + 7.6*i/120 for i in range(121)]
    cv.poly([(x, A0*math.sin(2*math.pi*x/Lw)) for x in xs], C["member"], 2.4)
    cv.arrow((-3.4, -1.1), (4.3, -1.1), C["muted"], 1.8, 9); cv.math((4.3, -1.1), "x", 15, C["muted"], "start", dx=6)
    yc = A0*math.sin(0) ; r = 0.28
    cv.circle((0, yc + r), r, "none", C["member"], 2.2)                         # #2 車輪貼地
    cv.line((0, yc + 2*r), (0, 1.2), C["member"], 2.2)
    cv.line((-0.9, 1.2), (0.9, 1.2), C["member"], 5, cap="butt")
    spring(cv, (-0.45, 1.25), (-0.45, 2.9), n=6, amp=0.16)                      # #4 k、c 並聯
    dashpot(cv, (0.45, 1.25), (0.45, 2.9), wd=0.14)
    cv.math((-0.45, 2.05), "k", 16, C["text"], "end", dx=-14); cv.math((0.45, 2.05), "c", 16, C["text"], "start", dx=14)
    cv.polygon([(-1.2, 2.9), (1.2, 2.9), (1.2, 4.3), (-1.2, 4.3)], "#D9DDE3", C["member"], 2.2)
    cv.math((0, 3.6), "m", 18, C["text"])
    cv.arrow((1.9, 3.6), (1.9, 5.1), C["deform"], 2.6, 9); cv.math((1.9, 5.1), "u^{t}", 16, C["deform"], "start", dx=8)   # #1
    cv.arrow((1.25, 3.6), (3.6, 3.6), C["load"], 2.2, 9, dash="6 4"); cv.math((3.6, 3.6), "v", 16, C["load"], "start", dx=6)  # #3
    cv.arrow((0.0, -1.1), (0.0, yc - 0.02), C["deform"], 1.8, 8)
    cv.text((0.15, -0.65), "u_{g}(x) = u_{g0} sin(2πx/L)", 13.5, C["text"], "start")
    cv.text_px(310, 455, "路面高程隨 x 起伏；車以等速 v 行駛（x = vt）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "u^t 是質塊垂直總位移；激振來自彈簧阻尼下端隨路面高程移動")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
