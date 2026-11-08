#!/usr/bin/env python3
"""
SS-2025-3 RH700×300×13×24 塑性彎矩、彈性彎矩與標稱彎矩強度 — 解題圖解腳本

用法：
    python3 gen_SS-2025-3.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2025-3-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2025-3.md §4，由下式即時算出（單位 tf、cm）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2025-3"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2025-3.md §4
# ══════════════════════════════════════════════════════════════
Q_D, Q_BF, Q_TW, Q_TF = 70.0, 30.0, 1.3, 2.4      # cm
Q_IX, Q_FY, Q_FR = 197000.0, 3.5, 0.7             # 題給
Q_LB, Q_LP, Q_LR = 3.0, 3.4, 10.5                 # m（題給）
Q_HW = Q_D - 2 * Q_TF
Q_SX = Q_IX / (Q_D / 2)                            # 5,628.6
Q_ARM_F = Q_HW / 2 + Q_TF / 2                     # 33.8
Q_ARM_W = Q_HW / 4                                # 16.3
Q_ZF = 2 * Q_BF * Q_TF * Q_ARM_F                  # 4,867.2
Q_ZW = 2 * (Q_HW / 2 * Q_TW) * Q_ARM_W            # 1,381.6
Q_ZX = Q_ZF + Q_ZW                                # 6,248.8
Q_MP = Q_FY * Q_ZX
Q_MR = (Q_FY - Q_FR) * Q_SX


def fig1_zx():
    W1, H1 = 1000, 520
    cv = Canvas(W1, H1, sx=5.0, ox=210, oy=H1 / 2 - 20)
    cv.panel("Zx = Σ(面積 × 至塑性中性軸距離)：翼板 ＋ 腹板", "對稱 H 型：塑性中性軸在腹板中點；全斷面拉壓各達 Fy")
    h = Q_D / 2
    for sgn in (1, -1):
        y0, y1 = sgn * h, sgn * (h - Q_TF)
        cv.polygon([(-Q_BF / 2, y0), (Q_BF / 2, y0), (Q_BF / 2, y1), (-Q_BF / 2, y1)], C["fill_c"], C["member"], 1.4)
    cv.polygon([(-Q_TW / 2, -(h - Q_TF)), (Q_TW / 2, -(h - Q_TF)), (Q_TW / 2, h - Q_TF), (-Q_TW / 2, h - Q_TF)], C["fill_c"], C["member"], 1.4)
    cv.line((-Q_BF / 2 - 4, 0), (Q_BF / 2 + 4, 0), C["accent"], 1.4, dash="8 3 2 3")
    cv.text((Q_BF / 2 + 4, 0), "PNA", 12, C["accent"], "start", dx=6, weight="700")
    xs = Q_BF / 2 + 14
    sw = 12
    cv.polygon([(xs, 0), (xs + sw, 0), (xs + sw, h), (xs, h)], "rgba(29,78,216,0.25)", C["compr"], 1.6)
    cv.polygon([(xs, 0), (xs - 0.01, 0), (xs - 0.01, -h), (xs, -h)], "none", "none")
    cv.polygon([(xs, 0), (xs + sw, 0), (xs + sw, -h), (xs, -h)], "rgba(124,58,237,0.25)", C["sfd"], 1.6)
    cv.text((xs + sw / 2, h), "Fy（壓）", 12, C["compr"], dy=-10, weight="700")
    cv.text((xs + sw / 2, -h), "Fy（拉）", 12, C["sfd"], dy=18, weight="700")
    cv.dim((-Q_BF / 2 - 8, 0), (-Q_BF / 2 - 8, Q_ARM_F), f"{Q_ARM_F:.1f}", off=0, label_off=-22)
    cv.dim((-6, 0), (-6, Q_ARM_W), f"{Q_ARM_W:.1f}", off=0, label_off=-18)
    xt = 520
    rows = [(f"翼板：2 × (30 × 2.4) × {Q_ARM_F:.1f} = {Q_ZF:,.1f}", C["text"], "400"),
            (f"腹板：2 × (32.6 × 1.3) × {Q_ARM_W:.1f} = {Q_ZW:,.1f}", C["text"], "400"),
            (f"Zx = {Q_ZX:,.1f} cm³", C["bmd"], "700"),
            ("", C["text"], "400"),
            (f"Sx = Ix / (d/2) = 197,000 / 35 = {Q_SX:,.1f} cm³", C["text"], "400"),
            ("Zx 大於 Sx：塑性比彈性多用到腹板與翼板內側", C["muted"], "400"),
            ("", C["text"], "400"),
            (f"Mp = Fy·Zx = {Q_MP:,.0f} tf·cm ≈ {Q_MP / 100:.1f} tf·m", C["bmd"], "700"),
            (f"Mr = (Fy − Fr)·Sx = {Q_MR:,.0f} tf·cm ≈ {Q_MR / 100:.1f} tf·m", C["compr"], "700")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 130 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-zx.svg")
    compose([cv], cols=1,
            title=f"圖 1　Zx = {Q_ZF:,.1f} + {Q_ZW:,.1f} = {Q_ZX:,.1f} cm³；Mp = {Q_MP / 100:.1f}、Mr = {Q_MR / 100:.1f} tf·m",
            sub="翼板力臂量到翼板形心（hw/2 + tf/2），腹板半高的力臂是 hw/4",
            note="用 Sx 算 Mp、或 Mr 漏扣殘留應力（取 FySx），都會把「塑性」與「彈性」彎矩混在一起",
            path=path)
    return path


def fig2_mn():
    W1, H1 = 1000, 500
    cv = Canvas(W1, H1, sx=1)
    cv.panel("Mn 對 Lb（tf·m；題給 Lp、Lr、Cb = 1）", "Lb = 3.0 m 小於 Lp = 3.4 m：塑性區，Mn = Mp")
    X0, X1, YB, YT = 100, 640, 420, 110
    lmax, mmax = 12.0, 240.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda m: YB - (YB - YT) * m / mmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 13, 2):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for v in range(0, 241, 60):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "Lb（m）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Mn（tf·m）", 13, C["text"], "start", weight="700")
    cv.poly([(PX(0), H1 - PY(Q_MP / 100)), (PX(Q_LP), H1 - PY(Q_MP / 100)), (PX(Q_LR), H1 - PY(Q_MR / 100))], C["bmd"], 2.8)
    cv.poly([(PX(Q_LR), H1 - PY(Q_MR / 100)), (PX(12), H1 - PY(Q_MR / 100 * (Q_LR / 12) ** 1.6))], C["ghost"], 2, dash="6 4")
    cv.text_px(PX(11.3), PY(Q_MR / 100 * (Q_LR / 11.3) ** 1.6) + 26, "彈性區（示意）", 11.5, C["muted"])
    for l, lab in ((Q_LP, f"Lp = {Q_LP}"), (Q_LR, f"Lr = {Q_LR}")):
        _hl(cv, H1, PX(l), YB, PX(l), YT, C["accent"], 1.1, dash="4 4")
        cv.text_px(PX(l) + 4, YT + 6, lab, 11.5, C["accent"], "start")
    cv.dot((PX(Q_LB), H1 - PY(Q_MP / 100)), 7, fill=C["load"])
    cv.text_px(PX(Q_LB) - 6, PY(Q_MP / 100) + 28, f"Lb = {Q_LB}：Mn = Mp = {Q_MP / 100:.1f}", 13, C["load"], "start", weight="700")
    cv.text_px(PX(Q_LR) - 8, PY(Q_MR / 100) + 20, f"Mr = {Q_MR / 100:.1f}", 12, C["compr"], "end", weight="700")
    xt = 680
    rows = [("題目三問：", C["text"], "700"),
            (f"塑性彎矩 Mp = {Q_MP / 100:.1f} tf·m", C["bmd"], "700"),
            (f"彈性彎矩 Mr = {Q_MR / 100:.1f} tf·m", C["compr"], "700"),
            (f"標稱強度 Mn = Mp = {Q_MP / 100:.1f} tf·m", C["load"], "700"),
            ("", C["text"], "400"),
            ("題目問「標稱」：答 Mn，不乘 φb", C["muted"], "400"),
            (f"（φbMn = {0.9 * Q_MP / 100:.1f} 僅供參考）", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-mn.svg")
    compose([cv], cols=1,
            title=f"圖 2　Lb = 3.0 m 小於 Lp = 3.4 m：標稱強度 Mn = Mp = {Q_MP / 100:.1f} tf·m",
            sub="Lp、Lr、Cb 題目已給，直接比較，不必重算",
            note="把設計強度 φbMn 當成標稱強度作答、或自行重算 Lp 而與題給值不符，都是常見失分",
            path=path)
    return path


FIGURES = [
    (fig1_zx, "§4 Step 2–4",
     "翼板力臂取 d/2；腹板漏算；用 Sx 算 Mp；Mr 漏扣 Fr"),
    (fig2_mn, "§4 Step 5–6",
     "答成 φbMn；自行重算 Lp、Lr"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
