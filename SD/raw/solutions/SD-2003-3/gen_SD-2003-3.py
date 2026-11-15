#!/usr/bin/env python3
"""SD-2003-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2003-3.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-3"
# ── §4 Part C 解得 ──
A0, A1 = math.pi / 15, 1 / (30 * math.pi)            # α (1/s)、β (s)
xi = lambda T: A0 * T / (4 * math.pi) + math.pi * A1 / T
def fig2():
    cv = Canvas(720, 420, bg="#FFFFFF")
    Ts = [0.4 + i * 0.01 for i in range(231)]
    X, Y = xy_plot(cv, (80, 50, 580, 290), (0.4, 2.7), (0.0, 0.10), [([(T, xi(T)) for T in Ts], C["deform"], 3, None),
              ([(T, A0 * T / (4 * math.pi)) for T in Ts], C["member2"], 1.6, "5 4"), ([(T, math.pi * A1 / T) for T in Ts], C["member2"], 1.6, "2 4")],
              xticks=(0.5, 1, 1.5, 2, 2.5), yticks=(0, 0.02, 0.04, 0.06, 0.08, 0.10), xlabel="週期 T (s)", ylabel="阻尼比 ξ")
    for T, lab, col in ((2.0, "第1振態 2 s、5%（錨定）", C["text"]), (1.0, "第3振態 1 s、5%（錨定）", C["text"]), (1.5, f"第2振態 1.5 s → {xi(1.5)*100:.2f}%", C["accent"])):
        cv.parts.append(f'<circle cx="{X(T):.1f}" cy="{Y(xi(T)):.1f}" r="6" fill="#FFFFFF" stroke="{col}" stroke-width="2.6"/>')
        cv.text_px(X(T), Y(xi(T)) + (22 if T != 1.5 else -22), lab, 12.5, col)
    cv.text_px(X(2.6), Y(0.036), "質量比例項 αT/(4π)", 11.5, C["muted"], "end"); cv.text_px(X(0.55), Y(0.072), "勁度比例項 πβ/T", 11.5, C["muted"], "start")
    cv.text_px(360, 22, "圖 2　雷利阻尼的 ξ–T 曲線（錨定第 1、第 3 振態）", 15, C["text"], weight="700")
    cv.text_px(360, 402, "兩錨定週期之間的振態阻尼比低於 5%；錨定點以外（更長或更短週期）阻尼比上升", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-xi-T.svg")
FIGURES = [(fig2, "錨定振態取錯（第 1、2 而非第 1、3）、把 ξ 寫成 T 的單調函數")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c, round(xi(1.5), 5))
