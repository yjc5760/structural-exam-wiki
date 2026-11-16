#!/usr/bin/env python3
"""SD-2016-2：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G2）
幾何、支承、彈簧逐項對應題目正本 SD-2016-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2016-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2016-2"
l, Y1, Y2 = 6.0, 2.0, 0.0
def ceil_spring(cv, x, y, top):
    spring(cv, (x, y), (x, top), n=4, amp=0.16, lead=0.22)
    cv.support((x, top), "fixed", ang=180, size=26)
def fig1():
    cv = fit(760, 340, (-1.0, 13.2), (-1.5, 4.3), L=20, R=20, T=20, B=30)
    cv.line((0, Y1), (l, Y1), C["member"], 8, cap="butt")                    # #3 左梁
    cv.line((l, Y2), (2*l, Y2), C["member"], 8, cap="butt")                  # #4 右梁
    cv.support((0, Y1 - 0.08), "pin"); cv.support((2*l, Y2 - 0.08), "pin")   # #10 鉸支承
    ceil_spring(cv, l/2, Y1, Y1 + 1.7)                                       # #5
    ceil_spring(cv, l, Y1, Y1 + 1.7)                                         # #6
    spring(cv, (l, Y1), (l, Y2), n=4, amp=0.16, lead=0.22)                   # #7 連接彈簧
    ceil_spring(cv, 1.5*l, Y2, Y2 + 1.7)                                     # #8
    for x, y in ((l/2, Y1 + 0.85), (l, Y1 + 0.85), (1.5*l, Y2 + 0.85)):
        cv.math((x, y), "k", 17, dx=18)                                      # #9
    cv.math((l, (Y1 + Y2)/2), "k", 17, dx=-20)
    for x, y in ((l/4, Y1), (3*l/4, Y1), (1.25*l, Y2), (1.75*l, Y2)):
        cv.math((x, y), "l / 2", 16, dy=-22)
    cv.text((l/2, Y1), "total mass = m", 14, C["text"], dy=34)
    cv.text((1.5*l, Y2), "total mass = m", 14, C["text"], dy=34)
    cv.text_px(380, 326, "兩支剛性梁各長 l、總質量 m（均勻）；四根彈簧皆為 k，左梁右端一點兩簧", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "左梁右端同時有上方接固定面的彈簧與向下的連接彈簧（共四根彈簧）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
