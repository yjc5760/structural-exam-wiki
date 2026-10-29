#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2017-4 圖解產生腳本（U 形偏心銲道群：彈性向量法求 P_u）

形心、J_w、各角點向量與 P_u 全部由下方幾何常數算出；改 b 或 d 重跑，圖形與臨界點跟著變。
執行：python3 gen_SS-2017-4.py   →   figs/*.svg
"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = os.path.join(_HERE, "figs")

# ══════════════════════════════════════════════════════════════
# L1：題目給定（§1）
# ══════════════════════════════════════════════════════════════
B    = 40.0      # cm 上、下水平銲道長（等長）
D    = 80.0      # cm 左垂直銲道長
EPR  = 50.0      # cm 托架板自銲道右端再懸挑之距離
TE   = 1.0       # cm 有效喉厚（題給 10 mm）
PHI  = 0.75
FEXX = 70 * 0.07031          # tf/cm^2  （4.922）

# ── Step 1～2：全長與形心（原點取銲道群左下角）──
LTOT = 2*B + D                               # 160
XBAR = B**2 / LTOT                           # 10（U 形速算 b^2/(2b+d)）
YBAR = D/2                                   # 40（對稱）
XP   = B + EPR                               # 90，P 距柱面

# ── Step 3：極慣性矩（線積分，單位 cm^3）──
def _I_horiz(y):
    """水平段 y = const，x: 0→B，對形心之 ∫r²dL"""
    return ((B-XBAR)**3 - (-XBAR)**3)/3 + (y-YBAR)**2 * B
def _I_vert():
    """垂直段 x = 0，y: 0→D"""
    return XBAR**2 * D + ((D-YBAR)**3 - (-YBAR)**3)/3

IW1 = _I_horiz(0.0)          # 下水平 73,333
IW2 = _I_vert()              # 左垂直 50,667
IW3 = _I_horiz(D)            # 上水平 73,333
JW  = IW1 + IW2 + IW3        # 197,333
# 交叉驗核：J = Ix + Iy
IX_CHK = 2*B*(YBAR)**2 + D**3/12
IY_CHK = D*XBAR**2 + 2*(B**3/12 + B*(B/2 - XBAR)**2)
assert abs((IX_CHK + IY_CHK) - JW) < 1e-6, "J_w 兩路徑不一致"

# ── Step 4～5：偏心矩、直接剪力與各角點合力 ──
ECC  = XP - XBAR                             # 80
FV   = 1.0 / LTOT                            # 直接剪力係數（每單位 P，向下）

def corner(rx, ry):
    """回傳 (f_tx, f_ty, f_res)，皆為每單位 P；CW 旋轉"""
    ftx = ECC*ry / JW
    fty = -ECC*rx / JW
    return ftx, fty, math.hypot(ftx, -FV + fty)

CORNERS = (("上水平右端", B - XBAR,  D - YBAR),
           ("下水平右端", B - XBAR, -YBAR),
           ("上水平左端",  -XBAR,    D - YBAR),
           ("下水平左端",  -XBAR,   -YBAR))
RES = {nm: corner(rx, ry) for nm, rx, ry in CORNERS}
F_CRIT = max(v[2] for v in RES.values())      # 0.024535

# ── Step 6：P_u ──
Q_UNIT = PHI * 0.6 * FEXX * TE                # 2.215 tf/cm
PU     = Q_UNIT / F_CRIT                      # 90.3 tf

# ── §6：方向性強度與瞬心法（後者為 .md §6.3 之數值解）──
FX_C, FY_C = RES["上水平右端"][0], -FV + RES["上水平右端"][1]
THETA_D = math.degrees(math.atan2(abs(FY_C), abs(FX_C)))     # 48.6°
K_DIR   = 1.0 + 0.5*math.sin(math.radians(THETA_D))**1.5     # 1.325
PU_DIR  = Q_UNIT*K_DIR / F_CRIT                              # 119.6
PU_IC   = 159.7        # tf  §6.3 之瞬心法數值解
PU_FIN  = 90.49        # tf  §5 有限寬度理想化
PU_BOOK = 90.9         # tf  §5 坊間詳解


# ══════════════════════════════════════════════════════════════
def fig1_weld_group():
    """圖 1：銲道群幾何、形心與偏心距"""
    W, H = 940, 560
    XL, XR = -22.0, 104.0
    YL, YH = -18.0, 100.0
    Lm, Rm, Tm, Bm = 56, 56, 116, 92
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    cv = Canvas(W, H, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx, bg="#FFFFFF")

    # 柱翼板
    cv.polygon([(-14, -8), (0, -8), (0, D+8), (-14, D+8)], "#DCE3EC", C["member"], 2.2)
    cv.text_px(cv.X(-7), cv.Y(D+8) - 16, "柱翼板", 12, C["muted"], weight="700")

    # 托架板（梯形；右端承載 P）
    cv.polygon([(0, 0), (XP, YBAR-9), (XP, YBAR+9), (0, D)], "#F3F6F9", C["member2"], 2.0)

    # U 形銲道（粗線）
    for p0, p1 in (((0, 0), (B, 0)), ((0, 0), (0, D)), ((0, D), (B, D))):
        cv.line(p0, p1, C["load"], 7.0, cap="butt")
    cv.text_px(cv.X(B/2), cv.Y(D) - 16, f"上水平銲道 b = {B:g}", 12, C["load"], weight="700")
    cv.text_px(cv.X(B/2), cv.Y(0) + 22, f"下水平銲道 b = {B:g}", 12, C["load"], weight="700")
    cv.text_px(cv.X(0) + 12, cv.Y(D*0.78), f"左垂直銲道 d = {D:g}", 12, C["load"], "start", weight="700")
    cv.text_px(cv.X(B) + 10, cv.Y(D/2), "右側無銲道（開口朝右）", 12, C["muted"], "start")

    # 形心
    cv.dot((XBAR, YBAR), 6.4, fill=C["bmd"])
    cv.line((XBAR, -10), (XBAR, D+10), C["bmd"], 1.4, dash="5 4")
    cv.text_px(cv.X(XBAR), cv.Y(YBAR) - 18,
               f"形心 ({XBAR:g}, {YBAR:g})", 13, C["bmd"], weight="700")

    # 尺寸線（下方）與「圓點不是形心」的辨正
    cv.dim((0, -8), (B, -8), f"{B:g}", off=26, label_off=12)
    cv.dim((B, -8), (XP, -8), f"{EPR:g}", off=26, label_off=12)
    cv.parts.append(f'<circle cx="{cv.X(B):.2f}" cy="{cv.Y(-8)+26:.2f}" r="5" '
                    f'fill="{C["accent"]}" stroke="#FFFFFF" stroke-width="1.6"/>')
    cv.text_px(cv.X(B), cv.Y(-8) + 56, "圓點＝尺寸線分段記號", 11.5, C["accent"], weight="700")
    cv.text_px(cv.X(B), cv.Y(-8) + 74, "（不是形心）", 11.5, C["accent"], weight="700")

    # 載重 P 與偏心距 e
    cv.arrow((XP, YBAR+30), (XP, YBAR+11), C["load"], 3.6, 12)
    cv.math_px(cv.X(XP), cv.Y(YBAR+34), "P", 18, C["load"], weight="700")
    cv.dim((XBAR, YBAR+22), (XP, YBAR+22), f"e = {ECC:g}", off=-20, label_off=-13,
           color=C["bmd"])

    cv.text_px(W/2, 34, "圖 1　U 形銲道群的幾何與形心", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               f"形心由 x̄ = b²/(2b+d) = {B:g}²/{LTOT:g} = {XBAR:g} cm 算出，偏心距要從形心量起",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"若把尺寸線上的圓點當形心（x̄ = {B:g}），反解得 b = 109.3 cm，與圖上長度比嚴重不符",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"J_w = {JW:,.0f} cm³（線積分；已用 J = Ix + Iy 交叉驗核）　"
               f"M = P·e = {ECC:g}P，順時針",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2017-4-fig-1-weld-group.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_vector():
    """圖 2：四個角點的向量疊加與臨界點辨識"""
    W, H = 880, 760
    XL, XR = -30.0, 72.0
    YL, YH = -24.0, 104.0
    Lm, Rm, Tm, Bm = 58, 250, 118, 92
    sx = min((W-Lm-Rm)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    cv = Canvas(W, H, sx=sx, ox=Lm - XL*sx, oy=Bm - YL*sx, bg="#FFFFFF")

    VS = 18.0 / F_CRIT            # 向量繪圖比例：最大合力 → 18 cm

    for p0, p1 in (((0, 0), (B, 0)), ((0, 0), (0, D)), ((0, D), (B, D))):
        cv.line(p0, p1, C["member"], 6.0, cap="butt")
    cv.dot((XBAR, YBAR), 6.0, fill=C["bmd"])
    cv.math_px(cv.X(XBAR) + 12, cv.Y(YBAR) + 14, "C", 14, C["bmd"], "start", weight="700")

    for nm, rx, ry in CORNERS:
        px, py = XBAR + rx, YBAR + ry
        ftx, fty, fres = RES[nm]
        crit = abs(fres - F_CRIT) < 1e-12
        # 半徑線（形心 → 該點）
        cv.line((XBAR, YBAR), (px, py), C["ghost"], 1.4, dash="4 3")
        # 直接剪力（向下）
        cv.arrow((px, py), (px, py - FV*VS), C["compr"], 2.6, 9)
        # 扭矩剪力
        cv.arrow((px, py), (px + ftx*VS, py + fty*VS), C["accent"], 2.6, 9)
        # 合成
        cv.arrow((px, py), (px + ftx*VS, py - FV*VS + fty*VS),
                 C["load"] if crit else C["muted"], 3.6 if crit else 2.4, 11)
        cv.dot((px, py), 5.6 if crit else 4.2,
               fill=C["load"] if crit else C["member"])
        lab = f"{fres:.5f}P"
        dx = 12 if rx > 0 else -12
        cv.text_px(cv.X(px) + dx, cv.Y(py) + (-16 if ry > 0 else 22), lab,
                   12.5, C["load"] if crit else C["muted"],
                   "start" if rx > 0 else "end", weight="700")

    cv.text_px(cv.X(B) + 20, cv.Y(D) + 66, "臨界點", 13, C["load"],
               "start", weight="700")

    cv.legend(W - Rm + 12, 172,
              [(C["compr"], "直接剪力 P/L（向下）"),
               (C["accent"], "扭矩剪力 Mr/J_w"),
               (C["load"], "合成（臨界點）"),
               (C["muted"], "合成（非臨界）")], size=12, gap=22)
    cv.math_px(W - Rm + 12, 288, f"f_{{v}} = P/{LTOT:g} = {FV:.5f}P", 12.5, C["compr"],
               "start", weight="700")
    cv.math_px(W - Rm + 12, 312, f"f_{{tx}} = M r_{{y}}/J_{{w}}", 12.5, C["accent"], "start")
    cv.math_px(W - Rm + 12, 334, f"f_{{ty}} = − M r_{{x}}/J_{{w}}", 12.5, C["accent"], "start")
    cv.text_px(W - Rm + 12, 366, "右端兩點的扭矩剪力", 12, C["text"], "start", weight="700")
    cv.text_px(W - Rm + 12, 386, "有向下分量，與直接剪力", 12, C["text"], "start")
    cv.text_px(W - Rm + 12, 406, "同向疊加 ⇒ 最不利", 12, C["text"], "start")
    cv.math_px(W - Rm + 12, 440, f"f_{{res}} = {F_CRIT:.5f}P", 14, C["load"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 2　彈性向量法：四個角點的疊加與臨界點", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "扭矩剪力垂直於半徑、大小正比於 r；直接剪力沿全長均勻向下",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "左端兩點離形心較近且扭矩分量向上（與直接剪力相消）——「離形心最遠」不等於「最不利」",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"q = φ·0.6F_EXX·t_e = {Q_UNIT:.3f} tf/cm ⇒ P_u = {Q_UNIT:.3f}/{F_CRIT:.5f} "
               f"= {PU:.1f} tf",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2017-4-fig-2-vector.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_method_compare():
    """圖 3：三種分析方法的強度差距"""
    W, H = 960, 430
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 330, 400
    rows = (("彈性向量法（本題主答案）", "台灣 2010／AISC 皆同此式", PU, C["load"]),
            ("＋ AISC 方向性強度", f"θ = {THETA_D:.1f}°，係數 {K_DIR:.3f}", PU_DIR, C["accent"]),
            ("瞬心法（AISC 手冊 Part 8）", "考慮非線性荷重–變形與方向性", PU_IC, C["compr"]))
    peak = max(v for *_, v, _ in rows) * 1.08
    for i, (nm, note, v, col) in enumerate(rows):
        y = 136 + i*72
        cv.text_px(x0 - 14, y - 9, nm, 13.5, C["text"], "end", weight="700")
        cv.text_px(x0 - 14, y + 12, note, 11.5, C["muted"], "end")
        cv.rect_px(x0, y-17, bw, 34, "#EDF1F6", 7)
        cv.rect_px(x0, y-17, bw*v/peak, 34, col, 7)
        cv.text_px(x0 + bw*v/peak + 12, y, f"{v:.1f} tf", 13.5, col, "start", weight="700")
        cv.text_px(x0 + bw*v/peak - 12, y, f"×{v/PU:.2f}", 12.5, "#FFFFFF", "end", weight="700")

    cv.text_px(W/2, 34, "圖 3　同一組銲道，三種方法差 1.77 倍", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58,
               "填角銲的基本強度式（0.6F_EXX、φ = 0.75）自 AISC LRFD 1993 至 360-22 從未改變",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"故彈性向量法在新舊規範同值 {PU:.1f} tf——差別全在「用哪一種分析法」，不在強度式",
               12.5, C["accent"])
    cv.text_px(W/2, H - 48,
               f"線理想化 {PU:.2f}／有限寬度 {PU_FIN:.2f}／坊間詳解 {PU_BOOK:.1f} tf，"
               f"三者差 {100*(PU_BOOK/PU-1):.1f}% ⇒ 答案穩健",
               13, C["muted"])
    cv.text_px(W/2, H - 24,
               "台灣 2010 規範無方向性強度與瞬心法條文，考場請答彈性向量法的 90 tf",
               12.5, C["load"])
    cv.save(os.path.join(OUT, "SS-2017-4-fig-3-method-compare.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_weld_group(); fig2_vector(); fig3_method_compare()
    print(f"L={LTOT:g} xbar={XBAR:g} ybar={YBAR:g} e={ECC:g}")
    print(f"Iw1={IW1:,.0f} Iw2={IW2:,.0f} Iw3={IW3:,.0f} Jw={JW:,.0f}"
          f"  (Ix+Iy={IX_CHK+IY_CHK:,.0f})")
    for nm, rx, ry in CORNERS:
        a, b_, c = RES[nm]
        print(f"  {nm}: r=({rx:+g},{ry:+g}) ftx={a:+.5f} fty={b_:+.5f} fres={c:.5f}")
    print(f"FEXX={FEXX:.3f} q={Q_UNIT:.4f} f_crit={F_CRIT:.5f} -> Pu={PU:.2f} tf")
    print(f"θ={THETA_D:.1f}° k={K_DIR:.3f} Pu_dir={PU_DIR:.1f} Pu_IC={PU_IC}")
    print("done ->", OUT)
