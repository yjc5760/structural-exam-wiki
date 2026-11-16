#!/usr/bin/env python3
"""SD-2017-3 解題圖解（struct-diagram；2026-11-16，SD-U3-1 組 U3-1-G1 階段 E）
fig-3：各柱可變形段（牆頂至梁底）的變形形狀＋剪力分配長條圖（虛框為舊讀法 h3=ℓ/4 的錯誤分配）。
數值取自勘誤後 §4（h = ℓ/2、ℓ/2、3ℓ/4、ℓ；V_i ∝ 1/h³）。用法：python3 gen_SD-2017-3.py [輸出目錄]。"""
import sys, os
from fractions import Fraction as F
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2017-3"
L, S = F(1), 1.0
WALL = (F(1, 2), F(1, 4))                                  # 1–2、2–3 牆高（ℓ）
H = [L - WALL[0], L - max(WALL), L - WALL[1], L]           # 可變形段：ℓ/2、ℓ/2、3ℓ/4、ℓ（柱 2 取較高的牆）
H_OLD = [F(1, 2), F(1, 2), F(1, 4), F(1)]                  # 舊讀法（柱 3 誤為 ℓ/4）
def share(hs):
    k = [1/h**3 for h in hs]; return [x/sum(k) for x in k]
V, V_OLD = share(H), share(H_OLD)
D = 0.16                                                   # 示意側移
def fig3():
    cv = fit(980, 340, (-0.5, 7.6), (-0.5, 1.2), L=14, R=14, T=14, B=14)
    for i, (a, h) in enumerate(((0, WALL[0]), (1, WALL[1]))):
        cv.polygon([(a*S, 0), ((a+1)*S, 0), ((a+1)*S, float(h)), (a*S, float(h))], "#E9E3D3", C["member2"], 1.2)
    Lf = float(L)
    cv.polygon([(D, Lf), (3*S + D, Lf), (3*S + D, Lf + 0.07), (D, Lf + 0.07)], "#E4E7EC", C["member"], 1.6)
    for i, h in enumerate(H):
        x = i*S; y0 = float(L - h)
        cv.line((x, 0), (x, y0), C["member"], 2.6)                                     # 牆內／不變形段
        cv.poly([(x + D*(3*t*t - 2*t**3), y0 + t*float(h)) for t in [j/40 for j in range(41)]], C["deform"], 2.6)
        cv.line((x, y0), (x, Lf), C["ghost"], 1.2, dash="4 3")
        cv.dot((x, y0), r=4, fill=C["accent"])
        cv.text((x, y0 + float(h)/2), f"h{i+1} = {['ℓ/2','ℓ/2','3ℓ/4','ℓ'][i]}", 12.5, C["accent"], "start", dx=10 + D*cv.sx*0.5)
        cv.text((x, 0), str(i + 1), 15, C["text"], dy=30)
    ground(cv, (-0.25, 0), (3*S + 0.25, 0))
    cv.arrow((-0.45, Lf + 0.035), (D - 0.03, Lf + 0.035), C["load"], 3, 10); cv.math((-0.3, Lf + 0.035), "V", 15, C["load"], dy=-14)
    # 長條圖
    bx, bw, sc = 4.4, 0.55, 1.15
    cv.line((bx - 0.15, 0), (bx + 4*0.75, 0), C["muted"], 1.4)
    for i in range(4):
        x = bx + i*0.75
        cv.polygon([(x, 0), (x + bw, 0), (x + bw, float(V[i])*sc), (x, float(V[i])*sc)], C["fill_s"], C["sfd"], 1.6)
        cv.poly([(x, 0), (x, float(V_OLD[i])*sc), (x + bw, float(V_OLD[i])*sc), (x + bw, 0)], C["muted"], 1.2, dash="4 3")
        cv.text((x + bw/2, float(V[i])*sc), f"{float(V[i]):.3f}V", 12, C["sfd"], dy=-12)
        cv.text((x + bw/2, 0), f"柱 {i+1}", 13, C["text"], dy=16)
    cv.text((bx + 1.5, -0.42), "實框：正確（h3 = 3ℓ/4）　虛框：舊讀法 h3 = ℓ/4（柱 3 得 0.790V）", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-3-shear.svg")
FIGURES = [(fig3, "柱 3 可變形段是 3ℓ/4 而非 ℓ/4；短柱是柱 1、2（合計 83%），不是柱 3")]
if __name__ == "__main__":
    assert V == [F(216, 523), F(216, 523), F(64, 523), F(27, 523)] and V_OLD[2] == F(64, 81)
    for fn, c in FIGURES: print(fn(), "—", c)
