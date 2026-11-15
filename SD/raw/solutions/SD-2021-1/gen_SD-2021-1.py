#!/usr/bin/env python3
"""SD-2021-1 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 3 階段 E）
fig-2 台車絕對速度歷時：ẋ/ω 對 ωt，由 §4 的通解（x(0)=0、ẋ(0)=0，構架 d=sin(ωt/2)）逐點計算；
另以細虛線畫「台車相對構架靜止」的替代讀法，攔初始條件誤設。
用法：python3 gen_SD-2021-1.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2021-1"
# ── §4：u = x − d，ü + ω²u = (ω²/4) sin(ωt/2)；u_p = (1/3) sin(ωt/2) ──
A_P = (1/4)/(1 - (1/2)**2)               # 特解振幅 1/3（r = 1/2）
C2 = (-0.5 - A_P*0.5)                     # u̇(0) = −ω/2 → C2 = −2/3（定案：台車絕對速度 0）
C2_ALT = -A_P*0.5                         # 替代讀法：u̇(0) = 0 → C2 = −1/6
def xdot(tau, c2):                        # ẋ/ω，tau = ωt
    return c2*math.cos(tau) + A_P*0.5*math.cos(tau/2) + 0.5*math.cos(tau/2)
def ddot(tau): return 0.5*math.cos(tau/2)  # 構架速度 ḋ/ω
TMAX = 4*math.pi; WM, HM = 14.0, 4.6; YR = 1.6
def P(tau, y): return (tau/TMAX*WM, (y/YR)*HM/2)
def fig2():
    cv = Canvas(1000, 470, sx=60, ox=70, oy=235, bg="#FFFFFF")
    cv.panel("台車絕對速度 v(t)/ω 對 ωt（v = dx/dt）", "x(0) = 0、v(0) = 0；構架 d(t) = sin(ωt/2)，構架速度在 t = 0 為 ω/2")
    for y in (-1.5, -1.0, -0.5, 0.5, 1.0, 1.5):
        cv.line(P(0, y), P(TMAX, y), "#E8ECF2", 1.1)
        cv.text_px(cv.X(0) - 8, cv.Y(P(0, y)[1]) + 4, f"{y:g}", 12, C["muted"], "end")
    cv.line(P(0, 0), P(TMAX, 0), C["muted"], 1.8); cv.line(P(0, -YR), P(0, YR), C["muted"], 1.8)
    for k in range(1, 5):
        cv.line(P(k*math.pi, -YR), P(k*math.pi, YR), "#E8ECF2", 1.1)
        cv.text_px(cv.X(P(k*math.pi, 0)[0]), cv.Y(P(0, -YR)[1]) + 18, f"{k}π", 12.5, C["muted"])
    N = 400; ts = [TMAX*i/N for i in range(N+1)]
    cv.poly([P(t, ddot(t)) for t in ts], C["ghost"], 2.0, dash="5 4")
    cv.poly([P(t, xdot(t, C2_ALT)) for t in ts], C["muted"], 1.8, dash="7 5")
    cv.poly([P(t, xdot(t, C2)) for t in ts], C["deform"], 3.4)
    cv.dot(P(0, 0), 0.08, fill=C["deform"])
    cv.dot(P(0, xdot(0, C2_ALT)), 0.07, fill=C["muted"])
    tpk = max(ts, key=lambda t: abs(xdot(t, C2))); vpk = xdot(tpk, C2)
    cv.dot(P(tpk, vpk), 0.08, fill=C["accent"])
    cv.text_px(cv.X(P(tpk, 0)[0]) + 14, cv.Y(P(0, vpk)[1]) + 6, f"|v| 最大 {abs(vpk):.3f}ω（ωt = {tpk/math.pi:.0f}π）", 13, C["accent"], "start")
    cv.text_px(cv.X(P(0, 0)[0]) + 12, cv.Y(P(0, 0)[1]) + 22, "v(0) = 0（定案）", 13, C["deform"], "start")
    cv.text_px(cv.X(P(0, 0)[0]) + 12, cv.Y(P(0, 1.0)[1]) + 4, f"替代讀法起點 v(0) = {xdot(0, C2_ALT):.2f}ω", 12.5, C["muted"], "start")
    cv.text_px(cv.X(P(TMAX, 0)[0]) - 4, cv.Y(P(0, 1.45)[1]), "藍實線：(2ω/3)[cos(ωt/2) − cos ωt]（定案）", 12.5, C["deform"], "end")
    cv.text_px(cv.X(P(TMAX, 0)[0]) - 4, cv.Y(P(0, 1.22)[1]), "深灰虛線：替代讀法 (ω/6)[4cos(ωt/2) − cos ωt]　淺灰虛線：構架速度", 12, C["muted"], "end")
    cv.text_px(cv.X(P(TMAX, 0)[0]), cv.Y(P(0, -YR)[1]) + 40, "ωt", 13, C["text"], "end")
    return compose([cv], title="圖 2　台車絕對速度歷時（無阻尼，r = 1/2）",
                   note="台車由絕對靜止開始，曲線從 0 出發；構架本身在 t = 0 已有速度 ω/2，所以台車相對構架的初速度是 −ω/2，不是 0",
                   path=f"{OUT}/{TAG}-fig-2-velocity.svg")
FIGURES = [(fig2, "初始條件把 u̇(0) 設為 0（台車絕對速度變成 ω/2）；忘了加回構架速度 ḋ")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
    print("C2", C2, "C2_ALT", C2_ALT, "check xdot(0)", xdot(0, C2), xdot(0, C2_ALT))
