#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2016-2 圖解產生腳本（回銲 End Return）

所有長度規定取自解題檔 §4／§5 所引之「鋼構造建築物鋼結構施工規範 §4.1.5」：
(1)~(3) 有效長度含端彎、(6) ≥4w、(7) 每段 ≥4w 且 ≥40 mm、(8) 搭接 ≥5t 且 ≥25 mm、
(9) 繞角銲 2w ≤ ℓ ≤ 4w。圖 2 之交會點 w = 40/4 由這些值現算。
執行：python3 gen_SS-2016-2.py   →   figs/*.svg
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
# 規範 §4.1.5 之係數（由 SS-2016-2 §4 三、§5.2、§5.3 取得）
# ══════════════════════════════════════════════════════════════
RET_LO_K = 2.0        # (9) 繞角銲長度下限係數 ×w
RET_HI_K = 4.0        # (9) 繞角銲長度上限係數 ×w
LMIN_K   = 4.0        # (6) 最小有效長度係數 ×w
SEG_K    = 4.0        # (7) 斷續銲每段下限係數 ×w
SEG_MM   = 40.0       # (7) 斷續銲每段下限絕對值（mm）
LAP_K    = 5.0        # (8) 搭接長度 ≥ 5 t_min
LAP_MM   = 25.0       # (8) 搭接長度 ≥ 25 mm
THROAT_K = 0.707      # (1) 等腳填角銲有效喉深 t_e = 0.707 w

# 數值示例
W    = 8.0            # mm 銲腳尺寸
LMAIN = 200.0         # mm 主填角銲道長度
RET  = 3.0*W          # mm 實際採用之回銲長度（取 2w～4w 之中間值 3w = 24）

RET_LO, RET_HI = RET_LO_K*W, RET_HI_K*W            # 16、32
L_TW   = LMAIN + 2*RET                             # 國內規範：含兩端端彎
L_NORET = LMAIN                                    # 誤法一：端彎不計入
L_DEDUCT = LMAIN - 2*W                             # 誤法二：兩端各扣 1w
W_CROSS = SEG_MM/SEG_K                             # 斷續銲兩個下限的交會點 = 10 mm


def dim_h(cv, x1, x2, y, lab, col, above=True):
    """水平尺寸線（像素座標）"""
    cv.parts.append(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
                    f'stroke="{col}" stroke-width="1.6"/>')
    for xx in (x1, x2):
        cv.parts.append(f'<line x1="{xx:.1f}" y1="{y-5:.1f}" x2="{xx:.1f}" '
                        f'y2="{y+5:.1f}" stroke="{col}" stroke-width="1.6"/>')
    cv.text_px((x1+x2)/2, y - 11 if above else y + 12, lab, 11, col, weight="700")


def dim_v(cv, y1, y2, x, lab, col, anchor="start"):
    """垂直尺寸線（像素座標）"""
    cv.parts.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" '
                    f'stroke="{col}" stroke-width="1.6"/>')
    for yy in (y1, y2):
        cv.parts.append(f'<line x1="{x-5:.1f}" y1="{yy:.1f}" x2="{x+5:.1f}" '
                        f'y2="{yy:.1f}" stroke="{col}" stroke-width="1.6"/>')
    dx = 8 if anchor == "start" else -8
    cv.text_px(x + dx, (y1+y2)/2, lab, 11, col, anchor, weight="700")


# ══════════════════════════════════════════════════════════════
def fig1_end_return():
    """圖 1：回銲的幾何、長度規定，以及有效長度怎麼算"""
    PWD, PH = 520, 470
    XL, XR, YL, YH = -18.0, 148.0, -20.0, 78.0
    Lm, Tm, Bm = 34, 106, 128
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    # ── 格 1：幾何 ──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("回銲＝繞過轉角再銲一小段", "§4.1.5(9)：在施工可能範圍下應繼續圍繞轉角銲接")
    PL, PR, PT = 0.0, 128.0, 52.0             # 構材（托架板）
    p1.polygon([(PL, 0), (PR, 0), (PR, PT), (PL, PT)], "#DCE3EC", C["member"], 2.2)
    p1.text_px(p1.X((PL+PR)/2), p1.Y(PT/2 + 6), "構材", 12.5, C["member"], weight="700")
    p1.text_px(p1.X((PL+PR)/2), p1.Y(PT/2 - 6), "（托架板、角鋼、連接板）", 10.5, C["muted"])
    # 主填角銲（沿縱向）
    p1.poly([(PL, 0), (PR, 0)], C["load"], 5.0)
    # 兩端回銲（繞轉角向上）
    RD = 16.0                                  # 繪圖上的回銲段長度
    for xx in (PL, PR):
        p1.poly([(xx, 0), (xx, RD)], C["accent"], 5.0)
    dim_h(p1, p1.X(PL), p1.X(PR), p1.Y(0) + 30, "主填角銲（縱向）", C["load"], above=False)
    dim_v(p1, p1.Y(0), p1.Y(RD), p1.X(PL) - 16, "ℓ", C["accent"], "end")
    dim_v(p1, p1.Y(0), p1.Y(RD), p1.X(PR) + 16, "ℓ", C["accent"], "start")
    p1.text_px(p1.X(PR) + 22, p1.Y(RD + 14), f"{RET_LO_K:g}w ≤ ℓ ≤ {RET_HI_K:g}w",
               12.5, C["accent"], "end", weight="700")
    p1.text_px(p1.X(PL), p1.Y(RD + 26), "回銲（繞轉角）", 11.5, C["accent"], weight="700")
    p1.text_px(p1.X(PR), p1.Y(RD + 26), "回銲（繞轉角）", 11.5, C["accent"], weight="700")
    p1.text_px(PWD/2, PH - 92,
               f"下限 {RET_LO_K:g}w：太短，起弧／收弧的弧坑與氣孔仍留在主受力斷面上",
               11.5, C["muted"])
    p1.text_px(PWD/2, PH - 70,
               f"上限 {RET_HI_K:g}w：太長，會過度束制接合端部的轉動",
               11.5, C["muted"])
    p1.text_px(PWD/2, PH - 44, "只寫下限 2w 拿不到滿分——上下限都要寫", 12.5,
               C["load"], weight="700")
    p1.text_px(PWD/2, PH - 20,
               f"本例 w = {W:g} mm ⇒ ℓ 應介於 {RET_LO:g} ～ {RET_HI:g} mm",
               12, C["accent"], weight="700")

    # ── 格 2：有效長度怎麼算 ──
    p2 = Canvas(PWD, PH, sx=1.0)
    p2.panel("有效長度：含端彎，不作任何扣除", "§4.1.5(1)～(3)")
    bx, bw = 205, 232
    peak = L_TW*1.02
    rows = ((f"國內規範", f"{LMAIN:g} ＋ 端彎 2×{RET:g}", L_TW, C["bmd"], True),
            (f"誤法一", "端彎不計入有效長度", L_NORET, C["load"], False),
            (f"誤法二", "IS 800／BS 體系：各扣 1w", L_DEDUCT, C["load"], False))
    for i, (nm, note, v, col, ok) in enumerate(rows):
        y = 172 + i*76
        p2.text_px(bx - 12, y - 9, nm, 12.5, col, "end", weight="700")
        p2.text_px(bx - 12, y + 12, note, 10.5, C["muted"], "end")
        p2.rect_px(bx, y - 15, bw, 30, "#EDF1F6", 6)
        p2.rect_px(bx, y - 15, bw*v/peak, 30, col, 6)
        p2.text_px(bx + bw*v/peak - 10, y, f"{v:.0f} mm", 12, "#FFFFFF", "end",
                   weight="700")
        if not ok:
            p2.text_px(bx + bw + 14, y, f"−{100*(1-v/L_TW):.0f}%", 12, col, "start",
                       weight="700")
    p2.text_px(PWD/2, PH - 92,
               f"同一組銲道，算法不同就差 {100*(L_TW/L_DEDUCT - 1):.0f}%", 12.5,
               C["load"], weight="700")
    p2.text_px(PWD/2, PH - 70, "國內考試一律採國內規範：回銲計入、不作扣除", 12,
               C["bmd"], weight="700")
    p2.text_px(PWD/2, PH - 44,
               f"（有效喉深另有 t_e = {THROAT_K:g}w，是「厚度」不是「長度」，不要混用）",
               11, C["muted"])
    p2.text_px(PWD/2, PH - 20,
               f"本例 t_e = {THROAT_K:g}×{W:g} = {THROAT_K*W:.2f} mm",
               11.5, C["muted"])

    compose([p1, p2], cols=2,
            title="圖 1　回銲：長度有上下限，而且整段都算進有效長度",
            sub="回銲把「品質最差的起弧／收弧」搬離「受力最大的主斷面」，"
                "同時讓強度在轉角處連續",
            note=f"§4.1.5(1)～(3) 明定有效銲道長度為含端彎在內之全部長度——"
                 f"「兩端各扣 1w」是 IS 800／BS 體系的算法，國內規範沒有這一條",
            path=os.path.join(OUT, "SS-2016-2-fig-1-end-return.svg"))


# ══════════════════════════════════════════════════════════════
def fig2_three_4w():
    """圖 2：三處 4w，方向各不相同"""
    W_, H_ = 1040, 610
    Lm, Rm, Tm, Bm = 96, 330, 140, 106
    WA, WB = 3.0, 16.0                 # 銲腳尺寸範圍（mm）
    YMAX = 4.0*WB*1.12
    cv = Canvas(W_, H_, sx=1.0, bg="#FFFFFF")
    X = lambda w: Lm + (W_-Lm-Rm)*(w-WA)/(WB-WA)
    Y = lambda v: (H_-Bm) - (H_-Tm-Bm)*v/YMAX

    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{X(WB)+14}" y2="{Y(0)}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    cv.parts.append(f'<line x1="{Lm}" y1="{Y(0)}" x2="{Lm}" y2="{Y(YMAX)-6}" '
                    f'stroke="{C["muted"]}" stroke-width="1.8"/>')
    for w in range(4, int(WB)+1, 2):
        cv.parts.append(f'<line x1="{X(w):.1f}" y1="{Y(0)}" x2="{X(w):.1f}" '
                        f'y2="{Y(0)+7}" stroke="{C["muted"]}" stroke-width="1.3"/>')
        cv.text_px(X(w), Y(0) + 22, f"{w}", 11, C["muted"])
    for v in range(0, int(YMAX)+1, 10):
        cv.parts.append(f'<line x1="{Lm-7}" y1="{Y(v):.1f}" x2="{Lm}" y2="{Y(v):.1f}" '
                        f'stroke="{C["muted"]}" stroke-width="1.3"/>')
        cv.text_px(Lm - 14, Y(v), f"{v}", 11, C["muted"], "end")
    cv.text_px((Lm+X(WB))/2, Y(0) + 44, "銲腳尺寸 w（mm）", 12.5, C["muted"])
    cv.text_px(Lm - 6, Tm - 16, "長度（mm）", 12.5, C["muted"], "start")

    # (9) 繞角銲允許帶 2w ～ 4w
    band = (" ".join(f"{X(WA + (WB-WA)*i/80):.1f},{Y(RET_HI_K*(WA+(WB-WA)*i/80)):.1f}"
                     for i in range(81)) + " " +
            " ".join(f"{X(WA + (WB-WA)*i/80):.1f},{Y(RET_LO_K*(WA+(WB-WA)*i/80)):.1f}"
                     for i in range(80, -1, -1)))
    cv.parts.append(f'<polygon points="{band}" fill="rgba(180,83,9,0.16)" '
                    f'stroke="none"/>')
    for k, col, sw in ((RET_HI_K, C["accent"], 3.0), (RET_LO_K, C["accent"], 2.2)):
        cv.parts.append(f'<line x1="{X(WA):.1f}" y1="{Y(k*WA):.1f}" x2="{X(WB):.1f}" '
                        f'y2="{Y(k*WB):.1f}" stroke="{col}" stroke-width="{sw}"/>')
    cv.text_px(X(12.4), Y(RET_HI_K*12.4) - 14, f"{RET_HI_K:g}w", 12.5, C["accent"],
               weight="700")
    cv.text_px(X(13.6), Y(RET_LO_K*13.6) - 13, f"{RET_LO_K:g}w", 12.5, C["accent"],
               weight="700")
    cv.text_px(X(12.2), Y(RET_LO_K*12.2 + 4), "(9) 繞角銲：只能落在這條帶子裡",
               12, C["accent"], weight="700")

    # (7) 斷續銲每段下限 = max(4w, 40)
    cv.parts.append(f'<line x1="{X(WA):.1f}" y1="{Y(SEG_MM):.1f}" x2="{X(WB):.1f}" '
                    f'y2="{Y(SEG_MM):.1f}" stroke="{C["bmd"]}" stroke-width="1.8" '
                    f'stroke-dasharray="6 4"/>')
    cv.text_px(X(WA) + 8, Y(SEG_MM) - 12, f"{SEG_MM:g} mm", 12, C["bmd"], "start",
               weight="700")
    gov = [(w, max(SEG_K*w, SEG_MM)) for w in
           [WA + (WB-WA)*i/120 for i in range(121)]]
    cv.parts.append('<polyline points="' +
                    " ".join(f"{X(w):.1f},{Y(v):.1f}" for w, v in gov) +
                    f'" fill="none" stroke="{C["bmd"]}" stroke-width="4.0" '
                    f'stroke-linejoin="round"/>')
    cv.parts.append(f'<circle cx="{X(W_CROSS):.1f}" cy="{Y(SEG_MM):.1f}" r="6" '
                    f'fill="{C["bmd"]}" stroke="#FFFFFF" stroke-width="2"/>')
    cv.text_px(X(W_CROSS), Y(SEG_MM) + 26, f"w = {W_CROSS:g} mm", 12, C["bmd"],
               weight="700")
    cv.text_px(X(W_CROSS), Y(SEG_MM) + 44, "兩個下限在此交會", 11, C["bmd"])
    cv.text_px(X(5.6), Y(SEG_MM) + 74, f"w ＜ {W_CROSS:g}：{SEG_MM:g} mm 控制",
               11.5, C["bmd"], weight="700")
    cv.text_px(X(13.4), Y(SEG_K*13.4) + 22, f"w ＞ {W_CROSS:g}：{SEG_K:g}w 控制",
               11.5, C["bmd"], weight="700")

    # 本例 w
    cv.parts.append(f'<line x1="{X(W):.1f}" y1="{Y(YMAX)-4:.1f}" x2="{X(W):.1f}" '
                    f'y2="{Y(0):.1f}" stroke="{C["load"]}" stroke-width="1.4" '
                    f'stroke-dasharray="4 4"/>')
    cv.text_px(X(W) - 6, Y(64), f"本例 w = {W:g}", 11.5, C["load"], "end", weight="700")

    # ── 右側：三個 4w 的方向 ──
    bx = W_ - Rm + 26
    cv.text_px(bx, 152, "三處都寫 4w，方向卻不同", 13, C["text"], "start", weight="700")
    rows = ((f"§4.1.5(6)", f"最小有效長度 ≥ {LMIN_K:g}w", "下限", C["compr"]),
            (f"§4.1.5(7)", f"斷續銲每段 ≥ {SEG_K:g}w 且 ≥ {SEG_MM:g} mm", "下限", C["bmd"]),
            (f"§4.1.5(9)", f"繞角銲 ≤ {RET_HI_K:g}w（且 ≥ {RET_LO_K:g}w）", "上限",
             C["accent"]))
    for i, (cl, txt, dirn, col) in enumerate(rows):
        y = 190 + i*74
        cv.rect_px(bx, y - 22, 276, 60, "#F5F7FA", 9, col, 1.8)
        cv.text_px(bx + 14, y - 4, cl, 12, col, "start", weight="700")
        cv.text_px(bx + 232, y - 4, dirn, 12.5, col, "end", weight="700")
        cv.text_px(bx + 14, y + 18, txt, 11.5, C["text"], "start")
    cv.text_px(bx, 434, "順帶記牢（§4.1.5 其餘）：", 12, C["muted"], "start", weight="700")
    cv.text_px(bx, 458, f"有效喉深 t_e = {THROAT_K:g}w（等腳）", 11.5, C["muted"], "start")
    cv.text_px(bx, 478, f"搭接長度 ≥ {LAP_K:g}×較薄板厚，且 ≥ {LAP_MM:g} mm", 11.5,
               C["muted"], "start")
    cv.text_px(bx, 498, "板邊 t ≤ 6 mm 時銲腳不得大於板厚", 11.5, C["muted"], "start")

    cv.text_px(W_/2, 34, "圖 2　三個「4w」不可混為一談", 17.5, C["text"], weight="700")
    cv.text_px(W_/2, 58, "同一個數字，(6)(7) 是下限、(9) 是上限——這是本單元最容易寫反的地方",
               13, C["muted"])
    cv.text_px(W_/2, 84,
               f"而 (7) 還有第二個門檻：w ＜ {W_CROSS:g} mm 時真正控制的是 {SEG_MM:g} mm，"
               f"不是 {SEG_K:g}w",
               12.5, C["accent"])
    cv.text_px(W_/2, 110,
               f"本例 w = {W:g} mm ⇒ 斷續銲每段至少 {max(SEG_K*W, SEG_MM):.0f} mm；"
               f"繞角銲 ℓ 介於 {RET_LO:g}～{RET_HI:g} mm",
               12.5, C["load"])
    cv.save(os.path.join(OUT, "SS-2016-2-fig-2-three-4w.svg"))


# ══════════════════════════════════════════════════════════════
def fig3_apply_or_not():
    """圖 3：該回銲與不該回銲，判準是「端部要不要能轉」"""
    PWD, PH = 520, 500
    XL, XR, YL, YH = -34.0, 130.0, -46.0, 62.0
    Lm, Tm, Bm = 32, 108, 152
    sx = min((PWD-2*Lm)/(XR-XL), (PH-Tm-Bm)/(YH-YL))
    OX, OY = Lm - XL*sx, Bm - YL*sx

    # ── 格 1：托架板（應回銲）──
    p1 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p1.panel("○ 適用：偏心受載之托架板", "銲道端部有最大的剝離分力")
    p1.polygon([(-26, -44), (-10, -44), (-10, 58), (-26, 58)], "#C3D2DC", C["member"], 2.2)
    p1.text_px(p1.X(-18), p1.Y(50), "柱", 12, C["member"], weight="700")
    p1.polygon([(-10, -4), (104, -4), (104, 42), (-10, 42)], "#DCE3EC", C["member"], 2.2)
    p1.text_px(p1.X(48), p1.Y(19), "托架板", 12.5, C["member"], weight="700")
    # 兩道縱向填角銲 + 兩端回銲
    for yy in (-4, 42):
        p1.poly([(-10, yy), (104, yy)], C["load"], 4.4)
    for xx, y0, y1 in ((-10, -4, 8), (-10, 42, 30), (104, -4, 8), (104, 42, 30)):
        p1.poly([(xx, y0), (xx, y1)], C["accent"], 4.4)
    # 載重與偏心
    p1.arrow((98, 60), (98, 44), C["load"], 3.0, 10)
    p1.math_px(p1.X(98) + 10, p1.Y(54), "P", 15, C["load"], "start", weight="700")
    dim_h(p1, p1.X(47), p1.X(98), p1.Y(-16), "e", C["load"], above=False)
    # 端部剝離分力（線性分佈，端點最大）
    for i in range(7):
        xx = -10 + 114*i/6
        f = abs(xx - 47)/57.0
        if f < 0.12 or abs(xx - 98) < 12:
            continue
        d = 12.0*f
        p1.arrow((xx, 42), (xx, 42 + d), C["bmd"], 2.0, 6)
    p1.text_px(p1.X(-10), p1.Y(58), "端部分力最大（撕開方向）", 11, C["bmd"],
               "start", weight="700")
    p1.text_px(PWD/2, PH - 118, "彎矩 M = P·e 在銲道群產生線性分佈分力，",
               11.5, C["muted"])
    p1.text_px(PWD/2, PH - 96, "最遠端最大，方向是把銲道撕開", 11.5, C["muted"])
    p1.text_px(PWD/2, PH - 70, "端部同時是：應力最大處 ＋ 幾何不連續處", 11.5, C["load"])
    p1.text_px(PWD/2, PH - 48, "＋ 起弧／收弧缺陷所在——三個不利因素疊加", 11.5, C["load"])
    p1.text_px(PWD/2, PH - 20,
               "判準：端部有較大剝離分力且需強度連續 ⇒ 應回銲", 12.5, C["bmd"],
               weight="700")

    # ── 格 2：雙角鋼外伸肢（不宜回銲）──
    p2 = Canvas(PWD, PH, sx=sx, ox=OX, oy=OY)
    p2.panel("× 不適用：需保持轉動撓性之外伸肢", "簡支梁之雙角鋼剪力接合")
    p2.polygon([(-26, -44), (-10, -44), (-10, 58), (-26, 58)], "#C3D2DC", C["member"], 2.2)
    p2.text_px(p2.X(-18), p2.Y(50), "柱", 12, C["member"], weight="700")
    # 角鋼：外伸肢貼柱面，另一肢連梁腹板
    p2.polygon([(-10, -18), (-2, -18), (-2, 40), (-10, 40)], "#B9C6D4", C["member"], 2.0)
    p2.polygon([(-2, 4), (34, 4), (34, 18), (-2, 18)], "#B9C6D4", C["member"], 2.0)
    p2.text_px(p2.X(16), p2.Y(11), "角鋼", 11, C["member"], weight="700")
    p2.text_px(p2.X(-6), p2.Y(-28), "外伸肢", 11, C["member"], weight="700")
    # 梁
    p2.polygon([(34, -14), (108, -14), (108, 36), (34, 36)], "#DCE3EC", C["member"], 2.2)
    p2.text_px(p2.X(72), p2.Y(11), "梁", 12.5, C["member"], weight="700")
    # 梁端轉動 → 外伸肢張開
    p2.poly([(-2, 30), (4, 34), (12, 36)], C["bmd"], 2.6)
    p2.arrow((4, 34), (12, 36), C["bmd"], 2.4, 8)
    p2.text_px(p2.X(16), p2.Y(40), "外伸肢須能張開", 11, C["bmd"], "start", weight="700")
    p2.text_px(p2.X(16), p2.Y(30), "才是真正的鉸接", 11, C["bmd"], "start", weight="700")
    # 若在此回銲 → 焊死
    p2.poly([(-10, 40), (-2, 40)], C["load"], 5.0)
    p2.parts.append(f'<circle cx="{p2.X(-6):.1f}" cy="{p2.Y(40):.1f}" r="13" '
                    f'fill="none" stroke="{C["load"]}" stroke-width="2.4"/>')
    p2.text_px(p2.X(2), p2.Y(58), "若在此回銲 ⇒ 焊死", 11, C["load"], "start",
               weight="700")
    p2.text_px(PWD/2, PH - 118, "回銲把端部焊死 ⇒ 轉動被束制 ⇒ 變成半剛接",
               11.5, C["load"], weight="700")
    p2.text_px(PWD/2, PH - 96, "產生設計時未計入的端彎矩", 11.5, C["load"])
    p2.text_px(PWD/2, PH - 70, "結果是回銲段自己先被拉裂，裂縫再延伸至主銲道",
               11.5, C["muted"])
    p2.text_px(PWD/2, PH - 48, "——做了回銲反而更不安全", 11.5, C["muted"])
    p2.text_px(PWD/2, PH - 20,
               f"規範以「≤ {RET_HI_K:g}w」的上限形式寫的就是這件事", 12.5, C["accent"],
               weight="700")

    compose([p1, p2], cols=2,
            title="圖 3　要不要回銲，看的是「這個端部該不該能轉」",
            sub="需要強度連續、端部承受剝離力 ⇒ 回銲；需要保持轉動撓性 ⇒ 不宜回銲",
            note="不適用的主答案是「需保持轉動撓性之外伸肢」；"
                 "斷續銲無轉角可繞屬「施工可能範圍」的做不到，不是規範禁止，"
                 "拿它當主答案會失分",
            path=os.path.join(OUT, "SS-2016-2-fig-3-apply-or-not.svg"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1_end_return(); fig2_three_4w(); fig3_apply_or_not()
    print(f"w = {W:g} mm ⇒ 繞角銲 {RET_LO:g} ～ {RET_HI:g} mm（採用 {RET:g}）")
    print(f"有效長度：國內 {L_TW:.0f}、端彎不計 {L_NORET:.0f}、兩端各扣 1w {L_DEDUCT:.0f} mm")
    print(f"  國內 / 兩端各扣 1w = {L_TW/L_DEDUCT:.3f} ⇒ 差 {100*(L_TW/L_DEDUCT-1):.0f}%")
    print(f"斷續銲每段下限交會點 w = {SEG_MM:g}/{SEG_K:g} = {W_CROSS:g} mm")
    print(f"  本例 w = {W:g} ⇒ 每段 ≥ max({SEG_K*W:.0f}, {SEG_MM:g}) = "
          f"{max(SEG_K*W, SEG_MM):.0f} mm（由 {SEG_MM:g} mm 控制）")
    print("done ->", OUT)
