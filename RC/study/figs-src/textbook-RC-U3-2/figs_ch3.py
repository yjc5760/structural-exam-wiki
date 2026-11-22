# -*- coding: utf-8 -*-
"""第 3 章：三個臨界斷面——剖面與平面。"""
from figs_common import *  # noqa
from calcs import footing

F = footing()


def fig3_1():
    W, H = 900, 610
    o = T(450, 24, '一條從柱面出發的 45° 裂縫，畫出三個臨界斷面', 16, INK, 'middle', 'bold')
    B, c, d, h = F['B'], F['c'], F['d'], F['h']
    sc = 2.4
    x0 = 450 - B * sc / 2 * 0.0  # placeholder
    # 剖面：只畫右半基腳（柱中心到邊緣），比例 2.4 px/cm
    xc = 120
    y0 = 110
    half = B / 2
    o += T(xc + half * sc, 64, '剖面（右半）', 15, INK, 'end', 'bold')
    o += R(xc, y0, half * sc, h * sc, STEEL2, INK, 1.6)
    o += R(xc - 4, y0 - 60, (c / 2) * sc + 4, 60, STEEL3, INK, 1.6)
    ys = y0 + d * sc
    o += L(xc, ys, xc + half * sc, ys, INK, 3)
    xf = xc + c / 2 * sc
    o += L(xf, y0, xf + d * sc, ys, COMP, 3)
    o += T(xf + d * sc * 0.5 + 10, y0 + d * sc * 0.5 - 4, '45° 裂縫', 15, COMP, 'start', 'bold')
    for xx, col, lab in ((xf, INK, '柱面'), (xf + d / 2 * sc, COMP, '*d*/2'), (xf + d * sc, WARN, '*d*')):
        o += L(xx, y0 - 8, xx, y0 + h * sc + 18, col, 1.6, '6 4')
        o += T(xx, y0 + h * sc + 38, lab, 15, col, 'middle', 'bold')
    o += T(xf - 6, y0 + h * sc + 60, '彎矩', 14, INK, 'end')
    o += T(xf + d / 2 * sc, y0 + h * sc + 60, '穿孔', 14, COMP, 'middle')
    o += T(xf + d * sc + 6, y0 + h * sc + 60, '單向剪力', 14, WARN, 'start')
    o += hdim(xf, xc + half * sc, y0 - 20, f"*L* = {F['L']:.0f}", TEN, -1, 15)
    o += vdim(xc + half * sc + 16, y0, ys, f'*d* = {d:.0f}', INK, 1, 15)
    # 平面
    s2 = 0.95
    px, py = 560, 300
    o += T(px, 64, '平面', 15, INK, 'start', 'bold')
    py = 90
    o += R(px, py, B * s2, B * s2, STEEL2, INK, 1.6)
    cx, cy = px + B * s2 / 2, py + B * s2 / 2
    a = (c + d) * s2
    o += R(cx - a / 2, cy - a / 2, a, a, COMP2, COMP, 2.4)
    o += R(cx - c * s2 / 2, cy - c * s2 / 2, c * s2, c * s2, STEEL3, INK, 1.4)
    xd = cx + (c / 2 + d) * s2
    o += L(xd, py, xd, py + B * s2, WARN, 2.2, '7 4')
    o += R(xd, py, (F['L'] - d) * s2, B * s2, WARN2, None, 0, op=0.7)
    o += L(xd, py, xd, py + B * s2, WARN, 2.2, '7 4')
    o += T(xd + (F['L'] - d) * s2 / 2, py + 40, '單向', 14, WARN, 'middle', 'bold')
    o += T(xd + (F['L'] - d) * s2 / 2, py + 60, f"{F['L']-d:.0f}×{B:.0f}", 14, WARN, 'middle')
    o += T(cx, cy + a / 2 + 22, f"*b*_{{o}} = 4(*c*+*d*) = {F['bo']:.0f}", 14, COMP, 'middle', 'bold')
    o += T(px + B * s2 / 2, py + B * s2 + 30, f"*B* = {B:.0f} cm、*c* = {c:.0f} cm", 14, MUT, 'middle')
    # 下方：兩個需求
    by = 420
    o += R(60, by, 380, 170, WARN2, WARN, 1.6, 10)
    o += T(250, by + 30, '單向剪力需求', 16, WARN, 'middle', 'bold')
    o += T(250, by + 64, '*V*_{u1} = *q*_{u}*B*(*L* − *d*)', 16, INK, 'middle', 'bold')
    o += T(250, by + 98, f"= {F['qu']:.0f} × {B/100:.1f} × ({F['L']/100:.2f} − {d/100:.2f})", 15, INK, 'middle')
    o += T(250, by + 128, f"= {F['Vu1']:.2f} tf", 16, WARN, 'middle', 'bold')
    o += R(470, by, 380, 170, COMP2, COMP, 1.6, 10)
    o += T(660, by + 30, '穿孔剪力需求', 16, COMP, 'middle', 'bold')
    o += T(660, by + 64, '*V*_{u2} = *P*_{u} − *q*_{u}(*c*+*d*)^{2}', 16, INK, 'middle', 'bold')
    o += T(660, by + 98, f"= {F['Pu']:.0f} − {F['qu']:.0f} × {(c+d)/100:.2f}^{{2}}", 15, INK, 'middle')
    o += T(660, by + 128, f"= {F['Vu2']:.2f} tf", 16, COMP, 'middle', 'bold')
    return svg(W, H, o, '三個臨界斷面')


ALL = {'fig3_1': fig3_1}
