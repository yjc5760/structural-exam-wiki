#!/usr/bin/env python3
"""
RC-2015-3 T 形梁斷面（負彎矩）— 題目附圖重繪腳本

用法：python3 gen_RC-2015-3.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2015-3-problem.md §4 判讀清單（已確認）。
只畫考卷給的東西（外形與尺寸；考卷附圖沒有畫鋼筋），另以文字標出負彎矩受拉側（判讀 #4）。
FIGURES
  fig-1-problem  題目附圖重繪  攔：負彎矩時把翼板當受壓區
  fig-2-negative 負彎矩斷面／應變／內力  攔：壓力區寬取 bf = 100；拉力筋畫在底部；d 由翼板頂以外量起；未驗 A's 降伏
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2015-3"

# ── 判讀清單（RC-2015-3-problem.md §4，已確認）──
BF, TF = 100.0, 15.0       # #1 翼板寬 100、厚 15（在上方）
BW = 40.0                  # #2 腹寬 40
H = 70.0                   # #3 全高 70
#                            #4 負彎矩：上緣受拉、下緣受壓


def fig1_problem():
    W, Hc = 620, 520
    s = min(330 / BF, 330 / H)
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - BF * s / 2, oy=90)
    cv.panel("T 形斷面（重繪）", "依題目正本判讀清單 #1–#4；考卷附圖未畫鋼筋")
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    pts = [(x0, 0), (x1, 0), (x1, H - TF), (BF, H - TF), (BF, H), (0, H), (0, H - TF), (x0, H - TF), (x0, 0)]
    cv.polygon(pts, "#EDF1F6", C["member"], 2.6)
    cv.dim((0, H), (BF, H), f"{BF:.0f} cm", off=-30, label_off=-13)
    cv.dim((BF, H), (BF, H - TF), f"{TF:.0f} cm", off=-26, label_off=-30)
    cv.dim((0, H), (0, 0), f"{H:.0f} cm", off=50, label_off=30)
    cv.dim((x0, 0), (x1, 0), f"{BW:.0f} cm", off=30, label_off=14)
    cv.text((BF / 2, H - TF / 2), "上緣受拉（Mu 為負）", 13, C["tension"], weight="700")
    cv.text((BF / 2, 4), "下緣受壓", 13, C["compr"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（重繪）",
            sub="翼板 100 × 15 在上方、腹寬 40、全高 70 cm；Mu = −150 tf-m",
            note="負彎矩時翼板在受拉側，受壓區在腹板底部（寬 40 cm）",
            path=path)
    return path



# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-13 補繪）：由題給量現算，檔尾對 §4 公佈值 assert
# ══════════════════════════════════════════════════════════
import math
DP = 7.0                                   # 判讀 #5：拉力筋形心距頂面 7；壓力筋距底面 7（§4 採用）
D = H - DP
FC, FY, ES, ECU, MU = 350.0, 4200.0, 2.04e6, 0.003, 150.0
B1 = 0.85 - 0.05 * (FC - 280) / 70
ET = 0.004                                 # §4 以 εt = 0.004 上限設計
C_ = 3 / 7 * D
A_ = B1 * C_
PHI = round(0.65 + (ET - 0.002) * 0.25 / 0.003, 3)
CC = 0.85 * FC * A_ * BW
PMN1 = round(PHI * CC * (D - A_ / 2) / 1e5, 1)
EPSP = ECU * (C_ - DP) / C_
DMU = MU - PMN1
ASP = DMU * 1e5 / (PHI * (FY - 0.85 * FC) * (D - DP))
AS = CC / FY + ASP * (FY - 0.85 * FC) / FY


def fig2_negative():
    PW, PH = 440, 560
    sc = min((PW - 130) / BF, (PH - 230) / H)
    oy = 175
    # 斷面（翼板在上；負彎矩 → 上拉下壓）
    p1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - BF * sc / 2 - 34, oy=oy)
    p1.panel("斷面（負彎矩）", "拉力筋在翼板內、壓力區在腹板底")
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    pts = [(x0, 0), (x1, 0), (x1, H - TF), (BF, H - TF), (BF, H), (0, H), (0, H - TF), (x0, H - TF), (x0, 0)]
    p1.polygon(pts, "#EDF1F6", C["member"], 2.4)
    p1.polygon([(x0, 0), (x1, 0), (x1, A_), (x0, A_)], C["fill_c"], C["compr"], 2.0)
    for i in range(8):
        p1.dot((6 + (BF - 12) * i / 7, H - DP), 4.6, fill=C["tension"], stroke="#FFFFFF", w=1.2)
    for i in range(3):
        p1.dot((x0 + 6 + (BW - 12) * i / 2, DP), 4.6, fill=C["compr"], stroke="#FFFFFF", w=1.2)
    p1.line((x0 - 8, C_), (x1 + 8, C_), C["accent"], 1.6, dash="6 4")
    p1.text_px(p1.X(0), p1.Y(C_) - 12, f"N.A.（c = {C_:.0f}）", 12, C["accent"], "start", weight="700")
    p1.dim((x0, 0), (x0, A_), f"a = {A_:.1f}", off=-24, label_off=-40)
    p1.dim((BF, 0), (BF, H - DP), f"d = {D:.0f}", off=22, label_off=30)
    p1.dim((x0, 0), (x1, 0), f"b_{{w}} = {BW:.0f}", off=24, label_off=14)
    p1.text_px(p1.X(BF / 2), p1.Y(0) + 62, "受壓寬只有 b_{w}，不是 b_{f}", 12, C["compr"], weight="700")
    p1.text_px(p1.X(BF / 2), p1.Y(0) + 86, "d 由受壓面（底）量到頂層拉力筋", 11.5, C["muted"])
    p1.math_px(p1.X(BF / 2), p1.Y(H - DP) + 18, f"A_{{s}} = {AS:.2f}", 12.5, C["tension"], weight="700")
    p1.math_px(p1.X(x1) + 8, p1.Y(DP), f"A'_{{s}} = {ASP:.2f}", 12, C["compr"], "start", weight="700")
    # 應變（真實比例）
    K = 70 / sc / ET
    p2 = Canvas(PW, PH, sx=sc, ox=PW * 0.48, oy=oy)
    p2.panel("應變（真實比例）", "上緣受拉、下緣 εcu")
    p2.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
    p2.polygon([(0, 0), (ECU * K, 0), (0, C_)], C["fill_c"], C["compr"], 2.2)
    p2.polygon([(0, C_), (-ET * K, H - DP), (0, H - DP)], C["fill_t"], C["tension"], 2.2)
    p2.line((0, DP), (EPSP * K * (1 - 0) , DP), C["compr"], 2.4)
    p2.line(((FY / ES) * K, -2), ((FY / ES) * K, C_ + 2), C["accent"], 1.2, dash="3 3")
    p2.math_px(p2.X(ECU * K) + 6, p2.Y(0), "0.003", 12, C["compr"], "start", weight="700")
    p2.math_px(p2.X(EPSP * K) + 8, p2.Y(DP) - 12, f"ε'_{{s}} = {EPSP:.5f}", 12, C["compr"], "start", weight="700")
    p2.math_px(p2.X(-ET * K) - 6, p2.Y(H - DP) - 14, f"ε_{{t}} = {ET}", 12.5, C["tension"], "start", weight="700")
    p2.math_px(p2.X(FY / ES * K) + 4, p2.Y(C_) - 8, "ε_{y}", 11.5, C["accent"], "start")
    p2.line((-80 / sc, C_), (80 / sc, C_), C["accent"], 1.4, dash="6 4")
    p2.text_px(PW / 2, PH - 64, f"ε's 大於 εy：A's 降伏，取 fy − 0.85f'c", 12.5, C["muted"])
    p2.text_px(PW / 2, PH - 38, f"εt = 0.004 → φ = {PHI:.3f}", 13, C["accent"], weight="700")
    # 內力
    p3 = Canvas(PW, PH, sx=sc, ox=PW * 0.40, oy=oy)
    M = 64 / sc
    p3.panel("內力與彎矩分配", "C_c + C_s = T")
    p3.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
    p3.polygon([(0, 0), (M, 0), (M, A_), (0, A_)], C["fill_c"], C["compr"], 2.0)
    p3.arrow((M * 0.4, A_ / 2), (M * 1.5, A_ / 2), C["compr"], 3.0, 10)
    p3.math_px(p3.X(M * 1.5) + 6, p3.Y(A_ / 2), f"C_{{c}} = {CC/1000:.1f} t", 12.5, C["compr"], "start", weight="700")
    cs = ASP * (FY - 0.85 * FC)
    p3.arrow((0, DP), (M * 1.15, DP), C["compr"], 2.4, 9)
    p3.math_px(p3.X(M * 1.15) + 6, p3.Y(DP) + 12, f"C_{{s}} = {cs/1000:.1f} t", 12, C["compr"], "start", weight="700")
    p3.arrow((0, H - DP), (-M * 0.9, H - DP), C["tension"], 3.0, 10)
    p3.math_px(p3.X(-M * 0.45), p3.Y(H - DP) - 16, f"T = {AS*FY/1000:.1f} t", 12.5, C["tension"], weight="700")
    p3.text_px(PW / 2, PH - 90, f"φMn1（單筋上限）= {PMN1:.1f} tf·m", 12.5, C["muted"])
    p3.text_px(PW / 2, PH - 64, f"ΔMu = 150 − {PMN1:.1f} = {DMU:.1f} tf·m 由 A's 與 ΔAs 承擔", 12.5, C["muted"])
    p3.text_px(PW / 2, PH - 38, f"As = {AS:.2f}、A's = {ASP:.2f} cm²", 13, C["accent"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-negative.svg")
    compose([p1, p2, p3], title=f"{TAG}　負彎矩 T 形梁：翼板受拉，壓力只能靠 40 cm 腹板",
            sub=f"單筋上限 φMn1 = {PMN1:.1f} 小於 Mu = 150 tf·m → 腹板底加壓力筋（雙筋設計，εt = 0.004）",
            note="壓力區寬若誤取 bf = 100，單筋就看似足夠——負彎矩時翼板在受拉側，對強度沒有幫助",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "負彎矩時把翼板當受壓區"),
           (fig2_negative, "§4 Step 1–4", "壓力區寬取 bf；未驗 A's 降伏")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2015-3.md §4 公佈值核對
    assert (round(C_, 2), round(A_, 2), round(CC)) == (27.0, 21.6, 257040) and PHI == 0.817
    assert PMN1 == 109.6 and round(EPSP, 5) == 0.00222
    assert round(ASP, 2) == 22.63 and round(AS, 2) == 82.22
    print("assert OK")
