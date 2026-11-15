#!/usr/bin/env python3
"""SD-2019-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 振態形狀：M、K 取自 §4（u1 梁端、u2 圓球，向下為正；圓球 (2/3)m），振態由程式解特徵值求得。
用法：python3 gen_SD-2019-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
from scipy.linalg import eigh
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import fit, spring
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2019-1"
K = np.array([[1.5, -1.0], [-1.0, 1.0]])        # §4：k 為單位
MB = 2/3                                          # 圓球質量 (2/3)m（判讀 #1）
def modes():
    out = []
    # ㈠ 梁無質量：靜力凝縮 u1 = (2/3) u2，ω² = (k/3)/(2m/3)
    out.append(("㈠ 梁質量 0", math.sqrt((1 - 1/1.5) / MB), (1/1.5, 1.0)))
    w2, V = eigh(K, np.diag([1/3, MB]))           # ㈡ 梁等效質量 m/3
    for i in range(2):
        u = V[:, i] / V[1, i]
        out.append((f"㈡ 第 {i+1} 振態", math.sqrt(w2[i]), (u[0], u[1])))
    return out
def panel(title, w, u):
    cv = fit(330, 380, (-0.4, 2.9), (-3.3, 1.9), L=14, R=14, T=64, B=10)
    cv.panel(title, f"ω = {w:.3f}√(k/m)；{{u1, u2}} = {{{u[0]:.3f}, {u[1]:.3f}}}")
    s = 0.9 / max(abs(u[0]), abs(u[1]))
    y1, y2 = -u[0]*s, -u[1]*s                      # 向下為正 → 圖上取負
    BY = -1.9                                       # 圓球原位置
    cv.line((0, 0), (2, 0), C["ghost"], 3, dash="5 4"); cv.circle((2, BY), 0.18, "none", C["ghost"], 2, dash="4 3")
    cv.line((0, 0), (2, y1), C["deform"], 5)
    spring(cv, (1, y1/2), (1, 1.6), n=3, amp=0.09, color=C["member2"], w=1.6)
    cv.line((0.75, 1.6), (1.25, 1.6), C["member2"], 2.2)
    spring(cv, (2, y1), (2, BY + y2 + 0.18), n=3, amp=0.09, color=C["member2"], w=1.6)
    cv.circle((2, BY + y2), 0.18, "#9AA3AF", C["deform"], 2.4)
    cv.support((0, 0), "pin")
    cv.text((2, y1), "u1", 12.5, C["deform"], "start", dx=10, dy=12 if y1 > 0 else 0)
    cv.text((2, BY + y2), "u2", 12.5, C["deform"], "start", dx=16)
    return cv
def fig2():
    ps = [panel(t, w, u) for t, w, u in modes()]
    return compose(ps, title="圖 2　振態形狀（圓球 (2/3)m；向下為正，灰虛線為靜平衡位置）",
                   note="㈡ 第 1 振態梁端與圓球同向，第 2 振態反向；㈠ 梁無質量只剩一個有限頻率", path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "第 2 振態誤畫成同向；㈠ 誤當 2 自由度求兩個頻率")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
