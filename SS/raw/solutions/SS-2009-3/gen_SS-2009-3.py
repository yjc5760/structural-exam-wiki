#!/usr/bin/env python3
"""
SS-2009-3 H 型鋼斷面之 Mp/My、Vn 與弱軸 λc — 題目附圖重繪腳本

用法：
    python3 gen_SS-2009-3.py [輸出目錄]

重繪依據：題目正本 SS-2009-3-problem.md §4 判讀清單（2026-11-02 已確認）。
考卷原圖為無尺寸線的示意圖；本圖依標示 H 500 × 304 × 15 × 24 按比例繪出並標上各尺寸對應位置
（#1 標示順序 d × b_f × t_w × t_f），不含任何解題結果。圓角不計（#3）。單位 mm。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2009-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2009-3-problem.md §4，已確認）；單位 mm
# ══════════════════════════════════════════════════════════
D, BF, TW, TF = 500.0, 304.0, 15.0, 24.0    # #1 d × b_f × t_w × t_f
#                                             #3 圓角未給，以三塊矩形計


def fig1_problem():
    W, H, sx = 560, 560, 0.72
    cv = Canvas(W, H, sx=sx, ox=W / 2 - 30, oy=H / 2 - 30)
    cv.panel("H 500 × 304 × 15 × 24", "依標示按比例；原圖為無尺寸線示意圖")
    h, b = D / 2, BF / 2
    for x0, x1, y0, y1 in ((-b, b, h - TF, h), (-b, b, -h, -h + TF), (-TW / 2, TW / 2, -h + TF, h - TF)):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.8)
    cv.dim((-b, h), (b, h), f"b_{{f}} = {BF:g}", off=-24, label_off=-14)
    cv.dim((-b, -h), (-b, h), f"d = {D:g}", off=-30, label_off=-44)
    cv.dim((b, h - TF), (b, h), f"t_{{f}} = {TF:g}", off=26, label_off=44)
    cv.arrow((TW / 2 + 70, 0), (TW / 2, 0), C["dim"], 1.2, 7)
    cv.arrow((-TW / 2 - 40, 0), (-TW / 2, 0), C["dim"], 1.2, 7)
    cv.math((TW / 2 + 70, 0), f"t_{{w}} = {TW:g}", 14, C["dim"], "start", dx=6)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2009-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3；單位 mm",
            note="標示順序為 d × b_f × t_w × t_f；翼板厚 24 大於腹板厚 15",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _pP(cv, x, y):
    return (x, cv.h - y)


def _pL(cv, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line(_pP(cv, x0, y0), _pP(cv, x1, y1), color, w, dash=dash, cap="butt")


def _pR(cv, x0, y0, x1, y1, fill, stroke="none", sw=1.2):
    cv.polygon([_pP(cv, x0, y0), _pP(cv, x1, y0), _pP(cv, x1, y1), _pP(cv, x0, y1)], fill, stroke, sw)


def _pA(cv, x0, y0, x1, y1, color, w=2.6, head=9):
    cv.arrow(_pP(cv, x0, y0), _pP(cv, x1, y1), color, w, head)


def _pT(cv, x, y, s, size=13, color=C["text"], anchor="middle", weight="400"):
    cv.text_px(x, y, s, size, color, anchor, weight=weight)


def _pPL(cv, pts, color, w=2.0, dash=None):
    cv.poly([_pP(cv, x, y) for x, y in pts], color, w, dash=dash)


def _fmt(v, nd=1):
    """與解析相同的顯示：四捨五入（加微量避免浮點 .x5 落到下方）＋千分位"""
    v = round(v + (1e-9 if v >= 0 else -1e-9), nd)
    return f"{v:,.{nd}f}"



# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2009-3.md §4，由下式即時算出（tf、cm）
# ══════════════════════════════════════════════════════════════
Q_D, Q_BF, Q_TW, Q_TF = D / 10, BF / 10, TW / 10, TF / 10
Q_FY, Q_E, Q_KL = 3.5, 2040.0, 400.0
Q_H = Q_D - 2 * Q_TF                                  # 45.2
Q_A = 2 * Q_BF * Q_TF + Q_H * Q_TW                    # 213.72
Q_DF = Q_D / 2 - Q_TF / 2                             # 23.8
Q_IXF = 2 * (Q_BF * Q_TF ** 3 / 12 + Q_BF * Q_TF * Q_DF ** 2)
Q_IXW = Q_TW * Q_H ** 3 / 12
Q_IX = Q_IXF + Q_IXW
Q_SX = Q_IX / (Q_D / 2)
Q_MY = Q_FY * Q_SX
Q_QF = Q_BF * Q_TF * Q_DF                             # 1,736.4
Q_QW = (Q_H / 2 * Q_TW) * (Q_H / 4)                   # 383.1
Q_ZX = 2 * (Q_QF + Q_QW)
Q_MP = Q_FY * Q_ZX
Q_HTW = Q_H / Q_TW                                    # 30.1
Q_HLIM = 2.45 * math.sqrt(Q_E / Q_FY)                 # 59.1
Q_AW = Q_D * Q_TW                                     # 75.0
Q_VN = 0.6 * Q_FY * Q_AW                              # 157.5
Q_IY = 2 * Q_TF * Q_BF ** 3 / 12 + Q_H * Q_TW ** 3 / 12
Q_RY = math.sqrt(Q_IY / Q_A)
Q_LC = Q_KL / (Q_RY * math.pi) * math.sqrt(Q_FY / Q_E)
Q_FCR = 0.658 ** (Q_LC ** 2) * Q_FY


def _q_hsec(cv, cx, cy, s, fill="#C9D0DA", web=None):
    h, b = Q_D * s / 2, Q_BF * s / 2
    _pR(cv, cx - b, cy - h, cx + b, cy - h + Q_TF * s, fill, C["member"], 1.4)
    _pR(cv, cx - b, cy + h - Q_TF * s, cx + b, cy + h, fill, C["member"], 1.4)
    _pR(cv, cx - Q_TW * s / 2, cy - h + Q_TF * s, cx + Q_TW * s / 2, cy + h - Q_TF * s, web or fill, C["member"], 1.4)
    return cy - h, cy + h


def fig2_shape():
    W1, H1 = 1120, 560
    cv = Canvas(W1, H1)
    cv.panel("同一斷面兩種極限：外緣剛降伏 My（三角形）與全斷面降伏 Mp（矩形）",
             "Mp / My = Zx / Sx，只與斷面形狀有關（形狀因子）")
    s = 7.6
    cx, cy = 150.0, 320.0
    yt, yb = _q_hsec(cv, cx, cy, s)
    _pL(cv, cx - 130, cy, cx + 130, cy, C["accent"], 1.3, dash="8 3 2 3")
    _pT(cv, cx + 100, cy - 12, "中性軸", 11.5, C["accent"], weight="700")
    _pT(cv, cx, yb + 22, "d = 50、bf = 30.4、tw = 1.5、tf = 2.4 cm", 11.5, C["muted"])
    # 彈性
    z1 = 360.0
    _pL(cv, z1, yt - 10, z1, yb + 10, C["member2"], 1.2)
    _pPL(cv, [(z1, yt), (z1 - 44, yt), (z1 + 44, yb), (z1, yb)], C["compr"], 1.6)
    cv.polygon([_pP(cv, z1, yt), _pP(cv, z1 - 44, yt), _pP(cv, z1, cy)], C["fill_c"], "none")
    cv.polygon([_pP(cv, z1, yb), _pP(cv, z1 + 44, yb), _pP(cv, z1, cy)], C["fill_t"], "none")
    _pT(cv, z1, yt - 26, "彈性極限", 13, C["text"], weight="700")
    _pT(cv, z1 - 50, yt, "Fy", 11.5, C["compr"], "end")
    _pT(cv, z1 + 44, yb + 14, "Fy", 11.5, C["tension"])
    # 塑性
    z2 = 520.0
    _pL(cv, z2, yt - 10, z2, yb + 10, C["member2"], 1.2)
    _pR(cv, z2 - 44, yt, z2, cy, C["fill_c"], C["compr"], 1.4)
    _pR(cv, z2, cy, z2 + 44, yb, C["fill_t"], C["tension"], 1.4)
    _pT(cv, z2, yt - 26, "全塑性", 13, C["text"], weight="700")
    _pL(cv, z1 - 60, cy, z2 + 60, cy, C["accent"], 1.0, dash="8 3 2 3")
    # 右側數字
    xt = 640.0
    rows = [("彈性：Sx = Ix / (d/2)", C["compr"], "700"),
            (f"Ix = 翼板 {_fmt(Q_IXF, 0)} ＋ 腹板 {_fmt(Q_IXW, 0)} = {_fmt(Q_IX, 0)}", C["muted"], "400"),
            (f"Sx = {_fmt(Q_SX, 0)} cm³，My = 3.5 × Sx = {_fmt(Q_MY, 0)} tf·cm", C["text"], "700"),
            ("塑性：Zx = 2 × PNA 以上一次面積矩", C["load"], "700"),
            (f"上翼板 72.96 × 23.8 = {_fmt(Q_QF, 1)}", C["muted"], "400"),
            (f"上半腹板 33.9 × 11.3 = {_fmt(Q_QW, 1)}", C["muted"], "400"),
            (f"Zx = 2 × {_fmt(Q_QF + Q_QW, 1)} = {_fmt(Q_ZX, 0)} cm³，Mp = {_fmt(Q_MP, 0)} tf·cm", C["text"], "700"),
            (f"Mp / My = {_fmt(Q_ZX, 0)} / {_fmt(Q_SX, 0)} ≈ {Q_ZX / Q_SX:.3f}", C["bmd"], "700")]
    for i, (sx, col, wt) in enumerate(rows):
        _pT(cv, xt, 130 + i * 44, sx, 13, col, "start", weight=wt)
    _pT(cv, xt, 130 + 8 * 44, "（翼板項精確為 82,725，解析寫 82,722，尾數差不影響 Sx）", 11, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-shape.svg")
    compose([cv], cols=1,
            title=f"圖 2　Mp / My = Zx / Sx = {_fmt(Q_ZX, 0)} / {_fmt(Q_SX, 0)} ≈ {Q_ZX / Q_SX:.3f}",
            sub="寬翼 H 型鋼的材料大多在翼板，三角形換成矩形只多出腹板中段的面積，形狀因子約 1.1～1.15",
            note="Zx 的一次面積矩要量到 PNA（對稱斷面即形心）；用 Ix / (d/2) 算出的是 Sx，不是 Zx",
            path=path)
    return path


def fig3_checks():
    PW1, PH1 = 560, 520
    # (a) 剪力
    a = Canvas(PW1, PH1)
    a.panel("(a) 剪力：Aw = d × tw（含翼板厚）", f"h/tw = {Q_HTW:.1f} 小於 2.45√(E/Fy) = {Q_HLIM:.1f} → Cv = 1.0")
    s = 6.4
    cx, cy = 130.0, 300.0
    yt, yb = _q_hsec(a, cx, cy, s, "#DDE2E9", "#DDE2E9")
    _pR(a, cx - Q_TW * s / 2, yt, cx + Q_TW * s / 2, yb, C["fill_s"], C["sfd"], 1.6)
    _pL(a, cx + 112, yt, cx + 112, yb, C["dim"], 1.2)
    _pL(a, cx + 106, yt, cx + 118, yt, C["dim"], 1.2)
    _pL(a, cx + 106, yb, cx + 118, yb, C["dim"], 1.2)
    _pT(a, cx + 112, yt - 16, "d = 50.0", 12.5, C["sfd"], weight="700")
    _pT(a, cx, yb + 24, "紫色條：Aw = 50.0 × 1.5", 12, C["sfd"], weight="700")
    rows = [(f"Aw = {_fmt(Q_AW, 1)} cm²", C["text"], "700"),
            ("Vn = 0.6 Fy Aw Cv", C["muted"], "400"),
            ("= 0.6 × 3.5 × 75.0 × 1.0", C["muted"], "400"),
            (f"= {_fmt(Q_VN, 1)} tf", C["sfd"], "700"),
            ("", C["text"], "400"),
            ("h/tw 用淨高 45.2 判斷挫屈；", C["muted"], "400"),
            ("Aw 則用全深 d", C["muted"], "400")]
    for i, (sx, col, wt) in enumerate(rows):
        if sx:
            _pT(a, 290, 140 + i * 34, sx, 13, col, "start", weight=wt)
    # (b) 柱曲線
    b = Canvas(PW1, PH1)
    b.panel("(b) 弱軸 λc = 0.727 落在非彈性段", f"KyLy / ry = 400 / {Q_RY:.3f} = {Q_KL / Q_RY:.1f}")
    X0, X1, Y0, Y1 = 80.0, 520.0, 440.0, 110.0
    gx = lambda l: X0 + l / 2.0 * (X1 - X0)
    gy = lambda r: Y0 - r * (Y0 - Y1)
    _pL(b, X0, Y0, X1, Y0, C["member"], 1.4)
    _pL(b, X0, Y0, X0, Y1, C["member"], 1.4)
    for l in (0, 0.5, 1.0, 1.5, 2.0):
        _pL(b, gx(l), Y0, gx(l), Y0 + 5, C["member"], 1.2)
        _pT(b, gx(l), Y0 + 18, f"{l:.1f}", 11.5, C["muted"])
    for r in (0, 0.5, 1.0):
        _pL(b, X0 - 5, gy(r), X0, gy(r), C["member"], 1.2)
        _pT(b, X0 - 9, gy(r), f"{r:.1f}", 11.5, C["muted"], "end")
    _pT(b, (X0 + X1) / 2, Y0 + 40, "λc", 13, C["muted"])
    _pT(b, X0, Y1 - 16, "Fcr / Fy", 12, C["muted"])
    ls = [i * 2.0 / 200 for i in range(201)]
    f = lambda l: 0.658 ** (l * l) if l <= 1.5 else 0.877 / (l * l)
    _pPL(b, [(gx(l), gy(f(l))) for l in ls if l <= 1.5], C["compr"], 2.6)
    _pPL(b, [(gx(l), gy(f(l))) for l in ls if l >= 1.5], C["member2"], 2.2, dash="6 4")
    _pL(b, gx(1.5), Y0, gx(1.5), gy(f(1.5)), C["muted"], 1.0, dash="3 3")
    _pT(b, gx(1.5) + 4, gy(f(1.5)) - 14, "1.5", 11.5, C["muted"], "start")
    _pT(b, gx(0.08), gy(0.66), "0.658 的 λc² 次方", 12, C["compr"], "start", weight="700")
    _pT(b, gx(1.62), gy(0.48), "0.877 / λc²", 12, C["member2"], "start")
    r = Q_FCR / Q_FY
    _pL(b, gx(Q_LC), Y0, gx(Q_LC), gy(r), C["accent"], 1.4, dash="5 3")
    b.dot(_pP(b, gx(Q_LC), gy(r)), 6, C["accent"])
    _pT(b, gx(Q_LC) + 10, gy(r) - 18, f"λc = {Q_LC:.3f}，Fcr = {Q_FCR / Q_FY:.3f} Fy ≈ 2.8 tf/cm²", 12.5, C["accent"], "start", weight="700")
    _pT(b, (X0 + X1) / 2 + 40, Y1 + 10, f"ry = √({_fmt(round(Q_IY - Q_H * Q_TW ** 3 / 12) + round(Q_H * Q_TW ** 3 / 12, 1), 0)} / {Q_A:.2f}) = {Q_RY:.3f} cm", 12, C["text"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-3-checks.svg")
    compose([a, b], cols=2,
            title=f"圖 3　Vn = {_fmt(Q_VN, 1)} tf（Cv = 1.0）；弱軸 λc = {Q_LC:.3f} ≤ 1.5",
            sub="㈡ 剪力面積取 d·tw；㈢ 只問 λc，Fcr 僅供參考",
            note="剪力常見錯：Aw 用淨高 h × tw（67.8）；λc 常見錯：用強軸 rx 或漏乘 √(Fy/E)/π",
            path=path)
    return path



FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把標示順序讀錯（例如 15 當翼板厚、24 當腹板厚，或 304 當深度）"),
    (fig2_shape, "§4 一",
     "用 Ix/(d/2) 當 Zx；一次面積矩沒量到 PNA；形狀因子倒數"),
    (fig3_checks, "§4 二、三",
     "Aw 用淨高 h；h/tw 判斷用 d；λc 用強軸 rx 或漏 √(Fy/E)/π"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
