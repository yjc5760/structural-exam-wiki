#!/usr/bin/env python3
"""
SS-2005-4 固接－簡支 T 型鋼梁塑性設計 — 題目附圖重繪腳本

用法：
    python3 gen_SS-2005-4.py [輸出目錄]

重繪依據：題目正本 SS-2005-4-problem.md §4 判讀清單（2026-11-02 已確認）。
圖上每個支承、尺寸、載重都對應清單一項；只畫考卷給的東西，不含任何解題結果。
斷面依比例繪製；梁立面跨度與載重高度為示意比例。
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2005-4"

# ══════════════════════════════════════════════════════════
# 判讀清單（SS-2005-4-problem.md §4，已確認）
# ══════════════════════════════════════════════════════════
SPAN = 600.0        # #1 跨度 600 cm
LEFT = "fixed"      # #2 左端固接
RIGHT = "pin"       # #3 右端鉸支（簡支）
#                     #4 均布 w_u，向下，滿跨
BF, TF = 40.0, 2.6  # #6 翼板寬 40 cm、#7 翼板厚 2.6 cm
D = 24.0            # #8 全深 24 cm（翼板頂至腹板底）
TW = 2.4            # #9 腹板厚 2.4 cm
#                     #5 T 型，翼板在上、腹板向下
HW = D - TF         # 腹板淨高（推得值 21.4 cm）

PW, PH = 520, 380


def _rect(cv, x0, x1, y0, y1):
    cv.polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], C["fill_c"], C["member"], 1.8)


def beam_panel():
    sx = (PW - 150) / SPAN
    cv = Canvas(PW, PH, sx=sx, ox=80, oy=170)
    cv.panel("梁立面", "左端固接、右端簡支（跨度示意）")
    cv.line((0, 0), (SPAN, 0), C["member"], 5, cap="butt")
    cv.support((0, 0), LEFT, -90, size=26)   # 牆在左側（剖線朝外）
    cv.support((SPAN, 0), RIGHT, 0, size=16)
    cv.dot((SPAN, 0), 5.5, fill="#FFFFFF", stroke=C["member"], w=2.2)
    cv.udl((0, 0), (SPAN, 0), 0.11 * SPAN, n=11, label="w_{u}")
    cv.dim((0, 0), (SPAN, 0), f"{SPAN:.0f} cm", off=70, label_off=16)
    return cv


def section_panel():
    sx = 7.2
    cv = Canvas(PW, PH, sx=sx, ox=PW / 2, oy=78)
    cv.panel("鋼梁斷面", "依比例；全深量至腹板底")
    _rect(cv, -BF / 2, BF / 2, D - TF, D)          # 翼板
    _rect(cv, -TW / 2, TW / 2, 0, D - TF)          # 腹板
    cv.dim((-BF / 2, D), (BF / 2, D), f"{BF:.0f} cm", off=-26, label_off=-14)
    cv.dim((BF / 2, D - TF), (BF / 2, D), f"{TF} cm", off=26, label_off=30)
    cv.dim((-TW / 2, 0), (-TW / 2, D), f"{D:.0f} cm", off=-(BF / 2 - TW / 2) * sx - 30,
           label_off=-30, color=C["accent"])
    cv.dim((-TW / 2, 0), (TW / 2, 0), f"{TW} cm", off=26, label_off=16)
    return cv


def fig1_problem():
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([beam_panel(), section_panel()], cols=2,
            title="SS-2005-4 題目附圖（重繪）",
            sub="依題目正本判讀清單 #1–#9；只畫考卷所給條件",
            note="24 cm 為全深（翼板頂至腹板底），腹板淨高 21.4 cm 為推得值",
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
# 解題圖解（2026-11-03 補繪）——塑性斷面與一端固定一端簡支梁的崩塌機構
# 斷面座標：x 水平（cm）、y 自頂面向下（cm）；Q_PLATES = [(x0, x1, y0, y1), ...]
# ══════════════════════════════════════════════════════════════
import math


def _nf(v):
    """≥ 1000 取整數，否則一位小數（與解析的有效位數一致）"""
    return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.1f}"


def _area_above(plates, yc):
    return sum((x1 - x0) * max(0.0, min(y1, yc) - y0) for x0, x1, y0, y1 in plates)


def q_section_props(plates, fy):
    A = sum((x1 - x0) * (y1 - y0) for x0, x1, y0, y1 in plates)
    ye = sum((x1 - x0) * (y1 - y0) * (y0 + y1) / 2 for x0, x1, y0, y1 in plates) / A
    lo, hi = 0.0, max(p[3] for p in plates)
    for _ in range(200):
        mid = (lo + hi) / 2
        if _area_above(plates, mid) < A / 2: lo = mid
        else: hi = mid
    yp = (lo + hi) / 2
    def zabout(yc):
        z = 0.0
        for x0, x1, y0, y1 in plates:
            b = x1 - x0
            for a, c in ((y0, min(y1, yc)), (max(y0, yc), y1)):
                if c > a:
                    z += b * (c - a) * abs((a + c) / 2 - yc)
        return z
    return dict(A=A, ye=ye, yp=yp, Z=zabout(yp), Zw=zabout(ye), Mp=fy * zabout(yp))


def q_mech(L, mp):
    """一端固定一端簡支、滿跨均布：s 自簡支端量起"""
    w = lambda s: 2 * mp * (L + s) / (L * s * (L - s))
    s_opt = L * (math.sqrt(2) - 1)
    wu = w(s_opt)
    R = wu * L / 2 - mp / L
    M = lambda s: R * s - wu * s * s / 2
    return dict(w=w, s=s_opt, wu=wu, R=R, M=M)


def q_fig_pna(tag, plates, props, fy, title_extra, note):
    W1, H1 = 1000, 560
    depth = max(p[3] for p in plates)
    width = max(p[1] for p in plates) - min(p[0] for p in plates)
    sx = min(330 / depth, 320 / width)
    cv = Canvas(W1, H1, sx=sx, ox=260, oy=H1 - 130)
    cv.panel("斷面（依比例，cm）：PNA 上下面積相等", "藍＝PNA 以上（受壓）、紅＝PNA 以下（受拉）")
    Y = lambda y: -y
    yp, ye = props["yp"], props["ye"]
    for x0, x1, y0, y1 in plates:
        if y0 < yp:
            cv.polygon([(x0, Y(y0)), (x1, Y(y0)), (x1, Y(min(y1, yp))), (x0, Y(min(y1, yp)))], C["fill_c"], "none")
        if y1 > yp:
            cv.polygon([(x0, Y(max(y0, yp))), (x1, Y(max(y0, yp))), (x1, Y(y1)), (x0, Y(y1))], C["fill_t"], "none")
        cv.polygon([(x0, Y(y0)), (x1, Y(y0)), (x1, Y(y1)), (x0, Y(y1))], "none", C["member"], 1.6)
    xl, xr = min(p[0] for p in plates) - 4, max(p[1] for p in plates) + 4
    cv.line((xl, Y(yp)), (xr, Y(yp)), C["accent"], 2.4, dash="7 4")
    cv.text_px(cv.X(xr) + 6, cv.Y(Y(yp)) - 8, f"PNA（距頂 {yp:.2f}）", 12.5, C["accent"], "start", weight="700")
    cv.line((xl, Y(ye)), (xr, Y(ye)), C["ghost"], 1.4, dash="10 4 2 4")
    cv.text_px(cv.X(xr) + 6, cv.Y(Y(ye)) + 14, f"彈性形心（距頂 {ye:.2f}）", 12, C["muted"], "start")
    xt = 690
    rows = [(f"A = {props['A']:.2f} cm²，A/2 = {props['A'] / 2:.2f}", C["text"]),
            (f"PNA 距頂 {yp:.2f} cm（上下各 {props['A'] / 2:.2f} cm²）", C["accent"]),
            (f"Z = {_nf(props['Z'])} cm³", C["text"]),
            (f"Mp = Fy·Z = {fy} × {_nf(props['Z'])} = {_nf(props['Mp'])} tf·cm", C["bmd"]),
            ("", C["text"]),
            (f"誤以彈性形心為軸：Z = {_nf(props['Zw'])}", C["load"]),
            (f"（{'高' if props['Zw'] > props['Z'] else '低'}估 {abs(props['Zw'] / props['Z'] - 1):.1%}；且上下合力不平衡）", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(xt, 160 + i * 34, s, 13.5, col, "start", weight="700" if col in (C["bmd"], C["accent"]) else "400")
    path = os.path.join(OUT, f"{tag}-fig-1-pna.svg")
    compose([cv], cols=1, title=f"圖 1　塑性中性軸 PNA 距頂 {yp:.2f} cm{title_extra}",
            sub="塑性中性軸由「上下面積相等」決定；彈性形心由「面積一次矩為零」決定，非對稱斷面兩者不同",
            note=note, path=path)
    return path


def q_fig_mech(tag, L, mech, mp, fixed_left, unit_w, wu_disp, note, simple_kind="pin"):
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 崩塌機構（上）與崩塌時彎矩圖（下）", "s 自簡支端量起；彎矩圖正值（跨內）畫在下方")
    x0, x1, yb = 110, 890, 160
    ym = 360
    sc = (x1 - x0) / L
    X = (lambda s: x1 - sc * s) if fixed_left else (lambda s: x0 + sc * s)
    _hl(cv, H1, x0, yb, x1, yb, C["member"], 4.0)
    xf, xs = (x0, x1) if fixed_left else (x1, x0)
    cv.support((xf, H1 - yb), "fixed", 90 if fixed_left else -90, size=22)
    cv.support((xs, H1 - yb), simple_kind, 0, size=14)
    for k in range(14):
        xa = x0 + 10 + k * (x1 - x0 - 20) / 13
        cv.arrow((xa, H1 - yb + 34), (xa, H1 - yb + 4), C["load"], 1.6, 7)
    _hl(cv, H1, x0, yb - 34, x1, yb - 34, C["load"], 1.6)
    ms = max(abs(mech["M"](L)), mp)
    k = 80 / ms
    _hl(cv, H1, x0, ym, x1, ym, C["muted"], 1.4)
    pts = [(X(s), H1 - (ym + k * mech["M"](s))) for s in [L * i / 200 for i in range(201)]]
    cv.polygon([(X(0), H1 - ym)] + pts + [(X(L), H1 - ym)], C["fill_m"], C["bmd"], 2.2)
    xh = X(mech["s"])
    for xx in (xh, xf):
        cv.dot((xx, H1 - yb), 7, fill="#FFFFFF", stroke=C["accent"], w=2.6)
        _hl(cv, H1, xx, yb + 10, xx, ym - 4, C["accent"], 1.0, dash="3 4")
    cv.text_px(xh, ym + k * mp + 22, f"+Mp（距簡支端 {mech['s']:.1f}）", 12.5, C["bmd"], weight="700")
    cv.text_px(xf + (12 if fixed_left else -12), ym - k * mp - 8, "−Mp", 12.5, C["bmd"], "start" if fixed_left else "end", weight="700")
    cv.text_px(xh, yb - 46, "塑性鉸", 12, C["accent"], weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"塑性鉸：固定端＋跨內 1 處（超靜定 1 次 → 2 個鉸）；距固定端 {L - mech['s']:.1f}", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, 520, sx=1)
    H2 = 520
    cv.panel("② 虛功法：wu 隨跨內鉸位置 s 變化，取最小值", "wu(s) = 2Mp(L + s) / [L·s(L − s)]")
    X0, X1, YB, YT = 120, 880, 390, 110
    lo, hi = 9.0, 20.0
    PX = lambda r: X0 + (X1 - X0) * r
    PY = lambda v: YB - (YB - YT) * (v - lo) / (hi - lo)
    _hl(cv, H2, X0, YB, X1, YB, C["muted"], 1.6)
    _hl(cv, H2, X0, YB, X0, YT, C["muted"], 1.6)
    for r in (0, 0.25, 0.5, 0.75, 1.0):
        cv.text_px(PX(r), YB + 20, f"{r:g}L", 12, C["muted"])
    for v in (10, 12, 14, 16, 18, 20):
        cv.text_px(X0 - 10, PY(v), f"{v}", 12, C["muted"], "end")
    cv.text_px(X0 - 8, YT - 16, "wu·L²/Mp", 12.5, C["text"], "start", weight="700")
    cv.text_px((X0 + X1) / 2, YB + 44, "跨內鉸距簡支端 s/L", 12.5, C["text"], weight="700")
    norm = L * L / mp
    pts = [(PX(r), H2 - PY(mech["w"](r * L) * norm)) for r in [0.12 + 0.76 * i / 300 for i in range(301)]
           if mech["w"](r * L) * norm <= hi]
    cv.poly(pts, C["bmd"], 3.0)
    vmin = mech["wu"] * norm
    rmin = mech["s"] / L
    cv.dot((PX(rmin), H2 - PY(vmin)), 7, fill=C["bmd"])
    cv.text_px(PX(rmin) + 12, PY(vmin) + 24, f"最小：s = (√2 − 1)L = {mech['s']:.1f}，wu = {vmin:.3f} Mp/L²", 13, C["bmd"], "start", weight="700")
    vmid = mech["w"](L / 2) * norm
    cv.dot((PX(0.5), H2 - PY(vmid)), 6, fill=C["load"])
    cv.text_px(PX(0.5) + 12, PY(vmid) - 14, f"誤取跨中：{vmid:.2f} Mp/L²（高估 {vmid / vmin - 1:.1%}，偏不安全）", 12.5, C["load"], "start", weight="700")
    p2 = cv
    path = os.path.join(OUT, f"{tag}-fig-2-mech.svg")
    compose([p1, p2], cols=1,
            title=f"圖 2　崩塌載重 wu = {vmin:.3f} Mp/L² = {wu_disp}",
            sub=f"Mp = {_nf(mp)} tf·cm、L = {L:g} cm；上限定理：真正的崩塌載重是所有機構中最小者",
            note=note, path=path)
    return path

Q_FY = 2.5                                         # t/cm²                    §1
Q_TW = 2.4                                         # 腹板厚 cm                §4.2
Q_PLATES = [(-BF / 2, BF / 2, 0.0, TF), (-Q_TW / 2, Q_TW / 2, TF, D)]
Q_PROPS = q_section_props(Q_PLATES, Q_FY)          # yp 1.942、Z 667.43、Mp 1668.6   §4.2
Q_MECH = q_mech(SPAN, Q_PROPS["Mp"])               # wu 0.0540 t/cm、距固端 351.5   §4.3–4.4


def fig1_pna():
    return q_fig_pna(TAG, Q_PLATES, Q_PROPS, Q_FY, "，落在翼板內",
                     "翼板面積 104 cm² 已超過 A/2 = 77.68 cm²，PNA 一定在翼板裡；T 形斷面正負彎矩的 Mp 相同")


def fig2_mech():
    return q_fig_mech(TAG, SPAN, Q_MECH, Q_PROPS["Mp"], True, "t/cm",
                      f"{Q_MECH['wu'] * 100:.2f} tf/m",
                      f"驗算：RA = wuL/2 + Mp/L，跨內 M 的極大值恰等於 Mp、出現在距固端 {SPAN - Q_MECH['s']:.1f} cm（下限定理亦成立）")


FIGURES = [
    (fig1_problem, "§1（題目正本 §4）",
     "把 24 cm 讀成腹板高（全深變 26.6 cm）；右端當成固定端"),
    (fig1_pna, "§4.2",
     "以彈性形心當中性軸算 Z；PNA 放在腹板裡"),
    (fig2_mech, "§4.1、§4.3–4.5",
     "跨內鉸取跨中（wu 偏不安全）；鉸距量錯端點；漏了固定端的鉸"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    assert abs(HW - 21.4) < 1e-9
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
