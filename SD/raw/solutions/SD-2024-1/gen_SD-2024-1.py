#!/usr/bin/env python3
"""SD-2024-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 三個振態形狀（對 3F 正規化）與有效質量比：由 §4 的 [M]=m·diag(1,1,1/2)、[K]=k[[2,-1,0],[-1,2,-1],[0,-1,1]]（k=24EI/h³）以特徵值重算。
用法：python3 gen_SD-2024-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
from scipy.linalg import eigh
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2024-1"
M = np.diag([1.0, 1.0, 0.5]); K = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.0]])   # 以 m、k 為單位
lam, V = eigh(K, M)                                    # λ = ω² m/k
W24 = np.sqrt(24*lam)                                  # ω / √(EI/mh³)
PHI = [V[:, i]/V[2, i] for i in range(3)]              # 對 3F 正規化
EFF = [(p @ M @ np.ones(3))**2/(p @ M @ p)/2.5 for p in PHI]
H = 2.0; BW = 4.0
def panel(n):
    p = PHI[n-1]
    cv = Canvas(330, 470, sx=40, ox=110, oy=50, bg="#FFFFFF")
    cv.panel(f"第 {n} 振態　ω{n} = {W24[n-1]:.3f}·√(EI/mh³)",
             "{" + ", ".join(f"{v:.3f}" for v in np.round(p, 6) + 0.0) + f"}}　有效質量 {100*EFF[n-1]:.2f}%")
    s = 1.3/max(abs(v) for v in p); d = [0.0] + [v*s for v in p]
    for x in (0, BW): cv.line((x, 0), (x, 3*H), C["ghost"], 2, dash="5 4")
    for j in (1, 2, 3): cv.line((0, j*H), (BW, j*H), C["ghost"], 2, dash="5 4")
    sh = lambda u: 3*u**2 - 2*u**3
    for x in (0, BW):
        for j in range(3):
            cv.poly([(x + d[j] + (d[j+1] - d[j])*sh(i/30), j*H + H*i/30) for i in range(31)], C["deform"], 3)
    for j in (1, 2, 3): cv.line((d[j], j*H), (BW + d[j], j*H), C["deform"], 6)
    cv.support((0, 0), "fixed"); cv.support((BW, 0), "fixed")
    return cv
def fig2():
    return compose([panel(1), panel(2), panel(3)], title="圖 2　三個振態形狀（對 3F 正規化，頂層質量 m/2）",
                   note="第 n 振態有 n−1 個節點；有效質量合計 100%（2.5m），第一振態 92.85%；灰虛線為原位置",
                   path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "頂層質量誤用 m（三層同質量時第一振態為 {0.445, 0.802, 1}）；正規化對象弄錯")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
    print("W24", W24, "PHI", PHI, "EFF", EFF, sum(EFF))
