#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2010-4 解題圖解腳本（Magnel 圖／偏心可行區）

2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；2026-11-20 FIX-RC-2010-4：直線鋼腱改用一般位置傳遞拉應力限值。數值由題目常數現算，檔尾 check_solution() 對解析 §4 assert。
用法（在題目資料夾執行）：python figs/gen_RC-2010-4.py [輸出目錄，預設 figs]
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2010-4"

# ── 題目常數（題目正本 §1／§2）與解析 §4 採用的假設 ──
B, H, L = 50.0, 90.0, 15.0                     # 斷面 cm、跨度 m
FCI, FC, ETA, PI, WL = 280.0, 350.0, 0.85, 200.0, 1.5   # kgf/cm²、f_pe/f_pi、P_i tf、活載 tf/m
GAM = 2.4                                         # 單位重 tf/m³（考卷未給，§4 假設）
A = B * H; Z = B * H ** 2 / 6                      # cm²、cm³（矩形）
MG = B * H / 1e4 * GAM * L ** 2 / 8 * 1e5           # 自重彎矩 kgf·cm（單位重 GAM tf/m³）
ML = WL * L ** 2 / 8 * 1e5
MT = MG + ML
FTI = 0.8 * math.sqrt(FCI); FTI_END = 1.6 * math.sqrt(FCI)   # kgf 制傳遞拉
FCI_A = 0.60 * FCI; FT = 2.0 * math.sqrt(FC); FC_A = 0.60 * FC  # U 類拉、使用壓（全部載重）
# 四條件寫成 e＝c0＋c1·y，y＝1000/P_i（1/tf）；P 以 kgf 計時 1/P＝y/1e6
LINES = [
    ("① 傳遞頂拉", Z / A, (MG + FTI * Z) / 1e6, "le", C["load"]),
    ("② 傳遞底壓", -Z / A, (FCI_A * Z + MG) / 1e6, "le", C["accent"]),
    ("③ 使用底拉", -Z / A, (MT - FT * Z) / (ETA * 1e6), "ge", C["deform"]),
    ("④ 使用頂壓", Z / A, (MT - FC_A * Z) / (ETA * 1e6), "ge", C["sfd"]),
]
Y_PI = 1000.0 / PI                                  # 1000/P_i（P_i 以 tf 計）
def e_line(c0, c1, y): return c0 + c1 * y
E_UP = min(e_line(c0, c1, Y_PI) for _n, c0, c1, k, _c in LINES if k == "le")
E_LO = max(e_line(c0, c1, Y_PI) for _n, c0, c1, k, _c in LINES if k == "ge")
# ㈠ 等偏心直線鋼腱：梁端無自重彎矩，且離端約 1.2 m 內都無足夠自重彎矩 → 用一般位置頂拉限 0.8√f'ci
#    （簡支端部放寬 1.6√f'ci 只適用很短的端部範圍，字面套用得 24.04 cm，見解析 §5 ⑥）→ e＝Z/A＋FTI·Z/P_i
ST_C0, ST_C1 = Z / A, FTI * Z / 1e6
E_ST_END = Z / A + FTI_END * Z / (PI * 1000)
E_ST = e_line(ST_C0, ST_C1, Y_PI)
def m_cap(e): return Z * (ETA * PI * 1000 / A + ETA * PI * 1000 * e / Z + FT) - MG   # 使用底拉控制的外加彎矩 kgf·cm
ML_ST, ML_CU = m_cap(E_ST) / 1e5, m_cap(E_UP) / 1e5
ETA_MG = ETA * MG / 1e5

MW, MH = 760, 420
LBL = {0: (33.0, 3.0, "start"), 2: (10.0, 7.5, "end"), 3: (-29.0, 6.3, "start")}                     # 線名標註位置 (e, y, 錨點)；未列者標在線段末端
PI_LBL = "right"
EX0, EX1, YY0, YY1 = -30.0, 70.0, 0.0, 10.0
PX0, PX1, PY0, PY1 = 90, 700, 70, 360               # 繪圖框（y 向上）
def P(e, y): return (PX0 + (e - EX0) / (EX1 - EX0) * (PX1 - PX0), PY0 + (y - YY0) / (YY1 - YY0) * (PY1 - PY0))


def _clip_line(c0, c1):
    ys = [YY0 + (YY1 - YY0) * i / 200 for i in range(201)]
    return [P(e_line(c0, c1, y), y) for y in ys if EX0 <= e_line(c0, c1, y) <= EX1]


def panel_magnel():
    cv = Canvas(MW, MH)
    cv.panel("Magnel 圖：四個應力條件的可行區（y＝1000/P_i）")
    for e in range(int(EX0), int(EX1) + 1, 10):
        cv.line(P(e, YY0), P(e, YY1), C["border"], 1)
        cv.text((P(e, YY0)[0], PY0 - 14), f"{e}", 11, color=C["muted"])
    for y in range(int(YY0), int(YY1) + 1, 2):
        cv.line(P(EX0, y), P(EX1, y), C["border"], 1)
        cv.text((PX0 - 8, P(EX0, y)[1]), f"{y}", 11, color=C["muted"], anchor="end")
    cv.text_px((PX0 + PX1) / 2, MH - 40, "跨中偏心 e（cm，形心以下為正）", 12, color=C["muted"])
    cv.text_px(PX0 - 40, MH - PY1 - 22, "1000/P_{i}（1/tf）", 12, color=C["muted"], anchor="start")
    feas = []
    ys = [YY0 + 0.2 + (YY1 - YY0 - 0.2) * i / 160 for i in range(161)]
    up = [(min(e_line(c0, c1, y) for _n, c0, c1, k, _c in LINES if k == "le"), y) for y in ys]
    lo = [(max(e_line(c0, c1, y) for _n, c0, c1, k, _c in LINES if k == "ge"), y) for y in ys]
    pts = [(e, y) for (e, y), (l, _) in zip(up, lo) if e >= l] + [(l, y) for (e, y), (l, _) in reversed(list(zip(up, lo))) if e >= l]
    pts = [(min(max(e, EX0), EX1), y) for e, y in pts]
    if pts:
        cv.polygon([P(*p) for p in pts], C["fill_m"])
    for i, (nm, c0, c1, k, col) in enumerate(LINES):
        seg = _clip_line(c0, c1)
        if len(seg) > 1:
            cv.poly(seg, col, 2.2)
            if i in LBL:
                le, ly_, an = LBL[i]
                cv.text(P(le, ly_), nm, 12, color=col, anchor=an, weight="700")
            else:
                lx, ly = seg[-1]
                cv.text((min(lx, PX1 - 4), min(ly, PY1) - 12), nm, 12, color=col, anchor="end" if lx > PX1 - 120 else "start", weight="700")
    seg = _clip_line(ST_C0, ST_C1)
    cv.poly(seg, C["member2"], 2.0, dash="7 4")
    cv.text(P(*(30.0, 0.45, "start")[:2]), "㈠ 直線鋼腱梁端頂拉（虛線，一般限值）", 12, color=C["member2"], anchor="start", weight="700")
    cv.dot(P(E_ST, Y_PI), 5, fill=C["member2"])
    cv.text((P(E_ST, Y_PI)[0] - 6, P(E_ST, Y_PI)[1] + 14), f"{E_ST:.2f}", 12, color=C["member2"], anchor="end", weight="700")
    cv.line(P(EX0, Y_PI), P(EX1, Y_PI), C["text"], 1.4, dash="6 4")
    cv.text((PX1 - 4 if PI_LBL == "right" else PX0 + 6, P(EX0, Y_PI)[1] + (-12 if PI_LBL == "right" else 12)), f"P_{{i}}＝{PI:.0f} tf", 12, color=C["text"], anchor="end" if PI_LBL == "right" else "start", weight="700")
    for e in (E_LO, E_UP):
        cv.dot(P(e, Y_PI), 5.5, fill=C["bmd"])
    cv.line(P(E_LO, Y_PI), P(E_UP, Y_PI), C["bmd"], 5)
    cv.text_px(MW / 2, MH - 17, f"P_{{i}}＝{PI:.0f} tf：{E_LO:.2f} ≤ e ≤ {E_UP:.2f} cm（上限 ① 傳遞頂拉、下限 ③ 使用底拉）", 13, color=C["bmd"], weight="700")
    return cv


def panel_cmp():
    cv = Canvas(MW, MH)
    cv.panel("㈠ 曲線 vs 等偏心直線鋼腱（P_i＝200 tf）：可承受的外加彎矩")
    rows = [(f"直線鋼腱 e＝{E_ST:.2f}（梁端、一般限值控制）", ML_ST, C["member2"]), (f"曲線鋼腱 e＝{E_UP:.2f}（跨中有自重抵銷）", ML_CU, C["bmd"])]
    x0, sc = 60, 470 / ML_CU
    for i, (lab, v, col) in enumerate(rows):
        y = 280 - i * 110
        cv.text_px(x0, MH - y - 22, lab, 13, anchor="start", weight="700")
        cv.rect_px(x0, MH - y, sc * v, 34, col, rx=4)
        cv.text_px(x0 + sc * v + 10, MH - y + 17, f"M_{{L}}＝{v:.2f} tf·m", 13.5, color=col, anchor="start", weight="700")
    cv.text_px(MW / 2, 300, f"提升 ΔM＝{ML_CU-ML_ST:.1f} tf·m（≈{(ML_CU-ML_ST)*8/L**2:.2f} tf/m，+{100*(ML_CU/ML_ST-1):.0f}%）", 15, color=C["bmd"], weight="700")
    cv.text_px(MW / 2, 330, f"＝ηM_{{G}}＝{ETA_MG:.1f} tf·m：曲線鋼腱跨中多放的偏心恰為 M_{{G}}/P_{{i}}", 12.5, color=C["muted"])
    cv.text_px(MW / 2, 356, f"若梁端套放寬限值 1.6√f'ci：直線 e＝{E_ST_END:.2f}、ΔM＝18.1 tf·m（離端 1.2 m 內超出一般限值）", 12.5, color=C["muted"])
    return cv


def fig1_magnel():
    return compose([panel_magnel(), panel_cmp()], cols=1,
                   title=f"{TAG} 圖 1　跨中偏心可行區（Magnel 圖）與曲線／直線鋼腱比較",
                   sub="kgf 制容許應力：傳遞拉 0.8√f'ci（直線鋼腱梁端也用此值）、U 類 2.0√f'c；壓 0.60f'ci、0.60f'c；單位重 2.4 tf/m3（假設）",
                   note="攔：拉應力取 0（範圍縮成 27.68～30.18）；直線鋼腱當零偏心；SI 係數直接代 kgf")


def check_solution():
    for name, got, want, tol in [("e up", E_UP, 34.71, 0.005), ("e lo", E_LO, 12.83, 0.005), ("e st", E_ST, 19.52, 0.005), ("e st end", E_ST_END, 24.04, 0.005),
                                 ("ML st", ML_ST, 53.56, 0.005), ("ML cu", ML_CU, 79.38, 0.005), ("dM", ML_CU - ML_ST, 25.82, 0.005),
                                 ("etaMG", ETA_MG, 25.8, 0.05)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES = [("1-magnel", fig1_magnel, "拉應力取 0；直線鋼腱當零偏心；SI 係數代 kgf")]


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"RC-2010-4-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
