#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2012-3 圖解產生腳本（LRFD 雙軸梁柱：B1 下限與 H1 互制）

圖上每個數值都由下方常數區（抄自解析 §1 題給）即時算出，改輸入重跑即改變圖形。
執行：python3 gen_SS-2012-3.py   →   figs/*.svg
"""
import sys, os, math
# struct-diagram 的 primitives 取自本知識庫自帶的 skill 副本（repo 相對路徑，故可原地重跑）；
# 若把本檔搬到別處，設環境變數 SD_SKILL 指向 struct-diagram 目錄即可。
_HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.environ.get("SD_SKILL",
                       os.path.normpath(os.path.join(_HERE, "..", "..", "..",
                                                     "skills", "struct-diagram")))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_HERE, "figs")
TAG = "SS-2012-3"

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


def _col_bmd(cv, H1, cx, yt, yb, m_top, m_bot, sc, col, fill, lab_top, lab_bot, top_sup="pin", bot_sup="fixed"):
    """垂直柱＋線性彎矩圖（正值畫在右側）。像素座標（y 向下）。"""
    _hl(cv, H1, cx, yt, cx, yb, C["member"], 5.0)
    z = None
    if m_top * m_bot < 0:                          # 變號：反曲點
        z = yt + (yb - yt) * m_top / (m_top - m_bot)
    pts = [(cx, H1 - yt), (cx + sc * m_top, H1 - yt), (cx + sc * m_bot, H1 - yb), (cx, H1 - yb)]
    if z is None:
        cv.polygon(pts, fill, col, 2.2)
    else:
        cv.polygon([(cx, H1 - yt), (cx + sc * m_top, H1 - yt), (cx, H1 - z)], fill, col, 2.2)
        cv.polygon([(cx, H1 - z), (cx + sc * m_bot, H1 - yb), (cx, H1 - yb)], fill, col, 2.2)
        cv.dot((cx, H1 - z), 5, fill="#FFFFFF", stroke=C["accent"], w=2.4)
    if lab_top:
        cv.text_px(cx + sc * m_top + (8 if m_top >= 0 else -8), yt - 14, lab_top, 13, col,
                   "start" if m_top >= 0 else "end", weight="700")
    if lab_bot:
        cv.text_px(cx + sc * m_bot + (8 if m_bot >= 0 else -8), yb + 18, lab_bot, 13, col,
                   "start" if m_bot >= 0 else "end", weight="700")
    return z


def _h1_panel(W1, H1, title, sub, pr, mr, extra=()):
    """H1 互制圖（正規化）：縱軸 Pu/φPn、橫軸 ΣMu/φMn；需求點與由原點射線"""
    cv = Canvas(W1, H1, sx=1)
    cv.panel(title, sub)
    X0, YB, S = 96, H1 - 96, min(W1 - 150, H1 - 210)
    PX = lambda x: X0 + S * x
    PY = lambda y: YB - S * y
    _hl(cv, H1, X0, YB, PX(1.12), YB, C["muted"], 1.6)
    _hl(cv, H1, X0, YB, X0, PY(1.1), C["muted"], 1.6)
    for v in (0.2, 0.5, 1.0):
        cv.text_px(X0 - 10, PY(v), f"{v:g}", 12, C["muted"], "end")
    for v in (0.5, 0.9, 1.0):
        cv.text_px(PX(v), YB + 18, f"{v:g}", 12, C["muted"])
    cv.text_px(PX(0.56), YB + 46, "ΣMu / φbMn", 13, C["text"], weight="700")
    cv.text_px(X0 - 8, PY(1.1) - 14, "Pu / φcPn", 13, C["text"], "start", weight="700")
    xb = 9 / 8 * 0.8                                 # 折點 (0.9, 0.2)
    cv.polygon([(PX(0), H1 - PY(0)), (PX(0), H1 - PY(1)), (PX(xb), H1 - PY(0.2)), (PX(1), H1 - PY(0))],
               C["fill_m"], C["bmd"], 2.6)
    _hl(cv, H1, X0, PY(0.2), PX(xb), PY(0.2), C["ghost"], 1.2, dash="4 4")
    cv.text_px(PX(0.42), PY(0.63) - 6, "H1-1a", 12.5, C["bmd"], "start", weight="700")
    cv.text_px(PX(0.97), PY(0.12), "H1-1b", 12.5, C["bmd"], "start", weight="700")
    # 射線與需求點
    r = pr + 8 / 9 * mr if pr >= 0.2 else pr / 2 + mr
    bx, by = mr / r, pr / r
    _hl(cv, H1, X0, YB, PX(bx), PY(by), C["accent"], 1.6, dash="6 4")
    cv.dot((PX(bx), H1 - PY(by)), 5, fill="#FFFFFF", stroke=C["bmd"], w=2.4)
    cv.dot((PX(mr), H1 - PY(pr)), 7, fill=C["load"])
    cv.text_px(PX(mr) - 14, PY(pr) - 34, f"需求點 ({mr:.3f}, {pr:.3f})", 13, C["load"], "end", weight="700")
    cv.text_px(PX(mr) - 14, PY(pr) - 14, f"距離比 = {r:.3f}", 13, C["load"], "end", weight="700")
    for x, y, s in extra:
        cv.text_px(x, y, s, 12.5, C["muted"], "start")
    return cv, r

# ══════════════════════════════════════════════════════════════
# 由 SS-2012-3 §1（題給）取得；§4 的每一步由下式重算
# ══════════════════════════════════════════════════════════════
PU, MUX, MUY = 800.0, 100.0, 50.0           # kN、kN·m（柱底固接端）         §1
KL = 4500.0                                 # mm，強弱軸同                    §1
F_Y, E_S = 350.0, 200000.0                  # MPa                             §1
ZX, ZY, A_G = 1884512.0, 604683.0, 12903.0  # mm^3、mm^2                      §1
R_X, R_Y = 153.0, 62.0                      # mm                              §1
PHI_C, PHI_B = 0.85, 0.90                   # §4 Step 1、3

LAMC = KL / R_Y / math.pi * math.sqrt(F_Y / E_S)               # Step 1（弱軸控制）
FCR  = 0.658**(LAMC**2) * F_Y if LAMC <= 1.5 else 0.877 / LAMC**2 * F_Y
PHIPN = PHI_C * FCR * A_G / 1e3                                # kN
M1M2 = 0.0                                                     # 頂端鉸接 M1 = 0          Step 2
CM   = 0.6 - 0.4 * M1M2
PEX  = math.pi**2 * E_S * R_X**2 * A_G / KL**2 / 1e3           # kN
PEY  = math.pi**2 * E_S * R_Y**2 * A_G / KL**2 / 1e3
B1X, B1Y = CM / (1 - PU / PEX), CM / (1 - PU / PEY)
B1X_USE, B1Y_USE = max(B1X, 1.0), max(B1Y, 1.0)
PHIMX = PHI_B * F_Y * ZX / 1e6                                 # kN·m         Step 3
PHIMY = PHI_B * F_Y * ZY / 1e6
PR  = PU / PHIPN                                               # Step 4
MRX, MRY = B1X_USE * MUX / PHIMX, B1Y_USE * MUY / PHIMY
MR  = MRX + MRY
RATIO = PR + 8 / 9 * MR                                        # Step 5
R_NO89 = PR + MR                                               # §5.3 漏乘 8/9
R_B1LT1 = PR + 8 / 9 * (B1X * MUX / PHIMX + B1Y * MUY / PHIMY) # 若誤用 B1 < 1 折減


def fig1_b1():
    W1, H1 = 520, 520
    cv = Canvas(W1, H1, sx=1)
    cv.panel("① 一階彎矩：底端最大、頂端為零", "柱底固接、柱頂鉸接（斜撐構架，無側移）")
    yt, yb = 140, 400
    sc = 1.5
    _col_bmd(cv, H1, 120, yt, yb, 0.0, MUX, sc, C["bmd"], C["fill_m"], None, f"Mux = {MUX:g}")
    _col_bmd(cv, H1, 330, yt, yb, 0.0, MUY, sc, C["accent"], C["fill_m"], None, f"Muy = {MUY:g}")
    cv.text_px(120, yt - 24, "強軸", 13.5, C["text"], weight="700")
    cv.text_px(330, yt - 24, "弱軸", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 62, f"M1/M2 = 0 ⇒ Cm = {CM:.1f}", 15, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 34, "最大彎矩在端點，構材中段的 P-δ 放大不會超過它", 12.5, C["muted"])
    p1 = cv

    cv = Canvas(W1, H1, sx=1)
    cv.panel("② B1 = Cm /(1 − Pu/Pe1) 與下限 1.0", "B1 小於 1 時取 1.0，不得折減一階彎矩")
    x0, sc2 = 140, 260.0
    _hl(cv, H1, x0 + sc2, 120, x0 + sc2, 330, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + sc2, 110, "下限 1.0", 12.5, C["load"], weight="700")
    for i, (nm, b, pe) in enumerate((("強軸 B1x", B1X, PEX), ("弱軸 B1y", B1Y, PEY))):
        y = 170 + i * 100
        cv.text_px(x0 - 14, y, nm, 14, C["text"], "end", weight="700")
        cv.rect_px(x0, y - 15, sc2 * b, 30, C["bmd"] if i == 0 else C["accent"], 4)
        cv.text_px(x0 + sc2 * b - 8, y, f"{b:.3f}", 12.5, "#FFFFFF", "end", weight="700")
        cv.text_px(x0, y + 30, f"Pe1 = {pe:,.0f} kN，Pu/Pe1 = {PU / pe:.3f}", 12, C["muted"], "start")
    cv.text_px(W1 / 2, H1 - 86, f"兩軸皆取 B1 = 1.0 ⇒ Mux = {MUX:g}、Muy = {MUY:g} kN·m", 13.5, C["text"], weight="700")
    cv.text_px(W1 / 2, H1 - 58, f"若拿 B1 折減彎矩，互制比會由 {RATIO:.3f} 被低估成 {R_B1LT1:.3f}", 12.5, C["load"])
    cv.text_px(W1 / 2, H1 - 32, "B1 小於 1 只代表 P-δ 不放大端彎矩，不代表彎矩變小", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-1-b1.svg")
    compose([p1, p2], cols=2,
            title="圖 1　Cm = 0.6 使 B1 小於 1——但 B1 取下限 1.0",
            sub=f"Pu = {PU:g} kN；KL = {KL / 1000:g} m（兩軸同）",
            note="B1 的意義是「跨中最大二階彎矩 ÷ 端點一階最大彎矩」；小於 1 表示端點仍是最大處",
            path=path)
    return path


def fig2_pm():
    W1, H1 = 560, 560
    p1, r = _h1_panel(W1, H1, "① H1 互制圖（正規化）", f"Pu/φcPn = {PR:.3f} ≥ 0.2 ⇒ H1-1a", PR, MR)
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② H1-1a 的組成與常見誤算", "長條長度＝比值；紅虛線＝1.0")
    x0, SC = 150, 300.0
    _hl(cv, H1, x0 + SC, 110, x0 + SC, 420, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + SC, 100, "上限 1.0", 12.5, C["load"], weight="700")
    COLS = [C["compr"], C["bmd"], C["accent"]]
    _stack_row(cv, x0, 160, SC, [PR, 8 / 9 * MRX, 8 / 9 * MRY], COLS, "正解 H1-1a", C["bmd"])
    cv.legend(x0 - 120, 214, [(COLS[0], f"Pu/φcPn = {PR:.3f}"),
                              (COLS[1], f"Mux/φbMnx = {MRX:.4f}，再 × 8/9"),
                              (COLS[2], f"Muy/φbMny = {MRY:.4f}，再 × 8/9")], size=12, gap=20)
    rows = ((f"漏乘 8/9", R_NO89), ("誤用 H1-1b", PR / 2 + MR), ("拿 B1 折減", R_B1LT1))
    for i, (nm, v) in enumerate(rows):
        y = 320 + i * 44
        cv.text_px(x0 - 14, y, nm, 13, C["muted"], "end")
        cv.rect_px(x0, y - 12, SC * v, 24, C["ghost"], 4)
        cv.text_px(x0 + SC * v + 10, y, f"{v:.2f}", 13, C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 30, f"φcPn = {PHIPN:,.0f} kN　φbMnx = {PHIMX:.1f}　φbMny = {PHIMY:.1f} kN·m", 12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-pm.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　LRFD 雙軸互制：H1-1a = {RATIO:.3f} ≤ 1.0，OK",
            sub=f"λc = {LAMC:.3f}（弱軸控制）　Fcr = {FCR:.1f} MPa",
            note="弱軸彎矩只有強軸的一半，貢獻卻比強軸大——因為 φbMny 只有 φbMnx 的 1/3",
            path=path)
    return path


FIGURES = [
    (fig1_b1, "§4 Step 2",
     "拿 B1 小於 1 去折減一階彎矩（互制比被低估）；固接－鉸接柱誤取 Cm = 1.0"),
    (fig2_pm, "§4 Step 4–5",
     "Pu/φcPn ≥ 0.2 卻套 H1-1b；漏乘 8/9；忽略弱軸項的分量"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for _fn, _sec, _catch in FIGURES:
        print(f"{os.path.basename(_fn()):<30} {_sec:<16} 攔：{_catch}")
    print(f"λc={LAMC:.4f} Fcr={FCR:.2f} φPn={PHIPN:.1f} Pex={PEX:.0f} Pey={PEY:.0f} "
          f"B1x={B1X:.4f} B1y={B1Y:.4f} φMx={PHIMX:.2f} φMy={PHIMY:.2f} ratio={RATIO:.4f}")
