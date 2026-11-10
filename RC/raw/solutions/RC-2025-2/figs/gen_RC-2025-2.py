#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2025-2 耐震梁（特殊矩形框架梁）靠柱端剪力筋設計 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2025-2.md §1 給定的原始資料（斷面、配筋、載重、材料）；
     d、a、M_pr、V_seis、V_e、V_c、V_s、s_req、s_o、2h、包絡線各點、
     φV_s、φ(V_c+V_s)、V_s,max、A_v,min/s 全部由這些原始值現算，
     檔尾對 §4／§Step 8 公佈值逐項 assert。
  2. 改 §1 任一輸入（例如 h、d'、根數、w_u、l_n、s_dense）重跑，
     四張圖的幾何、箍筋根數與位置、包絡線與門檻線全部跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。

用法：
    STRUCTDRAW_DIR=<skill>/scripts python3 gen_RC-2025-2.py figs
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2025-2"

# ══════════════════════════════════════════════════════════
# §1 原始給定（RC-2025-2.md「1. 原始題目重述」，不含任何解題結果）
# ══════════════════════════════════════════════════════════
FC, FY, FYT = 280.0, 4200.0, 2800.0    # kgf/cm^2（混凝土、主筋、D13 箍筋）
BW, HH, DP = 60.0, 76.0, 9.0           # 梁寬、梁總高、面至縱向筋形心（頂底皆同）cm
N_TOP, N_BOT = 8, 6                    # 柱面處頂／底 D32 根數
AB_D32, DB_D32 = 8.14, 3.22            # D32 單支面積 cm^2、標稱直徑 cm
AB_D13, DB_D13 = 1.27, 1.27            # D13 單支面積 cm^2、標稱直徑 cm
LN = 900.0                             # 淨跨距 cm（= 9 m）
WU = 20.0                              # 因數化重力均布載重 kgf/cm（= 2 tf/m）
CC = 4.0                               # 淨保護層 cm（§5 爭議3 之排筋檢核用）
PHI = 0.75                             # 剪力強度折減係數
OVER = 1.25                            # 可能彎矩強度之鋼筋超強係數 §18.6.5.1
N_LEG_D = 4                            # 密箍區箍筋腳數（外箍 2 腳 + 2 支繫筋）
N_LEG_G = 2                            # 一般區箍筋腳數（外箍）
S_DENSE, S_GEN, S_FIRST = 15.0, 20.0, 5.0   # 採用間距與第一支箍距柱面 cm
TF = 1e-3                              # kgf → tf
TFM = 1e-5                             # kgf·cm → tf·m

# ── 由上列現算（鐵則 1） ──────────────────────────────────
D = HH - DP                                     # 有效深度
AS_TOP, AS_BOT = N_TOP * AB_D32, N_BOT * AB_D32
FY_PR = OVER * FY                               # 1.25 f_y
SQFC = math.sqrt(FC)

A_TOP = AS_TOP * FY_PR / (0.85 * FC * BW)       # 等值應力塊深度（頂筋受拉）
A_BOT = AS_BOT * FY_PR / (0.85 * FC * BW)
MPR_N = AS_TOP * FY_PR * (D - A_TOP / 2)        # kgf·cm，頂筋受拉
MPR_P = AS_BOT * FY_PR * (D - A_BOT / 2)        # kgf·cm，底筋受拉

V_SEIS = (MPR_N + MPR_P) / LN                   # 地震（塑鉸）引致剪力 kgf
V_GRAV = WU * LN / 2                            # 重力剪力 kgf
V_E = V_SEIS + V_GRAV                           # 控制端（重力與地震同向）
V_E_MIN = V_SEIS - V_GRAV                       # 另一端
RATIO = V_SEIS / V_E                            # 地震剪力佔比 → V_c = 0 判準

VS_REQ = V_E / PHI                              # 密箍區 V_c = 0，全由箍筋承擔
AV_D = N_LEG_D * AB_D13                         # 密箍區 A_v（4 腳）
AV_G = N_LEG_G * AB_D13                         # 一般區 A_v（2 腳）
S_REQ = AV_D * FYT * D / VS_REQ                 # 強度需求間距
S_O = min(D / 4, 6 * DB_D32, 15.0)              # 耐震間距限制 §18.6.4.4
L_HINGE = 2 * HH                                # 密箍區長度（自柱面起）
VS_MAX = 2.12 * SQFC * BW * D                   # §22.5.1.2 斷面上限
AVMIN_S = max(3.5 * BW / FYT, 0.2 * SQFC * BW / FYT)
PHI_VS_D = PHI * AV_D * FYT * D / S_DENSE       # 密箍區實配 φV_s（V_c = 0）

VC = 0.53 * SQFC * BW * D                       # 一般區可計入之混凝土貢獻
PHI_VC = PHI * VC


def Ve(x):
    """設計剪力包絡線（x 自左柱面量起，cm；回傳 kgf）= 兩搖擺方向取大。"""
    return max(V_E - WU * x, V_E_MIN + WU * x)


X_HINGE_OUT = L_HINGE                           # 一般區控制點：密箍區外緣
VE_OUT = Ve(X_HINGE_OUT)
VE_MID = Ve(LN / 2)
VS_GEN = VE_OUT / PHI - VC                      # 一般區所需 V_s
S_GEN_REQ = AV_G * FYT * D / VS_GEN             # 一般區強度需求間距
PHI_CAP_G = PHI * (VC + AV_G * FYT * D / S_GEN)  # 一般區實配 φ(V_c+V_s)
X_CAP_G = (V_E - PHI_CAP_G) / WU                # 一般區配置不足的起點（自柱面）

# 排筋幾何（§5 爭議3、爭議4）：最外層主筋形心至側面
X_EDGE = CC + DB_D13 + DB_D32 / 2
SP_TOP = (BW - 2 * X_EDGE) / (N_TOP - 1)
SP_BOT = (BW - 2 * X_EDGE) / (N_BOT - 1)
TIE_IDX = (2, N_TOP - 3)                        # 兩支繫筋掛在第 3、6 根頂筋
TIE_X = [X_EDGE + SP_TOP * i for i in TIE_IDX]
LEG_X = [CC, TIE_X[0], TIE_X[1], BW - CC]       # 4 腳的水平位置

# 箍筋實際位置（由 S_FIRST / S_DENSE / S_GEN 現算，不可隨手畫）
DENSE_L, k = [], 0
while S_FIRST + S_DENSE * k <= L_HINGE:
    DENSE_L.append(S_FIRST + S_DENSE * k); k += 1
GEN_L, x = [], DENSE_L[-1] + S_GEN
while x <= LN / 2 + 1e-9:
    GEN_L.append(x); x += S_GEN
DENSE_R = [LN - p for p in DENSE_L]
GEN_R = [LN - p for p in GEN_L]


def M(s):
    """math()/math_px() 走襯線數學字型，缺中文字會被靜默丟掉——先攔下來。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


# ══════════════════════════════════════════════════════════
# 圖 1　斷面向量重繪：d = h - d'，A_v 是 4 腳
# ══════════════════════════════════════════════════════════
def fig1():
    W, H = 780, 520
    mL, mR, mT, mB = 170, 300, 92, 100
    sx = min((W - mL - mR) / BW, (H - mT - mB) / HH)
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")
    cv.panel(f"圖 1　{TAG} 斷面重繪：矩形耐震梁（柱面處配筋）",
             f"f'c = {FC:g}　f_y = {FY:g}　f_{{yt}} = {FYT:g} kgf/cm^{{2}}"
             f"　　箍筋 D13（A_b = {AB_D13:g} cm^{{2}}）")

    # 混凝土斷面
    cv.polygon([(0, 0), (BW, 0), (BW, HH), (0, HH)],
               C["panel"], C["member"], 2.8)

    # 外圍閉合箍（2 腳）＋ 135 度彎鉤
    hoop = [(CC, CC), (BW - CC, CC), (BW - CC, HH - CC), (CC, HH - CC), (CC, CC)]
    cv.poly(hoop, C["load"], 2.4)
    cv.line((CC, HH - CC), (CC + 4, HH - CC - 4), C["load"], 2.4)
    cv.line((BW - CC, HH - CC), (BW - CC - 4, HH - CC - 4), C["load"], 2.4)

    # 兩支繫筋（各 1 腳）＋ 彎鉤
    for tx in TIE_X:
        cv.line((tx, CC), (tx, HH - CC), C["load"], 2.4)
        cv.line((tx, HH - CC), (tx + 4.5, HH - CC - 4.5), C["load"], 2.4)
        cv.line((tx, CC), (tx - 4.5, CC + 4.5), C["load"], 2.4)

    # 主筋：頂 8-D32（受拉時給 M_pr^-）、底 6-D32
    for i in range(N_TOP):
        cv.dot((X_EDGE + SP_TOP * i, HH - DP), DB_D32 / 2 * sx,
               fill=C["tension"], stroke="#FFFFFF", w=1.4)
    for i in range(N_BOT):
        cv.dot((X_EDGE + SP_BOT * i, DP), DB_D32 / 2 * sx,
               fill=C["compr"], stroke="#FFFFFF", w=1.4)

    # 4 腳編號
    for i, lx in enumerate(LEG_X):
        cv.text((lx, HH / 2), "①②③④"[i], 14, C["accent"],
                weight="700", dx=9)

    # 尺寸線（垂直向下量測時 off 為正 → 落在左側；水平向右量測時 off 為正 → 落在下方）
    cv.dim((0, 0), (BW, 0), M(f"b_w = {BW:g}"), off=44, label_off=16)
    # 垂直尺寸線的標註須偏移超過字寬一半，否則會壓在尺寸線上
    cv.dim((BW, 0), (BW, HH), M(f"h = {HH:g}"), off=36, label_off=32)
    cv.dim((0, HH), (0, HH - DP), M(f"d' = {DP:g}"), off=18, label_off=34)
    cv.dim((0, HH), (0, DP), M(f"d = {D:g}"), off=74, label_off=36)

    # 右側說明槽
    tx0 = cv.X(BW) + 100
    rows = [
        (C["accent"], "700", 14.5, f"d = h - d' = {HH:g} - {DP:g} = {D:g} cm"),
        (C["muted"], "400", 12.5, f"不是 h = {HH:g} cm；頂／底 d' 皆 {DP:g} cm，"),
        (C["muted"], "400", 12.5, f"故兩個搖擺方向的 d 都是 {D:g} cm"),
        (None, None, None, None),
        (C["load"], "700", 14.5, f"A_{{v}} = {N_LEG_D} × {AB_D13:g} = {AV_D:g} cm^{{2}}"),
        (C["muted"], "400", 12.5, f"密箍區 4 腳 = 外箍 {N_LEG_G} 腳 + 繫筋 2 腳"),
        (C["load"], "400", 12.5, f"只算外箍 → {AV_G:g} cm^{{2}}，A_{{v}} 少一半"),
        (None, None, None, None),
        (C["tension"], "700", 13.5, f"頂 {N_TOP}-D32：A_{{s}} = {AS_TOP:g} cm^{{2}}"),
        (C["compr"], "700", 13.5, f"底 {N_BOT}-D32：A_{{s}} = {AS_BOT:g} cm^{{2}}"),
        (C["muted"], "400", 12.5, f"頂筋中心距 {SP_TOP:.2f} cm（單排放得下）"),
        (None, None, None, None),
        (C["muted"], "400", 12.5, f"一般區改用 2 腳：A_{{v}} = {AV_G:g} cm^{{2}}"),
    ]
    y = 128
    for col, wt, sz, txt in rows:
        if txt is None:
            y += 12; continue
        cv.text_px(tx0, y, txt, sz, col, "start", weight=wt)
        y += 22

    cv.text_px(W / 2, H - 16,
               f"紅＝頂層 {N_TOP}-D32（負彎矩受拉）　藍＝底層 {N_BOT}-D32　"
               f"紅框＝D13 閉合箍與繫筋（①～④ 共 {N_LEG_D} 腳）",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2　兩搖擺方向的梁自由體：V_e 的 ± 該取哪一個
# ══════════════════════════════════════════════════════════
PW2, PH2 = 540, 404


def _sway(title, sub, mL_lab, mL_val, mR_lab, mR_val, vL, vR, ccw, ctrl_left,
          sway):
    cv = Canvas(PW2, PH2, sx=1)
    mL = mR = 64
    sx = (PW2 - mL - mR) / (LN / 100)
    cv.sx, cv.ox, cv.oy = sx, mL, 168
    cv.panel(title, sub)
    span, dep = LN / 100, HH / 100          # 以 m 為模型單位

    # 端點彎矩標籤（與弧的旋轉方向同色）
    cv.text_px(18, 84, f"左端 {mL_lab} = {mL_val * TFM:.1f} tf·m",
               13, C["load"], "start", weight="700")
    cv.text_px(PW2 - 18, 84, f"右端 {mR_lab} = {mR_val * TFM:.1f} tf·m",
               13, C["load"], "end", weight="700")

    # 搖擺方向（決定哪一端是 M_pr^-）
    y_sw = (PH2 - 128 - cv.oy) / cv.sx
    cv.text_px(cv.X(span / 2), 104, "框架側向擺動方向", 12.5, C["deform"],
               weight="700")
    cv.arrow((span / 2 - 0.9 * sway, y_sw), (span / 2 + 0.9 * sway, y_sw),
             C["deform"], 3.0, 11)

    # 重力均布載重
    cv.text_px(cv.X(span / 2), 160, f"w_{{u}} = {WU / 10:g} tf/m",
               14, C["load"], weight="700")
    cv.udl((0, dep), (span, dep), 0.52, n=13, w=1.8)

    # 梁
    cv.polygon([(0, 0), (span, 0), (span, dep), (0, dep)],
               C["panel"], C["member"], 2.6)
    cv.text_px(cv.X(span / 2), cv.Y(dep / 2), f"l_{{n}} = {LN / 100:g} m",
               13, C["muted"])

    # 塑鉸端彎矩：兩端同一旋轉方向，合成 (M_pr^- + M_pr^+)/l_n
    cv.moment_arrow((0, dep / 2), r=26, ccw=ccw, color=C["load"], w=2.8,
                    span=100, start=150 if ccw else 250)
    cv.moment_arrow((span, dep / 2), r=26, ccw=ccw, color=C["load"], w=2.8,
                    span=100, start=290 if ccw else 30)

    # 端點剪力（向上為 +）
    for xe, v, xlab in ((0.0, vL, 110.0), (span, vR, PW2 - 110.0)):
        up = v > 0
        y0, y1 = (-0.62, -0.06) if up else (-0.06, -0.62)
        cv.arrow((xe, y0), (xe, y1), C["sfd"], 3.4, 11)
        cv.text_px(xlab, 286, f"V_{{e}} = {abs(v) * TF:.2f} tf", 14,
                   C["sfd"], weight="700")
        is_ctrl = (xe == 0.0) == ctrl_left
        cv.text_px(xlab, 306, "控制斷面" if is_ctrl else "（不控制）", 12.5,
                   C["sfd"] if is_ctrl else C["muted"],
                   weight="700" if is_ctrl else "400")

    cv.text_px(PW2 / 2, 334,
               f"V_{{seis}} = (M_{{pr}}^{{-}} + M_{{pr}}^{{+}}) / l_{{n}} = "
               f"{(MPR_N + MPR_P) * TFM:.1f} / {LN / 100:g} = {V_SEIS * TF:.2f} tf",
               13, C["text"])
    cv.text_px(PW2 / 2, 354,
               f"V_{{grav}} = w_{{u}} l_{{n}} / 2 = {V_GRAV * TF:.2f} tf　→　"
               f"V_{{e}} = {V_SEIS * TF:.2f} ± {V_GRAV * TF:.2f} tf",
               13, C["text"])
    cv.text_px(PW2 / 2, 380,
               f"地震剪力佔比 {V_SEIS * TF:.2f} / {V_E * TF:.2f} = "
               f"{RATIO * 100:.1f} %  ≥ 50 %  →  V_{{c}} = 0",
               13, C["accent"], weight="700")
    return cv


def fig2():
    a = _sway("(a) 搖擺向右", "左端頂筋受拉、右端底筋受拉",
              "M_{pr}^{-}", MPR_N, "M_{pr}^{+}", MPR_P,
              +V_E, -V_E_MIN, True, True, +1)
    b = _sway("(b) 搖擺向左", "左端底筋受拉、右端頂筋受拉",
              "M_{pr}^{+}", MPR_P, "M_{pr}^{-}", MPR_N,
              -V_E_MIN, +V_E, False, False, -1)
    return compose(
        [a, b],
        title="圖 2　兩個搖擺方向的梁自由體：正負號取「重力與地震同向」的那一端",
        sub=f"M_pr 以 1.25f_y = {FY_PR:g}（非 f_y = {FY:g}）與 φ = 1.0 計算；"
            f"用 f_y 會把梁端彎矩低估 {(1 - 1 / OVER) * 100:.0f} %，剪力筋跟著配不足",
        note=f"± 取「重力與地震同向」的那一端：{V_SEIS * TF:.2f} + {V_GRAV * TF:.2f} = "
             f"{V_E * TF:.2f} tf 才是設計值，取 − 得 {V_E_MIN * TF:.2f} tf 不控制",
        cols=2)


# ══════════════════════════════════════════════════════════
# 圖 3　全跨剪力設計包絡線與三條容量門檻（本題最重要的一張）
# ══════════════════════════════════════════════════════════
def fig3():
    W, H = 920, 536
    mL, mR, mT, mB = 92, 232, 100, 124
    span_m = LN / 100
    ytop = max(PHI_VS_D, V_E) * TF * 1.17
    sc_x = (W - mL - mR) / span_m
    sc_y = (H - mT - mB) / ytop
    k = sc_y / sc_x                      # tf → 模型單位（縱軸相對縮放）
    cv = Canvas(W, H, sx=sc_x, ox=mL, oy=mB, bg="#FFFFFF")

    def P(xm, v):                        # (m, tf) → 模型座標
        return (xm, v * k)

    cv.text_px(W / 2, 34, "圖 3　設計剪力包絡線 V_e(x)：跨中並不是重力剪力",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"橫軸：距左柱面距離（m）　縱軸：剪力（tf）　"
               f"包絡線 = max(兩搖擺方向)，全跨最小值仍在 {VE_MID * TF:.2f} tf",
               13, C["muted"])

    # 密箍區帶（自兩端柱面起 2h）
    xh = L_HINGE / 100
    for x0, x1 in ((0.0, xh), (span_m - xh, span_m)):
        cv.polygon([P(x0, 0), P(x1, 0), P(x1, ytop), P(x0, ytop)], C["fill_t"])

    # 兩個搖擺方向（虛線）
    n = 91
    xs = [span_m * i / (n - 1) for i in range(n)]
    right = [(V_E - WU * (x * 100)) * TF for x in xs]
    left = [(V_E_MIN + WU * (x * 100)) * TF for x in xs]
    cv.poly([P(x, v) for x, v in zip(xs, right)], C["member2"], 2.0, dash="7 5")
    cv.poly([P(x, v) for x, v in zip(xs, left)], C["ghost"], 2.4, dash="7 5")

    # 包絡線（實線＋填色）
    env = [Ve(x * 100) * TF for x in xs]
    cv.polygon([P(0, 0)] + [P(x, v) for x, v in zip(xs, env)] + [P(span_m, 0)],
               C["fill_s"], C["sfd"], 2.8)

    # 三條容量門檻
    thresholds = [
        (PHI_VS_D * TF, C["accent"], -11,
         f"φV_{{s}} = {PHI_VS_D * TF:.2f} tf（{N_LEG_D} 腳@{S_DENSE:g}）"),
        (PHI_CAP_G * TF, C["bmd"], +12,
         f"φ(V_{{c}}+V_{{s}}) = {PHI_CAP_G * TF:.2f} tf（{N_LEG_G} 腳@{S_GEN:g}）"),
        (PHI_VC * TF, C["load"], -11,
         f"φV_{{c}} = {PHI_VC * TF:.2f} tf（一般區）"),
    ]
    for val, col, dy, lab in thresholds:
        cv.line(P(0, val), P(span_m, val), col, 1.9, dash="7 5")
        cv.text_px(cv.X(span_m) + 14, cv.Y(val * k) + dy, lab, 11.5, col,
                   "start", weight="700")

    # 關鍵點
    for xm, v, dxp, dyp, anc, lab in (
        (0.0, V_E * TF, 18, -33, "start",
         f"柱面 x = 0：V_{{e}} = {V_E * TF:.2f} tf ← 設計控制值"),
        (xh, VE_OUT * TF, 12, 22, "start",
         f"密箍區外緣 x = {xh:g} m：{VE_OUT * TF:.2f} tf（一般區控制值）"),
        (span_m / 2, VE_MID * TF, 12, 20, "start",
         f"{VE_MID * TF:.2f} tf ← 包絡線最小值，仍是 φV_{{c}} 的 "
         f"{VE_MID / PHI_VC:.2f} 倍"),
    ):
        cv.dot(P(xm, v), 5.6, fill=C["sfd"], stroke="#FFFFFF", w=1.9)
        cv.text_px(cv.X(xm) + dxp, cv.Y(v * k) + dyp, lab, 12.5, C["accent"],
                   anc, weight="700")

    # 座標軸
    cv.arrow(P(0, 0), (span_m * 1.03, 0), C["muted"], 1.6, 9)
    cv.arrow(P(0, 0), P(0, ytop), C["muted"], 1.6, 9)
    cv.text_px(cv.X(0) - 14, cv.Y(ytop * k) + 8, "V_{e} (tf)", 12.5,
               C["muted"], "end")
    cv.text_px(cv.X(span_m) + 14, cv.Y(0) + 18, "x (m)", 12.5, C["muted"], "start")
    for v in range(0, int(ytop) + 1, 10):
        cv.line(P(0, v), (-0.06, v * k), C["muted"], 1.3)
        cv.text_px(cv.X(0) - 12, cv.Y(v * k), f"{v}", 12, C["muted"], "end")
    for xv in (0.0, xh, 3.0, span_m / 2, 6.0, span_m - xh, span_m):
        hot = abs(xv - xh) < 1e-9 or abs(xv - (span_m - xh)) < 1e-9
        cv.line(P(xv, 0), P(xv, -ytop * 0.02), C["muted"], 1.3)
        cv.text_px(cv.X(xv), 430, f"{xv:g}", 12,
                   C["accent"] if hot else C["muted"],
                   weight="700" if hot else "400")
    cv.line(P(span_m / 2, 0), P(span_m / 2, VE_MID * TF), C["muted"], 1.2,
            dash="4 4")

    # 圖例（畫在最後，蓋掉底下的輔助線）
    cv.rect_px(300, 300, 300, 92, C["panel"], 12, C["border"], 1.2)
    cv.legend(314, 322, [
        (C["sfd"], "設計包絡線 V_{e}(x)＝兩方向取大"),
        (C["member2"], f"搖擺向右：{V_E * TF:.2f} - {WU / 10:g}x"),
        (C["ghost"], f"搖擺向左：{V_E_MIN * TF:.2f} + {WU / 10:g}x"),
    ], size=12, gap=22)

    # 密箍區帶標註
    cv.text_px(cv.X(xh / 2), 456, f"密箍區 2h = {L_HINGE:g} cm", 12.5,
               C["load"], weight="700")
    cv.text_px(cv.X(span_m - xh / 2), 456, "密箍區", 12.5, C["load"], weight="700")

    cv.text_px(W / 2, 484,
               f"跨中 V_{{e}} = {VE_MID * TF:.2f} tf 是 φV_{{c}} = {PHI_VC * TF:.2f} tf 的 "
               f"{VE_MID / PHI_VC:.2f} 倍　→　全梁都必須配剪力筋"
               f"（誤用重力剪力 {V_GRAV * TF:.0f} tf 而取 s = 30 cm 者，此處即不足）",
               13, C["text"])
    cv.text_px(W / 2, 508,
               f"一般區配置 φ(V_{{c}}+V_{{s}}) = {PHI_CAP_G * TF:.2f} tf 在 "
               f"x = {X_CAP_G / 100:.2f} m 起即不足　→　柱面起 {L_HINGE:g} cm "
               f"須改 {N_LEG_D} 腳 D13@{S_DENSE:g}（且 V_{{c}} 不得計入）",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 4　箍筋配置立面：2h（不是 2d）、第一支 ≤ 5 cm
# ══════════════════════════════════════════════════════════
def fig4():
    W, H = 980, 540
    mL, mR, mT, mB = 90, 90, 180, 220
    sx = min((W - mL - mR) / LN, (H - mT - mB) / HH)
    cv = Canvas(W, H, sx=sx, ox=mL, oy=mB, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "圖 4　靠柱端剪力筋配置立面（間距與根數由設計值現算）",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"密箍區：自柱面起 2h = {L_HINGE:g} cm，{N_LEG_D} 腳 D13 閉合箍 @"
               f"{S_DENSE:g} cm　｜　一般區：{N_LEG_G} 腳 D13 @{S_GEN:g} cm",
               13, C["muted"])

    # 兩端柱
    cw = LN * 0.075
    for cx0, cx1 in ((-cw, 0.0), (LN, LN + cw)):
        cv.polygon([(cx0, -HH * 0.3), (cx1, -HH * 0.3),
                    (cx1, HH * 1.3), (cx0, HH * 1.3)],
                   C["border"], C["member2"], 2.0)
        cv.text_px(cv.X((cx0 + cx1) / 2), cv.Y(HH / 2), "柱", 15, C["muted"],
                   weight="700")

    # 密箍區底色 + 梁
    for x0, x1 in ((0.0, L_HINGE), (LN - L_HINGE, LN)):
        cv.polygon([(x0, 0), (x1, 0), (x1, HH), (x0, HH)], C["fill_t"])
    cv.polygon([(0, 0), (LN, 0), (LN, HH), (0, HH)], "none", C["member"], 2.8)
    for xf in (0.0, LN):                       # 柱面
        cv.line((xf, -HH * 0.16), (xf, HH * 1.16), C["member"], 2.6)

    # 箍筋（位置全部現算）
    for pos, col, lw in ((DENSE_L + DENSE_R, C["load"], 2.3),
                         (GEN_L + GEN_R, C["deform"], 1.9)):
        for p in pos:
            cv.line((p, CC), (p, HH - CC), col, lw, cap="butt")

    # 縱向筋示意
    for yb in (DP, HH - DP):
        cv.line((0, yb), (LN, yb), C["member2"], 1.4, dash="9 6")

    # 上方：l_n 與兩端 2h
    cv.dim((0, HH), (LN, HH), M(f"l_n = {LN:g} cm"), off=-120, label_off=-15)
    cv.dim((0, HH), (L_HINGE, HH), M(f"2h = {L_HINGE:g} cm"), off=-40, label_off=-15)
    cv.dim((LN - L_HINGE, HH), (LN, HH), M(f"2h = {L_HINGE:g} cm"),
           off=-40, label_off=-15)

    # 第一支箍 ≤ 5 cm
    cv.arrow((S_FIRST, HH * 1.9), (S_FIRST, HH * 1.06), C["accent"], 2.8, 10)
    cv.text_px(cv.X(S_FIRST) + 8, 170, f"第一支 ≤ {S_FIRST:g} cm", 12.5,
               C["accent"], "start", weight="700")

    # 下方：2d 的錯誤長度對照
    cv.dim((0, 0), (2 * D, 0), M(f"2d = {2 * D:g} cm"), off=38, label_off=15)
    cv.text_px(cv.X(2 * D) + 12, cv.Y(0) + 38,
               f"用 2d = {2 * D:g} cm 是錯的（短了 {L_HINGE - 2 * D:g} cm）",
               12.5, C["load"], "start", weight="700")

    # 分區標註
    cv.text_px(cv.X(L_HINGE / 2), 400,
               f"{N_LEG_D} 腳 D13@{S_DENSE:g}（{len(DENSE_L)} 支）", 12.5,
               C["load"], weight="700")
    cv.text_px(cv.X(LN - L_HINGE / 2), 400,
               f"{N_LEG_D} 腳 D13@{S_DENSE:g}（{len(DENSE_L)} 支）", 12.5,
               C["load"], weight="700")
    cv.text_px(cv.X(LN / 2), 400,
               f"{N_LEG_G} 腳 D13@{S_GEN:g}　（s ≤ d/2 = {D / 2:g} cm ✓）", 12.5,
               C["deform"], weight="700")

    cv.text_px(W / 2, 448,
               f"密箍區長度以「全高 h」計：2h = {L_HINGE:g} cm；"
               f"密箍區間距 s_o = min(d/4 = {D / 4:.2f}, 6d_b = {6 * DB_D32:.2f}, 15) = "
               f"{S_O:g} cm，與強度需求 {S_REQ:.2f} cm 取小 → 採 {S_DENSE:g} cm",
               13, C["text"])
    cv.text_px(W / 2, 472,
               f"耐震「梁」第一支箍距柱面 ≤ {S_FIRST:g} cm（§18.6.4.4）；"
               f"s_o/2 = {S_O / 2:g} cm 是「柱」的規定（§18.7.5.3），不可混用",
               13, C["accent"], weight="700")
    cv.text_px(W / 2, 500,
               f"一般區需求 V_s = {VS_GEN * TF:.2f} tf → s ≤ {S_GEN_REQ:.2f} cm，"
               f"採 {S_GEN:g} cm 貫通至跨中；紅＝{N_LEG_D} 腳（V_c = 0）　"
               f"藍＝{N_LEG_G} 腳（可計入 V_c）",
               12.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section", fig1,
     f"d 誤用 h = {HH:g} 而非 h - d' = {D:g}；A_v 只算外箍 2 腳 "
     f"{AV_G:g} 而非 4 腳 {AV_D:g} cm^2"),
    ("2-sway", fig2,
     "V_e 的 ± 取錯方向（重力與地震同向者才控制）；M_pr 用 f_y 而非 1.25f_y"),
    ("3-envelope", fig3,
     "把跨中當成「重力剪力 9 tf」而取 s = 30 cm；忘記 V_e 沿全梁都存在"),
    ("4-detailing", fig4,
     "密箍區長度寫 2d = 134 而非 2h = 152；第一支箍寫 s_o/2 = 7.5 而非梁的 5 cm"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("d cm",              D,                  67.0,    0.001),
        ("A_s,top cm2",       AS_TOP,             65.12,   0.001),
        ("A_s,bot cm2",       AS_BOT,             48.84,   0.001),
        ("1.25f_y",           FY_PR,              5250.0,  0.001),
        ("a_top cm",          A_TOP,              23.94,   0.01),
        ("M_pr^- tf·m",       MPR_N * TFM,        188.1,   0.05),
        ("a_bot cm",          A_BOT,              17.96,   0.01),
        ("M_pr^+ tf·m",       MPR_P * TFM,        148.8,   0.05),
        ("V_seis tf",         V_SEIS * TF,        37.43,   0.01),
        ("V_grav tf",         V_GRAV * TF,        9.00,    0.001),
        ("V_e tf",            V_E * TF,           46.43,   0.01),
        ("V_e(另一端) tf",     V_E_MIN * TF,       28.43,   0.01),
        ("地震剪力佔比",        RATIO,              0.806,   0.001),
        ("V_s,req tf",        VS_REQ * TF,        61.91,   0.01),
        ("A_v 4腳 cm2",        AV_D,               5.08,    0.001),
        ("s_req cm",          S_REQ,              15.39,   0.01),
        ("s_o cm",            S_O,                15.0,    0.001),
        ("2h cm",             L_HINGE,            152.0,   0.001),
        ("V_s,max tf",        VS_MAX * TF,        142.6,   0.05),
        ("A_v,min/s cm2/cm",  AVMIN_S,            0.0750,  0.0001),
        ("φV_s @15 tf",       PHI_VS_D * TF,      47.65,   0.01),
        ("V_c tf",            VC * TF,            35.65,   0.01),
        ("φV_c tf",           PHI_VC * TF,        26.74,   0.01),
        ("V_e(1.52 m) tf",    VE_OUT * TF,        43.39,   0.01),
        ("V_e(4.5 m) tf",     VE_MID * TF,        37.43,   0.01),
        ("V_s,一般區 tf",      VS_GEN * TF,        22.21,   0.01),
        ("s_一般區 cm",        S_GEN_REQ,          21.46,   0.01),
        ("φ(V_c+V_s)@20 tf",  PHI_CAP_G * TF,     44.61,   0.01),
        ("主筋中心距 cm",       SP_TOP,             6.61,    0.01),
    ]
    print(f"── 與 {TAG}.md §4 / §Step 8 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<18} 算得 {got:>12.6g}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    # 幾何自洽檢核
    assert PHI_VS_D >= V_E, "密箍區 φV_s 不足"
    assert PHI_CAP_G >= VE_OUT, "一般區 φ(V_c+V_s) 不足"
    assert S_DENSE <= min(S_REQ, S_O) and S_GEN <= min(S_GEN_REQ, D / 2)
    assert DENSE_L[0] == S_FIRST and DENSE_L[-1] <= L_HINGE < DENSE_L[-1] + S_DENSE
    print(f"  OK  密箍區箍筋 {len(DENSE_L)} 支（{DENSE_L[0]:g}～{DENSE_L[-1]:g} cm）"
          f"　一般區半跨 {len(GEN_L)} 支（{GEN_L[0]:g}～{GEN_L[-1]:g} cm）")

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<32} 攔：{catches}")


if __name__ == "__main__":
    main()
