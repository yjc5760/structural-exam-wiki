# -*- coding: utf-8 -*-
"""SM-2023-2 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2023-2-problem.md §4 判讀清單（#1–#5），不含任何解題結果。
用法：python gen_SM-2023-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H  = 8.0     # #1
AF = 60.0    # #2 坡面 AC
AP = 45.0    # #3 破壞面 AB
A = (0.0, 0.0)
C_ = (H / math.tan(math.radians(AF)), H)
B = (H / math.tan(math.radians(AP)), H)

def arc(cv, r, a0, a1, col):
    pts = [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a))) for a in [a0 + (a1 - a0) * i / 40 for i in range(41)]]
    cv.poly(pts, col, 1.4)

def fig_problem():
    W, H_ = 820, 440
    cv = Canvas(W, H_, bg="#FFFFFF", **fit(W, H_, (-7.0, B[0] + 6.0), (-1.2, H + 1.6), 40, 40, 40, 40))
    cv.polygon([A, C_, B], "rgba(180,83,9,0.20)")
    cv.poly([(-6.0, 0), A, C_, (B[0] + 5.0, H)], C["member"], 2.6)
    cv.line(A, B, C["load"], 2.2, dash="9 5")
    cv.line(A, (B[0] + 2.0, 0), C["member"], 1.2)
    arc(cv, 2.2, 0, AP, C["dim"]); arc(cv, 4.6, 0, AF, C["dim"])
    cv.text_px(cv.X(2.6), cv.Y(0.75), "45°", 13, C["dim"], weight="700")
    cv.text_px(cv.X(4.9), cv.Y(2.6), "60°", 13, C["dim"], weight="700")
    cv.text_px(cv.X(A[0] - 0.4), cv.Y(0.5), "A", 15, C["text"], weight="700", anchor="end")
    cv.text_px(cv.X(C_[0]), cv.Y(H + 0.7), "C", 15, C["text"], weight="700")
    cv.text_px(cv.X(B[0]), cv.Y(H + 0.7), "B", 15, C["text"], weight="700")
    cv.text_px(cv.X(B[0] + 1.0), cv.Y(4.0), "假設破壞面 AB（平面）", 12.5, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(B[0] + 1.0), cv.Y(3.1), "㈠ c = 50 kPa，φ = 36°", 12, C["text"], anchor="start")
    cv.text_px(cv.X(B[0] + 1.0), cv.Y(2.3), "㈡ c = 5 kPa，φ = 36°", 12, C["text"], anchor="start")
    cv.text_px(cv.X((A[0] + C_[0] + B[0]) / 3 + 0.4), cv.Y(H * 0.66), "γ = 20 kN/m³", 12, C["text"])
    xd = -4.0
    cv.dim((xd, 0), (xd, H), "H = 8 m", 0, C["dim"], 12.5, label_off=-34)
    cv.line((xd - 0.3, H), (C_[0], H), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2023-2 題目附圖重繪",
        sub="依題目正本判讀清單；坡面 AC 60°、破壞面 AB 45°，坡頂面水平",
        note="攔錯用：滑動楔體是 ABC（夾在 60° 坡面與 45° 破壞面之間），不是整個坡體；考卷沒有給水位。",
        path=os.path.join(OUT, "SM-2023-2-fig-1-problem.svg"))
