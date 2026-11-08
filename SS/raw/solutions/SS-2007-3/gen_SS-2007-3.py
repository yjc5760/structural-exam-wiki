#!/usr/bin/env python3
"""
SS-2007-3 H700×200×12×25 梁三種側撐條件的 LRFD 設計彎曲強度 — 解題圖解腳本

用法：
    python3 gen_SS-2007-3.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2007-3-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2007-3.md §4，由下式即時算出（單位 tf、cm）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2007-3"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


def q_mn_lrfd(lb, cb, mp, mr, lp, lr, sx, x1, x2, ry):
    """LRFD 撓曲 Mn（tf·cm；lb、lp、lr 為 cm）"""
    if lb <= lp:
        return mp
    if lb <= lr:
        return min(cb * (mp - (mp - mr) * (lb - lp) / (lr - lp)), mp)
    s = lb / ry
    return min(cb * sx * x1 * math.sqrt(2) / s * math.sqrt(1 + x1 * x1 * x2 / (2 * s * s)), mp)


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2007-3.md §4
# ══════════════════════════════════════════════════════════════
Q_FY, Q_FR, Q_E, Q_G = 3.5, 1.16, 2040.0, 790.0
Q_SX, Q_ZX, Q_IY, Q_RY, Q_J, Q_CW, Q_A = 4040.6, 4642.5, 3343.0, 4.33, 245.77, 3807536.63, 178.0
Q_MP = Q_FY * Q_ZX                                        # 16,248.8
Q_MR = (Q_FY - Q_FR) * Q_SX                               # 9,455.0
Q_X1 = math.pi / Q_SX * math.sqrt(Q_E * Q_G * Q_J * Q_A / 2)
Q_X2 = 4 * Q_CW / Q_IY * (Q_SX / (Q_G * Q_J)) ** 2
Q_LP = 80 * Q_RY / math.sqrt(Q_FY)
Q_LR = Q_RY * Q_X1 / (Q_FY - Q_FR) * math.sqrt(1 + math.sqrt(1 + Q_X2 * (Q_FY - Q_FR) ** 2))
Q_CASES = [("(一)", 0.0, 1.0), ("(二)", 500.0, 1.0), ("(三)", 800.0, 1.7)]
mn = lambda lb, cb: q_mn_lrfd(max(lb, 1e-6), cb, Q_MP, Q_MR, Q_LP, Q_LR, Q_SX, Q_X1, Q_X2, Q_RY)


def fig1_curve():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("φbMn 對 Lb（tf·m）：Cb = 1 與 Cb = 1.7", f"Lp = {Q_LP / 100:.2f} m、Lr = {Q_LR / 100:.2f} m；Mp = FyZx、Mr = (Fy − Fr)Sx")
    X0, X1, YB, YT = 100, 640, 460, 110
    lmax, mmax = 1000.0, 160.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda m: YB - (YB - YT) * m / mmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 1001, 200):
        cv.text_px(PX(v), YB + 18, f"{v / 100:g}", 11.5, C["muted"])
    for v in range(0, 161, 40):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "Lb（m）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "φbMn（tf·m）", 13, C["text"], "start", weight="700")
    ls = [lmax * i / 400 for i in range(0, 401)]
    cv.poly([(PX(l), H1 - PY(0.9 * mn(l, 1.7) / 100)) for l in ls], C["sfd"], 2.2, dash="7 4")
    cv.poly([(PX(l), H1 - PY(0.9 * mn(l, 1.0) / 100)) for l in ls], C["bmd"], 2.8)
    for l, lab in ((Q_LP, f"Lp = {Q_LP / 100:.2f}"), (Q_LR, f"Lr = {Q_LR / 100:.2f}")):
        _hl(cv, H1, PX(l), YB, PX(l), YT, C["accent"], 1.1, dash="4 4")
        cv.text_px(PX(l) + 4, YT + 6, lab, 11.5, C["accent"], "start")
    for name, lb, cb in Q_CASES:
        l = lb if lb > 0 else Q_LP
        v = 0.9 * mn(l, cb) / 100
        cv.dot((PX(l), H1 - PY(v)), 6.5, fill=C["load"])
        cv.text_px(PX(l) + 10, PY(v) + (22 if name == "(一)" else -12), f"{name} {v:.1f}", 13, C["load"], "start", weight="700")
    cv.legend(X1 - 190, YB - 70, [(C["bmd"], "Cb = 1.0"), (C["sfd"], "Cb = 1.7（≤ φMp）")], size=12, gap=19)
    xt = 680
    rows = [("塑性區 Lb ≤ Lp：φMp", C["text"], "400"),
            (f"(一) 0.9 × {Q_MP:,.1f} → {0.9 * Q_MP / 100:.1f}", C["load"], "700"),
            ("非彈性區 Lp 到 Lr：直線內插", C["text"], "400"),
            (f"(二) Lb = 5 m → {0.9 * mn(500, 1) / 100:.1f}", C["load"], "700"),
            ("彈性區 Lb > Lr：Mcr 式 × Cb", C["text"], "400"),
            (f"(三) Lb = 8 m、Cb 1.7 → {0.9 * mn(800, 1.7) / 100:.1f}", C["load"], "700"),
            (f"（Cb = 1 時只有 {0.9 * mn(800, 1) / 100:.1f}）", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        cv.text_px(xt, 140 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-curve.svg")
    compose([cv], cols=1,
            title=f"圖 1　三種側撐條件分屬塑性、非彈性、彈性三區：φbMn = {0.9 * Q_MP / 100:.1f}、{0.9 * mn(500, 1) / 100:.1f}、{0.9 * mn(800, 1.7) / 100:.1f} tf·m",
            sub=f"X1 = {Q_X1:.1f} tf/cm²、X2 = {Q_X2:.3f} cm⁴/tf²",
            note="Cb 只乘在 LTB 段且不得使 Mn 超過 Mp；(三) 雖 Lb 較長，但 Cb = 1.7 使強度只比 (二) 低一些",
            path=path)
    return path


def fig2_formula():
    W1, H1 = 1000, 500
    cv = Canvas(W1, H1, sx=1)
    cv.panel("考卷公式集的非彈性式分母印成 Lr − Lb（應為 Lr − Lp）", "Cb = 1；只畫非彈性區 Lp 到 Lr")
    X0, X1, YB, YT = 100, 640, 420, 110
    l0, l1, m0, m1 = 150.0, 600.0, -60.0, 180.0
    PX = lambda l: X0 + (X1 - X0) * (l - l0) / (l1 - l0)
    PY = lambda m: YB - (YB - YT) * (m - m0) / (m1 - m0)
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(150, 601, 50):
        cv.text_px(PX(v), YB + 18, f"{v / 100:g}", 11.5, C["muted"])
    for v in range(-60, 181, 60):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "Lb（m）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "φbMn（tf·m）", 13, C["text"], "start", weight="700")
    ls = [Q_LP + (Q_LR - Q_LP) * i / 200 for i in range(0, 201)]
    cv.poly([(PX(l), H1 - PY(0.9 * mn(l, 1) / 100)) for l in ls], C["bmd"], 2.8)
    wrong = lambda l: 0.9 * (Q_MP - (Q_MP - Q_MR) * (l - Q_LP) / (Q_LR - l)) / 100
    wl = [l for l in ls if l < Q_LR - 5 and wrong(l) > m0]
    cv.poly([(PX(l), H1 - PY(wrong(l))) for l in wl], C["load"], 2.2, dash="7 4")
    v5, w5 = 0.9 * mn(500, 1) / 100, wrong(500)
    cv.dot((PX(500), H1 - PY(v5)), 6.5, fill=C["bmd"])
    cv.text_px(PX(500) + 4, PY(v5) + 26, f"正確 {v5:.1f}", 13, C["bmd"], "start", weight="700")
    if w5 > m0:
        cv.dot((PX(500), H1 - PY(w5)), 6, fill=C["load"])
    cv.text_px(PX(440), PY(-30), f"照印錯式：Lb = 5 m 時 {w5:.1f}".replace("-", "−"), 13, C["load"], "end", weight="700")
    xt = 680
    rows = [("(Lb − Lp)/(Lr − Lp)", C["bmd"], "700"),
            (f"= (500 − {Q_LP:.1f})/({Q_LR:.1f} − {Q_LP:.1f})", C["text"], "400"),
            (f"= {(500 - Q_LP) / (Q_LR - Q_LP):.4f}", C["bmd"], "700"),
            ("", C["text"], "400"),
            ("印錯：(Lb − Lp)/(Lr − Lb)", C["load"], "700"),
            (f"= {(500 - Q_LP) / (Q_LR - 500):.2f}（大於 1，Mn 變負）", C["load"], "400"),
            ("", C["text"], "400"),
            ("卷首已要求自行檢查修正", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 30, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-formula.svg")
    compose([cv], cols=1,
            title=f"圖 2　非彈性區是 Mp 到 Mr 的直線內插：分母用 Lr − Lp；照考卷印錯的式子會得到 {w5:.1f}".replace("到 -", "到 −"),
            sub="Lb = Lp 時 Mn = Mp、Lb = Lr 時 Mn = Mr，兩端都要接得上",
            note="照抄印錯的分母是本題最大陷阱；用兩端點檢查公式即可發現",
            path=path)
    return path


FIGURES = [
    (fig1_curve, "§4 Step 2–4、案例 (一)–(三)",
     "三種 Lb 判錯區段；Cb 乘到塑性區或使 Mn 超過 Mp；X1、X2 代錯"),
    (fig2_formula, "§4 案例 (二)",
     "照抄考卷印錯的分母 Lr − Lb"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
