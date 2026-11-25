# -*- coding: utf-8 -*-
"""第 1 章：柱勁度四種邊界、串並聯、落下質量。"""
from sdfig import *  # noqa
from calcs import Q2010_2, PI
import math


def _col(ox, title, k, shape, top_fixed=True, top_pin=False, horiz=False):
    o = T(ox + 105, 30, title, 15.5, INK, 'middle', 'bold')
    if not horiz:
        xb, yb, h = ox + 80, 300, 210
        o += fixed_wall(xb, yb, 60)
        o += L(xb, yb, xb, yb - h, STEEL3, 6)
        D = 55
        pts = [(xb + D * shape(i / 60), yb - h * i / 60) for i in range(61)]
        o += P(pts, AC, 3.2)
        xt = xb + D
        if top_fixed:
            o += L(xt - 22, yb - h, xt + 22, yb - h, INK, 3)
            o += T(xt + 26, yb - h - 8, '不可轉', 14, MUT, 'start')
        if top_pin:
            o += C(xt, yb - h, 6, '#fff', INK, 1.8)
        o += A(xt + 6, yb - h + 30, xt + 50, yb - h + 30, COMP, 2.4, 10) + T(xt + 54, yb - h + 35, '*F*', 15, COMP, 'start', 'bold')
        o += dim(xb, yb - h - 26, xt, yb - h - 26, 'Δ', MUT)
        o += T(ox + 105, 340, f'*k* = {k}*EI*/*h*³', 16, KEY, 'middle', 'bold')
    else:
        xl, xr, y = ox + 20, ox + 200, 150
        o += pin(xl, y) + pin(xr, y)
        D = 55
        pts = [(xl + (xr - xl) * i / 60, y + D * shape(i / 60)) for i in range(61)]
        o += L(xl, y, xr, y, STEEL3, 6)
        o += P(pts, AC, 3.2)
        o += A((xl + xr) / 2, y + D - 60, (xl + xr) / 2, y + D - 4, COMP, 2.4, 10) + T((xl + xr) / 2 + 8, y + D - 46, '*F*', 15, COMP, 'start', 'bold')
        o += T(ox + 110, 340, f'*k* = {k}*EI*/*L*³', 16, KEY, 'middle', 'bold')
    return o


def fig1_1():
    W, H = 900, 370
    ff = lambda s: 3 * s * s - 2 * s ** 3
    fp = lambda s: (3 * s * s - s ** 3) / 2
    ss = lambda s: (3 * s - 4 * s ** 3) / 1.0 if s <= 0.5 else (3 * (1 - s) - 4 * (1 - s) ** 3)
    o = _col(0, '(a) 兩端固定柱', 12, ff)
    o += L(225, 20, 225, 360, GRID, 1.2)
    o += _col(225, '(b) 底固定、頂鉸接', 3, fp, top_fixed=False, top_pin=True)
    o += L(450, 20, 450, 360, GRID, 1.2)
    o += _col(450, '(c) 懸臂端受力', 3, fp, top_fixed=False)
    o += L(675, 20, 675, 360, GRID, 1.2)
    o += _col(675, '(d) 簡支梁跨中', 48, lambda s: ss(s), horiz=True)
    return svg(W, H, o, '四種邊界的側向勁度')


def fig1_2():
    W, H = 900, 400
    o = T(225, 30, '(a) 並聯：一起變形、力相加', 16, INK, 'middle', 'bold')
    yb, yt = 300, 120
    for xb in (110, 250, 340):
        pass
    o += fixed_wall(150, yb, 70) + fixed_wall(300, yb, 70)
    o += L(150, yb, 150, yt, STEEL, 5) + L(300, yb, 300, yt, STEEL, 5)
    o += R(120, yt - 20, 210, 20, AC2, AC, 1.8, 3)
    o += A(335, yt - 10, 395, yt - 10, COMP, 2.6, 11) + T(400, yt - 5, '*F*', 16, COMP, 'start', 'bold')
    o += T(150, yb + 30, '*k*_{1}', 15, INK, 'middle') + T(300, yb + 30, '*k*_{2}', 15, INK, 'middle')
    o += R(70, 345, 310, 40, KEY2, KEY, 1.4, 8) + T(225, 371, '*k* = *k*_{1} + *k*_{2}', 16, KEY, 'middle', 'bold')
    o += L(450, 20, 450, 390, GRID, 1.5)
    o += T(675, 30, '(b) 串聯：力相同、變形相加', 16, INK, 'middle', 'bold')
    o += fixed_wall(560, yb, 70)
    o += R(530, yb - 40, 60, 40, WARN2, WARN, 1.6, 4) + T(560, yb - 14, '*k*_{b}', 15, WARN, 'middle', 'bold')
    o += L(560, yb - 40, 560, yt, STEEL, 5)
    o += R(520, yt - 20, 80, 20, AC2, AC, 1.8, 3)
    o += T(575, yt + 70, '*k*', 15, INK, 'start')
    o += T(520, yb - 14, '隔震層', 14, WARN, 'end')
    o += A(605, yt - 10, 660, yt - 10, COMP, 2.6, 11) + T(665, yt - 5, '*F*', 16, COMP, 'start', 'bold')
    o += box(690, 120, 195, 150, '1/*k*_{eq} = 1/*k* + 1/*k*_{b}', ['*k*_{eq} = *kk*_{b}/(*k*+*k*_{b})', '比兩者都軟', '（2004-2 隔震）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '串聯與並聯')


def fig1_3():
    W, H = 900, 360
    dst, h = Q2010_2['dst'], Q2010_2['h']
    w = 2 * PI
    v0 = math.sqrt(2 * h * dst) * w        # √(2gh)，g = ω²δst
    u = lambda t: -dst * math.cos(w * t) + v0 / w * math.sin(w * t)
    pl = Plot(90, 40, 490, 280, 0, 1.5, -6, 6)
    o = pl.axes([0, 0.5, 1, 1.5], [-6, -3, 0, 3, 6], '*t*/*T*', '*u*/δ_{st}')
    o += pl.curve(u, 0, 1.5, AC, 2.8, n=400)
    o += pl.hline(-dst, c=WARN, w=1.4)
    o += T(pl.X(1.48), pl.Y(-dst) + 22, '梁的原位置（*u* = −δ_{st}）', 14, WARN, 'end')
    o += T(pl.X(1.48), pl.Y(0) - 8, '新的靜平衡位置 *u* = 0', 14, MUT, 'end')
    o += pl.dot(0, -dst, KEY, 6)
    o += T(pl.X(0) + 10, pl.Y(-dst) + 24, '*u*_{0} = −δ_{st}、*u̇*_{0} = √(2*gh*)', 15, KEY, 'start', 'bold')
    tp = (math.atan2(v0 / w, -dst)) / w
    o += pl.dot(tp, Q2010_2['umax'], COMP, 6)
    o += T(pl.X(tp) + 10, pl.Y(Q2010_2['umax']) - 6, f'{Q2010_2["umax"]:.2f}', 15, COMP, 'start', 'bold')
    o += box(630, 50, 260, 270, '落下質量（2010-2）', ['*k* = 3*EI*/*L*³', 'δ_{st} = *mg*/*k*', '從靜平衡位置量：', '重力與 *k*δ_{st} 抵銷', '*u*_{max} = √(δ_{st}² + 2*h*δ_{st})', f'例 δ_{{st}} = 1、*h* = 10：{Q2010_2["umax"]:.2f}', '（自梁原位置再加 δ_{st}）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '落下質量的初始條件')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
