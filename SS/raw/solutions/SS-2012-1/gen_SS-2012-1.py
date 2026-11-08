#!/usr/bin/env python3
"""
SS-2012-1 W14×90 非結實翼板簡支梁 LRFD 最大活載重 — 解題圖解腳本

用法：
    python3 gen_SS-2012-1.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2012-1-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2012-1.md §4，由下式即時算出（單位 kN、m、MPa）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2012-1"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2012-1.md §4
# ══════════════════════════════════════════════════════════════
Q_FY, Q_FR = 350.0, 69.0                 # MPa
Q_SX, Q_ZX = 2343350.0, 2572769.0        # mm³
Q_BF, Q_TF = 368.0, 18.0
Q_LAMP, Q_LAMR = 9.19, 22.3
Q_LP, Q_LR, Q_L = 4.5, 11.7, 10.0        # m
Q_WD = 5.8                               # kN/m
Q_MP = Q_FY * Q_ZX / 1e6                 # 900.47 kN·m
Q_MR = (Q_FY - Q_FR) * Q_SX / 1e6        # 658.48
Q_LAMF = round(Q_BF / (2 * Q_TF), 2)     # 10.22（解析取二位）
Q_CB = 12.5 / (2.5 + 3 * 0.75 + 4 + 3 * 0.75)   # 1.136
Q_MN_FLB = Q_MP - (Q_MP - Q_MR) * (Q_LAMF - Q_LAMP) / (Q_LAMR - Q_LAMP)
Q_MN_LTB = min(round(Q_CB, 3) * (Q_MP - (Q_MP - Q_MR) * (Q_L - Q_LP) / (Q_LR - Q_LP)), Q_MP)
Q_PHI_FLB, Q_PHI_LTB = 0.9 * Q_MN_FLB, 0.9 * Q_MN_LTB
Q_PHIMN = min(Q_PHI_FLB, Q_PHI_LTB)
Q_WL = (Q_PHIMN / (Q_L ** 2 / 8) - 1.2 * Q_WD) / 1.6


def _scale_panel(title, sub, x_lo, x_hi, xp, xr, xv, mn_v, lab_x, cb=1.0, fmt="{:g}"):
    W1, H1 = 500, 460
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    X0, X1, YB, YT = 70, 460, 370, 110
    m0, m1 = 600.0, 1000.0
    PX = lambda x: X0 + (X1 - X0) * (x - x_lo) / (x_hi - x_lo)
    PY = lambda m: YB - (YB - YT) * (m - m0) / (m1 - m0)
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(600, 1001, 100):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 58, lab_x, 12.5, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 16, "Mn（kN·m）", 12.5, C["text"], "start", weight="700")
    base = [(PX(x_lo), H1 - PY(Q_MP)), (PX(xp), H1 - PY(Q_MP)), (PX(xr), H1 - PY(Q_MR))]
    cv.poly(base, C["bmd"], 2.6)
    if cb != 1.0:
        pts = []
        for i in range(101):
            x = xp + (xr - xp) * i / 100
            pts.append((PX(x), H1 - PY(min(cb * (Q_MP - (Q_MP - Q_MR) * (x - xp) / (xr - xp)), Q_MP))))
        cv.poly(pts, C["compr"], 2.2, dash="7 4")
    for x, lab in ((xp, "p"), (xr, "r")):
        _hl(cv, H1, PX(x), YB, PX(x), PY(Q_MP) - 6, C["accent"], 1, dash="4 4")
        cv.text_px(PX(x), YB + 18, fmt.format(x), 11.5, C["accent"])
    _hl(cv, H1, PX(xv), YB, PX(xv), PY(mn_v), C["load"], 1.3, dash="3 3")
    cv.dot((PX(xv), H1 - PY(mn_v)), 6.5, fill=C["load"])
    cv.text_px(PX(xv) + (-12 if cb != 1.0 else 10), PY(mn_v) - 12, f"Mn ≈ {mn_v:.0f}", 13, C["load"], "end" if cb != 1.0 else "start", weight="700")
    cv.text_px(PX(xv), YB + 34, fmt.format(xv), 11.5, C["load"], weight="700")
    cv.text_px(PX(x_lo) + 6, PY(Q_MP) - 10, f"Mp = {Q_MP:.2f}", 11.5, C["bmd"], "start")
    cv.text_px(PX(xr) - 4, PY(Q_MR) + 16, f"Mr = {Q_MR:.2f}", 11.5, C["bmd"], "end")
    return cv


def fig1_limit():
    p1 = _scale_panel("翼板局部挫屈 FLB", f"λf = 368/(2 × 18) = {Q_LAMF}：介於 λp、λr → 非結實",
                      8.0, 24.0, Q_LAMP, Q_LAMR, Q_LAMF, Q_MN_FLB, "λ = bf / 2tf", fmt="{:g}")
    p2 = _scale_panel("側向扭轉挫屈 LTB", f"Lb = 10 m 介於 Lp、Lr；Cb = {Q_CB:.3f}（均佈載重）",
                      4.0, 12.0, Q_LP, Q_LR, Q_L, Q_MN_LTB, "Lb（m）", cb=round(Q_CB, 3))
    path = os.path.join(OUT, f"{TAG}-fig-1-limit.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　兩個極限狀態都是 Mp 到 Mr 的直線內插：FLB Mn ≈ {Q_MN_FLB:.0f}，LTB Mn ≈ {Q_MN_LTB:.0f} kN·m（控制）",
            sub=f"φbMn = min({Q_PHI_FLB:.1f}, {Q_PHI_LTB:.1f}) = {Q_PHIMN:.1f} kN·m；虛線為 Cb × 直線（上限 Mp）",
            note="翼板 10.22 剛超過 λp，只算 LTB 會漏掉 FLB；Cb 只乘在 LTB，不乘在 FLB",
            path=path)
    return path


def fig2_load():
    W1, H1 = 1000, 400
    cv = Canvas(W1, H1, sx=1)
    cv.panel("由 Mu = φbMn 反推 WL（kN·m）", "wu = 1.2 × 5.8 + 1.6WL；Mu = wuL²/8 = 12.5wu")
    x0, sc = 120, 0.95
    y = 190
    md = 12.5 * 1.2 * Q_WD
    ml = Q_PHIMN - md
    cv.rect_px(x0, y - 22, sc * md, 44, C["compr"], 2)
    cv.rect_px(x0 + sc * md, y - 22, sc * ml, 44, C["load"], 2)
    cv.text_px(x0 + sc * md / 2, y + 40, f"靜載 12.5 × 6.96 = {md:.1f}", 12, C["compr"])
    cv.text_px(x0 + sc * md + sc * ml / 2, y, f"活載 12.5 × 1.6WL = {ml:.1f}", 13, "#FFFFFF", weight="700")
    cv.text_px(x0 + sc * Q_PHIMN + 8, y, f"= φbMn = {Q_PHIMN:.1f}", 13, C["bmd"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 70, f"6.96 + 1.6WL = {Q_PHIMN:.1f} / 12.5 = {Q_PHIMN / 12.5:.2f}", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 40, f"WL = ({Q_PHIMN / 12.5:.2f} − 6.96) / 1.6 = {Q_WL:.1f} kN/m", 15, C["bmd"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-load.svg")
    compose([cv], cols=1,
            title=f"圖 2　WL ≈ {Q_WL:.1f} kN/m：活載可用的彎矩 = φbMn − 1.2 靜載彎矩",
            sub="題目沒給載重組合係數，依 LRFD 取 1.2D + 1.6L",
            note="用 FLB 的 793.3 或忘了乘 1.2／1.6，WL 都會偏大",
            path=path)
    return path


FIGURES = [
    (fig1_limit, "§4 Step 2–6",
     "只算 LTB 漏 FLB；Cb 乘到 FLB；λf 判成結實"),
    (fig2_load, "§4 Step 7",
     "用較大的 FLB 強度反推；漏乘載重係數"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
