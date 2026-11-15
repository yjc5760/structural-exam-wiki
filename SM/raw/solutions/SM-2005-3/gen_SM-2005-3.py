# -*- coding: utf-8 -*-
"""SM-2005-3 圖解。所有數值取自 SM-2005-3.md §4（二）。
用法：python gen_SM-2005-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 由 SM-2005-3 §4（二）解得 ──
GW = 9.81
H_C = 5.0
S0 = (20.0 - GW) * H_C / 2          # 25.475 kPa 中點初始有效應力（水位在黏土頂）
DS = 20.0 * 10.0                    # 200 kPa 回填
SF = S0 + DS                        # 225.475
TABLE = [(0, 60, 6.2e-4), (60, 120, 4.0e-4), (120, 180, 1.4e-4), (180, 300, 0.3e-4)]   # 考卷附表
segs = [(max(a, S0), min(b, SF), mv) for a, b, mv in TABLE if b > S0 and a < SF]
parts = [(a, b, mv, mv * H_C * (b - a)) for a, b, mv in segs]
S_TOT = sum(p[3] for p in parts)    # 0.2758 m

def fig_mv():
    W, H = 900, 520
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.7), (0, 1.0), 70, 40, 80, 76))
    XMAX, YMAX = 300.0, 7.0e-4
    SX = lambda s: s / XMAX * 1.7
    SY = lambda m: m / YMAX
    frame(cv, 0, 1.7, 0, 1.0, [], [], "有效應力 σ'（kPa）", "", grid=False)
    cv.math_px(cv.X(0) - 10, cv.Y(1.0) - 22, "m_v (10^{-4} kPa^{-1})", 13, C["text"], anchor="start")
    for v in (0, 60, 120, 180, 240, 300):
        cv.line((SX(v), 0), (SX(v), 1.0), C["border"], 1.0)
        cv.text_px(cv.X(SX(v)), cv.Y(0) + 17, "%d" % v, 12.5, C["muted"])
    for v in (0, 2, 4, 6):
        cv.line((0, SY(v * 1e-4)), (1.7, SY(v * 1e-4)), C["border"], 1.0)
        cv.text_px(cv.X(0) - 9, cv.Y(SY(v * 1e-4)), "%d" % v, 12.5, C["muted"], anchor="end")
    for a, b, mv in TABLE:                       # 附表階梯（全範圍，淡色）
        cv.line((SX(a), SY(mv)), (SX(b), SY(mv)), C["muted"], 2.0, dash="4 3")
    for k, (a, b, mv, s) in enumerate(parts):    # 實際用到的段（面積 × H = 沉陷）
        cv.polygon([(SX(a), 0), (SX(b), 0), (SX(b), SY(mv)), (SX(a), SY(mv))], C["bmd"], C["bmd"], 1.6, op=0.35 + 0.1 * (k % 2))
        tag_px(cv, cv.X(SX((a + b) / 2)), cv.Y(SY(mv)) - 18, "%.1f cm" % (s * 100), 12.5, C["bmd"])
    for s, lab in ((S0, "σ'0 = %.1f" % S0), (SF, "σ'f = %.1f" % SF)):
        cv.line((SX(s), 0), (SX(s), 1.0), C["accent"], 2.2, dash="7 4")
        tag_px(cv, cv.X(SX(s)), cv.Y(0.78), lab, 12.5, C["accent"])
    tag_px(cv, cv.X(SX(262)), cv.Y(0.45), "S = H Σ m_v Δσ' = %.2f cm" % (S_TOT * 100), 13.5, C["text"])
    return cv

compose([fig_mv()],
        title="圖 1　m_v 依有效應力分段：沉陷 = 層厚 × 陰影面積",
        sub="黏土中點 σ' 由 25.5 增至 225.5 kPa，橫跨附表四個區段，每段用自己的 m_v",
        note="攔錯用：整段只用第一格 m_v = 6.2（×1E-4），沉陷會算成 62 cm；只用 σ'f 所在區段 0.3（×1E-4），只有 3 cm。",
        path=os.path.join(OUT, "SM-2005-3-fig-1-mv-steps.svg"))
