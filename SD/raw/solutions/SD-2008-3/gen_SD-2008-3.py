#!/usr/bin/env python3
"""SD-2008-3 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2008-3.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2008-3"
# ── 題給 MF 公式；§4 解得 ──
MF = lambda r, x: 1 / math.sqrt((1 - r*r)**2 + (2*x*r)**2)
BS = {2: 0.80, 5: 1.00, 10: 1.33, 20: 1.60}; B1 = {2: 0.80, 5: 1.00, 10: 1.25, 20: 1.50}   # 現行規範表 3-1
def fig2():
    a = Canvas(460, 420, bg="#FFFFFF"); a.panel("簡諧 MF：ξ 由 2% 增為 20% 的位移比", None)
    rs = [i * 0.004 for i in range(0, 451)]
    X, Y = xy_plot(a, (60, 60, 370, 280), (0.6, 1.8), (0.0, 1.2), [([(r, MF(r, 0.20) / MF(r, 0.02)) for r in rs if r >= 0.6], C["deform"], 3, None)],
                   xticks=(0.6, 1.0, 1.5, 1.8), yticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2), xlabel="Tn/Tf", ylabel="位移比 MF(20%)/MF(2%)")
    for r in (1.0, 1.5):
        v = MF(r, 0.20) / MF(r, 0.02)
        a.parts.append(f'<circle cx="{X(r):.1f}" cy="{Y(v):.1f}" r="6" fill="#FFFFFF" stroke="{C["accent"]}" stroke-width="2.6"/>'); a.text_px(X(r) + 8, Y(v) + (-14 if r == 1.5 else 14), f"{v:.3f}", 12.5, C["accent"], "start")
    b = Canvas(460, 420, bg="#FFFFFF"); b.panel("規範表 3-1：BS 與 B1", None)
    xs = [2, 5, 10, 20]
    X2, Y2 = xy_plot(b, (60, 60, 370, 280), (0, 22), (0.6, 1.8), [([(x, BS[x]) for x in xs], C["load"], 3, None), ([(x, B1[x]) for x in xs], C["deform"], 3, "6 4")],
                     xticks=(2, 5, 10, 20), yticks=(0.8, 1.0, 1.2, 1.4, 1.6), xlabel="有效阻尼比 (%)", ylabel="阻尼修正係數")
    b.text_px(X2(20) - 4, Y2(1.60) - 14, "BS 1.60", 12.5, C["load"], "end"); b.text_px(X2(20) - 4, Y2(1.50) + 16, "B1 1.50", 12.5, C["deform"], "end")
    return compose([a, b], title="圖 2　阻尼的減振效益與規範阻尼修正係數", note="共振區比值 0.100、Tn/Tf = 1.5 為 0.903；規範 ξ = 20% 時 BS = 1.60 > B1 = 1.50（不是簡諧比值 4.0 與 1.1）", path=f"{OUT}/{TAG}-fig-2-damping.svg")
FIGURES = [(fig2, "把簡諧 MF 比值當成規範 BS、B1 數值")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
