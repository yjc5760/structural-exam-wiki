#!/usr/bin/env python3
"""
SS-2013-1 空心圓斷面之 S_x、Z_x 與形狀因數 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2013-1.py [輸出目錄]

重繪依據：題目正本 SS-2013-1-problem.md §4 判讀清單（2026-11-02 已確認）
與 §1 題文「d = 0.6D」。只畫考卷給的東西，不含任何解題結果。
內外徑比依題文 d = 0.6D 繪製（原圖未按比例）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2013-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2013-1-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
D_OUT = 1.0                 # #1 D 為外徑（繪圖取 1 個單位）
RATIO = 0.6                 # §1 題文 d = 0.6D
D_IN = RATIO * D_OUT        # #2 d 為內徑
#                             #3 斷面實體為兩圓之間的圓環


def fig1_problem():
    W, H, sx = 520, 440, 280
    cv = Canvas(W, H, sx=sx, ox=W / 2 + 20, oy=H / 2 - 30)
    cv.panel("圖 1　空心圓斷面", "內徑依題文 d = 0.6D 按比例")
    cv.circle((0, 0), D_OUT / 2, fill=C["fill_c"], stroke=C["member"], w=2.2)
    cv.circle((0, 0), D_IN / 2, fill=C["panel"], stroke=C["member"], w=2.2)
    cv.dim((-D_OUT / 2, -D_OUT / 2), (-D_OUT / 2, D_OUT / 2), "D", off=-30, label_off=-16)
    a = math.radians(45)
    p0 = (-D_IN / 2 * math.cos(a), D_IN / 2 * math.sin(a))
    p1 = (D_IN / 2 * math.cos(a), -D_IN / 2 * math.sin(a))
    cv.double_arrow(p0, p1, C["dim"], 1.4, 8)
    cv.math((0.05, 0.08), "d", 17, C["text"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2013-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3；只畫考卷所給條件",
            note="D 為外徑、d 為內徑；填色圓環為斷面實體",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 d 當成外徑或半徑；把內圓也當成實體"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
