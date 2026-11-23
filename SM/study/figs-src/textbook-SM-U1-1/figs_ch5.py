# -*- coding: utf-8 -*-
"""第 5 章：Dr 的三把尺、Dr 與 γd 的非線性。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig5_1():
    d = ex2020_3()
    W_, H = 900, 400
    x0, x1 = 190, 760         # Dr 0% at x0（最鬆） → 100% at x1（最緊）
    X = lambda Dr: x0 + Dr * (x1 - x0)
    o = T(X(0), 40, '最鬆', 15, MUT, 'middle', 'bold') + T(X(1), 40, '最緊', 15, MUT, 'middle', 'bold')
    rows = [
        (80, '*D*_{r}', [(0, '0%'), (0.5, '50%'), (1, '100%')], KEY),
        (150, '孔隙比 *e*', [(0, f"{d['emax']:.3f}"), (1, f"{d['emin']:.3f}")], AC),
        (220, '體積 *V*（ml）', [(0, '640'), (1, '440')], AC),
    ]
    for y, lab, ticks, c in rows:
        o += L(x0, y, x1, y, c, 3)
        o += T(x0 - 20, y + 5, lab, 15, c, 'end', 'bold')
        for t, s in ticks:
            o += L(X(t), y - 8, X(t), y + 8, c, 2)
            o += T(X(t), y + 28, s, 14, c, 'middle')
    # γd row: nonlinear positions
    y = 290
    o += L(x0, y, x1, y, COMP, 3)
    o += T(x0 - 20, y + 5, 'γ_{d}（kN/m³）', 15, COMP, 'end', 'bold')
    for g in (13.03, 14, 15, 16, 17, 18, 18.95):
        Dr = d['gdmax'] * (g - d['gdmin']) / (g * (d['gdmax'] - d['gdmin']))
        o += L(X(Dr), y - 8, X(Dr), y + 8, COMP, 2)
        o += T(X(Dr), y + 28, f'{g:g}', 14, COMP, 'middle')
    # current state line
    o += L(X(0.7), 60, X(0.7), 330, KEY, 2, '6 4')
    o += T(X(0.7), 356, f"現地：*e* = {d['e']:.3f}、*V* = 500、γ_{{d}} = {d['gd']:.2f} → *D*_{{r}} = 70%", 15, KEY, 'middle', 'bold')
    o += T(450, 388, 'e 與 V 的刻度是均勻的；γ_{d} 的刻度越往右越擠', 14, MUT, 'middle')
    return svg(W_, H, o, '相對密度的三把尺')


def fig5_2():
    d = ex2020_3()
    W_, H = 900, 360
    pl = Plot(100, 50, 520, 260, d['gdmin'], d['gdmax'], 0, 1)
    o = pl.axes([13, 14, 15, 16, 17, 18, 19], [0, 0.25, 0.5, 0.75, 1.0], 'γ_{d}', '*D*_{r}', xfmt=lambda t: f'{t:g}', yfmt=lambda t: f'{t * 100:.0f}%')
    Drg = lambda g: d['gdmax'] * (g - d['gdmin']) / (g * (d['gdmax'] - d['gdmin']))
    o += pl.curve(Drg, d['gdmin'], d['gdmax'], KEY, 3)
    o += pl.curve(lambda g: (g - d['gdmin']) / (d['gdmax'] - d['gdmin']), d['gdmin'], d['gdmax'], COMP, 2, '6 4')
    o += pl.dot(d['gd'], d['Dr_g'], KEY, 6)
    o += T(pl.X(d['gd']) - 10, pl.Y(d['Dr_g']) - 10, f"正解 {d['Dr_g'] * 100:.0f}%", 15, KEY, 'end', 'bold')
    o += pl.dot(d['gd'], d['Dr_lin_wrong'], COMP, 6)
    o += T(pl.X(d['gd']) + 10, pl.Y(d['Dr_lin_wrong']) + 20, f"直接內插（錯）{d['Dr_lin_wrong'] * 100:.1f}%", 15, COMP, 'start', 'bold')
    o += R(650, 80, 240, 140, KEY2, KEY, 1.4, 8)
    o += T(770, 108, 'γ_{d} 版多一個因子', 15, KEY, 'middle', 'bold')
    o += T(770, 140, 'γ_{d,max}/γ_{d}', 16, INK, 'middle')
    o += T(770, 172, '因為 *e* 和 1/γ_{d} 才是線性', 15, INK, 'middle')
    o += T(770, 200, '（2020-3 的數字）', 14, MUT, 'middle')
    return svg(W_, H, o, 'Dr 與乾單位重的非線性')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
