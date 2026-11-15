#!/usr/bin/env python3
"""SD-2012-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 反應譜 Sa(T) 與兩個週期的落點；fig-2 右側比較地震力與位移。數值取自計算彙整。
用法：python3 gen_SD-2012-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2012-1"
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

T1, T2 = 1.2, 1.4; S1, S2 = 0.12/T1, 0.12/T2      # 計算彙整
F1, F2 = 4906, 5724; X1, X2 = 3.58, 4.17          # N、cm
def left():
    cv = Canvas(480, 380, sx=1, bg="#FFFFFF")
    ax = Axes(cv, 70, 60, 380, 270, (0, 2.0), (0, 0.25))
    ax.frame([0, 0.6, 1.2, 1.4, 2.0], [0, 0.05, 0.10, 0.15, 0.20, 0.25], "T (s)", "S_{a}")
    T = np.linspace(0.01, 2.0, 400); ax.curve(T, np.where(T <= 0.6, 0.2, 0.12/T), C["deform"], 2.6)
    for T_, S_, lab in ((T1, S1, "(a) m1"), (T2, S2, "(b) m2")):
        ax.vline(T_, C["dim"], y1=S_); ax.dot(T_, S_); ax.label(T_, S_, f"{lab}：{S_:.4f}", C["accent"], dy=-14)
    cv.text_px(240, 24, "兩週期都在 Sa = 0.12/T 段", 14.5, C["text"], weight="700")
    return cv
def right():
    cv = Canvas(480, 380, sx=1, bg="#FFFFFF")
    cv.text_px(240, 24, "加質量後：力與位移都 ×1.167", 14.5, C["text"], weight="700")
    for i, (name, a, b, unit) in enumerate((("彈性地震力", F1, F2, "N"), ("最大位移", X1, X2, "cm"))):
        y = 270 - i*130; peak = max(a, b)
        for j, (v, lab, col) in enumerate(((a, "m1", C["member2"]), (b, "m2", C["deform"]))):
            yy = y - j*42; cv.rect_px(130, 380 - yy - 15, 260*v/peak, 30, col, 6)
            cv.text_px(122, 380 - yy, lab, 13, C["text"], "end")
            cv.text_px(136 + 260*v/peak, 380 - yy, f"{v:,.2f} {unit}" if unit == "cm" else f"{v:,.0f} {unit}", 13, C["text"], "start")
        cv.text_px(60, 380 - y + 21 - 42, name, 13, C["text"])
    return cv
def fig2():
    return compose([left(), right()], title="圖 2　反應譜取值與兩屋架的地震力、位移",
                   note="F = Sa·mg 與 x = F/k 都與 T 成正比（下降段）：質量增加 → 週期變長 → 力反而變大", path=f"{OUT}/{TAG}-fig-2-spectrum.svg")
FIGURES = [(fig2, "以為週期變長、Sa 變小，地震力就變小")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
