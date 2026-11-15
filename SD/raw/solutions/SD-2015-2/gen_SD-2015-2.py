#!/usr/bin/env python3
"""SD-2015-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 兩個振態形狀（φ 取自 §4 Step 3，ω 取自 Step 2，勘誤後）。
用法：python3 gen_SD-2015-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2015-2"
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

W = (6.180, 16.180); PHI = {1: (1.0, 1.618), 2: (1.0, -0.618)}    # §4（v1 二樓, v2 屋頂）
H = 3.0; BW = 4.0
def panel(n):
    cv = Canvas(400, 380, sx=40, ox=150, oy=50, bg="#FFFFFF"); cv.panel(f"第 {n} 振態　ω{n} = {W[n-1]} rad/s", f"{{v1, v2}} = {{{PHI[n][0]:.3f}, {PHI[n][1]:.3f}}}")
    s = 1.0/max(abs(v) for v in PHI[n]) * 1.6
    d1, d2 = PHI[n][0]*s, PHI[n][1]*s
    for x in (0, BW): cv.line((x, 0), (x, 2*H), C["ghost"], 2, dash="5 4")
    for y in (H, 2*H): cv.line((0, y), (BW, y), C["ghost"], 2, dash="5 4")
    sh = lambda u: 3*u**2 - 2*u**3
    for x in (0, BW):
        cv.poly([(x + d1*sh(i/30), H*i/30) for i in range(31)], C["deform"], 3)
        cv.poly([(x + d1 + (d2 - d1)*sh(i/30), H + H*i/30) for i in range(31)], C["deform"], 3)
    cv.line((d1, H), (BW + d1, H), C["deform"], 6); cv.line((d2, 2*H), (BW + d2, 2*H), C["deform"], 6)
    cv.support((0, 0), "fixed"); cv.support((BW, 0), "fixed")
    return cv
def fig2():
    return compose([panel(1), panel(2)], title="圖 2　振態形狀（m1 = m2 = 50 t，k1 = k2 = 50 kN/cm）",
                   note="兩層同質量同勁度：分量比為黃金比例 1.618 與 −0.618；灰虛線為原位置", path=f"{OUT}/{TAG}-fig-2-modes.svg")
FIGURES = [(fig2, "用錯層勁度（舊解 300／200 tf/cm 得 {1,2}、{−2,1}）；第二振態兩樓同向")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
