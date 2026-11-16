#!/usr/bin/env python3
"""SD-2013-2：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-1 組 U3-1-G1）
幾何逐項對應題目正本 SD-2013-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2013-2"
Lc, bc, h = 7.0, 0.6, 0.6                    # #2 柱心距 7 m、#7 柱寬 0.6 m、梁深 0.6 m
def fig1():
    cv = fit(760, 360, (-1.3, 8.6), (-2.3, 2.3), L=16, R=16, T=16, B=16)
    for xc, lab in ((0.0, "A"), (Lc, "B")):
        cv.polygon([(xc - bc/2, -1.2), (xc + bc/2, -1.2), (xc + bc/2, 1.2), (xc - bc/2, 1.2)], "#E4E7EC", C["member"], 2.0)
        cv.line((xc, -1.2), (xc, 1.2), C["dim"], 1.0, dash="6 4")
        cv.text((xc, 0), lab, 16, C["text"])
    cv.polygon([(bc/2, -h/2), (Lc - bc/2, -h/2), (Lc - bc/2, h/2), (bc/2, h/2)], "#F5F7FA", C["member"], 2.2)
    cv.line((Lc + bc/2, -h/2), (8.4, -h/2), C["member"], 2.0); cv.line((Lc + bc/2, h/2), (8.4, h/2), C["member"], 2.0)
    cv.text((8.45, 0), "…", 16, C["muted"], "start")
    for x, top, bot in ((bc/2 + 0.35, "+20", "−40"), (Lc - bc/2 - 0.35, "+17", "−48")):   # #4 端點彎矩
        cv.text((x, h/2), top, 15, C["bmd"], dy=-16); cv.text((x, -h/2), bot, 15, C["bmd"], dy=16)
    cv.text((Lc/2, h/2), "+19（梁中點）", 15, C["bmd"], dy=-16)
    cv.dim((0, -1.2), (Lc, -1.2), "7 m（柱中心距）", off=26)                                 # #2
    cv.dim((bc/2, -1.2), (Lc - bc/2, -1.2), "ℓn = 6.4 m（淨跨）", off=66)
    cv.text_px(380, 22, "彎矩單位 Tf-m；+M 下緣受拉、−M 上緣受拉；柱 60×60 cm、梁 40×60 cm", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "7 m 為柱中心距，淨跨 6.4 m（剪力設計用）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
