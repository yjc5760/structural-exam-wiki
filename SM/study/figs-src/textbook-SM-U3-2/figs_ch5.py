# -*- coding: utf-8 -*-
"""第 5 章：梯形底壓疊加、B′ 矩形、傾斜因數。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig5_1():
    d = ex2016_4()
    W, H = 900, 330
    o = ''
    V, B, e = d['V'], d['B'], d['e']
    q0 = V / B
    dq = q0 * 6 * e / B
    sc = 0.32
    w = 200
    for k, (title, f, c, fill) in enumerate((('均勻 Σ*V*/*B*', lambda t: q0, AC, AC2),
                                             ('彎矩 ±*M*/*S*', lambda t: dq * (1 - 2 * t), COMP, COMP2),
                                             ('相加＝梯形', lambda t: q0 + dq * (1 - 2 * t), WARN, WARN2))):
        x0 = 60 + k * 290
        y0 = 150
        o += R(x0, y0 - 24, w, 24, STEEL2, INK, 1.4)
        o += T(x0 + w / 2, 40, title, 16, c, 'middle', 'bold')
        pts = [(x0 + w * i / 20, y0 + f(i / 20) * sc) for i in range(21)]
        o += P([(x0, y0)] + pts + [(x0 + w, y0)], c, 2, fill=fill, close=True)
        o += L(x0, y0, x0 + w, y0, INK, 1.2)
        o += T(x0 - 4, y0 + f(0) * sc + 5, f'{f(0):.1f}', 14, c, 'end', 'bold')
        o += T(x0 + w + 4, y0 + f(1) * sc + 5, f'{f(1):.1f}', 14, c, 'start', 'bold')
        if k < 2:
            o += T(x0 + w + 45, 150, '＋' if k == 0 else '＝', 26, INK, 'middle', 'bold')
    o += T(60, 300, '牆趾', 14, MUT) + T(260, 300, '牆踵', 14, MUT, 'end')
    o += T(640, 300, f"*e*={e:.3f} < *B*/6={B / 6:.3f}：全斷面受壓", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '梯形底壓')


def fig5_2():
    d = ex2016_4()
    W, H = 900, 380
    o = ''
    s = 110
    x0, y0 = 160, 120
    X = lambda x: x0 + x * s
    B = d['B']
    o += R(X(0), y0 - 30, B * s, 30, STEEL2, INK, 1.6)
    o += C(X(0), y0, 6, KEY, '#fff', 2) + T(X(0) - 8, y0 - 8, '牆趾', 14, KEY, 'end', 'bold')
    sc = 0.5
    o += P([(X(0), y0), (X(0), y0 + d['qmax'] * sc), (X(B), y0 + d['qmin'] * sc), (X(B), y0)], WARN, 2, fill=WARN2, close=True, op=0.8)
    o += T(X(0) - 6, y0 + d['qmax'] * sc, f"{d['qmax']:.1f}", 15, WARN, 'end', 'bold')
    o += T(X(B) + 6, y0 + d['qmin'] * sc + 14, f"{d['qmin']:.1f}", 15, WARN, 'start', 'bold')
    xa, xb = d['xbar'] - d['Bp'] / 2, d['xbar'] + d['Bp'] / 2
    o += R(X(xa), y0, d['Bp'] * s, d['qp'] * sc, KEY2, KEY, 2.2, op=0.7)
    o += T(X(xa + d['Bp'] / 2), y0 + d['qp'] * sc + 22, f"*q*′={d['qp']:.1f} kPa（寬 *B*′={d['Bp']:.3f}）", 15, KEY, 'middle', 'bold')
    o += A(X(d['xbar']), y0 - 90, X(d['xbar']), y0 - 32, INK, 2.6, 12) + T(X(d['xbar']) + 8, y0 - 70, f"Σ*V*={d['V']:.2f}", 15, INK, 'start', 'bold')
    o += dim(X(0), y0 - 50, X(d['xbar']), y0 - 50, '', MUT) + T(X(d['xbar'] / 2), y0 - 58, f"*x̄*={d['xbar']:.3f}", 14, MUT, 'middle')
    o += L(X(B / 2), y0 - 40, X(B / 2), y0 + 20, MUT, 1, '4 3') + T(X(B / 2) + 4, y0 - 34, '中心', 14, MUT, 'start')
    return svg(W, H, o, '底壓與有效寬度')


def fig5_3():
    d = ex2016_4()
    W, H = 900, 380
    pl = Plot(90, 50, 560, 270, 0, 30, 0, 1.0)
    o = pl.axes([0, 5, 10, 15, 20, 25, 30], [0, 0.25, 0.5, 0.75, 1.0], '*ψ* (°)', '*F*_{i}')
    o += pl.curve(lambda p: (1 - p / 90) ** 2, 0, 30, AC, 3)
    o += pl.curve(lambda p: (1 - p / d['phi']) ** 2, 0, 30, COMP, 3)
    o += T(pl.X(29), pl.Y((1 - 29 / 90) ** 2) - 8, '*F*_{ci}', 15, AC, 'end', 'bold')
    o += T(pl.X(19), pl.Y(0.2), '*F*_{γi}（*φ*=30°）', 15, COMP, 'start', 'bold')
    for v in (d['Fci'], d['Fgi']):
        o += pl.dot(d['psi'], v, KEY, 6)
    o += pl.vline(d['psi'], 0, 1.0, KEY, 1.2)
    o += T(pl.X(d['psi']) + 8, pl.Y(d['Fci']) - 8, f"{d['Fci']:.3f}", 14, KEY, 'start', 'bold')
    o += T(pl.X(d['psi']) + 8, pl.Y(d['Fgi']) - 8, f"{d['Fgi']:.3f}", 14, KEY, 'start', 'bold')
    o += box(670, 70, 215, 160, '2016-4', [f"*ψ*={d['psi']:.2f}°", f"*q*_{{u}}={d['qu']:.1f}", f"*FS*={d['FS_BC']:.2f}<3.0", f"漏因數：{d['qu_noincl']:.0f}"], KEY2, KEY)
    return svg(W, H, o, '傾斜因數')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
