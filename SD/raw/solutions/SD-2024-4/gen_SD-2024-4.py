#!/usr/bin/env python3
"""SD-2024-4 解題圖解（struct-diagram；2026-11-16，X-G1 階段 E）
fig-3-shape：規範式用的靜變位形狀 u(x)/u(L/2) 與精確振態 sin(πx/L) 對照，以及兩者差值（放大）。
攔下的錯誤：舊解形狀比較表把 x/L=0.25 的值寫成 0.6758、最大差寫成 4.4%（實為 0.7125、0.62%）。
圖上數值全由下方函式算出。用法：python3 gen_SD-2024-4.py [輸出目錄]；再跑 struct-diagram 的 render.py 產 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2024-4"

un = lambda s: (s**4 - 2*s**3 + s)/(5/16)            # 均佈 w 下簡支梁靜變位／中點值
ph = lambda s: math.sin(math.pi*s)
N = 400; S = [i/N for i in range(N+1)]
D = [un(s) - ph(s) for s in S]
imax = max(range(N+1), key=lambda i: abs(D[i])); dmax, smax = D[imax], S[imax]

def fig3():
    W, H = 760, 520
    cv = Canvas(W, H, sx=1, bg="#FFFFFF")
    x0, x1 = 90, 690
    X = lambda s: x0 + (x1 - x0)*s
    # 上：形狀
    yb, ys = 250, 170
    Y = lambda v: yb + ys*v
    cv.text_px(W/2, H - 22, "上：形狀幾乎重合；下：差值放大 50 倍，全跨最大差 %.4f（x/L ≈ %.2f）" % (abs(dmax), smax), 13.5, C["muted"])
    cv.line((x0, yb), (x1, yb), C["muted"], 1.4)
    cv.poly([(X(s), Y(ph(s))) for s in S], C["deform"], 3.2)
    cv.poly([(X(s), Y(un(s))) for s in S], C["accent"], 2.2, dash="7 5")
    for s in (0.25, 0.5):
        cv.line((X(s), yb), (X(s), Y(un(s))), C["border"], 1.0, dash="3 3")
        if s == 0.5: cv.text_px(X(s), H - Y(un(s)) - 14, f"x/L={s:g}：u={un(s):.4f}，sin={ph(s):.4f}", 12, C["text"])
        else: cv.text_px(X(s) + 12, H - Y(un(s)) + 22, f"x/L={s:g}：u={un(s):.4f}，sin={ph(s):.4f}", 12, C["text"], "start")
    cv.legend(120, 40, [(C["deform"], "sin(πx/L)（考卷給的精確振態）"), (C["accent"], "u(x)/u(L/2)（規範式用的靜變位）")])
    # 下：差值×50
    yb2, ys2 = 95, 50*50
    Y2 = lambda v: yb2 + ys2*v
    cv.line((x0, yb2), (x1, yb2), C["muted"], 1.4)
    cv.poly([(X(s), Y2(d)) for s, d in zip(S, D)], C["load"], 2.2)
    cv.dot((X(smax), Y2(dmax)), 4.5, C["load"])
    cv.text_px(X(smax) + 8, H - Y2(dmax) - 12, f"最大差 {dmax:.4f}", 12.5, C["load"], "start")
    cv.text_px(x0 - 10, H - yb2, "差值", 12.5, C["muted"], "end")
    for s in (0, 0.5, 1):
        cv.text_px(X(s), H - yb2 + 18, f"x/L={s:g}", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-3-shape.svg")

FIGURES = [(fig3, "形狀比較表的數值（0.7125、最大差 0.62%）")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
