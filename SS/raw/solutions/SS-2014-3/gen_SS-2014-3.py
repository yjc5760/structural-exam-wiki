#!/usr/bin/env python3
"""
SS-2014-3 W21×93 雙向彎曲梁（LTB ＋ 弱軸上限 ＋ 互制）— 解題圖解產生腳本

用法：
    python3 gen_SS-2014-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2014-3.md 哪一節
  2. C_b 由四點求積式現算（兩種題意解讀各自算），M_nx 由線性內插式現算，
     改 L_b 或 L_r，曲線與互制線會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose
from recipes import plot_function

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2014-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2014-3.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 題目給定
FY, FR = 350.0, 78.0            # MPa
SX, SY = 3146316.0, 362154.0    # mm^3
ZX, ZY = 3621541.0, 568631.0    # mm^3
LP, LR, LB = 2.0, 5.8, 4.0      # m
MUX, MUY = 400.0, 50.0          # kN-m（已含載重係數）
PHI = 0.9
# §4 Step 2c
MP = FY * ZX / 1e6              # 1,267.5 kN-m
MR = (FY - FR) * SX / 1e6       # 855.8 kN-m
# §4 Step 2b：C_b 由四點求積式現算（兩種題意解讀）
def cb(qa, qb, qc, mmax=1.0):
    return 12.5 * mmax / (2.5 * mmax + 3 * qa + 4 * qb + 3 * qc)

CB_UNIFORM = cb(1.0, 1.0, 1.0)          # 甲：均勻彎矩（主答）→ 1.000
CB_UDL = cb(0.75, 1.0, 0.75)            # 乙：均佈載重之最大彎矩 → 1.136
# §4 Step 2d
BRACKET = MP - (MP - MR) * (LB - LP) / (LR - LP)      # 1,050.8 kN-m
MNX_A = min(CB_UNIFORM * BRACKET, MP)                 # 1,050.8
MNX_B = min(CB_UDL * BRACKET, MP)                     # 1,193.8
PHI_MNX_A, PHI_MNX_B = PHI * MNX_A, PHI * MNX_B       # 945.8 / 1,074.4
# §4 Step 3：弱軸上限
MNY_Z = FY * ZY / 1e6                                 # 199.0（F_y Z_y）
MNY_CAP15 = 1.5 * FY * SY / 1e6                       # 190.1（台灣 2010 上限）
MNY_CAP16 = 1.6 * FY * SY / 1e6                       # 202.8（AISC 360-10 起）
MNY = min(MNY_Z, MNY_CAP15)                           # 190.1 ← 上限控制
PHI_MNY = PHI * MNY                                   # 171.1
# §4 Step 4
RATIO_A = MUX / PHI_MNX_A + MUY / PHI_MNY             # 0.715（主答）
RATIO_B = MUX / PHI_MNX_B + MUY / PHI_MNY             # 0.664（另解）
# §5④ 中間側撐：L_b 減半至 L_p，可達全塑性
PHI_MP = PHI * MP                                     # 1,140.8
RATIO_BRACED = MUX / PHI_MP + MUY / PHI_MNY           # 0.643
# §6 AISC 360-16／-22
MR_A16 = 0.7 * FY * SX / 1e6                          # 770.9
BRACKET_A16 = MP - (MP - MR_A16) * (LB - LP) / (LR - LP)   # 1,006.1
PHI_MNX_A16 = PHI * min(CB_UNIFORM * BRACKET_A16, MP)      # 905.5
MNY_A16 = min(MNY_Z, MNY_CAP16)                            # 199.0
PHI_MNY_A16 = PHI * MNY_A16                                # 179.1
RATIO_A16 = MUX / PHI_MNX_A16 + MUY / PHI_MNY_A16          # 0.721


def mn_curve(lb, cbv):
    """§4 Step 2d 的三分區（彈性段題目未給 GJ、C_w，故不外推）"""
    if lb <= LP:
        return min(cbv * MP, MP)
    return min(cbv * (MP - (MP - MR) * (lb - LP) / (LR - LP)), MP)


# ══════════════════════════════════════════════════════════
# 圖 2：「均佈的雙向彎矩」的兩種題意解讀
# ══════════════════════════════════════════════════════════
PW2, PH2 = 520, 420
SX2, OX2, OY2 = 90.0, 77.0, 220.5
BMD_SCALE = -0.82 / MUX         # 400 kN-m 對應 0.82 模型單位，負號＝畫在梁下方
BASE_Y = -0.56


def _panel_cb(title, sub, quarters, cbv, phi_mnx, ratio, udl, tag_col):
    cv = Canvas(PW2, PH2, sx=SX2, ox=OX2, oy=OY2)
    cv.panel(title, sub)
    cv.line((0, 0), (4, 0), C["member"], 6.0, cap="butt")
    cv.pin_support((0, 0), size=14)
    cv.roller_support((4, 0), size=14)
    if udl:
        cv.udl((0, 0), (4, 0), 0.40, n=11, label="w")
    else:
        for x, ccw in ((0, False), (4, True)):
            cv.moment_arrow((x, 0), r=30, ccw=ccw, color=C["load"], w=3.0,
                            span=250, start=(200 if x == 0 else -20))
        cv.math_px(cv.X(0), cv.Y(0) - 52, "M", 17, C["load"], weight="700")
        cv.math_px(cv.X(4), cv.Y(0) - 52, "M", 17, C["load"], weight="700")

    xs = [i / 60.0 * 4 for i in range(61)]
    if udl:
        ys = [MUX * 4 * x * (4 - x) / 16 for x in xs]
    else:
        ys = [MUX for _ in xs]
    plot_function(cv, xs, ys, BMD_SCALE, BASE_Y, 0.0, C["bmd"], C["fill_m"], 2.2,
                  zero_line=False)
    cv.line((0, BASE_Y), (4, BASE_Y), C["muted"], 1.4)

    # 四分點：C_b 四點求積式真正用到的三個值
    for x, q, nm in ((1.0, quarters[0], "M_A"), (2.0, quarters[1], "M_B"),
                     (3.0, quarters[2], "M_C")):
        m = MUX * q
        cv.line((x, BASE_Y), (x, BASE_Y + m * BMD_SCALE), C["accent"], 1.6, dash="3 3")
        cv.dot((x, BASE_Y + m * BMD_SCALE), 4.6, fill="#FFFFFF", stroke=C["accent"], w=2.2)
        cv.math_px(cv.X(x), cv.Y(BASE_Y + m * BMD_SCALE) - 13, f"{m:.0f}", 12.5,
                   C["accent"], weight="700")
        cv.text_px(cv.X(x), cv.Y(BASE_Y) + 16, nm, 11.5, C["muted"])

    cv.text_px(PW2 / 2, PH2 - 78,
               f"C_b = 12.5({MUX:.0f}) ／ [2.5({MUX:.0f}) + 3({MUX*quarters[0]:.0f})"
               f" + 4({MUX*quarters[1]:.0f}) + 3({MUX*quarters[2]:.0f})]", 12, C["muted"])
    cv.text_px(PW2 / 2, PH2 - 54, f"C_b = {cbv:.3f}", 16, tag_col, weight="700")
    cv.text_px(PW2 / 2, PH2 - 28,
               f"φ_b M_{{nx}} = {phi_mnx:,.1f} kN-m　→　互制比 {ratio:.3f}", 13,
               tag_col, weight="700")
    return cv


def fig2_cb_reading():
    a = _panel_cb("（甲）均勻彎矩　← 主答", "「均佈」修飾「彎矩」；兩端施加等值同向端彎矩",
                  (1.0, 1.0, 1.0), CB_UNIFORM, PHI_MNX_A, RATIO_A, False, C["load"])
    b = _panel_cb("（乙）均佈載重之最大彎矩", "「均佈」慣用於載重；M_{ux} 為跨中最大值",
                  (0.75, 1.0, 0.75), CB_UDL, PHI_MNX_B, RATIO_B, True, C["muted"])
    compose([a, b],
            title="「均佈的雙向彎矩」怎麼讀，決定了彎矩修正係數——必須先畫彎矩圖再套四點求積式",
            sub="四點求積式只吃四分點的彎矩值：矩形彎矩圖三點全等於最大值（最不利），"
                "拋物線彎矩圖兩側四分點只剩最大值的四分之三",
            note=f"兩種解讀的互制比為 {RATIO_A:.3f} 與 {RATIO_B:.3f}，"
                 f"皆遠小於 1.0 ⇒ 結論一致「滿足設計要求」；考場作答時寫明所採解讀即可",
            path=f"{OUT}/{TAG}-fig-2-cb-reading.svg")
    return f"{OUT}/{TAG}-fig-2-cb-reading.svg"


# ══════════════════════════════════════════════════════════
# 圖 3：LTB 三分區與中間側撐的效益
# ══════════════════════════════════════════════════════════
def fig3_ltb_brace():
    W, HH = 940, 560
    OX, OY = 100, 92
    LMAX, MMAX = 7.0, 1400.0
    KX, KY = 106.0, 0.265

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=OY, bg="#FFFFFF")

    def P(l, m): return (l * KX, m * KY)

    def X(l): return cv.X(l * KX)

    def Y(m): return cv.Y(m * KY)

    cv.text_px(W / 2, 34, "L_b 是全梁長 4 m，不是一半——一支中間側撐就能回到全塑性",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"本題無側向中間支撐，兩端才有側撐 ⇒ L_b = 4 m 落在 L_p = {LP:.0f} 與 "
               f"L_r = {LR} m 之間（非彈性 LTB）", 13, C["muted"])

    for x0, x1, fill in ((0, LP, C["fill_m"]), (LP, LR, C["fill_t"]), (LR, LMAX, C["fill_c"])):
        cv.polygon([P(x0, 0), P(x1, 0), P(x1, MMAX), P(x0, MMAX)], fill)
    for xm, lab, col in ((LP / 2, "塑性", C["bmd"]), ((LP + LR) / 2, "非彈性 LTB", C["tension"]),
                         ((LR + LMAX) / 2, "彈性 LTB", C["compr"])):
        cv.text_px(X(xm), Y(90), lab, 13, col, weight="700")
    cv.text_px(X((LR + LMAX) / 2), Y(300), "題目未給 GJ、C_w", 11.5, C["compr"])
    cv.text_px(X((LR + LMAX) / 2), Y(190), "故本圖不外推", 11.5, C["compr"])

    for m in (400, 800, 1200):
        cv.line(P(0, m), P(LMAX, m), C["border"], 1.0)
        cv.math_px(X(0) - 12, Y(m), f"{m:,}", 12, C["muted"], "end")
    for l in (1, 2, 3, 4, 5, 6, 7):
        cv.line(P(l, 0), P(l, MMAX), C["border"], 1.0)
        cv.math_px(X(l), Y(0) + 20, f"{l}", 12, C["muted"])
    cv.arrow(P(0, 0), P(LMAX, 0), C["muted"], 1.8, 9)
    cv.arrow(P(0, 0), P(0, MMAX), C["muted"], 1.8, 9)
    cv.math_px(X(LMAX) - 26, Y(0) + 42, "L_b (m)", 14, C["muted"], "start")
    cv.text_px(X(0) - 14, Y(MMAX) - 8, "M_n（kN-m）", 13.5, C["muted"], "end")

    for m, lab, col in ((MP, f"M_p = {MP:,.1f}", C["bmd"]),
                        (MR, f"M_r = (F_y − F_r)S_x = {MR:,.1f}", C["muted"])):
        cv.line(P(0, m), P(LR, m), col, 1.6, dash="6 4")
        cv.text_px(X(0) + 8, Y(m) - 11, lab, 12, col, "start", weight="700")

    npt = 200
    for cbv, col, wid, dash in ((CB_UDL, C["muted"], 2.2, "5 4"), (CB_UNIFORM, C["deform"], 4.6, None)):
        pts = [P(LP + (LR - LP) * i / npt, mn_curve(LP + (LR - LP) * i / npt, cbv))
               for i in range(npt + 1)]
        pts = [P(0, min(cbv * MP, MP))] + pts
        cv.poly(pts, col, wid, dash=dash)

    for x in (LP, LR):
        cv.line(P(x, 0), P(x, MMAX), C["accent"], 2.0, dash="5 4")
    cv.math_px(X(LP) - 8, Y(1330), f"L_p = {LP:.0f} m", 12.5, C["accent"], "end", weight="700")
    cv.math_px(X(LR) + 8, Y(1330), f"L_r = {LR} m", 12.5, C["accent"], "start", weight="700")

    # 設計點 L_b = 4 m
    cv.line(P(LB, 0), P(LB, MNX_A), C["load"], 2.2)
    cv.dot(P(LB, MNX_A), 6.2, fill="#FFFFFF", stroke=C["load"], w=3.0)
    # 標註放在 M_r 水平線下方的空白帶，避免與曲線及 M_r 線打架
    cv.text_px(X(LB) - 16, Y(MNX_A) + 68, f"L_b = {LB:.0f} m（全梁長）", 13, C["load"],
               "end", weight="700")
    cv.math_px(X(LB) - 16, Y(MNX_A) + 89, f"M_{{nx}} = {MNX_A:,.1f}", 13, C["load"], "end",
               weight="700")
    cv.math_px(X(LB) - 16, Y(MNX_A) + 110, f"φ_b M_{{nx}} = {PHI_MNX_A:,.1f} kN-m", 13,
               C["load"], "end", weight="700")

    # L_b = 2 m：誤取一半，或真的加一支中間側撐
    cv.dot(P(LP, MP), 6.0, fill="#FFFFFF", stroke=C["bmd"], w=2.8)
    cv.text_px(X(LP) - 12, Y(MP) + 26, "若誤把 L_b 取成一半（2 m）", 12.5, C["bmd"],
               "end", weight="700")
    cv.text_px(X(LP) - 12, Y(MP) + 46, "或真的加一支中間側撐 ⇒ 達全塑性", 12.5, C["bmd"], "end")
    cv.math_px(X(LP) - 12, Y(MP) + 68, f"φ_b M_p = {PHI_MP:,.1f} kN-m", 13, C["bmd"],
               "end", weight="700")

    cv.rect_px(X(0.15), Y(560), 300, 66, "#FFFFFF", 10, C["border"], 1.2)
    cv.legend(X(0.15) + 16, Y(560) + 24,
              [(C["deform"], f"C_b = {CB_UNIFORM:.3f}（主答：均勻彎矩）"),
               (C["muted"], f"C_b = {CB_UDL:.3f}（另解：均佈載重）")], size=12, gap=21)

    cv.text_px(W / 2, HH - 40,
               f"一支中間側撐讓強軸強度由 {PHI_MNX_A:,.1f} 提升到 {PHI_MP:,.1f} kN-m"
               f"（＋{100*(PHI_MP/PHI_MNX_A-1):.1f}%），互制比由 {RATIO_A:.3f} 降到 "
               f"{RATIO_BRACED:.3f}", 13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               "這是 LTB 題型最重要的實務啟示：側撐位置比換大斷面便宜得多", 12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-3-ltb-brace.svg")
    return f"{OUT}/{TAG}-fig-3-ltb-brace.svg"


# ══════════════════════════════════════════════════════════
# 圖 4：雙向彎矩互制圖
# ══════════════════════════════════════════════════════════
def fig4_interaction():
    W, HH = 940, 560
    OX, OY = 105, 96
    XMAX, YMAX = 1250.0, 230.0
    KX, KY = 0.58, 1.62

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=OY, bg="#FFFFFF")

    def P(x, y): return (x * KX, y * KY)

    def X(x): return cv.X(x * KX)

    def Y(y): return cv.Y(y * KY)

    eqv_mx = MUY / PHI_MNY * PHI_MNX_A          # 弱軸用掉的裕度換算成等值強軸彎矩
    cv.text_px(W / 2, 34,
               f"雙向互制：{MUY:.0f} kN-m 的弱軸彎矩，吃掉的裕度和 {eqv_mx:.0f} kN-m 的"
               f"強軸彎矩一樣多", 16.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"φ_b M_ny = {PHI_MNY:.1f} kN-m 只有 φ_b M_nx = {PHI_MNX_A:.1f} 的 "
               f"{100*PHI_MNY/PHI_MNX_A:.0f}%——弱軸「單位彎矩的代價」高出 5.5 倍",
               13, C["muted"])

    for y in (50, 100, 150, 200):
        cv.line(P(0, y), P(XMAX, y), C["border"], 1.0)
        cv.math_px(X(0) - 12, Y(y), f"{y}", 12, C["muted"], "end")
    for x in (200, 400, 600, 800, 1000, 1200):
        cv.line(P(x, 0), P(x, YMAX), C["border"], 1.0)
        cv.math_px(X(x), Y(0) + 20, f"{x:,}", 12, C["muted"])
    cv.arrow(P(0, 0), P(XMAX, 0), C["muted"], 1.8, 9)
    cv.arrow(P(0, 0), P(0, YMAX), C["muted"], 1.8, 9)
    cv.math_px(X(XMAX) + 6, Y(0) + 22, "M_{ux} (kN-m)", 13.5, C["muted"], "start")
    cv.text_px(X(0) - 14, Y(YMAX) - 8, "M_{uy}（kN-m）", 13.5, C["muted"], "end")

    lines = [(PHI_MP, PHI_MNY, C["bmd"], "4 4", 2.2,
              f"加中間側撐（L_b = {LP:.0f} m）"),
             (PHI_MNX_B, PHI_MNY, C["muted"], "6 4", 2.2,
              f"另解 C_b = {CB_UDL:.3f}"),
             (PHI_MNX_A16, PHI_MNY_A16, C["compr"], "2 4", 2.0,
              "AISC 360-16／-22"),
             (PHI_MNX_A, PHI_MNY, C["load"], None, 4.4,
              f"主答 C_b = {CB_UNIFORM:.3f}")]
    for mx, my, col, dash, wid, _ in lines:
        cv.poly([P(mx, 0), P(0, my)], col, wid, dash=dash)

    # 設計點與兩個分項的貢獻
    cv.line(P(MUX, 0), P(MUX, MUY), C["accent"], 1.4, dash="3 3")
    cv.line(P(0, MUY), P(MUX, MUY), C["accent"], 1.4, dash="3 3")
    cv.dot(P(MUX, MUY), 7.0, fill="#FFFFFF", stroke=C["accent"], w=3.2)
    cv.math_px(X(MUX) + 14, Y(MUY) - 10, f"({MUX:.0f}, {MUY:.0f})", 14, C["accent"],
               "start", weight="700")
    cv.text_px(X(MUX) + 14, Y(MUY) + 12, "設計需求點", 12.5, C["accent"], "start", weight="700")

    cv.text_px(X(60), Y(100),
               f"強軸 {MUX:.0f}／{PHI_MNX_A:.1f} = {MUX/PHI_MNX_A:.3f}", 12.5,
               C["load"], "start", weight="700")
    cv.text_px(X(60), Y(84),
               f"弱軸 {MUY:.0f}／{PHI_MNY:.1f} = {MUY/PHI_MNY:.3f}", 12.5,
               C["tension"], "start", weight="700")
    cv.text_px(X(60), Y(66),
               f"合計 {RATIO_A:.3f} ≤ 1.0　✓ 滿足", 13.5, C["accent"], "start", weight="700")

    # 弱軸上限的三種取值：軸上只放色標（三者相差 3～13 kN-m，標籤放不下），文字集中成區塊
    caps = [(PHI * MNY_CAP16, C["muted"], f"1.6F_yS_y（AISC 360-10 起）→ {PHI*MNY_CAP16:.1f}"),
            (PHI * MNY_Z, C["compr"], f"F_yZ_y → {PHI*MNY_Z:.1f}"),
            (PHI * MNY_CAP15, C["load"], f"1.5F_yS_y（台灣 2010，本題控制）→ {PHI*MNY_CAP15:.1f}")]
    for m, col, _ in caps:
        cv.line((0.0, m * KY), (16.0, m * KY), col, 2.6)
    cv.text_px(X(215), Y(228), "弱軸強度上限的三種取值（kN-m）", 12, C["text"],
               "start", weight="700")
    for i, (m, col, lab) in enumerate(caps):
        yy = Y(210 - i * 17)
        cv.line((X(215) - cv.ox + 2, cv.h - yy - cv.oy), (X(215) - cv.ox + 24, cv.h - yy - cv.oy),
                col, 3.2)
        cv.text_px(X(215) + 32, yy, lab, 11.5, col, "start", weight="700")
    cv.line((16.0, PHI * MNY_Z * KY), (X(215) - cv.ox, (210 - 17) * KY), C["border"], 1.2)

    cv.rect_px(X(700), Y(215), 300, 92, "#FFFFFF", 10, C["border"], 1.2)
    cv.legend(X(700) + 16, Y(215) + 22,
              [(lines[3][2], lines[3][5]), (lines[1][2], lines[1][5]),
               (lines[2][2], lines[2][5]), (lines[0][2], lines[0][5])], size=11.5, gap=19)

    cv.text_px(W / 2, HH - 40,
               f"Z_y/S_y = {ZY/SY:.3f} 大於 1.5 ⇒ 弱軸由 1.5F_yS_y 上限控制"
               f"（{MNY_CAP15:.1f} 小於 F_yZ_y = {MNY_Z:.1f}）；漏掉這道上限會高估弱軸強度 4.7%",
               13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               "無軸力時 H1-1b 退化為線性互制式；規範中並無編號「H1-2」的式子",
               12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-4-interaction.svg")
    return f"{OUT}/{TAG}-fig-4-interaction.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_cb_reading, "§4 Step 2b·§5①",
     "不先判讀彎矩圖就假設 C_b（兩種題意解讀的四分點值完全不同）"),
    (fig3_ltb_brace, "§2 陷阱·§4 Step 2a·§5④",
     "把 L_b 誤取成梁長的一半（4 m → 2 m）而高估強度"),
    (fig4_interaction, "§4 Step 3～4·§6.3",
     "漏掉弱軸 1.5F_yS_y 上限，或以為弱軸彎矩小就可以忽略"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ref = [("M_p", MP, 1267.5), ("M_r", MR, 855.8), ("C_b 甲", CB_UNIFORM, 1.0),
           ("C_b 乙", CB_UDL, 1.136), ("中括號", BRACKET, 1050.8),
           ("φM_nx 甲", PHI_MNX_A, 945.8), ("φM_nx 乙", PHI_MNX_B, 1074.4),
           ("F_yZ_y", MNY_Z, 199.0), ("1.5F_yS_y", MNY_CAP15, 190.1),
           ("1.6F_yS_y", MNY_CAP16, 202.8), ("φM_ny", PHI_MNY, 171.1),
           ("互制 甲", RATIO_A, 0.715), ("互制 乙", RATIO_B, 0.664),
           ("φM_p", PHI_MP, 1140.8), ("互制 側撐", RATIO_BRACED, 0.643),
           ("M_r AISC", MR_A16, 770.9), ("φM_nx AISC", PHI_MNX_A16, 905.5),
           ("φM_ny AISC", PHI_MNY_A16, 179.1), ("互制 AISC", RATIO_A16, 0.721)]
    print("現算值 vs SS-2014-3.md 表列值：")
    for nm, got, want in ref:
        ok = "OK " if abs(got - want) <= max(abs(want) * 0.003, 0.05) else "!! "
        print(f"  {ok}{nm:<12} {got:>10,.4f}   （.md: {want:,}）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<40} {section:<22} 攔：{catches}")
