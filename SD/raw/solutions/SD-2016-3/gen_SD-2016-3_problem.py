#!/usr/bin/env python3
"""SD-2016-3：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 2）
幾何、支承、載重逐項對應題目正本 SD-2016-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2016-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2016-3"
MODES = [("第一振態", [1, 2, 3]), ("第二振態", [-1, -1, 2]), ("第三振態", [1, -1, 1])]   # #3–#5 由下往上
H = 1.6
def fig1():
    cv = fit(760, 360, (-1.0, 17.0), (-1.4, 5.8), L=20, R=20, T=20, B=20)
    BW = 2.6
    for x in (0, BW): cv.line((x, 0), (x, 3*H), C["member"], 2.2, cap="butt")
    ground(cv, (-0.5, 0), (BW + 0.5, 0))
    for j, lab in enumerate(("α", "β", "1000 kg")):                                   # #2
        y = (j + 1)*H
        cv.polygon([(0, y - 0.16), (BW, y - 0.16), (BW, y + 0.16), (0, y + 0.16)], "#C9CED6", C["member"], 1.6)
        cv.text((BW/2, y - H/2), lab, 14, C["text"])
    sc = 0.55
    for i, (name, ph) in enumerate(MODES):
        x0 = 5.6 + i*4.0
        cv.line((x0, 0), (x0, 3*H), C["member"], 2.6)
        pts = [(x0, 0)] + [(x0 + sc*v, (j + 1)*H) for j, v in enumerate(ph)]
        cv.poly(pts, C["deform"], 1.8)
        for j, v in enumerate(ph):
            y = (j + 1)*H; cv.arrow((x0, y), (x0 + sc*v, y), C["deform"], 1.6, 7)
            cv.text((x0 + sc*v, y), f"{v:g}".replace("-", "−"), 13.5, C["text"], "start" if v > 0 else "end", dx=6 if v > 0 else -6)
        cv.text((x0, -0.8), name, 13, C["text"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "振態分量由下往上：{1,2,3}、{−1,−1,2}、{1,−1,1}；α 在一樓、β 在二樓")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
