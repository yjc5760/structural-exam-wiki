#!/usr/bin/env python3
"""SD-2024-2：題目附圖（橋梁斷面簡化模型）重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G3）
幾何、彈簧、自由度、外力逐項對應題目正本 SD-2024-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
左半新聞照片不重繪（照片非結構圖）。
用法：python3 gen_SD-2024-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2024-2"
L, T = 8.0, 0.22               # 彈簧間距 L（考卷只給符號）、桿厚示意
def fig1():
    cv = fit(640, 400, (-1.4, L + 1.4), (-3.2, 2.9), L=20, R=20, T=20, B=20)
    cv.polygon([(0, -T/2), (L, -T/2), (L, T/2), (0, T/2)], "#E4E7EC", C["member"], 2.2)   # #7 剛性桿
    cv.line((-0.5, 0), (L + 0.5, 0), C["member2"], 1.0, dash="10 4 2 4")
    cv.text((L*0.28, T/2), "Rigid bar", 13, C["muted"], dy=-34)
    cv.line((L*0.27, T/2 + 0.5), (L*0.24, T/2), C["muted"], 1.0)
    cv.text((L*0.74, T/2), "m（沿桿均勻分布）", 13, C["text"], dy=-28)                         # #1
    for x, k in ((0, "k_{1}"), (L, "k_{2}")):                                             # #5
        spring(cv, (x, -T/2), (x, -1.6)); ground(cv, (x - 0.6, -1.6), (x + 0.6, -1.6), n=5)
        cv.math((x, -0.9), k, 15, C["text"], "start", dx=16)
    for x, u in ((0, "u_{1}"), (L, "u_{2}")):                                             # #4 向上
        cv.arrow((x, T/2 + 0.2), (x, T/2 + 1.4), C["deform"], 2.4, 9)
        cv.math((x, T/2 + 1.4), u, 15, C["deform"], "start", dx=6, dy=4)
    cv.arrow((L/2, T/2), (L/2, T/2 + 1.6), C["load"], 2.8, 10)                            # #3 p_t 向上
    cv.math((L/2, T/2 + 1.6), "p_{t}", 15, C["load"], "start", dx=6, dy=4)
    cv.moment_arrow((L/2, 0), r=24, ccw=True, color=C["load"], start=-80, span=230)       # #2 p_θ 逆時針
    cv.math((L/2, 0), "p_{θ}", 15, C["load"], "end", dx=-30, dy=-26)
    cv.dim((0, -1.6), (L/2, -1.6), "L/2", off=42)                                        # #6
    cv.dim((L/2, -1.6), (L, -1.6), "L/2", off=42)
    cv.text_px(320, 388, "u1、u2、p_t 向上為正；p_θ 作用於中點、逆時針為正", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "p_θ 逆時針、m 沿桿均勻分布、外力作用於中點")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
