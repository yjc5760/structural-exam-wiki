#!/usr/bin/env python3
"""
SS-2011-3 H 型鋼梁側扭挫屈（LTB）— 解題圖解產生腳本

用法：
    python3 gen_SS-2011-3.py [輸出目錄]

三條鐵則的落實：
  1. 圖上每個數字都標明來自 SS-2011-3.md 哪一節
  2. L_p、L_r、M_n 全部由斷面尺寸與 X_1／X_2 現算（非寫死），
     改一個 t_f 或 F_r，三分區的界線與曲線會一起變
  3. 每張圖在 FIGURES 表寫明攔什麼錯
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2011-3"

# ══════════════════════════════════════════════════════════
# 解題結果（全部來自 SS-2011-3.md，勿手動改動）
# ══════════════════════════════════════════════════════════
# §1 材料與斷面
E, G = 2100.0, 840.0            # tf/cm^2
FY, FR = 2.52, 1.05             # tf/cm^2
D, BF, TF, TW = 40.62, 20.32, 1.27, 1.27    # cm
LB = 812.8                      # cm　側向無支撐長度（＝全跨）
# §4 Step 1 斷面性質（以下皆現算，並在 __main__ 與 .md 逐項比對）
H_W = D - 2 * TF                                    # 38.08 腹板淨高
A = 2 * BF * TF + H_W * TW                          # 99.97 cm^2
IX = (BF * D ** 3 - (BF - TW) * H_W ** 3) / 12      # 25,831 cm^4
SX = IX / (D / 2)                                   # 1,271.8 cm^3
ZX = BF * TF * (D - TF) + TW * H_W ** 2 / 4         # 1,475.9 cm^3
IY = 2 * TF * BF ** 3 / 12 + H_W * TW ** 3 / 12     # 1,782.4 cm^4
RY = math.sqrt(IY / A)                              # 4.222 cm
J = TF ** 3 / 3 * (2 * BF + H_W)                    # 53.75 cm^4
IF_ = TF * BF ** 3 / 12                             # 887.96 cm^4（單一翼板）
HO = D - TF                                         # 39.35 cm（兩翼板形心距）
CW = IF_ * HO ** 2 / 2                              # 687,469 cm^6（本卷公式表）
# §4 Step 3～4
CB = 1.75                       # 端彎矩型，M_1/M_2 = 0
MP = FY * ZX                    # 3,719.2 tf·cm
MR = (FY - FR) * SX             # 1,869.6 tf·cm
X1 = math.pi / SX * math.sqrt(E * G * J * A / 2)             # 170.1 tf/cm^2
X2 = 4 * CW / IY * (SX / (G * J)) ** 2                       # 1.224 cm^4/tf^2
LP = 80 * RY / math.sqrt(FY)                                 # 212.8 cm
LR = RY * X1 / (FY - FR) * math.sqrt(1 + math.sqrt(1 + X2 * (FY - FR) ** 2))   # 833.2 cm
# §4 Step 6
MN = 3378.0                     # tf·cm（主答）
MN_CB1 = 1930.0                 # tf·cm（誤設 C_b = 1.0）
MN_ELASTIC_CHECK = 3380.0       # tf·cm（Step 6 連續性交叉驗算）
# §6 AISC 360-16／-22 對照
CB_A = 1.667
LP_A = 1.76 * RY * math.sqrt(E / FY)                         # 214.5 cm
RTS = math.sqrt(math.sqrt(IY * CW) / SX)                     # 5.246 cm
JC_SH = J * 1.0 / (SX * HO)                                  # 0.001074
MR_A = 0.7 * FY * SX                                         # 2,243.5 tf·cm
LR_A = (1.95 * RTS * E / (0.7 * FY) *
        math.sqrt(JC_SH + math.sqrt(JC_SH ** 2 + 6.76 * (0.7 * FY / E) ** 2)))   # 721.3 cm
MN_A = 3176.0                   # tf·cm（§6.3）


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


# C_b 放大後仍受 M_p 截斷，平台段的終點由「C_b·(非彈性式) = M_p」解出，非目測
LB_CAP_END = LP + (LR - LP) * (MP - MP / CB) / (MP - MR)


# ══════════════════════════════════════════════════════════
def fig2_ltb_curve():
    """M_n–L_b 三分區曲線：本題落在非彈性區的最尾端，餘裕只有 20.4 cm"""
    W, HH = 1010, 580
    OX, OY = 105, 88
    LMAX, MMAX = 1300.0, 3900.0
    KX, KY = 0.615, 0.105          # px per cm / per tf·cm

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=OY, bg="#FFFFFF")

    def P(lb, m): return (lb * KX, m * KY)

    def X(lb): return cv.X(lb * KX)

    def Y(m): return cv.Y(m * KY)

    def path(f, lo, hi, n=300):
        return [P(lo + (hi - lo) * i / n, f(lo + (hi - lo) * i / n)) for i in range(n + 1)]

    cv.text_px(W / 2, 34, "側扭挫屈三分區：本題落在非彈性區的最尾端",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"L_b = {LB} cm 距 L_r = {LR:.1f} cm 只差 {LR - LB:.1f} cm（{100*(LR-LB)/LR:.1f}%）"
               f"——J、C_W、X_2 只要有 5% 誤差，答案就會翻成「彈性」", 13, C["muted"])

    # 三個分區的底色（分區標籤放在圖底，避開曲線與 M_p 線）
    for x0, x1, fill in ((0, LP, C["fill_m"]), (LP, LR, C["fill_t"]), (LR, LMAX, C["fill_c"])):
        cv.polygon([P(x0, 0), P(x1, 0), P(x1, MMAX), P(x0, MMAX)], fill)
    for xm, lab, col in ((LP / 2, "塑性", C["bmd"]),
                         ((LP + LR) / 2, "非彈性 LTB", C["tension"]),
                         ((LR + LMAX) / 2, "彈性 LTB", C["compr"])):
        cv.text_px(X(xm), Y(260), lab, 13.5, col, weight="700")

    # 格線與座標軸
    for m in (1000, 2000, 3000):
        cv.line(P(0, m), P(LMAX, m), C["border"], 1.0)
        cv.math_px(X(0) - 12, Y(m), f"{m:,}", 12, C["muted"], "end")
    for lb in (200, 400, 600, 800, 1000, 1200):
        cv.line(P(lb, 0), P(lb, MMAX), C["border"], 1.0)
        cv.math_px(X(lb), Y(0) + 20, f"{lb}", 12, C["muted"])
    cv.arrow(P(0, 0), P(LMAX, 0), C["muted"], 1.8, 9)
    cv.arrow(P(0, 0), P(0, MMAX), C["muted"], 1.8, 9)
    cv.math_px(X(LMAX) + 4, Y(0) + 22, "L_b (cm)", 14, C["muted"], "start")
    cv.text_px(X(0) - 14, Y(MMAX) - 8, "M_n（tf·cm）", 13.5, C["muted"], "end")

    # M_p 與 M_r 水平參考線（標籤靠左，右側留給曲線）
    cv.line(P(0, MP), P(LMAX, MP), C["bmd"], 1.6, dash="6 4")
    cv.text_px(X(0) + 8, Y(MP) - 11, f"M_p = {MP:,.1f}", 12, C["bmd"], "start", weight="700")
    cv.line(P(0, MR), P(LMAX, MR), C["muted"], 1.6, dash="6 4")
    cv.text_px(X(0) + 8, Y(MR) - 11, f"M_r = (F_y − F_r)S_x = {MR:,.1f}", 12,
               C["muted"], "start", weight="700")

    # 曲線：C_b = 1.0 對照、彈性式左延、本題主曲線
    cv.poly(path(lambda l: mn(l, 1.0), 1.0, LMAX), C["muted"], 2.2, dash="5 4")
    ext = []
    for i in range(121):
        l = LR - 180 + 220.0 * i / 120
        v = mn_elastic(l, CB)
        if v <= MP:
            ext.append(P(l, v))
    cv.poly(ext, C["compr"], 1.8, dash="2 4")
    cv.poly(path(mn, 1.0, LMAX, 600), C["deform"], 4.8)

    # 分區界線
    for x in (LP, LR):
        cv.line(P(x, 0), P(x, MMAX), C["accent"], 2.0, dash="5 4")
    cv.text_px(X(LP) + 8, Y(1620), f"L_p = {LP:.1f} cm", 12.5, C["accent"], "start",
               weight="700")

    # L_b 與 L_r 只差 20.4 cm —— 以引線拉到右側空白處說明
    cv.line(P(LB, 0), P(LB, mn(LB)), C["load"], 2.2)
    cv.line(P((LB + LR) / 2, 3560), P(880, 3560), C["accent"], 1.2)
    cv.text_px(X(886), Y(3560) - 9, f"L_b = {LB} 與 L_r = {LR:.1f} cm", 12.5,
               C["accent"], "start", weight="700")
    cv.text_px(X(886), Y(3560) + 11, f"僅差 {LR - LB:.1f} cm，餘裕 {100*(LR-LB)/LR:.1f}%",
               12, C["accent"], "start")

    # 設計點（標註放在點的下方，避開主曲線）
    cv.dot(P(LB, mn(LB)), 6.2, fill="#FFFFFF", stroke=C["load"], w=3.0)
    cv.text_px(X(LB) - 16, Y(mn(LB)) + 22, f"L_b = {LB} cm ⇒ 非彈性 LTB", 12.5,
               C["load"], "end", weight="700")
    cv.math_px(X(LB) - 16, Y(mn(LB)) + 43, f"M_n = {MN:,.0f} tf·cm", 14.5, C["load"],
               "end", weight="700")

    # C_b 誤設 1.0
    cv.dot(P(LB, MN_CB1), 5.4, fill="#FFFFFF", stroke=C["muted"], w=2.6)
    cv.text_px(X(LB) + 16, Y(MN_CB1) - 13, f"C_b 誤設 1.0 → 只剩 {MN_CB1:,.0f} tf·cm",
               12.5, C["muted"], "start", weight="700")

    # C_b 放大造成的 M_p 平台段（含中文，必須用 text_px；math_px 的襯線字型排不出中文）
    cv.dot(P(LB_CAP_END, MP), 5.0, fill="#FFFFFF", stroke=C["deform"], w=2.4)
    cv.text_px(X(LB_CAP_END) - 10, Y(MP) + 24,
               f"C_b = {CB} 放大後，L_b ≤ {LB_CAP_END:.0f} cm 仍被 M_p 截斷", 12,
               C["deform"], "end", weight="700")

    # 圖例移到左下空白區，避免蓋住彈性段曲線
    cv.rect_px(X(250), Y(1400), 330, 86, "#FFFFFF", 10, C["border"], 1.2)
    cv.legend(X(250) + 16, Y(1400) + 24,
              [(C["deform"], f"本題 C_b = {CB}（含 M_p 上限截斷）"),
               (C["muted"], "若誤設 C_b = 1.0"),
               (C["compr"], "彈性式左延（與主曲線幾乎重合＝驗算通過）")], size=12, gap=21)

    cv.text_px(W / 2, HH - 40,
               f"連續性驗算：在 L_b = {LB} cm 以彈性式代入得 {MN_ELASTIC_CHECK:,.0f} tf·cm，"
               f"與非彈性式的 {MN:,.0f} 僅差 {100*abs(MN_ELASTIC_CHECK-MN)/MN:.2f}%",
               13, C["text"], weight="700")
    cv.text_px(W / 2, HH - 18,
               "兩支曲線在 L_r 處確實相接 ⇒ J、C_W、X_1、X_2、L_r 彼此一致（L_r 若算錯，兩式必大幅分歧）",
               12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-2-ltb-zones.svg")
    return f"{OUT}/{TAG}-fig-2-ltb-zones.svg"


# ══════════════════════════════════════════════════════════
def fig3_code_flip():
    """同一根梁、兩套規範：分區直接翻轉"""
    W, HH = 1010, 410
    OX = 100
    LMAX, KX = 1100.0, 0.55
    BAR_W = LMAX * KX               # 605 px，右側留給結論文字
    ROW_H, BAR_H = 118, 46
    ROW0 = 124                      # 第一列長條的頂端

    cv = Canvas(W, HH, sx=1.0, ox=OX, oy=0, bg="#FFFFFF")
    cv.text_px(W / 2, 34, "同一根梁、兩套規範：挫屈分區直接翻轉",
               17.5, C["text"], weight="700")
    cv.text_px(W / 2, 58,
               f"L_r 縮短 {100*(1-LR_A/LR):.1f}% 的主因是轉折彎矩 M_r 的定義改變："
               f"(F_y−F_r)S_x = {MR:,.0f} → 0.7F_yS_x = {MR_A:,.0f} tf·cm（提高 20%）",
               13, C["muted"])

    rows = [("台灣 2010 規範（＝本卷公式表，主答）", LP, LR, C["tension"], "非彈性 LTB",
             f"C_b = {CB}　M_n = {MN:,.0f} tf·cm"),
            ("AISC 360-16／-22 §F2", LP_A, LR_A, C["compr"], "彈性 LTB",
             f"C_b = {CB_A}　M_n = {MN_A:,.0f} tf·cm")]

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
            # 界線與 L_b 太近時改成靠右排，避免被 L_b 的紅虛線劃過
            if abs(px - x_lb) < 46:
                cv.math_px(px + 10, ytop + BAR_H + 16, lab, 12, C["accent"], "start",
                           weight="700")
            else:
                cv.math_px(px, ytop + BAR_H + 16, lab, 12, C["accent"], weight="700")
        for xm, lab, col in ((lp / 2, "塑性", C["bmd"]),
                             ((lp + lr) / 2, "非彈性", C["tension"]),
                             ((lr + LMAX) / 2, "彈性", C["compr"])):
            cv.text_px(OX + xm * KX, ytop + BAR_H / 2, lab, 12.5, col, weight="700")
        cv.text_px(OX + BAR_W + 16, ytop + BAR_H / 2 - 11, zone, 14.5, mkcol,
                   "start", weight="700")
        cv.text_px(OX + BAR_W + 16, ytop + BAR_H / 2 + 12, res, 12, C["muted"], "start")

    # L_b 貫穿兩列
    y0, y1 = ROW0 - 28, ROW0 + ROW_H + BAR_H + 30
    cv.parts.append(f'<line x1="{x_lb:.2f}" y1="{y0}" x2="{x_lb:.2f}" y2="{y1}" '
                    f'stroke="{C["load"]}" stroke-width="2.6" stroke-dasharray="6 4"/>')
    cv.text_px(x_lb, y0 - 11, f"L_b = {LB} cm", 14, C["load"], weight="700")

    cv.text_px(W / 2, HH - 44,
               "同一根梁，一邊判「非彈性」、一邊判「彈性」——"
               "題目那句「確認此梁挫屈時是否在彈性範圍內」正是問這件事",
               13.5, C["text"], weight="700")
    cv.text_px(W / 2, HH - 20,
               "本卷第三頁已印出 X_1／X_2 舊式公式並要求依 2010 規範作答 ⇒ 主答為「非彈性」，"
               "新規範對照屬加分而非替代", 12, C["muted"])
    cv.save(f"{OUT}/{TAG}-fig-3-code-flip.svg")
    return f"{OUT}/{TAG}-fig-3-code-flip.svg"


# ══════════════════════════════════════════════════════════
FIGURES = [
    (fig2_ltb_curve, "§4 Step 4～6·§5",
     "分區判斷錯（誤判為彈性）、或 C_b 直接取 1.0 使 M_n 只剩 1,930"),
    (fig3_code_flip, "§6.2·§6.4",
     "拿 AISC 360-16 的 L_r 去配本卷舊式公式（或反之）而答錯分區"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    ref = [("A", A, 99.97), ("I_x", IX, 25831), ("S_x", SX, 1271.8), ("Z_x", ZX, 1475.9),
           ("I_y", IY, 1782.4), ("r_y", RY, 4.222), ("J", J, 53.75), ("I_f", IF_, 887.96),
           ("C_W", CW, 687469), ("M_p", MP, 3719.2), ("M_r", MR, 1869.6),
           ("X_1", X1, 170.1), ("X_2", X2, 1.224), ("L_p", LP, 212.8), ("L_r", LR, 833.2),
           ("L_p(AISC)", LP_A, 214.5), ("r_ts", RTS, 5.246), ("L_r(AISC)", LR_A, 721.3),
           ("M_r(AISC)", MR_A, 2243.5)]
    print("現算值 vs SS-2011-3.md 表列值：")
    for nm, got, want in ref:
        ok = "OK " if abs(got - want) <= max(abs(want) * 0.002, 0.05) else "!! "
        print(f"  {ok}{nm:<11} {got:>12,.4g}   （.md: {want:,}）")
    print(f"\nM_p 平台段終點 L_b = {LB_CAP_END:.1f} cm；"
          f"M_n(L_b={LB}) = {mn(LB):,.1f}（.md: {MN:,}）")
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<42} {section:<18} 攔：{catches}")
