# -*- coding: utf-8 -*-
"""lecture-SS-U1-3 全部手算範例的獨立重算（圖與內文的唯一數字來源）。"""
import math
pi2 = math.pi ** 2
E, L = 2040.0, 700.0
Ag, Ix, Iy, Sx, Zx, rx, ry = 219.0, 66600.0, 22400.0, 3330.0, 3670.0, 17.44, 10.11


def Pe(I, K=1.0, Lc=L):
    return pi2 * E * I / (K * Lc) ** 2


def B1_aisc(p, r):            # r = M1/M2（單曲率為負）
    return (0.6 - 0.4 * r) / (1 - p)


def B1_tw(p, r):              # 台灣 LRFD (8.2-3)
    return 0.64 / (1 - p) * (1 - r) + 0.32 * r


def Fcr_lrfd(KLr, Fy):
    lc = KLr / math.pi * math.sqrt(Fy / E)
    return lc, (0.658 ** (lc ** 2) * Fy if lc <= 1.5 else 0.877 / lc ** 2 * Fy)


R = {}
# ── 範例 A ──
Pu = 250.0
R['Pe1x'] = Pe(Ix); R['Pe1y'] = Pe(Iy)
R['px'] = Pu / R['Pe1x']; R['py'] = Pu / R['Pe1y']
R['ampx'] = 1 / (1 - R['px']); R['ampy'] = 1 / (1 - R['py'])
R['A_rows'] = []
for r in (-1.0, -0.5, 0.0, 1.0):
    R['A_rows'].append((r, 0.6 - 0.4 * r, B1_aisc(R['px'], r), B1_tw(R['px'], r),
                        B1_aisc(R['py'], r), B1_tw(R['py'], r)))
# ── 範例 B ──
R['Pe2'] = Pe(Ix, 1.8)
R['sPe2_B'] = 2 * R['Pe2']
R['ratio_B_wrong'] = 500 / R['sPe2_B']; R['B2_B_wrong'] = 1 / (1 - R['ratio_B_wrong'])
R['ratio_B'] = 1100 / R['sPe2_B']; R['B2_B'] = 1 / (1 - R['ratio_B'])
# ── 範例 C ──
Fy = 3.5
R['KLrx'] = 1.8 * L / rx; R['KLry'] = 1.0 * L / ry
R['lc_C'], R['Fcr_C'] = Fcr_lrfd(max(R['KLrx'], R['KLry']), Fy)
R['phiPn_C'] = 0.85 * R['Fcr_C'] * Ag
R['phiMnx_C'] = 0.9 * Fy * Zx / 100
R['B1_C'] = max(1.0, B1_aisc(R['px'], -1)); R['B1_C_tw'] = max(1.0, B1_tw(R['px'], -1))
R['sPe2_C'] = 3 * R['Pe2']; R['ratio_C'] = 750 / R['sPe2_C']; R['B2_C'] = 1 / (1 - R['ratio_C'])
R['Mu_C'] = R['B1_C'] * 25 + R['B2_C'] * 15
R['Mu_C_tw'] = R['B1_C_tw'] * 25 + R['B2_C'] * 15
R['Pr_C'] = Pu / R['phiPn_C']
R['H1_C'] = R['Pr_C'] + 8 / 9 * R['Mu_C'] / R['phiMnx_C']
R['H1_C_tw'] = R['Pr_C'] + 8 / 9 * R['Mu_C_tw'] / R['phiMnx_C']
R['H1_C_1st'] = R['Pr_C'] + 8 / 9 * 40 / R['phiMnx_C']
R['B2_C_K1'] = 1 / (1 - 750 / (3 * R['Pe1x']))
# ── 範例 D（ASD）──
FyD = 2.5
fa = 140 / Ag; fbx = 2000 / Sx
Cc = math.sqrt(2 * pi2 * E / FyD)
klr = L / ry
FS = 5 / 3 + 3 * klr / (8 * Cc) - klr ** 3 / (8 * Cc ** 3)
Fa = (1 - klr ** 2 / (2 * Cc ** 2)) * FyD / FS
Fex = 12 * pi2 * E / (23 * (L / rx) ** 2)
Fbx = 0.66 * FyD
amp = 1 / (1 - fa / Fex)
R.update(fa=fa, fbx=fbx, Cc=Cc, klr=klr, FS=FS, Fa=Fa, Fex=Fex, ampD=amp,
         stabD=fa / Fa + fbx * amp / Fbx, strD=fa / (0.6 * FyD) + fbx / Fbx)
lcD, FcrD = Fcr_lrfd(klr, FyD)
R['phiPn_D'] = 0.85 * FcrD * Ag; R['lc_D'] = lcD; R['Fcr_D'] = FcrD
R['phiMn_D'] = 0.9 * FyD * Zx / 100
R['B1_D'] = B1_aisc(210 / R['Pe1x'], -1)
R['H1_D'] = 210 / R['phiPn_D'] + 8 / 9 * R['B1_D'] * 30 / R['phiMn_D']
# ── 範例 E（強柱弱梁）──
Zc, Zb, Fyc, Fyb = 3670.0, 2200.0, 3.5, 3.5
R['Mpc'] = Zc * (Fyc - Pu / Ag) / 100; R['sMpc'] = 2 * R['Mpc']
R['sMpc_noP'] = 2 * Zc * Fyc / 100
R['sMpb'] = 2 * Zb * Fyb / 100
R['E_tw'] = R['sMpc'] / (1.25 * R['sMpb'])
R['E_noP'] = R['sMpc_noP'] / (1.25 * R['sMpb'])
R['E_no125'] = R['sMpc'] / R['sMpb']
R['E_both'] = R['sMpc_noP'] / R['sMpb']
R['E_aisc'] = R['sMpc'] / (1.1 * 1.1 * R['sMpb'])   # AISC 341，SN490 Ry=1.1，略 Muv
R['E_red'] = Pu / (Ag * Fyc)

if __name__ == "__main__":
    for k, v in R.items():
        if isinstance(v, float):
            print(f"{k:12s} {v:.4f}")
    for row in R['A_rows']:
        print("A row", ["%.4f" % x for x in row])
