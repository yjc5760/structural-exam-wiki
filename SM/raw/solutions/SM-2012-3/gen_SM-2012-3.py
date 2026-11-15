# -*- coding: utf-8 -*-
"""SM-2012-3 解題圖解（數值取自解析正本 SM-2012-3.md，非題目重繪）。
用法：python gen_SM-2012-3.py [輸出資料夾]（預設本題 figs/）"""
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


# ══════ fig-1：抗拉樁的摩擦分布與累積抗拉力（解題圖解）══════
# ── 由 SM-2012-3 §4 Step 1–4 解得（水位在地表、樁有效單位重 23 − 9.81）──
from math import pi
D, H1, TU = 0.5, 8.0, 1200.0
P, AP = pi * D, pi * D ** 2 / 4
F1, F2 = 1.0 * 45, 0.75 * 70
WP = (23 - 9.81) * AP                         # 2.590 kN/m
X = (TU - F1 * P * H1 - WP * H1) / (F2 * P + WP)
L = H1 + X
assert round(X, 3) == 7.216 and round(L, 2) == 15.22, (X, L)
def f_(z): return F1 if z < H1 else F2
def t_(z): return P * (F1 * min(z, H1) + F2 * max(z - H1, 0)) + WP * z
ZM = 18.0

def pan_f():
    cv = Canvas(440, 560); cv.panel("單位摩擦 f = α cu", "上層 1.0 × 45、下層 0.75 × 70")
    m = PX(cv, 70, 40, 120, 60, 60, ZM)
    cv.polygon([m.p(0, 0), m.p(60, 0), m.p(60, H1), m.p(0, H1)], "rgba(63,74,90,0.10)", "none")
    cv.polygon([m.p(0, H1), m.p(60, H1), m.p(60, ZM), m.p(0, ZM)], "rgba(63,74,90,0.20)", "none")
    px_axes(m, [0, 20, 40, 60], [0, 4, 8, 12, 16], "f（kPa）")
    pts = [m.p(F1, 0), m.p(F1, H1), m.p(F2, H1), m.p(F2, L)]
    cv.polygon([m.p(0, 0)] + pts + [m.p(0, L)], C["fill_m"], "none"); cv.poly(pts, C["bmd"], 2.8)
    cv.poly([m.p(F2, L), m.p(F2, ZM)], C["bmd"], 1.6, dash="5 4")
    tag_px(cv, m.x(F1) - 8, m.y(4), "45", 12, C["bmd"], anchor="end")
    tag_px(cv, m.x(F2) - 8, m.y(11.5), "52.5", 12, C["bmd"], anchor="end")
    cv.line(m.p(0, L), m.p(60, L), C["member"], 1.6, dash="6 4")
    tag_px(cv, m.x(30), m.y(L) + 18, "樁底 L = %.2f m（x = %.3f m）" % (L, X), 12, C["member"])
    cv.text_px(m.x(2), m.y(0.7), "黏土 1（8 m）", 12, C["muted"], anchor="start")
    cv.text_px(m.x(2), m.y(H1 + 0.7), "黏土 2（20 m）", 12, C["muted"], anchor="start")
    return cv

def pan_t():
    cv = Canvas(440, 560); cv.panel("累積抗拉力 T(z) = 摩擦 + 有效自重", "到 T = 1200 kN 的深度即所需貫入深度")
    m = PX(cv, 70, 40, 120, 60, 1400, ZM)
    px_axes(m, [0, 400, 800, 1200], [0, 4, 8, 12, 16], "T（kN）")
    zs = [ZM * i / 360 for i in range(361)]
    cv.poly([m.p(t_(z), z) for z in zs if z <= L], C["compr"], 2.8)
    cv.poly([m.p(t_(z), z) for z in zs if z >= L], C["compr"], 1.6, dash="5 4")
    cv.line(m.p(TU, 0), m.p(TU, ZM), C["load"], 1.6, dash="3 4")
    cv.dot(m.p(TU, L), 5.5, fill=C["load"])
    tag_px(cv, m.x(TU) - 10, m.y(L) + 4, "1200 kN @ %.2f m" % L, 12, C["load"], anchor="end")
    tag_px(cv, m.x(t_(H1)) + 10, m.y(H1), "8 m：%.2f" % t_(H1), 12, C["compr"], anchor="start", weight="400")
    return cv

compose([pan_f(), pan_t()],
        title="圖 1　抗拉樁：上層摩擦不夠，往下層找剩下的 %.0f kN" % (TU - t_(H1)),
        sub="自重項也隨樁長增加；樁底不計吸力",
        note="攔錯用：只算進入下層的 7.22 m 不是答案，貫入深度由地表起算 15.22 m；自重要用浮單位重。",
        path=os.path.join(OUT, "SM-2012-3-fig-1-uplift.svg"))
