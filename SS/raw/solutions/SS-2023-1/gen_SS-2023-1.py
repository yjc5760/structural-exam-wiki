#!/usr/bin/env python3
"""
SS-2023-1 兩層不規則構架各柱有效長度係數 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2023-1.py [輸出目錄]

重繪依據：題目正本 SS-2023-1-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪構架（依比例）；所附對位圖屬設計圖表，不重繪。各構材 I 值見題目正本 §1 表格。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "..", "skills", "struct-diagram", "scripts"))   # 五科合一後 skill 在根目錄 skills/

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2023-1"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2023-1-problem.md §4，已確認）；單位 m
# ══════════════════════════════════════════════════════════
SP_AB, SP_BC = 6.0, 10.0          # #2 梁 DE（GH）6 m、EF 10 m
H1, H2 = 4.0, 4.0                 # #2 一樓、二樓各 4 m
SUPPORT = {"A": "fixed", "B": "fixed", "C": "pin"}    # #1 A、B 固接；C 鉸支
XA, XB, XC = 0.0, SP_AB, SP_AB + SP_BC
N = {"A": (XA, 0), "B": (XB, 0), "C": (XC, 0), "D": (XA, H1), "E": (XB, H1), "F": (XC, H1),
     "G": (XA, H1 + H2), "H": (XB, H1 + H2)}          # #4 二樓只在左跨
MEMBERS = ["AD", "BE", "CF", "DG", "EH", "DE", "EF", "GH"]   # #3 節點皆剛接


def fig1_problem():
    W, H, sx = 760, 540, 30
    cv = Canvas(W, H, sx=sx, ox=150, oy=110)
    cv.panel("構架", "依比例；節點皆剛接")
    for m in MEMBERS:
        cv.line(N[m[0]], N[m[1]], C["member"], 4.2, cap="butt")
    for n, kind in SUPPORT.items():
        cv.support(N[n], kind, 0, size=16 if kind == "pin" else 20)
    off = {"A": (-24, -8), "B": (24, -10), "C": (-24, -10), "D": (-16, -14), "E": (16, -14),
           "F": (16, -14), "G": (-16, -14), "H": (16, -14)}
    for n, (dx, dy) in off.items():
        cv.text(N[n], n, 16, C["text"], "middle", dx=dx, dy=dy, weight="700")
    for n, lab in (("A", "Fixed"), ("B", "Fixed"), ("C", "Hinge")):
        cv.text(N[n], lab, 13, C["muted"], dy=44)
    cv.dim((XA, 0), (XB, 0), f"{SP_AB:g}m", off=72, label_off=16)
    cv.dim((XB, 0), (XC, 0), f"{SP_BC:g}m", off=72, label_off=16)
    cv.dim((XA, 0), (XA, H1), f"{H1:g}m", off=-50, label_off=-24)
    cv.dim((XA, H1), (XA, H1 + H2), f"{H2:g}m", off=-50, label_off=-24)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2023-1 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；對位圖為設計圖表，不重繪",
            note="二樓只在左跨（柱 DG、EH，梁 GH）；F 只接柱 CF 與梁 EF；C 為鉸支",
            path=path)
    return path


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-15 補繪）——數值全部取自 SS-2023-1.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_IC = {"AD": 16000, "BE": 16000, "CF": 16000, "DG": 3000, "EH": 3000}   # cm⁴  §4 一
Q_IB = {"DE": 35000, "EF": 17000, "GH": 35000}
Q_LEN = {m: 100 * math.dist(N[m[0]], N[m[1]]) for m in MEMBERS}          # cm
Q_R = {m: (Q_IC.get(m) or Q_IB.get(m)) / Q_LEN[m] for m in MEMBERS}
G_SUP = {"A": 1.0, "B": 1.0, "C": 10.0}                                  # §4 二：固接 1、鉸接 10


def q_g(n):
    if n in G_SUP:
        return G_SUP[n]
    cols = sum(Q_R[m] for m in Q_IC if n in m)
    beams = sum(Q_R[m] for m in Q_IB if n in m)
    return cols / beams


Q_G = {n: q_g(n) for n in N}


def q_k(ga, gb):
    """側移未束制對位圖方程式之精確解"""
    def f(x):
        return (ga * gb * x * x - 36) / (6 * (ga + gb)) - x / math.tan(x)
    lo, hi = 1e-6, math.pi - 1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return math.pi / ((lo + hi) / 2)


Q_K = {m: q_k(Q_G[m[0]], Q_G[m[1]]) for m in Q_IC}
q2 = lambda v: f"{math.floor(v * 100 + 0.5) / 100:.2f}"


def q_g_for_k(ga, k):
    lo, hi = 0.0, 200.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if q_k(ga, mid) > k:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def fig2_g():
    W1, PH = 1000, 620
    cv = Canvas(W1, PH, sx=44, ox=170, oy=160)
    cv.panel("各節點 G = Σ(Ic/Lc) / Σ(Ib/Lb)，各柱 K（側移未束制）", "數字：桿件旁 = I/L（cm³）；方框 = G；柱右側 = K")
    for m in MEMBERS:
        col = C["compr"] if m in Q_IC else C["bmd"]
        cv.line(N[m[0]], N[m[1]], col, 4.6, cap="butt")
    for n, kind in SUPPORT.items():
        cv.support(N[n], kind, 0, size=16 if kind == "pin" else 20)
    for m in MEMBERS:
        (x0, y0), (x1, y1) = N[m[0]], N[m[1]]
        mid = ((x0 + x1) / 2, (y0 + y1) / 2)
        if m in Q_IB:
            cv.text(mid, f"{Q_IB[m]}/{Q_LEN[m]:.0f} = {Q_R[m]:.2f}", 12.5, C["bmd"], dy=18)
        else:
            cv.text(mid, f"{Q_R[m]:.1f}", 12.5, C["compr"], "end", dx=-10, dy=-12)
            cv.text(mid, f"K = {q2(Q_K[m])}", 14, C["load"], "start", dx=10, dy=4, weight="700")
    gpos = {"A": (0, 50), "B": (0, 50), "C": (0, 50), "D": (-50, -28), "E": (-48, -28),
            "F": (52, -28), "G": (-48, -24), "H": (52, -24)}
    for n, (dx, dy) in gpos.items():
        x, y = cv.P(N[n])
        g = Q_G[n]
        s = f"{n}：{g:.0f}" if n == "C" else f"{n}：{g:.1f}" if n in "AB" else f"{n}：{g:.2f}"
        w = 9 * len(s) + 14
        cv.rect_px(x + dx - w / 2, y + dy - 13, w, 26, "#FFFFFF", 6, stroke=C["accent"], sw=1.4)
        cv.text_px(x + dx, y + dy, s, 13, C["accent"], weight="700")
    cv.text_px(cv.X(XA), cv.Y(0) + 76, "固接取 1.0", 11.5, C["muted"])
    cv.text_px(cv.X(XC), cv.Y(0) + 76, "鉸接取 10", 11.5, C["muted"])
    cv.text_px(cv.X(XC), cv.Y(H1) - 58, "F 上方無柱、右方無梁", 12, C["muted"])
    cv.text_px(cv.X(XB) + 66, cv.Y(H1 + H2) - 4, "H 只接 EH 與 GH", 12, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-2-g.svg")
    compose([cv], cols=1,
            title=f"圖 2　G 值與 K：CF 柱 K = {q2(Q_K['CF'])} 最大，其餘 {q2(min(Q_K[m] for m in ('AD','BE','DG','EH')))}–{q2(max(Q_K[m] for m in ('AD','BE','DG','EH')))}",
            sub="只計入「剛接到該節點」的桿件；梁 EF 不接到 H，不能算進 G_H",
            note=f"E：({Q_R['BE']:.1f}+{Q_R['EH']:.1f})/({Q_R['DE']:.2f}+{Q_R['EF']:.2f})；F：{Q_R['CF']:.1f}/{Q_R['EF']:.2f}；H：{Q_R['EH']:.1f}/{Q_R['GH']:.2f}（誤加 EF 會得 {Q_R['EH']/(Q_R['GH']+Q_R['EF']):.2f}）",
            path=path)
    return path


def fig3_kcurve():
    W1, H1p = 1000, 560
    cv = Canvas(W1, H1p, sx=1)
    cv.panel("柱 CF：K 隨頂端 G 變化（底端鉸接 G = 10）", "曲線由對位圖方程式解出，即考場查圖的精確版")
    X0, X1, YB, YT = 110, 640, 460, 110
    gm, k0, k1 = 6.0, 1.0, 3.0
    PX = lambda g: X0 + (X1 - X0) * g / gm
    PY = lambda k: YB - (YB - YT) * (k - k0) / (k1 - k0)
    _hl(cv, H1p, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1p, X0, YB, X0, YT, C["muted"], 1.5)
    for g in range(0, 7):
        cv.text_px(PX(g), YB + 18, f"{g}", 11.5, C["muted"])
    for k in (1.0, 1.5, 2.0, 2.5, 3.0):
        cv.text_px(X0 - 8, PY(k), f"{k:.1f}", 11.5, C["muted"], "end")
        _hl(cv, H1p, X0, PY(k), X1, PY(k), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "頂端 G_F", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "K", 13, C["text"], "start", weight="700")
    gs = [gm * i / 200 for i in range(1, 201)]
    cv.poly([(PX(g), H1p - PY(min(q_k(10.0, g), k1))) for g in gs], C["bmd"], 2.8)
    gf, kf = Q_G["F"], Q_K["CF"]
    _hl(cv, H1p, PX(gf), YB, PX(gf), PY(kf), C["accent"], 1.4, dash="4 3")
    cv.dot((PX(gf), H1p - PY(kf)), 6.5, fill=C["bmd"])
    cv.text_px(PX(gf) + 12, PY(kf) + 18, f"K = {kf:.2f}", 13, C["bmd"], "start", weight="700")
    cv.text_px(PX(gf), YB + 34, f"{gf:.2f}", 11.5, C["accent"], weight="700")
    g25 = q_g_for_k(10.0, 2.5)
    cv.dot((PX(g25), H1p - PY(2.5)), 6, fill=C["load"])
    _hl(cv, H1p, PX(g25), YB, PX(g25), PY(2.5), C["load"], 1.2, dash="4 3")
    cv.text_px(PX(g25) + 10, PY(2.5) + 24, "誤讀 K = 2.50", 12.5, C["load"], "start", weight="700")
    xt = 680
    rows = [("CF 兩端：", C["text"]),
            (f"G_C = 10、G_F = {gf:.2f}", C["text"]),
            (f"K = {q2(kf)}，KL = {kf * Q_LEN['CF'] / 100:.2f} m", C["bmd"]),
            ("", C["text"]),
            ("查圖自我檢查：", C["text"]),
            (f"G_F 介於 2 與 3 ⇒ K 在 {q_k(10, 2):.2f}–{q_k(10, 3):.2f}", C["muted"]),
            (f"讀到 2.50 需要 G_F ≈ {g25:.1f}", C["load"]),
            ("與 2.35 不符，就是查錯線", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight="700" if col in (C["bmd"], C["load"]) else "400")
    path = os.path.join(OUT, f"{TAG}-fig-3-kcurve.svg")
    compose([cv], cols=1,
            title=f"圖 3　柱 CF 的 K：F 端 G = {gf:.2f} 時 K = {kf:.2f}",
            sub="底端鉸接（G = 10）、頂端只靠梁 EF 束制，K 是全構架最大",
            note=f"其餘四柱兩端 G 都小於 1.0，K 落在 {q2(min(Q_K[m] for m in ('AD','BE','DG','EH')))}–{q2(max(Q_K[m] for m in ('AD','BE','DG','EH')))}",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "C 讀成固接；二樓多畫到右跨；跨度 6／10 m 對調"),
    (fig2_g, "§4 二",
     "G_H 誤加梁 EF；F 節點補上不存在的上柱或右梁；C 取固接；柱梁 I/L 放錯分子分母"),
    (fig3_kcurve, "§4 三",
     "CF 柱對位圖查成 2.50；鉸接底取 ∞ 而非規定的 10"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
