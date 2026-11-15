# -*- coding: utf-8 -*-
"""SM-2009-2 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2009-2-problem.md §4 判讀清單（#2–#5、#8），不含任何解題結果。
用法：python gen_SM-2009-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill, wt_symbol, tag_px
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_CL = 12.0    # #2 黏土層厚（地表→砂土頂）
WT   = 3.0     # #4 地下水位：地表下 3 m
B    = 8.0     # #8 筏基寬 B（L = 12 m 在平面方向，剖面不畫）
DF   = 4.5     # #3 Df 由地表量到開挖底面——Df 為待求量，此處深度僅示意
H_SA = 2.0     # 砂土層：考卷未給厚度，示意
WALL = 2.2     # 開挖兩側壁伸出地表的高度（示意，照考卷附圖）

def fig_problem():
    W, H = 900, 560
    XL, XR = -11.0, 11.0
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL - 2.6, XR + 1.6), (-(H_CL + H_SA + 0.6), WALL + 0.4), 40, 40, 30, 30))
    Y = lambda d: -d
    # 地層
    soil_fill(cv, XL, -B/2, Y(DF), Y(0), "rgba(63,74,90,0.18)")
    soil_fill(cv, B/2, XR, Y(DF), Y(0), "rgba(63,74,90,0.18)")
    soil_fill(cv, XL, XR, Y(H_CL), Y(DF), "rgba(63,74,90,0.18)")
    soil_fill(cv, XL, XR, Y(H_CL + H_SA), Y(H_CL), "rgba(180,83,9,0.22)")
    cv.line((XL, Y(0)), (-B/2, Y(0)), C["member"], 2.6)
    cv.line((B/2, Y(0)), (XR, Y(0)), C["member"], 2.6)
    cv.line((XL, Y(H_CL)), (XR, Y(H_CL)), C["member2"], 1.8)
    # 開挖坑與兩側壁（照考卷附圖：側壁伸出地表）
    cv.poly([(-B/2, Y(-WALL)), (-B/2, Y(DF)), (B/2, Y(DF)), (B/2, Y(-WALL))], C["member"], 2.6)
    cv.polygon([(-B/2, Y(DF)), (B/2, Y(DF)), (B/2, Y(DF - 0.35)), (-B/2, Y(DF - 0.35))],
               "rgba(29,78,216,0.22)", C["deform"], 1.8)
    cv.arrow((0, Y(DF - 2.9)), (0, Y(DF - 0.4)), C["load"], 3.2, 10)
    cv.math_px(cv.X(0.35), cv.Y(Y(DF - 2.6)), "Q = 18 MN", 14, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(0), cv.Y(Y(DF + 0.7)), "筏式基礎 B × L = 8 m × 12 m", 12.5, C["deform"], weight="700")
    # 地下水位（地表下 3 m）
    cv.line((XL, Y(WT)), (-B/2, Y(WT)), C["deform"], 1.8, dash="8 5")
    cv.line((B/2, Y(WT)), (XR, Y(WT)), C["deform"], 1.8, dash="8 5")
    wt_symbol(cv, 8.6, Y(WT), C["deform"], 0.16)
    cv.text_px(cv.X(8.1), cv.Y(Y(WT)) + 16, "地下水位", 12.5, C["deform"], anchor="end", weight="700")
    # 層名與參數
    cv.text_px(cv.X(-10.5), cv.Y(Y(7.0)), "正常壓密黏土", 13, C["text"], anchor="start", weight="700")
    cv.math_px(cv.X(-10.5), cv.Y(Y(8.0)), "γ_{sat} = 17 kN/m^{3}", 13, C["text"], anchor="start")
    cv.math_px(cv.X(-10.5), cv.Y(Y(9.0)), "C_{u} = 35 kN/m^{2}", 13, C["text"], anchor="start")
    cv.text_px(cv.X(0), cv.Y(Y(H_CL + H_SA/2)), "砂土層（性質、厚度考卷未給）", 12.5, C["text"], weight="700")
    cv.text_px(cv.X(6.5), cv.Y(Y(-0.45)), "地表", 12.5, C["muted"])
    # 尺寸線
    xd = XL - 1.9
    cv.dim((xd, Y(H_CL)), (xd, Y(0)), "12 m", 0, C["dim"], 13, label_off=-26)
    cv.dim((XL - 0.35, Y(WT)), (XL - 0.35, Y(0)), "3 m", 0, C["dim"], 12.5, label_off=-22)
    for d in (0, WT, H_CL):
        cv.line((xd - 0.15, Y(d)), (XL, Y(d)), C["dim"], 0.9, dash="2 3")
    cv.dim((XR + 0.6, Y(DF)), (XR + 0.6, Y(0)), "D_{f}", 0, C["dim"], 14, label_off=-18)
    cv.line((B/2, Y(DF)), (XR + 0.75, Y(DF)), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2009-2 題目附圖重繪",
        sub="依題目正本判讀清單；Df 為待求量（深度示意），水位依題文在地表下 3 m",
        note="攔錯用：12 m 是地表到砂土頂的黏土全厚；Df 由地表量到開挖底面；水位深 3 m 以題文為準，考卷圖上的水位符號未按比例。",
        path=os.path.join(OUT, "SM-2009-2-fig-1-problem.svg"))


# ══════ fig-2-heave：解題圖解（2026-11-15 階段 E；數值取自 SM-2009-2.md §4、§5，盲解比對一致）══════
import math
CU, GSAT, GW_ = 35.0, 17.0, 9.81
DF_S  = 6.34                                   # §4（一）Step 3 解得 Df
T_CL  = H_CL - DF_S                            # 5.66 坑底下剩餘黏土
B1    = B / math.sqrt(2)                       # 5.66 Terzaghi 破壞塊寬
FS_HV = 2.58                                   # §4（二）Step 2（Terzaghi 形式）
FS_BE = 2.13                                   # §4（二）Bjerrum–Eide
W_PL  = T_CL * GSAT                            # 96.22 kPa 黏土塞重
U_SA  = (H_CL - WT) * GW_                      # 88.29 kPa 砂層水壓
FS_UP = W_PL / U_SA                            # 1.09

def fig_heave():
    W, H = 980, 600
    XL, XR = -1.5, 16.5
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (XL, XR + 6.5), (-(H_CL + 1.6), 1.2), 30, 30, 70, 30))
    cv.panel(title="開挖隆起與上舉：破壞塊深度剛好到砂層頂",
             sub="Terzaghi 塊寬 B/√2 = %.2f m ＝ 坑底下黏土厚 T = %.2f m" % (B1, T_CL))
    Y = lambda d: -d
    soil_fill(cv, XL, XR, Y(0), Y(H_CL), "rgba(120,94,60,0.14)")
    soil_fill(cv, XL, XR, Y(H_CL), Y(H_CL + 1.4), "rgba(217,180,90,0.30)")
    cv.polygon([(0, Y(0)), (B, Y(0)), (B, Y(DF_S)), (0, Y(DF_S))], "#FFFFFF")
    cv.line((XL, Y(0)), (0, Y(0)), C["muted"], 2); cv.line((B, Y(0)), (XR, Y(0)), C["muted"], 2)
    cv.poly([(0, Y(0)), (0, Y(DF_S)), (B, Y(DF_S)), (B, Y(0))], C["member"], 2.6)
    cv.line((XL, Y(H_CL)), (XR, Y(H_CL)), C["muted"], 1.6)
    cv.text_px(cv.X(XR - 0.2), cv.Y(Y(H_CL + 0.75)), "砂土（受壓水頭）", 12.5, C["text"], anchor="end", weight="700")
    cv.text_px(cv.X(XR - 0.2), cv.Y(Y(H_CL - 0.6)), "NC 黏土 c_u = 35、γ = 17", 12.5, C["text"], anchor="end")
    # 水位
    cv.line((B, Y(WT)), (XR, Y(WT)), C["deform"], 1.6, dash="7 5")
    cv.text_px(cv.X(XR - 0.2), cv.Y(Y(WT)) - 12, "外側水位 −%g m" % WT, 12, C["deform"], anchor="end", weight="700")
    cv.line((0, Y(DF_S)), (B, Y(DF_S)), C["deform"], 1.6, dash="7 5")
    cv.text_px(cv.X(B / 2), cv.Y(Y(DF_S)) - 12, "坑內水位抽至坑底", 12, C["deform"], weight="700")
    # Terzaghi 破壞塊與弧
    cv.polygon([(B, Y(0)), (B + B1, Y(0)), (B + B1, Y(DF_S)), (B, Y(DF_S))], "rgba(194,65,12,0.16)", C["load"], 1.6)
    arc = [(B + B1 * math.cos(math.radians(a)), Y(DF_S) + B1 * math.sin(math.radians(a))) for a in range(0, -181, -5)]
    cv.poly(arc, C["load"], 2.4, dash="8 5")
    cv.arrow((B + B1 / 2, Y(1.2)), (B + B1 / 2, Y(3.6)), C["load"], 3.2, 11)
    cv.text_px(cv.X(B + B1 / 2), cv.Y(Y(4.4)), "γH", 13, C["load"], weight="700")
    cv.dim((B, Y(0)), (B + B1, Y(0)), "B_{1} = 0.707B = %.2f m" % B1, -18, C["dim"], 12.5, label_off=-14)
    cv.dim((B + 0.3, Y(DF_S)), (B + 0.3, Y(H_CL)), "T = %.2f m" % T_CL, 0, C["dim"], 12.5, label_off=-40)
    cv.dim((-0.6, Y(DF_S)), (-0.6, Y(0)), "D_{f} = %.2f m" % DF_S, 0, C["dim"], 12.5, label_off=52)
    cv.dot((B, Y(H_CL)), 6, C["load"])
    cv.text_px(cv.X(B) + 12, cv.Y(Y(H_CL)) + 20, "弧底切齊砂層頂", 12, C["load"], anchor="start", weight="700")
    # 上舉：黏土塞
    cv.arrow((B / 2, Y(H_CL + 1.2)), (B / 2, Y(H_CL + 0.05)), C["deform"], 3.4, 11)
    cv.text_px(cv.X(B / 2) - 12, cv.Y(Y(H_CL + 0.75)), "U = (12 − 3)γ_w = %.2f kPa" % U_SA, 12, C["deform"], anchor="end", weight="700")
    cv.text_px(cv.X(B / 2 + 1.0), cv.Y(Y(DF_S + 0.75)), "黏土塞重 W = T·γ = %.2f kPa" % W_PL, 12, C["text"], weight="700")
    # 結果欄
    x0 = cv.X(XR + 0.6)
    cv.text_px(x0, cv.Y(Y(1.0)), "檢核結果（本解 §4、§5）", 13.5, C["text"], anchor="start", weight="700")
    rows = [("抗隆起 Terzaghi 形式", "FS = %.2f" % FS_HV, C["member"]),
            ("抗隆起 Bjerrum–Eide", "FS = %.2f" % FS_BE, C["member"]),
            ("抗上舉 W / U", "FS = %.2f" % FS_UP, C["load"])]
    for k, (a, b_, col) in enumerate(rows):
        yy = cv.Y(Y(2.4 + 2.0 * k))
        cv.text_px(x0, yy, a, 12.5, C["muted"], anchor="start")
        cv.text_px(x0, yy + 22, b_, 16, col, anchor="start", weight="700")
    cv.text_px(x0, cv.Y(Y(9.0)), "隆起各法 2.1～3.2 皆可；", 12, C["text"], anchor="start")
    cv.text_px(x0, cv.Y(Y(9.0)) + 20, "上舉 FS 低於 1.2 → 砂層需降壓", 12, C["load"], anchor="start", weight="700")
    return cv

compose([fig_heave()],
        title="SM-2009-2 ㈡ 開挖隆起與上舉檢核",
        note="數值取自本題 §4、§5（Df = 6.34 m）。攔錯用：破壞塊深度受砂層限制（T 與 B/√2 比較）；只算剪力隆起而漏掉砂層水壓造成的上舉。",
        path=os.path.join(OUT, "SM-2009-2-fig-2-heave.svg"))
