#!/usr/bin/env python3
"""SD-2015-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 穩態振幅放大係數 Rd 與相位角 θ 對頻率比 β（ξ 取 0.05、0.1、0.2、0.5 示意）；公式取自 §5。
用法：python3 gen_SD-2015-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2015-1"
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

XIS = [0.05, 0.1, 0.2, 0.5]; LAB = {0.05: (1.25, 4.6), 0.1: (1.25, 3.9), 0.2: (1.25, 2.4), 0.5: (0.45, 1.45)}; COLS = [C["load"], C["accent"], C["deform"], C["bmd"]]
b = np.linspace(0.001, 3, 900)
def left():
    cv = Canvas(480, 380, sx=1, bg="#FFFFFF"); cv.text_px(240, 24, "R_{d} = 1/√[(1−β²)² + (2ξβ)²]", 14, C["text"], weight="700")
    ax = Axes(cv, 60, 60, 390, 270, (0, 3), (0, 5)); ax.frame([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 1, 2, 3, 4, 5], "β = ω̄/ω", "R_{d}")
    for xi, col in zip(XIS, COLS):
        ax.curve(b, np.minimum(1/np.sqrt((1 - b**2)**2 + (2*xi*b)**2), 5), col, 2.2)
        ax.label(*LAB[xi], f"ξ = {xi:g}", col, dx=0)
    return cv
def right():
    cv = Canvas(480, 380, sx=1, bg="#FFFFFF"); cv.text_px(240, 24, "θ = arctan[2ξβ/(1−β²)]（0～180°）", 14, C["text"], weight="700")
    ax = Axes(cv, 60, 60, 390, 270, (0, 3), (0, 180)); ax.frame([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 45, 90, 135, 180], "β = ω̄/ω", "θ (°)")
    for xi, col in zip(XIS, COLS):
        ax.curve(b, np.degrees(np.arctan2(2*xi*b, 1 - b**2)), col, 2.2)
    ax.hline(90, C["muted"]); ax.label(1.0, 90, "β = 1 時 θ = 90°（與 ξ 無關）", C["muted"], dy=-12)
    return cv
def fig2():
    return compose([left(), right()], title="圖 2　穩態反應的振幅與相位", note="β > 1 時 1 − β² < 0，θ 要取 90°～180°（用 atan2，不可直接用計算機 tan^-1）",
                   path=f"{OUT}/{TAG}-fig-2-steady.svg")
FIGURES = [(fig2, "相位角在 β > 1 時取錯象限；以為共振峰在 β 恰為 1 以外")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
