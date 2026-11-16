#!/usr/bin/env python3
"""SD-2018-1：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-2 組 U3-2-G4）
幾何、支承、阻尼器逐項對應題目正本 SD-2018-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2018-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, dashpot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2018-1"
L, H, T = 6.0, 3.0, 0.32          # 跨距 L = 6 m、樓高 H = 3 m（題文，依比例）；梁厚示意
def fig1():
    cv = fit(640, 440, (-1.4, 8.0), (-1.3, 4.0), L=20, R=20, T=20, B=20)
    for x in (0, L):
        cv.line((x, 0), (x, H), C["member"], 2.6, cap="butt"); cv.support((x, 0), "fixed")     # #3 柱底固定、#4 兩柱
    cv.polygon([(0, H - T/2), (L, H - T/2), (L, H + T/2), (0, H + T/2)], C["member"], C["member"], 1.5)  # #2 剛性梁（塗黑）
    cv.text((L/2, H + T/2), "W = 70 kN", 15, C["text"], dy=-14)                                          # #7
    p0, p1 = (0.0, 0.0), (L, H - T/2)                                                                    # #5、#6 斜撐兩端
    q0 = (p0[0] + 0.45*(p1[0]-p0[0]), p0[1] + 0.45*(p1[1]-p0[1])); q1 = (p0[0] + 0.55*(p1[0]-p0[0]), p0[1] + 0.55*(p1[1]-p0[1]))
    cv.line(p0, q0, C["member"], 1.8); dashpot(cv, q0, q1, wd=0.13, color=C["member"], w=1.8); cv.line(q1, p1, C["member"], 1.8)
    for p in (p0, p1): cv.dot(p, 5.5, "#FFFFFF", C["member"], 1.8)                                    # #5 兩端鉸
    cv.math((L/2 + 0.25, H/2 - 0.35), "C", 16, C["text"], "start")                                       # #5 阻尼係數 C
    for x, a, dx in ((0, "end", -10), (L, "end", -10)):
        cv.math((x, H*0.42), "EI", 15, C["text"], a, dx=dx)                                              # #4 每柱 EI
    cv.dim((L + 0.9, 0), (L + 0.9, H), "H = 3 m", off=0, label_off=34)                                  # #6 H：柱底至梁中心線
    cv.dim((0, -0.75), (L, -0.75), "L = 6 m", off=0, label_off=16)                                       # #6 L：兩柱中心線
    cv.text_px(320, 428, "EI = 5000 kN·m²（每柱）；阻尼器兩端鉸接、對角斜撐", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "兩柱固定、剛性梁；阻尼器為左柱底至右柱頂的對角斜撐（兩端鉸），傾角由 H、L 決定")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
