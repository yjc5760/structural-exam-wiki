#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2019-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2019-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2019-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2019-4"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2019-4-problem.md §4）──
LT = 3600.0                    # #1 梁全長＝錨碇間 3600 cm（50＋3500＋50）
SUP = 50.0                     # #1 支承距梁端 50 cm（支承中心距 3500）
H, B = 180.0, 40.0             # #2 梁深 180、寬 40
T1_END, T1_MID = 45.0, 15.0    # #4、#5 鋼腱 1：端部距底 45、跨中距底 15
T2_END, T2_MID = 135.0, 30.0   # #4、#5 鋼腱 2：端部距底 135、跨中距底 30
YC = 90.0
SX, VX = 0.026, 0.55           # 立面：水平 1 cm → 0.026 px*，豎向 1 cm → 0.55 px（豎向放大示意）
PW, PH = 1220, 660


def prof(e_end, e_mid):
    return lambda x: e_mid + (e_end - e_mid) * (2 * x / LT - 1) ** 2


def panel_elev():
    cv = Canvas(PW, PH, sx=1.0, ox=120, oy=430)
    X = lambda x: x * SX * 10
    P = lambda x, y: (X(x), y * VX)
    _rect(cv, *P(0, 0), *P(LT, H))
    cv.line(P(-120, YC), P(LT + 120, YC), C["muted"], 1.2, dash="12 4 2 4")
    cv.line(P(LT / 2, -30), P(LT / 2, H + 40), C["muted"], 1.0, dash="10 4 2 4")
    cv.text(P(LT / 2, H + 52), "跨度中心線", 12.5, color=C["muted"])
    for e1, e2, lab, yl in ((T1_END, T1_MID, "預力鋼腱 1", 0.32), (T2_END, T2_MID, "預力鋼腱 2", 0.78)):
        f = prof(e1, e2)
        cv.poly([P(LT * i / 120, f(LT * i / 120)) for i in range(121)], TENDON, 2.6)
        for xe in (0, LT):
            cv.polygon([P(xe - 12, f(xe) - 9), P(xe + 12, f(xe) - 9), P(xe + 12, f(xe) + 9), P(xe - 12, f(xe) + 9)], C["member"])
        xl = LT * 0.2
        cv.text(P(xl, f(xl) + (16 if lab.endswith("2") else -16)), lab, 12.5, color=TENDON)
    cv.text(P(-60, 165), "端錨", 12.5, anchor="end")
    cv.support(P(SUP, 0), "pin", size=11)
    cv.support(P(LT - SUP, 0), "pin", size=11)
    cv.dim(P(0, 0), P(SUP, 0), "50", off=58, label_off=16)
    cv.dim(P(SUP, 0), P(LT - SUP, 0), "3500", off=58, label_off=16)
    cv.dim(P(LT - SUP, 0), P(LT, 0), "50", off=58, label_off=16)
    for k in range(4):
        cv.dim(P(LT, 45 * k), P(LT, 45 * (k + 1)), "45", off=34, label_off=18)
    cv.text((X(LT / 2), -98), "大梁立面圖（長度單位 cm；鋼腱採拋物線布設；豎向放大示意；A-A 在跨度中心線、B-B 在梁端）", 12.5, color=C["muted"])
    return cv


def _section(cv, x0, ys, lab):
    _rect(cv, x0, 0, x0 + B, H)
    cv.line((x0 - 10, YC), (x0 + B + 10, YC), C["muted"], 1.2, dash="10 4 2 4")
    for y in ys:
        cv.circle((x0 + B / 2, y), 3.2, fill=TENDON, stroke=TENDON, w=1)
    cv.dim((x0, 0), (x0 + B, 0), "40", off=26, label_off=14)
    cv.text((x0 + B / 2, -64), lab, 14, weight="700")


def panel_secs():
    cv = Canvas(PW, PH, sx=1.0, ox=330, oy=85)
    xa, xb = 0.0, 420.0
    _section(cv, xa, (T2_MID, T1_MID), "剖面 A-A（跨中）")
    cv.dim((xa, H), (xa, YC), "90", off=34, label_off=20)
    cv.dim((xa, YC), (xa, T2_MID), "60", off=34, label_off=20)
    cv.dim((xa, T2_MID), (xa, T1_MID), "15", off=34, label_off=20)
    cv.dim((xa, T1_MID), (xa, 0), "15", off=34, label_off=20)
    cv.text((xa + B + 14, T2_MID + 6), "鋼腱 2", 12.5, color=TENDON, anchor="start")
    cv.text((xa + B + 14, T1_MID - 6), "鋼腱 1", 12.5, color=TENDON, anchor="start")
    _section(cv, xb, (T2_END, T1_END), "剖面 B-B（梁端）")
    for k in range(4):
        cv.dim((xb + B, 45 * k), (xb + B, 45 * (k + 1)), "45", off=30, label_off=18)
    cv.text((xb - 14, T2_END), "鋼腱 2", 12.5, color=TENDON, anchor="end")
    cv.text((xb - 14, T1_END), "鋼腱 1", 12.5, color=TENDON, anchor="end")
    return cv


def fig1_problem():
    a = panel_elev()
    a.parts += panel_secs().parts
    return compose([a], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#7；兩鋼腱皆由兩端同步施拉（題文）",
                   note="A-A 為跨中、B-B 為梁端；跨中鋼腱 2 距底 30、鋼腱 1 距底 15；梁端鋼腱 2 距底 135、鋼腱 1 距底 45")


FIGURES = [("1-problem", fig1_problem, "A-A／B-B 對調；鋼腱 2 端部高度讀成 90；拋物線長取 3500")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；數值由常數現算，檔尾對 §4 assert）══
Q19_FC, Q19_EPS, Q19_APS, Q19_FPJ = 350.0, 1970000.0, 30.0, 12300.0
Q19_K, Q19_MU, Q19_L = 0.0049, 0.25, 36.0            # /m、/rad、錨碇至錨碇 m（#7）
Q19_B, Q19_HH = 40.0, 180.0
Q19_YEND = {1: 45.0, 2: 135.0}; Q19_YMID = {1: 15.0, 2: 30.0}   # 距底 cm（#4、#5）
Q19_PJ = Q19_FPJ * Q19_APS / 1000                     # tf
def _q19_om(t):
    f = (Q19_YEND[t] - Q19_YMID[t]) / 100
    return Q19_K * Q19_L / 2 + Q19_MU * 4 * f / Q19_L
Q19_PF = {t: Q19_PJ * math.exp(-_q19_om(t)) for t in (1, 2)}   # 跨中摩擦後
Q19_A = Q19_B * Q19_HH; Q19_I = Q19_B * Q19_HH ** 3 / 12; Q19_YC = Q19_HH / 2
Q19_N = Q19_EPS / (15000 * math.sqrt(Q19_FC))
def _q19_dfc(P2, sec):                               # 鋼腱 2 施拉在鋼腱 1 位置的混凝土應力增量
    y = Q19_YMID if sec == "cen" else Q19_YEND
    e2, e1 = Q19_YC - y[2], Q19_YC - y[1]
    return P2 * 1000 / Q19_A + P2 * 1000 * e2 * e1 / Q19_I
Q19_DFC_C = _q19_dfc(Q19_PF[2], "cen"); Q19_DFC_E = _q19_dfc(Q19_PJ, "end")
Q19_DP_C = Q19_N * Q19_DFC_C * Q19_APS / 1000; Q19_DP_E = Q19_N * Q19_DFC_E * Q19_APS / 1000
Q19_RES = {"P1,Cen": Q19_PF[1] - Q19_DP_C, "P2,Cen": Q19_PF[2], "P1,End": Q19_PJ - Q19_DP_E, "P2,End": Q19_PJ}
Q19_W, Q19_H = 760, 340


def panel_q19_elev():
    cv = Canvas(Q19_W, Q19_H)
    cv.panel("① 兩腱線形（全長 3600 cm，豎向放大示意）")
    x0, sx, y0 = 80, 600 / Q19_L, 62
    def P(x, y): return (x0 + sx * x, y0 + 1.0 * y)
    cv.polygon([P(0, 0), P(Q19_L, 0), P(Q19_L, Q19_HH), P(0, Q19_HH)], "#EDF1F6", stroke=C["member"], w=1.8)
    cv.line(P(0, Q19_YC), P(Q19_L, Q19_YC), C["member2"], 1.1, dash="10 4 2 4")
    for t, col in ((1, C["deform"]), (2, C["load"])):
        f = Q19_YEND[t] - Q19_YMID[t]
        pts = [P(Q19_L * i / 80, Q19_YEND[t] - 4 * f * (i / 80) * (1 - i / 80)) for i in range(81)]
        cv.poly(pts, col, 2.6)
        cv.text(P(Q19_L * (0.04 if t == 2 else 0.25), (150 if t == 2 else Q19_YEND[t] - 0.75 * f - 12)), f"鋼腱 {t}：端 {Q19_YEND[t]:.0f} → 跨中 {Q19_YMID[t]:.0f}（矢高 {f:.0f}）", 12, color=col, anchor="start" if t == 2 else "middle", weight="700")
    for x in (0.5, Q19_L - 0.5):
        cv.pin_support(P(x, 0), size=9)
    mx = x0 + sx * Q19_L / 2
    cv.line((mx, y0 - 6), (mx, y0 + 1.0 * Q19_HH + 6), C["accent"], 1.6, dash="6 4")
    cv.text((mx + 4, y0 + 1.0 * Q19_HH + 14), "A-A（跨中）", 12, color=C["accent"], anchor="start", weight="700")
    cv.text((x0 + sx * Q19_L - 2, y0 + 1.0 * Q19_HH + 14), "B-B（梁端錨碇）", 12, color=C["accent"], anchor="end", weight="700")
    cv.text_px(Q19_W / 2, 322, "兩腱皆兩端同步張拉 → 摩擦只算半長 18 m；先拉鋼腱 1，再拉鋼腱 2", 12.5, color=C["muted"])
    return cv


def panel_q19_bar():
    cv = Canvas(Q19_W, Q19_H)
    cv.panel("② 起始預力：摩擦後 − 鋼腱 2 施拉造成鋼腱 1 的彈性縮短（tf）")
    rows = [("P1,Cen", Q19_PF[1], Q19_DP_C), ("P2,Cen", Q19_PF[2], 0.0), ("P1,End", Q19_PJ, Q19_DP_E), ("P2,End", Q19_PJ, 0.0)]
    x0, sc = 200, 520 / Q19_PJ
    for i, (nm, pf, dp) in enumerate(rows):
        y = 70 + i * 56
        cv.text_px(x0 - 12, y + 13, nm, 14, anchor="end", weight="700")
        cv.rect_px(x0, y, sc * (pf - dp), 26, C["compr"], rx=3)
        if dp:
            cv.rect_px(x0 + sc * (pf - dp), y, sc * dp, 26, C["fill_t"], rx=0, stroke=C["tension"], sw=1.2)
        cv.rect_px(x0 + sc * pf, y, sc * (Q19_PJ - pf), 26, C["ghost"], rx=0)
        cv.text_px(x0 + sc * (pf - dp) - 6, y + 13, f"{pf - dp:.1f}", 13, color="#FFFFFF", anchor="end", weight="700")
    cv.text_px(Q19_W / 2, 296, f"n＝{Q19_N:.3f}；Δf_{{c}}：跨中 {Q19_DFC_C:.2f}、端部 {Q19_DFC_E:.2f} kgf/cm^{{2}} → ΔP_{{1}}＝{Q19_DP_C:.1f}／{Q19_DP_E:.1f} tf", 13, color=C["tension"], weight="700")
    cv.text_px(Q19_W / 2, 320, f"灰：摩擦損失（P_{{j}}＝{Q19_PJ:.0f}）；紅框：彈性縮短；鋼腱 2 最後張拉無此損失", 12, color=C["muted"])
    return cv


def fig2_tendons():
    return compose([panel_q19_elev(), panel_q19_bar()], cols=1,
                   title=f"{TAG} 圖 2　兩腱線形、摩擦與施拉順序造成的彈性縮短",
                   sub="單位 cm、tf；高程自梁底量起；Ec＝15000√f'c",
                   note="攔：A-A／B-B 對調；當成單端張拉；拋物線長取 3500；漏算鋼腱 1 的彈性縮短")


def check_solution():
    for name, got, want, tol in [("P1c", Q19_RES["P1,Cen"], 309.4, 0.05), ("P2c", Q19_RES["P2,Cen"], 328.1, 0.05),
                                 ("P1e", Q19_RES["P1,End"], 366.3, 0.05), ("P2e", Q19_RES["P2,End"], 369.0, 1e-9),
                                 ("dfc c", Q19_DFC_C, 121.53, 0.01), ("dfc e", Q19_DFC_E, 12.81, 0.01), ("n", Q19_N, 7.020, 5e-4)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-tendons", fig2_tendons, "A-A／B-B 對調；單端張拉；漏彈性縮短"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
