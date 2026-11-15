#!/usr/bin/env python3
"""SD-2005-4 解題圖解（struct-diagram；2026-11-15，SD-U1-3 批 1 階段 E）。數值取自 SD-2005-4.md §4（勿手改）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C, compose
from sdprob import xy_plot
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")

TAG = "SD-2005-4"
# ── §4 (二)(三) 的無因次式（黏滯阻尼主解）──
# 穩態振幅 U = (me/M)·r²/√[(1−r²)² + (2ξr)²]；傳到基礎的動力 F_T = me Ω²·√[1+(2ξr)²]/√[(1−r²)²+(2ξr)²]
amp = lambda r, x: r*r / math.sqrt((1 - r*r)**2 + (2*x*r)**2)
TR = lambda r, x: math.sqrt(1 + (2*x*r)**2) / math.sqrt((1 - r*r)**2 + (2*x*r)**2)
XIS = ((0.05, C["load"]), (0.20, C["deform"]), (0.50, C["bmd"]))      # 示意阻尼比（題目全為符號）
def fig2():
    a = Canvas(460, 420, bg="#FFFFFF"); a.panel("穩態位移 U ÷ (me/M)", None)
    rs = [i * 0.005 for i in range(1, 601)]
    X, Y = xy_plot(a, (60, 60, 370, 280), (0, 3), (0, 5), [([(r, min(amp(r, x), 5)) for r in rs], col, 2.6, None) for x, col in XIS],
                   xticks=(0, 1, 2, 3), yticks=(0, 1, 2, 3, 4, 5), xlabel="r = Ω/ωn", ylabel="")
    a.parts.append(f'<line x1="{X(0):.1f}" y1="{Y(1):.1f}" x2="{X(3):.1f}" y2="{Y(1):.1f}" stroke="{C["muted"]}" stroke-dasharray="3 3"/>'); a.text_px(X(2.95), Y(1) + 14, "r 大時 → me/M", 11.5, C["muted"], "end")
    b = Canvas(460, 420, bg="#FFFFFF"); b.panel("傳到基礎的動力 ÷ (meΩ²)", None)
    X2, Y2 = xy_plot(b, (60, 60, 370, 280), (0, 3), (0, 5), [([(r, min(TR(r, x), 5)) for r in rs], col, 2.6, None) for x, col in XIS],
                     xticks=(0, 1, 2, 3), yticks=(0, 1, 2, 3, 4, 5), xlabel="r = Ω/ωn", ylabel="")
    b.parts.append(f'<line x1="{X2(math.sqrt(2)):.1f}" y1="{Y2(0):.1f}" x2="{X2(math.sqrt(2)):.1f}" y2="{Y2(5):.1f}" stroke="{C["accent"]}" stroke-dasharray="4 3"/>'); b.text_px(X2(math.sqrt(2)) + 6, Y2(4.6), "r = √2", 12, C["accent"], "start")
    for i, (x, col) in enumerate(XIS): b.text_px(X2(2.2), Y2(3.8 - 0.4*i), f"ξ = {x:.2f}", 12, col, "start")
    return compose([a, b], title="圖 2　旋轉不平衡的穩態反應與傳力（黏滯阻尼，ξ 為示意）", note="r < √2 時阻尼越大傳力越小；r > √2 時阻尼反而增加傳力。圖上 ξ 為示意值，題目全為符號", path=f"{OUT}/{TAG}-fig-2-response.svg")
FIGURES = [(fig2, "把激振力寫成定值 me（漏 Ω²）、把傳力只算彈簧力 ku")]
if __name__ == "__main__":
    for fn, c in FIGURES: fn(); print(fn.__name__, "—", c)
