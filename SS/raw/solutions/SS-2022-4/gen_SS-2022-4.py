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
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

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


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把鋼材A 讀成只分布在 400～500 MPa；把縱軸當成機率而非機率密度"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
