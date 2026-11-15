#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2024-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2024-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2024-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2024-4"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2024-4-problem.md §4）──
L = 12.0                       # #1 梁全長 12 m
H = 60.0                       # #2 斷面深 60 cm，形心在中央
E0, EM, EL = 25.0, -15.0, 0.0  # #3 偏心（cm，上為正）：固定端 +25、跨中 -15、輥支承端 0
VX = 0.035                     # 立面豎向比例（1 cm → 0.035 模型單位，放大示意）
a = (EL - 2 * EM + E0) / (L ** 2 / 2)   # #4 通過三點的單一拋物線（係數只由考卷三點決定）
b = (EM - E0 - a * 36) / 6
PW, PH = 1020, 380


def ecc(x):
    return a * x * x + b * x + E0


def panel_beam():
    cv = Canvas(PW, PH, sx=58, ox=150, oy=235)
    y0 = -H / 2 * VX
    _rect(cv, 0, y0, L, -y0)
    cv.line((-0.9, 0), (L + 0.9, 0), C["muted"], 1.3, dash="12 4 2 4")
    cv.text((L * 0.72, 0.28), "混凝土形心", 12.5, color=C["muted"])
    _curve(cv, lambda x: ecc(x) * VX, 0, L, TENDON, 2.4, dash="3 3")
    cv.text((L * 0.22, -0.82), "拋物線預力鋼腱形心", 12.5, color=TENDON)
    cv.support((0, 0), "fixed", ang=-90, size=70)
    cv.support((L, y0), "roller", size=15)
    cv.dim((-0.95, 0), (-0.95, E0 * VX), "25 cm", off=0, label_off=-34)
    cv.line((-1.1, E0 * VX), (0, E0 * VX), C["dim"], 1, dash="3 3")
    cv.dim((6, 0), (6, EM * VX), "15 cm", off=-6, label_off=-26)
    cv.dim((L, y0), (L, 0), "30 cm", off=40, label_off=30)
    cv.dim((L, 0), (L, -y0), "30 cm", off=40, label_off=30)
    cv.dim((0, y0), (6, y0), "6 m", off=50, label_off=14)
    cv.dim((0, y0), (L, y0), "12 m", off=92, label_off=14)
    cv.text((L / 2, -3.45), "左端固定、右端輥支承；斷面 40×60 cm（立面豎向放大示意）", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_beam()], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#5；鋼腱為通過三個給定偏心的單一拋物線",
                   note="預力 120 tf 沿全長視為定值；偏心由形心量起，固定端在上、跨中在下、輥支承端為 0")


FIGURES = [("1-problem", fig1_problem, "固定端／輥支承端對調；把跨中當拋物線頂點、分成兩段拋物線")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；數值由常數現算，檔尾對 §4 assert）══
L_S, P_S = 12.0, 120.0                      # m、tf（§1 本解記號）
E0_S, EM_S, EL_S = -25.0, 15.0, 0.0               # cm，下為正（題目正本 #4）
# §4 Step 1：三點擬合 e(x)=a x²+b x+c（x：m；e：cm）
C_S = E0_S
A_S = ((EL_S - C_S) - 2 * (EM_S - C_S)) / (144 - 72)
B_S = ((EM_S - C_S) - 36 * A_S) / 6
def e_s(x): return A_S * x * x + B_S * x + C_S
def de_s(x): return (2 * A_S * x + B_S) / 100.0
W_S = -P_S * 2 * A_S / 100.0                # §4 Step 2 向上 tf/m
VA_ANC, VB_ANC = P_S * de_s(0), P_S * abs(de_s(L_S))   # 錨碇垂直力（向下）
M_ANC = P_S * abs(E0_S) / 100.0               # 固定端錨碇彎矩 tf·m
INT_S = 1728 * A_S + 288 * B_S + 72 * C_S   # ∫e(L−x)dx（cm·m²）
RB_S = 3 * P_S / L_S ** 3 * INT_S / 100.0   # §4 Step 3 路徑一
RB_S2 = VB_ANC - 3 * W_S * L_S / 8          # 路徑二
MA_S = RB_S * L_S
def m2_s(x): return RB_S * (L_S - x)
def ec_s(x): return e_s(x) - m2_s(x) / P_S * 100
EM_CONC = (-24 * E0_S - 0 * EL_S) / 48          # 一致：保留兩端，中央 e_m（Lagrange 權重 24／48／0）
EC_OLD_MID = 37.5                           # 舊解 C 線跨中（§5 討論一，作攔錯標記）
HALF = 30.0
FW, FH = 760, 360
X0, SXm, SYc = 80, 50.0, 3.6                # px：x 原點、每 m、每 cm


def _px(x, e, yc):                          # 物理 (m, cm 下為正) → Canvas 座標（y 向上）
    return (X0 + SXm * x, yc - SYc * e)


def panel_eqload():
    cv = Canvas(FW, FH)
    cv.panel("① 鋼腱作用在混凝土上的等值載重（必須自平衡）")
    yb = 170
    cv.line((X0, yb), (X0 + SXm * L_S, yb), C["member"], 9, cap="butt")
    for i in range(13):
        x = X0 + SXm * L_S * i / 12
        cv.arrow((x, yb - 62), (x, yb - 8), C["deform"], 2.0, 8)
    cv.text((X0 + SXm * 6, yb - 80), f"w＝{W_S:.4f} tf/m 向上（合力 {W_S*L_S:.1f} tf）", 13.5, color=C["deform"], weight="700")
    cv.arrow((X0, yb + 96), (X0, yb + 10), C["load"], 3.4)
    cv.arrow((X0 + SXm * L_S, yb + 96), (X0 + SXm * L_S, yb + 10), C["load"], 3.4)
    cv.text((X0 + 10, yb + 70), f"A 錨碇垂直分力 {VA_ANC:.1f} tf↓", 13, color=C["load"], anchor="start", weight="700")
    cv.text((X0 + SXm * L_S - 10, yb + 70), f"B 錨碇垂直分力 {VB_ANC:.1f} tf↓", 13, color=C["load"], anchor="end", weight="700")
    cv.moment_arrow((X0 - 36, yb), r=20, ccw=False, color=C["accent"], span=270, start=135)
    cv.text((X0 + 12, yb + 34), f"錨碇彎矩 {M_ANC:.0f} tf·m", 12.5, color=C["accent"], anchor="start")
    cv.text_px(FW / 2, 300, f"ΣF：{W_S*L_S:.1f} − {VA_ANC:.1f} − {VB_ANC:.1f} ＝ 0　　ΣM_A：{W_S*L_S*6:.0f} − {VB_ANC*L_S:.0f} − {M_ANC:.0f} ＝ 0", 13.5, color=C["text"], weight="700")
    cv.text_px(FW / 2, 326, "漏掉兩端錨碇垂直分力，等值載重就不自平衡（舊解錯在此）", 12.5, color=C["muted"])
    return cv


def panel_secondary():
    cv = Canvas(FW, FH)
    cv.panel("② 束制產生的二次反力與二次彎矩 M_{2}")
    yb = 250
    xa, xb = X0, X0 + SXm * L_S
    cv.line((xa, yb), (xb, yb), C["member"], 7, cap="butt")
    cv.fixed_support((xa, yb), ang=90, size=26)
    cv.roller_support((xb, yb - 4), ang=0, size=14)
    cv.arrow((xb + 34, yb - 70), (xb + 34, yb - 6), C["sfd"], 3.2)
    cv.text((xb + 30, yb - 84), f"R_{{B}}＝{RB_S:.2f} tf↑", 13.5, color=C["sfd"], anchor="end", weight="700")
    cv.arrow((xa + 50, yb + 60), (xa + 50, yb + 6), C["sfd"], 3.2)
    cv.text((xa + 60, yb + 50), f"V_{{A}}＝{RB_S:.2f} tf↓", 13.5, color=C["sfd"], anchor="start", weight="700")
    cv.moment_arrow((xa, yb), r=34, ccw=False, color=C["sfd"], span=150, start=150)
    cv.text((xa + 200, yb + 50), f"M_{{A}}＝R_{{B}}L＝{MA_S:.1f} tf·m", 13.5, color=C["sfd"], anchor="start", weight="700")
    sc = 30.0                                   # px／tf·m，正彎矩畫在下方（受拉側）
    pts = [(xa + SXm * L_S * i / 24, yb - 16 - sc * m2_s(L_S * i / 24)) for i in range(25)]
    cv.polygon([(xa, yb - 16)] + pts + [(xb, yb - 16)], C["fill_m"], stroke=C["bmd"], w=2.2)
    cv.text((xa + 8, yb - 16 - sc * MA_S - 14), f"M_{{2}}＝+{MA_S:.1f}", 13, color=C["bmd"], anchor="start", weight="700")
    cv.text((xa + SXm * 6, yb - 16 - sc * m2_s(6) - 14), f"+{m2_s(6):.2f}（梁中央）", 12.5, color=C["bmd"])
    cv.text_px(FW / 2, 318, f"相容法 R_{{B}}＝3P∫e(L−x)dx／L^{{3}}＝{RB_S:.2f}；等值載重法 {VB_ANC:.1f} − 3wL/8＝{RB_S2:.2f}", 13, color=C["text"], weight="700")
    cv.text_px(FW / 2, 342, "M_{2} 在兩支承間呈線性；舊解套「3wL/8 向上」得 R_{B}＝4.5、M_{2}＝54（錯）", 12.5, color=C["muted"])
    return cv


def panel_cline():
    cv = Canvas(FW, FH)
    cv.panel("③ 鋼腱、C 線與一致鋼腱（豎向放大，單位 cm，下為正）")
    yc = 196
    xa, xb = X0, X0 + SXm * L_S
    cv.polygon([_px(0, -HALF, yc), _px(L_S, -HALF, yc), _px(L_S, HALF, yc), _px(0, HALF, yc)], "#EDF1F6", stroke=C["member"], w=1.8)
    cv.line(_px(0, 0, yc), _px(L_S, 0, yc), C["member2"], 1.2, dash="10 4 2 4")
    n = 60
    ten = [_px(L_S * i / n, e_s(L_S * i / n), yc) for i in range(n + 1)]
    cln = [_px(L_S * i / n, ec_s(L_S * i / n), yc) for i in range(n + 1)]
    aa = (EL_S - E0_S - 2 * (EM_CONC - E0_S)) / 72.0; bb = (EM_CONC - E0_S - 36 * aa) / 6
    con = [_px(L_S * i / n, aa * (L_S * i / n) ** 2 + bb * L_S * i / n + E0_S, yc) for i in range(n + 1)]
    cv.poly(ten, C["member"], 2.4, dash="6 4")
    cv.poly(con, C["bmd"], 2.0, dash="2 4")
    cv.poly(cln, C["load"], 3.0)
    for x, lab in ((0, f"{ec_s(0):.1f}"), (6, f"+{ec_s(6):.2f}")):
        cv.dot(_px(x, ec_s(x), yc), 4.5, fill=C["load"])
    cv.text((xa + 8, yc - SYc * HALF - 18), f"固定端：C 線 {ec_s(0):.1f}、鋼腱 {E0_S:.0f}（形心上方）", 12.5, color=C["load"], anchor="start", weight="700")
    cv.text((X0 + SXm * 6, yc - SYc * ec_s(6) - 16), f"C 線 +{ec_s(6):.2f}（鋼腱 +{EM_S:.0f}；一致鋼腱 +{EM_CONC:.1f}）", 12.5, color=C["load"], weight="700")
    cv.dot(_px(3, 0, yc), 4.5, fill=C["accent"])
    cv.text((X0 + SXm * 3 - 8, yc - 16), "x＝3 m 穿過形心", 12, color=C["accent"], anchor="end")
    cv.dot(_px(6, EC_OLD_MID, yc), 5, fill="#FFFFFF", stroke=C["member2"], w=2)
    cv.text((X0 + SXm * 6 + 12, yc - SYc * EC_OLD_MID), f"舊解 C 線 +{EC_OLD_MID}（超出半梁深 {HALF:.0f}，不可能）", 12, color=C["muted"], anchor="start")
    cv.text((xb + 6, yc + SYc * HALF), "上緣", 11.5, color=C["muted"], anchor="start")
    cv.line((450, 40), (480, 40), C["member"], 2.4, dash="6 4"); cv.text_px(486, 320, "鋼腱", 12, anchor="start")
    cv.line((530, 40), (560, 40), C["load"], 3.0); cv.text_px(566, 320, "C 線", 12, anchor="start")
    cv.line((610, 40), (640, 40), C["bmd"], 2.0, dash="2 4"); cv.text_px(646, 320, "一致鋼腱", 12, anchor="start")
    cv.text_px(250, 320, "C 線與鋼腱在輥支承端相交", 12, color=C["muted"])
    return cv


def fig2_cline():
    return compose([panel_eqload(), panel_secondary(), panel_cline()], cols=1,
                   title=f"{TAG} 圖 2　等值載重 → 二次反力 → C 線（一端固定、一端輥支）",
                   sub="單位 tf、tf·m、cm；P＝120 tf 沿全長定值；彎矩以下緣受拉為正",
                   note="攔：漏錨碇垂直分力；固定端錨碇彎矩當成會造成撓度；R_B 方向套反；C 線超出斷面不起疑")


def check_solution():
    for name, got, want, tol in [("a", A_S, -0.76389, 1e-4), ("b", B_S, 11.25, 1e-6), ("w", W_S, 1.8333, 1e-4),
                                 ("VA anc", VA_ANC, 13.5, 1e-6), ("VB anc", VB_ANC, 8.5, 1e-6), ("int", INT_S, 120.0, 1e-6),
                                 ("RB", RB_S, 0.25, 1e-9), ("RB2", RB_S2, 0.25, 1e-6), ("MA", MA_S, 3.0, 1e-9),
                                 ("eC0", ec_s(0), -27.5, 1e-9), ("eC6", ec_s(6), 13.75, 1e-9), ("eC3", ec_s(3), 0.0, 1e-9),
                                 ("em conc", EM_CONC, 12.5, 1e-9)]:
        assert abs(got - want) <= tol, (name, got, want)
    assert VA_ANC + VB_ANC == W_S * L_S or abs(VA_ANC + VB_ANC - W_S * L_S) < 1e-9
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-cline", fig2_cline, "漏錨碇垂直分力；R_B 方向套反；C 線超出斷面"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
