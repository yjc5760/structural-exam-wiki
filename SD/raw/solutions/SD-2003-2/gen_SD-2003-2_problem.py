#!/usr/bin/env python3
"""SD-2003-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2003-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2003-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-2"
# ── 判讀清單 #1–#6 ── 外力歷時折線（s, N）
TA, TB, TC, TD, PMAX, PMIN = 0.10, 0.12, 0.20, 0.25, 2000.0, -500.0
SLOPE = PMIN / (TB - TA)              # #1 下降段斜率 = −25000 N/s（ta、tb、−500N 決定）
TP = TA - PMAX / (-SLOPE)             # #1 峰值時刻 = 0.02 s（由直線推得，考卷未標）
PTS = [(0, 0), (TP, PMAX), (TA, 0), (TB, PMIN), (TC, PMIN), (TD, 0), (0.30, 0)]
def fig1():
    XS, YS = 2400.0, 0.12             # 1 s → 2400 單位；1 N → 0.12 單位（只用於版面）
    P = lambda t, p: (t*XS, p*YS)
    cv = fit(760, 470, (-60, 760), (-110, 290), L=40, R=30, T=30, B=40)
    cv.arrow(P(0, 0), P(0.31, 0), C["muted"], 1.8, 9); cv.arrow(P(0, PMIN*1.4), P(0, PMAX*1.15), C["muted"], 1.8, 9)
    cv.math(P(0.31, 0), "t (s)", 15, C["muted"], "start", dx=6); cv.math(P(0, PMAX*1.15), "P(t) (N)", 15, C["muted"], "start", dx=8)
    cv.poly([P(t, p) for t, p in PTS], C["load"], 3.0)
    for t in (TB, TC): cv.line(P(t, 0), P(t, PMIN), C["dim"], 1.2, dash="4 4")
    cv.line(P(TP, 0), P(TP, PMAX), C["accent"], 1.4, dash="4 4")
    cv.text(P(TP, PMAX), "2000 N", 14, C["text"], dy=-14)
    cv.text(P(TC, PMIN), "−500 N", 14, C["text"], "start", dy=16, dx=-40)
    for t, s, dx, dy, an in ((TA, "t_{a} = 0.10", -18, -14, "end"), (TB, "t_{b} = 0.12", 8, 16, "start"), (TC, "t_{c} = 0.20", 0, -16, "middle"), (TD, "t_{d} = 0.25", 0, -16, "middle")):
        cv.math(P(t, 0), s, 13.5, C["text"], an, dx=dx, dy=dy)
    cv.text(P(TP, 0), "0.02（推得）", 13, C["accent"], "middle", dy=16)
    cv.text_px(400, 452, "下降段為同一直線：斜率 −25000 N/s，ta 為零交點、tb 達 −500 N；t > td 為自由振動", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "把 ta 讀成峰值時刻（峰值實在約 0.02 s，ta 是零交點）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
