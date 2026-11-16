#!/usr/bin/env python3
"""SD-2004-2 解題圖解（struct-diagram 規範；2026-11-16，U3-2-G1 階段 E）
fig-2：m_b=0 時相對位移 v2 在隔震層（k_b）與上部結構（k）之間的分配——攔下「把 x2−x1 當隔震支承位移」的錯誤。
數值取自已驗證正本 §5（scripts/fixes/2026-11-16_verify_SD-2004-2.py）：x1−ug = k/(k+kb)·v2、x2−x1 = kb/(k+kb)·v2。
用法：python3 gen_SD-2004-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。
（題目附圖重繪在另一支 gen_SD-2004-2_problem.py。）"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2004-2"
K_OVER_KB = 25.0                      # 正本 §5 例：k=100、kb=4
ISO = K_OVER_KB / (1 + K_OVER_KB)     # 0.9615
SUP = 1 / (1 + K_OVER_KB)             # 0.0385

def fig2():
    W, H = 720, 600
    cv = Canvas(W, H, bg="#FFFFFF")
    # ---- 上半：位移分配示意（v2 = 500 px）----
    cv.text_px(W/2, 26, "m_{b} = 0 時相對位移 v_{2} = x_{2} − u_{g} 的分配（k/k_{b} = 25，正本 §5 例）", 14.5, C["text"], weight="700")
    x0, L, yb = 90, 520, H - 120
    xa = x0 + ISO * L; xb = x0 + L
    for x, lab in ((x0, "u_{g}"), (xa, "x_{1}"), (xb, "x_{2}")):
        cv.line((x, yb - 26), (x, yb + 26), C["member"], 2.0)
        cv.math_px(x, H - (yb + 40), lab, 15)
    cv.line((x0, yb), (xb, yb), C["ghost"], 1.4, dash="4 4")
    # 隔震層段
    cv.polygon([(x0, yb - 10), (xa, yb - 10), (xa, yb + 10), (x0, yb + 10)], C["fill_c"], C["deform"], 1.6)
    cv.text_px((x0 + xa)/2, H - (yb - 30), f"x_{{1}} − u_{{g}} = k/(k+k_{{b}})·v_{{2}} = {ISO:.4f} v_{{2}}", 13.5, C["deform"])
    cv.text_px((x0 + xa)/2, H - (yb - 50), "隔震支承變形（彈簧 k_{b} 伸長）", 13, C["deform"])
    # 上部結構段
    cv.polygon([(xa, yb - 10), (xb, yb - 10), (xb, yb + 10), (xa, yb + 10)], C["fill_t"], C["load"], 1.6)
    cv.line((xb - 2, yb - 12), (xb + 40, yb - 52), C["load"], 1.2)
    cv.text_px(xb + 44, H - (yb - 62), f"x_{{2}} − x_{{1}} = {SUP:.4f} v_{{2}}", 13.5, C["load"], anchor="end")
    cv.text_px(xb + 44, H - (yb - 82), "上部結構變形（彈簧 k）", 13, C["load"], anchor="end")
    # ---- 下半：分配比例 vs k/k_b（對數軸）----
    gx0, gx1, gy0, gy1 = 90, 660, 100, 300            # 像素（y 由下往上）
    lx0, lx1 = math.log10(0.1), math.log10(100)
    X = lambda r: gx0 + (math.log10(r) - lx0) / (lx1 - lx0) * (gx1 - gx0)
    Y = lambda f: gy0 + f * (gy1 - gy0)
    cv.line((gx0, gy0), (gx1, gy0), C["member"], 1.6); cv.line((gx0, gy0), (gx0, gy1), C["member"], 1.6)
    for r in (0.1, 1, 10, 100):
        cv.line((X(r), gy0), (X(r), gy1), C["border"], 1.0)
        cv.text_px(X(r), H - gy0 + 16, f"{r:g}", 12, C["muted"])
    for f in (0, 0.5, 1.0):
        cv.line((gx0, Y(f)), (gx1, Y(f)), C["border"], 1.0)
        cv.text_px(gx0 - 8, H - Y(f), f"{f:g}", 12, C["muted"], anchor="end")
    cv.text_px((gx0 + gx1)/2, H - gy0 + 36, "k / k_{b}（上部結構勁度 / 隔震層勁度，對數軸）", 13, C["muted"])
    cv.text_px(gx0 - 40, H - (gy1 + 30), "占 v_{2} 的比例", 12.5, C["muted"], anchor="start")
    rs = [10 ** (lx0 + i * (lx1 - lx0) / 200) for i in range(201)]
    cv.poly([(X(r), Y(r/(1+r))) for r in rs], C["deform"], 2.6)
    cv.poly([(X(r), Y(1/(1+r))) for r in rs], C["load"], 2.6)
    for f, col, lab in ((0.52, C["deform"], "隔震層 k/(k+k_{b})"), (0.38, C["load"], "上部結構 k_{b}/(k+k_{b})")):
        cv.line((X(11), Y(f)), (X(16), Y(f)), col, 2.6)
        cv.text_px(X(17), H - Y(f), lab, 12.5, col, anchor="start")
    for r in (1.0, K_OVER_KB):
        for f, col in ((r/(1+r), C["deform"]), (1/(1+r), C["load"])):
            cv.dot((X(r), Y(f)), 4.5, col)
    cv.text_px(X(K_OVER_KB) + 8, H - Y(ISO) + 16, f"{ISO:.4f}", 12, C["deform"], anchor="start")
    cv.text_px(X(K_OVER_KB) + 8, H - Y(SUP) - 12, f"{SUP:.4f}", 12, C["load"], anchor="start")
    cv.line((X(1.0), Y(0.5)), (X(1.0), Y(1.0)), C["muted"], 1.2, dash="4 3")
    cv.text_px(X(1.0), H - Y(1.0) - 12, "k = k_{b}：各 0.5", 12, C["muted"])
    cv.text_px(W/2, H - 16, "隔震（k_{b} ≪ k）時 v_{2} 幾乎全由隔震層承擔；x_{2} − x_{1} 是上部結構變形，趨近 0", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-deform-split.svg")
FIGURES = [(fig2, "x2−x1 是上部結構變形、隔震支承變形是 x1−ug")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
