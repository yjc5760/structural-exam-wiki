# -*- coding: utf-8 -*-
"""RC-U4-1／U4-2 預力教科書（上下冊）：全部數值。單位 kgf、cm；力另列 tf、彎矩 tf·m。
執行 python3 calcs.py 印出全部數值，內文數字一律抄這裡的輸出。

符號約定（全書統一）：應力「壓為正、拉為負」；偏心 e「形心以下為正」；彎矩「使下緣受拉（正彎矩）為正」。
規範：建築物混凝土結構設計規範（112 年版）。kgf 制容許應力：傳遞 0.60f'ci、0.8√f'ci（簡支端部 0.70f'ci、1.6√f'ci）；
使用 0.45f'c（持續）／0.60f'c（全部）、U 類拉應力 ≤ 2.0√f'c、T 類 2.0～3.2√f'c。
"""
import math

SQ = math.sqrt


def tf(x):
    return x / 1000.0


def tfm(m):
    return m / 1e5


def stress(P, e, M, A, St, Sb):
    """回傳 (上緣, 下緣)，壓為正。M 為正彎矩（kgf·cm）。"""
    top = P / A - P * e / St + M / St
    bot = P / A + P * e / Sb - M / Sb
    return top, bot


def allow(fci=None, fc=None):
    d = {}
    if fci:
        d.update(ci=0.60 * fci, ci_end=0.70 * fci, ti=0.8 * SQ(fci), ti_end=1.6 * SQ(fci))
    if fc:
        d.update(cs=0.45 * fc, ct=0.60 * fc, tU=2.0 * SQ(fc), tT=3.2 * SQ(fc), fr=2.0 * SQ(fc))
    return d


# ------------------------------------------------------------ 示範梁 = RC-2014-4（對稱 I 形）
def demo():
    A, I, c = 1100.0, 469000.0, 30.0
    S = I / c
    r2 = I / A
    k = r2 / c
    e = 19.8
    Pi, Pe = 70000.0, 60000.0
    L = 1200.0
    wd, wl = 2.64, 11.0      # kgf/cm
    Md = wd * L ** 2 / 8
    MT = (wd + wl) * L ** 2 / 8
    t1 = stress(Pi, e, Md, A, S, S)
    t2 = stress(Pe, e, MT, A, S, S)
    ts = stress(Pe, e, Md, A, S, S)        # 持續（只有自重）
    al = allow(300, 420)
    yC1 = e - Md / Pi
    yC2 = e - MT / Pe
    fr = al['fr']
    Mdec = (Pe / A + Pe * e / S) * S        # 去壓彎矩（下緣應力歸零）
    Mcr = (Pe / A + Pe * e / S + fr) * S
    return dict(A=A, I=I, c=c, S=S, r2=r2, k=k, e=e, Pi=Pi, Pe=Pe, L=L, wd=wd, wl=wl, Md=Md, MT=MT,
                t1=t1, t2=t2, ts=ts, al=al, yC1=yC1, yC2=yC2, Mdec=Mdec, Mcr=Mcr,
                parts1=(Pi / A, Pi * e / S, Md / S), parts2=(Pe / A, Pe * e / S, MT / S))


def rc2011_5():
    Fi, F0, MG, MS, ML = 250000.0, 220000.0, 3e6, 1.5e6, 7e6
    n1 = dict(A=2500.0, Zt=40000.0, Zb=39000.0, e=25.0)
    n2 = dict(A=2800.0, Zt=41000.0, Zb=43000.0, I=1.9e6, e=24.0)
    n3 = dict(A=3900.0, Zt=137000.0, Zb=74000.0, I=4.3e6, e=39.0)
    t1 = stress(Fi, n1['e'], MG, n1['A'], n1['Zt'], n1['Zb'])
    a = stress(F0, n1['e'], MG, n1['A'], n1['Zt'], n1['Zb'])
    b = (MS / n2['Zt'], -MS / n2['Zb'])
    cc = (ML / n3['Zt'], -ML / n3['Zb'])
    top = a[0] + b[0] + cc[0]; bot = a[1] + b[1] + cc[1]
    dsig = MS * n2['e'] / n2['I'] + ML * n3['e'] / n3['I']
    fs1 = Fi / 24; fs0 = F0 / 24; fs2 = fs0 + 6 * dsig
    return dict(t1=t1, a=a, b=b, c=cc, top=top, bot=bot, fs1=fs1, fs0=fs0, dfs=6 * dsig, fs2=fs2)


def rc2012_1():
    b, h, L, e = 30.0, 90.0, 610.0, 30.0
    A = b * h; S = b * h * h / 6
    Pi = 0.75 * 19000 * 3 * 0.9871
    w = 2.3e-3 * b * h            # kgf/cm
    fci = 0.7 * 350
    al = allow(fci)
    Msw = w * L ** 2 / 2
    # 鋼鍵在形心上方 → e = -30（形心以下為正）；懸臂彎矩為負
    fix = stress(Pi, -e, -Msw, A, S, S)
    free = stress(Pi, -e, 0.0, A, S, S)
    xi = L * SQ((-free[1] - al['ti']) / (Msw / S))
    xi0 = L * SQ((-free[1]) / (Msw / S))
    return dict(A=A, S=S, Pi=Pi, w=w, Msw=Msw, fix=fix, free=free, al=al, xi=xi, xi0=xi0, fci=fci)


def rc2006_4():
    Pe = 210000.0
    A1, S1, e = 2400.0, 32000.0, 25.0
    w1 = 5.76 + 3.60
    M1 = w1 * 2000 ** 2 / 8
    s1 = stress(Pe, e, M1, A1, S1, S1)
    n = SQ(280 / 350)
    bt = 100 * n
    As = bt * 15
    yb = (A1 * 40 + As * 87.5) / (A1 + As)
    I1 = 30 * 80 ** 3 / 12
    Ic = I1 + A1 * (yb - 40) ** 2 + bt * 15 ** 3 / 12 + As * (87.5 - yb) ** 2
    Stop = Ic / (80 - yb); Sbot = Ic / yb
    ML = 5e6
    top = s1[0] + ML / Stop; bot = s1[1] - ML / Sbot
    return dict(s1=s1, M1=M1, n=n, bt=bt, yb=yb, Ic=Ic, Stop=Stop, Sbot=Sbot, dtop=ML / Stop, dbot=-ML / Sbot, top=top, bot=bot)


def rc2004_5():
    b, h, dp, Aps, fpu, fe, fc = 40.0, 90.0, 80.0, 6.16, 16500.0, 9900.0, 350.0
    b1 = 0.80
    A = b * h; S = b * h * h / 6; e = dp - h / 2
    Pe = Aps * fe
    fr = 2 * SQ(fc)
    fb = Pe / A + Pe * e / S
    Mcr = (fb + fr) * S
    rho = Aps / (b * dp)
    fps = fpu * (1 - 0.4 / b1 * rho * fpu / fc)
    a = Aps * fps / (0.85 * fc * b)
    Mn = Aps * fps * (dp - a / 2)
    c = a / b1
    et = 0.003 * (dp - c) / c
    wp = Aps * fps / (b * dp * fc)
    return dict(Pe=Pe, fb=fb, fr=fr, Mcr=Mcr, rho=rho, fps=fps, a=a, Mn=Mn, phiMn=0.9 * Mn, c=c, et=et, wp=wp, wlim=0.36 * b1,
                ratio=0.9 * Mn / Mcr, fe_ratio=fe / fpu)


def rc2023_4():
    b, dp, Ap, fse, fpu, fc = 20.0, 22.0, 1.47, 11000.0, 19000.0, 420.0
    rho = Ap / (b * dp)
    fps = fse + 700 + fc / (300 * rho)
    cap = min(0.85 * fpu, fse + 2100)
    As = 0.004 * b * 12.5
    T = Ap * fps + As * 4200
    a = T / (0.85 * fc * b)
    Mn = T * (dp - a / 2)
    c = a / 0.75
    return dict(rho=rho, fps=fps, cap=cap, As=As, T=T, a=a, Mn=Mn, Mn_m=Mn * 5, c=c, et=0.003 * (dp - c) / c)


def fps_unbonded(rho, fse=11000.0, fc=420.0, k=300):
    return fse + 700 + fc / (k * rho)


def rc2013_4():
    A, S, e, Fe, fc = 1800.0, 18000.0, 20.0, 65000.0, 350.0
    fb = Fe / A + Fe * e / S
    fr = 2 * SQ(fc)
    return dict(fb=fb, fr=fr, Mcr=(fb + fr) * S)


def rc2018_4():
    return dict(fse=100000 / 14, half=0.5 * 19000)


# ------------------------------------------------------------ 下冊
def window(b, h, L, Pi, eta, fci, fc, wL, gamma=2.4e-3, wG=None):
    A = b * h; S = b * h * h / 6
    Pe = eta * Pi
    wG = gamma * b * h if wG is None else wG
    MG = wG * L ** 2 / 8; ML = wL * L ** 2 / 8
    al = allow(fci, fc)
    # 四條件 → e 上下限（e 下為正）
    e1 = (Pi / A + MG / S + al['ti']) * S / Pi            # 傳遞頂拉 → 上限
    e2 = (al['ci'] - Pi / A + MG / S) * S / Pi            # 傳遞底壓 → 上限
    e3 = (Pe / A + (MG + ML) / S - al['ct']) * S / Pe     # 使用頂壓 → 下限
    e4 = ((MG + ML) / S - al['tU'] - Pe / A) * S / Pe     # 使用底拉 → 下限
    e4_0 = ((MG + ML) / S - Pe / A) * S / Pe              # 若拉應力取 0
    return dict(A=A, S=S, Pe=Pe, wG=wG, MG=MG, ML=ML, al=al, e1=e1, e2=e2, e3=e3, e4=e4, e4_0=e4_0,
                emax=min(e1, e2), emin=max(e3, e4), k=h / 6)


def rc2010_4():
    W = window(50, 90, 1500, 200000.0, 0.85, 280, 350, 15.0)
    # 直線鋼腱：梁端 M = 0，一般位置傳遞拉應力
    es = (W['Pi'] if 'Pi' in W else 200000.0)
    es = (200000.0 / W['A'] + W['al']['ti']) * W['S'] / 200000.0
    ec = W['emax']
    dM = W['Pe'] * (ec - es)
    # 使用階段可承受 ML（底拉控制）
    def MLcap(e):
        return (W['Pe'] / W['A'] + W['Pe'] * e / W['S'] + W['al']['tU']) * W['S'] - W['MG']
    return dict(W=W, es=es, ec=ec, dM=dM, MLc=MLcap(ec), MLs=MLcap(es), etaMG=0.85 * W['MG'])


def rc2025_4():
    return window(40, 120, 1200, 200000.0, 0.85, 320, 420, 15.0)


def rc2015_4():
    b, h, L, fca, fta = 30.0, 50.0, 1200.0, 140.0, 0.0
    A = b * h; S = b * h * h / 6
    wD = 2.4e-3 * A
    MD = wD * L ** 2 / 8
    ML = (fca + fta) * S
    F = (fca - fta) * A / 2
    e = (fca - F / A + MD / S) * S / F
    return dict(A=A, S=S, wD=wD, MD=MD, ML=ML, F=F, e=e, wL=8 * ML / L ** 2)


def rc2020_4():
    L = 1500.0; w = 16.0   # kgf/cm
    MB = -w * L ** 2 / 8; MD = w * L ** 2 / 16
    Pe = -MB / 35.0
    eD = MD / Pe
    f = eD - (0 + (-35)) / 2
    q = 8 * Pe * f / L ** 2
    Pi = Pe / 0.8
    qi = Pi / Pe * w
    MBt = MB + qi * L ** 2 / 8
    A, Z = 4500.0, 67500.0
    top = Pi / A + MBt / Z; bot = Pi / A - MBt / Z
    return dict(MB=MB, MD=MD, Pe=Pe, eD=eD, f=f, q=q, Pi=Pi, qi=qi, MBt=MBt, top=top, bot=bot)


def rc2024_4():
    L, P = 12.0, 120.0           # m, tf
    c = -25.0
    # 36a + 6b = 40 ; 144a + 12b = 25
    a = (25 - 2 * 40) / 72.0
    bb = (40 - 36 * a) / 6
    e = lambda x: a * x * x + bb * x + c      # cm
    w = -P * 2 * a / 100                      # tf/m（正 = 向上）
    VA = P * bb / 100                          # A 端錨碇向下分力
    VB = P * abs(2 * a * L + bb) / 100
    MA = P * abs(c) / 100
    integ = 1728 * a + 288 * bb + 72 * c       # cm·m²
    RB = 3 * P / L ** 3 * integ / 100
    M2 = lambda x: RB * (L - x)
    eC = lambda x: e(x) - M2(x) / P * 100
    xv = -bb / (2 * a)
    em = (600.0) / 48.0
    return dict(a=a, b=bb, c=c, e=e, w=w, VA=VA, VB=VB, MA=MA, integ=integ, RB=RB, M2=M2, eC=eC, xv=xv, emax=e(xv), em=em,
                MA2=RB * L)


def mu_delta_dummy():
    return None


if __name__ == '__main__':
    D = demo()
    print('== 示範梁 RC-2014-4')
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in D.items() if k not in ('al', 't1', 't2', 'ts', 'parts1', 'parts2')})
    print('al', {k: round(v, 2) for k, v in D['al'].items()})
    print('t1', [round(x, 2) for x in D['t1']], 'parts1', [round(x, 2) for x in D['parts1']])
    print('t2', [round(x, 2) for x in D['t2']], 'parts2', [round(x, 2) for x in D['parts2']])
    print('ts', [round(x, 2) for x in D['ts']])
    print('Mdec tf·m', round(tfm(D['Mdec']), 2), 'Mcr', round(tfm(D['Mcr']), 2), 'Md', tfm(D['Md']), 'MT', tfm(D['MT']))
    R = rc2011_5(); print('== 2011-5', {k: (tuple(round(x, 2) for x in v) if isinstance(v, tuple) else round(v, 2)) for k, v in R.items()})
    R = rc2012_1(); print('== 2012-1', {k: (tuple(round(x, 2) for x in v) if isinstance(v, tuple) else (round(v, 2) if isinstance(v, float) else v)) for k, v in R.items() if k != 'al'}, {k: round(v, 2) for k, v in R['al'].items()})
    R = rc2006_4(); print('== 2006-4', {k: (tuple(round(x, 2) for x in v) if isinstance(v, tuple) else round(v, 3)) for k, v in R.items()})
    R = rc2004_5(); print('== 2004-5', {k: round(v, 5) for k, v in R.items()})
    R = rc2023_4(); print('== 2023-4', {k: round(v, 4) for k, v in R.items()})
    print('== 2013-4', {k: round(v, 2) for k, v in rc2013_4().items()}, '2018-4', rc2018_4())
    R = rc2010_4(); W = R['W']
    print('== 2010-4', {k: round(v, 3) for k, v in W.items() if isinstance(v, float)}, {k: round(v, 2) for k, v in W['al'].items()})
    print('   es', round(R['es'], 2), 'ec', round(R['ec'], 2), 'dM', round(tfm(R['dM']), 2), 'MLc', round(tfm(R['MLc']), 2), 'MLs', round(tfm(R['MLs']), 2), 'etaMG', round(tfm(R['etaMG']), 2))
    W = rc2025_4(); print('== 2025-4', {k: round(v, 3) for k, v in W.items() if isinstance(v, float)}, {k: round(v, 2) for k, v in W['al'].items()})
    print('== 2015-4', {k: round(v, 3) for k, v in rc2015_4().items()})
    print('== 2020-4', {k: round(v, 3) for k, v in rc2020_4().items()})
    R = rc2024_4(); print('== 2024-4', {k: round(v, 4) for k, v in R.items() if isinstance(v, float)})
    for x in (0, 3, 6, 9, 12):
        print('   x', x, 'e', round(R['e'](x), 2), 'M2', round(R['M2'](x), 2), 'eC', round(R['eC'](x), 2))
