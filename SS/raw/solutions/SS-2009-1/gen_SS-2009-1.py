#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2009-1 圖解產生腳本（強柱弱梁 + P-M 互制曲線）

P-M 折線的三個控制點與兩段斜率全部由 8/9、1/2 兩係數推出，不是照抄座標。
執行：python3 gen_SS-2009-1.py   →   figs/*.svg
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
# 由 SS-2009-1 §4 之規範條文取得
# ══════════════════════════════════════════════════════════════
SPLIT   = 0.2        # 高／低軸力分界 P_u/φ_cP_n           §4 二 2.1
K_HIGH  = 8/9        # 高軸力式之彎矩項係數（8.2-1a）       §4 二 2.1
K_LOW   = 0.5        # 低軸力式之軸力項係數（8.2-1b）       §4 二 2.1
PHI_C, PHI_B = 0.85, 0.90                                # §4 二
PHI_C_AISC = 0.90                                        # §6.2
OVERSTR_TW   = 1.25          # 我國 (13.6-3) 梁側單一定值   §4 一 1.2
SH_AISC, RY_LOW, RY_HIGH = 1.1, 1.1, 1.5                 # AISC 341 之 1.1R_y  §6.1

# 三個控制點（由上面兩個係數解出，不是量出來的）
A_PT = (0.0, 1.0)                                  # 純軸壓
M_B  = (1.0 - SPLIT) / K_HIGH                      # 高軸力式代 P̄ = 0.2 → M̄
M_B2 = 1.0 - K_LOW*SPLIT                           # 低軸力式代 P̄ = 0.2 → M̄（須相同）
B_PT = (M_B, SPLIT)
C_PT = (1.0, 0.0)
K_AB = (B_PT[1] - A_PT[1]) / (B_PT[0] - A_PT[0])   # −8/9
K_BC = (C_PT[1] - B_PT[1]) / (C_PT[0] - B_PT[0])   # −2
assert abs(M_B - M_B2) < 1e-12, "折點不連續 —— 8/9 與 1/2 兩係數不相容"


# ══════════════════════════════════════════════════════════════
def fig3_pm():
    """圖 3：P-M 互制折線（子題二）"""
    W, H = 800, 590
    Lm, Rm, Tm, Bm = 108, 236, 116, 96
    XMAX, YMAX = 1.26, 1.22
    sx = min((W-Lm-Rm)/XMAX, (H-Tm-Bm)/YMAX)
    cv = Canvas(W, H, sx=sx, ox=Lm, oy=Bm, bg="#FFFFFF")

    cv.polygon([(0, 0), A_PT, B_PT, C_PT], C["fill_c"], C["compr"], 3.2)
    cv.arrow((0, 0), (XMAX, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, YMAX), C["muted"], 1.8, 9)
    cv.math((XMAX, 0), "M_{u}/φ_{b}M_{n}", 14, C["muted"], "start", dx=6, dy=16)
    cv.math((0, YMAX), "P_{u}/φ_{c}P_{n}", 14, C["muted"], "end", dx=-10)
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        cv.text_px(cv.X(0) - 10, cv.Y(v), f"{v:.1f}", 12, C["muted"], "end")
        cv.text_px(cv.X(v), cv.Y(0) + 18, f"{v:.1f}", 12, C["muted"])

    # 分界線與折點
    cv.line((0, SPLIT), (XMAX, SPLIT), C["accent"], 1.5, dash="5 4")
    cv.line((B_PT[0], 0), B_PT, C["accent"], 1.5, dash="5 4")
    for p, lab, dx, dy, anch in ((A_PT, "A　純軸壓 (0, 1.0)", 14, -8, "start"),
                                 (B_PT, f"B　折點 ({B_PT[0]:.1f}, {B_PT[1]:.1f})", -16, 24, "end"),
                                 (C_PT, "C　純彎 (1.0, 0)", 14, -26, "start")):
        cv.dot(p, 6.0, fill=C["compr"])
        cv.text_px(cv.X(p[0]) + dx, cv.Y(p[1]) + dy, lab, 13, C["compr"], anch, weight="700")

    # 兩段斜率標註（BC 段太短，改放在安全域內並以引線指回線段中點）
    def slope_block(ax, ay, k, name, col, leader=None):
        cv.text_px(ax, ay - 20, name, 12.5, col, "start", weight="700")
        cv.math_px(ax, ay, f"k = {k:.3f}", 13, col, "start", weight="700")
        cv.text_px(ax, ay + 20, "較平" if abs(k) < abs(K_BC) else "較陡", 12.5, col,
                   "start", weight="700")
        if leader:
            cv.parts.append(f'<line x1="{leader[0]:.2f}" y1="{leader[1]:.2f}" '
                            f'x2="{leader[2]:.2f}" y2="{leader[3]:.2f}" stroke="{col}" '
                            f'stroke-width="1.2" stroke-dasharray="4 3"/>')

    mabx, maby = (A_PT[0]+B_PT[0])/2, (A_PT[1]+B_PT[1])/2
    slope_block(cv.X(mabx) + 20, cv.Y(maby) - 6, K_AB, "AB 段（高軸力）", C["bmd"])
    mbcx, mbcy = (B_PT[0]+C_PT[0])/2, (B_PT[1]+C_PT[1])/2
    slope_block(cv.X(0.30), cv.Y(0.095), K_BC, "BC 段（低軸力）", C["load"],
                leader=(cv.X(0.58), cv.Y(0.095), cv.X(mbcx) - 8, cv.Y(mbcy)))

    cv.text_px(cv.X(0.26), cv.Y(0.42), "安全域（折線左下）", 14.5, C["compr"], weight="700")

    cv.legend(W - Rm + 10, 160,
              [(C["compr"], "設計強度折線"), (C["accent"], "0.2 分界與折點")], size=12, gap=21)
    cv.math_px(W - Rm + 10, 218, "P_{u}/φ_{c}P_{n} ≥ 0.2 ：", 13, C["bmd"], "start", weight="700")
    cv.math_px(W - Rm + 10, 240, "P_{u}/φ_{c}P_{n} + (8/9)M_{u}/φ_{b}M_{n} ≤ 1",
               11.5, C["bmd"], "start")
    cv.math_px(W - Rm + 10, 278, "P_{u}/φ_{c}P_{n} &lt; 0.2 ：", 13, C["load"], "start", weight="700")
    cv.math_px(W - Rm + 10, 300, "P_{u}/(2φ_{c}P_{n}) + M_{u}/φ_{b}M_{n} ≤ 1",
               11.5, C["load"], "start")
    cv.text_px(W - Rm + 10, 340, "折點連續性驗算：", 12.5, C["text"], "start", weight="700")
    cv.text_px(W - Rm + 10, 360, f"高軸力式 → {M_B:.1f}", 12, C["muted"], "start")
    cv.text_px(W - Rm + 10, 379, f"低軸力式 → {M_B2:.1f}", 12, C["muted"], "start")
    cv.text_px(W - Rm + 10, 398, "兩式同值 ⇒ 折線連續", 12, C["bmd"], "start", weight="700")
    cv.text_px(W - Rm + 10, 428, f"φc = {PHI_C}（我國）", 12, C["muted"], "start")
    cv.text_px(W - Rm + 10, 447, f"φc = {PHI_C_AISC}（AISC）", 12, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 3　LRFD 之 P-M 交互作用曲線（子題二）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "以正規化座標繪製；折線為真實外凸強度曲面的內接（保守）近似",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"|k_AB| = {abs(K_AB):.3f} 小於 |k_BC| = {abs(K_BC):.3f} ⇒ AB 段較平、BC 段較陡",
               13, C["accent"])
    cv.text_px(W/2, H - 26,
               "低軸力段幾乎已達純彎強度，再減軸力也換不到多少彎矩容量",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2009-1-fig-3-pm.svg"))


# ══════════════════════════════════════════════════════════════
def fig1_scwb():
    """圖 1：強柱弱梁不等式兩側的 Σ 範圍（子題一）"""
    W, H = 860, 560
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    cx, cy = 330, 316          # 節點中心（像素）
    cw, bh = 46, 34            # 柱寬、梁高
    cl, bl = 148, 176          # 柱段長、梁段長

    # 柱（上下兩段）與梁（左右兩支）
    cv.rect_px(cx-cw/2, cy-cl-bh/2, cw, cl, "#DCE3EC", 0, C["member"], 2.4)
    cv.rect_px(cx-cw/2, cy+bh/2, cw, cl, "#DCE3EC", 0, C["member"], 2.4)
    cv.rect_px(cx-cw/2-bl, cy-bh/2, bl, bh, "#F3DEDA", 0, C["load"], 2.4)
    cv.rect_px(cx+cw/2, cy-bh/2, bl, bh, "#F3DEDA", 0, C["load"], 2.4)
    cv.rect_px(cx-cw/2, cy-bh/2, cw, bh, "#C9D3E0", 0, C["member"], 2.4)

    # 塑鉸（目標位置：梁端）
    for sgn in (-1, 1):
        px = cx + sgn*(cw/2 + 26)
        cv.parts.append(f'<circle cx="{px}" cy="{cy}" r="9" fill="{C["load"]}" '
                        f'stroke="#FFFFFF" stroke-width="2.2"/>')
    cv.text_px(cx, cy - bh/2 - 128, "柱段（上）", 13, C["member"], weight="700")
    cv.text_px(cx, cy + bh/2 + 128, "柱段（下）", 13, C["member"], weight="700")
    cv.text_px(cx - cw/2 - bl/2, cy - bh/2 - 22, "梁（左）", 13, C["load"], weight="700")
    cv.text_px(cx + cw/2 + bl/2, cy - bh/2 - 22, "梁（右）", 13, C["load"], weight="700")
    cv.text_px(cx + cw/2 + 26, cy + bh/2 + 42, "塑鉸應在此（梁端）", 12, C["load"], "start", weight="700")

    # Σ 範圍框
    cv.parts.append(f'<rect x="{cx-cw/2-12}" y="{cy-cl-bh/2-12}" width="{cw+24}" '
                    f'height="{2*cl+bh+24}" rx="12" fill="none" stroke="{C["member"]}" '
                    f'stroke-width="2" stroke-dasharray="7 5"/>')
    cv.parts.append(f'<rect x="{cx-cw/2-bl-12}" y="{cy-bh/2-12}" width="{2*bl+cw+24}" '
                    f'height="{bh+24}" rx="12" fill="none" stroke="{C["load"]}" '
                    f'stroke-width="2" stroke-dasharray="7 5"/>')

    # 不等式
    x0 = 534
    cv.text_px(x0, 176, "我國規範 (13.6-3)", 15, C["text"], "start", weight="700")
    cv.math_px(x0, 214, "Σ Z_{c}( F_{yc} − P_{uc}/A_{g} )", 16, C["member"], "start", weight="700")
    cv.parts.append(f'<line x1="{x0}" y1="232" x2="{x0+226}" y2="232" '
                    f'stroke="{C["text"]}" stroke-width="2.2"/>')
    cv.math_px(x0, 254, f"{OVERSTR_TW} × Σ Z_{{b}} F_{{yb}}", 16, C["load"], "start", weight="700")
    cv.math_px(x0 + 240, 234, "≥ 1.0", 17, C["text"], "start", weight="700")

    cv.text_px(x0, 292, "分子：接頭上、下兩柱段之和", 12.5, C["member"], "start", weight="700")
    cv.text_px(x0, 312, "　　　扣掉軸壓已佔用的應力容量", 12, C["muted"], "start")
    cv.text_px(x0, 340, "分母：接頭左、右兩梁之和", 12.5, C["load"], "start", weight="700")
    cv.text_px(x0, 360, f"　　　乘 {OVERSTR_TW}（材料超強＋應變硬化）", 12, C["muted"], "start")
    cv.text_px(x0, 396, "AISC 341 對照：", 12.5, C["accent"], "start", weight="700")
    cv.text_px(x0, 416, f"梁側改為 1.1R_y（R_y = {RY_LOW}～{RY_HIGH}）並另加 M_uv",
               12, C["accent"], "start")
    cv.text_px(x0, 436, f"A992／SN490 時 1.1R_y = {SH_AISC*RY_LOW:.2f}，與 {OVERSTR_TW} 相當",
               11.5, C["muted"], "start")
    cv.text_px(x0, 455, f"A36／SS400 時 1.1R_y = {SH_AISC*RY_HIGH:.2f}，比我國嚴 "
                        f"{100*(SH_AISC*RY_HIGH/OVERSTR_TW-1):.0f}%", 11.5, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 1　強柱弱梁：不等式兩側各自加總的範圍（子題一）", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "1.25 乘在「被高估的一方」＝梁側；柱側則要扣掉軸壓佔用的應力容量",
               13, C["muted"])
    cv.text_px(W/2, 84, "灰虛線框＝柱側 Σ（上下兩段）；紅虛線框＝梁側 Σ（左右兩支）",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "軸壓愈大、柱可提供的彎矩愈小 —— 這正是高軸力柱最難滿足強柱弱梁的原因",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2009-1-fig-1-scwb.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_mechanism():
    """圖 2：梁機構 vs 柱（軟層）機構"""
    PWD, PH = 470, 500
    NB, NS = 1, 3               # 一跨、三層
    SPAN, STORY = 1.0, 0.72
    XL, XR = -0.26, SPAN + 0.26
    YL, YH = -0.16, NS*STORY + 0.22
    Lm, Tm, Bm = 44, 110, 82
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    def frame(cv, drift):
        """drift(level) → 該樓層之側移量"""
        for lv in range(NS+1):
            y = lv*STORY
            if lv > 0:
                cv.line((drift(lv), y), (SPAN + drift(lv), y), C["member"], 4.6, cap="butt")
        for xb in (0.0, SPAN):
            pts = [(xb + drift(lv), lv*STORY) for lv in range(NS+1)]
            cv.poly(pts, C["member"], 4.6)
        cv.fixed_support((0, 0), 0, 15)
        cv.fixed_support((SPAN, 0), 0, 15)

    def hinge(cv, p):
        x, y = cv.P(p)
        cv.parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7.2" fill="{C["load"]}" '
                        f'stroke="#FFFFFF" stroke-width="2"/>')

    # ── 梁機構：各層均勻分攤 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("梁機構（設計目標）", "塑鉸分散於各層梁端＋柱腳")
    d1 = 0.06
    frame(p1, lambda lv: d1*lv)
    for lv in range(1, NS+1):
        for xb in (0.0, SPAN):
            hinge(p1, (xb + d1*lv, lv*STORY))
    hinge(p1, (0.0, 0.0)); hinge(p1, (SPAN, 0.0))
    n1 = 2*NS + 2
    p1.text_px(PWD/2, PH - 62, f"塑鉸 {n1} 處，分散全樓", 13.5, C["bmd"], weight="700")
    p1.text_px(PWD/2, PH - 38, "韌性高、能量消散大", 12.5, C["muted"])
    p1.text_px(PWD/2, PH - 16, "變形可控", 12.5, C["muted"])

    # ── 柱（軟層）機構：全部側移集中在最下層 ──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("柱機構／側移機構（須避免）", "塑鉸集中於同一層柱之上下端")
    d2 = d1*NS
    frame(p2, lambda lv: d2 if lv >= 1 else 0.0)
    for xb in (0.0, SPAN):
        hinge(p2, (xb, 0.0))
        hinge(p2, (xb + d2, STORY))
    n2 = 4
    p2.text_px(PWD/2, PH - 62, f"塑鉸僅 {n2} 處，集中在單層", 13.5, C["load"], weight="700")
    p2.text_px(PWD/2, PH - 38, "該層側移急遽增大", 12.5, C["muted"])
    p2.text_px(PWD/2, PH - 16, "⇒ 軟層崩塌", 12.5, C["load"], weight="700")

    compose([p1, p2], cols=2,
            title="圖 2　強柱弱梁要換到的東西：梁機構，而不是軟層機構",
            sub="兩圖的頂層側移量相同，差別只在「側移由幾層分攤」",
            note="容量設計：先指定哪裡該壞（梁端），再把不該壞的柱設計成強於該處的實際最大強度",
            path=os.path.join(OUT, "SS-2009-1-fig-2-mechanism.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_scwb(); fig2_mechanism(); fig3_pm()
    print(f"折點 B = ({B_PT[0]:.4f}, {B_PT[1]:.4f})  兩式驗算：{M_B:.6f} vs {M_B2:.6f}")
    print(f"k_AB = {K_AB:.6f} (= -8/9)   k_BC = {K_BC:.6f} (= -2)")
    print(f"|k_AB| < |k_BC| ⇒ {abs(K_AB) < abs(K_BC)}")
    print("done ->", OUT)
