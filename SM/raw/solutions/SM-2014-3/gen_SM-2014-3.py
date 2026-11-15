# -*- coding: utf-8 -*-
"""SM-2014-3 圖解。
fig-1-problem：題目圖三重繪，幾何只取自題目正本 SM-2014-3-problem.md §4 判讀清單，不含任何解題結果
（鈑樁貫入段長度為所求，只畫示意）。
用法：python gen_SM-2014-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
SAND, SAND2, CLAY = "rgba(180,83,9,0.12)", "rgba(180,83,9,0.24)", "rgba(63,74,90,0.20)"


def ground(cv, x0, x1, y, n=4, s=0.35):
    """地面剖線（短斜線）。"""
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        cv.line((x, y), (x - s, y - s), C["member"], 1.3)


def wall(cv, x, y0, y1, t=0.18, fill="#3F4A5A"):
    cv.polygon([(x - t / 2, y0), (x + t / 2, y0), (x + t / 2, y1), (x - t / 2, y1)], fill)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_EXC = 4.5    # 開挖深度（＝砂土厚）
Z_ANC = 1.0    # 地錨（頂下）
Z_WT  = 2.1    # 背側地下水位
D_SK  = 2.6    # 黏土內貫入段（示意；所求）


def fig_problem():
    Wd, Ht = 860, 560
    XL, XR = -3.6, 7.6
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 1.3, XR + 0.2), (-(H_EXC + D_SK + 0.6), 1.0), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, 0, XR, Y(Z_WT), Y(0), SAND)
    soil_fill(cv, 0, XR, Y(H_EXC), Y(Z_WT), SAND2)
    soil_fill(cv, XL, XR, Y(H_EXC + D_SK + 0.4), Y(H_EXC), CLAY)
    cv.line((0, Y(0)), (XR, Y(0)), C["member"], 2.4)
    cv.line((0, Y(Z_WT)), (XR, Y(Z_WT)), C["deform"], 1.4, dash="7 4")
    wt_symbol(cv, 1.6, Y(Z_WT), C["deform"], 0.1)
    cv.line((XL, Y(H_EXC)), (XR, Y(H_EXC)), C["member"], 2.0)
    wt_symbol(cv, -2.2, Y(H_EXC), C["deform"], 0.1)
    wall(cv, 0, Y(0), Y(H_EXC + D_SK), 0.16)
    cv.arrow((0.1, Y(Z_ANC)), (2.4, Y(Z_ANC)), C["load"], 2.6, 10)
    cv.text_px(cv.X(1.2), cv.Y(Y(Z_ANC)) - 15, "地錨", 13.5, C["load"], weight="700")
    cv.text_px(cv.X(-0.4), cv.Y(Y(3.4)), "鈑樁", 13, C["muted"], anchor="end")
    cv.math_px(cv.X(4.0), cv.Y(Y(1.05)), "γ = 16.2 kN/m^{3}", 14, C["text"])
    cv.text_px(cv.X(1.0), cv.Y(Y(3.0)), "砂土", 14, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(2.6), cv.Y(Y(3.0)), "φ = 30°, c = 0", 14, C["text"], anchor="start")
    cv.math_px(cv.X(2.6), cv.Y(Y(3.8)), "γ_{sat} = 18.51 kN/m^{3}", 14, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(5.4)), "黏土", 14, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(2.6), cv.Y(Y(5.4)), "φ = 0, S_{u} = 50 kPa", 14, C["text"], anchor="start")
    cv.math_px(cv.X(2.6), cv.Y(Y(6.2)), "γ_{sat} = 19.11 kN/m^{3}", 14, C["text"], anchor="start")
    cv.text_px(cv.X(-1.8), cv.Y(Y(2.2)), "開挖側", 13, C["muted"])
    # 尺寸線
    xd = XL - 0.4
    cv.dim((xd, Y(H_EXC)), (xd, Y(0)), "4.5 m", 0, C["dim"], 12.5, label_off=-28)
    for d in (0, H_EXC):
        cv.line((xd - 0.12, Y(d)), (-0.1 if d == 0 else XL, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.dim((3.0, Y(Z_ANC)), (3.0, Y(0)), "1 m", 0, C["dim"], 12, label_off=20)
    cv.dim((XR - 0.5, Y(Z_WT)), (XR - 0.5, Y(0)), "2.1 m", 0, C["dim"], 12, label_off=-26)
    return cv


compose([fig_problem()],
        title="SM-2014-3 題目附圖（圖三）重繪",
        sub="依題目正本判讀清單；背側水位地表下 2.1 m，開挖側水位降至開挖面",
        note="攔錯用：2.1 m 是地表到背側水位，地錨在頂下 1 m；兩側水位差 2.4 m，開挖面以下兩側都是黏土。",
        path=os.path.join(OUT, "SM-2014-3-fig-1-problem.svg"))
