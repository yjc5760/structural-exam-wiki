# -*- coding: utf-8 -*-
"""SM-U1-1 土壤基本性質 教科書講義的所有數值。γw = 9.81 kN/m³（ρw = 1 g/cm³）。
考題數字取自 raw/solutions/（2026-11-15 後版本；SM-2008-1 已含 Gs 可行性檢核）。
"""
import math

GW = 9.81


def unit_phase(e, S, Gs):
    """令 Vs = 1：回傳六格（體積以 Vs 為單位、重量以 γw 為單位）。"""
    return dict(Vs=1.0, Vv=e, Vw=S * e, Va=e - S * e, V=1 + e, Ws=Gs, Ww=S * e, w=S * e / Gs, n=e / (1 + e))


def gamma(Gs, e, S):
    return (Gs + S * e) / (1 + e) * GW


def zav(w, Gs):
    return Gs * GW / (1 + w * Gs)


def gd_S(w, Gs, S):
    """固定 S 的乾單位重線：γd = Gsγw/(1 + wGs/S)"""
    return Gs * GW / (1 + w * Gs / S)


# ---------- SM-2004-1 夯實試體（第 2 章貫穿） ----------
def ex2004_1():
    d = dict(w=0.18, Gs=2.70, V=944.0, M=1955.0, S2=0.95)
    d['rho_t'] = d['M'] / d['V']
    d['rho_d'] = d['rho_t'] / (1 + d['w'])
    d['gt'] = d['rho_t'] * GW
    d['gd'] = d['rho_d'] * GW
    d['e'] = d['Gs'] / d['rho_d'] - 1
    d['S'] = d['w'] * d['Gs'] / d['e']
    d['e2'] = d['w'] * d['Gs'] / d['S2']
    d['gd2'] = d['Gs'] * GW / (1 + d['e2'])
    d['gt2'] = d['gd2'] * (1 + d['w'])
    d['gsat'] = gamma(d['Gs'], d['e'], 1.0)
    d['gp'] = d['gsat'] - GW
    d['gzav'] = zav(d['w'], d['Gs'])
    d['n'] = d['e'] / (1 + d['e'])
    return d


# ---------- SM-2007-1 壓密盒（第 3 章） ----------
def ex2007_1():
    d = dict(e0=1.30, Gs=2.72, H0=2.5, H1=1.9)
    d['g0'] = gamma(d['Gs'], d['e0'], 1.0)
    d['de'] = (d['H0'] - d['H1']) / d['H0'] * (1 + d['e0'])
    d['e1'] = d['e0'] - d['de']
    d['g1'] = gamma(d['Gs'], d['e1'], 1.0)
    d['w0'] = d['e0'] / d['Gs']
    d['w1'] = d['e1'] / d['Gs']
    d['dw'] = d['w0'] - d['w1']
    d['Hs'] = d['H0'] / (1 + d['e0'])
    d['de_wrong'] = (d['H0'] - d['H1']) / d['H0'] * d['e0']
    return d


# ---------- SM-2016-2 疏濬土方（第 4 章貫穿） ----------
def ex2016_2():
    d = dict(Wt_lab=1720.0, Ws_lab=1620.0, V_lab=1000.0, e_lab=0.70, Vhole=0.25, Whole=450.0,
             gdmax=19.50, Vfill=10000.0, omc=0.08)
    d['w'] = (d['Wt_lab'] - d['Ws_lab']) / d['Ws_lab']
    d['rho_d_lab'] = d['Ws_lab'] / d['V_lab']
    d['Gs'] = d['rho_d_lab'] * (1 + d['e_lab'])
    d['gt'] = d['Whole'] / d['Vhole'] * GW / 1000
    d['gd'] = d['gt'] / (1 + d['w'])
    d['Ws'] = d['gdmax'] * d['Vfill']
    d['Vborrow'] = d['Ws'] / d['gd']
    d['dWw'] = d['Ws'] * (d['omc'] - d['w'])
    d['Vw'] = d['dWw'] / GW
    d['e_borrow'] = d['Gs'] * GW / d['gd'] - 1
    d['e_fill'] = d['Gs'] * GW / d['gdmax'] - 1
    d['Vborrow_wrong'] = d['Vfill'] * d['gdmax'] / d['gt']    # 用濕單位重（錯）
    return d


# ---------- SM-2008-1 甲乙借土混合＋Gs 可行性檢核（第 4 章） ----------
def ex2008_1():
    d = dict(gtA=19.6, wA=0.09, gtB=20.6, wB=0.11, GsA=2.65, GsB=2.70, gd=20.0, w=0.12, ratio=4.0)
    d['gdA'] = d['gtA'] / (1 + d['wA'])
    d['gdB'] = d['gtB'] / (1 + d['wB'])
    d['Ws'] = d['gd'] * 1.0
    d['Ww'] = d['Ws'] * d['w']
    d['VB'] = d['Ws'] / (d['ratio'] * d['gdA'] + d['gdB'])
    d['VA'] = d['ratio'] * d['VB']
    d['WtA'] = d['gtA'] * d['VA']
    d['WtB'] = d['gtB'] * d['VB']
    d['WsA'] = d['gdA'] * d['VA']
    d['WsB'] = d['gdB'] * d['VB']
    d['dWw'] = d['Ww'] - d['WsA'] * d['wA'] - d['WsB'] * d['wB']
    d['Vs'] = d['WsA'] / (d['GsA'] * GW) + d['WsB'] / (d['GsB'] * GW)
    d['Vw'] = d['Ww'] / GW
    d['Gs_mix'] = d['Ws'] / (d['Vs'] * GW)
    d['e'] = 1.0 / d['Vs'] - 1
    d['S'] = d['Vw'] / (1.0 - d['Vs'])
    d['zav_mix'] = zav(d['w'], d['Gs_mix'])
    d['zav_B'] = zav(d['w'], d['GsB'])
    return d


# ---------- SM-2005-2 過大顆粒修正（第 4 章） ----------
def ex2005_2():
    coarse = [('1/2"', 18.0, 0.023, 2.41), ('3/8"', 26.0, 0.041, 2.32), ('#4', 40.0, 0.072, 2.35)]
    d = dict(V=315.0, Wf=650.0, wf=0.112)
    rows = []
    for nm, W, w, G in coarse:
        Ws = W / (1 + w)
        rows.append((nm, W, w, G, Ws, Ws / G))
    d['rows'] = rows
    d['Vc'] = sum(r[5] for r in rows)
    d['Vf'] = d['V'] - d['Vc']
    d['Wsf'] = d['Wf'] / (1 + d['wf'])
    d['rho_df'] = d['Wsf'] / d['Vf']
    d['rho_d_all'] = (d['Wsf'] + sum(r[4] for r in rows)) / d['V']
    d['rho_wrong'] = d['Wsf'] / d['V']       # 沒扣粗料體積
    return d


# ---------- SM-2020-3 相對密度（第 5 章） ----------
def ex2020_3():
    d = dict(V=500.0, W=900.0, Ws=850.0, S=0.27, Vmax=640.0, Vmin=440.0)
    d['Dr_V'] = (d['Vmax'] - d['V']) / (d['Vmax'] - d['Vmin'])
    d['Vw'] = d['W'] - d['Ws']
    d['Vv'] = d['Vw'] / d['S']
    d['Vs'] = d['V'] - d['Vv']
    d['Gs'] = d['Ws'] / d['Vs']
    d['e'] = d['Vv'] / d['Vs']
    d['emax'] = (d['Vmax'] - d['Vs']) / d['Vs']
    d['emin'] = (d['Vmin'] - d['Vs']) / d['Vs']
    d['Dr_e'] = (d['emax'] - d['e']) / (d['emax'] - d['emin'])
    d['gd'] = d['Ws'] / d['V'] * GW
    d['gdmin'] = d['Ws'] / d['Vmax'] * GW
    d['gdmax'] = d['Ws'] / d['Vmin'] * GW
    d['Dr_g'] = d['gdmax'] * (d['gd'] - d['gdmin']) / (d['gd'] * (d['gdmax'] - d['gdmin']))
    d['Dr_lin_wrong'] = (d['gd'] - d['gdmin']) / (d['gdmax'] - d['gdmin'])
    return d


# ---------- SM-2019-3（副）：Dr = 50% 夯到 R.C. = 95%（第 5 章） ----------
def ex2019_3():
    d = dict(emax=0.95, emin=0.55, Dr=0.50, Gs=2.65, RC=0.95, H0=2.0)
    d['e0'] = d['emax'] - d['Dr'] * (d['emax'] - d['emin'])
    d['gd0'] = d['Gs'] * GW / (1 + d['e0'])
    d['gdmax'] = d['Gs'] * GW / (1 + d['emin'])
    d['gdf'] = d['RC'] * d['gdmax']
    d['ef'] = d['Gs'] * GW / d['gdf'] - 1
    d['Drf'] = (d['emax'] - d['ef']) / (d['emax'] - d['emin'])
    d['dH'] = d['H0'] * (d['e0'] - d['ef']) / (1 + d['e0'])
    return d


# ---------- SM-2023-4（副）：液性指數（第 6 章） ----------
def ex2023_4():
    d = dict(w=41.0, PL=12.0, PI=20.0)
    d['LL'] = d['PL'] + d['PI']
    d['LI'] = (d['w'] - d['PL']) / d['PI']
    return d


# ---------- 第 6 章示意級配曲線（自訂，非考題） ----------
GRAD = [(0.075, 2), (0.15, 8), (0.3, 22), (0.6, 40), (1.18, 55), (2.36, 70), (4.75, 85), (9.5, 96), (19, 100)]


def grad_D(p):
    """在對數粒徑上線性內插，找通過百分比 p 的粒徑。"""
    for (d1, p1), (d2, p2) in zip(GRAD, GRAD[1:]):
        if p1 <= p <= p2:
            t = (p - p1) / (p2 - p1)
            return 10 ** (math.log10(d1) + t * (math.log10(d2) - math.log10(d1)))
    return None


def grad_coef():
    D10, D30, D60 = grad_D(10), grad_D(30), grad_D(60)
    return dict(D10=D10, D30=D30, D60=D60, Cu=D60 / D10, Cc=D30 ** 2 / (D10 * D60))


def aline(LL):
    return 0.73 * (LL - 20)


# ---------- 第 7 章綜合練習（自編） ----------
def practice():
    d = dict(V=0.5, Wt=9.5, Wd=8.2, Gs=2.68)          # m³、kN
    d['w'] = (d['Wt'] - d['Wd']) / d['Wd']
    d['gt'] = d['Wt'] / d['V']
    d['gd'] = d['Wd'] / d['V']
    d['e'] = d['Gs'] * GW / d['gd'] - 1
    d['S'] = d['w'] * d['Gs'] / d['e']
    d['n'] = d['e'] / (1 + d['e'])
    d['gsat'] = gamma(d['Gs'], d['e'], 1.0)
    d['gp'] = d['gsat'] - GW
    # 夯到 γd = 17.8、w = 17%，填 1000 m³
    d['gd2'], d['w2'], d['Vf'] = 17.8, 0.17, 1000.0
    d['Ws'] = d['gd2'] * d['Vf']
    d['Vb'] = d['Ws'] / d['gd']
    d['Vwater'] = d['Ws'] * (d['w2'] - d['w']) / GW
    d['S2'] = d['w2'] * d['Gs'] / (d['Gs'] * GW / d['gd2'] - 1)
    return d


if __name__ == '__main__':
    for nm, fn in [('2004-1', ex2004_1), ('2007-1', ex2007_1), ('2016-2', ex2016_2), ('2008-1', ex2008_1),
                   ('2020-3', ex2020_3), ('2019-3', ex2019_3), ('2023-4', ex2023_4), ('practice', practice)]:
        print('=====', nm)
        for k, v in fn().items():
            print(f'  {k} = {v:.5f}' if isinstance(v, float) else f'  {k} = {v}')
    d = ex2005_2()
    print('===== 2005-2')
    for r in d['rows']:
        print('  ', r[0], round(r[4], 3), round(r[5], 3))
    for k in ('Vc', 'Vf', 'Wsf', 'rho_df', 'rho_d_all', 'rho_wrong'):
        print(f'  {k} = {d[k]:.4f}')
    print('grad', {k: round(v, 4) for k, v in grad_coef().items()})
    print('aline(50)', aline(50))
