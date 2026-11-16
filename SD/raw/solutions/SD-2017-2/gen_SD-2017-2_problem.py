#!/usr/bin/env python3
"""SD-2017-2：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G3）
幾何、支承、自由度逐項對應題目正本 SD-2017-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2017-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2017-2"
H, LS = 4.0, 6.4               # 柱高 h、跨度 ℓ：考卷只給符號，比例照原圖
def fig1():
    cv = fit(640, 470, (-1.6, LS + 1.8), (-1.5, H + 1.0), L=20, R=20, T=20, B=20)
    A, B, Cn, D = (0, 0), (0, H), (LS, H), (LS, 0)
    cv.line(A, B, C["member"], 2.6); cv.line(D, Cn, C["member"], 2.6)          # #4 兩柱
    cv.line(B, Cn, C["member"], 2.6)                                             # #5 梁（剛接，無鉸圈）
    cv.support(A, "fixed"); cv.support(D, "fixed")                               # #4 柱底固定
    cv.math((0, H/2), "EI_{1}", 15, C["text"], "start", dx=8)
    cv.math((LS, H/2), "EI_{1}", 15, C["text"], "start", dx=8)
    cv.math((LS/2, H), "EI_{2}, m", 15, C["text"], dy=-16)                        # #1 m 標在梁上
    cv.moment_arrow(B, r=20, ccw=False, color=C["deform"], start=160, span=260)  # #2 v3 順時針
    cv.math(B, "v_{3}", 15, C["deform"], dx=-4, dy=-34)
    cv.moment_arrow(Cn, r=20, ccw=False, color=C["deform"], start=160, span=260) # #2 v2 順時針
    cv.math(Cn, "v_{2}", 15, C["deform"], dx=-4, dy=-34)
    cv.arrow(Cn, (LS + 1.1, H), C["deform"], 2.6, 9)                             # #3 v1 向右
    cv.math((LS + 1.1, H), "v_{1}", 15, C["deform"], "start", dx=6)
    cv.dim(A, B, "h", off=-55)                                                    # #4 h：柱底→梁
    cv.dim(A, D, "ℓ", off=52)                                                   # #5 ℓ：柱線→柱線
    cv.text_px(320, 458, "三自由度：v1 側移、v2／v3 節點轉角（順時針為正）；無阻尼", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "v2、v3 皆順時針；m 只標在梁上")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
