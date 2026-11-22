# -*- coding: utf-8 -*-
"""第 2 章：柱面彎矩——倒懸臂。"""
from figs_common import *  # noqa
from calcs import footing

F = footing()


def fig2_1():
    W, H = 900, 420
    o = T(450, 24, '把基腳翻過來：柱面是固定端，土壓是均佈載重', 16, INK, 'middle', 'bold')
    sc = 0.85
    B, c, Lc = F['B'], F['c'], F['L']
    # 左：剖面
    x0, y0 = 30, 150
    o += R(x0, y0, B * sc, 40, STEEL2, INK, 1.6)
    o += R(x0 + (B - c) / 2 * sc, y0 - 70, c * sc, 70, STEEL3, INK, 1.6)
    for i in range(9):
        xx = x0 + 8 + i * (B * sc - 16) / 8
        o += A(xx, y0 + 90, xx, y0 + 44, AC, 1.8, 8)
    o += T(x0 + B * sc / 2, y0 + 112, f"*q*_{{u}} = {F['qu']:.0f} tf/m²", 15, AC, 'middle', 'bold')
    xf = x0 + (B + c) / 2 * sc
    o += L(xf, y0 - 76, xf, y0 + 46, COMP, 1.6, '5 4')
    o += hdim(xf, x0 + B * sc, y0 - 22, f'*L* = {Lc:.0f}', TEN, -1, 15)
    o += T(xf, y0 + 140, '柱面', 15, COMP, 'middle', 'bold')
    o += T(x0 + B * sc / 2, 70, '① 剖面', 15, INK, 'middle', 'bold')
    # 中：翻過來的懸臂
    x1, y1 = 330, 150
    lw = Lc * sc * 1.2
    o += T(x1 + lw / 2 + 20, 70, '② 翻過來＝懸臂', 15, INK, 'middle', 'bold')
    o += R(x1, y1 - 60, 20, 140, STEEL3, INK, 1.4)
    for k in range(6):
        o += L(x1, y1 - 60 + k * 28, x1 - 10, y1 - 50 + k * 28, INK, 1)
    o += R(x1 + 20, y1, lw, 30, STEEL2, INK, 1.6)
    for i in range(7):
        xx = x1 + 30 + i * (lw - 20) / 6
        o += A(xx, y1 - 40, xx, y1 - 4, AC, 1.8, 8)
    pts = [(x1 + 20, y1 + 60)]
    for i in range(41):
        t = i / 40
        pts.append((x1 + 20 + lw * t, y1 + 60 + 70 * (1 - t) ** 2))
    pts.append((x1 + 20 + lw, y1 + 60))
    o += P(pts, COMP, 2, fill=COMP2, close=True)
    o += T(x1 + 30, y1 + 150, f"*M*_{{u}} = {F['Mu']:.2f} tf·m", 15, COMP, 'start', 'bold')
    o += T(x1 + 30, y1 + 172, '（固定端最大）', 14, COMP, 'start')
    # 右：平面
    x2, y2, s2 = 640, 90, 0.75
    o += T(x2 + B * s2 / 2, 70, '③ 平面', 15, INK, 'middle', 'bold')
    o += R(x2, y2, B * s2, B * s2, STEEL2, INK, 1.6)
    o += R(x2 + (B + c) / 2 * s2, y2, Lc * s2, B * s2, TEN2, TEN, 2)
    o += R(x2 + (B - c) / 2 * s2, y2 + (B - c) / 2 * s2, c * s2, c * s2, STEEL3, INK, 1.4)
    o += T(x2 + (B + c) / 2 * s2 + Lc * s2 / 2, y2 + B * s2 / 2 + 5, '*q*_{u}*BL*', 15, TEN, 'middle', 'bold')
    o += hdim(x2 + (B + c) / 2 * s2, x2 + B * s2, y2 + B * s2 + 16, f'*L*', TEN, 1, 15)
    o += vdim(x2 - 14, y2, y2 + B * s2, f'*B* = {B:.0f}', INK, -1, 15)
    o += T(x2 + B * s2 / 2, y2 + B * s2 + 70, '整條寬 *B* 都算到柱面', 14, MUT, 'middle')
    return svg(W, H, o, '倒懸臂')


ALL = {'fig2_1': fig2_1}
