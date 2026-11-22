# -*- coding: utf-8 -*-
"""第 4 章：用哪個斷面；偏心方向。"""
from figs_ps import *  # noqa
from calcs import rc2011_5, rc2012_1

R5 = rc2011_5(); R1 = rc2012_1()


def fig4_1():
    W, H = 900, 330
    o = T(450, 26, '後拉＋場鑄版：載重作用時斷面長什麼樣子，就用那個斷面', 16, INK, 'middle', 'bold')
    xs = [150, 450, 750]
    labs = [('① 施拉（導管未灌漿）', '淨斷面：扣掉導管', '*F*_{i}（後拉）、*M*_{G}'),
            ('② 灌漿後、版未硬化', '變換斷面：鋼腱 ×*n*', '版重 *M*_{S}'),
            ('③ 版硬化後', '合成斷面：梁＋版', '活載 *M*_{L}')]
    for i, (x, (t1, t2, t3)) in enumerate(zip(xs, labs)):
        o += R(x - 30, 90, 60, 110, STEEL2, INK, 1.4)
        if i == 0:
            o += C(x, 175, 9, '#fff', INK, 1.4)
        else:
            o += C(x, 175, 9, TEN, INK, 1.4)
        if i == 2:
            o += R(x - 80, 66, 160, 24, '#fff8e1', WARN, 1.4)
        o += T(x, 230, t1, 15, INK, 'middle', 'bold')
        o += T(x, 254, t2, 14, AC, 'middle')
        o += T(x, 278, t3, 14, COMP, 'middle', 'bold')
        if i < 2:
            o += A(x + 90, 145, x + 210, 145, MUT, 1.8, 10)
    o += T(450, 315, '已經作用的應力「鎖」在當時的斷面上；後來斷面變大，舊應力不會重新分配。', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '三個斷面')


def fig4_2():
    a, b, c = R5['a'], R5['b'], R5['c']
    return sum_panels([('*F*_{0}＋*M*_{G}（淨）', a[0], a[1]), ('*M*_{S}（變換）', b[0], b[1]), ('*M*_{L}（合成）', c[0], c[1])], (R5['top'], R5['bot']),
                      'RC-2011-5 全部載重：三段各用自己的斷面，再相加（kgf/cm²）', H=340, k=0.4,
                      note=f"上緣 {R5['top']:.2f}、下緣 {R5['bot']:.2f}（都受壓）；鋼腱 9,167 + 6 × 82.44 = {R5['fs2']:,.0f}")


def fig4_3():
    W, H = 900, 380
    o = T(450, 26, 'RC-2012-1：懸臂梁上偏心鋼鍵，自由端附近底纖維受拉超限（距自由端 ξ）', 16, INK, 'middle', 'bold')
    L = 610.0
    pl = Plot(100, 60, 560, 260, 0, 610, -20, 20)
    o += pl.axes([0, 100, 201, 300, 452, 610], [-20, -12.52, 0, 10, 20], 'ξ（cm）', '底纖維 *f*_{b}', xfmt=lambda v: f'{v:g}', yfmt=lambda v: f'{v:g}'.replace('-', '−'), size=14)
    fb = lambda x: R1['free'][1] + (R1['Msw'] / R1['S']) * (x / L) ** 2
    o += pl.area(lambda x: max(-R1['al']['ti'], fb(x)), lambda x: -20, 0, R1['xi'], COMP2, 0.8)
    o += pl.curve(fb, 0, 610, AC, 3)
    o += pl.hline(-R1['al']['ti'], 0, 610, COMP, 1.8, '7 4')
    o += T(pl.X(605), pl.Y(-R1['al']['ti']) + 20, '容許拉 −0.8√*f*′_{ci} = −12.52', 14, COMP, 'end', 'bold')
    o += pl.hline(0, 0, 610, INK, 1.2, None)
    o += T(pl.X(4), pl.Y(R1['free'][1]) + 22, f"自由端 {R1['free'][1]:.2f}".replace('-', '−'), 14, COMP, 'start', 'bold')
    o += T(pl.X(R1['xi']) + 6, pl.Y(-16), f"超限 {R1['xi']:.0f} cm", 14, COMP, 'start', 'bold')
    o += T(pl.X(560), pl.Y(fb(560)) - 10, f"固定端 +{R1['fix'][1]:.2f}（壓）", 14, AC, 'end', 'bold')
    o += box(680, 80, 210, 220, '為什麼', ['懸臂自重是負彎矩', '→ 鋼鍵要放上面', '但自由端 *M* = 0', '只剩 *P*/*A* 和 *Pe*/*S*', '→ 底纖維被拉', '補救：改變偏心', '（自由端 *e* → 0）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '懸臂超限')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
