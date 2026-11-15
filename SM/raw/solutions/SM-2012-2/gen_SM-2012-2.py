# -*- coding: utf-8 -*-
"""SM-2012-2 圖解：Casagrande 作圖法（題目㈠要求作圖）。
曲線為示意，作圖步驟依 SM-2012-2.md §4（一）六步；最大曲率點、切線、角平分線、交點皆由程式算出。
用法：python gen_SM-2012-2.py [輸出資料夾]"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 示意曲線 e(x)，x = log10 σ'（σ' 單位 kPa；只用於形狀）──
E0, CR, CC, XP, SM = 1.00, 0.04, 0.32, math.log10(120.0), 0.16
sp = lambda u: SM * math.log(1 + math.exp(u / SM))
e = lambda x: E0 - CR * (x - 1) - (CC - CR) * sp(x - XP)
de = lambda x, h=1e-4: (e(x + h) - e(x - h)) / (2 * h)
d2e = lambda x, h=1e-3: (e(x + h) - 2 * e(x) + e(x - h)) / h ** 2
XS = [1.0 + i * 2.0 / 4000 for i in range(4001)]
# 圖面座標下的曲率（x、e 各自正規化到 0–1 才符合「圖上看起來最彎」）
KX, KE = 2.0, 0.5
curv = lambda x: abs(d2e(x) * KX ** 2 / KE) / (1 + (de(x) * KX / KE) ** 2) ** 1.5 / KX ** 2 * KX
XA = max(XS, key=lambda x: abs(d2e(x) / KE * KX ** 2) / (1 + (de(x) * KX / KE) ** 2) ** 1.5)
EA = e(XA)
# 切線與水平線的夾角（圖面座標），角平分線
ang_t = math.atan(de(XA) * KX / KE)            # 負值
ang_b = ang_t / 2
slope_b = math.tan(ang_b) * KE / KX            # 回到資料座標的斜率
# 正常壓密段直線（x 大時的漸近線）延伸
xv = 2.9
s_v = de(xv); e_v = lambda x: e(xv) + s_v * (x - xv)
XC = (e_v(0) - (EA - slope_b * XA)) / (slope_b - s_v) if False else None
# 解 EA + slope_b (x - XA) = e(xv) + s_v (x - xv)
XC = (e(xv) - s_v * xv - EA + slope_b * XA) / (slope_b - s_v)
EC = EA + slope_b * (XC - XA)
SIG_P = 10 ** XC

def fig():
    W, H = 900, 580
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (0, 1.6), (0, 1.0), 70, 220, 70, 76))
    X0, X1, Y0, Y1 = 1.0, 3.0, 0.40, 1.04
    SX = lambda x: (x - X0) / (X1 - X0) * 1.6
    SY = lambda v: (v - Y0) / (Y1 - Y0)
    frame(cv, 0, 1.6, 0, 1.0, [], [], "有效應力 σ'（對數座標）", "", grid=False)
    cv.text_px(cv.X(0) - 10, cv.Y(1.0) - 22, "孔隙比 e", 13, C["text"], anchor="start")
    for x, lab in ((1, "10"), (2, "100"), (3, "1000")):
        cv.text_px(cv.X(SX(x)), cv.Y(0) + 18, lab, 12.5, C["muted"])
    cv.poly([(SX(x), SY(e(x))) for x in XS[::10]], C["member"], 3.0)
    # ① 最大曲率點 A
    cv.dot((SX(XA), SY(EA)), 6, fill=C["accent"])
    tag_px(cv, cv.X(SX(XA)) - 16, cv.Y(SY(EA)) + 30, "① A（最大曲率）", 12.5, C["accent"], anchor="end")
    # ② 水平線 ③ 切線 ④ 角平分線
    xr = XA + 0.75
    cv.line((SX(XA), SY(EA)), (SX(xr), SY(EA)), C["muted"], 1.8)
    cv.text_px(cv.X(SX(xr)) + 6, cv.Y(SY(EA)), "② 水平線", 12.5, C["muted"], anchor="start")
    cv.line((SX(XA - 0.25), SY(EA + de(XA) * -0.25)), (SX(XA + 0.55), SY(EA + de(XA) * 0.55)), C["deform"], 1.8)
    cv.text_px(cv.X(SX(XA + 0.55)) + 6, cv.Y(SY(EA + de(XA) * 0.55)), "③ 切線", 12.5, C["deform"], anchor="start")
    cv.line((SX(XA), SY(EA)), (SX(xr), SY(EA + slope_b * (xr - XA))), C["bmd"], 2.2)
    cv.text_px(cv.X(SX(xr)) + 6, cv.Y(SY(EA + slope_b * (xr - XA))), "④ 角平分線", 12.5, C["bmd"], anchor="start")
    # ⑤ 正常壓密段往上延伸
    cv.line((SX(XC - 0.15), SY(e_v(XC - 0.15))), (SX(3.0), SY(e_v(3.0))), C["load"], 1.8, dash="7 4")
    cv.text_px(cv.X(SX(2.55)) + 10, cv.Y(SY(e_v(2.55))), "⑤ 正常壓密段延伸", 12.5, C["load"], anchor="start")
    # ⑥ 交點 → σ'p
    cv.dot((SX(XC), SY(EC)), 6.5, fill="#FFFFFF", stroke=C["load"], w=2.8)
    cv.line((SX(XC), SY(EC)), (SX(XC), 0), C["load"], 1.6, dash="3 3")
    tag_px(cv, cv.X(SX(XC)), cv.Y(0) - 18, "⑥ σ'p", 13, C["load"])
    return cv

compose([fig()],
        title="圖 1　Casagrande 法決定預壓密應力（示意曲線）",
        sub="最大曲率點的水平線與切線取角平分線，與正常壓密直線段延伸的交點即 σ'p",
        note="攔錯用：把最大曲率點本身或曲線轉折處直接當 σ'p；σ'p 必須是角平分線與正常壓密段延伸線的交點，通常略大於 A 點應力。",
        path=os.path.join(OUT, "SM-2012-2-fig-1-casagrande.svg"))
print("A at", 10 ** XA, " sigma_p", SIG_P)
