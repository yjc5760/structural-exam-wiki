#!/usr/bin/env python3
"""
SS-2006-3 H600×300×12×20 斷面性質（Ix、ry、Zx、Mp）— 解題圖解腳本

用法：
    python3 gen_SS-2006-3.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2006-3-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2006-3.md §4，由下式即時算出（單位 mm；Mp 換 tf-cm）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2006-3"

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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2006-3.md §4，由下式即時算出（mm）
# ══════════════════════════════════════════════════════════════
Q_H, Q_BF, Q_TW, Q_TF = 600.0, 300.0, 12.0, 20.0
Q_FY = 3.5                                   # tf/cm²
Q_HW = Q_H - 2 * Q_TF                        # 560
Q_DF = Q_H / 2 - Q_TF / 2                    # 290
Q_IF0 = Q_BF * Q_TF ** 3 / 12                # 200,000（翼板自身）
Q_IFP = Q_BF * Q_TF * Q_DF ** 2              # 504,600,000（平行軸項）
Q_IW = Q_TW * Q_HW ** 3 / 12                 # 175,616,000
Q_IX = 2 * (Q_IF0 + Q_IFP) + Q_IW            # 1,185,216,000
Q_IYF = Q_TF * Q_BF ** 3 / 12                # 45,000,000
Q_IYW = Q_HW * Q_TW ** 3 / 12                # 80,640
Q_IY = 2 * Q_IYF + Q_IYW
Q_A = 2 * Q_BF * Q_TF + Q_HW * Q_TW          # 18,720
Q_RY = math.sqrt(Q_IY / Q_A)                 # 69.4
Q_ZF = Q_BF * Q_TF * (Q_H - Q_TF)            # 3,480,000
Q_ZW = Q_TW * Q_HW ** 2 / 4                  # 940,800
Q_ZX = Q_ZF + Q_ZW
Q_MP = Q_FY * Q_ZX / 1000                    # tf-cm（mm³ → cm³）


def _hsec(cv, cx, cy, s, fl=C["fill_c"], wb=C["fill_c"]):
    """以 (cx, cy) 為形心、比例 s px/mm 畫 H 斷面；回傳上下緣 y"""
    h, b = Q_H * s / 2, Q_BF * s / 2
    _pR(cv, cx - b, cy - h, cx + b, cy - h + Q_TF * s, fl, C["member"], 1.4)
    _pR(cv, cx - b, cy + h - Q_TF * s, cx + b, cy + h, fl, C["member"], 1.4)
    _pR(cv, cx - Q_TW * s / 2, cy - h + Q_TF * s, cx + Q_TW * s / 2, cy + h - Q_TF * s, wb, C["member"], 1.4)
    return cy - h, cy + h


def _bar(cv, x0, y, scale, v, col, lab, val, h=26):
    w = max(scale * v, 2.0)
    cv.rect_px(x0, y - h / 2, w, h, col, 3)
    _pT(cv, x0 - 12, y, lab, 12.5, C["text"], "end", weight="700")
    _pT(cv, x0 + w + 10, y, val, 12.5, C["text"], "start")


def fig1_inertia():
    W1, H1 = 1100, 560
    cv = Canvas(W1, H1)
    cv.panel("Ix 靠翼板的平行軸項；Iy 幾乎全由翼板對自身軸提供",
             "長條長度依各項數值比例；單位 mm⁴")
    s = 0.55
    cx, cy = 190.0, 320.0
    yt, yb = _hsec(cv, cx, cy, s)
    _pL(cv, cx - 120, cy, cx + 120, cy, C["accent"], 1.4, dash="8 3 2 3")
    _pT(cv, cx + 124, cy, "x", 13, C["accent"], "start", weight="700")
    _pL(cv, cx, yt - 26, cx, yb + 26, C["sfd"], 1.4, dash="8 3 2 3")
    _pT(cv, cx, yb + 40, "y", 13, C["sfd"], weight="700")
    # 翼板形心距
    yfc = cy - Q_DF * s
    _pL(cv, cx + 95, yfc, cx + 95, cy, C["dim"], 1.2)
    _pL(cv, cx + 88, yfc, cx + 102, yfc, C["dim"], 1.2)
    _pT(cv, cx + 100, (yfc + cy) / 2, f"d = {Q_H/2:.0f} − {Q_TF/2:.0f} = {Q_DF:.0f}", 12, C["text"], "start", weight="700")
    _pT(cv, cx, yt - 40, "H600×300×12×20", 13, C["text"], weight="700")
    _pT(cv, cx, yb + 62, f"hw = 600 − 2×20 = {Q_HW:.0f}", 12, C["muted"])
    # Ix 長條
    x0 = 560.0
    sc = 440.0 / Q_IX
    _pT(cv, x0 - 140, 112, f"強軸 Ix = {_fmt(Q_IX, 0)}", 14, C["compr"], "start", weight="700")
    _bar(cv, x0, 150, sc, 2 * Q_IFP, C["compr"], "翼板 Af·d²（×2）", _fmt(2 * Q_IFP, 0))
    _bar(cv, x0, 186, sc, 2 * Q_IF0, C["member2"], "翼板自身 bt³/12（×2）", _fmt(2 * Q_IF0, 0))
    _bar(cv, x0, 222, sc, Q_IW, C["bmd"], "腹板 tw·hw³/12", _fmt(Q_IW, 0))
    _pT(cv, x0, 256, f"平行軸項占 {2 * Q_IFP / Q_IX * 100:.1f}%：d 取 300（H/2）會多算 {_fmt(2 * Q_BF * Q_TF * (300 ** 2 - Q_DF ** 2), 0)}",
        12, C["load"], "start")
    # Iy 長條
    sc2 = 440.0 / Q_IY
    _pT(cv, x0 - 140, 318, f"弱軸 Iy = {_fmt(Q_IY, 0)}", 14, C["sfd"], "start", weight="700")
    _bar(cv, x0, 356, sc2, 2 * Q_IYF, C["sfd"], "翼板 tf·bf³/12（×2）", _fmt(2 * Q_IYF, 0))
    _bar(cv, x0, 392, sc2, Q_IYW, C["bmd"], "腹板 hw·tw³/12", _fmt(Q_IYW, 0) + "（極小）")
    _pT(cv, x0 - 140, 446, f"A = 2×300×20 + 560×12 = {_fmt(Q_A, 0)} mm²", 13, C["text"], "start")
    _pT(cv, x0 - 140, 478, f"ry = √(Iy / A) = √{_fmt(Q_IY / Q_A, 0)} ≈ {_fmt(Q_RY, 1)} mm", 14, C["sfd"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-inertia.svg")
    compose([cv], cols=1,
            title=f"圖 1　Ix = {_fmt(Q_IX, 0)} mm⁴；ry = {_fmt(Q_RY, 1)} mm",
            sub="組件疊加：每塊 = 自身慣性矩 ＋ 面積 × 至形心軸距離²（腹板通過形心，無平行軸項）",
            note="弱軸時腹板的「寬」是 tw = 12：hw·tw³/12 只有 8 萬，tw 與 hw 對調就差了上千倍",
            path=path)
    return path


def fig2_zx():
    W1, H1 = 1100, 540
    cv = Canvas(W1, H1)
    cv.panel("全塑性：PNA 在對稱軸，上半全壓 Fy、下半全拉 Fy",
             "Zx = 翼板 bf·tf·(H − tf) ＋ 腹板 tw·hw²/4")
    s = 0.62
    cx, cy = 200.0, 310.0
    yt, yb = _hsec(cv, cx, cy, s, "#C9D0DA", "#C9D0DA")
    _pL(cv, cx - 120, cy, cx + 260, cy, C["accent"], 1.4, dash="8 3 2 3")
    _pT(cv, cx - 124, cy, "PNA", 12, C["accent"], "end", weight="700")
    # 應力塊
    zx = 380.0
    _pL(cv, zx, yt - 10, zx, yb + 10, C["member2"], 1.2)
    _pR(cv, zx - 40, yt, zx, cy, C["fill_c"], C["compr"], 1.4)
    _pR(cv, zx, cy, zx + 40, yb, C["fill_t"], C["tension"], 1.4)
    _pT(cv, zx - 20, yt - 14, "Fy 壓", 12, C["compr"], weight="700")
    _pT(cv, zx + 20, yb + 16, "Fy 拉", 12, C["tension"], weight="700")
    # 力偶
    yf1, yf2 = cy - Q_DF * s, cy + Q_DF * s
    yw1, yw2 = cy - Q_HW / 4 * s, cy + Q_HW / 4 * s
    xa = 470.0
    _pA(cv, xa + 40, yf1, xa, yf1, C["compr"], 2.8, 9)
    _pA(cv, xa, yf2, xa + 40, yf2, C["tension"], 2.8, 9)
    _pA(cv, xa + 100, yw1, xa + 70, yw1, C["compr"], 2.4, 8)
    _pA(cv, xa + 70, yw2, xa + 100, yw2, C["tension"], 2.4, 8)
    _pL(cv, xa + 20, yf1 + 6, xa + 20, yf2 - 6, C["dim"], 1.2)
    _pT(cv, xa + 14, cy - 60, f"{_fmt(Q_H - Q_TF, 0)}", 12, C["text"], "end", weight="700")
    _pL(cv, xa + 85, yw1 + 6, xa + 85, yw2 - 6, C["dim"], 1.2)
    _pT(cv, xa + 91, cy - 40, f"{_fmt(Q_HW / 2, 0)}", 12, C["text"], "start", weight="700")
    _pT(cv, xa + 20, yf1 - 14, "翼板合力", 11.5, C["compr"])
    _pT(cv, xa + 85, yw1 - 14, "半腹板合力", 11.5, C["compr"])
    # 右側計算
    xt = 660.0
    rows = [("翼板：300 × 20 × (600 − 20)", C["text"], "700"),
            (f"= {_fmt(Q_ZF, 0)} mm³", C["compr"], "700"),
            ("（翼板力 × 力偶臂 H − tf = 580）", C["muted"], "400"),
            ("腹板：12 × 560² / 4", C["text"], "700"),
            (f"= {_fmt(Q_ZW, 0)} mm³", C["bmd"], "700"),
            ("（半腹板 12×280 × 力偶臂 280）", C["muted"], "400"),
            (f"Zx = {_fmt(Q_ZX, 0)} mm³ = {_fmt(Q_ZX / 1000, 1)} cm³", C["text"], "700"),
            (f"Mp = 3.5 × {_fmt(Q_ZX / 1000, 1)} = {_fmt(Q_MP, 1)} tf-cm", C["load"], "700"),
            (f"≈ {_fmt(Q_MP / 100, 1)} tf-m", C["load"], "700")]
    for i, (sx, col, wt) in enumerate(rows):
        _pT(cv, xt, 120 + i * 40, sx, 13.5, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-zx.svg")
    compose([cv], cols=1,
            title=f"圖 2　Zx = {_fmt(Q_ZX, 0)} mm³，Mp = Fy·Zx = {_fmt(Q_MP, 1)} tf-cm",
            sub="mm³ 換 cm³ 除以 1,000；Fy 用 tf/cm²，Mp 單位才是 tf-cm",
            note="翼板力偶臂是兩翼板形心距 H − tf，不是 H；腹板力偶臂是 hw/2，不是 hw",
            path=path)
    return path


FIGURES = [
    (fig1_inertia, "§4（一）（二）",
     "翼板 d 取 H/2；漏平行軸項；弱軸腹板 hw、tw 對調"),
    (fig2_zx, "§4（三）（四）",
     "力偶臂用 H 或 hw；mm³ 與 cm³ 換算；用 Sx 算 Mp"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
