#!/usr/bin/env python3
"""SD-2021-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何、支承、載重逐項對應題目正本 SD-2021-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2021-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2021-1"
W, H, T = 8.0, 3.2, 0.25        # 構架內寬、內高、框厚（考卷未給尺寸，示意）
def fig1():
    cv = fit(760, 400, (-1.2, 11.4), (-1.2, 4.6), L=20, R=20, T=20, B=30)
    ground(cv, (-0.8, -0.75), (W + 0.8, -0.75))                                   # 固定地面
    for x in (1.6, W - 1.6): cv.circle((x, -0.4), 0.33, C["member"], C["member"], 1)  # #3 構架下滾輪
    fr = "#E9D3CC"                                                                 # #3 剛性構架（四邊厚框）
    for pts in ([(-T, -T), (W + T, -T), (W + T, 0), (-T, 0)], [(-T, H), (W + T, H), (W + T, H + T), (-T, H + T)],
                [(-T, -T), (0, -T), (0, H + T), (-T, H + T)], [(W, -T), (W + T, -T), (W + T, H + T), (W, H + T)]):
        cv.polygon(pts, fr, C["member"], 2.0)
    cx, bw, bh = W/2, 1.9, 1.3                                                     # #4 台車
    for x in (cx - 0.5, cx + 0.5): cv.circle((x, 0.22), 0.22, C["member"], C["member"], 1)
    cv.polygon([(cx - bw/2, 0.44), (cx + bw/2, 0.44), (cx + bw/2, 0.44 + bh), (cx - bw/2, 0.44 + bh)], "#FFFFFF", C["member"], 2.4)
    cv.math((cx, 0.44 + bh/2), "m", 18)
    ys = 0.44 + bh/2                                                               # #5 兩根彈簧 k
    spring(cv, (0, ys), (cx - bw/2, ys), n=5, amp=0.28, lead=0.25)
    spring(cv, (cx + bw/2, ys), (W, ys), n=5, amp=0.28, lead=0.25)
    cv.math((cx/2 - 0.45, ys + 0.6), "k", 17); cv.math((W - (W - cx - bw/2)/2, ys + 0.6), "k", 17)
    top = 0.44 + bh                                                                # #2 x 箭頭（起點在台車頂上短線）
    cv.line((cx, top), (cx, top + 0.7), C["deform"], 2.0)
    cv.arrow((cx, top + 0.55), (cx + 1.3, top + 0.55), C["deform"], 2.4, 9); cv.math((cx + 0.75, top + 0.55), "x", 16, C["deform"], dy=-14)
    cv.arrow((W + 0.6, ys), (W + 3.0, ys), C["load"], 3.0, 10)                     # #6 構架位移
    cv.text((W + 1.8, ys), "d(t) = sin(ωt/2)", 14, C["load"], dy=-18)
    cv.text_px(380, 388, "ω 為本系統的自然振動頻率；無阻尼；構架為剛體、以滾輪置於地面", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "兩側各一根彈簧 k 接構架內壁；構架以滾輪受位移 d(t)；x 量測基準未標")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
