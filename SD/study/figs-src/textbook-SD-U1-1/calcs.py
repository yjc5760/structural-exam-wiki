# -*- coding: utf-8 -*-
"""SD-U1-1 結構動力基本性質及原理：教科書講義的所有數值（圖與內文共用）。
單位：SI（kg、N、m、s），2009-2 為英制（lb、in、s）。
考題數字取自 raw/solutions/SD-YYYY-N/SD-YYYY-N.md（2026-11 勘誤後版本）。
"""
import math
import numpy as np

PI = math.pi

# ---------------- 貫穿全冊的範例：SD-2021-2 的那台結構 ----------------
# m = 1e4 kg、ω = 10 rad/s；ξ 由第 3 章的兩組穩態振幅反求
EX = dict(m=1.0e4, w=10.0)
EX['k'] = EX['m'] * EX['w'] ** 2            # N/m
EX['T'] = 2 * PI / EX['w']                  # s
EX['f'] = 1 / EX['T']                       # Hz
EX['ccr'] = 2 * EX['m'] * EX['w']           # N·s/m
# 第 3 章：ω̄ = 0.1 → 2.4 cm（準靜態）、ω̄ = 10 → 20 cm（共振）
EX['u_st'] = 2.4   # cm
EX['u_res'] = 20.0  # cm
EX['xi'] = EX['u_st'] / (2 * EX['u_res'])   # 0.06
EX['c'] = EX['xi'] * EX['ccr']
EX['wD'] = EX['w'] * math.sqrt(1 - EX['xi'] ** 2)
EX['p0_harm'] = EX['k'] * EX['u_st'] / 100  # N（題目沒給，反推 = k·u_st）
# r = 0.01 時 Rd 與 1 的差（說明「準靜態」）
EX['Rd_001'] = 1 / math.sqrt((1 - 0.01 ** 2) ** 2 + (2 * EX['xi'] * 0.01) ** 2)


def Rd(r, xi):
    return 1 / math.sqrt((1 - r * r) ** 2 + (2 * xi * r) ** 2)


def phase(r, xi):
    return math.atan2(2 * xi * r, 1 - r * r)   # rad，0~π


def TR(r, xi):
    return math.sqrt(1 + (2 * xi * r) ** 2) * Rd(r, xi)


# ---------------- 第 2 章：自由振動、對數衰減 ----------------
def decay_ratio(xi, j=1, exact=True):
    if exact:
        return math.exp(-2 * PI * xi * j / math.sqrt(1 - xi * xi))
    return math.exp(-2 * PI * xi * j)


DEC = {}
for xi in (0.02, 0.05, 0.10, 0.20):
    DEC[xi] = dict(approx=decay_ratio(xi, 1, False), exact=decay_ratio(xi, 1, True),
                   delta_exact=2 * PI * xi / math.sqrt(1 - xi * xi), delta_approx=2 * PI * xi,
                   wD_w=math.sqrt(1 - xi * xi))
# SD-2017-1：ξ=0.05、初位移 v0、初速 0，3 個完整週期後
Q2017 = dict(xi=0.05)
Q2017['A3'] = math.exp(-6 * PI * 0.05)          # 0.390 v0
Q2017['A15'] = math.exp(-3 * PI * 0.05)         # 誤讀 1.5 週期：0.624 v0
Q2017['per'] = math.exp(-2 * PI * 0.05)         # 每週期 0.730
Q2017['X0'] = 1 / math.sqrt(1 - 0.05 ** 2)      # 初始振幅（含 ξωu0/ωD 項）1.00125 v0
# 反向用法：振幅 5 週期減半 → ξ
Q_half = dict(j=5)
Q_half['xi'] = math.log(2) / (2 * PI * 5)        # 0.0221

# ---------------- 第 3 章：簡諧外力 ----------------
H = {}
H['Rd_res'] = {xi: 1 / (2 * xi) for xi in (0.02, 0.05, 0.06, 0.10, 0.20)}
H['r_peak'] = {xi: math.sqrt(1 - 2 * xi * xi) for xi in (0.05, 0.20)}
H['Rd_peak'] = {xi: 1 / (2 * xi * math.sqrt(1 - xi * xi)) for xi in (0.05, 0.20)}
# SD-2008-3：阻尼 2% → 20%，共振位移比
H['q2008_ratio'] = (1 / (2 * 0.20)) / (1 / (2 * 0.02))   # 0.1
# 傳導率：r = √2 時 TR = 1（任何 ξ）
H['TR_sqrt2'] = {xi: TR(math.sqrt(2), xi) for xi in (0.0, 0.1, 0.3)}
H['TR_r3'] = {xi: TR(3.0, xi) for xi in (0.0, 0.1, 0.3)}
# SD-2009-2（英制、ξ=0）
Q2009 = dict(W=6500.0, F0=700.0, FT=50.0, fHz=12.0, g=386.0)
Q2009['TR'] = Q2009['FT'] / Q2009['F0']            # 1/14
Q2009['r2'] = 1 / Q2009['TR'] + 1                  # 15
Q2009['r'] = math.sqrt(Q2009['r2'])
Q2009['Om'] = 2 * PI * Q2009['fHz']                # 75.40 rad/s
Q2009['wn'] = Q2009['Om'] / Q2009['r']             # 19.47
Q2009['fn'] = Q2009['wn'] / (2 * PI)               # 3.10 Hz
Q2009['m'] = Q2009['W'] / Q2009['g']               # 16.84
Q2009['k'] = Q2009['m'] * Q2009['wn'] ** 2         # 6382 lb/in
# TMD（Den Hartog）
TMD = {}
for mu in (0.01, 0.02, 0.05):
    TMD[mu] = dict(f=1 / (1 + mu), xi=math.sqrt(3 * mu / (8 * (1 + mu) ** 3)))

# ---------------- 第 4 章：脈衝 ----------------
# 半正弦脈衝（SD-2021-2 ㈡）：p0 = 1e5 N、td = 0.1 s
PUL = dict(p0=1.0e5, td=0.1)
PUL['I'] = 2 * PUL['p0'] * PUL['td'] / PI          # 6366 N·s
PUL['ust'] = PUL['p0'] / EX['k']                    # 0.1 m
PUL['td_T'] = PUL['td'] / EX['T']                   # 0.159
PUL['u_imp'] = PUL['I'] / (EX['m'] * EX['w'])       # 0.0637 m


def sdof_sim(p_fun, m, k, xi, t_end, dt=1e-4, u0=0.0, v0=0.0):
    """常加速度法（Newmark β=1/4）。回傳 t, u, v。"""
    w = math.sqrt(k / m); c = 2 * xi * m * w
    n = int(round(t_end / dt)) + 1
    t = np.linspace(0, t_end, n)
    u = np.zeros(n); v = np.zeros(n); a = np.zeros(n)
    u[0], v[0] = u0, v0
    a[0] = (p_fun(0) - c * v0 - k * u0) / m
    kh = k + 2 * c / dt + 4 * m / dt ** 2
    for i in range(n - 1):
        ph = p_fun(t[i + 1]) + m * (4 / dt ** 2 * u[i] + 4 / dt * v[i] + a[i]) + c * (2 / dt * u[i] + v[i])
        u[i + 1] = ph / kh
        v[i + 1] = 2 / dt * (u[i + 1] - u[i]) - v[i]
        a[i + 1] = 4 / dt ** 2 * (u[i + 1] - u[i]) - 4 / dt * v[i] - a[i]
    return t, u, v


def halfsine(t):
    return PUL['p0'] * math.sin(PI * t / PUL['td']) if 0 <= t <= PUL['td'] else 0.0


_t, _u, _v = sdof_sim(halfsine, EX['m'], EX['k'], EX['xi'], 1.0)
PUL['umax_damped'] = float(_u.max())
PUL['t_at_max'] = float(_t[_u.argmax()])
PUL['u_td'] = float(np.interp(PUL['td'], _t, _u))
_t0, _u0, _ = sdof_sim(halfsine, EX['m'], EX['k'], 0.0, 1.0)
PUL['umax_undamped'] = float(_u0.max())
PUL_T = (_t, _u)


def shock_spectrum_halfsine(tdT, xi=0.0):
    """半正弦脈衝的最大反應比 umax/ust（數值）。"""
    T = 1.0; w = 2 * PI; m = 1.0; k = w * w; td = tdT * T
    p0 = k * 1.0
    f_ = lambda t: p0 * math.sin(PI * t / td) if 0 <= t <= td else 0.0
    tt, uu, _ = sdof_sim(f_, m, k, xi, td + 1.5 * T, dt=min(td, T) / 400)
    return float(np.abs(uu).max())


# SD-2003-2：分段線性脈衝、ξ = 30 %、m = 100 kg、k = 100 N/m
P03 = dict(m=100.0, k=100.0, xi=0.30)
_pts = [(0, 0), (0.02, 2000), (0.10, 0), (0.12, -500), (0.20, -500), (0.25, 0)]


def p2003(t):
    if t >= 0.25 or t < 0:
        return 0.0
    for (t1, p1), (t2, p2) in zip(_pts[:-1], _pts[1:]):
        if t1 <= t <= t2:
            return p1 + (p2 - p1) * (t - t1) / (t2 - t1)
    return 0.0


P03['I'] = sum((p1 + p2) / 2 * (t2 - t1) for (t1, p1), (t2, p2) in zip(_pts[:-1], _pts[1:]))   # 42.5
_t3, _u3, _v3 = sdof_sim(p2003, P03['m'], P03['k'], P03['xi'], 8.0, dt=2e-4)
P03['umax'] = float(_u3.max()); P03['t_max'] = float(_t3[_u3.argmax()])
P03['T'] = 2 * PI / math.sqrt(P03['k'] / P03['m'])   # 6.28 s
P03['td_T'] = 0.25 / P03['T']
P03['u_imp'] = P03['I'] / (P03['m'] * 1.0)           # 無阻尼衝量近似 0.425 m
# 有阻尼衝量近似：u = I/(m ωD) e^{-ξωt} sin ωD t 的最大值
_wD = math.sqrt(1 - 0.09)
_tp = math.atan(_wD / 0.30) / _wD
P03['u_imp_damped'] = P03['I'] / (P03['m'] * _wD) * math.exp(-0.30 * _tp) * math.sin(_wD * _tp)

# ---------------- 第 5 章：MDOF 性質 ----------------
# SD-2016-3：質量正交
Q2016 = dict(m3=1000.0)
Q2016['alpha'] = 1500.0; Q2016['beta'] = 2250.0
_M = np.diag([1500.0, 2250.0, 1000.0])
_p1 = np.array([1, 2, 3.]); _p2 = np.array([-1, -1, 2.]); _p3 = np.array([1, -1, 1.])
Q2016['chk12'] = float(_p1 @ _M @ _p2); Q2016['chk13'] = float(_p1 @ _M @ _p3)
Q2016['chk23'] = float(_p2 @ _M @ _p3)     # 不為 0：考卷振態本身不完全一致（題解 §5.2）

# SD-2025-3：Rayleigh 阻尼
Q2025 = dict(w=(14.5, 31.1, 46.2), z=0.05)
w1, w2, w3 = Q2025['w']
Q2025['a0'] = 2 * 0.05 * w1 * w3 / (w1 + w3)
Q2025['a1'] = 2 * 0.05 / (w1 + w3)
Q2025['z2'] = Q2025['a0'] / (2 * w2) + Q2025['a1'] * w2 / 2
Q2025['wmin'] = math.sqrt(Q2025['a0'] / Q2025['a1'])         # = √(ω1ω3)
Q2025['zmin'] = math.sqrt(Q2025['a0'] * Q2025['a1'])

# SD-2023-2：兩層剪力屋 + Rayleigh 阻尼（兩點不同 ξ）
Q2023 = dict(m=10000.0, k1=200000.0, k2=180000.0)
K = np.array([[Q2023['k1'] + Q2023['k2'], -Q2023['k2']], [-Q2023['k2'], Q2023['k2']]])
M = np.diag([Q2023['m'], Q2023['m']])
lam, vec = np.linalg.eig(np.linalg.solve(M, K))
lam, vec = lam.real, vec.real
idx = np.argsort(lam); lam = lam[idx]; vec = vec[:, idx]
vec = vec / vec[1, :]                     # 頂層正規化為 1
Q2023['w'] = np.sqrt(lam)
Q2023['f'] = Q2023['w'] / (2 * PI)
Q2023['phi'] = vec
Q2023['Mn'] = [float(vec[:, i] @ M @ vec[:, i]) for i in range(2)]
Q2023['Kn'] = [float(vec[:, i] @ K @ vec[:, i]) for i in range(2)]
Q2023['Ln'] = [float(vec[:, i] @ M @ np.ones(2)) for i in range(2)]
Q2023['G'] = [Q2023['Ln'][i] / Q2023['Mn'][i] for i in range(2)]
Q2023['Meff'] = [Q2023['Ln'][i] ** 2 / Q2023['Mn'][i] for i in range(2)]
wa, wb, za, zb = 2 * PI, 10 * PI, 0.03, 0.05
A = np.array([[1 / (2 * wa), wa / 2], [1 / (2 * wb), wb / 2]])
Q2023['alpha'], Q2023['beta'] = np.linalg.solve(A, [za, zb])
Q2023['alpha'], Q2023['beta'] = float(Q2023['alpha']), float(Q2023['beta'])
Q2023['xi1'] = Q2023['alpha'] / (2 * Q2023['w'][0]) + Q2023['beta'] * Q2023['w'][0] / 2
Q2023['xi2'] = Q2023['alpha'] / (2 * Q2023['w'][1]) + Q2023['beta'] * Q2023['w'][1] / 2
# Rayleigh 商：以「各樓層重量當側力」的靜變形為形狀
_F = M @ np.ones(2) * 9.81
_u = np.linalg.solve(K, _F)
Q2023['RQ_w'] = math.sqrt(9.81 * (np.ones(2) @ M @ _u) / (_u @ M @ _u))
Q2023['RQ_lin'] = math.sqrt((np.array([1, 2.]) @ K @ np.array([1, 2.])) / (np.array([1, 2.]) @ M @ np.array([1, 2.])))
Q2023['RQ_uni'] = math.sqrt((np.array([1, 1.]) @ K @ np.array([1, 1.])) / (np.array([1, 1.]) @ M @ np.array([1, 1.])))

# 三軸譜：T = 1 s、Sa = 0.5 g
SP = dict(T=1.0, Sa=0.5 * 9.81)
SP['w'] = 2 * PI / SP['T']
SP['Sv'] = SP['Sa'] / SP['w']
SP['Sd'] = SP['Sa'] / SP['w'] ** 2


if __name__ == '__main__':
    def pr(name, d):
        print('==', name)
        for k_, v_ in d.items():
            if isinstance(v_, float):
                print(f'  {k_} = {v_:.6g}')
            else:
                print(f'  {k_} = {v_}')
    pr('EX', EX); print(' DEC', {k_: {a: round(b, 4) for a, b in v_.items()} for k_, v_ in DEC.items()})
    pr('Q2017', Q2017); pr('Q_half', Q_half)
    print(' H', H); pr('Q2009', Q2009); print(' TMD', TMD)
    pr('PUL', PUL); pr('P03', P03)
    pr('Q2016', Q2016); pr('Q2025', Q2025); pr('Q2023', Q2023); pr('SP', SP)
    for tdT in (0.1, 0.159, 0.25, 0.5, 0.8, 1.0, 2.0):
        print('shock', tdT, round(shock_spectrum_halfsine(tdT), 4))


# ---------------- 第 3 章：TMD 頻率反應（主結構 ξ = 0.02、μ = 0.05、Den Hartog 最佳） ----------------
def tmd_response(r, mu=0.05, xi_s=0.02, f=None, xi_d=None, with_tmd=True):
    """主質量位移 / (p0/K)，外力作用在主質量。r = ω̄/ω_s。"""
    f = TMD[mu]['f'] if f is None else f
    xi_d = TMD[mu]['xi'] if xi_d is None else xi_d
    Mm, Kk = 1.0, 1.0
    ws = 1.0
    w_ = r * ws
    Zs = Kk - Mm * w_ ** 2 + 2j * xi_s * Mm * ws * w_
    if not with_tmd:
        return abs(1 / Zs)
    md = mu * Mm; wd = f * ws; kd = md * wd ** 2; cd = 2 * xi_d * md * wd
    Zd = kd + 1j * cd * w_
    A = np.array([[Zs + Zd, -Zd], [-Zd, Zd - md * w_ ** 2]])
    x = np.linalg.solve(A, np.array([1.0, 0.0]))
    return abs(x[0])


_rr = np.linspace(0.7, 1.3, 1201)
TMDR = dict(peak_without=max(tmd_response(r, with_tmd=False) for r in _rr),
            peak_with=max(tmd_response(r) for r in _rr))
