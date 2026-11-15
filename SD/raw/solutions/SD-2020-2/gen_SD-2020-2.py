#!/usr/bin/env python3
"""SD-2020-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-1 三個振態形狀＋有效質量比＋頂樓位移貢獻：全部由考卷給的週期、振態向量與反應譜重算（[M]=mI）。
用法：python3 gen_SD-2020-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2020-2"
# ── 題目正本 §1：振態向量（1F→3F）、週期；反應譜分段；g = 9.8 ──
PHI = [np.array([0.46346, 0.86379, 1.0]), np.array([-1.24698, -0.55496, 1.0]), np.array([1.80194, -2.24698, 1.0])]
T = [1.7, 0.5, 0.3]; G = 9.8
def Sa(t): return (0.2 + 1.5*t) if t < 0.2 else (0.5 if t < 1 else 0.5/t)
RHO = [p.sum()**2/(p @ p)/3 for p in PHI]                       # 有效質量比（[M]=mI）
GAM = [p.sum()/(p @ p) for p in PHI]
SD_ = [Sa(t)*G*t**2/(4*math.pi**2) for t in T]
U3 = [GAM[i]*PHI[i][2]*SD_[i] for i in range(3)]                  # 各振態頂樓位移（m）
NREQ = next(n for n in range(1, 4) if sum(RHO[:n]) >= 0.95)
USRSS = math.sqrt(sum(u*u for u in U3[:NREQ]))
H = 1.4
def panel(n):
    p = PHI[n-1]; used = n <= NREQ
    cv = Canvas(360, 430, sx=60, ox=185, oy=70, bg="#FFFFFF")
    cv.panel(f"振態 {n}（T = {T[n-1]} s）", f"有效質量 {100*RHO[n-1]:.2f}%" + ("　採用" if used else "　不需採用"))
    s = 1.3/max(abs(v) for v in p)
    cv.line((0, 0), (0, 3*H), C["ghost"], 2, dash="5 4")
    pts = [(0, 0)] + [(p[j]*s, (j+1)*H) for j in range(3)]
    cv.poly(pts, C["deform"] if used else C["muted"], 3.2)
    for j in range(3):
        cv.dot(pts[j+1], 0.09, fill=C["deform"] if used else C["muted"])
        cv.text_px(cv.X(pts[j+1][0]) + (12 if p[j] >= 0 else -12), cv.Y(pts[j+1][1]) + 5,
                   f"{p[j]:.3f}", 12.5, C["text"], "start" if p[j] >= 0 else "end")
        cv.text_px(16, cv.Y((j+1)*H) + 5, f"{j+1}F", 12.5, C["muted"], "start")
    cv.support((0, 0), "fixed")
    cv.text_px(180, 395, f"頂樓貢獻 {100*U3[n-1]:+.2f} cm", 13,
               C["accent"] if used else C["muted"])
    return cv
def fig1():
    cum = [sum(RHO[:i+1]) for i in range(3)]
    return compose([panel(1), panel(2), panel(3)], cols=3,
                   title="圖 1　三個振態形狀、有效質量比與頂樓位移貢獻（振態向量由 1F 排到 3F）",
                   sub=f"累積有效質量：振態 1 = {100*cum[0]:.2f}%（未達 95%），振態 1＋2 = {100*cum[1]:.2f}% → 最少 {NREQ} 個振態",
                   note=f"頂樓 SRSS = √({abs(100*U3[0]):.2f}² + {abs(100*U3[1]):.2f}²) = {100*USRSS:.2f} cm；振態 2 有效質量 7.5%，頂樓貢獻卻不到 1 cm",
                   path=f"{OUT}/{TAG}-fig-1-modes.svg")
FIGURES = [(fig1, "振態向量上下顛倒（考卷由 1F 排到 3F）；只取振態 1（92% < 95%）；以有效質量比誤判位移貢獻")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
    print("RHO", RHO, "GAM", GAM, "SD", SD_, "U3", U3, "N", NREQ, "SRSS", USRSS)
