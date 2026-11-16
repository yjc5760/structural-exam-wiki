#!/usr/bin/env python3
"""SD-2009-4：題目附圖重繪（struct-diagram 規範；2026-11-16，SD-U3-1 組 U3-1-G1）
幾何逐項對應題目正本 SD-2009-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2009-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2009-4"
D, CV, DB, DS = 55.0, 4.0, 2.54, 1.27     # #4 外徑、#3 淨保護層、#5 D25、#6 D13（標稱直徑）
def fig1():
    cv = fit(640, 520, (-36, 62), (-42, 34), L=20, R=20, T=20, B=20)
    R = D/2; Rs = R - CV - DS/2; Rb = R - CV - DS - DB/2
    cv.circle((0, 0), R, "#E4E7EC", C["member"], 2.4)                         # #4 柱外緣
    cv.circle((0, 0), Rs, "none", C["deform"], 2.2)                           # #6 螺箍筋
    for i in range(9):                                                              # #5 9 根縱筋均布
        a = math.radians(90 - 40*i); cv.dot((Rb*math.cos(a), Rb*math.sin(a)), r=DB/2*cv.sx, fill=C["member"], stroke=C["member"], w=0.5)
    cv.dim((-R, -R - 2), (R, -R - 2), "55 cm", off=18)                              # #4
    a = math.radians(135); p_out = (R*math.cos(a), R*math.sin(a)); p_in = ((R - CV)*math.cos(a), (R - CV)*math.sin(a))
    cv.arrow((p_out[0] - 5, p_out[1] + 5), p_out, C["text"], 2.0, 9); cv.arrow((p_in[0] + 4, p_in[1] - 4), p_in, C["text"], 2.0, 9)   # #3
    cv.text((p_out[0] - 7, p_out[1] + 9), "4 cm Clear (Typ.)", 13, C["text"], "middle")
    a = math.radians(50); pb = (Rb*math.cos(a), Rb*math.sin(a))
    cv.line(pb, (R + 6, pb[1]), C["muted"], 1.2); cv.text((R + 7, pb[1]), "9-D25", 14, C["text"], "start")
    pr = (Rs, -3.0); cv.line(pr, (R + 6, pr[1]), C["muted"], 1.2)
    cv.text((R + 7, pr[1]), "D13s@7.5 cm", 14, C["deform"], "start"); cv.text((R + 7, pr[1] - 4.5), "（螺箍筋）", 13, C["deform"], "start")
    cv.text_px(320, 505, "f′c = 350、fy = 4,200 kgf/cm²（螺箍筋）；淨保護層量至螺箍筋外緣", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "淨保護層 4 cm 量至螺箍筋外緣、縱筋 9 根")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
