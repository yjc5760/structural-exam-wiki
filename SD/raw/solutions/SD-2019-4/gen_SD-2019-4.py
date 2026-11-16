#!/usr/bin/env python3
"""SD-2019-4 解題圖解（struct-diagram；2026-11-16，組 U3-1-G2 階段 E）
fig-1 短柱效應：同一層間位移 Δ 下，窗台牆把柱的可變形長度由 H 縮成 h_e，
側向勁度 ∝ 1/L^3、撓曲降伏時的剪力 ∝ 1/L，兩者都放大（§4 ㈠ 的機制；窗台牆高約 1 m 取自 §4 ㈡）。
柱淨高 H＝3.0 m 為示意假設（考卷未給）；比值由程式計算。
用法：python3 gen_SD-2019-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C, compose, column_shape
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2019-4"
H = 3.0          # 柱淨高（m，示意假設）
HW = 1.0         # 窗台牆高（m，§4 ㈡「約 1 公尺高」）
HE = H - HW      # 可變形長度
DELTA = 0.22     # 層間位移（繪圖放大值，兩格相同）
K_RATIO = (H/HE)**3      # 側向勁度比 12EI/he^3 ÷ 12EI/H^3
V_RATIO = H/HE           # 撓曲降伏剪力比 2Mp/he ÷ 2Mp/H

def panel(short):
    cv = fit(460, 470, (-1.3, 1.6), (-0.4, 3.6), L=20, R=20, T=70, B=24)
    cv.panel("(b) 有窗台牆：短柱" if short else "(a) 無窗台牆：一般柱")
    ground(cv, (-1.1, 0), (1.4, 0))
    cv.line((-1.1, H), (1.4, H), C["ghost"], 6)                         # 原位置樓版
    cv.line((0, 0), (0, H), C["ghost"], 3, dash="5 4")                  # 原位置柱
    if short:
        cv.polygon([(-0.95, 0), (-0.12, 0), (-0.12, HW), (-0.95, HW)], "#E7D9C7", C["accent"], 1.6)
        cv.polygon([(0.12, 0), (1.4, 0), (1.4, HW), (0.12, HW)], "#E7D9C7", C["accent"], 1.6)
        cv.text((-0.53, HW/2), "窗台牆", 13, C["accent"]); cv.text((0.76, HW/2), "窗台牆", 13, C["accent"])
        pts = [(0, y) for y in (0, HW)] + column_shape((0, HW), HE, DELTA, 0.0)[1:]
        cv.dim((1.4, HW), (1.4, H), f"h_{{e}} = {HE:g} m", off=-18, label_off=-34, color=C["accent"])
    else:
        pts = column_shape((0, 0), H, DELTA, 0.0)
    cv.poly(pts, C["deform"], 4)
    cv.line((DELTA - 1.1, H), (DELTA + 1.4, H), C["member"], 6)        # 變位後樓版
    cv.arrow((0, H + 0.28), (DELTA, H + 0.28), C["deform"], 2.4, 8); cv.math((DELTA/2, H + 0.28), "Δ", 15, C["deform"], dy=-14)
    cv.dim((-1.1, 0), (-1.1, H), f"H = {H:g} m", off=18, label_off=34)
    if short:
        cv.text_px(230, 440, f"勁度 ×{K_RATIO:.2f}；撓曲降伏時剪力 ×{V_RATIO:.2f}", 13.5, C["load"], weight="700")
    else:
        cv.text_px(230, 440, "勁度 12EI/H^{3}；降伏剪力 2M_{p}/H", 13.5, C["text"])
    return cv

def fig1():
    return compose([panel(False), panel(True)],
                   title=f"{TAG}　短柱效應：同一層間位移 Δ，可變形長度由 H 縮為 he",
                   note="柱淨高 3.0 m 為示意；剪力需求放大而剪力強度不變 → 剪力破壞先於撓曲降伏",
                   path=f"{OUT}/{TAG}-fig-1-short-column.svg")
FIGURES = [(fig1, "攔下「短柱＝柱真的很短」與只談強度不談勁度的誤解；剪力需求放大的兩個來源")]
if __name__ == "__main__":
    for fn, catches in FIGURES: fn(); print(fn.__name__, "—", catches, f"K×{K_RATIO:.3f} V×{V_RATIO:.3f}")
