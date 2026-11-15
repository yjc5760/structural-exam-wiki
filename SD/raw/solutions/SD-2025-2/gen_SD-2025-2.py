#!/usr/bin/env python3
"""SD-2025-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 兩個振態形狀與參與因子：由 §4 的 [M]、[K]（m=100 kN·s²/m、k=1500 kN/m）以特徵值重算，下層分量取 1。
用法：python3 gen_SD-2025-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
from scipy.linalg import eigh
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2025-2"
# ── §4：m1=m2=100 kN·s²/m，k1=k2=1500 kN/m ──
m, k = 100.0, 1500.0
M = np.diag([m, m]); K = np.array([[2*k, -k], [-k, k]])
lam, V = eigh(K, M); W = np.sqrt(lam); T = 2*np.pi/W
PHI = [V[:, i]/V[0, i] for i in range(2)]                     # 下層（u1）取 1
GAM = [(p @ M @ np.ones(2))/(p @ M @ p) for p in PHI]
EFF = [(p @ M @ np.ones(2))**2/(p @ M @ p)/(2*m) for p in PHI]
H = 3.0; BW = 4.0
def panel(n):
    p = PHI[n-1]
    cv = Canvas(400, 400, sx=40, ox=150, oy=50, bg="#FFFFFF")
    cv.panel(f"第 {n} 振態　ω{n} = {W[n-1]:.3f} rad/s，T{n} = {T[n-1]:.3f} s",
             f"{{u1, u2}} = {{{p[0]:.3f}, {p[1]:.3f}}}　Γ{n} = {GAM[n-1]:.4f}（有效質量 {100*EFF[n-1]:.1f}%）")
    s = 1.6/max(abs(v) for v in p); d1, d2 = p[0]*s, p[1]*s
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["ghost"], 2, dash="5 4")
    for y in (H, 2*H): cv.line((0, y), (BW, y), C["ghost"], 2, dash="5 4")
    sh = lambda u: 3*u**2 - 2*u**3
    for x in (0, BW):
        cv.poly([(x + d1*sh(i/30), H*i/30) for i in range(31)], C["deform"], 3)
        cv.poly([(x + d1 + (d2 - d1)*sh(i/30), H + H*i/30) for i in range(31)], C["deform"], 3)
    cv.line((d1, H), (BW + d1, H), C["deform"], 6); cv.line((d2, 2*H), (BW + d2, 2*H), C["deform"], 6)
    cv.support((0, 0), "fixed"); cv.support((BW, 0), "fixed")
    return cv
def fig2():
    return compose([panel(1), panel(2)], title="圖 2　振態形狀與參與因子（m1 = m2 = 100 kN·s²/m，k1 = k2 = 1500 kN/m）",
                   note="下層分量取 1；第二振態上層反向（−0.618），樓層間出現一個節點；灰虛線為原位置",
                   path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "振態分量上下顛倒（u1 在下層）；Γ 與正規化不對應")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
    print("W", W, "T", T, "PHI", PHI, "GAM", GAM, "EFF", EFF)
