#!/usr/bin/env python3
"""SD-2021-3：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 3）
幾何、質量、勁度、自由度逐項對應題目正本 SD-2021-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2021-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C, column_shape
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2021-3"
H, BW, T = 2.2, 3.6, 0.3   # 樓高、跨度考卷未給，示意
D = 0.55                    # 一樓初始位移 6 cm（放大示意）
def slab(cv, x0, y):
    cv.polygon([(x0, y - T/2), (x0 + BW, y - T/2), (x0 + BW, y + T/2), (x0, y + T/2)], "#C9CED6", C["member"], 1.8)   # #9 剛性樓版
def fig1():
    cv = fit(860, 470, (-1.0, 13.6), (-1.5, 7.4), L=20, R=20, T=20, B=20)
    ground(cv, (-0.8, 0), (BW + D + 1.0, 0))                                      # #10 柱底固定
    for x in (0, BW):                                                              # 一層柱：變形（考卷畫成彎曲）
        cv.poly(column_shape((x, 0), H, D, 0.0), C["member"], 2.4)
        cv.line((x + D, H), (x + D, 3*H), C["member"], 2.4, cap="butt")            # 上兩層柱：直線（#1）
    for i, (ml, vl) in enumerate((("m", "v_{1}"), ("m", "v_{2}"), ("m/2", "v_{3}"))):   # #7 #11
        y = (i + 1) * H
        slab(cv, D, y)
        cv.math((D + BW/2, y - H/2), ml, 16, C["text"])                           # 質量標在樓層空間內（照考卷）
        cv.math((D + BW, y - H/2), "k", 16, C["text"], "start", dx=10)             # #8
        cv.arrow((D + BW + 0.2, y), (D + BW + 1.4, y), C["deform"], 2.2, 9, dash="5 4")
        cv.math((D + BW + 1.4, y), vl, 15, C["deform"], "start", dx=6)
    cv.arrow((D + BW + 0.2, H - 0.45), (D + BW + 2.4, H - 0.45), C["load"], 3.0, 10)   # 粗索拉一樓版（#1、#6）
    cv.text((D + BW + 2.6, H - 0.45), "粗索", 14, C["load"], "start")
    cv.line((BW, 0), (BW, -1.0), C["dim"], 1, dash="3 3"); cv.line((BW + D, H - T/2), (BW + D, -1.0), C["dim"], 1, dash="3 3")
    cv.dim((BW, -0.9), (BW + D, -0.9), "", 0); cv.text((BW + D, -0.9), "6 cm", 14, C["text"], "start", dx=8)   # #1 量柱腳至一樓版右緣
    # 考卷方框給定的頻率與振態（照錄，非解答）
    x0 = 8.6
    for j, s in enumerate(("ω_{1}^{2} = (2 − √3) k/m", "ω_{2}^{2} = 2 k/m", "ω_{3}^{2} = (2 + √3) k/m")):
        cv.text((x0, 6.4 - j*0.85), s, 15, C["text"], "start")
    cv.text((x0, 3.6), "φ 分量由上而下為 v_{1}、v_{2}、v_{3}：", 13.5, C["muted"], "start")
    for j, s in enumerate(("φ_{1} = {1, √3, 2}", "φ_{2} = {1, 0, −1}", "φ_{3} = {1, −√3, 2}")):
        cv.text((x0, 2.8 - j*0.85), s, 15, C["text"], "start")
    cv.text_px(430, 456, "初始位移：一樓版拉 6 cm、上兩層隨之平移（只有一層柱變形），自靜止放開", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "粗索只拉一樓版、上兩層樓版隨之平移（舊解讀成上兩層不動 {6,0,0}）")]

if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
