#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2007-2 解題圖解（2026-11-15 圖解補繪，DIAG-RC-U3-B1）
數值全由常數區（取自解析正本 §4 Step 1–3 的輸入）現算，檔尾 check_solution() 對 §4 公佈值 assert。
用法：python figs/gen_RC-2007-2.py [輸出目錄，預設 figs]
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2007-2"

# ── 解析正本 §4 Step 1–3 的輸入（kgf, cm）──
FC, FY, ES = 280.0, 4200.0, 2.04e6
B, H, L = 30.0, 60.0, 800.0
D1 = 60 - (4 + 1.27 + 1.27); D2 = D1 - (2.54 + 2.5)          # 兩排拉力筋（假設）
AS1 = AS2 = 4 * 5.07; ASP, DP = 8.55, 6.5                       # 8-D25 兩排、3-D19
WD = 2.4 * 0.30 * 0.60 * 10 + 1.0                                # kgf/cm（自重＋0.1 tf/m）
WS = WD + 0.2 * 20.0; WT = WD + 20.0                             # D＋0.2L、D＋L

EC = 15000 * math.sqrt(FC); N = ES / EC
IG = B * H ** 3 / 12; MCR = 2 * math.sqrt(FC) * IG / (H / 2)
_a, _b = B / 2, (N - 1) * ASP + N * (AS1 + AS2)
_c = -((N - 1) * ASP * DP + N * (AS1 * D1 + AS2 * D2))
KD = (-_b + math.sqrt(_b * _b - 4 * _a * _c)) / (2 * _a)
ICR = B * KD ** 3 / 3 + (N - 1) * ASP * (KD - DP) ** 2 + N * (AS1 * (D1 - KD) ** 2 + AS2 * (D2 - KD) ** 2)


def ie(ma):                                    # 現行規範表 24.2.3.5（2/3 Mcr 式）
    t = (2 / 3) * MCR / ma
    return IG if t >= 1 else min(IG, ICR / (1 - t * t * (1 - ICR / IG)))


def delta(w):                                  # 簡支均布跨中即時撓度
    return 5 * w * L ** 4 / (384 * EC * ie(w * L * L / 8)) if w > 0 else 0.0


DD, DS, DT = delta(WD), delta(WS), delta(WT)
SUS_INC, LIVE = DS - DD, DT - DD
LIVE_DIRECT = 5 * (WT - WD) * L ** 4 / (384 * EC * ie(WT * L * L / 8))   # 舊解直接法（同一 Ie 下只算 L）
RHO_P = ASP / (B * (D1 + D2) / 2)
TOT1 = DT + 1.4 / (1 + 50 * RHO_P) * DS
TOT5 = DT + 2.0 / (1 + 50 * RHO_P) * DS


def fig1_curve():
    W, Hh = 1200, 600
    cv = Canvas(W, Hh, sx=1, bg="#FFFFFF")
    cv.text_px(W / 2, 32, f"{TAG} 圖 1　載重–跨中即時撓度曲線：差值法 vs 直接法", 17.5, weight="700")
    cv.text_px(W / 2, 57, "曲線由 Δ(w)＝5wL^{4}/(384 E_{c} I_{e}(w)) 逐點現算；I_{e} 隨載重水準下降，所以曲線上彎", 13, C["muted"])
    x0, y0, pw, ph = 100, 90, 560, 420          # 繪圖區（像素，y 向上）
    wmax, dmax = 28.0, 1.5
    X = lambda w: x0 + w / wmax * pw
    Y = lambda d: y0 + d / dmax * ph
    cv.line((x0, y0), (x0 + pw, y0), C["member"], 1.6)
    cv.line((x0, y0), (x0, y0 + ph), C["member"], 1.6)
    for w in range(0, 29, 4):
        cv.line((X(w), y0), (X(w), y0 - 6), C["member"], 1)
        cv.text((X(w), y0 - 20), f"{w}", 12, C["muted"])
    for k in range(0, 7):
        d = k * 0.25
        cv.line((x0, Y(d)), (x0 - 6, Y(d)), C["member"], 1)
        cv.text((x0 - 12, Y(d)), f"{d:.2f}", 12, C["muted"], anchor="end")
    cv.text((x0 + pw / 2, y0 - 46), "均布載重 w（kgf/cm）", 13, C["muted"])
    cv.text((x0 + 8, y0 + ph + 16), "跨中撓度 Δ（cm）", 13, C["muted"], anchor="start")
    pts = [(X(w), Y(delta(w))) for w in [i * 0.1 for i in range(1, 281)]]
    cv.poly(pts, C["deform"], 2.6)
    cv.line((X(0), Y(0)), (X(wmax), Y(5 * wmax * L ** 4 / (384 * EC * IG))), C["ghost"], 1.4, dash="6 5")
    cv.text((X(26.5), Y(5 * 26.5 * L ** 4 / (384 * EC * IG)) - 16), "全斷面 I_{g}", 12.5, C["muted"])
    for w, d, lab in ((WD, DD, "D"), (WS, DS, "D＋0.2L"), (WT, DT, "D＋L")):
        cv.line((X(w), y0), (X(w), Y(d)), C["dim"], 1, dash="3 3")
        cv.dot((X(w), Y(d)), 5.5, C["deform"])
        cv.text((X(w) - 10, Y(d) + 16), f"{lab}：{d:.3f}", 12.5, C["deform"], anchor="end")
    xb1, xb2, xb3 = X(WT) + 50, X(WT) + 120, X(WT) + 250
    cv.line((X(WD), Y(DD)), (xb3 + 10, Y(DD)), C["dim"], 1, dash="3 3")
    cv.line((X(WS), Y(DS)), (xb1 + 10, Y(DS)), C["dim"], 1, dash="3 3")
    cv.line((X(WT), Y(DT)), (xb2 + 10, Y(DT)), C["dim"], 1, dash="3 3")
    cv.double_arrow((xb1, Y(DD)), (xb1, Y(DS)), C["bmd"], 2, 8)
    cv.text((xb1 - 8, (Y(DD) + Y(DS)) / 2), f"㈡增量 {SUS_INC:.3f}", 12.5, C["bmd"], anchor="end")
    cv.double_arrow((xb2, Y(DD)), (xb2, Y(DT)), C["bmd"], 2.2, 8)
    cv.text((xb2 + 10, (Y(DD) + Y(DT)) / 2), f"㈢ {LIVE:.3f}", 14, C["bmd"], anchor="start", weight="700")
    cv.double_arrow((xb3, Y(DD)), (xb3, Y(DD + LIVE_DIRECT)), C["load"], 2, 8)
    cv.line((xb3 - 10, Y(DT)), (xb3 + 10, Y(DT)), C["bmd"], 1.4, dash="3 3")
    cv.text((xb3 + 10, (Y(DD) + Y(DD + LIVE_DIRECT)) / 2), f"直接法 {LIVE_DIRECT:.3f}", 13, C["load"], anchor="start")
    cv.text((xb3 + 10, Y(DD + LIVE_DIRECT) - 2), f"少 {LIVE - LIVE_DIRECT:.3f}", 12, C["load"], anchor="start")
    tx = 990
    rows = [("差值法（主線）", C["bmd"]),
            (f"㈠ Δ_{{D}}＝{DD:.3f} cm", C["text"]),
            (f"㈡ Δ_{{D+0.2L}}＝{DS:.3f} cm", C["text"]),
            (f"    增量 {SUS_INC:.3f} cm", C["text"]),
            (f"㈢ Δ_{{D+L}}−Δ_{{D}}＝{LIVE:.3f}", C["text"]),
            (f"㈣ 1 年 {TOT1:.2f} cm", C["text"]),
            (f"㈤ 5 年 {TOT5:.2f} cm", C["text"]),
            ("", C["text"]),
            ("直接法（舊解）：", C["load"]),
            ("把 L 單獨配 I_{e}(D+L)，", C["load"]),
            ("漏掉 D 部分因 I_{e} 下降", C["load"]),
            ("增加的撓度", C["load"])]
    for i, (s, col) in enumerate(rows):
        if s:
            cv.text_px(tx, 120 + i * 26, s, 13, col, "start", weight="700" if i in (0, 8) else "400")
    cv.text_px(W / 2, Hh - 24, f"E_{{c}}＝15000√f'c＝{EC:,.0f} kgf/cm²；I_{{cr}}＝{ICR:,.0f}；I_{{e}}：D {ie(WD*L*L/8):,.0f}、D＋0.2L {ie(WS*L*L/8):,.0f}、D＋L {ie(WT*L*L/8):,.0f}（cm^{{4}}）", 12.5, C["muted"])
    return cv.svg()


FIGURES = [("1-load-deflection", fig1_curve, "直接法（把部分載重單獨配 Ie）低估撓度；㈢ 必須用總撓度相減")]


def check_solution():
    for name, got, want, tol in [("Icr", ICR, 397629, 300), ("Ie_D", ie(WD * L * L / 8), 519606, 300),
                                 ("Ie_DL", ie(WT * L * L / 8), 401793, 300),
                                 ("㈠", DD, 0.218, 0.0015), ("㈡總", DS, 0.460, 0.0015), ("㈡增", SUS_INC, 0.242, 0.0015),
                                 ("㈢", LIVE, 1.121, 0.0015), ("㈣", TOT1, 1.84, 0.006), ("㈤", TOT5, 2.06, 0.006)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        p = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(p, "w", encoding="utf-8").write(fn()); print("寫出", p, "｜攔：", why)


if __name__ == "__main__":
    main()
