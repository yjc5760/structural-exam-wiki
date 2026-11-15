#!/usr/bin/env python3
"""SD-2022-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 兩個振態的變形形狀：由 §4 (1) 的 4×4 勁度矩陣靜態濃縮，振態 φ 取自 (2)，
轉角 θ_A、θ_B 由 θ = −K_00^{-1} K_0t φ 回算，柱、梁以 Hermite 三次曲線畫出（轉角逆時針為正）。
用法：python3 gen_SD-2022-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C, compose
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2022-1"
# ── 題給（題目正本）與 §4 (1)(2) ──
L, EI = 3.0, 2000.0; mA, mB = 1.0, 2.0
c = EI / L**3
K = c * np.array([[12, 0, 6*L, 0], [0, 12, -6*L, -6*L], [6*L, -6*L, 8*L**2, 2*L**2], [0, -6*L, 2*L**2, 4*L**2]])
Ktt, Kt0, K00 = K[:2, :2], K[:2, 2:], K[2:, 2:]
Kc = Ktt - Kt0 @ np.linalg.solve(K00, Kt0.T)               # 濃縮勁度（§4 (1)）
Mc = np.diag([mA + mB, mB])
lam, V = np.linalg.eig(np.linalg.solve(Mc, Kc)); o = np.argsort(lam.real); lam, V = lam.real[o], V.real[:, o]
V = V / V[0]                                               # 第一分量取 1（同 §4 (2)）
TH = -np.linalg.solve(K00, Kt0.T) @ V                      # 回算轉角 θ_A、θ_B（逆時針正）
def herm(a0, s0, a1, s1, n=40):
    e = np.linspace(0, 1, n); h00 = 2*e**3 - 3*e**2 + 1; h10 = e**3 - 2*e**2 + e; h01 = -2*e**3 + 3*e**2; h11 = e**3 - e**2
    return e, h00*a0 + h10*L*s0 + h01*a1 + h11*L*s1
def panel(i):
    u1, u2 = V[:, i]; tA, tB = TH[:, i]
    s = 0.9 / max(abs(u1), abs(u2))                        # 示意放大
    cv = fit(430, 360, (-1.6, 5.2), (-0.8, 4.7), L=14, R=14, T=48, B=14)
    w = np.sqrt(lam[i])
    cv.text_px(215, 18, f"振態 {i+1}：ω = {w:.3f} rad/s", 14.5, C["text"], weight="700")
    cv.text_px(215, 38, f"φ = {{1, {u2:.4f}}}（u_{{1}}, u_{{2}}）", 12.5, C["muted"])
    cv.line((0, 0), (0, L), C["ghost"], 2.0, dash="5 4"); cv.line((0, L), (L, L), C["ghost"], 2.0, dash="5 4")
    cv.support((0, 0), "fixed")
    e, x = herm(0, 0, s*u1, -s*tA)                          # 柱：dx/dy = −θ（逆時針正）
    cv.poly([(xx, ee*L) for ee, xx in zip(e, x)], C["deform"], 2.8)
    e, v = herm(0, s*tA, s*u2, s*tB)                        # 梁：dv/dx = θ，整根隨 u1 平移
    cv.poly([(s*u1 + ee*L, L + vv) for ee, vv in zip(e, v)], C["deform"], 2.8)
    A, B = (s*u1, L), (s*u1 + L, L + s*u2)
    cv.dot(A, 6, C["deform"]); cv.dot(B, 6, C["deform"])
    cv.text(B, f"u_{{2}} = {u2:.3f}", 13, C["deform"], "start", dx=10)
    cv.text(A, "u_{1} = 1", 13, C["deform"], "end", dx=-10, dy=-12)
    return cv
def fig2():
    return compose([panel(0), panel(1)], title="圖 2　兩個振態的變形形狀（倒 L 形構架，忽略軸向變形）",
                   note="虛線為原位置；B 點水平位移等於 u1（mB 也參與 DOF 1）。振態 1 的 B 點垂直分量與 u1 反號、振態 2 同號；A 點維持剛接直角",
                   path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "M̂ 的 DOF 1 漏掉 m_B；振態分量正負號與構架變形方向對不起來")]

if __name__ == "__main__":
    print("ω =", np.sqrt(lam), "φ2 =", V[1], "θ =", TH)
    for fn, cc in FIGURES: fn(); print(fn.__name__, "—", cc)
