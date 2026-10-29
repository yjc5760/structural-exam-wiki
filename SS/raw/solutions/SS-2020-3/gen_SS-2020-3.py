#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2020-3 圖解產生腳本（LRFD 梁柱：求弱軸最大工作彎矩 M_wy）

斷面性質、B1、φM_n、互制比全部由腳本重算，與 .md §4 的數字逐項對照。
執行：python3 gen_SS-2020-3.py   →   figs/*.svg
"""
import sys, os, math
# struct-diagram 的 primitives 取自本知識庫自帶的 skill 副本（repo 相對路徑，故可原地重跑）；
# 若把本檔搬到別處，設環境變數 SD_SKILL 指向 struct-diagram 目錄即可。
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose, member_shape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ══════════════════════════════════════════════════════════════
# L1：題目給定（§1）
# ══════════════════════════════════════════════════════════════
PW_   = 150.0     # tf   工作軸壓
MWX   = 6.0       # tf·m 工作強軸彎矩（兩端等值）
LEN   = 500.0     # cm
KX, KY = 1.8, 1.2
FY, E = 2.5, 2100.0     # tf/cm^2
R_LF  = 1.6       # 載重係數
PHI_C, PHI_B = 0.85, 0.90
D_, BF, TW, TF = 40.0, 40.0, 1.2, 2.2       # H 400x400x12x22（cm）

# ── L2 Step 1：斷面性質（§4 Step 1，全部自行計算）──
HW  = D_ - 2*TF
A   = 2*BF*TF + HW*TW
IX  = 2*(BF*TF**3/12 + BF*TF*((HW+TF)/2)**2) + TW*HW**3/12
SX  = 2*IX/D_
ZX  = BF*TF*(D_-TF) + TW*HW**2/4
IY  = TF*BF**3/6 + HW*TW**3/12
SY  = 2*IY/BF
ZY  = TF*BF**2/2 + HW*TW**2/4
RX, RY = math.sqrt(IX/A), math.sqrt(IY/A)

# ── Step 2～4：設計載重與柱強度（§4）──
PU      = R_LF * PW_
MUX0    = R_LF * MWX * 100                       # tf·cm
LAM_CX  = KX*LEN/(math.pi*RX)*math.sqrt(FY/E)
LAM_CY  = KY*LEN/(math.pi*RY)*math.sqrt(FY/E)
LAM_C   = max(LAM_CX, LAM_CY)
FCR     = math.exp(-0.419*LAM_C**2)*FY
PHI_PN  = PHI_C*FCR*A

# ── Step 5：撓曲強度（§4）──
LP      = 80*RY/math.sqrt(FY)
MNX     = FY*ZX
PHI_MNX = PHI_B*MNX
MNY_Z   = FY*ZY                 # 4432.0
MNY_LIM = 1.5*FY*SY             # 4401.0  ← 台灣 2010 之弱軸上限
MNY     = min(MNY_Z, MNY_LIM)
PHI_MNY = PHI_B*MNY
MNY_LIM_AISC = 1.6*FY*SY        # AISC 360-16 §F6.1

# ── Step 6：B1（§4）──
M1M2_X, M1M2_Y = -1.0, -0.5     # 兩軸皆單曲率


def pe1(I, k):
    return math.pi**2 * E * I / (k*LEN)**2


def b1_tw(p_ratio, m1m2):
    """台灣 (8.2-3)"""
    return max(1.0, 0.64/(1 - p_ratio)*(1 - m1m2) + 0.32*m1m2)


def b1_aisc(p_ratio, m1m2):
    """AISC App.8 之 C_m/(1 − P_u/P_e1)"""
    return max(1.0, (0.6 - 0.4*m1m2)/(1 - p_ratio))


PE1X_K1 = pe1(IX, 1.0)          # 規範明文：P_e1 之 K ≤ 1.0
PE1Y_K1 = pe1(IY, 1.0)
PE1X_KQ = pe1(IX, KX)           # 若誤用題給 K
PE1Y_KQ = pe1(IY, KY)

B1X = b1_tw(PU/PE1X_K1, M1M2_X)
B1Y = b1_tw(PU/PE1Y_K1, M1M2_Y)
B1Y_RAW = 0.64/(1 - PU/PE1Y_K1)*(1 - M1M2_Y) + 0.32*M1M2_Y     # 0.935（未取下限）
MUX = B1X*MUX0


def solve_mwy(phi_pn, phi_mnx, phi_mny, b1x, b1y, mux0=MUX0, r=R_LF):
    """由 H1-1a 解出工作彎矩 M_wy（tf·m）"""
    lhs = PU/phi_pn
    a = 8/9 * (b1y*r*100) / phi_mny
    b = 8/9 * (b1x*mux0) / phi_mnx
    return (1.0 - lhs - b) / a


MWY = solve_mwy(PHI_PN, PHI_MNX, PHI_MNY, B1X, B1Y)


# ══════════════════════════════════════════════════════════════
def fig1_loading():
    """圖 1：強軸／弱軸端彎矩重繪（單曲率判定）"""
    PWD, PH = 470, 500
    XL, XR, YL, YH = -0.92, 0.98, -0.20, 1.42
    Lm, Tm, Bm = 40, 112, 96
    sx = min((PWD - 2*Lm)/(XR-XL), (PH - Tm - Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    panels = []
    for tag, sub, m1m2, lab_big, lab_small, pe_k1, axis in (
            ("強軸（繞 x 軸）", f"兩端等值 M_{{wx}} = {MWX:g} tf·m", M1M2_X,
             f"M_{{wx}} = {MWX:g}", f"M_{{wx}} = {MWX:g}", PE1X_K1, "x"),
            ("弱軸（繞 y 軸）", "一端 M_{wy}、另一端 0.5M_{wy}", M1M2_Y,
             "M_{wy}", "0.5 M_{wy}", PE1Y_K1, "y")):
        cv = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
        cv.panel(tag, sub)
        # 單曲率撓曲：κ 隨端彎矩線性變化（M1/M2 為負 ⇒ 全長同號）
        r = abs(m1m2)
        mf = lambda xi: -(r + (1-r)*xi)          # 由 −r（小端，底）變到 −1（大端，頂），全長同號
        # w'' = M ⇒ 以數值積分求撓度（非描摹）
        n = 200
        w = [0.0]*(n+1); th = 0.0
        h = 1.0/n
        for i in range(n):
            th += mf(i*h + h/2)*h
            w[i+1] = w[i] + th*h
        corr = w[n]
        wf = lambda xi: (w[int(round(xi*n))] - corr*xi)
        amp = 0.24/max(abs(v) for v in
                       [w[i] - corr*(i/n) for i in range(n+1)])
        cv.line((0, 0), (0, 1), C["ghost"], 3.0, dash="7 5")
        cv.poly(member_shape((0, 0), (0, 1), lambda xi: amp*wf(xi)), C["deform"], 5.0)

        # 端彎矩（反轉向 ⇒ 單曲率）
        cv.moment_arrow((0, 1.0), r=26, ccw=False, color=C["accent"], w=2.6, span=250, start=120)
        cv.moment_arrow((0, 0.0), r=26, ccw=True, color=C["accent"], w=2.6, span=250, start=120)
        cv.math_px(cv.X(0) + 42, cv.Y(1.0) - 30, lab_big, 14.5, C["accent"], "start", weight="700")
        cv.math_px(cv.X(0) + 42, cv.Y(0.0) + 26, lab_small, 14.5, C["accent"], "start", weight="700")

        # 軸壓與側向支撐
        cv.arrow((0, 1.34), (0, 1.04), C["load"], 3.2, 10)
        cv.arrow((0, -0.14), (0, -0.02), C["load"], 3.2, 9)
        cv.math_px(cv.X(0) - 14, cv.Y(1.20), f"P_{{w}} = {PW_:g} tf", 13.5, C["load"], "end", weight="700")
        for y in (0.0, 1.0):
            cv.line((-0.16, y), (-0.06, y), C["bmd"], 3.0)
        cv.text_px(cv.X(-0.20), cv.Y(0.5), "兩端側向支撐", 12, C["bmd"], "end")
        cv.dim((0, 0), (0, 1), f"L = {LEN:g} cm", off=52, label_off=15)

        cv.math_px(PWD/2 - 30, PH - 74, f"M_{{1}}/M_{{2}} = {m1m2:+g}", 15.5,
                   C["text"], weight="700")
        cv.text_px(PWD/2 + 46, PH - 74, "（單曲率）", 13.5, C["text"], "start", weight="700")
        cv.math_px(PWD/2, PH - 48, f"P_{{e1}}(K=1) = {pe_k1:,.0f} tf", 14, C["bmd"], weight="700")
        cv.math_px(PWD/2, PH - 24,
                   f"B_{{1{axis}}} = {(B1X if axis=='x' else B1Y):.3f}", 15, C["bmd"], weight="700")
        panels.append(cv)

    compose(panels, cols=2,
            title="圖 1　兩軸端彎矩之轉向與曲率（決定 M1/M2 的正負）",
            sub="兩端力偶反轉向 ⇒ 內力彎矩沿全長同號 ⇒ 單曲率 ⇒ M1/M2 為負（規範明文）",
            note=f"弱軸計算值 {B1Y_RAW:.3f} 小於 1，依規範取下限 1.0；若誤判為雙曲率（正值）"
                 f"會低估放大、偏不安全",
            path=os.path.join(OUT, "SS-2020-3-fig-1-loading.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_b1():
    """圖 3：B1 隨 Pu/Pe1 之變化（兩式對照＋下限 1.0）"""
    W, H = 880, 540
    Lm, Rm, Tm, Bm = 96, 250, 112, 84
    XMAX, YLO, YHI = 0.34, 0.80, 1.60
    sxx = (W-Lm-Rm)/XMAX
    syy = (H-Tm-Bm)/(YHI-YLO)
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda p: Lm + p*sxx
    Y = lambda v: H - Bm - (v-YLO)*syy

    cv.parts.append(f'<line x1="{Lm}" y1="{Y(YLO)}" x2="{X(XMAX)+14}" y2="{Y(YLO)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(YLO)}" x2="{Lm}" y2="{Y(YHI)-8}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.math_px(X(XMAX) + 20, Y(YLO) + 6, "P_{u}/P_{e1}", 14, C["muted"], "start")
    cv.math_px(Lm + 10, Y(YHI) - 22, "B_{1}", 15, C["muted"], "start")
    for v in (0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5):
        cv.parts.append(f'<line x1="{Lm}" y1="{Y(v)}" x2="{X(XMAX)}" y2="{Y(v)}" '
                        f'stroke="{C["border"]}" stroke-width="1"/>')
        cv.text_px(Lm - 12, Y(v), f"{v:.1f}", 12, C["muted"], "end")
    for p in (0.0, 0.1, 0.2, 0.3):
        cv.text_px(X(p), Y(YLO) + 20, f"{p:.1f}", 12, C["muted"])

    def draw(fn, m1m2, col, dash=None):
        n = 300
        pts = " ".join(f"{X(XMAX*i/n):.2f},{Y(max(YLO, min(YHI, fn(XMAX*i/n, m1m2)))):.2f}"
                       for i in range(n+1))
        d = f' stroke-dasharray="{dash}"' if dash else ""
        cv.parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" '
                        f'stroke-width="3.2" stroke-linejoin="round"{d}/>')

    # 未取下限的原始式（虛線），用來顯示「為何要取 1.0」
    raw_tw = lambda p, m: 0.64/(1-p)*(1-m) + 0.32*m
    for m1m2, col in ((M1M2_X, C["bmd"]), (M1M2_Y, C["accent"])):
        cv.parts.append('')
        n = 300
        pts = " ".join(f"{X(XMAX*i/n):.2f},{Y(max(YLO, min(YHI, raw_tw(XMAX*i/n, m1m2)))):.2f}"
                       for i in range(n+1))
        cv.parts.append(f'<polyline points="{pts}" fill="none" stroke="{col}" '
                        f'stroke-width="1.8" stroke-dasharray="5 4" opacity="0.75"/>')
        draw(b1_tw, m1m2, col)
        draw(b1_aisc, m1m2, C["compr"] if m1m2 == M1M2_X else C["muted"], dash="8 5")

    # B1 ≥ 1.0 下限
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(1.0)}" x2="{X(XMAX)}" y2="{Y(1.0)}" '
                    f'stroke="{C["load"]}" stroke-width="2.2" stroke-dasharray="7 5"/>')
    cv.text_px(X(XMAX) - 6, Y(1.0) - 14, "規範下限 B_1 = 1.0", 12.5, C["load"], "end", weight="700")

    # 本題兩點（K = 1.0）
    for pr, val, lab, col in ((PU/PE1X_K1, B1X, f"強軸 B_1x = {B1X:.3f}", C["bmd"]),
                              (PU/PE1Y_K1, B1Y, f"弱軸 B_1y = {B1Y_RAW:.3f} → 1.0", C["accent"])):
        cv.parts.append(f'<circle cx="{X(pr):.2f}" cy="{Y(val):.2f}" r="6" fill="{col}" '
                        f'stroke="#FFFFFF" stroke-width="2"/>')
        cv.text_px(X(pr) + 12, Y(val) + (18 if col == C["bmd"] else -16), lab, 12.5, col, "start", weight="700")
        cv.parts.append(f'<line x1="{X(pr)}" y1="{Y(YLO)}" x2="{X(pr)}" y2="{Y(val)}" '
                        f'stroke="{col}" stroke-width="1.1" stroke-dasharray="4 3"/>')

    # 若改用題給 K，Pu/Pe1 會右移到哪裡
    for pr, col, lab, ytxt in ((PU/PE1X_KQ, C["bmd"], "強軸 K=1.8", 1.46),
                               (PU/PE1Y_KQ, C["accent"], "弱軸 K=1.2", 1.38)):
        cv.parts.append(f'<line x1="{X(pr)}" y1="{Y(YLO)}" x2="{X(pr)}" y2="{Y(ytxt)-10}" '
                        f'stroke="{col}" stroke-width="1.4" stroke-dasharray="2 4" opacity="0.8"/>')
        cv.text_px(X(pr) - 8, Y(ytxt), f"若改用題給 {lab}", 11.5, col, "end")

    cv.legend(W - Rm + 8, 178,
              [(C["bmd"], "台灣 (8.2-3)　M1/M2 = −1"),
               (C["accent"], "台灣 (8.2-3)　M1/M2 = −0.5"),
               (C["compr"], "AISC Cm/(1−p)　−1"),
               (C["muted"], "AISC Cm/(1−p)　−0.5"),
               (C["load"], "下限 1.0")], size=11.5, gap=21)
    cv.text_px(W - Rm + 8, 300, "虛細線＝未取下限之原始值", 11.5, C["muted"], "start")
    cv.math_px(W - Rm + 8, 336, f"P_{{e1x}} = {PE1X_K1:,.0f} tf", 12.5, C["bmd"], "start", weight="700")
    cv.math_px(W - Rm + 8, 358, f"P_{{e1y}} = {PE1Y_K1:,.0f} tf", 12.5, C["accent"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 3　B1 放大係數：台灣 (8.2-3) 與 AISC 兩式對照", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "P_e1 之 K 依規範取 ≤ 1.0（P-δ 屬構材內效應）；用題給 K 等於把側移柔度重複計入",
               13, C["muted"])
    cv.text_px(W/2, 84, f"單曲率 M1/M2 為負時 B_1 最大；本題弱軸原始值 {B1Y_RAW:.3f} 低於下限，取 1.0",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "兩式在常用範圍差異約 ±3%，且單曲率時台灣式較保守——趨勢一致可互為驗算",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-3-fig-3-b1-curve.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_mny():
    """圖 2：弱軸撓曲強度的上限控制"""
    W, H = 900, 400
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 300, 420
    peak = max(MNY_Z, MNY_LIM, MNY_LIM_AISC)
    rows = ((f"F_y Z_y", "全塑性彎矩", MNY_Z, C["muted"]),
            (f"1.5 F_y S_y", "台灣 2010 規範 6.6 節上限", MNY_LIM, C["load"]),
            (f"1.6 F_y S_y", "AISC 360-16 §F6.1 上限", MNY_LIM_AISC, C["compr"]))
    for i, (nm, desc, val, col) in enumerate(rows):
        y = 148 + i*66
        cv.math_px(x0 - 18, y - 8, nm, 15, C["text"], "end", weight="700")
        cv.text_px(x0 - 18, y + 14, desc, 12, C["muted"], "end")
        cv.rect_px(x0, y - 17, bw, 34, "#EDF1F6", 7)
        cv.rect_px(x0, y - 17, bw*val/peak, 34, col, 7)
        cv.text_px(x0 + bw*val/peak + 14, y, f"{val:,.1f} tf·cm", 13.5, col, "start", weight="700")
    # 控制值標示
    yc = 148 + 1*66
    cv.text_px(x0 + bw*MNY_LIM/peak - 14, yc, "控制", 12.5, "#FFFFFF", "end", weight="700")

    cv.text_px(W/2, 34, "圖 2　弱軸撓曲強度：Zy/Sy 略大於 1.5 時由上限控制", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, f"Z_y/S_y = {ZY:,.1f}/{SY:,.1f} = {ZY/SY:.3f} > 1.5 ⇒ 台灣 2010 取上限",
               13, C["muted"])
    cv.math_px(W/2, 88, f"M_{{ny}} = min(F_{{y}}Z_{{y}}, 1.5F_{{y}}S_{{y}}) = {MNY:,.1f}"
                        f"　⇒　φ_{{b}}M_{{ny}} = {PHI_MNY:,.1f} tf·cm", 15, C["bmd"], weight="700")
    cv.text_px(W/2, H - 52,
               f"上限只壓低 {100*(1-MNY/MNY_Z):.1f}%，但這是規範明文；漏檢即扣分",
               13, C["accent"])
    cv.text_px(W/2, H - 26,
               "物理上：I 型斷面繞弱軸彎曲近似兩片獨立矩形板，形狀因數恰為 1.5",
               12.5, C["muted"])
    cv.save(os.path.join(OUT, "SS-2020-3-fig-2-mny-limit.svg"))


# ══════════════════════════════════════════════════════════════
def fig4_interaction():
    """圖 4：H1-1a 的三項組成與四種算法的敏感度"""
    PWD, PH = 560, 420
    SCALE = 300.0

    # 主答（K = 1.0，台灣式）之三項
    t_ax = PU/PHI_PN
    t_mx = 8/9 * MUX/PHI_MNX
    t_my = 8/9 * (B1Y*R_LF*100*MWY)/PHI_MNY
    COLS = [C["compr"], C["bmd"], C["accent"]]

    p1 = Canvas(PWD, PH, sx=1)
    p1.panel("① H1-1a 的三項組成", f"解得 M_wy = {MWY:.2f} tf·m 時恰好用滿 1.0")
    x0 = 132
    p1.parts.append(f'<line x1="{x0+SCALE}" y1="112" x2="{x0+SCALE}" y2="250" '
                    f'stroke="{C["load"]}" stroke-width="2" stroke-dasharray="6 4"/>')
    p1.text_px(x0 + SCALE, 104, "上限 1.0", 12.5, C["load"], weight="700")
    y = 170
    p1.text_px(x0 - 14, y, "H1-1a", 15, C["text"], "end", weight="700")
    p1.rect_px(x0, y-22, SCALE, 44, "#EDF1F6", 7)
    xx = x0
    for t, col in zip((t_ax, t_mx, t_my), COLS):
        p1.rect_px(xx, y-22, SCALE*t, 44, col, 0)
        if SCALE*t > 40:
            p1.text_px(xx + SCALE*t/2, y, f"{t:.3f}", 13, "#FFFFFF", weight="700")
        xx += SCALE*t
    p1.text_px(x0 + SCALE + 16, y, f"= {t_ax+t_mx+t_my:.3f}", 15, C["bmd"], "start", weight="700")
    p1.legend(x0 - 108, 240,
              [(COLS[0], f"P_u/φ_cP_n = {t_ax:.3f}"),
               (COLS[1], f"(8/9)·M_ux/φ_bM_nx = {t_mx:.3f}"),
               (COLS[2], f"(8/9)·M_uy/φ_bM_ny = {t_my:.3f}")], size=12, gap=22)
    p1.math_px(PWD/2, PH - 62, f"φ_{{c}}P_{{n}} = {PHI_PN:,.1f} tf", 13.5, C["muted"])
    p1.math_px(PWD/2, PH - 40, f"φ_{{b}}M_{{nx}} = {PHI_MNX:,.1f}   φ_{{b}}M_{{ny}} = {PHI_MNY:,.1f} tf·cm",
               13.5, C["muted"])
    p1.text_px(PWD/2, PH - 18, "答案是工作彎矩：解出 M_uy 後要再除以 r = 1.6", 12.5, C["load"],
               weight="700")

    # ── 格 2：四種算法 ──
    p2 = Canvas(PWD, PH, sx=1)
    p2.panel("② 四種算法的答案區間", "取捨全在 P_e1 的 K 與 B_1 公式")
    variants = (
        ("K=1.0　台灣 (8.2-3)（主答）",
         solve_mwy(PHI_PN, PHI_MNX, PHI_MNY, b1_tw(PU/PE1X_K1, M1M2_X),
                   b1_tw(PU/PE1Y_K1, M1M2_Y)), C["bmd"]),
        ("K=1.0　AISC Cm/(1−p)",
         solve_mwy(PHI_PN, PHI_MNX, PHI_MNY, b1_aisc(PU/PE1X_K1, M1M2_X),
                   b1_aisc(PU/PE1Y_K1, M1M2_Y)), C["compr"]),
        ("題給 K　台灣 (8.2-3)",
         solve_mwy(PHI_PN, PHI_MNX, PHI_MNY, b1_tw(PU/PE1X_KQ, M1M2_X),
                   b1_tw(PU/PE1Y_KQ, M1M2_Y)), C["accent"]),
        ("題給 K　AISC Cm/(1−p)",
         solve_mwy(PHI_PN, PHI_MNX, PHI_MNY, b1_aisc(PU/PE1X_KQ, M1M2_X),
                   b1_aisc(PU/PE1Y_KQ, M1M2_Y)), C["muted"]),
    )
    vmax = max(v for _, v, _ in variants)
    bx, bw2 = 212, 226
    for i, (nm, v, col) in enumerate(variants):
        y = 150 + i*54
        p2.text_px(bx - 14, y, nm, 12, C["text"], "end",
                   weight="700" if i == 0 else "400")
        p2.rect_px(bx, y-15, bw2, 30, "#EDF1F6", 6)
        p2.rect_px(bx, y-15, bw2*v/vmax, 30, col, 6)
        p2.text_px(bx + bw2*v/vmax + 12, y, f"{v:.2f} tf·m", 13, col, "start", weight="700")
    lo = min(v for _, v, _ in variants)
    p2.text_px(PWD/2, PH - 44,
               f"四種算法落在 {lo:.2f}～{vmax:.2f} tf·m（相差 {100*(vmax/lo-1):.1f}%）",
               13.5, C["text"], weight="700")
    p2.text_px(PWD/2, PH - 20,
               "考場把所採的 K 寫清楚即可；量級判斷不受影響", 12.5, C["muted"])

    compose([p1, p2], cols=2,
            title=f"圖 4　互制方程式求解與取捨：Mwy = {MWY:.2f} tf·m（主答）",
            sub=f"Pu/φcPn = {t_ax:.3f} ≥ 0.2 ⇒ 用 H1-1a（含 8/9 係數）",
            note="Pe1 用題給 K 會把側移柔度重複計入 P-δ；本題 Mlt = 0，更不該讓 B1 承擔側移效應",
            path=os.path.join(OUT, "SS-2020-3-fig-4-interaction.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_loading(); fig2_mny(); fig3_b1(); fig4_interaction()
    print(f"A={A:.2f} Ix={IX:,.0f} Sx={SX:,.1f} Zx={ZX:,.1f} Iy={IY:,.0f} Sy={SY:,.1f} Zy={ZY:,.1f}")
    print(f"rx={RX:.2f} ry={RY:.2f} Lp={LP:.1f}")
    print(f"lam_cx={LAM_CX:.4f} lam_cy={LAM_CY:.4f} Fcr={FCR:.3f} phiPn={PHI_PN:.1f}")
    print(f"Zy/Sy={ZY/SY:.4f} MnyZ={MNY_Z:.1f} MnyLim={MNY_LIM:.1f} phiMny={PHI_MNY:.1f}")
    print(f"Pe1x={PE1X_K1:,.0f} Pe1y={PE1Y_K1:,.0f} B1x={B1X:.4f} B1y_raw={B1Y_RAW:.4f} B1y={B1Y:.3f}")
    print(f"Mwy={MWY:.3f} tf·m")
    print("done ->", OUT)
