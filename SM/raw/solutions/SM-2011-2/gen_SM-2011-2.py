# -*- coding: utf-8 -*-
"""SM-2011-2 圖解。
fig-1-problem：題目附圖重繪，幾何只取自題目正本 SM-2011-2-problem.md §4 判讀清單（#1–#8），不含任何解題結果。
考卷附圖「未依比例尺繪」；本圖依判讀清單的數值按比例畫（4：3 斜率、B 層頂底面垂直於圍堰壁）。
fig-2-flownet：解題圖解（2026-11-15 階段 E，勘誤後），B 層流網與各點水頭，數值取自解析 §4。
用法：python gen_SM-2011-2.py [輸出資料夾]（預設本題 figs/）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))          # SM/raw/solutions/geo.py
from geo import *                                      # Canvas, C, compose, fit, wt_symbol
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

# ── 題目正本 §4 判讀清單（高程 m，參考位置 = 0）──────────
Z_B, Z_C, Z_D, Z_E, Z_G, Z_A = 0.0, 2.0, 3.0, 5.0, 6.0, 8.0   # #5、#6
SV, SH = 4.0, 3.0                       # #4 壁斜率 4（垂直）：3（水平）
GAP = 2.0                               # #4 兩壁垂直間距
L = math.hypot(SV, SH)
U = (-SH / L, SV / L)                   # 圍堰軸向（往上游＝左上）
N = (SV / L, SH / L)                    # 垂直於壁（#3：B 層頂、底面沿此方向）
def on_axis(z): t = z / U[1]; return (U[0] * t, z)
def wall_pt(z, side): p = on_axis(z); return (p[0] + side * N[0] * GAP / 2, p[1] + side * N[1] * GAP / 2)
def wall_at_y(side, y):                 # 壁線與水平線 y 的交點
    p0 = wall_pt(0, side); t = (y - p0[1]) / U[1]; return (p0[0] + U[0] * t, y)
def line_n(p, s): return (p[0] + N[0] * s, p[1] + N[1] * s)
XPZ = 4.6                               # 水壓計管位置（示意）

def clip(poly, inside, inter):
    out = []
    for i in range(len(poly)):
        a, b = poly[i - 1], poly[i]
        if inside(b):
            if not inside(a): out.append(inter(a, b))
            out.append(b)
        elif inside(a):
            out.append(inter(a, b))
    return out
def clip_box(poly, x1, y0, y1):
    def ix(a, b, x): r = (x - a[0]) / (b[0] - a[0]); return (x, a[1] + r * (b[1] - a[1]))
    def iy(a, b, y): r = (y - a[1]) / (b[1] - a[1]); return (a[0] + r * (b[0] - a[0]), y)
    poly = clip(poly, lambda p: p[1] <= y1, lambda a, b: iy(a, b, y1))
    poly = clip(poly, lambda p: p[1] >= y0, lambda a, b: iy(a, b, y0))
    poly = clip(poly, lambda p: p[0] <= x1, lambda a, b: ix(a, b, x1))
    return poly

def fig_problem():
    W, H = 900, 760
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-8.6, XPZ + 1.4), (-1.9, Z_A + 0.9), 30, 30, 20, 20))
    PB, PD = on_axis(Z_B), on_axis(Z_D)
    # 土層：b 線以下砂土、b–d 線之間 B 層、d 線以上（圍堰外）A 層——以沿 N 方向的長帶表示
    def band(p, s0, s1, h0, h1, fill):
        a0, a1 = line_n(p, s0), line_n(p, s1)
        pg = [(a0[0] + U[0] * h0, a0[1] + U[1] * h0), (a1[0] + U[0] * h0, a1[1] + U[1] * h0),
              (a1[0] + U[0] * h1, a1[1] + U[1] * h1), (a0[0] + U[0] * h1, a0[1] + U[1] * h1)]
        cv.polygon(clip_box(pg, XPZ - 0.1, -1.6, Z_G), fill)
    sB = (Z_D - Z_B) / U[1]             # b→d 沿軸距離
    band(PB, -3.0, 9.0, 0, sB, "rgba(180,83,9,0.22)")         # B 層
    band(PB, -3.0, 9.0, -2.4, 0, "rgba(180,83,9,0.10)")       # 砂土層
    # 圍堰內積水（d 線以上到地表，#1、#8）
    wl, wr = wall_pt(Z_D, -1), wall_pt(Z_D, +1)
    cv.polygon([wl, wr, wall_at_y(+1, Z_G), wall_at_y(-1, Z_G)], "rgba(29,78,216,0.16)")
    # B 層頂（開挖底面）與底（砂土層頂）
    cv.line(line_n(PD, -1.6), line_n(PD, (Z_G - Z_D) / N[1]), C["member"], 1.8)
    cv.line(line_n(PB, -1.6), line_n(PB, (XPZ - 0.1) / N[0]), C["member"], 1.8)
    # 地表
    cv.line((-8.4, Z_G), (XPZ - 0.3, Z_G), C["member"], 2.4)
    # 圍堰壁
    for s in (-1, +1):
        cv.line(wall_at_y(s, Z_G + 0.15), wall_at_y(s, -1.1), C["text"], 7, cap="butt")
    # 圍堰中心線與點位
    cv.line(on_axis(Z_E + 0.6), on_axis(Z_B), C["member2"], 1.0, dash="5 4")
    for z, lab in ((Z_E, "e"), (Z_D, "d"), (Z_C, "c"), (Z_B, "b")):
        p = on_axis(z); cv.dot(p, 6, fill=C["text"])
        cv.text((p[0] + 0.35, p[1] + 0.25), lab, 14.5, C["text"], anchor="start", weight="700")
    wt_symbol(cv, on_axis(Z_G)[0] + 0.2, Z_G + 0.09 * 2.4, C["deform"], 0.09)
    cv.text((on_axis(Z_G)[0] + 0.55, Z_G + 0.35), "圍堰內水位（地表）", 12, C["deform"], anchor="start", weight="700")
    # 交點 m、n
    for s, lab in ((-1, "m"), (+1, "n")):
        p = wall_pt(0, s)
        cv.text((p[0] + 0.15 * s + (0.25 if s > 0 else -0.45), p[1] - 0.35), lab, 13.5, C["text"], weight="700")
    # 水壓計：由 b 水平接到右側直立管，水位 a
    cv.line(PB, (XPZ, 0), C["member2"], 3.0)
    for dx in (-0.1, 0.1):
        cv.line((XPZ + dx, 0), (XPZ + dx, Z_A + 0.6), C["member"], 1.6)
    cv.polygon([(XPZ - 0.1, 0), (XPZ + 0.1, 0), (XPZ + 0.1, Z_A), (XPZ - 0.1, Z_A)], "rgba(29,78,216,0.25)")
    cv.dot((XPZ, Z_A), 5.5, fill=C["text"]); cv.text((XPZ - 0.3, Z_A + 0.05), "a", 14.5, C["text"], anchor="end", weight="700")
    cv.text((XPZ - 0.3, Z_A - 0.8), "水壓計", 12, C["muted"], anchor="end")
    cv.dim((XPZ + 0.6, 0), (XPZ + 0.6, Z_A), "8 m", 0, C["dim"], 12.5, label_off=22)
    # 參考位置
    cv.line((-8.4, 0), (XPZ, 0), C["dim"], 1.0, dash="6 4")
    cv.text((-8.3, -0.4), "參考位置（reference level）", 11.5, C["muted"], anchor="start")
    # 左側高程尺寸線（#5）
    for x, z, lab in ((-8.0, Z_G, "6 m"), (-7.0, Z_E, "5 m"), (-6.0, Z_D, "3 m"), (-5.0, Z_C, "2 m")):
        cv.dim((x, 0), (x, z), lab, 0, C["dim"], 12, label_off=-18)
        cv.line((x, z), (on_axis(z)[0] if z != Z_G else wall_at_y(-1, Z_G)[0], z), C["dim"], 0.8, dash="2 3")
    # 斜率三角形與 53°（#4）
    q = wall_pt(Z_E - 0.6, -1)
    cv.poly([(q[0] - 0.75, q[1] + 1.0), (q[0] - 0.75, q[1]), (q[0], q[1])], C["muted"], 1.3)
    cv.text((q[0] - 1.0, q[1] + 0.5), "4", 12, C["muted"], anchor="end")
    cv.text((q[0] - 0.38, q[1] - 0.3), "3", 12, C["muted"])
    p0 = wall_at_y(-1, 0)
    a0 = math.degrees(math.atan2(U[1], U[0]))          # 壁方向（約 127°）
    arcp = [(p0[0] + 0.7 * math.cos(math.radians(a0 + (180 - a0) * k / 20)),
             p0[1] + 0.7 * math.sin(math.radians(a0 + (180 - a0) * k / 20))) for k in range(21)]
    cv.poly(arcp, C["muted"], 1.3)
    cv.text((p0[0] - 1.25, p0[1] + 0.3), "53°", 12, C["muted"], anchor="end")
    # 壁間距 2 m（垂直於壁）
    m = on_axis(4.1)
    cv.dim((m[0] - N[0], m[1] - N[1]), (m[0] + N[0], m[1] + N[1]), "2 m", 0, C["dim"], 12, label_off=14)
    # 標籤
    cv.text((0.2, 3.6), "開挖底面 2 m × 2 m", 11.5, C["text"], anchor="start")
    cv.arrow((0.1, 3.55), (PD[0] + 0.3, PD[1] + 0.05), C["muted"], 1.3, 7)
    cv.text((-1.7, 5.4), "不透水 A 土層", 12.5, C["text"], anchor="start", weight="700")
    cv.text((0.0, 2.3), "透水 B 土層", 12.5, C["text"], anchor="start", weight="700")
    cv.text((2.4, -0.55), "砂土層", 12, C["text"], anchor="start")
    cv.text((-6.4, 6.4), "不透水圍堰", 12.5, C["text"], anchor="start", weight="700")
    cv.text((2.2, 6.3), "地表", 12, C["muted"], anchor="start")
    return cv

compose([fig_problem()],
        title="SM-2011-2 題目附圖重繪",
        sub="依題目正本判讀清單（按比例）；開挖底面在 d（3 m）、圍堰內積水到地表（6 m），B 層頂底面垂直於圍堰壁",
        note="攔錯用：e（5 m）在水中、不是開挖底面；B 層介於 d、b 兩條斜線之間，2 m × 2 m 是垂直於圍堰軸的斷面。",
        path=os.path.join(OUT, "SM-2011-2-fig-1-problem.svg"))


# ══════ fig-2：B 層流網與各點水頭（解題圖解，2026-11-15 階段 E）══════
# ── 由 SM-2011-2 §4 解得（勘誤後）──
H_B, H_D = Z_A, Z_G                     # b：水壓計水位 8 m；d：圍堰內積水面 6 m
L_BD = (Z_D - Z_B) / U[1]               # 3.75 m（沿圍堰軸）
I_BD = (H_B - H_D) / L_BD               # 0.533
def h_at(s): return H_B - I_BD * s      # B 層內沿軸距 b 為 s 處的總水頭
PTS = [("a", Z_A, H_B), ("b", Z_B, H_B), ("c", Z_C, h_at(Z_C / U[1])), ("d", Z_D, H_D), ("e", Z_E, H_D)]

def fig_flownet():
    W, H = 640, 660
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-6.2, 3.0), (-0.9, Z_G + 1.0), 20, 20, 40, 20))
    PB, PD = on_axis(Z_B), on_axis(Z_D)
    def P(s, n): return (PB[0] + U[0] * s + N[0] * n, PB[1] + U[1] * s + N[1] * n)
    cv.polygon([P(0, -1), P(0, 1), P(L_BD, 1), P(L_BD, -1)], "rgba(180,83,9,0.22)")           # B 層（圍堰內）
    cv.polygon([wall_pt(Z_D, -1), wall_pt(Z_D, +1), wall_at_y(+1, Z_G), wall_at_y(-1, Z_G)], "rgba(29,78,216,0.16)")
    cv.polygon([P(-0.9, -1), P(-0.9, 1), P(0, 1), P(0, -1)], "rgba(180,83,9,0.10)")           # 砂土層
    for s in (-1, +1):
        cv.line(wall_at_y(s, Z_G + 0.1), wall_at_y(s, -0.7), C["text"], 6, cap="butt")
    cv.line(P(0, 0), P(L_BD, 0), C["deform"], 1.8)                                               # 中間流線
    for n in (-1, 0, 1):
        cv.arrow(P(1.6, n * 0.92), P(2.2, n * 0.92), C["deform"], 1.8, 7) if n == 0 else None
    k = 0
    s = 0.0
    while s <= L_BD + 1e-9:                                                                      # 等勢線：沿軸每 1 m
        cv.line(P(s, -1), P(s, 1), C["load"], 1.6)
        q = P(s, 1)
        tag_px(cv, cv.X(q[0]) + 10, cv.Y(q[1]) + 2, "h = %.3f" % h_at(s), 11.5, C["load"], anchor="start", weight="700")
        s = s + 1.0 if s + 1.0 <= L_BD + 1e-9 else (L_BD if s < L_BD - 1e-9 else L_BD + 1)
    for lab, z, h in PTS[1:]:
        p = on_axis(z); cv.dot(p, 5.5, fill=C["text"])
        cv.text((p[0] - 0.3, p[1] + 0.1), lab, 14, C["text"], anchor="end", weight="700")
    wt_symbol(cv, on_axis(Z_G)[0] + 0.1, Z_G + 0.09 * 2.4, C["deform"], 0.09)
    cv.text((on_axis(Z_G)[0] + 0.5, Z_G + 0.3), "積水面 h = 6 m", 12, C["deform"], anchor="start", weight="700")
    cv.text((-5.9, -0.55), "砂土層：h = 8 m（水壓計）", 12, C["muted"], anchor="start")
    cv.text((-6.0, 2.0), "B 層內：一維平行流", 12.5, C["text"], anchor="start", weight="700")
    cv.text((-6.0, 1.55), "Nf = 2、Nd = 3.75（1 m 方格）", 12, C["text"], anchor="start")
    cv.text((-6.0, 1.1), "i = 2 / 3.75 = %.3f" % I_BD, 12, C["text"], anchor="start")
    return cv

def fig_heads():
    W, H = 640, 660
    cv = Canvas(W, H, bg="#FFFFFF", **fit(W, H, (-0.9, 5.4), (-1.3, 9.6), 50, 30, 40, 30))
    for v in range(0, 10, 2):
        cv.line((-0.3, v), (5.0, v), C["border"], 1.0)
        cv.text_px(cv.X(-0.3) - 8, cv.Y(v), "%d" % v, 12, C["muted"], anchor="end")
    cv.text_px(cv.X(-0.3) - 30, cv.Y(4.5), "m", 12.5, C["text"], anchor="end")
    cv.line((-0.3, 0), (5.0, 0), C["muted"], 1.8)
    for hh, lab in ((H_B, "h = 8（水壓計）"), (H_D, "h = 6（積水面）")):
        cv.line((-0.3, hh), (5.0, hh), C["deform"], 1.2, dash="6 4")
    for i, (lab, z, h) in enumerate(PTS):
        x = 0.35 + i * 1.0; bw = 0.5
        hp = h - z
        cv.polygon([(x - bw / 2, 0), (x + bw / 2, 0), (x + bw / 2, z), (x - bw / 2, z)], "rgba(138,148,166,0.45)")
        if hp > 1e-9:
            cv.polygon([(x - bw / 2, z), (x + bw / 2, z), (x + bw / 2, h), (x - bw / 2, h)], "rgba(29,78,216,0.55)")
        cv.text((x, -0.55), lab, 14, C["text"], weight="700")
        cv.text((x, h + 0.32), "%g" % round(h, 3), 12, C["deform"], weight="700")
        if hp > 0.6:
            cv.text((x, z + hp / 2), "%g" % round(hp, 3), 11.5, "#FFFFFF", weight="700")
    cv.text_px(cv.X(-0.3), cv.Y(-1.05), "灰：高度水頭 Z　藍：壓力水頭 P　柱頂：總水頭 h", 12, C["muted"], anchor="start")
    return cv

compose([fig_flownet(), fig_heads()],
        title="圖 2　B 層流網與各點水頭：邊界水頭 b = 8 m、d = 6 m（圍堰內積水）",
        sub="B 層頂底面垂直於圍堰壁 → 流線平行壁、等勢線垂直壁的正方形網；斷面 2 m × 2 m 即垂直於流向",
        note="攔錯用：e 在積水中、壓力水頭 1 m 不是 0；開挖面總水頭取積水面 6 m，不是開挖面高程。",
        path=os.path.join(OUT, "SM-2011-2-fig-2-flownet.svg"))
