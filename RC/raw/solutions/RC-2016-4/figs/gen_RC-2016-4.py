#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC-2016-4 題目附圖重繪腳本（-problem.svg）

依題目正本 RC-2016-4-problem.md §4 判讀清單（已確認）作圖；只畫考卷給的東西，不含解題結果。
用法：python figs/gen_RC-2016-4.py [輸出目錄，預設 figs]
（2026-11-15，RC-U4-2+U4-3+U4-4 批 1 題目正本推廣）
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR",
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else "figs"
TAG = "RC-2016-4"


# ── 題目附圖重繪共用小工具（各 gen 檔內聯一份）──
def _rect(cv, x0, y0, x1, y1, fill="#EDF1F6", stroke=None, w=2.4, dash=None):
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    if fill:
        cv.polygon(pts, fill)
    cv.poly(pts, stroke or C["member"], w, dash=dash)


def _curve(cv, f, x0, x1, color, w=2.6, dash=None, n=80):
    cv.poly([(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)], color, w, dash=dash)


TENDON = "#B45309"


# ── 題目附圖重繪（題目正本 RC-2016-4-problem.md §4）──
B, H = 20.0, 60.0      # #1 斷面 20×60
YC = H - 30.0          # #2 形心距頂 30（虛點線）
E = 15.0               # #3 鋼鍵在形心下 15
PW, PH = 560, 520


def panel_sec():
    cv = Canvas(PW, PH, sx=6.2, ox=218, oy=70)
    _rect(cv, 0, 0, B, H)
    cv.line((-6, YC), (B + 6, YC), C["muted"], 1.4, dash="8 3 2 3")
    cv.text((B / 2, YC + 2.4), "斷面中心", 12, color=C["muted"])
    cv.circle((B / 2, YC - E), 1.3, fill=TENDON, stroke=TENDON, w=1)
    cv.math((B / 2 + 2.2, YC - E + 2.6), "A_{ps}", 15, anchor="start")
    cv.dim((0, H), (B, H), "20 cm", off=-28, label_off=-14)
    cv.dim((0, H), (0, YC), "30 cm", off=32, label_off=26)
    cv.dim((0, YC), (0, YC - E), "15 cm", off=32, label_off=26)
    cv.dim((B, 0), (B, H), "60 cm", off=40, label_off=30)
    cv.text((B / 2, -5.5), "預力梁斷面（跨度、自重考卷未給）", 12.5, color=C["muted"])
    return cv


def fig1_problem():
    return compose([panel_sec()], title=f"{TAG} 題目附圖重繪",
                   sub="依題目正本判讀清單 #1–#3",
                   note="鋼鍵偏心 15 cm 量自斷面中心（形心）")


FIGURES = [("1-problem", fig1_problem, "15 cm 當成距底面；偏心量錯取 30 或 45")]


# ══ 解題圖解（2026-11-15 圖解補繪 DIAG-RC-U4-2-B1；數值由常數現算，檔尾對 §4 assert）══
Q16_B, Q16_H, Q16_E = 20.0, 60.0, 15.0               # 斷面 cm、偏心（中心以下）
Q16_APS, Q16_FPU, Q16_FC, Q16_N = 3.95, 19000.0, 350.0, 6.0
Q16_FCI = 0.7 * Q16_FC; Q16_FPI = 0.7 * Q16_FPU
Q16_A = Q16_B * Q16_H; Q16_I = Q16_B * Q16_H ** 3 / 12; Q16_Y = Q16_H / 2
Q16_PI = Q16_FPI * Q16_APS
Q16_FCPA = Q16_PI / Q16_A + Q16_PI * Q16_E ** 2 / Q16_I
Q16_DF = Q16_N * Q16_FCPA
Q16_PE = (Q16_FPI - Q16_DF) * Q16_APS
Q16_FT = Q16_PE / Q16_A - Q16_PE * Q16_E * Q16_Y / Q16_I   # 頂（壓為正）
Q16_FB = Q16_PE / Q16_A + Q16_PE * Q16_E * Q16_Y / Q16_I
Q16_FR = 2.0 * math.sqrt(Q16_FCI); Q16_T1 = 0.8 * math.sqrt(Q16_FCI); Q16_T2 = 1.6 * math.sqrt(Q16_FCI)
Q16_CA = 0.60 * Q16_FCI
Q16_Z = -Q16_FT / (Q16_FB - Q16_FT) * Q16_H               # 受拉區深
Q16_TT = 0.5 * (-Q16_FT) * Q16_Z * Q16_B                  # 受拉區總拉力 kgf
Q16_W, Q16_HP = 760, 420


def panel_q16():
    cv = Canvas(Q16_W, Q16_HP)
    cv.panel("初施預力彈性收縮後的斷面應力（kgf/cm^{2}，壓為正）")
    sy, top = 4.3, 318                                    # px/cm、頂緣 y（y 向上）
    def Yd(d): return top - sy * d                        # d：自頂向下 cm
    x0s = 70
    cv.polygon([(x0s, Yd(0)), (x0s + Q16_B * 3.5, Yd(0)), (x0s + Q16_B * 3.5, Yd(Q16_H)), (x0s, Yd(Q16_H))], "#EDF1F6", stroke=C["member"], w=2)
    cv.line((x0s - 6, Yd(Q16_Y)), (x0s + Q16_B * 3.5 + 6, Yd(Q16_Y)), C["member2"], 1, dash="8 3 2 3")
    cv.dot((x0s + Q16_B * 1.75, Yd(Q16_Y + Q16_E)), 6, fill=C["load"])
    cv.text((x0s + Q16_B * 1.75, Yd(Q16_Y + Q16_E) - 16), f"e＝{Q16_E:.0f}", 12, color=C["load"], weight="700")
    cv.text((x0s + Q16_B * 1.75, Yd(-5)), f"{Q16_B:.0f}×{Q16_H:.0f}", 12, color=C["muted"])
    x0, sx = 390, 2.35                                     # 應力 0 的 x、px per kgf/cm²
    def X(f): return x0 + sx * f
    cv.line((X(0), Yd(-4)), (X(0), Yd(Q16_H + 4)), C["member"], 1.4)
    cv.polygon([(X(0), Yd(0)), (X(Q16_FT), Yd(0)), (X(0), Yd(Q16_Z))], C["fill_t"], stroke=C["tension"], w=1.6)
    cv.polygon([(X(0), Yd(Q16_Z)), (X(Q16_FB), Yd(Q16_H)), (X(0), Yd(Q16_H))], C["fill_c"], stroke=C["compr"], w=1.6)
    cv.text((X(Q16_FT), Yd(-5)), f"頂 {Q16_FT:.2f}", 13, color=C["tension"], anchor="middle", weight="700")
    cv.text((X(Q16_FB) + 6, Yd(Q16_H) - 2), f"底 +{Q16_FB:.2f}", 13, color=C["compr"], anchor="start", weight="700")
    cv.text((X(0) + 8, Yd(Q16_Z / 2)), f"受拉區 {Q16_Z:.1f} cm，T＝{Q16_TT/1000:.2f} tf → 握裹輔助鋼筋", 12, color=C["tension"], anchor="start", weight="700")
    for f, lab, col, dash, dl in ((-Q16_FR, f"f_{{r}}＝{Q16_FR:.2f}（開裂）", C["member2"], "6 3", 19),
                                  (-Q16_T2, f"簡支端部 1.6√f'ci＝{Q16_T2:.2f}", C["accent"], "3 3", 23.5),
                                  (-Q16_T1, f"一般 0.8√f'ci＝{Q16_T1:.2f}", C["load"], None, 28)):
        cv.line((X(f), Yd(-1)), (X(f), Yd(dl - 1.5)), col, 2, dash=dash)
        cv.text((X(f) + 3, Yd(dl)), lab, 11.5, color=col, anchor="end", weight="700")
    cv.line((X(Q16_CA), Yd(44)), (X(Q16_CA), Yd(Q16_H + 2)), C["compr"], 2, dash="6 3")
    cv.text((X(Q16_CA) - 4, Yd(42)), f"0.60f'ci＝{Q16_CA:.0f}", 11.5, color=C["compr"], anchor="end")
    cv.text_px(Q16_W / 2, Q16_HP - 46, f"Δf_{{pES}}＝n·f_{{cpa}}＝{Q16_N:.0f}×{Q16_FCPA:.2f}＝{Q16_DF:.1f}；P＝{Q16_PE/1000:.2f} tf", 13, color=C["text"], weight="700")
    cv.text_px(Q16_W / 2, Q16_HP - 22, f"不開裂（{-Q16_FT:.2f}＜{Q16_FR:.2f}）、受壓未過多（{Q16_FB:.2f}＜{Q16_CA:.0f}），但頂拉超過一般限值 {Q16_T1:.2f}", 12.5, color=C["load"], weight="700")
    return cv


def fig2_stress():
    return compose([panel_q16()],
                   title=f"{TAG} 圖 2　彈性收縮後應力分布與現行限值",
                   sub="f'ci＝0.7f'c＝245 kgf/cm2；kgf 制傳遞拉 0.8√f'ci（簡支端部 1.6√f'ci）；fr 只判開裂，不是容許值",
                   note="攔：只比破裂模數就下「斷面安全」；漏傳遞拉應力限值與握裹輔助鋼筋")


def check_solution():
    for name, got, want, tol in [("df", Q16_DF, 459.7, 0.05), ("ft", Q16_FT, -21.13, 0.005), ("fb", Q16_FB, 105.67, 0.005),
                                 ("fr", Q16_FR, 31.30, 0.006), ("t1", Q16_T1, 12.52, 0.005), ("t2", Q16_T2, 25.04, 0.005),
                                 ("z", Q16_Z, 10.0, 0.05), ("T", Q16_TT / 1000, 2.11, 0.006), ("ca", Q16_CA, 147.0, 1e-9)]:
        assert abs(got - want) <= tol, (name, got, want)
    print("check_solution：§4 對帳全過")


FIGURES.append(("2-stress", fig2_stress, "只比 f_r；漏傳遞拉應力限值"))


def main():
    check_solution()
    os.makedirs(OUT, exist_ok=True)
    for name, fn, why in FIGURES:
        path = os.path.join(OUT, f"{TAG}-fig-{name}.svg")
        open(path, "w", encoding="utf-8").write(fn())
        print("寫出", path, "｜攔：", why)


if __name__ == "__main__":
    main()
