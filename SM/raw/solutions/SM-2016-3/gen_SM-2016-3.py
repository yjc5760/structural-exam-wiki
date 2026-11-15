# -*- coding: utf-8 -*-
"""SM-2016-3 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2016-3-problem.md §4 判讀清單，不含任何解題結果。
fig-2-fbd：外部穩定自由體圖（土壓分布、W 與 qs 合力、底面合力傾角與 Meyerhof 有效寬度），數值取自解析 §4（2026-11-15 勘誤後）。
用法：python gen_SM-2016-3.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
L_R  = 4.5     # #3 加勁土體寬（面板外緣→加勁區右端）
H    = 6.0     # #3 牆高（頂面→地面線）
N_RF = 8       # #5 圖上加勁材道數（間距未給，等距示意）
QS   = 60      # #2 均佈荷載 kPa（加勁土＋背填土上方）

def ground_hatch(cv, x, y, n=4, s=0.16):
    for k in range(n):
        cv.line((x + k * s, y), (x + k * s - s * 0.9, y - s * 1.1), C["member"], 1.3)

def fig_problem():
    W, Hp = 900, 620
    XL, XR = -3.2, 9.6
    cv = Canvas(W, Hp, bg="#FFFFFF", **fit(W, Hp, (XL, XR), (-2.2, H + 1.9), 40, 40, 40, 40))
    XE = XR - 0.4
    soil_fill(cv, L_R, XE, 0, H, "rgba(180,83,9,0.13)")                 # 背填土
    soil_fill(cv, 0, L_R, 0, H, "rgba(46,125,111,0.13)")                 # 加勁土體
    soil_fill(cv, XL + 0.2, XE, -1.35, 0, "rgba(63,74,90,0.14)")          # 基礎土壤
    cv.line((XL + 0.2, 0), (XE, 0), C["member"], 2.4)                     # 地面線＝底面高程（#7）
    cv.line((0, H), (XE, H), C["member"], 2.0)                            # 地表水平（#6）
    for x in (-2.6, 7.6):
        ground_hatch(cv, x, 0)
    ground_hatch(cv, 7.6, H)
    cv.line((L_R, 0), (L_R, H), C["member2"], 1.6)                        # 加勁區右端
    for k in range(N_RF):
        y = H * (k + 0.5) / N_RF
        cv.line((0.08, y), (L_R, y), C["bmd"], 2.0)
    cv.line((0, 0), (0, H), C["member"], 6.0)                              # 面板（#4）
    cv.udl((0, H), (XE, H), 0.85, n=15, color=C["load"], w=1.8)
    cv.text_px(cv.X(XE / 2), cv.Y(H + 1.25), "qs = 60 kPa（加勁土與背填土上方）", 13.5, C["load"], weight="700")
    cv.text_px(cv.X(L_R / 2), cv.Y(3.0), "加勁土體（視為剛體）", 13, C["bmd"], weight="700")
    cv.text_px(cv.X(L_R / 2), cv.Y(2.45), "γm = 20 kN/m³", 12.5, C["bmd"])
    cv.text_px(cv.X(7.0), cv.Y(4.3), "背填土（砂質）", 13, C["text"], weight="700")
    cv.text_px(cv.X(7.0), cv.Y(3.7), "γm = 18 kN/m³", 12.5, C["text"])
    cv.text_px(cv.X(7.0), cv.Y(3.15), "c' = 0，φ' = 32°", 12.5, C["text"])
    cv.text_px(cv.X(-0.9), cv.Y(H * 0.5), "面板", 12.5, C["member"], weight="700")
    cv.text_px(cv.X(4.6), cv.Y(-1.05), "基礎土壤（粘土質沉泥）φ' = 32°，c' = 20 kPa，γm = 18 kN/m³", 12.5, C["text"])
    cv.text_px(cv.X(4.6), cv.Y(-1.65), "底面界面 ca = 12 kPa，δ = 15°；Nc = 35.49，Nq = 23.18，Nγ = 30.22", 12.5, C["muted"])
    xd = -2.3
    cv.line((xd - 0.1, H), (-0.1, H), C["dim"], 0.9, dash="2 3")
    cv.dim((xd, 0), (xd, H), "6.0 m", 0, C["dim"], 12.5, label_off=-26)
    cv.dim((0, -0.35), (L_R, -0.35), "4.5 m", 0, C["dim"], 12.5, label_off=14)
    return cv

compose([fig_problem()],
        title="SM-2016-3 題目附圖重繪",
        sub="依題目正本判讀清單；加勁土體 4.5 m × 6.0 m，面板外側地面與底面同高（Df = 0）",
        note="攔錯用：qs 同時壓在加勁土體與背填土上；加勁土體底面就是基礎面（無埋入）；圖上 8 道加勁材只是示意，間距未給。",
        path=os.path.join(OUT, "SM-2016-3-fig-1-problem.svg"))


# ── 解析 §4 數值（2026-11-15 勘誤後；由給定量重算，標註與 §4 一致）──────────
PHI_B, G_B, G_M = 32.0, 18.0, 20.0
KA  = round(math.tan(math.radians(45 - PHI_B / 2)) ** 2, 4) # §4(一)1  0.3073（§4 以四位數續算）
PA1 = 0.5 * KA * G_B * H ** 2                              # 99.56 kN/m @ H/3
PA2 = KA * QS * H                                          # 110.63 kN/m @ H/2
PH  = PA1 + PA2                                            # 210.19
MO  = PA1 * H / 3 + PA2 * H / 2                            # 531.01
W_S = G_M * H * L_R                                        # 540
Q_S = QS * L_R                                             # 270
V   = W_S + Q_S                                            # 810
MR  = V * L_R / 2                                          # 1822.5
XR_ = (MR - MO) / V                                        # 1.594 合力距牆趾
E_  = round(L_R / 2 - XR_, 3)                              # 0.656（§4 取三位數續算）
LP  = L_R - 2 * E_                                         # 3.188 有效寬度
QE  = V / LP                                               # 254.08
TH  = math.degrees(math.atan(PH / V))                      # 14.55°
E_X = L_R / 2 - XR_                                        # 未進位 e，供 §5 對照 qmax/qmin
# 承載力因數以未進位 Ka 全程計算（§4(二) 3–5：θ = 14.55°、ic = 0.703、iγ = 0.298、qult = 756.97）
_KAX = math.tan(math.radians(45 - PHI_B / 2)) ** 2
_THX = math.degrees(math.atan((0.5 * _KAX * G_B * H ** 2 + _KAX * QS * H) / V))
IC, IG = (1 - _THX / 90) ** 2, (1 - _THX / 32) ** 2
QMAX, QMIN = V / L_R * (1 + 6 * E_X / L_R), V / L_R * (1 - 6 * E_X / L_R)   # 337.3 / 22.7

def fig_fbd():
    W, Hp = 1100, 720
    XL, XR = -3.4, 9.2
    cv = Canvas(W, Hp, bg="#FFFFFF", **fit(W, Hp, (XL, XR), (-3.2, H + 1.3), 40, 40, 40, 40))
    soil_fill(cv, 0, L_R, 0, H, "rgba(46,125,111,0.13)")
    cv.polygon([(0, 0), (L_R, 0), (L_R, H), (0, H)], "none", C["bmd"], 2.2)
    cv.line((0, 0), (0, H), C["member"], 6.0)
    # qs 於加勁土體上方（垂直力）
    cv.udl((0, H), (L_R, H), 0.7, n=9, color=C["load"], w=1.8)
    cv.text_px(cv.X(L_R / 2), cv.Y(H + 1.05), "qs = 60 kPa → Q = 60 × 4.5 = 270 kN/m", 13, C["load"], weight="700")
    # 土壓分布：背面 x = L_R，向左壓；比例 s m/kPa
    s = 0.045
    p_top, p_bot = KA * QS, KA * QS + KA * G_B * H
    cv.polygon([(L_R, H), (L_R + s * p_top, H), (L_R + s * p_bot, 0), (L_R, 0)], "rgba(180,83,9,0.16)", C["load"], 1.6)
    cv.line((L_R + s * p_top, H), (L_R + s * p_top, 0), C["load"], 1.0, dash="4 3")
    for k in range(7):
        y = H * (k + 0.5) / 7
        pp = p_top + KA * G_B * (H - y)
        cv.arrow((L_R + s * pp, y), (L_R + 0.06, y), C["load"], 1.3, 7)
    cv.text_px(cv.X(L_R + s * p_top) + 6, cv.Y(H) - 12, "Ka·qs = %.2f kPa" % p_top, 12, C["load"], anchor="start")
    cv.text_px(cv.X(L_R + s * p_bot) + 8, cv.Y(0) - 14, "Ka·qs + Ka·γb·H = %.2f kPa" % p_bot, 12, C["load"], anchor="start")
    # 合力
    xa = L_R + s * p_bot + 0.55
    cv.arrow((xa + 1.1, H / 3), (L_R + 0.05, H / 3), C["load"], 3.4, 12)
    cv.arrow((xa + 1.1, H / 2), (L_R + 0.05, H / 2), C["load"], 3.4, 12)
    tag_px(cv, cv.X(xa + 1.15), cv.Y(H / 3) + 0, "Pa1 = %.1f kN/m @ H/3 = 2.0 m" % PA1, 12, C["load"], anchor="start")
    tag_px(cv, cv.X(xa + 1.15), cv.Y(H / 2) - 0, "Pa2 = %.1f kN/m @ H/2 = 3.0 m" % PA2, 12, C["load"], anchor="start")
    tag_px(cv, cv.X(xa + 1.15), cv.Y(H / 2) - 34, "Ph = %.2f kN/m，MO = %.2f kN·m/m" % (PH, MO), 12, C["text"], anchor="start")
    # W、Q（作用於 L/2）
    cv.arrow((L_R / 2, 5.0), (L_R / 2, 3.4), C["member"], 3.4, 12)
    tag_px(cv, cv.X(L_R / 2), cv.Y(5.35), "W = 540、Q = 270 → V = %.0f kN/m（@ L/2 = 2.25 m）" % V, 12, C["member"])
    tag_px(cv, cv.X(L_R / 2), cv.Y(2.6), "加勁土體（剛體）γm = 20", 12, C["bmd"])
    # 底面：有效寬度均佈 q' 與梯形 qmax/qmin（虛線對照）
    sq = 0.0042
    cv.polygon([(0, 0), (LP, 0), (LP, -sq * QE), (0, -sq * QE)], "rgba(29,78,216,0.14)", C["deform"], 1.8)
    for k in range(6):
        x = LP * (k + 0.5) / 6
        cv.arrow((x, -sq * QE), (x, -0.06), C["deform"], 1.3, 7)
    cv.poly([(0, -sq * QMAX), (L_R, -sq * QMIN)], C["muted"], 1.4, dash="5 4")
    cv.line((0, 0), (0, -sq * QMAX), C["muted"], 1.0, dash="5 4")
    cv.line((L_R, 0), (L_R, -sq * QMIN), C["muted"], 1.0, dash="5 4")
    cv.dim((0, -sq * QMAX - 0.35), (LP, -sq * QMAX - 0.35), "有效寬度 L' = L − 2e = %.3f m" % LP, 0, C["deform"], 12.5, label_off=14)
    tag_px(cv, cv.X(-0.12), cv.Y(-sq * QE / 2), "q' = V/L' = %.2f kPa" % QE, 12, C["deform"], anchor="end")
    cv.text_px(cv.X(L_R) + 8, cv.Y(-sq * QMIN) + 30, "對照：qmax / qmin = %.1f / %.1f kPa（虛線，梯形分布）" % (QMAX, QMIN), 11.5, C["muted"], anchor="start")
    # 合力 R：作用於 x = XR_，傾角 TH（反力向上、向牆背側）
    a = 1.25
    p0 = (XR_ - a * math.tan(math.radians(TH)), -a - 0.05)
    cv.line((XR_, 0), (XR_, -a - 0.2), C["accent"], 1.0, dash="3 3")
    cv.arrow(p0, (XR_, 0.0), C["accent"], 3.6, 13)
    tag_px(cv, cv.X(XR_) + 150, cv.Y(-a - 0.15), "R 傾角 θ = arctan(Ph/V) = %.2f°" % TH, 12, C["accent"], anchor="start")
    tag_px(cv, cv.X(XR_) + 10, cv.Y(0.45), "x = %.3f m，e = %.3f m" % (XR_, E_), 11.5, C["accent"], anchor="start")
    cv.dot((XR_, 0), 5.0, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    cv.text_px(cv.X(-0.9), cv.Y(H * 0.5), "面板", 12.5, C["member"], weight="700")
    cv.dot((0, 0), 4.5, fill=C["member"])
    cv.text_px(cv.X(-0.35), cv.Y(0.3), "趾", 12, C["member"], anchor="end")
    return cv

compose([fig_fbd()],
        title="SM-2016-3 加勁土體外部穩定自由體圖",
        sub="Rankine Ka = %.4f；FS傾倒 = %.2f、FS滑動 = %.2f；承載 iγ = %.3f、ic = %.3f → FS承載 = %.2f" % (
            KA, MR / MO, (12 * L_R + V * math.tan(math.radians(15))) / PH,
            IG, IC, (20 * 35.49 * IC + 0.5 * 18 * LP * 30.22 * IG) / QE),
        note="攔錯用：底面合力傾斜 %.2f°，承載力必須乘考卷第 4 頁的傾斜因數（iγ 只剩 0.30）；qs 同時加推力與垂直力；有效寬度 L' 由牆趾量起。" % TH,
        path=os.path.join(OUT, "SM-2016-3-fig-2-fbd.svg"))
