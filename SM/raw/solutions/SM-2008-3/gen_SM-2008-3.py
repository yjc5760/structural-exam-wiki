# -*- coding: utf-8 -*-
"""SM-2008-3 圖解。
fig-1-problem：題目圖二重繪，幾何只取自題目正本 SM-2008-3-problem.md §4 判讀清單，不含任何解題結果。
用法：python gen_SM-2008-3.py [輸出資料夾]（預設本題 figs/）"""
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
Z_FILL = 3.0    # 回填土底＝背側地下水位（地表下）
H_EXC  = 16.0   # 開挖深度（A → C）
Z_STR  = 13.0   # 最下階支撐 B（C 上方 3 m）
L_WALL = 25.0   # 連續壁總深（A → D）


def fig_problem():
    Wd, Ht = 820, 760
    XL, XR = -7.0, 11.0
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 1.5, XR + 2.0), (-(L_WALL + 1.6), 1.6), 40, 40, 50, 40))
    Y = lambda d: -d
    soil_fill(cv, 0, XR, Y(Z_FILL), Y(0), SAND)
    soil_fill(cv, 0, XR, Y(L_WALL + 1.0), Y(Z_FILL), CLAY)
    soil_fill(cv, XL, 0, Y(L_WALL + 1.0), Y(H_EXC), CLAY)
    cv.line((0, Y(0)), (XR, Y(0)), C["member"], 2.4)
    ground(cv, 6.0, 9.0, Y(0), 4, 0.45)
    cv.line((0, Y(Z_FILL)), (XR, Y(Z_FILL)), C["member2"], 1.6)
    cv.line((XL, Y(H_EXC)), (0, Y(H_EXC)), C["member"], 2.4)
    wall(cv, 0, Y(0), Y(L_WALL), 0.4)
    wt_symbol(cv, 8.6, Y(Z_FILL), C["deform"], 0.17)
    wt_symbol(cv, -3.6, Y(H_EXC), C["deform"], 0.17)
    cv.arrow((-3.2, Y(Z_STR)), (-0.25, Y(Z_STR)), C["load"], 2.6, 10)
    cv.text_px(cv.X(-3.6), cv.Y(Y(Z_STR)) - 18, "最下階支撐", 13, C["text"], anchor="middle")
    for lab, d in (("A", 0), ("B", Z_STR), ("C", H_EXC), ("D", L_WALL)):
        cv.text_px(cv.X(0.55), cv.Y(Y(d)) + (14 if d > 0 else -12), lab, 14, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(1.0), cv.Y(Y(1.5)), "回填土", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(3.4), cv.Y(Y(1.5)), "γ_{t} = 18 kN/m^{3}", 13.5, C["text"], anchor="start")
    cv.text_px(cv.X(4.5), cv.Y(Y(8.5)), "黏土層", 14, C["text"], weight="700")
    cv.math_px(cv.X(4.5), cv.Y(Y(10.0)), "γ_{sat} = 20 kN/m^{3}", 13.5, C["text"])
    cv.math_px(cv.X(4.5), cv.Y(Y(11.4)), "S_{u}/σ'_{v0} = 0.25", 13.5, C["text"])
    cv.text_px(cv.X(-5.0), cv.Y(Y(H_EXC)) + 24, "最終開挖面", 13, C["muted"])
    cv.text_px(cv.X(-0.5), cv.Y(Y(6.0)), "連續壁", 13, C["muted"], anchor="end")
    # 尺寸線
    xl = XL - 0.6
    cv.dim((xl, Y(H_EXC)), (xl, Y(0)), "16 m", 0, C["dim"], 13, label_off=-30)
    cv.line((xl - 0.2, Y(0)), (-0.2, Y(0)), C["dim"], 0.9, dash="2 3")
    cv.line((xl - 0.2, Y(H_EXC)), (XL, Y(H_EXC)), C["dim"], 0.9, dash="2 3")
    cv.dim((-1.6, Y(H_EXC)), (-1.6, Y(Z_STR)), "3 m", 0, C["dim"], 12.5, label_off=-24)
    xr = XR + 1.0
    cv.dim((xr, Y(L_WALL)), (xr, Y(0)), "25 m", 0, C["dim"], 13, label_off=30)
    cv.line((0.2, Y(L_WALL)), (xr + 0.2, Y(L_WALL)), C["dim"], 0.9, dash="2 3")
    cv.dim((XR - 0.4, Y(Z_FILL)), (XR - 0.4, Y(0)), "3 m", 0, C["dim"], 12.5, label_off=-22)
    return cv


compose([fig_problem()],
        title="SM-2008-3 題目附圖（圖二）重繪",
        sub="依題目正本判讀清單；背側水位在回填土底，開挖側水位在開挖面",
        note="攔錯用：25 m 是壁全長（貫入 9 m），最下階支撐在地表下 13 m；兩側水位不同高。",
        path=os.path.join(OUT, "SM-2008-3-fig-1-problem.svg"))
