#!/usr/bin/env python3
"""SD-2005-1 解題圖解（struct-diagram 規範；2026-11-16，U3-2-G1 階段 E）
fig-1：BRB 彈性—完全塑性遲滯迴圈（μ = δmax/δy = 5，無因次）。每循環消能 W_D = 4F_y(δmax−δy)＝迴圈面積，
等效阻尼比用割線勁度 K_eff：ξ = W_D/(4πE_so)，E_so = ½K_eff δmax²——攔下舊版用初始勁度 K_e 的錯誤。
數值取自 scripts/fixes/2026-11-16_verify_SD-2005-1.py（μ=5：W_D=16、ξ=0.509）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import Canvas, C
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2005-1"
MU = 5.0
WD = 4 * (MU - 1)                 # ×F_y δ_y
ESO = 0.5 * MU * 1.0              # ½ K_eff δmax² = ½ F_y δmax
XI = WD / (4 * math.pi * ESO)
XI_OLD = WD / (4 * math.pi * MU**2)
def fig1():
    W, H = 720, 470
    cv = Canvas(W, H, bg="#FFFFFF")
    ox, oy, sx, sy = 330, 230, 50, 120          # 原點像素、每 δy、每 F_y
    P = lambda d, f: (ox + d * sx, oy + f * sy)
    cv.line(P(-6.2, 0), P(6.2, 0), C["member"], 1.4); cv.line(P(0, -1.5), P(0, 1.55), C["member"], 1.4)
    cv.text_px(ox + 6.2*sx + 4, H - oy, "δ/δ_{y}", 13, C["muted"], anchor="start")
    cv.text_px(ox + 8, H - (oy + 1.55*sy), "F/F_{y}", 13, C["muted"], anchor="start")
    for d in (-5, -3, -1, 1, 3, 5):
        cv.line(P(d, -0.04), P(d, 0.04), C["member"], 1.2); cv.text_px(P(d, 0)[0], H - oy + 16, f"{d:g}", 11.5, C["muted"])
    for f in (-1, 1):
        cv.text_px(ox + 6, H - P(0, f + (0.09 if f > 0 else -0.1))[1], f"{f:g}", 11.5, C["muted"], anchor="start")
    loop = [P(MU, 1), P(MU - 2, -1), P(-MU, -1), P(-MU + 2, 1), P(MU, 1)]
    cv.polygon(loop[:-1], C["fill_c"], "none")
    cv.poly(loop, C["deform"], 2.8)
    cv.polygon([P(0, 0), P(MU, 0), P(MU, 1)], C["fill_m"], C["bmd"], 1.4)
    cv.line(P(-1.3, -1.3), P(1.3, 1.3), C["accent"], 2.0, dash="6 4")
    cv.line(P(0, 0), P(MU, 1), C["bmd"], 2.2)
    cv.text_px(P(1.3, 1.3)[0] + 4, H - P(1.3, 1.3)[1] - 6, "K_{e}（初始）", 12.5, C["accent"], anchor="start")
    cv.text_px(P(5, 1.13)[0], H - P(5, 1.13)[1], "K_{eff} = F_{y}/δ_{max}", 12.5, C["bmd"], anchor="end")
    cv.text_px(P(-2.9, -0.5)[0], H - P(-2.9, -0.5)[1], f"W_{{D}} = 4F_{{y}}(δ_{{max}}−δ_{{y}}) = {WD:g} F_{{y}}δ_{{y}}", 13, C["deform"])
    cv.text_px(P(5.15, 0.45)[0], H - P(5.15, 0.45)[1], f"E_{{so}} = {ESO:g} F_{{y}}δ_{{y}}", 12.5, C["bmd"], anchor="start")
    cv.text_px(W/2, 24, f"BRB 彈性—完全塑性遲滯迴圈（μ = δ_{{max}}/δ_{{y}} = {MU:g}）", 14.5, C["text"], weight="700")
    cv.text_px(W/2, H - 46, f"ξ_{{eq}} = W_{{D}}/(4πE_{{so}}) = W_{{D}}/(2πK_{{eff}}δ_{{max}}^{{2}}) = {XI:.3f}  （= 2(μ−1)/(πμ)）", 13.5, C["text"])
    cv.text_px(W/2, H - 22, f"誤用初始勁度：W_{{D}}/(4πK_{{e}}δ_{{max}}^{{2}}) = {XI_OLD:.3f}（本庫舊版 §3.5 的式子，低估 10 倍）", 12.5, C["load"])
    return cv.save(f"{OUT}/{TAG}-fig-1-hysteresis.svg")
FIGURES = [(fig1, "等效阻尼比用割線勁度 K_eff，不是初始勁度 K_e")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
