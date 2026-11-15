#!/usr/bin/env python3
"""SD-2004-5 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2004-5.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2004-5"
# ── §4 解得／題給 ──
T1, T2 = 0.422, 0.162
def Cs(T): return 1 + 5*T if T <= 0.3 else (2.5 if T <= 1 else 2.5 / T)
def fig2():
    cv = Canvas(720, 400, bg="#FFFFFF")
    Ts = [i * 0.005 for i in range(0, 401)]
    X, Y = xy_plot(cv, (80, 50, 580, 270), (0, 2.0), (0, 3.0), [([(T, Cs(T)) for T in Ts], C["deform"], 3, None)],
                   xticks=(0, 0.3, 0.5, 1.0, 1.5, 2.0), yticks=(0, 1, 2, 2.5, 3), xlabel="週期 T (s)", ylabel="反應譜係數 C（Sa = C × 0.2g）")
    for T, lab in ((T1, f"T1 = {T1} s → C = {Cs(T1):.2f}"), (T2, f"T2 = {T2} s → C = {Cs(T2):.2f}")):
        cv.parts.append(f'<line x1="{X(T):.1f}" y1="{Y(0):.1f}" x2="{X(T):.1f}" y2="{Y(Cs(T)):.1f}" stroke="{C["accent"]}" stroke-dasharray="4 3"/>')
        cv.parts.append(f'<circle cx="{X(T):.1f}" cy="{Y(Cs(T)):.1f}" r="6" fill="#FFFFFF" stroke="{C["accent"]}" stroke-width="2.6"/>')
        cv.text_px(X(T) + 10, Y(Cs(T)) + (18 if T == T2 else -16), lab, 12.5, C["accent"], "start")
    cv.text_px(360, 22, "圖 2　題給反應譜係數與兩振態取值", 15, C["text"], weight="700")
    cv.text_px(360, 382, "第二振態落在 T ≤ 0.3 s 的上升段（C = 1 + 5T），不是平台值 2.5", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-spectrum.svg")
FIGURES = [(fig2, "第二振態誤取平台值 2.5（應為上升段 1.81）")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c, Cs(T1), Cs(T2))
