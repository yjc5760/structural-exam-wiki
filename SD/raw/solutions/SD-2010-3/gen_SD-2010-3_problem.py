#!/usr/bin/env python3
"""SD-2010-3：題目附圖重繪（struct-diagram 規範；2026-11-16，X-G1）
幾何、支承逐項對應題目正本 SD-2010-3-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2010-3_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2010-3"
L = 4.0                       # 跨長＝柱高＝L（#6、#7）
D, G = 0.50, 0.12             # 梁深、梁縫（示意）
PW = 0.52                     # 墩寬（示意）
BH = 0.34                     # 支承高（示意）
XP = [0.0, L, 2*L, 3*L]       # 四支墩柱中心（#2）
KIND = ["roller", "pin", "roller", "pin"]   # #2：第 1、3 墩兩側滾、第 2、4 墩兩側鉸
YT = L                        # 墩頂（支承下緣）高程；柱高 L 量至此（#7）
YB = YT + BH                  # 梁底
EXT = 0.55*L                  # 兩端延續段（#10，長度示意）

def girder(cv, x0, x1):
    cv.polygon([(x0, YB), (x1, YB), (x1, YB + D), (x0, YB + D)], "#FFFFFF", C["member"], 2.2)

def brk(cv, x, s):            # 波浪折斷線（#10）
    pts = [(x + s*0.10*math.sin(math.pi*t/12*2), YB - 0.12 + (D + 0.24)*t/12) for t in range(13)]
    cv.poly(pts, C["member"], 2.0)

def bearing(cv, x, kind):
    if kind == "roller":
        r = BH/2
        cv.circle((x, YT + r), r, "#FFFFFF", C["member"], 2.0)
    else:
        cv.polygon([(x, YB), (x - BH*0.75, YT), (x + BH*0.75, YT)], "#FFFFFF", C["member"], 2.0)

def fig1():
    cv = fit(900, 430, (-EXT - 0.3, 3*L + EXT + 1.2), (-0.7, YB + D + 1.0), L=12, R=12, T=12, B=36)
    # 上構：中間三跨＋兩端延續段，梁段在墩頂斷開（#3、#10）
    girder(cv, XP[0] - EXT, XP[0] - G/2); brk(cv, XP[0] - EXT, -1)
    for i in range(3): girder(cv, XP[i] + G/2, XP[i+1] - G/2)
    girder(cv, XP[3] + G/2, XP[3] + EXT); brk(cv, XP[3] + EXT, 1)
    for x, k in zip(XP, KIND):
        cv.polygon([(x - PW/2, 0), (x + PW/2, 0), (x + PW/2, YT), (x - PW/2, YT)], "#F3F4F6", C["member"], 2.2)  # 墩柱 #8
        cv.support((x, 0), "fixed", size=22)                                                              # #4
        for s in (-1, 1): bearing(cv, x + s*PW*0.30, k)                                                   # #2、#5
        cv.math((x, YT/2), "EI", 17, C["text"])                                                           # #8
    for i in range(3):                                                                                    # #6
        cv.dim((XP[i], YB + D), (XP[i+1], YB + D), "L", off=-26, size=17)
    cv.dim((XP[3] + PW/2 + 0.55, 0), (XP[3] + PW/2 + 0.55, YT), "L", off=26, size=17)                                # #7
    cv.text_px(450, 412, "○ 滾支承（第 1、3 墩兩側梁端）　△ 鉸支承（第 2、4 墩兩側梁端）；上構單位長度質量 m，墩柱不計質量", 13.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")

FIGURES = [(fig1, "第 1、3 墩為雙滾、第 2、4 墩為雙鉸（舊解讀成全部銷接、整橋 4 墩一起側移）")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
