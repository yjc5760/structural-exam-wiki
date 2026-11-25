# -*- coding: utf-8 -*-
"""第 3 章：耐震梁彎矩與配筋、細部規定。"""
from sdfig import *  # noqa
from calcs import MU, PHIMN, SEL, B
import math


def fig3_1():
    W, H = 900, 380
    o = T(450, 26, '2013-2 大梁 AB：分析彎矩（黑）與實配 φ*M*_{n}（彩色）tf·m', 15.5, INK, 'middle', 'bold')
    x0, x1, y0 = 120, 780, 190
    sc = 2.2
    o += L(x0, y0, x1, y0, MUT, 1.2)
    o += R(x0 - 40, y0 - 120, 40, 240, STEEL2, STEEL, 1.4) + R(x1, y0 - 120, 40, 240, STEEL2, STEEL, 1.4)
    o += T(x0 - 20, y0 + 145, 'A', 16, INK, 'middle', 'bold') + T(x1 + 20, y0 + 145, 'B', 16, INK, 'middle', 'bold')
    pts = {'A−': (x0, -MU['A−']), 'A+': (x0, MU['A+']), '中+': ((x0 + x1) / 2, MU['中+']), 'B−': (x1, -MU['B−']), 'B+': (x1, MU['B+'])}
    for k_, (x, m) in pts.items():
        y = y0 + m * sc
        o += L(x, y0, x, y, INK, 2.2)
        o += C(x, y, 4, INK, INK, 1)
        pm = PHIMN[k_] * (1 if m > 0 else -1)
        c = AC if m > 0 else COMP
        yy = y0 + pm * sc
        o += L(x + (12 if x < 450 else -12), y0, x + (12 if x < 450 else -12), yy, c, 6)
        anc = 'start' if x < 450 else 'end'
        dx = 22 if x < 450 else -22
        if k_ == '中+':
            anc, dx = 'start', 20
        o += T(x + dx, yy + (16 if m > 0 else -6), f'{abs(m)} → {PHIMN[k_]:.1f}（{SEL[k_]}-D25）', 14, c, anc, 'bold')
    o += T(450, y0 - 118, '負彎矩（上）', 14, COMP, 'middle') + T(450, y0 + 125, '正彎矩（下）', 14, AC, 'middle')
    o += T(450, 370, '規定：柱面 *M*_{n}^{+} ≥ ½*M*_{n}^{−}；任一斷面 *M*_{n}^{±} ≥ ¼ 最大柱面 *M*_{n}', 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '耐震梁彎矩與配筋')


def fig3_2():
    W, H = 900, 300
    x0, x1, y0, h = 80, 820, 110, 80
    o = T(450, 26, '特殊抗彎構架梁的箍筋區（立面）', 15.5, INK, 'middle', 'bold')
    o += R(x0 - 40, y0 - 40, 40, h + 80, STEEL2, STEEL, 1.4) + R(x1, y0 - 40, 40, h + 80, STEEL2, STEEL, 1.4)
    o += R(x0, y0, x1 - x0, h, '#fff', INK, 1.6)
    z = 2 * 60 * 0.9
    for x in [x0 + 5 + i * 14 for i in range(int(z / 14) + 1)] + [x1 - 5 - i * 14 for i in range(int(z / 14) + 1)]:
        o += L(x, y0 + 6, x, y0 + h - 6, COMP, 2)
    for x in [x0 + z + 30 + i * 30 for i in range(int((x1 - x0 - 2 * z - 30) / 30))]:
        o += L(x, y0 + 6, x, y0 + h - 6, AC, 1.6)
    o += dim(x0, y0 + h + 22, x0 + z, y0 + h + 22, '2*h*', COMP)
    o += dim(x1 - z, y0 + h + 22, x1, y0 + h + 22, '2*h*', COMP)
    o += T(x0 + z / 2, y0 + h + 70, '閉合箍 *s* ≤ min(*d*/4, 6*d*_{b}, 15 cm)', 14, COMP, 'middle', 'bold')
    o += T(x0 + z / 2, y0 + h + 92, '第一支距柱面 ≤ 5 cm', 14, COMP, 'middle')
    o += T(450, y0 + h + 70, '塑鉸區外 *s* ≤ *d*/2', 14, AC, 'middle', 'bold')
    o += T(450, y0 - 12, 'ρ ≤ 0.025；上下各至少 2 根連續筋', 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '箍筋區')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
