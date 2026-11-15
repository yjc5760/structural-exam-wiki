# -*- coding: utf-8 -*-
"""SM-2004-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2004-4-problem.md §4 判讀清單（#1–#4），不含任何解題結果。
用法：python gen_SM-2004-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
LAYERS = [("砂", "N = 3~9", 2.0), ("黏土", "N = 4~8", 4.0), ("砂", "N = 7~39", 8.0),
          ("黏土", "N = 6~10", 4.0)]           # #1 由上而下、厚度（m）
BOT = ("砂", "N = 14~39")                      # #1 最下層（厚度未標）
D_TANK, H_TANK = 60.0, 18.0                     # #3 油槽寬（直徑）、高
WT = 1.0                                        # #2 水位在最上層砂內，圖上未標深度——此處示意
PAD = 1.2                                       # #4 墊層厚度未標——示意
VEX = 2.5                                       # 地層深度方向放大倍率（考卷附圖亦未按比例）
FILL = {"砂": "rgba(180,83,9,0.20)", "黏土": "rgba(63,74,90,0.22)"}

def fig_problem():
    W, H = 900, 640
    XL, XR = -42.0, 42.0
    ZB = sum(t for _, _, t in LAYERS) + 3.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL, XR + 14), (-ZB * VEX, H_TANK + PAD + 5), 30, 20, 20, 20))
    Y = lambda d: -d * VEX
    z = 0.0
    for name, n, t in LAYERS:
        soil_fill(cv, XL, XR, Y(z + t), Y(z), FILL[name])
        cv.line((XL, Y(z + t)), (XR, Y(z + t)), C["member2"], 1.5)
        cv.text_px(cv.X(-6), cv.Y(Y(z + t/2)), name, 13, C["text"], anchor="end", weight="700")
        cv.math_px(cv.X(2), cv.Y(Y(z + t/2)), n, 13, C["text"], anchor="start")
        cv.dim((XR + 3, Y(z + t)), (XR + 3, Y(z)), "%g m" % t, 0, C["dim"], 12.5, label_off=24)
        z += t
    soil_fill(cv, XL, XR, Y(ZB), Y(z), FILL[BOT[0]])
    cv.text_px(cv.X(-6), cv.Y(Y(z + 1.5)), BOT[0], 13, C["text"], anchor="end", weight="700")
    cv.math_px(cv.X(2), cv.Y(Y(z + 1.5)), BOT[1], 13, C["text"], anchor="start")
    cv.text_px(cv.X(XR + 3), cv.Y(Y(z + 1.5)), "（厚度未標）", 11.5, C["muted"], anchor="start")
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    # 墊層（梯形，略寬於槽）與油槽
    cv.polygon([(-D_TANK/2 - 4, 0), (D_TANK/2 + 4, 0), (D_TANK/2 + 1.5, PAD), (-D_TANK/2 - 1.5, PAD)],
               "rgba(138,148,166,0.30)", C["member"], 1.6)
    cv.polygon([(-D_TANK/2, PAD), (D_TANK/2, PAD), (D_TANK/2, PAD + H_TANK), (-D_TANK/2, PAD + H_TANK)],
               "rgba(29,78,216,0.10)", C["member"], 2.4)
    cv.text_px(cv.X(0), cv.Y(PAD + H_TANK/2), "油槽", 18, C["text"], weight="700")
    cv.dim((-D_TANK/2, PAD + H_TANK + 3), (D_TANK/2, PAD + H_TANK + 3), "60 m", 0, C["dim"], 13, label_off=14)
    cv.dim((XR + 3, PAD), (XR + 3, PAD + H_TANK), "18 m", 0, C["dim"], 13, label_off=22)
    cv.line((D_TANK/2, PAD + H_TANK), (XR + 3.2, PAD + H_TANK), C["dim"], 0.9, dash="2 3")
    cv.line((D_TANK/2 + 1.5, PAD), (XR + 3.2, PAD), C["dim"], 0.9, dash="2 3")
    # 地下水位（最上層砂內，示意）
    cv.line((XL, Y(WT)), (-14, Y(WT)), C["deform"], 1.8, dash="8 5")
    wt_symbol(cv, -38.5, Y(WT), C["deform"], 0.45)
    cv.text_px(cv.X(-36.8), cv.Y(Y(WT)) + 10, "G.W.T.（未標深度）", 11.5, C["deform"], anchor="start", weight="700")
    return cv

compose([fig_problem()],
        title="SM-2004-4 題目附圖重繪",
        sub="依題目正本判讀清單；地下水位在最上層砂內（考卷未標深度，位置示意），墊層厚度示意；地層深度方向放大 2.5 倍",
        note="攔錯用：兩層黏土分別在 2–6 m 與 14–18 m；水位在地表下 2 m 以內的淺層砂中，不是 2 m 砂層底。",
        path=os.path.join(OUT, "SM-2004-4-fig-1-problem.svg"))
