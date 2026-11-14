#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2017-1 加大柱・雙折線本構 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2017-1.md §1 給定的原始資料；c_b、C_c、x̄_c、P_n,b、M_n,b
     一律由 bilinear_cc() / section() 現算，檔尾對 §4 公佈值 assert。
  2. 改 §1 任一數字（b、h、d'、f'c、根數）重跑，四張圖全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

2026-11-14 勘誤：擴柱後共 16 根 D25（原柱 8＋新增 8，題目正本判讀 #1）；原柱鋼筋假設距原柱面 6.5 cm（使用者定案）；
section() 改為多層鋼筋；e = 0 的軸力強度主線取 P(ε) 峰值（ε = ε_y）。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2017-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定
# ══════════════════════════════════════════════════════════
B      = 40.0      # 垂直彎曲方向寬 (cm)
H      = 70.0      # 彎曲方向全深 (cm)  ← 加大後 40×70
H_OLD  = 40.0      # 原有舊核心邊長 (cm)
DP     = 6.5       # 保護層（量至鋼筋中心）
FC     = 210.0     # f'c (kgf/cm^2)
FY     = 4200.0    # fy
ES     = 2.04e6
A_BAR  = 5.067     # D25 單根面積
N_SIDE = 4         # 每側根數（兩翼各 4 支）
C_OLD  = 6.5       # 原柱鋼筋距原柱面（考卷未給，假設＝新增鋼筋保護層；使用者定案）
EPS_CU = 0.003
EPS_PK = 0.002     # 雙折線峰值應變
DROP   = 0.8       # eps_cu 時的應力比

# ── 由上列推得 ──────────────────────────────────────────
D    = H - DP
AS   = N_SIDE * A_BAR
_X0  = (H - H_OLD) / 2                       # 原柱面距壓力面 15 cm
# 各層（距壓力面 cm, 面積）：新增 4／原柱 3／原柱 2／原柱 3／新增 4
LAYERS = [(DP, AS), (_X0 + C_OLD, 3 * A_BAR), (H / 2, 2 * A_BAR),
          (_X0 + H_OLD - C_OLD, 3 * A_BAR), (H - DP, AS)]
AST  = sum(a for _, a in LAYERS)
AG   = B * H
EPSY = FY / ES
CB   = EPS_CU / (EPS_CU + EPSY) * D
KGF_TF, KGCM_TFM = 1e-3, 1e-5


def fc_of(eps):
    """題目給定的雙折線本構。"""
    if eps <= 0:        return 0.0
    if eps <= EPS_PK:   return eps / EPS_PK * FC
    if eps <= EPS_CU:   return FC * (1 - (1 - DROP) * (eps - EPS_PK) / (EPS_CU - EPS_PK))
    return DROP * FC


def bilinear_cc(c):
    """壓力區合力與形心（距壓力面），對雙折線分區積分（梯形段＋三角形段）。"""
    xpk = c * (1 - EPS_PK / EPS_CU)          # eps = 0.002 的位置 = c/3
    C1 = B * xpk * (DROP * FC + FC) / 2
    x1 = xpk * (DROP * FC + 2 * FC) / (3 * (DROP * FC + FC))
    C2 = B * (c - xpk) * FC / 2
    x2 = xpk + (c - xpk) / 3
    Cc = C1 + C2
    return dict(C1=C1, x1=x1, C2=C2, x2=x2, xpk=xpk, Cc=Cc,
                xbar=(C1 * x1 + C2 * x2) / Cc)


def whitney_cc(c):
    b1 = 0.85 if FC <= 280 else max(0.65, 0.85 - 0.05 * (FC - 280) / 70)
    a = b1 * c
    return dict(a=a, Cc=0.85 * FC * a * B, xbar=a / 2, b1=b1)


def section(c, whitney=False):
    """平衡條件下的斷面內力。whitney=True 為（錯誤的）Whitney 近似對照。"""
    cc = whitney_cc(c) if whitney else bilinear_cc(c)
    Pn, Mn, rows = cc["Cc"], cc["Cc"] * (H / 2 - cc["xbar"]), []
    for d, A in LAYERS:
        eps = EPS_CU * (c - d) / c
        fs = max(-FY, min(FY, ES * eps))
        if whitney:
            fc_at = 0.85 * FC if (d < cc["a"] and fs > 0) else 0.0
        else:
            fc_at = fc_of(eps)                         # 排開的混凝土應力
        F = A * (fs - fc_at)
        rows.append(dict(d=d, eps=eps, fs=fs, fc_at=fc_at, F=F))
        Pn += F
        Mn += F * (H / 2 - d)
    return dict(cc=cc, rows=rows, eps_p=rows[0]["eps"], fc_at=rows[0]["fc_at"],
                Cs=rows[0]["F"], Ts=-rows[-1]["F"], Pn=Pn, Mn=Mn)


BAL = section(CB)
BAL_W = section(CB, whitney=True)


def P_axial(eps):
    """e = 0 時的軸力（全斷面同一應變）。"""
    return fc_of(eps) * (AG - AST) + min(FY, ES * eps) * AST


# ══════════════════════════════════════════════════════════
def _draw_section(cv):
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H)], C["fill_m"], C["member"], 2.6)
    x0 = (B - H_OLD) / 2
    y0 = (H - H_OLD) / 2
    cv.poly([(x0, y0), (x0 + H_OLD, y0), (x0 + H_OLD, y0 + H_OLD),
             (x0, y0 + H_OLD), (x0, y0)], C["ghost"], 2.0, dash="7 5")
    for y in (DP, D):                                   # 新增鋼筋（灰）
        for i in range(N_SIDE):
            xx = B * (i + 1) / (N_SIDE + 1)
            cv.dot((xx, y), 5.6, fill="#9AA3AE", stroke="#FFFFFF", w=1.6)
    xs3 = (x0 + C_OLD, x0 + H_OLD / 2, x0 + H_OLD - C_OLD)  # 原柱鋼筋（黑）
    for y, xs in ((y0 + C_OLD, xs3), (y0 + H_OLD / 2, (xs3[0], xs3[2])),
                  (y0 + H_OLD - C_OLD, xs3)):
        for xx in xs:
            cv.dot((xx, y), 5.6, fill=C["member"], stroke="#FFFFFF", w=1.6)


def fig1_section():
    W, HH = 700, 560
    L, Rm, T, Bm = 100, 268, 84, 92
    sx = min((W - L - Rm) / B, (HH - T - Bm) / H)
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")
    _draw_section(cv)
    cv.dim((0, 0), (B, 0), f"b = {B:.0f} cm", off=36, color=C["dim"])
    cv.dim((B, 0), (B, H), f"h = {H:.0f} cm", off=40, color=C["dim"])
    cv.dim((0, H), (0, D), f"d' = {DP:.1f}", off=40, color=C["compr"])
    cv.line((0, D), (B, D), C["compr"], 1.4, dash="5 4")
    cv.line((0, DP), (B, DP), C["load"], 1.4, dash="5 4")
    cv.text_px(cv.X(B) + 8, cv.Y(DP), f"d = {D:.1f} cm", 13, C["load"], "start")

    x = W - Rm + 12
    y = 118
    for col, expr, desc in [
        (C["member"], f"A_g = {B:.0f}×{H:.0f} = {AG:,.0f} cm^{{2}}", "加大後全斷面"),
        (C["member"], f"A_{{st}} = 16×{A_BAR} = {AST:.2f} cm^{{2}}",
         f"新增 2×{N_SIDE} 支（灰）＋原柱 8 支（黑）"),
        (C["member"], f"ρ_g = {100*AST/AG:.2f}%", "在 1%~8% 內"),
        (C["compr"], f"d = h − d' = {D:.1f} cm", "有效深度"),
    ]:
        cv.rect_px(x, y - 15, 10, 30, col, 3)
        cv.math_px(x + 20, y - 7, expr, 13.5, col, "start", weight="700")
        cv.text_px(x + 20, y + 14, desc, 12, C["muted"], "start")
        y += 54
    cv.text_px(x, y + 6, "灰虛線＝原 40×40 舊核心", 12.5, C["muted"], "start")
    cv.text_px(x, y + 28, "兩翼各 15 cm 為新增混凝土", 12.5, C["muted"], "start")
    cv.text_px(x, y + 56, "⚠ 原柱 8 支也要算", 13, C["load"], "start", weight="700")
    cv.text_px(x, y + 78, "原柱鋼筋距原柱面 6.5 cm", 12.2, C["muted"], "start")
    cv.text_px(x, y + 98, "（考卷未給，假設）", 12.2, C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 1　加大柱斷面（向量重繪）", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58, "彎曲方向為 70 cm 全深；16 支 D25 沿深度分 5 層（4／3／2／3／4）",
               12.8, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig2_bilinear():
    W, HH = 660, 520
    L, Rm, T, Bm = 96, 130, 84, 82
    e_max, f_max = 0.0035, FC * 1.18
    sx = (W - L - Rm) / e_max
    sy = (HH - T - Bm) / f_max
    k = sy / sx
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")

    cv.arrow((0, 0), (e_max, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, f_max * k), C["muted"], 1.8, 9)
    pts = [(e / 1e6, fc_of(e / 1e6) * k) for e in range(0, int(e_max * 1e6) + 1, 5)]
    cv.polygon([(0, 0)] + [p for p in pts if p[0] <= EPS_CU] + [(EPS_CU, 0)],
               C["fill_c"], "none")
    cv.poly([p for p in pts if p[0] <= EPS_CU], C["compr"], 3.4)

    for e, lab in [(EPS_PK, f"1.0f'_c = {FC:.0f}"), (EPS_CU, f"0.8f'_c = {DROP*FC:.0f}")]:
        f = fc_of(e)
        cv.line((e, 0), (e, f * k), C["muted"], 1.3, dash="4 4")
        cv.line((0, f * k), (e, f * k), C["muted"], 1.3, dash="4 4")
        cv.dot((e, f * k), 5.6, fill=C["accent"], stroke="#FFFFFF", w=1.8)
        cv.text_px(cv.X(e) + 8, cv.Y(f * k) - 12, lab, 13, C["accent"],
                   "start", weight="700")
        cv.text_px(cv.X(e), cv.Y(0) + 20, f"{e:.3f}", 12.5, C["muted"])
    cv.text_px(cv.X(e_max / 2), HH - 40, "混凝土壓應變 ε_c", 13.5, C["muted"])
    cv.text_px(cv.X(0) - 60, cv.Y(f_max * k / 2), "f_c", 15, C["muted"])

    cv.text_px(cv.X(0.0009), cv.Y(fc_of(0.0009) * k) - 26, "上升段", 13,
               C["compr"], weight="700")
    cv.text_px(cv.X(0.0025), cv.Y(fc_of(0.0025) * k) - 26, "下降段", 13,
               C["compr"], weight="700")

    cv.rect_px(L, HH - 74, W - L - 40, 40, "#FFF6E8", 8, C["load"], 1.3)
    cv.text_px(L + (W - L - 40) / 2, HH - 54,
               "題目給了本構就不能再套 Whitney：這條線沒有 0.85f'_c 這個值",
               13, C["load"], weight="700")

    cv.text_px(W / 2, 34, "圖 2　題目指定的雙折線應力—應變關係", 17,
               C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"峰值 1.0f'_c 在 ε = {EPS_PK}，極限 ε_cu = {EPS_CU} 時降為 {DROP}f'_c",
               12.8, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig3_stress_block():
    """平衡點壓力區：雙折線分區積分 vs Whitney 近似（疊圖）。"""
    W, HH = 1040, 620
    L, Rm, T, Bm = 116, 400, 104, 104
    f_span = FC * 1.35
    sx = (W - L - Rm) / f_span
    sy = (HH - T - Bm) / CB
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")

    def Y(depth):      # 距壓力面 depth → 模型 y（壓力面在上）
        return (CB - depth) * sy / sx

    bl = BAL["cc"]
    wt = BAL_W["cc"]

    # 中性軸與壓力面
    cv.line((0, Y(0)), (f_span, Y(0)), C["member"], 2.2)
    cv.line((0, Y(CB)), (f_span, Y(CB)), C["member"], 1.6, dash="6 4")
    cv.text_px(cv.X(0) + 6, cv.Y(Y(0)) - 14, "壓力面", 12.5, C["muted"], "start")
    cv.text_px(cv.X(0) + 6, cv.Y(Y(CB)) + 18,
               f"中性軸 c_b = {CB:.2f} cm", 12.5, C["muted"], "start")

    # Whitney 矩形（灰，錯誤對照）
    cv.polygon([(0, Y(0)), (0.85 * FC, Y(0)), (0.85 * FC, Y(wt["a"])), (0, Y(wt["a"]))],
               "rgba(120,130,140,0.18)", "none")
    cv.poly([(0, Y(0)), (0.85 * FC, Y(0)), (0.85 * FC, Y(wt["a"])),
             (0, Y(wt["a"])), (0, Y(0))], C["ghost"], 2.0, dash="6 4")
    cv.text_px(cv.X(0.85 * FC) + 6, cv.Y(Y(wt["a"] * 0.55)),
               "Whitney 0.85f'_c×a", 12.5, C["ghost"], "start", weight="700")

    # 雙折線實際分佈
    prof = []
    for i in range(0, 201):
        dep = CB * i / 200
        eps = EPS_CU * (CB - dep) / CB
        prof.append((fc_of(eps), Y(dep)))
    cv.polygon([(0, Y(0))] + prof + [(0, Y(CB))], C["fill_c"], C["compr"], 3.0)

    # 峰值線與分段界
    cv.line((0, Y(bl["xpk"])), (FC, Y(bl["xpk"])), C["accent"], 1.6, dash="5 4")
    cv.text_px(cv.X(FC) + 8, cv.Y(Y(bl["xpk"])) - 12,
               f"峰值 ε = {EPS_PK}", 12.5, C["accent"], "start", weight="700")
    cv.text_px(cv.X(FC) + 8, cv.Y(Y(bl["xpk"])) + 8,
               f"x = c_b/3 = {bl['xpk']:.2f} cm", 12, C["muted"], "start")

    # 兩個合力箭頭
    _eps_at = EPS_CU * (CB - bl["xbar"]) / CB
    cv.arrow((fc_of(_eps_at), Y(bl["xbar"])), (0.0, Y(bl["xbar"])),
             C["compr"], 3.4, 11)
    cv.dot((0, Y(bl["xbar"])), 5.4, fill=C["compr"], stroke="#FFFFFF", w=1.8)
    cv.text_px(cv.X(0) - 12, cv.Y(Y(bl["xbar"])),
               f"C_c = {bl['Cc']*KGF_TF:,.1f} tf", 13.5, C["compr"], "end",
               weight="700")
    cv.text_px(cv.X(0) - 12, cv.Y(Y(bl["xbar"])) + 20,
               f"x̄ = {bl['xbar']:.2f} cm", 12.5, C["muted"], "end")

    # 右側對照表
    x = W - Rm + 14
    y = 118
    cv.text_px(x, y - 30, "兩種算法的差距", 15, C["text"], "start", weight="700")
    rows = [
        ("C_c", bl["Cc"] * KGF_TF, wt["Cc"] * KGF_TF, "tf"),
        ("x̄", bl["xbar"], wt["xbar"], "cm"),
        ("P_{n,b}", BAL["Pn"] * KGF_TF, BAL_W["Pn"] * KGF_TF, "tf"),
        ("M_{n,b}", BAL["Mn"] * KGCM_TFM, BAL_W["Mn"] * KGCM_TFM, "tf·m"),
    ]
    cv.text_px(x, y, "量", 12.5, C["muted"], "start")
    cv.text_px(x + 108, y, "雙折線", 12.5, C["compr"], "start", weight="700")
    cv.text_px(x + 178, y, "Whitney", 12.5, C["ghost"], "start", weight="700")
    y += 26
    for name, a, bb, u in rows:
        cv.math_px(x, y, name, 13, C["text"], "start")
        cv.text_px(x + 108, y, f"{a:,.2f}", 12.8, C["compr"], "start", weight="700")
        cv.text_px(x + 178, y, f"{bb:,.2f}", 12.8, C["ghost"], "start")
        cv.text_px(x + 246, y, f"{100*(bb-a)/a:+.1f}%", 12.8,
                   C["load"] if abs(bb - a) / a > 0.03 else C["muted"],
                   "start", weight="700")
        y += 30
    cv.rect_px(x - 6, y + 24, W - x - 24, 92, "#FFF6E8", 9, C["load"], 1.3)
    cv.text_px(x + 6, y + 48, "偷套 Whitney 的代價", 13.5, C["load"],
               "start", weight="700")
    cv.text_px(x + 6, y + 72,
               f"C_c 高估 {100*(wt['Cc']-bl['Cc'])/bl['Cc']:.1f}%、"
               f"P_{{n,b}} 高估 {100*(BAL_W['Pn']-BAL['Pn'])/BAL['Pn']:.1f}%", 12.5,
               C["muted"], "start")
    cv.text_px(x + 6, y + 92,
               f"M_{{n,b}} 只差 {100*(BAL_W['Mn']-BAL['Mn'])/BAL['Mn']:.1f}%——彎矩看不太出來，但軸力錯得很明顯", 12.2,
               C["muted"], "start")

    cv.text_px(W / 2, 34, "圖 3　平衡點壓力區：雙折線分區積分 vs Whitney 近似",
               17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "藍色為題目本構的真實分佈（上梯形＋下三角）；灰虛線為 Whitney 矩形",
               12.8, C["muted"])
    cv.text_px(W / 2, HH - 22,
               f"封閉解可驗算：C_c = (19/30)·b·c·f'_c = {19/30*B*CB*FC:,.0f} kgf，"
               f"x̄ = 0.3743c = {0.374269*CB:.2f} cm", 13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
def fig4_axial():
    W, HH = 820, 520
    L, Rm, T, Bm = 100, 310, 90, 86
    e_max = 0.0035
    p_max = 1000e3
    sx = (W - L - Rm) / e_max
    sy = (HH - T - Bm) / p_max
    k = sy / sx
    cv = Canvas(W, HH, sx=sx, ox=L, oy=Bm, bg="#FFFFFF")

    cv.arrow((0, 0), (e_max, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, p_max * k), C["muted"], 1.8, 9)
    pts = [(e / 1e6, P_axial(e / 1e6) * k) for e in range(0, int(EPS_CU * 1e6) + 1, 5)]
    cv.poly(pts, C["compr"], 3.2)

    for e, col, note in [(EPSY, C["accent"], "P(ε) 的極大值（本解採用）"),
                         (EPS_CU, C["load"], "ε_cu 端點（對照）")]:
        p = P_axial(e)
        cv.line((e, 0), (e, p * k), col, 1.4, dash="5 4")
        cv.dot((e, p * k), 6.0, fill=col, stroke="#FFFFFF", w=2.0)
        _lab = f"ε_y = {e:.5f}" if abs(e - EPSY) < 1e-9 else f"ε = {e:.3f}"
        cv.text_px(cv.X(e) + 10, cv.Y(p * k) - 10,
                   f"{_lab} → {p*KGF_TF:,.0f} tf", 13, col, "start", weight="700")
        cv.text_px(cv.X(e) + 10, cv.Y(p * k) + 10, note, 12, C["muted"], "start")
        cv.text_px(cv.X(e), cv.Y(0) + 20, f"{e:.5f}" if abs(e - EPSY) < 1e-9 else f"{e:.3f}", 12.5, C["muted"])

    for p in range(0, int(p_max) + 1, 200000):
        cv.line((0, p * k), (0.00006, p * k), C["muted"], 1.2)
        cv.text_px(cv.X(0) - 10, cv.Y(p * k), f"{p*KGF_TF:,.0f}", 12, C["muted"], "end")
    cv.text_px(cv.X(e_max / 2), HH - 40, "全斷面同一壓應變 ε", 13.5, C["muted"])
    cv.text_px(cv.X(0) - 66, cv.Y(p_max * k / 2), "P (tf)", 13.5, C["muted"])

    x = W - Rm + 100
    cv.text_px(x, 118, "e = 0 的「軸壓強度」", 14, C["text"], "start", weight="700")
    y = 146
    for e in (0.0018, EPS_PK, round(EPSY, 6), 0.0025, EPS_CU):
        fs = min(FY, ES * e)
        cv.text_px(x, y, f"ε={e:.4f}", 12.2, C["muted"], "start")
        cv.text_px(x + 88, y, f"{P_axial(e)*KGF_TF:,.0f} tf", 12.2,
                   C["accent"] if abs(e - EPSY) < 1e-5 else
                   (C["load"] if abs(e - EPS_CU) < 1e-9 else C["muted"]),
                   "start", weight="700" if (abs(e - EPSY) < 1e-5 or e == EPS_CU) else "400")
        y += 24
    cv.text_px(x, y + 14, "16 支鋼筋時峰值在 ε = ε_y：", 12.2, C["muted"], "start")
    cv.text_px(x, y + 34, f"鋼筋剛降伏、混凝土 {fc_of(EPSY):.1f}", 12.2, C["muted"], "start")
    cv.text_px(x, y + 54, "再壓下去混凝土掉得比鋼筋多", 12.2, C["load"], "start", weight="700")

    cv.text_px(W / 2, 34, "圖 4　e = 0 時軸力隨應變的變化", 17, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               "雙折線下軸力是應變的函數，「強度」取哪一點必須說清楚", 12.8, C["muted"])
    cv.text_px(W / 2, HH - 18,
               f"取 ε_cu = 0.003 得 {P_axial(EPS_CU)*KGF_TF:,.0f} tf；取 P(ε) 峰值得 {P_axial(EPSY)*KGF_TF:,.0f} tf"
               f"——兩者差 {100*(P_axial(EPSY)-P_axial(EPS_CU))/P_axial(EPS_CU):.1f}%",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════
# 題目附圖重繪（2026-11-14，RC-U1-2 題目正本推廣・批 1）
# 依據：題目正本 <id>-problem.md §4 判讀清單（已確認）。只畫考卷給的東西，不含解題結果；
# 考卷未標尺寸的位置（如鋼筋在非彎曲方向的間距）畫成示意，並在副標寫明。
# ══════════════════════════════════════════════════════════
def _pc(Wm, Hm, maxpx=330, l=90, r=110, t=120, b=110):
    s = maxpx / max(Wm, Hm)
    return Canvas(int(Wm * s + l + r), int(Hm * s + t + b), sx=s, ox=l, oy=b)


def _prect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _pbar(cv, p, r=1.25, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)

P_W, P_H = 15 + 40 + 15.0, 40.0      # 判讀 #4
P_COVER = 6.5                         # 判讀 #2（使用者確認：量至鋼筋中心）


def fig1_problem():
    W, H = P_W, P_H
    cv = _pc(W, H)
    _prect(cv, 0, 0, 15, H, fill="#FFFFFF", w=2.0, dash="7 5")
    _prect(cv, W - 15, 0, W, H, fill="#FFFFFF", w=2.0, dash="7 5")
    _prect(cv, 15, 0, W - 15, H, fill="#EDF1F6")
    cv.poly([(19, 4), (W - 19, 4), (W - 19, H - 4), (19, H - 4), (19, 4)], C["muted"], 1.4)
    for x in (22.0, 35.0, 48.0):          # 原柱鋼筋位置考卷未給（示意，判讀 #3）
        for y in ((7.0, 20.0, 33.0) if x != 35.0 else (7.0, 33.0)):
            _pbar(cv, (x, y), 1.3)
    for x in (P_COVER, W - P_COVER):      # 新增鋼筋：垂直間距考卷未標（示意）
        for y in (8.0, 16.0, 24.0, 32.0):
            _pbar(cv, (x, y), 1.3, fill="#9AA3AE")
    cv.text((35, 20), "原柱 8-#8", 13, weight="700")
    for a, b_ in ((0.0, 15.0), (15.0, W - 15), (W - 15, W)):
        cv.dim((a, 0), (b_, 0), f"{b_ - a:.0f} cm", off=28, label_off=14)
    cv.dim((0, H), (P_COVER, H), f"{P_COVER} cm", off=-24, label_off=-14)
    cv.dim((W, H), (W, 0), f"{H:.0f} cm", off=-30, label_off=-30)
    return compose([cv], title=f"{TAG} 題目附圖（圖 1 重繪）",
                   sub="依題目正本判讀清單 #1–#5；原柱鋼筋位置、新增鋼筋垂直間距考卷未標（示意）",
                   note="擴柱後共 16 根 D25（原柱 8＋新增 8，灰色）；保護層 6.5 cm 量至新增鋼筋中心")


FIGURES = [
    ("1-problem", fig1_problem,
     "漏掉原柱 8 根鋼筋；保護層基準弄錯"),
    ("1-section",      fig1_section,
     "漏掉原柱 8 支鋼筋（只算新增 8 支）"),
    ("2-bilinear",     fig2_bilinear,
     "題目已給本構卻仍套 Whitney 的 0.85f'_c"),
    ("3-stress-block", fig3_stress_block,
     "用 C_c = 0.85f'_c·a·b 取代分區積分（C_c 高估 14%、P_n,b 高估 13%）"),
    ("4-axial",        fig4_axial,
     "把 ε_cu = 0.003 的軸力當成唯一答案，沒發現 P(ε) 的峰值在 ε = ε_y"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    b = BAL
    checks = [
        ("A_g",       AG,                    2800.0,  0.1),
        ("A_st",      AST,                   81.072,  0.01),
        ("eps_y",     EPSY,                  0.002059, 1e-6),
        ("c_b",       CB,                    37.657,  0.005),
        ("x_peak",    b["cc"]["xpk"],        12.552,  0.005),
        ("C_1",       b["cc"]["C1"],         94896,   3),
        ("x_1",       b["cc"]["x1"],         6.509,   0.005),
        ("C_2",       b["cc"]["C2"],         105440,  3),
        ("x_2",       b["cc"]["x2"],         20.921,  0.005),
        ("C_c",       b["cc"]["Cc"],         200335,  5),
        ("xbar_c",    b["cc"]["xbar"],       14.094,  0.005),
        ("eps'_s",    b["eps_p"],            0.002482, 1e-6),
        ("排開 f_c",   b["fc_at"],            189.75,  0.05),
        ("F 6.5",     b["rows"][0]["F"],     81280,   5),
        ("F 21.5",    b["rows"][1]["F"],     37861,   5),
        ("F 35",      b["rows"][2]["F"],     4151,    5),
        ("F 48.5",    b["rows"][3]["F"],     -26787,  5),
        ("F 63.5",    b["rows"][4]["F"],     -85126,  5),
        ("P_n,b tf",  b["Pn"] * KGF_TF,      211.71,  0.05),
        ("M_n,b tfm", b["Mn"] * KGCM_TFM,    98.04,   0.02),
        ("P(0.003)tf", P_axial(EPS_CU) * KGF_TF, 797.3, 0.2),
        ("P(0.002)tf", P_axial(EPS_PK) * KGF_TF, 901.7, 0.2),
        ("P(ε_y)tf",  P_axial(EPSY) * KGF_TF, 904.8, 0.2),
        ("Whitney C_c", BAL_W["cc"]["Cc"],   228540,  20),
        ("Whitney P_n,b", BAL_W["Pn"] * KGF_TF, 239.71, 0.05),
    ]
    print("── 與 RC-2017-1.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<12} 算得 {got:>12.5f}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print(f"  （對照）Whitney 高估 C_c {100*(BAL_W['cc']['Cc']-b['cc']['Cc'])/b['cc']['Cc']:.1f}%、"
          f"P_n,b {100*(BAL_W['Pn']-b['Pn'])/b['Pn']:.1f}%")

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
