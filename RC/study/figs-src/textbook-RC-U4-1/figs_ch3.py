# -*- coding: utf-8 -*-
"""第 3 章：兩階段與容許應力。"""
from figs_ps import *  # noqa
from calcs import demo
import math

D = demo(); AL = D['al']


def fig3_1():
    W, H = 900, 430
    o = T(450, 26, '示範梁的四個檢核點都落在各自的容許範圍內（kgf/cm²，壓為正）', 16, INK, 'middle', 'bold')
    pl = Plot(110, 60, 600, 300, 0, 4, -80, 280)
    o += pl.axes([], [-80, -40, 0, 40, 80, 120, 160, 200, 240, 280], '', 'kgf/cm²', size=14)
    pts = [('傳遞・上緣', D['t1'][0], AL['ci'], -AL['ti'], WARN), ('傳遞・下緣', D['t1'][1], AL['ci'], -AL['ti'], WARN),
           ('使用・上緣', D['t2'][0], AL['ct'], -AL['tU'], AC), ('使用・下緣', D['t2'][1], AL['ct'], -AL['tU'], AC)]
    for i, (lab, v, cmax, tmin, col) in enumerate(pts):
        x = i + 0.5
        o += R(pl.X(x) - 30, pl.Y(cmax), 60, pl.Y(tmin) - pl.Y(cmax), '#f5f5f5', col, 1.4)
        o += L(pl.X(x) - 30, pl.Y(v), pl.X(x) + 30, pl.Y(v), COMP if v > 0 else TEN, 4)
        o += T(pl.X(x) + 36, pl.Y(v) + 5, f'{v:.2f}'.replace('-', '−'), 14, COMP if v > 0 else TEN, 'start', 'bold')
        o += T(pl.X(x) - 34, pl.Y(cmax) + 5, f'{cmax:.0f}', 14, col, 'end')
        o += T(pl.X(x) - 34, pl.Y(tmin) + 5, f'{tmin:.2f}'.replace('-', '−'), 14, col, 'end')
        o += T(pl.X(x), pl.Y(-80) + 24, lab, 14, col, 'middle', 'bold')
    o += pl.hline(0, 0, 4, INK, 1.2, None)
    o += box(730, 70, 160, 290, '框＝容許範圍', ['傳遞（橘）', '壓 0.60*f*′_{ci} = 180', '拉 0.8√*f*′_{ci}', '= 13.86', '', '使用（藍）', '壓 0.60*f*′_{c} = 252', '拉 2.0√*f*′_{c}', '= 40.99（U 類）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '四個檢核點')


def fig3_2():
    W, H = 340, 1
    W, H = 900, 300
    o = T(450, 26, '使用階段拉應力的三個等級（kgf 制，*f*′_{c} = 420 時的數值）', 16, INK, 'middle', 'bold')
    sq = math.sqrt(420)
    pl = Plot(80, 90, 740, 60, 0, 90, 0, 1)
    o += pl.area(lambda x: 1, lambda x: 0, 0, 2 * sq, TEN2, 0.9)
    o += pl.area(lambda x: 1, lambda x: 0, 2 * sq, 3.2 * sq, WARN2, 0.9)
    o += pl.area(lambda x: 1, lambda x: 0, 3.2 * sq, 90, COMP2, 0.9)
    o += R(pl.X(0), pl.Y(1), pl.X(90) - pl.X(0), 60, 'none', INK, 1.2)
    o += T(pl.X(sq), pl.Y(0.5) + 5, 'U 類：未開裂', 15, TEN, 'middle', 'bold')
    o += T(pl.X(2.6 * sq), pl.Y(0.5) + 5, 'T 類：過渡', 15, WARN, 'middle', 'bold')
    o += T(pl.X(76), pl.Y(0.5) + 5, 'C 類：開裂', 15, COMP, 'middle', 'bold')
    for v, lab in ((2 * sq, '2.0√*f*′_{c} = 40.99'), (3.2 * sq, '3.2√*f*′_{c} = 65.58')):
        o += L(pl.X(v), pl.Y(1) - 8, pl.X(v), pl.Y(0) + 8, INK, 2)
        o += T(pl.X(v), pl.Y(0) + 28, lab, 14, INK, 'middle', 'bold')
    o += A(pl.X(26.51), pl.Y(1) - 34, pl.X(26.51), pl.Y(1) - 4, AC, 2, 9)
    o += T(pl.X(26.51), pl.Y(1) - 40, '示範梁 26.51', 14, AC, 'middle', 'bold')
    o += T(450, 250, '換算：SI 的 0.62√*f*′_{c}（MPa）× 3.19 ≈ 2.0√*f*′_{c}（kgf/cm²）；1.0√*f*′_{c} × 3.19 ≈ 3.2√*f*′_{c}', 15, KEY, 'middle', 'bold')
    o += T(450, 280, 'T 類要另做開裂斷面撓度與持續載重 0.45*f*′_{c} 等檢核；C 類要做裂縫控制', 14, MUT, 'middle')
    return svg(W, H, o, 'U T C')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
