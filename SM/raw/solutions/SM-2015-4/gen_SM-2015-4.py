# -*- coding: utf-8 -*-
"""SM-2015-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2015-4-problem.md §4 判讀清單（#1–#3），不含任何解題結果。
用法：python gen_SM-2015-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
WT  = 3.0     # #2 地下水位地表下 3 m
Z_C = 9.0     # #1 砂 0–9 m
Z_B = 17.0    # #1 黏土 9–17 m，其下 γsat = 18 的土層（#3）

def fig_problem():
    W, H = 860, 600
    XL, XR = 0.0, 10.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 2.8, XR + 1.6), (-(Z_B + 2.6), 0.8), 40, 40, 60, 50))
    Y = lambda d: -d
    for d0, d1, col in [(0, WT, "rgba(180,83,9,0.12)"), (WT, Z_C, "rgba(180,83,9,0.24)"),
                        (Z_C, Z_B, "rgba(63,74,90,0.22)"), (Z_B, Z_B + 2.0, "rgba(180,83,9,0.10)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member"], 2.0)
    cv.line((XL, Y(Z_B)), (XR, Y(Z_B)), C["member"], 2.0)
    cv.line((XL, Y(WT)), (XR, Y(WT)), C["deform"], 1.6, dash="8 5")
    wt_symbol(cv, 1.4, Y(WT), C["deform"], 0.16)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT)), "地下水位", 12.5, C["deform"], anchor="start", weight="700")
    # 參數
    cv.rect_px(cv.X(4.4), cv.Y(Y(4.0)) - 16, 200, 82, "#FFFFFFDD", 6, "rgba(0,0,0,0.12)", 1)
    cv.text_px(cv.X(4.6), cv.Y(Y(4.0)), "Sand", 13, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(4.6), cv.Y(Y(4.0)) + 24, "γdry = 16 kN/m³", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(4.6), cv.Y(Y(4.0)) + 48, "γsat = 18 kN/m³", 12.5, C["text"], anchor="start")
    cv.rect_px(cv.X(4.4), cv.Y(Y(11.0)) - 16, 220, 106, "#FFFFFFEE", 6, "rgba(0,0,0,0.12)", 1)
    cv.text_px(cv.X(4.6), cv.Y(Y(11.0)), "Clay（正常壓密）", 13, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(4.6), cv.Y(Y(11.0)) + 24, "e = 0.9，LL = 50", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(4.6), cv.Y(Y(11.0)) + 48, "γsat = 17.5 kN/m³", 12.5, C["text"], anchor="start")
    cv.math_px(cv.X(4.6), cv.Y(Y(11.0)) + 72, "k = 10^{-7} m/s", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(3.0), cv.Y(Y(Z_B + 1.0)), "γsat = 18 kN/m³（考卷未標土名）", 12.5, C["text"])
    # 尺寸線
    xd = XL - 1.0
    cv.dim((xd, Y(WT)), (xd, Y(0)), "3 m", 0, C["dim"], 12.5, label_off=14)
    cv.dim((xd - 1.0, Y(Z_C)), (xd - 1.0, Y(0)), "9 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((xd, Y(Z_B)), (xd, Y(Z_C)), "8 m", 0, C["dim"], 12.5, label_off=-28)
    for d in (0, WT, Z_C, Z_B):
        cv.line((xd - 1.1, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2015-4 題目附圖重繪",
        sub="依題目正本判讀清單；抽降的是黏土上方砂土層的水頭",
        note="攔錯用：9 m 是砂層全厚、3 m 是水位深；黏土下方地層只標 γsat = 18，題目正本判讀為透水層（水頭不受抽水影響）。",
        path=os.path.join(OUT, "SM-2015-4-fig-1-problem.svg"))


# ══════ fig-2：抽水前後黏土層的 u 與 σ' 沿深度（解題圖解）══════
# ── 由 SM-2015-4 §4 步驟二、三解得 ──
GW = 9.81
G_DRY, G_SAT_S, G_SAT_C = 16.0, 18.0, 17.5
DROP = 5.0                      # 上砂水頭抽降
WT_F = WT + DROP                # 8 m
def sv0(d):  # 抽水前總應力
    if d <= WT: return G_DRY * d
    if d <= Z_C: return G_DRY * WT + G_SAT_S * (d - WT)
    return G_DRY * WT + G_SAT_S * (Z_C - WT) + G_SAT_C * (d - Z_C)
def svf(d):  # 抽水後總應力（3–8 m 砂改乾）
    if d <= WT_F: return G_DRY * d
    if d <= Z_C: return G_DRY * WT_F + G_SAT_S * (d - WT_F)
    return G_DRY * WT_F + G_SAT_S * (Z_C - WT_F) + G_SAT_C * (d - Z_C)
u0 = lambda d: GW * max(0.0, d - WT)
U_TOP_F, U_BOT_F = GW * (Z_C - WT_F), GW * (Z_B - WT)     # 9.81、137.34（底部水頭不變）
uf = lambda d: U_TOP_F + (U_BOT_F - U_TOP_F) * (d - Z_C) / (Z_B - Z_C)
I_UP = DROP / (Z_B - Z_C)                                  # 0.625
Z_M = (Z_C + Z_B) / 2

def fig_seepage():
    W, H = 900, 560
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.0), (-1.0, 0), 96, 220, 76, 70))
    SMAX = 180.0
    SX = lambda s: s / SMAX
    SY = lambda d: -(d - Z_C) / (Z_B - Z_C)
    frame(cv, 0, 1.0, -1.0, 0, [], [], "應力（kPa）", "深度（m）", grid=False, ylab_dx=-72)
    for v in (0, 40, 80, 120, 160):
        cv.line((SX(v), -1.0), (SX(v), 0), C["border"], 1.0)
        cv.text_px(cv.X(SX(v)), cv.Y(-1.0) + 17, "%d" % v, 12.5, C["muted"])
    for d in (9, 11, 13, 15, 17):
        cv.line((0, SY(d)), (1.0, SY(d)), C["border"], 1.0)
        cv.text_px(cv.X(0) - 9, cv.Y(SY(d)), "%d" % d, 12.5, C["muted"], anchor="end")
    ds = [Z_C, Z_B]
    cv.poly([(SX(u0(d)), SY(d)) for d in ds], C["deform"], 2.4, dash="7 4")
    cv.poly([(SX(uf(d)), SY(d)) for d in ds], C["deform"], 3.0)
    cv.poly([(SX(sv0(d) - u0(d)), SY(d)) for d in ds], C["bmd"], 2.4, dash="7 4")
    cv.poly([(SX(svf(d) - uf(d)), SY(d)) for d in ds], C["bmd"], 3.2)
    for d, lab in ((Z_C, "頂"), (Z_B, "底")):
        a, b = sv0(d) - u0(d), svf(d) - uf(d)
        tag_px(cv, cv.X(SX(max(a, b))) + 10, cv.Y(SY(d)) + (16 if d == Z_C else -16),
               "%s Δσ' = %+.1f" % (lab, b - a), 12, C["bmd"], anchor="start", weight="400")
    a, b = sv0(Z_M) - u0(Z_M), svf(Z_M) - uf(Z_M)
    cv.dot((SX(b), SY(Z_M)), 5.5, fill=C["accent"])
    tag_px(cv, cv.X(SX(b)) + 10, cv.Y(SY(Z_M)), "中點 %.1f → %.1f" % (a, b), 12.5, C["accent"], anchor="start")
    lx, ly = cv.X(1.0) + 24, cv.Y(-0.12)
    for k, (col, dash, lab) in enumerate([(C["deform"], "7 4", "u 抽水前（靜水壓）"), (C["deform"], None, "u 抽水後（向上穩態滲流）"),
                                          (C["bmd"], "7 4", "σ' 抽水前"), (C["bmd"], None, "σ' 抽水後")]):
        d_ = ' stroke-dasharray="%s"' % dash if dash else ""
        cv.parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3"%s/>'
                        % (lx, ly + k * 24, lx + 28, ly + k * 24, col, d_))
        cv.text_px(lx + 36, ly + k * 24, lab, 12.5, col, anchor="start", weight="700")
    cv.text_px(lx, cv.Y(-0.62), "i = 5/8 = %.3f（向上）" % I_UP, 12.5, C["text"], anchor="start")
    cv.math_px(lx, cv.Y(-0.62) + 26, "q = k i = 6.25×10^{-8} m/s", 13, C["text"], anchor="start")
    return cv

compose([fig_seepage()],
        title="圖 2　抽水後黏土層：上部有效應力大增、底部微減",
        sub="底部水頭不變、頂部降 5 m → 孔隙水壓由靜水壓變為線性的向上滲流分布（黏土層 9–17 m）",
        note="攔錯用：若以為黏土整層 u 都降 5γw，或忘了 3–8 m 砂改用 γdry 使總應力也減少，中點 Δσ' 會算錯。",
        path=os.path.join(OUT, "SM-2015-4-fig-2-seepage.svg"))
