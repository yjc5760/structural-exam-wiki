#!/usr/bin/env python3
"""SD-2024-4：題目附圖重繪（struct-diagram 規範；2026-11-16，X-G1）
只重繪左半簡支梁與振態圖；右半規範公式為文字，照錄於題目正本 §2，不畫。
幾何逐項對應題目正本 SD-2024-4-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2024-4_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2024-4"
L, T = 10.0, 0.22             # 跨長 L（#4），梁深示意
YM = -4.2                     # 振態圖基線高程（示意）
A = 1.6                       # 振態圖振幅（示意）

def fig1():
    cv = fit(720, 470, (-1.2, L + 4.6), (YM - 1.0, 2.7), L=16, R=16, T=14, B=14)
    cv.polygon([(0, -T/2), (L, -T/2), (L, T/2), (0, T/2)], "#F3F4F6", C["member"], 2.2)     # 均質梁 #4
    cv.line((0, 0), (L, 0), C["muted"], 1.2, dash="10 4 2 4")                               # 點鏈線（梁軸）
    cv.support((0, -T/2), "pin"); cv.support((L, -T/2), "roller")                            # #3
    cv.arrow((L, 0), (L + 1.4, 0), C["muted"], 1.8, 8); cv.math((L + 1.4, 0), "x", 16, C["text"], "start", dx=6)   # #6
    cv.arrow((0, 0), (0, 2.2), C["muted"], 1.8, 8); cv.math((0, 2.2), "φ", 16, C["text"], dy=-12)                  # #6
    cv.math((L/2, T/2), "m, EI", 16, C["text"], dy=-16)                                      # #4、#5
    cv.dim((0, -1.25), (L, -1.25), "L", off=0, size=16)                                      # #4
    pts = [(L*i/80, YM + A*math.sin(math.pi*i/80)) for i in range(81)]                        # #7
    cv.line((0, YM), (L, YM), C["member"], 1.6); cv.poly(pts, C["deform"], 2.4)
    cv.math((L/2, YM + A), "φ_{1}(x) = sin(πx/L)", 16, C["text"], dy=-16)
    cv.math((L + 0.3, YM + 0.2), "ω_{1} = (π^{2}/L^{2})(EI/m)^{1/2}", 16, C["text"], "start")             # #7
    cv.text_px(360, 455, "左鉸右滾的均質簡支梁；m 為單位長度質量；振態曲線與頻率式為考卷給定的理論解", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")

FIGURES = [(fig1, "左鉸右滾簡支、m 為單位長度質量；圖示頻率式為考卷給的理論解")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
