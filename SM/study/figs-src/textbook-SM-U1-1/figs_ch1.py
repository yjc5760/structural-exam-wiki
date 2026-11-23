# -*- coding: utf-8 -*-
"""第 1 章：三相圖（令 Vs = 1）、n 與 e 的關係。"""
from plot import *  # noqa
from calcs import *  # noqa


def phase_bar(o, x, ytop, w, sc, Va, Vw, Vs, labels_l, labels_r, title=''):
    """畫三相柱：由上而下 空氣／水／土粒。回傳 (o, 各格 y 範圍)。"""
    y = ytop
    cells = []
    for v, fill, nm in ((Va, '#ffffff', '空氣'), (Vw, AC2, '水'), (Vs, '#d7ccc8', '土粒')):
        h = v * sc
        if h > 0.5:
            o += R(x, y, w, h, fill, INK, 1.6)
            if h > 22:
                o += T(x + w / 2, y + h / 2 + 5, nm, 15, INK, 'middle', 'bold')
        cells.append((y, y + h))
        y += h
    if title:
        o += T(x + w / 2, ytop - 14, title, 16, INK, 'middle', 'bold')
    for (y0, y1), lab in zip(cells, labels_l):
        if lab and y1 - y0 > 0.5:
            o += L(x - 6, y0, x - 6, y1, MUT, 1)
            o += T(x - 12, (y0 + y1) / 2 + 5, lab, 15, AC, 'end', 'bold')
    for (y0, y1), lab in zip(cells, labels_r):
        if lab and y1 - y0 > 0.5:
            o += T(x + w + 12, (y0 + y1) / 2 + 5, lab, 15, COMP, 'start', 'bold')
    return o, cells


def fig1_1():
    e, S = 0.8, 0.55     # 示意比例
    W_, H = 900, 590
    o = ''
    sc = 200
    o, cells = phase_bar(o, 420, 60, 150, sc, e - S * e, S * e, 1.0,
                         ['*V*_{a} = (1−*S*)*e*', '*V*_{w} = *Se*', '*V*_{s} = 1'],
                         ['*W*_{a} ≈ 0', '*W*_{w} = *Se*γ_{w}', '*W*_{s} = *G*_{s}γ_{w}'],
                         '令 *V*_{s} = 1（比例示意）')
    ytop, ybot = 60, cells[-1][1]
    o += dim(240, ytop, 240, cells[1][1], '*V*_{v} = *e*', KEY, 0, 15, -1)
    o += dim(150, ytop, 150, ybot, '*V* = 1 + *e*', INK, 0, 15, -1)
    o += R(200, 448, 500, 130, KEY2, KEY, 1.4, 8)
    o += T(450, 476, '四個定義（記分母！）', 15, KEY, 'middle', 'bold')
    o += T(450, 504, '*w* = *W*_{w}/*W*_{s}（乾土重）　*S* = *V*_{w}/*V*_{v}', 15, INK, 'middle')
    o += T(450, 532, '*e* = *V*_{v}/*V*_{s}　*n* = *V*_{v}/*V*', 15, INK, 'middle')
    o += T(450, 560, '*G*_{s} = *W*_{s}/(*V*_{s}γ_{w})', 15, INK, 'middle')
    return svg(W_, H, o, '三相圖，令 Vs = 1')


def fig1_2():
    W_, H = 900, 360
    pl = Plot(100, 50, 520, 250, 0, 3, 0, 1)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.25, 0.5, 0.75, 1.0], '*e*', '*n*')
    o += pl.curve(lambda e: e / (1 + e), 0, 3, KEY, 3)
    o += pl.hline(1.0, 0, 3, COMP, 1.4, '6 4')
    o += T(pl.X(3), pl.Y(1.0) - 10, '*n* 永遠 < 1', 15, COMP, 'end', 'bold')
    o += pl.area(lambda e: 1, lambda e: 0, 0.4, 0.9, ACM, 0.25)
    o += T(pl.X(0.65), pl.Y(0.08), '砂', 15, AC, 'middle', 'bold')
    o += pl.area(lambda e: 1, lambda e: 0, 1.0, 2.5, TENM, 0.2)
    o += T(pl.X(1.75), pl.Y(0.08), '軟黏土（可 > 1）', 15, TEN, 'middle', 'bold')
    o += pl.dot(1.0, 0.5, KEY, 5)
    o += T(pl.X(1.0) + 8, pl.Y(0.5) + 22, '*e* = 1 ⇔ *n* = 0.5', 14, KEY, 'start', 'bold')
    o += R(650, 80, 240, 120, KEY2, KEY, 1.4, 8)
    o += T(770, 108, '*V*_{s} = 1 時', 15, KEY, 'middle', 'bold')
    o += T(770, 138, '孔隙 = *e*、總體積 = 1 + *e*', 15, INK, 'middle')
    o += T(770, 170, '*n* = *e*/(1 + *e*)', 17, KEY, 'middle', 'bold')
    return svg(W_, H, o, '孔隙率與孔隙比')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
