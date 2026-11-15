# -*- coding: utf-8 -*-
"""SM-2014-4 圖解。
fig-1-problem：題目附圖（圖四）重繪，幾何只取自題目正本 SM-2014-4-problem.md §4 判讀清單（#1–#4），不含任何解題結果。
用法：python gen_SM-2014-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
WT  = 2.0     # #1/#3 乾砂 0–2 m，地下水位地表下 2 m
Z_C = 8.0     # #1 砂土 2–8 m，黏土頂
Z_R = 16.0    # #1 黏土 8–16 m，其下岩盤

def fig_problem():
    W, H = 860, 620
    XL, XR = 0.0, 10.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 2.2, XR + 1.6), (-(Z_R + 1.4), 2.4), 40, 40, 60, 50))
    Y = lambda d: -d
    for d0, d1, col in [(0, WT, "rgba(180,83,9,0.12)"), (WT, Z_C, "rgba(180,83,9,0.24)"),
                        (Z_C, Z_R, "rgba(63,74,90,0.22)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(WT)), (XR, Y(WT)), C["member2"], 1.2)
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member2"], 1.8)
    cv.line((XL, Y(Z_R)), (XR, Y(Z_R)), C["member"], 2.6)
    for x in (1.5, 5.0, 8.0):
        for k in range(4):
            cv.line((x + k * 0.35, Y(Z_R)), (x + k * 0.35 - 0.3, Y(Z_R + 0.55)), C["member"], 1.4)
    # 均佈載重 Δσ
    for i in range(15):
        x = 0.35 + i * (XR - 0.7) / 14
        cv.arrow((x, Y(-1.6)), (x, Y(-0.05)), C["load"], 2.0, 7)
    cv.line((0.35, Y(-1.6)), (XR - 0.35, Y(-1.6)), C["load"], 2.0)
    cv.math_px(cv.X(XR + 0.25), cv.Y(Y(-1.6)), "Δσ", 15, C["load"], anchor="start", weight="700")
    # 地下水位
    wt_symbol(cv, 1.6, Y(WT), C["deform"], 0.16)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT)), "地下水位", 12.5, C["deform"], anchor="start", weight="700")
    # 層名與參數
    cv.text_px(cv.X(4.0), cv.Y(Y(1.0)), "乾砂", 13, C["text"], weight="700")
    cv.text_px(cv.X(4.0), cv.Y(Y(4.0)), "砂土", 13, C["text"], weight="700")
    cv.text_px(cv.X(0.4), cv.Y(Y(5.6)), "砂（乾砂與砂土）", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(0.4), cv.Y(Y(6.6)), "e = 0.62，Gs = 2.67", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(4.0), cv.Y(Y(10.6)), "黏土", 13, C["text"], weight="700")
    cv.text_px(cv.X(0.4), cv.Y(Y(12.2)), "eo = 1.05，Gs = 2.72", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(0.4), cv.Y(Y(13.2)), "ωL = 45%，正常壓密", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(4.0), cv.Y(Y(Z_R + 1.0)), "岩盤", 13, C["text"], weight="700")
    # 尺寸線
    xd = XL - 1.0
    cv.dim((xd, Y(WT)), (xd, Y(0)), "2 m", 0, C["dim"], 12.5, label_off=-28)
    cv.dim((xd, Y(Z_C)), (xd, Y(WT)), "6 m", 0, C["dim"], 12.5, label_off=-28)
    cv.dim((xd, Y(Z_R)), (xd, Y(Z_C)), "8 m", 0, C["dim"], 12.5, label_off=-28)
    for d in (0, WT, Z_C, Z_R):
        cv.line((xd - 0.25, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2014-4 題目附圖（圖四）重繪",
        sub="依題目正本判讀清單；黏土上為透水砂層，下為岩盤",
        note="攔錯用：黏土厚 8 m 在地表下 8–16 m；砂的 e、Gs 同時適用乾砂與水位下砂土；岩盤是黏土唯一的下邊界。",
        path=os.path.join(OUT, "SM-2014-4-fig-1-problem.svg"))


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

# ── 由 SM-2014-4 §4 解得 ──
SC_14, CV_14, HDR_14 = 35.12, 0.005, 8.0          # cm、cm²/s、m（岩盤不透水，單向排水）
S20 = 20.0; U20 = S20 / SC_14                      # 56.94%
T20 = _Tv(U20) * (HDR_14 * 100) ** 2 / CV_14 / 86400   # 377.3 天
T20_BAD = math.pi / 4 * U20 * (HDR_14 * 100) ** 2 / CV_14 / 86400   # 照考卷漏平方式 663 天
compose([st_panel(SC_14, CV_14, HDR_14, S20, T20, 4.0, "若誤取雙向排水 Hdr = 4 m", "", "", 1500, 40)],
        title="圖 2　沉陷—時間：20 cm 在 U = %.1f%%、%d 天達到" % (U20 * 100, round(T20)),
        sub="Terzaghi 理論，U ≤ 60%% 用 Tv = (π/4)·U 的平方；照考卷漏印平方的式子會得 %d 天" % round(T20_BAD),
        note="攔錯用：岩盤不透水 → 單向排水 Hdr = 8 m；誤取雙向排水時間只剩四分之一（虛線）。",
        path=os.path.join(OUT, "SM-2014-4-fig-2-settlement-time.svg"))
print(U20, T20, T20_BAD)
