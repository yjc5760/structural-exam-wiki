#!/usr/bin/env python3
"""SD-2004-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G1）
幾何、支承、自由度逐項對應題目正本 SD-2004-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
比例取自 500 dpi 證據圖 fig-2 像素：柱底 y=857、m1 y=535、m2 y=212 → h1/h2≈0.50；x3：x 435→930 → x3/h2≈0.77（示意）。
用法：python3 gen_SD-2004-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。
（解析自繪圖仍由 gen_SD-2004-4.py 產生，本檔不動它。）"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2004-4"
H2 = 5.0; H1 = H2*(857-535)/(857-212); X3 = H2*(930-435)/(857-212)
def box(cv, p, s=0.17):
    x, y = p; cv.polygon([(x-s, y-s), (x+s, y-s), (x+s, y+s), (x-s, y+s)], "#FFFFFF", C["member"], 2.0)
def fig1():
    cv = fit(560, 470, (-3.0, 6.4), (-0.8, 6.6), L=20, R=20, T=20, B=40)
    cv.line((0, 0), (0, H2), C["member"], 2.6, cap="butt"); cv.support((0, 0), "fixed")   # #4 柱＋固定
    cv.line((0, H2), (X3, H2), C["member"], 2.6, cap="butt")                    # 梁
    for p in ((0, H1), (0, H2), (X3, H2)): box(cv, p)                          # #3 集中質量
    cv.math((0, H1), "m_{1}", 16, C["text"], "end", dx=-30)                     # #5
    cv.math((0, H2), "m_{2}", 16, C["text"], "end", dx=-30)                     # #6
    cv.math((X3, H2), "m_{3}", 16, C["text"], dx=-4, dy=-26)                    # #7
    cv.arrow((0.17, H1), (1.5, H1), C["deform"], 2.6, 9); cv.math((1.5, H1), "u_{1}", 15, C["deform"], "start", dx=6)          # #5
    cv.arrow((X3+0.17, H2), (X3+1.5, H2), C["deform"], 2.6, 9); cv.math((X3+1.5, H2), "u_{2}", 15, C["deform"], "start", dx=6)  # #1、#7
    cv.arrow((X3, H2-0.17), (X3, H2-1.5), C["deform"], 2.6, 9); cv.math((X3, H2-1.5), "u_{3}", 15, C["deform"], "start", dx=8)  # #7 向下
    cv.dim((-1.2, 0), (-1.2, H1), "h_{1}"); cv.dim((-2.3, 0), (-2.3, H2), "h_{2}")   # #5、#6 皆由柱底量起
    cv.dim((0, H2+0.9), (X3, H2+0.9), "x_{3}")                                  # #7
    cv.text_px(280, 440, "h1、h2 皆由柱底量起；各桿軸向剛性 → m2、m3 水平位移同為 u2", 12.5, C["muted"])
    cv.text_px(280, 460, "u1、u2 向右為正，u3 向下為正；支承轉動以順時鐘為正（判讀 #2、#8）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "h2 為柱底至 m2 的全高（非 m1→m2 段長）；u2 同時是 m2 的水平位移")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
