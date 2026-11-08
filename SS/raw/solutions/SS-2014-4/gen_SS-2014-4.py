#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SS-2014-4 圖解產生腳本（LRFD 梁柱：B1／B2 分開放大與 H1 互制）

圖上每個數值都由下方常數區（抄自解析 §1 題給）即時算出，改輸入重跑即改變圖形。
執行：python3 gen_SS-2014-4.py   →   figs/*.svg
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
TAG = "SS-2014-4"

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
    cv.text_px(PX(mr) - 14, PY(pr) - 34, f"需求點 ({mr:.2f}, {pr:.2f})", 13, C["load"], "end", weight="700")
    cv.text_px(PX(mr) - 14, PY(pr) - 14, f"距離比 = {r:.2f}", 13, C["load"], "end", weight="700")
    for x, y, s in extra:
        cv.text_px(x, y, s, 12.5, C["muted"], "start")
    return cv, r

# ══════════════════════════════════════════════════════════════
# 由 SS-2014-4 §1（題給）取得；§4 的每一步由下式重算
# ══════════════════════════════════════════════════════════════
P_NT, P_LT = 1600.0, 450.0          # kN：1.2D+0.5L、1.0E                      §1
MA_NT, MB_NT = 110.0, 70.0          # kN·m：頂端 Ma、底端 Mb（垂直力）          §1
MA_LT, MB_LT = 200.0, 200.0         # kN·m：地震力                             §1
SUM_PU, H_ST, DRIFT = 9000.0, 600.0, 5 / 1000     # 樓層 ΣPu、H、Δ/L           §1
L_MM = 3750.0                       # mm                                       §1
F_Y, E_S = 350.0, 200000.0          # MPa                                      §1
ZX, IX, A_G = 2572769.0, 415815194.0, 17097.0     # §1
R_X, R_Y, K_X, K_Y = 156.0, 94.0, 1.79, 1.0       # §1
PHI_C, PHI_B = 0.85, 0.90

PU   = P_NT + P_LT                                             # Step 1
B2   = 1 / (1 - SUM_PU * DRIFT * L_MM / (H_ST * L_MM))         # Step 2
PE1  = math.pi**2 * E_S * IX / L_MM**2 / 1e3                   # Step 3a（K = 1）
M1M2 = +MB_NT / MA_NT               # 兩端端彎矩同為順時針 ⇒ 雙曲率取正          Step 3b
CM   = 0.6 - 0.4 * M1M2
B1   = CM / (1 - PU / PE1)
B1U  = max(B1, 1.0)
MUX_TOP = B1U * MA_NT + B2 * MA_LT                             # Step 4
MUX_BOT = B1U * MB_NT + B2 * MB_LT
MUX  = max(MUX_TOP, MUX_BOT)
KLR  = max(K_X * L_MM / R_X, K_Y * L_MM / R_Y)                 # Step 5（強軸控制）
LAMC = KLR / math.pi * math.sqrt(F_Y / E_S)
FCR  = 0.658**(LAMC**2) * F_Y
PHIPN = PHI_C * FCR * A_G / 1e3
PHIMX = PHI_B * F_Y * ZX / 1e6                                 # Step 6
PR, MR = PU / PHIPN, MUX / PHIMX
RATIO = PR + 8 / 9 * MR                                        # Step 7
R_B1  = PR + 8 / 9 * (B1 * MA_NT + B2 * MA_LT) / PHIMX         # 誤：B1 未取 1.0
R_NOB2 = PR + 8 / 9 * (B1U * MA_NT + MA_LT) / PHIMX            # 誤：Mlt 未乘 B2
R_BOT  = PR + 8 / 9 * MUX_BOT / PHIMX                          # 誤：取底端


def fig1_superpose():
    W1, H1 = 340, 560
    yt, yb, cx = 150, 420, 120
    sc = 0.40                                     # 1 kN·m = 0.40 px
    panels = []
    for title, sub, mt, mb, col, lt, lb in (
            ("① 無側移 Mnt", f"× B1 = {B1U:.1f}（B1 = {B1:.3f} 取 1.0）",
             B1U * MA_NT, -B1U * MB_NT, C["bmd"], f"{B1U * MA_NT:.0f}", f"{B1U * MB_NT:.0f}"),
            ("② 側移 B2·Mlt", f"× B2 = {B2:.3f}",
             B2 * MA_LT, -B2 * MB_LT, C["accent"], f"{B2 * MA_LT:.1f}", f"{B2 * MB_LT:.1f}"),
            ("③ 疊加 Mux", "頂端控制",
             MUX_TOP, -MUX_BOT, C["load"], f"{MUX_TOP:.1f}", f"{MUX_BOT:.1f}")):
        cv = Canvas(W1, H1, sx=1)
        cv.panel(title, sub)
        z = _col_bmd(cv, H1, cx + 40, yt, yb, mt, mb, sc, col, C["fill_m"], lt, lb)
        cv.text_px(cx + 40, yt - 40, "頂端 a", 12.5, C["muted"])
        cv.text_px(cx + 40, yb + 44, "底端 b", 12.5, C["muted"])
        if z is not None:
            frac = (z - yt) / (yb - yt)
            cv.text_px(cx + 52, z, f"反曲點（距頂 {frac:.2f}L）", 11.5, C["accent"], "start")
        panels.append(cv)
    panels[0].text_px(W1 / 2, H1 - 56, f"兩端同轉向 ⇒ 雙曲率", 12.5, C["text"], weight="700")
    panels[0].text_px(W1 / 2, H1 - 32, f"M1/M2 = +{M1M2:.3f} ⇒ Cm = {CM:.3f}", 12.5, C["text"])
    panels[1].text_px(W1 / 2, H1 - 56, f"θ = ΣPuΔ/(ΣHL) = {1 - 1 / B2:.3f}", 12.5, C["text"])
    panels[1].text_px(W1 / 2, H1 - 32, "地震可反向：取與 Mnt 同號", 12.5, C["muted"])
    panels[2].text_px(W1 / 2, H1 - 56, f"頂 {MUX_TOP:.1f} > 底 {MUX_BOT:.1f}", 12.5, C["load"], weight="700")
    panels[2].text_px(W1 / 2, H1 - 32, f"Mux = {MUX:.1f} kN·m", 12.5, C["load"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-superpose.svg")
    compose(panels, cols=3,
            title="圖 1　Mux = B1·Mnt + B2·Mlt：分開放大、端點疊加",
            sub=f"Pu = {P_NT:g} + {P_LT:g} = {PU:g} kN；Pe1 = {PE1:,.0f} kN（K = 1）",
            note="同一張圖比例尺相同；控制端由疊加後決定，不是看 Mnt 或 Mlt 哪一端大",
            path=path)
    return path


def fig2_pm():
    W1, H1 = 560, 560
    p1, r = _h1_panel(W1, H1, "① H1 互制圖（正規化，Muy = 0）", f"Pu/φcPn = {PR:.2f} ≥ 0.2 ⇒ H1-1a", PR, MR)
    cv = Canvas(W1, H1, sx=1)
    cv.panel("② H1-1a 的組成與常見誤算", "長條長度＝比值；紅虛線＝1.0")
    x0, SC = 160, 300.0
    _hl(cv, H1, x0 + SC, 196, x0 + SC, 420, C["load"], 2.0, dash="6 4")
    cv.text_px(x0 + SC, 436, "上限 1.0", 12.5, C["load"], weight="700")
    COLS = [C["compr"], C["bmd"]]
    _stack_row(cv, x0, 160, SC, [PR, 8 / 9 * MR], COLS, "正解 H1-1a", C["bmd"], fmt="{:.2f}")
    cv.legend(x0 - 130, 214, [(COLS[0], f"Pu/φcPn = {PR:.2f}"),
                              (COLS[1], f"Mux/φbMnx = {MR:.4f}，再 × 8/9")], size=12, gap=20)
    rows = (("B1 未取 1.0", R_B1), ("Mlt 未乘 B2", R_NOB2), ("取底端彎矩", R_BOT))
    for i, (nm, v) in enumerate(rows):
        y = 300 + i * 44
        cv.text_px(x0 - 14, y, nm, 13, C["muted"], "end")
        cv.rect_px(x0, y - 12, SC * v, 24, C["ghost"], 4)
        cv.text_px(x0 + SC * v + 10, y, f"{v:.2f}", 13, C["muted"], "start", weight="700")
    cv.text_px(W1 / 2, H1 - 56, "三種誤算都低估需求，且都還判 OK——結論對了但數字錯", 12.5, C["muted"])
    cv.text_px(W1 / 2, H1 - 30, f"φcPn = {PHIPN:,.0f} kN（KL/r = {KLR:.2f}，強軸控制）　φbMnx = {PHIMX:.1f} kN·m",
               12.5, C["muted"])
    p2 = cv
    path = os.path.join(OUT, f"{TAG}-fig-2-pm.svg")
    compose([p1, p2], cols=2,
            title=f"圖 2　LRFD 互制：H1-1a = {RATIO:.2f} ≤ 1.0，OK",
            sub=f"λc = {LAMC:.3f}　Fcr = {FCR:.1f} MPa　B2 = {B2:.3f}",
            note="Kx = 1.79 使強軸 KL/r（43.03）反超弱軸（39.89）——φcPn 由強軸控制",
            path=path)
    return path


FIGURES = [
    (fig1_superpose, "§4 Step 2–4",
     "Mnt 與 Mlt 先加再一起放大；控制端取錯；雙曲率判成單曲率；B1 小於 1 未取 1.0"),
    (fig2_pm, "§4 Step 5–7",
     "KL/r 取弱軸而高估 φcPn；B1／B2 漏用使互制比被低估"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for _fn, _sec, _catch in FIGURES:
        print(f"{os.path.basename(_fn()):<30} {_sec:<16} 攔：{_catch}")
    print(f"B2={B2:.4f} Pe1={PE1:.0f} Cm={CM:.4f} B1={B1:.4f} Mtop={MUX_TOP:.2f} Mbot={MUX_BOT:.2f} "
          f"KLR={KLR:.3f} λc={LAMC:.4f} Fcr={FCR:.2f} φPn={PHIPN:.0f} φMx={PHIMX:.2f} PR={PR:.4f} MR={MR:.4f} ratio={RATIO:.4f}"
          f" R_B1={R_B1:.3f} R_NOB2={R_NOB2:.3f} R_BOT={R_BOT:.3f}")
