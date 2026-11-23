# -*- coding: utf-8 -*-
"""第 2 章：介面摩擦、σv' 剖面與臨界深度、K 的三種寫法。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig2_1():
    W, H = 900, 420
    o = T(225, 32, '(a) 磚塊壓在木板上', 17, INK, 'middle', 'bold')
    o += T(675, 32, '(b) 樁身上一小段', 17, INK, 'middle', 'bold')
    # (a)
    o += R(60, 250, 330, 22, '#d7ccc8', INK, 1.4)
    o += R(160, 170, 130, 80, STEEL2, INK, 1.6)
    o += A(225, 84, 225, 168, COMP, 3, 12)
    o += T(238, 110, '*N*（壓緊）', 15, COMP, 'start', 'bold')
    o += A(160, 210, 80, 210, TEN, 3, 12)
    o += T(76, 198, '*T*_{max}', 15, TEN, 'end', 'bold')
    o += A(300, 210, 372, 210, INK, 2.4, 11)
    o += T(372, 198, '推', 15, INK, 'end')
    o += R(70, 300, 310, 96, KEY2, KEY, 1.4, 8)
    o += T(225, 330, '*T*_{max} = *N* tan δ', 17, KEY, 'middle', 'bold')
    o += T(225, 360, '÷ 面積 → *f* = σ_{n} tan δ', 16, KEY, 'middle', 'bold')
    o += T(225, 386, '壓得越緊，越難滑', 15, INK, 'middle')
    # (b)
    cx = 600
    o += R(cx - 130, 60, 300, 300, SOIL, None)
    o += R(cx - 18, 60, 36, 300, STEEL2, INK, 1.6)
    o += L(cx - 130, 60, cx + 170, 60, SOILE, 1.4, '5 4')
    o += L(cx - 130, 360, cx + 170, 360, SOILE, 1.4, '5 4')
    # σv' 往下
    o += A(cx + 90, 90, cx + 90, 150, AC, 2.6, 11)
    o += T(cx + 100, 120, "σ_{v}′", 16, AC, 'start', 'bold')
    # σh 向樁
    for y in (190, 230, 270):
        o += A(cx + 80, y, cx + 22, y, AC, 2.4, 10)
    o += T(cx + 90, 236, "σ_{h}′ = *K*σ_{v}′", 16, AC, 'start', 'bold')
    # fs 向上 on pile surface
    for y in (210, 260):
        o += A(cx - 26, y + 16, cx - 26, y - 16, TEN, 2.6, 10)
    o += T(cx - 38, 240, '*f*_{s}', 16, TEN, 'end', 'bold')
    o += R(cx - 130, 372, 300, 40, KEY2, KEY, 1.4, 8)
    o += T(cx + 20, 398, "*f*_{s} = *K* σ_{v}′ tan δ", 17, KEY, 'middle', 'bold')
    return svg(W, H, o, '介面摩擦種子與樁身微小段')


def fig2_2():
    d = ex2007_3()
    W, H = 900, 470
    o = ''
    top, bot = 70, 400
    zmax = 16
    Y = lambda z: top + z / zmax * (bot - top)
    def axes(x0, w, xmax, ticks, lab):
        s = ''
        X = lambda v: x0 + v / xmax * w
        for t in ticks:
            s += L(X(t), top, X(t), bot, GRID, 1)
            s += T(X(t), top - 10, f'{t:g}', 14, MUT, 'middle')
        s += A(x0, top, x0 + w + 16, top, INK, 1.6, 9) + A(x0, top, x0, bot + 16, INK, 1.6, 9)
        s += T(x0 + w + 20, top + 5, lab, 15, INK, 'start')
        return s, X
    for z in (0, 5, 10, 15):
        o += T(70, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += T(30, bot + 30, '深度 *z*（m）', 14, INK, 'start')
    # 左：σv'
    s, X = axes(90, 260, 300, [0, 100, 180, 270], "σ_{v}′（kPa）")
    o += s
    o += P([(X(0), Y(0)), (X(d['qc']), Y(d['Lc'])), (X(d['qc']), Y(15))], AC, 3)
    o += P([(X(d['qc']), Y(d['Lc'])), (X(d['q15']), Y(15))], COMP, 2, dash='6 4')
    o += T(X(d['q15']) - 4, Y(15) + 22, '不封頂 270（錯）', 14, COMP, 'end')
    o += T(X(d['qc']) + 8, Y(12.5), '封頂 180', 15, AC, 'start', 'bold')
    # 右：fs
    x0 = 520
    s, X2 = axes(x0, 250, 60, [0, 20, 43.41], '*f*_{s}（kPa）')
    o += s
    o += P([(X2(0), Y(0)), (X2(d['fmax']), Y(d['Lc'])), (X2(0), Y(d['Lc']))], None, fill=TENM, close=True, op=0.8)
    o += R(X2(0), Y(d['Lc']), X2(d['fmax']) - X2(0), Y(15) - Y(d['Lc']), TEN2, None)
    o += P([(X2(0), Y(0)), (X2(d['fmax']), Y(d['Lc'])), (X2(d['fmax']), Y(15)), (X2(0), Y(15))], TEN, 3)
    o += T(X2(d['fmax'] * 0.35), Y(7), f"*Q*_{{s1}} = {d['Qs1']:.2f}", 14, TEN, 'middle', 'bold')
    o += T(X2(d['fmax'] * 0.5), Y(12.8), f"*Q*_{{s2}} = {d['Qs2']:.2f}", 14, TEN, 'middle', 'bold')
    o += T(X2(d['fmax']) + 8, Y(d['Lc']) - 6, f"{d['fmax']:.2f}", 14, TEN, 'start', 'bold')
    # Lc line across
    o += L(80, Y(d['Lc']), 800, Y(d['Lc']), WARN, 2, '8 5')
    o += T(372, Y(d['Lc']) - 8, '*L*_{c} = 20*D* = 10 m', 15, WARN, 'start', 'bold')
    o += L(80, Y(15), 800, Y(15), INK, 1.2, '3 3')
    o += T(800, Y(15) + 22, '樁底 15 m', 14, INK, 'end')
    return svg(W, H, o, 'SM-2007-3 有效覆土壓與單位摩擦剖面')


def fig2_3():
    W, H = 900, 400
    pl = Plot(100, 50, 520, 290, 25, 40, 0, 1.2)
    o = pl.axes([25, 28, 30, 32, 34, 36, 38, 40], [0, 0.3, 0.6, 0.9, 1.2], 'φ（°）', '*K*')
    k0 = lambda ph: 1 - math.sin(math.radians(ph))
    o += pl.curve(k0, 25, 40, AC, 3)
    o += pl.curve(lambda ph: 1.4 * k0(ph), 25, 40, TEN, 3)
    o += pl.curve(lambda ph: 1.8 * k0(ph), 25, 40, WARN, 3)
    o += pl.hline(1.0, 25, 40, COMP, 2, '6 4')
    o += T(pl.X(40) + 8, pl.Y(1.0) + 5, '*K* = 1.0（112 年題解）', 14, COMP, 'start', 'bold')
    o += T(pl.X(40) + 8, pl.Y(1.8 * k0(40)) + 5, '1.8(1 − sin φ)（96 年）', 14, WARN, 'start', 'bold')
    o += T(pl.X(40) + 8, pl.Y(1.4 * k0(40)) + 5, '1.4*K*_{0}（110 年）', 14, TEN, 'start', 'bold')
    o += T(pl.X(40) + 8, pl.Y(k0(40)) + 5, '*K*_{0} = 1 − sin φ（113 年）', 14, AC, 'start', 'bold')
    for ph, fn, c in [(30, lambda p: 1.8 * k0(p), WARN), (32, lambda p: 1.4 * k0(p), TEN), (38, k0, AC)]:
        o += pl.dot(ph, fn(ph), c, 6)
        o += T(pl.X(ph), pl.Y(fn(ph)) - 12, f'{fn(ph):.3f}', 14, c, 'middle', 'bold')
    return svg(W, H, o, '側向土壓力係數 K 的四種寫法')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
