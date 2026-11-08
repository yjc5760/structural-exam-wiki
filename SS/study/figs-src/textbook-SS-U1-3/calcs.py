# -*- coding: utf-8 -*-
"""教科書講義 SS-U1-3 梁柱桿件：所有數值（圖與內文共用，先算再寫）。

單位：貫穿範例 SS-2014-4 用 kN、mm、MPa（同考卷）；彎矩輸出 kN·m。
考題數字取自 raw/solutions/SS-2014-4/SS-2014-4.md（2026-11-01 勘誤後版本：雙曲率 Cm = 0.345、B1 取 1.0）。
執行 `python3 calcs.py` 印出全部數值，與內文逐一對照。
"""
import math

PI2 = math.pi ** 2


# ── 通用小工具 ──────────────────────────────────────────────
def amp(a):
    """放大係數 1/(1−α)，α = P/Pe。"""
    return 1.0 / (1.0 - a)


def amp_sec(a):
    """兩端等值彎矩（均勻彎矩）的精確彎矩放大：sec(π√α/2)。"""
    return 1.0 / math.cos(math.pi * math.sqrt(a) / 2)


def series_terms(a, n):
    """幾何級數各項 1, α, α², …（共 n 項）。"""
    return [a ** k for k in range(n)]


def lam_c(KL_r, Fy, E):
    return KL_r / math.pi * math.sqrt(Fy / E)


def Fcr_lrfd(lc, Fy):
    return (0.658 ** (lc ** 2)) * Fy if lc <= 1.5 else 0.877 / lc ** 2 * Fy


# ── 貫穿範例：SS-2014-4  W14×90（A572 Gr.50） ──────────────
W = dict(Fy=350.0, E=200000.0, A=17097.0, Ix=415815194.0, Zx=2572769.0,
         rx=156.0, ry=94.0, L=3750.0, Kx=1.79, Ky=1.0)
LOAD = dict(Pnt=1600.0, Plt=450.0, Mnt_a=110.0, Mnt_b=70.0, Mlt=200.0,
            SumPu=9000.0, H=600.0, drift=5 / 1000)


def ex2014():
    w, q = W, LOAD
    d = {}
    d['Pu'] = q['Pnt'] + q['Plt']                                   # 2050 kN
    d['Pe1'] = PI2 * w['E'] * w['Ix'] / w['L'] ** 2 / 1000          # kN（K=1）
    d['alpha1'] = d['Pu'] / d['Pe1']
    d['amp1'] = amp(d['alpha1'])
    d['PeKx'] = d['Pe1'] / w['Kx'] ** 2                             # 強軸 K=1.79 時（第 4、5 章用）
    # 第 1 章：若兩端等值彎矩 110（單曲率、均勻彎矩）時的一階中點撓度與 Pδ
    M0 = q['Mnt_a']
    d['M0'] = M0
    d['delta0_uniform'] = M0 * 1e6 * w['L'] ** 2 / (8 * w['E'] * w['Ix'])   # mm
    d['Pdelta0'] = d['Pu'] * d['delta0_uniform'] / 1000                     # kN·m
    d['Pdelta0_ratio'] = d['Pdelta0'] / M0
    d['Pdelta0_ratio_formula'] = PI2 / 8 * d['alpha1']                      # = (π²/8)·P/Pe
    d['amp1_sec'] = amp_sec(d['alpha1'])
    # B1（勘誤後：雙曲率）
    d['M1M2'] = q['Mnt_b'] / q['Mnt_a']                                     # +0.636
    d['Cm'] = 0.6 - 0.4 * d['M1M2']
    d['B1_raw'] = d['Cm'] / (1 - d['alpha1'])
    d['B1'] = max(1.0, d['B1_raw'])
    # B2：側移角版
    d['Delta'] = q['drift'] * w['L']                                        # 18.75 mm
    d['SumPDelta'] = q['SumPu'] * d['Delta'] / 1000                         # kN·m
    d['SumHL'] = q['H'] * w['L'] / 1000                                     # kN·m
    d['alpha2'] = d['SumPDelta'] / d['SumHL']                               # 0.075
    d['B2'] = amp(d['alpha2'])
    d['SumPeK_equiv'] = q['H'] / q['drift']                                 # 120000 kN
    d['Mux_a'] = d['B1'] * q['Mnt_a'] + d['B2'] * q['Mlt']
    d['Mux_b'] = d['B1'] * q['Mnt_b'] + d['B2'] * q['Mlt']
    d['Mux'] = max(d['Mux_a'], d['Mux_b'])
    # 容量（第 7、8 章）
    d['KLr_x'] = w['Kx'] * w['L'] / w['rx']
    d['KLr_y'] = w['Ky'] * w['L'] / w['ry']
    d['KLr'] = max(d['KLr_x'], d['KLr_y'])
    d['lc'] = lam_c(d['KLr'], w['Fy'], w['E'])
    d['Fcr'] = Fcr_lrfd(d['lc'], w['Fy'])
    d['phiPn'] = 0.85 * d['Fcr'] * w['A'] / 1000
    d['phiMn'] = 0.9 * w['Fy'] * w['Zx'] / 1e6
    d['Pu_ratio'] = d['Pu'] / d['phiPn']
    d['H1'] = d['Pu_ratio'] + 8 / 9 * d['Mux'] / d['phiMn']
    # ASD 對照（第 2 章）：同一支柱強軸 KL/r 的 Fe 與 F'e
    d['Fe_x'] = PI2 * w['E'] / d['KLr_x'] ** 2
    d['Fpe_x'] = 12 * PI2 * w['E'] / (23 * d['KLr_x'] ** 2)
    # 第 1 章：Pe1 = Ag·Fy/λc²（K=1、強軸）等價捷徑自我檢查
    lc1 = lam_c(w['L'] / w['rx'], w['Fy'], w['E'])
    d['lc1_x'] = lc1
    d['Pe1_via_lc'] = w['A'] * w['Fy'] / lc1 ** 2 / 1000
    return d



# ── 第 3 章：Cm、B1 ───────────────────────────────────────
def Mmax_exact(r, a, n=400):
    """兩端彎矩 M2（=1）與 M1 = r·M2（本書符號：單曲率 r<0）、軸力比 a = P/Pe 時，
    桿內二階彎矩的最大絕對值（解 M'' + k²M = 0，k L = π√a）。"""
    kL = math.pi * math.sqrt(a)
    A = 1.0
    B = (-r - math.cos(kL)) / math.sin(kL)
    return max(abs(A * math.cos(kL * i / n) + B * math.sin(kL * i / n)) for i in range(n + 1))


def Cm_exact(r, a):
    """等值均勻彎矩係數的精確值：讓 Cm/(1−a) 等於真正的最大彎矩（÷M2）。"""
    return Mmax_exact(r, a) * (1 - a)


def Cm_code(r):
    return 0.6 - 0.4 * r


def B1_tw(r, a):
    """台灣極限設計法規範 (8.2-3)。"""
    return 0.64 / (1 - a) * (1 - r) + 0.32 * r


def B1_aisc(r, a):
    return Cm_code(r) / (1 - a)


# SS-2020-3：H400×400×12×22，tf、cm
EX2020 = dict(Pu=1.6 * 150, E=2100.0, Ix=67452.0, Iy=23472.0, L=500.0, rx=-1.0, ry=-0.5, Mux0=1.6 * 6 * 100)


def ex2020():
    e = EX2020; d = {}
    d['Pe1x'] = PI2 * e['E'] * e['Ix'] / e['L'] ** 2
    d['Pe1y'] = PI2 * e['E'] * e['Iy'] / e['L'] ** 2
    d['ax'] = e['Pu'] / d['Pe1x']; d['ay'] = e['Pu'] / d['Pe1y']
    d['B1x_tw'] = B1_tw(e['rx'], d['ax']); d['B1y_tw'] = B1_tw(e['ry'], d['ay'])
    d['B1x_aisc'] = B1_aisc(e['rx'], d['ax']); d['B1y_aisc'] = B1_aisc(e['ry'], d['ay'])
    d['Cmx'] = Cm_code(e['rx']); d['Cmy'] = Cm_code(e['ry'])
    d['B1x'] = max(1, d['B1x_tw']); d['B1y'] = max(1, d['B1y_tw'])
    d['Mux'] = d['B1x'] * e['Mux0']
    d['Cmx_exact'] = Cm_exact(e['rx'], d['ax']); d['Cmy_exact'] = Cm_exact(e['ry'], d['ay'])
    d['B1x_exact'] = Mmax_exact(e['rx'], d['ax']); d['B1y_exact'] = Mmax_exact(e['ry'], d['ay'])
    return d


# SS-2003-4（ASD，W12×170，tf、cm）
EX2003 = dict(P=182.0, A=322.58, Sx=3850.96, Sy=1348.66, rx=14.58, ry=8.18, L=370.0, Fy=2.5, E=2100.0, Mx=2768.0, My=830.0, r=+1.0)


def ex2003():
    e = EX2003; d = {}
    d['fa'] = e['P'] / e['A']; d['fbx'] = e['Mx'] / e['Sx']; d['fby'] = e['My'] / e['Sy']
    d['Cm'] = Cm_code(e['r'])
    d['Fpex'] = 12 * PI2 * e['E'] / (23 * (e['L'] / e['rx']) ** 2)
    d['Fpey'] = 12 * PI2 * e['E'] / (23 * (e['L'] / e['ry']) ** 2)
    d['ampx'] = 1 / (1 - d['fa'] / d['Fpex']); d['ampy'] = 1 / (1 - d['fa'] / d['Fpey'])
    d['Cm_amp_x'] = d['Cm'] * d['ampx']; d['Cm_amp_y'] = d['Cm'] * d['ampy']
    return d


# ── 第 4 章：B2、靠桿 ─────────────────────────────────────
def ex_leaning():
    """以 SS-2014-4 的樓層勁度（ΣPe,story = 120,000 kN）示範：若只算抗側力柱的一半載重。"""
    d = ex2014()
    S = d['SumPeK_equiv']
    full, half = LOAD['SumPu'], LOAD['SumPu'] / 2
    return dict(S=S, B2_full=amp(full / S), B2_half=amp(half / S))


def ex2014_wrong():
    d = ex2014(); q = LOAD
    return dict(sum_then_amp=d['B2'] * (q['Mnt_a'] + q['Mlt']),
                B1_raw_used=d['B1_raw'] * q['Mnt_a'] + d['B2'] * q['Mlt'],
                no_B2=d['B1'] * q['Mnt_a'] + q['Mlt'])


# ── 第 5 章：對位圖 ───────────────────────────────────────
def _bisect(f, a, b, n=200):
    fa = f(a)
    for _ in range(n):
        m = (a + b) / 2; fm = f(m)
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return (a + b) / 2


def K_sway(GA, GB):
    """有側移對位圖的方程式：(GAGBu² − 36)/(6(GA+GB)) = u/tan u，u = π/K ∈ (0, π/2]。"""
    if GA + GB == 0:
        return 1.0
    f = lambda u: (GA * GB * u * u - 36) / (6 * (GA + GB)) - u / math.tan(u)
    return math.pi / _bisect(f, 1e-6, math.pi / 2 - 1e-9) if f(math.pi / 2 - 1e-9) > 0 else math.pi / _bisect(f, 1e-6, math.pi - 1e-6)


def K_braced(GA, GB):
    """無側移對位圖的方程式 (GAGB/4)u² + (GA+GB)/2·(1 − u/tan u) + 2tan(u/2)/u = 1，u = π/K ∈ (π, 2π)。
    兩邊乘 sin u·cos(u/2) 去掉奇點後再找根。"""
    def g(u):
        return ((GA * GB / 4 * u * u - 1) * math.sin(u) * math.cos(u / 2)
                + (GA + GB) / 2 * (math.sin(u) - u * math.cos(u)) * math.cos(u / 2)
                + 2 * math.sin(u / 2) * math.sin(u) / u)
    lo, hi = math.pi + 1e-4, 2 * math.pi - 1e-4
    xs = [lo + (hi - lo) * i / 4000 for i in range(4001)]
    for x0, x1 in zip(xs, xs[1:]):
        if (g(x0) < 0) != (g(x1) < 0):
            return math.pi / _bisect(g, x0, x1)
    return 0.5


def K_sway_JM(GA, GB):
    return math.sqrt((1.6 * GA * GB + 4 * (GA + GB) + 7.5) / (GA + GB + 7.5))


# 梁遠端條件 → 梁對近端的轉動勁度係數（× EI/L）
FAR_END = {'sway_assumed': 6, 'sway_far_pin': 3, 'sway_far_fixed': 4,
           'braced_assumed': 2, 'braced_far_pin': 3, 'braced_far_fixed': 4}


def ex2013():
    d = {}
    d['G_B_raw'] = 1 / (2 / 1.5)                  # (I/L) / (2·I/1.5L)
    d['G_B'] = d['G_B_raw'] / 0.5                 # 梁遠端滾支 ×0.5
    d['G_C'] = 10.0
    d['K'] = K_sway(d['G_B'], d['G_C'])
    d['K_JM'] = K_sway_JM(d['G_B'], d['G_C'])
    d['K_raw'] = K_sway(d['G_B_raw'], d['G_C'])
    d['PeK_coef'] = PI2 / d['K'] ** 2             # × EI/L²
    d['PeK_coef_raw'] = PI2 / d['K_raw'] ** 2
    d['B2_coef'] = 1 / d['PeK_coef']              # B2 = 1/(1 − coef·PL²/EI)
    return d


def lemessurier(Pe, Pi, SumP, SumPeK):
    return math.sqrt(Pe / Pi * SumP / SumPeK)


# ── 下冊：容量與互制 ─────────────────────────────────────
def H1(pr, mx, my=0.0):
    """LRFD H1：pr = Pu/φcPn，mx、my = Mu/φbMn。回傳（使用的分支, 值）。"""
    if pr >= 0.2:
        return 'a', pr + 8 / 9 * (mx + my)
    return 'b', pr / 2 + (mx + my)


def H1_curve_M(pr):
    """H1 = 1 時，給定 pr 的容許 M 比（單軸）。"""
    return 9 / 8 * (1 - pr) if pr >= 0.2 else 1 - pr / 2


def Mpc_ratio_strong(p):
    """W 型鋼強軸全塑性彎矩受軸力折減（AISC 塑性設計近似）：1.18(1−P/Py) ≤ 1。"""
    return min(1.0, 1.18 * (1 - p))


def Fa_asd(slr, Fy, E):
    Cc = math.sqrt(2 * PI2 * E / Fy)
    if slr <= Cc:
        x = slr / Cc
        return (1 - x * x / 2) * Fy / (5 / 3 + 3 * x / 8 - x ** 3 / 8)
    return 12 * PI2 * E / (23 * slr ** 2)


W14_d = 356.0   # mm，W14×90 深度（AISC 表 14.02 in）


def ex2014_cap():
    d = ex2014(); w = W
    c = {}
    c['Sx'] = w['Ix'] / (W14_d / 2)
    c['ZS'] = w['Zx'] / c['Sx']
    c['Fbx_equiv'] = 0.9 * c['ZS'] / 1.5          # φb·(Z/S)/1.5 ≈ 0.66
    c['Fa'] = Fa_asd(d['KLr'], w['Fy'], w['E'])
    c['phiFcr'] = 0.85 * d['Fcr']
    c['ratio_col'] = c['phiFcr'] / c['Fa']
    c['branch'], c['H1'] = H1(d['Pu_ratio'], d['Mux'] / d['phiMn'])
    c['M_ratio'] = d['Mux'] / d['phiMn']
    c['Mux_allow'] = H1_curve_M(d['Pu_ratio']) * d['phiMn']   # 同 Pu 下可承受的 Mux
    return c


def ex2020_H1():
    e = EX2020; d = ex2020()
    A = 218.72; Zx = 3706.6; Zy = 1772.8; Sy = 1173.6; Fy = 2.5; E = 2100.0
    ry = 10.36; KyL = 1.2 * 500
    r = {}
    r['lc'] = KyL / ry / math.pi * math.sqrt(Fy / E)
    r['Fcr'] = Fcr_lrfd(r['lc'], Fy)
    r['phiPn'] = 0.85 * r['Fcr'] * A
    r['pr'] = e['Pu'] / r['phiPn']
    r['phiMnx'] = 0.9 * Fy * Zx
    r['Mny_Z'] = Fy * Zy; r['Mny_cap'] = 1.5 * Fy * Sy
    r['phiMny'] = 0.9 * min(r['Mny_Z'], r['Mny_cap'])
    r['mx'] = d['Mux'] / r['phiMnx']
    r['my_allow'] = (1 - r['pr']) * 9 / 8 - r['mx']
    r['Muy'] = r['my_allow'] * r['phiMny']            # tf·cm
    r['Mwy'] = r['Muy'] / 1.6 / 100                    # tf·m（B1y = 1.0）
    return r


EX2012 = dict(Pu=800.0, A=12903.0, rx=153.0, ry=62.0, KL=4500.0, Fy=350.0, E=200000.0, Zx=1884512.0, Zy=604683.0, Mux=100.0, Muy=50.0)


def ex2012():
    e = EX2012; r = {}
    r['KLr'] = e['KL'] / min(e['rx'], e['ry'])
    r['lc'] = lam_c(r['KLr'], e['Fy'], e['E'])
    r['Fcr'] = Fcr_lrfd(r['lc'], e['Fy'])
    r['phiPn'] = 0.85 * r['Fcr'] * e['A'] / 1000
    r['phiMnx'] = 0.9 * e['Fy'] * e['Zx'] / 1e6
    r['phiMny'] = 0.9 * e['Fy'] * e['Zy'] / 1e6
    r['pr'] = e['Pu'] / r['phiPn']
    r['mx'] = e['Mux'] / r['phiMnx']; r['my'] = e['Muy'] / r['phiMny']
    r['branch'], r['H1'] = H1(r['pr'], r['mx'], r['my'])
    return r


EX2022 = dict(Pu=1119.0, M2=179.0, M3=19.4, bo=80.0, t=3.2, Fy=3.3, E=2040.0, KLr=30.54)


def ex2022():
    e = EX2022; r = {}
    bi = e['bo'] - 2 * e['t']
    r['A'] = e['bo'] ** 2 - bi ** 2
    r['Z'] = (e['bo'] ** 3 - bi ** 3) / 4
    r['lc'] = lam_c(e['KLr'], e['Fy'], e['E'])
    r['Fcr'] = Fcr_lrfd(r['lc'], e['Fy'])
    r['phiPn'] = 0.85 * r['Fcr'] * r['A']
    r['phiMn'] = 0.9 * e['Fy'] * r['Z'] / 100        # tf·m
    r['pr'] = e['Pu'] / r['phiPn']
    r['m2'] = e['M2'] / r['phiMn']; r['m3'] = e['M3'] / r['phiMn']
    r['branch'], r['H1'] = H1(r['pr'], r['m2'], r['m3'])
    return r


EX2019 = dict(P=12.0, A=83.4, Sx=1170.0, ry=4.56, rx=None, L=600.0, Fy=2.5, E=2040.0, MBC=400.0, MAB=800.0, Fbx=1.5, Fpex=8.24)


def ex2019():
    e = EX2019; r = {}
    r['fa'] = e['P'] / e['A']
    r['Fa'] = Fa_asd(e['L'] / e['ry'], e['Fy'], e['E'])
    r['faFa'] = r['fa'] / r['Fa']
    r['fbx'] = e['MBC'] / e['Sx']
    r['Cm'] = 0.6
    r['stab'] = r['faFa'] + r['Cm'] * r['fbx'] / ((1 - r['fa'] / e['Fpex']) * e['Fbx'])
    r['strg'] = r['fa'] / (0.6 * e['Fy']) + r['fbx'] / e['Fbx']
    r['AB'] = e['MAB'] / e['Sx'] / e['Fbx']
    r['simple'] = r['faFa'] + r['fbx'] / e['Fbx']    # 若誤用 0.15 簡化式
    return r


# 第 10 章
def tau_b(p):
    """直接分析法勁度折減 τb（p = αPr/Py）。"""
    return 1.0 if p <= 0.5 else 4 * p * (1 - p)


def crc_tangent(p):
    """CRC 拋物線柱曲線（殘留應力 0.5Fy）推出的 Et/E：Fcr/Fy = p 時 = 4p(1−p)。"""
    return 4 * p * (1 - p)


def alpha_asd(LD):
    """(1.2D + 1.6L)/(D + L)，LD = L/D。"""
    return (1.2 + 1.6 * LD) / (1 + LD)


# 第 2 章：放大曲線上標出的特定 α
ALPHA_MARKS = [0.1, 0.3, 0.5, 0.8]

if __name__ == '__main__':
    d = ex2014()
    for k, v in d.items():
        print(f'{k:>22s} = {v:.5g}' if isinstance(v, float) else f'{k} = {v}')
    print('--- 放大係數表')
    for a in [0.035, 0.075] + ALPHA_MARKS:
        print(f'  α={a:<6} 1/(1-α)={amp(a):.3f}   sec={amp_sec(a):.3f}   誤差={(amp_sec(a)/amp(a)-1)*100:.1f}%')
    print('--- ex2020', {k: round(v, 4) for k, v in ex2020().items()})
    print('--- ex2003', {k: round(v, 4) for k, v in ex2003().items()})
    print('--- leaning', {k: round(v, 4) for k, v in ex_leaning().items()})
    print('--- 2014 wrong', {k: round(v, 2) for k, v in ex2014_wrong().items()})
    print('--- ex2013', {k: round(v, 4) for k, v in ex2013().items()})
    print('--- Cm exact (a=0.1/0.3) vs code')
    for r in (-1, -0.5, 0, 0.5, 1):
        print(f'  r={r:+.1f}  code={Cm_code(r):.3f}  a=.1 {Cm_exact(r,.1):.3f}  a=.3 {Cm_exact(r,.3):.3f}  tw(a=0)={B1_tw(r,0):.3f}')
    print('--- K checks', 'sway(0,0)', round(K_sway(0.001,0.001),3), 'sway(1,1)', round(K_sway(1,1),3), 'sway(10,10)', round(K_sway(10,10),3),
          'braced(.01,.01)', round(K_braced(.01,.01),3), 'braced(1,1)', round(K_braced(1,1),3), 'braced(10,10)', round(K_braced(10,10),3), 'sway(10,1)', round(K_sway(10,1),3))
    for nm, fn in (('cap2014', ex2014_cap), ('H1_2020', ex2020_H1), ('ex2012', ex2012), ('ex2022', ex2022), ('ex2019', ex2019)):
        print('---', nm, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in fn().items()})
    print('--- alpha_asd', [round(alpha_asd(x), 3) for x in (0, 1, 3, 10, 1e9)])
    print('--- 級數（α=0.5）前 6 項累計')
    s = 0
    for k, t in enumerate(series_terms(0.5, 6)):
        s += t
        print(f'  第 {k} 項 {t:.4f}  累計 {s:.4f}')
