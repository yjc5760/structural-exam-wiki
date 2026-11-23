# -*- coding: utf-8 -*-
"""第 4 章：荷重傳遞曲線、位移相容、軸力分布與 Se1、Winkler 勁度。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig4_1():
    d = ex2005_4()
    W, H = 900, 400
    o = ''
    for k, (x0, title, ymax, ym, xm, yl, c, lab) in enumerate([
            (90, '(a) 側摩擦 τ_{s}–*s*', 12, d['tmax'], d['smax'], 'τ_{s}（kPa）', TEN, '2 cm 就到頂'),
            (520, '(b) 端承 *q*_{p}–*d*', 480, d['qmax'], d['dmax'], '*q*_{p}（kPa）', AC, '8 cm 才到頂')]):
        pl = Plot(x0, 60, 300, 260, 0, 10, 0, ymax)
        o += T(x0 + 150, 30, title, 16, INK, 'middle', 'bold')
        yt = [0, 5, 10] if k == 0 else [0, 200, 400]
        o += pl.axes([0, 2, 4, 6, 8, 10], yt, 'cm', yl)
        o += pl.curve(lambda s: min(ym, ym / xm * s), 0, 10, c, 3.2)
        for s, cc in ((1.0, KEY), (1.5, WARN)):
            v = min(ym, ym / xm * s)
            o += pl.vline(s, 0, v, cc, 1.6, '4 3')
            o += pl.dot(s, v, cc, 5)
            o += T(pl.X(s) + (10 if k == 0 else 22), pl.Y(v) + (24 if s == 1.0 else -14), f'{int(v / ym * 100 + 0.5)}%', 14, cc, 'start', 'bold')
        o += T(pl.X(xm) + (10 if k == 0 else -10), pl.Y(ym) - 12, lab, 15, c, 'start' if k == 0 else 'end', 'bold')
    o += T(450, 390, '紫＝位移 1 cm、橘＝1.5 cm：摩擦已出五～七成五，端承還不到兩成', 15, INK, 'middle', 'bold')
    return svg(W, H, o, 'SM-2005-4 兩條荷重傳遞曲線')


def fig4_2():
    d = ex2005_4()
    W, H = 900, 400
    pl = Plot(100, 50, 520, 280, 0, 9, 0, 1000)
    o = pl.axes([0, 1, 1.5, 2, 4, 6, 8], [0, 200, 400, 600, 800, 1000], 'Δ（cm）', '*Q*（kN）')
    Qs = lambda s: min(d['tmax'], d['tmax'] / d['smax'] * s) * d['As']
    Qp = lambda s: min(d['qmax'], d['qmax'] / d['dmax'] * s) * d['Ap']
    o += pl.area(Qs, lambda s: 0, 0, 9, TENM, 0.6)
    o += pl.area(lambda s: Qs(s) + Qp(s), Qs, 0, 9, ACM, 0.6)
    o += pl.curve(lambda s: Qs(s) + Qp(s), 0, 9, KEY, 3)
    o += pl.hline(d['Qall3'], 0, 9, COMP, 2, '6 4')
    o += T(pl.X(9) + 6, pl.Y(d['Qall3']) + 5, f"*Q*_{{u}}/3 = {d['Qall3']:.2f}", 14, COMP, 'start', 'bold')
    o += T(pl.X(9) + 6, pl.Y(d['Qu']) + 5, f"*Q*_{{u}} = {d['Qu']:.2f}", 14, KEY, 'start', 'bold')
    for s, v, c in ((1.0, d['Q1'], KEY), (1.5, d['Q15'], WARN)):
        o += pl.dot(s, v, c, 6)
    o += T(pl.X(1.0) + 10, pl.Y(d['Q1']) + 22, f"1 cm：{d['Q1']:.2f}", 14, KEY, 'start', 'bold')
    o += T(pl.X(1.5) + 10, pl.Y(d['Q15']) - 4, f"1.5 cm：{d['Q15']:.2f}", 14, WARN, 'start', 'bold')
    o += T(pl.X(5), pl.Y(220), '摩擦（綠）', 15, TEN, 'middle', 'bold')
    o += T(pl.X(6.5), pl.Y(640), '端承（藍）', 15, AC, 'middle', 'bold')
    return svg(W, H, o, 'SM-2005-4 荷重沉陷曲線')


def fig4_3():
    d = ex2014_2()
    W, H = 900, 430
    top, bot = 60, 380
    Y = lambda z: top + z / 26 * (bot - top)
    x0, w = 100, 380
    X = lambda q: x0 + q / 5000 * w
    o = ''
    for t in (0, 1000, 2000, 3000, 4000, 5000):
        o += L(X(t), top, X(t), bot, GRID, 1) + T(X(t), top - 10, f'{t}', 14, MUT, 'middle')
    for z in (0, 5, 10, 15, 20, 25):
        o += T(x0 - 8, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += A(x0, top, x0 + w + 14, top, INK, 1.6, 9) + A(x0, top, x0, bot + 14, INK, 1.6, 9)
    o += T(x0 + w + 18, top + 5, '*Q*(*z*)', 15, INK, 'start')
    o += T(30, bot + 34, '深度（m）', 14, INK, 'start')
    pts = [(X(d['Qz'](z / 4)), Y(z / 4)) for z in range(0, 101)]
    o += P([(X(0), Y(0))] + pts + [(X(0), Y(25))], None, fill=KEY2, close=True)
    o += P(pts, KEY, 3)
    o += P([(X(d['Qt']), Y(0)), (X(d['Qt']), Y(25))], COMP, 2, dash='6 4')
    o += T(X(d['Qt']) - 6, Y(25) + 22, '錯：全長 4500', 14, COMP, 'end', 'bold')
    o += T(X(d['Qwp']) - 10, Y(25) - 6, f"樁底 {d['Qwp']:.1f}", 14, KEY, 'end', 'bold')
    o += L(x0, Y(18), x0 + w, Y(18), WARN, 1.4, '5 4')
    o += T(x0 + 8, Y(18) - 6, '*f*_{s} 在 18 m 以下定值', 14, WARN, 'start')
    o += T(X(1500), Y(9), '面積 = ∫*Q* d*z*', 15, KEY, 'middle', 'bold')
    # bars
    bx = 600
    o += T(bx + 140, 40, '沉陷三分量（mm）', 16, INK, 'middle', 'bold')
    vals = [('*S*_{e1} 樁身壓縮', d['Se1'], KEY), ('*S*_{e2} 樁底', d['Se2'], AC), ('*S*_{e3} 樁側', d['Se3'], TEN)]
    for i, (lab, v, c) in enumerate(vals):
        y = 80 + i * 70
        o += T(bx, y, lab, 15, c, 'start', 'bold')
        o += R(bx, y + 10, v / 45 * 260, 26, c, None, 0, 4, op=0.75)
        o += T(bx + v / 45 * 260 + 8, y + 30, f'{v:.2f}', 15, INK, 'start', 'bold')
    o += R(bx, 300, 280, 50, KEY2, KEY, 1.4, 8)
    o += T(bx + 140, 332, f"*S*_{{e}} = {d['Se']:.2f} mm", 17, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SM-2014-2 軸力分布與沉陷三分量')


def fig4_4():
    W, H = 900, 420
    o = T(200, 30, '(a) Winkler 模型的一小段', 16, INK, 'middle', 'bold')
    cx = 200
    o += R(cx - 20, 70, 40, 280, STEEL2, INK, 1.6)
    for y in range(90, 340, 36):
        for s in (-1, 1):
            xs = cx + s * 20
            pts = [(xs, y)]
            for i in range(1, 7):
                pts.append((xs + s * i * 8, y + (6 if i % 2 else -6)))
            pts.append((xs + s * 60, y))
            o += P(pts, MUT, 1.4)
            o += L(xs + s * 60, y - 8, xs + s * 60, y + 8, INK, 2)
    o += R(cx - 20, 190, 40, 50, KEY2, KEY, 2)
    o += A(cx, 150, cx, 188, COMP, 2.4, 10)
    o += T(cx + 28, 168, '*P*', 15, COMP, 'start', 'bold')
    o += A(cx, 285, cx, 243, COMP, 2.4, 10)
    o += T(cx + 28, 280, '*P* + d*P*', 15, COMP, 'start', 'bold')
    o += A(cx - 30, 232, cx - 30, 198, TEN, 2.4, 9)
    o += T(cx - 92, 222, 'τ_{s}*S* d*z*', 15, TEN, 'end', 'bold')
    o += T(cx, 380, 'τ_{s} = *k*_{s} *v*（土是彈簧）', 15, INK, 'middle')
    # (b)
    pl = Plot(510, 70, 330, 260, 0, 4, 0, 1.15)
    o += T(675, 30, '(b) 勁度隨樁長收斂', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 1, 2, 3, 4], [0, 0.5, 1.0], 'λ*L*', '*K*/√(*k*_{s}*S EA*)')
    o += pl.curve(stiff_ratio, 0, 4, KEY, 3)
    o += pl.hline(1.0, 0, 4, AC, 1.6, '6 4')
    for x in (1, 2, 3):
        o += pl.dot(x, stiff_ratio(x), KEY, 5)
        o += T(pl.X(x) + 6, pl.Y(stiff_ratio(x)) + 22, f'{stiff_ratio(x):.3f}', 14, KEY, 'start')
    o += T(pl.X(4), pl.Y(1.0) - 10, '半無限長', 14, AC, 'end', 'bold')
    return svg(W, H, o, 'Winkler 彈簧模型與樁頭勁度')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}
