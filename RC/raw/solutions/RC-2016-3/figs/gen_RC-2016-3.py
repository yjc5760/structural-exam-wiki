#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2016-3 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U3-3-B2）
數值由常數現算（現行規範：C_m＝0.6－0.4M_1/M_2 無 0.4 下限、δns≥1.0），檔尾 check_solution() 對解析 §4 assert。
用法：python figs/gen_RC-2016-3.py [輸出目錄，預設 figs]
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2016-3"

# ── 題目給定（題目正本 §1）──
B, LU, K, PU, M1, M2 = 40.0, 800.0, 0.9, 130.0, 35.0, 40.0
EC = 15000 * math.sqrt(280.0)
EI = 0.25 * EC * B ** 4 / 12
PC = math.pi ** 2 * EI / (K * LU) ** 2 / 1000          # §4 Step 4（tf）
RAT = +M1 / M2                                          # 雙曲度：現行慣例為正
CM = 0.6 - 0.4 * RAT                                    # §4 Step 5（無下限）
X0 = PU / (0.75 * PC)
D_RAW = CM / (1 - X0); D_NEW = max(1.0, D_RAW)
D_OLD = max(1.0, max(0.4, CM) / (1 - X0))               # 考卷舊式 C_m≥0.4（§5 對照）
MC_NEW, MC_OLD = D_NEW * M2, D_OLD * M2
X_CROSS = 1 - CM                                        # C_m＝0.25 時 δ 計算值＝1 的軸力比
PU_CROSS = 0.75 * PC * X_CROSS
KLR, LIM = K * LU / (0.3 * B), min(40.0, 34 + 12 * RAT)
W, H = 520, 520


def panel_bmd():
    cv = Canvas(W, H, sx=0.42, ox=250, oy=100)
    cv.panel("① 雙曲度：端彎矩反向、柱中反曲")
    k = 3.2
    xi = M2 / (M1 + M2)                                  # 反曲點距 M_2 端
    y0 = LU * (1 - xi)                                   # M_2 在柱頂
    pts = [(0, LU), (M2 * k, LU), (0, y0), (-M1 * k, 0), (0, 0)]
    cv.polygon([(0, LU), (M2 * k, LU), (0, y0)], C["fill_m"]); cv.polygon([(0, y0), (-M1 * k, 0), (0, 0)], C["fill_m"])
    cv.poly([(0, LU), (M2 * k, LU), (-M1 * k, 0), (0, 0)], C["bmd"], 2.4)
    cv.line((0, -10), (0, LU + 10), C["member"], 4, cap="butt")
    cv.dot((0, y0), 6, fill="#FFFFFF", stroke=C["accent"], w=2.6)
    cv.text((-14, y0), f"反曲點（距 M_2 端 {xi*LU:.0f} cm）", 12, color=C["accent"], anchor="end")
    cv.text((M2 * k + 6, LU + 22), f"M_2＝{M2:.0f}", 13, color=C["bmd"], weight="700", anchor="end")
    cv.text((-M1 * k - 4, -24), f"M_1＝{M1:.0f}", 13, color=C["bmd"], weight="700", anchor="start")
    xs = 300
    cv.line((xs, 0), (xs, LU), C["ghost"], 2, dash="6 5")
    cv.poly([(xs + 40 * math.sin(2 * math.pi * i / 60) * (1 if True else 1), LU * i / 60) for i in range(61)], C["deform"], 3)
    cv.text((xs, -26), "S 形變形（示意）", 12, color=C["deform"])
    cv.text_px(260, 454, f"現行慣例雙曲率 M_1/M_2＝＋{RAT:.3f}", 12.5, color=C["text"])
    cv.text_px(260, 478, f"C_m＝0.6－0.4×{RAT:.3f}＝{CM:.2f}（無 0.4 下限）", 13, color=C["load"], weight="700")
    cv.text_px(260, 500, f"kℓu/r＝{KLR:.0f} ＞ min(44.5, 40)＝{LIM:.0f} → 細長", 12, color=C["muted"])
    return cv


def panel_delta():
    cv = Canvas(W, H)
    cv.panel("② δns 與軸力比：C_m 下限的差別")
    L_, R_, T_, B_ = 70, 30, 70, 90
    xmax, ymax = 0.9, 2.0
    X = lambda x: L_ + (W - L_ - R_) * x / xmax
    Y = lambda y: H - B_ - (H - T_ - B_) * y / ymax
    for gx in (0, 0.2, 0.4, 0.6, 0.8):
        cv.text_px(X(gx), H - B_ + 18, f"{gx:.1f}", 11.5, color=C["muted"])
    for gy in (0, 0.5, 1.0, 1.5, 2.0):
        cv.text_px(L_ - 10, Y(gy), f"{gy:.1f}", 11.5, color=C["muted"], anchor="end")
    S = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}" {}/>'
    def L2(x0, y0, x1, y1, col, w=2, dash=None):
        cv.parts.append(S.format(x0, y0, x1, y1, col, w, f'stroke-dasharray="{dash}"' if dash else ""))
    L2(X(0), Y(0), X(xmax), Y(0), C["member"], 1.6); L2(X(0), Y(0), X(0), Y(ymax), C["member"], 1.6)
    L2(X(0), Y(1), X(xmax), Y(1), C["muted"], 1.4, "5 4")
    cv.text_px(X(0.02), Y(1) - 10, "δns≥1.0", 11.5, color=C["muted"], anchor="start")
    def curve(cm, col, dash=None):
        pts = []
        for i in range(181):
            x = xmax * i / 180
            y = cm / (1 - x)
            if y > ymax: break
            pts.append(f"{X(x):.1f},{Y(y):.1f}")
        cv.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="2.8" {"stroke-dasharray=" + chr(34) + dash + chr(34) if dash else ""}/>')
    curve(CM, C["deform"]); curve(0.4, C["member2"], "7 5")
    L2(X(X0), Y(0), X(X0), Y(ymax), C["accent"], 1.6, "3 4")
    cv.text_px(X(X0) - 6, Y(ymax) + 12, f"本題 P_u/0.75P_c＝{X0:.3f}", 12, color=C["accent"], anchor="end")
    def DOT(x, y, r, fill, stroke="#FFFFFF", w=1.6):
        cv.parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>')
    DOT(X(X0), Y(D_RAW), 5, C["deform"]); DOT(X(X0), Y(D_NEW), 6, C["load"]); DOT(X(X0), Y(D_OLD), 5, C["member2"])
    cv.text_px(X(X0) - 8, Y(D_RAW) + 4, f"計算值 {D_RAW:.2f}", 12, color=C["deform"], anchor="end")
    cv.text_px(X(X0) - 8, Y(D_NEW) - 12, f"取 1.0 → M_c＝{MC_NEW:.1f}", 12.5, color=C["load"], anchor="end", weight="700")
    cv.text_px(X(X0) - 8, Y(D_OLD) - 8, f"舊式 C_m＝0.4：{D_OLD:.3f} → {MC_OLD:.1f}", 12, color=C["member2"], anchor="end")
    DOT(X(X_CROSS), Y(1), 4.5, "#FFFFFF", C["deform"], 2)
    L2(X(X_CROSS), Y(1), X(X_CROSS), Y(0), C["deform"], 1.2, "2 4")
    cv.text_px(X(X_CROSS) - 4, Y(0.16), f"{X_CROSS:.2f}（P_u＝{PU_CROSS:.1f} tf）", 11.5, color=C["deform"], anchor="end")
    cv.text_px(X(X_CROSS) - 4, Y(0.07), "起 δ 計算值才＞1", 11.5, color=C["deform"], anchor="end")
    cv.text_px(X(0.12), Y(0.25) + 2, f"C_m＝{CM:.2f}（現行）", 12, color=C["deform"], anchor="start")
    cv.text_px(X(0.12), Y(0.48) - 8, "C_m＝0.4（舊下限）", 12, color=C["member2"], anchor="start")
    cv.text_px((L_ + W - R_) / 2, H - B_ + 40, "P_u／(0.75P_c)", 12.5, color=C["text"])
    cv.text_px((L_ + W - R_) / 2, H - 22, f"P_c＝{PC:.1f} tf；δns＝C_m／(1－P_u/0.75P_c)", 12, color=C["muted"])
    return cv


def fig1_magnifier():
    return compose([panel_bmd(), panel_delta()], title=f"{TAG} 圖 1　雙曲度 Cm 與 δns≥1.0（現行無 0.4 下限）",
                   sub=f"Pu＝{PU:.0f} tf、EI＝0.25EcIg、kℓu＝{K*LU:.0f} cm；單位 tf·m",
                   note=f"現行主線 Mc＝{MC_NEW:.1f} tf·m；照考卷舊式 Cm≥0.4 為 {MC_OLD:.1f}（§5 對照）")


FIGURES = [("1-magnifier", fig1_magnifier, "雙曲度仍取 C_m≥0.4；忘記 δns≥1.0；細長比限值未套 40")]


def check_solution():
    for name, got, want, tol in [("Pc", PC, 254.9, 0.05), ("Cm", CM, 0.25, 1e-9), ("x", X0, 0.680, 6e-4),
                                 ("d_raw", D_RAW, 0.78, 0.005), ("Mc", MC_NEW, 40.0, 1e-9), ("old", MC_OLD, 50.0, 0.05),
                                 ("Pu cross", PU_CROSS, 143.4, 0.1), ("klr", KLR, 60, 1e-9), ("lim", LIM, 40, 1e-9)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
