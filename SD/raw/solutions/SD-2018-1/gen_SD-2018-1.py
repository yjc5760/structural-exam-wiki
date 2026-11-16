#!/usr/bin/env python3
"""SD-2018-1 解題圖解（struct-diagram；2026-11-16，U3-2-G4 階段 E）。可重跑：python3 gen_SD-2018-1.py [輸出目錄]
所有數值由下方常數（題目給定）依 §4 公式算出；題目附圖重繪另見 gen_SD-2018-1_problem.py。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, dashpot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2018-1"
# ── 題目給定 ──
W, H, L, EI, XI, G = 70.0, 3.0, 6.0, 5000.0, 0.05, 9.8
# ── §4 計算 ──
k = 2*12*EI/H**3; m = W/G; w0 = math.sqrt(k/m); T = 2*math.pi/w0
Ld = math.hypot(L, H); cs = L/Ld; th = math.degrees(math.atan2(H, L))
C_ = XI*2*m*w0/cs**2
Sa = min(0.15/T, 0.3)*G; Sd = Sa/w0**2; Sv = w0*Sd; Fd = C_*Sv*cs

def fig2():
    """側移 u 時阻尼器伸長 u·cosθ；軸力水平分量 F·cosθ → c_eff = C cos²θ"""
    cv = fit(680, 390, (-1.2, 9.2), (-0.6, 4.2), L=20, R=20, T=10, B=64)
    u = 1.2                                                          # 側移（放大示意）
    for x in (0, L):
        cv.line((x, 0), (x, H), C["ghost"], 2.0, dash="5 4")
        cv.support((x, 0), "fixed")
    cv.line((0, H), (L, H), C["ghost"], 2.0, dash="5 4")
    for x in (0, L): cv.line((x, 0), (x + u, H), C["member"], 2.6)
    cv.polygon([(u, H - 0.13), (L + u, H - 0.13), (L + u, H + 0.13), (u, H + 0.13)], C["member"], C["member"], 1)
    p0, p1 = (0.0, 0.0), (L + u, H - 0.13)
    cv.line(p0, (L, H - 0.13), C["ghost"], 1.4, dash="4 3")
    cv.line(p0, p1, C["deform"], 2.0)
    for p in (p0, p1): cv.dot(p, 5, "#FFFFFF", C["deform"], 1.8)
    cv.arrow((L, H + 0.55), (L + u, H + 0.55), C["deform"], 2.4, 9); cv.math((L + u/2, H + 0.55), "u", 15, C["deform"], dy=-13)
    # 伸長量 u cosθ：沿斜撐方向投影
    ex, ey = cs, H/Ld
    a = (L, H - 0.13); b = (L + u*ex*ex, H - 0.13 + u*ex*ey)
    cv.line(a, (L + u, H - 0.13), C["accent"], 1.6, dash="3 3")
    cv.line(b, (L + u, H - 0.13), C["accent"], 1.2, dash="2 3")
    cv.text((L + 1.0, H - 0.75), "伸長 δ = u·cosθ", 13, C["accent"], "start")
    cv.text_px(340, 338, f"θ = {th:.1f}°，cosθ = L / L_{{d}} = 6 / {Ld:.3f} = {cs:.4f}", 13, C["text"])
    cv.text_px(340, 368, f"樓層速度 v 時：水平阻尼力 = C·(v cosθ)·cosθ = C cos²θ·v　→　c_{{eff}} = {cs**2:.2f} C", 13, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-damper-geometry.svg")

def fig3():
    """加速度反應譜與本題週期：T = 0.252 s 落在 0.3g 平台段"""
    cv = fit(640, 320, (-0.15, 1.25), (-0.07, 0.36), L=50, R=20, T=10, B=40)
    sx = 1.0
    cv.line((0, 0), (1.15, 0), C["muted"], 1.6); cv.line((0, 0), (0, 0.37), C["muted"], 1.6)
    pts = [(t/200*1.1, min(0.15/max(t/200*1.1, 1e-9), 0.3)) for t in range(1, 201)]
    pts = [(0, 0.3)] + pts
    cv.poly(pts, C["deform"], 2.6)
    cv.line((0.5, 0), (0.5, 0.3), C["dim"], 1.0, dash="3 3"); cv.text((0.5, 0), "T* = 0.5 s", 12, C["muted"], dy=14)
    cv.line((T, 0), (T, 0.3), C["accent"], 1.6, dash="4 3"); cv.dot((T, 0.3), 5, C["accent"], "#FFFFFF", 1.4)
    cv.text((T, 0), f"T = {T:.3f} s", 12.5, C["accent"], dy=14)
    cv.text((T + 0.03, 0.3), f"Sa = 0.3g = {Sa:.2f} m/s²", 13, C["accent"], "start", dy=-14)
    cv.text((0.8, 0.15/0.8), "Sa = 0.15g/T", 13, C["deform"], "start", dy=-14)
    for v in (0.1, 0.2, 0.3):
        cv.line((-0.012, v), (0, v), C["muted"], 1.2); cv.text((0, v), f"{v:.1f}g", 11.5, C["muted"], "end", dx=-6)
    for t in (0.25, 0.5, 0.75, 1.0):
        cv.line((t, -0.008), (t, 0), C["muted"], 1.2)
    cv.text((1.15, 0), "T (s)", 12, C["muted"], "end", dy=28)
    cv.text_px(330, 300, f"S_{{d}} = S_{{a}}/ω_{{0}}^{{2}} = {Sd*1000:.3f} mm；S_{{v}} = ω_{{0}}S_{{d}} = {Sv:.4f} m/s；F_{{d}} = C·S_{{v}}·cosθ = {Fd:.2f} kN", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-3-spectrum.svg")

FIGURES = [(fig2, "攔：阻尼器當水平裝設（cosθ=1）或只乘一次 cosθ"),
           (fig3, "攔：T 落在下降段、套 0.15g/T；或 Sd 未除 ω₀²")]
if __name__ == "__main__":
    print(f"k={k:.1f} m={m:.4f} ω0={w0:.3f} T={T:.4f} C={C_:.3f} Sa={Sa:.3f} Sd={Sd*1000:.3f}mm Sv={Sv:.4f} Fd={Fd:.3f}")
    for fn, c in FIGURES: print(fn(), "—", c)
