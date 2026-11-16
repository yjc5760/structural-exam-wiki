#!/usr/bin/env python3
"""SD-2013-3：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G2）
幾何、支承逐項對應題目正本 SD-2013-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2013-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
from sdprob import fit

TAG = "SD-2013-3"
LL, T = 10.0, 0.4
def fig1():
    cv = fit(720, 340, (-0.8, 14.6), (-2.4, 3.2), L=20, R=20, T=20, B=40)
    cv.polygon([(0, -T/2), (LL, -T/2), (LL, T/2), (0, T/2)], "#E4E7EC", C["member"], 2.0)   # #6 均勻梁
    cv.support((0, 0), "fixed", ang=-90, size=34)                                            # #4 固定端
    bw, bh = 2.3, 0.9; x0 = LL/2 - bw/2                                                      # #2 重量塊中心在中點
    cv.polygon([(x0, T/2), (x0 + bw, T/2), (x0 + bw, T/2 + bh), (x0, T/2 + bh)], "#FFFFFF", C["load"], 2.0)
    for i in range(7):
        xa = x0 + 0.1 + i*0.36; cv.line((xa, T/2 + 0.05), (min(xa + 0.6, x0 + bw - 0.05), T/2 + bh - 0.05), C["load"], 1.1)
    cv.text((LL/2, T/2 + bh), "重量 = W", 15, C["text"], dy=-16)
    cv.text((LL, 0.35), "均勻梁", 14, C["text"], "start", dx=14)                             # #6
    cv.math((LL, -0.35), "EI", 15, C["text"], "start", dx=14); cv.text((LL, -0.35), "= 剛度", 14, C["text"], "start", dx=36)
    cv.math((LL, -1.05), "m", 15, C["text"], "start", dx=14); cv.text((LL, -1.05), "= 質量/長度", 14, C["text"], "start", dx=30)
    cv.dim((0, -T/2), (LL/2, -T/2), "L/2", off=62)                                          # #5
    cv.dim((LL/2, -T/2), (LL, -T/2), "L/2", off=62)
    cv.text_px(360, 322, "固定端－自由端懸臂；W 為重量（質量 W/g），視為中點集中質量（判讀 #2、#3）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "重量塊在中點 L/2 而非自由端；W 是重量")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
