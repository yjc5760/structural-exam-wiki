#!/usr/bin/env python3
"""SD-2025-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何、支承、載重逐項對應題目正本 SD-2025-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2025-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2025-2"
H, BW, T = 2.0, 3.6, 0.32       # 樓高、跨度考卷未給，示意
def slab(cv, y):
    cv.polygon([(0, y - T), (BW, y - T), (BW, y), (0, y)], "#E4E7EC", C["member"], 2.0)
    for i in range(5):
        x = 0.1 + i*0.72; cv.line((x, y - T), (x + 0.6, y), C["member"], 1.1)
def fig1():
    cv = fit(820, 420, (-1.2, 9.6), (-0.6, 5.0), L=20, R=20, T=20, B=20)
    for x in (0, BW):
        cv.line((x, 0), (x, 2*H), C["member"], 2.6, cap="butt"); cv.support((x, 0), "fixed")   # #5
    for i, (ml, kl, ul) in enumerate((("m_{1}", "k_{1}/2", "u_{1}"), ("m_{2}", "k_{2}/2", "u_{2}"))):
        y = (i + 1)*H
        slab(cv, y)                                                                            # #4 樓版
        cv.math((BW/2, y), ml, 15, C["text"], dy=-14)
        for x, a, dx in ((0, "end", -8), (BW, "start", 8)):
            cv.math((x, y - H/2 - T/2), kl, 15, C["text"], a, dx=dx)                            # #2 每柱 k/2
        cv.arrow((BW, y - T/2), (BW + 1.3, y - T/2), C["deform"], 2.6, 9)                       # #3
        cv.math((BW + 1.3, y - T/2), ul, 15, C["deform"], "start", dx=6)
    cv.poly([(5.4, 2.2), (6.1, 2.2), (6.1, 2.45), (6.6, 2.0), (6.1, 1.55), (6.1, 1.8), (5.4, 1.8), (5.4, 2.2)], C["member"], 2.0)
    X = 8.0                                                                                    # 右圖：串聯模型
    ground(cv, (X - 0.5, 0), (X + 0.5, 0))
    spring(cv, (X, 0), (X, H - 0.2), amp=0.14); spring(cv, (X, H + 0.2), (X, 2*H - 0.2), amp=0.14)
    for i, (ml, kl, ul) in enumerate((("m_{1}", "k_{1}", "u_{1}"), ("m_{2}", "k_{2}", "u_{2}"))):
        y = (i + 1)*H
        cv.circle((X, y), 0.2, "#D0D4DA", C["member"], 2.0)
        cv.math((X, y), ml, 15, C["text"], "end", dx=-22)
        cv.math((X, y - H/2), kl, 15, C["text"], "start", dx=16)
        cv.arrow((X + 0.2, y), (X + 1.1, y), C["deform"], 2.6, 9); cv.math((X + 1.1, y), ul, 15, C["deform"], "start", dx=6)
    cv.text_px(410, 405, "m_{1} = m_{2} = 100 kN·s²/m；k_{1} = k_{2} = 1500 kN/m（層勁度＝兩柱各 k/2 之和）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "每柱 k/2、兩柱合計為層勁度 k；u1 下層、u2 上層")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
