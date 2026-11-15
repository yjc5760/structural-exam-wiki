#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2018-2 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2018-2-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2018-2.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-3 批 2＋U1-3＋U2-3 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2018-2"

# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _bar(cv, p, r, fill=None):
    cv.circle(p, r, fill=fill or C["member"], stroke=C["member"], w=1.2)


def _hoop(cv, c, B, H, w=2.0, r=None):
    cv.poly([(c, c), (B - c, c), (B - c, H - c), (c, H - c), (c, c)], C["member"], w)


def _ring_bars(cv, B, H, e, n, r):
    """每面 n 根（含角筋）沿周邊等距排列，回傳座標"""
    pts = set()
    for i in range(n):
        t = e + (B - 2 * e) * i / (n - 1)
        u = e + (H - 2 * e) * i / (n - 1)
        for p in ((t, e), (t, H - e), (e, u), (B - e, u)):
            pts.add((round(p[0], 6), round(p[1], 6)))
    for p in pts:
        _bar(cv, p, r)
    return pts


# ── 題目附圖重繪（題目正本 RC-2018-2-problem.md §4）──
P_C = 50.0             # #7 柱 50×50；#4 梁寬＝柱寬 50
P_SX, P_SY = 400.0, 380.0   # 跨度考卷未給（示意，cm）
P_H = 380.0            # 題文樓層高 3.8 m
PW, PH = 600, 460


def panel_plan():
    cv = Canvas(PW, PH, sx=0.55, ox=70, oy=120)
    xs = (0, P_SX, 2 * P_SX)
    for x in xs:
        for y in (0, P_SY):
            _rect(cv, x - P_C / 2, y - P_C / 2, x + P_C / 2, y + P_C / 2, fill="#C9D1DC")
    for y in (0, P_SY):
        for x0, x1 in ((xs[0], xs[1]), (xs[1], xs[2])):
            cv.line((x0 + P_C / 2, y - P_C / 2), (x1 - P_C / 2, y - P_C / 2), C["member"], 1.8)
            cv.line((x0 + P_C / 2, y + P_C / 2), (x1 - P_C / 2, y + P_C / 2), C["member"], 1.8)
    for x in xs:
        cv.line((x - P_C / 2, P_C / 2), (x - P_C / 2, P_SY - P_C / 2), C["member"], 1.8)
        cv.line((x + P_C / 2, P_C / 2), (x + P_C / 2, P_SY - P_C / 2), C["member"], 1.8)
    cv.circle((2 * P_SX, 0), 95, stroke=C["accent"], w=2.0, dash="6 4")   # 角柱標示圈
    cv.text((2 * P_SX + 60, -60), "角柱接頭", 14, color=C["accent"], anchor="start", weight="700")
    cv.text((P_SX / 2, P_SY / 2), "平面（方塊＝柱斷面）", 13, color=C["muted"])
    cv.text((P_SX, -110), "跨度考卷未給（示意）；兩向梁尺寸與配筋相同", 12.5, color=C["muted"])
    return cv


def panel_joint():
    cv = Canvas(PW, PH, sx=0.44, ox=270, oy=118)
    hb = 70.0                              # 梁深考卷未給（示意）
    _rect(cv, -P_C / 2, -40, P_C / 2, P_H + 330)         # 上下柱連續（判讀 #1）
    _rect(cv, -P_C / 2 - 300, -hb, -P_C / 2, 0)            # 下層樓梁（示意）
    _rect(cv, -P_C / 2, -hb, P_C / 2, 0, fill="#F6E7D8")
    _rect(cv, -P_C / 2 - 300, P_H - hb, -P_C / 2, P_H)     # 框入的梁（另一向梁垂直紙面）
    _rect(cv, -P_C / 2, P_H - hb, P_C / 2, P_H, fill="#F6E7D8")
    cv.line((-P_C / 2 - 300, P_H - 6), (P_C / 2 - 6, P_H - 6), C["load"], 2.6)
    cv.text((-P_C / 2 - 150, P_H + 22), "8-D29 拉力筋，d＝43 cm", 13, color=C["load"])
    cv.text((-P_C / 2 - 170, P_H - hb - 24), "梁寬＝柱寬 50；梁全深考卷未給", 12.5, color=C["muted"])
    cv.dim((P_C / 2, 0), (P_C / 2, P_H), "3.8 m", off=40, label_off=30)
    cv.text((P_C / 2 + 18, P_H + 260), "上柱", 13, anchor="start")
    cv.text((P_C / 2 + 18, P_H / 2), "下柱", 13, anchor="start")
    cv.text((P_C / 2 + 18, P_H - hb / 2), "接頭", 13, color=C["accent"], anchor="start")
    cv.text((-120, -hb - 45), "角柱立面示意：中間樓層，上下皆有柱（判讀 #1）", 12.5, color=C["muted"])
    cv.text((-120, -hb - 78), "柱 50×50 cm；f'c＝280、D29 f_y＝4200 kgf/cm²", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_plan(), panel_joint()], title=f"{TAG} 題目附圖（構架平面重繪＋角柱接頭示意）",
                   sub="依題目正本判讀清單 #1–#7；跨度、梁深、樓版為示意（考卷未給）",
                   note="附圖是平面圖（不是立面）：角柱只有兩向各一支梁框入，梁寬＝柱寬")


FIGURES = [("1-problem", fig1_problem, "把平面圖當立面、把角柱接頭當屋頂層")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2；數值由常數現算，檔尾對 §4 assert）══
import math as _m
from structdraw import Canvas as _Cv, compose as _compose
FC8, FY8, AS8, D8, B8, H8 = 280.0, 4200.0, 8 * 6.47, 43.0, 50.0, 380.0
T8 = 1.25 * FY8 * AS8                               # §4 Step 2（kgf）
A8 = T8 / (0.85 * FC8 * B8)
MPR8 = T8 * (D8 - A8 / 2)                           # kgf·cm
VCOL8 = MPR8 / H8                                   # 角柱一支梁：V_{col}·H＝M_{pr}
VJ8 = T8 - VCOL8
PHIVN8 = 0.85 * 3.2 * _m.sqrt(FC8) * B8 * B8
T8_OLD = FY8 * AS8
MN8_OLD = T8_OLD * (D8 - T8_OLD / (0.85 * FC8 * B8) / 2)
VJ8_OLD = T8_OLD - 2 * MN8_OLD / H8                 # 舊解：A_sf_y、2M_n/H
RW, RH = 400, 500


def panel_r_sub():
    cv = _Cv(RW, RH, sx=0.9, ox=120, oy=250)
    cv.panel("① 角柱子結構：只有一支梁")
    h2 = H8 / 2
    cv.line((0, -h2), (0, h2), C["member2"], 22, cap="butt")
    cv.polygon([(-25, -25), (25, -25), (25, 25), (-25, 25)], "#C9D1DC", stroke=C["member"], w=2)
    cv.polygon([(25, -25), (265, -25), (265, 25), (25, 25)], "#EDF1F6", stroke=C["member"], w=2)
    cv.text((205, 0), "梁（示意）", 12, color=C["muted"])
    for y in (h2, -h2):
        cv.dot((0, y), 6, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    cv.text((14, h2 + 20), "反曲點（H/2）", 12, color=C["accent"], anchor="start")
    cv.text((14, -h2 - 2), "反曲點（H/2）", 12, color=C["accent"], anchor="start")
    cv.arrow((60, h2), (8, h2), C["sfd"], 3)
    cv.arrow((-60, -h2), (-8, -h2), C["sfd"], 3)
    cv.text((-14, h2 - 26), f"V_{{col}}＝{VCOL8/1e3:.2f}", 12.5, color=C["sfd"], anchor="end", weight="700")
    cv.text((14, -h2 + 26), f"V_{{col}}＝{VCOL8/1e3:.2f}", 12.5, color=C["sfd"], anchor="start", weight="700")
    cv.moment_arrow((95, 0), r=34, ccw=False, color=C["load"], span=230, start=200)
    cv.text((95, 58), f"M_{{pr}}＝{MPR8/1e5:.2f} tf·m", 12.5, color=C["load"], weight="700")
    cv.dim((-62, -h2), (-62, h2), f"{H8/100:.1f} m", off=-8, label_off=-22)
    cv.text_px(200, 452, "柱彎矩和＝梁端彎矩：V_{col}·H＝M_{pr}", 12.5, color=C["text"])
    cv.text_px(200, 474, "內柱兩支梁才是 (M_{pr}^{+}＋M_{pr}^{-})/H", 12, color=C["muted"])
    return cv


def panel_r_fbd():
    cv = _Cv(RW, RH, sx=3.0, ox=165, oy=250)
    cv.panel("② 接頭上半部水平自由體")
    s = 25
    cv.polygon([(-s, 0), (s, 0), (s, s), (-s, s)], "#C9D1DC", stroke=C["member"], w=2)
    cv.poly([(-s, -s), (s, -s), (s, 0), (-s, 0)], C["ghost"], 1.6, dash="5 4")
    cv.line((-s - 4, s - 6), (s + 34, s - 6), C["tension"], 2.4)
    cv.arrow((s + 2, s - 6), (s + 34, s - 6), C["tension"], 3.4)
    cv.text((s + 3, s + 9), "T＝1.25f_{y}A_{s}", 12.5, color=C["tension"], anchor="start", weight="700")
    cv.text((s + 3, s - 13), f"＝{T8/1e3:.2f}", 12.5, color=C["tension"], anchor="start", weight="700")
    cv.arrow((12, s + 22), (-20, s + 22), C["sfd"], 3)
    cv.text((-22, s + 30), f"V_{{col}}＝{VCOL8/1e3:.2f}", 12.5, color=C["sfd"], anchor="end", weight="700")
    cv.arrow((20, 0), (-24, 0), C["load"], 3.6)
    cv.text((0, -8), f"V_{{j}}＝T－V_{{col}}＝{VJ8/1e3:.1f} tf", 14, color=C["load"], weight="700")
    cv.text((0, -16), "（水平剪力面，取上半部平衡）", 12, color=C["muted"])
    cv.text_px(200, 400, f"A_{{j}}＝50×50；角柱係數 3.2√f'c（φ＝0.85）", 12.5, color=C["text"])
    cv.text_px(200, 424, f"φV_{{n}}＝{PHIVN8/1e3:.1f} tf", 13, color=C["deform"], weight="700")
    cv.text_px(200, 452, "梁筋拉力不乘 φ，且以 1.25f_{y} 計（18.8.2.1）", 12, color=C["muted"])
    return cv


def panel_r_bar():
    cv = _Cv(RW, RH)
    cv.panel("③ 需求 vs 強度")
    rows = [("V_{j} 現行（主線）", VJ8, C["load"]), ("V_{j} 舊解 A_{s}f_{y}、2M_{n}/H", VJ8_OLD, C["member2"]),
            ("φV_{n} 角柱", PHIVN8, C["deform"])]
    vmax = max(r[1] for r in rows); x0, wmax = 40, 300
    for i, (lab, v, col) in enumerate(rows):
        y = 120 + i * 92
        cv.text_px(x0, y - 18, lab, 13, color=C["text"], anchor="start")
        cv.rect_px(x0, y, wmax * v / vmax, 30, col, rx=4)
        cv.text_px(x0 + wmax * v / vmax - 6, y + 15, f"{v/1e3:.1f}", 13, color="#FFFFFF", anchor="end", weight="700")
    cv.text_px(200, 410, f"V_{{j}}／φV_{{n}}＝{VJ8/PHIVN8:.2f} ＞ 1 → NG", 15, color=C["load"], weight="700")
    cv.text_px(200, 440, f"舊解兩處都使 V_{{j}} 偏小（{VJ8_OLD/1e3:.1f}），結論 NG 不變", 12, color=C["muted"])
    cv.text_px(200, 462, f"柱需 √(V_{{j}}／0.85·3.2√f'c)＝{_m.sqrt(VJ8/(0.85*3.2*_m.sqrt(FC8))):.1f} cm 見方", 12, color=C["muted"])
    return cv


def fig2_joint():
    return _compose([panel_r_sub(), panel_r_fbd(), panel_r_bar()],
                    title=f"{TAG} 圖 2　角柱接頭剪力：T＝1.25fy·As 與 Vcol＝Mpr/H",
                    sub="單位 tf、tf·m；H 取樓層高 3.8 m（梁全深未給，§5.1）；忽略梁剪力對柱心的附加彎矩",
                    note="攔：T 用 As·fy（漏 1.25）；角柱套內柱的 2M/H；忘記減 Vcol")


def check_solution():
    for name, got, want, tol in [("T", T8 / 1e3, 271.74, 0.005), ("Mpr", MPR8 / 1e5, 85.82, 0.005),
                                 ("Vcol", VCOL8 / 1e3, 22.58, 0.006), ("Vj", VJ8 / 1e3, 249.2, 0.05),
                                 ("phVn", PHIVN8 / 1e3, 113.8, 0.05), ("ratio", VJ8 / PHIVN8, 2.19, 0.005),
                                 ("old Vj", VJ8_OLD / 1e3, 178.6, 0.05)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-joint", fig2_joint, "T 漏 1.25f_y；角柱套 2M/H；忘記減 V_col"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
