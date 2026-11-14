#!/usr/bin/env python3
"""
RC-2005-2 簡支 T 形梁（ACI 最大拉力筋量之半）— 解題圖解產生腳本

用法：python3 gen_RC-2005-2.py [輸出目錄]（預設 figs/）
三條鐵則：常數區只放題目正本 §1 的給定量；c_max、a_max、A_s,max、a、c、εt、φMn 一律現算，
檔尾對 RC-2005-2.md §4 公佈值 assert；改任一給定量重跑，圖跟著變。
FIGURES
  fig-1-tsection  As,max 與 As,max/2 的應力塊對照
                  攔：算 As,max 時只用翼板寬 b 的矩形應力塊（a_max 其實已進腹板）；
                      或以為取一半後仍是 T 形行為、繼續用翼腹分解
"""
import sys, os
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2005-2"

# ── 題目正本 §1／§4（已確認）──
BF, BW, HF, H, D = 120.0, 25.0, 12.0, 63.0, 50.0     # cm（b 為題給有效翼寬）
FC, FY = 280.0, 4200.0
ECU, ET_LIM = 0.003, 0.004                            # 判讀 #3：使用者選 εt ≥ 0.004
L, WD = 9.0, 0.75                                     # m、t/m（含自重）

B1 = 0.85                                             # f'c ≤ 280
C_MAX = ECU / (ECU + ET_LIM) * D
A_MAX = round(B1 * C_MAX, 2)                          # §4 公佈兩位
CMAX_F = 0.85 * FC * ((BF - BW) * HF + BW * A_MAX)
AS_MAX = round(CMAX_F / FY, 2)
AS = AS_MAX / 2
A_ = round(AS * FY / (0.85 * FC * BF), 2)
C_ = round(A_ / B1, 2)
ET = ECU * (D - C_) / C_
PHI = 0.90 if ET >= 0.005 else 0.65 + (ET - 0.002) * 0.25 / 0.003
MN = AS * FY * (D - A_ / 2)
PMN = round(PHI * MN / 1e5, 2)
WU = 8 * PMN / L ** 2
WL = (round(WU, 2) - 1.2 * WD) / 1.6


def outline():
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    return [(x0, 0), (x1, 0), (x1, H - HF), (BF, H - HF), (BF, H), (0, H), (0, H - HF), (x0, H - HF), (x0, 0)]


def block(a):
    x0, x1 = (BF - BW) / 2, (BF + BW) / 2
    if a <= HF:
        return [(0, H), (BF, H), (BF, H - a), (0, H - a)]
    return [(0, H), (BF, H), (BF, H - HF), (x1, H - HF), (x1, H - a), (x0, H - a), (x0, H - HF), (0, H - HF)]


def panel(a, c, title, sub, lines, main):
    PW, PH = 600, 520
    sc = min((PW - 270) / BF, (PH - 250) / H)
    cv = Canvas(PW, PH, sx=sc, ox=PW / 2 - BF * sc / 2 - 10, oy=PH - 140 - H * sc)
    cv.panel(title, sub)
    cv.polygon(outline(), "#EDF1F6", C["member"], 2.4)
    cv.polygon(block(a), C["fill_c"], C["compr"], 2.0)
    cv.line((0, H - HF), (BF, H - HF), C["member2"], 1.3, dash="4 4")
    x0 = (BF - BW) / 2
    for i in range(4):
        cv.dot((x0 + 4 + (BW - 8) * i / 3, H - D), 4.6, fill=C["tension"], stroke="#FFFFFF", w=1.2)
    cv.line((-4, H - c), (BF + 4, H - c), C["accent"], 1.6, dash="6 4")
    cv.text_px(cv.X(BF / 2), cv.Y(H) - 16, "橘虛線＝中性軸", 11.5, C["accent"])
    cv.dim((0, H), (0, H - a), f"a = {a:.2f}", off=30, label_off=40)
    cv.dim((BF, H), (BF, H - HF), f"h_{{f}} = {HF:.0f}", off=-26, label_off=-38)
    col = C["compr"] if main else C["muted"]
    for k, s in enumerate(lines):
        cv.text_px(PW / 2, PH - 106 + 26 * k, s, 13.5 if k == len(lines) - 1 else 12.5,
                   col if k == len(lines) - 1 else C["muted"], weight="700" if k == len(lines) - 1 else "400")
    return cv


def fig1_tsection():
    left = panel(A_MAX, C_MAX, "上限：εt = 0.004", "a_{max} 超過 h_{f} → 應力塊進入腹板",
                 [f"c_{{max}} = 3d/7 = {C_MAX:.2f} cm", f"C = 0.85f'_{{c}}[(b − b_{{w}})h_{{f}} + b_{{w}}·a_{{max}}]",
                  f"A_{{s,max}} = {AS_MAX:.2f} cm^{{2}}", "T 形行為：翼板外挑＋腹板"], False)
    right = panel(A_, C_, "本解：As = As,max / 2", "a 小於 h_{f} → 整個應力塊在翼板內",
                  [f"A_{{s}} = {AS:.2f} cm^{{2}}，c = {C_:.2f} cm，ε_{{t}} = {ET:.4f}", f"φ = {PHI:.2f}　Mn = {MN/1e5:.2f} tf·m",
                   f"wL = {WL:.2f} t/m（1.2D + 1.6L）", f"矩形梁行為（寬 b = {BF:.0f}）：φMn = {PMN:.2f} tf·m"], True)
    path = os.path.join(OUT, f"{TAG}-fig-1-tsection.svg")
    compose([left, right], title=f"{TAG}　同一個 T 形斷面，上限與一半走不同的公式",
            sub="左：求 As,max 時 a 已進腹板；右：As 取一半後 a 回到翼板內",
            note="判斷 a 與 hf 的大小要在每一個 As 重做一次，不能沿用上一步的結論",
            path=path)
    return path


FIGURES = [(fig1_tsection, "§4 Step 1–4", "As,max 用矩形塊；取一半後仍套 T 形公式")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2005-2.md §4 公佈值核對
    assert round(C_MAX, 2) == 21.43 and A_MAX == 18.21 and AS_MAX == 90.40
    assert round(AS, 2) == 45.20 and A_ == 6.65 and C_ == 7.82 and round(ET, 4) == 0.0162
    assert PMN == 79.75 and round(WL, 2) == 4.36
    print("assert OK")
