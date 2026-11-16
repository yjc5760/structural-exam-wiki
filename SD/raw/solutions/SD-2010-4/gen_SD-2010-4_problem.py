#!/usr/bin/env python3
"""SD-2010-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-1 組 U3-1-G1）
幾何逐項對應題目正本 SD-2010-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
圖四(c) 為示意性的彈性–完全塑性關係（無數據），依判讀 #8 重繪。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2010-4"
L, B, T = 1.0, 1.0, 0.1                     # 柱高 L（#5）、跨度與樓版厚為示意
def frame(cv, x0, bases, cap):
    cv.polygon([(x0, L), (x0 + B, L), (x0 + B, L + T), (x0, L + T)], "#3F4A5A", C["member"], 1.0)   # 剛性樓版
    cv.math((x0 + B/2, L + T), "M", 15, C["text"], dy=-12)                                          # #6
    for x, kind in zip((x0, x0 + B), bases):
        cv.line((x, 0), (x, L), C["member"], 2.6, cap="butt"); cv.support((x, 0), kind)           # #3、#4
        cv.math((x, L/2), "EI", 14, C["text"], "end", dx=-6)
    cv.arrow((x0 - 0.42, L + T/2), (x0 - 0.02, L + T/2), C["load"], 3.0, 10); cv.math((x0 - 0.5, L + T/2), "V", 15, C["load"])  # #7
    cv.dim((x0 + B + 0.25, 0), (x0 + B + 0.25, L), "L", off=0)                                     # #5
    cv.text((x0 + B/2, -0.42), cap, 14, C["text"])
def fig1():
    cv = fit(900, 330, (-0.7, 5.6), (-0.55, 1.3), L=16, R=16, T=16, B=16)
    frame(cv, 0.0, ("pin", "fixed"), "圖四(a)：左柱底鉸、右柱底固定")
    frame(cv, 2.1, ("fixed", "fixed"), "圖四(b)：兩柱底固定")
    ox = 4.3                                                                                       # 圖四(c) #8
    cv.arrow((ox, 0), (ox + 1.15, 0), C["muted"], 1.6, 8); cv.arrow((ox, 0), (ox, 1.2), C["muted"], 1.6, 8)
    cv.math((ox + 1.15, 0), "ε", 15, C["text"], dy=14); cv.math((ox, 1.2), "σ", 15, C["text"], "end", dx=-8)
    cv.poly([(ox, 0), (ox + 0.35, 0.8), (ox + 1.0, 0.8)], C["deform"], 2.4)
    cv.line((ox, 0.8), (ox + 0.35, 0.8), C["muted"], 1.0, dash="4 3"); cv.math((ox, 0.8), "σ_{y}", 14, C["text"], "end", dx=-6)
    cv.text((ox + 0.55, -0.42), "圖四(c)：彈性–完全塑性", 14, C["text"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "圖四(a) 只有左柱底為鉸、右柱底固定；(b) 兩柱底固定（舊解把 (a)(b) 對調並把兩柱都當鉸接）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
