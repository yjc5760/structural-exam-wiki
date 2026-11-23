# -*- coding: utf-8 -*-
"""第 3 章：兩個狀態——壓縮鎖 Vs（2007-1）、夯實鎖 Ws 與 w（2004-1）。"""
from plot import *  # noqa
from calcs import *  # noqa


def _bar(o, x, ybot, w, sc, Vs, Vw, Va, lab_r=True):
    y = ybot
    out = {}
    for v, fill, nm in ((Vs, '#d7ccc8', '土粒'), (Vw, AC2, '水'), (Va, '#ffffff', '空氣')):
        h = v * sc
        if h > 0.3:
            o += R(x, y - h, w, h, fill, INK, 1.6)
            if h > 24:
                o += T(x + w / 2, y - h / 2 + 5, nm, 15, INK, 'middle', 'bold')
        out[nm] = (y - h, y)
        y -= h
    return o, out


def fig3_1():
    d = ex2007_1()
    W_, H = 900, 420
    sc = 120          # px per cm
    ybot = 370
    o = ''
    for x, Hh, e, title in ((80, d['H0'], d['e0'], f"壓縮前 *H* = {d['H0']} cm"), (330, d['H1'], d['e1'], f"壓縮後 *H* = {d['H1']} cm")):
        Hs = d['Hs']
        o, cells = _bar(o, x, ybot, 150, sc, Hs, Hh - Hs, 0)
        o += T(x + 75, ybot - Hh * sc - 14, title, 16, INK, 'middle', 'bold')
        o += T(x + 160, (cells['水'][0] + cells['水'][1]) / 2 + 5, f'*e* = {e:.3f}', 15, AC, 'start', 'bold')
    o += L(70, ybot - d['Hs'] * sc, 490, ybot - d['Hs'] * sc, TEN, 2.4, '8 5')
    o += T(495, ybot - d['Hs'] * sc + 5, f"*H*_{{s}} = {d['Hs']:.3f} cm 不變", 15, TEN, 'start', 'bold')
    o += dim(500, ybot - d['H0'] * sc, 500, ybot - d['H1'] * sc, '', COMP, 0)
    o += T(510, ybot - (d['H0'] + d['H1']) / 2 * sc + 5, 'Δ*H* = 0.6 cm 全是水', 15, COMP, 'start', 'bold')
    o += R(650, 280, 240, 110, KEY2, KEY, 1.4, 8)
    o += T(770, 308, '土粒高不變', 15, KEY, 'middle', 'bold')
    o += T(770, 338, 'Δ*H*/*H*_{0} = Δ*e*/(1 + *e*_{0})', 15, INK, 'middle')
    o += T(770, 368, f"Δ*e* = 0.24 × 2.30 = {d['de']:.3f}", 15, INK, 'middle')
    return svg(W_, H, o, 'SM-2007-1 壓縮前後三相圖')


def fig3_2():
    d = ex2004_1()
    W_, H = 900, 360
    sc = 150
    ybot = 320
    o = ''
    for x, e, S, title in ((80, d['e'], d['S'], '夯實前 *S* = 90.3%'), (330, d['e2'], 0.95, '再夯實 *S* = 95%')):
        o, cells = _bar(o, x, ybot, 150, sc, 1.0, S * e, (1 - S) * e)
        top = ybot - (1 + e) * sc
        o += T(x + 75, top - 14, title, 16, INK, 'middle', 'bold')
        o += T(x + 160, top + 6, f'空氣 {(1 - S) * e:.4f}', 14, MUT, 'start')
        o += T(x + 160, (cells['水'][0] + cells['水'][1]) / 2 + 5, f'水 *Se* = {S * e:.3f}', 14, AC, 'start', 'bold')
    o += L(70, ybot - sc, 490, ybot - sc, TEN, 2.4, '8 5')
    o += T(495, ybot - sc + 5, '*V*_{s} = 1、*W*_{s}、*w* 都不變', 15, TEN, 'start', 'bold')
    o += R(650, 210, 240, 120, KEY2, KEY, 1.4, 8)
    o += T(770, 238, '水量不變、只擠空氣', 15, KEY, 'middle', 'bold')
    o += T(770, 268, '*Se* = *wG*_{s} = 0.486 不變', 15, INK, 'middle')
    o += T(770, 298, f"*e*：{d['e']:.3f} → {d['e2']:.3f}", 15, INK, 'middle')
    return svg(W_, H, o, 'SM-2004-1 夯實前後三相圖')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
