#!/usr/bin/env python3
"""SD-2017-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何逐項對應題目正本 SD-2017-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2017-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2017-1"
def fig1():
    cv = fit(620, 340, (-0.6, 9.0), (-1.0, 4.2), L=20, R=20, T=20, B=20)
    ground(cv, (0, 3.4), (0, -0.3))                                                # 左側固定牆
    cv.line((0, -0.3), (8.6, -0.3), C["member"], 3.0)
    for i in range(26):
        bx = 0.2 + i*0.33; cv.line((bx, -0.3), (bx - 0.25, -0.6), C["member"], 1.4)
    spring(cv, (0, 2.3), (4.2, 2.3), n=6, amp=0.16); cv.math((2.1, 2.3), "k", 16, C["text"], dy=-22)   # #4
    dashpot(cv, (0, 1.1), (4.2, 1.1), wd=0.18); cv.text((1.6, 1.1), "ξ = 0.05", 14, C["text"], dy=24)   # #4 #6
    cv.polygon([(4.2, 0.45), (6.6, 0.45), (6.6, 2.8), (4.2, 2.8)], "none", C["member"], 2.2)
    cv.math((5.4, 1.6), "M", 17, C["text"])
    for x in (4.75, 6.05): cv.circle((x, 0.075), 0.37, "none", C["member"], 2.0)
    V0 = 1.6                                                                       # v0 示意長度
    cv.poly([(6.6, 0.45), (6.6 + V0, 0.45), (6.6 + V0, 2.8), (6.6, 2.8)], C["muted"], 1.8, dash="6 4")   # 右移後位置（虛線） #5
    for x in (4.75 + V0, 6.05 + V0): cv.circle((x, 0.075), 0.37, "none", C["muted"], 1.6, dash="4 3")
    cv.line((6.6, 2.95), (6.6, 3.75), C["dim"], 1.4); cv.line((6.6 + V0, 2.95), (6.6 + V0, 3.75), C["dim"], 1.4)
    cv.arrow((6.6, 3.45), (6.6 + V0, 3.45), C["deform"], 2.2, 9); cv.math((6.6 + V0/2, 3.45), "v_{0}", 15, C["deform"], dy=-14)  # #5
    cv.text_px(310, 328, "初始位移 v_{0}（向右）、初始速度 0；k、M 只給符號", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "彈簧與阻尼器並聯；初始位移 v0 向右、初速 0 的自由振動")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
