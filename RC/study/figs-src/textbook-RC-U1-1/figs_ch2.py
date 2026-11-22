# -*- coding: utf-8 -*-
"""第 2 章：單筋矩形梁——C = T 推出 a、Mn。"""
from figs_common import *  # noqa
from calcs import demo_beam, mn_rect, sens, beta1

D = demo_beam()


def tri(o, D, y0, sc, title=True):
    """示範梁三聯圖：斷面、應變、內力。"""
    xs, xa, xf = 175, 420, 600
    if title:
        for x, t in ((xs, '斷面'), (xa, '應變（S1、S2）'), (xf + 110, '內力（S3、S5）')):
            o += T(x, y0 - 34, t, 15, INK, 'middle', 'bold')
    o += section(xs, y0, sc, D['b'], D['h'])
    o += bars(xs, y0 + D['d'] * sc, sc, D['b'], 4, 2.54, TEN)
    o += T(xs, y0 + D['d'] * sc + 30, '4-D25　*A*_{s} = 20.27', 14, TEN, 'middle', 'bold')
    o += vdim(xs - D['b'] * sc / 2 - 16, y0, y0 + D['d'] * sc, '*d* = 53', INK, -1)
    o += hdim(xs - D['b'] * sc / 2, xs + D['b'] * sc / 2, y0 + D['h'] * sc + 18, '*b* = 40', INK, 1)
    yc = y0 + D['c'] * sc
    o += L(xs - D['b'] * sc / 2, yc, xf + 120, yc, MUT, 1.1, '6 4')
    s, k, ex = strain_panel(xa, y0, sc, D['h'], D['c'], [(D['d'], D['et'], f"ε_{{t}} = {D['et']:.4f}", TEN)], emax_px=150)
    o += s
    o += T(xa - 10, yc + 18, f"*c* = {D['c']:.2f}", 14, INK, 'end', 'bold')
    # 內力
    wblk = 100
    o += R(xf, y0, wblk, D['a'] * sc, WARN2, WARN, 1.8)
    o += T(xf + wblk / 2, y0 - 8, "0.85*f*′_{c} = 238", 14, WARN, 'middle', 'bold')
    o += vdim(xf - 12, y0, y0 + D['a'] * sc, f"*a* = {D['a']:.2f}", WARN, -1)
    ya = y0 + D['a'] / 2 * sc
    yt = y0 + D['d'] * sc
    o += A(xf + wblk + 95, ya, xf + wblk + 8, ya, COMP, 3.2, 13)
    o += T(xf + wblk + 100, ya + 5, f"*C*_{{c}} = {D['T']/1000:.1f} tf", 15, COMP, 'start', 'bold')
    o += A(xf + wblk + 8, yt, xf + wblk + 95, yt, TEN, 3.2, 13)
    o += T(xf + wblk + 100, yt + 5, f"*T* = {D['T']/1000:.1f} tf", 15, TEN, 'start', 'bold')
    o += vdim(xf + wblk + 30, ya, yt, f"*z* = *d* − *a*/2 = {D['d'] - D['a']/2:.2f}", KEY, 1, weight='bold')
    return o


def fig2_1():
    W, H = 900, 470
    o = T(450, 24, '示範梁的極限狀態：一壓一拉，大小相等，形成力偶（依比例）', 16, INK, 'middle', 'bold')
    o = tri(o, D, 92, 4.6)
    o += T(450, 456, f"*M*_{{n}} = *T*·*z* = {D['T']/1000:.2f} tf × {(D['d']-D['a']/2)/100:.4f} m = {D['Mn']/1e5:.2f} tf·m", 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '單筋三聯圖')


def fig2_2():
    W, H = 900, 420
    pl = Plot(100, 50, 500, 300, 0, 50, 0, 100)
    o = pl.axes([0, 10, 20, 30, 40, 50], [0, 20, 40, 60, 80, 100], '*A*_{s}', '*M*_{n}', size=14)
    o += T(pl.X(50) + 20, pl.Y(0) + 26, '(cm²)', 14, MUT, 'start')
    o += T(pl.X(0) + 30, pl.Y(100) - 10, '(tf·m)', 14, MUT, 'start')
    o += pl.curve(lambda A: A * 4200 * 53 / 1e5, 0, 44.9, MUT, 2, dash='6 4')
    o += T(pl.X(30), pl.Y(30 * 4200 * 53 / 1e5) - 12, '上限 *A*_{s}*f*_{y}*d*（*a* → 0）', 14, MUT, 'end')
    cols = [(210, WARN), (280, AC), (350, TEN)]
    for fc, col in cols:
        Amax = 0.85 * fc * beta1(fc) * 3 / 8 * 53 * 40 / 4200
        o += pl.curve(lambda A, fc=fc: mn_rect(A, fc=fc) / 1e5, 0, Amax, col, 3)
        o += pl.dot(Amax, mn_rect(Amax, fc=fc) / 1e5, col, 5)
        o += T(pl.X(Amax) + 8, pl.Y(mn_rect(Amax, fc=fc) / 1e5) + 5, f"*f*′_{{c}} = {fc}", 14, col, 'start', 'bold')
    o += pl.dot(D['As'], D['Mn'] / 1e5, KEY, 6)
    o += T(pl.X(D['As']) + 10, pl.Y(D['Mn'] / 1e5) + 22, f"示範梁 {D['Mn']/1e5:.2f}", 14, KEY, 'start', 'bold')
    o += box(690, 70, 195, 210, '三條線幾乎疊在一起', ['*f*′_{c} 只透過 *a*/2', '影響力臂；', '線的終點（•）是', '拉力控制上限', '*A*_{s,max}（第 3 章）：', '*f*′_{c} 主要買的是', '「能放多少鋼筋」'], AC2, AC, 15, 14)
    return svg(W, H, o, 'Mn-As')


def fig2_3():
    W, H = 900, 330
    S = sens()
    items = [('*f*_{y}：4200 → 5600', S['fy 4200→5600'], TEN), ('*A*_{s}：+25%', S['As+25%'], TEN), ('*d*：53 → 63', S['d 53→63'], AC),
             ("*f*′_{c}：280 → 350", S['fc 280→350'], WARN), ('*b*：40 → 50', S['b 40→50'], WARN)]
    o = T(450, 24, '示範梁：每次只改一個參數，*M*_{n} 增加多少？', 16, INK, 'middle', 'bold')
    x0, y = 260, 60
    for name, v, col in items:
        o += T(x0 - 12, y + 24, name, 15, INK, 'end')
        w = v * 1600
        o += R(x0, y + 8, w, 26, col, None, 0, 4)
        o += T(x0 + w + 10, y + 27, f'+{v*100:.1f}%', 15, col, 'start', 'bold')
        y += 46
    o += L(x0, 60, x0, y + 6, INK, 1.4)
    o += T(450, 318, '*M*_{n} = *A*_{s}*f*_{y}(*d* − *a*/2)：*A*_{s}、*f*_{y}、*d* 在「外面」，*f*′_{c}、*b* 只躲在 *a*/2 裡', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '敏感度')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
