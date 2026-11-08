#!/usr/bin/env python3
"""
SS-2011-2 兩鋼架之靠桿效應（萊梅厥公式） — 題目附圖重繪腳本

用法：
    python3 gen_SS-2011-2.py [輸出目錄]

重繪依據：題目正本 SS-2011-2-problem.md §4 判讀清單（2026-11-02 已確認）。
只畫考卷給的東西（支承、節點、EI、載重、L、L_b）；不含任何解題結果。
L、L_b 為符號，圖形比例示意。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2011-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2011-2-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
#   #4 B 固接；#5 A 鉸圓（AB 頂與頂梁鉸接）；#6 C、E、G 鉸圓；#7 D、F、H 鉸支
#   #8 靠桿 EI = ∞、兩端鉸；#9 頂梁 EI = ∞；#10 每根柱頂一個 P，柱高皆 L
FRAMES = {"(I)": [("A", "B")] + [("C", "D")],
          "(II)": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H")]}
L_DRAW, LB_DRAW = 1.0, 1.3        # 繪圖比例（L、L_b 為符號）
W, PH = 860, 420


def frame_panel(name, cols):
    n = len(cols)
    span = (n - 1) * LB_DRAW
    sx = min(165, (W - 240) / max(span, 1e-9))
    cv = Canvas(W, PH, sx=sx, ox=(W - span * sx) / 2 + 10, oy=95)
    cv.panel(f"鋼架 {name}", "頂梁 EI = ∞；AB 以外皆為靠桿")
    xs = [k * LB_DRAW for k in range(n)]
    cv.line((0, L_DRAW), (xs[-1], L_DRAW), C["member"], 9, cap="butt")
    cv.math(((xs[-1]) / 2 if n > 2 else xs[-1] / 2, L_DRAW), "EI = ∞", 14, C["text"], dy=-18)
    for k, (top, bot) in enumerate(cols):
        x = xs[k]
        lean = k > 0
        cv.line((x, 0), (x, L_DRAW), C["member"], 7 if lean else 3.6, cap="butt")
        cv.support((x, 0), "pin" if lean else "fixed", 0, size=14 if lean else 20)
        cv.dot((x, L_DRAW), 6.5, fill="#FFFFFF", stroke=C["member"], w=2.6)
        cv.arrow((x, L_DRAW + 0.30), (x, L_DRAW + 0.05), C["load"], 2.8, 10)
        cv.math((x, L_DRAW + 0.30), "P", 15, C["load"], "start", dx=8, weight="700")
        cv.text((x, L_DRAW), top, 14, C["text"], "start", dx=10, dy=16, weight="700")
        cv.text((x, 0), bot, 14, C["text"], "start", dx=12, dy=-12, weight="700")
        cv.math((x, L_DRAW / 2), "EI = ∞" if lean else "EI", 14, C["text"], "start", dx=12)
        if not lean:
            cv.math((x, L_DRAW / 2), "K = ?", 14, C["text"], "end", dx=-12)
        if k:
            cv.dim((xs[k - 1], 0), (x, 0), "L_{b}", off=52, label_off=16)
    cv.dim((0, 0), (0, L_DRAW), "L", off=-66, label_off=-16)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([frame_panel(k, v) for k, v in FRAMES.items()], cols=1,
            title="SS-2011-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #4–#10；只畫考卷所給條件",
            note="B 固接、A 為鉸圓；靠桿 C-D、E-F、G-H 頂端鉸圓、底端鉸支",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2011-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_K0 = 2.0                                   # AB 底固頂鉸、可側移（旗桿柱）  §4 Step 1
Q_N = {k: len(v) for k, v in FRAMES.items()}  # 受 P 的柱數 2、4
Q_KP = {k: Q_K0 * math.sqrt(n) for k, n in Q_N.items()}          # 2√2、4      §4 Step 2–3
Q_PCR = {k: 1 / Q_KP[k] ** 2 for k in Q_N}                        # 每柱 P_cr（π²EI/L² 為單位）
Q_SUM = {k: Q_N[k] * Q_PCR[k] for k in Q_N}                       # 皆 1/4     §4 Step 4
Q_DL = 0.20


def _sway_panel(name, n):
    W1 = 560
    span = (n - 1) * LB_DRAW
    sx = min(150, (W1 - 220) / max(span, 1e-9))
    cv = Canvas(W1, PH + 60, sx=sx, ox=(W1 - span * sx) / 2 - 30, oy=130)
    cv.panel(f"鋼架 {name}：側移 δ，K' = {Q_KP[name]:.2f}", f"{n - 1} 根靠桿各把 P·δ/L 沿側移方向推給梁")
    xs = [k * LB_DRAW for k in range(n)]
    pts = [(Q_DL * (1 - math.cos(math.pi * t / 2)), L_DRAW * t) for t in [i / 40 for i in range(41)]]
    cv.line((0, 0), (0, L_DRAW), C["ghost"], 1.8, dash="6 5")
    cv.poly(pts, C["member"], 3.8)
    cv.support((0, 0), "fixed", 0, size=20)
    for x in xs[1:]:
        cv.line((x, 0), (x, L_DRAW), C["ghost"], 1.8, dash="6 5")
        cv.line((x, 0), (x + Q_DL, L_DRAW), C["member"], 6, cap="butt")
        cv.support((x, 0), "pin", 0, size=13)
    cv.line((Q_DL, L_DRAW), (xs[-1] + Q_DL, L_DRAW), C["member"], 9, cap="butt")
    for x in xs:
        cv.dot((x + Q_DL, L_DRAW), 6, fill="#FFFFFF", stroke=C["member"], w=2.4)
        cv.arrow((x + Q_DL, L_DRAW + 0.30), (x + Q_DL, L_DRAW + 0.05), C["load"], 2.6, 10)
        cv.text((x + Q_DL, L_DRAW + 0.30), "P", 14, C["load"], "start", dx=8, weight="700")
    for x in xs[1:]:
        cv.arrow((x + Q_DL - 0.04, L_DRAW - 0.20), (x + Q_DL + 0.30, L_DRAW - 0.20), C["sfd"], 2.4, 9)
    cv.text((xs[-1] + Q_DL + 0.06, L_DRAW - 0.20), "P·δ/L", 12.5, C["sfd"], "start", dy=20, weight="700")
    cv.text((0, L_DRAW / 2), "AB", 14, C["text"], "end", dx=-12, weight="700")
    cv.text_px(W1 / 2, PH + 60 - 52, f"AB 須抵抗 {n}·P·δ/L（含自身）", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, PH + 60 - 28, f"K' = 2 × √{n} = {Q_KP[name]:.2f}", 13, C["bmd"], weight="700")
    return cv


def fig1_sway():
    path = os.path.join(OUT, f"{TAG}-fig-1-sway.svg")
    compose([_sway_panel(k, n) for k, n in Q_N.items()], cols=2,
            title="圖 1　只有 AB 抗側：靠桿愈多，AB 要扛的 P–Δ 愈大",
            sub="AB 底固、頂與梁鉸接 ⇒ 單獨時是懸臂（旗桿）柱，K0 = 2.0",
            note="靠桿 CD、EF、GH 兩端鉸接，自身零側向勁度：載重計入 ΣP，但不計入 ΣPeK",
            path=path)
    return path


def fig2_sum():
    W1, H1 = 1000, 470
    cv = Canvas(W1, H1, sx=1)
    cv.panel("系統總挫屈載重 ΣPcr（單位 π²EI/L²）", "每根柱臨界 P 相同；長條每格 = 一根柱的 Pcr")
    x0, sc = 230, 2400
    rows = list(Q_N.items())
    for i, (k, n) in enumerate(rows):
        y = 150 + i * 110
        cv.text_px(x0 - 14, y, f"鋼架 {k}", 15, C["text"], "end", weight="700")
        for j in range(n):
            col = C["bmd"] if j == 0 else C["ghost"]
            cv.rect_px(x0 + j * sc * Q_PCR[k], y - 20, sc * Q_PCR[k] - 3, 40, col, 3)
            lab = "AB" if j == 0 else "靠桿"
            cv.text_px(x0 + (j + 0.5) * sc * Q_PCR[k], y, lab, 12, "#FFFFFF" if j == 0 else C["text"], weight="700")
        cv.text_px(x0 + sc * Q_SUM[k] + 12, y - 9, f"= {n} × 1/{1 / Q_PCR[k]:.0f} = 1/{1 / Q_SUM[k]:.0f}", 14, C["bmd"], "start", weight="700")
        cv.text_px(x0 + sc * Q_SUM[k] + 12, y + 13, f"每柱 Pcr = π²EI/({Q_KP[k]:.2f}L)²", 12, C["muted"], "start")
    xe = x0 + sc * 0.25
    _hl(cv, H1, xe, 110, xe, 340, C["accent"], 1.6, dash="5 4")
    cv.text_px(xe, 360, "AB 單獨 π²EI/(2L)² = 1/4", 12.5, C["accent"], weight="700")
    cv.text_px(W1 / 2, H1 - 50, f"ΣP(I)cr / ΣP(II)cr = {Q_SUM['(I)'] / Q_SUM['(II)']:.0f}", 16, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 24, "系統能扛的總重 = AB 的旗桿柱挫屈載重，與靠桿數無關", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-sum.svg")
    compose([cv], cols=1,
            title="圖 2　兩鋼架總挫屈載重相同：比值 = 1",
            sub="靠桿只把總重分散到更多柱上，每根柱分到的 Pcr 隨之變小",
            note="把靠桿也算進 ΣPeK、或以為靠桿愈多系統愈弱（比值 ≠ 1），都是錯的",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "B 讀成鉸支或 A 讀成剛接（AB 自身 K 判錯）；把 EI = ∞ 的靠桿當成有側向勁度"),
    (fig1_sway, "§4 Step 1–3",
     "AB 頂端當固接（K0 取 1）；靠桿計入 ΣPeK；漏算靠桿載重"),
    (fig2_sum, "§4 Step 4",
     "以為靠桿愈多系統總強度愈小；每柱 Pcr 與 ΣPcr 混淆"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
