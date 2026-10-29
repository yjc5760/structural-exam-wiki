#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2022-1 圖解產生腳本（BOX 800×800×32 梁柱之 LRFD 三重檢核）

斷面性質、λ_c、F_cr、φ_cP_n、φ_bM_p、A_w、φ_vV_n、互制比全部由腳本重算。
執行：python3 gen_SS-2022-1.py   →   figs/*.svg
"""
import sys, os, math
# struct-diagram 的 primitives 取自本知識庫自帶的 skill 副本（repo 相對路徑，故可原地重跑）；
# 若把本檔搬到別處，設環境變數 SD_SKILL 指向 struct-diagram 目錄即可。
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ══════════════════════════════════════════════════════════════
# L1：題目給定（§1）
# ══════════════════════════════════════════════════════════════
BO   = 80.0        # cm 外廓邊長（正方形）
T    = 3.2         # cm 板厚
KLR  = 30.54       # 受壓有效長細比（題給）
FY   = 3.3         # tf/cm^2
E    = 2040.0      # tf/cm^2
PU   = 1119.0      # tf
MU2  = 179.0       # tf·m
MU3  = 19.4        # tf·m
VU2  = 86.77       # tf
VU3  = 9.14        # tf
KV   = 5.0
PHI_C, PHI_B, PHI_V = 0.85, 0.90, 0.90
PHI_C_AISC, PHI_V_AISC = 0.90, 1.00   # §6.2 對照

# ── L2 Step 1：斷面性質（§4 一）──
BI  = BO - 2*T                     # 73.6
A   = BO**2 - BI**2                # 983.04
I   = (BO**4 - BI**4)/12           # 968,045
S   = I/(BO/2)                     # 24,201
Z   = (BO**3 - BI**3)/4            # 28,328（僅適用正方形箱形）
RG  = math.sqrt(I/A)               # 31.38

# ── Step 2：局部挫屈（§4 二）──
BT_NET  = BI/T                     # 23.0 淨寬定義
BT_OUT  = BO/T                     # 25.0 外緣寬定義（較嚴）
LAM_P   = 50/math.sqrt(FY)         # 27.52
LAM_P_AISC = 1.12*math.sqrt(E/FY)  # 27.85

# ── Step 3：壓力強度（§4 三）──
LAM_C   = KLR/math.pi*math.sqrt(FY/E)
FCR     = 0.658**(LAM_C**2) * FY
PN      = FCR*A
PHI_PN  = PHI_C*PN
PHI_PN_AISC = PHI_C_AISC*PN

# ── Step 4：彎曲強度（§4 四）──
MP      = FY*Z                     # tf·cm
PHI_MN  = PHI_B*MP/100             # tf·m（正方形兩軸相同）

# ── Step 5：剪力強度（§4 五）──
AW      = 2*BI*T                   # 471.04 —— 只有平行剪力方向的兩片板
AW_WRONG = 4*BI*T                  # 若誤把四片全算
VN      = 0.6*FY*AW
PHI_VN  = PHI_V*VN
PHI_VN_AISC = PHI_V_AISC*VN
H_TW    = BI/T
SHEAR_LIM = 50*math.sqrt(KV/FY)    # 61.5

# ── Step 6：P-M 互制（§4 六）──
R_AX  = PU/PHI_PN
R_M2  = MU2/PHI_MN
R_M3  = MU3/PHI_MN
H11A  = R_AX + 8/9*(R_M2 + R_M3)
R_AX_AISC = PU/PHI_PN_AISC
H11A_AISC = R_AX_AISC + 8/9*(R_M2 + R_M3)


# ══════════════════════════════════════════════════════════════
def fig1_section():
    """圖 1：BOX 斷面與局部挫屈檢核"""
    PWD, PH = 470, 500
    XL, XR = -0.30*BO, 1.34*BO
    YL, YH = -0.26*BO, 1.30*BO
    Lm, Tm, Bm = 40, 108, 96
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("BOX 800×800×32 斷面", f"外廓 {BO:g} cm、板厚 {T:g} cm")
    # 外框與內孔（閉口斷面：外減內）
    p1.polygon([(0, 0), (BO, 0), (BO, BO), (0, BO)], "#EDF1F6", C["member"], 2.8)
    p1.polygon([(T, T), (BO-T, T), (BO-T, BO-T), (T, BO-T)], "#FFFFFF", C["member"], 2.4)
    p1.dim((0, 0), (BO, 0), f"b_{{o}} = {BO:g}", off=48, label_off=15)
    p1.dim((T, BO-T), (BO-T, BO-T), f"b_{{i}} = b_{{o}} − 2t = {BI:g}", off=-40, label_off=-14,
           color=C["accent"])
    p1.dim((BO, 0), (BO, BO), f"{BO:g}", off=44, label_off=13)
    p1.dim((0, BO), (T, BO), f"t = {T:g}", off=-72, label_off=-14)
    p1.math_px(p1.X(BO/2), p1.Y(BO/2) - 4, f"A = {A:,.2f} cm^{{2}}", 14.5, C["bmd"], weight="700")
    p1.math_px(p1.X(BO/2), p1.Y(BO/2) + 22, f"I = {I:,.0f} cm^{{4}}", 13, C["muted"], weight="700")
    p1.math_px(p1.X(BO/2), p1.Y(BO/2) + 44, f"Z = {Z:,.0f} cm^{{3}}", 13, C["muted"], weight="700")

    p2 = Canvas(PWD, PH, sx=1.0)
    p2.panel("板件寬厚比 vs 結實界限", "兩種寬度定義皆通過 ⇒ 判定穩健")
    x0, bw = 196, 186
    peak = max(BT_OUT, LAM_P, LAM_P_AISC)
    # 符號用 math_px（襯線斜體），中文說明另用 text_px——數學字型沒有中文字，混寫會整段吃掉
    # 名稱一律用 text_px：含上下標又靠右對齊時，est_width 會低估含 √ 的寬度而壓到長條
    rows = (("bi/t", "淨寬定義", BT_NET, C["bmd"]),
            ("bo/t", "外緣寬定義（較嚴）", BT_OUT, C["compr"]),
            ("λp = 50/√Fy", "台灣 2010 結實界限", LAM_P, C["load"]),
            ("1.12√(E/Fy)", "AISC 360-16 §F7 界限", LAM_P_AISC, C["accent"]))
    for i, (nm, note, v, col) in enumerate(rows):
        y = 132 + i*54
        p2.text_px(x0 - 12, y - 9, nm, 13.5, C["text"], "end", weight="700")
        p2.text_px(x0 - 12, y + 12, note, 11.5, C["muted"], "end")
        p2.rect_px(x0, y-14, bw, 28, "#EDF1F6", 6)
        p2.rect_px(x0, y-14, bw*v/peak, 28, col, 6)
        p2.text_px(x0 + bw*v/peak + 10, y, f"{v:.2f}", 13, col, "start", weight="700")
    p2.parts.append(f'<line x1="{x0 + bw*LAM_P/peak}" y1="110" x2="{x0 + bw*LAM_P/peak}" '
                    f'y2="{132+3*54+22}" stroke="{C["load"]}" stroke-width="1.8" '
                    f'stroke-dasharray="6 4"/>')
    p2.text_px(PWD/2, PH - 86, f"KL/r = {KLR:g} ≪ 200 ✓", 14, C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 60, f"r = √(I/A) = {RG:.2f} cm ⇒ KL ≈ {KLR*RG:,.0f} cm",
               13, C["muted"])
    p2.text_px(PWD/2, PH - 30, "結實斷面（Compact）：局部挫屈不控制", 13, C["bmd"], weight="700")

    compose([p1, p2], cols=2,
            title="圖 1　閉口箱形斷面性質與局部挫屈",
            sub=f"清淨寬 bi = bo − 2t = {BI:g} cm（兩側板厚都要扣）——扣一次會把 b/t 由 {BT_NET:.1f} "
                f"變成 {(BO-T)/T:.1f}",
            note=f"Z = (bo³ − bi³)/4 僅適用正方形箱形；形狀因數 Z/S = {Z/S:.3f} 落在箱形常見的 1.12～1.20",
            path=os.path.join(OUT, "SS-2022-1-fig-1-section.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_shear():
    """圖 2：剪力有效面積 A_w 只取平行剪力方向的兩片板"""
    PWD, PH = 470, 540
    XL, XR = -0.16*BO, 1.16*BO
    YL, YH = -0.14*BO, 1.16*BO
    Lm, Tm, Bm = 44, 118, 96
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    def shell(cv):
        cv.polygon([(0, 0), (BO, 0), (BO, BO), (0, BO)], "#FFFFFF", C["member"], 2.6)
        cv.polygon([(T, T), (BO-T, T), (BO-T, BO-T), (T, BO-T)], "#FFFFFF", C["member"], 2.2)

    # ── 正解 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("正解：兩片平行腹板承剪", f"A_w = 2 h t = {AW:.2f} cm^{{2}}")
    shell(p1)
    for x in (0, BO-T):
        p1.polygon([(x, T), (x+T, T), (x+T, BO-T), (x, BO-T)], C["fill_s"], C["sfd"], 2.0)
    p1.arrow((BO/2, BO*0.30), (BO/2, BO*0.78), C["sfd"], 3.6, 12)
    p1.math_px(p1.X(BO/2) + 14, p1.Y(BO*0.56), f"V_{{u2}} = {VU2:g} tf", 13.5, C["sfd"],
               "start", weight="700")
    p1.text_px(p1.X(BO/2), p1.Y(BO) - 20, "左右兩片平行剪力方向 ⇒ 承剪", 12, C["sfd"], weight="700")
    p1.text_px(p1.X(BO/2), p1.Y(0) + 34, "上下兩片垂直剪力方向 ⇒ 不計", 12, C["muted"])

    # ── 誤解 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("誤解：四片全算", f"A_w = 4 h t = {AW_WRONG:.2f} cm^{{2}}（高估 {AW_WRONG/AW:.0f} 倍）")
    shell(p2)
    p2.polygon([(0, 0), (BO, 0), (BO, BO), (0, BO)], C["fill_t"], C["load"], 2.0)
    p2.polygon([(T, T), (BO-T, T), (BO-T, BO-T), (T, BO-T)], "#FFFFFF", C["load"], 2.0)
    p2.arrow((BO/2, BO*0.30), (BO/2, BO*0.78), C["load"], 3.6, 12)
    p2.text_px(p2.X(BO/2), p2.Y(BO) - 20, "四片全部計入", 12, C["load"], weight="700")
    p2.text_px(p2.X(BO/2), p2.Y(0) + 34, "上下兩片與剪力垂直，不能提供剪力抵抗", 12, C["load"])

    compose([p1, p2], cols=2,
            title=f"圖 2　箱形柱剪力面積的認定：φvVn = {PHI_VN:,.1f} tf",
            sub=f"h/tw = {H_TW:.1f} < 50√(kv/Fy) = {SHEAR_LIM:.1f} ⇒ 不折減，Vn = 0.6·Fy·Aw",
            note=f"剪力利用率僅 Vu2/φvVn = {VU2/PHI_VN*100:.1f}%、Vu3 為 {VU3/PHI_VN*100:.1f}%"
                 f"；若 Aw 誤取四片，會把利用率再低估一半",
            path=os.path.join(OUT, "SS-2022-1-fig-2-shear-area.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_pm():
    """圖 3：正規化 P-M 互制折線與本題需求點"""
    W, H = 780, 580
    Lm, Rm, Tm, Bm = 106, 210, 116, 92
    XMAX, YMAX = 1.24, 1.20
    sx = min((W-Lm-Rm)/XMAX, (H-Tm-Bm)/YMAX)
    cv = Canvas(W, H, sx=sx, ox=Lm, oy=Bm, bg="#FFFFFF")

    # 折線三控制點（由 8/9 與 1/2 兩係數推得，非目測）
    A_ = (0.0, 1.0)
    B_ = (9/8*(1 - 0.2), 0.2)          # 高軸力式代 P̄=0.2 → M̄ = 0.9
    Cc = (1.0, 0.0)

    cv.polygon([(0, 0), A_, B_, Cc], C["fill_c"], C["compr"], 3.0)
    cv.arrow((0, 0), (XMAX, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, YMAX), C["muted"], 1.8, 9)
    cv.math((XMAX, 0), "M_{u}/φ_{b}M_{n}", 14, C["muted"], "start", dx=6, dy=16)
    cv.math((0, YMAX), "P_{u}/φ_{c}P_{n}", 14, C["muted"], "end", dx=-10)
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        cv.text_px(cv.X(0) - 10, cv.Y(v), f"{v:.1f}", 12, C["muted"], "end")
        cv.text_px(cv.X(v), cv.Y(0) + 18, f"{v:.1f}", 12, C["muted"])
    cv.line((0, 0.2), (XMAX, 0.2), C["accent"], 1.4, dash="5 4")
    cv.text_px(cv.X(XMAX) - 4, cv.Y(0.2) - 14, "0.2 分界", 12, C["accent"], "end", weight="700")

    for p, lab in ((A_, "A 純軸壓"), (B_, "B 折點 (0.9, 0.2)"), (Cc, "C 純彎")):
        cv.dot(p, 5.4, fill=C["compr"])
    cv.text_px(cv.X(A_[0]) + 12, cv.Y(A_[1]) - 6, "A 純軸壓", 12.5, C["compr"], "start", weight="700")
    cv.text_px(cv.X(B_[0]) + 12, cv.Y(B_[1]) + 16, f"B 折點 ({B_[0]:.1f}, {B_[1]:.1f})",
               12.5, C["compr"], "start", weight="700")
    cv.text_px(cv.X(Cc[0]) + 10, cv.Y(Cc[1]) - 16, "C 純彎", 12.5, C["compr"], "start", weight="700")
    cv.text_px(cv.X(0.30), cv.Y(0.30), "安全域", 15, C["compr"], weight="700")

    # 本題需求點（雙軸彎矩合併於橫軸）
    mdem = R_M2 + R_M3
    cv.dot((mdem, R_AX), 6.4, fill=C["load"], stroke="#FFFFFF", w=2)
    cv.line((0, R_AX), (mdem, R_AX), C["load"], 1.2, dash="4 3")
    cv.line((mdem, 0), (mdem, R_AX), C["load"], 1.2, dash="4 3")
    cv.text_px(cv.X(mdem) + 14, cv.Y(R_AX) - 8,
               f"本題需求點 ({mdem:.3f}, {R_AX:.3f})", 13, C["load"], "start", weight="700")
    cv.text_px(cv.X(mdem) + 14, cv.Y(R_AX) + 14,
               f"H1-1a = {H11A:.3f} ≤ 1.0 ✓", 13, C["load"], "start", weight="700")

    # AISC 對照點（φc = 0.90）
    cv.dot((mdem, R_AX_AISC), 5.0, fill=C["accent"], stroke="#FFFFFF", w=1.8)
    cv.text_px(cv.X(mdem) + 14, cv.Y(R_AX) + 36,
               f"AISC φc = 0.90 ⇒ {H11A_AISC:.3f}", 12, C["accent"], "start", weight="700")

    cv.legend(W - Rm + 10, 168,
              [(C["compr"], "設計強度折線"), (C["load"], "台灣 2010 需求點"),
               (C["accent"], "AISC 360-16 對照")], size=12, gap=21)
    cv.math_px(W - Rm + 10, 244, f"φ_{{c}}P_{{n}} = {PHI_PN:,.0f} tf", 13, C["text"], "start", weight="700")
    cv.math_px(W - Rm + 10, 268, f"φ_{{b}}M_{{n}} = {PHI_MN:,.1f} tf·m", 13, C["text"], "start", weight="700")
    cv.math_px(W - Rm + 10, 292, f"M_{{u2}}/φ_{{b}}M_{{n}} = {R_M2:.4f}", 12.5, C["muted"], "start")
    cv.math_px(W - Rm + 10, 314, f"M_{{u3}}/φ_{{b}}M_{{n}} = {R_M3:.4f}", 12.5, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 3　P-M 互制折線與本題需求點", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"Pu/φcPn = {R_AX:.3f} ≥ 0.2 ⇒ 落在折點上方，用 H1-1a（含 8/9 係數）",
               13, C["muted"])
    cv.text_px(W/2, 84, "折點座標由 8/9 與 1/2 兩係數推得：兩式在 0.2 處皆給 0.9，曲線連續",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "載重已是「分析後之係數化二階值」⇒ 不可再乘 B1／B2（會重複計入）",
               13, C["load"])
    cv.save(os.path.join(OUT, "SS-2022-1-fig-3-pm.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_section(); fig2_shear(); fig3_pm()
    print(f"bi={BI:g} A={A:,.2f} I={I:,.0f} S={S:,.0f} Z={Z:,.0f} r={RG:.2f} Z/S={Z/S:.3f}")
    print(f"b/t net={BT_NET:.1f} out={BT_OUT:.1f} lam_p={LAM_P:.2f} (AISC {LAM_P_AISC:.2f})")
    print(f"lam_c={LAM_C:.3f} Fcr={FCR:.3f} Pn={PN:,.0f} phiPn={PHI_PN:,.0f}")
    print(f"Mp={MP:,.0f} tf·cm = {MP/100:.1f} tf·m  phiMn={PHI_MN:.1f} tf·m")
    print(f"Aw={AW:.2f} Vn={VN:.1f} phiVn={PHI_VN:.1f}  h/tw={H_TW:.1f} lim={SHEAR_LIM:.1f}")
    print(f"H1-1a = {R_AX:.3f} + 8/9({R_M2:.4f}+{R_M3:.4f}) = {H11A:.3f}"
          f"　AISC = {H11A_AISC:.3f}")
    print("done ->", OUT)
