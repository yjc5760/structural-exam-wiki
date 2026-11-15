#!/usr/bin/env python3
"""SD-2024-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何、支承、載重逐項對應題目正本 SD-2024-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2024-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2024-1"
H, BW = 1.0, 2.0                       # #6 樓高 h、跨度 2h（以 h 為單位）
def fig1():
    cv = fit(620, 560, (-1.6, 3.4), (-0.75, 3.45), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, 3*H), C["member"], 2.6, cap="butt"); cv.support((x, 0), "fixed")   # #5 柱底固定
        for i in range(3):
            cv.math((x, (i + 0.5)*H), "EI", 14, C["text"], "start" if x else "end", dx=8 if x else -8)  # 每層兩柱 EI
    for i, ml in enumerate(("m", "m", "m/2")):
        y = (i + 1)*H
        cv.line((0, y), (BW, y), C["member"], 4.0, cap="butt")                                # #1 剛性梁
        cv.circle((BW/2, y), 0.09 if i < 2 else 0.065, "#D0D4DA", C["member"], 1.8)            # #2 質量
        cv.math((BW/2, y), ml, 14, C["text"], dy=-22)
        cv.arrow((-0.9, y), (-0.03, y), C["load"], 2.6, 9)                                     # #3 外力 p_i(t)
        cv.math((-0.9, y), "p_{%d}(t)" % (i + 1), 14, C["load"], "end", dx=-6)
    cv.line((BW*0.7, 3*H), (BW*0.85, 3*H + 0.25), C["muted"], 1.2)
    cv.text((BW*0.86, 3*H + 0.3), "Rigid beams", 13, C["muted"], "start")
    for i in range(3):                                                                         # #6 樓高 h
        cv.dim((-1.35, i*H), (-1.35, (i + 1)*H), "h", 0)
    cv.dim((0, -0.45), (BW, -0.45), "2h", 0)                                                   # #6 跨度 2h
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "頂層質量 m/2、每層兩柱 EI、剛性梁柱底固定（層勁度 24EI/h³）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
