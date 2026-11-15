#!/usr/bin/env python3
"""SD-2004-5：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2004-5-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2004-5_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2004-5"
# ── 判讀清單 #1–#4 ──
MASS = [5000, 4000, 3000]   # #1 由下而上 u1、u2、u3
H = 3.0; BW = 4.0; K = 4e6  # #2 #3
def fig1():
    cv = fit(640, 520, (-3.0, 8.4), (-0.6, 9.8), L=20, R=20, T=20, B=20)
    ground(cv, (-0.6, 0), (BW+0.6, 0))
    for i, m in enumerate(MASS):
        y0, y1 = i*H, (i+1)*H
        for x in (0, BW): cv.line((x, y0), (x, y1-0.12), C["member"], 2.6, cap="butt")
        cv.polygon([(-0.15, y1-0.15), (BW+0.15, y1-0.15), (BW+0.15, y1+0.15), (-0.15, y1+0.15)], "#D5DAE1", C["member"], 1.6)
        cv.text((BW/2, y1), f"m{i+1} = {m} kg", 15, C["text"], dy=-22)
        cv.arrow((BW+0.3, y1), (BW+1.5, y1), C["deform"], 2.4, 9); cv.math((BW+1.5, y1), f"u_{{{i+1}}}", 16, C["deform"], "start", dx=6)
        cv.dim((-0.9, y0), (-0.9, y1), "3 m", off=0, label_off=22)
        cv.math((BW, (y0+y1)/2), "k = 4×10^{6} N/m", 12.5, C["muted"], "start", dx=8)
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "樓版質量由上往下排反（頂層是 3000 kg）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
