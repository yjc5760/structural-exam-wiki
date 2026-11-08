# -*- coding: utf-8 -*-
"""第 13 章：一端固定一端簡支梁的崩塌機構與 wu(ξ) 最小值。"""
from plot import *  # noqa
import math
import calcs

PL = calcs.ex_plastic()


def fig13_1():
    W, H = 900, 400
    o = ''
    x0, x1, yb = 70, 470, 120
    xi = PL['xi']
    xh = x0 + (x1 - x0) * xi
    o += T((x0 + x1) / 2, 30, '崩塌機構（虛位移）', 16, INK, 'middle', 'bold')
    # 固定端（左）：直立牆
    o += L(x0, yb - 40, x0, yb + 40, INK, 3)
    for k in range(7):
        yy = yb - 36 + k * 12
        o += L(x0, yy, x0 - 8, yy + 8, INK, 1)
    o += pin(x1, yb + 4)
    for k in range(12):
        xx = x0 + 16 + k * (x1 - x0 - 32) / 11
        o += A(xx, yb - 46, xx, yb - 8, COMP, 1.4, 7)
    o += T((x0 + x1) / 2, yb - 54, '*w*_{u}', 16, COMP, 'middle', 'bold')
    o += L(x0, yb, x1, yb, MUT, 1.4, '5 4')
    dl = 70
    o += P([(x0, yb), (xh, yb + dl), (x1, yb)], KEY, 3)
    for xx in (x0, xh):
        o += C(xx, yb + (dl if xx == xh else 0), 7, '#fff', KEY, 2.4)
    o += T(x0 + 12, yb + 26, '塑鉸 1', 14, KEY, 'start', 'bold')
    o += T(xh, yb + dl + 28, '塑鉸 2', 14, KEY, 'middle', 'bold')
    o += dim(x0, yb + 120, xh, yb + 120, f'ξ*L* = {xi:.3f}*L*', INK, 0, 14)
    o += dim(xh, yb + 120, x1, yb + 120, f'{1 - xi:.3f}*L*', INK, 0, 14)
    o += T((x0 + x1) / 2, yb + 170, '外功 = *w*_{u}×(三角形面積)；內功 = *M*_{p}×(各塑鉸轉角)', 14, INK, 'middle')
    # 右：wu(ξ) 曲線
    pl = Plot(560, 50, 290, 260, 0.2, 0.9, 10, 20)
    o += pl.axes([0.3, 0.5, xi, 0.8], [10, 12, 14, 16, 18, 20], 'ξ', '*w*_{u}*L*^{2}/*M*_{p}', size=14,
                 xfmt=lambda v: f'{v:.3f}' if abs(v - xi) < 1e-9 else f(v))
    xs = [0.2 + 0.7 * i / 1000 for i in range(1001)]
    ok = [x for x in xs if calcs.wu_curve(x) <= 20]
    o += pl.curve(calcs.wu_curve, ok[0], ok[-1], AC, 3)
    o += pl.dot(xi, PL['c'], KEY, 7)
    o += T(pl.X(xi) + 10, pl.Y(PL['c']) + 26, f'最小 {PL["c"]:.2f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.55), pl.Y(19.2), '真正的崩塌：取最小', 14, AC, 'middle', 'bold')
    return svg(W, H, o, '崩塌機構')


ALL = {'fig13_1': fig13_1}
