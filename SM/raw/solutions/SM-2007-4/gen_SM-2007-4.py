# -*- coding: utf-8 -*-
"""SM-2007-4 圖解。
fig-1-problem：題目圖一重繪，幾何只取自題目正本 SM-2007-4-problem.md §4 判讀清單，不含任何解題結果
（D、x、T 為所求，只畫成「？」；錨碇板位置與版樁底深度為示意）。
用法：python gen_SM-2007-4.py [輸出資料夾]（預設本題 figs/）"""
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
H_EXC = 7.5    # 開挖深度 H（版樁頂＝背側地表 → 開挖面）
Z_ANC = 1.5    # 地錨深度（版樁頂下）
X_PLT = 6.0    # 錨碇板位置（示意；x 為所求）
D_SK  = 4.0    # 版樁入土段（示意；D 為所求）


def fig_problem():
    Wd, Ht = 760, 640
    XL, XR = -4.0, 8.2
    cv = Canvas(Wd, Ht, bg="#FFFFFF", **fit(Wd, Ht, (XL - 1.2, XR + 0.4), (-(H_EXC + D_SK + 0.9), 1.4), 120, 30, 50, 40))
    Y = lambda d: -d
    soil_fill(cv, 0, XR, Y(H_EXC), Y(0), SAND)
    soil_fill(cv, XL, XR, Y(H_EXC + D_SK + 0.5), Y(H_EXC), SAND2)
    cv.line((0, Y(0)), (XR, Y(0)), C["member"], 2.4)
    ground(cv, 5.0, 7.4, Y(0), 4, 0.3)
    cv.line((XL, Y(H_EXC)), (0, Y(H_EXC)), C["member"], 2.4)
    ground(cv, XL + 0.6, -1.0, Y(H_EXC), 4, 0.3)
    cv.line((0, Y(H_EXC)), (XR, Y(H_EXC)), C["member2"], 1.6, dash="7 5")
    wall(cv, 0, Y(0), Y(H_EXC + D_SK))
    # 地錨拉桿＋錨碇板
    cv.line((0, Y(Z_ANC)), (X_PLT, Y(Z_ANC)), C["load"], 2.4)
    cv.polygon([(X_PLT, Y(Z_ANC - 0.45)), (X_PLT + 0.22, Y(Z_ANC - 0.45)),
                (X_PLT + 0.22, Y(Z_ANC + 0.45)), (X_PLT, Y(Z_ANC + 0.45))], "#FFFFFF", C["load"], 2.0)
    cv.text_px(cv.X(3.6), cv.Y(Y(Z_ANC)) - 16, "地錨 T = ？", 14, C["load"], weight="700")
    # 層名與參數
    cv.text_px(cv.X(0.5), cv.Y(Y(3.2)), "砂土層", 14, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(0.5), cv.Y(Y(4.1)), "φ_{s} = 30°", 14, C["text"], anchor="start")
    cv.math_px(cv.X(0.5), cv.Y(Y(4.9)), "γ_{s} = 17.3 kN/m^{3}", 14, C["text"], anchor="start")
    cv.math_px(cv.X(0.5), cv.Y(Y(5.7)), "c_{s} = 0", 14, C["text"], anchor="start")
    cv.text_px(cv.X(0.5), cv.Y(Y(H_EXC + 0.9)), "中等緊密砂土層", 14, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(0.5), cv.Y(Y(H_EXC + 1.8)), "φ = 35°", 14, C["text"], anchor="start")
    cv.math_px(cv.X(0.5), cv.Y(Y(H_EXC + 2.6)), "γ = 18 kN/m^{3}", 14, C["text"], anchor="start")
    cv.math_px(cv.X(0.5), cv.Y(Y(H_EXC + 3.4)), "c = 0", 14, C["text"], anchor="start")
    cv.text_px(cv.X(-2.2), cv.Y(Y(H_EXC + 2.3)), "開挖側", 13, C["muted"])
    # 尺寸線
    xd = XL - 0.4
    cv.dim((xd, Y(H_EXC)), (xd, Y(0)), "H = 7.5 m", 0, C["dim"], 13, label_off=-44)
    cv.dim((xd, Y(H_EXC + D_SK)), (xd, Y(H_EXC)), "D = ?", 0, C["dim"], 13, label_off=-34)
    for d in (0, H_EXC, H_EXC + D_SK):
        cv.line((xd - 0.12, Y(d)), (-0.1, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.dim((-0.9, Y(Z_ANC)), (-0.9, Y(0)), "1.5 m", 0, C["dim"], 12.5, label_off=-30)
    cv.dim((0, Y(-0.9)), (X_PLT + 0.11, Y(-0.9)), "x = ?", 0, C["dim"], 13, label_off=14)
    return cv


compose([fig_problem()],
        title="SM-2007-4 題目附圖（圖一）重繪",
        sub="依題目正本判讀清單；地下水位以上，固定土壤支撐法",
        note="攔錯用：H = 7.5 m 量到開挖面、地錨在頂下 1.5 m；x 由版樁量到錨碇板；開挖面以下兩側都是中等緊密砂土。",
        path=os.path.join(OUT, "SM-2007-4-fig-1-problem.svg"))
