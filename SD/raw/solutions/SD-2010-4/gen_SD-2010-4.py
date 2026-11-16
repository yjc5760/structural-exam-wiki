#!/usr/bin/env python3
"""SD-2010-4 解題圖解（struct-diagram；2026-11-16，SD-U3-1 組 U3-1-G1 階段 E）
fig-3：崩塌機構（塑鉸位置與柱剪力）＋推覆曲線 V–Δ。數值取自勘誤後 §4（K_a=15、K_b=24 EI/L³；V_a=3、V_b=4 M_p/L）。
用法：python3 gen_SD-2010-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2010-4"
# ── 由 §4 解得（EI=L=M_p=1 無因次）──
K_PIN, K_FIX = 3.0, 12.0                      # 頂固底鉸、兩端固定柱勁度
KA, KB = K_PIN + K_FIX, 2*K_FIX               # 15、24
Q_FIX, Q_PIN = 2.0, 1.0                       # 崩塌時柱剪力（M_p/L）
VA, VB = Q_FIX + Q_PIN, 2*Q_FIX               # 3、4
V1 = Q_FIX / (K_FIX/KA)                       # 2.5
DU_A = 1.0 / K_PIN                            # 左柱頂達 M_p：3Δ = 1 → Δ = 1/3
DU_B = VB / KB                                # 1/6
H, B, T, S = 1.0, 1.0, 0.09, 0.22             # 柱高、跨度、樓版厚、示意側移
def fixed_fixed(x0, s):                       # 兩端固定只平移：w = s(3ξ²−2ξ³)
    return [(x0 + s*(3*t*t - 2*t**3), t*H) for t in [i/40 for i in range(41)]]
def pin_fixed(x0, s):                         # 底鉸頂固：w = s(3ξ−ξ³)/2
    return [(x0 + s*(3*t - t**3)/2, t*H) for t in [i/40 for i in range(41)]]
def hinge(cv, p): cv.circle(p, 0.035, "#FFFFFF", C["accent"], 2.4)
def panel(cv, x0, bases, shears, V, title):
    cv.line((x0, H), (x0 + B, H), C["ghost"], 1.4, dash="5 4")
    for x in (x0, x0 + B): cv.line((x, 0), (x, H), C["ghost"], 1.4, dash="5 4")
    cv.polygon([(x0 + S, H), (x0 + B + S, H), (x0 + B + S, H + T), (x0 + S, H + T)], "#3F4A5A", C["member"], 1)
    for x, kind, q in zip((x0, x0 + B), bases, shears):
        pts = pin_fixed(x, S) if kind == "pin" else fixed_fixed(x, S)
        cv.poly(pts, C["deform"], 2.6); cv.support((x, 0), kind)
        hinge(cv, (x + S, H))
        if kind == "fixed": hinge(cv, (x, 0))
        cv.arrow((x + S*0.6 + 0.30, H*0.5), (x + S*0.6 + 0.06, H*0.5), C["sfd"], 2.2, 8)   # 柱剪力（柱作用於樓版之反力方向）
        cv.text((x + S*0.6 + 0.32, H*0.5), q, 12.5, C["sfd"], "start", dx=2)
    cv.arrow((x0 - 0.35 + S, H + T/2), (x0 + S - 0.02, H + T/2), C["load"], 3, 10)
    cv.text((x0 - 0.2 + S, H + T/2), V, 13.5, C["load"], dy=-15)
    cv.text((x0 + B/2 + S/2, -0.3), title, 13.5, C["text"])
def fig3():
    cv = fit(1000, 380, (-0.5, 6.0), (-0.75, 1.55), L=14, R=14, T=14, B=14)
    panel(cv, 0.0, ("pin", "fixed"), ("M_{p}/L", "2M_{p}/L"), "V_{a} = 3M_{p}/L", "(a) 3 個塑鉸：右柱頂底＋左柱頂")
    panel(cv, 1.9, ("fixed", "fixed"), ("2M_{p}/L", "2M_{p}/L"), "V_{b} = 4M_{p}/L", "(b) 4 個塑鉸同時形成")
    # 推覆曲線（右側）：橫軸 Δ/(M_pL²/EI) 0–0.5，縱軸 V/(M_p/L) 0–4.5
    ox, oy, wx, wy = 4.1, 0.0, 1.7, 1.35
    P = lambda d, v: (ox + d/0.5*wx, oy + v/4.5*wy)
    for v in (1, 2, 3, 4):
        cv.line(P(0, v), P(0.5, v), C["border"], 1); cv.text(P(0, v), str(v), 11.5, C["muted"], "end", dx=-5)
    for d, lab in ((1/6, "1/6"), (1/3, "1/3")):
        cv.line(P(d, 0), P(d, 4.5), C["border"], 1); cv.text(P(d, 0), lab, 11.5, C["muted"], dy=13)
    cv.line(P(0, 0), P(0.5, 0), C["muted"], 1.6); cv.line(P(0, 0), P(0, 4.5), C["muted"], 1.6)
    cv.poly([P(0, 0), P(DU_B, VB), P(0.5, VB)], C["load"], 2.6)
    cv.poly([P(0, 0), P(V1/KA, V1), P(DU_A, VA), P(0.5, VA)], C["deform"], 2.6)
    cv.dot(P(V1/KA, V1), r=4, fill=C["accent"]); cv.text(P(V1/KA, V1), "右柱成鉸 2.5", 11.5, C["accent"], "start", dx=6, dy=10)
    cv.text(P(0.5, VB), "(b)", 13, C["load"], "end", dy=-11); cv.text(P(0.5, VA), "(a)", 13, C["deform"], "end", dy=-11)
    cv.text(P(0.25, 0), "Δ／(M_{p}L²/EI)", 12.5, C["text"], dy=30)
    cv.text(P(0, 4.5), "V／(M_{p}/L)", 12.5, C["text"], "start", dx=4, dy=-10)
    return cv.save(f"{OUT}/{TAG}-fig-3-mechanism.svg")
FIGURES = [(fig3, "(a) 只有 3 個塑鉸、崩塌側力 3M_p/L 小於 (b) 的 4M_p/L；(a) 右柱先降伏、崩塌位移為 (b) 的 2 倍")]
if __name__ == "__main__":
    assert (KA, KB, VA, VB) == (15.0, 24.0, 3.0, 4.0) and abs(V1 - 2.5) < 1e-12 and abs(DU_A - 2*DU_B) < 1e-12
    for fn, c in FIGURES: print(fn(), "—", c)
