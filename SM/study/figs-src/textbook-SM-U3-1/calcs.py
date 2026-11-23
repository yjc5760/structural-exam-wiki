# -*- coding: utf-8 -*-
"""SM-U3-1 側向土壓力理論 教科書講義的所有數值。單位：kN、m、kPa；γw = 9.81 kN/m³。
考題數字取自 raw/solutions/（2026-11-15 後版本）。
"""
import math

GW = 9.81
r = math.radians
sin = lambda a: math.sin(r(a))
cos = lambda a: math.cos(r(a))
tan = lambda a: math.tan(r(a))


def Ka(phi):
    return tan(45 - phi / 2) ** 2


def Kp(phi):
    return tan(45 + phi / 2) ** 2


def K0(phi, OCR=1.0):
    return (1 - sin(phi)) * math.sqrt(OCR)


def Ka_incl(alpha, phi):
    ca, cp = cos(alpha), cos(phi)
    s = math.sqrt(ca ** 2 - cp ** 2)
    return ca * (ca - s) / (ca + s)


def Ka_coulomb(phi, beta, delta, alpha):
    num = sin(beta + phi) ** 2
    rt = math.sqrt(sin(phi + delta) * sin(phi - alpha) / (sin(beta - delta) * sin(alpha + beta)))
    return num / (sin(beta) ** 2 * sin(beta - delta) * (1 + rt) ** 2)


def Kae_MO(phi, beta, delta, alpha, kh, kv):
    th = math.degrees(math.atan(kh / (1 - kv)))
    num = sin(phi + beta - th) ** 2
    rt = math.sqrt(sin(phi + delta) * sin(phi - th - alpha) / (sin(beta - delta - th) * sin(alpha + beta)))
    return num / (cos(th) * sin(beta) ** 2 * sin(beta - delta - th) * (1 + rt) ** 2), th


# ---------- 第 2 章：莫爾圓示例（σv = 100, φ = 30, c = 0） ----------
def mohr_demo(sv=100.0, phi=30.0, c=0.0):
    return dict(sv=sv, sa=sv * Ka(phi) - 2 * c * math.sqrt(Ka(phi)), sp=sv * Kp(phi) + 2 * c * math.sqrt(Kp(phi)), s0=sv * K0(phi))


# ---------- 第 2 章：Coulomb 試驗楔（c = 0、牆背鉛直光滑、水平填土）＝ Rankine 驗證 ----------
def trial_wedge(rho, gamma=18.0, H=6.0, phi=30.0):
    """破壞面與水平夾 ρ：P = W tan(ρ − φ)，W = ½γH² cot ρ"""
    W = 0.5 * gamma * H ** 2 / tan(rho)
    return W * tan(rho - phi)


def trial_wedge_max(gamma=18.0, H=6.0, phi=30.0):
    best = max(((trial_wedge(rh / 100, gamma, H, phi), rh / 100) for rh in range(int(phi * 100) + 1, 8999)))
    return best   # (Pmax, ρ)


# ---------- SM-2004-3 水位上升到多高會滑 ----------
def ex2004_3():
    d = dict(H=6.0, g=19.2, phi=35.0, R=146.0)
    d['Ka'] = Ka(d['phi'])
    d['P0'] = 0.5 * d['Ka'] * d['g'] * d['H'] ** 2
    d['a'] = 0.5 * GW * (1 - d['Ka'])          # 每 x² 淨增
    d['x'] = math.sqrt((d['R'] - d['P0']) / d['a'])
    return d


def P_of_x(x, d=None):
    d = d or ex2004_3()
    return d['P0'] + d['a'] * x ** 2


# ---------- SM-2010-2 兩層土、水位在中間 ----------
def ex2010_2():
    d = dict(g1=17.0, g1s=18.0, g2=17.5, phi1=30.0, c2=30.0)
    k = Ka(d['phi1'])
    d['Ka1'] = k
    d['s2'] = 17 * 2 * k
    sv4 = 34 + (18 - GW) * 2
    d['s4a'] = sv4 * k
    d['u4'] = GW * 2
    d['s4top_total'] = d['s4a'] + d['u4']
    d['s4b'] = 70 - 2 * d['c2']
    d['s8'] = 140 - 2 * d['c2']
    blocks = [
        ('*P*_{1}', 0.5 * 2 * d['s2'], 6 + 2 / 3),
        ('*P*_{2}', 2 * d['s2'], 5.0),
        ('*P*_{3}', 0.5 * 2 * (d['s4a'] - d['s2']), 4 + 2 / 3),
        ('*P*_{4}（水）', 0.5 * 2 * d['u4'], 4 + 2 / 3),
        ('*P*_{5}', 4 * d['s4b'], 2.0),
        ('*P*_{6}', 0.5 * 4 * (d['s8'] - d['s4b']), 4 / 3),
    ]
    d['blocks'] = blocks
    d['P'] = sum(b[1] for b in blocks)
    d['M'] = sum(b[1] * b[2] for b in blocks)
    d['ybar'] = d['M'] / d['P']
    return d


# ---------- SM-2015-2 黏土（c、φ）上、砂下、水位在交界 ----------
def ex2015_2():
    d = dict(c1=20.0, phi1=20.0, g1=17.5, phi2=30.0, g2sat=18.5)
    k1, k2 = Ka(d['phi1']), Ka(d['phi2'])
    d['Ka1'], d['Ka2'] = k1, k2
    d['s0'] = -2 * d['c1'] * math.sqrt(k1)
    d['zc'] = 2 * d['c1'] / (d['g1'] * math.sqrt(k1))
    d['s4a'] = 70 * k1 - 2 * d['c1'] * math.sqrt(k1)
    d['s4b'] = 70 * k2
    gp = d['g2sat'] - GW
    d['s8'] = (70 + gp * 4) * k2
    d['u8'] = GW * 4
    blocks = [
        ('*P*_{1}', 0.5 * d['s4a'] * (4 - d['zc']), 4 + (4 - d['zc']) / 3),
        ('*P*_{2}', d['s4b'] * 4, 2.0),
        ('*P*_{3}', 0.5 * (d['s8'] - d['s4b']) * 4, 4 / 3),
        ('*P*_{w}', 0.5 * d['u8'] * 4, 4 / 3),
    ]
    d['blocks'] = blocks
    d['P'] = sum(b[1] for b in blocks)
    d['M'] = sum(b[1] * b[2] for b in blocks)
    d['ybar'] = d['M'] / d['P']
    d['FR'] = 133.48          # 題解 (二) 抗滑抵抗力（底部摩擦＋被動＋前趾水壓），直接引用
    d['FS'] = d['FR'] / d['P']
    d['Pw_crack'] = 0.5 * GW * d['zc'] ** 2
    d['FS_crack'] = d['FR'] / (d['P'] + d['Pw_crack'])
    d['P_neg_wrong'] = d['P'] + 0.5 * d['s0'] * d['zc']   # 負壓抵銷（錯）
    return d


# ---------- SM-2016-4 Coulomb＋M–O ----------
def ex2016_4():
    d = dict(phi=30.0, delta=15.0, alpha=0.0, g=18.0, H=8.0, kh=0.15, kv=0.05)
    d['beta'] = math.degrees(math.atan(8.0 / 2.0))
    d['Ka'] = Ka_coulomb(d['phi'], d['beta'], d['delta'], d['alpha'])
    d['Pa'] = 0.5 * d['g'] * d['H'] ** 2 * d['Ka']
    d['ang'] = (90 - d['beta']) + d['delta']
    d['Pah'] = d['Pa'] * cos(d['ang'])
    d['Pav'] = d['Pa'] * sin(d['ang'])
    d['Kae'], d['th'] = Kae_MO(d['phi'], d['beta'], d['delta'], d['alpha'], d['kh'], d['kv'])
    d['Pae'] = 0.5 * d['g'] * d['H'] ** 2 * (1 - d['kv']) * d['Kae']
    d['dP'] = d['Pae'] - d['Pa']
    d['zbar'] = (d['Pa'] * d['H'] / 3 + d['dP'] * 0.6 * d['H']) / d['Pae']
    d['Ka_rankine'] = Ka(d['phi'])
    return d


# ---------- 傾斜填土示例（2009-4 情境：α = 20°、φ = 30°） ----------
def ex_incl(alpha=20.0, phi=30.0):
    return dict(alpha=alpha, phi=phi, Ka=Ka_incl(alpha, phi), Ka0=Ka(phi))


# ---------- 第 6 章綜合練習（自編） ----------
def practice():
    d = dict(H=7.0, q=10.0, g=18.0, gsat=19.81, phi=30.0, zw=3.0)
    k = Ka(d['phi'])
    gp = d['gsat'] - GW
    d['Ka'] = k
    d['sq'] = d['q'] * k
    d['s3'] = d['g'] * 3 * k
    d['s7'] = (d['g'] * 3 + gp * 4) * k
    d['u7'] = GW * 4
    blocks = [
        ('超載', d['sq'] * 7, 3.5),
        ('土 0～3', 0.5 * d['s3'] * 3, 4 + 1),
        ('土 3～7 矩形', d['s3'] * 4, 2.0),
        ('土 3～7 三角', 0.5 * (d['s7'] - d['s3']) * 4, 4 / 3),
        ('水', 0.5 * d['u7'] * 4, 4 / 3),
    ]
    d['blocks'] = blocks
    d['P'] = sum(b[1] for b in blocks)
    d['ybar'] = sum(b[1] * b[2] for b in blocks) / d['P']
    return d


if __name__ == '__main__':
    print('Ka/Kp 30:', round(Ka(30), 4), round(Kp(30), 4), 'Ka35', round(Ka(35), 4), 'K0 30', round(K0(30), 3), 'K0 OCR4', round(K0(30, 4), 3))
    print('mohr', {k: round(v, 2) for k, v in mohr_demo().items()})
    print('trial wedge max', [round(x, 3) for x in trial_wedge_max()], 'Rankine', round(0.5 * 18 * 36 * Ka(30), 3))
    for nm, fn in [('2004-3', ex2004_3), ('2016-4', ex2016_4), ('incl', ex_incl)]:
        print('=====', nm, {k: round(v, 4) for k, v in fn().items()})
    for nm, fn in [('2010-2', ex2010_2), ('2015-2', ex2015_2), ('practice', practice)]:
        d = fn()
        print('=====', nm)
        for k, v in d.items():
            if k == 'blocks':
                for b in v:
                    print('   ', b[0], round(b[1], 3), round(b[2], 3), round(b[1] * b[2], 2))
            else:
                print(f'  {k} = {v:.4f}')
