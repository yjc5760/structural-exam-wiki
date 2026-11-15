#!/usr/bin/env python3
"""SD-2019-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 等位移法則下的力與位移：m、T、φ1、Sa、μ 取自 §3.5 L1；Γ1、M1*、Ve、Vy、Sd、U 依 §4 公式由程式算出。
用法：python3 gen_SD-2019-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2019-3"
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

m, T, SA, MU, g = 5e4, 1.0, 0.5, 5.0, 9.81
PHI = np.array([0.5, 1.0])
L1 = m*PHI.sum(); M1 = m*(PHI**2).sum(); G1 = L1/M1; MS = L1**2/M1
VE = MS*SA*g/1e3; VY = VE/MU                                  # kN
SD = SA*g*100/(2*math.pi/T)**2                                # cm
U = G1*SD*PHI                                                 # 彈性＝非彈性樓層位移（cm）
DR = np.diff(np.r_[0.0, U])
def left():
    cv = Canvas(360, 380, sx=1, bg="#FFFFFF"); cv.text_px(180, 24, "基礎剪力（kN）", 14.5, C["text"], weight="700")
    ax = Axes(cv, 70, 60, 260, 270, (0, 3), (0, 500)); ax.frame([], [0, 100, 200, 300, 400, 500], "", "")
    for i, (val, name, col) in enumerate(((VE, "彈性 Ve", C["member2"]), (VY, "韌性 5 時 Vy", C["load"]))):
        x = 0.6 + i*1.3
        cv.polygon([ax.P(x - 0.4, 0), ax.P(x + 0.4, 0), ax.P(x + 0.4, val), ax.P(x - 0.4, val)], col, "none", op=0.85)
        ax.label(x, val, f"{val:.2f}", C["text"], "middle", dx=0, dy=-12)
        ax.label(x, 0, name, C["text"], "middle", dx=0, dy=16)
    ax.label(1.25, 250, "÷ μ = 5", C["load"], "middle", dx=0)
    return cv
def right():
    cv = Canvas(380, 380, sx=1, bg="#FFFFFF"); cv.text_px(190, 24, "樓層位移（cm）：彈性 ＝ 非彈性", 14.5, C["text"], weight="700")
    ax = Axes(cv, 70, 60, 270, 270, (0, 18), (0, 2.3)); ax.frame([0, 5, 10, 15], [], "位移 (cm)", "")
    for i, nm in enumerate(("地面", "二樓", "屋頂")): ax.label(0, i, nm, C["muted"], "end", dx=-8)
    pts = [(0, 0)] + [(U[i], i + 1) for i in range(2)]
    ax.cv.poly([ax.P(x, y) for x, y in pts], C["deform"], 3)
    for i in range(2):
        ax.dot(U[i], i + 1, C["deform"]); ax.label(U[i], i + 1, f"u{i+1} = {U[i]:.2f}" if i else f"u1 = {U[i]:.3f}", C["deform"], "end", dx=-12, dy=-12)
        ax.label(U[i] - DR[i]/2, i + 0.5, f"Δ{i+1} = {DR[i]:.3f}", C["accent"], "start", dx=12)
    return cv
def fig2():
    return compose([left(), right()], title="圖 2　等位移法則：力除以 μ，位移不除",
                   note=f"Γ1 = {G1:.1f}、M1* = {MS:,.0f} kg、Sa = {SA}g、Sd = {SD:.3f} cm；層間位移不可再除以 5（{DR[0]/MU:.2f} cm 是折減力下的彈性位移）",
                   path=f"{OUT}/{TAG}-fig-2-equal-disp.svg")
FIGURES = [(fig2, "層間位移跟著力一起除以 μ；用總質量代替有效質量算剪力")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
