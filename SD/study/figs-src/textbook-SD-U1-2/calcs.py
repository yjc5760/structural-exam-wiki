# -*- coding: utf-8 -*-
"""SD-U1-2 運動方程式推導：教科書講義的所有數值（圖與內文共用）。
多為全符號題：這裡用數值積分驗算每一個係數（取 L = EI = m = 1 的無因次化）。
考題數字取自 raw/solutions/SD-YYYY-N/SD-YYYY-N.md（勘誤後版本）。
"""
import math
import numpy as np

PI = math.pi
N = 20001
X = np.linspace(0.0, 1.0, N)          # x/L


def integ(y):
    return float(np.trapezoid(y, X)) if hasattr(np, 'trapezoid') else float(np.trapz(y, X))


def d1(y):
    return np.gradient(y, X)


def d2(y):
    return np.gradient(np.gradient(y, X), X)


# ---------- 第 1 章：柱與梁的側向勁度（單位 EI/L³） ----------
STIFF = {'固-固柱（頂可平移不可轉）': 12, '固-鉸柱': 3, '懸臂端': 3, '簡支跨中': 48, '兩端固定梁跨中': 192}
# 2010-2：質量 m 自 h 落在懸臂端（全符號）：k = 3EI/L³、u0 = −δst、u̇0 = √(2gh)
#   u_max（自靜平衡量）= √(δst² + 2 h δst) ；示意：δst = 1 cm、h = 10 cm
Q2010_2 = dict(dst=1.0, h=10.0)
Q2010_2['umax'] = math.sqrt(Q2010_2['dst'] ** 2 + 2 * Q2010_2['h'] * Q2010_2['dst'])  # 自靜平衡起算
Q2010_2['total'] = Q2010_2['umax'] + Q2010_2['dst']                                  # 自梁原位置起算

# ---------- 第 2 章：剛體 ----------
# 倒擺 2010-1：k_eff = kL² − mgL，ω² = k/m − g/L；穩定 k > mg/L
def inv_pend_V(th, r):
    """V/(mgL) = cos θ + (r/2) sin²θ，r = kL/(mg)"""
    return math.cos(th) + r / 2 * math.sin(th) ** 2


# 2024-2：剛性桿（均勻 m、長 L），兩端彈簧 k1、k2，自由度 u1、u2（兩端位移）
#   T = ½ m v̄² + ½ (mL²/12) θ̇²，v̄ = (u1+u2)/2，θ = (u2−u1)/L
def rigid_bar_M():
    # 以單位速度法：M_ij = ∂²T/∂u̇i∂u̇j
    a = np.array([0.5, 0.5]); b = np.array([-1.0, 1.0])     # v̄ = a·u̇，θ̇·L = b·u̇
    return np.outer(a, a) + np.outer(b, b) / 12.0            # 乘 m
Q2024_2 = dict(M=rigid_bar_M())          # m/6·[[2,1],[1,2]] → [[1/3,1/6],[1/6,1/3]]

# ---------- 第 3 章：直接勁度法與靜態濃縮（2017-2 門形構架） ----------
def portal_Kstar(rho):
    """K*·h³/EI1，rho = (EI2/ℓ)/(EI1/h)。K* = 24 − 72/(4 + 6ρ)。"""
    return 24 - 72 / (4 + 6 * rho)


def portal_Kstar_check(rho):
    """以矩陣運算驗算（EI1 = h = 1）。"""
    a = 4 + 4 * rho; b = 2 * rho
    Ktt = 24.0; Kt0 = np.array([-6.0, -6.0]); K00 = np.array([[a, b], [b, a]])
    return Ktt - Kt0 @ np.linalg.solve(K00, Kt0)


PORTAL = {r: (portal_Kstar(r), portal_Kstar_check(r)) for r in (0.0, 0.5, 1.0, 2.0, 1e6)}

# 剪力屋 3 層（每層 k）：K = k·[[2,−1,0],[−1,2,−1],[0,−1,1]]
K3 = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.]])

# 2003-4 剛性樓版（質心座標）：k = 12EI/h³（I 柱），A、D 柱 2I
Q2003_4 = dict(Kc=np.array([[6, 0, 0], [0, 6, -1], [0, -1, 3.]]),  # ×k、a = 1
               Mc=np.diag([1, 1, 1 / 6.]),                          # ×m
               m_col2=(-1 / 2, 2 / 3, -1 / 6))
Q2003_4['xs'] = -1 / 6   # 剛心 x（a = 1，原點在樓版中心）

# ---------- 第 4 章：基礎運動與外力 ----------
# 2011-3 電梯：m ü + k u = k v t，u = v t − (v/ω) sin ωt（零初始條件）
def elevator(t, w=2 * PI, v=1.0):
    return v * t - v / w * math.sin(w * t)


# ---------- 第 5 章：廣義座標 ----------
def gen(phi, tip_mass=0.0, mbar=1.0, EI=1.0, p=1.0):
    """回傳 m*、k*、p*（L = 1）"""
    ms = integ(mbar * phi ** 2) + tip_mass * phi[-1] ** 2
    ks = integ(EI * d2(phi)[5:-5] ** 2 if False else EI * d2(phi) ** 2)
    ps = integ(p * phi)
    return ms, ks, ps


phi_sq = X ** 2                                   # 2017-4
phi_psi = X ** 2 * (1.5 - X / 2)                  # 2009-1（懸臂端集中力撓度）
phi_udl = (6 * X ** 2 - 4 * X ** 3 + X ** 4) / 3  # 均佈載重撓度（端點正規化為 1）
GEN = {}
for name, ph in (('x²/L²', phi_sq), ('Ψ（端點集中力撓度）', phi_psi), ('均佈載重撓度', phi_udl)):
    ms, ks, ps = gen(ph)
    GEN[name] = dict(m=ms, k=ks, p=ps, w=math.sqrt(ks / ms))
EXACT_CANT = 1.875104 ** 2      # 均勻懸臂梁 ω1 = 3.516 √(EI/mL⁴)
# 2009-1 閉合解：m* = 33/140、k* = 3、p* = 3/8
Q2009_1 = dict(m=33 / 140, k=3.0, p=3 / 8, w=math.sqrt(3 / (33 / 140)))
# 2017-4：k* = 4EI/L³、M* = M + mL/5；m → 0 時 2√(EI/ML³) vs 精確 √3
Q2017_4 = dict(k=4.0, m_dist=1 / 5, ratio_tip=2 / math.sqrt(3))
# 2013-3：均佈撓度形狀、中點重量 W
Q2013_3 = dict(num=144 / 5, den_m=104 / 45, den_W=289 / 256)
Q2013_3['W0'] = Q2013_3['num'] / Q2013_3['den_m']          # 12.46（精確 12.36）
Q2013_3['m0'] = Q2013_3['num'] / Q2013_3['den_W']          # 25.51（精確 24）
Q2013_3['err_W0'] = Q2013_3['W0'] / EXACT_CANT ** 2 - 1
Q2013_3['err_m0'] = Q2013_3['m0'] / 24 - 1
# 2002-2：簡支 + 跨中質量 + 軸壓：k* = π⁴EI/(2L³)(1 − N/Ncr)，m* = mL/2 + M
phi_sin = np.sin(PI * X)
Q2002_2 = dict(kb=integ(d2(phi_sin) ** 2), kg=integ(d1(phi_sin) ** 2), m=integ(phi_sin ** 2))
Q2002_2['kb_exact'] = PI ** 4 / 2; Q2002_2['kg_exact'] = PI ** 2 / 2
Q2002_2['Ncr'] = Q2002_2['kb'] / Q2002_2['kg']           # = π²
TN = {n: 1 / math.sqrt(1 - n) for n in (0, 0.25, 0.5, 0.75)}
# 2023-1：簡支梁 ωn = n²π² √(EI/m̄L⁴)，中點力的模態力 Qn = P sin(nπ/2)
SS_W = {n: (n * PI) ** 2 for n in (1, 2, 3)}


if __name__ == '__main__':
    print('2010-2', Q2010_2)
    print('倒擺 V(0.3, r=1.6)=', inv_pend_V(0.3, 1.6))
    print('2024-2 M/m =', Q2024_2['M'])
    print('portal K*', PORTAL)
    for k_, v_ in GEN.items():
        print('gen', k_, {a: round(b, 5) for a, b in v_.items()})
    print('exact cant', math.sqrt(EXACT_CANT))
    print('2009-1', Q2009_1); print('2017-4', Q2017_4); print('2013-3', Q2013_3); print('2002-2', Q2002_2); print('TN', TN)
