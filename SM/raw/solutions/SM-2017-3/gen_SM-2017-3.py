# -*- coding: utf-8 -*-
"""SM-2017-3 圖解。
fig-1-problem：考卷圖 3-2（基地）重繪，幾何只取自題目正本 SM-2017-3-problem.md §4 判讀清單（#5–#7），不含任何解題結果。
圖 3-1 平鈑載重—沉陷量曲線為試驗曲線圖，不重繪（重繪等於自編數據），讀值見題目正本 §3。
用法：python gen_SM-2017-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
DF   = 1.0     # #5 開挖深＝基礎平面深 Df = 1.0 m（平鈑與基腳同在基礎平面）
P    = 0.3     # #4 平鈑寬 0.3 m
B    = 2.0     # 基腳 2 m × 2 m
GM   = 18.0    # #7 回填 γm = 18.0 kN/m³，q0 = γm·Df
T_F  = 0.35    # 基腳厚（考卷未標，示意）
COL  = 0.35    # 柱寬（示意）
X_P, X_F = -1.6, 0.9     # 平鈑、基腳中心位置（示意，照考卷附圖左右關係）
PIT  = (-2.4, 2.2)       # 開挖坑左右緣（示意）

def fig_problem():
    W, H = 900, 400
    XL, XR = -4.2, 4.2
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 0.4, XR + 1.6), (-1.0, DF + 1.25), 30, 30, 40, 40))
    Y = lambda d: -d + DF        # 以基礎平面為 y = 0
    # 砂土地盤（基礎平面以下）與坑外地盤
    soil_fill(cv, XL, XR, Y(DF + 0.9), Y(DF), "rgba(180,83,9,0.20)")
    soil_fill(cv, XL, PIT[0], Y(DF), Y(0), "rgba(180,83,9,0.20)")
    soil_fill(cv, PIT[1], XR, Y(DF), Y(0), "rgba(180,83,9,0.20)")
    cv.poly([(XL, Y(0)), (PIT[0], Y(0)), (PIT[0], Y(DF)), (PIT[1], Y(DF)), (PIT[1], Y(0)), (XR, Y(0))],
            C["member"], 2.6)
    cv.line((PIT[0], Y(0)), (PIT[1], Y(0)), C["member2"], 1.2, dash="6 4")       # 回填面（原地表）
    # 平鈑
    cv.polygon([(X_P - P/2, Y(DF)), (X_P + P/2, Y(DF)), (X_P + P/2, Y(DF - 0.06)), (X_P - P/2, Y(DF - 0.06))],
               "rgba(29,78,216,0.35)", C["deform"], 1.6)
    cv.text_px(cv.X(X_P), cv.Y(Y(DF + 0.28)), "0.3 m × 0.3 m 平鈑", 12.5, C["deform"], weight="700")
    # 基腳與柱
    cv.polygon([(X_F - B/2, Y(DF)), (X_F + B/2, Y(DF)), (X_F + B/2, Y(DF - T_F)), (X_F - B/2, Y(DF - T_F))],
               "rgba(29,78,216,0.18)", C["deform"], 2.2)
    cv.polygon([(X_F - COL/2, Y(DF - T_F)), (X_F + COL/2, Y(DF - T_F)), (X_F + COL/2, Y(-0.15)), (X_F - COL/2, Y(-0.15))],
               "rgba(29,78,216,0.18)", C["deform"], 2.2)
    cv.text_px(cv.X(X_F), cv.Y(Y(DF + 0.28)), "2 m × 2 m 基腳", 12.5, C["deform"], weight="700")
    cv.arrow((X_F, Y(-0.95)), (X_F, Y(-0.18)), C["load"], 3.2, 10)
    cv.math_px(cv.X(X_F + 0.15), cv.Y(Y(-0.8)), "Q_{a}", 15, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(X_F + 0.15) + 30, cv.Y(Y(-0.8)), "（kN）", 13, C["load"], anchor="start", weight="700")
    # 回填超載 q0
    cv.arrow((X_P + 0.75, Y(0.05)), (X_P + 0.75, Y(DF - 0.12)), C["accent"], 2.0, 8)
    cv.text_px(cv.X(PIT[0] - 1.25), cv.Y(Y(-0.35)), "回填", 13, C["accent"], anchor="end", weight="700")
    cv.math_px(cv.X(PIT[0] - 1.2), cv.Y(Y(-0.35)), "q_{0} = γ_{m}·D_{f}", 13, C["accent"], anchor="start", weight="700")
    cv.text_px(cv.X(PIT[1] + 0.15), cv.Y(Y(-0.35)), "回填", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(PIT[1] + 0.15) + 34, cv.Y(Y(-0.35)), "γ_{m} = 18.0 kN/m^{3}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(-3.4), cv.Y(Y(DF + 0.6)), "砂土", 13, C["text"], weight="700")
    cv.text_px(cv.X(XR + 0.25), cv.Y(Y(DF)), "基礎平面", 12.5, C["muted"], anchor="start")
    # 尺寸線
    cv.dim((XR - 0.6, Y(DF)), (XR - 0.6, Y(0)), "D_{f} = 1.0 m", 0, C["dim"], 13, label_off=-52)
    return cv

compose([fig_problem()],
        title="SM-2017-3 考卷圖 3-2 重繪（基地，砂土）",
        sub="依題目正本判讀清單；基腳厚、柱寬與平面位置為示意；圖 3-1 試驗曲線不重繪，讀值見題目正本 §3",
        note="攔錯用：平鈑試驗做在開挖後的基礎平面（Df = 1.0 m），與基腳同高；兩側回填形成超載 q0 = γm·Df。",
        path=os.path.join(OUT, "SM-2017-3-fig-1-problem.svg"))


# ══════ fig-2-conversion：解題圖解（2026-11-15 階段 E；數值取自勘誤後 SM-2017-3.md §4，非考卷曲線重繪）══════
# ── §4 Step 1–3（勘誤後正本）────────────────────────
Q_ULT_P = 219.0          # §4 Step 1 圖 3-1 讀 ΔH = 2.54 cm
Q_END   = 246.0          # §4 Step 1 曲線終點讀值（3.95 cm）
DH_P1   = 0.86           # §4 Step 2 平鈑在 qa(P) 下的沉陷讀值
Q_P2    = 62.0           # §4 Step 3 ΔH_P = 0.331 cm 讀值
FS_     = 2.0
Q0      = GM * DF                                  # 18.0
TP      = (2 * B / (B + P)) ** 2                   # 3.025
QA_P    = Q0 + (Q_ULT_P - Q0) / FS_                # 118.5
QA_F    = QA_P * B / P                             # 790.0
QA1     = (QA_F - Q0) * B * B                      # 3088
DH_F1   = DH_P1 * TP                               # 2.6
DH_P2   = 1.0 / TP                                 # 0.331
QA2     = (Q_P2 - Q0) * B * B                      # 176


def fig_conversion():
    W_, H_ = 1120, 600
    cv = Canvas(W_, H_, sx=1, bg="#FFFFFF")
    cv.panel(title="平鈑 → 2 m × 2 m 基腳的兩條換算路線",
             sub=esc("㈠ 承載力：q_a 乘 B/P；㈡ 沉陷：同一接觸壓力下 ΔH 乘 T&P 係數，q 不再乘 B/P"))
    def box(x, y, w, s1, s2, col):
        cv.rect_px(x, y, w, 58, "#F4F6FA", 9, col, 1.8)
        cv.text_px(x + w / 2, y + 20, s1, 12.5, C["muted"])
        cv.text_px(x + w / 2, y + 42, s2, 15, col, weight="700")
    def harrow(x0, x1, y, lab, col):
        cv.line((x0, H_ - y), (x1 - 8, H_ - y), col, 2.2)
        cv.polygon([(x1, H_ - y), (x1 - 10, H_ - y + 5), (x1 - 10, H_ - y - 5)], col)
        cv.text_px((x0 + x1) / 2, y - 12, lab, 11.5, col)
    # ㈠
    y1 = 112
    cv.text_px(36, y1 - 18, "㈠ 承載力控制（FS = 2）", 14, C["load"], anchor="start", weight="700")
    xs = [36, 270, 504, 738]
    box(xs[0], y1, 190, "平鈑 q_{ult}（ΔH = 2.54 cm）", "%.0f kN/m²" % Q_ULT_P, C["text"])
    box(xs[1], y1, 190, "q_a(P) = q0 + (q_{ult} − q0)/FS", "%.1f kN/m²" % QA_P, C["text"])
    box(xs[2], y1, 190, "q_a(F) = q_a(P) × B/P", "%.1f kN/m²" % QA_F, C["load"])
    box(xs[3], y1, 340, "Q_a = (q_a(F) − q0) × A", "≈ %.0f kN" % (round(QA1 / 10) * 10), C["load"])
    harrow(226, 270, y1 + 29, "", C["muted"]); harrow(460, 504, y1 + 29, "× 2/0.3", C["load"]); harrow(694, 738, y1 + 29, "", C["muted"])
    cv.text_px(36, y1 + 84, "對應沉陷（考卷成對換算）：平鈑在 %.1f kN/m² 下 ΔH_P ≈ %.2f cm × %.3f = %.1f cm"
               % (QA_P, DH_P1, TP, DH_F1), 12.5, C["text"], anchor="start")
    cv.text_px(36, y1 + 106, "同壓換算需平鈑在 %.0f kN/m² 的沉陷——超出曲線（終點 ≈ %.0f），只知 > 4 × %.3f ≈ %.0f cm"
               % (QA_F, Q_END, TP, 4 * TP), 12.5, C["load"], anchor="start")
    # ㈡
    y2 = 288
    cv.text_px(36, y2 - 18, "㈡ 沉陷量控制（ΔH_F = 1 cm）", 14, C["member"], anchor="start", weight="700")
    box(xs[0], y2, 190, "基腳容許沉陷", "ΔH_F = 1.0 cm", C["text"])
    box(xs[1], y2, 190, "ΔH_P = ΔH_F / %.3f" % TP, "%.3f cm" % DH_P2, C["text"])
    box(xs[2], y2, 190, "讀曲線（總接觸壓力）", "q ≈ %.0f kN/m²" % Q_P2, C["member"])
    box(xs[3], y2, 340, "Q_a = (q − q0) × A（q 不乘 B/P）", "≈ %.0f kN" % QA2, C["member"])
    harrow(226, 270, y2 + 29, esc("÷ T&P"), C["member"]); harrow(460, 504, y2 + 29, "圖 3-1", C["muted"]); harrow(694, 738, y2 + 29, "同壓力", C["member"])
    # 壓力軸
    ya = 500; x0, x1, qmax = 70, 1060, 800.0
    QX = lambda q: x0 + (x1 - x0) * q / qmax
    cv.text_px(36, ya - 74, "接觸壓力落在試驗曲線範圍內嗎？", 14, C["text"], anchor="start", weight="700")
    cv.rect_px(QX(0), ya - 22, QX(Q_END) - QX(0), 44, "rgba(29,78,216,0.12)", 4)
    cv.text_px(QX(0) + 4, ya - 34, "試驗曲線範圍 0–%.0f" % Q_END, 12, C["deform"], anchor="start", weight="700")
    cv.line((x0, H_ - ya), (x1, H_ - ya), C["muted"], 1.8)
    for q in range(0, 801, 100):
        cv.line((QX(q), H_ - ya + 5), (QX(q), H_ - ya - 5), C["muted"], 1.4)
        cv.text_px(QX(q), ya + 20, "%d" % q, 11.5, C["muted"])
    cv.text_px(x1, ya + 42, "q (kN/m²)", 12, C["muted"], anchor="end")
    for q, lab, col, up in ((Q_P2, "㈡ %.0f" % Q_P2, C["member"], True), (QA_P, "q_a(P) %.1f" % QA_P, C["text"], False),
                            (Q_ULT_P, "q_{ult} %.0f" % Q_ULT_P, C["text"], True), (QA_F, "㈠ 基腳 %.0f" % QA_F, C["load"], True)):
        cv.dot((QX(q), H_ - ya), 6, col)
        cv.text_px(QX(q), ya + (44 if q in (QA_P, Q_P2) else -34), lab, 12, col, weight="700")
    return cv

compose([fig_conversion()],
        title="SM-2017-3 解題圖解：承載力控制與沉陷量控制的換算路線",
        note="數值取自本題 §4；圖 3-1 曲線不重繪。攔錯用：㈡ 不可再乘 B/P；㈠ 的基腳壓力 790 kN/m² 已在試驗範圍外，不可外插曲線求沉陷。",
        path=os.path.join(OUT, "SM-2017-3-fig-2-conversion.svg"))
