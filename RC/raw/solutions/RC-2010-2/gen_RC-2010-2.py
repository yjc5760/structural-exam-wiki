#!/usr/bin/env python3
"""
RC-2010-2 耐震柱縱筋搭接 — 題目附圖重繪腳本

用法：python3 gen_RC-2010-2.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2010-2-problem.md §4 判讀清單（已確認）。只畫考卷給的東西。
考卷只標 50 cm 與 9.3 cm 淨間距；其餘位置依考卷附圖比例示意，不標尺寸。
FIGURES
  fig-1-problem  柱斷面（上層／下層 D29 並排搭接）  攔：上下層鋼筋認反、9.3 cm 讀成中心距
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2010-2"

# ── 判讀清單（RC-2010-2-problem.md §4，已確認）──
B = 50.0                 # #1
DB = 2.87                # 註：D29
CLR = 9.3                # #3 下排相鄰兩根（下層）主筋淨距
CC_MID = CLR + DB        # 中間兩根中心距
# 以下依考卷附圖比例示意（500 dpi 量得，未標尺寸）
CORNER = 9.6             # 角筋中心距柱面
HOOP = 4.5               # 外箍距柱面
SPLIT = 34.2             # 兩支內箍的分隔線位置（距左面／距上面）
OPEN_OFF = 2.3           # 上層鋼筋（空心）緊貼下層鋼筋外側的偏移


def bar_positions():
    xs = [CORNER, B / 2 - CC_MID / 2, B / 2 + CC_MID / 2, B - CORNER]
    pts = [(x, B - CORNER) for x in xs] + [(x, CORNER) for x in xs]
    for y in (B / 2 + CC_MID / 2, B / 2 - CC_MID / 2):
        pts += [(CORNER, y), (B - CORNER, y)]
    return pts


def outward(p):
    """空心筋相對實心筋的外側方向：角筋取對角，邊筋取法線。"""
    x, y = p
    dx = -1 if x < B / 2 - 1 else (1 if x > B / 2 + 1 else 0)
    dy = -1 if y < B / 2 - 1 else (1 if y > B / 2 + 1 else 0)
    near_x = min(x, B - x) < 12
    near_y = min(y, B - y) < 12
    if near_x and near_y:
        k = 0.7071
        return (dx * k, dy * k)
    return (dx, 0) if near_x else (0, dy)


def fig1_problem():
    W, H = 700, 700
    s = 7.0
    cv = Canvas(W, H, sx=s, ox=84, oy=150)
    cv.panel("耐震柱斷面（重繪）", "依題目正本判讀清單 #1–#4；只有 50 與 9.3 有尺寸")
    cv.polygon([(0, 0), (B, 0), (B, B), (0, B)], "#EDF1F6", C["member"], 2.6)
    # 外箍與兩支內箍
    cv.polygon([(HOOP, HOOP), (B - HOOP, HOOP), (B - HOOP, B - HOOP), (HOOP, B - HOOP)], "none", C["deform"], 2.0)
    a, b = HOOP + 0.8, B - HOOP - 0.8
    cv.poly([(a, a), (SPLIT, a), (SPLIT, b), (a, b), (a, a)], C["accent"], 1.8, dash="6 3")
    cv.poly([(a, B - SPLIT), (b, B - SPLIT), (b, b), (a, b), (a, B - SPLIT)], C["accent"], 1.8, dash="2 3")
    r = DB / 2
    pts = bar_positions()
    for p in pts:
        ux, uy = outward(p)
        cv.circle((p[0] + ux * OPEN_OFF, p[1] + uy * OPEN_OFF), r, "#FFFFFF", C["member"], 1.6)
    for p in pts:
        cv.circle(p, r, C["member"], C["member"], 1.0)
    # 標註
    xr, yr = B - CORNER, B / 2 + CC_MID / 2
    cv.line((xr + OPEN_OFF + r, yr), (B + 6, yr + 3), C["muted"], 1)
    cv.text((B + 7, yr + 3), "D29 上層鋼筋（空心）", 13, C["text"], "start")
    cv.line((xr + r, yr - CC_MID), (B + 6, yr - CC_MID - 3), C["muted"], 1)
    cv.text((B + 7, yr - CC_MID - 3), "D29 下層彎折鋼筋（實心）", 13, C["text"], "start")
    cv.line((B * 0.3, B - HOOP), (B * 0.3 - 3, B + 4), C["muted"], 1)
    cv.text((B * 0.3 - 3, B + 5.5), "D13 @ 10 cm", 13, C["text"])
    x2, x3 = B / 2 - CC_MID / 2 + r, B / 2 + CC_MID / 2 - r
    for xx in (x2, x3):
        cv.line((xx, CORNER - r), (xx, -4), C["dim"], 1, dash="3 3")
    cv.dim((x2, -3.5), (x3, -3.5), "9.3 cm", off=0, label_off=13)
    cv.text((B / 2, -8.0), "淨間距", 12.5, C["muted"])
    cv.dim((0, -12), (B, -12), "50 cm", off=0, label_off=13)
    for xx in (0, B):
        cv.line((xx, -0.5), (xx, -12.5), C["dim"], 1, dash="3 3")
    cv.dim((0, B), (0, 0), "50 cm", off=26, label_off=26)
    cv.legend(40, H - 52, [(C["deform"], "外圍閉合箍筋"), (C["accent"], "內箍（兩支，135° 彎鉤）")])
    return compose([cv], title=f"{TAG} 題目附圖（重繪）",
                   sub="柱 50×50 cm；D29 下層柱 12 根（實心）伸入上層、上層柱 12 根（空心）並排搭接；D13 @ 10 cm",
                   note="9.3 cm 是下排相鄰兩根下層主筋的淨距；保護層考卷未給",
                   path=os.path.join(OUT, f"{TAG}-fig-1-problem.svg"))


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "上下層鋼筋認反、9.3 cm 讀成中心距")]

# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-14 補繪；數值取自 RC-2010-2.md §4 Part 二 Step 1–6，已驗證：盲解一致）
# ══════════════════════════════════════════════════════════
import math
from structdraw import Canvas, C, compose
FY, FC, DB = 4200.0, 280.0, 2.87
LD = FY / (3.5 * math.sqrt(FC)) * DB / 2.5   # Step 5：(c_b＋K_tr)/d_b 取上限 2.5 → 82.3 cm
LS = 1.3 * LD                                 # Step 6：乙級 → 107 cm
RHO = 12 * 6.469 / (50 * 50)                  # 每組 12-D29：3.1%
LN_DEMO = 300.0                               # 柱淨高：考卷未給，示意 3 m
COL_B = 50.0


def fig2_lap_elevation():
    W, H = 560, 660
    s = 1.12
    a = Canvas(W, H, sx=s, ox=W / 2 - COL_B * s / 2 - 30, oy=150)
    a.panel("柱立面：搭接位置與長度", "淨高為示意（考卷未給）；搭接長度依解題算出")
    for y0 in (-40.0, LN_DEMO):
        a.polygon([(-60, y0), (COL_B + 60, y0), (COL_B + 60, y0 + 40), (-60, y0 + 40)], "#DCE3EC", C["member"], 2.0)
    a.polygon([(0, 0), (COL_B, 0), (COL_B, LN_DEMO), (0, LN_DEMO)], "#EDF1F6", C["member"], 2.2)
    mid0, mid1 = LN_DEMO / 4, 3 * LN_DEMO / 4
    a.polygon([(0, mid0), (COL_B, mid0), (COL_B, mid1), (0, mid1)], C["fill_m"], C["bmd"], 1.8)
    y0 = (LN_DEMO - LS) / 2
    y1 = y0 + LS
    for x in (9.0, COL_B - 9.0):
        k = 1 if x < COL_B / 2 else -1
        a.poly([(x, -40), (x, y0 - 12), (x + 3.2 * k, y0), (x + 3.2 * k, y1)], C["member"], 2.6)
        a.line((x, y0), (x, LN_DEMO + 40), C["load"], 2.6)
    yy = y0
    while yy <= y1 + 0.1:
        a.line((4, yy), (COL_B - 4, yy), C["deform"], 1.4)
        yy += 10.0
    a.dim((COL_B + 8, y1), (COL_B + 8, y0), f"l_s = {LS:.0f} cm", off=-10, label_off=-46, size=13)
    a.dim((-8, mid1), (-8, mid0), "l_n/2", off=-10, label_off=24, size=13)
    a.text((COL_B + 85, LN_DEMO + 18), "上層柱 D29（直）", 12.5, C["load"], weight="700")
    a.text((COL_B + 85, -18), "下層柱 D29（彎折伸入）", 12.5, C["member"], weight="700")
    a.text_px(W / 2, H - 70, f"l_d＝4200/(3.5√280)×2.87/2.5＝{LD:.1f} cm", 13.5, C["text"], weight="700")
    a.text_px(W / 2, H - 44, f"乙級（全數同斷面搭接）：l_s＝1.3 l_d＝{LS:.0f} cm", 13.5, C["bmd"], weight="700")
    a.text_px(W / 2, H - 20, "搭接段全長 D13 @ 10 cm 圍封（比照圍束區）", 12.5, C["deform"])

    b = Canvas(W, H)
    b.panel("㈠ 規範要求的「面積」是縱筋比", "§18.4.4.1：0.01A_g ≤ A_{st} ≤ 0.06A_g；柱沒有「同斷面搭接 ≤ 50%」")
    x0, x1 = 120, W - 60
    vmax = 0.07
    def X(v): return x0 + (x1 - x0) * v / vmax
    rows = (("每組 12-D29", RHO, C["member"]), ("搭接段兩組並排", 2 * RHO, C["load"]))
    for i, (name, v, col) in enumerate(rows):
        y = 190 + i * 110
        b.rect_px(x0, y, X(v) - x0, 36, col, rx=6)
        b.text_px(x0 - 10, y + 18, name, 13, col, anchor="end", weight="700")
        b.text_px(X(v) + 8, y + 18, f"{v * 100:.1f}%", 14, col, anchor="start", weight="700")
    for v, lab in ((0.01, "1%"), (0.06, "6%")):
        b.line((X(v), H - 165), (X(v), H - 380), C["bmd"], 1.8, dash="6 4")
        b.text_px(X(v), 148, f"{lab}", 13, C["bmd"], weight="700")
    b.text_px(W / 2, 450, "6% 上限針對 A_{st}；搭接段鋼筋加倍，須檢討淨間距與澆置", 13, C["text"], weight="700")
    b.text_px(W / 2, H - 44, "搭接比例只影響甲／乙級，不是「超過 50% 就要改機械續接」", 13, C["load"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-lap.svg")
    compose([a, b], title=f"{TAG} 圖 2　耐震柱縱筋搭接：位置、長度與鋼筋比",
            sub="柱 50×50；D29 下層 12 根＋上層 12 根同斷面搭接；f'c＝280、fy＝4200；D13 @ 10 cm",
            note="搭接只能在柱中段 l_n/2，拉力搭接；淨高考卷未給，左圖淨高為示意",
            path=path)
    return path


FIGURES.append((fig2_lap_elevation, "§4 Part 一／Step 6", "搭接放在柱端、把「面積」答成 50% 搭接限制、l_s 忘了乘 1.3"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, where, catches in FIGURES:
        out = fn()
        print(os.path.basename(out) if out and len(out) < 300 else f"{TAG}-fig-1-problem.svg", "→", where, "攔：", catches)
