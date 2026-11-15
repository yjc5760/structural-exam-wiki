#!/usr/bin/env python3
"""SD-2013-4 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 兩振態等效靜力 f = ω²MφQ 與合計，對地面取矩；數值取自步驟五、六（勘誤後）。
用法：python3 gen_SD-2013-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2013-4"
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

H = [40, 30, 15]
F1 = [8.112, 10.140, 6.084]; F2 = [10.471, -20.941, -18.847]     # 步驟五（Tf）
FS = [a + b for a, b in zip(F1, F2)]
MB = [719.9, -492.1, 227.8]                                        # 步驟六（Tf·m）
def panel(title, F, mb, col):
    cv = Canvas(330, 470, sx=1, bg="#FFFFFF"); cv.panel(title, f"M_{{base}} = {mb:+.1f} Tf·m")
    x0, y0, s, hs = 205, 50, 3.6, 8.0
    cv.line((x0, y0), (x0, y0 + 40*hs), C["member"], 3); cv.line((x0 - 40, y0), (x0 + 40, y0), C["member"], 3)
    for h_, f in zip(H, F):
        y = y0 + h_*hs; cv.dot((x0, y), 5, C["member"])
        if abs(f) > 0.01:
            cv.arrow((x0, y), (x0 + s*f, y), col if f > 0 else C["compr"], 2.6, 9)
            cv.text((x0 + s*f, y), f"{f:+.2f}", 12.5, C["text"], "start" if f > 0 else "end", dx=6 if f > 0 else -6)
        cv.text_px(18, cv.h - y, f"{h_} m", 11.5, C["muted"], "start")
    return cv
def fig2():
    return compose([panel("振態 1", F1, MB[0], C["load"]), panel("振態 2", F2, MB[1], C["load"]), panel("合計（只取兩振態）", FS, MB[2], C["load"])],
                   title="圖 2　等效靜力 f = ω²MφQ（Tf）與底彎矩", note="兩振態底彎矩一正一負，相減後只剩 228 Tf·m；用總加速度 × 質量會帶進第三振態（舊解 401）",
                   path=f"{OUT}/{TAG}-fig-2-forces.svg")
FIGURES = [(fig2, "以總加速度乘質量求內力（含未取振態）；或兩振態用 SRSS")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
