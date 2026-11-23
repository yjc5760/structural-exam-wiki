# -*- coding: utf-8 -*-
"""第 1 章：主動圓與滑動楔、2015-2 分層土壓。"""
from plot import *  # noqa
from calcs import *  # noqa


def circle(pl, s1, s3, c, w=2.6, dash=None):
    C0, R = (s1 + s3) / 2, abs(s1 - s3) / 2
    pts = [pl.pt(C0 + R * math.cos(t), R * math.sin(t)) for t in [i * math.pi / 120 for i in range(121)]]
    return P(pts, c, w, dash=dash)


def fig1_1():
    W, H = 900, 400
    phi = 30.0
    pl = Plot(60, 70, 300, 150, 0, 120, 0, 60)
    o = pl.axes([0, 40, 80, 120], [0, 30, 60], '*σ*', '*τ*')
    o += L(pl.X(0), pl.Y(0), pl.X(60 / tan(phi)), pl.Y(60), WARN, 2.2)
    o += circle(pl, 100, 50, MUT, 1.6, '5 4') + circle(pl, 100, 100 / 3, TEN, 3)
    o += T(pl.X(100), pl.Y(0) + 40, '*σ*_{v}', 15, KEY, 'middle', 'bold') + T(pl.X(100 / 3), pl.Y(0) + 40, '*σ*_{a}', 15, TEN, 'middle', 'bold')
    o += T(pl.X(75), pl.Y(-2) + 20, '*K*_{0}', 14, MUT, 'middle')
    x0, y0, Hh = 640, 70, 260
    o += R(x0 - 40, y0, 40, Hh, STEEL2, INK, 1.6)
    o += L(x0, y0, x0 + 250, y0, INK, 1.6)
    wx = Hh * tan(45 - phi / 2)
    o += P([(x0, y0 + Hh), (x0 + wx, y0), (x0, y0)], TEN, 2, fill=TEN2, close=True, op=0.9)
    o += T(x0 + wx * 0.32, y0 + Hh * 0.42, '主動楔', 15, TEN, 'middle', 'bold')
    o += T(x0 + wx * 0.62 + 6, y0 + Hh * 0.6, '45°+*φ*/2', 14, TEN, 'start')
    xl = x0 - 40
    o += P([(xl, y0), (xl - 90, y0 + Hh), (xl, y0 + Hh)], TEN, 2, fill=TEN2, close=True)
    o += A(xl - 140, y0 + Hh * 2 / 3, xl - 4, y0 + Hh * 2 / 3, KEY, 2.8, 12)
    o += T(xl - 144, y0 + Hh * 2 / 3 - 8, '*P*_{a}', 15, KEY, 'end', 'bold')
    o += dim(xl - 160, y0 + Hh * 2 / 3, xl - 160, y0 + Hh, '', KEY) + T(xl - 168, y0 + Hh * 5 / 6 + 5, '*H*/3', 14, KEY, 'end', 'bold')
    o += T(xl - 90, y0 + Hh + 24, '*K*_{a}*γH*', 14, TEN, 'middle', 'bold')
    return svg(W, H, o, '主動圓與滑動楔')


def fig1_2():
    d = ex2015_2()
    W, H = 900, 460
    o = ''
    x0, y0, zs, sc = 520, 40, 44, 4.0
    Y = lambda z: y0 + z * zs
    o += L(x0, Y(0), x0, Y(8), INK, 2)
    for z in (0, 4, 8):
        o += T(x0 + 6, Y(z) + 5, f'{z} m', 14, MUT, 'start')
    # 右側土層柱
    o += R(700, Y(0), 160, Y(4) - Y(0), '#ede7f6', MUT, 1) + R(700, Y(4), 160, Y(8) - Y(4), '#fff8e1', MUT, 1)
    o += T(780, Y(2) - 6, '黏土', 15, INK, 'middle', 'bold') + T(780, Y(2) + 16, '*c*=20、*φ*=20°', 14, INK, 'middle')
    o += T(780, Y(6) - 6, '砂 *φ*=30°', 15, INK, 'middle', 'bold') + T(780, Y(6) + 16, '*γ*_{sat}=18.5', 14, INK, 'middle')
    o += L(700, Y(4), 860, Y(4), AC, 1.8, '6 4') + T(856, Y(4) - 6, '▽', 14, AC, 'end')
    s0 = -2 * d['c'] * math.sqrt(d['Ka1'])
    o += P([(x0, Y(0)), (x0 - s0 * sc, Y(0)), (x0, Y(d['zc']))], MUT, 1.4, fill=STEEL3, close=True, op=0.6)
    o += T(x0 - s0 * sc + 6, Y(0) + 5, f'拉 {s0:.2f}（不計）', 14, MUT, 'start')
    o += P([(x0, Y(d['zc'])), (x0 - d['s4c'] * sc, Y(4)), (x0, Y(4))], TEN, 2, fill=TEN2, close=True)
    o += L(x0 - 140, Y(d['zc']), x0, Y(d['zc']), MUT, 1, '3 3') + T(x0 - 144, Y(d['zc']) + 5, f"*z*_{{c}}={d['zc']:.3f}", 14, KEY, 'end', 'bold')
    o += T(x0 - d['s4c'] * sc - 6, Y(4) - 8, f"{d['s4c']:.2f}", 14, TEN, 'end', 'bold')
    o += P([(x0, Y(4)), (x0 - d['s4s'] * sc, Y(4)), (x0 - d['s8s'] * sc, Y(8)), (x0, Y(8))], TEN, 2, fill=TEN2, close=True)
    xw = x0 - d['s8s'] * sc
    o += P([(x0 - d['s4s'] * sc, Y(4)), (xw - d['u8'] * sc, Y(8)), (xw, Y(8))], AC, 2, fill=AC2, close=True)
    o += T(x0 - d['s4s'] * sc - 6, Y(4) + 22, f"{d['s4s']:.2f}", 14, TEN, 'end', 'bold')
    o += T(x0 - d['s8s'] * sc / 2, Y(8) + 22, f"有效 {d['s8s']:.2f}", 14, TEN, 'middle', 'bold')
    o += T(xw - d['u8'] * sc / 2, Y(8) + 22, f"＋水 {d['u8']:.2f}", 14, AC, 'middle', 'bold')
    o += box(40, 60, 230, 120, '合力（對牆底）', [f"*P*={d['P']:.1f} kN/m", f"*ȳ*={d['ybar']:.3f} m"], KEY2, KEY)
    return svg(W, H, o, '2015-2 分層土壓')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
