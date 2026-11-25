# -*- coding: utf-8 -*-
"""第 3 章：簡支梁靜撓度與正弦振態。"""
from sdfig import *  # noqa
from calcs import Q2024, PI
import math


def fig3_1():
    W, H = 900, 340
    pl = Plot(90, 40, 520, 240, 0, 1, 0, 1.1)
    o = pl.axes([0, 0.25, 0.5, 0.75, 1], [0, 0.5, 1], '*x*/*L*', '正規化撓度')
    us = lambda s: (s - 2 * s ** 3 + s ** 4) / (5 / 16)
    o += pl.curve(us, 0, 1, AC, 3.2)
    o += pl.curve(lambda s: math.sin(PI * s), 0, 1, COMP, 2.2, dash='7 5')
    o += pl.curve(lambda s: 20 * (us(s) - math.sin(PI * s)) + 0.08, 0, 1, KEY, 1.6)
    o += T(pl.X(0.5), pl.Y(1.05), '兩條幾乎重合', 15, INK, 'middle', 'bold')
    o += T(pl.X(0.08), pl.Y(0.2), '差值 × 20（紫）', 14, KEY, 'start')
    o += box(630, 50, 260, 250, '均佈 *w* 的靜撓度 vs 振態', ['藍：*u* ∝ *x*(*L*³ − 2*Lx*² + *x*³)', '紅虛：sin(π*x*/*L*)', f'β = *w*²*L*⁵/(120*EI*)', 'ζ = 31*w*³*L*⁹/(362880*E*²*I*²)', f'*T*_{{規範}}/*T*_{{1}} = {Q2024["T_ratio"]:.4f}', '規範式略偏短', '（Rayleigh 上界）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '簡支梁靜撓度與振態')


ALL = {'fig3_1': fig3_1}
