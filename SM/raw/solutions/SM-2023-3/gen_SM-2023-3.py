# -*- coding: utf-8 -*-
"""SM-2023-3 解題圖解（數值取自解析正本 SM-2023-3.md，非題目重繪）。
用法：python gen_SM-2023-3.py [輸出資料夾]（預設本題 figs/）"""
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


# ══════ fig-1：三層土＋臨界深度——σ'v 與 f_s 沿深度（解題圖解）══════
# ── 由 SM-2023-3 §4 Step 1–4 解得（假設 φ = 27 + 0.3N、K = 1.0、δ = φ、Zc = 20D，見 §5）──
from math import pi, tan, radians, exp
D, L, ZW, GW = 0.5, 25.0, 10.0, 9.81
ZC = 20 * D
LAY = [(0, 5, 18, 12, "SM"), (5, 15, 20, 15, "ML"), (15, 30, 20, 30, "SW")]   # 頂、底、γ、N、名
PHI = [27 + 0.3 * n for _, _, _, n, _ in LAY]                                  # 30.6、31.5、36.0
def sig(z):                       # 實際有效覆土壓
    s, zp = 0.0, 0.0
    for t, b, g, _, _ in LAY:
        for a0, a1 in ((t, min(b, ZW)), (max(t, ZW), b)):
            lo, hi = max(a0, 0), min(a1, z)
            if hi > lo: s += (g if a1 <= ZW else g - GW) * (hi - lo)
    return s
SC = sig(ZC)                                                                   # 190
def sdes(z): return min(sig(z), SC) if z <= ZC else SC
def lay(z): return 0 if z < 5 else (1 if z < 15 else 2)
def fs(z): return 1.0 * sdes(z) * tan(radians(PHI[lay(z)]))
P = pi * D
QSEG = [round(P * 5 * tan(radians(PHI[0])) * 45, 1), round(P * 5 * tan(radians(PHI[1])) * 140, 1),
        round(P * 5 * tan(radians(PHI[1])) * 190, 1), round(P * 10 * tan(radians(PHI[2])) * 190, 1)]
NQ = exp(pi * tan(radians(PHI[2]))) * tan(radians(45 + PHI[2] / 2)) ** 2
QP_C = SC * NQ * pi * D ** 2 / 4
# 正本 §4 以四位有效的 tan 值與 Nq = 37.73 手算，圖上標註照正本數字；程式值只做核對（差 < 0.1%）
QSEG_MD, QS_MD, NQ_MD, QP_MD = [209.0, 673.8, 914.4, 2168.3], 3965.5, 37.73, 1407.6
assert abs(SC - 190) < 1e-9 and all(abs(a - b) / b < 1e-3 for a, b in zip(QSEG, QSEG_MD))
assert abs(sum(QSEG) - QS_MD) / QS_MD < 1e-3 and abs(QP_C - QP_MD) / QP_MD < 1e-3 and abs(NQ - NQ_MD) < 0.05
QSEG, NQ, QP = QSEG_MD, NQ_MD, QP_MD
FILL = ["rgba(180,83,9,0.10)", "rgba(124,58,237,0.08)", "rgba(180,83,9,0.20)"]

def shade(cv, m, vmax):
    for (t, b, g, n, nm), f in zip(LAY, FILL):
        bb = min(b, 26.0)
        cv.polygon([m.p(0, t), m.p(vmax, t), m.p(vmax, bb), m.p(0, bb)], f, "none")
    cv.line(m.p(0, ZC), m.p(vmax, ZC), C["accent"], 1.6, dash="4 4")

def pan_sig():
    cv = Canvas(480, 600); cv.panel("有效覆土壓 σ'v", "實線：計算用（Zc 以下封頂）；虛線：實際")
    m = PX(cv, 70, 40, 120, 60, 400, 26)
    shade(cv, m, 400)
    px_axes(m, [0, 100, 200, 300, 400], [0, 5, 10, 15, 20, 25], "σ'v（kPa）")
    zs = [26 * i / 260 for i in range(261)]
    cv.poly([m.p(sig(z), z) for z in zs], C["member2"], 2.2, dash="7 5")
    cv.poly([m.p(sdes(z), z) for z in zs], C["deform"], 3.0)
    wt_symbol(cv, m.x(340), cv.h - m.y(ZW), C["deform"], 7)
    tag_px(cv, m.x(290), m.y(ZC) - 16, "水位＝Zc = 20D = 10 m", 12, C["accent"])
    tag_px(cv, m.x(SC) - 8, m.y(18), "190（封頂）", 12, C["deform"], anchor="end")
    tag_px(cv, m.x(sig(L)) - 8, m.y(L) - 16, "%.0f（不用）" % sig(L), 12, C["member2"], anchor="end", weight="400")
    for t, b, g, n, nm in LAY:
        cv.text_px(m.x(395), m.y(t + 1.4), "%s  N=%d" % (nm, n), 12, C["muted"], anchor="end")
    return cv

def pan_f():
    cv = Canvas(480, 600); cv.panel("單位摩擦 f = K σ'v tanδ", "K = 1.0、δ = φ；跨 Zc 的 ML 層拆兩段")
    m = PX(cv, 70, 40, 120, 60, 160, 26)
    shade(cv, m, 160)
    px_axes(m, [0, 40, 80, 120, 160], [0, 5, 10, 15, 20, 25], "f（kPa）")
    zs = sorted(set([L * i / 500 for i in range(501)] + [4.9999, 5.0, 14.9999, 15.0]))
    pts = [m.p(fs(z), z) for z in zs]
    cv.polygon([m.p(0, 0)] + pts + [m.p(0, L)], C["fill_m"], "none")
    cv.poly(pts, C["bmd"], 2.8)
    for (z, q) in zip((2.5, 7.5, 12.5, 20.0), QSEG):
        tag_px(cv, m.x(4), m.y(z), "%.1f kN" % q, 11.5, C["bmd"], anchor="start", weight="400")
    for z, s in ((5, "%.2f" % fs(4.999)), (ZC, "%.2f" % fs(ZC)), (15, "%.2f" % fs(15))):
        tag_px(cv, m.x(fs(z if z != 5 else 4.999)) + 8, m.y(z) - (10 if z == 5 else 0), s, 11.5, C["bmd"], anchor="start")
    cv.line(m.p(0, L), m.p(160, L), C["member"], 1.6, dash="6 4")
    tag_px(cv, m.x(80), m.y(L) + 18, "樁底 25 m：Qp = 190 × %.2f × Ap = %.1f kN" % (NQ, QP), 11.5, C["load"])
    return cv

compose([pan_sig(), pan_f()],
        title="圖 1　三層無凝聚性土：臨界深度與水位都在 10 m",
        sub="Qs = %s = %.1f kN（數值隨 K、δ、Nq 假設變動，見 §5）" % (" + ".join("%.1f" % q for q in QSEG), QS_MD),
        note="攔錯用：10 m 以下 σ'v 固定 190 kPa（不再加 γ'z）；ML 層 5–10 m 遞增、10–15 m 定值，不可整層用一個平均。",
        path=os.path.join(OUT, "SM-2023-3-fig-1-critical-depth.svg"))
