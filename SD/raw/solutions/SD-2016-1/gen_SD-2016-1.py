#!/usr/bin/env python3
"""SD-2016-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 2 階段 E）
fig-2 衝量近似與精確解（無阻尼數值積分）的位移歷時；近似式取自 §4 ⑤，最大值取自 ⑥（勘誤後）。
用法：python3 gen_SD-2016-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2016-1"
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

m, k = 2e3, 1e5; P0, TD, TC = 2.4e5, 0.2, 0.1
Mm = np.diag([2*m, m]); Kk = np.array([[3*k, -k], [-k, k]])
def exact(t_end=2.6, dt=1e-3):
    from scipy.integrate import solve_ivp
    p = lambda t: P0*t/0.1 if t <= 0.1 else (P0*(TD - t)/0.1 if t <= TD else 0.0)
    f = lambda t, y: np.r_[y[2:], np.linalg.solve(Mm, np.array([0, p(t)]) - Kk @ y[:2])]
    t = np.arange(0, t_end, dt); s = solve_ivp(f, [0, t_end], [0, 0, 0, 0], t_eval=t, max_step=1e-3, rtol=1e-9, atol=1e-12)
    return t, s.y[0], s.y[1]
def fig2():
    t, e1, e2 = exact(); tau = np.clip(t - TC, 0, None)
    a1 = 0.8*np.sin(5*tau) - 0.4*np.sin(10*tau); a2 = 1.6*np.sin(5*tau) + 0.4*np.sin(10*tau)   # §4 ⑤
    panels = []
    for name, a, e in (("v1（二樓）", a1, e1), ("v2（屋頂）", a2, e2)):
        cv = Canvas(480, 360, sx=1, bg="#FFFFFF"); cv.text_px(240, 24, name, 14.5, C["text"], weight="700")
        ax = Axes(cv, 60, 60, 390, 250, (0, 2.6), (-2, 2)); ax.frame([0, 0.5, 1, 1.5, 2, 2.5], [-2, -1, 0, 1, 2], "t (s)", "位移 (m)")
        ax.cv.polygon([ax.P(0, -2), ax.P(TD, -2), ax.P(TD, 2), ax.P(0, 2)], C["fill_t"], "none")
        ax.curve(t, e, C["member"], 2.2); ax.curve(t, a, C["deform"], 2.2, dash="7 4")
        ia, ie = np.abs(a).argmax(), np.abs(e).argmax()
        ax.dot(t[ia], a[ia], C["deform"]); ax.label(t[ia], a[ia], f"近似 {abs(a[ia]):.3f}", C["deform"], "end" if t[ia] > 1.8 else "start", dx=-8 if t[ia] > 1.8 else 8, dy=-14 if a[ia] > 0 else 14)
        ax.dot(t[ie], e[ie], C["member"]); ax.label(t[ie], e[ie], f"精確 {abs(e[ie]):.3f}", C["member"], dy=14 if e[ie] > 0 else -14)
        panels.append(cv)
    return compose(panels, title="圖 2　三角形脈衝下的位移歷時：精確解（實線）與衝量近似（虛線）",
                   note="紅底為脈衝期間 0–0.2 s；最大位移直接取歷時最大值，不是 SRSS（√(0.8²+0.4²) = 0.894 會低估）", path=f"{OUT}/{TAG}-fig-2-history.svg")
FIGURES = [(fig2, "把確定性時間歷時的最大值用 SRSS 估；忽略衝量近似的時間原點")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
