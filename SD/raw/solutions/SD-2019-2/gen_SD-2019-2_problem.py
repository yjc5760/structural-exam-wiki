#!/usr/bin/env python3
"""SD-2019-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何逐項對應題目正本 SD-2019-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2019-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2019-2"
H, BW, T = 2.6, 4.0, 0.3
def slab(cv, y):
    cv.polygon([(0, y - T/2), (BW, y - T/2), (BW, y + T/2), (0, y + T/2)], "#E4E7EC", C["member"], 2.0)
def fig1():
    cv = fit(720, 400, (-1.0, 12.6), (-0.8, 6.2), L=20, R=20, T=20, B=20)
    ground(cv, (-0.6, 0), (BW + 0.6, 0))
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["member"], 2.4, cap="butt")
    for y, ml, kl, ul in ((H, "m_{1} = 40 kg", "k_{1} = 2000 N/m", "u_{1}"), (2*H, "m_{2} = 20 kg", "k_{2} = 1000 N/m", "u_{2}")):   # #1
        slab(cv, y); cv.text((BW/2, y - H/2 + 0.6), ml, 14, C["text"])
        cv.text((BW + 0.25, y - H/2), kl, 14, C["text"], "start")
        cv.arrow((BW, y), (BW + 1.3, y), C["deform"], 2.6, 9); cv.math((BW + 1.3, y), ul, 15, C["deform"], "start", dx=6)   # #2
    cv.text((10.2, 4.3), "u_{1}(0) = 0.1 m，u_{2}(0) = 0.2 m", 14, C["text"])          # #4
    cv.text((10.2, 3.4), "初速度：兩層皆 0 m/sec", 14, C["text"])
    cv.text((10.2, 2.4), "起始條件（右圖）", 13, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "下層 40 kg／2000 N/m、上層 20 kg／1000 N/m；起始位移 0.1、0.2 m")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
