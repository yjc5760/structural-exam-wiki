#!/usr/bin/env python3
"""
SS-2008-3 簡支 H 型鋼梁（兩端局部均佈、四點側撐）LRFD 容許標稱載重 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2008-3.py [輸出目錄]

重繪依據：題目正本 SS-2008-3-problem.md §4 判讀清單（待確認）。
圖上每個支承、載重範圍、側撐都對應清單一項；只畫考卷給的東西，不含任何解題結果
（不畫彎矩圖、不標 Cb、Lb 判定）。
立面與平面的跨度依比例（L = 18 m 三等分）；載重箭頭高度、梁線寬為示意；
右側斷面依題給 d、bf、tf、tw 按比例放大繪製（只表達座標方位）。
不重繪：第 3–4 頁參考公式（已照錄於 problem.md §2）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2008-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2008-3-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
L = 18.0                        # 題文 L = 18 m
NSEG = 3                        # 圖 2：三等分 L/3
SUP_A, SUP_D = "roller", "pin"  # #1 A 滾支、D 鉸支
LOADED = (0, 2)                 # #2 w 只在 AB（第 0 段）、CD（第 2 段）；BC 無載重
BRACED = ("A", "B", "C", "D")   # #3 四點兩側側撐
#                                 #4 繞強軸 x，y 向下為載重方向
D, BF, TF, TW = 54.43, 21.22, 2.12, 1.31   # 題文斷面尺寸（cm），僅畫斷面方位

PW, PH = 820, 320
SEG = L / NSEG
NAMES = ["A", "B", "C", "D"]


def _sec(cv, x0, y0, k):
    """在 (x0, y0)（模型單位 m）畫 I 斷面，k = 每 cm 對應的模型長度；回傳半寬、半高"""
    bf, d = BF * k, D * k
    for xa, xb, ya, yb in ((-BF / 2, BF / 2, D / 2 - TF, D / 2), (-BF / 2, BF / 2, -D / 2, -D / 2 + TF),
                           (-TW / 2, TW / 2, -D / 2 + TF, D / 2 - TF)):
        cv.polygon([(x0 + xa * k, y0 + ya * k), (x0 + xb * k, y0 + ya * k),
                    (x0 + xb * k, y0 + yb * k), (x0 + xa * k, y0 + yb * k)],
                   C["fill_c"], C["member"], 1.4)
    return bf / 2, d / 2


def elev_panel():
    sx = 32.0
    cv = Canvas(PW, PH, sx=sx, ox=70, oy=140)
    cv.panel("立面", "A 滾支、D 鉸支；w 只作用於 AB、CD 兩段（BC 無載重）")
    cv.line((0, 0), (L, 0), C["member"], 4.5, cap="butt")
    cv.support((0, 0), SUP_A, 0, size=13)
    cv.support((L, 0), SUP_D, 0, size=13)
    for k in LOADED:
        x0, x1 = k * SEG, (k + 1) * SEG
        cv.udl((x0, 0), (x1, 0), 1.6, n=7, label="w")
    for j, nm in enumerate(NAMES):
        x = j * SEG
        dx = -20 if j == 0 else (24 if j == NSEG else 12)
        dy = -12 if j == 0 else (26 if j == NSEG else 18)
        cv.text((x, 0), nm, 15, C["text"], "end" if j == 0 else "start", dx=dx, dy=dy,
                weight="700")
        if 0 < j < NSEG:
            cv.line((x, -0.15), (x, 0.15), C["member"], 2)
    for k in range(NSEG):
        cv.dim((k * SEG, 0), ((k + 1) * SEG, 0), "L/3", off=58, label_off=14)
    cv.text_px(cv.X(L / 2), cv.Y(0) + 96, f"L = {L:.0f} m（題文）", 13, C["muted"])
    # 座標：z 向右、y 向下
    cv.arrow((L + 0.25, 0), (L + 1.6, 0), C["text"], 1.6, 8)
    cv.math((L + 1.6, 0), "z", 15, C["text"], "start", dx=6)
    cv.arrow((-1.1, -0.5), (-1.1, -2.4), C["text"], 1.6, 8)
    cv.math((-1.1, -2.4), "y", 15, C["text"], "end", dx=-6, dy=4)
    # 斷面方位（x 向左、y 向下）
    sx0, sy0 = L + 3.6, 1.3
    hb, hd = _sec(cv, sx0, sy0, 0.040)
    cv.arrow((sx0, sy0), (sx0 - hb - 1.0, sy0), C["text"], 1.6, 8)
    cv.math((sx0 - hb - 1.0, sy0), "x", 15, C["text"], "end", dx=-6)
    cv.arrow((sx0, sy0), (sx0, sy0 - hd - 0.9), C["text"], 1.6, 8)
    cv.math((sx0, sy0 - hd - 0.9), "y", 15, C["text"], dy=14)
    return cv


def plan_panel():
    sx = 32.0
    cv = Canvas(PW, PH, sx=sx, ox=70, oy=140)
    cv.panel("平面（側撐補強）", "A、B、C、D 四點兩側皆有側撐")
    cv.line((0, 0), (L, 0), C["member"], 4.5, cap="butt")
    for j, nm in enumerate(NAMES):
        x = j * SEG
        if nm in BRACED:
            cv.support((x, 0), "roller", 0, size=11)
            cv.support((x, 0), "roller", 180, size=11)
        cv.text((x, 0), nm, 15, C["text"], dy=-52, weight="700")
    cv.arrow((L + 0.6, 0), (L + 2.0, 0), C["text"], 1.6, 8)
    cv.math((L + 2.0, 0), "z", 15, C["text"], "start", dx=6)
    cv.arrow((-1.1, -0.3), (-1.1, -2.2), C["text"], 1.6, 8)
    cv.math((-1.1, -2.2), "x", 15, C["text"], "end", dx=-6, dy=4)
    cv.text((L, 0), "（側撐補強）", 13, C["muted"], "end", dy=60)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([elev_panel(), plan_panel()], cols=1,
            title="SS-2008-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#4；只畫考卷所給條件（圖 2）",
            note="w 只在兩端各 L/3（AB、CD），中段 BC 無載重；四點側撐把梁分成三段 L/3",
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


def q_mn_lrfd(lb, cb, mp, mr, lp, lr, sx, x1, x2, ry):
    """LRFD 撓曲 Mn（tf·cm；lb、lp、lr 為 cm）"""
    if lb <= lp:
        return mp
    if lb <= lr:
        return min(cb * (mp - (mp - mr) * (lb - lp) / (lr - lp)), mp)
    s = lb / ry
    return min(cb * sx * x1 * math.sqrt(2) / s * math.sqrt(1 + x1 * x1 * x2 / (2 * s * s)), mp)


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2008-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_FR, Q_E, Q_G = 3.5, 0.69, 2100.0, 840.0
Q_SX, Q_ZX, Q_IY, Q_RY, Q_J, Q_CW, Q_A = 2802.0, 3212.0, 3388.0, 4.65, 181.0, 2317464.0, 156.77
Q_MP = Q_FY * Q_ZX                                        # 11,242
Q_MR = (Q_FY - Q_FR) * Q_SX                               # 7,874
Q_X1 = math.pi / Q_SX * math.sqrt(Q_E * Q_G * Q_J * Q_A / 2)
Q_X2 = 4 * Q_CW / Q_IY * (Q_SX / (Q_G * Q_J)) ** 2
Q_LP = 80 * Q_RY / math.sqrt(Q_FY)
Q_LR = Q_RY * Q_X1 / (Q_FY - Q_FR) * math.sqrt(1 + math.sqrt(1 + Q_X2 * (Q_FY - Q_FR) ** 2))
Q_LB = L / NSEG * 100                                     # 600 cm
mn = lambda lb, cb: q_mn_lrfd(max(lb, 1e-6), cb, Q_MP, Q_MR, Q_LP, Q_LR, Q_SX, Q_X1, Q_X2, Q_RY)
Q_MCR = mn(Q_LB, 1.0)                                     # 7,465
Q_MCR2 = math.pi / Q_LB * math.sqrt(Q_E * Q_IY * Q_G * Q_J + (math.pi * Q_E / Q_LB) ** 2 * Q_IY * Q_CW)   # 雙路徑
Q_MW = lambda x: 6 * x - x * x / 2 if x <= 6 else (18.0 if x <= 12 else 6 * (18 - x) - (18 - x) ** 2 / 2)   # M/w
Q_CB_AB = 12.5 * 18 / (2.5 * 18 + 3 * Q_MW(1.5) + 4 * Q_MW(3) + 3 * Q_MW(4.5))   # 1.30
Q_CB_BC = 1.0
Q_PHIMN = {"AB": 0.9 * mn(Q_LB, Q_CB_AB) / 100, "BC": 0.9 * Q_MCR / 100, "CD": 0.9 * mn(Q_LB, Q_CB_AB) / 100}
Q_WCR = min(v / 18 for v in Q_PHIMN.values())             # 3.73 t/m


def fig1_cb():
    W1, H1 = 1000, 470
    cv = Canvas(W1, H1, sx=44, ox=110, oy=105)
    cv.panel("彎矩圖（M / w，t·m per t/m）與各無支撐段 Cb", "w 只作用在 AB、CD；BC 段彎矩為常數 18w")
    for i in range(NSEG):
        x0, x1 = i * SEG, (i + 1) * SEG
        if i in LOADED:
            cv.udl((x0, 4.2), (x1, 4.2), 0.9, n=9, color=C["load"], w=1.8)
    cv.line((0, 4.2), (L, 4.2), C["member"], 5, cap="butt")
    for k, n in enumerate(NAMES):
        x = k * SEG
        cv.line((x, 3.8), (x, 4.6), C["accent"], 2.4, cap="butt")
        cv.text((x, 3.8), n, 13, C["text"], dx=-12, dy=14, weight="700")
    sc = 0.15
    xs = [L * i / 180 for i in range(181)]
    cv.polygon([(0, 0)] + [(x, Q_MW(x) * sc) for x in xs] + [(L, 0)], C["fill_m"], C["bmd"], 2.4)
    cv.line((0, 0), (L, 0), C["muted"], 1.2)
    for x in (1.5, 3, 4.5):
        cv.line((x, 0), (x, Q_MW(x) * sc), C["bmd"], 1, dash="3 3")
        cv.text((x, Q_MW(x) * sc), f"{Q_MW(x):g}", 11, C["bmd"], dy=-10)
    cv.text((9, 18 * sc), "18w（均勻彎矩）", 12.5, C["bmd"], dy=-12, weight="700")
    for i, (seg, cb, note) in enumerate((("AB", Q_CB_AB, "四分點式"), ("BC", Q_CB_BC, "均勻彎矩"), ("CD", Q_CB_AB, "對稱"))):
        xm = (i + 0.5) * SEG
        cv.text((xm, 0), f"Cb = {cb:.2f}", 14, C["load"] if seg == "BC" else C["compr"], dy=24, weight="700")
        cv.text((xm, 0), note, 11.5, C["muted"], dy=44)
    path = os.path.join(OUT, f"{TAG}-fig-1-cb.svg")
    compose([cv], cols=1,
            title=f"圖 1　三段 Lb 都是 6 m，但 BC 段均勻彎矩 Cb = 1.0 最不利；AB、CD 段 Cb = {Q_CB_AB:.2f}",
            sub=f"AB 四分點 M = 7.875w、13.5w、16.875w，Mmax = 18w：Cb = 12.5 × 18 / (2.5 × 18 + 3 × 7.875 + 4 × 13.5 + 3 × 16.875)",
            note="以為 BC 段沒載重就不控制是錯的：它的彎矩最大且均勻，受壓翼板整段受同樣壓力",
            path=path)
    return path


def fig2_curve():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("φbMn 對 Lb（t·m）", f"Lp = {Q_LP:.0f} cm、Lr = {Q_LR:.0f} cm；Lb = {Q_LB:.0f} cm 略大於 Lr → 彈性 LTB")
    X0, X1, YB, YT = 100, 620, 450, 110
    lmax, mmax = 900.0, 110.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda m: YB - (YB - YT) * m / mmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 901, 150):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for v in range(0, 111, 20):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "Lb（cm）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "φbMn（t·m）", 13, C["text"], "start", weight="700")
    ls = [lmax * i / 300 for i in range(0, 301)]
    cv.poly([(PX(l), H1 - PY(0.9 * mn(l, Q_CB_AB) / 100)) for l in ls], C["compr"], 2.2, dash="7 4")
    cv.poly([(PX(l), H1 - PY(0.9 * mn(l, 1.0) / 100)) for l in ls], C["bmd"], 2.8)
    for l, lab in ((Q_LP, "Lp"), (Q_LR, "Lr")):
        _hl(cv, H1, PX(l), YB, PX(l), YT, C["accent"], 1.1, dash="4 4")
        cv.text_px(PX(l) + 4, YT + 6, f"{lab} = {l:.0f}", 11.5, C["accent"], "start")
    for seg, cb, col, dx, anc, nd in (("BC", 1.0, C["load"], -12, "end", 2), ("AB、CD", Q_CB_AB, C["compr"], 12, "start", 1)):
        v = 0.9 * mn(Q_LB, cb) / 100
        cv.dot((PX(Q_LB), H1 - PY(v)), 6.5, fill=col)
        cv.text_px(PX(Q_LB) + dx, PY(v) + 4, f"{seg}：{v:.{nd}f}", 13, col, anc, weight="700")
    cv.legend(X0 + 20, YB - 60, [(C["bmd"], "Cb = 1.0"), (C["compr"], f"Cb = {Q_CB_AB:.2f}（≤ φMp）")], size=12, gap=19)
    xt = 670
    rows = [(f"Mcr（Cb = 1）= {Q_MCR:,.0f} t·cm", C["text"], "400"),
            (f"直接公式驗算 {Q_MCR2:,.0f} ✓", C["muted"], "400"),
            ("", C["text"], "400"),
            ("各段需求 18w：", C["text"], "400"),
            (f"BC：w = {Q_PHIMN['BC']:.2f} / 18 = {Q_PHIMN['BC'] / 18:.2f} ← 控制", C["load"], "700"),
            (f"AB、CD：{Q_PHIMN['AB']:.1f} / 18 = {Q_PHIMN['AB'] / 18:.2f}", C["compr"], "400"),
            ("", C["text"], "400"),
            (f"可承受 w = {Q_WCR:.2f} t/m（設計值）", C["bmd"], "700")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-curve.svg")
    compose([cv], cols=1,
            title=f"圖 2　Lb = 600 cm 剛超過 Lr = {Q_LR:.0f} cm：BC 段 φbMn = {Q_PHIMN['BC']:.2f} t·m，w = {Q_WCR:.2f} t/m",
            sub="三段需求彎矩都是 18w，比的是各段強度；BC 段 Cb 最小而控制",
            note="以為 Lb 在 Lp、Lr 之間而用直線內插，會高估強度；Lr 要先算出來再比較",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把「兩側」讀成全跨均佈（BC 也有 w）；側撐只看兩端而以 L 當無支長度；A、D 支承讀反"),
    (fig1_cb, "§4 Step 6",
     "BC 段無載重而忽略；BC 段 Cb 取 1.75；AB 段四分點彎矩算錯"),
    (fig2_curve, "§4 Step 3–5、7",
     "Lb 判成非彈性區而用直線內插；控制段選錯"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
