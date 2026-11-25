# -*- coding: utf-8 -*-
"""第 4 章：容量設計剪力、強柱弱梁機構。"""
from sdfig import *  # noqa
from calcs import MPR, WU, VG, VEQ1, VEQ2, VE, B, PHIVS12, VU_2H
import math


def fig4_1():
    W, H = 900, 400
    o = T(450, 24, '容量設計：兩端都達到 *M*_{pr}（側移向右）', 15.5, INK, 'middle', 'bold')
    x0, x1, y0 = 170, 730, 110
    o += R(x0, y0 - 12, x1 - x0, 24, STEEL3, INK, 1.4)
    for i in range(12):
        x = x0 + 20 + i * 45
        o += A(x, y0 - 50, x, y0 - 14, WARN, 1.6, 7)
    o += T(x0 + 10, y0 - 56, f'*w*_{{u}} = 1.2*D* + 1.0*L* = {WU:.2f} tf/m', 14, WARN, 'start', 'bold')
    o += curve_arrow([(x0 - 30 * math.cos(a), y0 + 30 * math.sin(a)) for a in [math.radians(d) for d in range(-60, 70, 10)]], KEY, 2)
    o += curve_arrow([(x1 + 30 * math.cos(a), y0 + 30 * math.sin(a)) for a in [math.radians(d) for d in range(240, 110, -10)]], KEY, 2)
    o += T(x0 - 40, y0 + 52, f'*M*_{{pr}}^{{+}} = {MPR["A+"]:.2f}', 14, KEY, 'end', 'bold')
    o += T(x1 + 40, y0 + 52, f'*M*_{{pr}}^{{−}} = {MPR["B−"]:.2f}', 14, KEY, 'start', 'bold')
    o += T(450, y0 + 40, f'ℓ_{{n}} = {B["ln"]/100:.1f} m', 14, MUT, 'middle')
    pl = Plot(x0, 210, x1 - x0, 150, 0, 6.4, 0, 38)
    o += pl.axes([0, 1.2, 3.2, 5.2, 6.4], [0, 10, 20, 30], '*x* (m)', '|*V*| (tf)', grid=False)
    v2 = lambda x: (VEQ2 - VG) + WU * x
    v1 = lambda x: (VEQ1 + VG) - WU * x
    o += pl.curve(v2, 0, 6.4, COMP, 2.8) + pl.curve(v1, 0, 6.4, AC, 2, dash='6 4')
    o += T(pl.X(6.4) - 8, pl.Y(v2(6.4)) + 22, f'B 端 {VE:.2f}', 14, COMP, 'end', 'bold')
    o += pl.area(lambda x: 35.25 if x <= 1.2 or x >= 5.2 else 0, lambda x: 0, 0, 6.4, KEY2, 0.6)
    o += T(pl.X(0.6), pl.Y(36.5), f'φ*V*_{{s}} = {PHIVS12:.2f}', 14, KEY, 'middle', 'bold')
    o += box(745, 200, 150, 190, '*V*_{e}', [f'= *V*_{{eq}} + *V*_{{g}}', f'= {VEQ2:.2f}', f'+ {VG:.2f}', f'= {VE:.2f} tf', '*V*_{eq}/*V*_{e} > ½', '→ *V*_{c} = 0'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '容量設計剪力')


def _bldg(ox, title, mech):
    o = T(ox + 150, 26, title, 15.5, INK, 'middle', 'bold')
    n, sh, bw = 3, 80, 200
    xb, yb = ox + 50, 320
    D = 40
    for i in range(n):
        y_b, y_t = yb - i * sh, yb - (i + 1) * sh
        if mech == 'beam':
            db, dt = D * i / n, D * (i + 1) / n
        else:
            db, dt = (0 if i == 0 else D), D
        for cx in (xb, xb + bw):
            o += L(cx + db, y_b, cx + dt, y_t, STEEL, 5)
        o += L(xb + dt, y_t, xb + bw + dt, y_t, STEEL3, 6)
        if mech == 'beam':
            o += C(xb + dt + 12, y_t, 6, COMP, '#fff', 2) + C(xb + bw + dt - 12, y_t, 6, COMP, '#fff', 2)
        elif i == 0:
            for cx in (xb, xb + bw):
                o += C(cx + 2, y_b - 6, 6, COMP, '#fff', 2) + C(cx + dt - 2, y_t + 6, 6, COMP, '#fff', 2)
    if mech == 'beam':
        o += C(xb, yb - 6, 6, COMP, '#fff', 2) + C(xb + bw, yb - 6, 6, COMP, '#fff', 2)
    o += hatch_ground(xb - 30, yb, bw + 60)
    return o


def fig4_2():
    W, H = 900, 380
    o = _bldg(0, '強柱弱梁：梁端塑鉸（梁機構）', 'beam')
    o += L(450, 20, 450, 340, GRID, 1.5)
    o += _bldg(450, '強梁弱柱：一層柱端塑鉸（層機構）', 'story')
    o += T(225, 362, '塑鉸多、分散，總變形大才崩塌', 14, TEN, 'middle', 'bold')
    o += T(675, 362, '塑鉸集中在一層，小變形就崩塌', 14, COMP, 'middle', 'bold')
    return svg(W, H, o, '兩種崩塌機構')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
