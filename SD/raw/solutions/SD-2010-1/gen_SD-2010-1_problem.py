#!/usr/bin/env python3
"""SD-2010-1：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G2）
幾何、支承逐項對應題目正本 SD-2010-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2010-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2010-1"
L, TH = 4.0, math.radians(14)          # 桿長示意；θ 為示意的擾動角（#3、#7）
def fig1():
    cv = fit(560, 520, (-4.6, 1.8), (-0.9, 5.3), L=20, R=20, T=20, B=60)
    B = (0.0, 0.0); A = (-L*math.sin(TH), L*math.cos(TH)); r = 0.32
    cv.line((0, 0), (0, 4.9), C["muted"], 1.4, dash="7 6")                     # #3 通過 B 的鉛垂線
    cv.line(B, A, C["member"], 3.2)                                             # #5 剛性桿 AB
    cv.support(B, "pin")                                                        # #4 鉸支承
    wall = -3.9
    spring(cv, (wall, A[1]), (A[0] - r, A[1]), n=6, amp=0.16, lead=0.08)        # #2 水平彈簧
    cv.support((wall, A[1]), "fixed", ang=-90, size=22)                         # #2 牆
    cv.circle(A, r, "#FFFFFF", C["member"], 2.4)                         # #6 集中質量
    cv.math(A, "m", 17)
    cv.math(((wall + A[0] - r)/2, A[1]), "k", 17, dy=-24)
    cv.math(A, "A", 16, dx=-14, dy=36)
    cv.math((A[0]/2, A[1]/2), "L", 17, dx=-20)
    pts = [(2.3*math.sin(-a), 2.3*math.cos(a)) for a in [TH*i/20 for i in range(21)]]
    cv.poly(pts, C["member"], 1.4)                                              # #3 θ 角
    cv.math((-0.28, 2.55), "θ", 16)
    cv.math(B, "B", 16, dx=20, dy=-12)
    cv.text_px(280, 478, "B 鉸支承；剛性桿不計質量；θ 甚小，θ = 0 時彈簧無伸縮", 12.5, C["muted"])
    cv.text_px(280, 500, "鉛垂面內，重力向下（判讀 #1）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "倒單擺：鉸在下、質量在上，重力為傾覆作用；彈簧水平接牆")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
