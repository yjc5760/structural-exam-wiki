# -*- coding: utf-8 -*-
"""SM-2015-1 圖解。數值取自 SM-2015-1.md §4。用法：python gen_SM-2015-1.py [輸出資料夾]"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)


# ══════ 沉陷—時間曲線（解題圖解）══════
import math
def _Tv(U):          # Terzaghi 平均壓密度 → 時間因數（U 以小數）
    return math.pi / 4 * U ** 2 if U <= 0.6 else 1.781 - 0.933 * math.log10(100 - 100 * U)
def st_panel(SC, CV, HDR, S_T, T_T, ALT_HDR, ALT_LABEL, title, sub, TMAX, SMAX, ALT_T=None):
    """SC 最終沉陷（cm）、CV（cm²/s）、HDR（m）；S_T、T_T 目標沉陷與時間（cm、天）。"""
    W, H = 900, 520
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.7), (0, 1.0), 76, 210, 76, 76))
    SX = lambda t: t / TMAX * 1.7
    SY = lambda s: s / SMAX            # 沉陷向下畫：y = 1 - s/SMAX
    Y = lambda s: 1 - SY(s)
    frame(cv, 0, 1.7, 0, 1.0, [], [], "時間 t（天）", "", grid=False)
    cv.text_px(cv.X(0) - 10, cv.Y(1.0) - 22, "沉陷 S（cm，向下）", 13, C["text"], anchor="start")
    step_t = TMAX / 5
    for k in range(6):
        t = k * step_t
        cv.line((SX(t), 0), (SX(t), 1.0), C["border"], 1.0)
        cv.text_px(cv.X(SX(t)), cv.Y(0) + 17, "%d" % round(t), 12.5, C["muted"])
    for s in range(0, int(SMAX) + 1, 10):
        cv.line((0, Y(s)), (1.7, Y(s)), C["border"], 1.0)
        cv.text_px(cv.X(0) - 9, cv.Y(Y(s)), "%d" % s, 12.5, C["muted"], anchor="end")
    def curve_pts(hdr):
        pts = [(0, Y(0))]
        for i in range(1, 600):
            t = TMAX * (i / 599) ** 2
            Tv = CV * t * 86400 / (hdr * 100) ** 2
            pts.append((SX(t), Y(U_avg(max(Tv, 1e-6)) * SC)))
        return pts
    cv.poly(curve_pts(HDR), C["deform"], 3.0)
    cv.poly(curve_pts(ALT_HDR), C["muted"], 2.2, dash="7 4")
    cv.line((0, Y(SC)), (1.7, Y(SC)), C["member"], 1.6, dash="3 3")
    cv.text_px(cv.X(1.7) + 8, cv.Y(Y(SC)), "Sc = %.2f cm" % SC, 12.5, C["member"], anchor="start", weight="700")
    cv.line((0, Y(S_T)), (SX(T_T), Y(S_T)), C["accent"], 1.6, dash="6 4")
    cv.line((SX(T_T), 0), (SX(T_T), Y(S_T)), C["accent"], 1.6, dash="6 4")
    cv.dot((SX(T_T), Y(S_T)), 6, fill=C["accent"])
    tag_px(cv, cv.X(SX(T_T)) + 12, cv.Y(Y(S_T)) - 20, "%.2f cm，%d 天" % (S_T, round(T_T)), 12.5, C["accent"], anchor="start")
    lx, ly = cv.X(1.7) + 8, cv.Y(0.55)
    for k, (col, dash, lab) in enumerate([(C["deform"], None, "本解：Hdr = %g m" % HDR), (C["muted"], "7 4", ALT_LABEL)]):
        d_ = ' stroke-dasharray="%s"' % dash if dash else ""
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"%s/>' % (lx, ly + k * 24, lx + 28, ly + k * 24, col, d_))
        cv.text_px(lx + 36, ly + k * 24, lab, 12.5, col, anchor="start", weight="700")
    return cv

# ── 由 SM-2015-1 §4 解得 ──
SC_15, CV_15, HDR_15 = 52.46, 0.003, 4.0           # cm、cm²/s、m（上預載砂、下砂層：雙向排水）
T80 = 0.567                                         # 題給
S80 = 0.80 * SC_15
T_80 = T80 * (HDR_15 * 100) ** 2 / CV_15 / 86400    # 350 天
compose([st_panel(SC_15, CV_15, HDR_15, S80, T_80, 8.0, "若誤取單向排水 Hdr = 8 m", "", "", 1500, 60)],
        title="圖 1　預壓沉陷—時間：壓密 80%% 時 %.2f cm、%d 天" % (S80, round(T_80)),
        sub="題給 T80 = 0.567；預載砂與下方砂層都透水，雙向排水 Hdr = 4 m",
        note="攔錯用：預載砂讓黏土頂也成為排水面；誤取單向排水 Hdr = 8 m 時需 1400 天（虛線）。",
        path=os.path.join(OUT, "SM-2015-1-fig-1-settlement-time.svg"))
print(S80, T_80)
