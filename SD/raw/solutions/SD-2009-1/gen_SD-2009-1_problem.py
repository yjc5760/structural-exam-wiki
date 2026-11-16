#!/usr/bin/env python3
"""SD-2009-1：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U1-2 組 U1-2-G1）
幾何、支承、載重逐項對應題目正本 SD-2009-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
虛線變形曲線是考卷附圖本來就有的，依考卷給的 Ψ(x) 繪製（振幅示意）。
用法：python3 gen_SD-2009-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。
（解析自繪圖仍由 gen_SD-2009-1.py 產生，本檔不動它。）"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2009-1"
L, ZS = 8.0, 2.0
def psi(x): return (x/L)**2*(1.5 - x/(2*L))                                     # #5
def fig1():
    cv = fit(560, 560, (-4.6, 6.8), (-0.9, 9.9), L=20, R=20, T=20, B=40)
    cv.line((0, 0), (0, L), C["member"], 4, cap="butt"); ground(cv, (-1.4, 0), (1.6, 0))   # #2 懸臂、柱底固定
    cv.arrow((0, L), (0, L+1.0), C["muted"], 2.0, 8); cv.math((0, L+1.0), "x", 15, C["muted"], "start", dx=8)  # #3
    xl = -2.2; cv.line((xl, 0.05), (xl, L), C["load"], 1.8)
    for i in range(11):                                                          # #6 均佈荷重向右、全高
        y = 0.05 + (L-0.05)*i/10; cv.arrow((xl, y), (-0.1, y), C["load"], 1.8, 7)
    cv.text((xl, L+0.45), "均佈荷重 p(t)（荷重/長度）", 12.5, C["load"], "middle")
    cv.poly([(ZS*psi(L*i/60), L*i/60) for i in range(61)], C["deform"], 2.2, dash="8,6")   # Ψ(x) 形狀
    cv.dim((0, L+0.55), (ZS, L+0.55), "Z(t)")                                    # #4 柱頂位移
    cv.dim((-3.7, 0), (-3.7, L), "L")                                            # #3
    cv.text((2.7, 5.6), "v(x,t) = ψ(x)Z(t)", 14, C["text"], "start")
    cv.text((2.7, 4.8), "均佈柱：m（質量/長度）", 13, C["text"], "start")
    cv.text((2.7, 4.1), "EI＝抗彎勁度", 13, C["text"], "start")
    cv.text_px(280, 530, "柱底固定、柱頂自由；Z(t) 為柱頂側移；題文 p、m 上方另有橫線記號", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "懸臂邊界、Z 為柱頂位移、荷重沿全高同向")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
