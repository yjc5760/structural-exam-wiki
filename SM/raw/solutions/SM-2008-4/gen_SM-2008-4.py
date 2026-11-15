# -*- coding: utf-8 -*-
"""SM-2008-4 圖解。
fig-1-problem：題目附圖（圖三）重繪，幾何只取自題目正本 SM-2008-4-problem.md §4 判讀清單（#1–#11），不含任何解題結果。
用法：python gen_SM-2008-4.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
wt = lambda cv, x, y, s: wt_symbol(cv, x, y + 2.4 * s, C["deform"], s)   # ▽ 尖端落在水面線上

# ── 題目正本 §4 判讀清單 ─────────────────────────────
H_B   = 7.5            # #1 B 高於 A
A_AC  = 40.0           # #2 滑動面 AC 傾角
A_AB  = A_AC + 30.0    # #3 坡面 AB 傾角 70°
A_BC  = A_AC - 35.0    # #4 坡頂面 BC 傾角 5°
r = math.radians
A = (0.0, 0.0)
B = (H_B / math.tan(r(A_AB)), H_B)
# C = AC 線與 BC 線交點（幾何由 #2–#4 決定）
tAC, tBC = math.tan(r(A_AC)), math.tan(r(A_BC))
xC = (B[1] - tBC * B[0]) / (tAC - tBC)
C_ = (xC, tAC * xC)

def fig_problem():
    W, H = 900, 500
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-6.0, C_[0] + 6.5), (-3.0, C_[1] + 2.5), 40, 40, 40, 40))
    xe = C_[0] + 5.0
    top_end = (xe, C_[1] + tBC * (xe - C_[0]))         # #6 BC 延伸過 C
    cv.polygon([A, B, C_], "rgba(180,83,9,0.16)", C["member"], 0)
    cv.poly([(-5.5, 0), A, B, C_, top_end], C["member"], 2.6)
    for k in range(6):                                  # #7 地面符號
        x = -5.2 + k * 0.7
        cv.line((x, 0), (x - 0.35, -0.4), C["member"], 1.3)
    # 泥岩夾層（#8）：沿 AC 畫細斜線帶
    n = (-math.sin(r(A_AC)), math.cos(r(A_AC)))
    tb = 0.18
    band = [A, C_, (C_[0] - n[0] * tb, C_[1] - n[1] * tb), (A[0] - n[0] * tb, A[1] - n[1] * tb)]
    cv.polygon(band, "rgba(63,74,90,0.55)", C["member"], 1.2)
    cv.line((A[0] + 1.0, 0), (6.0, 0), C["member"], 1.6)
    # 地錨（#11）：錨頭在 BC 上近 B，垂直 AC 穿過夾層
    s0 = 0.9
    h0 = (B[0] + s0 * math.cos(r(A_BC)), B[1] + s0 * math.sin(r(A_BC)))
    d = (math.sin(r(A_AC)), -math.cos(r(A_AC)))          # 垂直 AC 往下
    L1 = 9.0
    p1 = (h0[0] + d[0] * L1, h0[1] + d[1] * L1)
    cv.line(h0, p1, C["load"], 2.0)
    cv.line(p1, (p1[0] + d[0] * 3.0, p1[1] + d[1] * 3.0), C["load"], 7.0)
    cv.text_px(cv.X(p1[0] + 1.6), cv.Y(p1[1] - 0.3), "地錨（僅㈡）", 12.5, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(p1[0] + 1.6), cv.Y(p1[1] - 1.1), "垂直 AC，間距 2 m", 12, C["load"], anchor="start")
    # 角度標註
    cv.text_px(cv.X(2.6), cv.Y(0.75), "40°", 13, C["dim"], weight="700")
    cv.text_px(cv.X(1.45), cv.Y(2.6), "30°", 13, C["dim"], weight="700")
    cv.text_px(cv.X(C_[0] - 2.2), cv.Y(C_[1] - 0.75), "35°", 13, C["dim"], weight="700")
    cv.text_px(cv.X(B[0] + 4.0), cv.Y(B[1] + 1.0), "坡頂面 5°", 12, C["muted"])
    # 點名
    cv.text_px(cv.X(A[0] - 0.5), cv.Y(A[1] + 0.5), "A", 15, C["text"], weight="700", anchor="end")
    cv.text_px(cv.X(B[0] - 0.4), cv.Y(B[1] + 0.4), "B", 15, C["text"], weight="700", anchor="end")
    cv.text_px(cv.X(C_[0]), cv.Y(C_[1] + 0.8), "C", 15, C["text"], weight="700")
    cv.text_px(cv.X(B[0] + 0.2), cv.Y(B[1] - 2.6), "砂岩", 13, C["text"], weight="700")
    cv.text_px(cv.X(B[0] + 0.2), cv.Y(B[1] - 3.4), "γ = 20 kN/m³", 12, C["text"])
    cv.text_px(cv.X(9.5), cv.Y(4.5), "泥岩夾層  c = 10 kN/m²，φ = 28°", 12.5, C["text"], anchor="start", weight="700")
    cv.arrow((9.4, 4.4), (5.9, 5.1), C["muted"], 1.4, 7)
    cv.arrow((-2.4, 4.2), (-4.0, 4.2), C["load"], 2.6, 9)
    cv.math_px(cv.X(-2.2), cv.Y(4.2), "K_{h}W", 13, C["load"], anchor="start", weight="700")
    cv.text_px(cv.X(-3.2), cv.Y(3.4), "Kh = 0.2（取向坡外）", 11.5, C["load"])
    # 7.5 m（#1）
    xd = -4.8
    cv.dim((xd, 0), (xd, H_B), "7.5 m", 0, C["dim"], 12.5, label_off=-26)
    cv.line((xd - 0.3, H_B), (B[0], H_B), C["dim"], 0.9, dash="2 3")
    return cv

compose([fig_problem()],
        title="SM-2008-4 題目附圖（圖三）重繪",
        sub="依題目正本判讀清單；角度依標註（考卷圖不按比例），7.5 m 為 B 高於 A",
        note="攔錯用：AB 傾角 = 40° + 30° = 70°，BC 傾角 = 40° − 35° = 5°；不可照考卷圖量角度。",
        path=os.path.join(OUT, "SM-2008-4-fig-1-problem.svg"))


# ═══ fig-2-forces：解題圖解（階段 E，2026-11-15）══════════════════════
# 數值取自解析 §4 Step 1–6（盲解一致，2026-11-15）。
W_ = 503.24; FH = 100.65; TD = 400.58; NN = 320.81; CL = 126.10; NTAN = 170.58; FS1 = 0.74; P_ANC = 346.09; T_ANC = 692.18
L_AC = 12.610
def fig_forces():
    W, H = 1040, 470
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-9.0, C_[0] + 14.0), (-2.6, C_[1] + 3.5), 30, 30, 20, 20))
    cv.polygon([A, B, C_], "rgba(180,83,9,0.16)", C["member"], 2.4)
    cv.line((-8.5, 0), A, C["member"], 2.2)
    G = ((A[0] + B[0] + C_[0]) / 3, (A[1] + B[1] + C_[1]) / 3)
    k = 3.2 / 500.0                                   # kN/m → m（繪圖比例）
    up = (math.cos(r(A_AC)), math.sin(r(A_AC)))       # 沿 AC 往上
    nn = (-math.sin(r(A_AC)), math.cos(r(A_AC)))      # AC 外法線（指向塊體）
    cv.dot(G, 4, fill=C["member"])
    cv.arrow(G, (G[0], G[1] - W_ * k), C["text"], 3.0)
    cv.text_px(cv.X(G[0]) + 6, cv.Y(G[1] - W_ * k) + 4, "W = %.1f" % W_, 12, C["text"], anchor="start", weight="700")
    cv.arrow(G, (G[0] - FH * k, G[1]), C["load"], 3.0)
    cv.text_px(cv.X(G[0] - FH * k) - 6, cv.Y(G[1]) - 12, "KhW = %.1f（向坡外）" % FH, 12, C["load"], anchor="end", weight="700")
    # AC 上的分量：畫在 AC 外側（平行偏移），驅動與抗滑分開兩條
    def on_ac(s, off):
        return (A[0] + (C_[0] - A[0]) * s - nn[0] * off, A[1] + (C_[1] - A[1]) * s - nn[1] * off)
    cv.line(on_ac(0.0, 0), on_ac(1.0, 0), C["member"], 2.4)
    a0 = on_ac(0.97, 0.9)
    a1 = (a0[0] - up[0] * TD * k, a0[1] - up[1] * TD * k)
    cv.arrow(a0, a1, C["load"], 3.2)
    cv.text_px(cv.X(a0[0]) + 8, cv.Y(a0[1]) + 4, "驅動 = W sin40° + KhW cos40° = %.1f" % TD, 12, C["load"], anchor="start", weight="700")
    R_ = CL + NTAN
    b0 = on_ac(0.22, 2.2)
    b1 = (b0[0] + up[0] * R_ * k, b0[1] + up[1] * R_ * k)
    cv.arrow(b0, b1, C["bmd"], 3.2)
    cv.text_px(cv.X(b0[0]) - 8, cv.Y(b0[1]) + 10, "抗滑 = cL + N tan28° = %.1f + %.1f = %.1f" % (CL, NTAN, R_), 12, C["bmd"], anchor="end", weight="700")
    p0 = on_ac(0.62, 0)
    q = (p0[0] - nn[0] * NN * k, p0[1] - nn[1] * NN * k)
    cv.arrow(q, p0, C["deform"], 3.2)
    cv.text_px(cv.X(q[0]) + 8, cv.Y(q[1]) + 8, "N = W cos40° − KhW sin40° = %.1f" % NN, 12, C["deform"], anchor="start", weight="700")
    # 地錨（㈡）：垂直 AC，壓向夾層
    h0 = (B[0] + 2.2 * math.cos(r(A_BC)), B[1] + 2.2 * math.sin(r(A_BC)))
    tip = (h0[0] + nn[0] * 0.0, h0[1])
    d = (math.sin(r(A_AC)), -math.cos(r(A_AC)))
    cv.arrow((h0[0] - d[0] * 3.0, h0[1] - d[1] * 3.0), h0, C["accent"], 3.0)
    cv.text_px(cv.X(h0[0] - d[0] * 3.0) - 6, cv.Y(h0[1] - d[1] * 3.0) - 10, "㈡ 地錨 T/2 = %.1f kN/m（垂直 AC）" % P_ANC, 12, C["accent"], anchor="end", weight="700")
    cv.text_px(cv.X(A[0] - 0.4), cv.Y(A[1] + 0.4), "A", 14, C["text"], weight="700", anchor="end")
    cv.text_px(cv.X(B[0] - 0.3), cv.Y(B[1] + 0.4), "B", 14, C["text"], weight="700", anchor="end")
    cv.text_px(cv.X(C_[0]), cv.Y(C_[1] - 0.7), "C", 14, C["text"], weight="700", anchor="start")
    cv.text_px(cv.X(C_[0] + 1.5), cv.Y(C_[1] + 2.4), "㈠ FS = %.1f / %.1f = %.2f" % (R_, TD, FS1), 13.5, C["text"], anchor="start", weight="700")
    cv.text_px(cv.X(C_[0] + 1.5), cv.Y(C_[1] + 1.4), "㈡ 1.2 × %.1f = %.1f + (T/2) tan28°" % (TD, R_), 12.5, C["text"], anchor="start")
    cv.text_px(cv.X(C_[0] + 1.5), cv.Y(C_[1] + 0.5), "→ T = %.0f kN／支（間距 2 m）" % T_ANC, 12.5, C["accent"], anchor="start", weight="700")
    cv.text_px(cv.X(C_[0] + 1.5), cv.Y(C_[1] - 0.4), "AC = %.2f m，單位 kN/m" % L_AC, 11.5, C["muted"], anchor="start")
    return cv

compose([fig_forces()],
        title="SM-2008-4 平面滑動：重量與地震力沿滑動面 AC 分解",
        sub="Kh 取向坡外：增加驅動、減少正向力；地錨垂直 AC 只增加正向力",
        note="攔錯用：KhW sin40° 要從 N 扣掉（不是加）；每公尺所需 346 kN 乘間距 2 m 才是每支荷重 692 kN。",
        path=os.path.join(OUT, "SM-2008-4-fig-2-forces.svg"))
