# -*- coding: utf-8 -*-
"""第 2 章：工址設計譜四段。"""
from sdfig import *  # noqa
from calcs import SaD, SITE
import math


def fig2_1():
    W, H = 900, 380
    SDS, SD1, T0 = SITE['SDS'], SITE['SD1'], SITE['T0']
    pl = Plot(90, 40, 560, 280, 0, 2.5, 0, 0.95)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5], [0, 0.32, 0.8], '*T* (s)', '*S*_{aD}', yfmt=lambda v: f'{v:.2f}')
    xs = [0, 0.2 * T0, T0, 2.5 * T0, 2.5]
    cols = [TEN, AC, KEY, MUT]
    for a, b, c in zip(xs[:-1], xs[1:], cols):
        o += pl.curve(SaD, a, b, c, 3.4, n=200)
    for x in xs[1:4]:
        o += pl.vline(x, 0, SaD(x), MUT, 1.1)
        o += pl.dot(x, SaD(x), COMP, 5)
    o += T(pl.X(0.03), pl.Y(0.42) + 30, '①', 16, TEN, 'start', 'bold')
    o += T(pl.X(0.35), pl.Y(0.86), '② 平台 *S*_{DS}', 15, AC, 'middle', 'bold')
    o += T(pl.X(1.0), pl.Y(0.55), '③ *S*_{D1}/*T*', 15, KEY, 'start', 'bold')
    o += T(pl.X(1.9), pl.Y(0.38), '④ 0.4*S*_{DS}', 15, MUT, 'middle', 'bold')
    o += T(pl.X(0.2 * T0), pl.Y(0) + 38, '0.2*T*_{0}', 14, MUT, 'middle')
    o += T(pl.X(T0), pl.Y(0) + 38, '*T*_{0}^{D}', 14, MUT, 'middle')
    o += T(pl.X(2.5 * T0), pl.Y(0) + 38, '2.5*T*_{0}', 14, MUT, 'middle')
    o += box(665, 40, 225, 300, '三個接點都要接得起來', ['*T*_{0}^{D} = *S*_{D1}/*S*_{DS}', '0.2*T*_{0}：0.4 + 0.6 = 1 ✔', '*T*_{0}：*S*_{D1}/*T*_{0} = *S*_{DS} ✔', '2.5*T*_{0}：*S*_{DS}/2.5', '= 0.4*S*_{DS} ✔', f'例 *S*_{{DS}} = {SDS}、*S*_{{D1}} = {SD1}', f'*T*_{{0}} = {T0:.4f} s', '寫錯的式子在接點', '一定接不起來'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '工址設計譜')


ALL = {'fig2_1': fig2_1}
