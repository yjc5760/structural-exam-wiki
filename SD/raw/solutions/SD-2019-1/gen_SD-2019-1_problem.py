#!/usr/bin/env python3
"""SD-2019-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何逐項對應題目正本 SD-2019-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2019-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2019-1"
L = 2.0
def panel(cv, x0, cap):
    cv.polygon([(x0, -0.09), (x0 + 2*L, -0.09), (x0 + 2*L, 0.09), (x0, 0.09)], C["member"], C["member"], 1)  # #5 剛性梁 2L
    cv.support((x0, -0.09), "pin")                                                   # #2 左端鉸
    xs = x0 + L
    spring(cv, (xs, 0.09), (xs, 1.4), n=4, amp=0.12); cv.math((xs, 0.75), "2k", 15, C["text"], "start", dx=12)   # #3
    cv.line((xs - 0.45, 1.4), (xs + 0.45, 1.4), C["member"], 2.6)
    for i in range(5):
        bx = xs - 0.4 + i*0.2; cv.line((bx, 1.4), (bx + 0.16, 1.58), C["member"], 1.4)
    xe = x0 + 2*L
    spring(cv, (xe, -0.09), (xe, -1.3), n=4, amp=0.12); cv.math((xe, -0.7), "k", 15, C["text"], "start", dx=12)   # #4
    cv.circle((xe, -1.55), 0.25, "#9AA3AF", C["member"], 2.0); cv.text((xe + 0.4, -1.55), "(2/3) m", 13.5, C["text"], "start")   # #1
    cv.dim((x0, -0.09), (xs, -0.09), "L", off=-0.5); cv.dim((xs, -0.09), (xe, -0.09), "L", off=-0.5)
    cv.text((x0 + L, -2.3), cap, 14, C["text"])
def fig1():
    cv = fit(860, 330, (-0.6, 11.4), (-2.6, 1.8), L=20, R=20, T=20, B=20)
    panel(cv, 0.0, "㈠ 剛性梁總質量 = 0")
    panel(cv, 6.3, "㈡ 剛性梁總質量 = m")
    cv.text_px(430, 322, "圓球：圖上標 (2/3) m（題文寫 m，判讀 #1）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "2k 在距鉸 L 處、k 懸吊圓球於自由端；圓球質量依圖 (2/3)m")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
