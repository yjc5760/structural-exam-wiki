#!/usr/bin/env python3
"""SD-2003-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G1）
幾何、支承、自由度逐項對應題目正本 SD-2003-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
斜投影：平面 (x, y) → 圖面 (x + k·y, z + k·y)，k = 0.6（示意；柱高 h 考卷只給符號）。
用法：python3 gen_SD-2003-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-4"
A_, H, K = 4.0, 3.2, 0.6
def P(x, y, z): return (x + K*y, z + K*y)
def fig1():
    cv = fit(640, 520, (-2.2, 9.6), (-1.6, 7.9), L=20, R=20, T=20, B=44)
    pts = {"D": (0, 0), "C": (A_, 0), "B": (A_, A_), "A": (0, A_)}               # #3 正方形 a×a
    I_ = {"D": "2I", "A": "2I", "B": "I", "C": "I"}                               # #7
    for n, (x, y) in pts.items():                                                 # 柱＋柱底固定 #1
        top, bot = P(x, y, H), P(x, y, 0)
        cv.line(bot, top, C["member"], 2.4, dash="7,5" if n == "A" else None, cap="butt")
        cv.support(bot, "fixed")
        side = "end" if n in ("D", "A") else "start"
        cv.math((bot[0], (bot[1]+top[1])/2), I_[n], 15, C["text"], side, dx=-8 if side == "end" else 8)
    D, Cc, B, A = (P(*pts[n], H) for n in "DCBA")
    cv.line(D, A, C["member"], 2.2); cv.line(A, B, C["member"], 2.2)             # 細線 DA、AB
    cv.line(D, Cc, C["member"], 6, cap="butt"); cv.line(Cc, B, C["member"], 6, cap="butt")  # #2 粗線 DC、CB（樓版剛性）
    for n, p, dx, dy in (("D", D, -16, -14), ("C", Cc, -12, -14), ("B", B, 16, -14), ("A", A, 12, 14)):
        cv.math(p, n, 16, C["text"], dx=dx, dy=dy)
    s = 1.2/math.hypot(K, K)
    cv.arrow(Cc, (Cc[0]+1.3, Cc[1]), C["deform"], 2.6, 9); cv.math((Cc[0]+1.3, Cc[1]), "u_{1}", 15, C["deform"], "start", dx=6)       # #4
    cv.arrow(B, (B[0]+K*s, B[1]+K*s), C["deform"], 2.6, 9); cv.math((B[0]+K*s, B[1]+K*s), "u_{2}", 15, C["deform"], "start", dx=6)   # #5
    cv.arrow(A, (A[0]+K*s, A[1]+K*s), C["deform"], 2.6, 9); cv.math((A[0]+K*s, A[1]+K*s), "u_{3}", 15, C["deform"], "start", dx=6)   # #6
    cv.dim((0, -1.0), (A_, -1.0), "a")                                            # #3 沿 DC
    off = (-0.55, 0.55)
    cv.dim((D[0]+off[0], D[1]+off[1]), (A[0]+off[0], A[1]+off[1]), "a")         # #3 沿 DA
    cv.text_px(320, 486, "柱底固定、柱頂與剛性樓版剛接（判讀 #1）；虛線為被遮住的 A 柱", 12.5, C["muted"])
    cv.text_px(320, 506, "u1、u2、u3 是三個角點的平移（C 沿 DC；B、A 沿 DA 方向），地震沿 D→B", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "u1、u2、u3 為角點平移而非質心 x、y 與扭轉（舊解讀成 x、y、θ）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
