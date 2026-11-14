#!/usr/bin/env python3
"""
RC-2002-4 雙筋矩形梁斷面 — 題目附圖重繪腳本

用法：python3 gen_RC-2002-4.py [輸出目錄]（預設 figs/）
重繪依據：題目正本 RC-2002-4-problem.md §4 判讀清單（已確認）。
只畫考卷給的東西（外形、A's、As 位置與尺寸），不含任何解題結果。
FIGURES
  fig-1-problem  題目附圖重繪          攔：把 60 cm 當全高、或把 d' 量到梁底
  fig-2-strain   斷面／應變／內力三聯圖 攔：壓力筋未驗降伏；εt 落在 0.004–0.005 仍取 φ = 0.9（答 Mn 或 0.9Mn）
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2002-4"

# ── 判讀清單（RC-2002-4-problem.md §4，已確認）──
B, H = 30.0, 70.0          # #2 寬 30、全高 70
D_TOP_AS = 60.0            # #3 頂面到 As 形心 60
D_TOP_ASP = 7.0            # #4 頂面到 A's 形心 7（7 + 53 = 60）


def fig1_problem():
    W, Hc = 520, 560
    s = min(220 / B, 380 / H)
    cv = Canvas(W, Hc, sx=s, ox=W / 2 - B * s / 2 - 20, oy=80)
    cv.panel("梁斷面（重繪）", "依題目正本判讀清單 #2–#5；鋼筋各畫一圈（考卷未給根數）")
    cv.polygon([(0, 0), (B, 0), (B, H), (0, H), (0, 0)], "#EDF1F6", C["member"], 2.6)
    yp, ys = H - D_TOP_ASP, H - D_TOP_AS
    cv.circle((B / 2, yp), 1.6, fill="#FFFFFF", stroke=C["member"], w=2)
    cv.circle((B / 2, ys), 1.6, fill="#FFFFFF", stroke=C["member"], w=2)
    cv.text((B / 2, yp), "A's", 15, C["text"], dy=24, weight="700")
    cv.text((B / 2, ys), "As", 15, C["text"], dy=-24, weight="700")
    for y in (yp, ys):
        cv.line((B / 2 + 2.2, y), (B + 3, y), C["ghost"], 1.2, dash="4 3")
    cv.dim((0, H), (0, 0), f"{H:.0f} cm", off=36, label_off=26)
    cv.dim((0, 0), (B, 0), f"{B:.0f} cm", off=30, label_off=14)
    cv.dim((B, H), (B, yp), f"{D_TOP_ASP:.0f} cm", off=-30, label_off=-30)
    cv.dim((B, yp), (B, ys), f"{D_TOP_AS - D_TOP_ASP:.0f} cm", off=-30, label_off=-30)
    cv.dim((B, H), (B, ys), f"{D_TOP_AS:.0f} cm", off=-80, label_off=-30)
    path = os.path.join(OUT, f"{TAG}-fig-1-problem.svg")
    compose([cv], title=f"{TAG} 題目附圖（重繪）",
            sub="右側尺寸：頂面 → A's 7 cm、A's → As 53 cm、頂面 → As 60 cm",
            note="60 cm 量到 As 形心（d），不是全高；全高 70 cm",
            path=path)
    return path


# ══════════════════════════════════════════════════════════
# 解題圖解（2026-11-13 補繪）：數值一律由題給量現算，檔尾對 §4 公佈值 assert
# ══════════════════════════════════════════════════════════
import math
FC, FY, ES, ECU = 350.0, 4200.0, 2.04e6, 0.003       # 題目正本 §1
AS, ASP = 50.70, 10.14
EPSY = FY / ES
B1 = 0.85 - 0.05 * (FC - 280) / 70                   # §4 β1 = 0.80
CS = ASP * (FY - 0.85 * FC)                           # 假設 A's 降伏，扣除被取代混凝土
A_ = round((AS * FY - CS) / (0.85 * FC * B), 2)       # §4 a（公佈兩位）
C_ = round(A_ / B1, 2)                                # §4 c
EPSP = ECU * (C_ - D_TOP_ASP) / C_                    # ε's
EPST = ECU * (D_TOP_AS - C_) / C_                     # εt（dt = d）
PHI = round(0.65 + (EPST - 0.002) * 0.25 / 0.003, 3)   # §4 公佈 0.851（後續以此乘 Mn）
CC = 0.85 * FC * A_ * B
MN = CC * (D_TOP_AS - A_ / 2) + CS * (D_TOP_AS - D_TOP_ASP)
T_ = AS * FY


def fig2_strain():
    PW, PH = 330, 470
    sc = (PH - 175) / H
    oy = 86
    # 斷面
    p1 = Canvas(PW, PH, sx=sc, ox=PW / 2 - B * sc / 2 + 34, oy=oy)
    p1.panel("斷面", f"b × h = {B:.0f} × {H:.0f} cm")
    p1.polygon([(0, 0), (B, 0), (B, H), (0, H)], "#EDF1F6", C["member"], 2.6)
    for x in (B * 0.25, B * 0.5, B * 0.75):
        p1.dot((x, H - D_TOP_ASP), 5.2, fill=C["compr"], stroke="#FFFFFF", w=1.4)
        p1.dot((x, H - D_TOP_AS), 5.6, fill=C["tension"], stroke="#FFFFFF", w=1.4)
    p1.line((-6, H - C_), (B + 6, H - C_), C["accent"], 1.8, dash="6 4")
    p1.text_px(p1.X(B) + 10, p1.Y(H - C_) - 10, "N.A.", 12, C["accent"], "start", weight="700")
    p1.math_px(p1.X(B / 2), p1.Y(H - D_TOP_ASP) + 18, "A'_{s} = 10.14", 12.5, C["compr"], weight="700")
    p1.math_px(p1.X(B / 2), p1.Y(H - D_TOP_AS) - 17, "A_{s} = 50.70", 12.5, C["tension"], weight="700")
    p1.dim((0, H), (0, H - C_), f"c = {C_:.2f}", off=34, label_off=34)
    p1.dim((0, H - C_), (0, H - D_TOP_AS), f"{D_TOP_AS - C_:.2f}", off=34, label_off=26)
    # 應變（水平比例 = 真實應變比例）
    K = 82 / sc / max(ECU, EPST)
    p2 = Canvas(PW, PH, sx=sc, ox=PW * 0.50, oy=oy)
    p2.panel("應變（真實比例）", "虛線＝ε_y；黃框＝0.004～0.005")
    p2.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
    p2.polygon([(0, H), (ECU * K, H), (0, H - C_)], C["fill_c"], C["compr"], 2.2)
    p2.polygon([(0, H - C_), (-EPST * K, H - D_TOP_AS), (0, H - D_TOP_AS)], C["fill_t"], C["tension"], 2.2)
    p2.polygon([(-0.004 * K, H - D_TOP_AS - 3), (-0.005 * K, H - D_TOP_AS - 3),
                (-0.005 * K, H - D_TOP_AS + 3), (-0.004 * K, H - D_TOP_AS + 3)], "rgba(180,83,9,0.15)", C["accent"], 1.2)
    for s in (EPSY, -EPSY):
        p2.line((s * K, H + 2), (s * K, 2), C["accent"], 1.2, dash="3 3")
    p2.line((0, H - D_TOP_ASP), (EPSP * K, H - D_TOP_ASP), C["compr"], 2.6)
    p2.dot((EPSP * K, H - D_TOP_ASP), 4.2, fill=C["compr"])
    p2.math_px(p2.X(ECU * K) + 6, p2.Y(H) - 2, "0.003", 12, C["compr"], "start", weight="700")
    p2.math_px(p2.X(EPSP * K) + 8, p2.Y(H - D_TOP_ASP) + 14, f"ε'_{{s}} = {EPSP:.6f}", 11.5, C["compr"], "start", weight="700")
    p2.math_px(p2.X(-EPST * K) - 6, p2.Y(H - D_TOP_AS) + 36, f"ε_{{t}} = {EPST:.5f}", 12, C["tension"], "start", weight="700")
    p2.math_px(p2.X(EPSY * K) + 4, p2.Y(4), f"ε_{{y}} = {EPSY:.6f}", 11, C["accent"], "start")
    p2.line((-90 / sc, H - C_), (90 / sc, H - C_), C["accent"], 1.4, dash="6 4")
    # 內力
    p3 = Canvas(PW, PH, sx=sc, ox=PW * 0.36, oy=oy)
    M = 70 / sc
    p3.panel("內力", "C_c + C_s = T")
    p3.line((0, 0), (0, H), C["ghost"], 2, dash="5 4")
    p3.polygon([(0, H), (M, H), (M, H - A_), (0, H - A_)], C["fill_c"], C["compr"], 2.2)
    p3.dim((0, H), (0, H - A_), f"a = {A_:.2f}", off=26, label_off=30)
    p3.arrow((M * 0.4, H - A_ / 2), (M * 1.45, H - A_ / 2), C["compr"], 3.0, 10)
    p3.math_px(p3.X(M * 1.45) + 6, p3.Y(H - A_ / 2), f"C_{{c}} = {CC/1000:.1f} t", 12.5, C["compr"], "start", weight="700")
    p3.arrow((0, H - D_TOP_ASP), (M * 1.2, H - D_TOP_ASP), C["compr"], 2.4, 9)
    p3.math_px(p3.X(M * 1.2) + 6, p3.Y(H - D_TOP_ASP) - 2, f"C_{{s}} = {CS/1000:.1f} t", 12, C["compr"], "start", weight="700")
    p3.arrow((0, H - D_TOP_AS), (-M * 0.9, H - D_TOP_AS), C["tension"], 3.0, 10)
    p3.math_px(p3.X(-M * 0.5), p3.Y(H - D_TOP_AS) - 16, f"T = {T_/1000:.1f} t", 12.5, C["tension"], weight="700")
    p3.text_px(PW / 2, PH - 62, f"εt = {EPST:.5f}：過渡區", 13, C["accent"], weight="700")
    p3.text_px(PW / 2, PH - 38, f"φ = {PHI:.3f}（不是 0.90）", 13, C["accent"], weight="700")
    path = os.path.join(OUT, f"{TAG}-fig-2-strain.svg")
    compose([p1, p2, p3], title=f"{TAG}　壓力筋降伏、拉力筋落在過渡區",
            sub=f"Mn = {MN/1e5:.1f} tf·m　→　φMn = {PHI:.3f} × {MN/1e5:.1f} = {PHI*MN/1e5:.1f} tf·m",
            note="ε's 剛超過 εy（壓力筋可取 fy）；εt 介於 0.004 與 0.005 之間，φ 須依 εt 內插",
            path=path)
    return path


FIGURES = [(fig1_problem, "§1（題目正本 §4）", "把 60 cm 當全高；d' 量錯基準"),
           (fig2_strain, "§4 Step 6", "壓力筋未驗降伏；過渡區仍取 φ = 0.9")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2002-4.md §4 公佈值核對
    assert (A_, C_) == (19.43, 24.29)
    assert abs(EPSP - 0.002135) < 5e-7 and abs(EPST - 0.00441) < 5e-6
    assert round(PHI, 3) == 0.851 and round(MN / 1e5, 1) == 108.2 and round(PHI * MN / 1e5, 1) == 92.1
    print("assert OK")
