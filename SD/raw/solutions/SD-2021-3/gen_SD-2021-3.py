#!/usr/bin/env python3
"""SD-2021-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 初始變形形狀：粗索只拉一樓版的靜力平衡形狀 {6,6,6} 與舊解 {6,0,0} 對照（§4 Step 1、§5）。
fig-3 頂層層剪力歷時 V3(t)/k：勘誤後 cos ω1t − 2cos ω2t + cos ω3t 與舊讀法對照，標 ±4k 上確界（§4 Step 6–7）。
所有係數由題給 ω、φ 與初始位移以振態展開重算，不寫死。
用法：python3 gen_SD-2021-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2021-3"
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

# ── 題給（題目正本 §2）與 §4 振態展開 ──
s3 = np.sqrt(3)
M = np.diag([1, 1, 0.5])                                  # ×m
W = np.sqrt([2 - s3, 2, 2 + s3])                          # ×√(k/m)
PHI = np.array([[1, 1, 1], [s3, 0, -s3], [2, -1, 2.]])    # 欄 = φ1、φ2、φ3（分量 v1、v2、v3）
def v3_coef(u0):
    q0 = (PHI.T @ M @ u0) / np.diag(PHI.T @ M @ PHI)      # A_i（§4 Step 4）
    return q0, q0 * (PHI[2] - PHI[1])                     # V3/k 各振態係數（cm）
U_NEW, U_OLD = np.array([6, 6, 6.]), np.array([6, 0, 0.])
H, BW, TS = 2.0, 3.0, 0.26
def frame_panel(u, title, sub, extra):
    cv = fit(430, 400, (-1.2, 6.6), (-1.0, 7.4), L=14, R=14, T=40, B=14)
    cv.text_px(215, 18, title, 14.5, C["text"], weight="700"); cv.text_px(215, 38, sub, 12, C["muted"])
    ground(cv, (-0.8, 0), (BW + 1.6, 0))
    sc = 0.11                                             # 6 cm → 0.66 示意放大
    xs = [0.0] + [ui * sc for ui in u]
    eta = np.linspace(0, 1, 30)
    for i in range(3):
        d0, d1 = xs[i], xs[i + 1]
        for x in (0, BW):
            pts = [(x + d0 + (d1 - d0) * (3*e**2 - 2*e**3), i*H + e*H) for e in eta]
            cv.poly(pts, C["member"], 2.4)
            cv.line((x, i*H), (x, (i + 1)*H), C["ghost"], 1.0, dash="4 4")
        y = (i + 1) * H
        cv.polygon([(d1, y - TS/2), (d1 + BW, y - TS/2), (d1 + BW, y + TS/2), (d1, y + TS/2)], "#C9CED6", C["member"], 1.6)
        cv.text((d1 + BW, y), f"{u[i]:g} cm", 13, C["deform"], "start", dx=10)
        drift = u[i] - (u[i - 1] if i else 0)
        cv.text((-0.3, i*H + H/2), f"層剪力 {drift:g}k", 12, C["sfd"], "end")
    extra(cv)
    return cv
def ex_new(cv):
    cv.arrow((0.66 + BW + 1.2, H - 0.55), (0.66 + BW + 2.4, H - 0.55), C["load"], 2.8, 9)
    cv.text((0.66 + BW + 1.2, H - 0.55), "F = 6k", 12.5, C["load"], "end", dx=-4)
def ex_old(cv):
    cv.arrow((0.66 + BW + 1.2, H - 0.55), (0.66 + BW + 2.4, H - 0.55), C["load"], 2.8, 9)
    cv.text((0.66 + BW + 1.2, H - 0.55), "12k", 12.5, C["load"], "end", dx=-4)
    cv.arrow((BW + 2.4, 2*H + 0.5), (BW + 1.2, 2*H + 0.5), C["load"], 2.8, 9)
    cv.text((BW + 2.4, 2*H + 0.5), "6k（題目沒有）", 12.5, C["load"], "start", dx=4)
def fig2():
    a = frame_panel(U_NEW, "正確：{6, 6, 6} cm", "只有一層柱有層剪力，上兩層剛體平移", ex_new)
    b = frame_panel(U_OLD, "舊解：{6, 0, 0} cm", "二樓版須另加向左 6k 才能靜止", ex_old)
    return compose([a, b], title="圖 2　粗索只拉一樓版時的初始變形（靜力平衡形狀）",
                   note="層剪力以 k×cm 表示；{6,0,0} 需要考卷沒有的二樓外力，不是「拉一樓」的平衡形狀",
                   path=f"{OUT}/{TAG}-fig-2-initial.svg")
def fig3():
    _, cn = v3_coef(U_NEW); _, co = v3_coef(U_OLD)
    t = np.linspace(0, 30, 3001)
    vn = (cn[None, :] * np.cos(np.outer(t, W))).sum(1); vo = (co[None, :] * np.cos(np.outer(t, W))).sum(1)
    cv = Canvas(860, 450, sx=1, bg="#FFFFFF")
    cv.text_px(430, 22, "頂層層剪力 V_{3}(t)/k（cm），t 以 √(m/k) 為單位", 14, C["text"], weight="700")
    ax = Axes(cv, 70, 70, 760, 290, (0, 30), (-8.5, 8.5))
    ax.frame([0, 5, 10, 15, 20, 25, 30], [-8, -4, 0, 4, 8], "t·√(k/m)", "V3/k (cm)")
    ax.curve(t, vo, C["muted"], 1.4, dash="5 4"); ax.curve(t, vn, C["deform"], 2.2)
    sup = np.abs(cn).sum(); ax.hline(-sup, C["accent"]); ax.hline(sup, C["accent"])
    ax.label(0.2, -sup, f"−{sup:g}k（上確界，可任意逼近）", C["accent"], "start", dx=4, dy=14)
    ax.label(0.3, 7.6, f"舊解 {{6,0,0}}：上確界 {np.abs(co).sum():g}k", C["muted"], "start", dx=4)
    i = np.argmin(vn); ax.dot(t[i], vn[i], C["deform"])
    cv.legend(250, 432, [(C["deform"], "勘誤後 {6,6,6}")]); cv.legend(470, 432, [(C["muted"], "舊解 {6,0,0}（虛線）")])
    return cv.save(f"{OUT}/{TAG}-fig-3-v3.svg")
FIGURES = [(fig2, "把「拉一樓」讀成只有一樓位移 {6,0,0}"),
           (fig3, "用 SRSS 估自由振動最大值；初始形狀錯導致層剪力加倍")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
