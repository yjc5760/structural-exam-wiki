#!/usr/bin/env python3
"""SD-2010-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2010-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2010-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2010-2"
L, H = 6.0, 1.2      # 梁長、落下高度：符號題，比例示意（#4 #6）
def fig1():
    cv = fit(620, 330, (-0.9, L + 1.6), (-1.6, H + 1.0), L=20, R=20, T=20, B=20)
    cv.line((0, 0), (L, 0), C["member"], 4, cap="butt")                       # #7 EI 常數
    cv.support((0, 0), "fixed", 90, 26)                                        # #5 A 固定
    cv.math((L/2, 0), "EI", 17, C["text"], dy=-16)
    cv.text((0, 0), "A", 16, C["text"], "start", dx=6, dy=18); cv.text((L, 0), "B（自由）", 15, C["text"], "end", dy=18)
    bw = 0.7
    cv.poly([(L - bw/2, H), (L + bw/2, H), (L + bw/2, H + 0.6), (L - bw/2, H + 0.6), (L - bw/2, H)], C["load"], 2.4)
    cv.math((L, H + 0.3), "m", 18, C["load"])
    cv.arrow((L - 0.75, H + 0.45), (L - 0.75, 0.25), C["load"], 2.2, 9, dash="5 4")   # #3 由靜止自由落下
    cv.text((L - 0.85, H*0.55), "輕輕放開", 12.5, C["load"], "end")
    cv.dim((L + 0.75, 0), (L + 0.75, H), "h", off=0, label_off=-14)            # #4 h：方塊底面到 B
    cv.dim((0, -0.9), (L, -0.9), "L", off=0, label_off=14)                      # #6
    cv.text_px(310, 318, "梁質量不計；落到 B 點後與梁一起振動", 12.5, C["muted"])  # #2 #7
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "h 是方塊底面到梁頂的高度；B 為自由端、A 固定")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
