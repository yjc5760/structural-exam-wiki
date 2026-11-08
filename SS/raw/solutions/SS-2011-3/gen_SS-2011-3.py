#!/usr/bin/env python3
"""
SS-2011-3 H 型鋼梁側扭挫屈（LTB）— 解題圖解產生腳本

用法：
    python3 gen_SS-2011-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2011-3.md 哪一節
  2. L_p、L_r、M_n 全部由斷面尺寸與 X_1／X_2 現算（非寫死；2026-11-03 起
     以腹板淨高 40.62 為輸入，全深 d = 43.16），
     改一個 t_f 或 F_r，三分區的界線與曲線會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯

圖 1（fig1_problem，2026-11-03 追加）：題目附圖重繪。
  重繪依據：題目正本 SS-2011-3-problem.md §4 判讀清單（待確認）；只畫考卷給的東西，不含解題結果。
  斷面依題給尺寸按比例；立面與平面的跨度、彎矩符號大小、右上斷面方位小圖為示意。
  不重繪：第 3 頁參考公式（已照錄於 problem.md §2）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2011-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2011-3.md，勿手動改動）
# 2026-11-03 勘誤：圖上 40.62 為「腹板淨高」（尺寸線止於翼板內緣），全深 d = 43.16
# ══════════════════════════════════════════════════════════
# §1 材料與斷面
E, G = 2100.0, 840.0            # tf/cm^2
FY, FR = 2.52, 1.05             # tf/cm^2
H_W_GIVEN, BF, TF, TW = 40.62, 20.32, 1.27, 1.27    # cm（40.62＝腹板淨高）
LB = 812.8                      # cm　側向無支撐長度（＝全跨）
CB = 1.75                       # 端彎矩型，M_1/M_2 = 0


def section(h_w):
    """§4 Step 1～4：由腹板淨高 h_w 現算全部斷面性質與 L_p、L_r"""
    d = h_w + 2 * TF
    ho = d - TF
    a = 2 * BF * TF + h_w * TW
    ix = (BF * d ** 3 - (BF - TW) * h_w ** 3) / 12
    sx = ix / (d / 2)
    zx = BF * TF * ho + TW * h_w ** 2 / 4
    i_f = TF * BF ** 3 / 12
    iy = 2 * i_f + h_w * TW ** 3 / 12
    ry = math.sqrt(iy / a)
    j = (2 * BF * TF ** 3 + h_w * TW ** 3) / 3
    cw = i_f * ho ** 2 / 2
    x1 = math.pi / sx * math.sqrt(E * G * j * a / 2)
    x2 = 4 * cw / iy * (sx / (G * j)) ** 2
    lp = 80 * ry / math.sqrt(FY)
    lr = ry * x1 / (FY - FR) * math.sqrt(1 + math.sqrt(1 + x2 * (FY - FR) ** 2))
    return dict(d=d, ho=ho, A=a, Ix=ix, Sx=sx, Zx=zx, If=i_f, Iy=iy, ry=ry, J=j, Cw=cw,
                X1=x1, X2=x2, Lp=lp, Lr=lr, Mp=FY * zx, Mr=(FY - FR) * sx)


S = section(H_W_GIVEN)            # 主答（正確讀圖）
S_BAD = section(H_W_GIVEN - 2 * TF)   # 誤把 40.62 當全深（腹板淨高變 38.08）
D, H_W, HO = S["d"], H_W_GIVEN, S["ho"]          # 43.16、40.62、41.89
A, IX, SX, ZX = S["A"], S["Ix"], S["Sx"], S["Zx"]  # 103.20、29,742、1,378.2、1,604.9
IY, RY, J, IF_, CW = S["Iy"], S["ry"], S["J"], S["If"], S["Cw"]  # 1,782.9、4.156、55.48、887.96、779,084
X1, X2, LP, LR = S["X1"], S["X2"], S["Lp"], S["Lr"]  # 162.0、1.529、209.5、803.1
MP, MR = S["Mp"], S["Mr"]                           # 4,044.3、2,026.0
# §6 AISC 360-16／-22 對照
CB_A = 12.5 / 7.5                                            # 1.667
LP_A = 1.76 * RY * math.sqrt(E / FY)                         # 211.2 cm
RTS = math.sqrt(math.sqrt(IY * CW) / SX)                     # 5.200 cm
JC_SH = J * 1.0 / (SX * HO)                                  # 0.000961
MR_A = 0.7 * FY * SX                                         # 2,431.2 tf·cm
LR_A = (1.95 * RTS * E / (0.7 * FY) *
        math.sqrt(JC_SH + math.sqrt(JC_SH ** 2 + 6.76 * (0.7 * FY / E) ** 2)))   # 698.4 cm
_s = LB / RTS
FCR_A = CB_A * math.pi ** 2 * E / _s ** 2 * math.sqrt(1 + 0.078 * JC_SH * _s ** 2)
MN_A = min(FCR_A * SX, MP)                                   # 3,279 tf·cm（§6.3）


def mn_inelastic(lb, cb):
    return cb * (MP - (MP - MR) * (lb - LP) / (LR - LP))


def mn_elastic(lb, cb):
    s = lb / RY
    return cb * SX * X1 * math.sqrt(2) / s * math.sqrt(1 + X1 ** 2 * X2 / (2 * s ** 2))


def mn(lb, cb=CB):
    """§4 Step 6 之三分區標稱彎矩（上限截斷於 M_p）"""
    if lb <= LP:
        v = cb * MP
    elif lb <= LR:
        v = mn_inelastic(lb, cb)
    else:
        v = mn_elastic(lb, cb)
    return min(v, MP)


MN = mn(LB)                       # 3,489 tf·cm（§4 Step 6 主答，彈性式）
MN_CB1 = mn(LB, 1.0)              # 1,993.5 tf·cm（誤設 C_b = 1.0；即 M_o,cr）
MO_CR = (math.pi / LB * math.sqrt(E * IY * G * J) *
         math.sqrt(1 + (math.pi / LB) ** 2 * E * CW / (G * J)))   # 1,993.5（雙路徑）


def mn_bad(lb, cb=CB):
    """誤把 40.62 當全深時之 M_n（攔錯用）"""
    s = S_BAD
    if lb <= s["Lp"]:
        v = cb * s["Mp"]
    elif lb <= s["Lr"]:
        v = cb * (s["Mp"] - (s["Mp"] - s["Mr"]) * (lb - s["Lp"]) / (s["Lr"] - s["Lp"]))
    else:
        sl = lb / s["ry"]
        v = (cb * s["Sx"] * s["X1"] * math.sqrt(2) / sl *
             math.sqrt(1 + s["X1"] ** 2 * s["X2"] / (2 * sl ** 2)))
    return min(v, s["Mp"])


MN_BAD = mn_bad(LB)               # 3,378 tf·cm（非彈性，錯）


# C_b 放大後仍受 M_p 截斷，平台段的終點由「C_b·(非彈性式) = M_p」解出，非目測
LB_CAP_END = LP + (LR - LP) * (MP - MP / CB) / (MP - MR)


# ══════════════════════════════════════════════════════════
def fig2_ltb_curve():
    """M_n–L_b 三分區曲線：本題落在彈性區的最前端，只超出 L_r 9.7 cm"""
    W, HH = 1010, 600
    OX, OY = 105, 92
    LMAX, MMAX = 1300.0, 4600.0
    KX, KY = 0.615, 0.090          # px per cm / per tf·cm

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=OY, bg="#FFFFFF")

    def P(lb, m): return (lb * KX, m * KY)

    def X(lb): return cv.X(lb * KX)

    def Y(m): return cv.Y(m * KY)

    def path(f, lo, hi, n=300):
        return [P(lo + (hi - lo) * i / n, f(lo + (hi - lo) * i / n)) for i in range(n + 1)]

    cv.text_px(W / 2, 30, "側扭挫屈三分區：本題落在彈性區的最前端",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 54,
               f"40.62 是腹板淨高（全深 d = {D:.2f} cm）⇒ L_r = {LR:.1f} cm，"
               f"L_b = {LB} cm 只超出 {LB - LR:.1f} cm（{100*(LB-LR)/LR:.1f}%）", 13, C["muted"])

    # 三個分區的底色
    for x0, x1, fill in ((0, LP, C["fill_m"]), (LP, LR, C["fill_t"]), (LR, LMAX, C["fill_c"])):
        cv.polygon([P(x0, 0), P(x1, 0), P(x1, MMAX), P(x0, MMAX)], fill)
    for xm, lab, col in ((LP / 2, "塑性", C["bmd"]),
                         ((LP + LR) / 2, "非彈性 LTB", C["tension"]),
                         ((LR + LMAX) / 2, "彈性 LTB", C["compr"])):
        cv.text_px(X(xm), Y(300), lab, 13.5, col, weight="700")

    # 格線與座標軸
    for m in (1000, 2000, 3000, 4000):
        cv.line(P(0, m), P(LMAX, m), C["border"], 1.0)
        cv.math_px(X(0) - 12, Y(m), f"{m:,}", 12, C["muted"], "end")
    for lb in (200, 400, 600, 800, 1000, 1200):
        cv.line(P(lb, 0), P(lb, MMAX), C["border"], 1.0)
        cv.math_px(X(lb), Y(0) + 20, f"{lb}", 12, C["muted"])
    cv.arrow(P(0, 0), P(LMAX, 0), C["muted"], 1.8, 9)
    cv.arrow(P(0, 0), P(0, MMAX), C["muted"], 1.8, 9)
    cv.math_px(X(LMAX) + 4, Y(0) + 22, "L_b (cm)", 14, C["muted"], "start")
    cv.text_px(X(0) - 14, Y(MMAX) - 8, "M_n（tf·cm）", 13.5, C["muted"], "end")

    # M_p 與 M_r 水平參考線
    cv.line(P(0, MP), P(LMAX, MP), C["bmd"], 1.6, dash="6 4")
    cv.text_px(X(0) + 8, Y(MP) - 11, f"M_p = {MP:,.1f}", 12, C["bmd"], "start", weight="700")
    cv.line(P(0, MR), P(LMAX, MR), C["muted"], 1.6, dash="6 4")
    cv.text_px(X(LP) + 8, Y(MR) - 11, f"M_r = (F_y − F_r)S_x = {MR:,.1f}", 12,
               C["muted"], "start", weight="700")

    # 曲線：C_b = 1.0 對照、本題主曲線
    cv.poly(path(lambda l: mn(l, 1.0), 1.0, LMAX), C["muted"], 2.2, dash="5 4")
    cv.poly(path(mn, 1.0, LMAX, 600), C["deform"], 4.8)

    # 分區界線（含誤讀時的 L_r）
    for x in (LP, LR):
        cv.line(P(x, 0), P(x, MMAX), C["accent"], 2.0, dash="5 4")
    cv.text_px(X(LP) + 8, Y(1600), f"L_p = {LP:.1f} cm", 12.5, C["accent"], "start",
               weight="700")
    lr_bad = S_BAD["Lr"]
    cv.line(P(lr_bad, 0), P(lr_bad, MMAX), C["tension"], 1.6, dash="2 4")

    # L_r、L_b、誤讀 L_r 三條線靠得很近 —— 以引線拉到右上空白處說明
    cv.line(P((LB + LR) / 2, 4400), P(900, 4400), C["accent"], 1.2)
    cv.text_px(X(906), Y(4400) - 9, f"L_b = {LB} > L_r = {LR:.1f} cm",
               12.5, C["accent"], "start", weight="700")
    cv.text_px(X(906), Y(4400) + 11, f"只超出 {LB - LR:.1f} cm（{100*(LB-LR)/LR:.1f}%）⇒ 彈性",
               12, C["accent"], "start")
    cv.line(P(lr_bad, 700), P(900, 700), C["tension"], 1.2)
    cv.text_px(X(906), Y(700) - 9, f"誤把 40.62 當全深：L_r = {lr_bad:.1f} cm",
               12, C["tension"], "start", weight="700")
    cv.text_px(X(906), Y(700) + 11, f"⇒ 誤判非彈性，M_n = {MN_BAD:,.0f} tf·cm",
               12, C["tension"], "start")

    # 設計點
    cv.line(P(LB, 0), P(LB, MN), C["load"], 2.2)
    cv.dot(P(LB, MN), 6.2, fill="#FFFFFF", stroke=C["load"], w=3.0)
    cv.text_px(X(LR) - 26, Y(MN) + 22, f"L_b = {LB} cm ⇒ 彈性 LTB", 12.5,
               C["load"], "end", weight="700")
    cv.math_px(X(LR) - 26, Y(MN) + 43, f"M_n = {MN:,.0f} tf·cm", 14.5, C["load"],
               "end", weight="700")

    # C_b 誤設 1.0
    cv.dot(P(LB, MN_CB1), 5.4, fill="#FFFFFF", stroke=C["muted"], w=2.6)
    cv.text_px(X(LR) - 26, Y(MN_CB1) + 22, f"C_b 誤設 1.0 → 只剩 {MN_CB1:,.1f} tf·cm",
               12.5, C["muted"], "end", weight="700")

    # C_b 放大造成的 M_p 平台段（含中文，必須用 text_px）
    cv.dot(P(LB_CAP_END, MP), 5.0, fill="#FFFFFF", stroke=C["deform"], w=2.4)
    cv.text_px(X(LB_CAP_END) - 10, Y(MP) + 24,
               f"C_b = {CB} 放大後，L_b ≤ {LB_CAP_END:.0f} cm 仍被 M_p 截斷", 12,
               C["deform"], "end", weight="700")

    # 圖例放左下空白區
    cv.rect_px(X(250), Y(1450), 330, 86, "#FFFFFF", 10, C["border"], 1.2)
    cv.legend(X(250) + 16, Y(1450) + 24,
              [(C["deform"], f"本題 C_b = {CB}（含 M_p 上限截斷）"),
               (C["muted"], "若誤設 C_b = 1.0"),
               (C["tension"], "誤把 40.62 當全深時的 L_r")], size=12, gap=21)

    cv.text_px(W / 2, HH - 40,
               f"雙路徑驗算：彈性 X_1–X_2 式 = C_b·M_o,cr = {CB} × {MO_CR:,.1f} = {MN:,.1f} tf·cm；"
               f"於 L_r 處兩式相接（C_b·M_r = {CB*MR:,.1f}）",
               13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               f"M_n/S_x = {MN/SX:.2f} tf/cm² > F_y − F_r：A 端外緣已達降伏；"
               "「彈性」指以 C_b = 1 定義的挫屈分區", 12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-2-ltb-zones.svg")
    return f"{OUT}/{TAG}-fig-2-ltb-zones.svg"


# ══════════════════════════════════════════════════════════
def fig3_code_flip():
    """兩套規範皆判彈性；誤讀斷面才會翻成非彈性"""
    W, HH = 1010, 520
    OX = 100
    LMAX, KX = 1100.0, 0.55
    BAR_W = LMAX * KX
    ROW_H, BAR_H = 118, 46
    ROW0 = 124

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=0, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "兩套規範都判彈性；把腹板淨高讀成全深才會翻成非彈性",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"AISC 的 L_r 短 {100*(1-LR_A/LR):.1f}%：轉折彎矩 "
               f"(F_y−F_r)S_x = {MR:,.0f} → 0.7F_yS_x = {MR_A:,.0f} tf·cm（提高 20%）",
               13, C["muted"])

    rows = [("台灣 2010 規範（＝本卷公式表，主答）", LP, LR, C["compr"], "彈性 LTB",
             f"C_b = {CB}　M_n = {MN:,.0f} tf·cm"),
            ("AISC 360-16／-22 §F2", LP_A, LR_A, C["compr"], "彈性 LTB",
             f"C_b = {CB_A:.3f}　M_n = {MN_A:,.0f} tf·cm"),
            ("台灣 2010，誤把 40.62 當全深（錯）", S_BAD["Lp"], S_BAD["Lr"], C["tension"],
             "非彈性 LTB（錯）", f"M_n = {MN_BAD:,.0f} tf·cm")]

    x_lb = OX + LB * KX
    for i, (name, lp, lr, mkcol, zone, res) in enumerate(rows):
        ytop = ROW0 + i * ROW_H
        cv.text_px(OX, ytop - 12, name, 14, C["text"], "start", weight="700")
        for x0, x1, fill in ((0, lp, C["fill_m"]), (lp, lr, C["fill_t"]), (lr, LMAX, C["fill_c"])):
            cv.rect_px(OX + x0 * KX, ytop, (x1 - x0) * KX, BAR_H, fill, 0)
        cv.rect_px(OX, ytop, BAR_W, BAR_H, "none", 0, C["border"], 1.2)
        for x, lab in ((lp, f"L_p = {lp:.1f}"), (lr, f"L_r = {lr:.1f}")):
            px = OX + x * KX
            cv.parts.append(f'<line x1="{px:.2f}" y1="{ytop}" x2="{px:.2f}" '
                            f'y2="{ytop + BAR_H}" stroke="{C["accent"]}" stroke-width="2.2"/>')
            if abs(px - x_lb) < 46:
                anchor_left = x < LB
                cv.math_px(px - 10 if anchor_left else px + 10, ytop + BAR_H + 16, lab, 12,
                           C["accent"], "end" if anchor_left else "start", weight="700")
            else:
                cv.math_px(px, ytop + BAR_H + 16, lab, 12, C["accent"], weight="700")
        for xm, lab, col in ((lp / 2, "塑性", C["bmd"]),
                             ((lp + lr) / 2, "非彈性", C["tension"]),
                             ((lr + LMAX) / 2, "彈性", C["compr"])):
            cv.text_px(OX + xm * KX, ytop + BAR_H / 2, lab, 12.5, col, weight="700")
        cv.text_px(OX + BAR_W + 16, ytop + BAR_H / 2 - 11, zone, 14.5, mkcol,
                   "start", weight="700")
        cv.text_px(OX + BAR_W + 16, ytop + BAR_H / 2 + 12, res, 12, C["muted"], "start")

    # L_b 貫穿三列
    y0, y1 = ROW0 - 28, ROW0 + 2 * ROW_H + BAR_H + 30
    cv.parts.append(f'<line x1="{x_lb:.2f}" y1="{y0}" x2="{x_lb:.2f}" y2="{y1}" '
                    f'stroke="{C["load"]}" stroke-width="2.6" stroke-dasharray="6 4"/>')
    cv.text_px(x_lb, y0 - 11, f"L_b = {LB} cm", 14, C["load"], weight="700")

    cv.text_px(W / 2, HH - 44,
               f"台灣 2010 版 L_b 只超出 L_r {100*(LB-LR)/LR:.1f}%，AISC 版超出 {100*(LB-LR_A)/LR_A:.0f}%"
               "——分區相同，但台灣版貼著邊界，讀錯尺寸就翻轉",
               13.5, C["text"], weight="700")
    cv.text_px(W / 2, HH - 20,
               "本卷第三頁已印出 X_1／X_2 舊式公式並要求依 2010 規範作答 ⇒ 主答「彈性」，"
               "新規範對照屬加分而非替代", 12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-3-code-flip.svg")
    return f"{OUT}/{TAG}-fig-3-code-flip.svg"


# ══════════════════════════════════════════════════════════
# 圖 1：題目附圖重繪（依題目正本 SS-2011-3-problem.md §4 判讀清單，待確認）
# 只畫考卷給的東西，與上方解題常數分開；不含任何解題結果（不標 C_b、L_p、L_r、M_n）
# ══════════════════════════════════════════════════════════
Q_L = 812.8                 # 題文 L = 812.8 cm
Q_SUP_A, Q_SUP_B = "roller", "pin"   # #1 A 滾支、B 鉸支；平面 A、B 兩端兩側側撐、無中間側撐
#                             #2 只有 A 端彎矩 M（方向照考卷附圖：順時針）
Q_BF = 20.32                # 圖面 翼寬 20.32 cm
Q_TF = 1.27                 # 圖面 t_f = 1.27 cm（上下）
Q_TW = 1.27                 # 圖面 t_w = 1.27 cm
Q_HW = 40.62                # #4 40.62 為腹板淨高（尺寸線止於上下翼板內側面）
Q_D = Q_HW + 2 * Q_TF       # 全深（推得值 43.16 cm，圖上不標）
Q_PW, Q_PH = 600, 560


def _q_ibeam(cv, x0, y0, k, lw=1.5):
    """以 (x0, y0) 為形心畫 I 斷面；k = 每 cm 對應的模型長度"""
    bf, d, tf, tw = Q_BF * k, Q_D * k, Q_TF * k, Q_TW * k
    for xa, xb, ya, yb in ((-bf / 2, bf / 2, d / 2 - tf, d / 2), (-bf / 2, bf / 2, -d / 2, -d / 2 + tf),
                           (-tw / 2, tw / 2, -d / 2 + tf, d / 2 - tf)):
        cv.polygon([(x0 + xa, y0 + ya), (x0 + xb, y0 + ya), (x0 + xb, y0 + yb), (x0 + xa, y0 + yb)],
                   C["fill_c"], C["member"], lw)
    return bf / 2, d / 2


def _q_beam():
    sx = 400 / Q_L
    cv = Canvas(Q_PW, Q_PH, sx=sx, ox=80, oy=0)
    cv.panel("立面與平面", "跨長示意；A 端受彎矩 M")
    # ── 立面（梁軸 y = ye）
    ye = (Q_PH - 170) / sx
    cv.line((0, ye), (Q_L, ye), C["member"], 4.5, cap="butt")
    cv.support((0, ye), Q_SUP_A, 0, size=13)
    cv.support((Q_L, ye), Q_SUP_B, 0, size=13)
    cv.moment_arrow((0, ye), r=24, ccw=False, color=C["load"], w=2.6, span=200, start=200)
    cv.math((0, ye), "M", 17, C["load"], "end", dx=-30, dy=-20, weight="700")
    cv.text((0, ye), "A", 15, C["text"], "start", dx=28, dy=-14, weight="700")
    cv.text((Q_L, ye), "B", 15, C["text"], dy=-22, weight="700")
    cv.arrow((Q_L + 18, ye), (Q_L + 80, ye), C["text"], 1.6, 8)
    cv.math((Q_L + 80, ye), "z", 15, C["text"], "start", dx=6)
    cv.arrow((-40, ye - 40), (-40, ye - 110), C["text"], 1.6, 8)
    cv.math((-40, ye - 110), "y", 15, C["text"], "end", dx=-6, dy=4)
    cv.dim((0, ye), (Q_L, ye), "L", off=48, label_off=14)
    # 右上斷面方位小圖（x 向左、y 向下）
    sxo, syo = Q_L + 130, ye + 150
    hb, hd = _q_ibeam(cv, sxo, syo, 1.5, 1.2)
    cv.arrow((sxo, syo), (sxo - hb - 40, syo), C["text"], 1.6, 8)
    cv.math((sxo - hb - 40, syo), "x", 15, C["text"], "end", dx=-6)
    cv.arrow((sxo, syo), (sxo, syo - hd - 40), C["text"], 1.6, 8)
    cv.math((sxo, syo - hd - 40), "y", 15, C["text"], dy=14)
    # ── 平面（梁軸 y = yp）
    yp = (Q_PH - 400) / sx
    cv.line((0, yp), (Q_L, yp), C["member"], 4.5, cap="butt")
    for x, nm in ((0, "A"), (Q_L, "B")):
        cv.support((x, yp), "roller", 0, size=11)
        cv.support((x, yp), "roller", 180, size=11)
        cv.text((x, yp), nm, 15, C["text"], dy=-50, weight="700")
    cv.arrow((Q_L + 30, yp), (Q_L + 92, yp), C["text"], 1.6, 8)
    cv.math((Q_L + 92, yp), "z", 15, C["text"], "start", dx=6)
    cv.arrow((-40, yp - 20), (-40, yp - 95), C["text"], 1.6, 8)
    cv.math((-40, yp - 95), "x", 15, C["text"], "end", dx=-6, dy=4)
    cv.text((Q_L / 2, yp), "平面：A、B 兩端兩側側撐，中間無側撐", 12.5, C["muted"], dy=-40)
    return cv


def _q_section():
    sx = 7.0
    cv = Canvas(Q_PW, Q_PH, sx=sx, ox=Q_PW / 2 - 40, oy=Q_PH / 2 - Q_D / 2 * sx - 40)
    cv.panel("斷面尺寸", "依比例；單位：cm")
    _q_ibeam(cv, 0, Q_D / 2, 1.0, 1.8)
    top, bot = Q_D, 0.0
    cv.dim((-Q_BF / 2, top), (Q_BF / 2, top), f"{Q_BF}", off=-30, label_off=-14)
    cv.dim((-Q_BF / 2, top - Q_TF), (-Q_BF / 2, bot + Q_TF), f"{Q_HW}", off=40, label_off=30,
           color=C["accent"])
    cv.math((Q_BF / 2, top - Q_TF / 2), "t_{f} = 1.27", 15, C["text"], "start", dx=10)
    cv.math((Q_TW / 2, Q_D / 2), "t_{w} = 1.27", 15, C["text"], "start", dx=12)
    cv.math((Q_BF / 2, bot + Q_TF / 2), "t_{f} = 1.27", 15, C["text"], "start", dx=10)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([_q_beam(), _q_section()], cols=2,
            title="SS-2011-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；只畫考卷所給條件（L = 812.8 cm 取自題文）",
            note="40.62 的尺寸線止於上下翼板內側面：是腹板淨高，不是全深",
            path=path)
    return path


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 40.62 讀成全深；A、B 支承或彎矩作用端讀反；平面圖誤以為有中間側撐"),
    (fig2_ltb_curve, "§4 Step 4～6·§5",
     "把腹板淨高 40.62 讀成全深（L_r 變 833.2 而誤判非彈性、M_n 3,378），或 C_b 直接取 1.0"),
    (fig3_code_flip, "§6.2·§6.4",
     "把腹板淨高讀成全深而把分區翻成非彈性；拿 AISC 的 L_r 配本卷舊式公式"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ref = [("d", D, 43.16), ("A", A, 103.20), ("I_x", IX, 29742), ("S_x", SX, 1378.2),
           ("Z_x", ZX, 1604.9), ("I_y", IY, 1782.9), ("r_y", RY, 4.156), ("J", J, 55.48),
           ("I_f", IF_, 887.96), ("C_W", CW, 779084), ("M_p", MP, 4044.3), ("M_r", MR, 2026.0),
           ("X_1", X1, 162.0), ("X_2", X2, 1.529), ("L_p", LP, 209.5), ("L_r", LR, 803.1),
           ("M_n", MN, 3489), ("M_o,cr", MO_CR, 1993.5), ("M_n(誤讀)", MN_BAD, 3378),
           ("L_r(誤讀)", S_BAD["Lr"], 833.2),
           ("L_p(AISC)", LP_A, 211.2), ("r_ts", RTS, 5.200), ("L_r(AISC)", LR_A, 698.4),
           ("M_r(AISC)", MR_A, 2431.2), ("M_n(AISC)", MN_A, 3279)]
    print("現算值 vs SS-2011-3.md 表列值：")
    for nm, got, want in ref:
        ok = "OK " if abs(got - want) <= max(abs(want) * 0.002, 0.05) else "!! "
        print(f"  {ok}{nm:<11} {got:>12,.4g}   （.md: {want:,}）")
    print(f"\nM_p 平台段終點 L_b = {LB_CAP_END:.1f} cm；"
          f"雙路徑 C_b·M_o,cr = {CB*MO_CR:,.1f} vs X1X2 式 {MN:,.1f}")
    for fn, section_, catches in FIGURES:
        print(f"{os.path.basename(fn()):<42} {section_:<18} 攔：{catches}")
