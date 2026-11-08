# -*- coding: utf-8 -*-
"""第 6 章：ASD 容許撓曲應力（H700）、ASD vs LRFD÷1.5。"""
from plot import *  # noqa
import math
import calcs

D = calcs.example()
A6 = calcs.ex_asd()
Fy = D['Fy']


def fb(Lcm):
    return calcs.asd_fb(Lcm, Fy, A6['rT'], A6['d_Af'], 1.0, True, A6['Lc'])


def f_rt(Lcm):
    lam = Lcm / A6['rT']
    if lam <= A6['hi']:
        return (2 / 3 - Fy * lam ** 2 / 107600) * Fy
    return 12000 / lam ** 2


def f_tor(Lcm):
    return 840 / (Lcm * A6['d_Af'])


def fig6_1():
    W, H = 900, 440
    pl = Plot(100, 50, 570, 300, 0, 10, 0, 0.75)
    o = pl.axes([0, A6['Lc'] / 100, A6['Lu'] / 100, 5, 8, 10], [0, 0.2, 0.4, 0.6, 0.66], '*L*_{b}（m）', '*F*_{b}/*F*_{y}', size=14,
                xfmt=lambda v: f'{v:.2f}' if v not in (0, 5, 8, 10) else f(v), yfmt=lambda v: f'{v:.2f}' if v else '0')
    o += pl.curve(lambda L: min(0.75, f_rt(L * 100) / Fy), 1.5, 10, AC, 2, dash='8 5')
    o += pl.curve(lambda L: f_tor(L * 100) / Fy, 840 / (0.75 * Fy * A6['d_Af']) / 100, 10, WARN, 2, dash='3 4')
    o += pl.curve(lambda L: fb(max(L, 0.01) * 100) / Fy, 0.02, 10, KEY, 3.2)
    o += pl.vline(A6['Lc'] / 100, 0, 0.66, MUT, 1.2) + pl.vline(A6['Lu'] / 100, 0, 0.6, MUT, 1.2)
    o += T(pl.X(1.05), pl.Y(0.66) - 10, '0.66*F*_{y}', 15, KEY, 'middle', 'bold')
    o += T(pl.X(2.5), pl.Y(0.6) - 10, '0.6', 14, KEY, 'middle', 'bold')
    o += T(pl.X(6.9), pl.Y(0.47), '*r*_{T} 式（柱：拋物線→Euler）', 14, AC, 'start', 'bold')
    o += T(pl.X(5.6), pl.Y(0.10), '840/(*Ld*/*A*_{f})（扭轉）', 14, WARN, 'start', 'bold')
    o += pl.dot(5, fb(500) / Fy, KEY, 6)
    o += T(pl.X(5) + 8, pl.Y(fb(500) / Fy) - 12, f'*L*_{{b}}=5 m：{fb(500):.3f} tf/cm²', 14, KEY, 'start', 'bold')
    o += box(690, 90, 200, 150, '兩條路「取大」', ['*r*_{T} 式＝翼板當柱', '840 式＝聖維南扭轉', '', 'ASD 取大值', 'LRFD 平方相加'], KEY2, KEY, 16, 14)
    o += T(pl.X(5), pl.Y(0) + 46, f'H700×200，*C*_{{b}}=1：*L*_{{c}}={A6["Lc"]:.0f} cm、*L*_{{u}}={A6["Lu"]:.0f} cm、*r*_{{T}}={A6["rT"]:.2f} cm', 14, MUT, 'middle')
    return svg(W, H, o, 'ASD 容許撓曲應力')


def fig6_2():
    W, H = 900, 400
    pl = Plot(100, 40, 570, 280, 0, 10, 0, 110)
    o = pl.axes([0, 2, 4, 5, 6, 8, 10], [0, 20, 40, 60, 80, 100], '*L*_{b}（m）', '容許彎矩（tf·m）', size=14)
    lrfd = lambda L: 0.9 * calcs.mn_ltb(L * 100, D['Mp'], D['Mr'], D['Lp'], D['Lr'], D['Sx'], D['X1'], D['X2'], D['ry']) / 1.5 / 100
    asd = lambda L: fb(max(L, 0.01) * 100) * D['Sx'] / 100
    o += pl.curve(lrfd, 0, 10, COMP, 3)
    o += pl.curve(asd, 0.01, 10, WARN, 3, dash='9 5')
    o += T(pl.X(7.6), pl.Y(lrfd(7.6)) - 16, 'LRFD φ*M*_{n} ÷ 1.5', 15, COMP, 'start', 'bold')
    o += T(pl.X(5.6), pl.Y(asd(5.6)) + 26, 'ASD *F*_{b}*S*_{x}', 15, WARN, 'start', 'bold')
    for L in (1.0, 5.0):
        r = asd(L) / lrfd(L)
        o += pl.dot(L, lrfd(L), COMP, 5) + pl.dot(L, asd(L), WARN, 5)
        o += T(pl.X(0.3) if L < 2 else pl.X(L) - 10, pl.Y(72) if L < 2 else pl.Y(asd(L)) + 26, f'ASD/LRFD = {r:.2f}', 14, KEY, 'start' if L < 2 else 'end', 'bold')
    o += box(690, 60, 200, 150, '÷1.5 只在短梁成立', ['塑性區：比 ≈ 1.0', 'LTB 區：ASD 偏保守', '（兩條路取大', '　vs 平方相加）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'ASD 與 LRFD 換算')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
