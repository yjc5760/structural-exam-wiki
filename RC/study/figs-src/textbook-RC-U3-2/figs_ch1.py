# -*- coding: utf-8 -*-
"""第 1 章：兩本帳。"""
from figs_common import *  # noqa
from calcs import footing

F = footing()


def _footing(x0, y0, w, hf, hs, col_w, soil=True):
    o = ''
    if soil:
        o += R(x0, y0 - hs, w, hs, '#efe6d8', None, 0)
        o += L(x0 - 20, y0 - hs, x0 + w + 20, y0 - hs, '#8d6e63', 1.4, '6 4')
    o += R(x0, y0, w, hf, STEEL2, INK, 1.6)
    o += R(x0 + w / 2 - col_w / 2, y0 - hs - 40, col_w, hs + 40, STEEL3, INK, 1.6)
    return o


def fig1_1():
    W, H = 900, 395
    o = T(450, 24, '同一個基腳，兩本帳', 16, INK, 'middle', 'bold')
    # 左：服務帳
    x0, y0, w, hf, hs = 40, 210, 300, 40, 60
    o += T(x0 + w / 2, 58, '① 服務帳：驗土壤', 16, WARN, 'middle', 'bold')
    o += _footing(x0, y0, w, hf, hs, 30)
    o += A(x0 + w / 2, y0 - hs - 92, x0 + w / 2, y0 - hs - 44, WARN, 3, 11)
    o += T(x0 + w / 2 + 10, y0 - hs - 70, f"*P*_{{D}}+*P*_{{L}} = {F['PD']+F['PL']:.0f} tf", 15, WARN, 'start', 'bold')
    for i in range(5):
        xx = x0 + 30 + i * 60
        if abs(xx - (x0 + w / 2)) < 30:
            continue
        o += A(xx, y0 - hs + 6, xx, y0 + hf - 6, MUT, 1.4, 8)
    o += T(x0 + 6, y0 - hs - 8, f"覆土 {F['Ws']:.2f} tf", 14, '#6d4c41', 'start', 'bold')
    o += T(x0 + w - 6, y0 - hs - 8, f"基腳 {F['Wf']:.2f} tf", 14, MUT, 'end', 'bold')
    for i in range(9):
        xx = x0 + 15 + i * 33.75
        o += A(xx, y0 + hf + 40, xx, y0 + hf + 4, '#6d4c41', 1.8, 8)
    o += T(x0 + w / 2, y0 + hf + 64, f"*q* = {F['q_serv']:.2f} ≤ *q*_{{a}} = {F['qa']:.0f} tf/m²", 15, '#6d4c41', 'middle', 'bold')
    o += T(x0 + w / 2, y0 + hf + 88, '服務載重、含自重與覆土', 14, MUT, 'middle')
    # 右：因數帳
    x0 = 560
    o += T(x0 + w / 2, 58, '② 因數帳：驗混凝土', 16, AC, 'middle', 'bold')
    o += _footing(x0, y0, w, hf, hs, 30, soil=False)
    o += A(x0 + w / 2, y0 - hs - 92, x0 + w / 2, y0 - hs - 44, AC, 3, 11)
    o += T(x0 + w / 2 + 10, y0 - hs - 70, f"*P*_{{u}} = {F['Pu']:.0f} tf", 15, AC, 'start', 'bold')
    for i in range(9):
        xx = x0 + 15 + i * 33.75
        o += A(xx, y0 + hf + 40, xx, y0 + hf + 4, AC, 1.8, 8)
    o += T(x0 + w / 2, y0 + hf + 64, f"*q*_{{u}} = *P*_{{u}}/*A* = {F['qu']:.1f} tf/m²", 15, AC, 'middle', 'bold')
    o += T(x0 + w / 2, y0 + hf + 88, '因數化、不含自重', 14, MUT, 'middle')
    # 中：小方塊
    cx, cy = 450, 230
    o += R(cx - 30, cy - 20, 60, 40, STEEL2, INK, 1.4)
    o += A(cx, cy - 56, cx, cy - 22, MUT, 2, 9)
    o += A(cx, cy + 58, cx, cy + 22, '#6d4c41', 2, 9)
    o += T(cx + 8, cy - 40, '*w*', 15, MUT, 'start', 'bold')
    o += T(cx + 8, cy + 48, '*w*', 15, '#6d4c41', 'start', 'bold')
    o += T(cx, cy + 90, '原地抵銷', 15, KEY, 'middle', 'bold')
    o += T(cx, cy + 112, '不彎、不剪', 14, KEY, 'middle')
    return svg(W, H, o, '兩本帳')


ALL = {'fig1_1': fig1_1}
