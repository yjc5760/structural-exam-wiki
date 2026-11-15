#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2020-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2020-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2020-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2020-4"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2020-4-problem.md §4）──
LS = 15.0                      # #1 兩跨各 15 m
H = 90.0                       # #2 斷面 50×90
EB = 35.0                      # #4 支承 B 鋼腱在形心上 35 cm
ED = -25.0                     # e_D、e_E 為待求量：只取示意幅度
VX = 0.024
PW, PH = 1260, 420


def span_curve(x):
    # 每跨一條拋物線：支承端 0、B 端 +35，中點示意（不代表答案）
    s = x if x <= LS else 2 * LS - x
    t = s / LS
    a_ = 2 * (EB - 2 * ED)
    b_ = EB - a_
    return (a_ * t * t + b_ * t) * VX


def panel_beam():
    cv = Canvas(PW, PH, sx=30, ox=70, oy=190)
    y0 = -H / 2 * VX
    _rect(cv, 0, y0, 2 * LS, -y0)
    cv.line((0, 0), (2 * LS, 0), C["muted"], 1.2, dash="5 4")
    _curve(cv, span_curve, 0, LS, TENDON, 2.4)
    _curve(cv, span_curve, LS, 2 * LS, TENDON, 2.4)
    cv.support((0, y0), "pin", size=14)
    cv.support((LS, y0), "roller", size=14)
    cv.support((2 * LS, y0), "roller", size=14)
    for x, n in ((0, "A"), (LS, "B"), (2 * LS, "C"), (LS / 2, "D"), (1.5 * LS, "E")):
        cv.text((x - 0.95 if n in "ABC" else x, y0 - 0.75), n, 15, weight="700")
    for x, n in ((LS / 2, "e_{D}"), (1.5 * LS, "e_{E}")):
        cv.double_arrow((x, 0), (x, span_curve(x)), C["text"], 1.5, 7)
        cv.math((x + 0.4, span_curve(x) / 2), n, 14, anchor="start")
        cv.text((x + 1.5, span_curve(x) / 2), "（待求）", 12, color=C["muted"], anchor="start")
    cv.dim((LS + 1.6, 0), (LS + 1.6, EB * VX), "35 cm", off=-4, label_off=30)
    cv.udl((0, -y0), (2 * LS, -y0), 1.5, n=21)
    cv.math((LS, -y0 + 2.1), "w = 1.6 tf/m（含自重）", 15, color=C["load"])
    cv.dim((0, y0), (LS, y0), "1500", off=62, label_off=14)
    cv.dim((LS, y0), (2 * LS, y0), "1500", off=62, label_off=14)
    cv.dim((0, y0), (LS / 2, y0), "750", off=100, label_off=14)
    cv.dim((1.5 * LS, y0), (2 * LS, y0), "750", off=100, label_off=14)
    cv.text((LS, -5.9), "單位：cm；虛線為斷面形心；鋼腱 A、C 端無偏心；立面豎向放大示意", 12.5, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=1.9, ox=1080, oy=200)
    _rect(cv, 0, 0, 50, 90)
    cv.dim((0, 0), (50, 0), "50", off=28, label_off=14)
    cv.dim((50, 0), (50, 90), "90", off=24, label_off=20)
    return cv


def fig1_problem():
    a = panel_beam()
    a.parts += panel_sec().parts
    return compose([a], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#7；e_D、e_E 幅度為示意（待求量）".replace("_", ""),
                   note="兩跨連續梁：A 鉸支承、B 與 C 滾支承；鋼腱每跨一條拋物線，於 B 點相交")


FIGURES = [("1-problem", fig1_problem, "B 點 35 cm 讀成形心下方；漏看 A、C 端偏心為 0；D、E 當支承")]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
