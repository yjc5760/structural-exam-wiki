#!/usr/bin/env python3
"""SD-2012-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2012-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2012-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2012-1"
H, BW, GAP = 3.0, 4.0, 2.4   # 樓高、跨度考卷未給，示意
def frame(cv, x0, mlab, Tlab):
    for x in (x0, x0 + BW):
        cv.line((x, 0), (x, H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #5
    cv.line((x0, H), (x0 + BW, H), C["member"], 7, cap="butt")
    cv.math((x0 + BW/2, H), mlab, 18, C["text"], dy=-18)
    cv.math((x0, H/2), "k", 17, C["text"], "end", dx=-10)
    cv.text((x0 + BW/2, -0.9), Tlab, 13.5, C["text"])
def fig1():
    cv = fit(660, 330, (-1.0, 2*BW + GAP + 0.6), (-1.4, H + 0.9), L=20, R=20, T=20, B=20)
    frame(cv, 0, "m_{1}", "圖一(a)　T = 1.2 s")                                     # #3
    frame(cv, BW + GAP, "m_{2}", "圖一(b)　T = 1.4 s")
    cv.text_px(330, 316, "m_{2} = m_{1} + 1806 kg；兩者 k 與阻尼比（5%）相同", 12.5, C["muted"])  # #2
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "兩屋架只差質量 1806 kg，k 與阻尼比不變")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
