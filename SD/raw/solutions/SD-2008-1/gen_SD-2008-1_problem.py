#!/usr/bin/env python3
"""SD-2008-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2008-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2008-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2008-1"
# ── 判讀清單 #1–#4 ──
H, BW = 3.0, 4.0     # 樓高、跨度考卷未給，示意
def fig1():
    cv = fit(560, 480, (-1.6, 7.4), (-0.8, 7.2), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #4
    for i, (y, u) in enumerate(((2*H, "u_{1}（頂層）"), (H, "u_{2}"))):                           # #1 u1 在頂層
        cv.line((0, y), (BW, y), C["member"], 7, cap="butt"); cv.math((BW/2, y), "m", 17, C["text"], dy=-18)
        cv.arrow((BW+0.2, y), (BW+1.4, y), C["deform"], 2.6, 9); cv.text((BW+1.4, y), u, 15, C["deform"], "start", dx=6)
        cv.math((0, y - H/2), "k", 16, C["text"], "end", dx=-10)
    cv.text_px(280, 466, "m = 1500 kg（每層）；兩層側向勁度皆 k", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "u1 是頂層、u2 是下層（與習慣的由下往上編號相反）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
