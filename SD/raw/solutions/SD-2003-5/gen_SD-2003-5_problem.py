#!/usr/bin/env python3
"""SD-2003-5：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2003-5-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2003-5_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-5"
# ── 判讀清單 #1–#5 ──
K = [5e6, 5e6, 3e6, 3e6, 3e6]        # #1 樓層勁度（兩柱各 k_i/2）
DELTA = [6, 5.6, 8, 6, 3.333]        # #3 層間變位 mm（題給）
M = 5000                              # #5
H, BW = 1.0, 1.6
def fig1():
    cv = fit(760, 600, (-1.0, 6.4), (-0.3, 5.5), L=20, R=20, T=20, B=20)
    ground(cv, (-0.4, 0), (BW+0.4, 0))
    for i in range(5):
        y0, y1 = i*H, (i+1)*H
        for x in (0, BW): cv.line((x, y0), (x, y1-0.05), C["member"], 2.6, cap="butt")
        cv.polygon([(-0.12, y1-0.07), (BW+0.12, y1-0.07), (BW+0.12, y1+0.07), (-0.12, y1+0.07)], "#D5DAE1", C["member"], 1.6)
        cv.math((0, (y0+y1)/2), f"k_{{{i+1}}}/2", 13, C["text"], "end", dx=-8)
        cv.math((BW, (y0+y1)/2), f"k_{{{i+1}}}/2", 13, C["text"], "start", dx=8)
        cv.math((BW/2, y1), f"m_{{{i+1}}}", 14, C["text"], dy=-16)
        cv.text((BW+0.75, (y0+y1)/2), f"k_{{{i+1}}} = {K[i]/1e6:g}×10^{{6}} N/m，δ_{{{i+1}}} = {DELTA[i]:g} mm", 13, C["deform"], "start")
    cv.text_px(380, 588, f"各層 m = {M} kg；δ 為層間變位（不是樓層位移）", 13, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "把 k_i/2 當成樓層勁度、把層間變位當成樓層位移")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
