# -*- coding: utf-8 -*-
"""第 4 章：需求 ÷ 供給長條、V*/V。"""
from sdfig import *  # noqa
from calcs import Q2025, Ra


def fig4_1():
    W, H = 900, 330
    q = Q2025
    steps = [('彈性需求 *I·S*_{aD}·*W*', q['I'] * q['SaD'] * q['W'], COMP),
             ('÷ *F*_{u} = 2（韌性）', q['I'] * q['SaD'] * q['W'] / q['Fu'], WARN),
             ('÷ 1.4（系統超強）', q['I'] * q['SaD'] * q['W'] / q['Fu'] / 1.4, KEY),
             ('÷ α_{y} = 1.4（起始降伏）', q['V'], AC)]
    o = T(450, 28, 'SD-2025-1：需求一路除到設計地震力（kN）', 16, INK, 'middle', 'bold')
    x0, sc = 300, 4.2
    for i, (nm, v, c) in enumerate(steps):
        y = 55 + i * 62
        o += T(x0 - 12, y + 30, nm, 15, c, 'end', 'bold')
        o += R(x0, y + 10, v * sc, 34, c, None, 0, 4, op=0.88)
        o += T(x0 + v * sc + 8, y + 33, f'{v:.2f}', 16, c, 'start', 'bold')
    o += T(450, 315, f'*V* = 120 ÷ 3.92 = {q["V"]:.2f} kN：只剩彈性需求的 1/3.92', 15, MUT, 'middle')
    return svg(W, H, o, '需求除以供給')


def fig4_2():
    W, H = 900, 330
    pl = Plot(90, 40, 520, 250, 1, 5, 0, 1.6)
    o = pl.axes([1, 2, 3, 4, 5], [0, 0.5, 1, 1.5], '*R*', '*V*^{*}/*V*')
    o += pl.curve(lambda R: Ra(R) / 3, 1, 5, KEY, 3)
    o += pl.curve(lambda R: Ra(R, True) / 2.5, 1, 5, WARN, 2.4, dash='6 4')
    o += pl.hline(1, c=COMP, w=1.4)
    o += pl.dot(4, 1, COMP, 6) + T(pl.X(4) + 8, pl.Y(1) + 24, '*R* = 4：*F*_{u} = 3', 15, COMP, 'start', 'bold')
    o += T(pl.X(4.6), pl.Y(1.42), '一般工址 *F*_{u}/3', 15, KEY, 'middle', 'bold')
    o += T(pl.X(2.2), pl.Y(0.85), '臺北盆地 *F*_{u}/2.5', 15, WARN, 'middle', 'bold')
    o += T(pl.X(4.5), pl.Y(0.15), '（長週期，未計 (·)_{m}）', 14, MUT, 'middle')
    o += box(630, 50, 260, 250, '誰控制設計？', ['*V*^{*}/*V* = *F*_{u}/3', '*F*_{u} > 3 → *V*^{*} 控制', '（RC 特殊抗彎構架', '*R* = 4.8 長週期：1.18）', '高韌性系統反而被', '「小震不壞」卡住', '設計取三者最大'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'V*/V')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
