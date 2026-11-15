# -*- coding: utf-8 -*-
"""lecture-RC-U4-2 數值重算。講義內文與圖上數字一律取自此檔，並以 assert 對帳題解正本。
單位：kgf、cm（彎矩 kgf·cm）；應力壓為正。"""
import math

TF = 1000.0          # tf → kgf
TFM = 1e5            # tf·m → kgf·cm


def close(a, b, tol):
    assert abs(a - b) <= tol, (a, b)


# ── 現行規範容許應力（kgf/cm²）──
def allow(fci, fc):
    return dict(fci_c=0.60 * fci, fci_c_end=0.70 * fci, fti=0.8 * math.sqrt(fci),
                fti_end=1.6 * math.sqrt(fci), fc_all=0.60 * fc, fc_sus=0.45 * fc,
                ftU=2.0 * math.sqrt(fc), ftT=3.2 * math.sqrt(fc))


# ── 四控制條件（矩形斷面、跨中）──
def four_limits(b, h, Pi, eta, MG, MT, al):
    A, S = b * h, b * h * h / 6
    k = S / A
    Pe = eta * Pi
    e1 = k + (MG + al["fti"] * S) / Pi                 # 傳遞頂拉 → 上限
    e2 = -k + (al["fci_c"] * S + MG) / Pi              # 傳遞底壓 → 上限
    e3 = -k + (MT - al["ftU"] * S) / Pe                # 使用底拉 → 下限
    e4 = k + (MT - al["fc_all"] * S) / Pe              # 使用頂壓 → 下限
    return dict(A=A, S=S, k=k, Pe=Pe, e1=e1, e2=e2, e3=e3, e4=e4,
                emax=min(e1, e2), emin=max(e3, e4))


def stresses(A, S, P, e, M):
    """回傳 (頂, 底)，壓為正；e 向下為正；M 正彎矩（頂壓）。"""
    return P / A - P * e / S + M / S, P / A + P * e / S - M / S


# ===== RC-2010-4 =====
b10, h10, L10 = 50.0, 90.0, 1500.0
Pi10, eta10 = 200 * TF, 0.85
wG10 = 2.4e-3 * b10 * h10                        # kgf/cm（2.4 tf/m³）
MG10 = wG10 * L10 ** 2 / 8
ML10 = 15.0 * L10 ** 2 / 8                       # 1.5 tf/m = 15 kgf/cm
al10 = allow(280, 350)
r10 = four_limits(b10, h10, Pi10, eta10, MG10, MG10 + ML10, al10)
close(MG10 / TFM, 30.375, 1e-3); close(ML10 / TFM, 42.19, 0.01)
close(al10["fti"], 13.39, 0.01); close(al10["fti_end"], 26.77, 0.01); close(al10["ftU"], 37.42, 0.01)
close(r10["e1"], 34.71, 0.01); close(r10["e3"], 12.83, 0.01)
close(r10["e2"], 56.89, 0.01); close(r10["e4"], -25.70, 0.02)
E10 = (r10["emin"], r10["emax"])
# 直線鋼腱：梁端 M=0、端部拉應力 1.6√f'ci
e_str10 = r10["k"] + al10["fti_end"] * r10["S"] / Pi10
close(e_str10, 24.04, 0.01)


def ML_cap(e, r, al, MG):
    """使用階段底纖維 U 類控制下可承受的活載彎矩（kgf·cm）。"""
    return (r["Pe"] / r["A"] + r["Pe"] * e / r["S"] + al["ftU"]) * r["S"] - MG


MLc10, MLs10 = ML_cap(r10["e1"], r10, al10, MG10), ML_cap(e_str10, r10, al10, MG10)
close(MLc10 / TFM, 79.38, 0.02); close(MLs10 / TFM, 61.24, 0.02)
dM10 = (MLc10 - MLs10) / TFM
close(dM10, 18.1, 0.06)
etaMG10 = eta10 * MG10 / TFM                      # 25.8 概念值
# 傳遞時跨中應力（e = e_max 與 e = e_min 兩種配置，供 §0 圖）
st10_tr_emax = stresses(r10["A"], r10["S"], Pi10, r10["e1"], MG10)
st10_sv_emin = stresses(r10["A"], r10["S"], r10["Pe"], r10["e3"], MG10 + ML10)
st10_sv_emax = stresses(r10["A"], r10["S"], r10["Pe"], r10["e1"], MG10 + ML10)
st10_tr_emin = stresses(r10["A"], r10["S"], Pi10, r10["e3"], MG10)
close(st10_tr_emax[0], -13.39, 0.01); close(st10_sv_emin[1], -37.42, 0.01)
close(st10_tr_emax[1], 102.27, 0.02); close(st10_sv_emin[0], 112.97, 0.02)

# ===== RC-2025-4 =====
b25, h25, L25 = 40.0, 120.0, 1200.0
Pi25, eta25 = 200 * TF, 0.85
MG25 = 2.4e-3 * b25 * h25 * L25 ** 2 / 8
ML25 = 15.0 * L25 ** 2 / 8
al25 = allow(320, 420)
r25 = four_limits(b25, h25, Pi25, eta25, MG25, MG25 + ML25, al25)
close(MG25 / TFM, 20.74, 0.01); close(al25["fti"], 14.31, 0.01); close(al25["ftU"], 40.99, 0.01)
close(r25["e1"], 37.24, 0.01); close(r25["e2"], 82.53, 0.01); close(r25["e3"], -15.07, 0.01)

# ===== RC-2015-4：四條件同時達限（S_t=S_b、單一 F）=====
b15, h15, L15 = 30.0, 50.0, 1200.0
fca, fta = 140.0, 0.0
A15, S15 = b15 * h15, b15 * h15 ** 2 / 6
MD15 = 2.4e-3 * b15 * h15 * L15 ** 2 / 8
ML15 = (fca - fta) * S15
F15 = (fca + fta) * A15 / 2
ep15 = (F15 / A15 - fta + MD15 / S15) * S15 / F15
wL15 = 8 * ML15 / L15 ** 2 * 100 / TF          # tf/m
close(MD15 / TFM, 6.48, 1e-3); close(ML15 / TFM, 17.5, 1e-6); close(F15 / TF, 105, 1e-6)
close(ep15, 14.50, 0.01); close(wL15, 0.972, 0.001)
st15_tr = stresses(A15, S15, F15, ep15, MD15)
st15_sv = stresses(A15, S15, F15, ep15, MD15 + ML15)
close(st15_tr[0], 0, 1e-6); close(st15_tr[1], 140, 1e-6)
close(st15_sv[0], 140, 1e-6); close(st15_sv[1], 0, 1e-6)

# ===== RC-2020-4：兩跨連續梁載重平衡 =====
w20, L20, eB20 = 16.0, 1500.0, -35.0            # w = 1.6 tf/m = 16 kgf/cm；eB 在形心上方
MB20 = -w20 * L20 ** 2 / 8
Pe20 = abs(MB20) / abs(eB20)
close(MB20 / TFM, -45.0, 1e-9); close(Pe20 / TF, 128.57, 0.01)


def M_twospan(x):                                  # 0 ≤ x ≤ 2L，A 為原點
    if x > L20:
        x = 2 * L20 - x
    RA = 3 * w20 * L20 / 8
    return RA * x - w20 * x * x / 2


MD20 = M_twospan(L20 / 2)
eD20 = MD20 / Pe20
close(MD20 / TFM, 22.5, 1e-9); close(eD20, 17.5, 1e-6)
sag20 = eD20 - (0 + eB20) / 2
wp20 = 8 * Pe20 * sag20 / L20 ** 2
close(sag20, 35.0, 1e-9); close(wp20, w20, 1e-9)
Pi20 = Pe20 / 0.8
A20, S20 = 50 * 90.0, 50 * 90.0 ** 2 / 6
Mnet20 = (Pi20 / Pe20 - 1) * w20 * L20 ** 2 / 8    # B 點淨彎矩（正＝頂壓）
top20 = Pi20 / A20 + Mnet20 / S20
bot20 = Pi20 / A20 - Mnet20 / S20
close(Mnet20 / TFM, 11.25, 1e-6); close(top20, 52.4, 0.05); close(bot20, 19.0, 0.05)

# ===== RC-2024-4：受撐懸臂梁、拋物線鋼腱 =====
P24, L24 = 120.0, 12.0                              # tf、m；e 以 cm、向下為正
c24 = -25.0
a24 = -55.0 / 72
b24 = (40 - 36 * a24) / 6
close(a24, -0.76389, 1e-5); close(b24, 11.25, 1e-9)


def e24(x):
    return a24 * x * x + b24 * x + c24


assert abs(e24(6) - 15) < 1e-9 and abs(e24(12)) < 1e-9
wq24 = -P24 * 2 * a24 / 100                        # tf/m（向上為正）
VA_anchor = P24 * (b24) / 100                      # 13.5 tf（向下）
VB_anchor = P24 * abs(2 * a24 * 12 + b24) / 100    # 8.5 tf（向下）
MA_anchor = P24 * 25 / 100                         # 30 tf·m
close(wq24, 1.8333, 1e-4); close(VA_anchor, 13.5, 1e-9); close(VB_anchor, 8.5, 1e-9)
close(wq24 * 12 - VA_anchor - VB_anchor, 0, 1e-9)
close(wq24 * 12 * 6 - VB_anchor * 12 - MA_anchor, 0, 1e-9)
integ = 1728 * a24 + 288 * b24 + 72 * c24
RB24 = 3 * P24 / L24 ** 3 * integ / 100
close(integ, 120, 1e-9); close(RB24, 0.25, 1e-12)
RB24_b = VB_anchor - 3 * wq24 * L24 / 8
close(RB24_b, 0.25, 1e-9)
MA2_24 = RB24 * L24


def M2_24(x):
    return RB24 * (L24 - x)


def eC24(x):
    return e24(x) - M2_24(x) / P24 * 100


close(eC24(0), -27.5, 1e-9); close(eC24(6), 13.75, 1e-9); close(eC24(12), 0, 1e-12)
# 同位鋼腱：保留兩端偏心、改梁中央 → e_m = 12.5
em24 = 600 / 48
close(em24, 12.5, 1e-12)

# ===== RC-2005-5：直線後拉鋼腱擺動摩擦 =====
Ks = (0.0016, 0.0066)
loss30 = [1 - math.exp(-K * 30) for K in Ks]
close(loss30[0] * 100, 4.7, 0.05); close(loss30[1] * 100, 18.0, 0.05)

if __name__ == "__main__":
    print("2010-4", {k: round(v, 2) for k, v in r10.items()}, "straight", round(e_str10, 2),
          "MLc", round(MLc10 / TFM, 2), "MLs", round(MLs10 / TFM, 2), "dM", round(dM10, 2))
    print("2025-4", {k: round(v, 2) for k, v in r25.items()})
    print("2015-4 F", F15 / TF, "ep", round(ep15, 2), "wL", round(wL15, 3))
    print("2020-4 Pe", round(Pe20 / TF, 2), "eD", eD20, "top/bot", round(top20, 1), round(bot20, 1))
    print("2024-4 RB", RB24, "eC", eC24(0), eC24(6))
    print("all asserts OK")

# 拉應力一律取 0（舊解做法）對照：2010-4
al10_zero = dict(al10, fti=0.0, ftU=0.0)
r10z = four_limits(b10, h10, Pi10, eta10, MG10, MG10 + ML10, al10_zero)
close(r10z["e1"], 30.19, 0.01); close(r10z["e3"], 27.68, 0.01)
