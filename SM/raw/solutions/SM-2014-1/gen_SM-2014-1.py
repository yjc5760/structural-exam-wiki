# -*- coding: utf-8 -*-
"""SM-2014-1 圖解。
fig-1-problem：題目附圖（圖一）重繪，幾何只取自題目正本 SM-2014-1-problem.md §4 判讀清單（#1–#8），不含任何解題結果。
用法：python gen_SM-2014-1.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單 ─────────────────────────────
BETA = 15.0     # #3 坡角
H    = 6.0      # #1 地表→岩層介面，鉛直（已確認）
HW   = 1.5      # #2 地表→水位，鉛直
t = math.tan(math.radians(BETA))

def fig_problem():
    W, H_ = 960, 500
    X0, X1 = 0.0, 24.0
    cv = Canvas(W, H_, bg="#FFFFFF", **fit(W, H_, (X0 - 4.5, X1 + 5.5), (-H - 1.2, t * X1 + 1.6), 30, 30, 40, 40))
    s = lambda x, d: (x, t * x - d)          # 地表下鉛直深度 d 的點
    cv.polygon([s(X0, 0), s(X1, 0), s(X1, HW), s(X0, HW)], "rgba(180,83,9,0.12)")
    cv.polygon([s(X0, HW), s(X1, HW), s(X1, H), s(X0, H)], "rgba(180,83,9,0.26)")
    cv.polygon([s(X0, H), s(X1, H), s(X1, H + 1.0), s(X0, H + 1.0)], "rgba(63,74,90,0.30)")
    cv.line(s(X0, 0), s(X1, 0), C["member"], 2.6)
    cv.line(s(X0, HW), s(X1, HW), C["deform"], 1.8, dash="8 5")
    cv.line(s(X0, H), s(X1, H), C["member"], 2.6)
    wt(cv, 15.0, t * 15.0 - HW, 0.22)
    # 坡角
    cv.line(s(1.0, 0), (6.0, t * 1.0), C["dim"], 1.1)
    cv.text_px(cv.X(6.6), cv.Y(t * 1.0 + 0.35), "15°", 13, C["dim"], weight="700")
    # 滲流箭頭（#5，平行坡面向下坡）
    for k, (xa, dd) in enumerate([(14.0, 2.6), (15.0, 3.4), (16.0, 4.2)]):
        p0 = s(xa + 3.0, dd); p1 = s(xa, dd)
        cv.arrow(p0, p1, C["deform"], 2.0, 9)
    cv.text_px(cv.X(19.6), cv.Y(t * 19.6 - 2.5), "滲流（平行坡面）", 12.5, C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(10.5), cv.Y(t * 10.5 - 0.75), "ω = 24%（水位以上）", 12.5, C["text"])
    cv.text_px(cv.X(5.5), cv.Y(t * 5.5 - 4.0), "Gs = 2.64，ω = 35%（水位以下）", 12.5, C["text"])
    cv.text_px(cv.X(9.0), cv.Y(t * 9.0 - 6.6), "岩層", 13, C["text"], weight="700")
    cv.text_px(cv.X(15.0), cv.Y(t * 15.0 - 7.15), "介面 c = 15 kPa，φ = 20°", 12.5, C["text"], anchor="start", weight="700")
    # 尺寸線（鉛直，#1、#2）
    cv.dim((X0 - 1.2, -H), (X0 - 1.2, 0), "6 m", 0, C["dim"], 12.5, label_off=-24)
    cv.line((X0 - 1.6, 0), (X0, 0), C["dim"], 0.9, dash="2 3")
    cv.line((X0 - 1.6, -H), (X0, -H), C["dim"], 0.9, dash="2 3")
    xr = X1 + 1.2
    cv.dim((xr, t * X1 - HW), (xr, t * X1), "1.5 m", 0, C["dim"], 12.5, label_off=24)
    cv.line((X1, t * X1), (xr + 0.4, t * X1), C["dim"], 0.9, dash="2 3")
    cv.line((X1, t * X1 - HW), (xr + 0.4, t * X1 - HW), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2014-1 題目附圖（圖一）重繪",
        sub="依題目正本判讀清單；6 m 與 1.5 m 皆為鉛直量測，三線平行、坡角 15°",
        note="攔錯用：尺寸線是鉛直的，6 m 是鉛直深度（不是垂直坡面的厚度）；水位以下飽和、以上 ω = 24%。",
        path=os.path.join(OUT, "SM-2014-1-fig-1-problem.svg"))
