# -*- coding: utf-8 -*-
"""第 6 章：阿太堡限度與液性指數、塑性圖 A 線、級配曲線。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    d = ex2023_4()
    W_, H = 900, 330
    x0, x1 = 80, 800
    wmax = 50
    X = lambda w: x0 + w / wmax * (x1 - x0)
    y = 140
    o = ''
    states = [(0, 6, '固態', STEEL2), (6, d['PL'], '半固態', '#efebe9'), (d['PL'], d['LL'], '塑性（可捏）', TEN2), (d['LL'], wmax, '液態（會流）', AC2)]
    for a, b, nm, c in states:
        o += R(X(a), y - 40, X(b) - X(a), 40, c, INK, 1.2)
        o += T((X(a) + X(b)) / 2, y - 14, nm, 15, INK, 'middle', 'bold')
    o += A(x0, y, x1 + 20, y, INK, 1.8, 10)
    o += T(x1 + 24, y + 5, '*w*（%）', 15, INK, 'start')
    for w, lab, c in [(6, 'SL', MUT), (d['PL'], f"PL = {d['PL']:g}", WARN), (d['LL'], f"LL = {d['LL']:g}", WARN)]:
        o += L(X(w), y - 50, X(w), y + 10, c, 2)
        o += T(X(w), y - 56, lab, 15, c, 'middle', 'bold')
    o += dim(X(d['PL']), y + 30, X(d['LL']), y + 30, f"*PI* = LL − PL = {d['PI']:g}", KEY, 0, 15, 1)
    # LI scale
    yl = 250
    o += L(x0, yl, x1, yl, KEY, 2.4)
    o += T(x0 - 6, yl + 5, '*LI*', 15, KEY, 'end', 'bold')
    for li in (0, 0.5, 1.0, 1.5):
        w = d['PL'] + li * d['PI']
        o += L(X(w), yl - 8, X(w), yl + 8, KEY, 2)
        o += T(X(w), yl + 28, f'{li:g}', 14, KEY, 'middle')
    o += C(X(d['w']), yl, 7, COMP, '#fff', 2)
    o += L(X(d['w']), y, X(d['w']), yl - 8, COMP, 1.6, '5 4')
    o += T(X(d['w']) - 10, yl - 14, f"2023-4：*w* = {d['w']:g}% → *LI* = {d['LI']:.2f}（超過 LL）", 15, COMP, 'end', 'bold')
    o += T(450, 318, '*LI* = (*w* − PL)/PI：PL 處為 0、LL 處為 1，量的是「離液態還有多遠」', 14, MUT, 'middle')
    return svg(W_, H, o, '阿太堡限度與液性指數')


def fig6_2():
    d = ex2023_4()
    W_, H = 900, 420
    pl = Plot(100, 50, 520, 300, 0, 100, 0, 60)
    o = pl.axes([0, 20, 40, 50, 60, 80, 100], [0, 10, 20, 30, 40, 50, 60], 'LL', 'PI')
    o += pl.curve(lambda x: max(0, aline(x)), 20, 100, COMP, 3)
    o += pl.vline(50, 0, 60, INK, 1.8, '6 4')
    o += pl.curve(lambda x: x, 0, 60, MUT, 1.2, '3 3')
    o += T(pl.X(45), pl.Y(57), 'PI = LL（不可能區）', 14, MUT, 'end')
    o += T(pl.X(30), pl.Y(40), 'CL', 18, AC, 'middle', 'bold')
    o += T(pl.X(75), pl.Y(48), 'CH', 18, AC, 'middle', 'bold')
    o += T(pl.X(40), pl.Y(5), 'ML／OL', 16, WARN, 'middle', 'bold')
    o += T(pl.X(82), pl.Y(14), 'MH／OH', 16, WARN, 'middle', 'bold')
    o += pl.dot(20, 0, COMP, 5)
    o += T(pl.X(20) - 8, pl.Y(0) - 10, '(20, 0)', 14, COMP, 'end', 'bold')
    o += pl.dot(50, aline(50), COMP, 5)
    o += T(pl.X(50) + 8, pl.Y(aline(50)) + 18, f'(50, {aline(50):.1f})', 14, COMP, 'start', 'bold')
    o += pl.dot(d['LL'], d['PI'], KEY, 6)
    o += T(pl.X(d['LL']) - 8, pl.Y(d['PI']) - 10, f"2023-4 ({d['LL']:g}, {d['PI']:g})", 14, KEY, 'end', 'bold')
    o += T(pl.X(92), pl.Y(aline(92)) + 26, 'A 線', 15, COMP, 'middle', 'bold')
    o += R(650, 80, 240, 170, KEY2, KEY, 1.4, 8)
    o += T(770, 108, 'A 線只記兩點', 15, KEY, 'middle', 'bold')
    o += T(770, 138, '(20, 0) 與 (50, 21.9)', 15, INK, 'middle')
    o += T(770, 166, 'A 線以上：黏土 C', 15, AC, 'middle')
    o += T(770, 194, 'A 線以下：粉土 M／有機 O', 15, WARN, 'middle')
    o += T(770, 222, 'LL 50 為 L／H 分界', 15, INK, 'middle')
    return svg(W_, H, o, '塑性圖與 A 線')


def fig6_3():
    g = grad_coef()
    W_, H = 900, 400
    lx0, lx1 = math.log10(0.05), math.log10(30)
    pl = Plot(100, 50, 520, 280, lx0, lx1, 0, 100)
    o = pl.axes([math.log10(v) for v in (0.075, 1, 4.75, 10)], [0, 10, 30, 60, 100], '粒徑（mm，對數）', '通過 %',
                xfmt=lambda t: f'{10 ** t:g}')
    pts = [pl.pt(math.log10(dd), p) for dd, p in GRAD]
    o += P(pts, AC, 3)
    for p, key, c in ((10, 'D10', TEN), (30, 'D30', WARN), (60, 'D60', KEY)):
        dd = g[key]
        o += pl.hline(p, lx0, math.log10(dd), c, 1.4, '5 4')
        o += pl.vline(math.log10(dd), 0, p, c, 1.4, '5 4')
        o += pl.dot(math.log10(dd), p, c, 5)
        o += T(pl.X(math.log10(dd)) + 10, pl.Y(p) + 22, f'*D*_{{{key[1:]}}} = {dd:.3f}', 14, c, 'start', 'bold')
    o += R(650, 70, 240, 200, KEY2, KEY, 1.4, 8)
    o += T(770, 98, '（自訂示意級配）', 14, MUT, 'middle')
    o += T(770, 128, f"*C*_{{u}} = *D*_{{60}}/*D*_{{10}} = {g['Cu']:.2f}", 15, INK, 'middle')
    o += T(770, 158, f"*C*_{{c}} = *D*_{{30}}²/(*D*_{{10}}*D*_{{60}}) = {g['Cc']:.2f}", 15, INK, 'middle')
    o += T(770, 192, '*C*_{u} > 6 可，但 *C*_{c} < 1', 15, COMP, 'middle', 'bold')
    o += T(770, 222, '→ 不是良好級配', 15, COMP, 'middle', 'bold')
    o += T(770, 250, '（中間粒徑缺一段）', 14, INK, 'middle')
    return svg(W_, H, o, '級配曲線與 Cu、Cc')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
