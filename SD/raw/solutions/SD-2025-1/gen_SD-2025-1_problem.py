#!/usr/bin/env python3
"""SD-2025-1：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U2-2 組 U2-2-G4）
幾何、支承、載重逐項對應題目正本 SD-2025-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2025-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2025-1"
N, h, BW, T = 8, 3.5, 11.0, 0.75     # 層數、層高（題文）；跨度、樓版厚考卷未給，示意
H = N * h                            # 28 m（#5）

def slab(cv, y):
    cv.polygon([(0, y - T), (BW, y - T), (BW, y), (0, y)], "#E4E7EC", C["member"], 1.8)
    for i in range(6):
        x = 0.4 + i * 1.8; cv.line((x, y - T), (min(x + 1.6, BW), y), C["member"], 1.0)

def fig1():
    cv = fit(560, 760, (-6.0, 20.0), (-6.2, 31.5), L=16, R=16, T=16, B=40)
    for x in (0, BW):
        cv.line((x, 0), (x, H), C["member"], 2.4, cap="butt"); cv.support((x, 0), "fixed")   # #7 柱底固定
    cv.text((BW + 1.9, 0.2), "0", 14, C["text"], anchor="start")
    for i in range(1, N + 1):
        y = i * h                                                                            # #5 h_i = 3.5 i
        slab(cv, y)
        cv.text((BW + 1.2, y - T/2), str(i), 14, C["text"], anchor="start")
        cv.math((BW/2, y - T - 0.8), f"m_{{{i}}}", 16, C["text"])                            # #4 m_i 在樓版 i
        cv.arrow((-4.2, y - T/2), (-0.15, y - T/2), C["load"], 2.6, 9)                      # #6 F_i 向右
        cv.math((-4.4, y - T/2), f"F_{{{i}}}", 16, C["load"], "end")
    cv.arrow((BW/2 - 1.6, H + 1.2), (BW/2 + 1.6, H + 1.2), C["load"], 2.6, 9)              # #1 屋頂 F_t
    cv.math((BW/2, H + 2.4), "F_{t}", 16, C["load"])
    cv.dim((BW + 3.6, 0), (BW + 3.6, H), "H = 28 m", off=0, label_off=36, size=15)                 # #5 H 由 0 量到 8
    cv.arrow((BW/2 + 1.6, -2.0), (BW/2 - 1.6, -2.0), C["deform"], 2.4, 9)                  # #8 V0（向左）
    cv.math((BW/2 + 2.0, -2.0), "V_{0}", 16, C["deform"], "start")
    cv.moment_arrow((BW/2 - 0.3, -4.0), r=20, ccw=True, color=C["deform"], span=220, start=160)  # #8 M0 逆時針
    cv.math((BW/2 + 1.6, -4.0), "M_{0}", 16, C["deform"], "start")
    cv.text_px(280, 742, "各層高 3.5 m；各樓層重 20 kN，W = 160 kN；跨度考卷未給（示意）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")

FIGURES = [(fig1, "屋頂 Ft 與 F8 分開畫、m_i 在第 i 層樓版、H 由 0 量到 8")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
