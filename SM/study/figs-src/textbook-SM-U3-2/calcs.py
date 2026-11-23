# -*- coding: utf-8 -*-
"""SM-U3-2 擋土結構物穩定分析｜教科書講義的所有數值。單位 kN、m、kPa、度；γw＝9.81。

考題數字取自 raw/solutions（勘誤後版本）：
  2016-4（貫穿範例：Coulomb → 傾倒、滑動 → 偏心、qmax、承載力 → M-O）、2018-4（懸臂式、虛擬牆背）、
  2009-4（B/3 反求底寬）、2025-3（φ=0 底土）、2004-3（水位上升）、2016-3（加勁土體＋超載＋承載力）、2015-2（張力裂縫）
"""
import math

GW = 9.81
rad, deg = math.radians, math.degrees
sin = lambda a: math.sin(rad(a))
cos = lambda a: math.cos(rad(a))
tan = lambda a: math.tan(rad(a))


def Ka_r(phi):
    return tan(45 - phi / 2) ** 2


def Ka_incl(alpha, phi):
    ca, cp = cos(alpha), cos(phi)
    r = math.sqrt(ca * ca - cp * cp)
    return ca * (ca - r) / (ca + r)


def Ka_coulomb(phi, beta, delta, alpha):
    num = sin(beta + phi) ** 2
    root = math.sqrt(sin(phi + delta) * sin(phi - alpha) / (sin(beta - delta) * sin(alpha + beta)))
    return num / (sin(beta) ** 2 * sin(beta - delta) * (1 + root) ** 2)


def Kae_mo(phi, beta, delta, alpha, th):
    num = sin(phi + beta - th) ** 2
    root = math.sqrt(sin(phi + delta) * sin(phi - alpha - th) / (sin(beta - delta - th) * sin(alpha + beta)))
    return num / (cos(th) * sin(beta) ** 2 * sin(beta - delta - th) * (1 + root) ** 2)


def ex2016_4():
    d = dict(H=8.0, Btop=3.0, B=5.0, g=18.0, gc=23.5, phi=30.0, deltaB=15.0, ca=15.0, deltaF=18.0, c=20.0,
             Nc=30.14, Ng=22.4, Kh=0.15, Kv=0.05)
    d['beta'] = deg(math.atan(d['H'] / (d['B'] - d['Btop'])))
    d['Ka'] = Ka_coulomb(d['phi'], d['beta'], d['deltaB'], 0.0)
    d['Pa'] = 0.5 * d['g'] * d['H'] ** 2 * d['Ka']
    d['ang'] = (90 - d['beta']) + d['deltaB']
    d['Pah'] = d['Pa'] * cos(d['ang'])
    d['Pav'] = d['Pa'] * sin(d['ang'])
    d['xpa'] = d['B'] - (d['H'] / 3) / d['H'] * (d['B'] - d['Btop'])
    d['W1'] = d['Btop'] * d['H'] * d['gc']; d['x1'] = d['Btop'] / 2
    d['W2'] = 0.5 * (d['B'] - d['Btop']) * d['H'] * d['gc']; d['x2'] = d['Btop'] + (d['B'] - d['Btop']) / 3
    d['V'] = d['W1'] + d['W2'] + d['Pav']
    d['MR'] = d['W1'] * d['x1'] + d['W2'] * d['x2'] + d['Pav'] * d['xpa']
    d['MO'] = d['Pah'] * d['H'] / 3
    d['FS_OT'] = d['MR'] / d['MO']
    d['FS_OT_alt'] = (d['W1'] * d['x1'] + d['W2'] * d['x2']) / (d['MO'] - d['Pav'] * d['xpa'])
    d['FR'] = d['ca'] * d['B'] + d['V'] * tan(d['deltaF'])
    d['FS_SL'] = d['FR'] / d['Pah']
    d['xbar'] = (d['MR'] - d['MO']) / d['V']
    d['e'] = d['B'] / 2 - d['xbar']
    d['qmax'] = d['V'] / d['B'] * (1 + 6 * d['e'] / d['B'])
    d['qmin'] = d['V'] / d['B'] * (1 - 6 * d['e'] / d['B'])
    d['Bp'] = d['B'] - 2 * d['e']
    d['qp'] = d['V'] / d['Bp']
    d['psi'] = deg(math.atan(d['Pah'] / d['V']))
    d['Fci'] = (1 - d['psi'] / 90) ** 2
    d['Fgi'] = (1 - d['psi'] / d['phi']) ** 2
    d['qu'] = d['c'] * d['Nc'] * d['Fci'] + 0.5 * d['g'] * d['Bp'] * d['Ng'] * d['Fgi']
    d['FS_BC'] = d['qu'] / d['qp']
    d['qu_noincl'] = d['c'] * d['Nc'] + 0.5 * d['g'] * d['Bp'] * d['Ng']
    d['th'] = deg(math.atan(d['Kh'] / (1 - d['Kv'])))
    d['Kae'] = Kae_mo(d['phi'], d['beta'], d['deltaB'], 0.0, d['th'])
    d['Pae'] = 0.5 * d['g'] * d['H'] ** 2 * (1 - d['Kv']) * d['Kae']
    d['dPae'] = d['Pae'] - d['Pa']
    d['zbar'] = (d['Pa'] * d['H'] / 3 + d['dPae'] * 0.6 * d['H']) / d['Pae']
    return d


def ex2018_4():
    d = dict(H=7.5, t=0.96, heel=3.5, toe=1.5, stem=0.6, alpha=12.0, phi=32.0, g=17.8, gc=23.55, phi2=28.0, c2=30.0)
    d['B'] = d['toe'] + d['stem'] + d['heel']
    d['Hp'] = d['H'] + d['t'] + d['heel'] * tan(d['alpha'])
    d['Ka'] = Ka_incl(d['alpha'], d['phi'])
    d['Pa'] = 0.5 * d['g'] * d['Hp'] ** 2 * d['Ka']
    d['Pah'] = d['Pa'] * cos(d['alpha']); d['Pav'] = d['Pa'] * sin(d['alpha'])
    W = [(0.4 * 7.5 * d['gc'], 1.9), (0.5 * 0.2 * 7.5 * d['gc'], 1.5 + 0.2 * 2 / 3), (d['B'] * d['t'] * d['gc'], d['B'] / 2),
         (d['heel'] * 7.5 * d['g'], 2.1 + d['heel'] / 2), (0.5 * d['heel'] * d['heel'] * tan(d['alpha']) * d['g'], 2.1 + d['heel'] * 2 / 3),
         (1.5 * 0.79 * d['g'], 0.75), (d['Pav'], d['B'])]
    d['V'] = sum(w for w, x in W)
    d['MR'] = sum(w * x for w, x in W)
    d['MO'] = d['Pah'] * d['Hp'] / 3
    d['FS_OT'] = d['MR'] / d['MO']
    d['delta'] = 2 / 3 * d['phi2']; d['ca'] = 2 / 3 * d['c2']
    d['FS_SL'] = (d['ca'] * d['B'] + d['V'] * tan(d['delta'])) / d['Pah']
    d['Ka_wrong'] = Ka_r(d['phi'])
    return d


def ex2009_4():
    d = dict(H=6.0, g=18.0, gc=24.0, alpha=20.0, phi=30.0, top=0.6)
    d['Ka'] = Ka_incl(d['alpha'], d['phi'])
    d['Pa'] = 0.5 * d['Ka'] * d['g'] * d['H'] ** 2
    d['Pah'] = d['Pa'] * cos(d['alpha']); d['Pav'] = d['Pa'] * sin(d['alpha'])
    # 72B² + 135B − 782.58 = 0 （由題解整理；此處重算）
    W1 = d['top'] * d['H'] * d['gc']
    def resid(B):
        W2 = 0.5 * (B - d['top']) * d['H'] * d['gc']
        V = W1 + W2 + d['Pav']
        MR = W1 * (B - d['top'] / 2) + W2 * 2 / 3 * (B - d['top']) + d['Pav'] * B
        MO = d['Pah'] * d['H'] / 3
        return (MR - MO) / V - B / 3
    lo, hi = 1.0, 6.0
    for _ in range(100):
        m = (lo + hi) / 2
        if resid(m) < 0:
            lo = m
        else:
            hi = m
    d['B'] = (lo + hi) / 2
    return d


def ex2025_3():
    d = dict(H=7.0, B=6.0, g=17.0, phi=30.0, Su=30.0)
    d['Ka'] = Ka_r(d['phi'])
    d['Pa'] = 0.5 * d['Ka'] * d['g'] * d['H'] ** 2
    d['R'] = d['Su'] * d['B']
    d['FS'] = d['R'] / d['Pa']
    return d


def ex2004_3():
    d = dict(H=6.0, phi=35.0, g=19.2, R=146.0)
    d['Ka'] = Ka_r(d['phi'])
    a = 0.5 * d['Ka'] * d['g'] * d['H'] ** 2
    b = 0.5 * GW - 0.5 * d['Ka'] * GW
    d['P0'] = a
    d['x'] = math.sqrt((d['R'] - a) / b)
    d['coef'] = b
    return d


def ex2016_3():
    d = dict(H=6.0, L=4.5, gb=18.0, gm=20.0, qs=60.0, phi=32.0, ca=12.0, delta=15.0)
    d['Ka'] = Ka_r(d['phi'])
    d['Pa1'] = 0.5 * d['Ka'] * d['gb'] * d['H'] ** 2
    d['Pa2'] = d['Ka'] * d['qs'] * d['H']
    d['Ph'] = d['Pa1'] + d['Pa2']
    d['MO'] = d['Pa1'] * d['H'] / 3 + d['Pa2'] * d['H'] / 2
    d['V'] = d['gm'] * d['H'] * d['L'] + d['qs'] * d['L']
    d['MR'] = d['V'] * d['L'] / 2
    d['FS_OT'] = d['MR'] / d['MO']
    d['FS_SL'] = (d['ca'] * d['L'] + d['V'] * tan(d['delta'])) / d['Ph']
    d['e'] = d['L'] / 2 - (d['MR'] - d['MO']) / d['V']
    d['Lp'] = d['L'] - 2 * d['e']
    d['qp'] = d['V'] / d['Lp']
    d['th'] = deg(math.atan(d['Ph'] / d['V']))
    d['FS_BC'] = 2.98
    return d


def ex2015_2():
    d = dict(c=20.0, phi1=20.0, g1=17.5, phi2=30.0, gsat2=18.5)
    d['Ka1'] = Ka_r(d['phi1']); d['Ka2'] = Ka_r(d['phi2'])
    d['zc'] = 2 * d['c'] / (d['g1'] * math.sqrt(d['Ka1']))
    d['s4c'] = d['g1'] * 4 * d['Ka1'] - 2 * d['c'] * math.sqrt(d['Ka1'])
    d['s4s'] = d['g1'] * 4 * d['Ka2']
    d['s8s'] = (d['g1'] * 4 + (d['gsat2'] - GW) * 4) * d['Ka2']
    d['u8'] = GW * 4
    P1 = 0.5 * d['s4c'] * (4 - d['zc']); P2 = d['s4s'] * 4; P3 = 0.5 * (d['s8s'] - d['s4s']) * 4; P4 = 0.5 * d['u8'] * 4
    d['P'] = P1 + P2 + P3 + P4
    d['Pw'] = P4
    d['ybar'] = (P1 * (4 + (4 - d['zc']) / 3) + P2 * 2 + P3 * 4 / 3 + P4 * 4 / 3) / d['P']
    return d


if __name__ == '__main__':
    def show(n, d):
        print('==', n)
        for k, v in d.items():
            print(f'  {k} = {v:.4f}' if isinstance(v, float) else f'  {k} = {v}')
    show('2016-4', ex2016_4())
    show('2018-4', ex2018_4())
    show('2009-4', ex2009_4())
    show('2025-3', ex2025_3())
    show('2004-3', ex2004_3())
    show('2016-3', ex2016_3())
    show('2015-2', ex2015_2())
    print('Ka(30)=', Ka_r(30), ' Ka_incl(0,30)=', Ka_incl(0.0001, 30), ' Coulomb(β=90,δ=0,α=0)=', Ka_coulomb(30, 90, 0, 0))


def coulomb_trial(rho, H=8.0, dx=2.0, g=18.0, phi=30.0, delta=15.0, kh=0.0, kv=0.0):
    """試誤楔：牆背由 A(0,0) 到 (−dx, H)，地表水平；滑動面由 A 以 rho 角往上。回傳 (P, W, R, 幾何)。"""
    xc = H / math.tan(rad(rho))
    area = 0.5 * abs((-dx) * H - H * xc)   # A,(−dx,H),(xc,H)
    W = g * area
    Lw = math.hypot(dx, H)
    nw = (H / Lw, dx / Lw); tw = (-dx / Lw, H / Lw)
    pd = (cos(delta) * nw[0] + sin(delta) * tw[0], cos(delta) * nw[1] + sin(delta) * tw[1])
    ns = (-sin(rho), cos(rho)); s = (cos(rho), sin(rho))
    rd = (cos(phi) * ns[0] + sin(phi) * s[0], cos(phi) * ns[1] + sin(phi) * s[1])
    Fx, Fy = kh * W, -(1 - kv) * W          # 慣性力指向牆（−x），故外力 = −kh W；此處平衡式寫 P+R+G=0，G=(−khW, −(1−kv)W)
    Gx, Gy = -kh * W, -(1 - kv) * W
    det = pd[0] * rd[1] - pd[1] * rd[0]
    P = (-Gx * rd[1] + Gy * rd[0]) / det
    R = (-Gy * pd[0] + Gx * pd[1]) / det
    return P, W, R, dict(xc=xc, pd=pd, rd=rd)


def coulomb_scan(**kw):
    best = (0, 0)
    rows = []
    for i in range(300, 800):
        rho = i * 0.1
        P = coulomb_trial(rho, **kw)[0]
        rows.append((rho, P))
        if P > best[1]:
            best = (rho, P)
    return best, rows


def practice():
    d = dict(H=5.0, B=3.0, gc=24.0, g=18.0, phi=30.0, q=10.0, delta=20.0)
    d['Ka'] = Ka_r(d['phi'])
    d['P1'] = 0.5 * d['Ka'] * d['g'] * d['H'] ** 2
    d['P2'] = d['Ka'] * d['q'] * d['H']
    d['Ph'] = d['P1'] + d['P2']
    d['MO'] = d['P1'] * d['H'] / 3 + d['P2'] * d['H'] / 2
    d['W'] = d['B'] * d['H'] * d['gc']
    d['MR'] = d['W'] * d['B'] / 2
    d['FS_SL'] = d['W'] * tan(d['delta']) / d['Ph']
    d['FS_OT'] = d['MR'] / d['MO']
    d['xbar'] = (d['MR'] - d['MO']) / d['W']
    d['e'] = d['B'] / 2 - d['xbar']
    d['qmax'] = d['W'] / d['B'] * (1 + 6 * d['e'] / d['B'])
    d['qmin'] = d['W'] / d['B'] * (1 - 6 * d['e'] / d['B'])
    d['Bp'] = d['B'] - 2 * d['e']
    d['psi'] = deg(math.atan(d['Ph'] / d['W']))
    return d
