# -*- coding: utf-8 -*-
"""SM-2021-2 圖解。
fig-1-problem：題目附圖（土壤剖面）重繪，幾何只取自題目正本 SM-2021-2-problem.md §4 判讀清單（#2–#5），不含任何解題結果。
用法：python gen_SM-2021-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
WT  = 1.0     # #2/#3 乾砂 0–1 m，地下水位地表下 1 m
Z_C = 2.0     # #2 飽和砂 1–2 m，黏土頂
Z_B = 7.0     # #2 黏土 2–7 m，其下飽和砂（#4）
Z_E = 8.4     # 圖面下層砂繪到此（示意，考卷未標厚度）

def fig_problem():
    W, H = 900, 600
    XL, XR = 0.0, 10.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 2.0, XR + 1.9), (-Z_E, 2.2), 40, 40, 60, 40))
    Y = lambda d: -d
    for d0, d1, col in [(0, WT, "rgba(180,83,9,0.10)"), (WT, Z_C, "rgba(180,83,9,0.22)"),
                        (Z_C, Z_B, "rgba(63,74,90,0.22)"), (Z_B, Z_E, "rgba(180,83,9,0.22)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(WT)), (XR, Y(WT)), C["deform"], 1.6, dash="8 5")
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member2"], 1.8)
    cv.line((XL, Y(Z_B)), (XR, Y(Z_B)), C["member2"], 1.8)
    # 均布載重（#5）
    for i in range(15):
        x = 0.35 + i * (XR - 0.7) / 14
        cv.arrow((x, Y(-1.5)), (x, Y(-0.05)), C["load"], 2.0, 7)
    cv.line((0.35, Y(-1.5)), (XR - 0.35, Y(-1.5)), C["load"], 2.0)
    cv.math_px(cv.X(XR + 0.25), cv.Y(Y(-1.5)), "Δσ = 100 kN/m^{2}", 13, C["load"], anchor="start", weight="700")
    wt_symbol(cv, 1.2, Y(WT), C["deform"], 0.12)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT)), "地下水位", 12.5, C["deform"], anchor="start", weight="700")
    # 層名與參數
    cv.text_px(cv.X(3.0), cv.Y(Y(WT / 2)), "乾砂", 13, C["text"], weight="700")
    cv.math_px(cv.X(5.4), cv.Y(Y(WT / 2)), "γ_{d} = 16.5 kN/m^{3}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(3.0), cv.Y(Y((WT + Z_C) / 2)), "飽和砂", 13, C["text"], weight="700")
    cv.math_px(cv.X(5.4), cv.Y(Y((WT + Z_C) / 2)), "γ_{sat} = 18.5 kN/m^{3}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(3.0), cv.Y(Y(Z_C + 1.0)), "飽和黏土（正常壓密）", 13, C["text"], weight="700")
    for k, s in enumerate(["γ_{sat} = 20 kN/m^{3}", "e_{o} = 0.9", "C_{c} = 0.5,  C_{s} = 0.1",
                           "c_{v} = 0.001 cm^{2}/sec"]):
        cv.math_px(cv.X(5.4), cv.Y(Y(Z_C + 2.0 + 0.75 * k)), s, 13, C["text"], anchor="start")
    cv.text_px(cv.X(3.0), cv.Y(Y((Z_B + Z_E) / 2)), "飽和砂", 13, C["text"], weight="700")
    cv.math_px(cv.X(5.4), cv.Y(Y((Z_B + Z_E) / 2)), "γ_{sat} = 18 kN/m^{3}", 13, C["text"], anchor="start")
    # 尺寸線（#2）
    xd = XL - 0.9
    cv.dim((xd, Y(WT)), (xd, Y(0)), "1 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((xd, Y(Z_C)), (xd, Y(WT)), "1 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((xd, Y(Z_B)), (xd, Y(Z_C)), "5 m", 0, C["dim"], 12.5, label_off=-26)
    for d in (0, WT, Z_C, Z_B):
        cv.line((xd - 0.25, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2021-2 題目附圖重繪",
        sub="依題目正本判讀清單；黏土 2–7 m，上下皆為砂（雙向排水）",
        note="攔錯用：水位在地表下 1 m，其上用乾砂 γd；黏土下方是飽和砂而非不透水層，排水路徑取半厚。",
        path=os.path.join(OUT, "SM-2021-2-fig-1-problem.svg"))


# ══════ fig-2：沉陷—時間曲線（解題圖解）══════
# ── 由 SM-2021-2 §4（一）（二）（三）解得 ──
import math
GW, G_D, G_SS, G_SC = 9.81, 16.5, 18.5, 20.0
CC, E0, H_CL = 0.5, 0.9, 5.0
D_SIG = 100.0
SIG0 = G_D * WT + G_SS * (Z_C - WT) + G_SC * (H_CL / 2) - GW * (Z_C - WT + H_CL / 2)   # 50.665 kPa（§4 一）
SC_CM = CC * H_CL * 100 / (1 + E0) * math.log10((SIG0 + D_SIG) / SIG0)               # 62.28 cm
CV = 0.001                         # cm²/s
HDR = H_CL / 2 * 100               # 250 cm（雙向排水）
DAY = 86400.0
def U_ap(Tv):                      # 考卷附註的兩段近似式
    tv60 = math.pi / 4 * 0.36
    return math.sqrt(4 * Tv / math.pi) if Tv <= tv60 else (100 - 10 ** ((1.781 - Tv) / 0.933)) / 100
S_t = lambda d, hdr=HDR: SC_CM * U_ap(CV * d * DAY / hdr ** 2)
MONTHS = [30, 60, 90]
S_TARGET = 50.0
U_T = round(S_TARGET / round(SC_CM, 2), 4)   # §4 Step 4 取 80.28%
TV_T = 1.781 - 0.933 * math.log10(100 - 100 * U_T)
T_TARGET = TV_T * HDR ** 2 / CV / DAY        # 414.4 天

def fig_settle():
    W, H = 920, 540
    cv = Canvas(W, H, bg="#FFFFFF")
    L, R, T, B = 100, 220, 30, 450
    TA, TB, SA, SB = 0, 600, 0, 70
    X = lambda t: L + (t - TA) / (TB - TA) * (W - L - R)
    Y = lambda s: B - (s - SA) / (SB - SA) * (B - T)
    for t in range(0, 601, 100):
        seg(cv, (X(t), T), (X(t), B), C["border"], 1.0)
        cv.text_px(X(t), B + 18, "%d" % t, 12.5, C["muted"])
    for s in range(0, 71, 10):
        seg(cv, (X(TA), Y(s)), (X(TB), Y(s)), C["border"], 1.0)
        cv.text_px(X(TA) - 9, Y(s), "%d" % s, 12.5, C["muted"], anchor="end")
    seg(cv, (X(TA), B), (X(TB), B), C["muted"], 1.9)
    seg(cv, (X(TA), B), (X(TA), T), C["muted"], 1.9)
    cv.text_px((X(TA) + X(TB)) / 2, B + 44, "時間 t（天）", 13.5, C["text"])
    cv.text_px(X(TA) - 40, T - 14, "沉陷 S（cm）", 13, C["text"])
    seg(cv, (X(TA), Y(SC_CM)), (X(TB), Y(SC_CM)), C["muted"], 1.5, dash="8 5")
    cv.text_px(X(TB) + 8, Y(SC_CM), "Sc = %.2f cm" % SC_CM, 12.5, C["muted"], anchor="start", weight="700")
    ts = [TB * j / 400 for j in range(401)]
    curve(cv, [(X(t), Y(S_t(t, 2 * HDR))) for t in ts], C["load"], 2.0, dash="7 5")
    curve(cv, [(X(t), Y(S_t(t))) for t in ts], C["deform"], 3.0)
    for d in MONTHS:
        s = S_t(d)
        dot(cv, X(d), Y(s), 6, C["deform"])
        tag_px(cv, X(d) + 10, Y(s) + 20 + (d - 60) / 6, "%d 天 %.2f" % (d, s), 12, C["deform"], anchor="start")
    seg(cv, (X(TA), Y(S_TARGET)), (X(T_TARGET), Y(S_TARGET)), C["accent"], 1.3, dash="4 4")
    seg(cv, (X(T_TARGET), Y(S_TARGET)), (X(T_TARGET), B), C["accent"], 1.3, dash="4 4")
    dot(cv, X(T_TARGET), Y(S_TARGET), 6.5, C["accent"])
    tag_px(cv, X(T_TARGET) + 10, Y(S_TARGET) + 24, "50 cm：t = %.1f 天（U = %.2f%%）" % (T_TARGET, U_T * 100), 12.5, C["accent"], anchor="start")
    cv.legend(W - R + 18, 300, [(C["deform"], "雙向排水 Hdr = 2.5 m"), (C["load"], "錯：Hdr = 5 m")], size=12)
    return cv

compose([fig_settle()],
        title="圖 2　黏土層沉陷—時間曲線",
        sub="Sc 以黏土中點 σ'0 = %.2f kPa 計；Tv = cv t / Hdr²，U ≤ 60%% 與 U > 60%% 用考卷附註兩式" % SIG0,
        note="攔錯用：黏土上下皆為砂，Hdr = 2.5 m；誤用 5 m 時同一沉陷要 4 倍時間（紅虛線），50 cm 會落到 600 天外。",
        path=os.path.join(OUT, "SM-2021-2-fig-2-settlement-time.svg"))
print("SIG0 %.3f SC %.2f" % (SIG0, SC_CM), ["%.2f" % S_t(d) for d in MONTHS], "T50 %.1f" % T_TARGET)
