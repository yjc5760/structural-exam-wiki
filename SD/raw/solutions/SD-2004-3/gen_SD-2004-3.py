#!/usr/bin/env python3
"""SD-2004-3：解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
fig-2：假設變形 v＝sin(πx/L)Z 下，F 點位移 √2/2·Z、CD 繞 C 鉸轉動（D 端 √2·Z），並與「整根平移」誤讀對照。
數值取自已驗證正本 SD-2004-3.md §4（驗算 scripts/fixes/2026-11-16_verify_SD-2004-3.py，MISMATCHES: 0）。
用法：python3 gen_SD-2004-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os, math
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2004-3"
L, HY, Z = 10.0, 3.6, 1.3                    # Z：跨中撓度（圖面放大）
vF = math.sin(math.pi/4)*Z                    # √2/2·Z
vD = vF*(L/2)/(L/4)                           # √2·Z
def fig2():
    cv = fit(720, 470, (-1.2, 11.6), (-1.3, 6.9), L=20, R=20, T=20, B=60)
    cv.line((0, 0), (L, 0), C["ghost"], 2.2); cv.line((0, HY), (L/2, HY), C["ghost"], 2.2)
    cv.support((0, 0), "pin"); cv.support((L, 0), "roller"); cv.support((0, HY), "pin")
    cv.poly([(L*i/80, Z*math.sin(math.pi*i/80)) for i in range(81)], C["deform"], 2.6)        # AB 變形
    cv.line((0, HY), (L/2, HY + vD), C["deform"], 4.0)                                         # CD 繞 C 轉
    cv.line((0, HY+vF), (L/2, HY + vF), C["load"], 2.0, dash="3,4")                            # 誤：整根平移
    cv.line((L/4, vF), (L/4, HY + vF), C["deform"], 2.0)                                       # EF
    for p in ((L/4, vF), (L/4, HY + vF)): cv.circle(p, 0.1, "#FFFFFF", C["deform"], 2)
    cv.text((L/4, vF), "E：v = (√2/2)Z", 12.5, C["deform"], "start", dx=10, dy=14)
    cv.text((L/4, HY + vF), "F：v = (√2/2)Z", 12.5, C["deform"], "end", dx=-10, dy=-16)
    cv.text((L/2, HY + vD), "D：v = √2 Z", 12.5, C["deform"], "start", dx=10)
    cv.text((0, HY), "C（鉸）", 12.5, C["muted"], "end", dx=-10, dy=-8)
    cv.text((L/2, Z), "AB：v = sin(πx/L)·Z", 12.5, C["deform"], "start", dx=14, dy=-10)
    cv.text((L/2, HY + vF), "誤讀：整根平移", 12, C["load"], "start", dx=10, dy=12)
    cv.text_px(360, 420, "正：CD 繞 C 轉動 θ = 2√2 Z / L，m*CD = I_C θ² = m0 L / 3", 13, C["deform"])
    cv.text_px(360, 442, "誤：CD 各點位移都取 (√2/2)Z → m*CD = m0 L / 4（少 25%）", 13, C["load"])
    return cv.save(f"{OUT}/{TAG}-fig-2-cd-rotation.svg")
FIGURES = [(fig2, "C 為鉸支承，CD 繞 C 轉、D 端位移是 F 的兩倍")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
