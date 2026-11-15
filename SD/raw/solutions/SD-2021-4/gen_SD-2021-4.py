#!/usr/bin/env python3
"""SD-2021-4 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 彈性穩態位移與降伏位移隨週期變化（T=0.1–0.35 s）：a_g=0.50 g（勘誤後）與 0.75 g（舊讀值）對照（§4 Step 2、㈠）。
fig-3 力–位移關係：彈性需求點、彈性–完全塑性、等位移與等能量法則的韌性比（§4 ㈡）。
數值全部由題給 m、ξ、R_y、地動（0.50 g、T_g=0.3 s、1g=980 cm/s²）計算。
用法：python3 gen_SD-2021-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2021-4"
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

# ── 題給（題目正本 §1、§4）──
m, xi, Ry = 2e6, 0.075, 2.5e7          # kg、—、N
g = 980.0                              # cm/s²（題給）
TG = 0.3; OM = 2*np.pi/TG              # 地動週期與圓頻率
def u_el(T, amp):                      # 穩態彈性位移（cm）
    w = 2*np.pi/T
    return amp*g/np.sqrt((w**2 - OM**2)**2 + (2*xi*w*OM)**2)
def u_y(T):                            # 降伏位移（cm）
    return Ry/(m*(2*np.pi/T)**2)*100
def fig2():
    T = np.linspace(0.1, 0.35, 501)
    cv = Canvas(860, 440, sx=1, bg="#FFFFFF")
    cv.text_px(430, 22, "最大彈性位移與降伏位移 vs 結構週期（ξ = 7.5%）", 14, C["text"], weight="700")
    ax = Axes(cv, 80, 80, 740, 290, (0.1, 0.35), (0, 12))
    ax.frame([0.1, 0.15, 0.2, 0.25, 0.3, 0.35], [0, 2, 4, 6, 8, 10, 12], "結構週期 T (s)", "位移 (cm)")
    cv.polygon([ax.P(0.3, 0), ax.P(0.35, 0), ax.P(0.35, 12), ax.P(0.3, 12)], "rgba(107,118,132,0.10)", "none")
    ax.label(0.325, 11.3, "題給範圍外", C["muted"], "middle", dx=0)
    ax.curve(T, u_el(T, 0.75), C["muted"], 1.6, dash="6 4")
    ax.curve(T, u_el(T, 0.50), C["deform"], 2.4)
    ax.curve(T, u_y(T), C["accent"], 2.0, dash="3 3")
    ue, uo, uy = u_el(0.3, 0.50), u_el(0.3, 0.75), u_y(0.3)
    ax.dot(0.3, ue, C["deform"]); ax.label(0.3, ue, f"7.45 cm（0.50 g）", C["deform"], "end", dx=-10, dy=-4)
    ax.dot(0.3, uo, C["muted"]); ax.label(0.3, uo, f"{uo:.2f} cm（舊讀 0.75 g）", C["muted"], "end", dx=-10)
    ax.dot(0.3, uy, C["accent"]); ax.label(0.3, uy, f"u_{{y}} = {uy:.2f} cm", C["accent"], "start", dx=10, dy=18)
    cv.legend(140, 424, [(C["deform"], "u_{el}，a_{g} = 0.50 g")]); cv.legend(370, 424, [(C["muted"], "舊讀 0.75 g")]); cv.legend(560, 424, [(C["accent"], "u_{y} = R_{y} / k")])
    return cv.save(f"{OUT}/{TAG}-fig-2-resonance.svg")
def fig3():
    k = m*OM**2; ue = u_el(0.3, 0.50); uy = u_y(0.3); Fe = k*ue/100/1e3; Fy = Ry/1e3
    R = Fe/Fy; mu_ed = R; mu_ee = (R**2 + 1)/2
    cv = Canvas(860, 460, sx=1, bg="#FFFFFF")
    cv.text_px(430, 22, "力–位移關係（T = 0.3 s）：等位移與等能量法則", 14, C["text"], weight="700")
    ax = Axes(cv, 90, 80, 720, 310, (0, 12), (0, 70000))
    ax.frame([0, 2, 4, 6, 8, 10, 12], [0, 20000, 40000, 60000], "位移 u (cm)", "力 (kN)", fmt_y="{:,.0f}")
    ax.curve([0, ue], [0, Fe], C["deform"], 2.2, dash="6 4")
    ax.curve([0, uy, 11.5], [0, Fy, Fy], C["member"], 2.6)
    ax.dot(ue, Fe, C["deform"]); ax.label(ue, Fe, f"彈性需求 F_{{e}} = {Fe:,.0f} kN，u_{{el}} = {ue:.2f} cm", C["deform"], "end", dx=-10, dy=-6)
    ax.dot(uy, Fy, C["accent"]); ax.label(uy, Fy, f"R_{{y}} = {Fy:,.0f} kN，u_{{y}} = {uy:.2f} cm", C["accent"], "start", dx=10, dy=18)
    ax.vline(ue, C["deform"], "4 4", y1=Fy); ax.label(ue, 6000, f"等位移 μ = {mu_ed:.2f}", C["deform"], "start", dx=6)
    ue_ee = mu_ee*uy; ax.vline(ue_ee, C["sfd"], "4 4", y1=Fy); ax.label(ue_ee, 14000, f"等能量 μ = {mu_ee:.2f}（{ue_ee:.1f} cm）", C["sfd"], "end", dx=-6)
    cv.text_px(430, 446, "R = F_{e} / R_{y} = 2.61；彈性–完全塑性時間歷時（簡諧共振、降伏後脫離共振）只得 μ ≈ 1.38，兩法則皆偏保守", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-3-ductility.svg")
FIGURES = [(fig2, "地表加速度振幅讀成縱軸上限 0.75 g；週期不確定時取平均週期而非共振"),
           (fig3, "等位移／等能量法則的韌性比混用；忘了先判定 F_e 大於 R_y")]

if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
