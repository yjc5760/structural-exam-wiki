# -*- coding: utf-8 -*-
"""SD-U1-3 單自由度、多自由度系統之動態分析及應用：教科書講義的所有數值。
貫穿全冊範例：SD-2022-3 兩層剪力屋（M = 100 kN·s²/m、K = [[3000,−1500],[−1500,1500]] kN/m、Sa = 0.45g/T ≤ 0.7g）。
單位：kN、m、s（質量 kN·s²/m = t）。考題數字取自 raw/solutions（勘誤後版本）。
"""
import math
import numpy as np

PI = math.pi
G = 9.81


def eig(K, M):
    lam, vec = np.linalg.eig(np.linalg.solve(M, K))
    lam, vec = lam.real, vec.real
    i = np.argsort(lam)
    lam, vec = lam[i], vec[:, i]
    vec = vec / vec[0, :]          # 一樓（第一個自由度）正規化為 1
    return lam, vec


# ---------------- 範例：SD-2022-3 ----------------
M = np.diag([100.0, 100.0])
K = np.array([[3000.0, -1500.0], [-1500.0, 1500.0]])
lam, PHI = eig(K, M)
W_ = np.sqrt(lam)
T_ = 2 * PI / W_
ONE = np.ones(2)
Mn = np.array([PHI[:, n] @ M @ PHI[:, n] for n in range(2)])
Ln = np.array([PHI[:, n] @ M @ ONE for n in range(2)])
GAM = Ln / Mn
MEFF = Ln ** 2 / Mn


def Sa_2022(T):
    return min(0.45 / T, 0.7) * G      # m/s²


SA = np.array([Sa_2022(t) for t in T_])
SD = SA / W_ ** 2
U = np.array([GAM[n] * PHI[:, n] * SD[n] for n in range(2)]).T          # 欄 n：第 n 振態樓層位移
F = np.array([GAM[n] * (M @ PHI[:, n]) * SA[n] for n in range(2)]).T    # 樓層側力 kN
VB = MEFF * SA                                                          # 振態基底剪力 kN
VSTORY = np.array([[F[i:, n].sum() for n in range(2)] for i in range(2)])   # 層剪力（第 i 層）
DRIFT = np.array([U[0, :], U[1, :] - U[0, :]])                          # 層間位移
SRSS = lambda a: math.sqrt(sum(x * x for x in a))
EX = dict(
    w2=lam, w=W_, T=T_, phi=PHI, Mn=Mn, Ln=Ln, G=GAM, Meff=MEFF, Meff_ratio=MEFF / M.trace(),
    Sa=SA, Sa_g=SA / G, Sd=SD, U=U, F=F, VB=VB, Vstory=VSTORY, drift=DRIFT,
    u_top=SRSS(U[1, :]), u_1=SRSS(U[0, :]), VB_srss=SRSS(VB), drift_srss=[SRSS(DRIFT[i, :]) for i in range(2)],
    Vstory_srss=[SRSS(VSTORY[i, :]) for i in range(2)],
    u_top_abs=abs(U[1, 0]) + abs(U[1, 1]),
    drift2_wrong=SRSS(U[1, :]) - SRSS(U[0, :]),           # 錯法：組合後相減
)
# 檢查：Σ有效質量 = 總質量；Σ Γφ = 1
EX['sum_Meff'] = MEFF.sum()
EX['sum_Gphi'] = (PHI * GAM).sum(axis=1)
EX['orth'] = PHI[:, 0] @ M @ PHI[:, 1]


# CQC（阻尼比 5%）
def rho(r, z=0.05):
    return 8 * z * z * (1 + r) * r ** 1.5 / ((1 - r * r) ** 2 + 4 * z * z * r * (1 + r) ** 2)


EX['beta'] = W_[0] / W_[1]
EX['rho12'] = rho(EX['beta'])
_u = U[1, :]
EX['u_top_cqc'] = math.sqrt(_u[0] ** 2 + _u[1] ** 2 + 2 * EX['rho12'] * _u[0] * _u[1])

# ---------------- 3DOF m、m、m/2（2016-4、2024-1 型）----------------
K3 = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 1.0]])
M3 = np.diag([1, 1, 0.5])
lam3, PHI3 = eig(K3, M3)
EX3 = dict(lam=lam3, phi=PHI3 / PHI3[2, :])      # 頂層正規化為 1 方便看形狀
EX3['poly_roots'] = sorted(np.roots([1, -6, 9, -2]).real)    # λ = ω²·(m/k)·?：檢查特性式
# 特性式：det(K − λM)，λ = ω²m/k；展開為 −0.5λ³ + 3λ² − 4.5λ + 1 = 0 → λ³ − 6λ² + 9λ − 2 = 0

# ---------------- 2016-1：頂層三角脈衝的模態疊加 ----------------
# M = diag(2m, m)、K = [[3k,−k],[−k,k]]，m = 2000 kg、k = 1e5 N/m；φ1 = {1,2}、φ2 = {1,−1}
Q2016 = dict(m=2000.0, k=1e5)
Q2016['w'] = (5.0, 10.0)
Q2016['M1'] = 6 * Q2016['m']; Q2016['M2'] = 3 * Q2016['m']
Q2016['amp1'] = 0.8; Q2016['amp2'] = 0.4        # 題解：η1 = 0.8 sin5(t−0.1)、η2 = −0.4 sin10(t−0.1)
Q2016['I'] = Q2016['amp1'] * Q2016['M1'] * 5 / 2   # η̇1 = 2I/M1 → I = amp1·ω1·M1/2 = 24000 N·s
Q2016['chk2'] = Q2016['I'] / Q2016['M2'] / 10      # = 0.4 ✔
Q2016['v2max_abs'] = 1.6 + 0.4                     # 頂層兩振態絕對值相加上界

# ---------------- 2021-3：初始位移展開（結果）----------------
Q2021_3 = dict(V3max_k=4.0)   # |V3|max = 4k（cm）

# ---------------- 2008-1：由週期反推 k ----------------
Q2008 = dict(m=1500.0, T1=0.197, T2=0.0752)
# 等質量等勁度兩層：ω1² = (3−√5)/2·k/m
Q2008['k_from_T1'] = (2 * PI / Q2008['T1']) ** 2 * Q2008['m'] / ((3 - math.sqrt(5)) / 2)
Q2008['k_from_T2'] = (2 * PI / Q2008['T2']) ** 2 * Q2008['m'] / ((3 + math.sqrt(5)) / 2)

# ---------------- 第 5 章：等位移、等能量 ----------------
RMU = {mu: dict(eq_disp=mu, eq_energy=math.sqrt(2 * mu - 1)) for mu in (1, 2, 3, 4, 5)}
# 範例：範例結構第一振態，μ = 4（等位移）→ 設計基底剪力 = Ve/μ、位移不變
EX['VB1_design_mu4'] = VB[0] / 4

# 2021-4：題解結果
Q2021_4 = dict(umax=7.45, mu=2.61)


if __name__ == '__main__':
    np.set_printoptions(precision=5, suppress=True)
    for k_, v_ in EX.items():
        print(k_, '=', v_)
    print('3DOF', EX3)
    print('2016-1', Q2016)
    print('2008-1', Q2008)
    print('RMU', RMU)


# ---------------- 第 1 章：2012-1 加質量反推 m、k ----------------
Q2012 = dict(T1=1.2, T2=1.4, dm=1806.0)
Q2012['ratio'] = (Q2012['T2'] / Q2012['T1']) ** 2
Q2012['m'] = Q2012['dm'] / (Q2012['ratio'] - 1)
Q2012['k'] = 4 * PI ** 2 * Q2012['m'] / Q2012['T1'] ** 2

_t16 = np.linspace(0.1, 3.0, 20001)
_v2 = 1.6 * np.sin(5 * (_t16 - 0.1)) + 0.4 * np.sin(10 * (_t16 - 0.1))
Q2016['v2max'] = float(np.abs(_v2).max()); Q2016['t_v2max'] = float(_t16[np.abs(_v2).argmax()])
_v1 = 0.8 * np.sin(5 * (_t16 - 0.1)) - 0.4 * np.sin(10 * (_t16 - 0.1))
Q2016['v1max'] = float(np.abs(_v1).max())


# ---------------- 第 5 章：合成地震下的模態組合示範（以範例結構）----------------
def _sdof_D(ag, dt, w, xi):
    """D(t)：ü + 2ξωu̇ + ω²u = −ag，常加速度法。"""
    n = len(ag); u = np.zeros(n); v = np.zeros(n); a = np.zeros(n)
    a[0] = -ag[0]
    kh = w * w + 2 * xi * w * 2 / dt + 4 / dt ** 2
    for i in range(n - 1):
        ph = -ag[i + 1] + (4 / dt ** 2 * u[i] + 4 / dt * v[i] + a[i]) + 2 * xi * w * (2 / dt * u[i] + v[i])
        u[i + 1] = ph / kh
        v[i + 1] = 2 / dt * (u[i + 1] - u[i]) - v[i]
        a[i + 1] = 4 / dt ** 2 * (u[i + 1] - u[i]) - 4 / dt * v[i] - a[i]
    return u


def synth_ground(seed, dur=20.0, dt=0.01):
    rng = np.random.default_rng(seed)
    n = int(dur / dt)
    t = np.arange(n) * dt
    wn = rng.standard_normal(n)
    # 以二階濾波（Kanai–Tajimi 型，ωg = 4π、ξg = 0.6）＋包絡
    ag = _sdof_D(wn, dt, 4 * PI, 0.6) * (4 * PI) ** 2 * -1
    env = np.minimum(1, t / 2) * np.exp(-np.maximum(0, t - 8) / 4)
    return t, ag * env


COMB = []
for _seed in range(1, 21):
    _t, _ag = synth_ground(_seed)
    _q = [GAM[n] * (PHI[1, n] - PHI[0, n]) * _sdof_D(_ag, 0.01, W_[n], 0.05) for n in range(2)]
    _true = float(np.abs(_q[0] + _q[1]).max())
    _p = [float(np.abs(x).max()) for x in _q]
    COMB.append(dict(true=_true, srss=math.sqrt(_p[0] ** 2 + _p[1] ** 2), absum=_p[0] + _p[1], p=_p))
COMB_STATS = dict(srss_ratio=float(np.mean([c['srss'] / c['true'] for c in COMB])),
                  abs_ratio=float(np.mean([c['absum'] / c['true'] for c in COMB])))
_t, _ag = synth_ground(1)
COMB_TH = (_t, [GAM[n] * (PHI[1, n] - PHI[0, n]) * _sdof_D(_ag, 0.01, W_[n], 0.05) for n in range(2)])
