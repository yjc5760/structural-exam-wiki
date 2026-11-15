#!/usr/bin/env python3
"""SD-2007-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2007-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2007-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2007-2"
# ── 判讀清單 #1–#5 ── 符號題，尺寸示意
def fig1():
    cv = fit(520, 600, (-2.6, 3.4), (-0.4, 7.0), L=20, R=20, T=20, B=20)
    top = 6.5; ground(cv, (0.6, top), (-0.6, top))                         # #1 上端固定（剖線朝上）
    m1 = (0, 4.0); m2 = (0, 1.0); b = 0.45
    spring(cv, (0, top), (m1[0], m1[1]+b), amp=0.2); cv.math((0.25, (top+m1[1]+b)/2), "k_{1}", 16, C["text"], "start", dx=6)
    spring(cv, (m1[0], m1[1]-b), (m2[0], m2[1]+b), amp=0.2); cv.math((0.25, (m1[1]+m2[1])/2), "k_{2}", 16, C["text"], "start", dx=6)  # #2
    for (x, y), s in ((m1, "m_{1}"), (m2, "m_{2}")):
        cv.polygon([(x-b, y-b), (x+b, y-b), (x+b, y+b), (x-b, y+b)], "#F5F7FA", C["member"], 2.4); cv.math((x, y), s, 16, C["text"])
    for (x, y), s in ((m1, "F_{1} cos ω_{f}t"), (m2, "F_{2} cos ω_{f}t")):                    # #4 向下
        cv.arrow((x+0.75, y+0.5), (x+0.75, y-0.5), C["load"], 2.6, 9); cv.math((x+0.95, y), s, 15, C["load"], "start")
    for (x, y), s in ((m1, "y_{1}"), (m2, "y_{2}")):                                          # #3 向下為正
        cv.line((x-1.5, y), (x-0.9, y), C["deform"], 1.6); cv.arrow((x-1.2, y), (x-1.2, y-0.8), C["deform"], 2.2, 8)
        cv.math((x-1.2, y-0.8), s, 15, C["deform"], dy=14)
    cv.text_px(260, 588, "無阻尼；y1、y2 向下為正", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "k1 接固定端與 m1、k2 接 m1 與 m2（不是兩彈簧都接地）；力與位移皆向下")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
