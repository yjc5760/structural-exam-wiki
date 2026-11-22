# -*- coding: utf-8 -*-
"""RC-U3-3 教科書講義（韌性與耐震）：全部數值（圖與內文共用）。單位 kgf、cm；力 tf、彎矩 tf·m。
執行 python3 calcs.py 印出全部數值，內文的數字一律抄這裡的輸出。

規範：建築物混凝土結構設計規範（112 年版，土木 401-112；ACI 318-19 世代）第 18 章（耐震），kgf/cm² 制。
  Mpr = As(1.25fy)(d − a/2)，a = 1.25 fy As /(0.85 f'c b)，φ = 1
  梁 Ve = (Mpr,l + Mpr,r)/ln ± wu ln/2；Vc = 0：VE ≥ Ve/2 且 Nu < Ag f'c/20
  梁塑鉸區：2h，s ≤ min(d/4, 6db, 15 cm)，第一支 ≤ 5 cm
  柱：lo ≥ max(h, ln/6, 45)；s ≤ min(b/4, 6db, so)，so = 10 + (35 − hx)/3，10 ≤ so ≤ 15
      Ash = max{0.3 s bc f'c/fyt (Ag/Ach − 1), 0.09 s bc f'c/fyt}
  接頭：Vjh = T1 + C2 − Vcol（外接頭 T − Vcol），T = 1.25 fy As；Vn = γ√f'c Aj（5.3／3.9／3.2），φ = 0.85
  搭接：ℓd = fy/(3.5λ√f'c) · ψ /((cb+Ktr)/db) · db，(cb+Ktr)/db ≤ 2.5；Class B = 1.3ℓd
  剪力牆：Vn = Acv(αc√f'c + ρt fy)，αc = 0.80（hw/lw ≤ 1.5）～0.53（≥ 2.0）
例題數據取自勘誤後題解（raw/solutions/RC-YYYY-N/RC-YYYY-N.md）。
"""
import math

PHI_V, PHI_J = 0.75, 0.85


def sq(fc):
    return math.sqrt(fc)


def mpr(As, fy, fc, b, d):
    T = 1.25 * fy * As
    a = T / (0.85 * fc * b)
    return T, a, T * (d - a / 2)


# ── 貫穿全書：RC-2012 連環題（梁 → 柱 → 接頭，同一構架）────────
def frame2012():
    F = dict(fc=280.0, fy=4200.0, fyt=4200.0, bw=50.0, hb=60.0, d=54.0, Atop=6 * 5.07, Abot=4 * 3.87,
             bc=60.0, hc=60.0, ln_col=300.0, Nu=50.0, db_col=2.22, dbt=1.27, cover_c=6.0)
    F['T_top'], F['a_neg'], M = mpr(F['Atop'], F['fy'], F['fc'], F['bw'], F['d'])
    F['Mpr_neg'] = M / 1e5
    F['T_bot'], F['a_pos'], M = mpr(F['Abot'], F['fy'], F['fc'], F['bw'], F['d'])
    F['Mpr_pos'] = M / 1e5
    F['Mn_neg'] = F['Atop'] * F['fy'] * (F['d'] - F['Atop'] * F['fy'] / (0.85 * F['fc'] * F['bw']) / 2) / 1e5
    # 柱（2012-3）
    F['Mcol_each'] = F['Mpr_neg'] / 2
    F['Vcol'] = F['Mpr_neg'] / (F['ln_col'] / 100)
    F['Vcol_wrong'] = 2 * F['Mpr_neg'] / (F['ln_col'] / 100)
    F['lo'] = max(F['ln_col'] / 6, F['hc'], 45.0)
    edge = F['cover_c'] - F['db_col'] / 2 - F['dbt']
    F['bcore'] = F['bc'] - 2 * edge
    F['Ag'] = F['bc'] * F['hc']
    F['Ach'] = F['bcore'] ** 2
    F['AgAch'] = F['Ag'] / F['Ach']
    F['hx'] = 48.0 / 3
    so = 10 + (35 - F['hx']) / 3
    F['so_raw'] = so
    F['so'] = min(15.0, max(10.0, so))
    F['s6db'] = 6 * F['db_col']
    F['s_geom'] = min(F['bc'] / 4, F['s6db'], F['so'])
    F['Av_col'] = 4 * 1.27
    k = F['fc'] / F['fyt']
    F['ash1_per_s'] = 0.3 * F['bcore'] * k * (F['AgAch'] - 1)
    F['ash2_per_s'] = 0.09 * F['bcore'] * k
    F['s_ash1'] = F['Av_col'] / F['ash1_per_s']
    F['s_ash2'] = F['Av_col'] / F['ash2_per_s']
    F['Nu_lim'] = 0.05 * F['fc'] * F['Ag'] / 1000
    F['Vs_col'] = F['Vcol'] / PHI_V
    F['s_shear'] = F['Av_col'] * F['fyt'] * F['d'] / (F['Vs_col'] * 1000)
    F['s_col'] = 13.0
    F['phiVs13'] = PHI_V * F['Av_col'] * F['fyt'] * F['d'] / 13 / 1000
    # 接頭（2012-4，外接頭／角隅邊柱）
    F['T1'] = F['T_top'] / 1000
    F['Vjh'] = F['T1'] - F['Vcol']
    F['Vjh_wrong'] = F['T1'] - F['Vcol_wrong']
    x = (F['bc'] - F['bw']) / 2
    F['bj'] = min(F['bw'] + F['hc'], F['bw'] + 2 * x, F['bc'])
    F['Aj'] = F['bj'] * F['hc']
    F['gamma'] = 3.2
    F['Vn_j'] = F['gamma'] * sq(F['fc']) * F['Aj'] / 1000
    F['phiVn_j'] = PHI_J * F['Vn_j']
    F['util'] = F['Vjh'] / F['phiVn_j']
    F['util_noVcol'] = F['T1'] / F['phiVn_j']
    return F


# ── RC-2025-2：耐震梁全鏈 ────────────────────────────────────
def p2025_2():
    P = dict(fc=280.0, fy=4200.0, fyt=2800.0, bw=60.0, d=76.0, h=85.0, ln=900.0, wu=2.0, db_min=3.22)
    P['Atop'], P['Abot'] = 8 * 8.14, 6 * 8.14
    _, P['a_neg'], M = mpr(P['Atop'], P['fy'], P['fc'], P['bw'], P['d']); P['Mpr_neg'] = M / 1e5
    _, P['a_pos'], M = mpr(P['Abot'], P['fy'], P['fc'], P['bw'], P['d']); P['Mpr_pos'] = M / 1e5
    P['Vseis'] = (P['Mpr_neg'] + P['Mpr_pos']) / (P['ln'] / 100)
    P['Vgrav'] = P['wu'] * P['ln'] / 100 / 2
    P['Ve'] = P['Vseis'] + P['Vgrav']
    P['Ve_other'] = P['Vseis'] - P['Vgrav']
    P['ratio'] = P['Vseis'] / P['Ve']
    P['Vs'] = P['Ve'] / PHI_V
    P['Av'] = 4 * 1.27
    P['s_req'] = P['Av'] * P['fyt'] * P['d'] / (P['Vs'] * 1000)
    P['s_cap'] = min(P['d'] / 4, 6 * P['db_min'], 15.0)
    P['hinge'] = 2 * P['h']
    P['phiVs15'] = PHI_V * P['Av'] * P['fyt'] * P['d'] / 15 / 1000
    P['Vsmax'] = 2.12 * sq(P['fc']) * P['bw'] * P['d'] / 1000
    # 區外
    P['Ve_170'] = P['Ve'] - P['wu'] * 1.70
    P['Vc'] = 0.53 * sq(P['fc']) * P['bw'] * P['d'] / 1000
    P['Vs_out'] = P['Ve_170'] / PHI_V - P['Vc']
    P['s_out'] = 2 * 1.27 * P['fyt'] * P['d'] / (P['Vs_out'] * 1000)
    P['phiVn_out20'] = PHI_V * (P['Vc'] + 2.54 * P['fyt'] * P['d'] / 20 / 1000)
    P['phiMn_over'] = P['Mpr_neg'] / (0.9 * P['Atop'] * P['fy'] * (P['d'] - P['Atop'] * P['fy'] / (0.85 * P['fc'] * P['bw']) / 2) / 1e5)
    return P


# ── RC-2016-2：Vc 不歸零、6db 控制 ───────────────────────────
def p2016_2():
    P = dict(fc=280.0, fy=4200.0, b=35.0, d=63.0, h=70.0, ln=750.0, Atop=3 * 6.47, Abot=3 * 3.87, wD=2.0, wL=1.0, db_min=2.22)
    _, _, M = mpr(P['Atop'], P['fy'], P['fc'], P['b'], P['d']); P['Mpr_neg'] = M / 1e5
    _, _, M = mpr(P['Abot'], P['fy'], P['fc'], P['b'], P['d']); P['Mpr_pos'] = M / 1e5
    P['wu'] = 1.2 * P['wD'] + 1.0 * P['wL']
    P['Vseis'] = (P['Mpr_neg'] + P['Mpr_pos']) / (P['ln'] / 100)
    P['Vgrav'] = P['wu'] * P['ln'] / 100 / 2
    P['Ve'] = P['Vseis'] + P['Vgrav']
    P['ratio'] = P['Vseis'] / P['Ve']
    P['Vc'] = 0.53 * sq(P['fc']) * P['b'] * P['d'] / 1000
    P['Vs'] = P['Ve'] / PHI_V - P['Vc']
    P['s_req'] = 3 * 0.71 * P['fy'] * P['d'] / (P['Vs'] * 1000)
    P['caps'] = (P['d'] / 4, 6 * P['db_min'], 15.0)
    P['s_cap'] = min(P['caps'])
    P['hinge'] = 2 * P['h']
    return P


# ── RC-2013-2：特殊矩形柱圍束 ────────────────────────────────
def p2013_2():
    P = dict(fc=280.0, fyt=2800.0, b=50.0, cover=4.0, db=3.22, dbt=1.27)
    P['hc'] = P['b'] - 2 * P['cover']
    P['Ag'] = P['b'] ** 2
    P['Ach'] = P['hc'] ** 2
    P['AgAch'] = P['Ag'] / P['Ach']
    k = P['fc'] / P['fyt']
    P['ash1'] = 0.3 * P['hc'] * (P['AgAch'] - 1) * k
    P['ash2'] = 0.09 * P['hc'] * k
    P['b4'] = P['b'] / 4
    P['s6db'] = 6 * P['db']
    P['hx'] = (P['hc'] - 2 * P['dbt'] - P['db']) / 4
    P['so_raw'] = 10 + (35 - P['hx']) / 3
    P['so'] = min(15.0, max(10.0, P['so_raw']))
    P['s'] = 12.0
    P['Ash_req'] = max(P['ash1'], P['ash2']) * P['s']
    P['legs'] = math.ceil(P['Ash_req'] / 1.27)
    P['Ash_prov'] = P['legs'] * 1.27
    P['s_out'] = min(P['s6db'], 15.0)
    return P


# ── RC-2005-3、RC-2018-2、RC-2003-3：接頭 ────────────────────
def p2005_3():
    P = dict(fc=280.0, fy=4200.0, H=365.0, bc=60.0, hc=60.0, bw=60.0, d=70.0, As=6 * 5.07)
    P['T'], P['a'], M = mpr(P['As'], P['fy'], P['fc'], P['bw'], P['d'])
    P['Mpr'] = M / 1e5
    P['Vcol'] = M / P['H'] / 1000
    P['T'] /= 1000
    P['Vjh'] = P['T'] - P['Vcol']
    P['Aj'] = 60 * 60.0
    P['phiVn'] = PHI_J * 3.2 * sq(P['fc']) * P['Aj'] / 1000
    P['util'] = P['Vjh'] / P['phiVn']
    return P


def p2018_2():
    P = dict(fc=280.0, fy=4200.0, H=380.0, b=50.0, d=43.0, As=8 * 6.47)
    T, a, M = mpr(P['As'], P['fy'], P['fc'], P['b'], P['d'])
    P['T'], P['a'], P['Mpr'] = T / 1000, a, M / 1e5
    P['Vcol'] = M / P['H'] / 1000
    P['Vj'] = P['T'] - P['Vcol']
    P['Aj'] = 50 * 50.0
    P['phiVn'] = PHI_J * 3.2 * sq(P['fc']) * P['Aj'] / 1000
    P['ratio'] = P['Vj'] / P['phiVn']
    return P


def p2003_3():
    P = dict(fc=280.0, fy=4200.0, H=350.0, h=40.0, bcol=50.0, bw=24.0, Atop=11.48, Abot=5.74, Mn_neg=24.0, Mn_pos=12.0)
    P['T1'] = 1.25 * P['Atop'] * P['fy'] / 1000
    P['T2'] = 1.25 * P['Abot'] * P['fy'] / 1000
    P['Vcol'] = 1.25 * (P['Mn_neg'] + P['Mn_pos']) / (P['H'] / 100)
    P['Vu'] = P['T1'] + P['T2'] - P['Vcol']
    x = P['bw'] / 2
    P['bj'] = min(P['bw'] + P['h'], 2 * x, P['bcol'])
    P['Aj'] = P['bj'] * P['h']
    P['Vn'] = 3.9 * sq(P['fc']) * P['Aj'] / 1000
    P['phiVn'] = PHI_J * P['Vn']
    P['ratio'] = P['Vu'] / P['phiVn']
    P['bj_center'] = min(P['bw'] + P['h'], P['bcol'])
    P['phiVn_center'] = PHI_J * 3.9 * sq(P['fc']) * P['bj_center'] * P['h'] / 1000
    return P


# ── RC-2022-4：韌性三層次（公路橋梁耐震規範公式）────────────
def p2022_4():
    P = dict(L=3.2, db=0.0322, fy=4200.0, M=232.5)
    a = 0.5
    P['phiy'] = 0.004 + a * 0.002
    P['My'] = 200 + a * 40
    P['phiu'] = 0.030 + a * (-0.020)
    P['Mu'] = 230 + a * 30
    P['phid'] = P['phiy'] + (P['M'] - P['My']) / (P['Mu'] - P['My']) * (P['phiu'] - P['phiy'])
    P['Lp1'] = 0.08 * P['L'] + 0.0022 * P['db'] * P['fy']
    P['Lp_min'] = 0.0044 * P['db'] * P['fy']
    P['Lp'] = max(P['Lp1'], P['Lp_min'])
    P['dy'] = P['phiy'] * P['L'] ** 2 / 3
    P['thy'] = P['dy'] / P['L']
    P['dd'] = P['M'] / P['My'] * P['dy'] + (P['phid'] - P['phiy']) * P['Lp'] * (P['L'] - 0.5 * P['Lp'])
    P['thd'] = P['dd'] / P['L']
    P['mu_phi'] = P['phid'] / P['phiy']
    P['mu_th'] = P['thd'] / P['thy']
    P['mu_d'] = P['dd'] / P['dy']
    # 容量（極限點）對照
    P['du'] = P['Mu'] / P['My'] * P['dy'] + (P['phiu'] - P['phiy']) * P['Lp'] * (P['L'] - 0.5 * P['Lp'])
    P['mu_phi_cap'] = P['phiu'] / P['phiy']
    P['mu_d_cap'] = P['du'] / P['dy']
    return P


# ── RC-2003-2：耐震柱拉力搭接 ────────────────────────────────
def p2003_2():
    P = dict(fc=280.0, fy=4200.0, b=60.0, db=2.87, dbt=1.27, cover=4.0, s=10.0, n=5, legs=3, ln=300.0)
    P['c_cover'] = P['cover'] + P['dbt'] + P['db'] / 2
    P['scc'] = (P['b'] - 2 * P['c_cover']) / 4
    P['cb'] = min(P['c_cover'], P['scc'] / 2)
    P['Atr'] = P['legs'] * 1.27
    P['Ktr'] = 40 * P['Atr'] / (P['s'] * P['n'])
    P['conf_raw'] = (P['cb'] + P['Ktr']) / P['db']
    P['conf'] = min(2.5, P['conf_raw'])
    P['ld'] = P['fy'] / (3.5 * sq(P['fc'])) / P['conf'] * P['db']
    P['lst'] = 1.3 * P['ld']
    P['zone'] = (P['ln'] / 4, 3 * P['ln'] / 4)
    P['ld_noconf'] = P['fy'] / (3.5 * sq(P['fc'])) / 1.0 * P['db']
    P['u_over_sqfc'] = 1 / (4 / 3.5 * 1)    # ℓd = fy db/(4u) ↔ fy db /(3.5√f'c·conf)：u = 3.5·conf·√f'c/4
    return P


# ── RC-2003-4：剪力牆（精簡）────────────────────────────────
def p2003_4():
    P = dict(fc=280.0, fy=4200.0, tw=15.0, lw=930.0, hw=800.0, Vu=75.0, s=30.0)
    P['Acv'] = P['tw'] * P['lw']
    P['single'] = 0.53 * sq(P['fc']) * P['Acv'] / 1000
    P['rmin_trigger'] = 0.27 * sq(P['fc']) * P['Acv'] / 1000
    P['s_rmin'] = 1.27 / (0.0025 * P['tw'])
    P['rho_t'] = 1.27 / (P['tw'] * P['s'])
    P['hwlw'] = P['hw'] / P['lw']
    P['alpha_c'] = 0.80
    P['Vn'] = P['Acv'] * (P['alpha_c'] * sq(P['fc']) + P['rho_t'] * P['fy']) / 1000
    P['Vn_cap'] = 2.12 * sq(P['fc']) * P['Acv'] / 1000
    P['phiVn'] = PHI_V * P['Vn']
    # 邊界構材需求（應力法）：全牆斷面（腹版 15×870＋兩端 30×30 邊界構材），1.2D+1.0L+1.0E 每端 116.5 tf
    A = 15 * 870 + 2 * 30 * 30
    I = 15 * 870 ** 3 / 12 + 2 * (30 ** 4 / 12 + 900 * 450 ** 2)
    P['A_wall'], P['I_wall'] = A, I
    P['Mu_wall'] = 45 * 8.0 + 30 * 4.5
    P['fc_edge'] = 2 * 116.5e3 / A + P['Mu_wall'] * 1e5 * 465 / I
    P['fc_lim'] = 0.2 * P['fc']
    P['F_ot'] = P['Mu_wall'] / 9.0
    P['BE_max'] = 116.5 + P['F_ot']
    P['BE_min'] = 65.25 - P['F_ot']
    return P


def p2019_3():
    P = dict(fc=280.0, fy=2800.0, t=18.0, L=500.0, Vu=100.0, phi=0.6)
    P['Acv'] = P['t'] * P['L']
    P['need'] = P['Vu'] * 1000 / (P['phi'] * P['Acv'])
    P['vc'] = 0.53 * sq(P['fc'])
    P['rho_t'] = (P['need'] - P['vc']) / P['fy']
    P['As_shear'] = P['rho_t'] * P['t']
    P['As_flex'] = 2 * 1.27 / 25
    P['As_tot'] = P['As_flex'] + P['As_shear']
    P['s_req'] = 2 * 1.27 / P['As_tot']
    P['s_use'] = 15.0
    P['rho_prov'] = (2 * 1.27 / 15 - P['As_flex']) / P['t']
    P['phiVn'] = P['phi'] * (P['vc'] + P['rho_prov'] * P['fy']) * P['Acv'] / 1000
    return P


# ── RC-2010-2：耐震柱 D29 拉力搭接（精簡）；RC-2012-4 外接頭彎鉤錨定 ──
def p2010_2():
    P = dict(fc=280.0, fy=4200.0, db=2.87, clear=9.3, cover=4.0, dbt=1.27, Atr=1.267, s=10.0, n=3)
    P['ctc'] = P['clear'] + P['db']
    P['c_half'] = P['ctc'] / 2
    P['c_cover'] = P['cover'] + P['dbt'] + P['db'] / 2
    P['cb'] = min(P['c_half'], P['c_cover'])
    P['Ktr'] = 40 * P['Atr'] / (P['s'] * P['n'])
    P['conf_raw'] = (P['cb'] + P['Ktr']) / P['db']
    P['conf'] = min(2.5, P['conf_raw'])
    P['ld'] = P['fy'] / (3.5 * sq(P['fc'])) / P['conf'] * P['db']
    P['lst'] = 1.3 * P['ld']
    return P


def hook2012():
    P = dict(fc=280.0, fy=4200.0, db=2.54, hc=60.0, cover=4.0)
    P['ldh_raw'] = P['fy'] * P['db'] / (17.2 * sq(P['fc']))
    P['ldh'] = max(P['ldh_raw'], 8 * P['db'], 15.0)
    P['avail'] = P['hc'] - P['cover']
    P['ld_straight_bond'] = P['fy'] * P['db'] / (4 * 0.875 * 2.5 * sq(P['fc']))
    return P


def quiz():
    Q = {}
    Q['ash_cross_AgAch'] = 1 + 0.09 / 0.3
    Q['richart_coef'] = 1 / 4.1
    Q['so_hx20'] = 10 + (35 - 20) / 3
    Q['q_Mpr'] = mpr(20.0, 4200, 280, 40, 55)[2] / 1e5
    Q['q_Ve'] = (40 + 25) / 6 + 3 * 6 / 2
    Q['q_ratio'] = ((40 + 25) / 6) / Q['q_Ve']
    Q['q_lo'] = max(400 / 6, 55, 45)
    Q['q_Vcol'] = (60 + 35) / 3.2
    Q['ratio_125_09'] = 1.25 / 0.9
    Q['mpr_over_mn_2012'] = None
    return Q


def _p(title, d):
    print(f'\n== {title}')
    for k, v in d.items():
        if isinstance(v, float):
            print(f'  {k:14s} = {v:,.4f}')
        elif isinstance(v, (list, tuple)):
            print(f'  {k:14s} = ' + ', '.join(f'{x:,.4f}' for x in v))
        else:
            print(f'  {k:14s} = {v}')


if __name__ == '__main__':
    F = frame2012()
    _p('RC-2012 連環題', F)
    print('  Mpr/Mn（頂筋）=', round(F['Mpr_neg'] / F['Mn_neg'], 3))
    _p('RC-2025-2', p2025_2())
    _p('RC-2016-2', p2016_2())
    _p('RC-2013-2', p2013_2())
    _p('RC-2005-3', p2005_3())
    _p('RC-2018-2', p2018_2())
    _p('RC-2003-3', p2003_3())
    _p('RC-2022-4', p2022_4())
    _p('RC-2003-2', p2003_2())
    _p('RC-2003-4', p2003_4())
    _p('RC-2019-3', p2019_3())
    _p('自我測驗／旁註', quiz())
