#!/usr/bin/env python3
"""SD-2017-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 阻尼自由振動歷時與包絡線：ξ 取自題目（0.05），初始條件 v(0)=v0、初速 0；第 3 週振幅取自 §4 Step 5。
用法：python3 gen_SD-2017-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2017-1"
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

XI = 0.05                                   # 題給阻尼比
WD = math.sqrt(1 - XI**2)                   # ω_D/ω（ω 取 1，時間以 T_D 為單位）
def v(tn):                                  # 精確解 v/v0，tn = t/T_D
    t = tn * 2*math.pi/WD
    return np.exp(-XI*t) * (np.cos(WD*t) + XI/WD*np.sin(WD*t))
A3 = math.exp(-6*math.pi*XI)                # §4 Step 5：v0·e^{-0.3π}
AH = math.exp(-3*math.pi*XI)                # 誤讀成 3 個半週期（1.5 T_D）的振幅
def fig2():
    cv = Canvas(760, 400, sx=1, bg="#FFFFFF")
    ax = Axes(cv, 70, 70, 640, 260, (0, 3.4), (-1.1, 1.1))
    ax.frame([0, 0.5, 1, 1.5, 2, 2.5, 3], [-1, -0.5, 0, 0.5, 1], "t / T_D", "v / v0")
    tn = np.linspace(0, 3.4, 1200)
    env = np.exp(-XI*tn*2*math.pi/WD)
    ax.curve(tn, env, C["accent"], 1.6, dash="6 4"); ax.curve(tn, -env, C["accent"], 1.6, dash="6 4")
    ax.curve(tn, v(tn), C["deform"], 2.4)
    for n in (1, 2, 3): ax.vline(n, C["dim"], "3 4", 1.0)
    ax.dot(3, float(v(np.array([3.0]))[0]), C["load"]); ax.label(3, 0.85, f"來回 3 次（t = 3T_D）：{A3:.3f} v0 ↓", C["load"], "end", dx=-4)
    ax.dot(1.5, -AH, C["muted"]); ax.label(1.5, -AH, f"誤讀 3 個半週期：{AH:.3f} v0", C["muted"], "start", dx=10, dy=14)
    ax.label(0.05, 1.0, "包絡線 v0·exp(−ξωt)", C["accent"], "start", dx=30, dy=-4)
    return compose([cv], title="圖 2　阻尼自由振動（ξ = 0.05，初始位移 v0、初速 0）",
                   note="每完成一週振幅乘 exp(−2πξ) = 0.730；3 週後 exp(−0.3π) = 0.390", path=f"{OUT}/{TAG}-fig-2-decay.svg")
FIGURES = [(fig2, "「來回 3 次」誤當 3 個半週期（0.624 v0）；振幅與位移 v(t) 混淆")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
