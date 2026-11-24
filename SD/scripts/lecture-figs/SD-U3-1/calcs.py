"""SD-U3-1 講義的全部數值。python calcs.py 會與題解正本的數字 assert 對帳。"""
import math
from fractions import Fraction as Fr
import numpy as np

# ---- SD-2013-2：容量設計剪力（tf、m、cm）----
fc, fy, b, d = 280.0, 4200.0, 40.0, 53.0
Ab25, Ab13 = 5.067, 1.267
def Mpr(n):                       # 實配 n-D25，1.25fy、φ=1、不計壓力筋 → tf·m
    As = n * Ab25; a = 1.25 * As * fy / (0.85 * fc * b)
    return As * 1.25 * fy * (d - a / 2) / 1e5
L, c1 = 7.0, 0.60; ln = L - c1
MprAm, MprAp, MprBm, MprBp = Mpr(5), Mpr(3), Mpr(6), Mpr(3)
Veq1 = (MprAm + MprBp) / ln; Veq2 = (MprAp + MprBm) / ln
wu = 1.2 * 2.7 + 1.0 * 1.4; Vg = wu * ln / 2
Ve = max(Veq1, Veq2) + Vg
Vu_analysis = (20 + 48) / ln + Vg          # 若直接用分析彎矩推剪力（對照用）
Av = 2 * Ab13; phi = 0.75
s_hinge_req = Av * fy * d / (Ve * 1000 / phi)   # cm
s_hinge = 12.0; phiVs_hinge = phi * Av * fy * d / s_hinge / 1000
Vc = 0.53 * math.sqrt(fc) * b * d / 1000
Vu_2h = Ve - wu * 1.2
s_out = 25.0; phiVn_out = phi * (Vc + Av * fy * d / s_out / 1000)
s_max_hinge = min(d / 4, 6 * 2.54, 15.0)

# ---- SD-2009-4：螺箍筋體積比 ----
D, cover = 55.0, 4.0; Dc = D - 2 * cover
Ag, Ac = math.pi * D**2 / 4, math.pi * Dc**2 / 4
fc9, fyt = 350.0, 4200.0
rho_req = 0.45 * (Ag / Ac - 1) * fc9 / fyt
rho_min_seis = 0.12 * fc9 / fyt
dsp = Dc - 1.27                               # 螺箍筋中心線直徑
rho_act = math.pi * dsp * Ab13 / (Ac * 7.5)
rho_s8 = math.pi * dsp * Ab13 / (Ac * 8.0)

# ---- SD-2017-3：短柱剪力分配（k ∝ 1/h³，h 以 ℓ 為單位）----
h = [Fr(1, 2), Fr(1, 2), Fr(3, 4), Fr(1)]
kk = [1 / x**3 for x in h]; Ksum = sum(kk)
share = [x / Ksum for x in kk]

# ---- SD-2015-4：懸臂梁法（tf、m）----
xs = [0.0, 7.0, 17.0]; H, P = 4.0, 20.0
xbar = sum(xs) / 3; dd = [x - xbar for x in xs]
M_OT = P * H / 2
kN = M_OT / sum(v * v for v in dd)
N = [kN * v for v in dd]                      # 正＝壓（向右側力 → 右柱受壓）
Vb12, Vb23 = -N[0], -N[0] - N[1]              # 梁剪力（左柱拉力向下由梁剪力平衡）
Mb12, Mb23 = Vb12 * 7 / 2, Vb23 * 10 / 2
Mc = [Mb12, Mb12 + Mb23, Mb23]                # 柱頂彎矩（=柱底，反曲點在柱中）
Vc_col = [m / (H / 2) for m in Mc]

# ---- SD-2010-4：兩種邊界的頻率與崩塌（單位 EI/L³、Mp/L、MpL²/EI）----
k_a, k_b = 3 + 12, 12 + 12
w_ratio = math.sqrt(k_a / k_b)
d1_a = 1 / 6; V1_a = k_a * d1_a               # 右柱（固-固）兩端先降伏
d2_a = 1 / 3; V2_a = 2 + 1                    # 左柱（底鉸）頂端降伏
d1_b = 1 / 6; V1_b = k_b * d1_b               # 四個塑鉸同時
push_a = [(0, 0), (d1_a, V1_a), (d2_a, V2_a), (0.6, V2_a)]
push_b = [(0, 0), (d1_b, V1_b), (0.6, V1_b)]

# ---- SD-2022-4：五種側推力分布（3 層、m 相同、H=3/6/9 m、V=600 kN、T=2.5 s）----
V = 600.0; Hs = np.array([3.0, 6.0, 9.0]); m = np.ones(3)
F_uni = np.full(3, V / 3)
F_tri = V * m * Hs / np.sum(m * Hs)
kexp = 2.0; F_exp = V * m * Hs**kexp / np.sum(m * Hs**kexp)
T1 = 2.5; Ft = min(0.07 * T1 * V, 0.25 * V)
F_emp = (V - Ft) * m * Hs / np.sum(m * Hs); F_emp[2] += Ft
K = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1]], float)    # 等 k 剪力屋架（k 只影響尺度）
lam, Ph = np.linalg.eigh(K)                                    # M = I
Tn = 1 / np.sqrt(lam); San = Tn.min() / 1.0 * 0 + 1 / Tn       # Sa ∝ 1/T
Vst = []
for n in range(3):
    ph = Ph[:, n] / Ph[2, n]; G = ph.sum() / (ph @ ph)
    Vst.append([G * San[n] * ph[i:].sum() for i in range(3)])
Vst = np.array(Vst); Vs = np.sqrt((Vst**2).sum(0))
F_srss = np.array([Vs[0] - Vs[1], Vs[1] - Vs[2], Vs[2]]); F_srss *= V / F_srss.sum()
DIST = [('均勻', F_uni), ('倒三角', F_tri), ('指數 k=2', F_exp), ('經驗（規範式）', F_emp), ('SRSS', F_srss)]

# ---- §0 延性 vs 脆性（示意，力以 V_y 正規化、位移以 Δ_y 正規化）----
mu_duct = 6.0
E_duct = 1 * (mu_duct - 1) + 0.5            # 彈性完全塑性曲線下面積
E_brit = 0.5 * 0.8 * 0.8 + 0.8 * 0.1 / 2     # 剪力破壞：到 0.8Vy 突然掉落

if __name__ == '__main__':
    near = lambda a, b, t: abs(a - b) <= t
    assert near(MprAm, 61.20, .02) and near(MprAp, 38.95, .02) and near(MprBm, 71.21, .02)
    assert near(Veq1, 15.65, .01) and near(Veq2, 17.21, .01) and near(wu, 4.64, 1e-9) and near(Vg, 14.85, .005)
    assert near(Ve, 32.06, .01) and near(phiVs_hinge, 35.25, .01) and near(Vc, 18.80, .01) and near(Vu_2h, 26.49, .01)
    assert near(phiVn_out, 31.02, .02) and near(Veq2 / Ve, 0.537, .001) and s_hinge <= s_max_hinge and s_hinge <= s_hinge_req
    assert near(Ag / Ac, 1.3693, 1e-4) and near(rho_req, 0.01385, 1e-5) and near(rho_act, 0.01399, 1e-5) and near(rho_s8, 0.01312, 1e-5)
    assert share[0] == Fr(216, 523) and share[2] == Fr(64, 523) and share[3] == Fr(27, 523) and 12 * Ksum == Fr(2092, 9)
    assert near(xbar, 8, 1e-12) and near(N[0], -160/73, 1e-12) and near(N[2], 180/73, 1e-12)
    assert near(Mb12, 560/73, 1e-12) and near(Mb23, 900/73, 1e-12) and near(Mc[1], 20, 1e-12) and near(sum(Vc_col), P, 1e-12)
    assert near(w_ratio, math.sqrt(15/24), 1e-12) and near(V2_a / V1_b, 0.75, 1e-12) and near(V1_a, 2.5, 1e-12)
    assert np.allclose(F_exp, [42.857, 171.429, 385.714], atol=1e-3) and np.allclose(F_emp, [82.5, 165, 352.5])
    assert np.allclose(F_srss, [121.4, 165.3, 313.3], atol=0.1), F_srss
    print(f'Mpr A- {MprAm:.2f} A+ {MprAp:.2f} B- {MprBm:.2f}; Ve {Ve:.2f}; 分析推 {Vu_analysis:.2f} (×{Ve/Vu_analysis:.3f}); s_req {s_hinge_req:.2f} cm; smax {s_max_hinge:.2f}')
    print(f'ρs req {rho_req:.5f} act {rho_act:.5f} s8 {rho_s8:.5f} min_seis {rho_min_seis:.4f}')
    print('share', share, 'N', [round(v, 4) for v in N], 'Mc', [round(v, 3) for v in Mc], 'Vcol', [round(v, 3) for v in Vc_col])
    print('2010-4 ratio', round(w_ratio, 4), 'pushover a', push_a, 'b', push_b)
    for nm, F in DIST: print(nm, np.round(F, 1))
    print('E ductile/brittle', E_duct, E_brit)
