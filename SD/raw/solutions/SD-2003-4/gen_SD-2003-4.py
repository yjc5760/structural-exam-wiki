#!/usr/bin/env python3
"""SD-2003-4：解題圖解（struct-diagram；2026-11-16 圖解補繪，非勘誤）
fig-2：u2＝1（u1＝u3＝0）時樓版繞 D 轉動 θ＝1/a 的平面圖，以及由此得到的勁度矩陣第二行。
所有數值取自已驗證正本 SD-2003-4.md §4（驗算 scripts/fixes/2026-11-16_verify_SD-2003-4.py，MISMATCHES: 0）。
用法：python3 gen_SD-2003-4.py [輸出目錄]；之後執行 struct-diagram 的 render.py 產生 2× PNG。"""
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "figs", "_lib"))
from structdraw import C
from sdprob import fit
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SD-2003-4"
A = 4.0                     # 邊長 a（圖面單位）
S = 0.6                     # 位移放大：u2＝1 畫成 0.6 個圖面單位
TH = 1.0/A                  # θ＝1/a（每單位 u2）
P = {"D": (0, 0), "C": (A, 0), "B": (A, A), "A": (0, A)}
DISP = {n: (-TH*y, TH*x) for n, (x, y) in P.items()}   # 以「u2＝1」為單位：A(−1,0) B(−1,1) C(0,1) D(0,0)
K2 = {"k12": "−3k", "k22": "5k", "k32": "−3k"}               # 正本 §4 Step 3（k＝12EI/h³）
def fig2():
    cv = fit(860, 470, (-1.6, 15.2), (-1.4, 6.3), L=20, R=20, T=30, B=50)
    # (a) 運動
    cv.text_px(215, 22, "(a) u2 = 1、u1 = u3 = 0：樓版繞 D 轉動 θ = 1/a", 14, C["text"], weight="700")
    sq = [P[n] for n in "DCBA"]
    cv.poly(sq + [sq[0]], C["ghost"], 2.4)
    dq = [(x + S*DISP[n][0], y + S*DISP[n][1]) for n, (x, y) in zip("DCBA", sq)]
    cv.poly(dq + [dq[0]], C["deform"], 2.6)
    for n, (x, y) in P.items():
        cv.math((x, y), n, 15, C["muted"], dx=-14 if x == 0 else 14, dy=14 if y == 0 else -12)
        dx, dy = DISP[n]
        if dx or dy:
            cv.arrow((x, y), (x + S*dx, y + S*dy), C["deform"], 2.2, 8)
            lab = f"({dx:+.0f}, {dy:+.0f})".replace("+0", "0").replace("-0", "0")
            cv.text((x + S*dx, y + S*dy), lab, 12.5, C["deform"], "start" if x > 0 else "end", dx=8 if x > 0 else -8, dy=-10)
    cv.dot(P["D"], 5, C["accent"]); cv.text(P["D"], "D 不動（轉動中心）", 12.5, C["accent"], "start", dx=10, dy=18)
    cv.text_px(215, 440, "灰：原位置　藍：u2 = 1 後（位移放大示意）；括號為角點位移 (δx, δy)", 12, C["muted"])
    # (b) 第二行
    ox = 9.6
    cv.text_px(650, 22, "(b) 需施加於 C、B、A 的廣義力 = 第二行", 14, C["text"], weight="700")
    Q = {n: (x + ox, y) for n, (x, y) in P.items()}
    cv.poly([Q[n] for n in "DCBA"] + [Q["D"]], C["member"], 2.4)
    for n, (x, y) in Q.items():
        cv.math((x, y), n, 15, C["muted"], dx=-14 if x == ox else 14, dy=14 if y == 0 else -12)
    cx, cy = Q["C"]; cv.arrow((cx + 0.2, cy), (cx - 1.4, cy), C["load"], 3.0, 10)
    cv.text((cx - 1.4, cy), "k12 = −3k（沿 −x）", 12.5, C["load"], "end", dx=-6, dy=-14)
    bx, by = Q["B"]; cv.arrow((bx, by), (bx, by + 1.5), C["load"], 3.0, 10)
    cv.text((bx, by + 1.5), "k22 = 5k", 12.5, C["load"], "start", dx=8)
    ax_, ay = Q["A"]; cv.arrow((ax_, ay + 1.0), (ax_, ay - 0.0), C["load"], 3.0, 10)
    cv.text((ax_, ay + 1.0), "k32 = −3k（向下）", 12.5, C["load"], "end", dx=-8)
    cv.text_px(650, 420, "k = 12EI/h³：k12 = −36EI/h³、k22 = 60EI/h³、k32 = −36EI/h³", 12.5, C["text"])
    cv.text_px(650, 440, "柱力合計 ΣFx = −3k、ΣFy = 2k、ΣM_D = 5ka", 12, C["muted"])
    return cv.save(f"{OUT}/{TAG}-fig-2-u2-unit.svg")
FIGURES = [(fig2, "u2 是 B 點平移、不是質心 y；u2＝1 時樓版繞 D 轉")]
if __name__ == "__main__":
    for fn, c in FIGURES: print(fn(), "—", c)
