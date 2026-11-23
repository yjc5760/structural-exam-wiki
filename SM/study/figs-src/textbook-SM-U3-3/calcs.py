# -*- coding: utf-8 -*-
"""SM-U3-3 坡地工程 教科書講義的所有數值。單位：kN、m、kPa；γw = 9.81 kN/m³。
考題數字取自 raw/solutions/（2026-11-15 後版本；SM-2021-4 採勘誤後量測表，FS = 0.98）。
"""
import math

GW = 9.81
r = math.radians
sin = lambda a: math.sin(r(a))
cos = lambda a: math.cos(r(a))
tan = lambda a: math.tan(r(a))


# ---------- SM-2024-2 無限邊坡乾／浸水、自由水層 i ----------
def ex2024_2():
    d = dict(beta=42.0, phi=35.0, theta=30.0)
    d['FS'] = tan(d['phi']) / tan(d['beta'])
    d['i'] = sin(d['theta'])
    d['i_wrong'] = tan(d['theta'])
    d['beta_crit'] = d['phi']
    return d


# ---------- 無限邊坡通式：滲流對 FS 的影響（第 3 章示意，c'=0） ----------
def seepage_ratio(gsat=20.0):
    return (gsat - GW) / gsat


# ---------- SM-2014-1 崩積土＋平行滲流（第 3 章貫穿） ----------
def ex2014_1():
    d = dict(H=6.0, H1=1.5, beta=15.0, w1=0.24, w2=0.35, Gs=2.64, c=15.0, phi=20.0)
    d['H2'] = d['H'] - d['H1']
    d['e'] = d['w2'] * d['Gs']
    d['gt'] = d['Gs'] * (1 + d['w1']) / (1 + d['e']) * GW
    d['gsat'] = d['Gs'] * (1 + d['w2']) / (1 + d['e']) * GW
    d['sv'] = d['gt'] * d['H1'] + d['gsat'] * d['H2']
    c2 = cos(d['beta']) ** 2
    d['u'] = GW * d['H2'] * c2
    d['sn'] = d['sv'] * c2 - d['u']
    d['tau'] = d['sv'] * sin(d['beta']) * cos(d['beta'])
    d['tf'] = d['c'] + d['sn'] * tan(d['phi'])
    d['FS'] = d['tf'] / d['tau']
    # 錯解：u = γw hw（不乘 cos²）
    snw = d['sv'] * c2 - GW * d['H2']
    d['FS_wrong_u'] = (d['c'] + snw * tan(d['phi'])) / d['tau']
    # 對照：無水（同單位重 γt 全段，u=0）
    d['FS_dry'] = (d['c'] + d['sv'] * c2 * tan(d['phi'])) / d['tau']
    return d


# ---------- SM-2023-2 楔形平面滑動 ----------
def ex2023_2():
    d = dict(H=8.0, alpha=60.0, theta=45.0, g=20.0, phi=36.0, c1=50.0, c2=5.0)
    d['L'] = d['H'] / sin(d['theta'])
    d['b'] = d['H'] / tan(d['theta']) - d['H'] / tan(d['alpha'])
    d['A'] = 0.5 * d['b'] * d['H']
    d['W'] = d['A'] * d['g']
    d['T'] = d['W'] * sin(d['theta'])
    d['N'] = d['W'] * cos(d['theta'])
    d['FS1'] = (d['c1'] * d['L'] + d['N'] * tan(d['phi'])) / d['T']
    d['FS2'] = (d['c2'] * d['L'] + d['N'] * tan(d['phi'])) / d['T']
    d['share_c1'] = d['c1'] * d['L'] / (d['c1'] * d['L'] + d['N'] * tan(d['phi']))
    return d


# ---------- SM-2008-4 岩坡平面滑動＋地震＋地錨 ----------
def ex2008_4():
    d = dict(H=7.5, a=40.0, A=30.0, Cang=35.0, g=20.0, c=10.0, phi=28.0, kh=0.2, FSreq=1.2, s=2.0)
    d['Bang'] = 180 - d['A'] - d['Cang']
    d['LAB'] = d['H'] / sin(d['a'] + d['A'])
    d['LAC'] = d['LAB'] * sin(d['Bang']) / sin(d['Cang'])
    d['Area'] = 0.5 * d['LAB'] * d['LAC'] * sin(d['A'])
    d['W'] = d['g'] * d['Area']
    d['Fh'] = d['kh'] * d['W']
    d['T0'] = d['W'] * sin(d['a'])
    d['N0'] = d['W'] * cos(d['a'])
    d['FS0'] = (d['c'] * d['LAC'] + d['N0'] * tan(d['phi'])) / d['T0']
    d['Td'] = d['W'] * sin(d['a']) + d['Fh'] * cos(d['a'])
    d['N'] = d['W'] * cos(d['a']) - d['Fh'] * sin(d['a'])
    d['Tr'] = d['c'] * d['LAC'] + d['N'] * tan(d['phi'])
    d['FS'] = d['Tr'] / d['Td']
    d['FS_halfwrong'] = (d['c'] * d['LAC'] + d['N0'] * tan(d['phi'])) / d['Td']   # 只加在分母
    d['P'] = (d['FSreq'] * d['Td'] - d['Tr']) / tan(d['phi'])
    d['Tanchor'] = d['P'] * d['s']
    return d


# ---------- SM-2006-3 軟弱夾層滑動塊體法 ----------
def ex2006_3():
    d = dict(H1=12.0, H2=2.0, g=20.0, c=10.0, phi=30.0, su=12.0, Lb=20.0)
    d['Ka'] = tan(45 - d['phi'] / 2) ** 2
    d['Kp'] = tan(45 + d['phi'] / 2) ** 2
    sKa, sKp = math.sqrt(d['Ka']), math.sqrt(d['Kp'])
    def case(gam, water):
        o = {}
        o['zc'] = 2 * d['c'] / (gam * sKa)
        sa = d['Ka'] * gam * d['H1'] - 2 * d['c'] * sKa
        o['sa_bot'] = sa
        o['PA'] = 0.5 * sa * (d['H1'] - o['zc'])
        o['pp_top'] = 2 * d['c'] * sKp
        o['pp_bot'] = d['Kp'] * gam * d['H2'] + 2 * d['c'] * sKp
        o['PP'] = 0.5 * (o['pp_top'] + o['pp_bot']) * d['H2']
        o['PwA'] = 0.5 * GW * d['H1'] ** 2 if water else 0.0
        o['PwP'] = 0.5 * GW * d['H2'] ** 2 if water else 0.0
        o['T'] = d['su'] * d['Lb']
        o['FS'] = (o['T'] + o['PP'] + o['PwP']) / (o['PA'] + o['PwA'])
        o['drive'] = o['PA'] + o['PwA']
        return o
    d['dry'] = case(d['g'], False)
    d['wet'] = case(d['g'] - GW, True)
    d['water_share'] = d['wet']['PwA'] / d['wet']['drive']
    return d


# ---------- SM-2021-4 普通切片法（勘誤後量測表） ----------
SLICES = [  # (W, α, ΔL, u)
    (555.9, 60, 10.90, 0.0),
    (846.4, 42, 6.74, 17.5),
    (765.6, 30, 5.73, 40.7),
    (578.6, 13, 5.26, 50.8),
    (227.7, 0, 5.25, 21.8),
]
SLICE_B = [5.45, 5.01, 4.96, 5.13, 5.25]


def ex2021_4(c=10.0, phi=36.0):
    rows = []
    for (W, a, dL, u) in SLICES:
        Wc = W * cos(a)
        uL = u * dL
        Np = Wc - uL
        rows.append(dict(W=W, a=a, dL=dL, u=u, Wc=Wc, uL=uL, Np=Np, cL=c * dL, Nt=Np * tan(phi), Ws=W * sin(a)))
    S = lambda k: sum(rw[k] for rw in rows)
    FS = (S('cL') + S('Nt')) / S('Ws')
    return dict(rows=rows, ScL=S('cL'), SNt=S('Nt'), SWs=S('Ws'), FS=FS)


def bishop(c=10.0, phi=36.0, it=30):
    """Bishop 簡化法（同一量測表，b 取切片寬）——示範迭代，不是考題答案。"""
    FS = 1.0
    hist = []
    for _ in range(it):
        num = 0
        for (W, a, dL, u), b in zip(SLICES, SLICE_B):
            ma = cos(a) * (1 + tan(a) * tan(phi) / FS)
            num += (c * b + (W - u * b) * tan(phi)) / ma
        den = sum(W * sin(a) for (W, a, dL, u) in SLICES)
        FS_new = num / den
        hist.append(FS_new)
        if abs(FS_new - FS) < 1e-5:
            FS = FS_new
            break
        FS = FS_new
    return FS, hist


# ---------- 第 2 章示意：c'-φ' 乾坡 FS 隨深度 z（自訂參數，非考題） ----------
DEMO = dict(c=10.0, g=18.0, beta=30.0, phi=25.0)


def cphi_FS(z, c=DEMO['c'], g=DEMO['g'], beta=DEMO['beta'], phi=DEMO['phi']):
    return c / (g * z * sin(beta) * cos(beta)) + tan(phi) / tan(beta)


def z_crit(c=DEMO['c'], g=DEMO['g'], beta=DEMO['beta'], phi=DEMO['phi']):
    """FS = 1 的深度"""
    return c / (g * sin(beta) * cos(beta) * (1 - tan(phi) / tan(beta)))


# ---------- 第 7 章綜合重建練習（自編） ----------
def practice():
    d = dict(beta=20.0, z=4.0, c=8.0, phi=30.0, gsat=19.81, gdry=18.0)
    gp = d['gsat'] - GW
    sc = sin(d['beta']) * cos(d['beta'])
    d['FS_seep'] = d['c'] / (d['gsat'] * d['z'] * sc) + gp / d['gsat'] * tan(d['phi']) / tan(d['beta'])
    d['FS_sub'] = d['c'] / (gp * d['z'] * sc) + tan(d['phi']) / tan(d['beta'])
    d['FS_dry'] = d['c'] / (d['gdry'] * d['z'] * sc) + tan(d['phi']) / tan(d['beta'])
    d['u'] = GW * d['z'] * cos(d['beta']) ** 2
    d['tau'] = d['gsat'] * d['z'] * sc
    d['sn'] = d['gsat'] * d['z'] * cos(d['beta']) ** 2 - d['u']
    return d


if __name__ == '__main__':
    for nm, fn in [('2024-2', ex2024_2), ('2014-1', ex2014_1), ('2023-2', ex2023_2), ('2008-4', ex2008_4)]:
        print('=====', nm)
        for k, v in fn().items():
            print(f'  {k} = {v:.4f}' if isinstance(v, float) else f'  {k} = {v}')
    d = ex2006_3()
    print('===== 2006-3 Ka Kp', round(d['Ka'], 4), round(d['Kp'], 4))
    for k in ('dry', 'wet'):
        print(k, {a: round(b, 3) for a, b in d[k].items()})
    print('water share', round(d['water_share'], 4))
    d = ex2021_4()
    print('===== 2021-4')
    for rw in d['rows']:
        print({k: round(v, 1) for k, v in rw.items()})
    print('ScL', round(d['ScL'], 1), 'SNt', round(d['SNt'], 1), 'SWs', round(d['SWs'], 1), 'FS', round(d['FS'], 4))
    fs, h = bishop()
    print('Bishop', round(fs, 4), [round(x, 4) for x in h[:6]])
    print('demo z_crit', round(z_crit(), 3), 'FS(1m)', round(cphi_FS(1), 3), 'tan/tan', round(tan(25)/tan(30), 4))
    print('practice', {k: round(v, 4) for k, v in practice().items()})
    print('seepage ratio γ\'/γsat (20)', round(seepage_ratio(), 4))
