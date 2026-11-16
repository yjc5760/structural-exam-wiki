#!/usr/bin/env python3
"""SD-2002-2：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G1）
幾何、支承、載重逐項對應題目正本 SD-2002-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2002-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2002-2"
L = 10.0
def fig1():
    cv = fit(640, 300, (-1.0, 13.6), (-2.2, 2.4), L=20, R=20, T=20, B=40)
    cv.line((0, 0), (L, 0), C["member"], 6, cap="butt")                         # #7 梁 m, EI
    cv.support((0, 0), "pin"); cv.support((L, 0), "roller")                     # #4 簡支
    bw, bh = 1.0, 1.1
    cv.polygon([(L/2-bw/2, 0.12), (L/2+bw/2, 0.12), (L/2+bw/2, 0.12+bh), (L/2-bw/2, 0.12+bh)], "#FFFFFF", C["member"], 2.0)
    cv.math((L/2, 0.12+bh/2), "M", 16)                                          # #3 跨中集中質量
    cv.math((7.6, 0.75), "m, EI", 15)                                           # #7
    cv.arrow((12.6, 0), (L+0.12, 0), C["load"], 3.0, 11); cv.math((12.6, 0), "N", 16, C["load"], "start", dx=8)  # #5 軸壓
    cv.dim((0, -1.25), (L/2, -1.25), "L/2"); cv.dim((L/2, -1.25), (L, -1.25), "L/2")  # #6
    cv.text_px(320, 285, "簡支梁；M 在跨中（L/2）；右端（滾支承端）受軸向壓力 N", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "M 在跨中、N 為壓力作用於滾支承端")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
