#!/usr/bin/env python3
"""
SS-2023-2 H 型鋼柱 ASD 挫屈型態判斷與彈性／非彈性交界柱長 — 解題圖解腳本

用法：
    python3 gen_SS-2023-2.py [輸出目錄]

本題考卷無附圖（題目正本 SS-2023-2-problem.md §3）；本腳本只產生解題圖解。
數值全部取自 SS-2023-2.md §4，由下式即時算出（單位 cm、tf/cm²）。
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", "skills", "struct-diagram", "scripts"))

from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "SS-2023-2"


# ── 解題圖解共用小工具（像素座標；y 由上往下）──
def _hl(cv, PH, x0, y0, x1, y1, color, w=2.0, dash=None):
    cv.line((x0, PH - y0), (x1, PH - y1), color, w, dash=dash, cap="butt")


# ══════════════════════════════════════════════════════════════
# 解題圖解（2026-11-03 補繪）——數值全部取自 SS-2023-2.md §4
# ══════════════════════════════════════════════════════════════
Q_L, Q_K = 650.0, 1.0
Q_RX, Q_RY = 17.0, 7.4
Q_FY, Q_E = 3.5, 2040.0
Q_CC = math.sqrt(2 * math.pi ** 2 * Q_E / Q_FY)       # 107.3
Q_SX, Q_SY = Q_K * Q_L / Q_RX, Q_K * Q_L / Q_RY      # 38.2、87.8
Q_LB = round(Q_CC, 1) * Q_RY / Q_K                   # 794（解析以 107.3 × 7.4）
Q_SX_B = Q_K * Q_LB / Q_RX                           # 46.7


def q_fa(klr):
    if klr >= Q_CC:
        return 12 * math.pi ** 2 * Q_E / (23 * klr ** 2)
    rr = klr / Q_CC
    return (1 - rr ** 2 / 2) * Q_FY / (5 / 3 + 3 * rr / 8 - rr ** 3 / 8)


def fig1_type():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("ASD 容許應力曲線：KL/r 與 Cc 比較決定公式", f"Cc = √(2π²E/Fy) = √(2π² × {Q_E:g} / {Q_FY}) = {Q_CC:.1f}")
    X0, X1, YB, YT = 100, 640, 440, 110
    kmax, fmax = 200.0, 2.2
    PX = lambda k: X0 + (X1 - X0) * k / kmax
    PY = lambda f: YB - (YB - YT) * f / fmax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 201, 50):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for i in range(0, 5):
        f = 0.5 * i
        if f <= fmax:
            cv.text_px(X0 - 8, PY(f), f"{f:.1f}", 11.5, C["muted"], "end")
            _hl(cv, H1, X0, PY(f), X1, PY(f), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "KL/r", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "Fa（tf/cm²）", 13, C["text"], "start", weight="700")
    ks = [kmax * i / 300 for i in range(0, 301)]
    cv.poly([(PX(k), H1 - PY(q_fa(k))) for k in ks if k <= Q_CC], C["bmd"], 3)
    cv.poly([(PX(k), H1 - PY(q_fa(k))) for k in ks if k >= Q_CC], C["compr"], 3)
    _hl(cv, H1, PX(Q_CC), YB, PX(Q_CC), YT, C["accent"], 1.4, dash="5 4")
    cv.text_px(PX(Q_CC) + 4, YT + 6, f"Cc = {Q_CC:.1f}", 12, C["accent"], "start", weight="700")
    cv.text_px(PX(50), YB - 20, "非彈性（Johnson 式）", 12.5, C["bmd"], weight="700")
    cv.text_px(PX(160), YB - 20, "彈性 12π²E/23(KL/r)²", 12.5, C["compr"], weight="700")
    for k, lab, col, dy in ((Q_SY, f"弱軸 {Q_SY:.1f}（控制）", C["load"], -14), (Q_SX, f"強軸 {Q_SX:.1f}", C["muted"], -14)):
        _hl(cv, H1, PX(k), YB, PX(k), PY(q_fa(k)), col, 1.1, dash="3 4")
        cv.dot((PX(k), H1 - PY(q_fa(k))), 6 if col == C["load"] else 4.5, fill=col)
        cv.text_px(PX(k) + 8, PY(q_fa(k)) + dy, lab, 12.5, col, "start", weight="700")
    xt = 680
    rows = [(f"KxL/rx = 650 / {Q_RX:g} = {Q_SX:.1f}", C["text"], "400"),
            (f"KyL/ry = 650 / {Q_RY:g} = {Q_SY:.1f}", C["text"], "400"),
            (f"控制 {Q_SY:.1f}（弱軸）", C["load"], "700"),
            ("", C["text"], "400"),
            (f"{Q_SY:.1f} 小於 Cc = {Q_CC:.1f}", C["bmd"], "700"),
            ("⇒ 非彈性挫屈，用 Johnson 式", C["bmd"], "700"),
            ("", C["text"], "400"),
            ("考卷三式未標範圍，須自行以 Cc 分界", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 140 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-1-type.svg")
    compose([cv], cols=1,
            title=f"圖 1　（一）弱軸 KL/r = {Q_SY:.1f} 小於 Cc = {Q_CC:.1f}：非彈性挫屈",
            sub="Kx = Ky = 1.0，L = 650 cm；兩軸各算、取大者",
            note="取強軸 38.2、或 Cc 代錯 Fy，都會判錯；彈性式只在 KL/r ≥ Cc 才能用",
            path=path)
    return path


def fig2_length():
    W1, H1 = 1000, 540
    cv = Canvas(W1, H1, sx=1)
    cv.panel("（二）KL/r 隨柱長 L 線性增加：弱軸先碰到 Cc", "KL/r = L / r（K = 1.0）")
    X0, X1, YB, YT = 100, 640, 440, 110
    lmax, smax = 1000.0, 140.0
    PX = lambda l: X0 + (X1 - X0) * l / lmax
    PY = lambda s: YB - (YB - YT) * s / smax
    _hl(cv, H1, X0, YB, X1, YB, C["muted"], 1.5)
    _hl(cv, H1, X0, YB, X0, YT, C["muted"], 1.5)
    for v in range(0, 1001, 200):
        cv.text_px(PX(v), YB + 18, f"{v}", 11.5, C["muted"])
    for v in range(0, 141, 20):
        cv.text_px(X0 - 8, PY(v), f"{v}", 11.5, C["muted"], "end")
        _hl(cv, H1, X0, PY(v), X1, PY(v), C["ghost"], 0.6, dash="2 4")
    cv.text_px((X0 + X1) / 2, YB + 42, "柱長 L（cm）", 13, C["text"], weight="700")
    cv.text_px(X0 - 4, YT - 18, "KL/r", 13, C["text"], "start", weight="700")
    cv.poly([(PX(0), H1 - PY(0)), (PX(lmax), H1 - PY(min(lmax / Q_RY, smax)))] if lmax / Q_RY <= smax else
            [(PX(0), H1 - PY(0)), (PX(smax * Q_RY), H1 - PY(smax))], C["load"], 2.8)
    cv.poly([(PX(0), H1 - PY(0)), (PX(lmax), H1 - PY(lmax / Q_RX))], C["compr"], 2.8)
    cv.text_px(PX(450) - 8, PY(450 / Q_RY) - 12, f"弱軸 L/{Q_RY:g}", 12.5, C["load"], "end", weight="700")
    cv.text_px(PX(450) + 4, PY(450 / Q_RX) + 22, f"強軸 L/{Q_RX:g}", 12.5, C["compr"], "start", weight="700")
    _hl(cv, H1, X0, PY(Q_CC), X1, PY(Q_CC), C["accent"], 1.4, dash="5 4")
    cv.text_px(X0 + 6, PY(Q_CC) - 10, f"Cc = {Q_CC:.1f}", 12, C["accent"], "start", weight="700")
    for l, s, col, lab in ((Q_L, Q_SY, C["muted"], f"L = 650：{Q_SY:.1f}"), (Q_LB, round(Q_CC, 1), C["bmd"], f"L = {Q_LB:.0f}：= Cc")):
        _hl(cv, H1, PX(l), YB, PX(l), PY(s), col, 1.2, dash="3 4")
        cv.dot((PX(l), H1 - PY(s)), 6, fill=col)
        cv.text_px(PX(l) + (8 if l > 700 else -8), PY(s) + (18 if l > 700 else -12), lab, 12.5, col, "start" if l > 700 else "end", weight="700")
    cv.dot((PX(Q_LB), H1 - PY(Q_SX_B)), 4.5, fill=C["compr"])
    cv.text_px(PX(Q_LB) + 8, PY(Q_SX_B) + 16, f"強軸 {Q_SX_B:.1f}", 12, C["compr"], "start")
    xt = 680
    rows = [(f"令 KyL/ry = Cc：", C["text"], "400"),
            (f"L = {Q_CC:.1f} × {Q_RY:g} = {Q_LB:.0f} cm", C["bmd"], "700"),
            (f"≈ {Q_LB / 100:.2f} m", C["bmd"], "700"),
            ("", C["text"], "400"),
            (f"此時強軸 {Q_LB:.0f}/{Q_RX:g} = {Q_SX_B:.1f}", C["text"], "400"),
            ("仍是非彈性 ⇒ 弱軸才是交界軸", C["muted"], "400")]
    for i, (s, col, wt) in enumerate(rows):
        if s:
            cv.text_px(xt, 150 + i * 32, s, 13, col, "start", weight=wt)
    path = os.path.join(OUT, f"{TAG}-fig-2-length.svg")
    compose([cv], cols=1,
            title=f"圖 2　（二）柱長改為 L = {Q_CC:.1f} × {Q_RY:g} = {Q_LB:.0f} cm（≈ {Q_LB / 100:.2f} m）時，弱軸恰在交界點",
            sub="ry 較小，弱軸的 KL/r 增加得快，先到達 Cc",
            note="用 rx 求 L（得 1,824 cm）會讓弱軸早已進入彈性段，交界點不在那裡",
            path=path)
    return path


FIGURES = [
    (fig1_type, "§4 一、二、三",
     "取強軸細長比；Cc 代錯；KL/r 小於 Cc 卻用彈性式"),
    (fig2_length, "§4 四",
     "用 rx 求交界柱長；忘了驗算另一軸"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, section, catches in FIGURES:
        print(f"{os.path.basename(fn()):<34} {section:<20} 攔：{catches}")
