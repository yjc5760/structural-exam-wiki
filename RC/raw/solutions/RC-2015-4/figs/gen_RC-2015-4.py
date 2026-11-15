#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2015-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2015-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2015-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2015-4"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2015-4-problem.md §4）──
L = 12.0               # #1 跨度 12 m
HD = 1.5               # 梁深 50 cm（立面高度放大示意）
EPD = 0.45             # e_p 示意幅度（數值待求）
PW, PH = 1060, 330


def panel_beam():
    cv = Canvas(PW, PH, sx=52, ox=72, oy=130)
    _rect(cv, 0, 0, L, HD)
    yc = HD / 2
    cv.line((-0.6, yc), (L + 0.6, yc), C["muted"], 1.3, dash="10 5")
    f = lambda x: yc - EPD * (1 - (2 * x / L - 1) ** 2)
    _curve(cv, f, 0, L, TENDON, 2.6, dash="9 5")
    cv.arrow((-1.1, yc + 0.75), (0, yc), C["load"], 3.0, 11)
    cv.arrow((L + 1.1, yc + 0.75), (L, yc), C["load"], 3.0, 11)
    cv.math((-1.25, yc + 1.0), "F", 16, color=C["load"])
    cv.math((L + 1.25, yc + 1.0), "F", 16, color=C["load"])
    cv.double_arrow((L / 2, yc), (L / 2, yc - EPD), C["text"], 1.6, 7)
    cv.math((L / 2 + 0.25, yc - EPD / 2), "e_{p}", 15, anchor="start")
    cv.support((0, 0), "roller", size=15)
    cv.support((L, 0), "pin", size=15)
    cv.udl((0, HD), (L, HD), 0.9, n=13)
    cv.math((L / 2, HD + 1.2), "w_{L}", 16, color=C["load"])
    cv.dim((0, 0), (L, 0), "L = 12 m", off=62, label_off=16)
    cv.text((L / 2, -2.0), "端部無偏心之拋物線鋼鍵（後拉法）；梁深方向放大示意", 12.5, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=4.4, ox=800, oy=80)
    _rect(cv, 0, 0, 30, 50)
    cv.line((-8, 25), (38, 25), C["muted"], 1.3, dash="10 5")
    cv.circle((15, 12), 1.3, fill=TENDON, stroke=TENDON, w=1)
    cv.dim((0, 0), (30, 0), "30 cm", off=30, label_off=14)
    cv.dim((30, 0), (30, 50), "50 cm", off=34, label_off=30)
    cv.text((15, -17), "斷面（鋼鍵位置示意）", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    a = panel_beam()
    a.parts += panel_sec().parts          # 斷面另用一個比例，疊在同一張畫布右側
    return compose([a], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#6；跨中偏心量 ep 為待求量，曲線幅度只是示意",
                   note="左端滾支承、右端鉸支承；施預力時與全部載重時之預力皆為 F（考卷未給損失）")


FIGURES = [("1-problem", fig1_problem, "把端部當成有偏心；把施預力與使用階段預力分成兩值")]


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
