#!/usr/bin/env python3
"""SD-2005-4：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2005-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2005-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2005-4"
# ── 判讀清單 #1–#5 ── 全部為符號題，尺寸僅示意
TH = math.radians(30)        # #3 Ωt 由水平線量起（示意角度）
def fig1():
    cv = fit(640, 520, (-3.2, 4.4), (-2.6, 3.6), L=20, R=20, T=20, B=20)
    W, Hb, yb = 4.0, 2.6, 0.0
    cv.polygon([(-W/2, yb), (W/2, yb), (W/2, yb+Hb), (-W/2, yb+Hb)], "#F5F7FA", C["member"], 2.6)   # #2
    cv.text((-1.2, yb+0.45), "(M − m)", 15, C["text"])
    c0 = (0.2, yb+1.4); e = 1.1; pm = (c0[0]+e*math.cos(TH), c0[1]+e*math.sin(TH))
    cv.line(c0, pm, C["member"], 2.6); cv.dot(c0, 4.5, "#FFFFFF", C["member"], 2); cv.dot(pm, 11, C["member"], C["member"], 1)
    cv.line(c0, (c0[0]+1.4, c0[1]), C["dim"], 1.4, dash="4 3")
    cv.poly([(c0[0]+0.55*math.cos(a), c0[1]+0.55*math.sin(a)) for a in [i*TH/20 for i in range(21)]], C["deform"], 1.8)
    cv.math((c0[0]+0.72, c0[1]+0.16), "Ωt", 15, C["deform"], "start")
    cv.math(((c0[0]+pm[0])/2, (c0[1]+pm[1])/2), "e", 16, C["text"], dx=-10, dy=-10); cv.math(pm, "m", 16, C["text"], dx=16, dy=-16)
    yg = -1.9; ground(cv, (-2.4, yg), (2.4, yg))
    spring(cv, (-1.4, yb), (-1.4, yg), amp=0.18); spring(cv, (1.4, yb), (1.4, yg), amp=0.18)   # #5
    cv.math((-1.4, (yb+yg)/2), "k/2", 15, C["text"], "end", dx=-16); cv.math((1.4, (yb+yg)/2), "k/2", 15, C["text"], "start", dx=16)
    dashpot(cv, (0, yb), (0, yg), wd=0.2)                                                       # #1
    cv.math((0, (yb+yg)/2), "c", 16, C["text"], "start", dx=22)
    cv.arrow((3.2, yb+0.6), (3.2, yb+1.8), C["deform"], 2.4, 9); cv.math((3.2, yb+1.8), "u", 16, C["deform"], "start", dx=8)  # #4
    cv.text_px(320, 505, "圖上 c 為黏滯阻尼器符號；題文稱「遲滯阻尼」（判讀 #1）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "總質量 M 已含馬達 m；u 向上為正；阻尼器 c 的型式（題文遲滯、圖為黏滯）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
