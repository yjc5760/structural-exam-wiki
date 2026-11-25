# -*- coding: utf-8 -*-
"""第 3 章：解耦示意、2016-1 模態疊加歷時。"""
from sdfig import *  # noqa
from calcs import Q2016, EX
import math


def fig3_1():
    W, H = 900, 330
    s, pts = shear_building(60, 290, 2, bw=110, sh=100, disp=[25, 40])
    o = T(115, 28, '兩層樓 *u* = φ_{1}*q*_{1} + φ_{2}*q*_{2}', 15.5, INK, 'middle', 'bold') + s
    o += T(270, 190, '=', 30, INK, 'middle', 'bold')
    o += cart(410, 200, 100, 60, '*q*_{1}', AC, AC2, wall_x=320, cs=False)
    o += T(415, 100, '*M*_{1}*q̈*_{1} + *K*_{1}*q*_{1} = φ_{1}^{T}*p*', 15, AC, 'middle', 'bold')
    o += T(560, 190, '+', 30, INK, 'middle', 'bold')
    o += cart(730, 200, 100, 60, '*q*_{2}', COMP, COMP2, wall_x=640, cs=False)
    o += T(740, 100, '*M*_{2}*q̈*_{2} + *K*_{2}*q*_{2} = φ_{2}^{T}*p*', 15, COMP, 'middle', 'bold')
    o += T(600, 280, '正交性讓交叉項全部消失：兩台台車各跳各的', 15, KEY, 'middle', 'bold')
    o += T(600, 308, '算完再用 *u* = Σφ_{n}*q*_{n} 加回來', 15, KEY, 'middle')
    return svg(W, H, o, '模態解耦')


def fig3_2():
    W, H = 900, 380
    pl = Plot(90, 40, 560, 290, 0, 2.5, -2.2, 2.2)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5], [-2, -1, 0, 1, 2], '*t* (s)', '*v*_{2} (m)')
    a = lambda t: 1.6 * math.sin(5 * (t - 0.1)) if t > 0.1 else 0
    b = lambda t: 0.4 * math.sin(10 * (t - 0.1)) if t > 0.1 else 0
    o += pl.curve(a, 0, 2.5, AC, 1.8, dash='6 4')
    o += pl.curve(b, 0, 2.5, COMP, 1.8, dash='6 4')
    o += pl.curve(lambda t: a(t) + b(t), 0, 2.5, KEY, 3, n=600)
    o += pl.hline(2.0, c=WARN, w=1.4) + T(pl.X(2.5), pl.Y(2.0) - 8, '絕對值和上界 2.0', 14, WARN, 'end', 'bold')
    ts = [0.1 + i * 0.0005 for i in range(4801)]
    tm = max(ts, key=lambda t: abs(a(t) + b(t)))
    vm = a(tm) + b(tm)
    o += pl.dot(tm, vm, KEY, 6)
    o += T(pl.X(tm) + 10, pl.Y(vm) - 10, f'實際最大 |*v*_{{2}}| = {abs(vm):.2f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(1.3), pl.Y(-1.85), '第 1 振態 1.6 sin 5(*t*−0.1)', 14, AC, 'middle')
    o += T(pl.X(1.95), pl.Y(-0.75), '第 2 振態 0.4 sin 10(*t*−0.1)', 14, COMP, 'middle')
    o += box(670, 50, 220, 290, '2016-1 頂層', ['頂層三角脈衝', f'衝量 *I* = {Q2016["I"]:.0f} N·s', '*t*_{d}/*T*_{1} 小 → 衝量近似', 'η̇_{n} = φ_{n}^{T}*I*/*M*_{n}', '*v*_{2} = 2η_{1} − η_{2}', '兩個振態的峰', '不在同一時刻'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '2016-1 模態疊加')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
