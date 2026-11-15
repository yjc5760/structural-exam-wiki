# -*- coding: utf-8 -*-
"""SM-2009-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2009-4-problem.md §4 判讀清單，不含任何解題結果。
牆底寬 B 為㈠所求（判讀 #6），圖上牆面斜率僅為示意，不是解得的 B。
fig-2-fbd：解題自由體圖（B 由 §4 二次式解出；土壓、分塊牆重、合力落在 B/3 與三角形底壓），數值取自解析 §4。
用法：python gen_SM-2009-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, soil_fill
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H     = 6.0     # #4 牆高（牆頂→牆底）
B_TOP = 0.6     # #5 牆頂寬（牆頂左角→牆背）
ALPHA = 20.0    # #9 背填土面傾角（自牆背頂點起）
B_SKETCH = 2.2  # #6 牆底寬 B 未知（㈠所求）——僅供示意的繪圖值，不是答案

def ground_hatch(cv, x, y, n=4, s=0.16):
    for k in range(n):
        cv.line((x + k * s, y), (x + k * s - s * 0.9, y - s * 1.1), C["member"], 1.3)

def fig_problem():
    W, Hpx = 900, 640
    XL, XR = -3.2, 4.6
    cv = Canvas(W, Hpx, bg="#FFFFFF", **fit(W, Hpx, (XL, XR), (-1.4, H + 2.0), 40, 40, 40, 40))
    xb = 0.0                        # 牆背（鉛直，#3）
    xt = xb - B_TOP                 # 牆頂左角
    xtoe = xb - B_SKETCH            # 牆趾（示意）
    # 背填土
    xe = XR - 0.2
    ye = H + (xe - xb) * math.tan(math.radians(ALPHA))
    cv.polygon([(xb, 0), (xe, 0), (xe, ye), (xb, H)], "rgba(180,83,9,0.13)")
    # 基礎土壤
    soil_fill(cv, XL + 0.2, XR - 0.2, -1.0, 0, "rgba(63,74,90,0.14)")
    cv.line((XL + 0.2, 0), (XR - 0.2, 0), C["member"], 2.4)          # 地面線＝牆底高程（#11）
    for x in (-2.7, 3.4):
        ground_hatch(cv, x, 0)
    # 牆身（梯形，#3）
    cv.polygon([(xtoe, 0), (xb, 0), (xb, H), (xt, H)], "rgba(29,78,216,0.16)", C["deform"], 2.4)
    # 背填土面 20°（#9）
    cv.line((xb, H), (xe, ye), C["member"], 2.2)
    cv.line((xb, H), (xb + 1.6, H), C["dim"], 1.0, dash="4 3")
    r = 1.05
    pts = [(xb + r * math.cos(math.radians(a)), H + r * math.sin(math.radians(a))) for a in range(0, int(ALPHA) + 1)]
    cv.poly(pts, C["accent"], 1.6)
    cv.text_px(cv.X(xb + r + 0.45), cv.Y(H + 0.2), "20°", 14, C["accent"], weight="700")
    # 文字
    cv.text_px(cv.X(2.4), cv.Y(3.4), "砂土（背填土）", 14, C["text"], weight="700")
    cv.text_px(cv.X(2.4), cv.Y(2.8), "γ = 18 kN/m³，摩擦角 30°", 12.5, C["text"])
    cv.text_px(cv.X(-1.0), cv.Y(2.4), "混凝土", 12.5, C["deform"], weight="700")
    cv.text_px(cv.X(-1.0), cv.Y(1.9), "24 kN/m³", 12, C["deform"])
    cv.text_px(cv.X(2.2), cv.Y(-0.55), "基礎土壤  γ = 16 kN/m³，摩擦角 33°", 12.5, C["text"])
    cv.text_px(cv.X(xtoe) - 6, cv.Y(0.45), "牆趾", 12, C["muted"], anchor="end")
    cv.text_px(cv.X(xb) + 8, cv.Y(0.45), "牆踵", 12, C["muted"], anchor="start")
    # 尺寸線
    cv.dim((xt, H + 0.55), (xb, H + 0.55), "0.6 m", 0, C["dim"], 12.5, label_off=-14)
    for x in (xt, xb):
        cv.line((x, H + 0.05), (x, H + 0.7), C["dim"], 0.9, dash="2 3")
    xd = xtoe - 0.9
    cv.dim((xd, 0), (xd, H), "6 m", 0, C["dim"], 12.5, label_off=-26)
    cv.line((xd - 0.1, H), (xt - 0.05, H), C["dim"], 0.9, dash="2 3")
    cv.dim((xtoe, -0.45), (xb, -0.45), "B", 0, C["load"], 13, label_off=14)
    cv.text_px(cv.X((xtoe + xb) / 2), cv.Y(-0.45) + 34, "牆底寬（㈠所求）", 12, C["load"], weight="700")
    return cv

compose([fig_problem()],
        title="SM-2009-4 題目附圖重繪",
        sub="依題目正本判讀清單；牆背鉛直、牆面傾斜，背填土面自牆背頂點上傾 20°",
        note="攔錯用：牆底寬 B 是㈠所求（圖上牆面斜率只是示意）；牆前地面與牆底同高、沒有被動土；題目沒給 δ 與牆底介面參數。",
        path=os.path.join(OUT, "SM-2009-4-fig-1-problem.svg"))


# ── 解析 §4 數值（由給定量重算；B 取 §4 的兩位數 2.49 續算）──────────────
G_S, PHI, G_C = 18.0, 30.0, 24.0
_ca, _cp = math.cos(math.radians(ALPHA)), math.cos(math.radians(PHI))
KA  = _ca * (_ca - math.sqrt(_ca**2 - _cp**2)) / (_ca + math.sqrt(_ca**2 - _cp**2))   # 0.4142
PA  = 0.5 * KA * G_S * H**2                                    # 134.20
PAH, PAV = PA * _ca, PA * math.sin(math.radians(ALPHA))        # 126.11 / 45.90
# ㈠ 3(ΣMR − MO) = B·ΣV → 72B² + aB + c = 0（§4 Step 3）
def _resid(B):
    W1, W2 = B_TOP * H * G_C, 0.5 * (B - B_TOP) * H * G_C
    SV = W1 + W2 + PAV
    MR = W1 * (B - B_TOP / 2) + W2 * 2 / 3 * (B - B_TOP) + PAV * B
    return (MR - PAH * H / 3) / SV - B / 3
_lo, _hi = 1.0, 5.0
for _ in range(80):
    _m = (_lo + _hi) / 2
    _lo, _hi = (_m, _hi) if _resid(_lo) * _resid(_m) > 0 else (_lo, _m)
B_EX = _m                                                      # 2.490
B   = round(B_EX, 2)                                           # 2.49
W1, W2 = B_TOP * H * G_C, 0.5 * (B - B_TOP) * H * G_C          # 86.4 / 136.08
X1, X2 = B - B_TOP / 2, 2 / 3 * (B - B_TOP)
SV  = W1 + W2 + PAV                                            # 268.38
MR  = W1 * X1 + W2 * X2 + PAV * B                              # 474.96
MO  = PAH * H / 3                                              # 252.22
XBAR = (MR - MO) / SV                                          # 0.830 = B/3
QTOE = 2 * SV / B                                              # e = B/6 → 三角形底壓

def fig_fbd():
    W, Hpx = 1100, 720
    XL, XR = -2.6, 7.6
    cv = Canvas(W, Hpx, bg="#FFFFFF", **fit(W, Hpx, (XL, XR), (-2.6, H + 1.9), 40, 40, 40, 40))
    xt = B - B_TOP
    cv.polygon([(0, 0), (B, 0), (B, H), (xt, H)], "rgba(29,78,216,0.12)", C["deform"], 2.4)
    cv.line((xt, H), (xt, 0), C["muted"], 1.0, dash="4 3")      # 分塊線
    # 背填土面（自牆背頂上傾 20°）
    xe = B + 1.6
    cv.line((B, H), (xe, H + 1.6 * math.tan(math.radians(ALPHA))), C["member"], 1.8)
    cv.text_px(cv.X(xe) + 4, cv.Y(H + 1.6 * math.tan(math.radians(ALPHA))), "α = 20°", 12, C["member"], anchor="start")
    # 土壓分布：沿牆背三角形，方向平行地表（向牆、向下 20°）
    s = 0.045
    pb = KA * G_S * H
    ux, uy = _ca, math.sin(math.radians(ALPHA))
    cv.polygon([(B, H), (B, 0), (B + s * pb * ux, s * pb * uy)], "rgba(180,83,9,0.16)", C["load"], 1.5)
    for k in range(1, 7):
        y = H * (1 - k / 7)
        pp = KA * G_S * (H - y)
        cv.arrow((B + s * pp * ux, y + s * pp * uy), (B + 0.05 * ux, y + 0.05 * uy), C["load"], 1.2, 7)
    cv.text_px(cv.X(B + s * pb * ux) + 8, cv.Y(s * pb * uy) + 4, "Ka·γ·H = %.2f kPa" % pb, 12, C["load"], anchor="start")
    # Pa 合力 @ H/3，平行地表
    L = 2.4
    cv.arrow((B + L * ux, H / 3 + L * uy), (B + 0.04, H / 3), C["load"], 3.6, 13)
    tag_px(cv, cv.X(B + L * ux) + 8, cv.Y(H / 3 + L * uy) - 4, "Pa = %.2f kN/m（平行地表，@ H/3 = 2 m）" % PA, 12, C["load"], anchor="start")
    tag_px(cv, cv.X(B + L * ux) + 8, cv.Y(H / 3 + L * uy) + 28, "Pah = %.2f → MO = %.2f；Pav = %.2f（力臂 B）" % (PAH, MO, PAV), 12, C["text"], anchor="start")
    # 牆重
    cv.arrow((X1, 4.3), (X1, 2.9), C["member"], 3.0, 11)
    tag_px(cv, cv.X(X1) - 10, cv.Y(4.55), "W1 = %.1f（x = B − 0.3 = %.2f）" % (W1, X1), 11.5, C["member"], anchor="end")
    cv.arrow((X2, 2.6), (X2, 1.2), C["member"], 3.0, 11)
    tag_px(cv, cv.X(X2) - 10, cv.Y(2.85), "W2 = %.2f（x = 2/3·(B − 0.6) = %.2f）" % (W2, X2), 11.5, C["member"], anchor="end")
    # 底壓：三角形，牆趾最大、牆踵為 0
    sq = 0.006
    cv.polygon([(0, 0), (B, 0), (0, -sq * QTOE)], "rgba(29,78,216,0.14)", C["deform"], 1.8)
    for k in range(5):
        x = B * k / 5 + 0.08
        cv.arrow((x, -sq * QTOE * (1 - x / B)), (x, -0.05), C["deform"], 1.2, 7)
    tag_px(cv, cv.X(-0.15), cv.Y(-sq * QTOE), "q趾 = 2ΣV/B = %.1f kPa" % QTOE, 12, C["deform"], anchor="end")
    tag_px(cv, cv.X(B) + 10, cv.Y(-0.25), "q踵 = 0（e = B/6）", 12, C["deform"], anchor="start")
    # 合力 @ B/3
    cv.line((XBAR, 0.0), (XBAR, -sq * QTOE - 0.2), C["accent"], 1.0, dash="3 3")
    cv.dot((XBAR, 0), 5.0, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    tag_px(cv, cv.X(B) + 10, cv.Y(-0.8), "合力點 x̄ = (ΣMR − MO)/ΣV = %.3f m = B/3（距牆趾）" % XBAR, 12, C["accent"], anchor="start")
    cv.dim((0, -sq * QTOE - 0.45), (B, -sq * QTOE - 0.45), "B = %.2f m" % B, 0, C["dim"], 12.5, label_off=14)
    cv.dim((0, -sq * QTOE - 0.95), (XBAR, -sq * QTOE - 0.95), "B/3", 0, C["accent"], 12, label_off=14)
    cv.dot((0, 0), 4.5, fill=C["member"])
    cv.text_px(cv.X(-0.15), cv.Y(0.3), "趾", 12, C["member"], anchor="end")
    tag_px(cv, cv.X(-0.4), cv.Y(1.6), "ΣV = %.2f kN/m" % SV, 12, C["text"], anchor="end")
    tag_px(cv, cv.X(-0.4), cv.Y(1.0), "ΣMR = %.1f kN·m/m" % MR, 12, C["text"], anchor="end")
    return cv

compose([fig_fbd()],
        title="SM-2009-4 重力式擋土牆自由體圖（B = %.2f m）" % B,
        sub="Rankine 傾斜地表 Ka = %.4f；FS傾倒 = %.2f（< 2.0）、FS滑動 = ΣV·tan33° / Pah = %.2f（< 1.5）" % (
            KA, MR / MO, SV * math.tan(math.radians(33)) / PAH),
        note="攔錯用：Pa 平行地表（不是水平），Pav 作用在牆背、力臂為 B；合力距牆趾 B/3 ⇔ e = B/6，底壓為三角形、牆踵恰為 0。",
        path=os.path.join(OUT, "SM-2009-4-fig-2-fbd.svg"))
