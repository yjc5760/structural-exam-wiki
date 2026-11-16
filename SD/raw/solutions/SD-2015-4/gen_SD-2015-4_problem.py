#!/usr/bin/env python3
"""SD-2015-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-1 組 U3-1-G1）
幾何逐項對應題目正本 SD-2015-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2015-4"
X = (0.0, 7.0, 17.0); H = 4.0                    # #3 跨距 7、10 m；#4 柱高 4 m
def fig1():
    cv = fit(680, 400, (-3.2, 19.6), (-2.6, 5.4), L=20, R=20, T=20, B=20)
    cv.line((X[0], H), (X[2], H), C["member"], 2.6)
    for i, x in enumerate(X):
        cv.line((x, 0), (x, H), C["member"], 2.6); cv.support((x, 0), "fixed")          # #2
        cv.text((x, H), str(i + 1), 15, C["text"], "middle", italic=True, dy=-16, dx=-8 if i == 0 else 0)  # #6
        cv.text((x, 0), str(i + 4), 15, C["text"], "start", italic=True, dx=6, dy=-14)
    cv.arrow((X[0] - 2.8, H), (X[0] - 0.08, H), C["load"], 3.0, 11); cv.text((X[0] - 1.6, H), "20 tf", 14, C["load"], dy=-14)  # #5
    cv.dim((X[0], 0), (X[1], 0), "7 m", off=58); cv.dim((X[1], 0), (X[2], 0), "10 m", off=58)    # #3
    cv.dim((X[2] + 1.4, 0), (X[2] + 1.4, H), "4 m", off=0)                               # #4
    cv.text_px(340, 388, "柱斷面積皆 1 m²；柱底 4、5、6 固定（圖未依比例）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "跨距 7 m／10 m、柱底皆固定、20 tf 作用於節點 1")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
