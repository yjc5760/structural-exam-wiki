#!/usr/bin/env python3
"""SD-2022-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 左：兩振態形狀與參與因子；右：設計反應譜 S_a = min(0.45/T, 0.7) g 與兩振態的取值點（§4 ㈡ Step A–D）。
全部由題給 M、K 與反應譜計算（g = 9.81 m/s²，同 §4）。
用法：python3 gen_SD-2022-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2022-3"
# ── 小型 x–y 圖工具（像素座標，原點左下；只畫軸、格線、曲線，數據由呼叫端給）──
class Axes:
    def __init__(self, cv, x0, y0, w, h, xr, yr):
        self.cv, self.x0, self.y0, self.w, self.h, self.xr, self.yr = cv, x0, y0, w, h, xr, yr
    def P(self, x, y):
        return (self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w,
                self.y0 + (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h)
    def frame(self, xt, yt, xlab, ylab, fmt_x="{:g}", fmt_y="{:g}"):
        cv = self.cv
        for x in xt:
            a = self.P(x, self.yr[0]); b = self.P(x, self.yr[1]); cv.line(a, b, C["border"], 1)
            cv.text(a, fmt_x.format(x), 12, C["muted"], dy=14)
        for y in yt:
            a = self.P(self.xr[0], y); b = self.P(self.xr[1], y); cv.line(a, b, C["border"], 1)
            cv.text(a, fmt_y.format(y), 12, C["muted"], "end", dx=-6)
        cv.line(self.P(self.xr[0], self.yr[0]), self.P(self.xr[1], self.yr[0]), C["muted"], 1.6)
        cv.line(self.P(self.xr[0], self.yr[0]), self.P(self.xr[0], self.yr[1]), C["muted"], 1.6)
        cv.text(self.P((self.xr[0] + self.xr[1]) / 2, self.yr[0]), xlab, 13, C["text"], dy=34)
        cv.text(self.P(self.xr[0], self.yr[1]), ylab, 13, C["text"], "start", dx=4, dy=-14)
    def curve(self, xs, ys, color, w=2.4, dash=None):
        pts = [self.P(x, y) for x, y in zip(xs, ys) if self.yr[0] - 1e-9 <= y <= self.yr[1] + 1e-9]
        self.cv.poly(pts, color, w, dash=dash)
    def hline(self, y, color=C["dim"], dash="4 4", w=1.2):
        self.cv.line(self.P(self.xr[0], y), self.P(self.xr[1], y), color, w, dash=dash)
    def vline(self, x, color=C["dim"], dash="4 4", w=1.2, y1=None):
        self.cv.line(self.P(x, self.yr[0]), self.P(x, self.yr[1] if y1 is None else y1), color, w, dash=dash)
    def dot(self, x, y, color=C["accent"], r=5):
        self.cv.dot(self.P(x, y), r, color)
    def label(self, x, y, s, color=C["text"], anchor="start", dx=8, dy=0, size=12.5):
        self.cv.text(self.P(x, y), s, size, color, anchor, dx=dx, dy=dy)

# ── 題給（題目正本 §1）──
M = np.diag([100.0, 100.0]); K = np.array([[3000.0, -1500.0], [-1500.0, 1500.0]]); g = 9.81
lam, V = np.linalg.eig(np.linalg.solve(M, K)); o = np.argsort(lam); lam, V = lam[o], V[:, o]; V = V / V[0]
W = np.sqrt(lam); T = 2*np.pi/W
GAM = (V.T @ M @ np.ones(2)) / np.diag(V.T @ M @ V)
Sa = lambda t: np.minimum(0.45/t, 0.7)
SD = Sa(T)*g/lam; X2 = GAM*V[1]*SD
def modes():
    cv = fit(440, 460, (-1.6, 6.4), (-0.8, 7.2), L=14, R=14, T=48, B=14)
    cv.text_px(220, 18, "振態形狀（下層分量取 1）", 14.5, C["text"], weight="700")
    for j in range(2):
        x0 = 0.6 + j*3.4; sc = 0.9
        ground(cv, (x0 - 0.6, 0), (x0 + 0.6, 0))
        pts = [(x0, 0), (x0 + sc*V[0, j], 2.6), (x0 + sc*V[1, j], 5.2)]
        cv.line((x0, 0), (x0, 5.2), C["ghost"], 1.6, dash="5 4")
        cv.poly(pts, C["deform"], 2.6)
        for p, val in zip(pts[1:], V[:, j]):
            cv.dot(p, 6, C["deform"]); cv.text(p, f"{val:.3f}", 12.5, C["deform"], "start", dx=9)
        cv.text((x0, -0.4), f"振態 {j+1}：T = {T[j]:.3f} s", 12.5, C["text"], dy=6)
        cv.text((x0, 6.2), f"Γ = {GAM[j]:.4f}", 12.5, C["muted"])
    return cv
def spectrum():
    cv = Canvas(440, 460, sx=1, bg="#FFFFFF")
    cv.text_px(220, 18, "設計反應譜與取值點", 14.5, C["text"], weight="700")
    ax = Axes(cv, 60, 110, 360, 280, (0, 3.0), (0, 0.8))
    ax.frame([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.2, 0.4, 0.6, 0.8], "T (s)", "S_a (g)")
    t = np.linspace(0.05, 3, 600); ax.curve(t, Sa(t), C["member"], 2.4)
    ax.hline(0.7, C["accent"]); ax.label(3.0, 0.7, "上限 0.7 g（T 小於 0.643 s）", C["accent"], "end", dx=-4, dy=-12)
    for j in range(2):
        ax.vline(T[j], C["dim"], "3 3", y1=Sa(T[j])); ax.dot(T[j], Sa(T[j]), C["deform"])
        ax.label(T[j], Sa(T[j]), f"T{j+1} = {T[j]:.3f} s，S_{{a}} = {Sa(T[j]):.4f} g", C["deform"], "end" if j == 0 else "start", dx=-8 if j == 0 else 8, dy=-44 if j == 0 else -14)
    cv.text_px(220, 420, f"S_{{d}} = {SD[0]:.4f}、{SD[1]:.4f} m；頂樓 {X2[0]:.4f}、{X2[1]:.4f} m", 12.5, C["text"])
    cv.text_px(220, 440, f"SRSS 頂樓位移 = {np.hypot(*X2):.3f} m", 12.5, C["text"], weight="700")
    return cv
def fig2():
    return compose([modes(), spectrum()], title="圖 2　振態形狀與反應譜取值（SRSS 頂樓位移）",
                   note="兩個週期都落在 0.45/T 下降段，0.7 g 上限不控制；第二振態頂樓分量與第一振態反號",
                   path=f"{OUT}/{TAG}-fig-2-spectrum.svg")
FIGURES = [(fig2, "頂樓取錯振態分量（用了下層分量）；未檢查 0.7 g 上限；S_a 以 g 計未乘 g")]

if __name__ == "__main__":
    print("T =", T, "Γ =", GAM, "Sd =", SD, "X2 =", X2, np.hypot(*X2))
    for fn, cc in FIGURES: fn(); print(fn.__name__, "—", cc)
