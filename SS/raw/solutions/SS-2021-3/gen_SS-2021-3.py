#!/usr/bin/env python3
"""
SS-2021-3 耐震固接－滾支鋼梁之選斷面與塑性極限強度 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2021-3.py [輸出目錄]

重繪依據：題目正本 SS-2021-3-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西；表一已照錄於題目正本 §2，不重繪。跨度依比例、載重高度示意。單位 cm。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2021-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2021-3-problem.md §4，已確認）；單位 cm
# ══════════════════════════════════════════════════════════
SEG = [600.0, 600.0]      # #3 跨度 600 + 600 = 1200 cm；#4 中間黑點只是尺寸線分段點
SPAN = sum(SEG)
#                           #1 A 固接（與鋼柱彎矩接合）；#2 B 滾支；#5 側撐只在 A、B；#6 均布 w 滿跨


def fig1_problem():
    W, H, sx = 760, 400, 0.5
    cv = Canvas(W, H, sx=sx, ox=(W - SPAN * sx) / 2, oy=190)
    cv.panel("圖三", "A 固接、B 滾支；側向支撐只在 A、B")
    cv.line((0, 0), (SPAN, 0), C["member"], 5, cap="butt")
    cv.support((0, 0), "fixed", -90, size=30)
    cv.support((SPAN, 0), "roller", 0, size=15)
    cv.udl((0, 0), (SPAN, 0), 90, n=15, label="w")
    cv.text((0, 0), "A", 16, C["text"], dx=-14, dy=-34, weight="700")
    cv.text((SPAN, 0), "B", 16, C["text"], dx=20, dy=-34, weight="700")
    x = 0.0
    for s in SEG:
        cv.dim((x, 0), (x + s, 0), f"{s:g} cm", off=78, label_off=16)
        x += s
    cv.dot((SEG[0], 0), 4, fill=C["dim"], stroke=C["dim"], w=1)
    cv.text((SEG[0], 0), "（尺寸分段點，非支承、非側撐）", 12, C["muted"], dy=112)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title="SS-2021-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#6；表一已照錄於題目正本 §2",
            note="跨度 1200 cm；跨中黑點只是尺寸線分段點，未支撐長度 L_b = 1200 cm",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2021-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_FR = 3.5, 1.16                       # tf/cm²
Q_ZX, Q_SX, Q_RY, Q_X1, Q_X2 = 6330.0, 5670.0, 7.03, 144.0, 1.82   # BH700×300×12×25（題給表）
Q_MP = Q_FY * Q_ZX                           # 22,155 tf·cm
Q_FL = Q_FY - Q_FR
Q_MR = Q_FL * Q_SX
Q_LP = 80 * Q_RY / math.sqrt(Q_FY)           # 300.6
Q_LR = Q_RY * Q_X1 / Q_FL * math.sqrt(1 + math.sqrt(1 + Q_X2 * Q_FL ** 2))   # 898
mn = lambda lb, cb: q_mn_lrfd(max(lb, 1e-6), cb, Q_MP, Q_MR, Q_LP, Q_LR, Q_SX, Q_X1, Q_X2, Q_RY)
Q_LB0, Q_LB1 = SPAN, 300.0
Q_X = (math.sqrt(2) - 1)                     # 跨內鉸距簡支端 0.414L
Q_WU = 2 * Q_MP / 100 / (Q_X * SPAN / 100) ** 2   # 17.9 t/m


def fig1_ltb():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("BH700×300×12×25：Mn 對 Lb（t·m）", f"Lp = {Q_LP:.1f} cm、Lr = {Q_LR:.0f} cm；Mp = {Q_MP / 100:.1f}、Mr = FL·Sx = {Q_MR / 100:.1f}")
    X0, X1, YB, YT = 100, 640, 450, 110
    lmax, mmax = 1300.0, 240.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda m: YB - (YB - YT) * m / mmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 1301, 300):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for v in range(0, 241, 60):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "Lb（cm）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Mn（t·m）", 13, C["text"], "start", weight="700")
    ls = [lmax * i / 400 for i in range(0, 401)]
    cv.poly([(PX(l), H1 - PY(mn(l, 1.75) / 100)) for l in ls], C["compr"], 2.2, dash="7 4")
    cv.poly([(PX(l), H1 - PY(mn(l, 1.0) / 100)) for l in ls], C["bmd"], 2.8)
    for l, lab in ((Q_LP, "Lp"), (Q_LR, "Lr")):
        _hl(cv, H1, PX(l), YB, PX(l), YT, C["accent"], 1.1, dash="4 4")
        cv.text_px(PX(l) + 4, YT + 6, f"{lab} = {l:.0f}", 11.5, C["accent"], "start")
    for lb, cb, col, lab, dx, dy, anc in ((Q_LB0, 1.0, C["load"], "Lb = 1200、Cb = 1", -12, -14, "end"), (Q_LB0, 1.75, C["compr"], "Cb = 1.75", -12, -14, "end"),
                                         (Q_LB1, 1.0, C["bmd"], "加側撐 Lb = 300", -10, -16, "end")):
        v = mn(lb, cb) / 100
        cv.dot((PX(lb), H1 - PY(v)), 6.5, fill=col)
        cv.text_px(PX(lb) + dx, PY(v) + dy, f"{lab}：{v:.1f}", 12.5, col, anc, weight="700")
    cv.legend(X0 + 20, YB - 60, [(C["bmd"], "Cb = 1.0（保守）"), (C["compr"], "Cb = 1.75（上限 Mp）")], size=12, gap=19)
    xt = 680
    rows = [(f"Lb = 1200 大於 Lr = {Q_LR:.0f}", C["text"], "400"),
            ("⇒ 彈性 LTB", C["text"], "400"),
            (f"Mn = {mn(Q_LB0, 1) / 100:.1f}～{mn(Q_LB0, 1.75) / 100:.1f} t·m", C["load"], "700"),
            (f"均小於 Mp = {Q_MP / 100:.1f}：無法塑性", C["load"], "700"),
            ("", C["text"], "400"),
            ("每 300 cm 加一處側撐（3 處）", C["bmd"], "700"),
            (f"Lb = 300 ≤ Lp = {Q_LP:.1f} ⇒ Mn = Mp", C["bmd"], "700"),
            ("耐震上限 170ry/√Fy = 639 cm 不控制", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-ltb.svg")
    compose([cv], cols=1,
            title=f"圖 1　只在兩端側撐時 Mn 最多 {mn(Q_LB0, 1.75) / 100:.1f} t·m 小於 Mp；每 3 m 加側撐後 Lb ≤ Lp，可發揮 Mp = {Q_MP / 100:.1f} t·m",
            sub="考卷的 1.75 式只適用線性彎矩圖；本題拋物線彎矩圖保守取 Cb = 1.0",
            note="即使取 Cb = 1.75 仍不到 Mp：不加側撐就談塑性極限強度是錯的",
            path=path)
    return path


def fig2_mech():
    W1, H1 = 1000, 470
    L = SPAN / 100
    cv = Canvas(W1, H1, sx=62, ox=150, oy=230)
    cv.panel("加側撐後的塑性崩塌機構（固端 A、簡支 B、滿跨均布）", f"跨內塑性鉸距 B 端 (√2 − 1)L = {Q_X * L:.2f} m（距 A {L - Q_X * L:.2f} m）")
    cv.line((0, 0), (L, 0), C["ghost"], 2, dash="6 5")
    xh = L - Q_X * L
    dh = 1.6
    cv.poly([(0, 0), (xh, -dh), (L, 0)], C["member"], 4.5)
    cv.support((0, 0), "fixed", 90, size=24)
    cv.support((L, 0), "roller", 0, size=14)
    cv.udl((0, 1.2), (L, 1.2), 0.8, n=13, color=C["load"], w=1.6)
    cv.text((L / 2, 2.35), f"wu = 2Mp / (0.414L)² = {Q_WU:.1f} t/m", 13.5, C["load"], weight="700")
    for x, lab in ((0, "塑性鉸 A（固端，−Mp）"), (xh, "塑性鉸（+Mp）")):
        cv.dot((x, -dh if x else 0), 8, fill="#FFFFFF", stroke=C["load"], w=2.6)
        cv.text((x, -dh if x else 0), lab, 12.5, C["load"], "start" if x == 0 else "middle", dx=16 if x == 0 else 0, dy=26 if x else -16, weight="700")
    for k in (1, 2, 3):
        cv.line((3 * k, 0.25), (3 * k, -0.25), C["accent"], 3, cap="butt")
        cv.text((3 * k, 0.25), f"側撐 {3 * k} m", 11, C["accent"], dy=-10)
    cv.dim((xh, -dh - 0.9), (L, -dh - 0.9), f"0.414L = {Q_X * L:.2f} m", off=0, label_off=16)
    path = os.path.join(OUT, f"{TAG}-fig-2-mech.svg")
    compose([cv], cols=1,
            title=f"圖 2　塑性極限強度 wu = 11.66Mp/L² = {Q_WU:.1f} t/m（φ 後 {0.9 * Q_WU:.1f}）",
            sub="跨內塑性鉸落在 6～9 m 側撐段內，兩側都有側撐",
            note="跨內鉸若取跨中、或漏了固端鉸，崩塌載重都會算錯；虛功法對鉸位置求極小，得距簡支端 0.414L",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把跨中黑點當成側撐（L_b 誤取 600 cm）；B 端讀成鉸支或固接"),
    (fig1_ltb, "§4 Step 4–5",
     "不加側撐就用 Mp；Cb 直接取 1.75；側撐間距只看耐震上限"),
    (fig2_mech, "§4 Step 6",
     "跨內塑性鉸取跨中；固端鉸漏算"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
