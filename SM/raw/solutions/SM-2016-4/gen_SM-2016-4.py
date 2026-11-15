# -*- coding: utf-8 -*-
"""SM-2016-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2016-4-problem.md §4 判讀清單，不含任何解題結果。
fig-2-fbd：㈠㈡ 靜態自由體圖（Coulomb Pa 方向、分塊牆重、偏心底壓）與 ㈢ M–O 合力作用點分解，數值取自解析 §4。
用法：python gen_SM-2016-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H     = 8.0    # #3 牆高
B_TOP = 3.0    # #4 牆頂寬
B_BOT = 5.0    # #4 牆底寬（牆面鉛直，#2）
BETA  = math.degrees(math.atan2(H, B_BOT - B_TOP))   # #1 β 由幾何定出（考卷未印數值）

def ground_hatch(cv, x, y, n=4, s=0.18):
    for k in range(n):
        cv.line((x + k * s, y), (x + k * s - s * 0.9, y - s * 1.1), C["member"], 1.3)

def fig_problem():
    W, Hp = 900, 640
    XL, XR = -3.6, 11.0
    cv = Canvas(W, Hp, bg="#FFFFFF", **fit(W, Hp, (XL, XR), (-2.9, H + 1.4), 40, 40, 40, 40))
    XE = XR - 0.4
    cv.polygon([(B_TOP, H), (XE, H), (XE, 0), (B_BOT, 0)], "rgba(180,83,9,0.13)")   # 背填土
    soil_fill(cv, XL + 0.2, XE, -1.4, 0, "rgba(63,74,90,0.14)")
    cv.line((XL + 0.2, 0), (XE, 0), C["member"], 2.4)                                 # 地面線＝牆底（#6）
    cv.line((B_TOP, H), (XE, H), C["member"], 2.0)                                    # α = 0（#5）
    for x in (-2.9,):
        ground_hatch(cv, x, 0)
    ground_hatch(cv, 9.2, H)
    cv.polygon([(0, 0), (B_BOT, 0), (B_TOP, H), (0, H)], "rgba(29,78,216,0.16)", C["deform"], 2.4)
    s = 0.32                                                                          # 牆面直角符號（#2）
    cv.poly([(-s, 0), (-s, s), (0, s)], C["member"], 1.3)
    # β：牆踵內側，牆背與牆底夾角（#1）
    r = 1.15
    pts = [(B_BOT + r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
           for a in [180 - BETA + i * BETA / 30 for i in range(31)]]
    cv.poly(pts, C["accent"], 1.8)
    am = math.radians(180 - BETA / 2)
    cv.text_px(cv.X(B_BOT + 1.65 * math.cos(am)), cv.Y(1.65 * math.sin(am)), "β", 15, C["accent"], weight="700")
    cv.text_px(cv.X(1.5), cv.Y(4.6), "混凝土擋土牆", 13, C["deform"], weight="700")
    cv.text_px(cv.X(1.5), cv.Y(4.0), "γc = 23.5 kN/m³", 12.5, C["deform"])
    cv.text_px(cv.X(8.2), cv.Y(6.6), "背填土（α = 0）", 13, C["text"], weight="700")
    cv.text_px(cv.X(8.2), cv.Y(5.95), "γm = 18 kN/m³", 12.5, C["text"])
    cv.text_px(cv.X(8.2), cv.Y(5.35), "c' = 0，φ' = 30°", 12.5, C["text"])
    cv.text_px(cv.X(8.2), cv.Y(4.75), "δB = 15°", 12.5, C["text"])
    cv.text_px(cv.X(3.6), cv.Y(-1.2), "基礎土壤（粘土質沉泥）φ' = 30°，c' = 20 kPa，γm = 18 kN/m³", 12.5, C["text"])
    cv.text_px(cv.X(3.6), cv.Y(-2.1), "牆底界面 ca = 15 kPa，δF = 18°；Nc = 30.14，Nq = 18.4，Nγ = 22.4", 12.5, C["muted"])
    xd = -1.5
    cv.line((xd - 0.1, H), (-0.1, H), C["dim"], 0.9, dash="2 3")
    cv.dim((xd, 0), (xd, H), "8.0 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((0, H + 0.55), (B_TOP, H + 0.55), "3.0 m", 0, C["dim"], 12.5, label_off=-14)
    cv.dim((0, -0.4), (B_BOT, -0.4), "5.0 m", 0, C["dim"], 12.5, label_off=14)
    return cv

compose([fig_problem()],
        title="SM-2016-4 題目附圖重繪",
        sub="依題目正本判讀清單；牆面鉛直、牆背外斜，β 為牆背與牆底（水平）的夾角，背填土面水平",
        note="攔錯用：β 是牆背面的傾角（tanβ = 8.0／2.0），不是背填土面傾角（α = 0）；牆前地面與牆底同高（Df = 0）。",
        path=os.path.join(OUT, "SM-2016-4-fig-1-problem.svg"))


# ── 解析 §4 數值（由題給量重算）────────────────────────────
G_S, PHI, DB, G_C = 18.0, 30.0, 15.0, 23.5
KH, KV = 0.15, 0.05
_r = math.radians
def _ka(th=0.0):
    b, p, d, a = _r(BETA), _r(PHI), _r(DB), 0.0
    t_ = _r(th)
    num = math.sin(p + b - t_) ** 2
    den = math.cos(t_) * math.sin(b) ** 2 * math.sin(b - d - t_) * (1 + math.sqrt(
        math.sin(p + d) * math.sin(p - a - t_) / (math.sin(b - d - t_) * math.sin(a + b)))) ** 2
    return num / den
KA   = _ka()                                   # 0.4148
PA   = 0.5 * G_S * H ** 2 * KA                 # 238.92
ANG  = 90 - BETA + DB                          # 29.04° below horizontal
PAH, PAV = PA * math.cos(_r(ANG)), PA * math.sin(_r(ANG))   # 208.89 / 115.97
XPA  = B_BOT - (H / 3) / H * (B_BOT - B_TOP)   # 4.333
W1, X1 = B_TOP * H * G_C, B_TOP / 2            # 564 @ 1.5
W2, X2 = 0.5 * (B_BOT - B_TOP) * H * G_C, B_TOP + (B_BOT - B_TOP) / 3   # 188 @ 3.667
SV   = W1 + W2 + PAV                           # 867.97
MR   = W1 * X1 + W2 * X2 + PAV * XPA           # 2037.9
MO   = PAH * H / 3                             # 557.1
XB   = (MR - MO) / SV                          # 1.706
E_   = B_BOT / 2 - XB                          # 0.794
QMAX, QMIN = SV / B_BOT * (1 + 6 * E_ / B_BOT), SV / B_BOT * (1 - 6 * E_ / B_BOT)   # 339.0 / 8.2
BP   = B_BOT - 2 * E_                          # 3.412
TH   = math.degrees(math.atan(PAH / SV))       # 13.53
THP  = math.degrees(math.atan(KH / (1 - KV)))  # 8.97
KAE  = _ka(THP)                                # 0.5414
PAE  = 0.5 * G_S * H ** 2 * (1 - KV) * KAE     # 296.26
DPAE = PAE - PA                                # 57.34
ZB   = (PA * H / 3 + DPAE * 0.6 * H) / PAE     # 3.08

def _wall(cv):
    cv.polygon([(0, 0), (B_BOT, 0), (B_TOP, H), (0, H)], "rgba(29,78,216,0.12)", C["deform"], 2.4)
    cv.line((B_TOP, H), (B_TOP, 0), C["muted"], 1.0, dash="4 3")
    cv.line((B_TOP, H), (B_TOP + 2.6, H), C["member"], 1.8)
    cv.dot((0, 0), 4.5, fill=C["member"])
    cv.text_px(cv.X(-0.15), cv.Y(0.3), "趾", 12, C["member"], anchor="end")

def _on_back(z):
    return (B_BOT - z / H * (B_BOT - B_TOP), z)

def fig_static():
    W, Hpx = 900, 760
    cv = Canvas(W, Hpx, bg="#FFFFFF", **fit(W, Hpx, (-3.4, 11.0), (-3.6, H + 1.0), 40, 40, 80, 30))
    cv.panel("㈠㈡ 靜態：Coulomb Pa、牆重與底壓", "Pa 與牆背法線夾 δB = 15° → 與水平夾 %.2f°（斜向下推牆）" % ANG)
    _wall(cv)
    ux, uy = -math.cos(_r(ANG)), -math.sin(_r(ANG))
    p = _on_back(H / 3); L = 4.6
    cv.arrow((p[0] - L * ux, p[1] - L * uy), p, C["load"], 3.6, 13)
    tag_px(cv, cv.X(p[0] - L * ux) - 4, cv.Y(p[1] - L * uy) - 22, "Pa = %.1f kN/m（Ka = %.4f）" % (PA, KA), 12, C["load"], anchor="middle")
    tag_px(cv, cv.X(p[0] - L * ux) - 4, cv.Y(p[1] - L * uy) + 12, "Pah = %.2f，Pav = %.2f" % (PAH, PAV), 12, C["load"], anchor="middle")
    tag_px(cv, cv.X(p[0]) + 14, cv.Y(p[1]) + 26, "@ H/3，x = %.3f m" % XPA, 11.5, C["load"], anchor="start")
    cv.arrow((X1, 5.6), (X1, 3.8), C["member"], 3.0, 11)
    tag_px(cv, cv.X(X1), cv.Y(6.0), "W1 = %.0f（x = %.1f）" % (W1, X1), 11.5, C["member"])
    cv.arrow((X2, 3.4), (X2, 1.8), C["member"], 3.0, 11)
    tag_px(cv, cv.X(X2) - 6, cv.Y(1.3), "W2 = %.0f（x = %.3f）" % (W2, X2), 11.5, C["member"], anchor="end")
    sq = 0.0062
    cv.polygon([(0, 0), (B_BOT, 0), (B_BOT, -sq * QMIN), (0, -sq * QMAX)], "rgba(29,78,216,0.14)", C["deform"], 1.8)
    for k in range(6):
        x = 0.1 + (B_BOT - 0.2) * k / 5
        q = QMAX + (QMIN - QMAX) * x / B_BOT
        if q * sq > 0.12:
            cv.arrow((x, -sq * q), (x, -0.05), C["deform"], 1.2, 7)
    tag_px(cv, cv.X(-0.15), cv.Y(-sq * QMAX), "qmax = %.1f kPa" % QMAX, 12, C["deform"], anchor="end")
    tag_px(cv, cv.X(B_BOT) + 10, cv.Y(-0.2), "qmin = %.1f kPa" % QMIN, 12, C["deform"], anchor="start")
    cv.dot((XB, 0), 5.0, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    tag_px(cv, cv.X(B_BOT) + 10, cv.Y(-0.85), "x̄ = %.3f m，e = %.3f m（小於 B/6）" % (XB, E_), 12, C["accent"], anchor="start")
    tag_px(cv, cv.X(B_BOT) + 10, cv.Y(-1.5), "B' = %.3f m，θ = %.2f°（傾斜因數）" % (BP, TH), 12, C["accent"], anchor="start")
    cv.dim((0, -sq * QMAX - 0.35), (B_BOT, -sq * QMAX - 0.35), "B = 5.0 m", 0, C["dim"], 12, label_off=14)
    tag_px(cv, cv.X(-0.4), cv.Y(6.6), "ΣV = %.2f" % SV, 11.5, C["text"], anchor="end")
    tag_px(cv, cv.X(-0.4), cv.Y(6.0), "ΣMR = %.1f" % MR, 11.5, C["text"], anchor="end")
    tag_px(cv, cv.X(-0.4), cv.Y(5.4), "MO = %.1f" % MO, 11.5, C["text"], anchor="end")
    return cv

def fig_mo():
    W, Hpx = 900, 760
    cv = Canvas(W, Hpx, bg="#FFFFFF", **fit(W, Hpx, (-3.4, 11.0), (-3.6, H + 1.0), 40, 40, 80, 30))
    cv.panel("㈢ M–O：靜態 Pa ＋ 動態增量 ΔPae", "θ' = %.2f°，Kae = %.4f；方向同靜態（與水平夾 %.2f°）" % (THP, KAE, ANG))
    _wall(cv)
    ux, uy = -math.cos(_r(ANG)), -math.sin(_r(ANG))
    for z, F, lab, col, L in ((H / 3, PA, "Pa = %.1f @ H/3 = %.3f m" % (PA, H / 3), C["load"], 4.4),
                              (0.6 * H, DPAE, "ΔPae = %.2f @ 0.6H = %.1f m" % (DPAE, 0.6 * H), C["bmd"], 2.0)):
        p = _on_back(z)
        cv.arrow((p[0] - L * ux, p[1] - L * uy), p, col, 3.2, 12)
        tag_px(cv, cv.X(p[0] - L * ux) + 8, cv.Y(p[1] - L * uy) - 4, lab, 12, col, anchor="start")
    p = _on_back(ZB); L = 2.4
    cv.arrow((p[0] - L * ux, p[1] - L * uy), p, C["accent"], 3.8, 13, dash="7 4")
    tag_px(cv, cv.X(5.6), cv.Y(2.0), "Pae = %.2f kN/m @ z̄ = %.2f m" % (PAE, ZB), 12.5, C["accent"], anchor="start")
    # 高度刻度
    for z, c in ((H / 3, C["load"]), (ZB, C["accent"]), (0.6 * H, C["bmd"])):
        q = _on_back(z)
        cv.line((-0.3, z), (q[0], z), c, 0.9, dash="3 3")
        cv.text_px(cv.X(-0.4), cv.Y(z), "%.2f m" % z, 12, c, anchor="end")
    tag_px(cv, cv.X(2.5), cv.Y(-1.2), "z̄ = [Pa·H/3 + ΔPae·0.6H] / Pae（Seed–Whitman）", 12, C["text"])
    tag_px(cv, cv.X(2.5), cv.Y(-2.0), "對照：全部 @ H/3 → 2.67 m；增量 @ 0.5H → 2.92 m", 11.5, C["muted"])
    return cv

compose([fig_static(), fig_mo()], cols=2,
        title="SM-2016-4 重力式擋土牆自由體圖與 M–O 合力位置",
        sub="FS傾倒 = %.2f、FS滑動 = %.2f；qmax = %.1f kPa；Pae = %.2f kN/m @ %.2f m" % (
            MR / MO, (15 * B_BOT + SV * math.tan(_r(18))) / PAH, QMAX, PAE, ZB),
        note="攔錯用：β 是牆背與水平面夾角（斜牆背使 Ka 變大）；Pa 與牆背法線夾 δB、與水平夾 29.04°；Pav 力臂取牆背上 H/3 處；ΔPae 作用高 0.6H。",
        path=os.path.join(OUT, "SM-2016-4-fig-2-fbd.svg"))
