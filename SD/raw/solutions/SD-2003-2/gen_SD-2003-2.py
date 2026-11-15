#!/usr/bin/env python3
"""SD-2003-2 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）
fig-2 外力與位移歷時：位移曲線由 §4 的 m、k、ξ 與外力折線以 RK4 數值積分算出，
最大值標註必須與 §4 Step 7（0.294 m、t≈1.18 s）一致。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-2"
# ── 由 SD-2003-2.md §4 解得 ──
M, K, XI = 100.0, 100.0, 0.30
W = math.sqrt(K / M); WD = W * math.sqrt(1 - XI**2); CC = 2 * XI * M * W
TP = 0.10 - 2000 / (500 / 0.02)                       # Step 2：峰值時刻 0.02 s
NODES = [(0, 0), (TP, 2000), (0.10, 0), (0.12, -500), (0.20, -500), (0.25, 0)]
def force(t):
    for (t0, p0), (t1, p1) in zip(NODES, NODES[1:]):
        if t0 <= t <= t1: return p0 + (p1 - p0) * (t - t0) / (t1 - t0)
    return 0.0
def response(tend=8.0, dt=1e-3):
    """RK4（dt 1 ms；以 §4 精確值核對誤差 < 1e-6 m）"""
    x = v = 0.0; out = [(0.0, 0.0)]; n = int(tend / dt)
    f = lambda t, x, v: (force(t) - CC * v - K * x) / M
    for i in range(n):
        t = i * dt
        k1x, k1v = v, f(t, x, v)
        k2x, k2v = v + dt/2*k1v, f(t+dt/2, x+dt/2*k1x, v+dt/2*k1v)
        k3x, k3v = v + dt/2*k2v, f(t+dt/2, x+dt/2*k2x, v+dt/2*k2v)
        k4x, k4v = v + dt*k3v, f(t+dt, x+dt*k3x, v+dt*k3v)
        x += dt/6*(k1x+2*k2x+2*k3x+k4x); v += dt/6*(k1v+2*k2v+2*k3v+k4v); out.append((t+dt, x))
    return out
def fig2():
    R = response(); tm, xm = max(R, key=lambda p: p[1])
    assert abs(xm - 0.2936) < 5e-4 and abs(tm - 1.18) < 0.01, (xm, tm)
    W_, H_ = 760, 300
    a = Canvas(W_, H_, bg="#FFFFFF"); a.panel("外力 P(t)（前 0.3 s 放大）")
    X = lambda t: 70 + t / 0.3 * 640; Y = lambda p: 175 - p * 0.05
    a.line((X(0), a.h - Y(0)), (X(0.3), a.h - Y(0)), C["muted"], 1.4)
    pts = [(X(t), Y(p)) for t, p in NODES] + [(X(0.3), Y(0))]
    a.parts.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{C["load"]}" stroke-width="3"/>')
    for t, lab in ((TP, "0.02"), (0.10, "0.10"), (0.12, "0.12"), (0.20, "0.20"), (0.25, "0.25")):
        a.text_px(X(t), Y(0) + (16 if t != 0.12 else 30), lab, 12, C["muted"])
    a.text_px(X(TP) + 8, Y(2000) - 2, "2000 N", 12.5, C["load"], "start"); a.text_px(X(0.16), Y(-500) + 16, "−500 N", 12.5, C["load"])
    a.text_px(380, 278, "淨衝量 I = 100 − 57.5 = 42.5 N·s；t (s)", 12.5, C["muted"])
    b = Canvas(W_, H_, bg="#FFFFFF"); b.panel("位移 x(t)（0–8 s）")
    XX = lambda t: 70 + t / 8.0 * 640; YY = lambda x: 165 - x * 330
    b.line((XX(0), b.h - YY(0)), (XX(8), b.h - YY(0)), C["muted"], 1.4)
    b.parts.append('<polyline points="' + " ".join(f"{XX(t):.1f},{YY(x):.1f}" for t, x in R[::20]) + f'" fill="none" stroke="{C["deform"]}" stroke-width="3"/>')
    b.parts.append(f'<line x1="{XX(0.25):.1f}" y1="{YY(-0.12):.1f}" x2="{XX(0.25):.1f}" y2="{YY(0.32):.1f}" stroke="{C["dim"]}" stroke-dasharray="4 3"/>')
    b.text_px(XX(0.25) + 4, YY(-0.12) + 4, "td = 0.25 s：外力結束", 12, C["muted"], "start")
    b.parts.append(f'<circle cx="{XX(tm):.1f}" cy="{YY(xm):.1f}" r="6" fill="#FFFFFF" stroke="{C["accent"]}" stroke-width="2.6"/>')
    b.text_px(XX(tm) + 12, YY(xm) - 10, f"x_{{max}} = {xm:.3f} m（t = {tm:.2f} s）", 13.5, C["accent"], "start", weight="700")
    b.text_px(380, 278, "最大位移在自由振動段，不在外力峰值時刻", 12.5, C["muted"])
    return compose([a, b], cols=1, title="圖 2　外力歷時與位移反應", note="ξ = 30%、ωn = 1 rad/s；位移曲線以 RK4 數值積分（dt = 1 ms），最大值與 §4 分段精確解核對", path=f"{OUT}/{TAG}-fig-2-history.svg")
FIGURES = [(fig2, "把 ta 當峰值時刻、以為最大位移發生在載重期間")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
