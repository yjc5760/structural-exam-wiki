#!/usr/bin/env python3
"""SD-2005-3：解題圖解（struct-diagram；2026-11-16，組 U2-2-G1 階段 E）
數值由題目給定量依現行規範 §2.6／§2.11 重算（與 §4 及 scripts/fixes/2026-11-16_verify_SD-2005-3.py 相同）。
用法：python3 gen_SD-2005-3.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2005-3"
# ── 題目給定（題目正本 §2）與 §4 解得 ──
h = [4.0 + 3.2*i for i in range(12)]; W = [400] + [300]*10 + [200]; V = 450.0
LV = ["2F"] + [f"{i}F" for i in range(3, 13)] + ["R"]
hn = h[-1]; T = 0.070*hn**0.75; Ft = min(0.07*T*V, 0.25*V) if T > 0.7 else 0.0
S = sum(w*x for w, x in zip(W, h))
F = [(V - Ft)*w*x/S for w, x in zip(W, h)]; Fd_roof = F[-1]; F[-1] += Ft
F0 = [V*w*x/S for w, x in zip(W, h)]
Vs = [sum(F[k:]) for k in range(12)]; Vs0 = [sum(F0[k:]) for k in range(12)]

def fig1():
    Wpx, Hpx = 900, 560
    cv = fit(Wpx, Hpx, (-3.0, 30.0), (-4.5, 44.5), L=16, R=16, T=16, B=16)
    # 左：樓層地震力（1 t → 0.12 單位）
    sF, x0 = 0.12, 0.0
    cv.line((x0, 0), (x0, hn), C["member"], 2.4)
    cv.line((x0 - 1.5, 0), (x0 + 11, 0), C["member"], 2.0)
    for k, (y, f, f0) in enumerate(zip(h, F, F0)):
        if k == 11:
            cv.polygon([(x0, y - 0.6), (x0 + Fd_roof*sF, y - 0.6), (x0 + Fd_roof*sF, y + 0.6), (x0, y + 0.6)], C["fill_c"], C["deform"], 1.2)
            cv.polygon([(x0 + Fd_roof*sF, y - 0.6), (x0 + f*sF, y - 0.6), (x0 + f*sF, y + 0.6), (x0 + Fd_roof*sF, y + 0.6)], C["fill_t"], C["load"], 1.2)
        else:
            cv.polygon([(x0, y - 0.6), (x0 + f*sF, y - 0.6), (x0 + f*sF, y + 0.6), (x0, y + 0.6)], C["fill_c"], C["deform"], 1.2)
        cv.line((x0 + f0*sF, y - 0.95), (x0 + f0*sF, y + 0.95), C["muted"], 1.6, dash="3,3")
        cv.text((x0, y), LV[k], 11.5, C["muted"], "end", dx=-6)
        cv.text((x0 + max(f, f0)*sF, y), f"{f:.1f}", 11, C["text"], "start", dx=6)
    cv.text((x0 + Fd_roof*sF + Ft*sF/2, hn), f"F_t = {Ft:.1f}", 12, C["load"], dy=-18)
    cv.text((x0 + 5, -2.4), "樓層地震力 F_x（t）", 13.5, C["text"], weight="700")
    # 右：層剪力（1 t → 0.022 單位）
    sV, x1 = 0.022, 17.0
    cv.line((x1, 0), (x1, hn), C["member"], 2.4); cv.line((x1 - 1.5, 0), (x1 + 11.5, 0), C["member"], 2.0)
    pts, pts0 = [], []
    for k in range(11, -1, -1):
        top, bot = h[k], (h[k-1] if k else 0.0)
        pts += [(x1 + Vs[k]*sV, top), (x1 + Vs[k]*sV, bot)]; pts0 += [(x1 + Vs0[k]*sV, top), (x1 + Vs0[k]*sV, bot)]
    cv.polygon([(x1, hn)] + pts + [(x1, 0)], C["fill_s"], C["sfd"], 1.6)
    cv.poly([(x1, hn)] + pts0, C["muted"], 1.5, dash="5,4")
    for k in (11, 10, 5, 0):
        cv.text((x1 + Vs[k]*sV, (h[k] + (h[k-1] if k else 0))/2), f"{Vs[k]:.1f}", 11, C["text"], "start", dx=5)
    cv.text((x1 + 5, -2.4), "層剪力 V_x（t）", 13.5, C["text"], weight="700")
    cv.text_px(Wpx/2, Hpx - 12, f"T = 0.070·39.2^{{3/4}} = {T:.3f} s > 0.7 s → F_t = 0.07TV = {Ft:.2f} t；虛線＝舊解 F_t = 0（屋頂 {F0[-1]:.1f} t）", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-1-story-forces.svg")

FIGURES = [(fig1, "沒給 T 不代表 F_t = 0：頂層集中力使屋頂力 47.5→78.4 t，其餘樓層同比例減少")]
if __name__ == "__main__":
    for fn, catches in FIGURES: print(fn(), "—", catches)
