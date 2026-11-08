# -*- coding: utf-8 -*-
"""第 8 章：腹板剪力三段、張力場效應。"""
from plot import *  # noqa
import math
import calcs

D = calcs.example()
S8 = calcs.ex_shear()


def fig8_1():
    W, H = 900, 430
    Fy, kv = D['Fy'], 5.0
    a, b = 50 * math.sqrt(kv / Fy), 62 * math.sqrt(kv / Fy)
    pl = Plot(100, 50, 560, 290, 0, 200, 0, 1.2)
    o = pl.axes([0, 50, a, b, 100, 150, 200], [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], '*h*/*t*_{w}', '*V*_{n}/(0.6*F*_{y}*A*_{w})', size=14,
                xfmt=lambda v: f'{v:.1f}' if v in (a, b) else f(v))
    el = lambda x: 1860 * kv / x ** 2 / (0.6 * Fy)
    st = 1860 * kv / (1.2 * 0.6 * Fy)
    o += pl.curve(el, math.sqrt(st), 200, AC, 1.8, dash='6 4')
    o += pl.curve(lambda x: calcs.vn_ratio(max(x, 1), kv, Fy), 1, 200, WARN, 3.2)
    o += pl.hline(0.8, 0, 200, MUT, 1.2)
    o += T(pl.X(185), pl.Y(0.8) - 8, '0.8', 14, MUT, 'middle')
    o += T(pl.X(20), pl.Y(1.0) - 12, '降伏：0.6*F*_{y}*A*_{w}', 15, TEN, 'start', 'bold')
    o += T(pl.X(118), pl.Y(0.72), '幾何平均', 15, WARN, 'start', 'bold')
    o += T(pl.X(118), pl.Y(0.64), '√(0.8 × 彈性)', 14, WARN, 'start')
    o += T(pl.X(150), pl.Y(0.30), '彈性剪力挫屈', 15, AC, 'start', 'bold')
    o += T(pl.X(150), pl.Y(0.22), '1860*k*_{v}/(*h*/*t*_{w})^{2}', 14, AC, 'start')
    o += pl.dot(S8['lam'], 1.0, KEY, 6)
    o += T(pl.X(S8['lam']) - 6, pl.Y(1.0) + 24, f'H700：{S8["lam"]:.1f}', 14, KEY, 'end', 'bold')
    o += box(680, 70, 210, 160, '*k*_{v} = 5、*F*_{y} = 3.5', [f'50√(*k*_{{v}}/*F*_{{y}}) = {a:.1f}', f'62√(*k*_{{v}}/*F*_{{y}}) = {b:.1f}', '', '兩個分界都是', '「兩條線交點」'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '腹板剪力三段')


def fig8_2():
    W, H = 900, 360
    o = ''
    # 板格：兩加勁板之間
    x0, y0, w, h = 60, 60, 300, 220
    o += R(x0, y0, w, h, STEEL2, INK, 1.4)
    o += R(x0 - 10, y0 - 14, w + 20, 14, STEEL3, INK, 1.4) + R(x0 - 10, y0 + h, w + 20, 14, STEEL3, INK, 1.4)
    o += R(x0 - 8, y0, 8, h, ACM, AC, 1.4) + R(x0 + w, y0, 8, h, ACM, AC, 1.4)
    # 拉力帶（對角）
    band = [(x0 + 20, y0 + h), (x0 + 110, y0 + h), (x0 + w - 20, y0), (x0 + w - 110, y0)]
    o += P(band, None, fill=TENM, close=True, op=0.7)
    for k in range(5):
        t = 0.2 + 0.15 * k
        xa, ya = x0 + 40 + (w - 120) * t, y0 + h - h * t
        o += A(xa - 22, ya + 16, xa + 22, ya - 16, TEN, 2, 8)
    # 挫屈皺摺（另一方向）
    for k in range(3):
        cx = x0 + 70 + k * 80
        o += L(cx - 30, y0 + 40, cx + 30, y0 + h - 40, COMP, 1.6, '5 4')
    o += T(x0 + w / 2, y0 - 26, '板格（兩加勁板之間，間距 *a*，高 *h*）', 15, INK, 'middle', 'bold')
    o += T(x0 + w + 16, y0 + 20, '加勁板＝壓桿', 14, AC, 'start', 'bold')
    o += T(x0 + w / 2, y0 + h + 40, '綠：對角拉力帶　紅虛線：挫屈皺摺', 14, MUT, 'middle')
    # 長條圖
    pl = Plot(560, 70, 260, 200, 0, 2, 0, 1.0)
    o += pl.axes([], [0, 0.2, 0.4, 0.6, 0.8, 1.0], '', '*V*_{n}/(0.6*F*_{y}*A*_{w})', size=14)
    for i, (v, lab, c) in enumerate(((S8['tf_Cv'], '只算挫屈', AC), (S8['tf_ratio'], '加張力場', TEN))):
        x = 0.25 + i
        o += R(pl.X(x), pl.Y(v), pl.X(x + 0.5) - pl.X(x), pl.Y(0) - pl.Y(v), c, None, 0, 4, op=0.85)
        o += T(pl.X(x + 0.25), pl.Y(v) - 8, f'{v:.3f}', 15, c, 'middle', 'bold')
        o += T(pl.X(x + 0.25), pl.Y(0) + 22, lab, 14, INK, 'middle', 'bold')
    o += T(690, 340, '*h*/*t*_{w} = 150、*a*/*h* = 1、*F*_{y} = 3.5（*k*_{v} = 10）', 14, MUT, 'middle')
    return svg(W, H, o, '張力場效應')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
