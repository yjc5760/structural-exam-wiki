#!/usr/bin/env python3
"""SD-2023-3 解題圖解（struct-diagram；2026-11-16，U3-2-G4 階段 E）。可重跑：python3 gen_SD-2023-3.py [輸出目錄]
㈢ 等效阻尼比的能量意義：割線勁度 K_eff、彈性應變能 E_S0 = K_eff D²/2（三角形）、遲滯迴圈面積 E_D。
考卷只給迴圈面積 50 kN·m，迴圈形狀為示意（雙線性，參數由面積＝50、頂點＝(D, K_eff·D) 反算）。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2023-3"
W, D, K, ED, G = 5000.0, 0.4, 1000.0, 50.0, 9.81      # 題目給定（kN、m）
Fm = K*D; ES0 = 0.5*K*D*D; xi = ED/(2*math.pi*K*D*D); T = 2*math.pi*math.sqrt(W/(G*K))
K1 = 3000.0                                            # 示意雙線性迴圈：初始勁度（假設）
def loop(Q=None):
    Q = QQ if Q is None else Q
    K2 = (Fm - Q)/D                                    # 上下分支 y = ±Q + K2·x 通過頂點 (±D, ±Fm)
    xb = (Fm + Q - K1*D)/(K2 - K1)                     # 自頂點以 K1 卸載至下分支
    return [(-D, -Fm), (-xb, -(-Q + K2*xb)), (D, Fm), (xb, -Q + K2*xb)]
def area(p):
    return abs(sum(p[i][0]*p[(i+1) % len(p)][1] - p[(i+1) % len(p)][0]*p[i][1] for i in range(len(p))))/2
lo, hi = 0.0, Fm/2
for _ in range(200):                                   # 以二分法求 Q 使示意迴圈面積 = E_D
    QQ = (lo + hi)/2
    if area(loop(QQ)) < ED: lo = QQ
    else: hi = QQ
def fig1():
    s = 1/1000                                         # kN → 圖面單位（1 單位 = 1000 kN）
    cv = fit(660, 440, (-0.55, 0.62), (-0.50, 0.52), L=30, R=20, T=14, B=56)
    cv.line((-0.5, 0), (0.55, 0), C["muted"], 1.5); cv.line((0, -0.47), (0, 0.48), C["muted"], 1.5)
    cv.text((0.55, 0), "位移 (m)", 12, C["muted"], "end", dy=16); cv.text((0, 0.48), "力 (kN)", 12, C["muted"], "start", dx=6)
    P = [(x, y*s) for x, y in loop()]
    cv.polygon(P, "rgba(46,125,111,0.20)", C["bmd"], 2.2)                      # E_D
    cv.polygon([(0, 0), (D, 0), (D, Fm*s)], "rgba(192,57,43,0.16)", C["load"], 1.2)   # E_S0
    cv.line((-D*1.1, -Fm*s*1.1), (D*1.15, Fm*s*1.15), C["deform"], 2.0, dash="6 4")  # K_eff
    cv.dot((D, Fm*s), 5, C["deform"], "#FFFFFF", 1.4)
    cv.text((D, Fm*s), f"(D, K_{{eff}}D) = (0.4 m, {Fm:.0f} kN)", 12.5, C["deform"], "start", dx=10, dy=6)
    cv.text((0.13, 0.05), f"E_{{S0}} = {ES0:.0f} kN·m", 12.5, C["load"], "start")
    cv.text((0.06, -0.30), f"E_{{D}} = {ED:.0f} kN·m（迴圈面積）", 13, C["bmd"], "start")
    cv.text((0.06, -0.35), "迴圈形狀為示意，考卷只給面積", 11.5, C["muted"], "start")
    cv.text((0.17, 0.30), f"割線 K_{{eff}} = {K:.0f} kN/m", 12.5, C["deform"], "end")
    for v in (-0.4, -0.2, 0.2, 0.4):
        cv.line((v, -0.01), (v, 0.01), C["muted"], 1.2)
        cv.text((v, 0), f"{v:g}", 11, C["muted"], dy=14 if v > 0 else -12)
        cv.line((-0.01, v), (0.01, v), C["muted"], 1.2)
        cv.text((0, v), f"{v*1000:g}", 11, C["muted"], "end" if v > 0 else "start", dx=-8 if v > 0 else 8)
    cv.text_px(330, 400, f"ξ = E_{{D}} / (4π E_{{S0}}) = E_{{D}} / (2π K_{{eff}} D²) = {ED:.0f} / (4π×{ES0:.0f}) = {xi*100:.2f}%；E_{{S0}} = K_{{eff}}D²/2", 13, C["text"])
    cv.text_px(330, 424, f"T_{{eff}} = 2π (W / g K_{{eff}})^{{1/2}} = {T:.2f} s（g = 9.81 m/s²）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-energy.svg")
FIGURES = [(fig1, "攔：分母漏 2π（ξ 誤為 31%）或用 4π K D²（誤為 2.5%）；E_S0 是割線三角形不是迴圈面積")]
if __name__ == "__main__":
    assert abs(area(loop()) - ED) < 1e-6, area(loop())
    print(f"E_S0={ES0} ξ={xi:.5f} T={T:.4f} 示意迴圈面積={area(loop()):.3f} Q={QQ:.2f} kN")
    for fn, c in FIGURES: print(fn(), "—", c)
