# -*- coding: utf-8 -*-
"""第 1 章：三項應力疊加。"""
from figs_ps import *  # noqa
from calcs import demo

D = demo()


def fig1_1():
    W, H = 900, 360
    o = T(450, 26, '示範梁（RC-2014-4）：簡支 12 m、對稱 I 形、鋼腱在形心下 19.8 cm', 16, INK, 'middle', 'bold')
    x0, x1, yt = 60, 600, 120
    hb = 60 * 1.6
    o += R(x0, yt, x1 - x0, hb, STEEL2, INK, 1.4)
    yg = yt + hb / 2
    o += L(x0 - 10, yg, x1 + 10, yg, KEY, 1.2, '6 4')
    o += T(x1 + 14, yg + 5, '形心', 14, KEY, 'start')
    ye = yg + 19.8 * 1.6
    o += L(x0, ye, x1, ye, TEN, 3)
    o += A(x0 - 40, ye, x0 - 2, ye, COMP, 3, 11)
    o += A(x1 + 40, ye, x1 + 2, ye, COMP, 3, 11)
    o += T(x0 - 44, ye + 5, '*P*', 16, COMP, 'end', 'bold')
    o += T(x1 + 44, ye + 5, '*P*', 16, COMP, 'start', 'bold')
    o += vdim(x1 - 30, yg, ye, '*e* = 19.8', TEN, -1, 14)
    o += pin(x0 + 6, yt + hb) + pin(x1 - 6, yt + hb)
    for i in range(13):
        xx = x0 + (x1 - x0) * i / 12
        o += A(xx, yt - 40, xx, yt - 3, WARN, 1.6, 8)
    o += T((x0 + x1) / 2, yt - 50, '*w*_{d} = 0.264、*w*_{l} = 1.1 tf/m', 15, WARN, 'middle', 'bold')
    o += T((x0 + x1) / 2, yt + hb + 52, 'L = 12 m', 15, INK, 'middle')
    o += ibeam(780, 110, 2.6)
    o += L(780 - 50, 110 + 30 * 2.6, 780 + 50, 110 + 30 * 2.6, KEY, 1.2, '4 3')
    o += C(780, 110 + (30 + 19.8) * 2.6, 6, TEN, '#fff', 1.4)
    o += T(780, 300, '*A* = 1100、*I* = 469,000', 14, INK, 'middle')
    o += T(780, 320, '*c*_{t} = *c*_{b} = 30 cm', 14, INK, 'middle')
    return svg(W, H, o, '示範梁')


def fig1_2():
    a, b_, c = D['parts1']
    t, bb = D['t1']
    return sum_panels([('*P*_{i}/*A*', a, a), ('*P*_{i}*e*/*S*', -b_, b_), ('*M*_{d}/*S*', c, -c)], (t, bb),
                      '傳遞階段（*P*_{i} = 70 tf、只有自重 *M*_{d} = 4.75 tf·m）：三張圖相加', H=340, k=0.9,
                      note='上緣：63.64 − 88.66 + 30.40 = +5.38（壓）；下緣：63.64 + 88.66 − 30.40 = +121.90（壓）')


def fig1_3():
    a, b_, c = D['parts2']
    t, bb = D['t2']
    return sum_panels([('*P*_{e}/*A*', a, a), ('*P*_{e}*e*/*S*', -b_, b_), ('*M*_{T}/*S*', c, -c)], (t, bb),
                      '使用階段（*P*_{e} = 60 tf、全部載重 *M*_{T} = 24.55 tf·m）', H=340, k=0.45,
                      note=f'上緣：54.55 − 75.99 + 157.05 = +135.60（壓）；下緣：54.55 + 75.99 − 157.05 = {bb:.2f}（拉）')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
