#!/usr/bin/env python3
"""
RC-2015-1 對稱雙排配筋方形柱・最大彎矩（平衡點） — 解題圖解產生腳本

用法：
    python3 gen_RC-2015-1.py [輸出目錄]

三條鐵則的落實：
  1. 常數區只放 RC-2015-1.md §1 給定的原始資料；其餘（beta1、cb、ab、Cc、Cs'、Ts、
     Pn、Mn、phi）全部由 section_forces() 現算，並在檔尾對 §4 的公佈值做 assert。
  2. 改 §1 任一個數字（斷面、fc、fy、配筋）重跑，四張圖的幾何與 P-M 曲線都會跟著變。
  3. FIGURES 表寫明每張圖攔什麼錯。
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", "/mnt/skills/user/struct-diagram/scripts"))

from structdraw import Canvas, C, compose, esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2015-1"

# ══════════════════════════════════════════════════════════
# §1 原始給定（唯一的手輸入區；其餘一律由此推算）
# ══════════════════════════════════════════════════════════
B      = 60.0        # 斷面寬 b (cm)
HH     = 60.0        # 斷面全深 h (cm)
DP     = 8.0         # d'：受壓面至縱筋形心 (cm)
FC     = 350.0       # f'c (kgf/cm^2)
FY     = 4200.0      # fy (kgf/cm^2)
ES     = 2_040_000.0 # Es (kgf/cm^2)   →  0.003*Es = 6120，與 §4 Step 2 一致
A_BAR  = 8.143       # #10 單根斷面積 (cm^2)，鋼筋表
N_BAR  = 4           # 每排根數（頂 4 + 底 4）
EPS_CU = 0.003       # 混凝土極限壓應變

# ── 由上列推得 ──────────────────────────────────────────
D      = HH - DP                                   # 有效深度 = 52
AS     = N_BAR * A_BAR                             # 單排鋼筋量 = 32.572
AST    = 2 * AS                                    # 全斷面 = 65.144
AG     = B * HH
BETA1  = max(0.65, min(0.85, 0.85 - 0.05 * (FC - 280) / 70))
EPSY   = FY / ES
CB     = (EPS_CU * ES) / (EPS_CU * ES + FY) * D    # 平衡中性軸
AB     = BETA1 * CB
LAYERS = ((DP, AS), (D, AS))                       # (深度, 面積)：頂排、底排

KGF_TF   = 1e-3        # kgf   → tf
KGCM_TFM = 1e-5        # kgf·cm → tf·m


# ══════════════════════════════════════════════════════════
# 斷面分析：給中性軸深度 c，回傳該應變狀態下的所有內力
# 這支函式就是全部四張圖的唯一數值來源
# ══════════════════════════════════════════════════════════
def section_forces(c):
    """壓力為正。回傳 dict（單位 kgf、kgf·cm、tf、tf·m）。"""
    a = min(BETA1 * c, HH)
    Cc = 0.85 * FC * a * B
    Mn = Cc * (HH / 2 - a / 2)
    Pn = Cc
    bars = []
    for di, Ai in LAYERS:
        eps = EPS_CU * (c - di) / c                       # 壓為正
        fs = max(-FY, min(FY, ES * eps))
        # 位於等值應力塊範圍內的壓力鋼筋，須扣除混凝土占位（陷阱③）
        f_net = fs - 0.85 * FC if di <= a else fs
        F = Ai * f_net
        Pn += F
        Mn += F * (HH / 2 - di)
        bars.append(dict(d=di, eps=eps, fs=fs, f_net=f_net, F=F))
    eps_t = EPS_CU * (D - c) / c                          # 最外層拉應變（拉為正）
    # phi：依 wiki/code-ref/ACI-318.md §21.2.2 的現行式
    #      壓力控制 eps_t <= eps_ty；過渡區 eps_ty < eps_t < 0.005；eps_ty = fy/Es
    phi = 0.65 + 0.25 * (eps_t - EPSY) / (0.005 - EPSY)
    phi = max(0.65, min(0.90, phi))
    return dict(c=c, a=a, Cc=Cc, bars=bars, Pn=Pn, Mn=Mn, eps_t=eps_t, phi=phi,
                Pn_tf=Pn * KGF_TF, Mn_tfm=Mn * KGCM_TFM,
                fPn_tf=phi * Pn * KGF_TF, fMn_tfm=phi * Mn * KGCM_TFM)


def c_at_zero_axial():
    """純彎矩點（Pn = 0）的中性軸深度，二分法解出，不是猜的。"""
    lo, hi = 0.5, HH
    while hi - lo > 1e-9:
        mid = (lo + hi) / 2
        if section_forces(mid)["Pn"] > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def max_design_moment(n=4000):
    """φM_n 的最大值。φ 隨 ε_t 增大而由 0.65 升至 0.90，故 φM_n 的峰值
    並不落在標稱 M_n 的峰值（平衡點）上——這是本題最容易被忽略的一點。"""
    best = None
    for i in range(n + 1):
        c = C0 + (CB * 1.6 - C0) * i / n
        r = section_forces(c)
        if best is None or r["fMn_tfm"] > best["fMn_tfm"]:
            best = r
    return best


# ── 關鍵狀態 ────────────────────────────────────────────
BAL = section_forces(CB)                 # 平衡點 = 標稱 M_n 之最大值
C0  = c_at_zero_axial()
PB  = section_forces(C0)                 # 純彎矩點
PN_MAX = 0.80 * (0.85 * FC * (AG - AST) + FY * AST)          # 純軸壓上限（束制柱）
FPN_MAX = 0.65 * PN_MAX
DMAX = max_design_moment()               # φM_n 峰值（位於過渡區，非平衡點）


def pm_curve(n=260):
    """由 section_forces 掃描 c 產生 P-M 曲線（自純軸壓至純彎矩）。"""
    cs = [C0 + (12.0 * HH - C0) * (i / (n - 1)) ** 2.2 for i in range(n)][::-1]
    Mn, Pn, fM, fP = [], [], [], []
    for c in cs:
        r = section_forces(c)
        p_tf = min(r["Pn_tf"], PN_MAX * KGF_TF)
        fp_tf = min(r["fPn_tf"], FPN_MAX * KGF_TF)
        Mn.append(r["Mn_tfm"]); Pn.append(p_tf)
        fM.append(r["fMn_tfm"]); fP.append(fp_tf)
    return Mn, Pn, fM, fP


# ══════════════════════════════════════════════════════════
# 共用：畫斷面（含兩排鋼筋與箍筋）
# ══════════════════════════════════════════════════════════
DB10 = 3.22          # #10 標稱直徑 (cm)，鋼筋表；僅供箍筋示意定位，不標註尺寸


def draw_section(cv, bars=True, tie=True, fill="#EDF1F6"):
    cv.polygon([(0, 0), (B, 0), (B, HH), (0, HH)], fill, C["member"], 2.8)
    if tie:
        t = DP - DB10 / 2                       # 箍筋內緣與鋼筋外緣相切
        cv.poly([(t, t), (B - t, t), (B - t, HH - t), (t, HH - t), (t, t)],
                C["member2"], 2.0)
    if bars:
        for y in (HH - DP, DP):
            for i in range(N_BAR):
                x = DP + (B - 2 * DP) * i / (N_BAR - 1)
                cv.dot((x, y), 6.2, fill=C["member"], stroke="#FFFFFF", w=1.5)


# ══════════════════════════════════════════════════════════
# 圖 1：題目重繪
# ══════════════════════════════════════════════════════════
def fig1_section():
    W, Hpx = 700, 600
    sx = 5.2
    cv = Canvas(W, Hpx, sx=sx, ox=W / 2 - B * sx / 2, oy=100, bg="#FFFFFF")
    draw_section(cv)

    # 尺寸線一律置於斷面之外（左：d'；右：h、d；下：b）
    cv.dim((0, 0), (B, 0), f"b = {B:g} cm", off=52, label_off=17)
    cv.dim((B, 0), (B, HH), f"h = {HH:g} cm", off=46, label_off=42)
    # d' 與 d 的標註手動放置：dim() 的 label 會落在尺寸線上，短尺寸會被箭頭穿過
    cv.dim((0, HH), (0, HH - DP), "", off=42)
    cv.math_px(cv.X(0) - 50, cv.Y(HH - DP / 2), f"d' = {DP:g}", 13, C["dim"], "end")
    cv.dim((0, HH), (0, DP), "", off=112)
    cv.math_px(cv.X(0) - 120, cv.Y((HH + DP) / 2), f"d = {D:g}", 13, C["dim"], "end")

    # 受壓側／受拉側（最大彎矩狀態：上壓下拉）
    for xf in (0.28, 0.72):
        cv.arrow((B * xf, HH + 4.5), (B * xf, HH + 0.8), C["compr"], 2.8, 9)
        cv.arrow((B * xf, -0.8), (B * xf, -4.5), C["tension"], 2.8, 9)
    cv.text((B / 2, HH - DP / 2), "受壓側", 13, C["compr"], weight="700")
    cv.text((B / 2, DP / 2), "受拉側", 13, C["tension"], weight="700")

    cv.text_px(W / 2, 34, "圖 1　斷面重繪（向量版）", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, f"d' 量至縱筋形心，非淨保護層 → d = h − d' = {D:g} cm",
               13, C["muted"])
    # 中文一律走 text_px（黑體）；math_px 是襯線數學字型，缺中文字會整段消失
    cv.math_px(W / 2, 84,
               f"f'_{{c}} = {FC:g} kgf/cm^{{2}}    f_{{y}} = {FY:g} kgf/cm^{{2}}"
               f"    A_{{#10}} = {A_BAR:g} cm^{{2}}", 13, C["muted"])
    cv.text_px(W / 2, 106,
               f"縱筋 {2*N_BAR}-#10（頂 {N_BAR} 根 + 底 {N_BAR} 根，對稱雙排）",
               13, C["muted"])
    cv.math_px(W / 2, 128,
               f"A_{{s}} = A'_{{s}} = {AS:.3f} cm^{{2}}    "
               f"A_{{st}} = {AST:.3f} cm^{{2}}    ρ_{{g}} = {AST/AG*100:.2f}%",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 2：平衡點的斷面／應變／合力三聯
# ══════════════════════════════════════════════════════════
def fig2_balanced():
    PW, PH = 430, 500
    sc = 4.6

    # ---- (a) 斷面與壓力區 ----
    p1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - B * sc / 2, oy=70)
    p1.panel("斷面與壓力區", f"c_{{b}} = {CB:.2f} cm　　a_{{b}} = {AB:.2f} cm")
    draw_section(p1)
    p1.polygon([(0, HH - AB), (B, HH - AB), (B, HH), (0, HH)], C["fill_c"], "none")
    p1.line((-3, HH - CB), (B + 3, HH - CB), C["accent"], 2.0, dash="7 4")
    p1.text_px(p1.X(B) + 8, p1.Y(HH - CB), "N.A.", 12.5, C["accent"], "start", weight="700")
    # 數值放在面板副標；此處只留符號，尺寸線才不會擠出面板
    p1.dim((0, HH), (0, HH - CB), "c_{b}", off=30, label_off=20, color=C["accent"])
    p1.dim((B, HH), (B, HH - AB), "a_{b}", off=-30, label_off=-20, color=C["compr"])

    # ---- (b) 應變分佈 ----
    KE = 17.0 / EPS_CU                        # 應變 → 模型單位
    p2 = Canvas(PW, PH, sx=sc, ox=PW * 0.44, oy=70)
    p2.panel("應變分佈（平衡點）", "平面保持平面 → 線性")
    p2.line((0, 0), (0, HH), C["ghost"], 2, dash="5 4")
    e_top = EPS_CU
    e_sp = BAL["bars"][0]["eps"]
    e_bot = BAL["bars"][1]["eps"]             # 負值 = 拉
    p2.polygon([(0, HH - CB), (e_top * KE, HH), (0, HH)], C["fill_c"], C["compr"], 2.4)
    p2.polygon([(0, HH - CB), (e_bot * KE, HH - D), (0, HH - D)], C["fill_t"],
               C["tension"], 2.4)
    p2.line((-20, HH - CB), (20, HH - CB), C["accent"], 1.8, dash="6 4")
    p2.math_px(p2.X(e_top * KE) + 6, p2.Y(HH) + 13, f"ε_{{cu}} = {EPS_CU}", 12.5,
               C["compr"], "start", weight="700")
    p2.line((0, HH - DP), (e_sp * KE, HH - DP), C["compr"], 2.0)
    p2.dot((e_sp * KE, HH - DP), 4.6, fill=C["compr"], stroke="#FFFFFF", w=1.4)
    p2.math_px(p2.X(e_sp * KE) + 7, p2.Y(HH - DP), f"ε'_{{s}} = {e_sp:.5f}", 12.5,
               C["compr"], "start", weight="700")
    p2.dot((e_bot * KE, HH - D), 4.6, fill=C["tension"], stroke="#FFFFFF", w=1.4)
    p2.math_px(p2.X(e_bot * KE) + 34, p2.Y(HH - D) + 18,
               f"ε_{{t}} = ε_{{y}} = {abs(e_bot):.5f}", 12.5, C["tension"], weight="700")
    p2.text_px(p2.X(20) + 5, p2.Y(HH - CB), "N.A.", 12, C["accent"], "start", weight="700")
    p2.text_px(PW / 2, PH - 46, esc(f"ε'_s = {e_sp:.5f} > ε_y = {EPSY:.5f}"), 13,
               C["compr"], weight="700")
    p2.text_px(PW / 2, PH - 26, "→ 壓力鋼筋已降伏", 13, C["compr"], weight="700")

    # ---- (c) 應力與合力 ----
    SW = 12.0
    p3 = Canvas(PW, PH, sx=sc, ox=PW * 0.52, oy=70)
    p3.panel("等值應力塊與合力", "Whitney block")
    p3.line((0, 0), (0, HH), C["ghost"], 2, dash="5 4")
    p3.polygon([(0, HH - AB), (SW, HH - AB), (SW, HH), (0, HH)], C["fill_c"],
               C["compr"], 2.4)
    p3.math_px(p3.X(SW) + 6, p3.Y(HH) + 12, f"0.85f'_{{c}}", 12.5, C["compr"],
               "start", weight="700")

    Cc_tf = BAL["Cc"] * KGF_TF
    Cs_tf = BAL["bars"][0]["F"] * KGF_TF
    Ts_tf = -BAL["bars"][1]["F"] * KGF_TF
    # C_c 作用於 a_b/2、C'_s 於 d'、T_s 於 d：三者 y 位置由解題幾何決定，
    # 標註各自貼在箭頭端，靠 y 差（≥ 20 px）分開，不再上下堆疊
    p3.arrow((SW * 0.30, HH - AB / 2), (SW * 1.60, HH - AB / 2), C["compr"], 3.4, 11)
    p3.math_px(p3.X(SW * 1.60) + 8, p3.Y(HH - AB / 2),
               f"C_{{c}} = {Cc_tf:.2f} tf", 12.5, C["compr"], "start", weight="700")
    p3.arrow((0, HH - DP), (SW * 1.05, HH - DP), C["compr"], 3.0, 10)
    p3.math_px(p3.X(SW * 1.05) + 8, p3.Y(HH - DP),
               f"C'_{{s}} = {Cs_tf:.2f} tf", 12.5, C["compr"], "start", weight="700")
    p3.arrow((0, HH - D), (-SW * 1.20, HH - D), C["tension"], 3.2, 10)
    p3.math_px(p3.X(-SW * 1.20) - 8, p3.Y(HH - D),
               f"T_{{s}} = {Ts_tf:.2f} tf", 12.5, C["tension"], "end", weight="700")
    p3.line((-SW * 1.35, HH / 2), (SW * 1.35, HH / 2), C["ghost"], 1.6, dash="4 4")
    p3.text_px(p3.X(SW * 1.35) + 5, p3.Y(HH / 2), "形心", 11.5, C["muted"], "start")
    p3.math_px(PW / 2, PH - 46, f"C'_{{s}} = A'_{{s}}(f_{{y}} − 0.85f'_{{c}})", 12.5,
               C["compr"], weight="700")
    p3.text_px(PW / 2, PH - 26, "壓力鋼筋須扣混凝土占位", 12.5, C["muted"])

    # compose() 的 title／sub／note 走純文字（不經 mtext），故不寫 _{} 也不用 ₁ ² 等字元
    return compose(
        [p1, p2, p3],
        title=f"圖 3　平衡點狀態：斷面／應變／合力（cb = {CB:.2f} cm）",
        sub=f"三格垂直比例相同，故 cb、ab、d 的相對位置為真（ab = β1 × cb，β1 = {BETA1:.2f}）",
        note=(f"力平衡 Pn,b = Cc + Cs' − Ts = {BAL['Pn_tf']:.1f} tf　｜　"
              f"對形心取矩 Mn,max = {BAL['Mn_tfm']:.2f} tf·m"))


# ══════════════════════════════════════════════════════════
# 圖 3：M_n – c 曲線（§5 導數論證的視覺版）
# ══════════════════════════════════════════════════════════
def fig3_mn_c():
    W, Hpx = 760, 520
    L, R, T, Bm = 92, 118, 96, 74
    c_max = 1.5 * CB
    m_max = BAL["Mn_tfm"] * 1.30
    kx = (W - L - R) / c_max
    ky = (Hpx - T - Bm) / m_max
    cv = Canvas(W, Hpx, sx=1.0, ox=L, oy=Bm, bg="#FFFFFF")

    def P(c, m):
        return (c * kx, m * ky)

    # 曲線（由 section_forces 逐點算出）
    n = 400
    cs = [0.25 + (c_max - 0.25) * i / (n - 1) for i in range(n)]
    pts = [P(c, section_forces(c)["Mn_tfm"]) for c in cs]

    # 座標軸
    cv.arrow((0, 0), (c_max * kx * 1.02, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, m_max * ky * 1.02), C["muted"], 1.8, 9)
    for c in range(0, int(c_max) + 1, 10):
        cv.line(P(c, 0), (c * kx, -7), C["muted"], 1.2)
        cv.text_px(cv.X(c * kx), cv.Y(-7) + 16, f"{c}", 12, C["muted"])
    for m in range(0, int(m_max) + 1, 30):
        cv.line(P(0, m), (-7, m * ky), C["muted"], 1.2)
        cv.text_px(cv.X(-10), cv.Y(m * ky), f"{m}", 12, C["muted"], "end")
    cv.text_px(cv.X(c_max * kx * 1.02) + 6, cv.Y(0) + 20, "c（cm）", 13, C["muted"], "end")
    cv.text_px(cv.X(0) - 6, cv.Y(m_max * ky * 1.02) - 14, "M_n（tf·m）", 13, C["muted"])

    # 兩段分色：c ≤ cb 遞增、c > cb 遞減
    left = [p for p, c in zip(pts, cs) if c <= CB]
    right = [p for p, c in zip(pts, cs) if c >= CB]
    cv.polygon(left + [(CB * kx, 0), (left[0][0], 0)], C["fill_c"], "none")
    cv.poly(left, C["compr"], 3.4)
    cv.poly(right, C["tension"], 3.4)

    # 峰值（平衡點）
    cv.line(P(CB, 0), P(CB, BAL["Mn_tfm"]), C["accent"], 1.6, dash="6 4")
    cv.line(P(0, BAL["Mn_tfm"]), P(CB, BAL["Mn_tfm"]), C["accent"], 1.6, dash="6 4")
    # 含中文的標註一律用 text_px；math_px 的襯線字型沒有中文字，整段中文會消失
    cv.dot(P(CB, BAL["Mn_tfm"]), 6.4, fill=C["accent"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(CB * kx) + 12, cv.Y(BAL["Mn_tfm"] * ky) - 36,
               f"平衡點 c_{{b}} = {CB:.2f} cm", 13.5, C["accent"], "start", weight="700")
    cv.text_px(cv.X(CB * kx) + 12, cv.Y(BAL["Mn_tfm"] * ky) - 15,
               f"M_{{n,max}} = {BAL['Mn_tfm']:.2f} tf·m（P_{{n}} = {BAL['Pn_tf']:.1f} tf）",
               13, C["accent"], "start", weight="700")

    # 純彎矩點
    cv.dot(P(C0, PB["Mn_tfm"]), 5.6, fill=C["member"], stroke="#FFFFFF", w=1.8)
    cv.text_px(cv.X(C0 * kx) + 14, cv.Y(PB["Mn_tfm"] * ky) + 20,
               f"純彎矩點 P_{{n}} = 0", 12.5, C["member"], "start", weight="700")
    cv.text_px(cv.X(C0 * kx) + 14, cv.Y(PB["Mn_tfm"] * ky) + 40,
               f"c = {C0:.2f} cm，M_{{n}} = {PB['Mn_tfm']:.2f} tf·m", 12.5,
               C["muted"], "start")

    cv.text_px(cv.X(CB * kx * 0.44), cv.Y(BAL["Mn_tfm"] * ky * 0.12),
               esc("dM_n/dc > 0（遞增）"), 13, C["compr"], weight="700")
    cv.text_px(cv.X((CB + c_max) / 2 * kx), cv.Y(BAL["Mn_tfm"] * ky * 0.12),
               esc("dM_n/dc < 0（遞減）"), 13, C["tension"], weight="700")

    cv.text_px(W / 2, 34, "圖 2　標稱彎矩隨中性軸深度的變化", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "曲線由斷面分析逐點算出，峰值位置不是畫上去的",
               13, C["muted"])
    cv.text_px(W / 2, Hpx - 22,
               f"M_n(c_b)/M_n(純彎矩) = {BAL['Mn_tfm']/PB['Mn_tfm']:.2f} 倍"
               "　→　最大彎矩絕不在 P = 0 處", 13.5, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
# 圖 4：P-M 交互曲線
# ══════════════════════════════════════════════════════════
def fig4_pm():
    """兩條曲線（標稱／設計）的軸壓截頂高度不同，recipes.pm_interaction 只吃一條，
    故此圖以 primitives 自行組裝。"""
    Mn, Pn, fM, fP = pm_curve()
    W, Hpx = 820, 700
    L, R, T, Bm = 96, 200, 92, 120
    m_max = max(max(Mn), max(fM)) * 1.20
    p_max = max(max(Pn), max(fP)) * 1.12
    kx = (W - L - R) / m_max
    ky = (Hpx - T - Bm) / p_max
    cv = Canvas(W, Hpx, sx=1.0, ox=L, oy=Bm, bg="#FFFFFF")

    def P(m, p):
        return (m * kx, p * ky)

    # 座標軸與刻度
    cv.arrow((0, 0), (m_max * kx * 1.02, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, p_max * ky * 1.02), C["muted"], 1.8, 9)
    for m in range(0, int(m_max) + 1, 30):
        cv.line(P(m, 0), (m * kx, -7), C["muted"], 1.2)
        cv.text_px(cv.X(m * kx), cv.Y(-7) + 16, f"{m}", 12, C["muted"])
    for p in range(0, int(p_max) + 1, 200):
        cv.line(P(0, p), (-7, p * ky), C["muted"], 1.2)
        cv.text_px(cv.X(-10), cv.Y(p * ky), f"{p}", 12, C["muted"], "end")
    cv.text_px(cv.X(m_max * kx * 1.02), cv.Y(0) + 36, "M（tf·m）", 13, C["muted"])
    cv.text_px(cv.X(0), cv.Y(p_max * ky * 1.02) - 16, "P（tf）", 13, C["muted"])

    # 設計曲線（安全區）與標稱曲線
    dpts = [P(m, p) for m, p in zip(fM, fP)]
    cv.polygon([(0, dpts[0][1])] + dpts + [(0, dpts[-1][1])], C["fill_c"], "none")
    cv.poly(dpts, C["compr"], 3.0)
    cv.poly([P(m, p) for m, p in zip(Mn, Pn)], C["muted"], 2.0, dash="7 5")
    cv.text_px(cv.X(m_max * kx * 0.20), cv.Y(p_max * ky * 0.45), "安全區", 15,
               C["compr"], weight="700")

    # 壓力控制／拉力控制分界（平衡點所在水平線）
    cv.line(P(0, BAL["fPn_tf"]), P(m_max * 0.95, BAL["fPn_tf"]), C["accent"], 1.4,
            dash="9 5")
    cv.text_px(cv.X(m_max * kx * 0.55), cv.Y(p_max * ky * 0.59),
               "壓力控制（φ = 0.65）", 13, C["compr"], weight="700")
    cv.text_px(cv.X(m_max * kx * 0.92), cv.Y(p_max * ky * 0.045),
               "拉力控制（φ = 0.90）", 13, C["tension"], weight="700")

    # 關鍵點：純軸壓、平衡點（標稱 M_n 峰值）、φM_n 峰值、純彎矩
    for m, p in ((fM[0], fP[0]), (BAL["fMn_tfm"], BAL["fPn_tf"]),
                 (DMAX["fMn_tfm"], DMAX["fPn_tf"]), (PB["fMn_tfm"], 0.0)):
        cv.dot(P(m, p), 6.0, fill=C["accent"], stroke="#FFFFFF", w=2.0)
    cv.text_px(cv.X(fM[0] * kx) + 14, cv.Y(fP[0] * ky) - 20,
               f"純軸壓　φP_{{n,max}} = {FPN_MAX*KGF_TF:.1f} tf", 12.5, C["accent"],
               "start", weight="700")
    cv.text_px(cv.X(BAL["fMn_tfm"] * kx) - 14, cv.Y(BAL["fPn_tf"] * ky) - 17,
               f"平衡點（標稱 M_{{n}} 峰值）　({BAL['fMn_tfm']:.1f}, {BAL['fPn_tf']:.1f})",
               12.5, C["accent"], "end", weight="700")
    cv.line(P(DMAX["fMn_tfm"], DMAX["fPn_tf"]),
            (DMAX["fMn_tfm"] * kx + 10 / kx, DMAX["fPn_tf"] * ky - 16 / ky),
            C["accent"], 1.2)
    cv.text_px(cv.X(DMAX["fMn_tfm"] * kx) + 14, cv.Y(DMAX["fPn_tf"] * ky) + 22,
               f"φM_{{n}} 峰值 = {DMAX['fMn_tfm']:.1f} tf·m", 12.5, C["accent"],
               "start", weight="700")
    cv.text_px(cv.X(DMAX["fMn_tfm"] * kx) + 14, cv.Y(DMAX["fPn_tf"] * ky) + 41,
               f"（ε_{{t}} = 0.005，φ = 0.90，φP_{{n}} = {DMAX['fPn_tf']:.1f} tf）",
               12, C["muted"], "start")
    cv.text_px(cv.X(PB["fMn_tfm"] * kx) - 14, cv.Y(0) - 17,
               f"純彎矩　φM_{{n}} = {PB['fMn_tfm']:.1f} tf·m", 12.5, C["accent"],
               "end", weight="700")

    cv.legend(L, Hpx - 46,
              [(C["compr"], "設計強度 φP_n – φM_n（含 0.80φP_n,max 截頂）"),
               (C["muted"], "標稱強度 P_n – M_n")])
    cv.text_px(W / 2, 34, "圖 4　P-M 交互曲線", 17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58, "曲線由斷面分析掃描中性軸深度產生，非示意圖",
               13, C["muted"])
    return cv.svg()


# ══════════════════════════════════════════════════════════
FIGURES = [
    ("1-section",  fig1_section, "把 d'=8 誤讀成淨保護層 → d 算錯；漏看頂底各 4 根對稱配筋"),
    ("2-mn-c",     fig3_mn_c,    "以為最大彎矩發生在純彎矩（P=0）點"),
    ("3-balanced", fig2_balanced, "c 與 a 搞混；壓力鋼筋忘扣 0.85f'c 占位；未驗 ε'_s 是否降伏"),
    ("4-pm",       fig4_pm,      "平衡點位置畫錯；壓力控制／拉力控制分區搞反"),
]


def main():
    os.makedirs(OUT, exist_ok=True)

    # ── 對 RC-2015-1.md §4 公佈值的自我檢核 ──
    checks = [
        ("beta1",   BETA1,                       0.80,    0.005),
        ("c_b",     CB,                          30.84,   0.01),
        ("a_b",     AB,                          24.67,   0.01),
        ("eps'_s",  BAL["bars"][0]["eps"],       0.00222, 1e-5),
        ("C_c",     BAL["Cc"] * KGF_TF,          440.36,  0.05),
        ("T_s",     -BAL["bars"][1]["F"] * KGF_TF, 136.80, 0.05),
        ("P_n,b",   BAL["Pn_tf"],                430.7,   0.2),
        ("M_n,max", BAL["Mn_tfm"],               135.85,  0.05),
        ("phi",     BAL["phi"],                  0.650,   0.001),
        ("phiM_n",  BAL["fMn_tfm"],              88.30,   0.1),
        ("phiP_n,max", FPN_MAX * KGF_TF,         689.1,   0.5),
    ]
    print("── 與 RC-2015-1.md §4 對帳 ──")
    for name, got, want, tol in checks:
        ok = abs(got - want) <= tol
        print(f"  {'OK ' if ok else 'X  '} {name:<12} 算得 {got:>10.5f}   .md {want:>9}")
        assert ok, f"{name} 與解題檔不符：{got} vs {want}"
    print(f"  （補算）純彎矩 c = {C0:.2f} cm, M_n = {PB['Mn_tfm']:.2f} tf·m, "
          f"ε_t = {PB['eps_t']:.5f}, φ = {PB['phi']:.2f}, φM_n = {PB['fMn_tfm']:.2f} tf·m")
    print(f"  （補算）φM_n 峰值 c = {DMAX['c']:.2f} cm, ε_t = {DMAX['eps_t']:.5f}, "
          f"φ = {DMAX['phi']:.2f}, φM_n = {DMAX['fMn_tfm']:.2f} tf·m "
          f"（平衡點僅 {BAL['fMn_tfm']:.2f} tf·m）")

    print("\n── 產圖 ──")
    for name, fn, catches in FIGURES:
        svg = fn()
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        if svg is not None:
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            open(path, "w", encoding="utf-8").write(svg)
        print(f"  {os.path.basename(path):<34} 攔：{catches}")


if __name__ == "__main__":
    main()
