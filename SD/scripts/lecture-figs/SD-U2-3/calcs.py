"""SD-U2-3 講義的全部數值（講義內文與圖上的數字都從這裡來）。python calcs.py 會 assert 對帳。"""
import math
import numpy as np

g = 9.81
C2PI = 2 * math.pi / math.sqrt(g)                 # 2.006（u 用 m）
C2PI_cm = 2 * math.pi / math.sqrt(981)            # 0.2006（u 用 cm）

# ---- 簡支梁：規範式 vs 理論（SD-2024-4），以 w=EI=L=1 無因次化 ----
x = np.linspace(0, 1, 20001)
u_st = (x**4 - 2*x**3 + x) / 24                   # w x (L^3 - 2Lx^2 + x^3)/(24EI)
trap = lambda f: float(np.sum((f[1:] + f[:-1]) * np.diff(x)) / 2)
beta = trap(u_st)                                  # = 1/120
gamma = trap(u_st**2)                              # = 31/362880
ratio_code = math.sqrt((gamma / beta) * math.pi**4)   # T_code/T1 = sqrt(31 pi^4/3024)
ratio_code_exact = math.sqrt(31 * math.pi**4 / 3024)
# 其他假設形狀的 Rayleigh 商（能量式 ω² = EI∫u''² / m∫u²）
def rayleigh_T_ratio(u, upp):
    w2 = trap(upp**2) / trap(u**2)
    return math.pi**2 / math.sqrt(w2)              # T_R/T1 = ω1/ω_R
r_sine = rayleigh_T_ratio(np.sin(np.pi*x), -np.pi**2*np.sin(np.pi*x))
r_para = rayleigh_T_ratio(x*(1-x), -2*np.ones_like(x))          # π²/√120
# 跨中集中載重的撓度形狀（分段三次）
up = np.where(x <= .5, 3*x - 4*x**3, 3*(1-x) - 4*(1-x)**3)
upp_p = np.where(x <= .5, -24*x, -24*(1-x))
r_point = rayleigh_T_ratio(up, upp_p)
# 靜變位與正弦正規化後的最大差
ust_n = u_st / u_st.max(); dmax = float(np.max(np.abs(ust_n - np.sin(np.pi*x))))

# ---- SD-2002-3 ㈢：w 的兩個角色 ----
case_T = {'原式（施加 w）': 1.0, '施加 2w、直接代原式（錯）': math.sqrt(2),
          '施加 2w、β 權重改用 2w': 1.0, '質量也加倍': math.sqrt(2)}

# ---- SD-2010-3：縱向振動單元 ----
coef_unit = 2 * math.pi * math.sqrt(2 / 3)         # T = coef · L²√(m/EI)
coef_old = 2 * math.pi * math.sqrt(3 / 12)         # 舊解：3 跨、4 墩並聯 → π

# ---- 三軸反應譜示意（Newmark–Hall 比例，PGA = 1 g） ----
PGA = 981.0; PGV = 48 * 2.54; PGD = 36 * 2.54     # cm/s², cm/s, cm
aA, aV, aD = 2.71, 2.30, 2.01                     # 84.1% 放大係數（5% 阻尼）
Ta, Tb, Tc = 0.01, 1/33, 1/8
Td = 2*math.pi*aV*PGV/(aA*PGA); Te = 2*math.pi*aD*PGD/(aV*PGV); Tf = 10.0
def spv_from_spa(T, Spa): return T * Spa / (2*math.pi)
def spv_from_sd(T, Sd): return 2*math.pi*Sd / T
tri = [(Ta, spv_from_spa(Ta, PGA)), (Tb, spv_from_spa(Tb, PGA)), (Tc, spv_from_spa(Tc, aA*PGA)),
       (Td, aV*PGV), (Te, aV*PGV), (Tf, spv_from_sd(Tf, aD*PGD))]

# ---- 規範設計譜四段（示意值，SD-2018-2 考卷附表型式） ----
SDS, SD1 = 0.60, 0.35; T0 = SD1 / SDS
def SaD(T):
    T = np.asarray(T, float)
    return np.where(T <= 0.2*T0, SDS*(0.4 + 3*T/T0), np.where(T <= T0, SDS, SD1/np.maximum(T, 1e-9)))

T_exA = C2PI * math.sqrt(0.05); T_exA_wrong = C2PI * math.sqrt(5)

if __name__ == '__main__':
    assert abs(T_exA - 0.449) < 5e-4 and abs(T_exA_wrong - 4.49) < 5e-3
    assert abs(r_para - 0.901) < 5e-4 and abs(1/r_para - 1.11) < 5e-3 and abs((K:=(2/3)/(3/12)) - 8/3) < 1e-12
    assert abs(C2PI - 2.006) < 5e-4 and abs(C2PI_cm - 0.2006) < 5e-5
    assert abs(beta - 1/120) < 1e-9 and abs(gamma - 31/362880) < 1e-11
    assert abs(ratio_code - ratio_code_exact) < 1e-6 and abs(ratio_code - 0.9993) < 1e-4
    assert abs(r_sine - 1) < 1e-6 and abs(r_para - math.pi**2/math.sqrt(120)) < 1e-6
    assert abs(dmax - 0.0062) < 2e-4
    assert abs(coef_unit - 5.130) < 1e-3 and abs(coef_old - math.pi) < 1e-12
    for i in range(len(tri) - 1): assert tri[i+1][0] > tri[i][0]
    print(f'2π/√g={C2PI:.4f}  β={beta:.6f} γ={gamma:.3e} Tcode/T1={ratio_code:.4f}')
    print(f'Rayleigh T/T1: sine {r_sine:.4f} parabola {r_para:.4f} point-load {r_point:.4f}  靜變位 vs sin 最大差 {dmax*100:.2f}%')
    print(f'2010-3 coef {coef_unit:.3f} old {coef_old:.3f} ratio {coef_unit/coef_old:.3f}')
    print(f'tripartite Td={Td:.3f} Te={Te:.3f}', [(round(t,4), round(v,2)) for t,v in tri])
    print(f'T0={T0:.3f}')
