# -*- coding: utf-8 -*-
"""SM-U2-3 開挖之穩定性分析｜教科書講義的所有數值。單位 kN、m、kPa（2017-4 依原題用 tf、m）。

考題數字取自 raw/solutions（勘誤後版本）：
  2015-3（貫穿範例：等值參數→Peck→三維隆起）、2011-4（Peck＋鉸接法＋截面模數）、2012-4、
  2005-1（自由端）、2022-4（懸臂淨壓力法）、2020-2（簡化法、砂湧）、2003-3（上舉反算）、2017-4（管湧、上舉、隆起）
"""
import math

GW = 9.81
rad, deg = math.radians, math.degrees
tan = lambda a: math.tan(rad(a))
sin = lambda a: math.sin(rad(a))
cos = lambda a: math.cos(rad(a))


def Ka(phi):
    return tan(45 - phi / 2) ** 2


def Kp(phi):
    return tan(45 + phi / 2) ** 2


# ---------- 第 1 章 ----------
def ex2005_1():
    d = dict(gs=18.0, phi=32.0, H=9.0, gc=None, cu=45.0, ha=1.5)
    d['Ka'] = Ka(d['phi'])
    d['pa'] = d['gs'] * d['H'] * d['Ka']
    d['pnet'] = 4 * d['cu'] - d['gs'] * d['H']
    d['Pa'] = 0.5 * d['pa'] * d['H']
    La = 2 / 3 * d['H'] - d['ha']
    # pnet·D·(H-ha+D/2) = Pa·La  →  (pnet/2)D² + pnet(H-ha)D - Pa La = 0
    a, b, c = d['pnet'] / 2, d['pnet'] * (d['H'] - d['ha']), -d['Pa'] * La
    d['D'] = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    d['T'] = d['Pa'] - d['pnet'] * d['D']
    d['La'] = La
    return d


def water_error(phi=30.0, gsat=19.0, z=6.0):
    """水壓與土壓分開 vs 錯把 γsat 乘 Ka"""
    gp = gsat - GW
    right = Ka(phi) * gp * z + GW * z
    wrong = Ka(phi) * gsat * z
    return dict(right=right, wrong=wrong, ratio=wrong / right, Ka=Ka(phi))


# ---------- 第 2 章 懸臂樁（2022-4） ----------
def ex2022_4():
    d = dict(g=16.5, gsat=19.3, phi=38.0, L1=3.0, L2=6.0)
    gp = d['gsat'] - GW
    d['gp'] = gp
    ka, kp = Ka(d['phi']), Kp(d['phi'])
    d['Ka'], d['Kp'] = ka, kp
    s2 = d['g'] * d['L1']
    s3 = s2 + gp * d['L2']
    d['pa2'], d['pa3'] = s2 * ka, s3 * ka
    k = gp * (kp - ka)
    d['k'] = k
    d['L3'] = d['pa3'] / k
    P1 = 0.5 * d['L1'] * d['pa2']; z1 = d['L2'] + d['L3'] + d['L1'] / 3
    P2a = d['pa2'] * d['L2']; z2a = d['L3'] + d['L2'] / 2
    P2b = 0.5 * d['L2'] * (d['pa3'] - d['pa2']); z2b = d['L3'] + d['L2'] / 3
    P3 = 0.5 * d['L3'] * d['pa3']; z3 = 2 / 3 * d['L3']
    P = P1 + P2a + P2b + P3
    M = P1 * z1 + P2a * z2a + P2b * z2b + P3 * z3
    d['P'], d['zbar'] = P, M / P
    s5 = s3 * kp + gp * d['L3'] * (kp - ka)     # σ5′（Das）
    A1 = s5 / k
    A2 = 8 * P / k
    A3 = 6 * P * (2 * d['zbar'] * k + s5) / k ** 2
    A4 = P * (6 * d['zbar'] * s5 + 4 * P) / k ** 2
    f = lambda x: x ** 4 + A1 * x ** 3 - A2 * x ** 2 - A3 * x - A4
    lo, hi = 0.1, 30
    for _ in range(200):
        m = (lo + hi) / 2
        if f(m) < 0:
            lo = m
        else:
            hi = m
    d['A'] = (A1, A2, A3, A4)
    d['L4'] = (lo + hi) / 2
    d['DL'] = d['L3'] + d['L4']
    # 簡化法：對樁尖取矩，淨被動三角形
    g = lambda x: k * x ** 3 / 6 - P * (d['zbar'] + x)
    lo, hi = 0.1, 30
    for _ in range(200):
        m = (lo + hi) / 2
        if g(m) < 0:
            lo = m
        else:
            hi = m
    d['L4s'] = (lo + hi) / 2
    d['Ds'] = d['L3'] + d['L4s']
    d['Ds12'] = 1.2 * d['Ds']
    return d


# ---------- 第 4 章 Peck ----------
def ex2015_3():
    d = dict(gs=16.5, Hs=3.0, gc=17.5, Hc=5.0, phis=32.0, cuc=30.0, Ks=1.0, B=6.0, L=15.0)
    H = d['Hs'] + d['Hc']
    d['H'] = H
    d['gbar'] = (d['gs'] * d['Hs'] + d['gc'] * d['Hc']) / H
    d['sv'] = d['gbar'] * H
    d['cus'] = 0.5 * d['gs'] * d['Hs'] * d['Ks'] * tan(d['phis'])
    d['cubar'] = (d['cus'] * d['Hs'] + d['cuc'] * d['Hc']) / H
    d['Ns'] = d['sv'] / d['cubar']
    d['pa1'] = d['sv'] - 4 * d['cubar']
    d['pa2'] = 0.3 * d['sv']
    d['pa'] = max(d['pa1'], d['pa2'])
    d['Ptri'] = 0.5 * 0.25 * H * d['pa']
    d['Prect'] = 0.75 * H * d['pa']
    d['P'] = d['Ptri'] + d['Prect']
    d['zbar'] = (d['Ptri'] * (2 / 3 * 0.25 * H) + d['Prect'] * (0.25 * H + 0.375 * H)) / d['P']
    d['P_wrong'] = 0.5 * H * d['pa'] * 0 + (0.5 * H * d['pa'] + 0.25 * H * d['pa'])  # 誤用硬黏土梯形：0.25H 漸增、0.5H 定值、0.25H 遞減
    d['P_wrong'] = 0.5 * 0.25 * H * d['pa'] * 2 + 0.5 * H * d['pa']
    d['Nc'] = 5 * (1 + 0.2 * d['B'] / d['L']) * (1 + 0.2 * H / d['B'])
    d['Nc_max'] = 7.5 * (1 + 0.2 * d['B'] / d['L'])
    d['FS'] = d['Nc'] * d['cuc'] / d['sv']
    d['FS_2D'] = 5.14 * d['cuc'] / d['sv']
    return d


def ex2011_4():
    d = dict(Gs=2.70, Sr=0.30, e=0.617, H=7.0, c=30.0, s=5.0, zA=1.0, zB=4.0, zC=6.0, sall=170000.0)
    d['g'] = (d['Gs'] + d['Sr'] * d['e']) / (1 + d['e']) * GW
    d['Ns'] = d['g'] * d['H'] / d['c']
    d['pa1'] = d['g'] * d['H'] - 4 * d['c']
    d['pa2'] = 0.3 * d['g'] * d['H']
    p = max(d['pa1'], d['pa2'])
    d['pa'] = p
    H = d['H']
    z1 = 0.25 * H
    F1 = 0.5 * z1 * p; F2 = (d['zB'] - z1) * p
    RA = (F1 * (d['zB'] - 2 / 3 * z1) + F2 * (d['zB'] - z1) / 2) / (d['zB'] - d['zA'])
    RB1 = F1 + F2 - RA
    RB2 = RC1 = p * (d['zC'] - d['zB']) / 2
    RC2 = p * (H - d['zC']) / 2
    d['RA'], d['RB1'], d['RB2'], d['RC2'] = RA, RB1, RB2, RC2
    d['PA'] = RA * d['s']
    d['PB'] = (RB1 + RB2) * d['s']
    d['PC'] = (RC1 + RC2) * d['s']
    zz = z1 + (RA - F1) / p
    d['z_V0'] = zz
    d['Mmax'] = RA * (zz - d['zA']) - (F1 * (zz - 2 / 3 * z1) + p * (zz - z1) ** 2 / 2)
    d['S'] = d['Mmax'] / d['sall'] * 1e6   # cm³/m
    return d


# ---------- 第 5 章 隆起 ----------
def ex2017_4_heave():
    d = dict(gH=14.392, q=1.0, l=4.5, Dw=6.0, Navg=None)
    d['Navg'] = (4 * 2.32 + 13.333 * 3.68) / 6.0
    d['Su'] = 10 * d['Navg'] / 16
    d['X'] = d['l'] + d['Dw']
    d['alpha'] = math.acos(d['l'] / d['X'])
    d['FS'] = d['Su'] * (math.pi + 2 * d['alpha']) / (d['gH'] + d['q'])
    return d


# ---------- 第 6 章 水 ----------
def ex2003_3():
    d = dict(hp=7.0, gc=17.5, Hc=10.0)
    d['u'] = d['hp'] * GW
    d['t'] = d['u'] / d['gc']
    d['D'] = d['Hc'] - d['t']
    d['D10'] = d['Hc'] - d['hp'] * 10 / d['gc']
    return d


def ex2017_4_water():
    d = dict(out=1.0, inn=8.0, tip=14.0, gt_CL=1.86, top_SM=10.32)
    d['L'] = (d['tip'] - d['out']) + (d['tip'] - d['inn'])
    d['dH'] = d['inn'] - d['out']
    d['i'] = d['dH'] / d['L']
    d['icr'] = d['gt_CL'] - 1.0
    d['FSp'] = d['icr'] / d['i']
    d['t'] = d['top_SM'] - d['inn']
    d['W'] = d['gt_CL'] * d['t']
    d['U'] = 1.0 * (d['top_SM'] - d['out'])
    d['FSu'] = d['W'] / d['U']
    d['h_req'] = d['W'] / 2.0
    d['GL_req'] = d['top_SM'] - d['h_req']
    return d


if __name__ == '__main__':
    def show(n, d):
        print('==', n)
        for k, v in d.items():
            if isinstance(v, float):
                print(f'  {k} = {v:.4f}')
            elif isinstance(v, tuple):
                print(f'  {k} = ' + ', '.join(f'{x:.3f}' for x in v))
            else:
                print(f'  {k} = {v}')
    show('2005-1', ex2005_1())
    show('water', water_error())
    show('2022-4', ex2022_4())
    show('2015-3', ex2015_3())
    show('2011-4', ex2011_4())
    show('2017-4 heave', ex2017_4_heave())
    show('2003-3', ex2003_3())
    show('2017-4 water', ex2017_4_water())
    print('π+2 =', math.pi + 2)


def practice():
    d = dict(g=18.0, cu=25.0, H=6.0, q=10.0, B=8.0, L=20.0, t=3.0, top_sand=9.0, gw_lvl=1.0)
    d['gH'] = d['g'] * d['H']
    d['Ns'] = d['gH'] / d['cu']
    d['pa'] = max(d['gH'] - 4 * d['cu'], 0.3 * d['gH'])
    d['FS2D'] = 5.14 * d['cu'] / (d['gH'] + d['q'])
    d['Nc'] = 5 * (1 + 0.2 * d['B'] / d['L']) * (1 + 0.2 * d['H'] / d['B'])
    d['FS3D'] = d['Nc'] * d['cu'] / (d['gH'] + d['q'])
    d['Su_req'] = 1.5 * (d['gH'] + d['q']) / d['Nc']
    d['qu_req'] = 2 * d['Su_req']
    hw = d['top_sand'] - d['gw_lvl']
    d['FSu'] = d['g'] * d['t'] / (GW * hw)
    d['hw_req'] = d['g'] * d['t'] / (GW * 1.5)
    d['GL_req'] = d['top_sand'] - d['hw_req']
    return d
