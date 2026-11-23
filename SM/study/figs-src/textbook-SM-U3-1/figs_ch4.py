# -*- coding: utf-8 -*-
"""第 4 章：水位上升（2004-3）、兩層土＋水（2010-2）、裂縫＋水（2015-2）的土壓力圖與合力。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'


def _diagram(o, x0, w, top, bot, Hm, smax, polys, ticks, ybar=None, P=None, wall=True):
    Y = lambda z: top + z / Hm * (bot - top)
    X = lambda s: x0 + s / smax * w
    if wall:
        o += R(x0 - 22, top, 22, bot - top, STEEL3, INK, 1.4)
    for t in ticks:
        o += L(X(t), top, X(t), bot, GRID, 1) + T(X(t), top - 10, f'{t:g}', 14, MUT, 'middle')
    o += A(x0, top, X(smax) + 14, top, INK, 1.4, 8)
    for pts, c, fill in polys:
        o += P_(pts, X, Y, c, fill)
    o += L(x0, top, x0, bot, INK, 2)
    if ybar is not None:
        zb = Hm - ybar
        o += A(X(smax * 0.92), Y(zb), x0 + 3, Y(zb), KEY, 3.4, 13)
        o += T(X(smax * 0.92) + 6, Y(zb) + 5, f'*P* = {P:.2f}', 15, KEY, 'start', 'bold')
        o += T(X(smax * 0.92) + 6, Y(zb) + 25, f'*ȳ* = {ybar:.3f} m', 15, KEY, 'start', 'bold')
    return o, X, Y


def P_(pts, X, Y, c, fill):
    return P([(X(s), Y(z)) for s, z in pts], c, 1.6, fill=fill, close=True)


def fig4_1():
    d = ex2004_3()
    W_, H = 900, 420
    Hm, x = d['H'], d['x']
    k, g = d['Ka'], d['g']
    zw = Hm - x
    sw = k * g * zw
    sb = sw + k * (g - GW) * x
    u = GW * x
    top, bot = 60, 360
    polys = [([(0, 0), (sw, zw), (0, zw)], TEN, TENM),
             ([(0, zw), (sw, zw), (sb, Hm), (0, Hm)], TEN, TEN2),
             ([(sb, Hm), (sw, zw), (sw + 0.001, zw), (sb + u, Hm)], AC, AC2)]
    o, X, Y = _diagram('', 90, 260, top, bot, Hm, 70, polys, [0, 20, 40, 60])
    o += L(60, Y(zw), 380, Y(zw), AC, 1.6, '6 4')
    o += T(380, Y(zw) - 6, f'水位 *x* = {x:.2f} m', 14, AC, 'end', 'bold')
    o += T(X(sb + u) + 6, Y(Hm), f'{sb + u:.1f}', 14, AC, 'start', 'bold')
    o += T(X(sb) - 4, Y(Hm) + 20, f'土 {sb:.1f}', 14, TEN, 'end', 'bold')
    o += T(220, 30, '(a) 水位到 *x* 時的壓力圖', 16, INK, 'middle', 'bold')
    pl = Plot(520, 60, 330, 280, 0, 6, 80, 220)
    o += T(685, 30, '(b) 總推力隨水位上升', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 1, 2, 3, 4, 5, 6], [80, 120, 160, 200], '*x*', '*P*')
    o += pl.curve(lambda xx: P_of_x(xx, d), 0, 6, KEY, 3)
    o += pl.hline(d['R'], 0, 6, COMP, 1.8, '6 4')
    o += T(pl.X(0.1), pl.Y(d['R']) - 8, '可抵抗 146', 14, COMP, 'start', 'bold')
    o += pl.dot(x, d['R'], KEY, 6)
    o += T(pl.X(x) + 8, pl.Y(d['R']) + 22, f'*x* = {x:.2f} m', 15, KEY, 'start', 'bold')
    o += pl.dot(0, d['P0'], AC, 5)
    o += T(pl.X(0) + 8, pl.Y(d['P0']) - 8, f"乾 {d['P0']:.2f}", 14, AC, 'start', 'bold')
    return svg(W_, H, o, 'SM-2004-3 水位上升與推力')


def fig4_2():
    d = ex2010_2()
    W_, H = 900, 440
    top, bot, Hm = 60, 380, 8.0
    s2, s4a, u4, s4b, s8 = d['s2'], d['s4a'], d['u4'], d['s4b'], d['s8']
    polys = [([(0, 0), (s2, 2), (0, 2)], TEN, TENM),
             ([(0, 2), (s2, 2), (s2, 4), (0, 4)], TEN, TEN2),
             ([(s2, 2), (s4a, 4), (s2, 4)], TEN, TENM),
             ([(s4a, 4), (s2, 2), (s4a + u4, 4)], AC, AC2),
             ([(0, 4), (s4b, 4), (s4b, 8), (0, 8)], WARN, WARN2),
             ([(s4b, 4), (s8, 8), (s4b, 8)], WARN, '#ffe0b2')]
    o, X, Y = _diagram('', 110, 420, top, bot, Hm, 90, polys, [0, 20, 40, 60, 80], d['ybar'], d['P'])
    for z in (0, 2, 4, 8):
        o += T(80, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += T(40, bot + 30, '深度 *z*（m）', 14, INK, 'start')
    o += L(80, Y(2), X(90), Y(2), AC, 1.4, '6 4')
    o += T(X(90), Y(2) - 6, '水位', 14, AC, 'end', 'bold')
    o += T(X(s4a + u4) + 6, Y(4) - 4, f'{s4a + u4:.2f}', 14, AC, 'start', 'bold')
    o += T(X(s4b) + 6, Y(4) + 18, f'{s4b:.2f}', 14, WARN, 'start', 'bold')
    o += T(X(s8) - 4, Y(8) + 20, f'{s8:.2f}', 14, WARN, 'end', 'bold')
    o += T(X(s2) + 6, Y(2) - 4, f'{s2:.2f}', 14, TEN, 'start', 'bold')
    o += T(X(45), Y(3.2), '砂（有效）＋水', 14, INK, 'start')
    o += T(X(20), Y(6.6), '黏土 φ = 0（總應力）', 14, INK, 'start')
    o += R(660, 220, 230, 110, KEY2, KEY, 1.4, 8)
    o += T(775, 248, '6 塊 → 對牆底取矩', 15, KEY, 'middle', 'bold')
    o += T(775, 278, f"Σ*P*_{{i}}*y*_{{i}} = {d['M']:.2f}", 15, INK, 'middle')
    o += T(775, 306, f"*H*/3 = 2.667（不適用）", 14, MUT, 'middle')
    return svg(W_, H, o, 'SM-2010-2 主動土壓力分布與合力')


def fig4_3():
    d = ex2015_2()
    W_, H = 900, 440
    top, bot, Hm = 60, 380, 8.0
    zc = d['zc']
    polys = [([(0, zc), (d['s4a'], 4), (0, 4)], TEN, TENM),
             ([(0, 4), (d['s4b'], 4), (d['s4b'], 8), (0, 8)], TEN, TEN2),
             ([(d['s4b'], 4), (d['s8'], 8), (d['s4b'], 8)], TEN, TENM),
             ([(d['s8'], 8), (d['s4b'], 4), (d['s4b'] + 0.001, 4), (d['s8'] + d['u8'], 8)], AC, AC2)]
    o, X, Y = _diagram('', 110, 420, top, bot, Hm, 90, polys, [0, 20, 40, 60, 80], d['ybar'], d['P'])
    for z in (0, 4, 8):
        o += T(80, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += T(80, Y(zc) + 5, f'{zc:.2f}', 14, COMP, 'end', 'bold')
    o += T(40, bot + 30, '深度 *z*（m）', 14, INK, 'start')
    o += P([(X(0), Y(0)), (X(0), Y(zc))], COMP, 4)
    o += T(X(3), Y(zc / 2), '張力裂縫：土壓 0', 14, COMP, 'start', 'bold')
    o += L(80, Y(4), X(90), Y(4), AC, 1.4, '6 4')
    o += T(X(90), Y(4) - 6, '水位＝層界', 14, AC, 'end', 'bold')
    o += T(X(d['s4a']) + 6, Y(4) - 4, f"{d['s4a']:.2f}", 14, TEN, 'start', 'bold')
    o += T(X(d['s4b']) + 6, Y(4) - 6, f"{d['s4b']:.2f}", 14, TEN, 'start', 'bold')
    o += T(X(d['s8'] + d['u8']) + 6, Y(8), f"{d['s8']:.2f} + {d['u8']:.2f}", 14, AC, 'start', 'bold')
    o += T(X(2), Y(6), '砂（有效）', 14, INK, 'start')
    return svg(W_, H, o, 'SM-2015-2 主動土壓力分布與合力')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
