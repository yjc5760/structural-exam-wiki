#!/usr/bin/env python3
"""SD-2007-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2007-3.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2007-3"
# ── §4 子題(三)(四) 解得 ──
P0, M, OM, UMAX = 10e3, 1000.0, 2 * math.pi, 0.10
K4 = P0 / UMAX + M * OM**2                              # 139.5 kN/m
R3 = 1 / math.sqrt(3); R4 = math.sqrt(M * OM**2 / K4)  # (三) 界限 r、(四) 設計 r
acc = lambda r: r*r / abs(1 - r*r)                      # (三) |ü|/(p0/m)，無阻尼
dis = lambda r: 1 / abs(1 - r*r)                        # 位移放大 |u|/(p0/k)
def fig2():
    cv = Canvas(760, 420, bg="#FFFFFF")
    rs = [i * 0.005 for i in range(0, 401) if abs(i*0.005 - 1) > 0.02]
    seg = lambda f: [[(r, min(f(r), 4)) for r in rs if r < 1], [(r, min(f(r), 4)) for r in rs if r > 1]]
    a1, a2 = seg(acc); d1, d2 = seg(dis)
    X, Y = xy_plot(cv, (80, 50, 600, 290), (0, 2.0), (0, 4.0), [(a1, C["load"], 3, None), (a2, C["load"], 3, None), (d1, C["deform"], 2.4, "6 4"), (d2, C["deform"], 2.4, "6 4")],
                   xticks=(0, 0.5, 1.0, 1.5, 2.0), yticks=(0, 0.5, 1, 2, 3, 4), xlabel="頻率比 r = Ω/ωn", ylabel="放大倍率")
    cv.parts.append(f'<line x1="{X(0):.1f}" y1="{Y(0.5):.1f}" x2="{X(2):.1f}" y2="{Y(0.5):.1f}" stroke="{C["accent"]}" stroke-dasharray="3 3"/>')
    cv.text_px(X(1.2), Y(0.5) - 10, "(三) 上限 0.05g/0.1g = 0.5", 11.5, C["accent"], "start")
    cv.parts.append(f'<circle cx="{X(R3):.1f}" cy="{Y(0.5):.1f}" r="6" fill="#FFFFFF" stroke="{C["accent"]}" stroke-width="2.6"/>')
    cv.text_px(X(0.03), Y(0.78), f"(三) r ≤ 1/√3 = {R3:.3f} → k ≥ 3mΩ²", 12, C["accent"], "start")
    cv.parts.append(f'<circle cx="{X(R4):.1f}" cy="{Y(dis(R4)):.1f}" r="6" fill="#FFFFFF" stroke="{C["deform"]}" stroke-width="2.6"/>')
    cv.text_px(X(R4) + 8, Y(dis(R4)) - 14, f"(四) r = {R4:.3f}，k = {K4/1000:.1f} kN/m", 12, C["deform"], "start")
    cv.text_px(X(1.35), Y(3.4), "紅：加速度 r²/|1−r²|", 12, C["load"], "start"); cv.text_px(X(1.35), Y(3.0), "藍虛：位移 1/|1−r²|", 12, C["deform"], "start")
    cv.text_px(380, 22, "圖 2　無阻尼穩態放大倍率與兩個設計點", 15, C["text"], weight="700")
    cv.text_px(380, 402, "r > 1 一側加速度放大恆大於 1，(三) 只能取 r 小於 1 的勁性解", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-design.svg")
FIGURES = [(fig2, "忽略 r > 1 分支是否可行、(三) 的界限誤取 r = 1/√2")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c, K4, R3, R4)
