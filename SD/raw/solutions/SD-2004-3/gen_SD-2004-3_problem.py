#!/usr/bin/env python3
"""SD-2004-3：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G1）
幾何、支承、接頭逐項對應題目正本 SD-2004-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
CD 與 AB 的高差考卷未給，示意。
用法：python3 gen_SD-2004-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2004-3"
L, HY, T = 10.0, 3.6, 0.36
def fig1():
    cv = fit(640, 440, (-1.4, 11.4), (-2.9, 5.6), L=20, R=20, T=20, B=40)
    cv.line((0, 0), (L, 0), C["member"], 3.2, cap="butt")                         # #5 AB 彈性梁
    cv.support((0, 0), "pin"); cv.support((L, 0), "roller")                     # #5
    yb = HY - T/2
    cv.polygon([(0, yb), (L/2, yb), (L/2, HY+T/2), (0, HY+T/2)], "#E4E7EC", C["member"], 2.0)   # #4 CD 剛性桿 L/2
    for i in range(13):
        x = 0.15 + i*0.38; cv.line((x, yb), (min(x+0.34, L/2), HY+T/2), C["member"], 1.0)
    cv.support((0, yb), "pin")                                                   # #1 C 鉸支承在 A 正上方
    cv.line((L/4, 0.13), (L/4, yb-0.13), C["member"], 2.2)                       # #2 EF 鉛直剛性連桿
    cv.circle((L/4, 0.13), 0.11, "#FFFFFF", C["member"], 2); cv.circle((L/4, yb-0.13), 0.11, "#FFFFFF", C["member"], 2)  # #3 鉸
    for p, s, dx, dy in (((0, 0), "A", -26, -6), ((L, 0), "B", 22, -6), ((L/4, 0.13), "E", 16, -10),
                         ((L/4, yb-0.13), "F", 16, 12), ((0, HY), "C", -22, 0), ((L/2, HY), "D", 18, 0)):
        cv.math(p, s, 16, C["text"], dx=dx, dy=dy)
    cv.math((L/2-0.9, HY+T/2), "m_{0}", 15, C["text"], dy=-14)                  # #8
    cv.math((8.0, 0), "m, EI", 15, C["text"], dy=20)                             # #8
    cv.arrow((0.05, 0.85), (0.95, 0.85), C["muted"], 2.0, 8); cv.math((0.95, 0.85), "x", 15, C["muted"], "start", dx=6)  # #6
    cv.dim((0, 5.0), (L/2, 5.0), "L/2")                                          # #4
    cv.dim((0, -1.35), (L/4, -1.35), "L/4"); cv.dim((0, -2.2), (L, -2.2), "L")   # #2、#5
    cv.text_px(320, 425, "C 為鉸支承（在 A 正上方），CD 可繞 C 轉動、D 端自由；E、F 為鉸，EF 鉛直", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "C 端為鉸支承、CD 繞 C 轉動（舊解讀成 CD 整根平移）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
