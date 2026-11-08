#!/usr/bin/env python3
"""
SS-2002-2 A36 簡支梁 W12×65 移動集中載重之容許 P（ASD）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2002-2.py [輸出目錄]

重繪依據：題目正本 SS-2002-2-problem.md §4 判讀清單（待確認）。
圖上每個支承、側撐、載重都對應清單一項；只畫考卷給的東西，不含任何解題結果。
示意部分：P 的位置（移動載重，畫在跨中只是示意）、梁立面高度與載重箭頭長度；
斷面依 W12×65 題給尺寸（d、bf、tf、tw）按比例繪製。
不重繪：無（本題附圖只有梁立面與斷面座標）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2002-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2002-2-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
SPAN = 14.0                 # 題文／附圖 跨長 14 m
LEFT, RIGHT = "pin", "roller"   # #1 左端鉸支、右端滾支
BRACE_N = 4                 # #3 兩端及每 1/4 跨設弱軸側撐
P_AT = 0.5                  # #4 P 為移動載重；跨中位置僅為示意
SW = "97 kg/m"              # #5 自重全跨均佈
#                             #2 工字形直立，繞強軸 x 彎曲
D, BF, TF, TW = 30.3, 30.0, 1.5, 1.0    # 題文 W12×65：d、bf、tf、tw（cm）

PW, PH = 560, 400
SW_, SH_ = PW, PH


def _rect(cv, x0, x1, y0, y1):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.8)


def beam_panel():
    sx = (PW - 140) / SPAN
    cv = Canvas(PW, PH, sx=sx, ox=70, oy=150)
    cv.panel("梁立面", "左端鉸支、右端滾支；P 位置可移動（示意）")
    cv.line((0, 0), (SPAN, 0), C["member"], 5, cap="butt")
    cv.support((0, 0), LEFT, 0, size=15)
    cv.support((SPAN, 0), RIGHT, 0, size=15)
    # #5 自重（全跨均佈）
    cv.udl((0, 0), (SPAN, 0), 0.9, n=12, color=C["load"], w=1.4)
    cv.text((SPAN, 0.9), f"自重 {SW}（全跨）", 12.5, C["load"], "end", dy=-12)
    # #4 移動集中載重 P
    xp = P_AT * SPAN
    cv.arrow((xp, 3.3), (xp, 0.95), C["load"], 3.0, 11)
    cv.math((xp, 3.3), "P", 17, C["load"], dy=-12, weight="700")
    cv.double_arrow((xp - 1.6, 3.0), (xp + 1.6, 3.0), C["muted"], 1.6, 8)
    cv.text((xp + 1.9, 3.0), "移動", 12.5, C["muted"], "start")
    # #3 側撐：兩端及每 1/4 跨
    for k in range(BRACE_N + 1):
        x = SPAN * k / BRACE_N
        cv.text((x, 0), "×", 20, C["accent"], weight="700", dy=-1)
    cv.text_px(PW / 2, 88, "× 弱軸方向側向支撐：兩端及每 1/4 跨", 12.5, C["accent"])
    cv.line((SPAN * 0.80, -0.15), (SPAN * 0.86, -1.6), C["muted"], 1.2)
    cv.text((SPAN * 0.86, -1.6), "W12×65", 13, C["text"], "start", dx=4, dy=4)
    cv.dim((0, 0), (SPAN, 0), f"{SPAN:.0f} m", off=80, label_off=16)
    return cv


def section_panel():
    sx = 6.0
    cv = Canvas(SW_, SH_, sx=sx, ox=SW_ / 2 - 10, oy=60)
    cv.panel("斷面座標", "W12×65 依比例")
    _rect(cv, -BF / 2, BF / 2, D - TF, D)
    _rect(cv, -BF / 2, BF / 2, 0, TF)
    _rect(cv, -TW / 2, TW / 2, TF, D - TF)
    yc = D / 2
    cv.arrow((0, yc), (0, D + 9), C["text"], 1.6, 9)
    cv.arrow((0, yc), (BF / 2 + 9, yc), C["text"], 1.6, 9)
    cv.math((0, D + 9), "y", 16, C["text"], dy=-12, weight="700")
    cv.math((BF / 2 + 9, yc), "x", 16, C["text"], "start", dx=6, weight="700")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([beam_panel(), section_panel()], cols=2,
            title="SS-2002-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#5；只畫考卷所給條件（跨長、自重、側撐取自題文）",
            note="P 是移動載重，圖上位置只是示意；側撐在兩端與每 1/4 跨，不是只在兩端",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2002-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
Q_FY, Q_SX = 2.5, 1373.0                 # t/cm²、cm³（題文）
Q_LC, Q_LU = 3.87, 8.44                  # m（題文）
Q_W = 0.097                              # t/m 自重
Q_LB = SPAN / BRACE_N                    # 3.5
Q_FB = 0.66 * Q_FY if Q_LB <= Q_LC else 0.60 * Q_FY
Q_MA = round(Q_FB * Q_SX / 100 + 1e-9, 3)   # t·m 22.655（四捨五入，與解析同）
Q_MSW = round(Q_W * SPAN ** 2 / 8 + 1e-9, 3)   # 2.377
Q_MAV = Q_MA - Q_MSW                     # 20.278
Q_PA = Q_MAV / (SPAN / 4)                # 5.79
Q_VMAX = Q_PA + Q_W * SPAN / 2
Q_VA = 0.4 * Q_FY * D * TW


def fig1_lb():
    W1, H1 = 1000, 280
    cv = Canvas(W1, H1, sx=56, ox=110, oy=100)
    cv.panel("梁立面：側撐每 1/4 跨，Lb = 14 / 4 = 3.5 m", "移動載重 P 在跨中時恰落在側撐點，不改變 Lb")
    cv.line((0, 0), (SPAN, 0), C["member"], 6, cap="butt")
    cv.support((0, 0), "pin", 0, size=14)
    cv.support((SPAN, 0), "roller", 0, size=14)
    for k in range(BRACE_N + 1):
        x = SPAN * k / BRACE_N
        cv.line((x, -0.45), (x, 0.45), C["accent"], 2.4, cap="butt")
        cv.text((x, 0.45), f"{x:g}", 11.5, C["accent"], dy=-10)
    cv.arrow((SPAN / 2 + 0.25, 1.15), (SPAN / 2 + 0.25, 0.15), C["load"], 3, 10)
    cv.text((SPAN / 2 + 0.25, 1.0), "P（移動）", 13, C["load"], "start", dx=8, weight="700")
    p1 = cv
    cv = Canvas(W1, 280, sx=1)
    cv.panel("ASD 容許撓曲應力分區（Lb 對 Lc、Lu）", "結實斷面：Lb ≤ Lc → 0.66Fy；Lc 到 Lu → 0.60Fy；大於 Lu → LTB 公式")
    X0, X1, Y = 120, 880, 160
    lmax = 10.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    for a, b, lab, col in ((0, Q_LC, "0.66Fy", "rgba(46,125,50,0.25)"), (Q_LC, Q_LU, "0.60Fy", "rgba(46,125,50,0.12)"),
                           (Q_LU, lmax, "LTB 式", "rgba(192,57,43,0.12)")):
        cv.rect_px(PX(a), Y - 26, PX(b) - PX(a), 52, col, 0)
        cv.text_px((PX(a) + PX(b)) / 2, Y - 40, lab, 13, C["bmd"] if "Fy" in lab else C["load"], weight="700")
    _hl(cv, 280, X0, Y + 26, X1, Y + 26, C["muted"], 1.5)
    for v, lab in ((0, "0"), (Q_LC, f"Lc = {Q_LC}"), (Q_LU, f"Lu = {Q_LU}"), (lmax, "10 m")):
        cv.text_px(PX(v), Y + 46, lab, 12, C["muted"])
    _hl(cv, 280, PX(Q_LB), Y - 30, PX(Q_LB), Y + 30, C["load"], 3)
    cv.text_px(PX(Q_LB) - 8, Y + 2, f"Lb = {Q_LB:g}", 13, C["load"], "end", weight="700")
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-lb.svg")
    compose([p1, p2], cols=1,
            title=f"圖 1　Lb = {Q_LB:g} m 小於 Lc = {Q_LC} m：Fb = 0.66Fy = {Q_FB:.2f} tf/cm²",
            sub="題目已給 Lc、Lu，直接比較即可，不必再算",
            note="把 Lb 取全跨 14 m（大於 Lu）會改用 LTB 公式，容許彎矩大幅下降",
            path=path)
    return path


def fig2_moment():
    W1, H1 = 1000, 520
    cv = Canvas(W1, H1, sx=1)
    cv.panel(f"P = {Q_PA:.2f} tf 在跨中時的彎矩圖（tf·m）", "自重拋物線 wL²/8 ＋ 集中載重三角形 PL/4，跨中合計 = Ma")
    X0, X1, YB, YT = 100, 600, 420, 120
    mmax = 24.0
    PX = lambda x: X0 + (X1 - X0) * x / SPAN
    PY = lambda m: YB - (YB - YT) * m / mmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    for v in range(0, 25, 6):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    for x in (0, 3.5, 7, 10.5, 14):
        cv.text_px(PX(x), YB + 18, f"{x:g}", 11.5, C["muted"])
    xs = [SPAN * i / 100 for i in range(101)]
    msw = lambda x: Q_W * x * (SPAN - x) / 2
    mp = lambda x: Q_PA * min(x, SPAN - x) / 2
    cv.polygon([(PX(0), H1 - PY(0))] + [(PX(x), H1 - PY(msw(x) + mp(x))) for x in xs] + [(PX(SPAN), H1 - PY(0))], C["fill_m"], C["bmd"], 2.4)
    cv.poly([(PX(x), H1 - PY(mp(x))) for x in xs], C["load"], 1.8, dash="6 4")
    cv.poly([(PX(x), H1 - PY(msw(x))) for x in xs], C["compr"], 1.8, dash="6 4")
    _hl(cv, H1, X0, PY(Q_MA), X1, PY(Q_MA), C["accent"], 1.4, dash="5 4")
    cv.text_px(X1, PY(Q_MA) - 10, f"Ma = {Q_MA:.3f}", 12, C["accent"], "end", weight="700")
    cv.text_px(PX(4.2), PY(mp(4.2)) + 26, "P 的三角形", 12, C["load"], "start")
    cv.text_px(PX(7), PY(msw(7)) - 12, "自重拋物線", 12, C["compr"])
    xt, x0 = 650, 650
    sc = 12.0
    y = 200
    cv.text_px(xt, 150, "跨中彎矩預算", 13, C["text"], "start", weight="700")
    cv.rect_px(x0, y - 16, sc * Q_MSW, 32, C["compr"], 2)
    cv.rect_px(x0 + sc * Q_MSW, y - 16, sc * Q_MAV, 32, C["load"], 2)
    cv.text_px(x0 + sc * Q_MSW / 2, y + 32, f"{Q_MSW:.3f}", 11.5, C["compr"])
    cv.text_px(x0 + sc * Q_MSW + sc * Q_MAV / 2, y, f"{Q_MAV:.3f}", 12, "#FFFFFF", weight="700")
    rows = [(f"Ma = {Q_FB:.2f} × {Q_SX:g} = {Q_MA:.3f} tf·m", C["text"], "400"),
            (f"自重 0.097 × 14² / 8 = {Q_MSW:.3f}", C["compr"], "400"),
            (f"3.5P ≤ {Q_MAV:.3f}", C["load"], "400"),
            (f"Pa = {Q_MAV:.3f} / 3.5 = {Q_PA:.2f} tf", C["bmd"], "700"),
            (f"剪力 {Q_VMAX:.2f} ≤ {Q_VA:.1f} tf ✓", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        cv.text_px(xt, 270 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-moment.svg")
    compose([cv], cols=1,
            title=f"圖 2　跨中 3.5P + {Q_MSW:.3f} ≤ {Q_MA:.3f} ⇒ Pa = {Q_PA:.2f} tf",
            sub="移動集中載重在跨中時跨中彎矩最大：PL/4 = 3.5P",
            note="忘了扣自重彎矩、或把自重也乘 L/4，都會算錯 Pa",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把移動載重固定在圖上位置；漏看每 1/4 跨側撐而以全跨 14 m 當無支長度；兩端支承讀反"),
    (fig1_lb, "§4 步驟 1–2",
     "Lb 取全跨 14 m；Lb 與 Lc、Lu 比錯而用 0.60Fy 或 LTB 式"),
    (fig2_moment, "§4 步驟 3–6",
     "忘了扣自重彎矩；P 的最不利位置不在跨中"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
