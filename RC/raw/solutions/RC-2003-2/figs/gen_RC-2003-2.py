#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2003-2 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2003-2-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2003-2.py [輸出目錄，預設 figs]
（2026-11-15，RC-U3-3 批 2＋U1-3＋U2-3 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2003-2"

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


# ── 題目附圖重繪（題目正本 RC-2003-2-problem.md §4）──
P_B = 60.0            # #6 斷面 60×60
P_COV = 4.0           # #3 淨保護層 4 cm（至 #4 箍筋外緣）
P_DH = 1.27           # #4 箍筋 d_b
P_DB = 2.87           # #9 d_b
P_N = 5               # #7 每面 5 根，共 16
P_LN = 300.0          # #5 柱淨高 300 cm
PW, PH = 560, 520


def panel_elev():
    cv = Canvas(PW, PH, sx=0.95, ox=230, oy=95)
    hb = 70.0                                          # 梁深考卷未標（示意）
    _rect(cv, 0, -60, P_B, P_LN + hb + 60)
    for y0 in (-hb, P_LN):
        _rect(cv, -150, y0, 0, y0 + hb)
        _rect(cv, P_B, y0, P_B + 150, y0 + hb)
    cv.dim((-150, 0), (-150, P_LN), "300 cm", off=-30, label_off=-26)
    cv.text((P_B / 2, P_LN / 2), "柱", 15, weight="700")
    cv.text((P_B + 18, 25), "A-A", 13, color=C["muted"], anchor="start")
    cv.text((P_B / 2, -hb - 45), "立面：柱淨高 300 cm（上梁底至下梁頂）；梁深為示意", 12.5, color=C["muted"])
    return cv


def panel_sec():
    cv = Canvas(PW, PH, sx=5.0, ox=80, oy=120)
    _rect(cv, 0, 0, P_B, P_B)
    c = P_COV + P_DH / 2
    _hoop(cv, c, P_B, P_B, w=2.2)
    cv.line((P_B / 2, c), (P_B / 2, P_B - c), C["member"], 1.8)
    cv.line((c, P_B / 2), (P_B - c, P_B / 2), C["member"], 1.8)
    e = P_COV + P_DH + P_DB / 2
    bars = _ring_bars(cv, P_B, P_B, e, P_N, P_DB / 2)
    assert len(bars) == 16
    cv.dim((0, P_B), (P_B, P_B), "60 cm", off=-28, label_off=-14)
    cv.dim((0, 0), (0, P_B), "60 cm", off=-34, label_off=-24)
    cv.dim((P_B, 0), (P_B, P_COV), "4", off=-22, label_off=-12)
    cv.text((P_B + 7, P_B - 6), "#4@10 cm", 13, anchor="start")
    cv.text((P_B + 7, P_B - 11), "（閉合箍＋十字繫筋）", 12, color=C["muted"], anchor="start")
    cv.text((P_B + 7, 14), "16-#9", 13, anchor="start")
    cv.text((P_B + 7, 9), "（每面 5 根）", 12, color=C["muted"], anchor="start")
    cv.text((P_B / 2, -9), "斷面 A-A：淨保護層 4 cm 量到箍筋外緣", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_elev(), panel_sec()], title=f"{TAG} 題目附圖（圖 3 重繪）",
                   sub="依題目正本判讀清單 #3–#8；梁深、繫筋彎鉤細節為示意",
                   note="f'c＝280（常重）、fy＝4200（未塗布，主筋與箍筋同）；搭接類別考卷未給")


FIGURES = [("1-problem", fig1_problem, "保護層量到主筋；300 cm 當層高")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2；數值由常數現算，檔尾對 §4 assert）══
from structdraw import Canvas as _Cv
LN3, DB3, FC3, FY3 = 300.0, 2.87, 280.0, 4200.0
LD3 = FY3 / (3.5 * math.sqrt(FC3)) * DB3 / 2.5          # §4 Step 5（(c+Ktr)/db 取 2.5）
LST3 = 1.3 * LD3
LUSE3 = math.ceil(LST3 / 10) * 10
Z0, Z1 = LN3 / 4, 3 * LN3 / 4
S0, S1 = LN3 / 2 - LUSE3 / 2, LN3 / 2 + LUSE3 / 2
LO3 = max(60.0, LN3 / 6, 45.0)                           # 圍束區 ℓo（示意）
EW, EH = 620, 560


def _elev():
    cv = _Cv(EW, EH, sx=1.45, ox=230, oy=60)
    cv.panel(None)
    w = 60
    cv.polygon([(-w / 2, 0), (w / 2, 0), (w / 2, LN3), (-w / 2, LN3)], "#EDF1F6", stroke=C["member"], w=2)
    for y in (0, LN3):
        cv.polygon([(-110, y if y else -20), (110, y if y else -20), (110, y + 20 if y else 0), (-110, y + 20 if y else 0)], "#C9D1DC", stroke=C["member"], w=2)
    cv.polygon([(-w / 2, Z0), (w / 2, Z0), (w / 2, Z1), (-w / 2, Z1)], C["fill_m"])
    for y0, y1 in ((0, LO3), (LN3 - LO3, LN3)):
        cv.polygon([(-w / 2, y0), (w / 2, y0), (w / 2, y1), (-w / 2, y1)], C["fill_c"])
    cv.line((-6, 0), (-6, S1), C["member"], 3, cap="butt")          # 下柱伸出筋：止於搭接終點
    cv.line((6, S0), (6, LN3), C["member"], 3, cap="butt")           # 上柱筋：起於搭接起點
    cv.poly([(-14, S0), (14, S0), (14, S1), (-14, S1), (-14, S0)], C["load"], 2.4)
    cv.dim((w / 2, S0), (w / 2, S1), f"{LUSE3:.0f}", off=26, label_off=18)
    for y, t in ((Z0, f"{Z0:.0f}（中央半段下限）"), (Z1, f"{Z1:.0f}（中央半段上限）"), (S0, f"{S0:.0f} 搭接起點"), (S1, f"{S1:.0f} 搭接終點")):
        cv.line((-w / 2 - 6, y), (-w / 2 - 30, y), C["dim"], 1.4)
        cv.text((-w / 2 - 34, y), t, 12.5, color=C["accent"] if "搭接" in t else C["bmd"], anchor="end")
    cv.text((w / 2 + 70, LN3 / 2), "乙級拉力搭接", 13, color=C["load"], anchor="start", weight="700")
    cv.text((w / 2 + 70, LN3 / 2 - 18), f"1.3ℓd＝1.3×{LD3:.1f}", 12.5, color=C["load"], anchor="start")
    cv.text((w / 2 + 70, LN3 / 2 - 34), f"＝{LST3:.1f} → {LUSE3:.0f} cm", 12.5, color=C["load"], anchor="start")
    cv.text((w / 2 + 70, LO3 / 2), "兩端圍束區（示意）", 12, color=C["deform"], anchor="start")
    cv.text((0, -34), f"柱淨高 {LN3:.0f} cm（下梁頂起算）", 12.5, color=C["muted"])
    cv.text((0, LN3 + 34), "上梁", 12.5, color=C["muted"])
    return cv


def fig2_lap():
    return compose([_elev()], title=f"{TAG} 圖 2　耐震柱搭接位置：中央半段內、置中",
                   sub="綠底＝18.7.4.3 允許搭接的柱淨高中央半段；紅線＝搭接區；數值取自 §4",
                   note="攔：把搭接放在柱端（圍束區、塑鉸區）；用受壓搭接或把 ℓdc＝54 當搭接長度")


def check_solution():
    for name, got, want, tol in [("ld", LD3, 82.3, 0.05), ("lst", LST3, 107.0, 0.05), ("use", LUSE3, 110, 0),
                                 ("S0", S0, 95, 1e-9), ("S1", S1, 205, 1e-9), ("Z0", Z0, 75, 1e-9), ("Z1", Z1, 225, 1e-9)]:
        assert abs(got - want) <= tol, (name, got, want)
    assert Z0 <= S0 and S1 <= Z1
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-lap", fig2_lap, "搭接放在柱端；受壓搭接；ℓdc 當搭接長度"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
