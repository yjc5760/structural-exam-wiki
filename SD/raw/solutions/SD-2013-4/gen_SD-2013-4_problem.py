#!/usr/bin/env python3
"""SD-2013-4：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2013-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2013-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2013-4"
HS = [15.0, 30.0, 40.0]       # #2 節點高度（由地面量起）
def fig1():
    cv = fit(620, 600, (-14, 34), (-7, 45), L=20, R=20, T=20, B=20)
    wb, wt = 3.0, 1.2
    cv.line((-wb/2, 0), (-wt/2, 40), C["member"], 2.4); cv.line((wb/2, 0), (wt/2, 40), C["member"], 2.4)
    cv.line((-wt/2, 40), (wt/2, 40), C["member"], 2.4)
    ground(cv, (-6, 0), (6, 0))                                                    # #6 固定
    for h in HS:
        cv.circle((0, h), 2.0, "#D9DDE3", C["member"], 2.2)                        # 集中質量（大小考卷未給，#1）
    prev = 0
    for h in HS:
        cv.dim((8, prev), (8, h), f"{h-prev:g} m", off=0, label_off=-20); prev = h
    cv.arrow((3, -3.2), (-5, -3.2), C["load"], 2.6, 10)                            # #5
    cv.math((-1, -5.6), "v̈_{g} = A sin ω̄t", 15, C["load"])
    x0 = 15
    cv.text((x0, 30), "ω_{1} = 5.0 rad/s，ω_{2} = 12.0 rad/s", 13.5, C["text"], "start")  # #4
    cv.text((x0, 25.5), "振態    (1)      (2)", 13.5, C["text"], "start")
    for i, (h, a, b) in enumerate(((40, "1.00", "1.00"), (30, "0.5", "−0.8"), (15, "0.25", "−0.6"))):   # #3 列序：頂→下
        y = 22 - 3.4*i
        cv.text((x0, y), f"{h:g} m 節點", 13, C["muted"], "start")
        cv.text((x0 + 8.4, y), a, 13.5, C["text"], "end"); cv.text((x0 + 14.2, y), b, 13.5, C["text"], "end")
    cv.text((x0, 9.0), "A = 1.5 m/s^{2}，ω̄ = 8 rad/s", 13.5, C["text"], "start")
    cv.text((x0, 5.6), "塔台單位長度重量 10 Tf/m", 13.5, C["text"], "start")
    cv.text((x0, 2.2), "忽略阻尼，只取前兩振態穩態反應", 12.5, C["muted"], "start")
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "三個集中質量在 15／30／40 m；Φ 第一列是塔頂；考卷只給單位長度重量，未給各節點質量")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
