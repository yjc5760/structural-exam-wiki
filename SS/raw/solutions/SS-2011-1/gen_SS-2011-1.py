#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2011-1 圖解產生腳本（AISC 2010 Chapter C 直接分析法四子題）

本題無附圖、無數值答案；四張圖各自對應一個子題，且各攔一種「答得似是而非」的錯。
執行：python3 gen_SS-2011-1.py   →   figs/*.svg
"""
import sys, os, math
# struct-diagram 的 primitives 取自本知識庫自帶的 skill 副本（repo 相對路徑，故可原地重跑）；
# 若把本檔搬到別處，設環境變數 SD_SKILL 指向 struct-diagram 目錄即可。
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose, column_shape, member_shape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")

# ══════════════════════════════════════════════════════════════
# 由 SS-2011-1 §4 之規範條文取得（本題為概念題，數字全為規範定值）
# ══════════════════════════════════════════════════════════════
TILT      = 1/500      # 初始傾斜 Δ0/L（AISC 施工容許誤差）      §4 (二)
NI_COEF   = 0.002      # N_i = 0.002·α·Y_i（= Δ0/L）             §4 (二)
NI_ALT    = 0.001      # τ_b = 1 之替代規定所需額外假想水平力     §4 (三)
EI_RED    = 0.8        # 無條件基本折減                          §4 (三)
TAUB_BRK  = 0.5        # τ_b 之分段門檻 αP_r/P_y                 §4 (三)
ALPHA_LR  = 1.0        # LRFD                                    §4 (四)
ALPHA_ASD = 1.6        # ASD（本題子題四）                        §4 (四)
OMEGA_C   = 1.67       # ASD 之安全係數（與 α 是兩回事）          §4 (四)
GAMMA_D, GAMMA_L = 1.2, 1.6      # LRFD 重力組合係數             §4 (四)
LD_TYPICAL = 3.0       # AISC 標定所用之 L/D（給出 γ = 1.5）      §4 (四)


def tau_b(x):
    """x = αP_r/P_y"""
    return 1.0 if x <= TAUB_BRK else max(0.0, 4*x*(1 - x))


def gamma(ld):
    """(1.2D + 1.6L)/(D + L)，以 L/D 為變數"""
    return (GAMMA_D + GAMMA_L*ld) / (1 + ld)


# ══════════════════════════════════════════════════════════════
def fig1_second_order():
    """圖 1：P-Δ 與 P-δ（子題一）"""
    PW, PH = 470, 470
    Lm, Tm, Bm = 40, 112, 78
    XL, XR, YL, YH = -0.80, 0.62, -0.16, 1.52
    sx = min((PW - 2*Lm) / (XR - XL), (PH - Tm - Bm) / (YH - YL))
    OX = Lm - XL*sx
    OY = Bm - YL*sx

    D = 0.20                    # 繪圖用層間側移 Δ/L
    d = 0.085                   # 繪圖用構材撓曲 δ/L

    # ── 格 1：P-Δ ──
    p1 = Canvas(PW, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("P-Δ：層間側移效應", "整體結構穩定")
    p1.line((0, 0), (0, 1), C["ghost"], 3.0, dash="7 5")
    # 柱底固接、柱頂側移 Δ 且無轉角（雙曲率）
    p1.poly(column_shape((0, 0), 1.0, D, 0.0, 0.0, 0.0), C["deform"], 5.2)
    p1.fixed_support((0, 0), 0, 20)
    p1.arrow((D, 1.42), (D, 1.04), C["load"], 3.4, 11)
    p1.math_px(p1.X(D) + 14, p1.Y(1.26), "P", 17, C["load"], "start", weight="700")
    p1.arrow((D - 0.62, 1.0), (D - 0.06, 1.0), C["load"], 3.0, 10)
    p1.math_px(p1.X(D - 0.34), p1.Y(1.0) - 15, "H", 15, C["load"], weight="700")
    p1.dim((0, 1.0), (D, 1.0), "Δ", off=-30, label_off=-13, color=C["deform"])
    p1.math_px(PW/2, PH - 46, "M_{add} = P · Δ", 17, C["accent"], weight="700")
    p1.text_px(PW/2, PH - 22, "由 B_2（層）處理", 12.5, C["muted"])

    # ── 格 2：P-δ ──
    p2 = Canvas(PW, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("P-δ：構材撓曲效應", "構材本身的彎矩分布")
    p2.line((0, 0), (0, 1), C["ghost"], 3.0, dash="7 5")
    # 兩端不動、構材中段外凸（單曲率半正弦）
    p2.poly(member_shape((0, 0), (0, 1), lambda xi: -d*math.sin(math.pi*xi)),
            C["deform"], 5.2)
    # 構材自由體：兩端各施軸壓 P 與端彎矩（不畫支承——P-δ 是「兩端當作不動點」的現象）
    p2.arrow((0, 1.42), (0, 1.04), C["load"], 3.4, 11)
    p2.math_px(p2.X(0) + 14, p2.Y(1.26), "P", 17, C["load"], "start", weight="700")
    p2.arrow((0, -0.14), (0, -0.02), C["load"], 3.4, 9)
    p2.moment_arrow((0, 1.0), r=26, ccw=True, color=C["accent"], w=2.6, span=250, start=120)
    p2.moment_arrow((0, 0.0), r=26, ccw=False, color=C["accent"], w=2.6, span=250, start=120)
    p2.dim((0, 0.5), (d, 0.5), "δ", off=0, label_off=-13, color=C["deform"])
    p2.line((0, 0.5), (0, 0.5), C["muted"], 1)
    p2.math_px(PW/2, PH - 46, "M_{add} = P · δ", 17, C["accent"], weight="700")
    p2.text_px(PW/2, PH - 22, "由 B_1（構材）處理；兩端視為不動點", 12.5, C["muted"])

    compose([p1, p2], cols=2,
            title="圖 1　二階分析要同時涵蓋的兩種效應（子題一）",
            sub="一階分析以未變形幾何建立平衡；二階分析以「變形後」幾何建立平衡",
            note="兩者缺一不可——只寫 P-Δ 而漏 P-δ 是本子題最常見的失分",
            path=os.path.join(OUT, "SS-2011-1-fig-1-p-delta.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_imperfection():
    """圖 2：初始不完美的兩種模擬方式（子題二）"""
    PW, PH = 470, 470
    Lm, Tm, Bm = 40, 112, 78
    XL, XR, YL, YH = -0.86, 1.02, -0.16, 1.50
    sx = min((PW - 2*Lm) / (XR - XL), (PH - Tm - Bm) / (YH - YL))
    OX = Lm - XL*sx
    OY = Bm - YL*sx
    TILT_DRAW = 0.14                 # 傾斜的繪圖放大量（實際為 1/500，畫不出來）

    p1 = Canvas(PW, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("方法一：直接設置幾何偏移", "節點座標直接偏移")
    p1.line((0, 0), (0, 1), C["ghost"], 3.0, dash="7 5")
    p1.line((0, 0), (TILT_DRAW, 1), C["member"], 5.6, cap="butt")
    p1.line((TILT_DRAW, 1), (TILT_DRAW + 0.85, 1), C["member"], 5.0, cap="butt")
    p1.fixed_support((0, 0), 0, 18)
    p1.dim((0, 1.0), (TILT_DRAW, 1.0), f"Δ_{{0}} = L/500", off=-52, label_off=-15,
           color=C["accent"])
    p1.arrow((TILT_DRAW, 1.36), (TILT_DRAW, 1.05), C["load"], 3.2, 11)
    p1.math_px(p1.X(TILT_DRAW) + 16, p1.Y(1.20), "Y_{i}", 15, C["load"], "start", weight="700")
    p1.text_px(PW/2, PH - 46, "幾何不完美「畫進模型裡」", 13.5, C["text"], weight="700")
    p1.text_px(PW/2, PH - 22, "需修改結構幾何，實務上麻煩", 12.5, C["muted"])

    p2 = Canvas(PW, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("方法二：等效假想水平力 N_{i}", "幾何維持完美，改加水平力")
    p2.line((0, 0), (0, 1), C["member"], 5.6, cap="butt")
    p2.line((0, 1), (0.85, 1), C["member"], 5.0, cap="butt")
    p2.fixed_support((0, 0), 0, 18)
    p2.arrow((0, 1.36), (0, 1.05), C["load"], 3.2, 11)
    p2.math_px(p2.X(0) + 14, p2.Y(1.22), "Y_{i}", 15, C["load"], "start", weight="700")
    p2.arrow((-0.70, 1.0), (-0.08, 1.0), C["accent"], 3.4, 12)
    p2.math_px(p2.X(-0.39), p2.Y(1.0) - 16, "N_{i}", 16, C["accent"], weight="700")
    p2.math_px(PW/2, PH - 68, f"N_{{i}} = {NI_COEF} · α · Y_{{i}}", 17, C["accent"], weight="700")
    p2.text_px(PW/2, PH - 44, f"α = {ALPHA_LR:g}（LRFD）／{ALPHA_ASD:g}（ASD）", 12.5, C["muted"])
    p2.text_px(PW/2, PH - 22, f"Y_i 是該層「重力載重」，不是 P_r", 12.5, C["load"], weight="700")

    compose([p1, p2], cols=2,
            title="圖 2　起始不完美的兩種等效模擬（子題二）",
            sub=f"係數 {NI_COEF} 就是 Δ0/L = 1/{int(1/TILT)}——傾斜量與假想水平力比例是同一個數",
            note=f"另有替代規定：一律取 τb = 1，但須再加 {NI_ALT}·Yi（見圖 3）；圖中傾斜量為示意放大",
            path=os.path.join(OUT, "SS-2011-1-fig-2-imperfection.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_taub():
    """圖 3：勁度折減（子題三）"""
    W, H = 820, 520
    Lm, Rm, Tm, Bm = 96, 246, 110, 82
    XMAX, YMAX = 1.08, 1.18
    sx = min((W-Lm-Rm) / XMAX, (H-Tm-Bm) / YMAX)
    cv = Canvas(W, H, sx=sx, ox=Lm, oy=Bm, bg="#FFFFFF")

    cv.arrow((0, 0), (XMAX, 0), C["muted"], 1.8, 9)
    cv.arrow((0, 0), (0, YMAX), C["muted"], 1.8, 9)
    cv.math((XMAX, 0), "α P_{r}/P_{y}", 14.5, C["muted"], "start", dx=6, dy=16)
    cv.text((0, YMAX), "折減倍率", 14, C["muted"], "end", dx=-10)
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        cv.line((0, v), (XMAX, v), C["border"], 1.0)
        cv.text_px(cv.X(0) - 10, cv.Y(v), f"{v:.1f}", 12, C["muted"], "end")
        cv.text_px(cv.X(v), cv.Y(0) + 18, f"{v:.1f}", 12, C["muted"])

    n = 300
    xs = [XMAX*i/n for i in range(n+1)]
    # τ_b 本身
    cv.poly([(x, tau_b(x)) for x in xs], C["accent"], 3.0)
    # 0.8·τ_b（實際用於分析的彎曲勁度倍率）
    cv.poly([(x, EI_RED*tau_b(x)) for x in xs], C["bmd"], 3.4)
    # 0.8（軸向勁度倍率，無條件）
    cv.line((0, EI_RED), (XMAX, EI_RED), C["compr"], 2.6, dash="7 5")

    cv.dot((TAUB_BRK, 1.0), 5.4, fill=C["accent"])
    cv.line((TAUB_BRK, 0), (TAUB_BRK, 1.0), C["accent"], 1.4, dash="5 4")
    cv.text_px(cv.X(TAUB_BRK), cv.Y(1.0) - 18, f"分段門檻 {TAUB_BRK:g}", 12.5,
               C["accent"], weight="700")
    cv.dot((1.0, 0.0), 5.4, fill=C["accent"])
    cv.text_px(cv.X(1.0) - 6, cv.Y(0.0) - 30, "τ_b = 0（全斷面降伏）", 12.5, C["accent"], "end", weight="700")

    cv.legend(W - Rm + 8, 168,
              [(C["accent"], "τ_b（條件折減）"),
               (C["bmd"], "0.8·τ_b：彎曲勁度 EI*"),
               (C["compr"], "0.8：軸向勁度 EA*")], size=12, gap=22)
    cv.math_px(W - Rm + 8, 248, "EI^{*} = 0.8 τ_{b} EI", 14, C["bmd"], "start", weight="700")
    cv.math_px(W - Rm + 8, 272, "EA^{*} = 0.8 EA", 14, C["compr"], "start", weight="700")
    cv.text_px(W - Rm + 8, 306, "0.8 無條件生效；", 12.5, C["text"], "start", weight="700")
    cv.text_px(W - Rm + 8, 326, f"τ_b 只在超過 {TAUB_BRK:g} 後", 12.5, C["text"], "start")
    cv.text_px(W - Rm + 8, 346, "才額外折減", 12.5, C["text"], "start")

    cv.text_px(W/2, 34, "圖 3　直接分析法的勁度折減（子題三）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "兩個層次要分清楚：0.8 是無條件的基本折減，τ_b 才是有條件的額外折減",
               13, C["muted"])
    cv.text_px(W/2, 84, f"τ_b 在門檻處為 4(0.5)(0.5) = 1.0，函數連續、無跳躍", 12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"替代規定：一律取 τ_b = 1，但所有組合須另加 N_i = {NI_ALT}·Y_i",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2011-1-fig-3-taub.svg"))


# ══════════════════════════════════════════════════════════════
def fig4_alpha():
    """圖 4：ASD 載重係數 α = 1.6 的由來（子題四）"""
    W, H = 820, 520
    Lm, Rm, Tm, Bm = 96, 232, 110, 82
    XMAX = 10.0
    YLO, YHI = 1.10, 1.70
    sx_x = (W-Lm-Rm) / XMAX
    sy = (H-Tm-Bm) / (YHI-YLO)
    # 本圖 x、y 尺度不同，故直接以像素座標作圖
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda ld: Lm + ld*sx_x
    Y = lambda g: H - Bm - (g-YLO)*sy

    # 軸
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(YLO)}" x2="{X(XMAX)+16}" y2="{Y(YLO)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(YLO)}" x2="{Lm}" y2="{Y(YHI)-10}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.text_px(X(XMAX) + 22, Y(YLO) + 4, "L/D", 14, C["muted"], "start")
    cv.math_px(Lm, Y(YHI) - 24, "(1.2D + 1.6L)/(D + L)", 14, C["muted"], "middle")
    for g in (1.2, 1.3, 1.4, 1.5, 1.6):
        cv.parts.append(f'<line x1="{Lm}" y1="{Y(g)}" x2="{X(XMAX)}" y2="{Y(g)}" '
                        f'stroke="{C["border"]}" stroke-width="1"/>')
        cv.text_px(Lm - 12, Y(g), f"{g:.1f}", 12, C["muted"], "end")
    for ld in (0, 2, 4, 6, 8, 10):
        cv.text_px(X(ld), Y(YLO) + 20, f"{ld}", 12, C["muted"])

    # 曲線
    n = 400
    pts = " ".join(f"{X(XMAX*i/n):.2f},{Y(gamma(XMAX*i/n)):.2f}" for i in range(n+1))
    cv.parts.append(f'<polyline points="{pts}" fill="none" stroke="{C["bmd"]}" '
                    f'stroke-width="3.4" stroke-linejoin="round"/>')

    # 上下界與標定點
    for g, col in ((GAMMA_D, C["muted"]), (GAMMA_L, C["load"])):
        cv.parts.append(f'<line x1="{Lm}" y1="{Y(g)}" x2="{X(XMAX)}" y2="{Y(g)}" '
                        f'stroke="{col}" stroke-width="2" stroke-dasharray="7 5"/>')
    cv.text_px(X(XMAX) + 10, Y(GAMMA_L), f"上界 {GAMMA_L:g}", 12.5, C["load"], "start", weight="700")
    cv.text_px(X(XMAX) + 10, Y(GAMMA_L) + 20, "← 規範取此值", 12, C["load"], "start", weight="700")
    cv.text_px(X(XMAX*0.62), Y(GAMMA_D) - 15, f"L → 0 之下界 {GAMMA_D:g}（純靜載）",
               12.5, C["muted"], "middle", weight="700")
    cv.text_px(X(XMAX*0.30), Y(GAMMA_L) - 16, "L 遠大於 D 時趨近上界",
               12, C["load"], "middle")

    g3 = gamma(LD_TYPICAL)
    cv.parts.append(f'<circle cx="{X(LD_TYPICAL):.2f}" cy="{Y(g3):.2f}" r="5.6" '
                    f'fill="{C["accent"]}" stroke="#FFFFFF" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(g3)}" x2="{X(LD_TYPICAL)}" y2="{Y(g3)}" '
                    f'stroke="{C["accent"]}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    cv.text_px(X(LD_TYPICAL) + 12, Y(g3) - 14,
               f"L/D = {LD_TYPICAL:g} 時 = {g3:.2f}（AISC 標定值，360-05 用此數）",
               12, C["accent"], "start", weight="700")

    # 與 Ω 的區別
    cv.rect_px(W - Rm + 4, H - 190, Rm - 22, 96, "#FDF3F2", 10, C["load"], 1.2)
    cv.text_px(W - Rm + 16, H - 166, "1.6 是「載重係數 α」", 12.5, C["load"], "start", weight="700")
    cv.text_px(W - Rm + 16, H - 145, f"不是安全係數 Ω_c = {OMEGA_C}", 12.5, C["text"], "start")
    cv.text_px(W - Rm + 16, H - 124, "兩者數值接近純屬巧合", 12, C["muted"], "start")
    cv.text_px(W - Rm + 16, H - 106, "內力算完要再除以 1.6", 12, C["muted"], "start")

    cv.text_px(W/2, 34, "圖 4　ASD 載重係數 α = 1.6 的由來（子題四）", 17.5, C["text"], weight="700")
    cv.text_px(W/2, 58, "二階效應對載重非線性 ⇒ 必須先把 ASD 載重抬到 LRFD（強度）位階再分析",
               13, C["muted"])
    cv.text_px(W/2, 84, "比值區間為 1.2～1.6，規範取上界 1.6（較典型值 1.5 保守）", 12.5, C["bmd"])
    cv.save(os.path.join(OUT, "SS-2011-1-fig-4-alpha.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_second_order(); fig2_imperfection(); fig3_taub(); fig4_alpha()
    print(f"tau_b(0.5)={tau_b(0.5):.3f}  tau_b(0.75)={tau_b(0.75):.3f}  tau_b(1.0)={tau_b(1.0):.3f}")
    print(f"gamma(L/D=3)={gamma(3):.3f}  gamma(0)={gamma(0):.2f}  gamma(inf)->{GAMMA_L:g}")
    print("done ->", OUT)
