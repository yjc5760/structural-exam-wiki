#!/usr/bin/env python3
"""
SS-2018-2 箱型斷面柱 LRFD 強度檢核 — 解題圖解腳本

用法：
    python3 gen_SS-2018-2.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2018-2-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2018-2.md §4，由下式即時算出（80 cm 為外緣寬，判讀 #2）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2018-2"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2018-2.md §4
# ══════════════════════════════════════════════════════════════
Q_BO, Q_T, Q_L = 80.0, 3.2, 400.0                # cm（題文）
Q_PU, Q_K1, Q_K2 = 1119.0, 2.284, 2.397          # tf、兩方向 K
Q_FY, Q_E = 3.3, 2040.0                          # tf/cm²
Q_BI = Q_BO - 2 * Q_T
Q_A = Q_BO ** 2 - Q_BI ** 2                      # 983.04
Q_R = math.sqrt((Q_BO ** 2 + Q_BI ** 2) / 12)    # 31.38
Q_BT = Q_BI / Q_T                                # 23.0
Q_LR_AISC = 1.40 * math.sqrt(Q_E / Q_FY)         # 34.8
Q_LR_TW = 50 / math.sqrt(Q_FY)                   # 27.5（國內寫法）
Q_KLR = max(Q_K1, Q_K2) * Q_L / Q_R              # 30.55
Q_LC = Q_KLR / math.pi * math.sqrt(Q_FY / Q_E)   # 0.391
Q_FCR = math.exp(-0.419 * Q_LC ** 2) * Q_FY      # 3.095
Q_PN = Q_FCR * Q_A
Q_PHI = {"0.85（國內 99 年版）": 0.85, "0.90（AISC 360-16）": 0.90}


def fig1_section():
    W1, H1 = 1000, 520
    cv = Canvas(W1, H1, sx=4.0, ox=230, oy=H1 / 2 - 20)
    cv.panel("箱型 80 × 80 × 3.2：斷面性質與壁板 b/t", "80 cm 為外緣；四片壁板四邊有支撐（stiffened）")
    h, hi = Q_BO / 2, Q_BI / 2
    cv.polygon([(-h, -h), (h, -h), (h, h), (-h, h)], C["fill_c"], C["member"], 1.6)
    cv.polygon([(-hi, -hi), (hi, -hi), (hi, hi), (-hi, hi)], C["panel"] if "panel" in C else "#F5F6F9", C["member"], 1.4)
    cv.dim((-h, -h), (h, -h), f"{Q_BO:g}", off=26, label_off=14)
    cv.dim((-hi, hi - 6), (hi, hi - 6), f"b = {Q_BI:.1f}", off=0, label_off=-14)
    cv.text((h, 0), f"t = {Q_T}", 12.5, C["text"], "start", dx=10)
    x0 = 480
    rows = [(f"A = 80² − 73.6² = {Q_A:.2f} cm²", C["text"], "400"),
            (f"r² = (80² + 73.6²)/12 ⇒ r = {Q_R:.2f} cm", C["text"], "400"),
            ("（正方形：兩軸 r 相同）", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        cv.text_px(x0, 130 + i * 30, s, 13, col, "start", weight=wt)
    sc = 12.0
    bars = [("b/t = 73.6 / 3.2", Q_BT, C["bmd"]),
            ("國內 50/√Fy", Q_LR_TW, C["ghost"]),
            ("AISC 1.40√(E/Fy)", Q_LR_AISC, C["ghost"])]
    for i, (lab, v, col) in enumerate(bars):
        y = 265 + i * 58
        cv.text_px(x0, y - 20, lab, 12.5, C["text"], "start")
        cv.rect_px(x0, y - 9, sc * v, 18, col, 3)
        cv.text_px(x0 + sc * v + 8, y, f"{v:.1f}", 13, C["bmd"] if col == C["bmd"] else C["muted"], "start", weight="700")
    cv.text_px(x0, H1 - 36, f"{Q_BT:.1f} 小於 {Q_LR_TW:.1f}、{Q_LR_AISC:.1f} ⇒ 非細長，Q = 1，全斷面有效", 13, C["bmd"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-section.svg")
    compose([cv], cols=1,
            title=f"圖 1　A = {Q_A:.2f} cm²、r = {Q_R:.2f} cm；壁板 b/t = {Q_BT:.1f} 通過局部挫屈",
            sub="b 取內淨寬（板件在兩側腹板之間的寬度），不是外寬 80",
            note="把 80 當內寬、或忘了檢核 b/t，就沒完成「強度設計檢核」",
            path=path)
    return path


def fig2_strength():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("Fcr / Fy 對 λc 與設計強度", f"控制 K = {max(Q_K1, Q_K2)}：KL/r = {Q_KLR:.2f}，λc = {Q_LC:.3f}")
    X0, X1, YB, YT = 100, 560, 440, 110
    lmax = 2.5
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda r: YB - (YB - YT) * r / 1.05
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for i in range(6):
        cv.text_px(PX(0.5 * i), YB + 18, f"{0.5 * i:.1f}", 11.5, C["muted"])
    for i in range(6):
        cv.text_px(X0 - 8, PY(0.2 * i), f"{0.2 * i:.1f}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(0.2 * i), X1, PY(0.2 * i), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "λc", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Fcr / Fy", 13, C["text"], "start", weight="700")
    ls = [lmax * i / 250 for i in range(0, 251)]
    cv.poly([(PX(l), H1 - PY(math.exp(-0.419 * l * l) if l <= 1.5 else 0.877 / l ** 2)) for l in ls], C["bmd"], 2.8)
    _hl(cv, H1, PX(1.5), YB, PX(1.5), YT, C["accent"], 1.2, dash="5 4")
    cv.text_px(PX(1.5) + 4, YT + 6, "1.5", 12, C["accent"], "start")
    rr = Q_FCR / Q_FY
    _hl(cv, H1, PX(Q_LC), YB, PX(Q_LC), PY(rr), C["load"], 1.2, dash="4 3")
    cv.dot((PX(Q_LC), H1 - PY(rr)), 6.5, fill=C["load"])
    cv.text_px(PX(Q_LC) + 10, PY(0.42), f"λc = {Q_LC:.3f}", 12.5, C["load"], "start", weight="700")
    cv.text_px(PX(Q_LC) + 10, PY(0.42) + 22, f"Fcr/Fy = {rr:.4f}", 12.5, C["load"], "start")
    x0, sc = 610, 0.11
    cv.text_px(x0, 140, f"Fcr = {rr:.4f} × {Q_FY} = {Q_FCR:.3f}", 13, C["text"], "start")
    cv.text_px(x0, 170, f"Pn = {Q_FCR:.3f} × {Q_A:.2f} = {Q_PN:,.0f} tf", 13, C["text"], "start")
    for i, (lab, phi) in enumerate(Q_PHI.items()):
        y = 230 + i * 92
        cap = phi * Q_PN
        cv.text_px(x0, y - 22, f"φc = {lab}", 12.5, C["text"], "start")
        cv.rect_px(x0, y - 10, sc * cap, 20, C["fill_m"], 3, stroke=C["bmd"], sw=1.2)
        cv.rect_px(x0, y - 10, sc * Q_PU, 20, C["load"], 3)
        cv.text_px(x0 + sc * cap + 6, y, f"{cap:,.0f}", 12.5, C["bmd"], "start", weight="700")
        cv.text_px(x0, y + 26, f"Pu / φcPn = {Q_PU:,.0f} / {cap:,.0f} = {Q_PU / cap:.3f}", 12.5, C["bmd"], "start", weight="700")
    cv.text_px(x0, H1 - 46, "紅：Pu = 1,119 tf；外框：φcPn", 12, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-strength.svg")
    compose([cv], cols=1,
            title=f"圖 2　λc = {Q_LC:.3f}（非彈性），φcPn = {0.85 * Q_PN:,.0f} tf，Pu / φcPn = {Q_PU / (0.85 * Q_PN):.3f} ⇒ OK",
            sub="控制方向取兩個 K 的大者 2.397；正方形斷面兩軸 r 相同",
            note="取較小 K（2.284）會高估強度；λc ≤ 1.5 才用指數式",
            path=path)
    return path


FIGURES = [
    (fig1_section, "§4 Step 1–2",
     "80 當內寬；b 取外寬算 b/t；漏做局部挫屈檢核"),
    (fig2_strength, "§4 Step 3–6",
     "控制 K 取 2.284；λc 公式漏 π；φc 未註明版本"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
