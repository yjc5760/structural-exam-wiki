# -*- coding: utf-8 -*-
"""第 1 章：能量交換、靜撓度。"""
from sdfig import *  # noqa
from calcs import C201, PI
import math


def fig1_1():
    W, H = 900, 380
    o = T(225, 28, '(a) 動能與位能此消彼長', 15.5, INK, 'middle', 'bold')
    pl = Plot(60, 60, 330, 220, 0, 1, 0, 1.1)
    o += pl.axes([0, 0.25, 0.5, 0.75, 1], [0, 1], '*t*/*T*', '能量', grid=False)
    o += pl.curve(lambda t: math.sin(2 * PI * t) ** 2, 0, 1, COMP, 2.6)
    o += pl.curve(lambda t: math.cos(2 * PI * t) ** 2, 0, 1, AC, 2.6)
    o += pl.hline(1, c=MUT, w=1.2)
    o += T(pl.X(0.25), pl.Y(1) - 10, '*T*_{max}', 15, COMP, 'middle', 'bold') + T(pl.X(0.5), pl.Y(1) - 10, '*V*_{max}', 15, AC, 'middle', 'bold')
    o += T(pl.X(0.75), pl.Y(0.55), '總和不變', 15, KEY, 'middle', 'bold')
    o += T(225, 345, '紅：動能 ∝ sin²　藍：位能 ∝ cos²', 14, MUT, 'middle')
    o += L(450, 20, 450, 370, GRID, 1.5)
    o += T(675, 28, '(b) 沿計算方向施加 *w*(*x*)', 15.5, INK, 'middle', 'bold')
    xl, xr, y = 500, 850, 140
    o += L(xl, y, xr, y, STEEL3, 7)
    for i in range(9):
        x = xl + 20 + i * 39
        o += A(x, y - 50, x, y - 8, WARN, 1.8, 8)
    o += T(xl + 10, y - 58, '*w*(*x*)', 15, WARN, 'start', 'bold')
    pts = [(xl + (xr - xl) * s, y + 70 * (s - 2 * s ** 3 + s ** 4) / (5 / 16)) for s in [i / 60 for i in range(61)]]
    o += P(pts, AC, 3)
    o += pin(xl, y + 4) + pin(xr, y + 4)
    o += T(675, y + 105, '靜撓度 *u*(*x*)', 15, AC, 'middle', 'bold')
    o += box(490, 270, 370, 100, f'2π/√*g* = 2π/√9.81 = {C201:.3f} ≈ 2.01', ['*T* = 2.01√(γ/β)：*u* 以 m 計、*T* 以秒計'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '能量守恆與靜撓度')


ALL = {'fig1_1': fig1_1}
