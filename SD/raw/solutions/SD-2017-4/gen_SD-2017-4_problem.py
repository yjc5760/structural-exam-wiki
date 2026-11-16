#!/usr/bin/env python3
"""SD-2017-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G3）
幾何、支承、地動逐項對應題目正本 SD-2017-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2017-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2017-4"
L, BW, MW, MH = 5.0, 0.9, 2.2, 1.1     # 柱高 L（考卷只給符號）、柱寬、質量塊尺寸皆示意
def fig1():
    cv = fit(520, 560, (-2.2, 3.4), (-1.6, L + MH + 0.4), L=20, R=20, T=20, B=20)
    cv.polygon([(-BW/2, 0), (BW/2, 0), (BW/2, L), (-BW/2, L)], "#E4E7EC", C["member"], 2.2)   # #2 柱身 EI、m
    for i in range(1, 16):
        y = L*i/16; cv.line((-BW/2, y), (BW/2, y - 0.08), C["member2"], 1.0)
    cv.polygon([(-MW/2, L), (MW/2, L), (MW/2, L + MH), (-MW/2, L + MH)], "#FFFFFF", C["member"], 2.4)  # #1 M 在柱頂
    cv.math((0, L + MH/2), "M", 17, C["text"])
    cv.math((BW/2, L/2), "EI, m", 15, C["text"], "start", dx=10)
    ground(cv, (-1.8, 0), (1.8, 0))                                             # #5 柱底固定
    cv.dim((1.8, 0), (1.8, L), "L", off=-1, label_off=14)                       # #3 L：地面→柱頂（質量塊底面）
    cv.arrow((2.7, 0), (2.7, 0.9), C["muted"], 2.0, 8); cv.math((2.7, 0.9), "x", 15, C["muted"], "start", dx=6)  # #4 x 由底向上
    cv.double_arrow((-1.7, -0.9), (1.7, -0.9), C["load"], 2.4, 9)               # #6 水平地動
    cv.math((0, -0.9), "v̈_{g} sin ωt", 15, C["load"], dy=22)
    cv.text_px(260, 548, "振態 φ(x) = x²/L²（x 由柱底量起）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "M 為柱頂集中質量、L 量到柱頂、x 由柱底向上")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
