# -*- coding: utf-8 -*-
"""第 6 章：側推側力分布、容量震譜。"""
from sdfig import *  # noqa
from calcs import PO, k_exp
import math

EMP = [82.5, 165.0, 352.5]     # 2022-4 題解自設例：規範豎向分配（含 Ft）
SRSS = [121.4, 165.3, 313.3]   # 2022-4 題解自設例：振態組合


def fig6_1():
    W, H = 900, 340
    sets = [('均勻 *k* = 0', PO['uniform'], MUT), ('倒三角 *k* = 1', PO['tri'], AC), ('指數 *k* = 2', PO['k2'], KEY), ('規範（含 *F*_{t}）', EMP, WARN), ('SRSS', SRSS, COMP)]
    o = T(450, 24, '3 層、層高 3 m、基底剪力 600 kN 的五種側力分布（kN）', 15.5, INK, 'middle', 'bold')
    for j, (nm, F, c) in enumerate(sets):
        x0 = 30 + j * 176
        o += T(x0 + 80, 58, nm, 14.5, c, 'middle', 'bold')
        o += L(x0 + 30, 300, x0 + 30, 80, STEEL, 4)
        o += hatch_ground(x0 + 10, 300, 40)
        for i, f_ in enumerate(F):
            y = 300 - (i + 1) * 70
            o += A(x0 + 32, y, x0 + 32 + f_ * 0.3, y, c, 2.6, 10)
            o += T(x0 + 36 + f_ * 0.3, y - 8, f'{f_:.0f}', 14, c, 'start', 'bold')
    o += T(450, 330, '*F*_{i} = *V* · *w*_{i}*h*_{i}^{k}/Σ*w*_{j}*h*_{j}^{k}；*k* = 1（*T* ≤ 0.5 s）～2（*T* ≥ 2.5 s）線性內插', 14, MUT, 'middle')
    return svg(W, H, o, '側推側力分布')


def fig6_2():
    W, H = 900, 360
    o = T(220, 24, '(a) 容量曲線', 15.5, INK, 'middle', 'bold')
    pl = Plot(60, 50, 300, 230, 0, 1, 0, 1)
    o += pl.axes([0], [0], 'δ_{roof}', '*V*/*W*', grid=False)
    cap = lambda x: 0.55 * (1 - math.exp(-x / 0.18))
    o += pl.curve(cap, 0, 1, AC, 3)
    o += L(450, 30, 450, 340, GRID, 1.5)
    o += T(675, 24, '(b) 容量震譜（ADRS）＋需求譜', 15.5, INK, 'middle', 'bold')
    p2 = Plot(500, 50, 340, 230, 0, 1, 0, 1)
    o += p2.axes([0], [0], '*S*_{d}', '*S*_{a}', grid=False)
    o += p2.curve(lambda x: cap(x) / 0.8, 0, 1, AC, 3)
    o += p2.curve(lambda x: min(0.95, 0.16 / max(x, 1e-3)), 0.05, 1, COMP, 2.6)
    o += p2.curve(lambda x: min(0.75, 0.11 / max(x, 1e-3)), 0.05, 1, COMP, 1.8, dash='6 4')
    xs = [i / 1000 for i in range(50, 1000)]
    xp = min(xs, key=lambda x: abs(cap(x) / 0.8 - min(0.75, 0.11 / x)))
    o += p2.dot(xp, cap(xp) / 0.8, KEY, 7)
    o += T(p2.X(xp) + 10, p2.Y(cap(xp) / 0.8) - 10, '性能點', 15, KEY, 'start', 'bold')
    o += T(p2.X(0.7), p2.Y(0.3), '5% 需求譜', 14, COMP, 'middle') + T(p2.X(0.75), p2.Y(0.1) - 4, '折減後', 14, COMP, 'middle')
    o += A(370, 160, 480, 160, KEY, 2.4, 11)
    o += T(425, 150, '換軸', 14, KEY, 'middle', 'bold')
    o += T(450, 330, '*S*_{a} = (*V*/*W*)/α_{1}、*S*_{d} = δ_{roof}/(*PF*_{1}φ_{1,roof})', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '容量曲線轉容量震譜')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
