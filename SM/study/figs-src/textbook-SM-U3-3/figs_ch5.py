# -*- coding: utf-8 -*-
"""第 5 章：軟弱夾層三塊法。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig5_1():
    d = ex2006_3()
    W_, H = 900, 430
    sc = 22
    ox, oy = 60, 360          # 夾層高程 = 0
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    o = ''
    # ground: left excavation at y=2 from x=0..8; slope to x=28 at y=12; right flat to x=36
    xl, xt, xr = 8, 28, 36
    o += P([(X(0), Y(2)), (X(xl), Y(2)), (X(xt), Y(12)), (X(xr), Y(12)), (X(xr), Y(-2.5)), (X(0), Y(-2.5))], SOILE, 1.4, fill=SOIL, close=True)
    o += R(X(0), Y(0.18), X(xr) - X(0), 8, '#90a4ae', None)
    o += T(X(1), Y(0) + 26, '軟弱黏土夾層 10 cm（*s*_{u} = 12 kPa）', 14, INK, 'start', 'bold')
    # block outline
    o += P([(X(xl), Y(0)), (X(xl), Y(2)), (X(xt), Y(12)), (X(xt), Y(0))], KEY, 2.2, fill=KEY2, close=True, op=0.85)
    o += L(X(xt), Y(0), X(xt), Y(12), COMP, 2, '6 4')
    o += L(X(xl), Y(0), X(xl), Y(2), TEN, 2, '6 4')
    # tension crack
    zc = d['dry']['zc']
    o += L(X(xt) + 3, Y(12), X(xt) + 3, Y(12 - zc), COMP, 3)
    o += T(X(xt) + 10, Y(12 - zc / 2) + 5, f'裂縫 *z*_{{c}} = {zc:.2f}', 14, COMP, 'start', 'bold')
    # PA
    o += A(X(xt) + 120, Y(4), X(xt) + 8, Y(4), COMP, 3.4, 13)
    o += T(X(xt) + 118, Y(4) - 12, f"*P*_{{A}} = {d['dry']['PA']:.2f}", 15, COMP, 'end', 'bold')
    o += T(X(xt) + 118, Y(4) + 24, '主動楔推', 14, COMP, 'end')
    # PP
    o += A(X(xl) - 90, Y(1), X(xl) - 6, Y(1), TEN, 3.4, 13)
    o += T(X(xl) - 92, Y(1) - 12, f"*P*_{{P}} = {d['dry']['PP']:.2f}", 15, TEN, 'start', 'bold')
    # T
    o += A(X(xt - 4), Y(0) + 18, X(xl + 4), Y(0) + 18, TEN, 3, 12)
    o += T(X(18), Y(-1.6) + 4, f"*T* = *s*_{{u}}*L* = 12 × 20 = {d['dry']['T']:.0f}", 15, TEN, 'middle', 'bold')
    o += dim(X(xt) + 40, Y(0), X(xt) + 40, Y(12), '', INK, 0)
    o += T(X(xt) + 46, Y(8.6), '12 m', 14, INK, 'start')
    o += T(X(xl) - 8, Y(2) - 8, '開挖面', 14, INK, 'end')
    o += T(X(18) - 30, Y(7) + 4, '中間塊', 16, KEY, 'middle', 'bold')
    o += R(60, 30, 190, 130, KEY2, KEY, 1.4, 8)
    o += T(155, 58, '常時（無水）', 15, KEY, 'middle', 'bold')
    o += T(155, 88, '(*T* + *P*_{P}) / *P*_{A}', 15, INK, 'middle')
    o += T(155, 122, f"FS = {d['dry']['FS']:.2f}", 18, KEY, 'middle', 'bold')
    return svg(W_, H, o, 'SM-2006-3 軟弱夾層三塊法')


def fig5_2():
    d = ex2006_3()
    W_, H = 900, 400
    pl = Plot(110, 50, 560, 270, 0, 4, 0, 900)
    o = pl.axes([], [0, 300, 600, 900], '', 'kN/m')
    def stack(x, parts, lab):
        s = ''
        y0 = 0
        for v, c, t in parts:
            s += R(pl.X(x - 0.32), pl.Y(y0 + v), pl.X(x + 0.32) - pl.X(x - 0.32), pl.Y(y0) - pl.Y(y0 + v), c, INK, 1)
            if v > 40:
                s += T(pl.X(x), pl.Y(y0 + v / 2) + 5, t, 14, INK, 'middle', 'bold')
            y0 += v
        s += T(pl.X(x), pl.Y(y0) - 8, f'{y0:.1f}', 15, INK, 'middle', 'bold')
        s += T(pl.X(x), pl.Y(0) + 24, lab, 15, INK, 'middle', 'bold')
        return s
    dr, we = d['dry'], d['wet']
    o += stack(0.5, [(dr['PA'], COMPM, '*P*_{A}')], '常時 推')
    o += stack(1.5, [(dr['T'], TENM, '*T*'), (dr['PP'], TEN2, '*P*_{P}')], '常時 抗')
    o += stack(2.5, [(we['PA'], COMPM, "*P*_{A}′"), (we['PwA'], ACM, '水壓 706.32')], '豪雨 推')
    o += stack(3.5, [(we['T'], TENM, '*T*'), (we['PP'], TEN2, "*P*_{P}′"), (we['PwP'], ACM, '')], '豪雨 抗')
    o += R(700, 70, 190, 160, KEY2, KEY, 1.4, 8)
    o += T(795, 98, f"常時 FS = {dr['FS']:.2f}", 16, KEY, 'middle', 'bold')
    o += T(795, 128, f"豪雨 FS = {we['FS']:.2f}", 16, COMP, 'middle', 'bold')
    o += T(795, 162, '豪雨推力中', 15, INK, 'middle')
    o += T(795, 188, f"水壓佔 {d['water_share'] * 100:.0f}%", 15, AC, 'middle', 'bold')
    return svg(W_, H, o, 'SM-2006-3 常時與豪雨的力帳')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
