#!/usr/bin/env python3
"""SD-2007-3：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2007-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2007-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2007-3"
# ── 判讀清單 #1–#3 ──
def fig1():
    cv = fit(720, 360, (-2.6, 7.6), (-1.6, 2.2), L=20, R=20, T=20, B=20)
    wx = 0.0; ground(cv, (wx, 1.5), (wx, -0.9))                       # 固定牆（剖線在左）
    mx0, mx1 = 3.2, 4.4
    cv.polygon([(mx0, -0.8), (mx1, -0.8), (mx1, 1.4), (mx0, 1.4)], "#D5DAE1", C["member"], 2.4); cv.math(((mx0+mx1)/2, 0.3), "m", 18, C["text"])
    spring(cv, (wx, 0.9), (mx0, 0.9), amp=0.16); cv.math((mx0/2, 0.9), "k", 16, C["text"], dy=-20)        # #1
    dashpot(cv, (wx, -0.3), (mx0, -0.3), wd=0.2); cv.math((mx0/2, -0.3), "c", 16, C["text"], dy=24)
    cv.arrow((mx1, 0.3), (mx1+1.8, 0.3), C["load"], 2.8, 10); cv.math((mx1+0.15, 0.3), "p(t) = p_{0} sin Ωt", 15, C["load"], "start", dy=-20)  # #2
    cv.arrow((wx-0.2, 0.3), (wx-1.6, 0.3), C["muted"], 2.2, 9); cv.math((wx-1.6, 0.3), "R", 16, C["muted"], dy=-16)  # #3
    cv.line((mx0, -1.25), (mx0, -1.05), C["deform"], 1.6); cv.arrow((mx0, -1.15), (mx0+1.2, -1.15), C["deform"], 2.2, 8)
    cv.math((mx0+1.2, -1.15), "u", 16, C["deform"], "start", dx=6)
    cv.text_px(360, 346, "㈢㈣不考慮阻尼；R 為支承反力（各小題未問）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "外力直接作用在質量上（不是支承運動）；R 是反力不是外力")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
