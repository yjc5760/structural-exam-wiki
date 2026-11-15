# -*- coding: utf-8 -*-
"""SM-2024-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2024-4-problem.md §4 判讀清單（#9–#11），不含任何解題結果。
用法：python gen_SM-2024-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
D     = 1.0     # 題文 樁徑 1 m
P     = 2000    # 題文 垂直載重 kN
STICK = 0.5     # #9 樁頂略高出地表（示意高度）
LDRAW = 8.0     # 樁長未知（?），繪圖長度示意

def fig_problem():
    W, H = 760, 600
    XL, XR = -4.5, 4.5
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 0.8, XR + 0.4), (-(LDRAW + 1.6), 2.6), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(LDRAW + 0.8), Y(0), "rgba(63,74,90,0.12)")
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    for x in (3.3,):
        for k in range(3):
            cv.line((x + k * 0.22, Y(0)), (x + k * 0.22 - 0.2, Y(0.25)), C["member"], 1.4)
    cv.polygon([(-D / 2, Y(-STICK)), (D / 2, Y(-STICK)), (D / 2, Y(LDRAW)), (-D / 2, Y(LDRAW))],
               C["member"], C["member"], 1.4)
    cv.arrow((0, Y(-2.2)), (0, Y(-STICK - 0.08)), C["load"], 4.0, 12)
    cv.math_px(cv.X(0.35), cv.Y(Y(-1.9)), "2000 kN", 14, C["load"], anchor="start", weight="700")
    wt_symbol(cv, 2.2, Y(0), C["deform"], 0.2)
    cv.text_px(cv.X(2.2), cv.Y(Y(0)) - 26, "地下水位（地表）", 12, C["deform"], weight="700")
    xd = -2.4
    cv.dim((xd, Y(LDRAW)), (xd, Y(0)), "L = ?", 0, C["dim"], 14, label_off=-28)
    cv.line((XL + 0.5, Y(LDRAW)), (-D / 2 - 0.1, Y(LDRAW)), C["member"], 1.6)
    cv.dim((-D / 2, Y(LDRAW + 0.55)), (D / 2, Y(LDRAW + 0.55)), "1 m", 0, C["dim"], 12.5, label_off=14)
    cv.text_px(cv.X(1.0), cv.Y(Y(3.2)), "情況一：全為黏土層", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(4.2)), "情況二：全為飽和砂土層", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(5.2)), "（兩情況分開求樁長）", 12, C["muted"], anchor="start")
    return cv

compose([fig_problem()],
        title="SM-2024-4 題目附圖重繪",
        sub="依題目正本判讀清單；樁長 L 由地表量到樁底，地下水位在地表",
        note="攔錯用：L 是入土長度（不含高出地表段）；水位在地表，砂土情況全段用有效應力。",
        path=os.path.join(OUT, "SM-2024-4-fig-1-problem.svg"))


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


# ══════ fig-2：樁身阻抗分布圖（題目㈡要求；解題圖解）══════
# ── 由 SM-2024-4 §4 Step 2–4 解得（數值取正本，未重新假設）──
from math import pi, tan, radians, sin
QU = 2.5 * P                       # 5000 kN
AP, PER = pi * D ** 2 / 4, pi * D
# 黏土（Step 2）
F_CL = 0.62 * 60                    # α cu = 37.20 kPa
QP_CL = round(AP * 60 * 9, 2)       # 424.12
L_CL = round((QU - QP_CL) / (PER * F_CL), 2)    # 39.15
# 砂土（Step 3）
LC = 15 * D
F_SA = 32.64                         # §4 Step 3 f_s,max（K0 σ0' tan0.8φ，σ0' = 144.75）
QP_SA = round(AP * 0.5 * 100 * 20 * tan(radians(38)), 1)   # 613.6（q_l 控制）
QS1 = round(0.5 * PER * LC * F_SA, 1)                       # 769.1
L_SA = round(LC + (QU - QP_SA - QS1) / (PER * F_SA), 2)     # 50.28
assert (QP_CL, L_CL, QP_SA, QS1, L_SA) == (424.12, 39.15, 613.6, 769.1, 50.28), (QP_CL, L_CL, QP_SA, QS1, L_SA)
ZM = 54.0

def n_cl(z): return QU - PER * F_CL * z
def f_sa(z): return F_SA * min(z, LC) / LC
def n_sa(z):
    return QU - (0.5 * PER * F_SA * z * z / LC if z <= LC else QS1 + PER * F_SA * (z - LC))

def pan_f(title, sub, fz, Lp, marks, col):
    cv = Canvas(440, 560); cv.panel(title, sub)
    m = PX(cv, 70, 40, 120, 50, 45, ZM)
    px_axes(m, [0, 10, 20, 30, 40], [0, 10, 20, 30, 40, 50], "單位摩擦阻抗 f（kPa）")
    zs = [Lp * i / 200 for i in range(201)]
    cv.polygon([m.p(0, 0)] + [m.p(fz(z), z) for z in zs] + [m.p(0, Lp)], col, "none", 1, op=0.18)
    cv.poly([m.p(fz(z), z) for z in zs], col, 2.8)
    cv.line(m.p(0, Lp), m.p(45, Lp), C["member"], 1.6, dash="6 4")
    for z, s in marks:
        tag_px(cv, m.x(fz(z)) + 8, m.y(z), s, 12, col, anchor="start", weight="400")
    tag_px(cv, m.x(22), m.y(Lp) + 16, "樁底 L = %.2f m" % Lp, 12, C["member"], weight="700")
    return cv

def pan_n(title, sub, nz, Lp, qp, marks):
    cv = Canvas(440, 560); cv.panel(title, sub)
    m = PX(cv, 70, 40, 120, 50, 5000, ZM)
    px_axes(m, [0, 1000, 2000, 3000, 4000, 5000], [0, 10, 20, 30, 40, 50], "樁身軸力 N（kN）")
    zs = [Lp * i / 200 for i in range(201)]
    cv.polygon([m.p(0, 0)] + [m.p(nz(z), z) for z in zs] + [m.p(0, Lp)], C["fill_c"], "none", 1)
    cv.poly([m.p(nz(z), z) for z in zs], C["compr"], 2.8)
    cv.line(m.p(0, Lp), m.p(5000, Lp), C["member"], 1.6, dash="6 4")
    cv.arrow(m.p(qp, Lp + 3.2), m.p(qp, Lp + 0.3), C["load"], 2.6, 9)
    tag_px(cv, m.x(qp) + 12, m.y(Lp + 2.2), "端承 Qp = %.2f kN" % qp if qp < 500 else "端承 Qp = %.1f kN" % qp,
           12, C["load"], anchor="start", weight="700")
    for z, s, dx in marks:
        tag_px(cv, m.x(nz(z)) + dx, m.y(z), s, 12, C["compr"], anchor="start" if dx > 0 else "end", weight="400")
    return cv

compose([pan_f("黏土：f 沿深度均勻", "α cu = 0.62 × 60", lambda z: F_CL, L_CL,
               [(20, "%.2f kPa" % F_CL)], C["bmd"]),
         pan_n("黏土：軸力線性遞減", "每米摩擦 %.2f kN/m" % (PER * F_CL), n_cl, L_CL, QP_CL,
               [(0.6, "Qu = %d" % QU, -10)]),
         pan_f("砂土：0～15D 線性、以下定值", "K0 σ'v tan(0.8φ)，σ'v 在 Lc = 15 m 封頂", f_sa, L_SA,
               [(LC, "%.2f kPa" % F_SA)], C["accent"]),
         pan_n("砂土：先拋物線、後直線遞減", "15 m 處 N = %.1f kN" % (QU - QS1), n_sa, L_SA, QP_SA,
               [(LC, "%.1f" % (QU - QS1), 10), (0.6, "Qu = %d" % QU, -10)])],
        cols=2,
        title="圖 2　樁身阻抗分布：黏土（上）與飽和砂土（下）",
        sub="Qu = 2.5 × 2000 = 5000 kN；樁頂軸力扣掉沿途摩擦，到樁底剩下的就是端承",
        note="攔錯用：砂土 15 m 以下 f 不再增加（臨界深度封頂），端承由 ql 控制只剩 613.6 kN；黏土 f 與深度無關。",
        path=os.path.join(OUT, "SM-2024-4-fig-2-resistance.svg"))
