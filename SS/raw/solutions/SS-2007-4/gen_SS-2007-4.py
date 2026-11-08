#!/usr/bin/env python3
"""
SS-2007-4 兩層不規則構架各柱有效長度係數 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2007-4.py [輸出目錄]

重繪依據：題目正本 SS-2007-4-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪圖三構架（依比例）；考卷所附對位圖（Sidesway Uninhibited）屬設計圖表，不重繪。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2007-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2007-4-problem.md §4，已確認）；單位 m
# ══════════════════════════════════════════════════════════
SPAN_AB, SPAN_BC = 6.0, 10.0       # #2 A-B 6 m、B-C 10 m
H1, H2 = 4.0, 3.0                  # #3 一層 4 m、二層 3 m
SUPPORT = {"A": "pin", "B": "fixed", "C": "fixed"}     # #1 A 鉸接、B、C 固接
XA, XB, XC = 0.0, SPAN_AB, SPAN_AB + SPAN_BC
NODES = {"A": (XA, 0), "B": (XB, 0), "C": (XC, 0),
         "D": (XA, H1), "E": (XB, H1), "F": (XC, H1),
         "G": (XB, H1 + H2), "H": (XC, H1 + H2)}       # #4 二層只在 B-C 跨上方
MEMBERS = ["AD", "BE", "CF", "EG", "FH", "DE", "EF", "GH"]
LABEL_DIR = {"A": (-22, -6), "B": (26, -10), "C": (-26, -10), "D": (-16, -14), "E": (-14, -14),
             "F": (16, -14), "G": (-14, -14), "H": (16, -14)}


def fig1_problem():
    W, H, sx = 760, 470, 30
    cv = Canvas(W, H, sx=sx, ox=130, oy=110)
    cv.panel("圖三　構架", "依比例；側移未束制")
    for m in MEMBERS:
        cv.line(NODES[m[0]], NODES[m[1]], C["member"], 4.2, cap="butt")
    for n, kind in SUPPORT.items():
        cv.support(NODES[n], kind, 0, size=16 if kind == "pin" else 20)
    for n, (dx, dy) in LABEL_DIR.items():
        cv.text(NODES[n], n, 16, C["text"], "middle", dx=dx, dy=dy, weight="700")
    cv.text((XA, 0), "hinge", 13, C["muted"], dy=46)
    cv.text((XB, 0), "Fixed", 13, C["muted"], dy=46)
    cv.text((XC, 0), "Fixed", 13, C["muted"], dy=46)
    cv.dim((XA, 0), (XB, 0), f"{SPAN_AB:g} m", off=70, label_off=16)
    cv.dim((XB, 0), (XC, 0), f"{SPAN_BC:g} m", off=70, label_off=16)
    cv.dim((XC, 0), (XC, H1), f"{H1:g} m", off=50, label_off=26)
    cv.dim((XC, H1), (XC, H1 + H2), f"{H2:g} m", off=50, label_off=26)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2007-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；對位圖為設計圖表，不重繪",
            note="二層只在 B-C 跨上方（柱 EG、FH，梁 GH）；D 上方無柱",
            path=path)
    return path


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def rsum(terms, nd=3):
    """與解析相同的加法：各項先四捨五入到 nd 位再相加"""
    return round(sum(round(t, nd) for t in terms), nd)


def _stack_row(cv, x0, y, scale, terms, colors, name, total_color, h=34, fmt="{:.3f}"):
    """水平堆疊長條：互制比 1.0 對應 scale 像素"""
    cv.text_px(x0 - 14, y, name, 14, C["text"], "end", weight="700")
    xx = x0
    for t, col in zip(terms, colors):
        w = scale * t
        cv.rect_px(xx, y - h/2, w, h, col, 0)
        if w > 44:
            cv.text_px(xx + w/2, y, fmt.format(t), 12.5, "#FFFFFF", weight="700")
        xx += w
    tot = rsum(terms)
    cv.text_px(xx + 12, y, "= " + fmt.format(tot), 15, total_color, "start", weight="700")
    return tot


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2007-4.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_IC = {"AD": 15000, "BE": 15000, "CF": 15000, "EG": 4000, "FH": 4000}   # cm⁴  §4 Step 1
Q_IB = {"DE": 17000, "EF": 36000, "GH": 36000}
Q_LEN = {m: 100 * math.dist(NODES[m[0]], NODES[m[1]]) for m in MEMBERS}  # cm
Q_R = {m: (Q_IC.get(m) or Q_IB.get(m)) / Q_LEN[m] for m in MEMBERS}


def q_g(n):
    if n == "A":
        return 10.0
    if n in ("B", "C"):
        return 1.0
    cols = sum(Q_R[m] for m in Q_IC if n in m)
    beams = sum(Q_R[m] for m in Q_IB if n in m)
    return cols / beams


Q_G = {n: q_g(n) for n in NODES}


def q_k(ga, gb):
    """側移未束制對位圖方程式之精確解（ga 可為 inf）"""
    def f(x):
        if math.isinf(ga):
            lhs = gb * x * x / 6
        else:
            lhs = (ga * gb * x * x - 36) / (6 * (ga + gb))
        return lhs - x / math.tan(x)
    lo, hi = 1e-6, math.pi - 1e-9
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return math.pi / ((lo + hi) / 2)


Q_K = {m: q_k(Q_G[m[0]], Q_G[m[1]]) for m in Q_IC}
q2 = lambda v: f"{math.floor(v * 100 + 0.5) / 100:.2f}"   # 四捨五入（與解析同）


def q_g_for_k(ga, k):
    lo, hi = 0.0, 100.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if q_k(ga, mid) > k:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def fig1_g():
    W1, PH = 1000, 600
    cv = Canvas(W1, PH, sx=44, ox=200, oy=150)
    cv.panel("各節點 G = Σ(Ic/Lc) / Σ(Ib/Lb)，各柱 K（側移未束制）", "數字：桿件旁 = I/L（cm³）；方框 = G；柱右側 = K")
    for m in MEMBERS:
        col = C["compr"] if m in Q_IC else C["bmd"]
        cv.line(NODES[m[0]], NODES[m[1]], col, 4.6, cap="butt")
    for n, kind in SUPPORT.items():
        cv.support(NODES[n], kind, 0, size=16 if kind == "pin" else 20)
    for m in MEMBERS:
        (x0, y0), (x1, y1) = NODES[m[0]], NODES[m[1]]
        mid = ((x0 + x1) / 2, (y0 + y1) / 2)
        if m in Q_IB:
            cv.text(mid, f"{Q_IB[m]}/{Q_LEN[m]:.0f} = {Q_R[m]:.2f}", 12.5, C["bmd"], dy=18)
        else:
            cv.text(mid, f"{Q_R[m]:.2f}", 12.5, C["compr"], "end", dx=-10, dy=-12)
            cv.text(mid, f"K = {q2(Q_K[m])}", 14, C["load"], "start", dx=10, dy=4, weight="700")
    gpos = {"A": (-46, 0), "B": (0, 46), "C": (0, 46), "D": (-46, -28), "E": (-46, -28),
            "F": (52, -28), "G": (-46, -24), "H": (52, -24)}
    for n, (dx, dy) in gpos.items():
        x, y = cv.P(NODES[n])
        s = f"{n}：{Q_G[n]:.0f}" if n == "A" else f"{n}：{Q_G[n]:.1f}" if n in "BC" else f"{n}：{Q_G[n]:.2f}"
        w = 9 * len(s) + 14
        cv.rect_px(x + dx - w / 2, y + dy - 13, w, 26, "#FFFFFF", 6, stroke=C["accent"], sw=1.4)
        cv.text_px(x + dx, y + dy, s, 13, C["accent"], weight="700")
    cv.text_px(cv.X(XA) - 100, cv.Y(0) + 4, "鉸接取 10", 11.5, C["muted"])
    cv.text_px(cv.X(XB), cv.Y(0) + 72, "固接取 1.0", 11.5, C["muted"])
    cv.text_px(cv.X(XA), cv.Y(H1) - 56, "D 上方無柱", 12, C["muted"])
    cv.text_px(cv.X(XC) + 60, cv.Y(H1) + 26, "F 右方無梁", 12, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-1-g.svg")
    compose([cv], cols=1,
            title=f"圖 1　G 值與 K：AD 柱 K = {q2(Q_K['AD'])} 最大，其餘 {q2(min(Q_K[m] for m in ('BE','CF','EG','FH')))}–{q2(max(Q_K[m] for m in ('BE','CF','EG','FH')))}",
            sub="只計入「剛接到該節點」的桿件；不存在的柱或梁不能補上",
            note=f"D：{Q_R['AD']:.2f}/{Q_R['DE']:.2f}；E：({Q_R['BE']:.2f}+{Q_R['EG']:.2f})/({Q_R['DE']:.2f}+{Q_R['EF']:.2f})；F：({Q_R['CF']:.2f}+{Q_R['FH']:.2f})/{Q_R['EF']:.2f}",
            path=path)
    return path


def fig3_kcurve():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("柱 AD：K 隨頂端 G 變化（底端 G = 10 與 G = ∞）", "曲線由對位圖方程式解出，即考場查圖的精確版")
    X0, X1, YB, YT = 110, 640, 460, 110
    gm, k0, k1 = 6.0, 1.0, 3.5
    PX = lambda g: X0 + (X1 - X0) * g / gm
    PY = lambda k: YB - (YB - YT) * (k - k0) / (k1 - k0)
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for g in range(0, 7):
        cv.text_px(PX(g), YB + 18, f"{g}", 11.5, C["muted"])
    for k in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        cv.text_px(X0 - 8, PY(k), f"{k:.1f}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(k), X1, PY(k), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "頂端 G_D", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "K", 13, C["text"], "start", weight="700")
    gs = [gm * i / 200 for i in range(1, 201)]
    cv.poly([(PX(g), H1 - PY(q_k(math.inf, g))) for g in gs if q_k(math.inf, g) <= k1], C["ghost"], 2.4, dash="7 5")
    cv.poly([(PX(g), H1 - PY(min(q_k(10.0, g), k1))) for g in gs], C["bmd"], 2.8)
    gd = Q_G["D"]
    kd, ki = Q_K["AD"], q_k(math.inf, gd)
    _hl(cv, H1, PX(gd), YB, PX(gd), PY(ki), C["accent"], 1.4, dash="4 3")
    cv.dot((PX(gd), H1 - PY(kd)), 6.5, fill=C["bmd"])
    cv.text_px(PX(gd) + 10, PY(kd) + 16, f"G = 10：K = {kd:.2f} ✓", 13, C["bmd"], "start", weight="700")
    cv.dot((PX(gd), H1 - PY(ki)), 5, fill=C["muted"])
    cv.text_px(PX(gd) - 10, PY(ki) - 12, f"G = ∞：{ki:.2f}", 12.5, C["muted"], "end")
    g25 = q_g_for_k(10.0, 2.5)
    cv.dot((PX(g25), H1 - PY(2.5)), 6, fill=C["load"])
    _hl(cv, H1, PX(g25), YB, PX(g25), PY(2.5), C["load"], 1.2, dash="4 3")
    cv.text_px(PX(g25) - 12, PY(2.5) - 16, f"誤讀 K = 2.5 ⇒ G_D 需 ≈ {g25:.1f}", 12.5, C["load"], "end", weight="700")
    cv.text_px(PX(gd), YB + 34, f"{gd:.2f}", 11.5, C["accent"], weight="700")
    cv.legend(X1 - 230, YB - 70, [(C["bmd"], "底端 G = 10（規定）"), (C["ghost"], "底端 G = ∞（理論鉸）")], size=12, gap=19)
    xt = 680
    rows = [("AD 兩端：", C["text"]),
            (f"G_A = 10、G_D = {gd:.2f}", C["text"]),
            (f"K = {q2(kd)}，KL = {kd * Q_LEN['AD']:.0f} cm", C["bmd"]),
            ("", C["text"]),
            ("查圖自我檢查：", C["text"]),
            ("鉸接底 + 有限剛度頂", C["muted"]),
            ("⇒ K 必略小於 2（G=∞、頂固時正好 2）", C["muted"]),
            (f"讀到 2.5 就是查錯線", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight="700" if col in (C["bmd"], C["load"]) else "400")
    path = os.path.join(OUT, f"{TAG}-fig-2-kcurve.svg")
    compose([cv], cols=1,
            title=f"圖 2　柱 AD 的 K：D 端 G = {gd:.2f} 時 K = {kd:.2f}（若底端取 ∞ 則 {ki:.2f}）",
            sub="題目規定鉸接取 G = 10，K 比理論鉸接小",
            note="同一頂端 G，底端 G 從 ∞ 改成 10 會讓 K 明顯下降；K 落在 2.5 需要 D 端 G 遠大於本題值",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "A 端讀成固接；D 上方多畫一根柱；跨度 6／10 m 對調"),
    (fig1_g, "§4 Step 1–3",
     "D 節點補上不存在的上柱；F 節點多算右梁；A 取固接；柱梁 I/L 放錯分子分母"),
    (fig3_kcurve, "§4 Step 3",
     "AD 柱對位圖查成 2.5；鉸接底取 ∞ 而非規定的 10"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
