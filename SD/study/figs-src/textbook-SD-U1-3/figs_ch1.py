# -*- coding: utf-8 -*-
"""第 1 章：SDOF 計算流程、加質量反推、反應譜換算鏈。"""
from sdfig import *  # noqa
from calcs import Q2012, PI, G
import math


def fig1_1():
    W, H = 900, 340
    m0, dm = Q2012['m'], Q2012['dm']
    pl = Plot(90, 40, 460, 250, 0, 7500, 0, 2.2)
    o = pl.axes([0, 2000, 4000, 6000], [0, 0.5, 1, 1.5, 2], '*m* (kg)', '*T*² (s²)', xfmt=lambda t: f'{t:.0f}')
    k = Q2012['k']
    o += pl.curve(lambda m: 4 * PI ** 2 * m / k, 0, 7500, AC, 2.6)
    o += pl.dot(m0, 1.44, KEY, 6) + pl.dot(m0 + dm, 1.96, COMP, 6)
    o += T(pl.X(m0) - 10, pl.Y(1.44) - 10, '*T* = 1.2 s', 15, KEY, 'end', 'bold')
    o += T(pl.X(m0 + dm) - 10, pl.Y(1.96) - 10, '加 1806 kg：*T* = 1.4 s', 15, COMP, 'end', 'bold')
    o += pl.vline(m0, 0, 1.44, KEY) + pl.vline(m0 + dm, 0, 1.96, COMP)
    o += box(600, 50, 290, 240, '*T*² = 4π²*m*/*k*：對 *m* 是直線', ['(1.4/1.2)² = (*m* + 1806)/*m*', f'*m* = 1806/{Q2012["ratio"]-1:.4f}', f'= {Q2012["m"]:.0f} kg', f'*k* = 4π²*m*/*T*² = {Q2012["k"]/1000:.1f} kN/m', '（2012-1）'], KEY2, KEY, 15, 15)
    return svg(W, H, o, '加質量反推 m、k')


def fig1_2():
    W, H = 900, 250
    items = [('*S*_{a}', '譜加速度', '（考卷給，以 *g* 計要 ×*g*）', AC), ('*S*_{d}', '= *S*_{a}/ω²', '= *S*_{a}*T*²/4π²', KEY), ('*F* = *kS*_{d}', '= *mS*_{a}', '最大彈簧力', COMP), ('*S*_{v}', '= ω*S*_{d}', '（擬速度）', TEN)]
    o = ''
    for i, (a, b, c, col) in enumerate(items):
        x = 20 + i * 220
        o += R(x, 50, 190, 140, '#fff', col, 2.2, 12)
        o += T(x + 95, 90, a, 20, col, 'middle', 'bold')
        o += T(x + 95, 126, b, 16, INK, 'middle')
        o += T(x + 95, 158, c, 14, MUT, 'middle')
        if i < 3:
            o += A(x + 193, 120, x + 217, 120, INK, 2.2, 10)
    o += T(450, 230, '同一點 *T* 上，*S*_{a}、*S*_{v}、*S*_{d} 只差 ω 的次方——讀一個就有全部', 15, MUT, 'middle')
    return svg(W, H, o, '反應譜換算鏈')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
