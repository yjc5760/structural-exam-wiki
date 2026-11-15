#!/usr/bin/env python3
"""SD-2005-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2005-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2005-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2005-2"
# ── 判讀清單 #1–#11 ──
XL, XM, XR = 0.0, 7.0, 15.0    # #11 跨距 7 m、8 m
H1, H2 = 4.2, 3.2              # #8
def fig1():
    cv = fit(820, 520, (-2.0, 19.5), (-1.6, 9.6), L=20, R=20, T=20, B=20)
    y1, y2 = H1, H1 + H2
    for x in (XL, XM, XR): cv.line((x, 0), (x, y1), C["member"], 3.2, cap="butt")   # #9 一樓三柱 50×50
    for x in (XM, XR): cv.line((x, y1), (x, y2), C["member"], 3.2, cap="butt")      # #5 二樓兩柱 40×40（右跨）
    cv.line((XL, y1), (XR, y1), C["member"], 6, cap="butt"); cv.line((XM, y2), (XR, y2), C["member"], 6, cap="butt")
    cv.support((XL, 0), "fixed"); cv.support((XR, 0), "fixed")                       # #1 #3
    cv.support((XM, 0), "pin", size=16); cv.dot((XM, 0), 4.5, "#FFFFFF", C["load"], 2.2)  # #2 中柱底鉸支承
    cv.text((XM, 0), "鉸支承", 13, C["load"], "start", dx=18, dy=-14)
    cv.text(((XL+XM)/2, y1), "35000 kg", 14, C["text"], dy=-16); cv.text(((XM+XR)/2, y1), "40000 kg", 14, C["text"], dy=-16)  # #6
    cv.text(((XM+XR)/2, y2), "20000 kg", 14, C["text"], dy=-16)                                                            # #7
    for y, s in ((y1, "y_{1}"), (y2, "y_{2}")):
        cv.arrow((XR+0.2, y), (XR+2.0, y), C["deform"], 2.4, 9); cv.math((XR+2.0, y), s, 16, C["deform"], "start", dx=6)
    cv.dim((XL, 0), (XM, 0), "7 m", off=34, label_off=14); cv.dim((XM, 0), (XR, 0), "8 m", off=34, label_off=14)
    cv.dim((XR+3.2, 0), (XR+3.2, y1), "4.2 m", off=0, label_off=-26); cv.dim((XR+3.2, y1), (XR+3.2, y2), "3.2 m", off=0, label_off=-26)
    cv.text(((XL+XM)/2, y1/2), "一樓 3 柱 50×50 cm", 12.5, C["muted"]); cv.text(((XM+XR)/2, y1+H2/2), "二樓 2 柱 40×40 cm", 12.5, C["muted"])
    cv.text_px(410, 505, "E = 2.3×10^6 kgf/cm^2；樓版剛性（剪力屋架）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "中柱底為鉸支承（側向勁度 3EI/h³，不是 12EI/h³）；二樓只在右跨")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
