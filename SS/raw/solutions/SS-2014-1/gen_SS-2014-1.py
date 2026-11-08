#!/usr/bin/env python3
"""
SS-2014-1 AISC-LRFD 柱強度曲線 λc 推導、Fy 提升影響、理論 K 值 — 解題圖解腳本

用法：
    python3 gen_SS-2014-1.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2014-1-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2014-1.md §4，由下式即時算出；E 取 200,000 MPa（題目未給，僅示意用）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2014-1"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2014-1.md §4
# ══════════════════════════════════════════════════════════════
Q_LC_B = 1.5                                  # 兩公式分界
Q_FY1, Q_FY2, Q_E = 350.0, 450.0, 200000.0    # MPa（E 為示意值）
Q_SHIFT = math.sqrt(Q_FY2 / Q_FY1)            # 1.134


def q_ratio(lc):
    """Fcr / Fy"""
    return 0.658 ** (lc * lc) if lc <= Q_LC_B else 0.877 / (lc * lc)


def q_lc(klr, fy):
    return klr / math.pi * math.sqrt(fy / Q_E)


def q_fcr(klr, fy):
    return q_ratio(q_lc(klr, fy)) * fy


def _axes(cv, H1, X0, X1, YB, YT, xt, yt, xl, yl, fx="{:g}", fy_="{:g}"):
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v, px in xt:
        cv.text_px(px, YB + 18, fx.format(v), 11.5, C["muted"])
    for v, py in yt:
        cv.text_px(X0 - 8, py, fy_.format(v), 11.5, C["muted"], "end")
        _hl(cv, H1, X0, py, X1, py, C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, xl, 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, yl, 13, C["text"], "start", weight="700")


def fig1_curve():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("Fcr / Fy 對 λc（兩條公式與適用範圍）", "λc² = Fy / Fe；λc = 1.5 時 Fe = 0.444 Fy")
    X0, X1, YB, YT = 100, 640, 460, 110
    lmax = 3.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda r: YB - (YB - YT) * r / 1.1
    _axes(cv, H1, X0, X1, YB, YT, [(v / 2, PX(v / 2)) for v in range(7)], [(v / 10, PY(v / 10)) for v in range(0, 11, 2)],
          "λc", "Fcr / Fy", "{:.1f}", "{:.1f}")
    ls = [lmax * i / 300 for i in range(1, 301)]
    inel = [l for l in ls if l <= Q_LC_B]
    ela = [l for l in ls if l >= Q_LC_B]
    cv.poly([(PX(0), H1 - PY(1))] + [(PX(l), H1 - PY(0.658 ** (l * l))) for l in inel], C["bmd"], 3)
    cv.poly([(PX(l), H1 - PY(0.877 / l ** 2)) for l in ela], C["compr"], 3)
    cv.poly([(PX(l), H1 - PY(min(1 / l ** 2, 1.1))) for l in ls if l > 0.95], C["ghost"], 1.8, dash="6 4")
    cv.text_px(PX(1.08), PY(1.0) - 8, "Euler 1/λc²", 12, C["muted"], "start")
    cv.poly([(PX(l), H1 - PY(0.877 / l ** 2)) for l in [1.0 + 0.5 * i / 50 for i in range(51)]], C["compr"], 1.4, dash="3 4")
    _hl(cv, H1, PX(Q_LC_B), YB, PX(Q_LC_B), YT, C["accent"], 1.4, dash="5 4")
    cv.dot((PX(Q_LC_B), H1 - PY(q_ratio(Q_LC_B))), 6, fill=C["accent"])
    cv.text_px(PX(Q_LC_B) + 10, PY(q_ratio(Q_LC_B)) - 14, f"λc = 1.5：0.658 的 2.25 次方 = {0.658 ** 2.25:.4f}", 12, C["accent"], "start", weight="700")
    cv.text_px(PX(Q_LC_B) + 10, PY(q_ratio(Q_LC_B)) + 4, f"0.877/2.25 = {0.877 / 2.25:.4f}（兩式相接）", 12, C["accent"], "start")
    cv.dot((PX(1.0), H1 - PY(0.658)), 4.5, fill=C["bmd"])
    cv.text_px(PX(1.0) - 12, PY(0.658) + 16, "λc = 1：0.658（Fe = Fy）", 12, C["bmd"], "end")
    cv.text_px(PX(0.6), YB - 24, "非彈性 0.658 的 λc² 次方", 13, C["bmd"], weight="700")
    cv.text_px(PX(2.3), YB - 24, "彈性 0.877 / λc²", 13, C["compr"], weight="700")
    xt = 690
    rows = [("λc", "非彈性", "彈性")] + [(f"{l:g}", f"{0.658 ** (l * l):.3f}" if l <= 1.5 else "—", f"{0.877 / l ** 2:.3f}" if l >= 1.5 else "—")
                                        for l in (0, 0.5, 1.0, 1.5, 2.0, 3.0)]
    for i, r in enumerate(rows):
        for c, v in enumerate(r):
            cv.text_px(xt + c * 95, 140 + i * 30, v, 12.5, C["text"], weight="700" if i == 0 else "400")
    cv.text_px(xt, 140 + 8 * 30, "0.877：考慮初始彎曲，", 12.5, C["muted"], "start")
    cv.text_px(xt, 140 + 9 * 30, "彈性段比 Euler 打 0.877 折", 12.5, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-1-curve.svg")
    compose([cv], cols=1,
            title="圖 1　柱強度曲線：λc ≤ 1.5 用 0.658 的 λc² 次方，λc > 1.5 用 0.877/λc²，兩式在 1.5 相接",
            sub="λc = (KL/rπ)·√(Fy/E) 是 √(Fy/Fe)，把所有鋼材與細長比放在同一條無因次曲線上",
            note="分界取 1.5 不是 1.0；λc = 1 時 Fe = Fy，但仍在非彈性段",
            path=path)
    return path


def fig2_fy():
    W1, H1 = 1000, 560
    cv = Canvas(W1, H1, sx=1)
    cv.panel("同一根柱（KL/r 不變），Fy 350 → 450 MPa", f"λc 放大 √(450/350) = {Q_SHIFT:.3f} 倍；E = 200,000 MPa（示意）")
    X0, X1, YB, YT = 100, 640, 460, 110
    kmax, fmax = 200.0, 480.0
    PX = lambda k: X0 + (X1 - X0) * k / kmax
    PY = lambda f: YB - (YB - YT) * f / fmax
    _axes(cv, H1, X0, X1, YB, YT, [(v, PX(v)) for v in range(0, 201, 50)], [(v, PY(v)) for v in range(0, 481, 120)],
          "KL/r", "Fcr（MPa）")
    ks = [kmax * i / 300 for i in range(1, 301)]
    cv.poly([(PX(0), H1 - PY(Q_FY2))] + [(PX(k), H1 - PY(q_fcr(k, Q_FY2))) for k in ks], C["load"], 2.8)
    cv.poly([(PX(0), H1 - PY(Q_FY1))] + [(PX(k), H1 - PY(q_fcr(k, Q_FY1))) for k in ks], C["compr"], 2.8, dash="8 5")
    for fy, col in ((Q_FY1, C["compr"]), (Q_FY2, C["load"])):
        kb = Q_LC_B * math.pi / math.sqrt(fy / Q_E)
        _hl(cv, H1, PX(kb), YB, PX(kb), PY(q_fcr(kb, fy)), col, 1.0, dash="3 4")
        cv.text_px(PX(kb) + (-8 if fy > 400 else 8), YB - 12, f"{kb:.0f}", 11.5, col, "end" if fy > 400 else "start")
    cv.legend(X1 - 190, YT + 10, [(C["load"], "Fy = 450 MPa"), (C["compr"], "Fy = 350 MPa")], size=12, gap=19)
    xt = 690
    cv.text_px(xt, 140, "KL/r", 12.5, C["text"], weight="700")
    cv.text_px(xt + 90, 140, "350", 12.5, C["text"], weight="700")
    cv.text_px(xt + 165, 140, "450", 12.5, C["text"], weight="700")
    cv.text_px(xt + 240, 140, "比值", 12.5, C["text"], weight="700")
    for i, k in enumerate((10, 50, 80, 120, 160)):
        a, b = q_fcr(k, Q_FY1), q_fcr(k, Q_FY2)
        y = 172 + i * 30
        for c, v in enumerate((f"{k}", f"{a:.0f}", f"{b:.0f}", f"{b / a:.3f}")):
            cv.text_px(xt + [0, 90, 165, 240][c], y, v, 12.5, C["accent"] if c == 3 else C["text"])
    cv.text_px(xt - 30, 172 + 6 * 30, f"短柱：比值 → {Q_FY2 / Q_FY1:.3f}（= 450/350）", 12.5, C["muted"], "start")
    cv.text_px(xt - 30, 172 + 7 * 30, "中長柱：比值遞減", 12.5, C["muted"], "start")
    cv.text_px(xt - 30, 172 + 8 * 30, "彈性段：比值 = 1，與 Fy 無關", 12.5, C["accent"], "start", weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-fy.svg")
    compose([cv], cols=1,
            title="圖 2　提高 Fy：短柱強度幾乎等比例提高，細長柱（彈性段）完全沒有增加",
            sub="彈性段 Fcr = 0.877π²E/(KL/r)²，式中沒有 Fy",
            note="只看 Fcr/Fy 曲線會誤以為「比值不變所以強度等比例增加」；同一根柱的 λc 會右移",
            path=path)
    return path


def _mode_panel(title, sub, k, free_top, oy=110):
    W1, H1 = 500, 640
    L = 1.0
    cv = Canvas(W1, H1, sx=190, ox=W1 / 2 - 40, oy=oy)
    cv.panel(title, sub)
    a = 0.28
    if free_top:
        pts = [(a * (1 - math.cos(math.pi * t / 2)), L * t) for t in [i / 50 for i in range(51)]]
        cv.support((0, 0), "fixed", 0, size=22)
        cv.text((a, L), "自由端", 12.5, C["muted"], "start", dx=14, dy=14)
        cv.poly([(a * (1 - math.cos(math.pi * t / 2)), L * t) for t in [1 + i / 50 for i in range(51)]], C["ghost"], 1.6, dash="5 4")
        cv.text((a * 2, L * 1.6), "鏡射延伸：等同 2L 的鉸接柱", 11.5, C["muted"], "start", dx=10)
        top = (a, L)
    else:
        pts = [(a * math.sin(math.pi * t), L * t) for t in [i / 50 for i in range(51)]]
        cv.support((0, 0), "pin", 0, size=15)
        cv.support((0, L), "pin", 180, size=15)
        top = (0, L)
    cv.line((0, 0), (0, L), C["ghost"], 1.8, dash="6 5")
    cv.poly(pts, C["member"], 4)
    cv.arrow((top[0], top[1] + 0.28), (top[0], top[1] + 0.04), C["load"], 2.8, 10)
    cv.text((top[0], top[1] + 0.28), "P", 14, C["load"], "start", dx=8, weight="700")
    cv.dim((0, 0), (0, L), "L", off=-60, label_off=-16)
    cv.text_px(W1 / 2, H1 - 50, f"理論 K = {k:.1f}，KL = {k:.0f}L" if k != 1 else "理論 K = 1.0，KL = L", 14, C["accent"], weight="700")
    cv.text_px(W1 / 2, H1 - 26, f"Pe = π²EI/({k:g}L)² = {1 / k ** 2:g} × π²EI/L²", 12.5, C["muted"])
    return cv


def fig3_modes():
    p1 = _mode_panel("兩端鉸接", "半個正弦波，反曲點在兩端", 1.0, False, oy=200)
    p2 = _mode_panel("一端固接、一端自由", "四分之一正弦波，頂端側移", 2.0, True)
    path = os.path.join(OUT, f"{TAG}-fig-3-modes.svg")
    compose([p1, p2], cols=2,
            title="圖 3　挫屈變形與理論 K：鉸–鉸 K = 1.0，固–自由 K = 2.0（強度只剩 1/4）",
            sub="K = 兩反曲點（彎矩為零）間的距離 / L",
            note="懸臂柱頂端會側移，K 是 2.0 不是 0.5；0.5 是兩端固接的值",
            path=path)
    return path


FIGURES = [
    (fig1_curve, "§4 (一)、(二)",
     "兩式分界取 λc = 1.0；彈性段誤用 Euler 不乘 0.877；λc 推導漏掉 π"),
    (fig2_fy, "§4 (二)",
     "以為 Fy 提高強度就等比例提高；忽略彈性段與 Fy 無關"),
    (fig3_modes, "§4 (三)",
     "懸臂柱 K 寫成 0.5；挫屈形狀畫成對稱半波"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
