#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2006-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2006-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2006-3.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-1／U3-2 題目正本推廣・批 1）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2006-3"
PW, PH = 560, 420          # 各子圖畫布尺寸（px，compose 要求相同）


def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


# ── 判讀清單數值（題目正本 §4）──
L_SPAN = 8.0                     # #5 跨度 8 m（支承間）
B = 30.0                         # #4 梁寬
D_TOP = 8.0                      # #3 頂面至壓力筋中心
D_A, D_B, D_C = 34.0, 8.0, 8.0   # #1 尺寸鏈：頂面→上排拉力筋 34、兩排 8、下排→底面 8
H = D_A + D_B + D_C              # #1 全深 50（由尺寸鏈相加）
Y_LOW, Y_UP = D_C, D_C + D_B     # #2 下排（3 根）距底 8、上排（2 根）距底 16
R9 = 2.87 / 2                    # #9 鋼筋半徑（示意大小）


def panel_elev():
    cv = Canvas(PW, PH, sx=56, ox=36, oy=150)
    hb = 0.32                                            # 梁高（示意）
    _rect(cv, 0, 0, L_SPAN, hb)
    cv.support((0, 0), "pin")                            # #5 左端鉸
    cv.support((L_SPAN, 0), "roller")                    # #5 右端滾
    cv.udl((0, hb), (L_SPAN, hb), 0.55, n=13)            # #6 w_D 全跨
    cv.math((1.0, hb + 1.38), "w_{D} = 0.8 tf/m", 14, color=C["load"], anchor="start")
    cv.text((1.0, hb + 1.05), "（含自重，先施加）", 12, color=C["load"], anchor="start")
    cv.arrow((L_SPAN / 2, hb + 2.05), (L_SPAN / 2, hb + 0.62), C["load"], 3.2)   # #6 P_L 跨中
    cv.math((L_SPAN / 2 + 0.15, hb + 1.95), "P_{L} = 5 tf", 14, color=C["load"], anchor="start")
    cv.text((L_SPAN / 2 + 0.15, hb + 1.62), "（跨中，後施加）", 12, color=C["load"], anchor="start")
    cv.dim((0, 0), (L_SPAN, 0), "8 m", off=62, label_off=14)
    cv.text((L_SPAN / 2, -1.85), "簡支梁立面", 13, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=5.6, ox=150, oy=58)
    _rect(cv, 0, 0, B, H)
    c = 4.0                                              # 箍筋位置（考卷未標，示意）
    cv.poly([(c, c), (B - c, c), (B - c, H - c), (c, H - c), (c, c)], C["member"], 2.2)
    xs3 = (c + 2.4, B / 2, B - c - 2.4)
    for x in (xs3[0], xs3[2]):
        _bar(cv, (x, H - D_TOP), R9, fill="#FFFFFF")     # #3 壓力筋 2-#9（可不考慮，空心表示）
    for x in xs3:
        _bar(cv, (x, Y_LOW), R9)                         # #2 下排 3 根
    for x in (xs3[0], xs3[2]):
        _bar(cv, (x, Y_UP), R9)                          # #2 上排 2 根
    cv.text((B / 2, H - D_TOP - 5), "2-#9（題註可不考慮）", 12.5, color=C["muted"])
    cv.text((B / 2, Y_UP + 6), "5-#9（拉力筋）", 13)
    cv.dim((0, H), (B, H), "30 cm", off=-30, label_off=-14)
    cv.dim((B, H), (B, Y_UP), "34 cm", off=-34, label_off=-28)
    cv.dim((B, Y_UP), (B, Y_LOW), "8 cm", off=-34, label_off=-26)
    cv.dim((B, Y_LOW), (B, 0), "8 cm", off=-34, label_off=-26)
    cv.dim((0, H), (0, H - D_TOP), "8 cm", off=34, label_off=26)
    cv.text((B / 2, -6.5), "梁斷面（全深 34＋8＋8＝50 cm）", 13, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_elev(), panel_sec()], title=f"{TAG} 題目附圖（圖三重繪）",
                   sub="依題目正本判讀清單 #1–#6；箍筋位置、梁立面高度為示意",
                   note="34 cm 由頂面量到上排拉力筋中心；拉力筋兩排（下 3、上 2）")


FIGURES = [("1-problem", fig1_problem, "把 34 cm 讀成全深（漏加下方 8＋8 cm）")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-B1；數值由常數現算，檔尾對 §4 assert）══
BS, HS, NN, EC_ = 30.0, 50.0, 8.0, 2.04e6 / 8
AS1, D1_, AS2, D2_ = 3 * 6.47, 42.0, 2 * 6.47, 34.0
IG_ = BS * HS ** 3 / 12; MCR_ = 2 * math.sqrt(280) * IG_ / (HS / 2)
_qa, _qb, _qc = BS / 2, NN * (AS1 + AS2), -NN * (AS1 * D1_ + AS2 * D2_)
KD_ = (-_qb + math.sqrt(_qb ** 2 - 4 * _qa * _qc)) / (2 * _qa)
ICR_ = BS * KD_ ** 3 / 3 + NN * AS1 * (D1_ - KD_) ** 2 + NN * AS2 * (D2_ - KD_) ** 2
DC_ = (AS1 * D1_ + AS2 * D2_) / (AS1 + AS2)
LB = 800.0; WD_ = 8.0; PL_ = 5000.0
MD_, MDL_ = WD_ * LB ** 2 / 8, WD_ * LB ** 2 / 8 + PL_ * LB / 4


def ie_(ma, branson=False):
    r = MCR_ / ma
    if branson:
        return min(IG_, r ** 3 * IG_ + (1 - r ** 3) * ICR_)
    t = 2 / 3 * r
    return IG_ if t >= 1 else min(IG_, ICR_ / (1 - t * t * (1 - ICR_ / IG_)))


UD, UP = 5 * WD_ * LB ** 4 / 384, PL_ * LB ** 3 / 48
DEL_D = UD / (EC_ * ie_(MD_)); DEL_DL = (UD + UP) / (EC_ * ie_(MDL_))
INC = DEL_DL - DEL_D
INC_B = (UD + UP) / (EC_ * ie_(MDL_, True)) - UD / (EC_ * ie_(MD_, True))
PL_ONLY = UP / (EC_ * ie_(MDL_))


def panel_crsec():
    cv = Canvas(PW, PH, sx=5.8, ox=PW / 2 - 30, oy=40)
    cv.panel("開裂轉換斷面（h＝50，兩排拉力筋）", f"I_{{cr}}＝{ICR_:,.0f}、I_{{g}}＝{IG_:,.0f} cm^{{4}}")
    _rect(cv, -BS / 2, 0, BS / 2, HS, fill="#EDF1F6", w=2.2)
    _rect(cv, -BS / 2, HS - KD_, BS / 2, HS, fill="rgba(29,78,216,0.18)", stroke="none", w=0)
    cv.line((-BS / 2 - 3, HS - KD_), (BS / 2 + 3, HS - KD_), C["compr"], 1.6, dash="6 4")
    cv.text((-BS / 2 - 4, HS - KD_), "中性軸", 12, C["compr"], anchor="end")
    for k in range(3):
        _bar(cv, (-9 + 9 * k, HS - D1_), 1.7, C["tension"])
    for k in range(2):
        _bar(cv, (-4.5 + 9 * k, HS - D2_), 1.7, C["tension"])
    cv.line((-BS / 2, HS - DC_), (BS / 2, HS - DC_), C["accent"], 1, dash="2 3")
    cv.dim((BS / 2, HS), (BS / 2, HS - KD_), f"kd {KD_:.2f}", off=-14, label_off=-30)
    cv.dim((BS / 2, HS), (BS / 2, HS - D2_), "d_{2} 34", off=-62, label_off=-26)
    cv.dim((BS / 2, HS), (BS / 2, HS - D1_), "d_{1} 42", off=-108, label_off=-26)
    cv.dim((-BS / 2, 0), (-BS / 2, HS), "h 50", off=-16, label_off=-24)
    cv.dim((-BS / 2, 0), (BS / 2, 0), "30", off=14, label_off=12)
    cv.text((-BS / 2 - 4, HS - DC_), f"形心 d＝{DC_:.1f}", 11.5, C["accent"], anchor="end")
    return cv


def panel_defl():
    cv = Canvas(PW, PH, sx=1, ox=0, oy=0)
    cv.panel("增量撓度＝兩個載重階段相減", "每個階段用自己的 I_{e}（現行 2/3 M_{cr} 式）")
    x0, sc = 150, 150.0
    rows = [("w_{D}", DEL_D, f"I_{{e}}^{{D}}＝{ie_(MD_):,.0f}", C["deform"]),
            ("w_{D}＋P_{L}", DEL_DL, f"I_{{e}}^{{DL}}＝{ie_(MDL_):,.0f}", C["deform"])]
    for i, (lab, v, s, col) in enumerate(rows):
        y = PH - 110 - i * 62
        cv.rect_px(x0, y - 13, v * sc, 26, "rgba(29,78,216,0.22)", 4, col, 1.2)
        cv.text_px(x0 - 10, y, lab, 13, C["text"], "end")
        cv.text_px(x0 + v * sc + 8, y, f"{v:.3f} cm", 13, col, "start", weight="700")
        cv.text_px(x0 + 6, y + 24, s, 11.5, C["muted"], "start")
    yb = PH - 250
    cv.rect_px(x0 + DEL_D * sc, yb - 13, INC * sc, 26, "rgba(46,125,111,0.25)", 4, C["bmd"], 1.4)
    cv.text_px(x0 + DEL_D * sc + INC * sc / 2, yb - 28, f"增量 {INC:.2f} cm（答案）", 14, C["bmd"], weight="700")
    cv.text_px(x0 - 10, yb, "相減", 13, C["text"], "end")
    ys = PH - 330
    cv.text_px(40, ys + 10, f"對照：Branson 式 {INC_B:.2f} cm；只用 P_{{L}} 配 I_{{e}}^{{DL}} 得 {PL_ONLY:.3f} cm（漏掉 w_{{D}} 撓度增加的部分）", 11.5, C["muted"], "start")
    return cv


def fig2_section_defl():
    return compose([panel_crsec(), panel_defl()], title=f"{TAG} 圖 2　兩排拉力筋開裂斷面與增量撓度",
                   sub="數值取自解析 §4（Ec＝Es/n、n＝8）",
                   note="攔：把 34 cm 當全深、5 根同排；只用 P_L 單獨算撓度")


def check_solution():
    for name, got, want, tol in [("kd", KD_, 18.65, 0.006), ("Icr", ICR_, 173923, 60), ("IeD", ie_(MD_), 189914, 60),
                                 ("IeDL", ie_(MDL_), 176182, 60), ("dD", DEL_D, 0.881, 0.0015), ("dDL", DEL_DL, 2.137, 0.0015),
                                 ("inc", INC, 1.26, 0.006), ("incB", INC_B, 1.35, 0.006)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-section-deflection", fig2_section_defl, "全深 50、兩排筋；兩階段 Ie 相減"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
