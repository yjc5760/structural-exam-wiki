# -*- coding: utf-8 -*-
"""第 5 章：組合斷面。"""
from figs_ps import *  # noqa
from calcs import rc2006_4

RR = rc2006_4()


def fig5_1():
    W, H = 900, 400
    o = T(450, 26, 'RC-2006-4：把 *f*′_{c} = 280 的版換算成梁的混凝土（*n* = √(280/350) = 0.894）', 16, INK, 'middle', 'bold')
    sc = 3.2; xc = 260; ytop = 70
    o += R(xc - 50 * sc, ytop, 100 * sc, 15 * sc, '#fff8e1', WARN, 1.4, dash='6 4')
    o += T(xc - 50 * sc - 6, ytop + 30, '實際版 100', 14, WARN, 'end')
    bt = RR['bt']
    o += R(xc - bt / 2 * sc, ytop, bt * sc, 15 * sc, WARN2, WARN, 2)
    o += T(xc, ytop + 30, f'換算寬 {bt:.2f}', 14, WARN, 'middle', 'bold')
    o += R(xc - 15 * sc, ytop + 15 * sc, 30 * sc, 80 * sc, STEEL2, INK, 1.6)
    yb = ytop + 95 * sc
    yg = yb - RR['yb'] * sc
    o += L(xc - 70 * sc / 2 - 40, yg, xc + 180, yg, KEY, 1.4, '6 4')
    o += T(xc + 184, yg + 5, f"合成形心 *ȳ*_{{b}} = {RR['yb']:.2f}", 14, KEY, 'start', 'bold')
    yg1 = yb - 40 * sc
    o += L(xc - 30, yg1, xc + 120, yg1, MUT, 1.2, '3 3')
    o += T(xc + 124, yg1 + 5, '梁單獨形心 40', 14, MUT, 'start')
    o += C(xc, yb - 15 * sc, 6, TEN, '#fff', 1.4)
    o += T(xc - 14, yb - 15 * sc + 5, '鋼腱 15', 14, TEN, 'end')
    o += box(560, 230, 330, 150, '合成斷面性質', [f"*I*_{{c}} = {RR['Ic']:,.0f} cm⁴", f"梁頂 *S* = *I*_{{c}}/{80 - RR['yb']:.2f} = {RR['Stop']:,.0f}", f"梁底 *S* = *I*_{{c}}/{RR['yb']:.2f} = {RR['Sbot']:,.0f}"], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '轉換斷面')


def fig5_2():
    s1 = RR['s1']
    return sum_panels([('第 1 階段（梁單獨）', s1[0], s1[1]), ('活載（合成斷面）', RR['dtop'], RR['dbot'])], (RR['top'], RR['bot']),
                      'RC-2006-4：*P*_{e}＋梁重＋版重在梁單獨斷面，活載 50 tf·m 在合成斷面（梁頂／梁底）', H=340, k=0.55,
                      note=f"梁頂 {RR['top']:.1f}、梁底 {RR['bot']:.1f}（都受壓）→ U 類")


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
