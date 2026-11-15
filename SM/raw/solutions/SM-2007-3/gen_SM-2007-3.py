# -*- coding: utf-8 -*-
"""SM-2007-3 解題圖解（數值取自解析正本 SM-2007-3.md，非題目重繪）。
用法：python gen_SM-2007-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)


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


# ══════ fig-1：臨界深度——σ'v 與 f_s 沿深度（解題圖解）══════
# ── 由 SM-2007-3 §4 Step 1–3 解得 ──
from math import pi, tan, radians, sin
D, L, G, NQ = 0.5, 15.0, 18.0, 21
LC = 20 * D                                   # 10 m
K, DELTA = 1.8 * (1 - sin(radians(30))), 15.0
QC = G * LC                                   # 180 kPa
FMAX = round(K * QC * tan(radians(DELTA)), 3)  # 43.408
P = pi * D
QS1 = round(P * 0.5 * FMAX * LC, 2); QS2 = round(P * FMAX * (L - LC), 2)
QP = round(QC * NQ * pi * D ** 2 / 4, 2)
assert (FMAX, QS1, QS2, QP) == (43.408, 340.93, 340.93, 742.20), (FMAX, QS1, QS2, QP)

def pan_sig():
    cv = Canvas(460, 560); cv.panel("有效覆土壓 σ'v", "實線：計算用（Lc 以下封頂）；虛線：實際")
    m = PX(cv, 70, 40, 120, 60, 300, 16)
    px_axes(m, [0, 100, 200, 300], [0, 5, 10, 15], "σ'v（kPa）")
    cv.poly([m.p(0, 0), m.p(G * L, L)], C["member2"], 2.2, dash="7 5")
    cv.poly([m.p(0, 0), m.p(QC, LC), m.p(QC, L)], C["deform"], 3.0)
    cv.line(m.p(0, LC), m.p(300, LC), C["accent"], 1.6, dash="4 4")
    tag_px(cv, m.x(225), m.y(LC) - 16, "Lc = 20D = 10 m", 12, C["accent"])
    tag_px(cv, m.x(QC) - 10, m.y(12.5), "%.0f（樁底用）" % QC, 12, C["deform"], anchor="end")
    tag_px(cv, m.x(G * L) - 8, m.y(L) - 18, "%.0f（不用）" % (G * L), 12, C["member2"], anchor="end", weight="400")
    return cv

def pan_f():
    cv = Canvas(460, 560); cv.panel("單位摩擦 f = K σ'v tanδ", "K = 0.9、δ = 15°")
    m = PX(cv, 70, 40, 120, 60, 50, 16)
    px_axes(m, [0, 10, 20, 30, 40, 50], [0, 5, 10, 15], "f（kPa）")
    cv.polygon([m.p(0, 0), m.p(FMAX, LC), m.p(FMAX, L), m.p(0, L)], C["fill_m"], "none")
    cv.poly([m.p(0, 0), m.p(FMAX, LC), m.p(FMAX, L)], C["bmd"], 3.0)
    cv.line(m.p(0, LC), m.p(50, LC), C["accent"], 1.6, dash="4 4")
    tag_px(cv, m.x(FMAX / 2) - 6, m.y(6.5), "三角形 Qs1 = %.2f" % QS1, 12, C["bmd"], anchor="end", weight="400")
    tag_px(cv, m.x(FMAX / 2), m.y(12.5), "矩形 Qs2 = %.2f" % QS2, 12, C["bmd"], weight="400")
    tag_px(cv, m.x(FMAX) - 6, m.y(LC) - 18, "%.2f" % FMAX, 12, C["bmd"], anchor="end")
    tag_px(cv, m.x(25), m.y(L) + 22, "樁底 15 m：Qp = 180 × 21 × Ap = %.2f kN" % QP, 11.5, C["load"])
    return cv

compose([pan_sig(), pan_f()],
        title="圖 1　臨界深度 20D：樁身摩擦與樁底端承都用封頂後的 σ'v",
        sub="Qs = %.2f + %.2f = %.2f kN；Qa = Qp/4 + Qs/3 = 412.84 kN" % (QS1, QS2, QS1 + QS2),
        note="攔錯用：10 m 以下 σ'v 不再隨深度增加；樁底若用實際 270 kPa，Qp 高估 1.5 倍（字面讀法見 §5）。",
        path=os.path.join(OUT, "SM-2007-3-fig-1-critical-depth.svg"))
