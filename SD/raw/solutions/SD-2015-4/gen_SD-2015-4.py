#!/usr/bin/env python3
"""SD-2015-4 解題圖解（struct-diagram；2026-11-16，SD-U3-1 組 U3-1-G1 階段 E）
fig-2：懸臂梁法——反曲點、柱軸力拉／壓方向、梁柱彎矩圖。數值由腳本依 §4 公式重算（x̄、N_i、梁剪力、端彎矩）。
用法：python3 gen_SD-2015-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
from fractions import Fraction as F
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2015-4"
X = [F(0), F(7), F(17)]; Hc = F(4); P = F(20)
XB = sum(X)/3; Dd = [x - XB for x in X]
N = [P*Hc/2/sum(d*d for d in Dd)*d for d in Dd]           # 壓為正：−160/73、−20/73、+180/73
VB12 = -N[0]; VB23 = VB12 - N[1]
MB = [VB12*F(7, 2), VB23*5]                                 # 梁端彎矩 560/73、900/73
MC = [MB[0], MB[0] + MB[1], MB[1]]                          # 柱端彎矩（頂＝底）
SC = 0.045                                                  # 彎矩圖比例（m／tf·m），畫在受拉側
def fig2():
    xs = [float(x) for x in X]; h = float(Hc)
    cv = fit(900, 470, (-3.0, 20.6), (-2.6, 6.3), L=14, R=14, T=14, B=14)
    cv.line((xs[0], h), (xs[2], h), C["member"], 2.4)
    for x in xs: cv.line((x, 0), (x, h), C["member"], 2.4); cv.support((x, 0), "fixed")
    cv.arrow((-2.6, h), (-0.1, h), C["load"], 3, 10); cv.text((-1.4, h), "20 tf", 13, C["load"], dy=-14)
    # 梁彎矩圖（反對稱，中點為 0）
    for (xa, xb), m in zip(((xs[0], xs[1]), (xs[1], xs[2])), MB):
        mm = float(m)*SC; xm = (xa + xb)/2
        cv.polygon([(xa, h), (xa, h - mm), (xm, h)], C["fill_m"], C["bmd"], 1.4)      # 左端下緣受拉
        cv.polygon([(xm, h), (xb, h + mm), (xb, h)], C["fill_m"], C["bmd"], 1.4)      # 右端上緣受拉
        cv.dot((xm, h), r=4, fill=C["accent"])
        cv.text((xa + 1.8, h - mm*0.6), f"{float(m):.2f}", 12, C["bmd"], "start", dy=12)
        cv.text((xb - 0.9, h + mm*0.75), f"{float(m):.2f}", 12, C["bmd"], "end", dy=-10)
    # 柱彎矩圖（反曲點在柱中高）
    for x, m in zip(xs, MC):
        mm = float(m)*SC
        cv.polygon([(x, h), (x + mm, h), (x, h/2)], C["fill_m"], C["bmd"], 1.4)      # 柱頂右側受拉
        cv.polygon([(x, h/2), (x - mm, 0), (x, 0)], C["fill_m"], C["bmd"], 1.4)      # 柱底左側受拉
        cv.dot((x, h/2), r=4, fill=C["accent"])
        cv.text((x - mm, 0), f"{float(m):.2f}", 12, C["bmd"], "end", dx=-5, dy=-10)
        cv.text((x + mm*0.5, h*0.75), f"{float(m):.2f}", 12, C["bmd"], "start", dx=8)
    # 柱軸力（拉／壓）
    for x, n in zip(xs, N):
        col = C["tension"] if n < 0 else C["compr"]; kind = "拉" if n < 0 else "壓"
        if n < 0: cv.arrow((x, -0.5), (x, -1.4), col, 2.6, 9)
        else: cv.arrow((x, -1.4), (x, -0.5), col, 2.6, 9)
        cv.text((x, -1.75), f"{kind} {abs(float(n)):.2f} tf", 12.5, col)
    cv.text((float(XB), -2.3), f"形心 x̄ = {float(XB):g} m（自柱 1 起算）；側力向右 → 左、中柱受拉，右柱受壓；彎矩單位 tf·m，畫在受拉側", 12, C["muted"])
    cv.line((float(XB), h + 1.0), (float(XB), h + 1.6), C["dim"], 1.4); cv.text((float(XB), h + 1.6), "x̄", 13, C["dim"], dy=-10)
    return cv.save(f"{OUT}/{TAG}-fig-2-cantilever.svg")
FIGURES = [(fig2, "柱軸力方向：側力向右時左柱受拉、右柱受壓（舊解寫反）；反曲點在梁、柱中點")]
if __name__ == "__main__":
    assert N == [F(-160, 73), F(-20, 73), F(180, 73)] and MC[1] == 20 and MB == [F(560, 73), F(900, 73)]
    for fn, c in FIGURES: print(fn(), "—", c)
