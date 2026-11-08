#!/usr/bin/env python3
"""
SS-2024-3 RH488×300×11×18 外伸梁強軸／弱軸受集中載重之 LRFD 檢核 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2024-3.py [輸出目錄]

重繪依據：題目正本 SS-2024-3-problem.md §4 判讀清單（待確認）。
圖上每個支承、側撐、載重都對應清單一項；只畫考卷給的東西，不含任何解題結果（不畫彎矩圖、不標 Cb）。
梁跨度與梁深依比例（mm：3 m＋3 m；圖(a) 梁深 488、圖(b) 梁深 300）；左側斷面小圖依比例放大表方位。
示意部分：載重箭頭長度、支承符號大小；C 處豎線照考卷附圖照描（圖(a) 實線、圖(b) 虛線），清單未判讀其意義。
不重繪：題內參考公式（圖片，已照錄於 problem.md §2）。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2024-3"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2024-3-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
X_A, X_C, X_B = 0.0, 3000.0, 6000.0    # #1 A 鉸支、C 滾支（距 A 3 m）、B 外伸自由端（距 C 3 m）
LOAD = "DL=5tf　LL=5tf"                # #1 集中載重在 B（題文 DL = LL = 5 tf）
BRACES = (X_A, X_B)                    # #2 「×」側向及扭轉支撐只在 A、B（上下翼板）；C 無面外束制
D, BF, TW, TF = 488.0, 300.0, 11.0, 18.0   # 題文 RH488×300×11×18（mm）
#                                        #3 圖(a) 強軸（腹板垂直）、圖(b) 弱軸（腹板水平）

PW, PH = 900, 290


def _rect(cv, x0, x1, y0, y1, fill, stroke, w=1.4):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, stroke, w)


def _icon(cv, cx, cy, k, strong):
    """左側斷面方位小圖（model 單位 mm；k = 放大倍數）"""
    if strong:
        parts = ((-BF / 2, BF / 2, D / 2 - TF, D / 2), (-BF / 2, BF / 2, -D / 2, -D / 2 + TF),
                 (-TW / 2, TW / 2, -D / 2 + TF, D / 2 - TF))
    else:   # 腹板水平：翼板直立
        parts = ((D / 2 - TF, D / 2, -BF / 2, BF / 2), (-D / 2, -D / 2 + TF, -BF / 2, BF / 2),
                 (-D / 2 + TF, D / 2 - TF, -TW / 2, TW / 2))
    for xa, xb, ya, yb in parts:
        _rect(cv, cx + xa * k, cx + xb * k, cy + ya * k, cy + yb * k, C["fill_c"], C["member"], 1.2)
    half = (D / 2 if not strong else BF / 2) * k + 120
    cv.line((cx - half, cy), (cx + half, cy), C["muted"], 1.0, dash="8 3 2 3")


def _x(cv, p):
    cv.text(p, "×", 22, C["accent"], weight="700", dy=-1)


def beam_panel(strong):
    sx = 0.092
    cv = Canvas(PW, PH, sx=sx, ox=300, oy=110)
    tag = "圖(a)" if strong else "圖(b)"
    cv.panel(f"{tag}　{'強軸受彎（腹板垂直）' if strong else '弱軸受彎（腹板水平）'}",
             "A 鉸支、C 滾支、B 外伸自由端；支承與載重兩圖相同")
    h = D if strong else BF
    # 梁外形
    _rect(cv, X_A, X_B, 0, h, "none", C["member"], 2.2)
    if strong:
        cv.line((X_A, TF), (X_B, TF), C["member"], 1.0)
        cv.line((X_A, h - TF), (X_B, h - TF), C["member"], 1.0)
        cv.line((X_C, TF), (X_C, h - TF), C["member"], 1.6)
    else:
        for y in (h / 2 - TW / 2, h / 2 + TW / 2):
            cv.line((X_A, y), (X_B, y), C["member"], 1.2, dash="7 4")
        cv.line((X_C, 0), (X_C, h), C["member"], 1.2, dash="5 4")
    # 支承
    cv.support((X_A, 0), "pin", 0, size=14)
    cv.support((X_C, 0), "roller", 0, size=14)
    # 側向及扭轉支撐（A、B 上下翼板）
    for x in BRACES:
        _x(cv, (x, 0)); _x(cv, (x, h))
    # 載重（B 端）
    cv.arrow((X_B, h + 760), (X_B, h + 60), C["load"], 4.0, 13)
    cv.text((X_B, h + 760), "集中載重", 13, C["load"], "end", dx=-12, dy=4)
    cv.text((X_B, h + 760), LOAD, 13, C["load"], "end", dx=-12, dy=22)
    # 點名
    cv.text((X_A, h), "A", 15, C["text"], "end", dx=-12, dy=-14, weight="700")
    cv.text((X_C, h), "C", 15, C["text"], dy=-16, weight="700")
    cv.text((X_B, h), "B", 15, C["text"], "start", dx=12, dy=-14, weight="700")
    # 尺寸
    cv.dim((X_A, 0), (X_C, 0), f"{(X_C - X_A) / 1000:.0f} m", off=52, label_off=14)
    cv.dim((X_C, 0), (X_B, 0), f"{(X_B - X_C) / 1000:.0f} m", off=52, label_off=14)
    # 左側斷面方位
    _icon(cv, -1700, h / 2, 1.4, strong)
    cv.text_px(cv.X(-1700), cv.Y(h / 2) + 52, "RH488×300×11×18", 12, C["muted"])
    if strong:
        cv.text_px(30, 92, "× 側向及扭轉支撐點", 13, C["accent"], "start")
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([beam_panel(True), beam_panel(False)], cols=1,
            title="SS-2024-3 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#3；只畫考卷所給條件",
            note="× 只在 A、B：C 雖為滾支承，但無面外束制，不是側撐點",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2024-3.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_FY, Q_E, Q_G = 2.35, 2040.0, 810.0          # tf/cm²（解析所取 E、G）
Q_FL = Q_FY - 0.7
Q_H, Q_B, Q_TW, Q_TF = D / 10, BF / 10, TW / 10, TF / 10
Q_HW = Q_H - 2 * Q_TF
Q_A = 2 * Q_B * Q_TF + Q_HW * Q_TW
Q_IX = 2 * (Q_B * Q_TF ** 3 / 12 + Q_B * Q_TF * ((Q_H - Q_TF) / 2) ** 2) + Q_TW * Q_HW ** 3 / 12
Q_SX = Q_IX / (Q_H / 2)
Q_IY = 2 * Q_TF * Q_B ** 3 / 12 + Q_HW * Q_TW ** 3 / 12
Q_RY = math.sqrt(Q_IY / Q_A)
Q_SY = Q_IY / (Q_B / 2)
Q_J = (2 * Q_B * Q_TF ** 3 + (Q_H - Q_TF) * Q_TW ** 3) / 3
Q_CW = Q_IY * (Q_H - Q_TF) ** 2 / 4
Q_ZX = 2 * (Q_B * Q_TF * (Q_H - Q_TF) / 2 + Q_TW * Q_HW ** 2 / 8)
Q_ZY = 2 * Q_TF * Q_B ** 2 / 4 + Q_HW * Q_TW ** 2 / 4
Q_X1 = math.pi / Q_SX * math.sqrt(Q_E * Q_G * Q_J * Q_A / 2)
Q_X2 = 4 * Q_CW / Q_IY * (Q_SX / (Q_G * Q_J)) ** 2
Q_LP = 80 * Q_RY / math.sqrt(Q_FY)
Q_LR = Q_RY * Q_X1 / Q_FL * math.sqrt(1 + math.sqrt(1 + Q_X2 * Q_FL ** 2))
Q_PU = 1.2 * 5 + 1.6 * 5                       # 14 tf
Q_LBM = (X_B - X_A) / 1000                     # 6 m
Q_MW = lambda x: -Q_PU * x if x <= 3 else -Q_PU * (6 - x)   # t·m（A 反力向下）
Q_MU = abs(Q_MW(3))
Q_CB = 12.5 * Q_MU / (2.5 * Q_MU + 3 * abs(Q_MW(1.5)) + 4 * abs(Q_MW(3)) + 3 * abs(Q_MW(4.5)))
Q_MP = Q_FY * Q_ZX
Q_MR = Q_FL * Q_SX
Q_LB = Q_LBM * 100
Q_MNX = min(Q_CB * (Q_MP - (Q_MP - Q_MR) * (Q_LB - Q_LP) / (Q_LR - Q_LP)), Q_MP)
Q_MNX1 = Q_MP - (Q_MP - Q_MR) * (Q_LB - Q_LP) / (Q_LR - Q_LP)
Q_MNY = min(Q_FY * Q_ZY, 1.5 * Q_FY * Q_SY)


def fig1_moment():
    W1, H1 = 1000, 500
    cv = Canvas(W1, H1, sx=120, ox=180, oy=290)
    cv.panel(f"外伸梁彎矩圖（Pu = 1.2 × 5 + 1.6 × 5 = {Q_PU:g} tf）", "A 反力向下 14 tf、C 反力向上 28 tf；全梁負彎矩，C 點 −42 t·m")
    cv.line((0, 0), (6, 0), C["member"], 5, cap="butt")
    cv.support((0, 0), "pin", 0, size=13)
    cv.support((3, 0), "roller", 0, size=13)
    cv.arrow((6, 1.05), (6, 0.08), C["load"], 3, 10)
    cv.text((6, 1.05), f"Pu = {Q_PU:g}", 13, C["load"], "start", dx=8, weight="700")
    for x, n in ((0, "A"), (3, "C"), (6, "B")):
        cv.text((x, 0), n, 14, C["text"], dy=36 if x != 6 else -14, dx=18 if x == 6 else 0, weight="700")
    for x in (0, 6):
        cv.text((x, 0.42), "×", 18, C["accent"], weight="700")
    cv.text((3, 0.55), "C 無面外束制", 12, C["muted"])
    sc = 0.02
    xs = [6 * i / 120 for i in range(121)]
    yb = -0.8
    cv.polygon([(0, yb)] + [(x, yb + Q_MW(x) * sc) for x in xs] + [(6, yb)], C["fill_m"], C["bmd"], 2.2)
    for x in (1.5, 3, 4.5):
        cv.line((x, yb), (x, yb + Q_MW(x) * sc), C["bmd"], 1, dash="3 3")
        cv.text((x, yb + Q_MW(x) * sc), f"{Q_MW(x):g}".replace("-", "−"), 12, C["bmd"], dy=16, weight="700")
    cv.dim((0, yb + 0.25), (6, yb + 0.25), f"Lb = {Q_LBM:g} m", off=0, label_off=-12)
    cv.text_px(W1 - 40, H1 - 60, "負彎矩：上翼板受拉、", 12.5, C["muted"], "end")
    cv.text_px(W1 - 40, H1 - 36, "下翼板受壓而側向挫屈", 12.5, C["muted"], "end")
    path = os.path.join(OUT, f"{TAG}-fig-1-moment.svg")
    compose([cv], cols=1,
            title=f"圖 1　Lb = 6 m（只有 A、B 側撐），四分點取絕對值 21、42、21：Cb = {Q_CB:.3f}",
            sub=f"Cb = 12.5 × 42 / (2.5 × 42 + 3 × 21 + 4 × 42 + 3 × 21) = {Q_CB:.3f}；式中 MA、MB、MC 是無支撐段的 1/4、1/2、3/4 點，不是圖上的 A、B、C 點",
            note="把 C 當側撐點（Lb 取 3 m）、或把 Cb 式的 MA／MC 代成支點彎矩 0，都會算錯",
            path=path)
    return path


def fig2_axes():
    W1, H1 = 1000, 480
    cv = Canvas(W1, H1, sx=1)
    cv.panel("同一斷面、同一支承與載重：強軸 vs 弱軸（t·m）", f"Lp = {Q_LP:.0f}、Lr = {Q_LR:,.0f} cm；Mp = {Q_MP:,.0f}、Mr = {Q_MR:,.0f} tf·cm")
    x0, sc = 330, 6.5
    rows = [("圖(a) 強軸：φbMn", 0.9 * Q_MNX / 100, C["bmd"], f"Cb × 內插 = {Q_CB * Q_MNX1:,.0f} 大於 Mp → 取 Mp"),
            ("　（不計 Cb）", 0.9 * Q_MNX1 / 100, C["ghost"], "結論相同"),
            ("圖(b) 弱軸：φbMny", 0.9 * Q_MNY / 100, C["load"], f"min(FyZy {Q_FY * Q_ZY:,.0f}, 1.5FySy {1.5 * Q_FY * Q_SY:,.0f})")]
    for i, (lab, v, col, s) in enumerate(rows):
        y = 140 + i * 80
        cv.text_px(x0 - 12, y, lab, 13, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, sc * v, 30, col, 3)
        ok = v >= Q_MU
        cv.text_px(x0 + sc * v + 8, y - 6, f"{v:.1f}　{'OK' if ok else 'NG'}", 13.5, C["bmd"] if ok else C["load"], "start", weight="700")
        cv.text_px(x0 + sc * v + 8, y + 14, s, 11.5, C["muted"], "start")
    xm = x0 + sc * Q_MU
    _hl(cv, H1, xm, 110, xm, 330, C["accent"], 1.6, dash="5 4")
    cv.text_px(xm, 350, f"Mu = {Q_MU:g}", 13, C["accent"], weight="700")
    cv.text_px(W1 / 2, H1 - 40, "弱軸彎曲不會側扭挫屈，但塑性模數小、且受 1.5FySy 上限：強度只剩強軸的約 1/4", 12.5, C["muted"])
    path = os.path.join(OUT, f"{TAG}-fig-2-axes.svg")
    compose([cv], cols=1,
            title=f"圖 2　強軸 φbMn = {0.9 * Q_MNX / 100:.1f} t·m ≥ 42 OK；弱軸 φbMny = {0.9 * Q_MNY / 100:.1f} t·m 小於 42 NG",
            sub=f"Mn = Cb × 內插（{Q_CB:.3f} × {Q_MNX1:,.0f}）超過 Mp，以 Mp 為上限",
            note="弱軸忘了 1.5FySy 上限（取 FyZy）、或以為弱軸也要算 LTB，都會判錯；Cb 放大後不得超過 Mp",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 C 滾支承當成側撐點而把無支長度切成兩段 3 m；強軸、弱軸兩圖的斷面方位對調"),
    (fig1_moment, "§4 設計用彎矩、圖(a) Cb",
     "C 當側撐點（Lb 取 3 m）；Cb 式 MA、MC 代支點彎矩；A 反力方向弄反"),
    (fig2_axes, "§4 圖(a)、圖(b)",
     "Cb 放大後超過 Mp 未截斷；弱軸漏 1.5FySy 上限；弱軸也算 LTB"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
