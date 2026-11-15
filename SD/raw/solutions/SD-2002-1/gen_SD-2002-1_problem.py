#!/usr/bin/env python3
"""SD-2002-1：題目附圖重繪（struct-diagram 規範；2026-11-15，SD-U1-3 批 1）
幾何、支承、載重逐項對應題目正本 SD-2002-1-problem.md §4 判讀清單（註解中的 #n），只畫考卷給的東西。
用法：python3 gen_SD-2002-1_problem.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, dashpot, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2002-1"
# ── 判讀清單 #1–#6 ──
L = 3.0          # #3 樓版質心至基座質心 3 m
B, HB = 4.0, 0.9 # 基座繪圖寬、厚（考卷未給尺寸，僅示意）
SPAN = 3.0       # 兩柱間距（示意）
def fig1():
    cv = fit(720, 420, (-3.4, 5.4), (-1.0, 4.0))
    yb = 0.0; ytop = L            # 基座質心 y=0；樓版質心 y=L
    cv.polygon([(-B/2, -HB/2), (B/2, -HB/2), (B/2, HB/2), (-B/2, HB/2)], "#D5DAE1", C["member"], 2)
    ground(cv, (-3.2, HB/2), (-B/2-0.1, HB/2)); ground(cv, (B/2+0.1, HB/2), (3.2, HB/2))
    for x in (-SPAN/2, SPAN/2):   # #2 兩根柱，各 k
        cv.line((x, HB/2), (x, ytop - 0.1), C["member"], 3.4, cap="butt")
        cv.math((x, (HB/2 + ytop)/2), "k", 18, C["text"], "middle", dx=-16 if x < 0 else 16)
    cv.polygon([(-SPAN/2-0.3, ytop-0.12), (SPAN/2+0.3, ytop-0.12), (SPAN/2+0.3, ytop+0.12), (-SPAN/2-0.3, ytop+0.12)], C["member"])
    cv.text((0, ytop + 0.12), "M_{2}, I_{2}（對樓版質心）", 15, C["text"], dy=-16)
    cv.dot((0, ytop), 5, "#FFFFFF", C["accent"], 2.2); cv.dot((0, yb), 5, "#FFFFFF", C["accent"], 2.2)
    cv.text((-1.0, yb), "I_{1}（對基座質心）", 13, C["text"], "end", dx=-4)
    # #1 基座只繞質心轉：旋轉彈簧 kθ
    cv.moment_arrow((0, yb), r=16, ccw=True, color=C["deform"], w=2.2, span=270, start=0)
    cv.math((0.55, yb), "k_{θ}", 16, C["deform"], "start", dx=6)
    cv.dim((3.9, yb), (3.9, ytop), "L = 3 m", off=0, label_off=-34)
    cv.text((3.9, ytop/2), "質心至質心", 12.5, C["muted"], "start", dx=10)
    cv.text_px(360, 405, "基座不平移、只繞基座質心旋轉；柱不計軸向變形", 13, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-problem.svg")
FIGURES = [(fig1, "L 的量測基準（質心至質心，非地表至樓版）、I2 對樓版質心、兩根柱各 k")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
