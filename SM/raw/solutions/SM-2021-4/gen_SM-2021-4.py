# -*- coding: utf-8 -*-
"""SM-2021-4 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2021-4-problem.md §4 判讀清單（#2–#12；
考卷附圖依 5 m 比例尺量測的座標，精度約 ±0.2 m），不含任何解題結果。
用法：python gen_SM-2021-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單（原點＝坡趾，m）────────────────
CREST = (20.4, 14.0)                       # #3 坡肩
X_B   = [0.0, 5.25, 10.38, 15.34, 20.35, 25.8]          # #4 切片邊界（坡趾→坡肩側）
Y_TOP = [0.0, 3.60, 7.11, 10.49, 13.92, 14.0]          # #5 邊界上端（地表）
Y_BOT = [0.0, -0.55, -0.09, 1.45, 4.70, 14.0]          # #5 邊界下端（圓弧）
ALPHA = {1: "60°", 2: "42°", 3: "30°", 4: "13°", 5: "0°（未標，判讀）"}   # #6
O     = (3.5, 18.6)                        # #7 圓心（量測，示意）
Y_WT  = 4.77                               # #8 坡體內水位高程
X_WT  = Y_WT * CREST[0] / CREST[1]         # 水位與坡面交點（≈ 6.96）
LEFT_GROUND = (-7.2, -0.46)                # #3 坡趾左側地面

def catmull(pts, n=16):
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t * t
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t ** 3) for k in (0, 1)))
    return out + [pts[-1]]

def fig_problem():
    W, H = 1000, 640
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-8.5, 33.5), (-4.6, 20.0), 30, 30, 40, 40))
    ground = [LEFT_GROUND, (0, 0), CREST, (32.0, CREST[1])]
    arcp = catmull(list(zip(X_B, Y_BOT)))
    cv.polygon([(0, 0), CREST, (X_B[-1], CREST[1])] + arcp[::-1], "rgba(180,83,9,0.16)")
    cv.poly(ground, C["member"], 2.8)
    cv.poly(arcp, C["load"], 2.6, dash="10 6")
    for x, yt, yb in zip(X_B[1:-1], Y_TOP[1:-1], Y_BOT[1:-1]):
        cv.line((x, yt), (x, yb), C["member"], 1.8)
    # 地下水位（#8、#9）
    cv.line((X_WT, Y_WT), (32.0, Y_WT), C["deform"], 1.9, dash="8 5")
    cv.line((0, 0), (X_WT, Y_WT), C["deform"], 4.5, dash="8 5", op=0.55)
    cv.line(LEFT_GROUND, (0, 0), C["deform"], 4.5, dash="8 5", op=0.55)
    wt(cv, 29.0, Y_WT, 0.32)
    wt(cv, -4.5, -0.29, 0.32)
    cv.text_px(cv.X(32.0) - 4, cv.Y(Y_WT) + 16, "地下水位", 12, C["deform"], anchor="end", weight="700")
    cv.text_px(cv.X(1.2), cv.Y(3.4), "水位沿坡面", 11.5, C["deform"], anchor="end")
    # 切片編號與 α（#6、#12）
    for n in range(1, 6):
        i = 5 - n
        xm = (X_B[i] + X_B[i + 1]) / 2
        ym = (min(Y_TOP[i + 1], CREST[1]) + max(Y_BOT[i], Y_BOT[i + 1])) / 2
        if n == 1: xm, ym = 22.4, 11.0
        if n == 5: xm, ym = 3.3, 1.1
        cv.text_px(cv.X(xm), cv.Y(ym), str(n), 15, C["text"], weight="700")
        lab = "α%d = %s" % (n, ALPHA[n])
        yb = min(Y_BOT[i], Y_BOT[i + 1]) - 1.3
        if n == 1: xm, yb = 25.6, 8.0
        if n == 5: xm = 1.0
        tag_px(cv, cv.X(xm), cv.Y(yb), lab, 11.5, C["load"] if n != 5 else C["accent"], weight="700")
    # 圓心
    cv.dot(O, 6, fill=C["member"])
    cv.text_px(cv.X(O[0]) - 10, cv.Y(O[1]), "O（量測約 (3.5, 18.6)，示意）", 11.5, C["muted"], anchor="end")
    # 比例尺與尺寸
    cv.dim((X_B[3], 17.5), (X_B[4], 17.5), "5 m", 0, C["dim"], 12, label_off=-14)
    cv.text_px(cv.X(X_B[4]) + 8, cv.Y(17.5), "考卷比例尺", 11.5, C["muted"], anchor="start")
    cv.text_px(cv.X(12.0), cv.Y(19.6), "γ = 18、γsat = 20 kN/m³，c' = 10 kN/m²，φ' = 36°", 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(27.5), cv.Y(CREST[1] + 0.8), "假設破壞面", 12.5, C["load"], weight="700")
    cv.dim((-2.0, 0), (-2.0, CREST[1]), "≈14.0 m", 0, C["dim"], 11.5, label_off=-30)
    cv.line((-2.4, CREST[1]), (CREST[0], CREST[1]), C["dim"], 0.9, dash="2 3")
    cv.dim((0, -3.6), (CREST[0], -3.6), "≈20.4 m", 0, C["dim"], 11.5, label_off=14)
    return cv

compose([fig_problem()],
        title="SM-2021-4 題目附圖重繪（依比例尺量測）",
        sub="考卷沒有給切片尺寸；座標由 5 m 比例尺量得（±0.2 m），α 依考卷標註，α5 未標、判讀為 0°",
        note="攔錯用：切片 1 底部在水位以上（u = 0）；水位在坡面轉沿坡面到坡趾；切片邊界是鉛直實線，不是 O 的虛線半徑。",
        path=os.path.join(OUT, "SM-2021-4-fig-1-problem.svg"))


# ═══ fig-2-slices：解題圖解（階段 E，2026-11-15）══════════════════════
# 幾何：題目正本 #3–#5、#8 的比例尺量測（58.5 px/m，坡趾原點）；邊界之間圓弧為同一框架的像素描點。
# 數值：解析 §4 Step 2–5（勘誤 2026-11-15 後，verify 腳本 MISMATCHES: 0）。
import math
ARC_PX = [(480,1292),(560,1306),(640,1312),(720,1316),(760,1316),(840,1312),(920,1306),(1000,1296),(1040,1289),
          (1120,1269),(1160,1256),(1200,1246),(1240,1232),(1320,1201),(1360,1182),(1400,1164),(1440,1141),(1480,1113),
          (1560,1064),(1600,1031),(1680,961),(1720,919),(1760,872),(1800,816),(1840,756),(1880,686)]
PXM, PX0, PY0 = 58.5, 441.8, 1283.9
ARC = [(0.0, 0.0)] + [((px - PX0) / PXM, (PY0 - py) / PXM) for px, py in ARC_PX] + [(25.8, 13.92)]
O_PX = (651, 200); O2 = ((O_PX[0] - PX0) / PXM, (PY0 - O_PX[1]) / PXM)      # 考卷 O 點（像素量測）
WPT_PX = {1: (1790, 826), 2: (1519, 1094), 3: (1220, 1244), 4: (894, 1308), 5: (656, 1323)}   # W_n 作用點（圓弧上）
SLOPE, YCR = 0.684, 13.92
# §4 Step 2–4
W_N   = {1: 555.9, 2: 846.4, 3: 765.6, 4: 578.6, 5: 227.7}
U_N   = {1: 0.0, 2: 17.5, 3: 40.7, 4: 50.8, 5: 21.8}
A_LAB = {1: 60, 2: 42, 3: 30, 4: 13, 5: 0}
SUM_R, SUM_D = 338.8 + 1183.3, 1560.8
FS_MAIN = SUM_R / SUM_D
def arc_y(x):
    for (x0, y0), (x1, y1) in zip(ARC, ARC[1:]):
        if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return ARC[-1][1]

def fig_slices():
    W, H = 1100, 700
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-5.5, 32.0), (-7.0, 20.5), 30, 30, 30, 30))
    crest = (YCR / SLOPE, YCR)
    xwt = Y_WT / SLOPE
    # 土體：水位以上／以下分色
    top = [(0, 0), crest, (25.8, YCR)]
    poly_soil = top + ARC[::-1]
    cv.polygon(poly_soil, "rgba(180,83,9,0.13)")
    # 水位以下區（切到圓弧）
    xr = next(x for x in [i / 100 for i in range(0, 2581)] if arc_y(x) >= Y_WT and x > 15)
    satpoly = [(0, 0), (xwt, Y_WT), (xr, Y_WT)] + [p for p in ARC[::-1] if p[0] <= xr]
    cv.polygon(satpoly, "rgba(29,78,216,0.13)")
    cv.poly([(-5.0, -0.32), (0, 0), crest, (31.5, YCR)], C["member"], 2.8)
    cv.poly(ARC, C["load"], 2.6, dash="10 6")
    cv.line((xwt, Y_WT), (31.5, Y_WT), C["deform"], 1.9, dash="8 5")
    cv.line((0, 0), (xwt, Y_WT), C["deform"], 4.5, dash="8 5", op=0.5)
    cv.text_px(cv.X(31.3), cv.Y(Y_WT) - 12, "水位 y = 4.77 m", 12, C["deform"], anchor="end", weight="700")
    # O 的半徑（通過 W_n 作用點）與 W_n
    for n in range(1, 6):
        px, py = WPT_PX[n]; p = ((px - PX0) / PXM, (py - PY0) / -PXM)
        cv.line(O2, (O2[0] + (p[0] - O2[0]) * 1.12, O2[1] + (p[1] - O2[1]) * 1.12), C["muted"], 1.1, dash="4 4")
        ang = math.degrees(math.atan2(p[0] - O2[0], O2[1] - p[1]))
        cv.arrow(p, (p[0], p[1] - 2.6), C["text"], 2.4, 9)
        cv.text_px(cv.X(p[0]) + 6, cv.Y(p[1] - 3.15), "W%d = %.1f" % (n, W_N[n]), 11.5, C["text"], anchor="start", weight="700")
        lab = "α5 = 0°（未標）" if n == 5 else "α%d = %d°（半徑角 %.0f°）" % (n, A_LAB[n], ang)
        cv.text_px(cv.X(p[0]) + 6, cv.Y(p[1] - 3.95), lab, 11, C["accent"], anchor="start")
    cv.dot(O2, 6, fill=C["member"])
    cv.text_px(cv.X(O2[0]) - 10, cv.Y(O2[1]), "O", 14, C["member"], anchor="end", weight="700")
    # 切片邊界與編號
    for x in X_B[1:5]:
        cv.line((x, min(SLOPE * x, YCR)), (x, arc_y(x)), C["member"], 1.8)
    for n in range(1, 6):
        i = 5 - n; xm = (X_B[i] + X_B[i + 1]) / 2
        ym = (min(SLOPE * xm, YCR) + max(arc_y(xm), Y_WT if n <= 2 else arc_y(xm))) / 2
        if n == 5: ym = 0.75
        if n == 4: ym = 2.9
        cv.text_px(cv.X(xm), cv.Y(ym), str(n), 16, C["text"], weight="700")
        if U_N[n] > 0:
            yb = arc_y(xm)
            cv.text_px(cv.X(xm), cv.Y(yb) - 14, "u = %.1f" % U_N[n], 10.5, C["deform"])
    cv.text_px(cv.X(23.6), cv.Y(arc_y(22.9)) - 4, "u1 = 0（底在水位上）", 10.5, C["deform"], anchor="start")
    # 寬度標註
    for i in range(5):
        cv.dim((X_B[i], -6.0), (X_B[i + 1], -6.0), "%.2f" % (X_B[i + 1] - X_B[i]), 0, C["dim"], 10.5, label_off=13)
    cv.text_px(cv.X(-0.3), cv.Y(-6.0), "b (m)", 11, C["muted"], anchor="end")
    cv.text_px(cv.X(7.0), cv.Y(19.7), "FS = (Σc'ΔL + ΣN'tanφ') / ΣW sinα = %.1f / %.1f = %.3f ≈ %.2f" % (SUM_R, SUM_D, FS_MAIN, FS_MAIN),
               13.5, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(7.0), cv.Y(18.5), "W (kN/m)、u (kPa)；淺藍＝水位以下 γsat = 20，淡橘＝水位以上 γ = 18", 11.5, C["muted"], anchor="start")
    return cv

compose([fig_slices()],
        title="SM-2021-4 普通切片法：量測幾何、W_n、u_n 與 α",
        sub="虛線半徑都由 O 通過 W_n 作用點，標註 α 即半徑與鉛直線夾角；所畫圓弧不是以 O 為圓心的正圓",
        note="攔錯用：α 照標註（改用圓弧弦角會得 FS ≈ 1.37）；切片 1 底在水位以上 u = 0；切片數據要依比例尺量圖，不是自編表。",
        path=os.path.join(OUT, "SM-2021-4-fig-2-slices.svg"))
