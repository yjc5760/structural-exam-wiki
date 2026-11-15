#!/usr/bin/env python3
"""SD-2015-3：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2015-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2015-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2015-3"
N_SHOW = 10; DH = 1.0       # 示意樓層數與樓高（N 為符號）
def fig1():
    cv = fit(560, 620, (-5.0, 7.2), (-2.4, 12.4), L=20, R=20, T=20, B=20)
    BWd = 1.6
    cv.line((-BWd/2, 0), (-BWd/2, N_SHOW*DH), C["member"], 2.0); cv.line((BWd/2, 0), (BWd/2, N_SHOW*DH), C["member"], 2.0)
    for j in range(1, N_SHOW + 1): cv.line((-BWd/2, j*DH), (BWd/2, j*DH), C["member"], 2.6)
    ground(cv, (-1.6, 0), (1.6, 0))                                                  # #5 固定
    cv.poly([(0, 0)] + [(0.25*(j/N_SHOW)*N_SHOW*0.4, j*DH) for j in range(1, N_SHOW + 1)], C["deform"], 1.8, dash="6 4")  # 第一振態示意
    labs = {1: "m_{1}", 2: "m_{2}", 3: "m_{3}", 6: "m_{i}", N_SHOW: "m_{N}"}
    for j, s in labs.items(): cv.math((BWd/2, j*DH), s, 14, C["text"], "start", dx=8)
    cv.dim((3.2, 0), (3.2, 6*DH), "h_{i}", off=0, label_off=-16)                       # #3
    cv.dim((5.2, 0), (5.2, N_SHOW*DH), "H", off=0, label_off=-14)
    cv.line((-4.0, -1.6), (-4.0, 11.6), C["muted"], 1.4); cv.text((-3.9, 11.9), "Reference axis", 12, C["muted"], "start")
    cv.double_arrow((-4.0, -1.5), (0.0, -1.5), C["deform"], 1.6, 8); cv.line((0, -0.1), (0, -1.8), C["deform"], 1.2); cv.math((-2.0, -1.5), "v_{g}(t)", 13, C["deform"], dy=13)   # #4 參考軸→構架中心線的尺寸
    cv.arrow((-4.0, 6*DH + 0.35), (0.8, 6*DH + 0.35), C["deform"], 1.6, 8); cv.math((-1.6, 6*DH + 0.35), "v_{i}^{t}(t)", 13, C["deform"], dy=-11)
    cv.arrow((0, 6*DH - 0.3), (0.62, 6*DH - 0.3), C["deform"], 1.4, 6); cv.math((1.05, 6*DH - 0.85), "v_{i}(t)", 12, C["deform"], "start")
    cv.arrow((1.6, -0.7), (-0.6, -0.7), C["load"], 2.2, 8); cv.math((2.2, -0.7), "U_{0}(t)", 13, C["load"], "start")
    cv.arrow((0, N_SHOW*DH), (0, N_SHOW*DH + 1.4), C["muted"], 1.6, 8); cv.math((0, N_SHOW*DH + 1.4), "x", 13, C["muted"], "start", dx=6)
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "h_i、H 都由地面量起；v_i 為相對位移、v_i^t 為對參考軸的總位移")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
