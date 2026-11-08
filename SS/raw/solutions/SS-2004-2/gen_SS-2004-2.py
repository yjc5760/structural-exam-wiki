#!/usr/bin/env python3
"""
SS-2004-2 H 型鋼拉力構材翼板續接（摩阻型螺栓設計）— 題目附圖重繪腳本

用法：
    python3 gen_SS-2004-2.py [輸出目錄]

重繪依據：題目正本 SS-2004-2-problem.md §4 判讀清單（待確認）。
只畫考卷附圖所示：兩段 H150×150×7×10 對接、間隙 5 mm、翼板外側外連接板、內側內連接板。
構材深度、翼板厚與 5 mm 間隙依比例；連接板厚度與長度為所求，只示意位置，不標尺寸；
考卷附圖未畫螺栓（螺栓直徑、個數、配置皆為所求），本圖亦不畫。
附表（聯結物容許應力）已照錄於題目正本 §2，不重繪。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2004-2"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2004-2-problem.md §4，待確認）
# ══════════════════════════════════════════════════════════
D, TF = 150.0, 10.0     # 題文 H150×150×7×10：全深 150 mm、翼板厚 10 mm
GAP = 5.0               # #2 兩段構材端面間隙 5 mm
#                         #1 每片翼板：外側一片外連接板、內側（腹板兩側）內連接板
# 示意（為所求，考卷未給）：
T_PL = 9.0              # 連接板厚（示意）
L_PL = 300.0            # 連接板全長（示意）
L_MEM = 380.0           # 每段構材畫出長度（示意）

PW, PH = 1000, 470


def _rect(cv, x0, x1, y0, y1, fill=C["fill_c"], w=1.8):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, C["member"], w)


def _break_end(cv, x, sgn):
    """構材斷裂端：S 形曲線（同考卷）"""
    n = 40
    pts = [(x + sgn * 12 * math.sin(2 * math.pi * i / n), D + 4 - (D + 8) * i / n)
           for i in range(n + 1)]
    cv.poly(pts, C["member"], 2.0)


def panel():
    sx = 1.18
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2, oy=150)
    cv.panel("翼板續接立面", "兩段 H150×150×7×10 對接；本設計僅在翼板連結")
    g = GAP / 2
    for sg in (-1, 1):
        xa, xb = sg * g, sg * L_MEM
        # 翼板（上、下）與構材外輪廓
        for y0 in (0.0, D - TF):
            _rect(cv, min(xa, xb), max(xa, xb), y0, y0 + TF, "rgba(63,74,90,0.10)", 1.6)
        cv.line((xa, TF), (xa, D - TF), C["member"], 1.6)      # 端面
        _break_end(cv, xb, sg)
    # 外連接板（翼板外側）
    _rect(cv, -L_PL / 2, L_PL / 2, D, D + T_PL)
    _rect(cv, -L_PL / 2, L_PL / 2, -T_PL, 0)
    # 內連接板（翼板內側；立面上腹板兩側的兩片重疊成一條）
    _rect(cv, -L_PL / 2, L_PL / 2, D - TF - T_PL, D - TF)
    _rect(cv, -L_PL / 2, L_PL / 2, TF, TF + T_PL)
    # 標註
    p_out = (-L_PL / 2 + 30, D + T_PL)
    q_out = (-L_PL / 2 - 40, D + 60)
    cv.line(p_out, q_out, C["muted"], 1.2)
    cv.dot(p_out, 3, C["muted"], C["muted"], 0)
    cv.text(q_out, "外連接板", 15, C["text"], "end", dx=-6)
    p_in = (L_PL / 2 - 30, D - TF - T_PL / 2)
    q_in = (L_PL / 2 + 50, D + 60)
    cv.line(p_in, q_in, C["muted"], 1.2)
    cv.dot(p_in, 3, C["muted"], C["muted"], 0)
    cv.text(q_in, "內連接板", 15, C["text"], "start", dx=6)
    # 5 mm 間隙（外側箭頭）
    yd = -T_PL - 32
    for sg in (-1, 1):
        cv.line((sg * g, 0), (sg * g, yd - 6), C["dim"], 1, dash="3 3")
        cv.arrow((sg * (g + 28), yd), (sg * g, yd), C["dim"], 1.4, 8)
    cv.math((0, yd), f"{GAP:.0f} mm", 15, C["text"], dy=24)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([panel()], cols=1,
            title="SS-2004-2 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1、#2；梁深、翼板厚與間隙依比例，連接板厚度與長度為所求（示意）",
            note="每片翼板上下兩面都有連接板（外＋內）→ 螺栓雙剪；內連接板在腹板兩側各一片",
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
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2004-2.md §4，由下式即時算出
# ══════════════════════════════════════════════════════════════
import math
Q_T   = 40.0 + 30.0                  # t，DL + LL                        §4.1
Q_TF  = Q_T / 2                      # 每翼板 35 t
Q_BF, Q_TW, Q_R = 150.0, 7.0, 11.0   # mm：bf、tw、圓角 R（題給）         §1
Q_BIN = (Q_BF - Q_TW - 2 * Q_R) / 2  # 內板可用寬 60.5 → 60 mm           §4.1
Q_BIN_USE = math.floor(Q_BIN)
Q_FV  = 1.19                         # t/cm²，A325 摩阻型標準孔（題給表）  §4.2
Q_DS  = [16, 20, 22, 24]             # mm
def q_opt(d):
    ab = math.pi * (d / 10) ** 2 / 4
    cap = 2 * Q_FV * ab               # 雙剪
    n = math.ceil(Q_TF / cap); n += n % 2
    m = n // 2
    return dict(d=d, ab=ab, cap=cap, n=n, m=m, len=1.5 * d + (m - 1) * 3 * d + 1.5 * d, win=3 * d)
Q_OPTS = [q_opt(d) for d in Q_DS]
Q_D   = max(o["d"] for o in Q_OPTS if o["win"] <= Q_BIN_USE)    # 20
Q_SEL = q_opt(Q_D)
Q_E1, Q_PITCH = 1.5 * Q_D, 3 * Q_D                              # 30、60 mm
Q_LSIDE = Q_SEL["len"]                                          # 180
Q_LPL = 2 * Q_LSIDE + GAP                                       # 365
Q_T_OUT, Q_T_IN = 8.0, 10.0                                     # mm（§4.5 採用）


def fig1_inner():
    W1, H1 = 560, 520
    sx = 2.7
    cv = Canvas(W1, H1, sx=sx, ox=W1 / 2 - 75 * sx, oy=300)
    cv.panel("① 翼板斷面：內連接板只能放在圓角以外", "H150×150×7×10，R = 11 mm（依比例）")
    def rect(x0, x1, y0, y1, fill, st=C["member"], w=1.6):
        cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, st, w)
    xw0, xw1 = (Q_BF - Q_TW) / 2, (Q_BF + Q_TW) / 2
    rect(0, Q_BF, 0, TF, "rgba(63,74,90,0.18)")                        # 翼板
    rect(xw0, xw1, -70, 0, "rgba(63,74,90,0.18)")                      # 腹板
    for sg, xe in ((-1, xw0), (1, xw1)):                               # 圓角
        cx = xe + sg * Q_R
        pts = [(xe, 0), (xe, -Q_R)] + [(cx - sg * Q_R * math.cos(a), -Q_R + Q_R * math.sin(a))
                                       for a in [k * math.pi / 2 / 12 for k in range(13)]]
        cv.polygon(pts, "rgba(63,74,90,0.18)", C["member"], 1.0)
    rect(0, Q_BF, TF, TF + Q_T_OUT, C["fill_c"], C["compr"])           # 外板
    rect(0, Q_BIN_USE, -Q_T_IN, 0, C["fill_m"], C["bmd"])              # 內板
    rect(Q_BF - Q_BIN_USE, Q_BF, -Q_T_IN, 0, C["fill_m"], C["bmd"])
    for xb in (Q_E1, Q_BF - Q_E1):                                     # 螺栓
        rect(xb - Q_D / 2, xb + Q_D / 2, -Q_T_IN - 6, TF + Q_T_OUT + 6, "rgba(185,28,28,0.25)", C["load"], 1.2)
    cv.dim((0, -Q_T_IN), (Q_BIN, -Q_T_IN), f"{Q_BIN:.1f}", off=26, label_off=14, size=12.5)
    cv.dim((0, TF + Q_T_OUT), (Q_E1, TF + Q_T_OUT), f"{Q_E1:.0f}", off=-20, label_off=-13, size=12.5)
    cv.dim((Q_E1, TF + Q_T_OUT), (Q_BIN_USE, TF + Q_T_OUT), f"{Q_BIN_USE - Q_E1:.0f}", off=-20, label_off=-13, size=12.5)
    cv.text_px(cv.X(Q_BF) + 8, cv.Y(TF + Q_T_OUT / 2), f"外板 {Q_T_OUT:.0f}", 12, C["compr"], "start", weight="700")
    cv.text_px(cv.X(Q_BF) + 8, cv.Y(-Q_T_IN / 2), f"內板 {Q_T_IN:.0f}", 12, C["bmd"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 70, f"可用寬 = (bf − tw − 2R)/2 = (150 − 7 − 22)/2 = {Q_BIN:.1f} → {Q_BIN_USE} mm", 13, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 44, f"一行螺栓兩側邊距 1.5d：3d ≤ {Q_BIN_USE} ⇒ d ≤ {Q_BIN_USE / 3:.0f} mm", 13, C["bmd"], weight="700")
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② 螺栓直徑試選（每翼板每側）", "灰＝內板寬需求 3d；藍＝每側連接長度")
    x0, sc1, sc2 = 120, 2.3, 1.05
    _hl(cv, H1, x0 + sc1 * Q_BIN_USE, 108, x0 + sc1 * Q_BIN_USE, 408, C["load"], 1.8, dash="5 4")
    cv.text_px(x0 + sc1 * Q_BIN_USE, 98, f"可用 {Q_BIN_USE}", 12, C["load"], weight="700")
    for i, o in enumerate(Q_OPTS):
        y = 140 + i * 72
        ok = o["win"] <= Q_BIN_USE
        cv.text_px(x0 - 14, y + 8, f"M{o['d']}", 15, C["text"] if ok else C["muted"], "end", weight="700")
        cv.rect_px(x0, y - 12, sc1 * o["win"], 18, C["ghost"] if ok else "rgba(185,28,28,0.35)", 3)
        cv.text_px(x0 + sc1 * o["win"] + 6, y - 3, f"3d = {o['win']}" + ("" if ok else "（放不下）"), 11.5,
                   C["muted"] if ok else C["load"], "start", weight="700")
        cv.rect_px(x0, y + 10, sc2 * o["len"], 16, C["compr"] if o["d"] == Q_D else "rgba(29,78,216,0.35)", 3)
        cv.text_px(x0 + sc2 * o["len"] + 6, y + 18, f"{o['n']} 顆、{o['len']:.0f} mm", 11.5, C["compr"], "start",
                   weight="700" if o["d"] == Q_D else "400")
    cv.text_px(W1 / 2, H1 - 70, f"M22、M24 較短但內板放不下；M16 要 8 顆、192 mm", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 44, f"採 M{Q_D}：雙剪 {Q_SEL['cap']:.2f} t/顆 × {Q_SEL['n']} = {Q_SEL['cap'] * Q_SEL['n']:.1f} ≥ {Q_TF:g} t", 13, C["text"], weight="700")
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-inner.svg")
    compose([p1, p2], cols=2,
            title=f"圖 1　內連接板寬度決定螺栓上限：d ≤ {Q_BIN_USE / 3:.0f} mm → 採 M{Q_D}",
            sub=f"T = {Q_T:g} t，每翼板 {Q_TF:g} t；A325 摩阻型標準孔 Fv = {Q_FV} t/cm²（雙剪）",
            note="直徑越大螺栓越少、接合越短，但卡在腹板圓角與翼板邊緣之間那 60 mm",
            path=path)
    return path


def fig2_layout():
    W1, H1 = 1000, 540
    sx = 1.8
    cv = Canvas(W1, H1, sx=sx, ox=W1 / 2, oy=130)
    cv.panel("翼板續接平面（每片翼板，單位 mm）", f"外板 PL{Q_T_OUT:.0f}×{Q_BF:.0f}×{Q_LPL:.0f}；內板 2-PL{Q_T_IN:.0f}×{Q_BIN_USE}×{Q_LPL:.0f}（虛線）")
    g = GAP / 2
    L = Q_LPL / 2
    for sg in (-1, 1):                                       # 兩段構材翼板
        xa, xb = sg * g, sg * (L + 45)
        cv.polygon([(min(xa, xb), 0), (max(xa, xb), 0), (max(xa, xb), Q_BF), (min(xa, xb), Q_BF)],
                   "rgba(63,74,90,0.08)", C["member"], 1.4)
    cv.polygon([(-L, 0), (L, 0), (L, Q_BF), (-L, Q_BF)], C["fill_c"], C["compr"], 2.0)
    for y0 in (0, Q_BF - Q_BIN_USE):
        cv.poly([(-L, y0), (L, y0), (L, y0 + Q_BIN_USE), (-L, y0 + Q_BIN_USE), (-L, y0)], C["bmd"], 1.4, dash="6 4")
    cv.line((-L - 45, Q_BF / 2), (L + 45, Q_BF / 2), C["ghost"], 1.2, dash="10 4 2 4")
    cv.text_px(cv.X(-L - 45) + 4, cv.Y(Q_BF / 2) - 10, "腹板中線", 11.5, C["muted"], "start")
    xs = [g + Q_E1 + k * Q_PITCH for k in range(Q_SEL["m"])]
    for sg in (-1, 1):
        for x in xs:
            for y in (Q_E1, Q_BF - Q_E1):
                cv.circle((sg * x, y), (Q_D + 2) / 2, fill="#FFFFFF", stroke=C["load"], w=2.0)
    # 尺寸
    ticks = [-L] + [-x for x in reversed(xs)] + [-g, g] + xs + [L]
    for a, b in zip(ticks[:-1], ticks[1:]):
        if b - a > 1:
            cv.dim((a, Q_BF), (b, Q_BF), f"{b - a:.0f}", off=-22, label_off=-13, size=12)
    cv.dim((-L, 0), (L, 0), f"{Q_LPL:.0f}", off=34, label_off=16, size=13)
    cv.dim((L, 0), (L, Q_E1), f"{Q_E1:.0f}", off=26, label_off=18, size=12)
    cv.dim((L, Q_E1), (L, Q_BF - Q_E1), f"{Q_BF - 2 * Q_E1:.0f}", off=26, label_off=18, size=12)
    cv.dim((L, Q_BF - Q_E1), (L, Q_BF), f"{Q_E1:.0f}", off=26, label_off=18, size=12)
    path = os.path.join(OUT, f"{TAG}-fig-2-layout.svg")
    compose([cv], cols=1,
            title=f"圖 2　螺栓配置：每側 2 行 × {Q_SEL['m']} 列 M{Q_D}，連接板長 {Q_LPL:.0f} mm",
            sub=f"端距 = 邊距 = 1.5d = {Q_E1:.0f}；列距 3d = {Q_PITCH:.0f}；行距 {Q_BF - 2 * Q_E1:.0f}（腹板兩側各一行，恰在內板中心）",
            note=f"每側長度 {Q_E1:.0f} + {Q_SEL['m'] - 1}×{Q_PITCH:.0f} + {Q_E1:.0f} = {Q_LSIDE:.0f}；全長 2 × {Q_LSIDE:.0f} + {GAP:.0f} = {Q_LPL:.0f}；全接合 {Q_SEL['n']} × 2 側 × 2 翼板 = {Q_SEL['n'] * 4} 顆",
            path=path)
    return path


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "只看到外連接板而按單剪設計；把內連接板當成腹板續接板"),
    (fig1_inner, "§4.1–4.3",
     "選 M22 以上（較短）卻沒檢查內連接板放不放得下；忽略腹板圓角 R 而高估可用寬"),
    (fig2_layout, "§4.4",
     "端距、列距配錯；漏算構材間隙；螺栓行沒落在內連接板中心"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
