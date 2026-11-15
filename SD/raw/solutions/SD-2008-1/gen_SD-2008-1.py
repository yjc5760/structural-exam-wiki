#!/usr/bin/env python3
"""SD-2008-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）
fig-2 兩個振態形狀，自由度依考卷：u1 在頂層、u2 在下層。振態取自 §4（u1 分量正規化為 1）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2008-1"
# ── 由 SD-2008-1.md §4 解得（{u1 頂, u2 下}）──
PHI = {1: (1.0, (math.sqrt(5) - 1) / 2), 2: (1.0, -(math.sqrt(5) + 1) / 2)}   # 0.618、−1.618
T = {1: 0.197, 2: 0.0752}
H, BW = 3.0, 3.0
fixed = lambda s: 3*s**2 - 2*s**3
def panel(n):
    u1, u2 = PHI[n]; sc = 1.1 / max(abs(u1), abs(u2)); d_top, d_low = u1 * sc, u2 * sc
    cv = Canvas(380, 420, sx=48, ox=95, oy=55, bg="#FFFFFF")
    cv.panel(f"第 {n} 振態　T{n} = {T[n]} s", f"{{u1（頂）, u2（下）}} = {{1, {u2:.3f}}}")
    for x in (0, BW):
        cv.line((x, 0), (x, 2*H), C["ghost"], 2, dash="5 4"); cv.support((x, 0), "fixed")
        cv.poly([(x + d_low*fixed(i/30), H*i/30) for i in range(31)], C["deform"], 3)
        cv.poly([(x + d_low + (d_top - d_low)*fixed(i/30), H + H*i/30) for i in range(31)], C["deform"], 3)
    for y, d, lab in ((2*H, d_top, "u_{1}"), (H, d_low, "u_{2}")):
        cv.line((0, y), (BW, y), C["ghost"], 2, dash="5 4"); cv.line((d, y), (BW + d, y), C["deform"], 6)
        cv.math((BW + max(d, 0), y), lab, 16, C["deform"], "start", dx=10)
    return cv
def fig2():
    return compose([panel(1), panel(2)], title="圖 2　振態形狀（u1 在頂層）",
                   note="u1 是頂層：「u1 分量為 1」表示頂層為 1；第二振態下層反向且較大（−1.618）", path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "把 u1 當成下層，振態上下顛倒（0.618 與 1.618 互換）")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
