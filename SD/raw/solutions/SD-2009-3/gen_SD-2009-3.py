#!/usr/bin/env python3
"""SD-2009-3 圖解產生器 — 三種地震水準：回歸期與 50 年超越機率

曲線 P(T) = 1 - (1 - 1/T)^n（n = 50 年使用年限）由程式逐點計算；三個規範水準的回歸期取自
現行《建築物耐震設計規範及解說》（111 年版）1.2 節解說、2.3 節、2.10.1 解說（解析 §3.5 L1 表）。
另標出「10 年超越機率 10%（≈95 年）」這個本庫舊解誤用的定義，讓它在 50 年尺度上的位置一目了然。
用法：python3 gen_SD-2009-3.py   （輸出 figs/SD-2009-3-fig-1-hazard-levels.svg；PNG 由 render.py 產生）
"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("STRUCTDRAW", os.path.join(HERE, "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))
sys.path.insert(0, SKILL)
from structdraw import Canvas, C

OUT = os.path.join(HERE, "figs")
N_LIFE = 50                                   # 使用年限（年）
def P50(T): return 1 - (1 - 1 / T) ** N_LIFE  # 50 年超越機率
def T_from(p, n): return -n / math.log(1 - p) # 由 n 年超越機率 p 反推回歸期（Poisson）

# ── 由 §3.5 L1 表／§4㈡（規範原文）──
LEVELS = [  # (回歸期, 名稱, 設計地震力, 性能, 規範寫的 50 年超越機率)
    (30,   "中小度地震", "V*", "保持彈性", "約 80%"),
    (475,  "設計地震",   "V",  "韌性需求 ≤ 容許韌性容量", "10%"),
    (2500, "最大考量地震", "V_{M}", "韌性可達韌性容量", "2%"),
]
T_WRONG = T_from(0.10, 10)                    # 10 年 10% → 94.9 年（舊解誤用）

def main():
    W, H = 900, 520
    L, R, T, B = 86, 40, 70, 70
    xmin, xmax = math.log10(10), math.log10(5000)
    pw, ph = W - L - R, H - T - B
    X = lambda Tr: L + (math.log10(Tr) - xmin) / (xmax - xmin) * pw
    Y = lambda p: B + p * ph                   # 數學座標（y 向上，原點在底）
    cv = Canvas(W, H, sx=1.0, ox=0, oy=0)
    cv.text_px(W / 2, 30, "三種地震水準：回歸期與 50 年超越機率", 18, C["text"], weight="700")
    # 格線與座標軸
    for p in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        cv.line((L, Y(p)), (L + pw, Y(p)), C["border"], w=1)
        cv.text((L - 10, Y(p)), f"{p*100:.0f}%", 12.5, C["muted"], anchor="end")
    for Tr in [10, 30, 100, 475, 1000, 2500, 5000]:
        cv.line((X(Tr), B), (X(Tr), B + ph), C["border"], w=1)
        cv.text((X(Tr), B - 18), f"{Tr}", 12.5, C["muted"])
    cv.line((L, B), (L + pw, B), C["member"], w=1.8)
    cv.line((L, B), (L, B + ph), C["member"], w=1.8)
    cv.text_px(L + pw / 2, H - 14, "回歸期 T（年，對數座標）", 13.5, C["text"])
    cv.text((L, B + ph + 20), "50 年超越機率", 13.5, C["text"], anchor="start")
    # 曲線
    pts, k = [], 0
    while True:
        Tr = 10 ** (xmin + k * 0.01)
        if Tr > 5000: break
        pts.append((X(Tr), Y(P50(Tr)))); k += 1
    cv.poly(pts, C["deform"], w=2.6)
    cv.text((560, B + 0.70 * ph), "P = 1 − (1 − 1/T)^{50}", 13.5, C["deform"], anchor="start")
    # 誤用定義（灰色空心）
    xw, yw = X(T_WRONG), Y(P50(T_WRONG))
    cv.dot((xw, yw), r=6, fill="#FFFFFF", stroke=C["muted"], w=2)
    cv.line((xw + 5, yw + 4), (xw + 40, yw + 22), C["muted"], w=1.2, dash="4 3")
    cv.text((xw + 44, yw + 38), "非台灣規範的中小度地震定義", 12.5, C["load"], anchor="start")
    cv.text((xw + 44, yw + 20), f"10 年超越 10%（≈{T_WRONG:.0f} 年，50 年超越 {P50(T_WRONG)*100:.0f}%）", 12.5, C["muted"], anchor="start")
    # 三個規範水準：標籤位置 (anchor x, 第一列 y)
    pos = {30: (X(30) + 34, Y(P50(30)) + 10, "start"),
           475: (X(475) + 14, 225, "start"),
           2500: (850, 175, "end")}
    for Tr, name, force, perf, ptxt in LEVELS:
        x, y = X(Tr), Y(P50(Tr))
        cv.dot((x, y), r=7, fill=C["accent"])
        lx, ly, anc = pos[Tr]
        if Tr != 30:
            cv.line((x, y + 7), (x + (6 if anc == "start" else 0), ly - 44), C["accent"], w=1.2)
        cv.text((lx, ly), f"{name}（{Tr} 年，{ptxt}）", 13.5, C["text"], anchor=anc, weight="700")
        cv.text((lx, ly - 18), f"設計地震力 {force}；{perf}", 12.5, C["accent"], anchor=anc)
        cv.text((lx, ly - 35), f"計算值 {P50(Tr)*100:.1f}%", 12, C["muted"], anchor=anc)
    os.makedirs(OUT, exist_ok=True)
    cv.save(os.path.join(OUT, "SD-2009-3-fig-1-hazard-levels.svg"))

if __name__ == "__main__":
    main()
