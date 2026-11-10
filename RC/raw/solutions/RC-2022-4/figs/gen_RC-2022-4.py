#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2022-4　依公路橋梁耐震評估規範求三種韌性需求 — 解題圖解產生腳本

三條鐵則：
  1. 常數區只放 RC-2022-4.md §1 給定的原始資料（表 3 兩組軸力下的塑鉸參數、
     l_u、d_b、f_y、P = 270、M = 232.5）。α、φ_y、M_y、φ_u、M_u、L、L_p、
     δ_y、θ_y、δ_u、θ_u、μ_φ、μ_θ、μ、φ_d、δ_d、λ、μ_approx 全部現算，
     檔尾對 §4／§5 公佈值 assert。
  2. 改 §1 任一數字重跑，三張圖跟著變（含表格、內插點位置、變形曲線比例）。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  "/mnt/skills/user/struct-diagram/scripts"))
from structdraw import Canvas, C, compose, esc
from recipes import bar_compare

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2022-4"

# ══════════════════════════════════════════════════════════
# §1 原始給定（唯一可手寫的數字）
# ══════════════════════════════════════════════════════════
LU = 6.4                     # m　柱淨高
DB = 3.22 / 100.0            # m　D32 主筋直徑（3.22 cm）
FY = 4200.0                  # kgf/cm^2
P_APP = 270.0                # tf　施加軸壓力
M_APP = 232.5                # tf\u00b7m　施加彎矩

# 表 3：兩組軸力下的雙線性塑鉸參數（φ: rad/m，M: tf\u00b7m）
P_LO, P_HI = 180.0, 360.0
LO = {"phi_y": 0.004, "M_y": 200.0, "phi_u": 0.030, "M_u": 230.0}
HI = {"phi_y": 0.006, "M_y": 240.0, "phi_u": 0.010, "M_u": 260.0}

# ══════════════════════════════════════════════════════════
# 現算（§4）
# ══════════════════════════════════════════════════════════
L = LU / 2.0                                        # 反曲點在淨高中點 → 懸臂長
ALPHA = (P_APP - P_LO) / (P_HI - P_LO)              # 線性內插係數


def itp(key):
    """表 3 線性內插；φ_u 之差為負，方向由資料自己決定，不得手動改號。"""
    return LO[key] + ALPHA * (HI[key] - LO[key])


PHI_Y, M_Y, PHI_U, M_U = itp("phi_y"), itp("M_y"), itp("phi_u"), itp("M_u")

LP_EQ1 = 0.08 * L + 0.0022 * DB * FY                # 第一式
LP_LOWER = 0.0044 * DB * FY                         # 下限式
LP = max(LP_EQ1, LP_LOWER)
LP_CTRL = "下限式" if LP_LOWER > LP_EQ1 else "第一式"

DELTA_Y = PHI_Y * L ** 2 / 3.0
THETA_Y = DELTA_Y / L
HARDEN = M_U / M_Y                                  # 應變硬化比 M_u/M_y
ARM = L - 0.5 * LP                                  # 塑鉸轉角對頂點的力臂
THETA_P = (PHI_U - PHI_Y) * LP                      # 塑鉸轉角
DELTA_U = HARDEN * DELTA_Y + THETA_P * ARM
THETA_U = DELTA_U / L
DELTA_U_NOHARD = DELTA_Y + THETA_P * ARM            # 拿掉硬化項

MU_PHI = PHI_U / PHI_Y                              # 讀法A：斷面層次
MU_THETA = THETA_U / THETA_Y                        # 讀法A：構件層次
MU = DELTA_U / DELTA_Y                              # 讀法A：整體層次

# 讀法B：以實際承受的 M = 232.5 評估（§5 爭議點 2）
PHI_D = PHI_Y + (M_APP - M_Y) / (M_U - M_Y) * (PHI_U - PHI_Y)
MU_PHI_B = PHI_D / PHI_Y
DELTA_D = (M_APP / M_Y) * DELTA_Y + (PHI_D - PHI_Y) * LP * ARM
MU_B = DELTA_D / DELTA_Y
CAP_DEM = MU / MU_B                                 # 容量／需求

# 近似式（§5 進階）
LAM = 3.0 * (LP / L) * (1.0 - 0.5 * LP / L)
MU_APPROX = 1.0 + (MU_PHI - 1.0) * LAM

M_MID = (M_Y + M_U) / 2.0                           # 用來證明 232.5 是正中點
CM = 100.0                                          # m → cm


def M(s):
    """FONT_M（Latin Modern Math）缺中日韓字，cairosvg 會靜默丟字。
    所有進 math()/math_px()/dim() 的字串一律經此守衛。"""
    assert not any(ord(ch) > 0x2E80 for ch in s), f"math 字串不得含中日韓字元：{s}"
    return s


def tr(a, b):
    """趨勢箭頭由資料算出，不手打。"""
    return "↑" if b > a else ("↓" if b < a else "→")


# ══════════════════════════════════════════════════════════
# 圖 1　彎矩–曲率雙線性曲線與線性內插
# ══════════════════════════════════════════════════════════
def fig1():
    W, H = 1020, 690
    mL, mR, mT, mB = 96, 176, 104, 142
    phi_max = max(LO["phi_u"], HI["phi_u"], PHI_U) * 1.1167     # 0.0335
    m_max = max(LO["M_u"], HI["M_u"], M_U) * 1.0846             # 282
    sc_x = (W - mL - mR) / phi_max
    sc_y = (H - mT - mB) / m_max
    K = sc_y / sc_x                       # 縱軸相對縮放（tf\u00b7m → 模型單位）
    cv = Canvas(W, H, sx=sc_x, ox=mL, oy=mB, bg="#FFFFFF")

    def Ym(m):
        return cv.Y(m * K)

    cv.text_px(W / 2, 32,
               "圖 1　彎矩–曲率雙線性曲線：兩組軸力的塑鉸性質與 P = 270 tf 的線性內插",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 56,
               f"α = {ALPHA:.1f}；φ_{{y}}、M_{{y}}、M_{{u}} 隨軸壓遞增，"
               f"唯 φ_{{u}} 遞減 —— 內插方向弄反是本題最大失分點",
               13, C["muted"])

    # ── 座標軸 ──
    cv.arrow((0, 0), (phi_max, 0), C["muted"], 1.6, 9)
    cv.arrow((0, 0), (0, m_max * K), C["muted"], 1.6, 9)
    cv.math_px(cv.X(phi_max) + 8, cv.Y(0), M("φ"), 15, C["muted"], "start")
    cv.text_px(cv.X(phi_max) + 22, cv.Y(0), "(rad/m)", 12.5, C["muted"], "start")
    cv.text_px(mL + 6, mT - 18, "M (tf\u00b7m)", 12.5, C["muted"], "start")

    for i in range(7):
        xv = 0.005 * i
        cv.line((xv, 0), (xv, -m_max * K * 0.016), C["muted"], 1.4)
        cv.text_px(cv.X(xv), cv.Y(0) + 20, f"{xv:.3f}", 12, C["muted"])
    for mv in (50, 100, 150, 200, 250):
        cv.line((0, mv * K), (-phi_max * 0.008, mv * K), C["muted"], 1.4)
        cv.text_px(cv.X(0) - 12, Ym(mv), f"{mv:g}", 12, C["muted"], "end")

    # ── 三條雙線性折線（原點 → 降伏 → 極限）──
    curves = [
        (LO, C["ghost"], 3.4, f"P = {P_LO:.0f} tf"),
        (HI, C["member2"], 3.4, f"P = {P_HI:.0f} tf"),
        ({"phi_y": PHI_Y, "M_y": M_Y, "phi_u": PHI_U, "M_u": M_U},
         C["deform"], 5.2, f"P = {P_APP:.0f} tf"),
    ]
    for d, col, lw, _ in curves:
        cv.poly([(0, 0), (d["phi_y"], d["M_y"] * K), (d["phi_u"], d["M_u"] * K)],
                col, lw)
    for d, col, _, _ in curves:
        cv.dot((d["phi_y"], d["M_y"] * K), 5.2, fill=col, stroke="#FFFFFF", w=1.6)
        cv.dot((d["phi_u"], d["M_u"] * K), 5.8, fill=col, stroke="#FFFFFF", w=1.8)

    # 曲線名稱與極限點座標
    cv.text_px(cv.X(LO["phi_u"]) + 12, Ym(LO["M_u"]) - 2, f"P = {P_LO:.0f} tf",
               13, C["muted"], "start", weight="700")
    cv.text_px(cv.X(LO["phi_u"]) + 12, Ym(LO["M_u"]) + 20,
               f"({LO['phi_u']:.3f}, {LO['M_u']:.0f})", 12.5, C["muted"], "start")
    cv.text_px(cv.X(HI["phi_u"]) - 26, Ym(HI["M_u"]) - 27, f"P = {P_HI:.0f} tf",
               13, C["member2"], "end", weight="700")
    cv.text_px(cv.X(HI["phi_u"]) - 26, Ym(HI["M_u"]) - 6,
               f"({HI['phi_u']:.3f}, {HI['M_u']:.0f})", 12.5, C["member2"], "end")
    cv.text_px(cv.X(PHI_U) + 58, Ym(M_U) - 40,
               f"P = {P_APP:.0f} tf（內插，α = {ALPHA:.1f}）", 13.5, C["deform"],
               weight="700")
    cv.text_px(cv.X(PHI_U) + 58, Ym(M_U) - 18,
               f"極限點 ({PHI_U:.3f}, {M_U:.0f})", 13, C["deform"], weight="700")

    # 內插曲線的降伏點：拉出引線標到左下空白區
    cv.line((PHI_Y, M_Y * K), (PHI_Y + 0.0007, 126 * K), C["deform"], 1.3,
            dash="4 3")
    cv.text_px(cv.X(PHI_Y + 0.0010), Ym(120),
               f"降伏點 ({PHI_Y:.3f}, {M_Y:.0f})", 13, C["deform"], "start",
               weight="700")

    # ── M = 232.5 的水平虛線與內插曲線上的位置 ──
    cv.line((0, M_APP * K), (PHI_D, M_APP * K), C["load"], 2.0, dash="7 5")
    cv.line((PHI_D, M_APP * K), (PHI_D, 0), C["load"], 1.6, dash="5 4")
    cv.dot((PHI_D, M_APP * K), 6.2, fill=C["load"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(0) + 8, Ym(M_APP) - 13, f"M = {M_APP:g} tf\u00b7m", 13, C["load"],
               "start", weight="700")
    cv.math_px(cv.X(PHI_D) + 10, Ym(M_APP) + 22, M("φ_{d}"), 15, C["load"],
               "start", weight="700")
    cv.line((PHI_D, 0), (PHI_D, -m_max * K * 0.016), C["load"], 2.0)
    cv.text_px(cv.X(PHI_D), cv.Y(0) + 20, f"{PHI_D:.4f}", 12, C["load"],
               weight="700")

    # ── φ_u 遞減的證據：三條落線 + 由 180 指向 360 的箭頭 ──
    m_tr = m_max * 0.585                      # 落線的水平參考高度
    m_lo = m_tr + 8 / sc_y                    # 落線讓開文字帶的下緣
    m_hi = m_tr + 52 / sc_y                   # 落線讓開文字帶的上緣
    for d, col in ((LO, C["ghost"]), (HI, C["member2"]),
                   ({"phi_u": PHI_U, "M_u": M_U}, C["deform"])):
        cv.line((d["phi_u"], d["M_u"] * K), (d["phi_u"], m_hi * K), col, 1.4,
                dash="5 4")
        cv.line((d["phi_u"], m_lo * K), (d["phi_u"], m_tr * K), col, 1.4,
                dash="5 4")
    cv.arrow((LO["phi_u"], m_tr * K), (HI["phi_u"], m_tr * K), C["accent"], 2.6, 11)
    cv.dot((PHI_U, m_tr * K), 5.2, fill=C["accent"], stroke="#FFFFFF", w=1.6)
    xmid = (cv.X(LO["phi_u"]) + cv.X(HI["phi_u"])) / 2
    cv.text_px(xmid, Ym(m_tr) - 40, f"軸壓 P 由 {P_LO:.0f} → {P_HI:.0f} tf",
               13, C["accent"], weight="700")
    cv.text_px(xmid, Ym(m_tr) - 19,
               f"φ_{{u}} 由 {LO['phi_u']:.3f} 遞減至 {HI['phi_u']:.3f}"
               f"（唯一遞減的參數）", 13, C["accent"], weight="700")
    cv.text_px(cv.X(PHI_U), Ym(m_tr) + 20,
               f"內插 α = {ALPHA:.1f} → φ_{{u}} = {PHI_U:.3f}", 12.5, C["accent"])

    # ── 內插對照表（兼作圖例）──
    bx, by, bw, bh = 450, 350, 390, 152
    cv.text_px(bx + bw / 2, by - 14,
               "表 3 內插對照（φ 單位 rad/m，M 單位 tf\u00b7m）", 12.5, C["muted"])
    cv.rect_px(bx, by, bw, bh, C["panel"], 12, C["border"], 1.3)
    cols = [bx + 180, bx + 240, bx + 300, bx + 360]
    heads = [("φ_{y}", C["muted"]), ("M_{y}", C["muted"]),
             ("φ_{u}", C["accent"]), ("M_{u}", C["muted"])]
    for cx, (hd, hc) in zip(cols, heads):
        cv.text_px(cx, by + 22, hd, 14, hc, weight="700")
    rows = [(f"P = {P_LO:.0f} tf", C["ghost"], LO, "400"),
            (f"P = {P_HI:.0f} tf", C["member2"], HI, "400"),
            (f"P = {P_APP:.0f} tf 內插",
             C["deform"],
             {"phi_y": PHI_Y, "M_y": M_Y, "phi_u": PHI_U, "M_u": M_U}, "700")]
    for i, (nm, col, d, wt) in enumerate(rows):
        y = by + 50 + i * 26
        if i == 2:
            cv.rect_px(bx + 4, y - 13, bw - 8, 26, C["fill_c"], 6)
        cv.parts.append(f'<line x1="{bx+12}" y1="{y}" x2="{bx+36}" y2="{y}" '
                        f'stroke="{col}" stroke-width="4" stroke-linecap="round"/>')
        cv.text_px(bx + 44, y, nm, 12.5, C["text"], "start", weight=wt)
        for cx, v in zip(cols, (d["phi_y"], d["M_y"], d["phi_u"], d["M_u"])):
            s = f"{v:.3f}" if v < 1 else f"{v:.0f}"
            cv.text_px(cx, y, s, 13, col if i < 2 else C["deform"], weight=wt)
    ytr = by + 50 + 3 * 26 + 4
    cv.text_px(bx + 44, ytr, "隨軸壓的趨勢", 12.5, C["muted"], "start")
    for cx, key in zip(cols, ("phi_y", "M_y", "phi_u", "M_u")):
        a = tr(LO[key], HI[key])
        cv.text_px(cx, ytr, a, 16,
                   C["accent"] if a == "↓" else C["muted"], weight="700")
    cv.text_px(bx + bw / 2, by + bh + 20,
               f"α = ({P_APP:.0f} - {P_LO:.0f})/({P_HI:.0f} - {P_LO:.0f}) "
               f"= {ALPHA:.1f}", 12.5, C["muted"])

    # ── 頁尾：232.5 的角色 ──
    cv.text_px(W / 2, H - 68,
               f"M = {M_APP:g} tf\u00b7m = ({M_Y:.0f} + {M_U:.0f})/2，"
               f"恰為內插後 M_{{y}} 與 M_{{u}} 的正中點 → 這個數字是要被「用」的"
               f"（讀法B），不只是確認已降伏",
               13, C["muted"])
    cv.text_px(W / 2, H - 42,
               f"φ_{{d}} = φ_{{y}} + ({M_APP:g} - {M_Y:.0f})/({M_U:.0f} - {M_Y:.0f})"
               f"×(φ_{{u}} - φ_{{y}}) = {PHI_Y:.3f} + "
               f"{(M_APP-M_Y)/(M_U-M_Y):.3f}×{PHI_U-PHI_Y:.3f} = {PHI_D:.4f} rad/m",
               13, C["load"], weight="700")
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2　反曲點、懸臂長度、塑鉸與變形
# ══════════════════════════════════════════════════════════
PW2, PH2 = 560, 620
PLOT_H2 = 370             # 兩格共用的繪圖高度（px）
OY2 = 130
AMP = 25.0                # 變形放大倍率（純視覺；比例仍為真）
D_FULL = 1.2              # 左格全柱側移示意量（m，示意）


def _u_full(xi):
    """兩端不轉動、相對側移 D_FULL 的雙曲率位移；反曲點在 xi = 0.5。"""
    return D_FULL * (3 * xi ** 2 - 2 * xi ** 3)


def fig2_left():
    cv = Canvas(PW2, PH2, sx=PLOT_H2 / LU, ox=230, oy=OY2)
    cv.panel("反曲點把雙曲率柱拆成兩根懸臂柱",
             "柱兩端受彎、中點彎矩為零")

    # 原位置與帽梁
    cv.line((0, 0), (0, LU), C["ghost"], 3.0, dash="7 5")
    cv.line((-0.35, LU), (0.35, LU), C["ghost"], 3.0, dash="6 5", cap="butt")
    # 雙曲率變形（theta_top = theta_bot = 0 → S 形，反曲點在中點）
    cv.poly([(_u_full(i / 120), LU * i / 120) for i in range(121)],
            C["deform"], 5.4)
    # 柱頂帽梁：隨柱頂平移但不轉動
    ut = _u_full(1.0)
    cv.line((ut - 0.35, LU), (ut + 0.35, LU), C["member"], 6.0, cap="butt")
    cv.fixed_support((0, 0), size=20)

    # 反曲點：位置由形狀函數算出，不目測
    u_inf = _u_full(0.5)
    cv.line((-0.50, L), (1.28, L), C["accent"], 1.6, dash="6 4")
    cv.dot((u_inf, L), 6.0, fill="#FFFFFF", stroke=C["accent"], w=2.9)
    cv.text_px(cv.X(1.32), cv.Y(L) - 22, "反曲點 M = 0", 12.5, C["accent"], "start",
               weight="700")

    # 側向力
    cv.arrow((ut + 0.55, LU), (ut + 1.10, LU), C["load"], 3.2, 11)
    cv.text_px(cv.X(ut + 1.16), cv.Y(LU), "V", 15, C["load"], "start",
               weight="700", italic=True)

    # 尺寸線
    cv.dim((-0.55, 0), (-0.55, LU), M(f"l_{{u}} = {LU:g} m"), off=-38, label_off=-62)
    cv.dim((1.00, 0), (1.00, L), M(f"L = lu/2 = {L:g} m"), off=30, label_off=76)

    for i, (t, col) in enumerate([
            ("① 兩端受彎 → M 沿柱高變號", C["text"]),
            ("② 反曲點（M = 0）在中點", C["accent"]),
            (f"③ 每半段為 L = {L:g} m 懸臂", C["deform"]),
            (f"⚠ L ≠ l_{{u}} = {LU:g} m 全柱高", C["load"])]):
        cv.text_px(348, 152 + i * 25, t, 12.5, col, "start",
                   weight="700" if i == 3 else "400")

    cv.text_px(PW2 / 2, 540,
               "柱頂可平移、不可轉動 → 彎矩在柱高中點變號", 12.5, C["muted"])
    cv.text_px(PW2 / 2, 566,
               f"L = lu/2 = {LU:g}/2 = {L:g} m（⚠ 不是全柱淨高 {LU:g} m）",
               13, C["load"], weight="700")
    cv.text_px(PW2 / 2, 592, "側移量為示意放大，不影響反曲點位置", 12.5, C["muted"])
    return cv


def _elastic(xi):
    """懸臂柱受頂端集中力之彈性撓曲形狀（無因次，頂端 = 1）。"""
    return (3 * xi ** 2 - xi ** 3) / 2.0


def fig2_right():
    cv = Canvas(PW2, PH2, sx=PLOT_H2 / L, ox=170, oy=OY2)
    cv.panel("懸臂柱的降伏與極限變形",
             "塑鉸長度 L_{p} 集中於柱底，力臂為 L - 0.5L_{p}")

    dy_d = AMP * DELTA_Y
    du_el = AMP * HARDEN * DELTA_Y            # 極限狀態的等效彈性段
    tp_d = AMP * THETA_P                      # 放大後的塑鉸轉角

    cv.line((0, 0), (0, L), C["ghost"], 3.0, dash="7 5")

    # 塑鉸區（填色帶）
    cv.polygon([(-0.13, 0), (0.13, 0), (0.13, LP), (-0.13, LP)],
               C["fill_t"], C["load"], 1.8)

    # 降伏變形（彈性三次曲線）
    cv.poly([(dy_d * _elastic(i / 100), L * i / 100) for i in range(101)],
            C["deform"], 4.4)

    # 極限變形＝硬化後彈性段 ＋ 塑鉸轉角繞塑鉸中心的剛體轉動
    def u_ult(y):
        return du_el * _elastic(y / L) + tp_d * max(0.0, y - 0.5 * LP)

    cv.poly([(u_ult(L * i / 100), L * i / 100) for i in range(101)],
            C["load"], 4.6)

    cv.fixed_support((0, 0), size=20)
    cv.dot((dy_d, L), 5.4, fill=C["deform"], stroke="#FFFFFF", w=1.8)
    cv.dot((u_ult(L), L), 6.0, fill=C["load"], stroke="#FFFFFF", w=2.0)
    cv.math_px(cv.X(dy_d), cv.Y(L) - 20, M("δ_{y}"), 14.5, C["deform"],
               weight="700")
    cv.math_px(cv.X(u_ult(L)), cv.Y(L) - 20, M("δ_{u}"), 14.5, C["load"],
               weight="700")

    # 塑鉸中心與力臂
    cv.line((-0.16, 0.5 * LP), (0.15, 0.5 * LP), C["muted"], 1.5, dash="5 4")
    cv.dot((0, 0.5 * LP), 5.0, fill=C["accent"], stroke="#FFFFFF", w=1.6)
    cv.math_px(cv.X(0.16), cv.Y(0.5 * LP) - 26, M("0.5L_{p}"), 12.5, C["accent"],
               "start", weight="700")
    cv.dim((1.00, 0), (1.00, LP), M(f"L_{{p}} = {LP:.3f} m"), off=18, label_off=-52)
    cv.dim((1.45, 0.5 * LP), (1.45, L),
           M(f"L - 0.5L_{{p}} = {ARM:.4f} m"), off=16, label_off=80)
    cv.dim((-0.10, 0), (-0.10, L), M(f"L = {L:g} m"), off=-30, label_off=-58)

    blk = 372
    cv.text_px(blk, 100, f"δ_{{y}} = {DELTA_Y*CM:.3f} cm", 13.5, C["deform"],
               "start", weight="700")
    cv.text_px(blk, 122, f"δ_{{u}} = {DELTA_U*CM:.3f} cm", 13.5, C["load"],
               "start", weight="700")
    cv.text_px(blk, 146, f"μ = δ_{{u}}/δ_{{y}} = {MU:.2f}", 13.5, C["accent"],
               "start", weight="700")
    cv.text_px(blk, 184, "δ_{u} 的兩項：", 12, C["muted"], "start")
    cv.text_px(blk, 206,
               f"(M_{{u}}/M_{{y}})δ_{{y}} = {HARDEN*DELTA_Y*CM:.3f} cm",
               12, C["muted"], "start")
    cv.text_px(blk, 228,
               f"θ_{{p}}(L - 0.5L_{{p}}) = {THETA_P*ARM*CM:.3f} cm",
               12, C["muted"], "start")

    cv.text_px(PW2 / 2, 540,
               f"θ_{{p}} = (φ_{{u}} - φ_{{y}})L_{{p}} = {PHI_U-PHI_Y:.3f} × "
               f"{LP:.3f} = {THETA_P:.6f} rad", 12.5, C["muted"])
    cv.text_px(PW2 / 2, 566,
               f"L_{{p}} = max({LP_EQ1:.4f}, {LP_LOWER:.4f}) = {LP:.4f} m　"
               f"← {LP_CTRL} 0.0044d_{{b}}f_{{y}} 控制", 13, C["load"], weight="700")
    cv.text_px(PW2 / 2, 592,
               f"變形放大 {AMP:g} 倍；δ_{{u}}/δ_{{y}} = {MU:.3f} 為真實比例",
               12.5, C["muted"])
    return cv


def fig2():
    return compose(
        [fig2_left(), fig2_right()],
        title="圖 2　反曲點把雙曲率柱拆成兩根懸臂柱：懸臂長度、塑鉸長度與降伏／極限變形",
        sub=f"L = lu/2 = {L:g} m（不是全柱淨高 {LU:g} m）；"
            f"塑鉸長度由{LP_CTRL}控制 = {LP:.3f} m",
        note=f"極限位移第二項的力臂是 L - 0.5Lp = {ARM:.4f} m —— 不是 L，也不是 Lp",
        cols=2)


# ══════════════════════════════════════════════════════════
# 圖 3　三層韌性與兩種讀法
# ══════════════════════════════════════════════════════════
def fig3():
    KIND = ("sec", "mem", "mem", "sec", "mem")
    VALS = (MU_PHI, MU, MU_APPROX, MU_PHI_B, MU_B)
    COLS = (C["accent"], C["load"], C["member2"], C["bmd"], C["deform"])
    peak = max(VALS)

    Y0, Y1, XW = 0.12, 1.24, 1.00           # 迷你圖框內可用範圍（120×74 px）

    def sketch(mini, i):
        col, v = COLS[i], VALS[i]
        f = v / peak
        if KIND[i] == "sec":                 # 斷面層次：曲率（應變分佈楔形）
            mini.line((0.35, Y0), (0.35, Y1), C["member"], 2.6, cap="butt")
            mini.polygon([(0.35, Y0), (0.35, Y1),
                          (0.35 + XW * f, Y1)], C["fill_c"], col, 1.8)
        else:                                # 構件／整體層次：懸臂頂點位移
            mini.line((0.35, Y0), (0.35, Y1), C["ghost"], 2.0, dash="4 3")
            mini.poly([(0.35 + XW * f * _elastic(j / 24), Y0 + (Y1 - Y0) * j / 24)
                       for j in range(25)], col, 3.0)
            mini.dot((0.35 + XW * f, Y1), 3.2, fill=col, stroke="#FFFFFF", w=1.2)

    cases = [
        ("μ_{φ}　讀法A", "斷面層次", MU_PHI,
         M(f"φ_{{u}}/φ_{{y}} = {PHI_U:.3f}/{PHI_Y:.3f} = {MU_PHI:.3f}"), COLS[0]),
        ("μ_{θ} = μ　讀法A", "構件／整體層次", MU,
         M(f"δ_{{u}}/δ_{{y}} = {DELTA_U*CM:.4f}/{DELTA_Y*CM:.4f} = {MU:.3f}"),
         COLS[1]),
        ("近似式驗算", "拿掉應變硬化項後完全吻合", MU_APPROX,
         M(f"1 + (μ_{{φ}}-1)λ = {MU_APPROX:.3f},  λ = {LAM:.3f}"), COLS[2]),
        ("μ_{φ}　讀法B", f"M = {M_APP:g} 之實際狀態", MU_PHI_B,
         M(f"φ_{{d}}/φ_{{y}} = {PHI_D:.4f}/{PHI_Y:.3f} = {MU_PHI_B:.3f}"), COLS[3]),
        ("μ_{θ} = μ　讀法B", "嚴格意義的韌性需求", MU_B,
         M(f"δ_{{d}}/δ_{{y}} = {DELTA_D*CM:.4f}/{DELTA_Y*CM:.4f} = {MU_B:.3f}"),
         COLS[4]),
    ]
    cv = bar_compare(
        cases, sketch=sketch,
        title="圖 3　三層韌性（斷面 → 構件 → 整體）與兩種讀法的完整對照",
        sub="長條長度＝該韌性比相對最大值的百分比；左側示意圖：楔形＝斷面曲率，"
            "曲線＝懸臂頂點位移",
        note=f"μ_{{θ}} 與 μ 必定相等（θ = δ/L，分子分母同除 L）；"
             f"且 μ ≤ μ_{{φ}}，因塑鉸只佔 L_{{p}}/L = {LP/L:.1%}，貢獻被稀釋")
    cv.text_px(cv.w / 2, cv.h - 96,
               f"讀法A（用 φ_{{u}}、δ_{{u}}）算的是韌性容量；"
               f"讀法B（M = {M_APP:g} 對應之實際狀態）才是嚴格的韌性需求",
               13, C["text"], weight="700")
    cv.text_px(cv.w / 2, cv.h - 70,
               f"容量／需求 = {MU:.3f} / {MU_B:.3f} = {CAP_DEM:.3f} → "
               f"尚有 {(CAP_DEM-1)*100:.1f}% 韌性餘裕（耐震評估判準：容量 ≥ 需求）",
               13, C["accent"], weight="700")
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 每張圖攔下什麼錯
# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-bilinear", fig1,
     "φ_u 內插方向弄反（0.030→0.010 是遞減，α=0.5 得 0.020）；"
     "誤以為 M=232.5 只是拿來確認已降伏"),
    ("2-cantilever", fig2,
     "L 誤用全柱淨高 6.4 m；δ_u 第二項力臂誤用 L 或 Lp；Lp 忘記取下限"),
    ("3-ductility", fig3,
     "把 μ 算得大於 μ_φ（不可能）；μ_θ 與 μ 算出不同值（必定相等）"),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    checks = [
        ("alpha",              ALPHA,           0.5,       1e-12),
        ("phi_y rad/m",        PHI_Y,           0.005,     1e-12),
        ("M_y tf\u00b7m",           M_Y,             220.0,     1e-9),
        ("phi_u rad/m",        PHI_U,           0.020,     1e-12),
        ("M_u tf\u00b7m",           M_U,             245.0,     1e-9),
        ("L m",                L,               3.2,       1e-12),
        ("Lp_eq1 m",           LP_EQ1,          0.553,     6e-4),
        ("Lp_lower m",         LP_LOWER,        0.595,      6e-4),
        ("Lp m",               LP,              0.595,      6e-4),
        ("delta_y m",          DELTA_Y,         0.017067,  1e-6),
        ("theta_y rad",        THETA_Y,         0.0053333, 1e-7),
        ("Mu_My",              HARDEN,          1.1136,    1e-4),
        ("arm m",              ARM,             2.9025,    5e-4),
        ("delta_u m",          DELTA_U,         0.044905,  2e-5),
        ("theta_u rad",        THETA_U,         0.014033,  6e-6),
        ("mu_phi",             MU_PHI,          4.000,     1e-9),
        # μ 的精確值為 2.6316（.md 印 2.63；用四捨五入後的 cm 相除得 2.631）
        ("mu_theta",           MU_THETA,        2.631,     1e-3),
        ("mu",                 MU,              2.631,     1e-3),
        ("phi_d rad/m",        PHI_D,           0.0125,    1e-12),
        ("mu_phi_B",           MU_PHI_B,        2.500,     1e-9),
        ("delta_d m",          DELTA_D,         0.030986,  1e-5),
        ("mu_B",               MU_B,            1.816,     5e-4),
        ("lambda",             LAM,             0.506,     5e-4),
        ("mu_approx",          MU_APPROX,       2.518,     5e-4),
        ("delta_u_nohard m",   DELTA_U_NOHARD,  0.042966,  1e-5),
    ]
    print(f"── 與 {TAG}.md §4／§5 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<18} 算得 {got:>12.6g}   .md {want:>10}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"

    # 內建物理檢核（改輸入重跑時仍須成立）
    assert MU_THETA == MU or abs(MU_THETA - MU) < 1e-12, "μ_θ 必須等於 μ"
    assert MU <= MU_PHI, "μ 不可能大於 μ_φ"
    assert MU_B <= MU_PHI_B, "讀法B 的 μ 不可能大於 μ_φ"
    assert HI["phi_u"] < LO["phi_u"], "φ_u 應隨軸壓遞減"
    assert abs(DELTA_U_NOHARD / DELTA_Y - MU_APPROX) < 5e-4, "無硬化 μ 應等於近似式"
    assert abs(M_APP - M_MID) < 1e-9, "M = 232.5 應為 M_y 與 M_u 的正中點"
    print("  OK  物理檢核：μ_θ = μ、μ ≤ μ_φ、φ_u 遞減、無硬化 μ = 近似式、"
          "232.5 為正中點")

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
