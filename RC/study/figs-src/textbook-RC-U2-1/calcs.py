# -*- coding: utf-8 -*-
"""RC-U2-1 教科書講義（剪力）：全部數值（圖與內文共用）。單位 kgf、cm；剪力另列 tf。
執行 python3 calcs.py 印出全部數值，內文的數字一律抄這裡的輸出。

規範：建築物混凝土結構設計規範（112 年版，土木 401-112；ACI 318-19 世代），kgf/cm² 制。
  Vc（Av ≥ Av,min）＝ max{0.53√f'c + Nu/6Ag , 2.1ρw^(1/3)√f'c + Nu/6Ag}·bw·d ≤ 1.33√f'c·bw·d，Nu/6Ag ≤ 0.05f'c，Vc ≥ 0
  Vs ≤ 2.12√f'c·bw·d；Vs > 1.06√f'c·bw·d 時間距減半；Av,min = max(0.2√f'c, 3.5)·bw·s/fyt
  扭力：Tth = 0.265√f'c·Acp²/pcp（= Tcr/4）；Tcr = 1.06√f'c·Acp²/pcp
例題數據取自勘誤後題解（raw/solutions/RC-YYYY-N/RC-YYYY-N.md）。
"""
import math

PHI_V = 0.75
AB = {'D10': 0.7133, 'D13': 1.267, 'D16': 1.986, 'D19': 2.865, 'D22': 3.871, 'D25': 5.067, 'D29': 6.469, 'D32': 8.143}


def sq(fc):
    return math.sqrt(fc)


def vc_simple(fc, bw, d, Nu=0.0, Ag=None):
    """現行簡化式（Nu 壓為正、拉為負）：[0.53√f'c + Nu/6Ag]bw d ≥ 0。"""
    ax = 0.0 if not Nu else Nu / (6 * Ag)
    if ax > 0:
        ax = min(ax, 0.05 * fc)
    return max(0.0, (0.53 * sq(fc) + ax) * bw * d)


def vc_rho(fc, bw, d, rho, Nu=0.0, Ag=None):
    ax = 0.0 if not Nu else Nu / (6 * Ag)
    if ax > 0:
        ax = min(ax, 0.05 * fc)
    return max(0.0, (2.1 * rho ** (1 / 3) * sq(fc) + ax) * bw * d)


def vc_cap(fc, bw, d):
    return 1.33 * sq(fc) * bw * d


def smax_code(fc, bw, d, Vs):
    lim = 1.06 * sq(fc) * bw * d
    return (min(d / 2, 60.0) if Vs <= lim else min(d / 4, 30.0)), lim


def avmin_per_s(fc, bw, fyt):
    return max(0.2 * sq(fc), 3.5) * bw / fyt


# ── 示範梁：RC-2021-1 的 T 形梁（支承端剪力）────────────────
def demo():
    D = dict(bw=40.0, d=60.0, h=70.0, bf=100.0, hf=10.0, fc=240.0, fy=4200.0, fyt=2800.0,
             L=800.0, wD=1.8, wL=4.5)
    D['wu'] = 1.2 * D['wD'] + 1.6 * D['wL']                # tf/m
    D['Vsup'] = D['wu'] * D['L'] / 100 / 2 * 1000            # 支承面 kgf
    D['Vu'] = D['wu'] * (D['L'] / 2 - D['d']) / 100 * 1000   # 距支承面 d
    D['sqfc'] = sq(D['fc'])
    D['vc_stress'] = 0.53 * D['sqfc']                        # kgf/cm²
    D['Vc'] = vc_simple(D['fc'], D['bw'], D['d'])
    D['phiVc'] = PHI_V * D['Vc']
    D['half_phiVc'] = 0.5 * D['phiVc']
    D['Vs'] = D['Vu'] / PHI_V - D['Vc']
    D['Av'] = 2 * AB['D10']
    D['s_req'] = D['Av'] * D['fyt'] * D['d'] / D['Vs']
    D['s_code'], D['lim106'] = smax_code(D['fc'], D['bw'], D['d'], D['Vs'])
    D['Vsmax'] = 2.12 * D['sqfc'] * D['bw'] * D['d']
    D['phiVnmax'] = PHI_V * (D['Vc'] + D['Vsmax'])
    D['avmin_s'] = avmin_per_s(D['fc'], D['bw'], D['fyt'])
    D['s_avmin'] = D['Av'] / D['avmin_s']
    D['s_use'] = 10.0
    D['Vs_use'] = D['Av'] * D['fyt'] * D['d'] / D['s_use']
    D['phiVn_use'] = PHI_V * (D['Vc'] + D['Vs_use'])
    # 若誤用支承面
    D['Vs_face'] = D['Vsup'] / PHI_V - D['Vc']
    D['s_face'] = D['Av'] * D['fyt'] * D['d'] / D['Vs_face']
    # 直到哪裡不需要剪力筋（x 自支承面量起，cm）
    w = D['wu'] * 10  # kgf/cm
    D['x_halfphiVc'] = (D['Vsup'] - D['half_phiVc']) / w
    D['x_phiVc'] = (D['Vsup'] - D['phiVc']) / w
    # 以 MPa 制交叉驗算 0.53 ↔ 1/6
    D['mpa_ratio'] = 0.53 / (1 / 6 * math.sqrt(1 / 0.0980665) * 0.0980665 * 1 / 0.0980665 * 0.0980665)
    return D


def unit_check():
    """0.53 kgf 制 ↔ 1/6 MPa 制：1/6·√(f'c[MPa]) MPa 換回 kgf/cm²。"""
    k = 1 / 6 * math.sqrt(0.0980665) / 0.0980665   # 對 √(f'c kgf/cm²) 的係數
    return k


# ── 第 1、2 章：莫爾圓（示意用單位應力）─────────────────────
def mohr(sig, tau):
    """σ 拉為正。回傳 (σ1, σ2, θp 主拉方向與梁軸夾角°)。"""
    c = sig / 2
    r = math.sqrt((sig / 2) ** 2 + tau ** 2)
    th = 0.5 * math.degrees(math.atan2(2 * tau, sig))
    return c + r, c - r, th


def crack_angle(sig, tau):
    """斜裂縫與梁軸夾角（裂縫垂直主拉方向）。σ 拉為正。"""
    _, _, th = mohr(sig, tau)
    return 90 - th


# ── RC-2010-3：軸力修正（簡化式）────────────────────────────
def p2010_3():
    P = dict(fc=280.0, bw=40.0, h=60.0, d=52.0, Nu=30000.0, Vu=20000.0)
    P['Ag'] = P['bw'] * P['h']
    P['ax'] = P['Nu'] / (6 * P['Ag'])
    out = {}
    for k, N in (('a', 0.0), ('b', P['Nu']), ('c', -P['Nu'])):
        Vc = vc_simple(P['fc'], P['bw'], P['d'], N, P['Ag'])
        out[k] = dict(N=N, Vc=Vc, phiVc=PHI_V * Vc)
    P['cases'] = out
    # 舊式對照（401-100：壓 1+Nu/140Ag、拉 1+Nu/35Ag）
    s = 0.53 * sq(P['fc']) * P['bw'] * P['d']
    P['old_b'] = PHI_V * s * (1 + P['Nu'] / (140 * P['Ag']))
    P['old_c'] = PHI_V * s * max(0, 1 - P['Nu'] / (35 * P['Ag']))
    P['NuAg'] = P['Nu'] / P['Ag']
    return P


# ── RC-2014-3：兩式取大＋軸力 ────────────────────────────────
def p2014_3():
    P = dict(fc=280.0, bw=30.0, d=60.0, h=70.0, As=24.42, Nu=25000.0, wu=5.0, half=250.0)
    P['Ag'] = P['bw'] * P['h']
    P['rho'] = P['As'] / (P['bw'] * P['d'])
    P['rho13'] = P['rho'] ** (1 / 3)
    P['ka'] = 0.53 * sq(P['fc'])
    P['kb'] = 2.1 * P['rho13'] * sq(P['fc'])
    P['cap'] = vc_cap(P['fc'], P['bw'], P['d'])
    P['ax'] = P['Nu'] / (6 * P['Ag'])
    P['Vu'] = P['wu'] * 10 * (P['half'] - P['d'])
    P['cases'] = {}
    for k, N in (('1', 0.0), ('2', P['Nu']), ('3', -P['Nu'])):
        a = vc_simple(P['fc'], P['bw'], P['d'], N, P['Ag'])
        b = vc_rho(P['fc'], P['bw'], P['d'], P['rho'], N, P['Ag'])
        P['cases'][k] = dict(N=N, a=a, b=b, Vc=min(max(a, b), P['cap']))
    # 舊版 Mm 法對照（401-100，軸壓）：Vc = [0.53√f'c + 176ρw Vu d/Mm] bw d ≤ 0.93√f'c bw d √(1+Nu/35Ag)
    Mu = P['wu'] * 10 * (P['half'] * P['d'] - P['d'] ** 2 / 2) + 0  # 均佈：M(x)=w(Lx/2 - x²/2)，此處 L/2=half
    P['Mu'] = P['wu'] * 10 * (2 * P['half'] * P['d'] / 2 - P['d'] ** 2 / 2)
    return P


# ── RC-2020-2：倒 T 梁，不可 d 偏移 ──────────────────────────
def p2020_2():
    P = dict(fc=280.0, fyt=4200.0, bw=35.0, h=70.0, d=64.0, wu=15.0, L=800.0)
    P['Av'] = 2 * AB['D13']
    P['Vc'] = vc_simple(P['fc'], P['bw'], P['d'])
    P['phiVc'] = PHI_V * P['Vc']
    P['Vu_face'] = P['wu'] * P['L'] / 100 / 2 * 1000
    P['Vu_d'] = P['Vu_face'] - P['wu'] * 10 * P['d']
    P['Vs'] = P['Vu_face'] / PHI_V - P['Vc']
    P['s_code'], P['lim106'] = smax_code(P['fc'], P['bw'], P['d'], P['Vs'])
    P['s_req'] = P['Av'] * P['fyt'] * P['d'] / P['Vs']
    P['Vsmax'] = 4 * P['Vc']
    P['Vumax'] = PHI_V * 5 * P['Vc']
    # 誤判可偏移
    P['Vs_wrong'] = P['Vu_d'] / PHI_V - P['Vc']
    P['s_wrong'] = P['Av'] * P['fyt'] * P['d'] / P['Vs_wrong']
    return P


# ── RC-2006-1：撓曲強度反推設計剪力（懸臂）───────────────────
def p2006_1():
    P = dict(fc=280.0, fy=4200.0, Es=2.04e6, b=30.0, d=45.0, dp=8.0, As=40.0, Asp=24.0, L=450.0)
    P['Av'] = 2 * 0.71
    b1 = 0.85
    # 試假設壓力筋降伏
    a0 = (P['As'] - P['Asp']) * P['fy'] / (0.85 * P['fc'] * P['b'])
    c0 = a0 / b1
    P['a0'], P['c0'] = a0, c0
    P['esp0'] = 0.003 * (c0 - P['dp']) / c0
    # 未降伏：0.85fc·b1·b·c + As'(6120(c-d')/c - 0.85fc) = As fy
    A = 0.85 * P['fc'] * b1 * P['b']
    k = P['Es'] * 0.003
    # A c² + (k As' - 0.85fc As' - As fy) c - k As' d' = 0
    B = k * P['Asp'] - 0.85 * P['fc'] * P['Asp'] - P['As'] * P['fy']
    Cq = -k * P['Asp'] * P['dp']
    c = (-B + math.sqrt(B * B - 4 * A * Cq)) / (2 * A)
    a = b1 * c
    fsp = k * (c - P['dp']) / c
    Cc = 0.85 * P['fc'] * a * P['b']
    Cs = P['Asp'] * (fsp - 0.85 * P['fc'])
    Mn = Cc * (P['d'] - a / 2) + Cs * (P['d'] - P['dp'])
    et = 0.003 * (P['d'] - c) / c
    P.update(c=c, a=a, fsp=fsp, Cc=Cc, Cs=Cs, Mn=Mn, et=et)
    P['phiMn'] = 0.9 * Mn
    P['wu'] = 2 * P['phiMn'] / P['L'] ** 2          # kgf/cm
    P['Vu'] = P['wu'] * (P['L'] - P['d'])
    P['Vu_face'] = P['wu'] * P['L']
    P['Vc'] = vc_simple(P['fc'], P['b'], P['d'])
    P['phiVc'] = PHI_V * P['Vc']
    P['Vs'] = P['Vu'] / PHI_V - P['Vc']
    P['s_code'], P['lim106'] = smax_code(P['fc'], P['b'], P['d'], P['Vs'])
    P['s_req'] = P['Av'] * P['fy'] * P['d'] / P['Vs']
    P['s_avmin'] = P['Av'] * P['fy'] / (3.5 * P['b'])
    P['Vs_face'] = P['Vu_face'] / PHI_V - P['Vc']
    P['s_face'] = P['Av'] * P['fy'] * P['d'] / P['Vs_face']
    return P


# ── RC-2023-3：懸臂偏心載重，扭力可忽略門檻 ──────────────────
def p2023_3():
    P = dict(fc=280.0, bw=35.0, h=60.0, d=53.0, L=350.0, wu=2.5)
    P['Vu'] = P['wu'] * 10 * (P['L'] - P['d'])
    P['Vu_face'] = P['wu'] * 10 * P['L']
    P['Vc'] = vc_simple(P['fc'], P['bw'], P['d'])
    P['phiVc'] = PHI_V * P['Vc']
    P['Acp'] = P['bw'] * P['h']
    P['pcp'] = 2 * (P['bw'] + P['h'])
    P['A2p'] = P['Acp'] ** 2 / P['pcp']
    P['Tth'] = 0.265 * sq(P['fc']) * P['A2p']
    P['phiTth'] = PHI_V * P['Tth']
    P['Tcr'] = 1.06 * sq(P['fc']) * P['A2p']
    P['emax'] = P['phiTth'] / P['Vu']
    # 單位陷阱：SI 係數 1/12 直接代 kgf
    P['Tth_wrong'] = PHI_V * (1 / 12) * sq(P['fc']) * P['A2p']
    P['e_wrong'] = P['Tth_wrong'] / P['Vu']
    return P


# ── RC-2011-4：Tu = Tcr 時尚可承受的 Vu ─────────────────────
def p2011_4():
    P = dict(fc=280.0, fyt=2800.0, bw=35.0, h=60.0, d=53.0, cover=4.0, dbt=1.27, s=8.0)
    P['Ab'] = AB['D13']
    P['Acp'] = P['bw'] * P['h']
    P['pcp'] = 2 * (P['bw'] + P['h'])
    P['Tcr'] = 1.06 * sq(P['fc']) * P['Acp'] ** 2 / P['pcp']
    P['xoh'] = P['bw'] - 2 * (P['cover'] + P['dbt'] / 2)
    P['yoh'] = P['h'] - 2 * (P['cover'] + P['dbt'] / 2)
    P['Aoh'] = P['xoh'] * P['yoh']
    P['ph'] = 2 * (P['xoh'] + P['yoh'])
    P['Ao'] = 0.85 * P['Aoh']
    P['At_s'] = P['Tcr'] / (2 * PHI_V * P['Ao'] * P['fyt'])
    P['leg_s'] = P['Ab'] / P['s']
    P['Av_s'] = 2 * (P['leg_s'] - P['At_s'])
    P['Vs'] = P['Av_s'] * P['fyt'] * P['d']
    P['Vc'] = vc_simple(P['fc'], P['bw'], P['d'])
    P['Vu1'] = PHI_V * (P['Vc'] + P['Vs'])
    P['tau_t'] = P['Tcr'] * P['ph'] / (1.7 * P['Aoh'] ** 2)
    P['rhs'] = PHI_V * (P['Vc'] / (P['bw'] * P['d']) + 2.12 * sq(P['fc']))
    P['Vu2'] = math.sqrt(P['rhs'] ** 2 - P['tau_t'] ** 2) * P['bw'] * P['d']
    P['Vu'] = min(P['Vu1'], P['Vu2'])
    return P


# ── RC-2018-1：扭剪疊加設計箍筋 ──────────────────────────────
def p2018_1():
    P = dict(fc=280.0, fyt=2800.0, b=50.0, h=50.0, d=43.0, cover=4.0, dbt=1.27, Tu=400000.0, Vu=20000.0)
    P['Ab'] = AB['D13']
    P['Acp'] = P['b'] * P['h']
    P['pcp'] = 2 * (P['b'] + P['h'])
    P['phiTth'] = PHI_V * 0.265 * sq(P['fc']) * P['Acp'] ** 2 / P['pcp']
    x1 = P['b'] - 2 * (P['cover'] + P['dbt'] / 2)
    P['Aoh'] = x1 * x1
    P['ph'] = 4 * x1
    P['Ao'] = 0.85 * P['Aoh']
    P['Vc'] = vc_simple(P['fc'], P['b'], P['d'])
    P['v'] = P['Vu'] / (P['b'] * P['d'])
    P['t'] = P['Tu'] * P['ph'] / (1.7 * P['Aoh'] ** 2)
    P['lhs'] = math.hypot(P['v'], P['t'])
    P['rhs'] = PHI_V * (P['Vc'] / (P['b'] * P['d']) + 2.12 * sq(P['fc']))
    P['At_s'] = P['Tu'] / (2 * PHI_V * P['Ao'] * P['fyt'])
    P['Vs'] = P['Vu'] / PHI_V - P['Vc']
    P['Av_s'] = P['Vs'] / (P['fyt'] * P['d'])
    P['need'] = P['At_s'] + P['Av_s'] / 4
    P['s'] = P['Ab'] / P['need']
    P['ph8'] = P['ph'] / 8
    return P


# ── RC-2017-2：介面摩擦剪力（植筋）──────────────────────────
def p2017_2():
    P = dict(fc=210.0, fy=4200.0, Vu=195742.0, mu=1.0, Ab_exam=3.871, width=40.0)
    P['Vn'] = P['Vu'] / PHI_V
    P['Avf'] = P['Vn'] / (P['mu'] * P['fy'])
    P['n'] = math.ceil(P['Avf'] / P['Ab_exam'])
    P['vlim'] = min(0.2 * P['fc'], 55.0)
    P['Ac_req'] = P['Vn'] / P['vlim']
    P['len_req'] = P['Ac_req'] / P['width']
    P['n_D19'] = math.ceil(P['Avf'] / AB['D19'])
    # 若誤用 μ=0.6（未粗糙）
    P['Avf_06'] = P['Vn'] / (0.6 * P['fy'])
    P['Avf_14'] = P['Vn'] / (1.4 * P['fy'])
    return P


# ── RC-2009-3：壓拉桿模式（φ=1）──────────────────────────────
def p2009_3():
    P = dict(fc=250.0, fy=4200.0, b=20.0, lb=20.0, ht=20.0, hc=20.0, h=70.0, a=50.0, As=6 * 2.87)
    P['z'] = P['h'] - P['hc'] / 2 - P['ht'] / 2
    P['theta'] = math.degrees(math.atan2(P['z'], P['a']))
    th = math.radians(P['theta'])
    P['ws'] = P['lb'] * math.sin(th) + P['ht'] * math.cos(th)
    P['F_strut'] = 1 / math.sin(th) / 2           # 斜壓桿力 / P
    P['P_tie'] = P['As'] * P['fy'] / 0.5
    P['P_strut'] = 0.85 * 0.75 * P['fc'] * P['b'] * P['ws'] / P['F_strut']
    P['P_cct'] = 0.85 * 0.80 * P['fc'] * P['b'] * P['lb'] / 0.5
    P['P_ccc'] = 0.85 * 1.0 * P['fc'] * P['b'] * P['hc'] / 0.5
    P['Pmax'] = min(P['P_tie'], P['P_strut'], P['P_cct'], P['P_ccc'])
    P['ad'] = P['a'] / (P['h'] - 10)
    return P


# ── RC-2025-2：耐震梁剪力鏈（本書只精簡，完整見 U3-3）───────
def p2025_2():
    P = dict(fc=280.0, fy=4200.0, fyt=2800.0, bw=60.0, d=76.0, h=85.0, ln=900.0, wu=2.0)
    P['Atop'] = 8 * 8.14
    P['Abot'] = 6 * 8.14
    for k, As in (('neg', P['Atop']), ('pos', P['Abot'])):
        T = As * 1.25 * P['fy']
        a = T / (0.85 * P['fc'] * P['bw'])
        P['a_' + k] = a
        P['Mpr_' + k] = T * (P['d'] - a / 2)
    P['Vseis'] = (P['Mpr_neg'] + P['Mpr_pos']) / P['ln']
    P['Vgrav'] = P['wu'] * 10 * P['ln'] / 2
    P['Ve'] = P['Vseis'] + P['Vgrav']
    P['ratio'] = P['Vseis'] / P['Ve']
    P['Vs'] = P['Ve'] / PHI_V
    P['Av'] = 4 * 1.27
    P['s_req'] = P['Av'] * P['fyt'] * P['d'] / P['Vs']
    P['Vc_if'] = vc_simple(P['fc'], P['bw'], P['d'])
    P['s_if_Vc'] = P['Av'] * P['fyt'] * P['d'] / (P['Ve'] / PHI_V - P['Vc_if'])
    return P


# ── RC-2016-2：剛好 49.6%，Vc 可計入 ─────────────────────────
def p2016_2():
    P = dict(fc=280.0, fy=4200.0, b=35.0, d=63.0, ln=750.0, Atop=19.41, Abot=11.61, wD=2.0, wL=1.0)
    for k, As in (('neg', P['Atop']), ('pos', P['Abot'])):
        T = As * 1.25 * P['fy']
        a = T / (0.85 * P['fc'] * P['b'])
        P['Mpr_' + k] = T * (P['d'] - a / 2)
    P['wu'] = 1.2 * P['wD'] + 1.0 * P['wL']
    P['Vseis'] = (P['Mpr_neg'] + P['Mpr_pos']) / P['ln']
    P['Vgrav'] = P['wu'] * 10 * P['ln'] / 2
    P['Ve'] = P['Vseis'] + P['Vgrav']
    P['ratio'] = P['Vseis'] / P['Ve']
    return P


# ── 自我測驗與內文旁註用到的數字 ─────────────────────────────
def quiz():
    Q = {}
    Q['ch1_Q2_Vc'] = vc_simple(350, 30, 55)
    Q['ch1_Q2_phiVc'] = PHI_V * Q['ch1_Q2_Vc']
    Q['ch1_ratio_053_16'] = 0.53 / unit_check() * 0.53 / 0.53 * (unit_check() / (1 / 6))  # 0.53 ÷ 1/6
    Q['ch1_fc_double_gain'] = math.sqrt(420 / 210) - 1
    Q['ch2_Q2_Vc'] = vc_simple(280, 30, 50, -20000, 30 * 55)
    Q['ch2_rho_cross'] = (0.53 / 2.1) ** 3
    Q['ch3_Q2_Vs'] = 2 * AB['D13'] * 4200 * 50 / 15
    Q['ch3_Q3_2Vc'] = 1.06 * sq(350) * 30 * 55
    Q['avmin_cross_fc'] = (3.5 / 0.2) ** 2
    Q['strut_f2_over_fc_280'] = 2 * 2.65 * sq(280) / 280
    Q['ch4_Q1_Vu'] = 8 * (3.0 - 0.5) * 1000
    Q['ch4_Q2_Vu'] = (8 * 3.0 + 10 * (6 - 0.3) / 6) * 1000
    Q['ch5_Q3_ratio'] = 30 / (30 + 25)
    Q['ch5_mpr_over_phimn'] = 1.25 / 0.9
    Q['ch6_A2p_35x60'] = 2100 ** 2 / 190
    Q['ch6_A2p_20x105'] = 2100 ** 2 / 250
    Q['ch6_Q2_phiTth'] = PHI_V * 0.265 * sq(280) * 2400 ** 2 / 200
    Q['ch7_Q2_Avf'] = 50000 / (0.75 * 1.0 * 4200)
    Q['ch7_vlim_cross_fc'] = 55 / 0.2
    Q['ch8_R5_Ve'] = (60 + 40) / 8 + 3 * 8 / 2
    Q['ch8_R5_ratio'] = ((60 + 40) / 8) / Q['ch8_R5_Ve']
    return Q


def _p(title, d, keys=None):
    print(f'\n== {title}')
    for k, v in d.items():
        if keys and k not in keys:
            continue
        if isinstance(v, float):
            print(f'  {k:12s} = {v:,.4f}')
        elif isinstance(v, dict):
            for kk, vv in v.items():
                print(f'  {k}.{kk} = ' + ', '.join(f'{a}={b:,.2f}' for a, b in vv.items()) if isinstance(vv, dict) else f'  {k}.{kk}={vv}')
        else:
            print(f'  {k:12s} = {v}')


if __name__ == '__main__':
    print('0.53 ↔ 1/6 MPa 換算係數 =', round(unit_check(), 4))
    D = demo(); D.pop('mpa_ratio')
    _p('示範梁 RC-2021-1', D)
    for s, t in ((0, 1), (-1.0, 1), (1.0, 1)):
        print('  mohr σ=', s, 'τ=', t, '→', [round(x, 3) for x in mohr(s, t)], '裂縫角', round(crack_angle(s, t), 1))
    _p('RC-2010-3', p2010_3())
    _p('RC-2014-3', p2014_3())
    _p('RC-2020-2', p2020_2())
    _p('RC-2006-1', p2006_1())
    _p('RC-2023-3', p2023_3())
    _p('RC-2011-4', p2011_4())
    _p('RC-2018-1', p2018_1())
    _p('RC-2017-2', p2017_2())
    _p('RC-2009-3', p2009_3())
    _p('RC-2025-2', p2025_2())
    _p('RC-2016-2', p2016_2())
    _p('自我測驗／旁註', quiz())
