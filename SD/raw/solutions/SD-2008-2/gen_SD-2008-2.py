#!/usr/bin/env python3
"""SD-2008-2 圖解產生器 — 每 3 層換斷面時各層強度／需求比 r_i 與 0.8 r_{i+1} 門檻（§4 示例）。
圖上數字全由頂端參數算出，與 §4 示例表一致（scripts/fixes/2026-11-16_verify_SD-2008-2.py 驗算）。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get("STRUCTDRAW", os.path.join(HERE, "../../../../skills/struct-diagram/scripts")))
from structdraw import Canvas, C
OUT = os.path.join(HERE, "figs")

# ── 由 §4 示例：12 層、等重等高、倒三角、每 GROUP 層換斷面、各群強度＝群底層設計層剪力 ──
N, GROUP, LIM = 12, 3, 0.8
V = [sum(range(i, N + 1)) for i in range(1, N + 1)]
Vu = [V[(i // GROUP) * GROUP] for i in range(N)]
r = [Vu[i] / V[i] for i in range(N)]

def fig1():
    W, H = 980, 700
    L, T_, B = 120, 100, 80
    XR = 3.0
    row = (H - T_ - B) / N
    sx = 1.0
    cv = Canvas(W, H, sx=sx, ox=0, oy=0)
    X0, XW = L, 560
    px = lambda v: X0 + v / XR * XW
    cv.text_px(W / 2, 32, "圖 1　每 3 層換一次斷面：各層強度／需求比 r_i 與 0.8 r_{i+1} 門檻（示例）", 16.5, C["text"], weight="700")
    cv.text_px(W / 2, 56, "12 層、等重等高、倒三角層剪力；各斷面群強度＝該群最底層設計層剪力", 13, C["muted"])
    ytop = T_
    yc = lambda i: ytop + (N - 1 - i) * row + row / 2      # i = 0 為一樓（最下）
    for i in range(N):
        weak = i < N - 1 and r[i] < LIM * r[i + 1]
        col = C["load"] if weak else (C["deform"] if i % GROUP == 0 else C["member2"])
        cv.rect_px(X0, yc(i) - row * 0.32, px(r[i]) - X0, row * 0.64, col, rx=4)
        cv.text_px(X0 - 14, yc(i), f"{i+1}F", 13, C["text"], "end", weight="700")
        xl = max(r[i], LIM * r[i + 1] if i < N - 1 else 0)
        cv.text_px(px(xl) + 10, yc(i), f"{r[i]:.3f}", 12.5, col, "start", weight="700")
        if i < N - 1:
            th = LIM * r[i + 1]
            cv.line((px(th), H - (yc(i) - row * 0.45)), (px(th), H - (yc(i) + row * 0.45)), C["accent"], 3.0)
            q = r[i] / r[i + 1]
            cv.text_px(X0 + XW + 150, yc(i), f"r_{{{i+1}}}/r_{{{i+2}}} = {q:.3f}" + ("  弱層" if q < LIM else ""), 12.5,
                       C["load"] if q < LIM else C["muted"], "start", weight="700" if q < LIM else "400")
    for g in range(1, N // GROUP):
        y = ytop + (N - g * GROUP) * row
        cv.line((X0 - 60, H - y), (X0 + XW + 140, H - y), C["border"], 1.6, dash="6 5")
    cv.text_px(X0 + XW + 30, ytop - 14, "換斷面（虛線）", 12, C["muted"], "start")
    cv.line((px(1.0), H - ytop + 6), (px(1.0), H - (ytop + N * row)), C["muted"], 1.0, dash="3 4")
    for v in (0, 1, 2, 3):
        cv.text_px(px(v), ytop + N * row + 18, f"{v}", 12, C["muted"])
    cv.text_px(px(1.5), ytop + N * row + 40, "r_i = V_{u,i} / V_i", 13, C["muted"])
    cv.legend(X0 + XW - 150, ytop + 4 * row,
              [(C["deform"], "各群最底層（r 最低）"), (C["member2"], "群內其他層"),
               (C["load"], "r_i ＜ 0.8 r_{i+1}：弱層"), (C["accent"], "門檻 0.8 r_{i+1}")])
    cv.text_px(W / 2, H - 16, "攔錯：規範比的是「強度／需求」比值，不是 V_{u,i} / V_{u,i+1}；換斷面處下方那層比值反而較高", 13, C["muted"])
    cv.save(f"{OUT}/SD-2008-2-fig-1-strength-ratio.svg")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig1()
    print("r =", [round(x, 3) for x in r])
