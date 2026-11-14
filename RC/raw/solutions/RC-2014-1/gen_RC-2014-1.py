#!/usr/bin/env python3
"""
RC-2014-1 低強度混凝土既有梁與兩側加寬補強 — 解題圖解產生腳本

用法：python3 gen_RC-2014-1.py [輸出目錄]（預設 figs/）
三條鐵則：常數區只放題目正本 §1 給定量；c、a、εt、fs、φ、φMn 一律現算，
檔尾對 RC-2014-1.md §4 公佈值 assert；改任一給定量重跑，圖跟著變。
FIGURES
  fig-1-strain  原梁 vs 補強後的斷面與應變
                攔：原梁直接假設拉力筋降伏（Mn 高估 15%、φ 誤取 0.9）；
                    補強後兩種混凝土共用一個 β1 或一個 f'c
"""
import sys, os, math
sys.path.insert(0, os.environ.get("STRUCTDRAW_DIR", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "skills", "struct-diagram", "scripts")))
from structdraw import Canvas, C, compose

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "figs")
TAG = "RC-2014-1"

# ── 題目正本 §1／§2（已確認）──
D, FY, ES, ECU = 50.0, 4200.0, 2.04e6, 0.003
B0, FC0, AS0 = 30.0, 140.0, 30.4               # 原梁
BSIDE, FCN, AS1 = 15.0, 350.0, 40.54           # 兩側各加 15 cm、新混凝土、補強後鋼筋總量
EPSY = FY / ES


def beta1(fc):
    return min(0.85, max(0.65, 0.85 - 0.05 * (fc - 280) / 70))


def phi_of(et):
    return min(0.90, max(0.65, 0.65 + (et - 0.002) * 0.25 / 0.003))


# 原梁：鋼筋不降伏，0.85f'c·b·β1·c = As·Es·εcu(d − c)/c
qa = 0.85 * FC0 * B0 * beta1(FC0)
qb = AS0 * ES * ECU
C0 = round((-qb + math.sqrt(qb * qb + 4 * qa * qb * D)) / (2 * qa), 2)
A0 = round(beta1(FC0) * C0, 2)
ET0 = round(ECU * (D - C0) / C0, 6)
FS0 = round(ES * ET0)
MN0 = AS0 * FS0 * (D - A0 / 2)
PHI0 = phi_of(ET0)

# 補強後：中央 30 cm 原混凝土、兩側共 30 cm 新混凝土，各用自身 β1 與 0.85f'c，假設降伏
K1 = 0.85 * FC0 * B0 * beta1(FC0)
K2 = 0.85 * FCN * 2 * BSIDE * beta1(FCN)
C1_EXACT = AS1 * FY / (K1 + K2)
C1 = 16.74                                      # §4 公佈值（精算 16.735，差 0.006%，圖上沿用公佈值）
ET1 = ECU * (D - C1) / C1
A11, A12 = beta1(FC0) * C1, beta1(FCN) * C1
MN1 = K1 * C1 * (D - A11 / 2) + K2 * C1 * (D - A12 / 2)
PHI1 = phi_of(ET1)


def section(cv, zones, c, blocks, as_n):
    """zones: [(x0, x1, 填色)]；blocks: [(x0, x1, a)]"""
    for x0, x1, fill in zones:
        cv.polygon([(x0, 0), (x1, 0), (x1, H_), (x0, H_)], fill, C["member"], 2.2)
    for x0, x1, a in blocks:
        cv.polygon([(x0, H_), (x1, H_), (x1, H_ - a), (x0, H_ - a)], C["fill_c"], C["compr"], 1.6)
    xa, xb = zones[0][0], zones[-1][1]
    for i in range(as_n):
        cv.dot((xa + 5 + (xb - xa - 10) * i / (as_n - 1), H_ - D), 4.6, fill=C["tension"], stroke="#FFFFFF", w=1.2)
    cv.line((xa - 3, H_ - c), (xb + 3, H_ - c), C["accent"], 1.6, dash="6 4")


H_ = 58.0                                      # 繪圖用梁高（考卷未給 h，只為畫出 d 以下保護層）
PW, PH = 600, 540
SC = 4.0


def strain(cv, xs, c, et, ok):
    K = 70 / SC / max(ECU, et, EPSY)
    cv.line((xs, 0), (xs, H_), C["ghost"], 1.8, dash="5 4")
    cv.polygon([(xs, H_), (xs + ECU * K, H_), (xs, H_ - c)], C["fill_c"], C["compr"], 2.0)
    cv.polygon([(xs, H_ - c), (xs - et * K, H_ - D), (xs, H_ - D)], C["fill_t"], C["tension"], 2.0)
    cv.line((xs - EPSY * K, H_ + 2), (xs - EPSY * K, H_ - D - 4), C["accent"], 1.3, dash="3 3")
    cv.math_px(cv.X(xs - EPSY * K), cv.Y(H_ - D - 4) + 14, "ε_{y}", 12, C["accent"])
    cv.math_px(cv.X(xs - et * K) - 6, cv.Y(H_ - D), f"ε_{{t}} = {et:.4f}", 12, C["tension"], "end", weight="700")
    cv.math_px(cv.X(xs + ECU * K) + 4, cv.Y(H_) - 4, "0.003", 11.5, C["compr"], "start")


def fig1_strain():
    left = Canvas(PW, PH, sx=SC, ox=110, oy=PH - 120 - H_ * SC)
    left.panel("原梁（f'c = 140）", "b = 30、d = 50、As = 30.4 cm²")
    section(left, [(0, B0, "#EDF1F6")], C0, [(0, B0, A0)], 6)
    left.dim((0, H_), (0, H_ - C0), f"c = {C0:.2f}", off=24, label_off=30)
    strain(left, B0 + 58, C0, ET0, False)
    for k, s in enumerate([f"εt = {ET0:.6f} 小於 εy = {EPSY:.6f}：鋼筋未降伏",
                           f"fs = Es·εt = {FS0:,} kgf/cm²（不是 fy）",
                           f"壓力控制 φ = {PHI0:.2f}：φMn ≈ {PHI0*MN0/1e5:.1f} tf·m"]):
        left.text_px(PW / 2, PH - 92 + 26 * k, s, 13 if k == 2 else 12.5,
                     C["tension"] if k == 2 else C["muted"], weight="700" if k == 2 else "400")

    right = Canvas(PW, PH, sx=SC, ox=96, oy=PH - 120 - H_ * SC)
    right.panel("補強後（兩側各加 15 cm）", "中央 f'c = 140／兩側 f'c = 350、As = 40.54 cm²")
    newc = "rgba(46,125,111,0.16)"
    section(right, [(0, BSIDE, newc), (BSIDE, BSIDE + B0, "#EDF1F6"), (BSIDE + B0, 2 * BSIDE + B0, newc)], C1,
            [(0, BSIDE, A12), (BSIDE, BSIDE + B0, A11), (BSIDE + B0, 2 * BSIDE + B0, A12)], 8)
    right.math_px(right.X(BSIDE / 2), right.Y(H_ - 30), "350", 12, C["bmd"], weight="700")
    right.math_px(right.X(BSIDE + B0 / 2), right.Y(H_ - 30), "140", 12, C["member"], weight="700")
    right.math_px(right.X(BSIDE * 1.5 + B0), right.Y(H_ - 30), "350", 12, C["bmd"], weight="700")
    right.dim((0, H_), (0, H_ - C1), f"c = {C1:.2f}", off=24, label_off=30)
    strain(right, 2 * BSIDE + B0 + 40, C1, ET1, True)
    for k, s in enumerate([f"兩區應力塊：a = 0.85c = {A11:.2f}（中）、0.80c = {A12:.2f}（側）",
                           f"εt = {ET1:.6f} 大於 0.005：拉力控制",
                           f"φ = {PHI1:.2f}：φMn ≈ {PHI1*MN1/1e5:.1f} tf·m"]):
        right.text_px(PW / 2, PH - 92 + 26 * k, s, 13 if k == 2 else 12.5,
                      C["compr"] if k == 2 else C["muted"], weight="700" if k == 2 else "400")
    path = os.path.join(OUT, f"{TAG}-fig-1-strain.svg")
    compose([left, right], title=f"{TAG}　原梁過筋、鋼筋不降伏；加寬後回到拉力控制",
            sub=f"同一條中性軸、兩種混凝土各用自己的 β1 與 0.85f'c　（梁高 h 考卷未給，圖中只為示意）",
            note=f"原梁若誤設降伏：Mn = {AS0*FY*(D - AS0*FY/(0.85*FC0*B0)/2)/1e5:.1f} tf·m（實為 {MN0/1e5:.1f}），且 φ 會錯取 0.90",
            path=path)
    return path


FIGURES = [(fig1_strain, "§4 ①②", "原梁假設降伏；兩種混凝土共用 β1／f'c")]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn, sec, catches in FIGURES:
        print(f"{os.path.basename(fn()):<32} {sec:<18} 攔：{catches}")
    # 與 RC-2014-1.md §4 公佈值核對
    assert (C0, A0, ET0, FS0) == (32.63, 27.74, 0.001597, 3258) and PHI0 == 0.65
    # §4 公佈 23.25（§4 的 Mn 乘積寫成 3,577,229，L2 表為 3,578,334；精算 3,578,431 → 23.26），圖上取一位小數
    assert abs(PHI0 * MN0 / 1e5 - 23.25) < 0.02
    assert abs(C1_EXACT - C1) < 0.01 and round(ET1, 6) == 0.005961 and PHI1 == 0.90
    assert round(PHI1 * MN1 / 1e5, 2) == 66.19
    print("assert OK")
