# -*- coding: utf-8 -*-
"""第 5 章：負摩擦力中性點、群樁效率。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig5_1():
    W, H = 900, 440
    top, bot = 70, 380
    o = T(220, 34, '(a) 誰沉得多？', 17, INK, 'middle', 'bold')
    o += T(660, 34, '(b) 摩擦方向與軸力', 17, INK, 'middle', 'bold')
    # (a) settlement profiles
    x0, w = 90, 260
    Y = lambda z: top + z / 20 * (bot - top)
    X = lambda s: x0 + s / 10 * w
    o += A(x0, top, x0 + w + 14, top, INK, 1.6, 9) + A(x0, top, x0, bot + 14, INK, 1.6, 9)
    o += T(x0 + w + 18, top + 5, '沉陷', 15, INK, 'start')
    o += T(x0 - 8, bot + 30, '深度', 14, INK, 'start')
    soil = lambda z: 9 * max(0, 1 - z / 16) ** 1.6 + 0.4
    pile = lambda z: 3.0 - 0.6 * z / 20
    o += P([(X(soil(z / 4)), Y(z / 4)) for z in range(81)], WARN, 3)
    o += P([(X(pile(z / 4)), Y(z / 4)) for z in range(81)], AC, 3)
    # neutral point
    zn = next(z / 100 for z in range(2000) if soil(z / 100) <= pile(z / 100))
    o += C(X(pile(zn)), Y(zn), 6, KEY, '#fff', 2)
    o += L(x0, Y(zn), x0 + w, Y(zn), KEY, 1.6, '5 4')
    o += T(x0 + w, Y(zn) - 8, '中性點', 15, KEY, 'end', 'bold')
    o += T(200, Y(14), '橘：土（填土、液化）', 14, WARN, 'start', 'bold')
    o += T(200, Y(16.5), '藍：樁', 14, AC, 'start', 'bold')
    o += T(x0 + 10, Y(zn / 2) + 5, '土 > 樁', 14, COMP, 'start', 'bold')
    o += T(x0 + 12, Y(19.2), '樁 > 土', 14, TEN, 'start', 'bold')
    # (b)
    cx = 600
    o += R(cx - 16, top, 32, bot - top, STEEL2, INK, 1.6)
    for y in range(int(top) + 20, int(Y(zn)) - 5, 34):
        o += A(cx - 30, y - 12, cx - 30, y + 12, COMP, 2.2, 9)
        o += A(cx + 30, y - 12, cx + 30, y + 12, COMP, 2.2, 9)
    for y in range(int(Y(zn)) + 22, int(bot) - 5, 34):
        o += A(cx - 30, y + 12, cx - 30, y - 12, TEN, 2.2, 9)
        o += A(cx + 30, y + 12, cx + 30, y - 12, TEN, 2.2, 9)
    o += L(cx - 60, Y(zn), cx + 60, Y(zn), KEY, 1.6, '5 4')
    o += T(cx - 44, Y(zn / 2), '負摩擦 ↓', 15, COMP, 'end', 'bold')
    o += T(cx - 44, Y((zn + 20) / 2), '正摩擦 ↑', 15, TEN, 'end', 'bold')
    # axial force curve
    ax0 = 700
    o += A(ax0, top, ax0 + 150, top, INK, 1.4, 8) + A(ax0, top, ax0, bot + 10, INK, 1.4, 8)
    o += T(ax0 + 150, top - 10, '軸力', 14, INK, 'end')
    Q = lambda z: 60 + 70 * (z / zn) ** 1.2 if z <= zn else 130 - 80 * (z - zn) / (20 - zn)
    o += P([(ax0 + Q(z / 4), Y(z / 4)) for z in range(81)], KEY, 3)
    o += T(ax0 + Q(zn) + 6, Y(zn) + 5, '最大', 14, KEY, 'start', 'bold')
    return svg(W, H, o, '負摩擦力與中性點（示意）')


def fig5_2():
    W, H = 900, 380
    pl = Plot(100, 50, 520, 270, 1.5, 8, 0.5, 1.0)
    o = pl.axes([2, 3, 4, 5, 6, 7, 8], [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], '*s*/*D*', '*E*_{g}')
    eg = lambda sd: eg_CL(3, 3, 1.0, sd)[0]
    o += pl.curve(eg, 1.5, 8, KEY, 3)
    o += pl.dot(3, eg(3), KEY, 6)
    o += T(pl.X(3) + 10, pl.Y(eg(3)) + 22, f'*s* = 3*D*：{eg(3):.3f}', 15, KEY, 'start', 'bold')
    o += pl.hline(1.0, 1.5, 8, TEN, 1.6, '6 4')
    o += T(pl.X(8), pl.Y(1.0) - 10, '*E*_{g} = 1：各樁互不干擾', 14, TEN, 'end', 'bold')
    o += R(650, 80, 235, 180, KEY2, KEY, 1.4, 8)
    o += T(767, 108, '3×3 群樁', 16, KEY, 'middle', 'bold')
    o += T(767, 138, 'Converse–Labarre', 15, INK, 'middle')
    o += T(767, 166, '樁越密，越互相搶土', 15, INK, 'middle')
    o += T(767, 194, '黏土：另檢核塊體', 15, COMP, 'middle', 'bold')
    o += T(767, 222, '砂土打入：可能 > 1', 15, TEN, 'middle', 'bold')
    return svg(W, H, o, '群樁效率隨樁距變化')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
