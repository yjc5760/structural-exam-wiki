# -*- coding: utf-8 -*-
"""SM-2025-4 圖解。
fig-1-problem：題目附圖（T 形載重平面）重繪，幾何只取自題目正本 SM-2025-4-problem.md §4 判讀清單（#1–#4），不含任何解題結果。
Newmark 影響圖是查圖用圖表，不重繪（見題目正本 §3、§4 #6）。
fig-2-split：解題圖解（2026-11-15 階段 E），以 A 為角點拆三塊矩形，數值取自解析 §4。
用法：python gen_SM-2025-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
BL, BH = 120.0, 40.0          # #1 下方長方形
SW, SH = 40.0, 40.0           # #2 凸出部寬、高
SX0 = BL - 40.0 - SW          # #3 凸出部左緣（右側段 40 m 量自凸出部右緣到長方形右端）
A = (SX0, BH)                 # #4 A 點（凹角）
Q = 200                       # 題文 均布荷重 kPa

def fig_problem():
    W, H = 900, 600
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-14, BL + 26), (-24, BH + SH + 22), 30, 30, 20, 20))
    pts = [(0, 0), (BL, 0), (BL, BH), (SX0 + SW, BH), (SX0 + SW, BH + SH), (SX0, BH + SH), (SX0, BH), (0, BH)]
    cv.polygon(pts, "rgba(192,57,43,0.12)", C["member"], 2.6)
    cv.text((BL / 2, BH / 2), "均布荷重 %d kPa" % Q, 15, C["load"], weight="700")
    cv.dot(A, 7, fill=C["text"])
    cv.text((A[0] - 3.5, A[1] + 4.5), "A", 16, C["text"], weight="700")
    cv.line((A[0], A[1]), (SX0 + SW, BH), C["member2"], 1.0, dash="4 4")
    # 尺寸線：上方兩段（#2、#3）
    yt = BH + SH + 9
    cv.dim((SX0, yt), (SX0 + SW, yt), "40 m", 0, C["dim"], 13, label_off=-14)
    cv.dim((SX0 + SW, yt), (BL, yt), "40 m", 0, C["dim"], 13, label_off=-14)
    for x, y0 in ((SX0, BH + SH), (SX0 + SW, BH + SH), (BL, BH)):
        cv.line((x, y0 + 1), (x, yt), C["dim"], 0.9, dash="2 3")
    # 右側兩段（#1、#2）
    xr = BL + 10
    cv.dim((xr, 0), (xr, BH), "40 m", 0, C["dim"], 13, label_off=22)
    cv.dim((xr, BH), (xr, BH + SH), "40 m", 0, C["dim"], 13, label_off=22)
    cv.line((SX0 + SW + 1, BH + SH), (xr, BH + SH), C["dim"], 0.9, dash="2 3")
    # 下方總寬（#1）
    cv.dim((0, -10), (BL, -10), "120 m", 0, C["dim"], 13, label_off=16)
    # 左側缺口（由 #3 推得）
    cv.dim((0, BH + 7), (SX0, BH + 7), "40 m（推得）", 0, C["muted"], 12, label_off=-13)
    return cv

compose([fig_problem()],
        title="SM-2025-4 題目附圖重繪（載重平面）",
        sub="依題目正本判讀清單；上方第二段 40 m 量自凸出部右緣，左側缺口 40 m 為推得；Newmark 影響圖不重繪",
        note="攔錯用：A 在凸出部左緣與下方長方形上緣的凹角，距左端 40 m、距右端 80 m；求 A 正下方 40 m 處。",
        path=os.path.join(OUT, "SM-2025-4-fig-1-problem.svg"))


# ══════ fig-2：以 A 為共同角點拆成三塊矩形（解題圖解，2026-11-15 階段 E）══════
# ── 由 SM-2025-4 §4 Step 1–3 解得 ──
import math
Z = 40.0
def I_corner(m, n):                      # Fadum／Newmark 角隅影響係數
    a = m*m + n*n + 1; b = m*m*n*n
    t1 = 2*m*n*math.sqrt(a) / (a + b) * (a + 1) / a
    t2 = math.atan2(2*m*n*math.sqrt(a), a - b)
    return (t1 + t2) / (4*math.pi)
RECTS = [("①凸出部", (SX0, BH), (SX0 + SW, BH + SH), "rgba(29,78,216,0.22)"),
         ("②左下", (0.0, 0.0), (SX0, BH), "rgba(46,125,111,0.22)"),
         ("③右下", (SX0, 0.0), (BL, BH), "rgba(180,83,9,0.22)")]

def fig_split():
    W, H = 900, 520
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-10, BL + 60), (-22, BH + SH + 12), 30, 30, 20, 20))
    tot = 0.0
    for lab, p0, p1, col in RECTS:
        cv.polygon([p0, (p1[0], p0[1]), p1, (p0[0], p1[1])], col, C["member"], 1.8)
        b, l = p1[0] - p0[0], p1[1] - p0[1]
        m, n = min(b, l) / Z, max(b, l) / Z
        I = I_corner(m, n); tot += round(I, 4)        # §4 以四位小數相加
        cx, cy = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
        cv.text((cx, cy + 6), lab, 13, C["text"], weight="700")
        cv.text((cx, cy - 1), "%g×%g m" % (b, l), 12, C["text"])
        cv.text((cx, cy - 8), "m = %g，n = %g，I = %.4f" % (m, n, round(I, 4)), 12, C["deform"], weight="700")
    cv.dot(A, 7, fill=C["load"])
    cv.text((A[0] - 2, A[1] + 4), "A", 15, C["load"], anchor="end", weight="700")
    cv.text((BL + 6, 62), "三塊都以 A 為角點", 12.5, C["text"], anchor="start", weight="700")
    cv.text((BL + 6, 52), "z = 40 m", 12.5, C["text"], anchor="start")
    cv.text((BL + 6, 42), "ΣI = %.4f" % round(tot, 4), 12.5, C["deform"], anchor="start", weight="700")
    cv.text((BL + 6, 32), "Δσz = %d × ΣI" % Q, 12.5, C["text"], anchor="start")
    cv.text((BL + 6, 22), "    = %.2f kPa" % (Q * round(tot, 4)), 12.5, C["load"], anchor="start", weight="700")
    cv.dim((0, -10), (SX0, -10), "40 m", 0, C["dim"], 12, label_off=-14)
    cv.dim((SX0, -10), (BL, -10), "80 m", 0, C["dim"], 12, label_off=-14)
    return cv

compose([fig_split()],
        title="圖 2　以 A 為共同角點，T 形拆成三塊不重疊的矩形",
        sub="角隅影響係數相加：0.1752 + 0.1752 + 0.1999 = 0.5503（Newmark 圖約 110 格 × 0.005）",
        note="攔錯用：上方第一段 40 m 是凸出部寬、第二段是凸出部右緣到右端；A 是內角，三塊直接相加、不必相減。",
        path=os.path.join(OUT, "SM-2025-4-fig-2-split.svg"))
