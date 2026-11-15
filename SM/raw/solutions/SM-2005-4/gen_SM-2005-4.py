# -*- coding: utf-8 -*-
"""SM-2005-4 圖解。
fig-1-problem：題目附圖（τs–s、qp–d 兩張關係圖）重繪，幾何只取自題目正本 SM-2005-4-problem.md §4 判讀清單（#4–#6），不含任何解題結果。
兩條雙線性關係完全由考卷標註的轉折點決定（不是讀曲線取值），重繪不會自編數據。
用法：python gen_SM-2005-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
S_Y, TAU_MAX = 2.0, 10.0      # #4 τs–s：線性到 (2 cm, 10 kPa) 後水平
D_Y, QP_MAX  = 8.0, 400.0     # #5 qp–d：線性到 (8 cm, 400 kPa) 後水平

def panel(xmax, ymax, xk, yk, xlab, ylab, xname, yname, title):
    W, H = 470, 400
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.12), (0, 1.0), 86, 30, 70, 70))
    cv.panel(title, None)
    X = lambda v: v / xmax
    Yv = lambda v: v / ymax * 0.82
    cv.arrow((0, 0), (1.10, 0), C["muted"], 1.9, 9)
    cv.arrow((0, 0), (0, 0.98), C["muted"], 1.9, 9)
    cv.poly([(0, 0), (X(xk), Yv(yk)), (1.04, Yv(yk))], C["member"], 3.0)
    cv.line((X(xk), Yv(yk)), (X(xk), 0), C["dim"], 1.3, dash="6 4")
    cv.line((X(xk), Yv(yk)), (0, Yv(yk)), C["dim"], 1.3, dash="6 4")
    cv.dot((X(xk), Yv(yk)), 5, fill=C["accent"])
    cv.text_px(cv.X(X(xk)), cv.Y(0) + 18, xlab, 13.5, C["text"])
    cv.text_px(cv.X(0) - 10, cv.Y(Yv(yk)), ylab, 13.5, C["text"], anchor="end")
    cv.math_px(cv.X(1.06), cv.Y(0) + 20, xname, 14, C["text"], anchor="end")
    cv.math_px(cv.X(0) + 10, cv.Y(0.95), yname, 14, C["text"], anchor="start")
    cv.text_px(cv.X(0.62), cv.Y(Yv(yk)) - 16, "完全塑性（水平）", 12, C["muted"])
    return cv

compose([panel(5.0, 14.0, S_Y, TAU_MAX, "2", "10", "s (cm)", "τ_{s} (kPa)", "側向摩擦剪應力 τs 與剪位移 s"),
         panel(20.0, 560.0, D_Y, QP_MAX, "8", "400", "d (cm)", "q_{p} (kPa)", "底部承載應力 qp 與位移 d")],
        title="SM-2005-4 題目附圖重繪",
        sub="依題目正本判讀清單；兩條都是線性上升後水平的雙線性關係（橫軸依標註數值按比例重畫）",
        note="攔錯用：摩擦在 s = 2 cm 就達上限 10 kPa，端承要到 d = 8 cm 才達 400 kPa；考卷原圖刻度未按比例。",
        path=os.path.join(OUT, "SM-2005-4-fig-1-problem.svg"))


# ══════ 解題圖解共用：像素座標的深度剖面框（G5，2026-11-15）══════
class PX:
    """值 v → 水平像素、深度 z → 垂直像素（向下）。p() 回傳 Canvas 模型座標（sx = 1）。"""
    def __init__(s, cv, L, R, T, B, vmax, zmax, vmin=0.0):
        s.cv, s.L, s.R, s.T, s.B = cv, L, cv.w - R, T, cv.h - B
        s.vmin, s.vmax, s.zmax = vmin, vmax, zmax
    def x(s, v): return s.L + (v - s.vmin) / (s.vmax - s.vmin) * (s.R - s.L)
    def y(s, z): return s.T + z / s.zmax * (s.B - s.T)
    def p(s, v, z): return (s.x(v), s.cv.h - s.y(z))

def px_axes(m, vt, zt, vlab, zlab="z（m）"):
    cv = m.cv
    for v in vt:
        cv.line(m.p(v, 0), m.p(v, m.zmax), C["border"], 1.0)
        cv.text_px(m.x(v), m.T - 12, "%g" % v, 12, C["muted"])
    for z in zt:
        cv.line(m.p(m.vmin, z), m.p(m.vmax, z), C["border"], 1.0)
        cv.text_px(m.L - 8, m.y(z), "%g" % z, 12, C["muted"], anchor="end")
    cv.line(m.p(m.vmin, 0), m.p(m.vmax, 0), C["muted"], 1.8)
    cv.line(m.p(m.vmin, 0), m.p(m.vmin, m.zmax), C["muted"], 1.8)
    cv.text_px((m.L + m.R) / 2, m.T - 34, vlab, 13, C["text"], weight="700")
    cv.text_px(m.L - 8, m.B + 22, zlab, 12.5, C["muted"], anchor="end")


# ══════ fig-2：荷重–沉陷曲線（剛性墩，摩擦＋端承分量；解題圖解）══════
# ── 由 SM-2005-4 §4（一）（二）解得：τs、qp 的雙線性關係取自題目正本轉折點 ──
from math import pi
DD, LL = 1.2, 12.0
AS_, AB_ = pi * DD * LL, pi * DD ** 2 / 4
def tau(d): return 10.0 * min(d, 2.0) / 2.0          # kPa，d 單位 cm
def qpd(d): return 400.0 * min(d, 8.0) / 8.0
def qs_(d): return tau(d) * AS_
def qb_(d): return qpd(d) * AB_
def qt_(d): return qs_(d) + qb_(d)
QU_ = qt_(8.0); QALL = QU_ / 3
Q1, Q15 = qt_(1.0), qt_(1.5)
assert (round(QU_, 2), round(QALL, 2), round(Q1, 2), round(Q15, 2)) == (904.78, 301.59, 282.74, 424.12)
D_ALL = QALL / (qt_(1.0) / 1.0)                        # FS = 3 對應沉陷（線性段）

def pan_qd():
    cv = Canvas(900, 560); cv.panel("墩頂荷重 Q 與沉陷 Δ（剛性墩：s = d = Δ）", "摩擦 2 cm 就到頂，端承要 8 cm")
    m = PX(cv, 90, 60, 100, 70, 10, 1000)               # v = Δ（cm）、z = 1000 − Q（讓 Q 向上）
    P_ = lambda d, q: m.p(d, 1000 - q)
    for d in range(0, 11):
        cv.line(P_(d, 0), P_(d, 1000), C["border"], 1.0)
        cv.text_px(m.x(d), m.B + 18, "%d" % d, 12, C["muted"])
    for q in range(0, 1001, 200):
        cv.line(P_(0, q), P_(10, q), C["border"], 1.0)
        cv.text_px(m.L - 8, m.y(1000 - q), "%d" % q, 12, C["muted"], anchor="end")
    cv.line(P_(0, 0), P_(10, 0), C["muted"], 1.8); cv.line(P_(0, 0), P_(0, 1000), C["muted"], 1.8)
    cv.text_px((m.L + m.R) / 2, m.B + 42, "沉陷 Δ（cm）", 13, C["text"], weight="700")
    cv.text_px(m.L - 8, m.T - 18, "Q（kN）", 13, C["text"], weight="700", anchor="end")
    ds = [10 * i / 400 for i in range(401)]
    cv.poly([P_(d, qs_(d)) for d in ds], C["bmd"], 2.4, dash="7 4")
    cv.poly([P_(d, qb_(d)) for d in ds], C["accent"], 2.4, dash="7 4")
    cv.poly([P_(d, qt_(d)) for d in ds], C["compr"], 3.0)
    cv.line(P_(0, QALL), P_(10, QALL), C["load"], 1.6, dash="3 4")
    tag_px(cv, m.x(9.9), m.y(1000 - QALL) - 16, "Qu/3 = %.2f（約 Δ = %.2f cm）" % (QALL, D_ALL), 12, C["load"], anchor="end")
    for d, q in ((1.0, Q1), (1.5, Q15)):
        cv.line(P_(d, 0), P_(d, q), C["compr"], 1.2, dash="2 3")
        cv.dot(P_(d, q), 5.5, fill=C["compr"])
    tag_px(cv, m.x(1.0) - 8, m.y(1000 - Q1) + 14, "1 cm：%.2f" % Q1, 12, C["compr"], anchor="end", weight="400")
    tag_px(cv, m.x(1.5) + 10, m.y(1000 - Q15) - 14, "1.5 cm：%.2f" % Q15, 12, C["compr"], anchor="start", weight="400")
    cv.dot(P_(8.0, QU_), 5.5, fill=C["compr"])
    tag_px(cv, m.x(8.0), m.y(1000 - QU_) - 18, "Qu = %.2f kN（Δ = 8 cm 才到）" % QU_, 12, C["compr"])
    tag_px(cv, m.x(5.5), m.y(1000 - qs_(5)) - 14, "摩擦 %.2f（Δ ≥ 2 cm 定值）" % qs_(5), 12, C["bmd"], weight="400")
    tag_px(cv, m.x(5.0), m.y(1000 - qb_(5)) + 16, "端承 qp·Ab（8 cm 才到 %.2f）" % qb_(8), 12, C["accent"], weight="400")
    return cv

compose([pan_qd()],
        title="圖 2　荷重–沉陷：極限法與位移限制法的落差",
        sub="實線＝摩擦＋端承；兩條虛線為分量",
        note="攔錯用：Qu 要沉陷 8 cm 才發揮；1～1.5 cm 時摩擦已動員 50～75%，端承只有 12.5～19%。",
        path=os.path.join(OUT, "SM-2005-4-fig-2-load-settlement.svg"))
