# -*- coding: utf-8 -*-
"""SM-2024-3 圖解。
fig-1-problem：題目附圖（簡化土層剖面）重繪，幾何只取自題目正本 SM-2024-3-problem.md §4 判讀清單（#3–#5），不含任何解題結果。
用法：python gen_SM-2024-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
Z_B, Z_C, Z_E = 8.0, 20.0, 30.0     # #3 覆土 0–8、砂土 8–20、黏土 20–30 m
Z_D = (Z_C + Z_E) / 2               # #3 D 在黏土層中點
WT0, WT1 = 2.0, 18.0                # #4 初始水位、#5 降水後水位（題文）

def fig_problem():
    W, H = 900, 760
    XL, XR = 0.0, 10.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 3.0, XR + 5.2), (-(Z_E + 2.4), 1.6), 40, 40, 60, 40))
    Y = lambda d: -d
    for d0, d1, col in [(0, Z_B, "rgba(180,83,9,0.12)"), (Z_B, Z_C, "rgba(180,83,9,0.24)"),
                        (Z_C, Z_E, "rgba(63,74,90,0.22)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(Z_B)), (XR, Y(Z_B)), C["member2"], 1.8)
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member2"], 1.8)
    cv.line((XL, Y(Z_E)), (XR, Y(Z_E)), C["member"], 2.6)
    for x in (1.0, 4.4, 7.8):        # 不透水層（題文；考卷圖未畫，示意）
        for k in range(4):
            cv.line((x + k * 0.35, Y(Z_E)), (x + k * 0.35 - 0.3, Y(Z_E + 0.8)), C["member"], 1.4)
    cv.text_px(cv.X(5.0), cv.Y(Y(Z_E + 1.6)), "不透水層（題文）", 12.5, C["text"], weight="700")
    # 地下水位：初始（實線色）、降水後（同色虛線）
    cv.line((XL, Y(WT0)), (XR, Y(WT0)), C["deform"], 1.6, dash="8 5")
    wt_symbol(cv, 8.8, Y(WT0), C["deform"], 0.3)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT0)), "初始水位", 12.5, C["deform"], anchor="start", weight="700")
    cv.line((XL, Y(WT1)), (XR, Y(WT1)), C["deform"], 1.6, dash="3 4")
    wt_symbol(cv, 8.8, Y(WT1), C["deform"], 0.3)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT1)), "降水後水位", 12.5, C["deform"], anchor="start", weight="700")
    # 層名與參數
    cv.text_px(cv.X(5.0), cv.Y(Y(1.0)), "地表面", 12.5, C["muted"])
    cv.text_px(cv.X(1.0), cv.Y(Y(4.2)), "覆土層", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(1.0), cv.Y(Y(5.4)), "γ_{d} = 16.00 kN/m^{3}", 12.5, C["text"], anchor="start")
    cv.math_px(cv.X(1.0), cv.Y(Y(6.6)), "γ_{sat} = 19.68 kN/m^{3},  ω = 23%", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(12.0)), "砂土層", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(1.0), cv.Y(Y(13.6)), "γ_{sat} = 18.29 kN/m^{3},  ω = 18%", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(22.6)), "黏土層", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(1.0), cv.Y(Y(27.6)), "γ_{sat} = 21.78 kN/m^{3},  ω = 21%", 12.5, C["text"], anchor="start")
    # 點位 A–E（左緣）
    for name, d in [("A", 0), ("B", Z_B), ("C", Z_C), ("D", Z_D), ("E", Z_E)]:
        dot(cv, cv.X(XL), cv.Y(Y(d)), 5, C["text"])
        cv.text_px(cv.X(XL) - 12, cv.Y(Y(d)), name, 13, C["text"], anchor="end", weight="700")
    # 尺寸線
    xd = XL - 1.7
    cv.dim((xd, Y(Z_B)), (xd, Y(0)), "8 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((xd, Y(Z_C)), (xd, Y(Z_B)), "12 m", 0, C["dim"], 12.5, label_off=-28)
    cv.dim((xd, Y(Z_E)), (xd, Y(Z_C)), "10 m", 0, C["dim"], 12.5, label_off=-28)
    xr = XR + 4.6
    cv.dim((xr, Y(WT0)), (xr, Y(0)), "2 m", 0, C["dim"], 12, label_off=24)
    cv.dim((xr - 0.0, Y(WT1)), (xr, Y(WT0)), "16 m", 0, C["dim"], 12, label_off=26)
    for d in (0, WT0, WT1):
        cv.line((XR, Y(d)), (xr + 0.25, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2024-3 題目附圖重繪",
        sub="依題目正本判讀清單；水位由地表下 2 m 降到 18 m（仍在砂土層內），D 為黏土層中點",
        note="攔錯用：C 是砂土與黏土交界（地表下 20 m），降水後水位仍在 C 之上 2 m；黏土下方不透水。",
        path=os.path.join(OUT, "SM-2024-3-fig-1-problem.svg"))


# ══════ fig-2：降水前後有效應力沿深度（解題圖解）══════
# ── 由 SM-2024-3 §4（一）（二）（四）解得 ──
GW = 9.81
G_FD, G_FS = 16.00, 19.68           # 覆土 γd、γsat（題給）
G_SS, W_S = 18.29, 0.18             # 砂土 γsat、w
G_SD = G_SS / (1 + W_S)             # 15.50（題目正本 #1 定案：降水後改用乾單位重）
G_CL = 21.78                        # 黏土 γsat
SIG_P = 300.0                       # ㈣ σ'p
def gam(d, wt, dry_above=True):
    """深度 d 處的單位重：水位以上用 γd（dry_above=False 時沿用 γsat，作對照）。"""
    if d < Z_B:
        return G_FD if (d < wt and dry_above) or (d < WT0) else G_FS
    if d < Z_C:
        return G_SD if (d < wt and dry_above) else G_SS
    return G_CL
def sig_eff(d, wt, dry_above=True, n=600):
    s = sum(gam(d * (k + 0.5) / n, wt, dry_above) * d / n for k in range(n))
    return s - GW * max(0.0, d - wt)

def fig_profile():
    W, H = 900, 720
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R, T, B = 90, 250, 40, 660
    SA, SB = 0, 500
    X = lambda s: L + (s - SA) / (SB - SA) * (W - L - R)
    Y = lambda d: T + d / Z_E * (B - T)
    for s in range(0, 501, 100):
        seg(cv, (X(s), T), (X(s), B), C["border"], 1.0)
        cv.text_px(X(s), T - 12, "%d" % s, 12.5, C["muted"])
    for d in (0, 2, 8, 18, 20, 25, 30):
        seg(cv, (L, Y(d)), (W - R, Y(d)), C["border"], 1.0)
        cv.text_px(L - 9, Y(d), "%d" % d, 12.5, C["muted"], anchor="end")
    for d0, d1, col, lab in ((0, Z_B, "rgba(180,83,9,0.07)", "覆土"), (Z_B, Z_C, "rgba(180,83,9,0.14)", "砂土"),
                             (Z_C, Z_E, "rgba(63,74,90,0.12)", "黏土")):
        cv.rect_px(L, Y(d0), W - R - L, Y(d1) - Y(d0), col, 0)
        cv.text_px(W - R - 8, (Y(d0) + Y(d1)) / 2, lab, 13, C["muted"], anchor="end", weight="700")
    seg(cv, (L, T), (W - R, T), C["muted"], 1.9); seg(cv, (L, T), (L, B), C["muted"], 1.9)
    cv.text_px((L + W - R) / 2, B + 30, "有效應力 σ'（kPa）", 13.5, C["text"])
    cv.text_px(L - 40, T - 30, "深度（m）", 12.5, C["text"], anchor="middle")
    ds = [Z_E * j / 300 for j in range(301)]
    curve(cv, [(X(sig_eff(d, WT1, False)), Y(d)) for d in ds], C["load"], 1.8, dash="6 4")
    curve(cv, [(X(sig_eff(d, WT0)), Y(d)) for d in ds], C["member2"], 2.6)
    curve(cv, [(X(sig_eff(d, WT1)), Y(d)) for d in ds], C["deform"], 3.0)
    # σ'p
    seg(cv, (X(SIG_P), Y(Z_C)), (X(SIG_P), Y(Z_E)), C["accent"], 1.4, dash="4 4")
    cv.text_px(X(SIG_P) + 4, Y(Z_E) - 12, "σ'p = 300（㈣）", 11.5, C["accent"], anchor="start", weight="700")
    for d, nm in ((Z_C, "C"), (Z_D, "D")):
        a, b = sig_eff(d, WT0), sig_eff(d, WT1)
        dot(cv, X(a), Y(d), 5.5, C["member2"]); dot(cv, X(b), Y(d), 6, C["deform"])
        cv.arrow((X(a) + 8, cv.h - Y(d)), (X(b) - 8, cv.h - Y(d)), C["deform"], 1.8, 7)
        tag_px(cv, X(a) - 8, Y(d) - 18, "%s %.2f" % (nm, a), 11.5, C["member2"], anchor="end")
        tag_px(cv, X(b) + 8, Y(d) - 18, "%.2f（+%.2f）" % (b, b - a), 11.5, C["deform"], anchor="start")
    c_wrong = sig_eff(Z_C, WT1, False) - sig_eff(Z_C, WT0)
    cv.legend(W - R + 18, 140, [(C["member2"], "降水前（水位 2 m）"), (C["deform"], "降水後（水位 18 m）"),
                                (C["load"], "錯：水位以上仍用 γsat")], size=11.5)
    cv.text_px(W - R + 18, 270, "降水後水位以上用 γd", 11.5, C["deform"], anchor="start", weight="700")
    cv.text_px(W - R + 18, 240, "錯法 C 點增量 +%.2f" % c_wrong, 11.5, C["load"], anchor="start", weight="700")
    cv.text_px(W - R + 18, 300, "黏土內各深度增量相同", 11.5, C["text"], anchor="start", weight="700")
    cv.text_px(W - R + 18, 322, "（只由水位以上改變決定）", 11.5, C["text"], anchor="start")
    return cv

compose([fig_profile()],
        title="圖 2　降水前後有效應力沿深度分布",
        sub="降水後 2–18 m 改用乾單位重（覆土 16.00、砂土 18.29/1.18 = 15.50）；黏土維持飽和",
        note="攔錯用：水位以上仍用 γsat（紅虛線）會使 C 點增量多算約 50 kPa；D 點跨過 σ'p = 300，㈣ 要分兩段算沉陷。",
        path=os.path.join(OUT, "SM-2024-3-fig-2-stress-profile.svg"))
print("C", round(sig_eff(Z_C, WT0), 2), round(sig_eff(Z_C, WT1), 2), "D", round(sig_eff(Z_D, WT0), 2), round(sig_eff(Z_D, WT1), 2),
      "wrong", round(sig_eff(Z_C, WT1, False) - sig_eff(Z_C, WT0), 2))
