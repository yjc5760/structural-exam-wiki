#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2019-3 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2019-3-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2019-3.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-3 批 2＋U1-3＋U2-3 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2019-3"

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


# ── 題目附圖重繪（題目正本 RC-2019-3-problem.md §4）──
P_L = 500.0          # #4 平面 500×500 cm
P_T = 18.0           # #4 厚 18 cm
P_S = 25.0           # #5 撓曲筋 #4@25 雙層雙向
PW, PH = 560, 470


def panel_plan():
    cv = Canvas(PW, PH, sx=0.56, ox=130, oy=120)
    _rect(cv, 0, 0, P_L, P_L)
    for y in (P_L + 40, -40):                             # V_u,X：平行 X 向兩邊（方向示意）
        cv.double_arrow((120, y), (380, y), C["load"], 2.6)
    for x in (-45, P_L + 45):                             # V_u,Y：平行 Y 向兩邊
        cv.double_arrow((x, 120), (x, 380), C["load"], 2.6)
    cv.math((250, P_L + 75), "V_{u,X} = 100 tf", 14, color=C["load"])
    cv.math((P_L + 60, 250), "V_{u,Y} = 100 tf", 14, color=C["load"], anchor="start")
    cv.dim((0, 0), (P_L, 0), "500", off=62, label_off=13)
    cv.axes((-110, -110), 70, 70, labels=("X", "Y"))
    cv.text((P_L / 2, P_L / 2 + 20), "橫膈版平面", 14)
    cv.text((P_L / 2, P_L / 2 - 20), "受剪斷面 A_{cv}＝500×18（每一方向）", 12.5, color=C["muted"])
    cv.text((P_L / 2, -190), "長度單位 cm；雙向箭頭示剪力方向（地震往復）", 12.5, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=4.4, ox=60, oy=170)
    w = 100.0                                             # 取 100 cm 寬示意
    _rect(cv, 0, 0, w, P_T)
    cov = 3.0                                             # 保護層考卷未給（示意）
    for k in range(5):
        x = 12.5 + P_S * k
        if x < w:
            _bar(cv, (x, cov + 1.9), 0.64)                # 下層（垂直紙面方向）
            _bar(cv, (x, P_T - cov - 1.9), 0.64)          # 上層
    cv.line((0, cov + 0.6), (w, cov + 0.6), C["member"], 2.2)        # 下層（沿紙面方向）
    cv.line((0, P_T - cov - 0.6), (w, P_T - cov - 0.6), C["member"], 2.2)
    cv.udl((0, P_T), (w, P_T), 9, n=9)
    cv.math((w / 2, P_T + 13.5), "1.2W_{D} + 1.0W_{L}", 14, color=C["load"])
    cv.text((w / 2, P_T + 17.5), "垂直設計荷重", 12.5, color=C["load"])
    cv.dim((w, 0), (w, P_T), "18", off=30, label_off=16)
    cv.dim((12.5, 0), (37.5, 0), "25", off=26, label_off=13)
    cv.text((w / 2, -12), "版斷面（取 1 m 寬示意）：撓曲筋 #4@25", 13)
    cv.text((w / 2, -17), "上下雙層、X／Y 雙向、等間距；f_y＝2800、f'c＝280", 12.5, color=C["muted"])
    cv.text((w / 2, -22), "最終間距＝撓曲＋抗剪鋼筋合計（判讀 #1）", 12.5, color=C["accent"])
    return cv


def fig1_problem():
    return compose([panel_plan(), panel_sec()], title=f"{TAG} 題目附圖（橫膈版重繪）",
                   sub="依題目正本判讀清單 #1–#6；保護層、剪力箭頭位置為示意",
                   note="φ＝0.6（題給）；ρt 取平行於剪力方向的分布鋼筋（雙層合計）")


FIGURES = [("1-problem", fig1_problem, "最終間距只取撓曲與剪力較小者（應合計）；A_cv 取版面積")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2；數值由常數現算，檔尾對 §4 assert）══
from structdraw import Canvas as _Cv
AB9, T9, L9, FY9, VU9, PHI9 = 1.27, 18.0, 500.0, 2800.0, 100000.0, 0.6
ACV9 = T9 * L9
VC9 = 0.53 * math.sqrt(280.0)
RHO9 = (VU9 / (PHI9 * ACV9) - VC9) / FY9               # §4.2
SH9 = RHO9 * ACV9 / L9                                 # 抗剪 cm²/cm（雙層合計）
FL9 = 2 * AB9 / 25                                     # 撓曲 #4@25 雙層
S9 = 2 * AB9 / (FL9 + SH9)                             # §4.4
SUSE9 = math.floor(S9)
PROV9 = 2 * AB9 / SUSE9
PHIVN9 = PHI9 * (VC9 + (PROV9 - FL9) / T9 * FY9) * ACV9
GW, GH = 1040, 330


def fig2():
    return compose([fig2_steel_canvas()], title=f"{TAG} 圖 2　最終鋼筋量＝撓曲＋抗剪（不是兩者取小）",
                   sub="同一組合 1.2D＋1.0L±1.0E 下，重力撓曲已用掉 #4@25，面內剪力的拉桿要另外加",
                   note="攔：最終間距取 min(撓曲 25, 抗剪 40.9)＝25（把撓曲筋重複當抗剪筋）")


def fig2_steel_canvas():
    cv = _Cv(GW, GH)
    x0, wmax, vmax = 300, 600, 0.18
    sc = lambda v: wmax * v / vmax
    rows = [("需求：撓曲＋抗剪（主線）", [(FL9, C["bmd"], f"撓曲 {FL9:.4f}"), (SH9, C["sfd"], f"抗剪 {SH9:.4f}")], f"＝{FL9+SH9:.4f}"),
            (f"提供：#4@{SUSE9} 雙層", [(PROV9, C["deform"], f"{PROV9:.4f}")], f"需 s ≤ {S9:.1f} → {SUSE9} ✓"),
            ("舊解 #4@25（取小）", [(FL9, C["member2"], f"{FL9:.4f}")], "抗剪被重複計算（不足）")]
    for i, (lab, segs, tail) in enumerate(rows):
        y = 50 + i * 80
        cv.text_px(x0 - 12, y + 15, lab, 13.5, color=C["text"], anchor="end")
        x = x0
        for v, col, t in segs:
            cv.rect_px(x, y, sc(v), 30, col, rx=3)
            cv.text_px(x + sc(v) / 2, y + 15, t, 12.5, color="#FFFFFF", weight="700")
            x += sc(v)
        cv.text_px(x + 8, y + 15, tail, 13, color=C["load"] if i != 1 else C["deform"], anchor="start", weight="700")
    cv.text_px(GW / 2, 282, f"單位 cm²/cm（每 cm 版寬、上下雙層合計）；ρ_t＝{RHO9:.6f}，A_{{cv}}＝18×500", 12.5, color=C["muted"])
    cv.text_px(GW / 2, 306, f"@{SUSE9} 驗算：扣撓曲後 ρ_t＝{(PROV9-FL9)/T9:.6f} → φV_n＝{PHIVN9/1e3:.1f} tf ≥ 100 ✓", 12.5, color=C["muted"])
    return cv


def check_solution():
    for name, got, want, tol in [("rho", RHO9, 0.003446, 1e-6), ("shear", SH9, 0.0620, 5e-5), ("flex", FL9, 0.1016, 1e-9),
                                 ("s", S9, 15.5, 0.05), ("use", SUSE9, 15, 0), ("phVn", PHIVN9 / 1e3, 104.8, 0.05)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-steel", fig2, "最終間距取撓曲與抗剪較小者（應相加）"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
