#!/usr/bin/env python3
"""
SS-2011-4 無側撐鋼架柱 DE、EF 之有效長度係數 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2011-4.py [輸出目錄]

重繪依據：題目正本 SS-2011-4-problem.md §4 判讀清單（2026-11-02 已確認）。
只重繪構架（依比例）；考卷所附對位圖（Sidesway not prevented）屬設計圖表，不重繪。
各構材 I 值在考卷表格中（題目正本 §1），圖上不重複。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2011-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2011-4-problem.md §4，已確認）；單位 m
# ══════════════════════════════════════════════════════════
H_UP, H_LO = 4.0, 5.0           # #11 上層 4 m（AB、DE）、下層 5 m（BC、EF）
SP_L, SP_R = 6.0, 8.0           # #11 左跨 6 m（AD、BE）、右跨 8 m（DG、EH）
X0, X1, X2 = 0.0, SP_L, SP_L + SP_R
Y0, Y1, Y2 = 0.0, H_LO, H_LO + H_UP
N = {"A": (X0, Y2), "B": (X0, Y1), "C": (X0, Y0), "D": (X1, Y2), "E": (X1, Y1),
     "F": (X1, Y0), "G": (X2, Y2), "H": (X2, Y1)}
MEMBERS = ["AB", "BC", "DE", "EF", "AD", "DG", "BE", "EH"]   # #10 D 上方無柱
#   #4 A 鉸圓；#5 B 剛接；#6 C 固接；#7 F 鉸支；#8 G 導槽（可平移、不可轉）；#9 H 滾支（可轉）


def _guided(cv, p):
    """G：方塊上下各一排滾輪、外側固定面 → 可水平移動、不可轉動、不可垂直移動"""
    x, y = cv.P(p)
    m = C["member"]
    cv.parts.append(f'<rect x="{x:.1f}" y="{y-6:.1f}" width="22" height="12" fill="{m}"/>')
    for sgn in (-1, 1):
        for dx in (6, 16):
            cv.parts.append(f'<circle cx="{x+dx:.1f}" cy="{y+sgn*11:.1f}" r="4.6" fill="#FFFFFF" '
                            f'stroke="{m}" stroke-width="1.8"/>')
        yy = y + sgn * 17
        cv.parts.append(f'<line x1="{x-2:.1f}" y1="{yy:.1f}" x2="{x+26:.1f}" y2="{yy:.1f}" '
                        f'stroke="{m}" stroke-width="2.4"/>')
        for k in range(4):
            bx = x + k * 8
            cv.parts.append(f'<line x1="{bx:.1f}" y1="{yy:.1f}" x2="{bx+6:.1f}" y2="{yy+sgn*7:.1f}" '
                            f'stroke="{m}" stroke-width="1.6"/>')


def fig1_problem():
    W, H, sx = 700, 560, 34
    cv = Canvas(W, H, sx=sx, ox=150, oy=120)
    cv.panel("構架", "依比例；無側撐")
    for m in MEMBERS:
        cv.line(N[m[0]], N[m[1]], C["member"], 4.0, cap="butt")
    cv.dot(N["A"], 6, fill="#FFFFFF", stroke=C["member"], w=2.4)      # A 鉸圓
    cv.support(N["C"], "fixed", 0, size=20)
    cv.support(N["F"], "pin", 0, size=14)
    _guided(cv, N["G"])
    cv.support(N["H"], "roller", 0, size=14)
    off = {"A": (-16, -14), "B": (-16, -14), "C": (-16, -14), "D": (0, -18), "E": (-16, -14),
           "F": (-16, -14), "G": (-14, -16), "H": (0, -22)}
    for n, (dx, dy) in off.items():
        cv.text(N[n], n, 15, C["text"], "middle", dx=dx, dy=dy, weight="700")
    cv.dim(N["B"], N["A"], f"{H_UP:g}m", off=-50, label_off=-24)
    cv.dim(N["C"], N["B"], f"{H_LO:g}m", off=-50, label_off=-24)
    cv.dim((X0, Y0), (X1, Y0), f"{SP_L:g}m", off=62, label_off=16)
    cv.dim((X1, Y0), (X2, Y0), f"{SP_R:g}m", off=62, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2011-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #4–#11；對位圖為設計圖表，不重繪",
            note="A 鉸接、C 固接、F 鉸支；G 可平移不可轉、H 可轉；D 上方無柱",
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


q2 = lambda v: f"{math.floor(v * 100 + 0.5) / 100:.2f}"   # 四捨五入（與解析同）


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2011-4.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_I = {"DE": 11400, "EF": 11400, "AD": 24000, "DG": 28000, "BE": 30000, "EH": 36000}   # cm⁴
Q_L = {m: 100 * math.dist(N[m[0]], N[m[1]]) for m in Q_I}
Q_ALPHA = {"AD": 1 / 2, "DG": 2 / 3, "BE": 1.0, "EH": 1 / 2}     # 遠端：鉸／固定可滑／剛接連續柱／滾支  §4 Step 1a
Q_FAR = {"AD": "遠端鉸 ×1/2", "DG": "遠端不轉 ×2/3", "BE": "×1.0", "EH": "遠端可轉 ×1/2"}
Q_R = {m: Q_I[m] / Q_L[m] for m in Q_I}
Q_GD = Q_R["DE"] / (Q_ALPHA["AD"] * Q_R["AD"] + Q_ALPHA["DG"] * Q_R["DG"])
Q_GE = (Q_R["DE"] + Q_R["EF"]) / (Q_ALPHA["BE"] * Q_R["BE"] + Q_ALPHA["EH"] * Q_R["EH"])
Q_GF = 10.0
Q_GD0 = Q_R["DE"] / (Q_R["AD"] + Q_R["DG"])
Q_GE0 = (Q_R["DE"] + Q_R["EF"]) / (Q_R["BE"] + Q_R["EH"])
Q_FY, Q_E, Q_RG = 2.52, 2040.0, 10.5          # tf/cm²、cm（柱 r）            §4 Part 2
Q_CC = math.sqrt(2 * math.pi ** 2 * Q_E / Q_FY)


def q_fa(klr):
    if klr >= Q_CC:
        return 12 * math.pi ** 2 * Q_E / (23 * klr ** 2)
    rr = klr / Q_CC
    return (1 - rr ** 2 / 2) * Q_FY / (5 / 3 + 3 * rr / 8 - rr ** 3 / 8)


def q_iter(k0, n=3):
    rows, k = [], k0
    for _ in range(n):
        klr = k * Q_L["EF"] / Q_RG
        fa, fe = q_fa(klr), 12 * math.pi ** 2 * Q_E / (23 * klr ** 2)
        tau = fa / fe
        knew = q_k(tau * Q_GE, Q_GF)
        rows.append((k, klr, fa, fe, tau, tau * Q_GE, knew))
        k = knew
    return rows


def fig1_alpha():
    W1, PH1 = 1000, 560
    cv = Canvas(W1, PH1, sx=36, ox=150, oy=100)
    cv.panel("梁遠端修正：G = Σ(Ic/Lc) / Σ(α·Ib/Lb)", "數字：桿件旁 I/L（cm³）× α；方框 G（括號為未修正值）；柱旁 K")
    for m in MEMBERS:
        cv.line(N[m[0]], N[m[1]], C["compr"] if m in ("AB", "BC", "DE", "EF") else C["bmd"], 4.2, cap="butt")
    cv.dot(N["A"], 6, fill="#FFFFFF", stroke=C["member"], w=2.4)
    cv.support(N["C"], "fixed", 0, size=20)
    cv.support(N["F"], "pin", 0, size=14)
    _guided(cv, N["G"])
    cv.support(N["H"], "roller", 0, size=14)
    for m in ("AD", "DG", "BE", "EH"):
        (x0, y0), (x1, y1) = N[m[0]], N[m[1]]
        mid = ((x0 + x1) / 2, y0)
        col = C["load"] if Q_ALPHA[m] != 1 else C["bmd"]
        cv.text(mid, f"{Q_R[m]:.2f} {Q_FAR[m]} = {Q_ALPHA[m] * Q_R[m]:.2f}", 12.5, col, dy=-14 if m in ("AD", "DG") else 18, weight="700")
    for m in ("DE", "EF"):
        (x0, y0), (x1, y1) = N[m[0]], N[m[1]]
        mid = (x0, (y0 + y1) / 2)
        cv.text(mid, f"{Q_R[m]:.2f}", 12.5, C["compr"], "end", dx=-10)
    kde, kef = q_k(Q_GD, Q_GE), q_k(Q_GE, Q_GF)
    kde0, kef0 = q_k(Q_GD0, Q_GE0), q_k(Q_GE0, Q_GF)
    cv.text((X1, (Y1 + Y2) / 2), f"K = {q2(kde)}（{q2(kde0)}）", 14, C["accent"], "start", dx=12, weight="700")
    cv.text((X1, Y1 / 2), f"K = {q2(kef)}（{q2(kef0)}）", 14, C["accent"], "start", dx=12, weight="700")
    for n, g, g0, dx, dy in (("D", Q_GD, Q_GD0, 0, -44), ("E", Q_GE, Q_GE0, 78, -24)):
        x, y = cv.P(N[n])
        s = f"{n}：{g:.3f}（{g0:.3f}）"
        w = 8.6 * len(s) + 10
        cv.rect_px(x + dx - w / 2, y + dy - 13, w, 26, "#FFFFFF", 6, stroke=C["accent"], sw=1.4)
        cv.text_px(x + dx, y + dy, s, 12.5, C["accent"], weight="700")
    x, y = cv.P(N["F"])
    cv.text_px(x + 50, y + 8, "F：10（鉸支）", 12.5, C["accent"], "start", weight="700")
    for n, dx, dy in (("A", -16, -14), ("C", -16, -14), ("G", 44, -4), ("H", 46, 4), ("B", -16, -14)):
        cv.text(N[n], n, 14, C["text"], "middle", dx=dx, dy=dy, weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-alpha.svg")
    compose([cv], cols=1,
            title=f"圖 1　遠端修正後 G_D = {Q_GD:.3f}、G_E = {Q_GE:.3f}：K_DE = {q2(kde)}、K_EF = {q2(kef)}",
            sub="對位圖假設梁兩端等角同向轉（近端 6EI/L）；遠端鉸 → 3EI/L、遠端不轉 → 4EI/L",
            note=f"未修正（括號）會高估梁的束制，K 偏小（{q2(kde0)}、{q2(kef0)}），偏不安全",
            path=path)
    return path


def fig2_iter():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("柱 EF：K 對頂端 G（底端 G_F = 10）與非彈性迭代", "G' = τa·G，τa = Fa / F'e；迭代至 K 不再變動")
    X0, X1, YB, YT = 100, 520, 450, 120
    g0, g1, k0, k1 = 0.45, 0.75, 1.76, 1.86
    PX = lambda g: X0 + (X1 - X0) * (g - g0) / (g1 - g0)
    PY = lambda k: YB - (YB - YT) * (k - k0) / (k1 - k0)
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for i in range(7):
        g = g0 + 0.05 * i
        cv.text_px(PX(g), YB + 18, f"{g:.2f}", 11.5, C["muted"])
    for i in range(6):
        k = k0 + 0.02 * i
        cv.text_px(X0 - 8, PY(k), f"{k:.2f}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(k), X1, PY(k), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "柱頂 G（節點 E）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "K", 13, C["text"], "start", weight="700")
    gs = [g0 + (g1 - g0) * i / 100 for i in range(101)]
    cv.poly([(PX(g), H1 - PY(q_k(g, Q_GF))) for g in gs], C["bmd"], 2.6)
    rows = q_iter(q_k(Q_GE, Q_GF))
    cv.dot((PX(Q_GE), H1 - PY(rows[0][0])), 6.5, fill=C["compr"])
    cv.text_px(PX(Q_GE) - 10, PY(rows[0][0]) - 16, f"彈性 G = {Q_GE:.3f}，K = {rows[0][0]:.3f}", 12, C["compr"], "end", weight="700")
    for i, r in enumerate(rows):
        cv.dot((PX(r[5]), H1 - PY(r[6])), 5, fill=C["load"] if i < len(rows) - 1 else C["accent"])
    last = rows[-1]
    cv.text_px(PX(last[5]) + 8, PY(last[6]) + 22, f"收斂 G' = {last[5]:.3f}，K = {last[6]:.2f}", 12.5, C["accent"], "start", weight="700")
    xt, y0 = 560, 140
    hdr = ["次", "K", "KL/r", "Fa", "F'e", "τa", "G'E", "新 K"]
    xs = [xt + 22 * 0 + c * 52 for c in range(8)]
    for c, h in enumerate(hdr):
        cv.text_px(xs[c], y0, h, 12.5, C["text"], weight="700")
    for i, r in enumerate(rows):
        vals = [f"{i + 1}", f"{r[0]:.3f}", f"{r[1]:.1f}", f"{r[2]:.3f}", f"{r[3]:.3f}", f"{r[4]:.3f}", f"{r[5]:.3f}", f"{r[6]:.3f}"]
        for c, v in enumerate(vals):
            cv.text_px(xs[c], y0 + 32 * (i + 1), v, 12, C["accent"] if c == 7 else C["text"])
    cv.text_px(xt, y0 + 32 * 5, f"Cc = {Q_CC:.1f}；KL/r 小於 Cc ⇒ 非彈性，τa 小於 1", 12.5, C["muted"], "start")
    cv.text_px(xt, y0 + 32 * 6, "τa 只乘在柱的 I/L；G_F = 10 是指定值，不折減", 12.5, C["muted"], "start")
    cv.text_px(xt, y0 + 32 * 7, f"非彈性 K ≈ {last[6]:.2f}（彈性 {rows[0][0]:.2f}）", 13, C["accent"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-iter.svg")
    compose([cv], cols=1,
            title=f"圖 2　ASD 非彈性 K：τa ≈ {last[4]:.2f}，G'_E = {last[5]:.3f}，K_EF 由 {rows[0][0]:.2f} 降到 {last[6]:.2f}",
            sub="一次修正（以彈性 KL/r 求 τa）已得 1.80，與收斂值差不到 0.5%",
            note="τa 誤乘到梁、或把 G_F = 10 也乘 τa，都會讓 K 偏離；非彈性 K 一定小於彈性 K",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "A 讀成剛接、F 讀成固接；G、H 遠端條件對調（梁遠端修正係數用錯）"),
    (fig1_alpha, "§4 Part 1",
     "梁遠端條件不修正（α 一律取 1）；G 點不可轉卻取 1/2；D 補上不存在的上柱"),
    (fig2_iter, "§4 Part 2",
     "τa 乘到梁或乘到 G_F；KL/r 超過 Cc 仍用非彈性式；忘了迭代"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
