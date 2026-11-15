#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2021-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2021-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2021-3.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-1／U3-2 題目正本推廣・批 1）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2021-3"
PW, PH = 560, 520          # 各子圖畫布尺寸（px，compose 要求相同）


def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


# ── 判讀清單數值（題目正本 §4）──
BC = 260.0                       # 樁帽 260×260
E_P = 40.0                       # #2 樁中心距樁帽邊 40 → 樁位 ±90
XP = BC / 2 - E_P                # 90
DP = 30.0                        # #3 基樁直徑 30（D30）
CC = 50.0                        # #4 柱 50×50 置中
D_CAP = 55.0                     # #8 樁帽厚 55
C_BOT = 10.0                     # #1 樁帽底面至底部主筋 10
EX_DRAW = 18.0                   # #5 e_x 為所求；圖上偏移量僅示意


def panel_plan():
    cv = Canvas(PW, PH, sx=1.35, ox=PW / 2 + 30, oy=PH / 2 + 8)
    h = BC / 2
    _rect(cv, -h, -h, h, h, fill="#EDF1F6")
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            cv.circle((sx_ * XP, sy_ * XP), DP / 2, fill="#FFFFFF", stroke=C["member"], w=1.6, dash="5 4")
    _rect(cv, -CC / 2, -CC / 2, CC / 2, CC / 2, fill="#C9D1DC", w=2.0)
    cv.line((0, 0), (h + 40, 0), C["muted"], 1.2, dash="10 5")          # 考卷 x 軸由中心往右
    cv.line((0, 0), (0, h + 40), C["muted"], 1.2, dash="10 5")          # 考卷 y 軸由中心往上
    cv.math((h + 50, 0), "x", 15, color=C["muted"])
    cv.math((0, h + 50), "y", 15, color=C["muted"])
    cv.text((XP + 22, XP + 26), "D30（樁徑）", 12, anchor="start", color=C["muted"])
    cv.dim((-h, -h), (-XP, -h), "40", off=24, label_off=13)
    cv.dim((-XP, -h), (XP, -h), "180", off=24, label_off=13)
    cv.dim((XP, -h), (h, -h), "40", off=24, label_off=13)
    cv.dim((-h, -h), (h, -h), "260", off=58, label_off=13)
    cv.dim((-h, h), (-h, XP), "40", off=24, label_off=16)
    cv.dim((-h, XP), (-h, -XP), "180", off=24, label_off=20)
    cv.dim((-h, -XP), (-h, -h), "40", off=24, label_off=16)
    cv.dim((-h, h), (-h, -h), "260", off=60, label_off=20)
    cv.dim((-CC / 2, -CC / 2), (CC / 2, -CC / 2), "50", off=16, label_off=12)
    cv.dim((-CC / 2, CC / 2), (-CC / 2, -CC / 2), "50", off=16, label_off=14)
    cv.text((-h - 60, h + 30), "圖三之一 平面（單位 cm）", 13, color=C["muted"], anchor="start")
    return cv


def panel_elev():
    cv = Canvas(PW, PH, sx=1.35, ox=PW / 2 - 6, oy=150)
    h = BC / 2
    _rect(cv, -h, 0, h, D_CAP)                                     # 樁帽
    _rect(cv, -CC / 2, D_CAP, CC / 2, D_CAP + 95)                  # 柱
    for sx_ in (-1, 1):                                            # 基樁（下方截斷）
        x = sx_ * XP
        cv.poly([(x - DP / 2, 0), (x - DP / 2, -55)], C["member"], 1.8)
        cv.poly([(x + DP / 2, 0), (x + DP / 2, -55)], C["member"], 1.8)
        cv.poly([(x - DP / 2 - 4, -55), (x - 3, -55), (x + 1, -50), (x + 3, -60), (x + DP / 2 + 4, -55)], C["member"], 1.4)
    yb = C_BOT                                                     # #1 底部主筋
    cv.poly([(-h + 8, D_CAP - 14), (-h + 8, yb), (h - 8, yb), (h - 8, D_CAP - 14)], C["member"], 3.4)
    cv.line((0, -70), (0, D_CAP + 130), C["muted"], 1.2, dash="10 5")
    cv.arrow((EX_DRAW, D_CAP + 150), (EX_DRAW, D_CAP + 97), C["load"], 3.2)
    cv.math((EX_DRAW + 6, D_CAP + 160), "P_{u} = 100 tf", 14, color=C["load"], anchor="start")
    cv.dim((0, D_CAP + 118), (EX_DRAW, D_CAP + 118), "e_{x}", off=-1, label_off=-14)
    cv.dim((h, D_CAP), (h, 0), "D = 55", off=-26, label_off=-34)
    cv.dim((-h, 0), (-h, yb), "", off=-22, label_off=0)
    cv.math((-h - 34, yb / 2), "10", 14, color=C["dim"])
    cv.text((0, -95), "圖三之二 立面（沿 x 軸；e_x 量值為所求，圖上為示意）", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_plan(), panel_elev()], title=f"{TAG} 題目附圖（圖三之一、之二重繪）",
                   sub="依題目正本判讀清單 #1–#8；樁長、柱高、偏心距圖上大小為示意",
                   note="樁中心距樁帽邊 40（樁位 ±90）；10 為樁帽底面至底部主筋中心")


FIGURES = [("1-problem", fig1_problem, "樁位量到樁邊而非樁心；10 cm 的量測基準")]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
