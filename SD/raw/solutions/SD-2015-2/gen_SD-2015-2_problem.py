#!/usr/bin/env python3
"""SD-2015-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2015-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2015-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2015-2"
H, BW, T = 3.0, 5.0, 0.35     # 樓高、跨度考卷未給，示意
def slab(cv, y):
    cv.polygon([(0, y - T/2), (BW, y - T/2), (BW, y + T/2), (0, y + T/2)], "#E4E7EC", C["member"], 2.0)
    for i in range(14):
        x = 0.2 + i*0.36; cv.line((x, y - T/2), (min(x + 0.35, BW), y + T/2), C["member"], 1.0)
def fig1():
    cv = fit(600, 480, (-1.0, 8.2), (-0.8, 7.4), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #5
    for i, (y, ml, kl, vl) in enumerate(((H, "m_{1} = 50 t", "k_{1}", "v_{1}"), (2*H, "m_{2} = 50 t", "k_{2}", "v_{2}"))):
        slab(cv, y)                                                                           # #4 剛性梁
        cv.text((BW/2, y), ml, 14, C["text"], dy=-22)                                          # #1
        cv.math((BW, y - H/2), kl, 16, C["text"], "start", dx=10)                              # #2 層勁度
        cv.arrow((BW + 0.2, y), (BW + 1.8, y), C["deform"], 2.6, 9); cv.math((BW + 1.8, y), vl, 15, C["deform"], "start", dx=6)  # #3
    cv.text_px(300, 465, "k_{1} = k_{2} = 50 kN/cm（層側向勁度）；50 t = 50 公噸", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "兩層勁度皆 50 kN/cm、質量皆 50 t（舊解讀成 300／200 tf/cm）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
