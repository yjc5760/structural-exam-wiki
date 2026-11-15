#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2025-4 解題圖解腳本（Magnel 圖／偏心可行區）

2026-11-15 圖解補繪 DIAG-RC-U4-2-B1。數值由題目常數現算，檔尾 check_solution() 對解析 §4 assert。
用法（在題目資料夾執行）：python figs/gen_RC-2025-4.py [輸出目錄，預設 figs]
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2025-4"

# ── 題目常數（題目正本 §1／§2）與解析 §4 採用的假設 ──
B, H, L = 40.0, 120.0, 12.0                    # 斷面 cm、跨度 m
FCI, FC, ETA, PI, WL = 320.0, 420.0, 0.85, 200.0, 1.5   # kgf/cm²、f_pe/f_pi、P_i tf、活載 tf/m
GAM = 2.4                                         # 單位重 tf/m³（題文未提自重，§1 假設計入）
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
E_FT0 = -Z / A + MT / (ETA * PI * 1000)                          # 使用拉應力取 0 的下限（§5 對照）
E_OLD_UP = Z / A + (MG + 0.5 * math.sqrt(FCI) * Z) / (PI * 1000)  # 舊解 0.5√f'ci 的上限（§5 對照）

MW, MH = 760, 420
LBL = {1: (66.0, 3.6, "start"), 3: (-39.0, 3.1, "start")}                     # 線名標註位置 (e, y, 錨點)；未列者標在線段末端
PI_LBL = "left"
EX0, EX1, YY0, YY1 = -40.0, 90.0, 0.0, 10.0
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
    for e, lab in ((E_FT0, f"f_{{t}}＝0：{E_FT0:.2f}"), (E_OLD_UP, f"舊 0.5√f'ci：{E_OLD_UP:.2f}")):
        cv.dot(P(e, Y_PI), 4.5, fill="#FFFFFF", stroke=C["member2"], w=1.8)
        cv.text((P(e, Y_PI)[0], P(e, Y_PI)[1] - 16), lab, 11.5, color=C["muted"])
    cv.line(P(EX0, Y_PI), P(EX1, Y_PI), C["text"], 1.4, dash="6 4")
    cv.text((PX1 - 4 if PI_LBL == "right" else PX0 + 6, P(EX0, Y_PI)[1] + (-12 if PI_LBL == "right" else 12)), f"P_{{i}}＝{PI:.0f} tf", 12, color=C["text"], anchor="end" if PI_LBL == "right" else "start", weight="700")
    for e in (E_LO, E_UP):
        cv.dot(P(e, Y_PI), 5.5, fill=C["bmd"])
    cv.line(P(E_LO, Y_PI), P(E_UP, Y_PI), C["bmd"], 5)
    cv.text_px(MW / 2, MH - 17, f"P_{{i}}＝{PI:.0f} tf：{E_LO:.2f} ≤ e ≤ {E_UP:.2f} cm（上限 ① 傳遞頂拉、下限 ③ 使用底拉）", 13, color=C["bmd"], weight="700")
    return cv


def fig1_magnel():
    return compose([panel_magnel()],
                   title=f"{TAG} 圖 1　跨中偏心可行區（Magnel 圖）",
                   sub="kgf 制：傳遞拉 0.8√f'ci＝14.31、U 類 2.0√f'c＝40.99、壓 0.60f'ci、0.60f'c；自重以 2.4 tf/m3 計入（假設）",
                   note="攔：傳遞拉用 0.5√f'ci（kgf 制無此係數）；使用拉應力取 0；漏計自重")


def check_solution():
    for name, got, want, tol in [("e up", E_UP, 37.24, 0.005), ("e lo", E_LO, -15.07, 0.005), ("ft0", E_FT0, 8.08, 0.005),
                                 ("cond2", e_line(LINES[1][1], LINES[1][2], Y_PI), 82.53, 0.005)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES = [("1-magnel", fig1_magnel, "傳遞拉用 0.5 倍係數；使用拉應力取 0；漏自重")]


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"RC-2025-4-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
