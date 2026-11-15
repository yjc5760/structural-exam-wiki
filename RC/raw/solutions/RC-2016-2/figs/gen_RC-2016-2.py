#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2016-2 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2016-2-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2016-2.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-3 批 2＋U1-3＋U2-3 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2016-2"

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


# ── 題目附圖重繪（題目正本 RC-2016-2-problem.md §4）──
P_L = 7.5            # #5 淨跨 7.5 m，兩端固定
P_B, P_H = 35.0, 70.0  # #7 斷面 35×70
P_D = 63.0           # #2 頂、底筋受拉時 d＝63 → 筋心距外緣 7
P_E = P_H - P_D
PW, PH = 600, 430


def panel_beam():
    cv = Canvas(PW, PH, sx=60, ox=75, oy=190)
    hb = 0.30
    _rect(cv, 0, 0, P_L, hb)
    cv.support((0, hb / 2), "fixed", ang=90, size=30)
    cv.support((P_L, hb / 2), "fixed", ang=-90, size=30)
    cv.udl((0, hb), (P_L, hb), 0.75, n=13)                    # #4 全跨均布
    cv.math((P_L / 2 - 0.9, hb + 1.25), "w_{D} = 2 tf/m", 14, color=C["load"])
    cv.text((P_L / 2 + 0.3, hb + 1.25), "（含自重）", 12.5, color=C["load"], anchor="start")
    cv.math((P_L / 2, hb + 1.62), "w_{L} = 1 tf/m", 14, color=C["load"])
    cv.dim((0, 0), (P_L, 0), "L = 7.5 m", off=48, label_off=15)
    cv.text((P_L / 2, -1.7), "兩端固定之 RC 梁（承第一題）", 13, color=C["muted"])
    cv.text((P_L / 2, -2.15), "第一題 M_E＝16.5 tf-m 供第一題設計用", 12, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=4.6, ox=200, oy=60)
    _rect(cv, 0, 0, P_B, P_H)
    c = 4.5                                                   # 箍筋位置（考卷未給，示意）
    _hoop(cv, c, P_B, P_H)
    for y0, y1 in ((c, P_E + 3.2), (P_E + 7.0, P_H - P_E - 7.0), (P_H - P_E - 3.2, P_H - c)):
        cv.line((P_B / 2, y0), (P_B / 2, y1), C["member"], 1.8, dash="6 3")   # 第 3 股（示意，避開標註）
    xs = (c + 2.5, P_B / 2, P_B - c - 2.5)
    for x in xs:
        _bar(cv, (x, P_H - P_E), 1.44)                       # 頂 3-D29
        _bar(cv, (x, P_E), 1.11)                             # 底 3-D22
    cv.text((P_B / 2, P_H - P_E - 5), "頂 3-D29", 13)
    cv.text((P_B / 2, P_E + 5), "底 3-D22", 13)
    cv.dim((0, P_H), (P_B, P_H), "35 cm", off=-28, label_off=-14)
    cv.dim((P_B, P_H), (P_B, P_E), "d = 63 cm", off=-30, label_off=-44)
    cv.dim((0, 0), (0, P_H), "70 cm", off=-34, label_off=-24)
    cv.text((P_B / 2, -6), "梁斷面：3 股 D10 箍筋（第 3 股位置示意）", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_beam(), panel_sec()], title=f"{TAG} 題目附圖（第一題附圖重繪＋第二題配筋）",
                   sub="依題目正本判讀清單 #1、#2、#4、#5、#7；箍筋位置與第 3 股位置為示意",
                   note="頂、底筋受拉時有效深度皆取 63 cm（題文）；計算彎矩強度以單筋斷面")


FIGURES = [("1-problem", fig1_problem, "把第二題當成無附圖、漏看兩端固定與 d＝63（頂底皆同）")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2；數值由常數現算，檔尾對 §4 assert）══
from structdraw import Canvas as _Cv
D6, DBMIN6, DBT6, H6, AV6, FY6 = 63.0, 2.22, 0.95, 70.0, 2.13, 4200.0
FS6 = 1.25 * FY6
_mpr = lambda As: As * FS6 * (D6 - As * FS6 / (0.85 * 280 * 35) / 2) / 1e5
MN6, MP6 = _mpr(19.41), _mpr(11.61)
VE6 = (MN6 + MP6) / 7.5 + 3.4 * 7.5 / 2
VC6 = 0.53 * math.sqrt(280.0) * 35 * D6 / 1e3
SSTR6 = AV6 * FY6 * D6 / ((VE6 / 0.75 - VC6) * 1e3)
NEW6 = [("d/4", D6 / 4), ("6d_{b}（D22）", 6 * DBMIN6), ("15 cm", 15.0)]
OLD6 = [("d/4", D6 / 4), ("8d_{b}", 8 * DBMIN6), ("24d_{bt}（D10）", 24 * DBT6), ("30 cm", 30.0)]
SMAX6 = min(v for _, v in NEW6); SOLD6 = min(v for _, v in OLD6)
SUSE6 = math.floor(SMAX6)
KW, KH = 1040, 420


def _spacing_canvas():
    cv = _Cv(KW, KH)
    x0, wmax, vmax = 300, 560, 40.0
    sc = lambda v: wmax * v / vmax
    y = 40
    cv.text_px(40, y, "現行 18.6.4.4（主線）", 14, color=C["deform"], anchor="start", weight="700")
    y += 22
    for lab, v in NEW6:
        ctrl = abs(v - SMAX6) < 1e-9
        cv.math_px(x0 - 12, y + 11, lab, 13, color=C["text"], anchor="end")
        cv.rect_px(x0, y, sc(v), 22, C["load"] if ctrl else C["deform"], rx=3)
        cv.text_px(x0 + sc(v) + 8, y + 11, f"{v:.2f}" + ("　← 控制 → @%d cm" % SUSE6 if ctrl else ""), 12.5,
                   color=C["load"] if ctrl else C["text"], anchor="start", weight="700" if ctrl else "400")
        y += 30
    y += 14
    cv.text_px(40, y, "401-100（考卷指定，舊）", 14, color=C["member2"], anchor="start", weight="700")
    y += 22
    for lab, v in OLD6:
        ctrl = abs(v - SOLD6) < 1e-9
        cv.math_px(x0 - 12, y + 11, lab, 13, color=C["text"], anchor="end")
        cv.rect_px(x0, y, sc(v), 22, C["member2"], rx=3)
        cv.text_px(x0 + sc(v) + 8, y + 11, f"{v:.2f}" + ("　← 控制 → @15（舊解）" if ctrl else ""), 12.5, color=C["text"], anchor="start")
        y += 30
    y += 10
    cv.rect_px(x0, y, sc(SSTR6), 22, C["sfd"], rx=3)
    cv.text_px(x0 - 12, y + 11, "強度需求", 13, color=C["text"], anchor="end")
    cv.text_px(x0 + sc(SSTR6) - 8, y + 11, f"{SSTR6:.2f}（不控制）", 12.5, color="#FFFFFF", anchor="end", weight="700")
    cv.text_px(KW / 2, KH - 18, f"V_e＝{VE6:.2f} tf、地震剪力比 {(MN6+MP6)/7.5/VE6:.3f}＜0.5 → 可計 V_c；塑鉸區自柱面 2h＝{2*H6:.0f} cm，第一支 ≤ 5 cm", 12.5, color=C["muted"])
    return cv


def fig2_spacing():
    return compose([_spacing_canvas()], title=f"{TAG} 圖 2　塑鉸區箍筋間距上限：現行 6db 控制（cm）",
                   sub="3 股 D10；強度需求間距遠大於構造上限，答案由構造上限決定",
                   note="攔：沿用 401-100 的 8db／24dbt／30 cm（得 15 cm）；6db 誤用頂筋 D29")


def check_solution():
    for name, got, want, tol in [("Mpr-", MN6, 57.97, 0.006), ("Mpr+", MP6, 36.17, 0.006), ("Ve", VE6, 25.30, 0.006),
                                 ("s_str", SSTR6, 39.75, 0.02), ("smax", SMAX6, 13.32, 1e-9), ("use", SUSE6, 13, 0),
                                 ("old", SOLD6, 15.75, 1e-9)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-spacing", fig2_spacing, "沿用舊規範 8d_b／30 cm；6d_b 用錯鋼筋"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
