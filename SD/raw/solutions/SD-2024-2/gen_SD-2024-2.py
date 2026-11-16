#!/usr/bin/env python3
"""SD-2024-2：解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
fig-2-virtual：兩個虛位移狀態 δu1 = 1、δu2 = 1，各自的中點位移 δv、轉角 δθ，與 p_t、p_θ 做的虛功 → Q1、Q2。
攔下的錯誤：p_θ 正向（逆時針）與 δθ = (δu2 − δu1)/L 的符號搭配錯，Q1、Q2 中 p_θ/L 項正負對調。
用法：python3 gen_SD-2024-2.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit, spring, ground
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2024-2"

# ── 由 SD-2024-2.md §4 Step 1、Step 4 ──
L = 1.0
def kin(du1, du2):           # δv = (δu1+δu2)/2，δθ = (δu2−δu1)/L（逆時針正）
    return (du1 + du2)/2, (du2 - du1)/L
STATES = [((1, 0), "δu_{1} = 1", "Q_{1} = p_{t}/2 − p_{θ}/L"),
          ((0, 1), "δu_{2} = 1", "Q_{2} = p_{t}/2 + p_{θ}/L")]

def fig2():
    cv = fit(860, 420, (-0.6, 11.4), (-2.6, 3.4), L=20, R=20, T=20, B=20)
    S, A = 4.4, 1.3                 # 桿長（圖上）、單位虛位移的放大
    for j, ((d1, d2), lab, q) in enumerate(STATES):
        ox = 0.4 + j*5.8
        dv, dth = kin(d1, d2)
        cv.line((ox, 0), (ox + S, 0), C["ghost"], 3.0, dash="6 4")               # 原位置
        y1, y2 = A*d1, A*d2
        cv.line((ox, y1), (ox + S, y2), C["member"], 3.2)                         # 虛位移後剛性桿
        for x, y in ((ox, y1), (ox + S, y2)):
            spring(cv, (x, y), (x, -1.4), n=5, amp=0.1); ground(cv, (x - 0.45, -1.4), (x + 0.45, -1.4), n=4)
        xm, ym = ox + S/2, A*dv
        cv.dot((xm, ym), 4.5, C["load"])
        cv.arrow((xm, ym), (xm, ym + 1.2), C["load"], 2.6, 9)
        cv.math((xm, ym + 1.2), "p_{t}", 14, C["load"], "start", dx=6, dy=4)
        cv.moment_arrow((xm, ym), r=20, ccw=True, color=C["load"], start=-80, span=230)
        cv.math((xm, ym), "p_{θ}", 14, C["load"], "end", dx=-26, dy=-22)
        dsel = (ox, y1) if d1 else (ox + S, y2)
        xa = dsel[0] + (-0.35 if d1 else 0.35)
        cv.line((xa, 0), (dsel[0], 0), C["deform"], 1.0, dash="3 3"); cv.line((xa, dsel[1]), dsel, C["deform"], 1.0, dash="3 3")
        cv.arrow((xa, 0), (xa, dsel[1]), C["deform"], 2.4, 8)
        cv.math((xa, dsel[1]), lab, 14, C["deform"], "start" if d1 else "end", dx=8 if d1 else -8, dy=-14)
        sgn = "+" if dth > 0 else "−"
        cv.text((ox + S/2, -2.0), f"δv = {dv:g}，δθ = {sgn}1/L（{'逆' if dth > 0 else '順'}時針）", 12.5, C["text"])
        cv.math((ox + S/2, -2.0), q, 14, C["load"], dy=22)
    cv.text_px(430, 18, "虛功 δW = p_t·δv + p_θ·δθ；u1、u2、p_t 向上為正，p_θ 逆時針為正", 12.5, C["muted"], baseline="hanging")
    return cv.save(f"{OUT}/{TAG}-fig-2-virtual.svg")

FIGURES = [(fig2, "p_θ/L 項在 Q1、Q2 的正負號")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
