#!/usr/bin/env python3
"""SD-2021-2：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
載重歷時逐項對應題目正本 SD-2021-2-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西（半正弦波由題給峰值與延時決定，非讀圖數據）。
用法：python3 gen_SD-2021-2_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2021-2"
P0, TD = 100.0, 0.1            # #2 峰值 10² kN、延時 0.1 s
def fig1():
    S = 1000.0                    # 橫軸模型座標＝t×1000（只為縮放，標籤仍寫 s）
    cv = fit(640, 340, (-60, 300), (-25, 135), L=20, R=20, T=20, B=40)
    cv.arrow((0, 0), (0.17*S, 0), C["muted"], 1.8, 9); cv.arrow((0, 0), (0, 128), C["muted"], 1.8, 9)
    pts = [(TD*S*i/60, P0*math.sin(math.pi*i/60)) for i in range(61)]
    cv.polygon(pts, C["fill_t"], C["load"], 2.4)
    cv.line((0, P0), (TD*S, P0), C["dim"], 1, dash="3 3"); cv.line((TD*S, P0), (TD*S, 0), C["dim"], 1, dash="3 3")
    cv.text((0, P0), "10^{2} kN", 14, C["text"], "end", dx=-8)
    cv.text((TD*S, 0), "0.1", 14, C["text"], dy=18); cv.text((0, 0), "0", 13, C["text"], "end", dx=-6, dy=10)
    cv.text((0, 128), "p(t)  (kN)", 14, C["text"], "start", dx=10)
    cv.text((0.17*S, 0), "t (sec)", 14, C["text"], "end", dy=-14)
    cv.text((0.115*S, 70), "半正弦波（half-sine）", 14, C["load"], "start")
    cv.text_px(330, 326, "t > 0.1 s 時 p = 0；m = 10^{4} kg，ω_{n} = 10 rad/s（同㈠的系統）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "半正弦波峰值 100 kN、延時 0.1 s，峰值在 0.05 s")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
