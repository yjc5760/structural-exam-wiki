#!/usr/bin/env python3
"""SD-2016-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 α–β 平面上三條正交方程（I）(II)(III) 的直線與交點；方程取自 §4、§5.2（勘誤後）。
用法：python3 gen_SD-2016-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2016-3"
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

EQ = {"(I) φ1⊥φ2：α + 2β = 6000": (1, 2, 6000), "(II) φ1⊥φ₃：α − 2β = −3000": (1, -2, -3000), "(III) φ2⊥φ₃：−α + β = −2000": (-1, 1, -2000)}
COL = [C["deform"], C["load"], C["bmd"]]
def fig2():
    cv = Canvas(760, 470, sx=1, bg="#FFFFFF"); cv.text_px(380, 26, "圖 2　三條正交方程不交於一點：考卷數據自相矛盾", 15.5, C["text"], weight="700")
    ax = Axes(cv, 80, 70, 420, 340, (0, 8000), (0, 6000)); ax.frame(range(0, 8001, 2000), range(0, 6001, 2000), "α (kg)", "β (kg)")
    a = np.linspace(0, 8000, 400); L = list(EQ.values())
    for (name, (p, q, r)), col, k in zip(EQ.items(), COL, range(3)):
        ax.curve(a, (r - p*a)/q, col, 2.4); cv.text_px(520, 380 - (90 + k*26), name, 12.5, col, "start")
    pts = {"本解 (I)(II)": (1500, 2250), "(I)(III)": (10000/3, 4000/3), "(II)(III)": (7000, 5000)}
    for k, (n, (x, y)) in enumerate(pts.items()):
        ax.dot(x, y, C["accent"] if k == 0 else C["muted"]); ax.label(x, y, f"{n}：({x:.0f}, {y:.0f})", C["accent"] if k == 0 else C["muted"], dy=-12)
    cv.text_px(520, 380 - 190, "代入本解：(III) 殘差 = 2750 ≠ 0", 12.5, C["text"], "start")
    cv.text_px(520, 380 - 214, "取哪兩條，答案就不同", 12.5, C["muted"], "start")
    return cv.save(f"{OUT}/{TAG}-fig-2-orthogonality.svg")
FIGURES = [(fig2, "以為第三條正交條件是冗餘、必然成立")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
