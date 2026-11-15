#!/usr/bin/env python3
"""SD-2022-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何、支承、自由度、外力逐項對應題目正本 SD-2022-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2022-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2022-1"
L = 3.0                                                         # #2 柱長＝梁長＝3 m
def fig1():
    cv = fit(720, 470, (-2.2, 7.6), (-1.0, 5.4), L=20, R=20, T=20, B=20)
    A, B = (0, L), (L, L)
    cv.line((0, 0), A, C["member"], 3.0, cap="butt"); cv.line(A, B, C["member"], 3.0)   # #2 倒 L 形、A 剛接、B 自由
    cv.support((0, 0), "fixed")                                                          # #3
    cv.dot(A, 7.5); cv.dot(B, 7.5)
    cv.text(A, "A", 16, C["text"], "end", dx=-30, dy=22); cv.text(B, "B", 16, C["text"], "start", dx=26)
    cv.arrow((-1.8, L), (-0.35, L), C["deform"], 2.4, 9); cv.text((-1.8, L), "1", 15, C["deform"], "end", dx=-6)   # #4
    cv.arrow((L, L + 0.15), (L, L + 1.1), C["deform"], 2.4, 9); cv.text((L, L + 1.1), "2", 15, C["deform"], "end", dx=-8, dy=4)   # #5
    cv.moment_arrow(A, r=24, ccw=True, color=C["deform"], w=2.0, span=270, start=-90); cv.text(A, "3", 15, C["deform"], "end", dx=-24, dy=-30)   # #6 逆時針
    cv.moment_arrow(B, r=24, ccw=True, color=C["deform"], w=2.0, span=270, start=-90); cv.text(B, "4", 15, C["deform"], "end", dx=-24, dy=-30)
    cv.arrow((L + 0.35, L + 0.25), (L + 0.35, L + 1.7), C["load"], 2.8, 10); cv.text((L + 0.35, L + 1.7), "p(t) = sin(5t)", 15, C["load"], "start", dx=8)   # #7
    cv.dim((0, -0.55), (L, -0.55), "L = 3 m", 0)                                        # 柱、梁長
    cv.dim((-1.0, 0), (-1.0, L), "L = 3 m", 0, label_off=-34)
    cv.text((4.4, 1.6), "m_{A} = 1 kg", 15, C["text"], "start"); cv.text((4.4, 0.9), "m_{B} = 2 kg", 15, C["text"], "start")   # #9
    cv.axes((4.6, -0.6), 0.9, 0.9)
    cv.text_px(360, 458, "EI = 2000（考卷寫 N/m²，應為 N·m²）；忽略軸向變形、構架質量與旋轉慣量", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "B 點只標垂直自由度 2；B 的水平位移等於自由度 1（忽略軸向變形）；轉角 3、4 逆時針為正")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
