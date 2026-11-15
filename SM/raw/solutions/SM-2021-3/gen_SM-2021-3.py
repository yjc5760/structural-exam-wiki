# -*- coding: utf-8 -*-
"""SM-2021-3 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2021-3-problem.md §4 判讀清單（#3–#5），不含任何解題結果。
用法：python gen_SM-2021-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_S = 6.0      # #3 砂土 0–6 m
L   = 12.0     # #3 樁底深度（黏土 6–12 m，黏土向下延伸）
D   = 0.6      # 題文 直徑 60 cm
WT  = 0.0      # #5 地下水位在地表
BW  = 0.9      # 樁寬繪圖用（略放大示意）

def fig_problem():
    W, H = 900, 560
    XL, XR = -6.0, 11.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 1.6, XR + 0.4), (-(L + 1.6), 1.4), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(H_S), Y(0), "rgba(180,83,9,0.18)")
    soil_fill(cv, XL, XR, Y(L + 1.4), Y(H_S), "rgba(63,74,90,0.18)")
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(H_S)), (XR, Y(H_S)), C["member2"], 1.8)
    cv.polygon([(-BW / 2, Y(0)), (BW / 2, Y(0)), (BW / 2, Y(L)), (-BW / 2, Y(L))], "#8A94A6", C["member"], 1.6)
    wt_symbol(cv, -2.6, Y(WT), C["deform"], 0.17)
    cv.text_px(cv.X(-2.1), cv.Y(Y(0)) - 14, "地下水位（地表）", 12, C["deform"], anchor="start", weight="700")
    cv.text_px(cv.X(5.0), cv.Y(Y(1.5)), "砂土層", 13, C["text"], weight="700")
    cv.math_px(cv.X(5.0), cv.Y(Y(2.6)), "c' = 0 kN/m^{2},   φ' = 32°", 13, C["text"])
    cv.math_px(cv.X(5.0), cv.Y(Y(3.7)), "γ_{sat} = 19.2 kN/m^{3}", 13, C["text"])
    cv.text_px(cv.X(5.0), cv.Y(Y(8.5)), "黏土層", 13, C["text"], weight="700")
    cv.math_px(cv.X(5.0), cv.Y(Y(9.6)), "c_{u} = 100 kN/m^{2}", 13, C["text"])
    cv.math_px(cv.X(5.0), cv.Y(Y(10.7)), "γ_{sat} = 18.9 kN/m^{3}", 13, C["text"])
    cv.text_px(cv.X(BW / 2 + 0.3), cv.Y(Y(L - 0.5)), "預鑄混凝土樁 D = 60 cm", 12, C["muted"], anchor="start")
    xd = -4.4
    cv.dim((xd, Y(H_S)), (xd, Y(0)), "6 m", 0, C["dim"], 12.5, label_off=-24)
    cv.dim((xd, Y(L)), (xd, Y(H_S)), "6 m", 0, C["dim"], 12.5, label_off=-24)
    cv.line((xd - 0.4, Y(L)), (-BW / 2 - 0.2, Y(L)), C["dim"], 0.9, dash="2 3")
    cv.text_px(cv.X(0), cv.Y(Y(L + 1.0)), "黏土層向下延伸（考卷未標底界）", 12, C["muted"])
    return cv

compose([fig_problem()],
        title="SM-2021-3 題目附圖重繪",
        sub="依題目正本判讀清單；樁頂齊地表，地下水位在地表",
        note="攔錯用：樁長 12 m＝砂土 6 m＋黏土 6 m，樁底在黏土中；水位在地表，砂土全段用浮單位重。",
        path=os.path.join(OUT, "SM-2021-3-fig-1-problem.svg"))


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


# ══════ fig-2：單位摩擦分布與受壓軸力（解題圖解）══════
# ── 由 SM-2021-3 §4 Step 1–6 解得（γw = 9.81）──
from math import pi, tan, radians, sin
DQ, HS, HC_, GW_ = 0.6, 6.0, 6.0, 9.81
KK = 1.4 * (1 - sin(radians(32))); TD = tan(radians(0.8 * 32))
GP = 19.2 - GW_
def fz_(z): return KK * GP * z * TD if z <= HS else 0.65 * 100
F6 = KK * GP * HS * TD
# 正本 §4 的手算值（A_p 取 0.2827）照抄標註；程式值只核對（差 < 0.1%）
QS1_, QS2_, QP_, QUN, QAC, WP_, QAT = 100.46, 735.15, 254.43, 1090.04, 363.35, 48.15, 326.69
PQ = pi * DQ
assert abs(PQ * KK * TD * GP * HS ** 2 / 2 - QS1_) < 0.1 and abs(PQ * 65 * HC_ - QS2_) / QS2_ < 1e-3
assert abs(900 * pi * DQ ** 2 / 4 - QP_) / QP_ < 1e-3 and abs((QS1_ + QS2_ + QP_) / 3 - QAC) < 0.01
assert abs((QS1_ + QS2_) / 3 + WP_ - QAT) < 0.01
def nz_(z):
    if z <= HS: return QUN - PQ * KK * TD * GP * z * z / 2 * (QS1_ / (PQ * KK * TD * GP * HS ** 2 / 2))
    return QUN - QS1_ - QS2_ * (z - HS) / HC_

def pan_f():
    cv = Canvas(460, 560); cv.panel("單位摩擦 f", "砂：K σ'v tanδ'（水位在地表）；黏土：α cu")
    m = PX(cv, 70, 40, 120, 60, 80, 12.5)
    cv.polygon([m.p(0, 0), m.p(80, 0), m.p(80, HS), m.p(0, HS)], "rgba(180,83,9,0.12)", "none")
    cv.polygon([m.p(0, HS), m.p(80, HS), m.p(80, 12.5), m.p(0, 12.5)], "rgba(63,74,90,0.14)", "none")
    px_axes(m, [0, 20, 40, 60, 80], [0, 2, 4, 6, 8, 10, 12], "f（kPa）")
    pts = [m.p(0, 0), m.p(F6, HS), m.p(65, HS), m.p(65, 12)]
    cv.polygon(pts + [m.p(0, 12)], C["fill_m"], "none"); cv.poly(pts, C["bmd"], 2.8)
    tag_px(cv, m.x(F6) + 8, m.y(HS) - 18, "%.2f" % F6, 12, C["bmd"], anchor="start")
    tag_px(cv, m.x(65) - 8, m.y(9), "65", 12, C["bmd"], anchor="end")
    tag_px(cv, m.x(4), m.y(2.0), "Qs1 = %.2f" % QS1_, 12, C["bmd"], anchor="start", weight="400")
    tag_px(cv, m.x(20), m.y(9), "Qs2 = %.2f" % QS2_, 12, C["bmd"], anchor="start", weight="400")
    cv.text_px(m.x(78), m.y(0.6), "砂土", 12, C["muted"], anchor="end")
    cv.text_px(m.x(78), m.y(6.6), "黏土", 12, C["muted"], anchor="end")
    cv.line(m.p(0, 12), m.p(80, 12), C["member"], 1.6, dash="6 4")
    return cv

def pan_n():
    cv = Canvas(460, 560); cv.panel("極限受壓時的樁身軸力", "Qu = Qs + Qp；拉拔時樁底不計、改加有效自重")
    m = PX(cv, 70, 40, 120, 60, 1200, 12.5)
    px_axes(m, [0, 300, 600, 900, 1200], [0, 2, 4, 6, 8, 10, 12], "N（kN）")
    zs = [12 * i / 240 for i in range(241)]
    cv.polygon([m.p(0, 0)] + [m.p(nz_(z), z) for z in zs] + [m.p(0, 12)], C["fill_c"], "none")
    cv.poly([m.p(nz_(z), z) for z in zs], C["compr"], 2.8)
    tag_px(cv, m.x(QUN) - 8, m.y(0.7), "Qu = %.2f" % QUN, 12, C["compr"], anchor="end")
    tag_px(cv, m.x(nz_(HS)) + 10, m.y(HS), "%.2f" % nz_(HS), 12, C["compr"], anchor="start", weight="400")
    tag_px(cv, m.x(QP_) + 10, m.y(12) - 6, "樁底 Qp = %.2f" % QP_, 12, C["load"], anchor="start")
    tag_px(cv, m.x(470), m.y(3.0), "容許受壓 Qu/3 = %.2f kN" % QAC, 12, C["text"])
    tag_px(cv, m.x(470), m.y(4.0), "容許拉拔 Qs/3 + W'p = %.2f kN" % QAT, 12, C["text"])
    return cv

compose([pan_f(), pan_n()],
        title="圖 2　上砂下黏：兩種摩擦機制與極限軸力",
        sub="砂土段 f 由 0 線性增至 6 m，黏土段 f = 0.65 × 100 與深度無關",
        note="攔錯用：水位在地表，砂土用 γ' = 9.39（不是 19.2）；黏土 f 不隨深度增加；拉拔不加樁底。",
        path=os.path.join(OUT, "SM-2021-3-fig-2-resistance.svg"))
