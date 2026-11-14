#!/usr/bin/env python3
"""
RC-2014-2 單筋矩形梁三個特徵點的彎矩–曲率 — 解題圖解產生腳本

用法：python3 gen_RC-2014-2.py [輸出目錄]（預設 figs/）
三條鐵則：常數區只放題目正本 §1 給定量與 §4 採用的 fr；Mcr、φcr、kd、Mel、φel、Mn、φu 一律現算，
檔尾對 RC-2014-2.md §4 公佈值 assert；改任一給定量重跑，圖跟著變。
FIGURES
  fig-1-mphi  M–φ 三特徵點（開裂／彈性極限／標稱強度）
              攔：把 φcr、φel、φu 當強度折減係數；以為開裂後斷面就失效；把兩個比值的意義講反
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2014-2"

# ── 題目正本 §1（已確認）＋ §4 採用值 ──
B, H, D = 30.0, 60.0, 53.5
FC, FY, AS, EEL = 210.0, 4200.0, 30.4, 0.00055
ES, ECU = 2.04e6, 0.003
EC = 15000 * math.sqrt(FC)                 # 卷首公式
N = ES / EC
FR = 2.0 * math.sqrt(FC)                   # §4 採規範 fr = 2√f'c（考卷未給）
B1 = 0.85

# 開裂：未開裂轉換斷面（§4 Step 2–3）
AT = B * H + (N - 1) * AS
YBAR = (B * H * H / 2 + (N - 1) * AS * D) / AT
YB = H - YBAR
IT = B * H ** 3 / 12 + B * H * (YBAR - H / 2) ** 2 + (N - 1) * AS * (D - YBAR) ** 2
MCR = FR * IT / YB
PCR = FR / (EC * YB)
# 彈性極限：開裂轉換斷面（§4 Step 4–5）
KD = (-N * AS + math.sqrt((N * AS) ** 2 + 2 * B * N * AS * D)) / B
ICR = B * KD ** 3 / 3 + N * AS * (D - KD) ** 2
PEL = EEL / KD
MEL = EC * EEL * ICR / KD
# 標稱強度（§4 Step 6）
A_ = AS * FY / (0.85 * FC * B)
C_ = round(A_ / B1, 2)                     # §4 公佈 c = 28.05（φu 以此計）
PU = ECU / C_
MN = AS * FY * (D - A_ / 2)


def fig1_mphi():
    W, Hc = 940, 600
    xmax, ymax = PU * 1.12, MN / 1e5 * 1.18
    L, R, T, Bm = 110, 60, -40, 110
    cv = Canvas(W, Hc, sx=1.0, ox=0, oy=0)
    X = lambda p: L + p / xmax * (W - L - R)
    Y = lambda m: Hc - Bm - m / ymax * (Hc - T - Bm - 40)
    cv.line((X(0), Hc - Y(0)), (X(xmax), Hc - Y(0)), C["muted"], 1.6)
    cv.line((X(0), Hc - Y(0)), (X(0), Hc - Y(ymax)), C["muted"], 1.6)
    for k in range(0, 6):
        m = k * 10
        cv.text_px(X(0) - 10, Y(m), f"{m}", 12, C["muted"], "end")
        cv.line((X(0) - 4, Hc - Y(m)), (X(0), Hc - Y(m)), C["muted"], 1.2)
    for k in range(0, 6):
        p = k * 2e-5
        cv.text_px(X(p), Y(0) + 18, f"{p*1e5:.0f}", 12, C["muted"])
    cv.text_px((X(0) + X(xmax)) / 2, Y(0) + 44, "曲率 φ（×10^{-5} 1/cm）", 13, C["muted"])
    cv.text_px(X(0) - 70, Y(ymax / 2), "M（tf·m）", 13, C["muted"])
    pts = [(0, 0), (PCR, MCR / 1e5), (PEL, MEL / 1e5), (PU, MN / 1e5)]
    P = [(X(p), Hc - Y(m)) for p, m in pts]
    cv.poly(P[:3], C["bmd"], 3.0)
    cv.poly(P[2:], C["bmd"], 3.0, dash="7 5")
    labs = [("開裂", PCR, MCR, -1), ("彈性極限", PEL, MEL, -1), ("標稱強度", PU, MN, 1)]
    for (name, p, m, side), (px, py) in zip(labs, P[1:]):
        cv.dot((px, py), 6, fill=C["accent"])
    cv.text_px(X(PCR) + 14, Y(MCR / 1e5) + 4, f"開裂：φcr = {PCR*1e5:.4f}×10^{{-5}}，Mcr = {MCR/1e5:.2f}", 12.5, C["accent"], "start", weight="700")
    cv.text_px(X(PEL) + 14, Y(MEL / 1e5) + 10, f"彈性極限（εc = {EEL}）：φel = {PEL*1e5:.3f}×10^{{-5}}，Mel = {MEL/1e5:.2f}", 12.5, C["accent"], "start", weight="700")
    cv.text_px(X(PU) - 12, Y(MN / 1e5) - 18, f"標稱強度：φu = {PU*1e5:.2f}×10^{{-5}}，Mn = {MN/1e5:.1f}", 12.5, C["accent"], "end", weight="700")
    cv.text_px((X(PEL) + X(PU)) / 2 + 30, (Y(MEL / 1e5) + Y(MN / 1e5)) / 2 + 30,
               "虛線：鋼筋降伏、混凝土非線性（只連端點，非真實曲線）", 11.5, C["muted"], "start")
    path = os.path.join(OUT, f"{TAG}-fig-1-mphi.svg")
    compose([cv], title=f"{TAG}　這題的 φ 是曲率，不是強度折減係數",
            sub=f"φu/φcr = {PU/PCR:.1f}（變形儲備）　Mn/Mcr = {MN/MCR:.2f}（強度儲備）",
            note="開裂後勁度驟降但還能再承受約 7 倍彎矩；曲率比遠大於彎矩比，代表斷面以變形吸收能量",
            path=path)
    return path


FIGURES = [(fig1_mphi, "§4 Step 2–7", "φ 當成折減係數；比值意義講反")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2014-2.md §4 公佈值核對
    assert round(N, 3) == 9.385 and round(YBAR, 2) == 32.92 and round(IT) == 663307
    # §4 公佈 Mcr = 7.097、Mn = 53.10（中間值四捨五入鏈造成末位差），圖上取 7.10、53.1
    assert abs(MCR / 1e5 - 7.097) < 0.002 and round(PCR * 1e6, 3) == 4.923
    assert round(KD, 2) == 23.78 and round(PEL * 1e5, 3) == 2.313 and round(MEL / 1e5, 2) == 19.43
    assert round(C_, 2) == 28.05 and round(PU * 1e4, 3) == 1.070 and abs(MN / 1e5 - 53.10) < 0.02
    assert round(PU / PCR, 1) == 21.7 and round(MN / MCR, 2) == 7.48
    print("assert OK")
