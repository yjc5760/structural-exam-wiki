# -*- coding: utf-8 -*-
"""SM-2011-3 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2011-3-problem.md §4 判讀清單（#1–#6），不含任何解題結果。
用法：python gen_SM-2011-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol, tag_px
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
DF   = 1.5     # #1 基礎埋深（地表→基底）
WT   = 1.5     # #2 地下水位在基底高程
H_S2 = 1.2     # #3 基底下砂土厚
H_C  = 3.0     # #4 黏土層厚，下為岩盤（#5）
B    = 1.8     # #6 基礎 1.8 m × 1.8 m
Z_C  = DF + H_S2           # 黏土頂深度
Z_R  = Z_C + H_C           # 岩盤頂深度
T_F  = 0.45                # 基礎版厚（考卷未標，示意）
COL  = 0.45                # 柱寬（示意）

def fig_problem():
    W, H = 900, 560
    XL, XR = -3.4, 4.2
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 1.3, XR), (-(Z_R + 0.7), 1.6), 40, 40, 64, 60))
    Y = lambda d: -d
    for d0, d1, col in [(0, WT, "rgba(180,83,9,0.12)"), (WT, Z_C, "rgba(180,83,9,0.24)"),
                        (Z_C, Z_R, "rgba(63,74,90,0.22)")]:
        soil_fill(cv, XL, XR, Y(d1), Y(d0), col)
    cv.line((XL, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(Z_C)), (XR, Y(Z_C)), C["member2"], 1.8)
    cv.line((XL, Y(Z_R)), (XR, Y(Z_R)), C["member"], 2.6)
    for x in (-2.6, 0.9, 2.9):        # 岩盤剖線
        for k in range(4):
            cv.line((x + k * 0.18, Y(Z_R)), (x + k * 0.18 - 0.16, Y(Z_R + 0.25)), C["member"], 1.4)
    # 基礎（倒 T）
    cv.polygon([(-B/2, Y(DF)), (B/2, Y(DF)), (B/2, Y(DF - T_F)), (COL/2, Y(DF - T_F)),
                (COL/2, Y(-0.6)), (-COL/2, Y(-0.6)), (-COL/2, Y(DF - T_F)), (-B/2, Y(DF - T_F))],
               "rgba(29,78,216,0.22)", C["deform"], 2.2)
    cv.arrow((0, Y(-1.45)), (0, Y(-0.65)), C["load"], 3.2, 10)
    cv.math_px(cv.X(0.2), cv.Y(Y(-1.3)), "Q = 1 MN", 14, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(0), cv.Y(Y(DF - T_F/2)), "1.8 m × 1.8 m", 11, C["deform"], weight="700")
    # 地下水位（基底高程，虛線）
    cv.line((B/2 + 0.15, Y(WT)), (XR, Y(WT)), C["deform"], 1.8, dash="8 5")
    wt_symbol(cv, 3.55, Y(WT), C["deform"], 0.075)
    cv.text_px(cv.X(XR) + 8, cv.Y(Y(WT)), "地下水位", 12.5, C["deform"], anchor="start", weight="700")
    # 層名與參數
    cv.text_px(cv.X(1.2), cv.Y(Y(0.3)), "砂土  e = 0.65，Gs = 2.65", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.2), cv.Y(Y(0.72)), "水位以上 S = 50%", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(1.0), cv.Y(Y(2.15)), "砂土  c' = 0，φ' = 30°", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(-3.2), cv.Y(Y(3.25)), "黏土  Gs = 2.70，c = 40 kPa，φ = 0", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(-3.2), cv.Y(Y(3.85)), "eo = 0.68，Cc = 0.25，Cs = 0.06", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(-3.2), cv.Y(Y(4.45)), "前期最大壓密應力 = 100 kPa", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(0.6), cv.Y(Y(Z_R + 0.5)), "岩盤", 13, C["text"], weight="700")
    cv.text_px(cv.X(2.6), cv.Y(Y(-0.25)), "地表面", 12.5, C["muted"])
    # 尺寸線（左側，端點對齊判讀清單 #1、#3、#4）
    xd = XL - 0.45
    cv.dim((xd, Y(DF)), (xd, Y(0)), "1.5 m", 0, C["dim"], 12.5, label_off=-30)
    cv.dim((xd, Y(Z_C)), (xd, Y(DF)), "1.2 m", 0, C["dim"], 12.5, label_off=-30)
    cv.dim((xd, Y(Z_R)), (xd, Y(Z_C)), "3 m", 0, C["dim"], 12.5, label_off=-30)
    for d in (0, DF, Z_C, Z_R):
        cv.line((xd - 0.12, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    # 基礎寬度
    cv.dim((-B/2, Y(DF + 0.35)), (B/2, Y(DF + 0.35)), "1.8 m", 0, C["dim"], 12.5, label_off=14)
    cv.dim((-B/2, Y(DF + 0.75)), (0, Y(DF + 0.75)), "0.9 m", 0, C["dim"], 12, label_off=14)
    return cv

compose([fig_problem()],
        title="SM-2011-3 題目附圖重繪",
        sub="依題目正本判讀清單；地下水位在基底高程，黏土下為岩盤",
        note="攔錯用：1.5 m 量到基底（不是基礎頂），1.2 m 是基底到黏土頂；水位與基底同高，基底以上的砂用 S = 50% 的濕單位重。",
        path=os.path.join(OUT, "SM-2011-3-fig-1-problem.svg"))


# ══════ fig-2：2:1 應力增量沿深度＋平均值與中點值的差（解題圖解）══════
# ── 由 SM-2011-3 §4 Step 3–4 解得（2026-11-15 勘誤後）──
import math
Q, BF = 1000.0, B
Z_T, Z_B = H_S2, H_S2 + H_C                     # 基底下黏土頂、底（m）
DS = lambda z: Q / (BF + z) ** 2                # 2:1 法
DS_AVG = round(Q / H_C * (1 / (BF + Z_T) - 1 / (BF + Z_B)), 2)   # 55.56 積分平均（取至 0.01，與 §4 一致）
DS_MID = DS((Z_T + Z_B) / 2)                              # 49.38 中點值
P0, PC, E0, CC, CS = 53.20, 100.0, 0.68, 0.25, 0.06
S1 = CS * H_C * 1000 / (1 + E0) * math.log10(PC / P0)     # 29.37 回脹段（兩法相同）
S2_AVG = CC * H_C * 1000 / (1 + E0) * math.log10((P0 + DS_AVG) / PC)   # 16.28
S2_MID = CC * H_C * 1000 / (1 + E0) * math.log10((P0 + DS_MID) / PC)   # 4.94

def panel_ds():
    W, H = 520, 520
    cv = Canvas(W, H, **fit(W, H, (0, 1.0), (-1.0, 0), 92, 40, 70, 70))
    cv.panel("2:1 法應力增量沿深度", "z 由基底起算；陰影為黏土層")
    SX = lambda s: s / 320.0
    SY = lambda z: -z / 4.6
    soil_fill(cv, 0, SX(320), SY(Z_B), SY(Z_T), "rgba(63,74,90,0.16)")
    frame(cv, 0, SX(320), SY(4.6), SY(0), [], [], "Δσ（kPa）", "z（m）", grid=False)
    for v in (0, 100, 200, 300):
        cv.line((SX(v), SY(4.6)), (SX(v), SY(0)), C["border"], 1.0)
        cv.text_px(cv.X(SX(v)), cv.Y(SY(4.6)) + 17, "%d" % v, 12.5, C["muted"])
    for v in (0, 1, 2, 3, 4):
        cv.line((0, SY(v)), (SX(320), SY(v)), C["border"], 1.0)
        cv.text_px(cv.X(0) - 9, cv.Y(SY(v)), "%d" % v, 12.5, C["muted"], anchor="end")
    pts = [(SX(DS(z)), SY(z)) for z in [i * 4.6 / 120 for i in range(121)]]
    cv.poly(pts, C["member"], 2.8)
    cv.line((SX(DS_AVG), SY(Z_T)), (SX(DS_AVG), SY(Z_B)), C["bmd"], 2.6, dash="7 4")
    cv.dot((SX(DS_MID), SY((Z_T + Z_B) / 2)), 6, fill=C["accent"])
    for z, v in ((Z_T, DS(Z_T)), (Z_B, DS(Z_B))):
        cv.dot((SX(v), SY(z)), 4.5, fill=C["member"])
        tag_px(cv, cv.X(SX(v)) + 10, cv.Y(SY(z)), "%.2f" % v, 12, C["member"], anchor="start", weight="400")
    tag_px(cv, cv.X(SX(DS_AVG)) + 10, cv.Y(SY(3.75)), "平均 %.2f" % DS_AVG, 12.5, C["bmd"], anchor="start")
    tag_px(cv, cv.X(SX(DS_MID)) - 12, cv.Y(SY(2.7)) - 26, "中點 %.2f" % DS_MID, 12.5, C["accent"], anchor="end")
    return cv

def panel_sc():
    W, H = 460, 520
    cv = Canvas(W, H, **fit(W, H, (0, 1.0), (0, 1.0), 70, 30, 70, 70))
    cv.panel("沉陷分成兩段", "回脹段相同，差在越過 σ'c 的 Cc 段")
    SY = lambda s: s / 52.0
    frame(cv, 0, 1.0, 0, SY(50), [], [], "", "S（mm）", grid=False)
    for v in (0, 10, 20, 30, 40, 50):
        cv.line((0, SY(v)), (1.0, SY(v)), C["border"], 1.0)
        cv.text_px(cv.X(0) - 9, cv.Y(SY(v)), "%d" % v, 12.5, C["muted"], anchor="end")
    for i, (x, s2, lab, col) in enumerate(((0.28, S2_MID, "中點值", C["accent"]), (0.70, S2_AVG, "平均值（本解）", C["bmd"]))):
        w = 0.22
        cv.polygon([(x - w/2, 0), (x + w/2, 0), (x + w/2, SY(S1)), (x - w/2, SY(S1))], "rgba(29,78,216,0.30)", C["deform"], 1.5)
        cv.polygon([(x - w/2, SY(S1)), (x + w/2, SY(S1)), (x + w/2, SY(S1 + s2)), (x - w/2, SY(S1 + s2))], col, col, 1.5, op=0.55)
        cv.text_px(cv.X(x), cv.Y(SY(S1 / 2)), "Cs 段 %.2f" % S1, 12, C["text"])
        cv.text_px(cv.X(x), cv.Y(SY(S1 + s2)) - 14, "合計 %.1f" % (S1 + s2), 13, col, weight="700")
        cv.text_px(cv.X(x), cv.Y(0) + 20, lab, 12.5, C["text"])
        tag_px(cv, cv.X(x + w/2) + 6, cv.Y(SY(S1 + s2 / 2)), "Cc 段 %.2f" % s2, 11.5, col, anchor="start", weight="400")
    return cv

compose([panel_ds(), panel_sc()],
        title="圖 2　「平均」新增應力：沿層厚平均，不是中點一點",
        sub="2:1 分布沿深度上凹，中點值必低於平均；終應力在 σ'c 附近時差距被放大",
        note="攔錯用：把中點 49.38 kPa 當平均，p'_f 只越過 σ'_c 2.6 kPa，Cc 段少算 11 mm、總沉陷少 25%。",
        path=os.path.join(OUT, "SM-2011-3-fig-2-avg-stress.svg"))
