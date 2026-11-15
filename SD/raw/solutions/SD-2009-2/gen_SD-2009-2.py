#!/usr/bin/env python3
"""SD-2009-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 無阻尼傳遞率 TR(β)＝1/|1−β²|；設計點 TR＝50/700 取自 §4（β²＝15），k 取自 §4 結果。
用法：python3 gen_SD-2009-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2009-2"
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

TR_T = 50/700                 # §4：隔振後／隔振前
BETA = math.sqrt(1 + 1/TR_T)  # §4：β² − 1 = 1/TR → β = √15
K_RES = 6382                  # §4 結果（lb/in）
def fig2():
    cv = Canvas(760, 430, sx=1, bg="#FFFFFF")
    cv.text_px(380, 26, "圖 2　無阻尼傳遞率與設計點", 16, C["text"], weight="700")
    ax = Axes(cv, 80, 70, 620, 290, (0, 5), (0, 3))
    ax.frame([0, 1, 2, 3, 4, 5], [0, 0.5, 1, 1.5, 2, 2.5, 3], "頻率比 β = ω/ω_{n}", "TR")
    b = np.linspace(0, 5, 801)
    with np.errstate(divide="ignore"): tr = 1/np.abs(1 - b**2)
    for seg in (b < 0.985, b > 1.015):
        ax.curve(b[seg], np.minimum(tr[seg], 3), C["deform"], 2.6)
    ax.vline(math.sqrt(2)); ax.label(math.sqrt(2), 2.7, "β = √2：TR = 1", C["muted"])
    ax.hline(1, C["muted"])
    ax.dot(BETA, TR_T); ax.label(BETA, TR_T + 0.25, f"設計點 β = √15 = {BETA:.3f}，TR = 1/14", C["accent"], "middle", dx=0)
    cv.text_px(380, 412, f"β > √2 才有隔振效果；由 TR = 1/(β² − 1) 得 β² = 15，k = mω²/15 ≈ {K_RES:,} lb/in", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-tr.svg")
FIGURES = [(fig2, "把設計點放在 β < √2（TR > 1）那一支；或把 12 Hz 當 rad/s")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
