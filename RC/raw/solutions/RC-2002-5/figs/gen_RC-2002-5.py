#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2002-5 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2002-5-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2002-5.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2002-5"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2002-5-problem.md §4）──
# 只用考卷數值：分段水平長度、R、角度；鋼腱高程考卷未標，由「直線＋圓弧」幾何與 A 點在梁深中央推得，只作示意
H = 1.20                        # #2 梁深 0.60＋0.60 m
XA, XB, XC, XD, XE = 0.0, 5.35, 5.35 + 7.60, 5.35 + 7.60 + 5.35, 21.50   # #3–#6
R1, R2 = 45.0, 30.0             # #4、#6
TH1, TH2 = 0.169, 0.107         # #4 B→C 角變、#6 D→E 角變（E 點切線水平）
SPAN = 21.50                    # #1 兩跨各 21.50 m
VX = 4.0                        # 豎向放大 4 倍示意
PW, PH = 1200, 420


def tendon_left():
    s_cd = TH2                  # C→D 直線斜率（E 點水平，弧 D→E 轉 0.107）
    s_ab = s_cd - TH1           # A→B 直線斜率
    pts, y = [], H / 2
    for i in range(21):
        x = XB * i / 20; pts.append((x, y + s_ab * x))
    yb = y + s_ab * XB
    for i in range(1, 41):      # B→C 圓弧（曲率 1/R1，斜率線性變化）
        x = XB + (XC - XB) * i / 40; dx = x - XB
        pts.append((x, yb + s_ab * dx + dx * dx / (2 * R1)))
    yc = pts[-1][1]
    for i in range(1, 21):
        x = XC + (XD - XC) * i / 20; pts.append((x, yc + s_cd * (x - XC)))
    yd = pts[-1][1]
    for i in range(1, 21):      # D→E 圓弧（向下凹，曲率 -1/R2）
        x = XD + (XE - XD) * i / 20; dx = x - XD
        pts.append((x, yd + s_cd * dx - dx * dx / (2 * R2)))
    return pts


def panel_elev():
    cv = Canvas(PW, PH, sx=24.5, ox=100, oy=180)
    P = lambda p: (p[0], p[1] * VX)
    _rect(cv, *P((0, 0)), *P((2 * SPAN, H)))
    L = tendon_left()
    R_ = [(2 * SPAN - x, y) for x, y in reversed(L)]
    cv.poly([P(p) for p in L], TENDON, 2.6, dash="10 5")
    cv.poly([P(p) for p in R_], TENDON, 2.6, dash="10 5")
    for xe in (0, 2 * SPAN):
        cv.polygon([P((xe - 0.12, 0.52)), P((xe + 0.12, 0.52)), P((xe + 0.12, 0.68)), P((xe - 0.12, 0.68))], C["member"])
    for x in (0, SPAN, 2 * SPAN):
        cv.support(P((x, 0)), "pin", size=12)
    yy = dict(L)
    for x, n, dy in ((XA, "A", 0.10), (XB, "B", 0.12), (XC, "C", 0.12), (XD, "D", 0.12), (XE, "E", -0.16)):
        y = min(L, key=lambda p: abs(p[0] - x))[1]
        cv.dot(P((x, y)), 4.2, fill=C["text"])
        cv.text(P((x + (0.5 if n == "A" else -0.2), y + dy)), n, 15, weight="700", dy=-6)
    cv.text(P(((XB + XC) / 2, -0.17)), "R = 45 m，角變 0.169 rad（B→C）", 12.5, color=TENDON)
    cv.text(P((XE + 1.0, 1.36)), "R = 30 m，角變 0.107 rad（D→E）", 12.5, color=TENDON, anchor="start")
    cv.text(P(((XA + XB) / 2, 0.80)), "直線", 12, color=C["muted"])
    cv.text(P(((XC + XD) / 2, 0.30)), "直線", 12, color=C["muted"])
    cv.dim(P((0, 0.6)), P((0, H)), "0.60 m", off=-6, label_off=-32)
    cv.dim(P((0, 0)), P((0, 0.6)), "0.60 m", off=-6, label_off=-32)
    for a, b, t in ((XA, XB, "5.35 m"), (XB, XB + 3.8, "3.80 m"), (XB + 3.8, XC, "3.80 m"), (XC, XD, "5.35 m"), (XD, XE, "3.2 m")):
        cv.dim(P((a, 0)), P((b, 0)), t, off=46, label_off=15, size=12.5)
    cv.dim(P((SPAN, 0)), P((2 * SPAN, 0)), "21.50 m", off=46, label_off=15)
    cv.dim(P((0, 0)), P((SPAN, 0)), "21.50 m", off=86, label_off=15)
    cv.text((SPAN, -4.6), "後拉連續梁，鋼腱由兩端拉（右半與左半對稱）；E 在中間支承上方；鋼腱高程考卷未標，依直線＋圓弧幾何示意；豎向放大 4 倍", 12, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_elev()], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#8；A→B 直線、B→C 圓弧、C→D 直線、D→E 圓弧",
                   note="μ = 0.4、k = 0.0026/m；45 × 0.169 ≈ 7.60 m、30 × 0.107 ≈ 3.2 m 與分段長度相符")


FIGURES = [("1-problem", fig1_problem, "A→B 讀成圓弧、C→D 併入圓弧、D 當中間支承")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；數值由常數現算，檔尾對 §4 assert）══
Q5_MU, Q5_K = 0.4, 0.0026                   # 題目
Q5_SEG = [("A→B 直線", 5.35, 0.0), ("B→C 圓弧 R＝45 m", 7.60, 0.169),
          ("C→D 直線", 5.35, 0.0), ("D→E 圓弧 R＝30 m", 3.20, 0.107)]   # 題目正本 #3–#7
Q5_PTS = ["A", "B", "C", "D", "E"]
Q5_X = [0.0]; Q5_AL = [0.0]
for _n, _l, _a in Q5_SEG:
    Q5_X.append(Q5_X[-1] + _l); Q5_AL.append(Q5_AL[-1] + _a)
Q5_F = [math.exp(-(Q5_MU * al + Q5_K * x)) for x, al in zip(Q5_X, Q5_AL)]
Q5_OLD = [1.0, 0.940, 0.900, 0.850, 0.808]   # 舊解（§5 對照）
Q5_W, Q5_H = 760, 330
Q5_X0, Q5_SX = 80, 600 / Q5_X[-1]


def _q5_al(x):                              # 沿線累積角變（圓弧內線性增加）
    for i, (_n, l, a) in enumerate(Q5_SEG):
        if x <= Q5_X[i + 1] + 1e-9:
            return Q5_AL[i] + a * (x - Q5_X[i]) / l
    return Q5_AL[-1]


def panel_q5_alpha():
    cv = Canvas(Q5_W, Q5_H)
    cv.panel("① 線形與累積角變 Σα（只有圓弧段增加）")
    yb = 206
    for i, (nm, l, a) in enumerate(Q5_SEG):
        x0, x1 = Q5_X0 + Q5_SX * Q5_X[i], Q5_X0 + Q5_SX * Q5_X[i + 1]
        col = C["load"] if a > 0 else C["member2"]
        cv.line((x0, yb), (x1, yb), col, 10, cap="butt")
        cv.text(((x0 + x1) / 2, yb + 22), nm, 12, color=col, weight="700")
        cv.text(((x0 + x1) / 2, yb - 20), f"{l:.2f} m" + (f"，α＝{a}" if a else "，α＝0"), 11.5, color=C["muted"])
    for i, p in enumerate(Q5_PTS):
        cv.dot((Q5_X0 + Q5_SX * Q5_X[i], yb), 5, fill=C["member"])
        cv.text((Q5_X0 + Q5_SX * Q5_X[i], yb + 44), p, 13.5, weight="700")
    ys, sc = 70, 300                        # Σα 軸：0 在 ys，每 rad 300 px
    cv.line((Q5_X0, ys), (Q5_X0 + 600, ys), C["muted"], 1.2)
    pts = [(Q5_X0 + Q5_SX * Q5_X[-1] * i / 200, ys + sc * _q5_al(Q5_X[-1] * i / 200)) for i in range(201)]
    cv.poly(pts, C["deform"], 2.6)
    for i in range(1, 5):
        cv.dot((Q5_X0 + Q5_SX * Q5_X[i], ys + sc * Q5_AL[i]), 4, fill=C["deform"])
        cv.text((Q5_X0 + Q5_SX * Q5_X[i] + 6, ys + sc * Q5_AL[i] + (-14 if i in (1, 3) else 12)), f"{Q5_AL[i]:.3f}", 12, color=C["deform"], anchor="start", weight="700")
    cv.text((Q5_X0 - 8, ys + 40), "Σα", 13, color=C["deform"], anchor="end", weight="700")
    cv.text_px(Q5_W / 2, 312, "A→B、C→D 是切線直線段：不增加角變（舊解把 A→B 當圓弧多算 0.119 rad）", 12.5, color=C["muted"])
    return cv


def panel_q5_force():
    cv = Canvas(Q5_W, Q5_H)
    cv.panel("② 張力沿線分布 F/F_{1}＝exp[−(μΣα＋kx)]")
    y0, sc, fmin = 50, 900, 0.79           # F/F1＝fmin 落在 y0
    def Y(f): return y0 + sc * (f - fmin)
    for f in (0.80, 0.85, 0.90, 0.95, 1.00):
        cv.line((Q5_X0, Y(f)), (Q5_X0 + 600, Y(f)), C["border"], 1)
        cv.text((Q5_X0 - 8, Y(f)), f"{f:.2f}", 11.5, color=C["muted"], anchor="end")
    xs = [Q5_X[-1] * i / 200 for i in range(201)]
    cv.poly([(Q5_X0 + Q5_SX * x, Y(math.exp(-(Q5_MU * _q5_al(x) + Q5_K * x)))) for x in xs], C["tension"], 3)
    cv.poly([(Q5_X0 + Q5_SX * x, Y(f)) for x, f in zip(Q5_X, Q5_OLD)], C["member2"], 1.6, dash="5 4")
    for i, p in enumerate(Q5_PTS):
        X = Q5_X0 + Q5_SX * Q5_X[i]
        cv.dot((X, Y(Q5_F[i])), 5, fill=C["tension"])
        cv.text((X + 6 if i < 4 else X + 9, Y(Q5_F[i]) + (15 if i < 4 else 0)), f"{p} {Q5_F[i]:.3f}", 12.5, color=C["tension"], anchor="start", weight="700")
        if i:
            cv.dot((X, Y(Q5_OLD[i])), 4, fill="#FFFFFF", stroke=C["member2"], w=1.6)
    cv.text((Q5_X0 + Q5_SX * Q5_X[4] - 8, Y(Q5_OLD[4]) - 2), f"舊解 {Q5_OLD[4]:.3f}", 11.5, color=C["muted"], anchor="end")
    cv.text_px(Q5_W / 2, 312, f"A→E 摩擦損失 {100*(1-Q5_F[-1]):.1f}%（舊解 {100*(1-Q5_OLD[-1]):.1f}%）；x 以水平長累計", 13, color=C["text"], weight="700")
    return cv


def fig2_friction():
    return compose([panel_q5_alpha(), panel_q5_force()], cols=1,
                   title=f"{TAG} 圖 2　直線＋圓弧段的累積角變與張力分布（A 端張拉至中間支承 E）",
                   sub=f"μ＝{Q5_MU}、k＝{Q5_K}/m；兩端張拉、左右對稱，只畫左半",
                   note="攔：把切線直線段算進角變；C 點只累積半個圓弧角；D 當成中間支承")


def check_solution():
    for name, got, want, tol in [("FB", Q5_F[1], 0.986, 6e-4), ("FC", Q5_F[2], 0.904, 6e-4), ("FD", Q5_F[3], 0.891, 6e-4),
                                 ("FE", Q5_F[4], 0.847, 6e-4), ("sum a", Q5_AL[-1], 0.276, 1e-9),
                                 ("omega E", Q5_MU * Q5_AL[-1] + Q5_K * Q5_X[-1], 0.16630, 1e-5),
                                 ("loss", 100 * (1 - Q5_F[-1]), 15.3, 0.05)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-friction", fig2_friction, "直線段算進角變；C 點只累積半個圓弧角"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
