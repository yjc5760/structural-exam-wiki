# -*- coding: utf-8 -*-
"""第 2 章：振動單元（2010-3）。"""
from sdfig import *  # noqa
from calcs import Q2010
import math


def fig2_1():
    W, H = 900, 380
    o = T(330, 28, '兩跨上構（每跨 *L*、單位長度質量 *m*）＋中間一支墩（高 *L*）', 15.5, INK, 'middle', 'bold')
    xl, xm, xr, yd = 70, 330, 590, 120
    U0 = 36
    o += L(xl, yd, xr, yd, GRID, 6, '6 5')
    o += R(xl + U0, yd - 10, xr - xl, 20, AC2, AC, 2, 3)
    for x in (xl, xr):
        o += C(x + U0 / 2, yd + 18, 6, '#fff', INK, 1.5) + hatch_ground(x - 20, yd + 25, 60)
    o += T(xl + 10, yd + 60, '橋台：活動支承', 14, MUT, 'start')
    yb = yd + 230
    o += fixed_wall(xm, yb, 70)
    pts = [(xm + U0 * (3 * s * s - s ** 3) / 2, yb - 230 * s) for s in [i / 60 for i in range(61)]]
    o += L(xm, yb, xm, yd, STEEL3, 6) + P(pts, STEEL, 6)
    o += C(xm + U0, yd + 12, 6, '#fff', INK, 1.8)
    o += T(xm - 14, (yd + yb) / 2, '*EI*、高 *L*', 15, INK, 'end')
    o += A(xr + U0 + 10, yd, xr + U0 + 60, yd, COMP, 2.4, 10) + T(xr + U0 + 66, yd + 5, '縱向', 14, COMP, 'start', 'bold')
    o += dim(xm, yd - 34, xm + U0, yd - 34, '*U*_{0}', KEY)
    o += box(660, 150, 230, 210, '振動單元', ['上構兩跨：*W* = 2*mgL*', '軸向剛性 → 處處 *U*_{0}', '墩：底固、頂鉸', '*k* = 3*EI*/*L*³', '*U*_{0} = *W*/*k*', f'*T* = 2π√(*U*_{{0}}/*g*)', f'= {Q2010["coef"]:.3f}*L*²√(*m*/*EI*)'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '2010-3 振動單元')


ALL = {'fig2_1': fig2_1}
