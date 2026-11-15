# -*- coding: utf-8 -*-
"""SM-2014-2 圖解。
fig-1-problem：題目附圖（圖二）重繪，幾何只取自題目正本 SM-2014-2-problem.md §4 判讀清單（#3–#5、#7），不含任何解題結果。
用法：python gen_SM-2014-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
L    = 25.0    # #4 樁長（樁頂→樁底）
Z_K  = 18.0    # #3/#4 摩擦轉折深度
F_MX = 50.0    # #3 摩擦應力上限 kPa
D    = 1.2     # #7 樁徑
Q_T  = 4500    # 題文 樁頂軸重 kN
BW   = 5.0     # 樁寬繪圖用（放大示意，非比例）
FS   = 4.0 / F_MX   # 摩擦分布水平比例（模型單位 / kPa）

def fig_problem():
    W, H = 800, 640
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-9.5, 17.5), (-(L + 3.2), 5.0), 30, 30, 40, 40))
    Y = lambda d: -d
    soil_fill(cv, -9.0, 11.5, Y(L + 0.6), Y(0), "rgba(180,83,9,0.10)")
    cv.polygon([(0, Y(0)), (BW, Y(0)), (BW, Y(L)), (0, Y(L))], "rgba(63,74,90,0.18)", C["member"], 2.4)
    # 側向摩擦分布（樁右側）
    x0 = BW
    cv.polygon([(x0, Y(0)), (x0 + F_MX * FS, Y(Z_K)), (x0 + F_MX * FS, Y(L)), (x0, Y(L))],
               "rgba(124,58,237,0.16)", C["sfd"], 2.2)
    cv.text_px(cv.X(x0 + F_MX * FS) + 6, cv.Y(Y(Z_K)), "50 kPa", 12.5, C["sfd"], anchor="start", weight="700")
    cv.text_px(cv.X(x0 + F_MX * FS) + 6, cv.Y(Y(L - 0.8)), "50 kPa", 12.5, C["sfd"], anchor="start", weight="700")
    cv.text_px(cv.X(x0) + 6, cv.Y(Y(0)) - 10, "0", 12, C["sfd"], anchor="start", weight="700")
    cv.text_px(cv.X(x0 + 1.4), cv.Y(Y(-1.4)), "側向摩擦應力", 12.5, C["sfd"], anchor="start", weight="700")
    # 載重
    cv.arrow((BW / 2, Y(-4.2)), (BW / 2, Y(-0.15)), C["load"], 3.2, 11)
    cv.math_px(cv.X(BW / 2 + 0.4), cv.Y(Y(-3.4)), "4500 kN", 14, C["load"], anchor="start", weight="700")
    # 參數
    cv.math_px(cv.X(BW / 2), cv.Y(Y(7.0)), "E_{c} =", 13, C["text"])
    cv.math_px(cv.X(BW / 2), cv.Y(Y(8.3)), "2×10^{7} kPa", 13, C["text"])
    cv.text_px(cv.X(BW / 2), cv.Y(Y(10.0)), "基樁", 13, C["text"], weight="700")
    cv.math_px(cv.X(-8.6), cv.Y(Y(7.0)), "E_{s} = 3×10^{4} kPa", 13, C["text"], anchor="start")
    cv.math_px(cv.X(-8.6), cv.Y(Y(9.0)), "μ_{s} = 0.35", 13, C["text"], anchor="start")
    cv.text_px(cv.X(-8.6), cv.Y(Y(11.0)), "砂質土壤", 13, C["text"], anchor="start")
    # 尺寸線
    xd = 12.6
    cv.dim((xd, Y(Z_K)), (xd, Y(0)), "18 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((xd, Y(L)), (xd, Y(Z_K)), "7 m", 0, C["dim"], 12.5, label_off=-22)
    cv.dim((xd + 2.6, Y(L)), (xd + 2.6, Y(0)), "L = 25 m", 0, C["dim"], 12.5, label_off=34)
    for d in (0, Z_K, L):
        cv.line((BW + F_MX * FS + 0.3 if d else BW + 0.3, Y(d)), (xd + 2.9, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.dim((0, Y(L + 1.2)), (BW, Y(L + 1.2)), "D = 1.2 m", 0, C["dim"], 12.5, label_off=14)
    return cv

compose([fig_problem()],
        title="SM-2014-2 題目附圖（圖二）重繪",
        sub="依題目正本判讀清單；樁寬放大示意，深度按比例",
        note="攔錯用：摩擦由樁頂 0 線性增到 18 m 深的 50 kPa，之後 7 m 維持 50 kPa；4500 kN 中摩擦未承擔的部分才到樁底。",
        path=os.path.join(OUT, "SM-2014-2-fig-1-problem.svg"))


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


# ══════ fig-2：荷重傳遞與沉陷三成分（解題圖解）══════
# ── 由 SM-2014-2 §4 Step 2–6 解得 ──
from math import pi, sqrt
QT, LP, ZK, FK, EP, ES, MU, IWP = 4500.0, 25.0, 18.0, 50.0, 2.0e7, 3.0e4, 0.35, 0.85
DP = 1.2
AP, PP = pi * DP ** 2 / 4, pi * DP
def fz(z): return FK * min(z, ZK) / ZK
def nz(z):
    return QT - PP * (FK / ZK * z * z / 2 if z <= ZK else FK * ZK / 2 + FK * (z - ZK))
QWS = round(QT - nz(LP), 2); QWP = round(nz(LP), 2)
INTQ = 25 * QT - 7075 * PP
SE1 = INTQ / (AP * EP) * 1000
SE2 = (QWP / AP) * DP / ES * (1 - MU ** 2) * IWP * 1000
SE3 = (QWS / (PP * LP)) * DP / ES * (1 - MU ** 2) * (2 + 0.35 * sqrt(LP / DP)) * 1000
SE = [round(SE1, 2), round(SE2, 2), round(SE3, 2)]
assert (QWS, QWP, SE) == (3015.93, 1484.07, [3.79, 39.15, 4.04]), (QWS, QWP, SE)

def pan_n():
    cv = Canvas(480, 580); cv.panel("樁身軸力 N(z)", "樁頂 4500 kN，扣掉沿途摩擦 p∫f dz")
    m = PX(cv, 70, 40, 120, 60, 5000, 26)
    px_axes(m, [0, 1000, 2000, 3000, 4000, 5000], [0, 5, 10, 15, 20, 25], "N（kN）")
    zs = [LP * i / 250 for i in range(251)]
    cv.polygon([m.p(0, 0)] + [m.p(nz(z), z) for z in zs] + [m.p(0, LP)], C["fill_c"], "none")
    cv.poly([m.p(nz(z), z) for z in zs], C["compr"], 2.8)
    cv.line(m.p(0, ZK), m.p(5000, ZK), C["accent"], 1.4, dash="4 4")
    tag_px(cv, m.x(nz(ZK)) + 10, m.y(ZK), "18 m：%.1f" % nz(ZK), 12, C["compr"], anchor="start", weight="400")
    tag_px(cv, m.x(QWP) + 12, m.y(LP) - 4, "樁底 Qwp = %.2f kN" % QWP, 12, C["load"], anchor="start")
    tag_px(cv, m.x(2300), m.y(9), "面積 ∫N dz → Se1", 12, C["compr"], weight="400")
    cv.text_px(m.x(4400), m.y(20.6), "摩擦承擔", 12, C["muted"], anchor="end")
    cv.text_px(m.x(4400), m.y(21.9), "Qws = %.2f kN" % QWS, 12, C["muted"], anchor="end")
    return cv

def pan_bar():
    cv = Canvas(480, 580); cv.panel("沉陷三成分（mm）", "Se = Se1 + Se2 + Se3")
    m = PX(cv, 70, 40, 120, 60, 3, 50)          # 用 PX 只取縱向比例：v 為欄位、z 為沉陷
    px_axes(m, [], [0, 10, 20, 30, 40, 50], "", zlab="mm")
    labs = ["Se1 樁身壓縮", "Se2 樁底", "Se3 樁側"]
    cols = [C["compr"], C["load"], C["bmd"]]
    for i, (s, lab, col) in enumerate(zip(SE, labs, cols)):
        x0, x1 = 0.2 + i, 0.8 + i
        cv.polygon([m.p(x0, 0), m.p(x1, 0), m.p(x1, s), m.p(x0, s)], col, col, 1.2, op=0.55)
        cv.text_px(m.x(i + 0.5), m.y(s) + 16, "%.2f" % s, 13, col, weight="700")
        cv.text_px(m.x(i + 0.5), m.T - 14, lab, 12, C["text"])
    tag_px(cv, m.x(1.5), m.B - 30, "合計 %.2f mm（Se2 佔 %.0f%%）" % (sum(SE), SE[1] / sum(SE) * 100), 13, C["text"])
    return cv

compose([pan_n(), pan_bar()],
        title="圖 2　荷重傳遞：摩擦吃掉 2/3，樁底剩 1484 kN 卻貢獻 83% 沉陷",
        sub="Qwp 由力平衡 4500 − Qws 求得；Se1 用軸力分段積分，不套 ξ 係數",
        note="攔錯用：把 4500 kN 全部當樁底荷重，Se2 會放大 3 倍；Se3 公式的 P 是周長 πD，不是荷重。",
        path=os.path.join(OUT, "SM-2014-2-fig-2-load-transfer.svg"))
