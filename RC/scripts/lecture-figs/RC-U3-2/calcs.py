# -*- coding: utf-8 -*-
"""lecture-RC-U3-2 數值重算（kgf、cm；土壓 kgf/cm²）。講義與圖上數字一律取自此檔，並以 assert 對帳題解正本。"""
import math

TF, TFM = 1000.0, 1e5


def close(a, b, tol):
    assert abs(a - b) <= tol, (a, b)


def lam_s(d):                       # d 以 cm 計
    return min(1.0, math.sqrt(2 / (1 + 0.04 * d)))


def vc_punch(beta, alpha_s, bo, d):
    """穿孔三式中的係數 κ（乘 √f'c bo d）。"""
    return min(1.06, 0.53 * (1 + 2 / beta), 0.265 * (2 + alpha_s * d / bo))


class Footing:
    def __init__(s, B, c, d, PD, PL, fc, fy, As, h=None, qa=None, hs=None, gs=None, gc=2.4e-3):
        s.B, s.c, s.d, s.fc, s.fy, s.As = B, c, d, fc, fy, As
        s.Pu = 1.2 * PD + 1.6 * PL
        s.qu = s.Pu / B ** 2
        s.Lc = (B - c) / 2
        s.Mu = s.qu * B * s.Lc ** 2 / 2
        a = As * fy / (0.85 * fc * B)
        s.phiMn = 0.9 * As * fy * (d - a / 2)
        s.Vu1 = s.qu * B * (s.Lc - d)
        s.rho_w = As / (B * d)
        s.phiVc1 = 0.75 * 2.12 * s.rho_w ** (1 / 3) * math.sqrt(fc) * B * d
        s.phiVc1_old = 0.75 * 0.53 * math.sqrt(fc) * B * d
        s.bo = 4 * (c + d)
        s.Vu2 = s.Pu - s.qu * (c + d) ** 2
        s.phiVc2 = 0.75 * vc_punch(1, 40, s.bo, d) * math.sqrt(fc) * s.bo * d
        s.phiVc2_ls = s.phiVc2 * lam_s(d)
        if h is not None:
            s.Wf = gc * B * B * h
            s.Ws = gs * B * B * hs
            s.q_serv = (PD + PL + s.Wf + s.Ws) / B ** 2
            s.Asmin = 0.0018 * B * h


# ===== RC-2007-3 =====
F07 = Footing(300, 45, 50, 100 * TF, 80 * TF, 280, 4200, 50.0, h=60, hs=90, gs=2.0e-3)
close(F07.Pu / TF, 248, 1e-9); close(F07.qu * 10, 27.56, 0.01); close(F07.Mu / TFM, 67.19, 0.01)
close(F07.phiMn / TFM, 91.72, 0.01); close(F07.Vu1 / TF, 64.07, 0.01); close(F07.phiVc1 / TF, 59.62, 0.01)
close(F07.phiVc1_old / TF, 99.77, 0.01)
close(F07.bo, 380, 1e-9); close(F07.Vu2 / TF, 223.13, 0.01); close(F07.phiVc2 / TF, 252.75, 0.01)
close(F07.q_serv * 10, 23.24, 0.01); close(F07.Asmin, 32.4, 1e-9)

# ===== RC-2025-1（96 年同型）=====
F25 = Footing(300, 40, 50, 80 * TF, 75 * TF, 280, 4200, 50.0, h=60, hs=90, gs=2.0e-3)
close(F25.Pu / TF, 216, 1e-9); close(F25.qu * 10, 24.0, 1e-9); close(F25.Mu / TFM, 60.84, 0.01)
close(F25.phiMn / TFM, 91.7, 0.03); close(F25.Vu2 / TF, 196.56, 0.01); close(F25.phiVc2 / TF, 239.45, 0.01)
close(F25.phiVc2_ls / TF, 195.51, 0.01); close(F25.q_serv * 10, 20.46, 0.01)

# ===== RC-2017-3 =====
F17 = Footing(400, 45, 69.96, 180 * TF, 120 * TF, 210, 4200, 65.87, h=80, hs=100, gs=1.9e-3)
close(F17.Pu / TF, 408, 1e-9); close(F17.qu * 10, 25.5, 1e-9); close(F17.Mu / TFM, 160.68, 0.01)
close(F17.Vu1 / TF, 109.69, 0.01); close(F17.phiVc1 / TF, 85.77, 0.02)
close(F17.bo, 459.84, 1e-6); close(F17.Vu2 / TF, 374.30, 0.01); close(F17.phiVc2 / TF, 370.62, 0.02)
close(F17.q_serv * 10, 22.57, 0.01); close(F17.phiVc1_old / TF, 161.2, 0.1)
# 所需 As（φMn = Mu）
def As_req(Mu, b, d, fc, fy):
    Rn = Mu / (0.9 * b * d * d)
    rho = 0.85 * fc / fy * (1 - math.sqrt(1 - 2 * Rn / (0.85 * fc)))
    return rho * b * d
close(As_req(F17.Mu, 400, 69.96, 210, 4200), 62.40, 0.02)

# ===== RC-2020-3：無梁版內柱穿孔 =====
c20, d20, wu20 = 100.0, 35.0, 0.46            # wu 4.6 tf/m² = 0.46 kgf/cm²
bo20 = 4 * (c20 + d20)
ls20 = lam_s(d20)
Vu20 = wu20 * (800 * 900 - (c20 + d20) ** 2)
phiVc20 = 0.75 * 1.06 * ls20 * math.sqrt(280) * bo20 * d20
Vcw20 = 0.53 * ls20 * math.sqrt(280) * bo20 * d20
Vs20 = Vu20 / 0.75 - Vcw20
Av20 = 4 * 2 * 1.267
s20 = Av20 * 4200 * d20 / Vs20
phiVnmax20 = 0.75 * 1.59 * math.sqrt(280) * bo20 * d20
close(bo20, 540, 1e-9); close(ls20, 0.9129, 1e-4); close(Vu20 / TF, 322.82, 0.01)
close(phiVc20 / TF, 229.52, 0.02); close(Vcw20 / TF, 153.01, 0.02); close(Vs20 / TF, 277.41, 0.03)
close(s20, 5.37, 0.01); close(phiVnmax20 / TF, 377.1, 0.1)

# ===== RC-2021-3：四樁樁帽 =====
Pu21, xi21 = 100.0, 90.0
e_Pc21 = (40 - Pu21 / 4) * 4 * xi21 ** 2 / (Pu21 * xi21)
e_Pt21 = (Pu21 / 4 + 10) * 4 * xi21 ** 2 / (Pu21 * xi21)
close(e_Pc21, 54, 1e-9); close(e_Pt21, 126, 1e-9)
d21 = 45.0
ls21 = lam_s(d21)
bo_col21 = 4 * (50 + d21)
phiVc_col21 = 0.75 * 1.06 * ls21 * math.sqrt(280) * bo_col21 * d21
bo_pile21 = 2 * 40 + math.pi * (15 + d21 / 2) / 2
phiVc_pile21 = 0.75 * 1.06 * ls21 * math.sqrt(280) * bo_pile21 * d21
close(ls21, 0.845, 1e-3); close(phiVc_col21 / TF, 192.3, 0.15)
close(bo_pile21, 138.9, 0.05); close(phiVc_pile21 / TF, 70.3, 0.1)

# ===== RC-2013-1：單向版 =====
ln13 = 450.0
h13 = math.ceil(ln13 / 24)
d13 = h13 - 2 - 0.96 / 2
wu13 = 1.2 * (2.4 * h13 / 100 + 0.1) + 1.6 * 0.6          # tf/m²
Mu13 = wu13 * 0.1 * 100 * ln13 ** 2 / 24                  # kgf·cm/m：wu(kgf/cm²)×100 cm 寬
Asmin13 = 0.0018 * 100 * h13
close(h13, 19, 0); close(d13, 16.52, 1e-9); close(wu13, 1.627, 0.001)
close(Mu13, 137278, 30); close(Asmin13, 3.42, 1e-9)

# ===== RC-2019-3：橫膈版 =====
rho_t19 = (100000 / (0.6 * 9000) - 0.53 * math.sqrt(280)) / 2800
s19 = 2 * 1.27 / (2 * 1.27 / 25 + rho_t19 * 9000 / 500)
close(rho_t19, 0.003446, 1e-6); close(s19, 15.5, 0.06)

if __name__ == "__main__":
    for nm, F in (("2007-3", F07), ("2025-1", F25), ("2017-3", F17)):
        print(nm, {k: round(v, 3) for k, v in vars(F).items() if isinstance(v, float)})
    print("2020-3", round(Vu20 / TF, 2), round(phiVc20 / TF, 2), round(s20, 2))
    print("2021-3", e_Pc21, e_Pt21, round(phiVc_pile21 / TF, 1))
    print("2013-1", h13, round(wu13, 3), round(Mu13), "2019-3", round(rho_t19, 6), round(s19, 2))
    print("all asserts OK")
