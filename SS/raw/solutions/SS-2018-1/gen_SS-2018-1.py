#!/usr/bin/env python3
"""
SS-2018-1 中央細縫鋼板受拉之伸長量 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2018-1.py [輸出目錄]

重繪依據：題目正本 SS-2018-1-problem.md §4 判讀清單（待確認）。
只重繪上方鋼板示意（細縫、標點、尺寸）；下方應力–應變圖屬曲線圖，不重繪（數值見題目正本 §2、§4）。
板長與 w 的比例為示意；細縫長 0.2w 依比例。不含任何解題結果。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2018-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2018-1-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
L0 = 1000.0          # #5 標點間距 l0 = 1000 mm，兩標點在細縫兩側
W_DRAW = 1.0         # 板寬 w（符號；繪圖單位）
SLIT = 0.2           # #4 細縫寬方向長 0.2w，位於板寬中央、垂直拉力方向；淨寬 0.8w（推得值）
SLIT_T = 0.035       # 細縫沿拉力方向極窄（未標，示意）
LEN_DRAW, GAP = 6.0, 0.6   # 繪圖用：板長（示意）、標點距板端


def fig1_problem():
    W, H, sx = 820, 380, 105
    cv = Canvas(W, H, sx=sx, ox=(W - LEN_DRAW * sx) / 2, oy=170)
    cv.panel("鋼板（示意）", "應力–應變圖為曲線圖，不重繪；兩鋼材數值見題目正本")
    cv.polygon([(0, 0), (LEN_DRAW, 0), (LEN_DRAW, W_DRAW), (0, W_DRAW)], C["fill_c"], C["member"], 1.8)
    xm = LEN_DRAW / 2
    y0 = (W_DRAW - SLIT) / 2
    cv.polygon([(xm - SLIT_T, y0), (xm + SLIT_T, y0), (xm + SLIT_T, y0 + SLIT), (xm - SLIT_T, y0 + SLIT)],
               C["text"], C["text"], 1)
    xa, xb = GAP, LEN_DRAW - GAP
    for x in (xa, xb):
        cv.dot((x, W_DRAW / 2), 6, fill=C["text"], stroke=C["text"], w=1)
    cv.arrow((0, W_DRAW / 2), (-0.55, W_DRAW / 2), C["load"], 3, 10)
    cv.arrow((LEN_DRAW, W_DRAW / 2), (LEN_DRAW + 0.55, W_DRAW / 2), C["load"], 3, 10)
    cv.dim((xm + SLIT_T, y0), (xm + SLIT_T, y0 + SLIT), "0.2w", off=34, label_off=26)
    cv.dim((xa + 1.0, 0), (xa + 1.0, W_DRAW), "w", off=0, label_off=14)
    cv.dim((xa, 0), (xb, 0), f"l_{{0}} = {L0:.0f} mm", off=46, label_off=16)
    cv.text((xm, W_DRAW), "細縫", 13, C["text"], dy=-16, weight="700")
    cv.text((xb, W_DRAW), "標點", 13, C["text"], dy=-16, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2018-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #4、#5（待確認）；只畫考卷所給條件",
            note="細縫垂直拉力方向、長 0.2w，細縫處淨寬 0.8w；兩標點跨過細縫、間距 1000 mm",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把細縫讀成平行拉力方向；標點間距沒有跨過細縫"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
