#!/usr/bin/env python3
"""
SS-2017-3 H700×300×25×50 軸壓柱 ASD 容許應力合理性 — 解題圖解腳本

用法：
    python3 gen_SS-2017-3.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2017-3-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2017-3.md §4，由下式即時算出（E = 2040 tf/cm²，Fy 由 Cc = 128 反推）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2017-3"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2017-3.md §4
# ══════════════════════════════════════════════════════════════
Q_D, Q_BF, Q_TW, Q_TF = 70.0, 30.0, 2.5, 5.0          # cm（題目正本判讀 #1）
Q_L, Q_KX, Q_KY, Q_CC = 600.0, 0.8, 2.1, 128.0         # 題文
Q_E = 2040.0
Q_FA_ENG = 0.34                                        # 工程師所得 Fa/Fy
Q_HW = Q_D - 2 * Q_TF
Q_A = 2 * Q_BF * Q_TF + Q_HW * Q_TW
Q_IX = 2 * (Q_BF * Q_TF ** 3 / 12 + Q_BF * Q_TF * ((Q_D - Q_TF) / 2) ** 2) + Q_TW * Q_HW ** 3 / 12
Q_IY = 2 * Q_TF * Q_BF ** 3 / 12 + Q_HW * Q_TW ** 3 / 12
Q_RX, Q_RY = math.sqrt(Q_IX / Q_A), math.sqrt(Q_IY / Q_A)
Q_SX = Q_KX * Q_L / Q_RX                                # 16.9
Q_SY = Q_KY * Q_L / Q_RY                                # 177.9（控制）
Q_SBAD = Q_KY * Q_L / Q_RX                              # 44.4（Ky 配 rx）
Q_FY = 2 * math.pi ** 2 * Q_E / Q_CC ** 2               # 2.458


def q_fa_fy(klr):
    """ASD Fa / Fy"""
    if klr >= Q_CC:
        return 12 * math.pi ** 2 * Q_E / (23 * klr ** 2) / Q_FY
    rr = klr / Q_CC
    return (1 - rr ** 2 / 2) / (5 / 3 + 3 * rr / 8 - rr ** 3 / 8)


def q_klr_for(ratio):
    lo, hi = 0.0, 250.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if q_fa_fy(mid) > ratio:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


Q_K_ENG = q_klr_for(Q_FA_ENG)


def fig1_axes():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=4.6, ox=200, oy=H1 / 2 - 20)
    cv.panel("H700×300×25×50：兩軸各自的 KL/r", "強軸 x（水平）、弱軸 y（垂直）；斷面依比例（cm）")
    h, b = Q_D / 2, Q_BF / 2
    for sgn in (1, -1):
        y0 = sgn * h
        y1 = sgn * (h - Q_TF)
        cv.polygon([(-b, y0), (b, y0), (b, y1), (-b, y1)], C["fill_c"], C["member"], 1.6)
    cv.polygon([(-Q_TW / 2, -(h - Q_TF)), (Q_TW / 2, -(h - Q_TF)), (Q_TW / 2, h - Q_TF), (-Q_TW / 2, h - Q_TF)], C["fill_c"], C["member"], 1.6)
    cv.line((-b - 6, 0), (b + 6, 0), C["compr"], 1.4, dash="8 3 2 3")
    cv.line((0, -h - 5), (0, h + 5), C["sfd"], 1.4, dash="8 3 2 3")
    cv.text((b + 6, 0), "x", 14, C["compr"], "start", dx=6, weight="700")
    cv.text((0, h + 5), "y", 14, C["sfd"], dy=-12, weight="700")
    cv.dim((-b, -h), (b, -h), f"{Q_BF:g}", off=26, label_off=14)
    cv.dim((b, -h), (b, h), f"{Q_D:g}", off=40, label_off=22)
    x0, sc = 470, 2.3
    rows = [(f"強軸 KxL/rx = {Q_KX}×{Q_L:g}/{Q_RX:.2f}", Q_SX, C["compr"], ""),
            (f"弱軸 KyL/ry = {Q_KY}×{Q_L:g}/{Q_RY:.3f}", Q_SY, C["load"], "控制"),
            (f"誤：Ky 配 rx = {Q_KY}×{Q_L:g}/{Q_RX:.2f}", Q_SBAD, C["ghost"], "")]
    for i, (lab, v, col, tag) in enumerate(rows):
        y = 150 + i * 92
        cv.text_px(x0, y - 26, lab, 12.5, C["text"], "start")
        cv.rect_px(x0, y - 12, sc * v, 24, col, 3)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}" + (f"（{tag}）" if tag else ""), 13.5, col if col != C["ghost"] else C["muted"], "start", weight="700")
    xc = x0 + sc * Q_CC
    wp = lambda px, py: ((px - cv.ox) / cv.sx, (cv.h - py - cv.oy) / cv.sx)   # 像素 → 世界座標
    cv.line(wp(xc, 110), wp(xc, 380), C["accent"], 1.6, dash="5 4", cap="butt")
    cv.text_px(xc, 398, f"Cc = {Q_CC:g}", 12.5, C["accent"], weight="700")
    cv.text_px(x0, H1 - 52, f"A = {Q_A:g} cm²、Ix = {Q_IX:,.0f}、Iy = {Q_IY:,.0f} cm⁴", 12.5, C["muted"], "start")
    cv.text_px(x0, H1 - 28, f"rx = {Q_RX:.2f}、ry = {Q_RY:.3f} cm", 12.5, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-1-axes.svg")
    compose([cv], cols=1,
            title=f"圖 1　弱軸 KyL/ry = {Q_SY:.1f} 超過 Cc = {Q_CC:g}，控制；強軸只有 {Q_SX:.1f}",
            sub="K 與 r 必須是同一軸：Kx 配 rx、Ky 配 ry",
            note="只算強軸、或把 Ky 配上 rx（44.4），都會落在非彈性段而高估 Fa",
            path=path)
    return path


def fig2_fa():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("ASD Fa / Fy 對 KL/r（Cc = 128）", f"Fy 由 Cc 反推 = 2π²E/Cc² = {Q_FY:.3f} tf/cm²")
    X0, X1, YB, YT = 100, 640, 460, 110
    kmax, rmax = 200.0, 0.6
    PX = lambda k: X0 + (X1 - X0) * k / kmax
    PY = lambda r: YB - (YB - YT) * r / rmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 201, 50):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for i in range(7):
        r = 0.1 * i
        cv.text_px(X0 - 8, PY(r), f"{r:.1f}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(r), X1, PY(r), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "KL/r", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Fa / Fy", 13, C["text"], "start", weight="700")
    ks = [kmax * i / 300 for i in range(0, 301)]
    cv.poly([(PX(k), H1 - PY(q_fa_fy(k))) for k in ks], C["compr"], 2.8)
    _hl(cv, H1, PX(Q_CC), YB, PX(Q_CC), YT, C["accent"], 1.2, dash="5 4")
    cv.text_px(PX(Q_CC) + 4, YT + 6, f"Cc = {Q_CC:g}", 12, C["accent"], "start")
    marks = [(Q_SY, q_fa_fy(Q_SY), f"弱軸 {Q_SY:.1f}：{q_fa_fy(Q_SY):.3f}（正確）", C["bmd"], 1, -16),
             (Q_K_ENG, Q_FA_ENG, f"0.34Fy 對應 KL/r ≈ {Q_K_ENG:.0f}", C["load"], 1, -14),
             (Q_SBAD, q_fa_fy(Q_SBAD), f"Ky 配 rx {Q_SBAD:.1f}：{q_fa_fy(Q_SBAD):.2f}", C["muted"], -1, 26),
             (Q_SX, q_fa_fy(Q_SX), f"強軸 {Q_SX:.1f}：{q_fa_fy(Q_SX):.2f}", C["muted"], 1, -12)]
    for k, r, lab, col, side, dy in marks:
        _hl(cv, H1, PX(k), YB, PX(k), PY(r), col, 1.0, dash="3 4")
        cv.dot((PX(k), H1 - PY(r)), 6 if col == C["bmd"] else 5, fill=col)
        cv.text_px(PX(k) + 8 * side, PY(r) + dy, lab, 12, col, "start" if side > 0 else "end", weight="700")
    xt = 680
    rows = [("彈性段 Fa = 12π²E / 23(KL/r)²", C["text"], "400"),
            (f"= 12π² × 2040 / (23 × {Q_SY:.1f}²)", C["text"], "400"),
            (f"= {q_fa_fy(Q_SY) * Q_FY:.4f} tf/cm²", C["bmd"], "700"),
            (f"Fa / Fy = {q_fa_fy(Q_SY):.3f}", C["bmd"], "700"),
            ("", C["text"], "400"),
            (f"工程師 0.34 是正確值的 {Q_FA_ENG / q_fa_fy(Q_SY):.1f} 倍", C["load"], "700"),
            ("⇒ 不合理，偏不安全", C["load"], "700")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-fa.svg")
    compose([cv], cols=1,
            title=f"圖 2　正確 Fa = {q_fa_fy(Q_SY):.3f}Fy；工程師的 0.34Fy 相當於 KL/r ≈ {Q_K_ENG:.0f} 的柱",
            sub="弱軸細長比落在彈性段，Fa 與 Fy 無關",
            note="KL/r 超過 Cc 仍套非彈性公式、或只看強軸，都會得到偏高的 Fa",
            path=path)
    return path


FIGURES = [
    (fig1_axes, "§4 Step 1–3",
     "只算強軸 KL/r；Ky 配 rx；斷面 I 漏翼板平行軸項"),
    (fig2_fa, "§4 Step 4–5",
     "KL/r 超過 Cc 仍用非彈性式；把 0.34Fy 判為合理"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
