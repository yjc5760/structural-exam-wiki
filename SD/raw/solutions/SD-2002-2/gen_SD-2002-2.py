#!/usr/bin/env python3
"""SD-2002-2：解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
fig-2：軸壓比 N/Ncr 對週期比 T/T0 與頻率平方比 (ω/ω0)² 的關係（正本 §4：T＝T0/√(1−N/Ncr)、k*∝1−N/Ncr）。
用法：python3 gen_SD-2002-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2002-2"
SX, SY, YMAX = 8.0, 1.2, 4.0                   # x：N/Ncr 0–1 → 0–8；y：比值 0–4 → 0–4.8
def fig2():
    cv = fit(640, 440, (-1.4, 9.6), (-1.1, 5.6), L=20, R=20, T=20, B=40)
    cv.arrow((0, 0), (8.6, 0), C["muted"], 1.8, 8); cv.arrow((0, 0), (0, YMAX*SY + 0.5), C["muted"], 1.8, 8)
    for v in (0.25, 0.5, 0.75, 1.0):
        cv.line((v*SX, 0), (v*SX, -0.12), C["muted"], 1.4); cv.text((v*SX, 0), f"{v:g}", 12, C["muted"], dy=18)
    for v in (1, 2, 3, 4):
        cv.line((0, v*SY), (-0.12, v*SY), C["muted"], 1.4); cv.text((0, v*SY), f"{v}", 12, C["muted"], "end", dx=-8)
    cv.text((8.6, 0), "N/Ncr", 13, C["text"], "start", dx=6)
    cv.line((SX, 0), (SX, YMAX*SY), C["accent"], 1.6, dash="6,5"); cv.text((SX, YMAX*SY), "挫屈：k* = 0", 12, C["accent"], "start", dx=6, dy=-4)
    r = [i/200*0.94 for i in range(201)]
    cv.poly([(x*SX, SY/math.sqrt(1-x)) for x in r], C["deform"], 2.8)
    cv.poly([(x*SX, SY*(1-x)) for x in [i/100 for i in range(101)]], C["bmd"], 2.4)
    for x in (0.5, 0.75):
        y = 1/math.sqrt(1-x); cv.dot((x*SX, y*SY), 4.5, C["deform"])
        cv.text((x*SX, y*SY), f"T/T0 = {y:.3f}", 12, C["deform"], "end", dx=-8, dy=-8)
    cv.legend(230, 150, [(C["deform"], "T/T0 = 1/√(1 − N/Ncr)"), (C["bmd"], "(ω/ω0)² = k*/k*(N=0) = 1 − N/Ncr")])
    cv.text_px(320, 425, "T0 = (2/π)·√[L³(mL + 2M)/EI]（N = 0 時的週期）；M 只改變 T0，不改變曲線形狀", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-period-axial.svg")
FIGURES = [(fig2, "軸壓使週期延長，N→Ncr 時 T→∞")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
