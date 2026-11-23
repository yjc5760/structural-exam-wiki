# -*- coding: utf-8 -*-
"""SM-U1-5 土壤強度特性與變形性｜教科書講義的所有數值。單位 kPa（kN/m²）、度。

考題數字取自 raw/solutions（勘誤後版本）：
  2018-2（貫穿範例：NC 黏土 CU）、2024-1（CD、c≠0、破壞面應力）、2025-2（CU→CD 預測）、
  2003-4、2010-1（由 φ′ 推 Su）、2012-1（反求現地應力）、2008-2（Skempton 求破壞水位）、2013-3（AC／LE 應力路徑）
"""
import math

GW = 9.81
rad, deg = math.radians, math.degrees
sin = lambda a: math.sin(rad(a))
cos = lambda a: math.cos(rad(a))
tan = lambda a: math.tan(rad(a))


def Np(phi):
    return tan(45 + phi / 2) ** 2


def s1_fail(s3, phi, c=0.0):
    """主應力式：σ1 = σ3 tan²(45+φ/2) + 2c tan(45+φ/2)"""
    return s3 * Np(phi) + 2 * c * math.sqrt(Np(phi))


def phi_from_circle(s1, s3):
    return deg(math.asin((s1 - s3) / (s1 + s3)))


def ex2018_2():
    d = dict(s3=100.0, dsd=85.0, uf=67.0, s3b=250.0)
    d['s1'] = d['s3'] + d['dsd']
    d['phi_cu'] = phi_from_circle(d['s1'], d['s3'])
    d['s3e'] = d['s3'] - d['uf']
    d['s1e'] = d['s1'] - d['uf']
    d['phi_e'] = phi_from_circle(d['s1e'], d['s3e'])
    d['dsd_b'] = d['s3b'] * d['dsd'] / d['s3']
    d['s1b'] = d['s3b'] + d['dsd_b']
    d['theta'] = 45 + d['phi_e'] / 2
    d['theta_wrong'] = 45 + d['phi_cu'] / 2
    d['Af'] = d['uf'] / d['dsd']
    d['Su'] = d['dsd'] / 2
    return d


def ex2024_1():
    d = dict(c=25.0, s3=100.0, dsd=240.0, s3b=200.0)
    d['s1'] = d['s3'] + d['dsd']
    # 解 φ：s1 = s3 Np + 2c √Np
    lo, hi = 1.0, 60.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if s1_fail(d['s3'], mid, d['c']) < d['s1']:
            lo = mid
        else:
            hi = mid
    d['phi'] = (lo + hi) / 2
    d['C'] = (d['s1'] + d['s3']) / 2
    d['R'] = (d['s1'] - d['s3']) / 2
    d['sff'] = d['C'] - d['R'] * sin(d['phi'])
    d['tff'] = d['R'] * cos(d['phi'])
    d['tff_check'] = d['c'] + d['sff'] * tan(d['phi'])
    d['theta'] = 45 + d['phi'] / 2
    d['Kp'] = Np(d['phi'])
    d['s1b'] = s1_fail(d['s3b'], d['phi'], d['c'])
    d['dsd_b'] = d['s1b'] - d['s3b']
    d['dsd_b_wrong'] = d['dsd'] * d['s3b'] / d['s3']   # 誤用比例（c≠0 不成立）
    return d


def ex2025_2():
    d = dict(s3_1=75.0, ds_1=40.0, u_1=35.0, s3_2=150.0, ds_2=70.0, u_2=70.0, s3_3=200.0)
    d['s3e1'] = d['s3_1'] - d['u_1']; d['s1e1'] = d['s3_1'] + d['ds_1'] - d['u_1']
    d['s3e2'] = d['s3_2'] - d['u_2']; d['s1e2'] = d['s3_2'] + d['ds_2'] - d['u_2']
    d['N'] = (d['s1e2'] - d['s1e1']) / (d['s3e2'] - d['s3e1'])
    d['K'] = d['s1e1'] - d['s3e1'] * d['N']      # 2c′√N
    d['phi'] = 2 * (deg(math.atan(math.sqrt(d['N']))) - 45)
    d['c'] = d['K'] / (2 * math.sqrt(d['N']))
    d['s1_3'] = d['s3_3'] * d['N'] + d['K']
    d['ds_3'] = d['s1_3'] - d['s3_3']
    d['ds_3_c0'] = d['s3_3'] * (Np(phi_from_circle(d['s1e1'], d['s3e1'])) - 1)   # 錯：令 c′=0 只用試體一
    return d


def su_from_phi(sv0, phi, Af=1.0):
    s = sin(phi)
    return sv0 * s / (1 + (2 * Af - 1) * s)


def ex2003_4():
    d = dict(phi=30.0, Su=30.76)
    d['sv0'] = d['Su'] * (1 + sin(d['phi'])) / sin(d['phi'])
    d['Su_calc'] = su_from_phi(d['sv0'], d['phi'])
    d['Su_A05'] = su_from_phi(d['sv0'], d['phi'], 0.5)
    d['Su_A0'] = su_from_phi(d['sv0'], d['phi'], 0.0)
    d['Su_mesri'] = 0.22 * d['sv0']
    d['ratio'] = d['Su'] / d['sv0']
    return d


def ex2010_1():
    d = dict(phi=28.0, Su=35.75, s3=50.0)
    d['sv0'] = d['Su'] * (1 + sin(d['phi'])) / sin(d['phi'])
    d['s3f_e'] = d['sv0'] - 2 * d['Su']
    return d


def ex2012_1():
    d = dict(phi_cu=22.0, Su=50.0)
    d['sc'] = d['Su'] / sin(d['phi_cu']) - d['Su']
    return d


def ex2008_2():
    d = dict(Gs=2.66, e=0.7, S=0.5, gc=19.0, K0=0.5, Af=0.7, phi=30.0)
    d['gsand'] = (d['Gs'] + d['S'] * d['e']) / (1 + d['e']) * GW
    d['sv0'] = d['gsand'] * 2 + d['gc'] * 3.5 - GW * 3.5
    d['sh0'] = d['K0'] * d['sv0']
    # Δσv = 2/3 Δq, Δσh = 1/3 Δq, Δu = 1/3Δq + Af·1/3Δq
    a1 = 2 / 3 - (1 + d['Af']) / 3     # σ1f′ = sv0 + a1 Δq
    a3 = 1 / 3 - (1 + d['Af']) / 3     # σ3f′ = sh0 + a3 Δq
    N = Np(d['phi'])
    d['dq'] = (N * d['sh0'] - d['sv0']) / (a1 - N * a3)
    d['H'] = d['dq'] / GW
    d['a1'], d['a3'] = a1, a3
    return d


def ex2013_3():
    d = dict(K0=0.7, sv=400.0, sh=280.0, dq_f=275.0, uAC=125.0, uLE=-30.0)
    d['p0'] = (d['sv'] + d['sh']) / 2; d['q0'] = (d['sv'] - d['sh']) / 2
    d['pAC'] = (555 + 280) / 2; d['qf'] = 275 / 2
    d['pLE'] = (400 + 125) / 2
    d['pE'] = d['pAC'] - d['uAC']
    d['Af'] = d['uAC'] / 155
    d['phi_e'] = phi_from_circle(430, 155)
    d['phi_AC'] = phi_from_circle(555, 280)
    d['phi_LE'] = phi_from_circle(400, 125)
    d['theta'] = 45 + d['phi_e'] / 2
    d['alpha'] = deg(math.atan(sin(d['phi_e'])))
    return d


def vane(T, d, h):
    return T / (math.pi * (d * d * h / 2 + d ** 3 / 6))


def jaky(phi):
    return 1 - sin(phi)


if __name__ == '__main__':
    def show(n, d):
        print('==', n)
        for k, v in d.items():
            print(f'  {k} = {v:.4f}' if isinstance(v, float) else f'  {k} = {v}')
    show('2018-2', ex2018_2())
    show('2024-1', ex2024_1())
    show('2025-2', ex2025_2())
    show('2003-4', ex2003_4())
    show('2010-1', ex2010_1())
    show('2012-1', ex2012_1())
    show('2008-2', ex2008_2())
    show('2013-3', ex2013_3())
    print('Np(30)=', Np(30), ' Jaky K0(30)=', jaky(30), ' Su/σ (φ′=30, Af=1)=', su_from_phi(1, 30))
    print('vane T=50 N·m, d=0.065, h=0.13 → Su(kPa)=', vane(50, 0.065, 0.13) / 1000)


def practice():
    d = dict(s3=150.0, dsd=120.0, uf=80.0, sv0=90.0, s3cd=200.0)
    d['s1'] = d['s3'] + d['dsd']
    d['phi_cu'] = phi_from_circle(d['s1'], d['s3'])
    d['s3e'] = d['s3'] - d['uf']; d['s1e'] = d['s1'] - d['uf']
    d['phi_e'] = phi_from_circle(d['s1e'], d['s3e'])
    d['theta'] = 45 + d['phi_e'] / 2
    d['Af'] = d['uf'] / d['dsd']
    d['Su_field'] = su_from_phi(d['sv0'], d['phi_e'], d['Af'])
    d['ds_cd'] = d['s3cd'] * (Np(d['phi_e']) - 1)
    d['ff_s'] = (d['s1e'] + d['s3e']) / 2 - d['dsd'] / 2 * sin(d['phi_e'])
    d['ff_t'] = d['dsd'] / 2 * cos(d['phi_e'])
    return d
