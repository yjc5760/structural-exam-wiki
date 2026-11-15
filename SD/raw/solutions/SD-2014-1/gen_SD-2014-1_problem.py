#!/usr/bin/env python3
"""SD-2014-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2014-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2014-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2014-1"
H, BW = 3.0, 4.0     # 樓高、跨度考卷未給，示意
def fig1():
    cv = fit(560, 460, (-1.6, 7.6), (-0.8, 7.4), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #7
    for y, u in ((H, "u_{1}"), (2*H, "u_{2}（屋頂）")):                                          # #2 由下往上
        cv.line((0, y), (BW, y), C["member"], 7, cap="butt"); cv.math((BW/2, y), "m", 17, C["text"], dy=-18)
        cv.arrow((BW+0.2, y), (BW+1.4, y), C["deform"], 2.6, 9); cv.text((BW+1.4, y), u, 15, C["deform"], "start", dx=6)
    cv.text_px(280, 440, "m = 1500 kg（每層）；φ = {φ(u_{1}), φ(u_{2})}，屋頂分量 = 1.00", 12.5, C["muted"])   # #3 #4
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "u1 是二樓、u2 是屋頂；振態向量分量依 (u1, u2) 排列")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
