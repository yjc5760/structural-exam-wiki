#!/usr/bin/env python3
"""
SS-2010-1 階梯形斷面之 M_y 與 M_p — 題目附圖重繪腳本

用法：
    python3 gen_SS-2010-1.py [輸出目錄]

重繪依據：題目正本 SS-2010-1-problem.md §4 判讀清單（2026-11-02 已確認）。
圖上每個尺寸都對應清單一項；只畫考卷給的東西，不含任何解題結果（ENA、PNA 不畫）。
斷面依比例繪製。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2010-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2010-1-problem.md §4，已確認）；單位 cm
# ══════════════════════════════════════════════════════════
X_SEG = [2.0, 2.0, 2.0]          # #1 水平分段 2-2-2，總寬 6
Y_SEG = [2.0, 2.0, 2.0, 2.0]     # #2 垂直分段 2-2-2-2，總高 8
# 由下而上各層：（寬度所佔水平分段的起訖索引）
LAYERS = [(0, 3),                # #3 第 1 層：全寬 6×2
          (1, 2),                # #4 第 2 層：中央 2×2
          (0, 3),                # #5 第 3 層：全寬 6×2
          (1, 2)]                # #6 第 4 層：頂部中央凸塊 2×2
#                                  #7 左右對稱、上下不對稱

XS = [sum(X_SEG[:i]) for i in range(len(X_SEG) + 1)]   # 0, 2, 4, 6
YS = [sum(Y_SEG[:i]) for i in range(len(Y_SEG) + 1)]   # 0, 2, 4, 6, 8


def outline():
    """由各層矩形組出外框（右側由下而上、左側由上而下）"""
    right, left = [], []
    for k, (i0, i1) in enumerate(LAYERS):
        right += [(XS[i1], YS[k]), (XS[i1], YS[k + 1])]
        left += [(XS[i0], YS[k]), (XS[i0], YS[k + 1])]
    return right + left[::-1]


def fig1_problem():
    W, H, sx = 520, 470, 38
    cv = Canvas(W, H, sx=sx, ox=W / 2 - XS[-1] / 2 * sx - 30, oy=90)
    cv.panel("圖一　斷面", "依比例；單位為公分")
    cv.polygon(outline(), C["fill_c"], C["member"], 2.0)
    xr = XS[-1]
    for k in range(len(Y_SEG)):
        cv.dim((xr, YS[k]), (xr, YS[k + 1]), f"{Y_SEG[k]:g}", off=40, label_off=16)
    for i in range(len(X_SEG)):
        cv.dim((XS[i], 0), (XS[i + 1], 0), f"{X_SEG[i]:g}", off=30, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2010-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#7；只畫考卷所給條件",
            note="由下而上：全寬 6×2、中央 2×2、全寬 6×2、頂部凸塊 2×2（上下不對稱）",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把斷面讀成上下對稱的十字形（漏看底部全寬段與頂部凸塊的差異）"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert XS[-1] == 6 and YS[-1] == 8
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
