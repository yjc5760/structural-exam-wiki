#!/usr/bin/env python3
"""
SS-2022-4 強柱弱梁之機率分析 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2022-4.py [輸出目錄]

重繪依據：題目正本 SS-2022-4-problem.md §4 判讀清單（待確認）。
(a) 構架為無尺寸情境示意；(b) 降伏強度分布為考卷給定的均勻分布（端點與高度皆為圖上標示值，
非從曲線讀值），依判讀清單 #1–#3 重繪。不含任何解題結果（機率不畫）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))   # 五科合一後 skill 在根目錄 skills/

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2022-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2022-4-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
DIST = {"鋼材B": (300.0, 400.0, 1 / 100),     # #1 B：300～400 MPa，縱軸 1/100
        "鋼材A": (300.0, 500.0, 1 / 200)}     # #2 A：300～500 MPa，縱軸 1/200（300～400 段畫在 B 之下）
#                                               #3 縱軸為每 MPa 機率密度（面積 = 1）；#6 (a) 無尺寸


def frame_panel():
    W, H, sx = 440, 400, 200
    cv = Canvas(W, H, sx=sx, ox=110, oy=110)
    cv.panel("(a) 門型構架", "兩柱底鉸支；情境示意")
    cv.line((0, 0), (0, 1), C["member"], 4, cap="butt")
    cv.line((1.1, 0), (1.1, 1), C["member"], 4, cap="butt")
    cv.line((0, 1), (1.1, 1), C["member"], 4, cap="butt")
    for x in (0, 1.1):
        cv.support((x, 0), "pin", 0, size=14)
    cv.arrow((-0.45, 1), (-0.03, 1), C["load"], 3, 11)
    cv.text((-0.45, 1), "水平力", 13, C["load"], "start", dy=-16, weight="700")
    cv.text((0.55, 1), "鋼梁", 13, C["text"], dy=-16, weight="700")
    cv.text((1.1, 0.55), "鋼柱", 13, C["text"], "start", dx=12, weight="700")
    return cv


def dist_panel():
    W, H = 440, 400
    sxx, syy = 1.25, 22000.0           # x：每 MPa 像素；y：每單位機率密度像素
    cv = Canvas(W, H, sx=1, ox=0, oy=0)
    cv.panel("(b) 降伏強度分布", "均勻分布；縱軸為每 MPa 機率")
    x0, y0 = 90 - 280 * sxx, 90
    X = lambda v: x0 + v * sxx
    Y = lambda p: y0 + p * syy
    cv.line((X(280), y0), (X(540), y0), C["text"], 1.4)
    cv.line((X(280), y0), (X(280), Y(1 / 100) + 40), C["text"], 1.4)
    a0, a1, ha = DIST["鋼材A"]
    b0, b1, hb = DIST["鋼材B"]
    cv.polygon([(X(b0), y0), (X(b1), y0), (X(b1), Y(hb)), (X(b0), Y(hb))], C["fill_c"], C["compr"], 1.8)
    cv.polygon([(X(a0), y0), (X(a1), y0), (X(a1), Y(ha)), (X(a0), Y(ha))], C["fill_s"], C["sfd"], 1.8)
    for v in (300, 400, 500):
        cv.text((X(v), y0), f"{v}", 12.5, C["text"], dy=16)
    for p, lab in ((hb, "1/100"), (ha, "1/200")):
        cv.line((X(280), Y(p)), (X(b0), Y(p)), C["muted"], 1, dash="4 3")
        cv.text((X(280), Y(p)), lab, 12.5, C["text"], "end", dx=-6)
    cv.text((X(350), Y(hb)), "鋼材B（300～400）", 12.5, C["compr"], dy=-14, weight="700")
    cv.text((X(450), Y(ha)), "鋼材A（300～500）", 12.5, C["sfd"], dy=-14, weight="700")
    cv.text((X(410), y0), "降伏強度 (MPa)", 12.5, C["muted"], dy=36)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([frame_panel(), dist_panel()], cols=2,
            title="SS-2022-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3、#6（待確認）；只畫考卷所給條件",
            note="鋼材A 從 300 延伸到 500 MPa（300～400 段在 B 之下），不是只有 400～500",
            path=path)
    return path


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-15 補繪）——數值取自 SS-2022-4.md §4
# ══════════════════════════════════════════════════════════════
RATIO = 1.25                                       # 強梁弱柱：F_y,梁 > 1.25 F_y,柱
DIST_U = {"A": (300.0, 500.0), "B": (300.0, 400.0)}  # 題目正本：A 300–500、B 300–400 均勻


def _fail_region(lo, hi):
    """y > RATIO·x 在 [lo,hi]² 內的區域（直角三角形）"""
    x_hi = hi / RATIO
    return [(lo, RATIO * lo), (lo, hi), (x_hi, hi)]


def _prob(lo, hi):
    (x0, y0), (_, y1), (x1, _) = _fail_region(lo, hi)
    area = 0.5 * (x1 - x0) * (y1 - y0)
    return area, area / (hi - lo) ** 2


def fig2_region():
    panels = []
    for k, col in (("A", C["compr"]), ("B", C["tension"])):
        lo, hi = DIST_U[k]
        area, p = _prob(lo, hi)
        cv = Canvas(470, 500, sx=1.6, ox=-300 * 1.6 + 90, oy=-300 * 1.6 + 90)
        cv.panel(f"鋼材 {k}：{lo:.0f}–{hi:.0f} MPa 均勻", f"有效面積 {area:,.0f} MPa²，機率 {p * 100:.1f}%")
        g0, g1 = 300, 500
        cv.polygon([(g0, g0), (g1, g0), (g1, g1), (g0, g1)], "#FFFFFF", C["ghost"], 1.0)
        cv.polygon([(lo, lo), (hi, lo), (hi, hi), (lo, hi)], C["fill_s"], col, 2.0)
        cv.polygon(_fail_region(lo, hi), C["fill_t"], C["load"], 1.6)
        cv.line((g0, RATIO * g0), (g1 / RATIO, g1), C["load"], 1.6, dash="6 4")
        for v in (300, 400, 500):
            cv.text((v, g0), f"{v:.0f}", 11.5, C["muted"], dy=18)
            cv.text((g0, v), f"{v:.0f}", 11.5, C["muted"], "end", dx=-8, dy=4)
        cv.text(((g0 + g1) / 2, g0), "柱 Fy（MPa）", 12.5, C["text"], dy=40, weight="700")
        cv.text((g0, g1), "梁 Fy", 12.5, C["text"], "start", dx=-30, dy=-16, weight="700")
        (x0, y0), (_, y1), (x1, _) = _fail_region(lo, hi)
        lp = (306, 490) if k == "A" else (350, 418)
        cv.text(lp, f"梁 Fy > {RATIO} 柱 Fy", 12, C["load"], "start", weight="700")
        cv.text((x1, y1), f"({x1:.0f}, {y1:.0f})", 11.5, C["load"], "start", dx=6, dy=-6)
        cv.text((x0, y0), f"({x0:.0f}, {y0:.0f})", 11.5, C["load"], "start", dx=6, dy=14)
        panels.append(cv)
    pa, pb = _prob(*DIST_U["A"])[1], _prob(*DIST_U["B"])[1]
    path = os.path.join(OUT, f"{TAG}-fig-2-region.svg")
    compose(panels, cols=2,
            title=f"圖 2　強梁弱柱機率：A {pa * 100:.1f}%、B {pb * 100:.1f}%（{pa / pb:.2f} 倍）",
            sub="同一座標比例；方框 = 梁、柱 Fy 可能落點，紅色三角 = 梁 Fy 超過柱 Fy 的 1.25 倍",
            note="B 的上限降到 400，紅色區只剩柱 Fy 300–320、梁 Fy 375–400 的小三角；把 B 讀成 350–450 會整個位移",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把鋼材A 讀成只分布在 400～500 MPa；把縱軸當成機率而非機率密度"),
    (fig2_region, "§4 二、三",
     "把 B 讀成 350–450；機率忘了除以範圍平方；以為範圍窄機率只線性下降"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
