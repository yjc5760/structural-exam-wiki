# -*- coding: utf-8 -*-
"""第 6 章：三種攻擊、上舉（2003-3）、最短流徑（2017-4）。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    W, H = 900, 380
    o = ''
    panels = [(30, '上舉（頂）', AC), (320, '砂湧（沖）', COMP), (610, '水壓（推）', AC)]
    for k, (x, title, c) in enumerate(panels):
        o += R(x, 30, 260, 300, '#fff', MUT, 1.2, 12)
        o += T(x + 130, 56, title, 16, c, 'middle', 'bold')
        gx = x + 20
        if k == 0:
            o += R(gx, 160, 220, 60, '#ede7f6', INK, 1.2) + T(gx + 110, 195, '不透水黏土 *t*', 14, INK, 'middle')
            o += R(gx, 220, 220, 80, '#e3f2fd', INK, 1.2) + T(gx + 110, 290, '受壓砂層', 14, AC, 'middle')
            for xx in (60, 110, 160):
                o += A(gx + xx, 260, gx + xx, 214, AC, 2.6, 11)
            o += T(gx + 110, 150, '*γ*_{w}*h*_{w} 往上頂', 14, AC, 'middle', 'bold')
        elif k == 1:
            o += L(gx + 110, 90, gx + 110, 280, STEEL, 6)
            o += R(gx, 120, 110, 180, '#fff8e1', None, 0) + R(gx + 110, 200, 110, 100, '#fff8e1', None, 0)
            o += L(gx, 120, gx + 110, 120, AC, 2, '6 4') + L(gx + 110, 200, gx + 220, 200, AC, 2, '6 4')
            pts = [(gx + 80, 130), (gx + 90, 250), (gx + 110, 295), (gx + 130, 250), (gx + 140, 205)]
            o += curve_arrow(pts, COMP, 2.6, 11)
            o += T(gx + 165, 190, '出口坡降 *i*', 14, COMP, 'start', 'bold')
        else:
            o += L(gx + 110, 90, gx + 110, 300, STEEL, 6)
            o += P([(gx + 110, 110), (gx + 20, 290), (gx + 110, 290)], AC, 2, fill=AC2, close=True)
            o += T(gx + 20, 318, '*γ*_{w}*z*（*K*=1）', 14, AC, 'start', 'bold')
    o += T(450, 362, '插深能救砂湧，救不了上舉', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '水的三種攻擊')


def fig6_2():
    d = ex2003_3()
    W, H = 900, 420
    o = ''
    s = 26
    x0, y0 = 60, 50
    Y = lambda z: y0 + z * s
    D = d['D']
    o += R(x0, Y(D), 300, Y(10) - Y(D), '#ede7f6', INK, 1.2) + T(x0 + 150, Y((D + 10) / 2) + 5, f'剩餘黏土 10−*D*', 14, INK, 'middle', 'bold')
    o += R(x0, Y(10), 300, 60, '#e3f2fd', INK, 1.2) + T(x0 + 150, Y(10) + 40, '受壓砂層（水頭 7 m）', 14, AC, 'middle', 'bold')
    o += L(x0, Y(0), x0 + 300, Y(0), MUT, 1, '4 3') + T(x0 + 4, Y(0) - 6, '原地表', 14, MUT)
    o += L(x0, Y(D), x0 + 300, Y(D), INK, 1.6) + T(x0 + 296, Y(D) - 6, f'開挖面 *D*={D:.2f}', 14, INK, 'end', 'bold')
    for xx in (60, 150, 240):
        o += A(x0 + xx, Y(D) + 10, x0 + xx, Y(10) - 6, TEN, 2.4, 10)
        o += A(x0 + xx + 20, Y(10) + 30, x0 + xx + 20, Y(10) + 4, AC, 2.4, 10)
    o += T(x0 + 310, Y((D + 10) / 2), '17.5(10−*D*)', 14, TEN, 'start', 'bold')
    o += T(x0 + 310, Y(10) + 22, '68.67 kPa', 14, AC, 'start', 'bold')
    pl = Plot(520, 60, 320, 270, 0, 8, 0, 3)
    o += pl.axes([0, 2, 4, 6, 8], [0, 1, 2, 3], '*D* (m)', '*FS*')
    f = lambda Dd: 17.5 * (10 - Dd) / d['u']
    o += pl.curve(f, 0, 8, KEY, 3)
    o += pl.hline(1.0, 0, 8, COMP, 1.4) + pl.hline(1.5, 0, 8, WARN, 1.2)
    o += T(pl.X(0.1), pl.Y(1.5) - 6, '門檻 1.5', 14, WARN, 'start')
    o += pl.dot(D, 1.0, COMP, 6.5) + T(pl.X(D) - 6, pl.Y(1.0) + 24, f'FS=1：{D:.2f} m', 14, COMP, 'end', 'bold')
    D15 = 10 - 1.5 * d['u'] / 17.5
    o += pl.dot(D15, 1.5, WARN, 6) + T(pl.X(D15) + 8, pl.Y(1.5) - 10, f'{D15:.2f} m', 14, WARN, 'start', 'bold')
    return svg(W, H, o, '上舉')


def fig6_3():
    d = ex2017_4_water()
    W, H = 900, 440
    o = ''
    s = 26
    xw, y0 = 380, 30
    X = lambda x: xw + x * s
    Y = lambda z: y0 + z * s
    o += R(X(-11), Y(0), 11 * s, 15 * s, '#efe6d8', None, 0) + R(X(0), Y(8), 11 * s, 7 * s, '#efe6d8', None, 0)
    o += L(X(-11), Y(0), X(0), Y(0), INK, 1.4) + L(X(0), Y(8), X(11), Y(8), INK, 1.4)
    o += L(X(0), Y(0), X(0), Y(14), STEEL, 6)
    o += L(X(-11), Y(1), X(0), Y(1), AC, 2, '6 4') + T(X(-10.8), Y(1) - 6, '▽ GL−1.0（坑外）', 14, AC, 'start', 'bold')
    o += L(X(0), Y(8), X(11), Y(8), AC, 2, '6 4') + T(X(10.8), Y(8) - 6, '▽ GL−8.0（坑內）', 14, AC, 'end', 'bold')
    pts = [(X(-0.5), Y(1.2)), (X(-0.5), Y(13.6)), (X(0), Y(14.4)), (X(0.5), Y(13.6)), (X(0.5), Y(8.2))]
    o += curve_arrow(pts, COMP, 3, 12)
    o += dim(X(-2), Y(1), X(-2), Y(14), '', COMP) + T(X(-2.3), Y(7.5), '13 m', 15, COMP, 'end', 'bold')
    o += dim(X(2), Y(8), X(2), Y(14), '', COMP) + T(X(2.3), Y(11), '6 m', 15, COMP, 'start', 'bold')
    o += T(X(0), Y(14) + 26, '壁底 GL−14.0', 14, INK, 'middle')
    o += box(640, 260, 245, 160, '最短流徑', [f"*L*=13+6={d['L']:.0f} m", f"*i*=7/19={d['i']:.3f}", f"*i*_{{cr}}={d['icr']:.2f}", f"*FS*={d['FSp']:.2f}"], KEY2, KEY)
    return svg(W, H, o, '最短流徑')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
