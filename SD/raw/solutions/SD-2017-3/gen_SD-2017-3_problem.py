#!/usr/bin/env python3
"""SD-2017-3：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-1 組 U3-1-G1）
幾何逐項對應題目正本 SD-2017-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。柱距考卷未給，示意等距。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2017-3"
S, L, T = 1.0, 1.0, 0.07                           # 柱距（示意）、柱高 ℓ（#6）、梁厚（示意）
WALLS = ((0, 1, L/2), (1, 2, L/4))                 # 1–2 牆高 ℓ/2、2–3 牆高 ℓ/4（#2）
def wall(cv, x0, x1, h):
    cv.polygon([(x0, 0), (x1, 0), (x1, h), (x0, h)], "#E9E3D3", C["member"], 1.6)
    n = 9
    for i in range(1, n):
        for j in range(1, max(2, int(h/0.06))):
            cv.dot((x0 + (x1 - x0)*i/n, h*j/max(2, int(h/0.06))), r=1.3, fill=C["muted"], stroke="none", w=0)
    cv.text(((x0 + x1)/2, h/2), "牆（剛性）", 13, C["text"])
def fig1():
    cv = fit(660, 460, (-0.75, 3.75), (-0.42, 1.32), L=20, R=20, T=20, B=20)
    for (a, b, h) in WALLS: wall(cv, a*S, b*S, h)                                         # #2、#4
    cv.polygon([(0, L), (3*S, L), (3*S, L + T), (0, L + T)], "#E4E7EC", C["member"], 2.0)  # 剛性梁
    for i in range(16): x = 0.02 + i*0.19; cv.line((x, L), (min(x + 0.07, 3*S), L + T), C["member"], 1.0)
    for i in range(4):
        cv.line((i*S, 0), (i*S, L), C["member"], 2.6)                                    # #3、#5
        cv.math((i*S, 0.86*L), "EI", 15, C["text"], "start", dx=6)
        cv.text((i*S, 0), str(i + 1), 16, C["text"], italic=True, dy=34)
    ground(cv, (-0.3, 0), (3*S + 0.3, 0))
    cv.arrow((-0.6, L + T/2), (-0.03, L + T/2), C["load"], 3.0, 11); cv.math((-0.45, L + T/2), "V", 16, C["load"], dy=-15)  # #7
    cv.dim((-0.22, 0), (-0.22, L/2), "ℓ/2", off=0, label_off=-18)
    cv.dim((2*S + 0.12, 0), (2*S + 0.12, L/4), "ℓ/4", off=0, label_off=18)
    cv.dim((3*S + 0.35, 0), (3*S + 0.35, L), "ℓ", off=0)                                  # #6 量至梁底
    cv.text_px(330, 448, "牆及梁為剛性；四柱 EI 相同；ℓ 為地面至梁底", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "柱 3 旁牆高 ℓ/4 → 柱 3 可變形段 3ℓ/4（舊解讀成 ℓ/4）；柱 2 受較高牆 ℓ/2 束制")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
