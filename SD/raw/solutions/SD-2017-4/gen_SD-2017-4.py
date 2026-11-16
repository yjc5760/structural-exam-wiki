#!/usr/bin/env python3
"""SD-2017-4：解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
fig-2-shape：假設振態 φ = x²/L² 與懸臂靜力位移形（三次式）的形狀與曲率比較。
攔下的錯誤：Rayleigh 商分子用 φ' 代替 φ''；以為 x²/L² 是真實振態（它在自由端仍有曲率 → 彎矩 ≠ 0，K* 偏大 → ω̄ 為上界）。
用法：python3 gen_SD-2017-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2017-4"

# ── 由 SD-2017-4.md 解得 ──
phi      = lambda s: s**2                      # §4 Step 1：φ(x)=x²/L²，s = x/L
phi_ex   = lambda s: 1.5*s**2 - 0.5*s**3       # §5.1：懸臂靜力位移形 3x²/2L² − x³/2L³
curv     = lambda s: 2.0                       # §4 Step 1：φ''·L² = 2（常數）
curv_ex  = lambda s: 3.0*(1 - s)               # 由 §5.1 三次式微分兩次：φ''·L² = 3(1 − x/L)
K_ASSUME = 2.0**2                              # §4 Step 2：K*·L³/EI = ∫(φ''L²)² ds = 4
K_EXACT  = sum(curv_ex((i+0.5)/2000)**2 for i in range(2000))/2000   # ∫(3(1−s))² ds = 3
RATIO    = (K_ASSUME/K_EXACT)**0.5             # §4 物理意義驗算：m→0 時 2/√3 ≈ 1.155

N = 60
def fig2():
    cv = fit(820, 470, (-0.6, 7.6), (-0.9, 4.0), L=20, R=20, T=20, B=20)
    H, Wd = 3.2, 2.2                          # 每格高 3.2 代表 L；水平比例 Wd 代表 φ=1 或 φ''L²=3
    # (a) 形狀
    x0 = 0.3
    cv.line((x0, 0), (x0, H), C["ghost"], 2.0)
    cv.line((x0 - 0.3, 0), (x0 + 0.5, 0), C["member"], 3.0)
    cv.poly([(x0 + Wd*phi(i/N), H*i/N) for i in range(N+1)], C["deform"], 2.6)
    cv.poly([(x0 + Wd*phi_ex(i/N), H*i/N) for i in range(N+1)], C["accent"], 2.2, dash="7 4")
    cv.dot((x0 + Wd, H), 4, C["deform"])
    cv.text((x0 + Wd, H), "φ(L) = 1", 12.5, C["text"], "start", dx=8)
    cv.text((x0 + 1.1, -0.25), "(a) 振態形狀", 13.5, C["text"], baseline="hanging")
    cv.text((x0 + 0.1, H*0.80), "x²/L²（假設）", 12.5, C["deform"], "start", dx=4)
    cv.text((x0 + 1.5, H*0.38), "3x²/2L² − x³/2L³", 12, C["accent"], "start")
    cv.text((x0 + 1.5, H*0.38), "（靜力位移形）", 12, C["accent"], "start", dy=16)
    # (b) 曲率 φ''·L²
    x1 = 4.4; sc = Wd/3.0
    cv.line((x1, 0), (x1, H), C["member"], 1.6)
    cv.poly([(x1 + sc*curv(i/N), H*i/N) for i in range(N+1)], C["deform"], 2.6)
    cv.poly([(x1 + sc*curv_ex(i/N), H*i/N) for i in range(N+1)], C["accent"], 2.2, dash="7 4")
    cv.text((x1 + sc*2, H), "2（自由端仍有曲率 → 彎矩 ≠ 0）", 12, C["deform"], "start", dx=4, dy=-12)
    cv.text((x1, H), "0", 12, C["accent"], "end", dx=-6)
    cv.text((x1 + sc*3, 0), "3", 12, C["accent"], "start", dx=6, dy=-8)
    cv.text((x1 + 1.1, -0.25), "(b) 曲率 φ''·L²", 13.5, C["text"], baseline="hanging")
    cv.text_px(410, 455, f"K*·L³/EI：假設振態 {K_ASSUME:.0f}，靜力位移形 {K_EXACT:.0f} → m→0 時頻率高估 {RATIO:.3f} 倍（上界）", 12.5, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-shape.svg")

FIGURES = [(fig2, "φ' 與 φ'' 混用；把 x²/L² 當真實振態")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
