#!/usr/bin/env python3
"""SD-2005-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）
fig-2 兩個振態形狀：樓版側移比例取自 §4 Step 7；柱的撓曲形狀依柱端條件——
固定底柱：u = Δ(3ξ² − 2ξ³)（兩端無轉角），鉸底中柱：u = Δ(3ξ − ξ³)/2（底端彎矩為零、頂端無轉角）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2005-2"
# ── 由 SD-2005-2.md §4 Step 6–7 解得 ──
W1, W2 = 64.98, 154.2
PHI = {1: (1.000, 1.315), 2: (1.000, -2.851)}       # (y1, y2)
H1, H2 = 4.2, 3.2; XL, XM, XR = 0.0, 7.0, 15.0
fixed = lambda s: 3*s**2 - 2*s**3
pinned = lambda s: (3*s - s**3) / 2
def col(cv, x, ya, yb, da, db, base_pin=False, color=C["deform"]):
    pts = []
    for i in range(41):
        s = i / 40; d = da + (db - da) * (pinned(s) if base_pin else fixed(s))
        pts.append((x + d, ya + (yb - ya) * s))
    cv.poly(pts, color, 3.2)
def panel(n):
    y1, y2 = PHI[n]; s = 2.2 / max(abs(y1), abs(y2))      # 繪圖放大倍率（示意）
    d1, d2 = y1 * s, y2 * s
    cv = Canvas(460, 330, sx=20, ox=60, oy=55, bg="#FFFFFF"); cv.panel(f"第 {n} 振態　ω{n} = {W1 if n == 1 else W2} rad/s", f"{{y1, y2}} = {{{y1:.3f}, {y2:.3f}}}")
    for x in (XL, XM, XR): cv.line((x, 0), (x, H1), C["ghost"], 2, dash="5 4")
    for x in (XM, XR): cv.line((x, H1), (x, H1 + H2), C["ghost"], 2, dash="5 4")
    cv.line((XL, H1), (XR, H1), C["ghost"], 2, dash="5 4"); cv.line((XM, H1 + H2), (XR, H1 + H2), C["ghost"], 2, dash="5 4")
    col(cv, XL, 0, H1, 0, d1); col(cv, XR, 0, H1, 0, d1); col(cv, XM, 0, H1, 0, d1, base_pin=True, color=C["accent"])
    col(cv, XM, H1, H1 + H2, d1, d2); col(cv, XR, H1, H1 + H2, d1, d2)
    cv.line((XL + d1, H1), (XR + d1, H1), C["deform"], 5); cv.line((XM + d2, H1 + H2), (XR + d2, H1 + H2), C["deform"], 5)
    cv.support((XL, 0), "fixed"); cv.support((XR, 0), "fixed"); cv.support((XM, 0), "pin", size=13)
    cv.text((XM, 0), "鉸", 12.5, C["accent"], "start", dx=14, dy=-12)
    return cv
def fig2():
    return compose([panel(1), panel(2)], title="圖 2　振態形狀（中柱底鉸接）",
                   note="橙色：中柱底鉸接，柱底有轉角、彎矩為零（側向勁度 3EI/h³）；灰虛線為原位置", path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "中柱底當成固定（12EI/h³）；振態第二模態兩樓反向")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
