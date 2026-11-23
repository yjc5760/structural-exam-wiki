# -*- coding: utf-8 -*-
"""SM-U2-2 深基礎 教科書講義的所有數值。單位：kN、m、kPa；γw = 9.81 kN/m³。

考題數字取自 raw/solutions/SM-YYYY-N/SM-YYYY-N.md（2026-11-15 後版本）。
執行 `python3 calcs.py` 印出所有數字，與內文逐一對照。
"""
import math

GW = 9.81
PA = 100.0
r = math.radians


def circ(D):
    return math.pi * D ** 2 / 4, math.pi * D


# ---------- 貫穿範例：SM-2007-3 砂土打入樁（第 1、2、3 章） ----------
def ex2007_3():
    d = dict(L=15.0, D=0.5, g=18.0, phi=30.0, Nq=21.0, FSp=4.0, FSs=3.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['Lc'] = 20 * d['D']
    d['qc'] = d['g'] * d['Lc']                      # 臨界深度處 σv'
    d['K'] = 1.8 * (1 - math.sin(r(d['phi'])))
    d['delta'] = 0.5 * d['phi']
    d['fmax'] = d['K'] * d['qc'] * math.tan(r(d['delta']))
    d['Qs1'] = d['p'] * 0.5 * d['fmax'] * d['Lc']
    d['Qs2'] = d['p'] * d['fmax'] * (d['L'] - d['Lc'])
    d['Qs'] = d['Qs1'] + d['Qs2']
    d['Qp'] = d['qc'] * d['Nq'] * d['Ap']
    d['Qa'] = d['Qp'] / d['FSp'] + d['Qs'] / d['FSs']
    d['Qa_wrong'] = (d['Qp'] + d['Qs']) / 3.5          # 先加後除（隨便取 3.5）對照
    d['Qa_sum4'] = (d['Qp'] + d['Qs']) / 4.0
    d['Qa_sum3'] = (d['Qp'] + d['Qs']) / 3.0
    # 錯解：不封頂（σv' 一路線性到 15 m）
    d['q15'] = d['g'] * d['L']
    d['Qs_nocap'] = d['p'] * 0.5 * d['K'] * d['q15'] * math.tan(r(d['delta'])) * d['L']
    d['Qp_nocap'] = d['q15'] * d['Nq'] * d['Ap']
    return d


# ---------- SM-2024-4 由 FS 反求樁長（第 3 章） ----------
def ex2024_4():
    d = dict(Q=2000.0, FS=2.5, D=1.0, cu=60.0, alpha=0.62, Nc=9.0,
             gm=17.98, w=0.16, Gs=2.65, phi=38.0, Nq=20.0)
    d['Qu'] = d['Q'] * d['FS']
    d['Ap'], d['p'] = circ(d['D'])
    # 黏土
    d['Qp_c'] = d['Ap'] * d['cu'] * d['Nc']
    d['fs_c'] = d['alpha'] * d['cu']
    d['L_c'] = (d['Qu'] - d['Qp_c']) / (d['p'] * d['fs_c'])
    # 砂土：三相
    d['gd'] = d['gm'] / (1 + d['w'])
    d['e'] = d['Gs'] * GW / d['gd'] - 1
    d['gsat'] = (d['Gs'] + d['e']) / (1 + d['e']) * GW
    d['gp'] = d['gsat'] - GW
    d['Lcr'] = 15 * d['D']
    d['s0'] = d['gp'] * d['Lcr']
    d['K0'] = 1 - math.sin(r(d['phi']))
    d['dlt'] = 0.8 * d['phi']
    d['fmax'] = d['K0'] * d['s0'] * math.tan(r(d['dlt']))
    d['ql'] = 0.5 * PA * d['Nq'] * math.tan(r(d['phi']))
    d['qpN'] = d['s0'] * d['Nq']
    d['Qp_s'] = d['Ap'] * min(d['qpN'], d['ql'])
    d['Qs1'] = 0.5 * d['p'] * d['Lcr'] * d['fmax']
    d['Qs2'] = d['Qu'] - d['Qp_s'] - d['Qs1']
    d['L2'] = d['Qs2'] / (d['p'] * d['fmax'])
    d['L_s'] = d['Lcr'] + d['L2']
    # 錯解：直接 γ' = 17.98 − 9.81
    gw_ = d['gm'] - GW
    s0w = gw_ * d['Lcr']
    fw = d['K0'] * s0w * math.tan(r(d['dlt']))
    Qs1w = 0.5 * d['p'] * d['Lcr'] * fw
    d['L_s_wrong'] = d['Lcr'] + (d['Qu'] - d['Qp_s'] - Qs1w) / (d['p'] * fw)
    return d


# ---------- SM-2021-3 雙層樁＋拉拔（第 1、3 章） ----------
def ex2021_3():
    d = dict(D=0.6, Ls=6.0, Lcl=6.0, gs=19.2, phi=32.0, cu=100.0, alpha=0.65, Nc=9.0, gc=24.0, FS=3.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['L'] = d['Ls'] + d['Lcl']
    d['Wp'] = d['Ap'] * d['L'] * (d['gc'] - GW)
    d['gp'] = d['gs'] - GW
    d['K0'] = 1 - math.sin(r(d['phi']))
    d['K'] = 1.4 * d['K0']
    d['dlt'] = 0.8 * d['phi']
    d['sv6'] = d['gp'] * d['Ls']
    d['fs1'] = d['K'] * d['sv6'] / 2 * math.tan(r(d['dlt']))
    d['Qs1'] = d['fs1'] * d['p'] * d['Ls']
    d['fs2'] = d['alpha'] * d['cu']
    d['Qs2'] = d['fs2'] * d['p'] * d['Lcl']
    d['Qs'] = d['Qs1'] + d['Qs2']
    d['Qp'] = d['cu'] * d['Nc'] * d['Ap']
    d['Qa'] = (d['Qs'] + d['Qp']) / d['FS']
    d['Tu'] = d['Qs'] + d['Wp']
    d['Ta'] = d['Qs'] / d['FS'] + d['Wp']
    return d


# ---------- SM-2012-3 抗拔樁反求貫入深度（第 1 章） ----------
def ex2012_3():
    d = dict(D=0.5, H1=8.0, a1=1.0, cu1=45.0, a2=0.75, cu2=70.0, gc=23.0, T=1200.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['gcp'] = d['gc'] - GW
    d['Qs1'] = d['a1'] * d['cu1'] * d['p'] * d['H1']
    d['W1'] = d['gcp'] * d['Ap'] * d['H1']
    d['T1'] = d['Qs1'] + d['W1']
    d['k2'] = d['a2'] * d['cu2'] * d['p'] + d['gcp'] * d['Ap']   # 每公尺增加
    d['x'] = (d['T'] - d['T1']) / d['k2']
    d['L'] = d['H1'] + d['x']
    return d


# ---------- SM-2023-3 零供給三層砂（第 3 章） ----------
def ex2023_3():
    d = dict(D=0.5, K=1.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['Lc'] = 20 * d['D']
    N = [12, 15, 30]
    d['phis'] = [27 + 0.3 * n for n in N]
    d['s5'] = 18 * 5
    d['s10'] = d['s5'] + 20 * 5
    t = lambda ph: math.tan(r(ph))
    seg = [(45, d['phis'][0], 5), (140, d['phis'][1], 5), (190, d['phis'][1], 5), (190, d['phis'][2], 10)]
    d['Qseg'] = [d['K'] * s * t(ph) * d['p'] * Lh for s, ph, Lh in seg]
    d['Qs'] = sum(d['Qseg'])
    ph3 = d['phis'][2]
    d['Nq'] = math.exp(math.pi * t(ph3)) * math.tan(r(45 + ph3 / 2)) ** 2
    d['Qp'] = d['s10'] * d['Nq'] * d['Ap']
    d['Qp45'] = d['s10'] * 45 * d['Ap']
    d['Qs_K15'] = d['Qs'] * 1.5
    return d


# ---------- SM-2005-4 位移相容（第 4 章） ----------
def ex2005_4():
    d = dict(D=1.2, L=12.0, tmax=10.0, smax=2.0, qmax=400.0, dmax=8.0)
    d['As'] = math.pi * d['D'] * d['L']
    d['Ap'] = math.pi * d['D'] ** 2 / 4
    d['Qsm'] = d['tmax'] * d['As']
    d['Qpm'] = d['qmax'] * d['Ap']
    d['Qu'] = d['Qsm'] + d['Qpm']
    d['Qall3'] = d['Qu'] / 3
    Q = lambda s: min(d['tmax'], d['tmax'] / d['smax'] * s) * d['As'] + min(d['qmax'], d['qmax'] / d['dmax'] * s) * d['Ap']
    d['Qfun'] = Q
    d['Q1'] = Q(1.0)
    d['Q15'] = Q(1.5)
    d['Q2'] = Q(2.0)
    return d


# ---------- SM-2014-2 沉陷三分量（第 4 章） ----------
def ex2014_2():
    d = dict(D=1.2, L=25.0, Ep=2.0e7, Es=3.0e4, mu=0.35, Iwp=0.85, Qt=4500.0, z1=18.0, f=50.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['Qws'] = d['p'] * (0.5 * d['z1'] * d['f'] + (d['L'] - d['z1']) * d['f'])
    d['Qwp'] = d['Qt'] - d['Qws']
    d['qwp'] = d['Qwp'] / d['Ap']
    integ = 25 * d['Qt'] - 7075 * d['p']
    d['intQ'] = integ
    d['Se1'] = integ / (d['Ap'] * d['Ep']) * 1000
    d['Se2'] = d['qwp'] * d['D'] / d['Es'] * (1 - d['mu'] ** 2) * d['Iwp'] * 1000
    d['Iws'] = 2 + 0.35 * math.sqrt(d['L'] / d['D'])
    d['fav'] = d['Qws'] / (d['p'] * d['L'])
    d['Se3'] = d['fav'] * d['D'] / d['Es'] * (1 - d['mu'] ** 2) * d['Iws'] * 1000
    d['Se'] = d['Se1'] + d['Se2'] + d['Se3']
    # 軸力分布 Q(z)
    def Qz(z):
        if z <= d['z1']:
            return d['Qt'] - d['p'] * d['f'] / d['z1'] * z ** 2 / 2
        return d['Qt'] - d['p'] * d['f'] * d['z1'] / 2 - d['p'] * d['f'] * (z - d['z1'])
    d['Qz'] = Qz
    d['Se1_naive'] = d['Qt'] * d['L'] / (d['Ap'] * d['Ep']) * 1000
    return d


# ---------- 勁度 ODE 無因次曲線（第 4 章） ----------
def stiff_ratio(lamL):
    return math.tanh(lamL)


# ---------- 群樁效率 Converse–Labarre 示例（第 5 章） ----------
def eg_CL(n1=3, n2=3, D=0.5, s=1.5):
    th = math.degrees(math.atan(D / s))
    return 1 - th / 90 * ((n1 - 1) * n2 + (n2 - 1) * n1) / (n1 * n2), th


# ---------- 第 6 章綜合重建練習（自編） ----------
def practice():
    d = dict(D=0.6, L=18.0, gp=10.0, phi=32.0, Nq=30.0, FS=3.0, gc=24.0)
    d['Ap'], d['p'] = circ(d['D'])
    d['Lc'] = 20 * d['D']
    d['sc'] = d['gp'] * d['Lc']
    d['K'] = 1.4 * (1 - math.sin(r(d['phi'])))
    d['fmax'] = d['K'] * d['sc'] * math.tan(r(0.8 * d['phi']))
    d['Qs'] = d['p'] * (0.5 * d['fmax'] * d['Lc'] + d['fmax'] * (d['L'] - d['Lc']))
    d['ql'] = 0.5 * PA * d['Nq'] * math.tan(r(d['phi']))
    d['Qp'] = d['Ap'] * min(d['sc'] * d['Nq'], d['ql'])
    d['Qa'] = (d['Qs'] + d['Qp']) / d['FS']
    d['W'] = d['Ap'] * d['L'] * (d['gc'] - GW)
    d['Ta'] = d['Qs'] / d['FS'] + d['W']
    return d


if __name__ == '__main__':
    for nm, fn in [('2007-3', ex2007_3), ('2024-4', ex2024_4), ('2021-3', ex2021_3), ('2012-3', ex2012_3),
                   ('2023-3', ex2023_3), ('2005-4', ex2005_4), ('2014-2', ex2014_2), ('practice', practice)]:
        print('=====', nm)
        for k, v in fn().items():
            if callable(v):
                continue
            if isinstance(v, float):
                print(f'  {k} = {v:.4f}')
            elif isinstance(v, list):
                print(f'  {k} = {[round(x, 3) for x in v]}')
            else:
                print(f'  {k} = {v}')
    print('Eg(3x3, s=3D) =', [round(x, 4) for x in eg_CL()])
    print('tanh(1),tanh(2),tanh(3) =', [round(stiff_ratio(x), 4) for x in (1, 2, 3)])
