# -*- coding: utf-8 -*-
"""第 2 章：自由振動、三種阻尼、衰減包絡。"""
from sdfig import *  # noqa
from calcs import Q2017, DEC, PI
import math


def fig2_1():
    W, H = 900, 400
    xi = Q2017['xi']; w = 2 * PI; wD = w * math.sqrt(1 - xi * xi)
    B = xi * w / wD
    u = lambda t: math.exp(-xi * w * t) * (math.cos(wD * t) + B * math.sin(wD * t))
    pl = Plot(90, 50, 640, 290, 0, 3.6, -1.1, 1.15)
    o = pl.axes([0, 1, 2, 3], [-1, -0.5, 0, 0.5, 1], '*t*/*T*', '*u*/*v*_{0}')
    o += pl.curve(lambda t: math.exp(-xi * w * t), 0, 3.6, TEN, 2, dash='7 5')
    o += pl.curve(lambda t: -math.exp(-xi * w * t), 0, 3.6, TEN, 2, dash='7 5')
    o += pl.curve(u, 0, 3.6, AC, 2.6, n=600)
    TD = 2 * PI / wD
    for j in range(4):
        tj = j * TD / 1.0 / (2 * PI / w) if False else j * (w / wD)
        val = math.exp(-xi * w * j * TD)
        o += pl.dot(tj, val, KEY if j == 3 else COMP, 6 if j == 3 else 5)
        o += T(pl.X(tj) + (8 if j else 10), pl.Y(val) - 12, (f'{Q2017["A3"]:.3f}' if j == 3 else f'{val:.3f}') if j else '1', 15, KEY if j == 3 else COMP, 'start', 'bold')
    o += pl.dot(1.5 * w / wD, -math.exp(-xi * w * 1.5 * TD), WARN, 5)
    o += T(pl.X(1.5 * w / wD) + 10, pl.Y(-math.exp(-xi * w * 1.5 * TD)) + 22, f'1.5 圈：{Q2017["A15"]:.3f}（誤讀）', 14, WARN, 'start')
    o += T(pl.X(2.55), pl.Y(0.78), '包絡 e^{−ξω*t*}', 16, TEN, 'middle', 'bold')
    o += R(750, 80, 140, 150, KEY2, KEY, 1.4, 8)
    o += T(820, 108, 'ξ = 0.05', 16, KEY, 'middle', 'bold')
    o += T(820, 138, '每圈 × 0.730', 15, INK, 'middle')
    o += T(820, 166, '3 圈 = 0.730³', 15, INK, 'middle')
    o += T(820, 196, f'= {Q2017["A3"]:.3f}', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '阻尼自由振動與包絡線')


def fig2_2():
    W, H = 900, 360
    pl = Plot(90, 50, 600, 260, 0, 2.5, -0.8, 1.1)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5], [-0.5, 0, 0.5, 1], '*t*/*T*', '*u*/*u*_{0}')
    w = 2 * PI

    def under(xi):
        wD = w * math.sqrt(1 - xi * xi)
        return lambda t: math.exp(-xi * w * t) * (math.cos(wD * t) + xi * w / wD * math.sin(wD * t))
    crit = lambda t: math.exp(-w * t) * (1 + w * t)
    xi2 = 2.0
    s1 = -w * (xi2 - math.sqrt(xi2 ** 2 - 1)); s2 = -w * (xi2 + math.sqrt(xi2 ** 2 - 1))
    over = lambda t: (s2 * math.exp(s1 * t) - s1 * math.exp(s2 * t)) / (s2 - s1)
    o += pl.curve(under(0.1), 0, 2.5, AC, 2.6, n=500)
    o += pl.curve(crit, 0, 2.5, KEY, 2.8)
    o += pl.curve(over, 0, 2.5, WARN, 2.6)
    o += pl.hline(0, c=MUT, dash=None, w=1)
    o += T(pl.X(0.62), pl.Y(-0.66), 'ξ = 0.1 欠阻尼：會振盪', 15, AC, 'start', 'bold')
    o += T(pl.X(0.36), pl.Y(0.30), 'ξ = 1 臨界', 15, KEY, 'start', 'bold')
    o += T(pl.X(1.15), pl.Y(0.55), 'ξ = 2 過阻尼：爬得更慢', 15, WARN, 'start', 'bold')
    o += R(710, 70, 180, 210, KEY2, KEY, 1.4, 8)
    o += T(800, 98, '臨界阻尼', 16, KEY, 'middle', 'bold')
    o += T(800, 128, '最快回到原點', 15, INK, 'middle')
    o += T(800, 154, '而不越過', 15, INK, 'middle')
    o += T(800, 190, '*c*_{cr} = 2*m*ω', 16, KEY, 'middle', 'bold')
    o += T(800, 222, '結構 ξ 約 0.02～0.05', 14, INK, 'middle')
    o += T(800, 250, '遠在欠阻尼這一側', 14, INK, 'middle')
    return svg(W, H, o, '三種阻尼')


def fig2_3():
    W, H = 900, 330
    pl = Plot(90, 40, 520, 240, 0, 0.3, 0, 1.0)
    o = pl.axes([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3], [0, 0.25, 0.5, 0.75, 1], 'ξ', '每圈剩下')
    o += pl.curve(lambda x: math.exp(-2 * PI * x), 0, 0.3, TEN, 3)
    o += pl.curve(lambda x: math.exp(-2 * PI * x / math.sqrt(1 - x * x)), 0, 0.3, COMP, 2, dash='6 4')
    for xi in (0.02, 0.05, 0.10, 0.20):
        v = DEC[xi]['approx']
        o += pl.dot(xi, v, KEY, 5)
        o += T(pl.X(xi) + 8, pl.Y(v) - 8, f'{v:.2f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.21), pl.Y(0.52), '近似 e^{−2πξ}', 15, TEN, 'start', 'bold')
    o += T(pl.X(0.22), pl.Y(0.12), '精確（虛線）', 15, COMP, 'start')
    o += R(640, 60, 250, 190, KEY2, KEY, 1.4, 8)
    o += T(765, 88, 'δ = ln(*u*_{i}/*u*_{i+1})', 16, KEY, 'middle', 'bold')
    o += T(765, 120, '= 2πξ/√(1−ξ²) ≈ 2πξ', 15, INK, 'middle')
    o += T(765, 156, 'ξ ≤ 0.1：兩者差 < 0.5 %', 15, INK, 'middle')
    o += T(765, 188, '*n* 圈後：e^{−2π*n*ξ}', 15, INK, 'middle')
    o += T(765, 220, '反求：ξ = δ/(2π)', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '每圈衰減比')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
