# -*- coding: utf-8 -*-
"""第 1 章：超越機率與回歸期。"""
from sdfig import *  # noqa
from calcs import P_from, TRS, LEVELS
import math


def fig1_1():
    W, H = 900, 360
    pl = Plot(90, 40, 540, 270, 1, 4, 0, 1)       # x = log10 TR
    o = pl.axes([1, 2, 3, 4], [0, 0.25, 0.5, 0.75, 1], '*T*_{R}（年）', '50 年內超越機率', xfmt=lambda t: f'{10**t:g}', yfmt=lambda v: f'{v*100:.0f}%')
    o += pl.curve(lambda x: P_from(10 ** x), 1, 4, KEY, 3)
    for (nm, p), c in zip(LEVELS.items(), (TEN, AC, COMP)):
        tr = TRS[nm]
        x = math.log10(tr)
        o += pl.dot(x, p, c, 6) + pl.vline(x, 0, p, c)
        lab = f'{nm}：{p*100:.0f}% → {tr:.1f} 年' if tr < 100 else f'{nm}：{p*100:.0f}% → {tr:.0f} 年'
        o += T(pl.X(x) + (8 if p > 0.05 else -8), pl.Y(p) - (10 if p > 0.05 else 18), lab, 15, c, 'start' if p > 0.05 else 'end', 'bold')
    o += box(650, 50, 240, 260, '50 年擲 50 次骰子', ['每年中獎機率 1/*T*_{R}', '50 年都沒中：(1 − 1/*T*_{R})^{50}', '至少中一次：', '*P* = 1 − (1 − 1/*T*_{R})^{50}', '小機率近似：', '*T*_{R} ≈ 50/*P*', '（10% → 500、2% → 2500；', ' 80% 不能用近似）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '超越機率與回歸期')


ALL = {'fig1_1': fig1_1}
