# -*- coding: utf-8 -*-
"""第 1 章：牆的位移與 K（示意）、三種牆。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig1_1():
    W_, H = 900, 400
    pl = Plot(130, 50, 600, 280, -1.0, 5.0, 0, 3.4)
    o = pl.axes([-1, 0, 1, 2, 3, 4, 5], [0, 1 / 3, 1, 2, 3], '牆位移 Δ/*H*（%）', '*K*', yfmt=lambda t: {1 / 3: '1/3', 0.5: '0.5'}.get(t, f'{t:g}'))
    ka, k0, kp = Ka(30), K0(30), Kp(30)
    def K(x):
        if x <= 0:
            return ka + (k0 - ka) * math.exp(x / 0.12)
        return k0 + (kp - k0) * (1 - math.exp(-x / 1.1))
    o += pl.curve(K, -1.0, 5.0, KEY, 3.2)
    o += pl.vline(0, 0, 3.4, INK, 1.2, '3 3')
    o += pl.dot(0, k0, AC, 6)
    o += T(pl.X(0) + 10, pl.Y(k0) + 22, '*K*_{0}：不動（被樓版夾住）', 15, AC, 'start', 'bold')
    o += T(pl.X(-0.95), pl.Y(ka) + 26, '*K*_{a}：離開填土', 15, TEN, 'start', 'bold')
    o += T(pl.X(4.9), pl.Y(kp) + 26, '*K*_{p}：推向填土', 15, COMP, 'end', 'bold')
    o += pl.area(lambda x: 3.4, lambda x: 0, -0.4, -0.1, TENM, 0.25)
    o += pl.area(lambda x: 3.4, lambda x: 0, 2, 5, COMPM, 0.15)
    o += T(pl.X(-0.25), pl.Y(3.2), '0.1～0.4%', 14, TEN, 'middle', 'bold')
    o += T(pl.X(3.5), pl.Y(3.2), '2～5% 才到頂', 14, COMP, 'middle', 'bold')
    o += T(450, 390, '（示意：φ = 30°；曲線形狀只表趨勢，門檻值依土質不同）', 14, MUT, 'middle')
    return svg(W_, H, o, '牆位移與側向土壓力係數')


def fig1_2():
    W_, H = 900, 330
    o = ''
    for i, (title, c, mv, lab) in enumerate([('地下室外牆', AC, 0, '*K*_{0}'), ('懸臂擋土牆', TEN, -1, '*K*_{a}'), ('推向土（錨碇塊）', COMP, 1, '*K*_{p}')]):
        x = 60 + i * 290
        o += T(x + 110, 30, title, 16, INK, 'middle', 'bold')
        o += R(x + 70, 70, 150, 200, SOIL, None)
        o += L(x + 70, 70, x + 220, 70, SOILE, 1.6)
        o += R(x + 56, 60, 14, 210, STEEL3, INK, 1.4)
        if mv == 0:
            o += L(x + 20, 80, x + 56, 80, INK, 3) + L(x + 20, 200, x + 56, 200, INK, 3)
            o += T(x + 14, 84, '樓版', 14, INK, 'end')
        else:
            if mv < 0:
                o += A(x + 52, 160, x + 26, 160, c, 3, 12)
            else:
                o += A(x + 22, 160, x + 54, 160, c, 3, 12)
        for y in (110, 160, 210, 250):
            o += A(x + 120, y, x + 74, y, c, 2, 9)
        o += T(x + 145, 300, f'{lab}', 18, c, 'middle', 'bold')
    return svg(W_, H, o, '三種牆的土壓狀態')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
