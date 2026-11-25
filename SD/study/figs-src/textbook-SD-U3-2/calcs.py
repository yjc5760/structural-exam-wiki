# -*- coding: utf-8 -*-
"""SD-U3-2 隔減震原理：教科書講義的所有數值。單位依考題（cm、kN、tf、s）。"""
import math
import numpy as np

PI = math.pi

# ---------- 第 1 章：譜的兩端（示範：Sa = SD1/T、平台 SDS） ----------
DEMO = dict(SDS=0.8, SD1=0.45)


def Sa_demo(T):
    T0 = DEMO['SD1'] / DEMO['SDS']
    return DEMO['SDS'] if T <= T0 else DEMO['SD1'] / T


def Sd_demo(T, g=981.0):
    return Sa_demo(T) * g * T * T / (4 * PI ** 2)


ISO = dict(T_fixed=0.5, T_iso=2.5)
ISO['Sa_fixed'] = Sa_demo(ISO['T_fixed']); ISO['Sa_iso'] = Sa_demo(ISO['T_iso'])
ISO['Sd_fixed'] = Sd_demo(ISO['T_fixed']); ISO['Sd_iso'] = Sd_demo(ISO['T_iso'])

# 串聯週期：T_sys² = T_eD² + T²
SER = dict(TeD=2.5, T=0.5)
SER['Tsys'] = math.sqrt(SER['TeD'] ** 2 + SER['T'] ** 2)
SER['DpD'] = 1 / math.sqrt(1 + (SER['T'] / SER['TeD']) ** 2)     # D′D/DD


# ---------- 2011-1：隔震 2DOF 反應譜 ----------
def q2011(order='upper_first'):
    g = 981.0
    Wu, Wb = 300.0, 200.0
    if order == 'upper_first':
        m = np.diag([Wu, Wb]) / g
    else:
        m = np.diag([Wb, Wu]) / g
    phi = np.array([[1.041, -0.641], [1.000, 1.000]])
    T = [2.0, 0.25]
    B1, BS = 1.25, 1.0
    Sa = [0.6 / (T[0] * B1), 0.6 / BS]
    out = {}
    U = []
    for n in range(2):
        p = phi[:, n]
        Mn = p @ m @ p; Ln = p @ m @ np.ones(2)
        G = Ln / Mn
        Sd = Sa[n] * g * T[n] ** 2 / (4 * PI ** 2)
        U.append(G * p * Sd)
    U = np.array(U).T
    return dict(U=U, Sa=Sa)


Q2011 = {k: q2011(k) for k in ('upper_first', 'base_first')}

# ---------- 2016-5／2018-4：FPS ----------
def fps_T(R_cm, g=980.0):
    return 2 * PI * math.sqrt(R_cm / g)


FPS_T = {R: fps_T(R * 100) for R in (1.0, 2.0, 3.0, 4.0)}   # R 以 m
B_TAB = [(2, 0.80), (5, 1.00), (10, 1.25), (20, 1.50), (30, 1.63), (40, 1.70), (50, 1.75)]


def B_of(xi_pct):
    for (x1, b1), (x2, b2) in zip(B_TAB[:-1], B_TAB[1:]):
        if x1 <= xi_pct <= x2:
            return b1 + (b2 - b1) * (xi_pct - x1) / (x2 - x1)
    return B_TAB[-1][1] if xi_pct > 50 else B_TAB[0][1]


def xi_of_B(B):
    for (x1, b1), (x2, b2) in zip(B_TAB[:-1], B_TAB[1:]):
        if b1 <= B <= b2:
            return x1 + (x2 - x1) * (B - b1) / (b2 - b1)
    return None


Q2018 = dict(D=25.0, A=0.08, g=980.0)
Q2018['Te'] = 2 * PI * math.sqrt(Q2018['D'] / (Q2018['A'] * Q2018['g']))
Q2018['Sa'] = min(0.48 / Q2018['Te'], 0.8)
Q2018['B'] = Q2018['g'] * Q2018['Sa'] * Q2018['Te'] ** 2 / (4 * PI ** 2 * Q2018['D'])
Q2018['xi'] = xi_of_B(Q2018['B']) / 100
Q2018['mu'] = Q2018['A'] * PI / 2 * Q2018['xi']
Q2018['R'] = Q2018['D'] / (Q2018['A'] - Q2018['mu'])

# ---------- 第 3 章：等值阻尼（2023-4、2023-3） ----------
Q2023_4 = dict(m=1.0, k=16 * PI ** 2)
Q2023_4['wn'] = math.sqrt(Q2023_4['k'] / Q2023_4['m'])         # 4π


def xi_eq(ED, u0, wbar, m=1.0, k=16 * PI ** 2):
    Es0 = 0.5 * k * u0 ** 2
    wn = math.sqrt(k / m)
    return ED / (4 * PI * Es0) * wn / wbar


TAB4 = {}
for wbar in (2 * PI, 4 * PI):
    for rho in (0.01, 0.02):
        EDa = PI * (5 * wbar) * rho * rho          # 橢圓：π × (u = 0 時的力) × 振幅
        EDb = PI * (20 * PI * rho) * rho
        EDc = 4 * (0.4 * PI) * rho
        TAB4[(wbar, rho)] = (xi_eq(EDa, rho, wbar), xi_eq(EDb, rho, wbar), xi_eq(EDc, rho, wbar))

Q2023_3 = dict(W=5000.0, D=0.4, K=1000.0, ED=50.0, g=9.81)
Q2023_3['T'] = 2 * PI * math.sqrt(Q2023_3['W'] / (Q2023_3['K'] * Q2023_3['g']))
Q2023_3['beta'] = Q2023_3['ED'] / (2 * PI * Q2023_3['K'] * Q2023_3['D'] ** 2)

# 2008-3：共振位移比
Q2008 = dict(ratio=(1 / (2 * 0.2)) / (1 / (2 * 0.02)))

# ---------- 第 4 章：雙線性 LRB 迭代（示範數值） ----------
LRB = dict(W=10000.0, Fy=500.0, ko=25000.0, alpha=0.10, SD1=0.45, g=9.81)
LRB['Dy'] = LRB['Fy'] / LRB['ko']
LRB['kd'] = LRB['alpha'] * LRB['ko']
LRB['Q'] = LRB['Fy'] * (1 - LRB['alpha'])


def lrb_iter(D0=0.20, n=12):
    hist = []
    D = D0
    for _ in range(n):
        K = LRB['Q'] / D + LRB['kd']
        T = 2 * PI * math.sqrt(LRB['W'] / (K * LRB['g']))
        A = 4 * LRB['Q'] * (D - LRB['Dy'])
        xi = A / (2 * PI * K * D * D)
        B = B_of(xi * 100)
        Dn = LRB['g'] * LRB['SD1'] * T / (4 * PI ** 2 * B)
        hist.append(dict(D=D, K=K, T=T, A=A, xi=xi, B=B, Dn=Dn))
        if abs(Dn - D) < 1e-5:
            break
        D = Dn
    return hist


LRB_HIST = lrb_iter()

# ---------- 第 5 章：消能元件 ----------
Q2012 = dict(k=8e4, m=2000.0, c=4e3, th=30.0, xi0=0.05)
Q2012['w'] = math.sqrt(Q2012['k'] / Q2012['m'])
Q2012['T'] = 2 * PI / Q2012['w']
Q2012['ceff'] = Q2012['c'] * math.cos(math.radians(Q2012['th'])) ** 2
Q2012['xid'] = Q2012['ceff'] / (2 * Q2012['m'] * Q2012['w'])
Q2012['beff'] = Q2012['xi0'] + Q2012['xid']
Q2012['B1'] = 1.25 + (1.50 - 1.25) * (Q2012['beff'] * 100 - 10) / 10
Q2012['Sa'] = 0.2 if Q2012['T'] <= 0.6 else 0.12 / Q2012['T']
Q2012['Sd'] = Q2012['Sa'] * 9.81 * Q2012['T'] ** 2 / (4 * PI ** 2) / Q2012['B1']
# 用提示式 WVj 驗算：β_eff = β + W_V/(4πW_k)，W_V = 2π²/T·C·(δ cos θ)²，W_k = ½kδ²
Q2012['beff_hint'] = Q2012['xi0'] + (2 * PI ** 2 / Q2012['T'] * Q2012['c'] * math.cos(math.radians(30)) ** 2) / (4 * PI * 0.5 * Q2012['k'])

Q2018_1 = dict(W=70.0, H=3.0, L=6.0, EI=5000.0, g=9.8)
Q2018_1['k'] = 2 * 12 * Q2018_1['EI'] / Q2018_1['H'] ** 3
Q2018_1['m'] = Q2018_1['W'] / Q2018_1['g']
Q2018_1['w'] = math.sqrt(Q2018_1['k'] / Q2018_1['m'])
Q2018_1['T'] = 2 * PI / Q2018_1['w']
Q2018_1['th'] = math.atan(Q2018_1['H'] / Q2018_1['L'])
Q2018_1['cos2'] = math.cos(Q2018_1['th']) ** 2
Q2018_1['ceff'] = 2 * 0.05 * Q2018_1['m'] * Q2018_1['w']
Q2018_1['C'] = Q2018_1['ceff'] / Q2018_1['cos2']
Q2018_1['Sa'] = min(0.15 / Q2018_1['T'], 0.3) * Q2018_1['g']
Q2018_1['Sd'] = Q2018_1['Sa'] / Q2018_1['w'] ** 2
Q2018_1['Sv'] = Q2018_1['w'] * Q2018_1['Sd']
Q2018_1['Fd'] = Q2018_1['C'] * math.cos(Q2018_1['th']) * Q2018_1['Sv']

# ---------- 第 6 章：TMD（同 U1-1） ----------
TMD = {mu: dict(f=1 / (1 + mu), xi=math.sqrt(3 * mu / (8 * (1 + mu) ** 3))) for mu in (0.01, 0.02, 0.05)}


def tmd_response(r, mu=0.05, xi_s=0.02, with_tmd=True):
    f = TMD[mu]['f']; xi_d = TMD[mu]['xi']
    w_ = r
    Zs = 1 - w_ ** 2 + 2j * xi_s * w_
    if not with_tmd:
        return abs(1 / Zs)
    md = mu; wd = f; kd = md * wd ** 2; cd = 2 * xi_d * md * wd
    Zd = kd + 1j * cd * w_
    A = np.array([[Zs + Zd, -Zd], [-Zd, Zd - md * w_ ** 2]])
    return abs(np.linalg.solve(A, np.array([1.0, 0.0]))[0])


if __name__ == '__main__':
    print('ISO', ISO, 'SER', SER)
    for k_, v_ in Q2011.items():
        print('2011-1', k_, np.round(v_['U'], 3), 'iso max', np.sqrt((v_['U'] ** 2).sum(axis=1)))
    print('FPS_T', FPS_T); print('2018-4', Q2018)
    print('2023-4', {k: tuple(round(x, 4) for x in v) for k, v in TAB4.items()})
    print('2023-3', Q2023_3)
    print('LRB', LRB); [print({a: round(b, 4) for a, b in h.items()}) for h in LRB_HIST]
    print('2012-2', Q2012); print('2018-1', Q2018_1)


def q2011_full():
    g = 981.0
    m = np.diag([300.0, 200.0]) / g
    phi = np.array([[1.041, -0.641], [1.000, 1.000]])
    T = [2.0, 0.25]; Sa = [0.6 / (2.0 * 1.25), 0.6 / 1.0]
    r = dict(G=[], Meff=[], Vb=[], Sd=[], U=[])
    for n in range(2):
        p = phi[:, n]; Mn = p @ m @ p; Ln = p @ m @ np.ones(2)
        r['G'].append(Ln / Mn); r['Meff'].append(Ln ** 2 / Mn * g)          # 以 tf 計（×g）
        r['Vb'].append(Ln ** 2 / Mn * Sa[n] * g)
        Sd = Sa[n] * g * T[n] ** 2 / (4 * PI ** 2); r['Sd'].append(Sd)
        r['U'].append(Ln / Mn * p * Sd)
    U = np.array(r['U'])
    r['iso'] = math.sqrt(U[0, 1] ** 2 + U[1, 1] ** 2)
    r['drift'] = math.sqrt((U[0, 0] - U[0, 1]) ** 2 + (U[1, 0] - U[1, 1]) ** 2)
    r['Vb_srss'] = math.sqrt(sum(v * v for v in r['Vb']))
    r['Sa'] = Sa
    return r


Q2011F = q2011_full()
