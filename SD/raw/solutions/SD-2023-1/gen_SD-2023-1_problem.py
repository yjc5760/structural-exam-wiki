#!/usr/bin/env python3
"""SD-2023-1：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G3）
幾何、支承、載重逐項對應題目正本 SD-2023-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2023-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2023-1"
L, T = 8.0, 0.3                 # 跨度 L（考卷只給符號）、梁厚示意
def fig1():
    cv = fit(640, 330, (-0.8, L + 0.8), (-2.0, 2.6), L=20, R=20, T=20, B=20)
    cv.polygon([(0, 0), (L, 0), (L, T), (0, T)], "#D5DAE1", C["member"], 2.2)      # #5 均質等斷面 EI、m̄
    cv.support((0, 0), "pin"); cv.support((L, 0), "roller")                        # #2 左鉸右滾
    cv.arrow((L/2, T + 1.6), (L/2, T), C["load"], 3.0, 11)                         # #4 中點向下
    cv.math((L/2, T + 1.6), "P(t)", 16, C["load"], dy=-12)
    cv.math((L/2, T), "EI, m̄", 14, C["text"], "start", dx=60, dy=-14)
    cv.dim((0, 0), (L, 0), "L", off=78)                                           # #3 支承中心→支承中心
    cv.dim((0, 0), (L/2, 0), "L/2", off=40, size=12)                              # #4 中點
    cv.text_px(320, 318, "簡支梁，均質等斷面；P(t) 作用於跨中、鉛垂向下", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "左鉸右滾、P(t) 在跨中")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
