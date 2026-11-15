#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2022-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2022-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2022-3.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2022-3"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2022-3-problem.md §4）──
L = 20.0                       # #1 跨徑 20 m
BF, TF = 45.0, 20.0            # #4 上翼板 45×20
BW, HW = 17.5, 50.0            # #4 腹板 17.5×50
BB, TB = 45.0, 20.0            # #5 下翼板 45×20（寬度考卷未標，依向量量測與上翼板同寬）
H = TF + HW + TB               # 90
YP = 12.0                      # #6 鋼腱距底 12 cm（直線）
VX = 0.028
PW, PH = 1240, 470


def panel_elev():
    cv = Canvas(PW, PH, sx=36, ox=90, oy=250)
    hb = H * VX
    _rect(cv, 0, 0, L, hb)
    yt = YP * VX
    cv.line((0, yt), (L, yt), TENDON, 2.4)
    cv.arrow((-1.3, yt), (0, yt), C["load"], 3.0, 11)
    cv.arrow((L + 1.3, yt), (L, yt), C["load"], 3.0, 11)
    cv.math((-1.55, yt), "F_{e}", 16, color=C["load"], anchor="end")
    cv.math((L + 1.55, yt), "F_{e}", 16, color=C["load"], anchor="start")
    cv.support((0, 0), "pin", size=14)
    cv.support((L, 0), "roller", size=14)
    cv.udl((0, hb), (L, hb), 1.2, n=21)
    cv.math((L / 2 - 0.6, hb + 1.55), "W_{G} , W_{D} , W_{E}", 15, color=C["load"])
    cv.text((L * 0.80, hb + 1.55), "（全跨均佈）", 12.5, color=C["load"], anchor="start")
    for x in (L / 3, 2 * L / 3):
        cv.arrow((x, hb + 2.4), (x, hb), C["load"], 3.6, 13)
        cv.math((x, hb + 2.75), "P_{L}", 15, color=C["load"])
    for x0, sgn in ((0.9, 1), (L - 0.9, -1)):     # 腹剪裂縫（考卷紅色斜線，位置約一倍有效深度）
        cv.line((x0 - 0.3 * sgn, 0.55), (x0 + 0.3 * sgn, hb - 0.55), C["load"], 1.8)
    cv.dim((0, hb + 2.4), (L / 3, hb + 2.4), "L/3", off=-18, label_off=-14)
    cv.dim((2 * L / 3, hb + 2.4), (L, hb + 2.4), "L/3", off=-18, label_off=-14)
    cv.dim((0, 0), (L, 0), "L = 20 m", off=52, label_off=15)
    cv.text((L / 2, -2.3), "簡支（左鉸右滾）；直線鋼腱距底 12 cm；紅色斜線為梁端附近腹剪裂縫；豎向放大示意", 12.5, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=2.6, ox=1080, oy=140)
    xc = 0.0
    pts = [(-BB / 2, 0), (BB / 2, 0), (BB / 2, TB), (BW / 2, TB), (BW / 2, TB + HW), (BF / 2, TB + HW),
           (BF / 2, H), (-BF / 2, H), (-BF / 2, TB + HW), (-BW / 2, TB + HW), (-BW / 2, TB), (-BB / 2, TB), (-BB / 2, 0)]
    cv.polygon(pts, "#EDF1F6"); cv.poly(pts, C["member"], 2.2)
    cv.circle((0, YP), 2.2, fill=TENDON, stroke=TENDON, w=1)
    cv.dim((-BF / 2, H), (BF / 2, H), "45 cm", off=-22, label_off=-13)
    cv.dim((-BW / 2, 45), (BW / 2, 45), "17.5", off=0, label_off=-12, size=12)
    cv.dim((-BB / 2, 0), (BB / 2, 0), "45 cm", off=22, label_off=13)
    cv.text((0, -20), "下翼板寬考卷未標，依圖面量測", 11.5, color=C["muted"])
    cv.dim((BF / 2, TB + HW), (BF / 2, H), "20", off=20, label_off=16)
    cv.dim((BF / 2, TB), (BF / 2, TB + HW), "50", off=20, label_off=16)
    cv.dim((BF / 2, 0), (BF / 2, TB), "20", off=20, label_off=16)
    cv.dim((-BF / 2, 0), (-BF / 2, H), "90 cm", off=-28, label_off=-30)
    cv.dim((-12, 0), (-12, YP), "12", off=0, label_off=-12, size=12)
    cv.text((0, -32), "PCI 斷面", 13, weight="700")
    return cv


def fig1_problem():
    a = panel_elev()
    a.parts += panel_sec().parts
    return compose([a], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#8；下翼板寬考卷未標，依 PDF 向量座標與上翼板同寬 45 cm",
                   note="12 cm 為鋼腱形心距梁底（不是下翼板寬）；兩個 P_L 各在距支承 L/3 處".replace("_", ""))


FIGURES = [("1-problem", fig1_problem, "把 12 cm 當成下翼板寬；鋼腱距底取 10 cm")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；數值由常數現算，檔尾對 §4 assert）══
Q22_BF, Q22_TF, Q22_BW, Q22_HW = 45.0, 20.0, 17.5, 50.0     # 上下翼板 45×20、腹板 17.5×50（#1–#3）
Q22_H = 2 * Q22_TF + Q22_HW; Q22_DP = Q22_H - 12.0           # 鋼腱距底 12 → d_p
Q22_FC, Q22_FYT, Q22_FE, Q22_L, Q22_G = 420.0, 2800.0, 200.0, 20.0, 2.4
Q22_WD, Q22_PL, Q22_AV = 1.1, 25.0, 2 * 0.7133
Q22_A = 2 * Q22_BF * Q22_TF + Q22_BW * Q22_HW
Q22_FPC = Q22_FE * 1000 / Q22_A
Q22_VCW = (0.93 * math.sqrt(Q22_FC) + 0.3 * Q22_FPC) * Q22_BW * Q22_DP / 1000
Q22_WDL = Q22_A / 1e4 * Q22_G + Q22_WD                      # 自重＋靜載 tf/m
def q22_vu(x): return 1.2 * Q22_WDL * (Q22_L / 2 - x) + 1.6 * Q22_PL
def q22_ve(x): return 1.2 * Q22_WDL * (Q22_L / 2 - x) + 0.25 * Q22_WDL * (Q22_L / 2 - x) + 1.0 * Q22_PL
Q22_XC = Q22_H / 2 / 100
Q22_VS = q22_vu(Q22_XC) / 0.75 - Q22_VCW
Q22_S = Q22_AV * Q22_FYT * Q22_DP / (Q22_VS * 1000)
def q22_phivn(s): return 0.75 * (Q22_VCW + Q22_AV * Q22_FYT * Q22_DP / s / 1000)
Q22_W, Q22_HP = 760, 360


def panel_q22_sec():
    cv = Canvas(Q22_W, Q22_HP)
    cv.panel("① 斷面（下翼板寬 45；12 cm 是鋼腱距梁底）")
    s, ox, oy = 2.8, 110, 50
    def P(x, y): return (ox + s * x, oy + s * y)
    hb = (Q22_BF - Q22_BW) / 2
    outline = [(0, 0), (Q22_BF, 0), (Q22_BF, Q22_TF), (Q22_BF - hb, Q22_TF), (Q22_BF - hb, Q22_TF + Q22_HW),
               (Q22_BF, Q22_TF + Q22_HW), (Q22_BF, Q22_H), (0, Q22_H), (0, Q22_TF + Q22_HW), (hb, Q22_TF + Q22_HW),
               (hb, Q22_TF), (0, Q22_TF), (0, 0)]
    cv.polygon([P(*p) for p in outline], "#EDF1F6", stroke=C["member"], w=2)
    cv.dot(P(Q22_BF / 2, 12), 6, fill=C["load"])
    cv.dim(P(0, 0), P(Q22_BF, 0), f"{Q22_BF:.0f}", off=22, label_off=-14)
    cv.dim(P(Q22_BF, 0), P(Q22_BF, 12), "12", off=-26, label_off=-14)
    cv.dim(P(Q22_BF, Q22_H), P(Q22_BF, 12), f"d_{{p}} = {Q22_DP:.0f}", off=-70, label_off=-28)
    cv.dim(P(0, Q22_H), P(0, 0), f"h = {Q22_H:.0f}", off=26, label_off=30)
    cv.text(P(Q22_BF - hb + 2, Q22_H / 2), f"b_{{w}}＝{Q22_BW}", 12, color=C["muted"], anchor="start")
    cv.text(P(Q22_BF / 2 - 4, 12), "鋼腱", 12, color=C["load"], anchor="end", weight="700")
    x = 430
    lines = [(f"A＝2(45×20)＋17.5×50＝{Q22_A:.0f} cm^{{2}}", C["text"]),
             (f"f_{{pc}}＝F_{{e}}/A＝{Q22_FPC:.2f} kgf/cm^{{2}}", C["text"]),
             (f"V_{{cw}}＝(0.93√f'c＋0.3f_{{pc}})b_{{w}}d_{{p}}", C["text"]),
             (f"　＝{Q22_VCW:.2f} tf（V_{{p}}＝0，直線鋼腱）", C["compr"]),
             (f"V_{{ci}}≈280 tf ≫ V_{{cw}} → 腹剪控制", C["muted"]),
             ("舊解：12 當下翼板寬 → A＝2015、V_{cw}＝68.38", C["muted"])]
    for i, (tx, col) in enumerate(lines):
        cv.text_px(x, 110 + 34 * i, tx, 13, color=col, anchor="start", weight="700" if i == 3 else "400")
    return cv


def panel_q22_shear():
    cv = Canvas(Q22_W, Q22_HP)
    cv.panel("② 支承附近剪力需求 vs 強度（tf）")
    x0, sx, y0, vmin, sv = 80, 460 / 3.0, 60, 40.0, 7.0
    xr = x0 + 460 + 10
    def P(x, v): return (x0 + sx * x, y0 + sv * (v - vmin))
    for v in (40, 45, 50, 55, 60, 65):
        cv.line(P(0, v), P(3.0, v), C["border"], 1)
        cv.text((x0 - 8, P(0, v)[1]), f"{v}", 11.5, color=C["muted"], anchor="end")
    xs = [3.0 * i / 60 for i in range(61)]
    cv.poly([P(x, q22_vu(x)) for x in xs], C["load"], 3)
    cv.poly([P(x, q22_ve(x)) for x in xs], C["sfd"], 2.2, dash="6 4")
    for s, col, lab in ((13, C["deform"], "φV_{n} D10 雙肢 @13"), (15, C["member2"], "φV_{n} 原設計 @15")):
        cv.line(P(0, q22_phivn(s)), P(3.0, q22_phivn(s)), col, 2, dash=None if s == 13 else "8 4")
        cv.text((xr, P(3.0, q22_phivn(s))[1] + (8 if s == 13 else -8)), f"{lab}＝{q22_phivn(s):.2f}", 12, color=col, anchor="start", weight="700")
    cv.line(P(0, 0.75 * Q22_VCW), P(3.0, 0.75 * Q22_VCW), C["compr"], 1.6, dash="3 3")
    cv.text((xr, P(3.0, 0.75 * Q22_VCW)[1]), f"φV_{{cw}}＝{0.75*Q22_VCW:.2f}", 12, color=C["compr"], anchor="start")
    for xx, lab in ((Q22_XC, "h/2"), (Q22_DP / 100, "d_{p}")):
        cv.line(P(xx, vmin), P(xx, 68), C["accent"], 1.2, dash="4 3")
        cv.text((P(xx, 68)[0] + (-4 if lab == "h/2" else 4), P(xx, 68)[1] + 10), f"{lab}＝{xx:.2f} m", 11.5, color=C["accent"], anchor="end" if lab == "h/2" else "start")
    cv.dot(P(Q22_XC, q22_vu(Q22_XC)), 5, fill=C["load"])
    cv.text((P(Q22_XC, q22_vu(Q22_XC))[0] + 10, P(Q22_XC, q22_vu(Q22_XC))[1] + 22), f"V_{{u}}＝{q22_vu(Q22_XC):.2f}（1.2D＋1.6L）", 12.5, color=C["load"], anchor="start", weight="700")
    cv.text((P(0.95, q22_ve(0.95))[0], P(0.95, q22_ve(0.95))[1] + 16), f"1.2D＋1.0E＋1.0L（h/2 處 {q22_ve(Q22_XC):.2f}，不控制）", 12, color=C["sfd"], anchor="start")
    cv.text_px(Q22_W / 2, 336, f"V_{{s}}＝V_{{u}}/φ − V_{{cw}}＝{Q22_VS:.2f} → s ≤ {Q22_S:.1f} cm；@15 的 φV_{{n}} 小於 V_{{u}}，與裂縫吻合", 13, color=C["text"], weight="700")
    return cv


def fig2_shear():
    return compose([panel_q22_sec(), panel_q22_shear()], cols=1,
                   title=f"{TAG} 圖 2　斷面、臨界斷面與腹剪強度",
                   sub="單位 cm、tf；f'c＝420、fyt＝2800 kgf/cm2；x 自支承量起",
                   note="攔：12 cm 讀成下翼板寬；垂直地震乘 1.2 又與 1.6L 同時作用；漏比較原設計 @15")


def check_solution():
    for name, got, want, tol in [("A", Q22_A, 2675, 1e-9), ("fpc", Q22_FPC, 74.77, 0.005), ("Vcw", Q22_VCW, 56.63, 0.005),
                                 ("Vu", q22_vu(Q22_XC), 59.96, 0.005), ("Vs", Q22_VS, 23.32, 0.005), ("s", Q22_S, 13.4, 0.05),
                                 ("E comb", q22_ve(Q22_XC), 49.12, 0.005), ("phiVn15", q22_phivn(15), 58.05, 0.005),
                                 ("phiVn13", q22_phivn(13), 60.45, 0.005)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-shear", fig2_shear, "12 cm 讀成下翼板寬；自訂載重組合；漏比原設計"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
