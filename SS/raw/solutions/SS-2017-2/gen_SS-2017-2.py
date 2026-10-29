#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2017-2 圖解產生腳本（摩阻型螺栓接合：傳力機制與極限狀態）

本題為敘述題，圖上的數值全部取自規範表列值（台灣 ASD 表 C10.3-2 與 AISC 各版之 μ）。
執行：python3 gen_SS-2017-2.py   →   figs/*.svg
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
# 由 SS-2017-2 §4／§5／§6 之規範表列值取得
# ══════════════════════════════════════════════════════════════
PRELOAD_K = 0.70          # T_b = 0.70 F_u^b A_t（三版規範未變）      §4(一)
AT_OVER_AB = 0.75         # 螺紋處有效抗拉面積 ≈ 0.75 A_b            §4(一)
MU_TW, MU_05, MU_10 = 0.33, 0.35, 0.30      # A 類滑動係數           §6.2
MU_B = 0.50               # B 類（噴砂）                              §6.2
DU = 1.13                 # 實際／規定最小預拉力之比（AISC）           §4(一)

# 台灣 ASD 表 C10.3-2（標準孔），單位 tf/cm^2                          §5
FV = {
    "A325 摩阻型":       1.19,
    "A325 承壓型 N":     1.48,
    "A325 承壓型 X":     2.11,
    "A490 摩阻型":       1.47,
    "A490 承壓型 N":     1.97,
    "A490 承壓型 X":     2.81,
}
RATIO_A490 = FV["A490 摩阻型"] / FV["A490 承壓型 X"]      # 0.523

# 孔型對 φ 的影響（AISC 360-10 起）                                    §6.1
PHI_HOLE = (("標準孔／短槽孔垂直力向", 1.00),
            ("超大孔／短槽孔平行力向", 0.85),
            ("長槽孔", 0.70))


# ══════════════════════════════════════════════════════════════
def fig1_mechanism():
    """圖 1：預拉力 → 夾緊力 → 接觸面摩擦（雙剪）"""
    W, H = 940, 520
    XL, XR = -13.0, 13.0
    YL, YH = -6.2, 6.2
    Tm, Bm = 118, 98
    sx = min((W-120)/(XR-XL), (H-Tm-Bm)/(YH-YL))
    ox = (W - (XR-XL)*sx)/2 - XL*sx          # 水平置中
    cv = Canvas(W, H, sx=sx, ox=ox, oy=Bm - YL*sx, bg="#FFFFFF")

    T = 1.4                                   # 每片板厚（繪圖單位）
    XO0, XO1 = -11.5, 2.0                     # 外板 x 範圍
    XM0, XM1 = -3.0, 11.5                     # 中板 x 範圍

    # 中板（被兩片外板夾住）
    cv.polygon([(XM0, -T/2), (XM1, -T/2), (XM1, T/2), (XM0, T/2)], "#EDF1F6", C["member"], 2.0)
    # 上、下外板
    for sgn in (1, -1):
        y0, y1 = sgn*T/2, sgn*3*T/2
        cv.polygon([(XO0, min(y0, y1)), (XO1, min(y0, y1)),
                    (XO1, max(y0, y1)), (XO0, max(y0, y1))], "#DCE3EC", C["member"], 2.0)
    cv.text_px(cv.X(XO0) + 10, cv.Y(T), "板 A（外）", 11.5, C["muted"], "start")
    cv.text_px(cv.X(XM1) - 10, cv.Y(0), "板 B（中）", 11.5, C["muted"], "end")

    # 螺栓：桿 + 頭 + 螺帽
    cv.polygon([(-1.0, -3*T/2), (1.0, -3*T/2), (1.0, 3*T/2), (-1.0, 3*T/2)],
               "#FFFFFF", C["member"], 2.0)
    for yy in (3*T/2, -3*T/2 - 0.85):
        cv.polygon([(-2.2, yy), (2.2, yy), (2.2, yy+0.85), (-2.2, yy+0.85)],
                   "#C9D3E0", C["member"], 2.0)

    # 預拉力（螺栓桿內為拉力，對板則形成夾緊壓力）
    cv.arrow((0, 0.5), (0, 3*T/2 + 0.6), C["load"], 3.0, 10)
    cv.arrow((0, -0.5), (0, -3*T/2 - 0.6), C["load"], 3.0, 10)
    cv.math_px(cv.X(0) + 16, cv.Y(3*T/2 + 1.9), f"T_{{b}} = {PRELOAD_K}F_{{u}}A_{{t}}",
               14, C["load"], "start", weight="700")
    cv.text_px(cv.X(0) + 16, cv.Y(3*T/2 + 1.9) + 20, "螺栓預拉力 → 板間夾緊力",
               11.5, C["load"], "start")

    # 兩個接觸面與其上的摩擦力
    for sgn, lab in ((1, "接觸面 1"), (-1, "接觸面 2")):
        y = sgn*T/2
        cv.line((XM0, y), (XO1, y), C["bmd"], 3.6)
        cv.arrow((-0.4, y + sgn*0.42), (-4.6, y + sgn*0.42), C["bmd"], 2.6, 9)
        cv.text_px(cv.X(-4.9), cv.Y(y + sgn*0.42), lab, 11.5, C["bmd"], "end", weight="700")
    cv.math_px(cv.X(-8.6), cv.Y(4.1), f"f = μ · T_{{b}}", 15, C["bmd"], weight="700")
    cv.text_px(cv.X(-8.6), cv.Y(4.1) + 20, "（每支、每個接觸面）", 11.5, C["bmd"])

    # 外力 V
    cv.arrow((XO0 - 2.6, T), (XO0 - 0.3, T), C["compr"], 3.4, 12)
    cv.math_px(cv.X(XO0 - 1.4), cv.Y(T) - 16, "V", 17, C["compr"], weight="700")
    cv.arrow((XM1 + 2.6, 0), (XM1 + 0.3, 0), C["compr"], 3.4, 12)
    cv.math_px(cv.X(XM1 + 1.4), cv.Y(0) - 16, "V", 17, C["compr"], weight="700")

    cv.text_px(cv.X(0), cv.Y(-3*T/2 - 2.3), "滑動前螺栓桿幾乎不受剪、孔壁不承壓",
               12.5, C["load"], weight="700")

    cv.text_px(W/2, 34, "圖 1　摩阻型接合的剪力傳遞機制（雙剪，n_s = 2）", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "預緊 → 板間夾緊力 → 接觸面摩擦力抵抗剪力；力完全不經過螺栓桿",
               13, C["muted"])
    cv.text_px(W/2, 84,
               f"A_t 是螺紋處有效抗拉面積（約 {AT_OVER_AB:g}A_b）；誤用全斷面積會把預拉力高估 "
               f"{100*(1/AT_OVER_AB - 1):.0f}%",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               f"AISC：R_n = μ·D_u·h_f·T_b·n_s（D_u = {DU}）；台灣 ASD 則直接查表列容許剪應力",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2017-2-fig-1-mechanism.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_slip_behavior():
    """圖 2：荷重–滑移行為與四個極限狀態的先後"""
    W, H = 940, 580
    Lm, Rm, Tm, Bm = 96, 280, 116, 96
    XMAX = 1.0                    # 正規化滑移量
    sxx = (W-Lm-Rm)/XMAX
    # 縱軸以 A490 標準孔之表列容許剪應力為刻度（tf/cm^2）
    YMAX = FV["A490 承壓型 X"] * 1.30
    syy = (H-Tm-Bm)/YMAX
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    X = lambda t: Lm + t*sxx
    Y = lambda v: H - Bm - v*syy

    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{X(XMAX)+16}" y2="{Y(0)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{Lm}" y2="{Y(YMAX)-8}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.text_px(X(XMAX/2), Y(0) + 28, "滑移量 →", 13, C["muted"])
    cv.text_px(Lm + 8, Y(YMAX) - 20, "接合承載力", 13, C["muted"], "start")

    SLIP = FV["A490 摩阻型"]
    BEAR = FV["A490 承壓型 X"]
    for v, col, lab in ((SLIP, C["bmd"], f"滑動強度 {SLIP} tf/cm²（摩阻型表列）"),
                        (BEAR, C["load"], f"螺栓剪力強度 {BEAR} tf/cm²（承壓型 X 表列）")):
        cv.parts.append(f'<line x1="{Lm}" y1="{Y(v)}" x2="{X(XMAX)}" y2="{Y(v)}" '
                        f'stroke="{col}" stroke-width="1.6" stroke-dasharray="6 4"/>')
        cv.text_px(X(XMAX) + 10, Y(v), lab, 11.5, col, "start", weight="700")

    # 荷重–滑移路徑（分段：摩擦線性 → 滑動平台 → 承壓再上升 → 破壞）
    T1, T2, T3 = 0.10, 0.30, 0.86
    pts = []
    n = 120
    for i in range(n+1):
        t = XMAX*i/n
        if t <= T1:
            v = SLIP * t/T1
        elif t <= T2:
            v = SLIP                                   # 滑動：載重幾乎不增、位移增加
        elif t <= T3:
            v = SLIP + (BEAR - SLIP)*((t-T2)/(T3-T2))**0.75   # 轉承壓型
        else:
            v = BEAR
        pts.append((X(t), Y(v)))
    cv.parts.append('<polyline points="' + " ".join(f"{a:.2f},{b:.2f}" for a, b in pts) +
                    f'" fill="none" stroke="{C["compr"]}" stroke-width="3.4" '
                    f'stroke-linejoin="round"/>')

    # 四個極限狀態的標記
    marks = ((T1, SLIP, "① 接觸面滑動", "主要極限狀態", C["bmd"]),
             (T2 + (T3-T2)*0.35, SLIP + (BEAR-SLIP)*0.35**0.75,
              "② 孔壁承壓／撕出", "滑動後螺栓桿接觸孔壁", C["accent"]),
             (T3, BEAR, "③ 螺栓桿剪力破壞", "接合最終破壞", C["load"]))
    for t, v, nm, note, col in marks:
        cv.parts.append(f'<circle cx="{X(t):.2f}" cy="{Y(v):.2f}" r="6" fill="{col}" '
                        f'stroke="#FFFFFF" stroke-width="2"/>')
        cv.text_px(X(t), Y(v) - 24, nm, 12.5, col, weight="700")
        cv.text_px(X(t), Y(v) - 8, note, 11, C["muted"])
    cv.text_px(X((T1+T2)/2), Y(SLIP) + 24, "滑動平台：摩擦已喪失", 11.5, C["bmd"])

    cv.text_px(W - Rm + 10, 392, "④ 板件淨斷面斷裂／塊狀撕裂", 12, C["muted"], "start")
    cv.text_px(W - Rm + 10, 412, "　 （另行檢核，不在此曲線上）", 12, C["muted"], "start")
    cv.text_px(W - Rm + 10, 448, "滑動之「分類」：", 12.5, C["text"], "start", weight="700")
    cv.text_px(W - Rm + 10, 470, "使用性極限 → 以服務載重檢核", 11.5, C["muted"], "start")
    cv.text_px(W - Rm + 10, 490, "強度極限 → 以因數化載重檢核", 11.5, C["muted"], "start")
    cv.text_px(W - Rm + 10, 522,
               "AISC 360-10 起 φ 改依孔型（"
               + "／".join(f"{ph:.2f}" for _, ph in PHI_HOLE) + "）",
               11.5, C["accent"], "start", weight="700")

    cv.text_px(W/2, 34, "圖 2　摩阻型接合的荷重–滑移行為與極限狀態先後", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "縱軸刻度為台灣 ASD 表 C10.3-2 之 A490 標準孔表列容許剪應力",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "滑動不是「破壞」，而是傳力機制的切換——答題只寫「滑動」而不說後續，等於漏掉一半",
               12.5, C["accent"])
    cv.text_px(W/2, H - 26,
               "設計優先序：滑動阻抗 ≥ 設計剪力；若容許滑動，才接著檢核螺栓剪力、承壓與淨斷面",
               13, C["muted"])
    cv.save(os.path.join(OUT, "SS-2017-2-fig-2-slip-behavior.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_strength_compare():
    """圖 3：摩阻型 vs 承壓型的容許剪應力（台灣 ASD 表列）"""
    W, H = 940, 500
    cv = Canvas(W, H, sx=1.0, bg="#FFFFFF")
    x0, bw = 240, 460
    order = ("A325 摩阻型", "A325 承壓型 N", "A325 承壓型 X",
             "A490 摩阻型", "A490 承壓型 N", "A490 承壓型 X")
    peak = max(FV.values()) * 1.10
    for i, nm in enumerate(order):
        v = FV[nm]
        col = C["bmd"] if "摩阻" in nm else (C["compr"] if "N" in nm else C["load"])
        y = 128 + i*46
        cv.text_px(x0 - 14, y, nm, 12.5, C["text"], "end",
                   weight="700" if "摩阻" in nm else "400")
        cv.rect_px(x0, y-14, bw, 28, "#EDF1F6", 6)
        cv.rect_px(x0, y-14, bw*v/peak, 28, col, 6)
        cv.text_px(x0 + bw*v/peak + 10, y, f"{v:.2f}", 12.5, col, "start", weight="700")
    # A490 之比較線
    y1 = 128 + 3*46
    y2 = 128 + 5*46
    xa, xb = x0 + bw*FV["A490 摩阻型"]/peak, x0 + bw*FV["A490 承壓型 X"]/peak
    cv.parts.append(f'<line x1="{xa}" y1="{y1+16}" x2="{xa}" y2="{y2+26}" '
                    f'stroke="{C["bmd"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    cv.parts.append(f'<line x1="{xb}" y1="{y2+16}" x2="{xb}" y2="{y2+26}" '
                    f'stroke="{C["load"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    cv.text_px((xa+xb)/2, y2 + 42, f"A490：摩阻型只有承壓型 X 的 {RATIO_A490*100:.0f}%",
               13, C["accent"], weight="700")

    cv.text_px(W/2, 34, "圖 3　摩阻型不是「更強」，而是「更嚴格地不允許位移」", 17.5,
               C["text"], weight="700")
    cv.text_px(W/2, 58, "台灣 ASD 表 C10.3-2（標準孔）之容許剪應力，單位 tf/cm²",
               13, C["muted"])
    cv.text_px(W/2, 84,
               "摩阻型的上限由「μ × 夾持力」決定，而夾持力受限於預拉力只能到 0.7F_u；"
               "承壓型可用到螺栓的剪力強度",
               12.5, C["accent"])
    cv.text_px(W/2, H - 46,
               f"滑動係數 μ（A 類）：台灣 {MU_TW}／AISC 360-05 {MU_05}／360-10 起 {MU_10}；"
               f"B 類（噴砂）三版皆 {MU_B}",
               13, C["muted"])
    cv.text_px(W/2, H - 22,
               "若接合無避免滑動之需求，採承壓型較經濟——這是設計選型的關鍵判斷",
               12.5, C["muted"])
    cv.save(os.path.join(OUT, "SS-2017-2-fig-3-strength-compare.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_mechanism(); fig2_slip_behavior(); fig3_strength_compare()
    print(f"預拉力係數={PRELOAD_K}  At/Ab={AT_OVER_AB}  誤用 Ab 高估 {100*(1/AT_OVER_AB-1):.0f}%")
    print(f"A490 摩阻/承壓X = {FV['A490 摩阻型']}/{FV['A490 承壓型 X']} = {RATIO_A490:.3f}")
    print(f"μ(A 類)：台灣 {MU_TW}／360-05 {MU_05}／360-10 {MU_10}；B 類 {MU_B}")
    print("done ->", OUT)
