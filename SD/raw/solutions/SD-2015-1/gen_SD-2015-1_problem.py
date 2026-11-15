#!/usr/bin/env python3
"""SD-2015-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2015-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2015-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2015-1"
def fig1():
    cv = fit(620, 330, (-0.6, 8.6), (-1.2, 3.6), L=20, R=20, T=20, B=20)
    ground(cv, (0, 3.2), (0, -0.3))                                               # 左牆（剖線朝左）
    cv.line((0, -0.3), (8.3, -0.3), C["member"], 3.0)
    for i in range(24):
        bx = 0.2 + i*0.34; cv.line((bx, -0.3), (bx - 0.25, -0.6), C["member"], 1.4)
    dashpot(cv, (0, 2.2), (4.2, 2.2), wd=0.18); cv.math((2.3, 2.2), "c", 16, C["text"], dy=-22)          # #1
    spring(cv, (0, 1.2), (4.2, 1.2), n=6, amp=0.16); cv.math((2.1, 1.2), "k", 16, C["text"], dy=22)
    cv.polygon([(4.2, 0.45), (6.4, 0.45), (6.4, 2.6), (4.2, 2.6)], "none", C["member"], 2.2)
    cv.math((5.3, 1.55), "m", 17, C["text"])
    for x in (4.75, 5.85): cv.circle((x, 0.075), 0.37, "none", C["member"], 2.0)
    cv.arrow((6.4, 1.8), (8.0, 1.8), C["load"], 2.6, 10); cv.text((6.5, 0.9), "p(t) = P_{0} sin ω̄t", 13.5, C["load"], "start")   # #2
    cv.arrow((6.6, 3.2), (8.0, 3.2), C["deform"], 2.2, 9); cv.math((7.3, 3.2), "v", 15, C["deform"], dy=-12)          # #3
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "彈簧與阻尼器並聯接固定牆；外力直接作用於質塊（非支承激振）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
