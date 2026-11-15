#!/usr/bin/env python3
"""SD-2006-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）
fig-2 樓層剪力圖：振態剪力、SRSS 與規範豎向分配並列。數值全部取自 SD-2006-2.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2006-2"
# ── 由 §4 子題(三)(四) 解得 ──
F1 = (11358, 18377); F2 = (3997, -2470)          # 題給等效樓層橫力（一樓, 二樓）
V_M1 = (F1[0] + F1[1], F1[1]); V_M2 = (F2[0] + F2[1], F2[1])   # 振態樓層剪力（一樓層, 二樓層）
V_SRSS = tuple(round(math.hypot(a, b)) for a, b in zip(V_M1, V_M2))   # (29774, 18542)
V_CODE = (V_SRSS[0], round(V_SRSS[0] * 2 / 3))     # 等樓高、Ft=0：F2 = 2/3 V，(29774, 19849)
def panel(title, sets, note):
    cv = Canvas(420, 420, sx=1, bg="#FFFFFF"); cv.panel(title, note)
    x0, x1, yb, h = 60, 400, 360, 130; vmax = 40000
    X = lambda v: x0 + (x1 - x0) * v / vmax
    for s in (0, 1, 2): cv.line((x0, cv.h - (yb - s*h)), (x1, cv.h - (yb - s*h)), C["ghost"], 1, dash="3 3")
    cv.line((x0, cv.h - yb), (x0, cv.h - (yb - 2*h)), C["member"], 2.2)
    for k, (vals, col, dy) in enumerate(sets):
        for st in (0, 1):
            ytop, ybot = yb - (st+1)*h + 18 + dy, yb - st*h - 18 + dy
            cv.rect_px(x0, ytop, X(abs(vals[st])) - x0, 22, col, 0)
            cv.text_px(X(abs(vals[st])) + 6, ytop + 11, f"{vals[st]:,} N", 12.5, col, "start")
    for st, lab in ((0, "一樓層"), (1, "二樓層")): cv.text_px(30, yb - st*h - h/2, lab, 12.5, C["muted"])
    return cv
def fig2():
    a = panel("(三) 振態剪力與 SRSS", [(V_M1, C["deform"], 0), (V_M2, C["sfd"], 26), (V_SRSS, C["load"], 52)], "藍：第一振態　紫：第二振態（絕對值）　紅：SRSS")
    b = panel("(四) 規範豎向分配（Ft = 0）", [(V_CODE, C["bmd"], 0), (V_SRSS, C["load"], 26)], "綠：靜力法　紅：SRSS（對照）")
    return compose([a, b], title="圖 2　樓層剪力圖", note="一樓層剪力兩法相同（基底剪力取 SRSS）；二樓層靜力法 19,849 N 大於 SRSS 18,542 N", path=f"{OUT}/{TAG}-fig-2-shear.svg")
FIGURES = [(fig2, "把等效樓層橫力當成樓層剪力；SRSS 先疊加橫力再求剪力（順序錯）")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c, V_SRSS, V_CODE)
