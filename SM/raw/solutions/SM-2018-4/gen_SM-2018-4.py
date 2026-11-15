# -*- coding: utf-8 -*-
"""SM-2018-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2018-4-problem.md §4 判讀清單，不含任何解題結果。
fig-2-fbd：Rankine 虛擬背自由體圖（虛擬背高 H'、Pa 平行地表、分塊重量、底面抗滑力），數值取自解析 §4。
用法：python gen_SM-2018-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_STEM = 7.5    # #2 牆身高：牆身頂 → 底版頂面（不含底版）
T_TOP  = 0.4    # #3 牆身頂寬
T_BOT  = 0.6    # #3 牆身底寬（牆背鉛直、牆面傾斜）
T_BASE = 0.96   # #4 底版厚
L_TOE  = 1.5    # #4 趾長
L_HEEL = 3.5    # #4 踵長
D_F    = 1.75   # #1 牆前地面 → 底版底
ALPHA  = 12.0   # #5 背填土面傾角（自牆身頂背側起）

def ground_hatch(cv, x, y, n=4, s=0.16):
    for k in range(n):
        cv.line((x + k * s, y), (x + k * s - s * 0.9, y - s * 1.1), C["member"], 1.3)

def fig_problem():
    W, Hp = 900, 720
    XL, XR = -2.6, 9.4
    cv = Canvas(W, Hp, bg="#FFFFFF", **fit(W, Hp, (XL, XR), (-1.9, T_BASE + H_STEM + 1.6), 40, 40, 40, 40))
    xf0 = L_TOE                       # 牆面底
    xb  = L_TOE + T_BOT               # 牆背（鉛直）
    xf1 = xb - T_TOP                  # 牆面頂
    xh  = xb + L_HEEL                 # 踵端
    ytop = T_BASE + H_STEM
    XE = XR - 0.4
    ye = ytop + (XE - xb) * math.tan(math.radians(ALPHA))
    cv.polygon([(xb, T_BASE), (XE, T_BASE), (XE, ye), (xb, ytop)], "rgba(180,83,9,0.13)")   # 背填土
    cv.polygon([(xh, 0), (XE, 0), (XE, T_BASE), (xh, T_BASE)], "rgba(180,83,9,0.13)")
    xg = xf0 + (xf1 - xf0) * (D_F - T_BASE) / H_STEM                                        # 牆面在地面高程的 x
    cv.polygon([(XL + 0.2, 0), (0, 0), (0, T_BASE), (xf0, T_BASE), (xg, D_F), (XL + 0.2, D_F)],
               "rgba(120,113,108,0.16)")                                                    # 牆前（趾上）覆土
    soil_fill(cv, XL + 0.2, XE, -1.1, 0, "rgba(63,74,90,0.14)")                             # 基礎土壤
    cv.line((XL + 0.2, D_F), (xg, D_F), C["member"], 2.0)                                   # 牆前地面（#1）
    cv.line((xh, 0), (XE, 0), C["member"], 1.6)
    cv.line((XL + 0.2, 0), (0, 0), C["member"], 1.6)
    ground_hatch(cv, -1.5, D_F)
    ground_hatch(cv, 7.6, 0)
    cv.line((xb, ytop), (XE, ye), C["member"], 2.2)                                          # α = 12°（#5）
    cv.line((xb, ytop), (xb + 2.2, ytop), C["dim"], 1.0, dash="4 3")
    r = 1.9
    pts = [(xb + r * math.cos(math.radians(a)), ytop + r * math.sin(math.radians(a))) for a in [i * ALPHA / 12 for i in range(13)]]
    cv.poly(pts, C["accent"], 1.6)
    cv.text_px(cv.X(xb + r + 0.55), cv.Y(ytop + 0.2), "α = 12°", 13, C["accent"], weight="700")
    # 牆身＋底版
    cv.polygon([(0, 0), (xh, 0), (xh, T_BASE), (xb, T_BASE), (xb, ytop), (xf1, ytop), (xf0, T_BASE), (0, T_BASE)],
               "rgba(29,78,216,0.16)", C["deform"], 2.4)
    cv.text_px(cv.X(5.3), cv.Y(6.3), "背填土  γ1 = 17.8 kN/m³", 12.5, C["text"])
    cv.text_px(cv.X(5.3), cv.Y(5.75), "φ1 = 32°，c1 = 0", 12.5, C["text"])
    cv.text_px(cv.X(-0.4), cv.Y(4.2), "懸臂式擋土牆", 12.5, C["deform"], weight="700")
    cv.text_px(cv.X(-0.4), cv.Y(3.7), "γc = 23.55 kN/m³", 12, C["deform"])
    cv.text_px(cv.X(-0.6), cv.Y(1.35), "趾上覆土（土性未標）", 11.5, C["muted"])
    cv.text_px(cv.X(4.0), cv.Y(-0.6), "基礎土壤  γ2 = 16.6 kN/m³，φ2 = 28°，c2 = 30 kN/m²", 12.5, C["text"])
    # 尺寸線
    cv.dim((xf1, ytop + 0.5), (xb, ytop + 0.5), "0.4 m", 0, C["dim"], 12, label_off=-14)
    for x in (xf1, xb):
        cv.line((x, ytop + 0.05), (x, ytop + 0.65), C["dim"], 0.9, dash="2 3")
    xH = xb + 0.75
    cv.line((xb + 0.05, ytop), (xH + 0.15, ytop), C["dim"], 0.9, dash="2 3")
    cv.dim((xH, T_BASE), (xH, ytop), "H = 7.5 m", 0, C["load"], 13, label_off=40)
    xr = xh + 0.45
    cv.dim((xr, 0), (xr, T_BASE), "0.96 m", 0, C["dim"], 12, label_off=30)
    xl = -2.1
    cv.dim((xl, 0), (xl, D_F), "1.75 m", 0, C["dim"], 12, label_off=-30)
    yb = -1.55
    cv.dim((0, yb), (xf0, yb), "1.5 m", 0, C["dim"], 12, label_off=14)
    cv.dim((xf0, yb), (xb, yb), "0.6", 0, C["dim"], 11, label_off=14)
    cv.dim((xb, yb), (xh, yb), "3.5 m", 0, C["dim"], 12, label_off=14)
    for x in (0, xf0, xb, xh):
        cv.line((x, -1.12), (x, yb - 0.1), C["dim"], 0.8, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2018-4 題目附圖重繪",
        sub="依題目正本判讀清單；H = 7.5 m 為牆身高（底版頂 → 牆身頂），底版另厚 0.96 m",
        note="攔錯用：H 不含底版（牆全高 8.46 m）；背填土面自牆身頂背側上傾 12°；牆前地面在底版底上方 1.75 m。",
        path=os.path.join(OUT, "SM-2018-4-fig-1-problem.svg"))


# ── 解析 §4 數值（由題給量重算）────────────────────────────
G1, PHI1, G_C = 17.8, 32.0, 23.55
PHI2, C2, K1, K2 = 28.0, 30.0, 2 / 3, 2 / 3
B   = L_TOE + T_BOT + L_HEEL                                   # 5.6
XB  = L_TOE + T_BOT                                            # 2.1 牆背
DH  = round(L_HEEL * math.tan(math.radians(ALPHA)), 3)         # 0.744（§4 三位數續算）
HV  = T_BASE + H_STEM + DH                                     # 9.204 虛擬背高
_ca, _cp = math.cos(math.radians(ALPHA)), math.cos(math.radians(PHI1))
KA  = round(_ca * (_ca - math.sqrt(_ca**2 - _cp**2)) / (_ca + math.sqrt(_ca**2 - _cp**2)), 4)   # 0.3275（§4 四位數續算）
PA  = 0.5 * G1 * HV**2 * KA                                    # 246.92
PAH, PAV = PA * round(_ca, 4), PA * round(math.sin(math.radians(ALPHA)), 4)   # 241.51 / 51.33（§4 cos/sin 四位數）
BLK = [  # (名稱, W, x)  §4 Step 3
    ("W1 牆身矩形", T_TOP * H_STEM * G_C, XB - T_TOP / 2),
    ("W2 牆身三角", 0.5 * (T_BOT - T_TOP) * H_STEM * G_C, L_TOE + 2 / 3 * (T_BOT - T_TOP)),
    ("W3 底版", B * T_BASE * G_C, B / 2),
    ("W4 踵上土", L_HEEL * H_STEM * G1, XB + L_HEEL / 2),
    ("W5 踵上土三角", 0.5 * L_HEEL * DH * G1, XB + 2 / 3 * L_HEEL),
    ("W6 趾上覆土", L_TOE * (D_F - T_BASE) * G1, L_TOE / 2),
]
SV  = sum(w for _, w, _ in BLK) + PAV                          # 777.76
MR  = sum(w * x for _, w, x in BLK) + PAV * B                  # 2722.5
MO  = PAH * round(HV / 3, 3)                                   # 740.95（§4 y_a = 3.068）
DEL = K1 * PHI2                                                # 18.67°
CA  = K2 * C2                                                  # 20
FR  = CA * B + SV * round(math.tan(math.radians(DEL)), 4)      # 374.73（§4 tanδ = 0.3378）

def fig_fbd():
    W, Hp = 1300, 780
    XL, XR = -2.2, 11.6
    cv = Canvas(W, Hp, bg="#FFFFFF", **fit(W, Hp, (XL, XR), (-2.4, HV + 1.2), 40, 40, 40, 40))
    top = T_BASE + H_STEM
    # 土塊（踵上，虛擬背內）
    cv.polygon([(XB, T_BASE), (B, T_BASE), (B, HV), (XB, top)], "rgba(180,83,9,0.13)", C["muted"], 1.0)
    cv.line((XB, top), (B, top), C["muted"], 0.9, dash="3 3")
    cv.polygon([(0, T_BASE), (L_TOE, T_BASE), (L_TOE, D_F), (0, D_F)], "rgba(180,83,9,0.10)", C["muted"], 1.0)
    # 混凝土
    cv.polygon([(0, 0), (B, 0), (B, T_BASE), (XB, T_BASE), (XB, top), (XB - T_TOP, top), (L_TOE, T_BASE), (0, T_BASE)],
               "rgba(29,78,216,0.14)", C["deform"], 2.4)
    # 地表
    cv.line((XB, top), (B + 2.0, HV + 2.0 * math.tan(math.radians(ALPHA))), C["member"], 1.8)
    cv.line((-1.2, D_F), (L_TOE - 0.02, D_F), C["member"], 1.8)
    # 虛擬背
    cv.line((B, 0), (B, HV), C["accent"], 2.2, dash="8 5")
    cv.text_px(cv.X(B) + 6, cv.Y(HV) - 16, "虛擬背（過踵端鉛直面）", 12, C["accent"], anchor="start", weight="700")
    cv.dim((B + 2.4, 0), (B + 2.4, HV), "H' = %.3f m" % HV, 0, C["accent"], 12.5, label_off=46)
    cv.text_px(cv.X(B + 2.9), cv.Y(HV * 0.62), "H' = 0.96 + 7.5 + 3.5·tan12°", 12, C["accent"], anchor="start")
    # 土壓分布：沿虛擬背三角形、平行地表
    s = 0.034
    ux, uy = _ca, math.sin(math.radians(ALPHA))
    pb = KA * G1 * HV
    xo = B
    cv.polygon([(xo, HV), (xo, 0), (xo + s * pb * ux, s * pb * uy)], "rgba(180,83,9,0.16)", C["load"], 1.4)
    for k in range(1, 7):
        y = HV * (1 - k / 7)
        pp = KA * G1 * (HV - y)
        cv.arrow((xo + s * pp * ux, y + s * pp * uy), (xo + 0.05 * ux, y + 0.05 * uy), C["load"], 1.1, 6)
    cv.text_px(cv.X(xo + s * pb * ux) + 6, cv.Y(s * pb * uy) + 2, "Ka·γ1·H' = %.1f kPa" % pb, 11.5, C["load"], anchor="start")
    L = 2.9
    cv.arrow((B + L * ux, HV / 3 + L * uy), (B + 0.04, HV / 3), C["load"], 3.6, 13)
    tag_px(cv, cv.X(B + 2.9), cv.Y(HV / 3 + 0.9), "Pa = %.2f kN/m（平行地表 12°，@ H'/3 = %.3f m）" % (PA, HV / 3), 12, C["load"], anchor="start")
    tag_px(cv, cv.X(B + 2.9), cv.Y(HV / 3 + 0.3), "Pah = %.2f → MO = %.1f；Pav = %.2f @ x = 5.6" % (PAH, MO, PAV), 12, C["text"], anchor="start")
    # 分塊重量箭頭
    ys = {"W1": top - 2.2, "W2": top - 4.2, "W3": T_BASE * 0.5 + 0.8, "W4": T_BASE + H_STEM * 0.55, "W5": top + DH * 0.33 + 0.9, "W6": D_F + 0.75}
    for name, w, x in BLK:
        k = name[:2]
        y0 = ys[k]
        cv.arrow((x, y0), (x, y0 - 0.75), C["member"], 2.6, 9)
    tag_px(cv, cv.X(XB + L_HEEL / 2), cv.Y(T_BASE + H_STEM * 0.55 + 0.45), "W4 = %.2f" % BLK[3][1], 11.5, C["member"])
    tag_px(cv, cv.X(XB + 2 / 3 * L_HEEL), cv.Y(top + DH * 0.33 + 1.25), "W5 = %.2f" % BLK[4][1], 11.5, C["member"])
    tag_px(cv, cv.X(XB - T_TOP / 2) - 12, cv.Y(top - 2.0), "W1 = %.2f" % BLK[0][1], 11.5, C["member"], anchor="end")
    tag_px(cv, cv.X(BLK[1][2]) - 12, cv.Y(top - 4.0), "W2 = %.2f" % BLK[1][1], 11.5, C["member"], anchor="end")
    tag_px(cv, cv.X(B / 2) + 12, cv.Y(T_BASE * 0.5 + 0.55), "W3 = %.2f" % BLK[2][1], 11.5, C["member"], anchor="start")
    tag_px(cv, cv.X(L_TOE / 2), cv.Y(D_F + 1.15), "W6 = %.2f（覆土 0.79 m）" % BLK[5][1], 11.5, C["member"])
    # 底面抗滑
    for k in range(7):
        x = 0.3 + (B - 0.6) * k / 6
        cv.arrow((x - 0.32, -0.18), (x + 0.32, -0.18), C["bmd"], 1.6, 7)
    tag_px(cv, cv.X(B / 2), cv.Y(-0.75), "FR = ca·B + ΣV·tanδ = 20 × 5.6 + %.1f × tan%.2f° = %.1f kN/m" % (SV, DEL, FR), 12, C["bmd"])
    tag_px(cv, cv.X(B / 2), cv.Y(-1.4), "δ = k1·φ2 = %.2f°，ca = k2·c2 = %.0f kPa（Pp = 0）" % (DEL, CA), 11.5, C["muted"])
    cv.dim((0, -2.0), (B, -2.0), "B = 1.5 + 0.6 + 3.5 = 5.6 m", 0, C["dim"], 12, label_off=14)
    cv.dot((0, 0), 4.5, fill=C["member"])
    cv.text_px(cv.X(-0.15), cv.Y(0.25), "趾", 12, C["member"], anchor="end")
    tag_px(cv, cv.X(-0.3), cv.Y(6.4), "ΣV = %.1f kN/m" % SV, 12, C["text"], anchor="end")
    tag_px(cv, cv.X(-0.3), cv.Y(5.8), "ΣMR = %.1f kN·m/m" % MR, 12, C["text"], anchor="end")
    return cv

compose([fig_fbd()],
        title="SM-2018-4 懸臂式擋土牆：Rankine 虛擬背自由體圖",
        sub="Ka = %.4f；FS傾覆 = ΣMR / MO = %.2f；FS滑移 = FR / Pah = %.2f" % (KA, MR / MO, FR / PAH),
        note="攔錯用：H' 量到踵端上方的傾斜地表（含底版 0.96 m 與 3.5·tan12°）；踵上土是牆體的一部分、Pav 作用在虛擬背（力臂 5.6 m）；Pa 平行地表。",
        path=os.path.join(OUT, "SM-2018-4-fig-2-fbd.svg"))
