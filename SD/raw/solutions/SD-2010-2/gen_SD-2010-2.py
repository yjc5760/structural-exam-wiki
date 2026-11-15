#!/usr/bin/env python3
"""SD-2010-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 B 點位置示意：原位置、新靜平衡位置（δst）、振動上下界（δst ± A）；比例示意，式子取自 §4。
用法：python3 gen_SD-2010-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2010-2"
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

DST, AMP = 1.0, 1.8           # 示意比例（本題全符號；A 與 δst 的關係見 §4：A = √(δst² + 2hδst)）
def fig2():
    cv = Canvas(760, 430, sx=1, bg="#FFFFFF")
    cv.text_px(380, 26, "圖 2　B 點的位置：振幅 A 繞新靜平衡位置量，最大撓度 = δst + A", 15.5, C["text"], weight="700")
    ax = Axes(cv, 90, 60, 600, 300, (0, 4*math.pi), (-(DST + AMP) - 0.4, AMP - DST + 0.8))
    t = np.linspace(0, 3.05*math.pi, 600); x0, v0 = -DST, math.sqrt(AMP**2 - DST**2)
    y = -(DST + (x0*np.cos(t) + v0*np.sin(t)))      # 向下為負：B 點高程 = −(δst + x)
    for yy, s, col in ((0, "原位置（梁未變形）", C["muted"]), (-DST, "新靜平衡位置：δst = mgL³/3EI", C["accent"]),
                       (-(DST + AMP), "最低點：δst + A", C["load"]), (AMP - DST, "最高點：A − δst", C["deform"])):
        ax.hline(yy, col); ax.label(4*math.pi, yy, s, col, "end", dx=0, dy=-10)
    ax.curve(t, y, C["deform"], 2.6)
    ax.dot(0, 0, C["load"]); ax.label(0, 0, "撞擊瞬間：x0 = −δst，v0 = √(2gh)", C["load"], dx=-4, dy=-16)
    cv.line(ax.P(math.pi*0.55, -DST), ax.P(math.pi*0.55, -(DST + AMP)), C["load"], 1.6)
    ax.label(math.pi*0.55, -(DST + AMP/2), "A", C["load"], size=15)
    cv.text_px(390, 405, "時間 →（ω = √(3EI/mL³)）　　比例示意；A = √(δst² + 2hδst)", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-position.svg")
FIGURES = [(fig2, "把 A 當成自原位置量起的撓度；或漏掉撞擊瞬間質量在靜平衡位置上方 δst")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
