#!/usr/bin/env python3
"""SD-2019-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 振態形狀與起始位移：M、K 取自 §4-1（m1=40、m2=20 kg；k1=2000、k2=1000 N/m），振態與 q_n(0) 由程式求得。
用法：python3 gen_SD-2019-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
from scipy.linalg import eigh
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2019-2"
M = np.diag([40.0, 20.0]); K = np.array([[3000.0, -1000.0], [-1000.0, 1000.0]])
U0 = np.array([0.1, 0.2])                           # 起始位移（m）
w2, V = eigh(K, M); W = np.sqrt(w2)
PHI = [V[:, i] / V[0, i] for i in range(2)]          # 二樓分量取 1
Q0 = [round(float(p @ M @ U0 / (p @ M @ p)), 12) + 0.0 for p in PHI]  # 振態座標初值
H, BW = 3.0, 4.0
sh = lambda t: 3*t**2 - 2*t**3
def frame(title, sub, d1, d2, color):
    cv = Canvas(330, 380, sx=36, ox=105, oy=40, bg="#FFFFFF"); cv.panel(title, sub)
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["ghost"], 2, dash="5 4")
    for y in (H, 2*H): cv.line((0, y), (BW, y), C["ghost"], 2, dash="5 4")
    for x in (0, BW):
        cv.poly([(x + d1*sh(i/30), H*i/30) for i in range(31)], color, 3)
        cv.poly([(x + d1 + (d2 - d1)*sh(i/30), H + H*i/30) for i in range(31)], color, 3)
    cv.line((d1, H), (BW + d1, H), color, 6); cv.line((d2, 2*H), (BW + d2, 2*H), color, 6)
    cv.support((0, 0), "fixed"); cv.support((BW, 0), "fixed")
    return cv
def fig2():
    ps = []
    for n in range(2):
        p = PHI[n]; s = 1.4 / max(abs(p))
        ps.append(frame(f"第 {n+1} 振態　ω{n+1} = {W[n]:.0f} rad/s", f"{{u1, u2}} = {{{p[0]:.0f}, {p[1]:.0f}}}", p[0]*s, p[1]*s, C["deform"]))
    s = 1.4 / max(abs(U0))
    ps.append(frame("起始位移", f"{{0.1, 0.2}} m ＝ {Q0[0]:.1f} φ1 ＋ {Q0[1]:.1f} φ2", U0[0]*s, U0[1]*s, C["load"]))
    return compose(ps, title="圖 2　振態形狀與起始位移（m1 = 40、m2 = 20 kg；k1 = 2000、k2 = 1000 N/m）",
                   note="起始位移與第 1 振態同形，q2(0) = 0：結構只以 ω1 = 5 rad/s 振動", path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "把兩個振態都疊進反應；第 2 振態兩樓畫成同向")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
