#!/usr/bin/env python3
"""SD-2003-5 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2003-5.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2003-5"
# ── §4 Step 2–5 解得 ──
DELTA = [6, 5.6, 8, 6, 10/3]                          # 層間變位 mm（題給，δ5＝10/3）
K = [5e6, 5e6, 3e6, 3e6, 3e6]
V = [k * d / 1000 for k, d in zip(K, DELTA)]           # 層剪力 N
F = [V[i] - (V[i+1] if i < 4 else 0) for i in range(5)]
U = [sum(DELTA[:i+1]) for i in range(5)]               # 樓層位移 mm
def fig2():
    cv = Canvas(760, 420, bg="#FFFFFF")
    X, Y = xy_plot(cv, (90, 60, 270, 290), (0, 32), (0, 5), [([(0, 0)] + [(u, i+1) for i, u in enumerate(U)], C["deform"], 3, None),
             ([(0, 0)] + [(d, i+1) for i, d in enumerate(DELTA)], C["member2"], 1.8, "5 4")], xticks=(0, 10, 20, 30), yticks=(0, 1, 2, 3, 4, 5), xlabel="位移 (mm)", ylabel="樓層")
    for i, u in enumerate(U): cv.text_px(X(u) + 6, Y(i+1), f"u{i+1} = {u:.2f}", 11.5, C["deform"], "start")
    cv.text_px(X(9), Y(0.5), "虛線：層間變位 δi", 11.5, C["muted"], "start")
    X2, Y2 = xy_plot(cv, (480, 60, 230, 290), (0, 12), (0, 5), [], xticks=(0, 4, 8, 12), yticks=(), xlabel="側力 (kN)")
    for i, f in enumerate(F):
        cv.parts.append(f'<rect x="{X2(0):.1f}" y="{Y2(i+1)-9:.1f}" width="{X2(f/1000)-X2(0):.1f}" height="18" fill="{C["load"]}"/>')
        cv.text_px(X2(f/1000) + 6, Y2(i+1), f"F{i+1} = {f/1000:.1f} kN", 11.5, C["load"], "start")
    cv.text_px(380, 24, "圖 2　樓層位移（累加層間變位）與側力分布", 15, C["text"], weight="700")
    cv.text_px(380, 402, "雷利法要用樓層位移 ui（實線），不是層間變位 δi；側力呈倒三角形 2–4–6–8–10 kN", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-profile.svg")
FIGURES = [(fig2, "把層間變位直接當樓層位移代入雷利商")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c, [round(f) for f in F], [round(u, 3) for u in U])
