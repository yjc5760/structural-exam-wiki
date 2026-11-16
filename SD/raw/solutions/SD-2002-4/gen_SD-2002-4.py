#!/usr/bin/env python3
"""SD-2002-4：解題圖解（struct-diagram；2026-11-16，組 U2-2-G1 階段 E）
所有數值由題目給定量重算（與 §4 及 scripts/fixes/2026-11-16_verify_SD-2002-4.py 相同公式）。
用法：python3 gen_SD-2002-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
import numpy as np
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2002-4"
# ── 題目給定（題目正本 §2）與 §4 解得 ──
g, m, L, EI = 9.81, 800.0, 3.0, 4.5e4
def Cs(T):
    return 1.0 if T <= 0.03 else 8.824*T + 0.7352 if T <= 0.2 else 2.5 if T <= 1.32 else 3.3/T if T <= 3.3 else 1.0
ks = 2*12*EI/L**3
wA2 = ks/m; dA = Cs(2*math.pi/math.sqrt(wA2))*0.2*g/wA2                    # §4 Step 2
lam = np.array([(3 - 5**0.5)/2, (3 + 5**0.5)/2]); w2 = lam*ks/m          # §4 Step 4
r = 2 - lam                                                               # φ2/φ1
G = (1 + r)/(1 + r**2); Sd = np.array([Cs(2*math.pi/math.sqrt(x))*0.2*g/x for x in w2])
dB2F = math.sqrt(((G*Sd)**2).sum()); dBR = math.sqrt(((G*r*Sd)**2).sum())  # §4 Step 8
D_ABS = dA + dB2F; D_SRSS = math.hypot(dA, dB2F); D_06 = 0.6*D_ABS

def fig3():
    W, H = 900, 470
    cv = fit(W, H, (-0.8, 19.0), (-1.2, 7.2), L=16, R=16, T=16, B=16)
    BW, AMP = 4.0, 6.0                       # 跨度示意；位移放大 6 倍
    gap = D_ABS*AMP                          # 繪圖間距 = 主答 Δ（放大後），恰好接觸
    xA, xB = 0.0, BW + gap
    ground(cv, (-0.6, 0), (xB + BW + 0.8, 0))
    # 未變形（淡）
    for x0, n in ((xA, 1), (xB, 2)):
        for x in (x0, x0 + BW): cv.line((x, 0), (x, n*L), C["ghost"], 1.6, dash="5,4")
        for k in range(1, n + 1): cv.line((x0, k*L), (x0 + BW, k*L), C["ghost"], 1.6, dash="5,4")
    # A 屋往右 dA；B 屋往左（二樓 dB2F、屋頂 dBR）——最不利的反向同時
    uA = dA*AMP; uB1 = -dB2F*AMP; uB2 = -dBR*AMP
    for x in (xA, xA + BW): cv.line((x, 0), (x + uA, L), C["deform"], 2.6)
    cv.line((xA + uA, L), (xA + BW + uA, L), C["deform"], 5.0)
    for x in (xB, xB + BW):
        cv.line((x, 0), (x + uB1, L), C["deform"], 2.6); cv.line((x + uB1, L), (x + uB2, 2*L), C["deform"], 2.6)
    cv.line((xB + uB1, L), (xB + BW + uB1, L), C["deform"], 5.0); cv.line((xB + uB2, 2*L), (xB + BW + uB2, 2*L), C["deform"], 5.0)
    cv.dot((xA + BW + uA, L), 6, C["load"], "#FFFFFF")
    cv.text((xA + BW + uA, L), "接觸點（高度 L）", 12.5, C["load"], "end", dx=-12, dy=22)
    cv.text((xA + BW/2 - 0.6, L), f"d_A = {dA*1000:.1f} mm →", 13, C["deform"], dy=-22)
    cv.text((xB + BW/2 - 0.7, L), f"← d_{{B,2F}} = {dB2F*1000:.1f} mm", 13, C["deform"], dy=44)
    cv.text((xB + BW/2, 2*L), f"屋頂 {dBR*1000:.0f} mm（高於 A 屋，不會相撞）", 12, C["muted"], dy=-22)
    cv.text((xA + BW/2, -0.75), "A 屋（單層）", 13.5, C["text"]); cv.text((xB + BW/2, -0.75), "B 屋（雙層）", 13.5, C["text"])
    cv.line((xA + BW, 0), (xA + BW, -0.45), C["dim"], 1.0); cv.line((xB, 0), (xB, -0.45), C["dim"], 1.0)
    cv.double_arrow((xA + BW, -0.3), (xB, -0.3), C["dim"], 1.4, 7)
    cv.text(((xA + BW + xB)/2, -0.3), f"Δ = {D_ABS*1000:.0f} mm", 13, C["text"], dy=16)
    # 右側：三種組合比較
    x0, y0, sc = 13.4, 1.0, 0.016             # 1 mm → 0.016 繪圖單位
    cv.text((x0 + 2.2, 6.6), "兩棟位移組合方式", 14.5, C["text"], weight="700")
    items = [(D_ABS, "絕對值和 d_A + d_B（主答）", C["load"]), (D_SRSS, "SRSS（機率性替代）", C["deform"]),
             (D_06, "0.6 × 和（規範 2.16.2 觀念對照，非規範值）", C["member2"])]
    for i, (v, lab, col) in enumerate(items):
        y = 5.2 - i*1.7
        cv.polygon([(x0, y - 0.28), (x0 + v*1000*sc, y - 0.28), (x0 + v*1000*sc, y + 0.28), (x0, y + 0.28)], col)
        cv.text((x0 + v*1000*sc, y), f"{v*1000:.0f} mm", 13, C["text"], "start", dx=6)
        cv.text((x0, y + 0.28), lab, 12.5, C["muted"], "start", dx=8, dy=-11)
    cv.line((x0, 0.6), (x0, 6.0), C["member"], 1.4)
    cv.text_px(W/2, H - 14, f"變形放大 {AMP:.0f} 倍；繪圖間距取主答 Δ，兩屋在高度 L 恰好接觸。Sa = 0.2·C(T)·g", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-3-pounding.svg")

FIGURES = [(fig3, "碰撞高度在 L（不是 B 屋屋頂）；兩棟反向同時最大時的間距＝絕對值和，SRSS 與 0.6×和為較小的估計")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
