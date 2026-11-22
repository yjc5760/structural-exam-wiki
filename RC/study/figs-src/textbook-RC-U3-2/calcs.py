# -*- coding: utf-8 -*-
"""RC-U3-2 教科書講義（樓版與基腳）：全部數值（圖與內文共用）。單位 kgf、cm；力另列 tf、彎矩 tf·m。
執行 python3 calcs.py 印出全部數值，內文的數字一律抄這裡的輸出。

規範：建築物混凝土結構設計規範（112 年版，土木 401-112；ACI 318-19 世代），kgf/cm² 制。
  單向剪力（無剪力筋 Av < Av,min）：Vc = 2.12 λs λ ρw^(1/3) √f'c bw d ≤ 1.33√f'c bw d
  雙向剪力：Vc = λs √f'c bo d · min{1.06, 0.53(1+2/β), 0.265(2+αs d/bo)}；λs = √(2/(1+0.04d)) ≤ 1（d 以 cm 計）
  13.2.6.2：一向淺基礎、獨立基腳、聯合基腳、筏基可取 λs = 1；樓版、樁帽不可。
  有剪力筋（閉合箍）：vc = 0.53 λs √f'c；Vn ≤ 1.59√f'c bo d；Vs = Av fyt d / s
例題數據取自勘誤後題解（raw/solutions/RC-YYYY-N/RC-YYYY-N.md）。
"""
import math

PHI_V, PHI_M = 0.75, 0.90


def sq(fc):
    return math.sqrt(fc)


def lam_s(d):
    return min(1.0, math.sqrt(2 / (1 + 0.04 * d)))


def punch_coefs(beta, alpha_s, d, bo):
    k1 = 1.06
    k2 = 0.53 * (1 + 2 / beta)
    k3 = 0.265 * (2 + alpha_s * d / bo)
    return k1, k2, k3


def flex(As, fy, fc, b, d):
    a = As * fy / (0.85 * fc * b)
    c = a / 0.85 if fc <= 280 else a / max(0.65, 0.85 - 0.05 * (fc - 280) / 70)
    et = 0.003 * (d - c) / c
    Mn = As * fy * (d - a / 2)
    return a, c, et, Mn


def as_req(Mu, fy, fc, b, d, phi=0.9):
    """解 Mu = φ As fy (d − As fy /(1.7 fc b))。"""
    A = phi * fy ** 2 / (1.7 * fc * b)
    B = -phi * fy * d
    C = Mu
    return (-B - math.sqrt(B * B - 4 * A * C)) / (2 * A)


# ── 貫穿全書的範例：RC-2025-1 獨立基腳 ───────────────────────
def footing(B=300.0, c=40.0, d=50.0, h=60.0, PD=80.0, PL=75.0, qa=25.0, fc=280.0, fy=4200.0, As=50.0,
            gc=2.4, gs=2.0, Df=150.0):
    F = dict(B=B, c=c, d=d, h=h, PD=PD, PL=PL, qa=qa, fc=fc, fy=fy, As=As)
    A = (B / 100) ** 2
    F['A'] = A
    F['Wf'] = A * h / 100 * gc
    F['Ws'] = A * (Df - h) / 100 * gs
    F['q_serv'] = (PD + PL + F['Wf'] + F['Ws']) / A
    F['q_net_allow'] = qa - (h / 100 * gc + (Df - h) / 100 * gs)
    F['Pu'] = 1.2 * PD + 1.6 * PL
    F['qu'] = F['Pu'] / A                       # tf/m²
    F['qu_wrong'] = (F['Pu'] + 1.2 * (F['Wf'] + F['Ws'])) / A
    L = (B - c) / 2
    F['L'] = L
    F['Mu'] = F['qu'] * (B / 100) * (L / 100) ** 2 / 2        # tf·m
    a, cc, et, Mn = flex(As, fy, fc, B, d)
    F.update(a=a, cna=cc, et=et, Mn=Mn / 1e5, phiMn=PHI_M * Mn / 1e5)
    F['Asmin'] = 0.0018 * B * h
    F['smax'] = min(3 * h, 45.0)
    # 單向剪力
    F['Vu1'] = F['qu'] * (B / 100) * ((L - d) / 100)
    F['rho'] = As / (B * d)
    F['rho13'] = F['rho'] ** (1 / 3)
    F['Vc1'] = 2.12 * F['rho13'] * sq(fc) * B * d / 1000
    F['phiVc1'] = PHI_V * F['Vc1']
    F['phiVc1_old'] = PHI_V * 0.53 * sq(fc) * B * d / 1000
    F['Vc1_cap'] = 1.33 * sq(fc) * B * d / 1000
    # 穿孔
    F['bo'] = 4 * (c + d)
    F['Vu2'] = F['Pu'] - F['qu'] * ((c + d) / 100) ** 2
    k = punch_coefs(1.0, 40, d, F['bo'])
    F['k'] = k
    F['kmin'] = min(k)
    F['sqbod'] = sq(fc) * F['bo'] * d
    F['Vc2_each'] = [ki * F['sqbod'] / 1000 for ki in k]
    F['phiVc2'] = PHI_V * F['kmin'] * F['sqbod'] / 1000
    F['lam_s'] = lam_s(d)
    F['phiVc2_lams'] = F['phiVc2'] * F['lam_s']
    return F


def f2007_3():
    return footing(c=45.0, PD=100.0, PL=80.0)


def f2017_3():
    """4 m×4 m，h=80，d 兩向平均 69.96，f'c=210，PD=180、PL=120，qa=30，覆土 1 m（1.9）。"""
    B, c, h, fc, fy = 400.0, 45.0, 80.0, 210.0, 4200.0
    d = ((80 - 7.5 - 1.27) + (80 - 7.5 - 1.27 - 2.54)) / 2
    F = dict(B=B, c=c, h=h, d=d, fc=fc, fy=fy, PD=180.0, PL=120.0, qa=30.0)
    A = (B / 100) ** 2
    F['Wf'] = A * 0.8 * 2.4
    F['Ws'] = A * 1.0 * 1.9
    F['q_serv'] = (300 + F['Wf'] + F['Ws']) / A
    F['q_net_allow'] = 30 - (0.8 * 2.4 + 1.0 * 1.9)
    F['Pu'] = 1.2 * 180 + 1.6 * 120
    F['qu'] = F['Pu'] / A
    L = (B - c) / 2
    F['L'] = L
    F['Mu'] = F['qu'] * (B / 100) * (L / 100) ** 2 / 2
    F['As_req'] = as_req(F['Mu'] * 1e5, fy, fc, B, d)
    F['Asmin'] = 0.0018 * B * h
    F['n'] = math.ceil(F['As_req'] / 5.067)
    F['As_prov'] = F['n'] * 5.067
    F['Vu1'] = F['qu'] * (B / 100) * ((L - d) / 100)
    F['rho'] = F['As_prov'] / (B * d)
    F['phiVc1'] = PHI_V * 2.12 * F['rho'] ** (1 / 3) * sq(fc) * B * d / 1000
    F['phiVc1_old'] = PHI_V * 0.53 * sq(fc) * B * d / 1000
    F['bo'] = 4 * (c + d)
    F['Vu2'] = F['qu'] * ((B / 100) ** 2 - ((c + d) / 100) ** 2)
    F['phiVc2'] = PHI_V * 1.06 * sq(fc) * F['bo'] * d / 1000
    F['ratio2'] = F['Vu2'] / F['phiVc2']
    return F


# ── RC-2020-3：無梁版內柱穿孔＋剪力筋 ────────────────────────
def p2020_3():
    P = dict(fc=280.0, fyt=4200.0, c=100.0, h=40.0, d=35.0, wu=4.6, lx=8.0, ly=9.0)
    P['bo'] = 4 * (P['c'] + P['d'])
    P['lam_s'] = lam_s(P['d'])
    P['sqbod'] = sq(P['fc']) * P['bo'] * P['d']
    P['Vu'] = P['wu'] * (P['lx'] * P['ly'] - ((P['c'] + P['d']) / 100) ** 2)
    P['k'] = punch_coefs(1.0, 40, P['d'], P['bo'])
    P['Vc'] = min(P['k']) * P['lam_s'] * P['sqbod'] / 1000
    P['phiVc'] = PHI_V * P['Vc']
    P['phiVc_nolam'] = PHI_V * min(P['k']) * P['sqbod'] / 1000
    P['Vcw'] = 0.53 * P['lam_s'] * P['sqbod'] / 1000
    P['Vs'] = P['Vu'] / PHI_V - P['Vcw']
    P['phiVnmax'] = PHI_V * 1.59 * P['sqbod'] / 1000
    P['Av'] = 4 * 2 * 1.267
    P['s'] = P['Av'] * P['fyt'] * P['d'] / (P['Vs'] * 1000)
    P['phiVn5'] = PHI_V * (P['Vcw'] + P['Av'] * P['fyt'] * P['d'] / 5 / 1000)
    return P


# ── RC-2021-3：偏心四樁樁帽 ──────────────────────────────────
def p2021_3():
    P = dict(fc=280.0, Pu=100.0, x=90.0, n=4, Pc=40.0, Pt=10.0, D=55.0, d=45.0, c=50.0, rp=15.0, edge=40.0)
    P['sumx2'] = P['n'] * P['x'] ** 2
    P['k_e'] = P['Pu'] * P['x'] / P['sumx2']          # 每 cm 偏心，樁力增量 tf
    P['e_comp'] = (P['Pc'] - P['Pu'] / P['n']) / P['k_e']
    P['e_tens'] = (P['Pt'] + P['Pu'] / P['n']) / P['k_e']
    P['emax'] = min(P['e_comp'], P['e_tens'])
    P['lam_s'] = lam_s(P['d'])
    P['bo_col'] = 4 * (P['c'] + P['d'])
    P['phiVc_col'] = PHI_V * 1.06 * P['lam_s'] * sq(P['fc']) * P['bo_col'] * P['d'] / 1000
    rc = P['rp'] + P['d'] / 2
    P['r_crit'] = rc
    P['bo_corner'] = 2 * P['edge'] + math.pi * rc / 2
    P['bo_full'] = 2 * math.pi * rc
    P['phiVc_pile'] = PHI_V * 1.06 * P['lam_s'] * sq(P['fc']) * P['bo_corner'] * P['d'] / 1000
    P['k3_pile'] = 0.265 * (2 + 20 * P['d'] / P['bo_corner'])
    return P


# ── RC-2013-1：連續單向版外支承 ──────────────────────────────
def p2013_1():
    P = dict(fc=280.0, fy=4200.0, l=480.0, bw=30.0, wL=0.6, wSD=0.1, cover=2.0, db=0.953)
    P['ln'] = P['l'] - P['bw']
    P['hmin'] = P['l'] / 24
    P['hmin_in'] = P['l'] / 28
    P['h'] = 20.0
    P['wsw'] = 2.4 * P['h'] / 100
    P['wD'] = P['wSD'] + P['wsw']
    P['wu'] = 1.2 * P['wD'] + 1.6 * P['wL']
    w = P['wu'] * 10   # kgf/cm（1 m 寬）
    P['Mu'] = w * P['ln'] ** 2 / 24
    P['d'] = P['h'] - P['cover'] - 0.96 / 2
    P['As_flex'] = as_req(P['Mu'], P['fy'], P['fc'], 100, P['d'])
    P['Asmin'] = 0.0018 * 100 * P['h']
    P['s'] = 0.71 * 100 / P['Asmin']
    P['As19'] = 0.71 * 100 / 19
    P['As20'] = 0.71 * 100 / 20
    P['coef'] = {'外支承 1/24': 1 / 24, '外跨正 1/14': 1 / 14, '第一內支承 1/10': 1 / 10, '內跨正 1/16': 1 / 16, '其他內支承 1/11': 1 / 11}
    P['Mcoef'] = {k: v * w * P['ln'] ** 2 / 1e5 for k, v in P['coef'].items()}
    P['wLwD'] = P['wL'] / P['wD']
    return P


# ── RC-2019-3：橫膈版（精簡）─────────────────────────────────
def p2019_3():
    P = dict(fc=280.0, fy=2800.0, t=18.0, L=500.0, Vu=100.0, phi=0.6, Ab=1.27, s_flex=25.0)
    P['Acv'] = P['t'] * P['L']
    P['vc'] = 0.53 * sq(P['fc'])
    P['need'] = P['Vu'] * 1000 / (P['phi'] * P['Acv'])
    P['rho_t'] = (P['need'] - P['vc']) / P['fy']
    P['As_shear_s'] = P['rho_t'] * P['Acv'] / P['L']
    P['As_flex_s'] = 2 * P['Ab'] / P['s_flex']
    P['tot'] = P['As_shear_s'] + P['As_flex_s']
    P['s'] = 2 * P['Ab'] / P['tot']
    return P


def quiz():
    Q = {}
    Q['lam_s_d'] = {d: lam_s(d) for d in (25, 35, 45, 50, 70, 100)}
    Q['beta2_coef'] = 0.53 * (1 + 2 / 2)
    Q['beta_cross'] = 2 / (1.06 / 0.53 - 1)
    Q['bo_d_cross_int'] = 40 / (1.06 / 0.265 - 2)    # 內柱：αs d/bo = 2 → bo/d = 20
    Q['q1_qu'] = (1.2 * 60 + 1.6 * 40) / 2.5 ** 2
    Q['q2_bo'] = 4 * (50 + 40)
    Q['q2_Vu'] = 200 - 32 * 0.9 ** 2
    Q['q3_P'] = 120 / 4 + 120 * 20 * 75 / (4 * 75 ** 2)
    Q['ratio_rho_0.2%'] = 2.12 * 0.002 ** (1 / 3) / 0.53
    Q['ratio_rho_0.4%'] = 2.12 * 0.004 ** (1 / 3) / 0.53
    Q['rho_cross_oneway'] = (0.53 / 2.12) ** 3
    Q['ch2_Q1_Mu'] = 21.76 * 2.5 * 1.0 ** 2 / 2
    Q['ch3_c2_only'] = 216 - 24 * 0.4 ** 2
    Q['ch2_B2_over_L'] = (150 / 130) ** 2
    Q['old_new_ratio_2007'] = 2.12 * (50 / (300 * 50)) ** (1 / 3) / 0.53
    return Q


def _p(title, d):
    print(f'\n== {title}')
    for k, v in d.items():
        if isinstance(v, float):
            print(f'  {k:14s} = {v:,.4f}')
        elif isinstance(v, (list, tuple)):
            print(f'  {k:14s} = ' + ', '.join(f'{x:,.4f}' for x in v))
        elif isinstance(v, dict):
            print(f'  {k:14s} = ' + ', '.join(f'{a}:{b:,.4f}' for a, b in v.items()))
        else:
            print(f'  {k:14s} = {v}')


if __name__ == '__main__':
    _p('示範基腳 RC-2025-1', footing())
    _p('RC-2007-3', f2007_3())
    _p('RC-2017-3', f2017_3())
    _p('RC-2020-3', p2020_3())
    _p('RC-2021-3', p2021_3())
    _p('RC-2013-1', p2013_1())
    _p('RC-2019-3', p2019_3())
    _p('自我測驗／旁註', quiz())
