# -*- coding: utf-8 -*-
"""第 3 章：平行滲流的等勢線、自由水層水力坡降、2014-1。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig3_1():
    W_, H = 900, 530
    be = 25
    t = math.tan(r(be))
    x0, y0, xe = 30, 320, 600
    ys = lambda x: y0 - (x - x0) * t
    o = ''
    zw, zz = 70, 230
    o += P([(x0, ys(x0)), (xe, ys(xe)), (xe, ys(xe) + zz), (x0, ys(x0) + zz)], SOILE, 1.4, fill=SOIL, close=True)
    o += P([(x0, ys(x0) + zw), (xe, ys(xe) + zw), (xe, ys(xe) + zz), (x0, ys(x0) + zz)], None, fill=AC2, close=True, op=0.9)
    o += L(x0, ys(x0) + zw, xe, ys(xe) + zw, AC, 2.4)
    o += T(xe - 6, ys(xe) + zw - 8, '地下水位（平行坡面）', 14, AC, 'end', 'bold')
    o += L(x0, ys(x0) + zz, xe, ys(xe) + zz, COMP, 2.6, '9 5')
    o += T(x0 + 260, ys(x0 + 260) + zz + 24, '滑動面', 15, COMP, 'start', 'bold')
    # flow arrows along slope
    for xx in (120, 230):
        yy = ys(xx) + 160
        o += A(xx + 70, yy - 70 * t, xx, yy, AC, 2, 9)
    o += T(150, ys(150) + 196, '流線（平行坡面）', 14, AC, 'start')
    # point A on slip surface
    xA = 420
    yA = ys(xA) + zz
    yW = ys(xA) + zw                    # water table directly above A
    hw = yA - yW
    o += C(xA, yA, 6, KEY, '#fff', 2)
    o += T(xA + 10, yA + 22, 'A', 16, KEY, 'start', 'bold')
    o += L(xA, yA, xA, yW, INK, 1.6, '4 3')
    o += dim(xA - 16, yW, xA - 16, yA, '', INK, 0)
    o += T(xA - 26, (yA + yW) / 2 + 5, '*h*_{w}', 16, INK, 'end', 'bold')
    # equipotential: perpendicular to slope through A
    d = hw * math.cos(r(be))      # perpendicular distance A to WT
    nx, ny = math.sin(r(be)), -math.cos(r(be))   # up-normal (toward surface)
    xB, yB = xA + nx * d, yA + ny * d
    o += L(xA - nx * 20, yA - ny * 20, xA + nx * (d + 60), yA + ny * (d + 60), KEY, 2.4)
    o += C(xB, yB, 6, KEY, '#fff', 2)
    o += T(xB + 10, yB - 8, 'B（水位上，*u* = 0）', 15, KEY, 'start', 'bold')
    o += T(xA + nx * (d + 60) + 6, yA + ny * (d + 60), '等勢線 ⊥ 流線', 15, KEY, 'start', 'bold')
    # vertical rise from A to B
    o += L(xB, yB, xB, yA, WARN, 2, '5 3')
    o += L(xA, yA, xB, yA, WARN, 1.2, '2 3')
    o += T(xB + 8, yB + 46, '*h*_{w} cos²β', 16, WARN, 'start', 'bold')
    o += R(660, 120, 230, 190, KEY2, KEY, 1.4, 8)
    o += T(775, 148, '同一條等勢線上', 15, KEY, 'middle', 'bold')
    o += T(775, 176, '*h*_{A} = *h*_{B}', 15, INK, 'middle')
    o += T(775, 204, '*z*_{A} + *u*_{A}/γ_{w} = *z*_{B}', 15, INK, 'middle')
    o += T(775, 234, '*u*_{A} = γ_{w}(*z*_{B} − *z*_{A})', 15, INK, 'middle')
    o += T(775, 268, '= γ_{w}*h*_{w} cos²β', 17, KEY, 'middle', 'bold')
    return svg(W_, H, o, '平行坡面滲流的孔隙水壓')


def fig3_2():
    d = ex2024_2()
    W_, H = 900, 360
    th = d['theta']
    o = ''
    x0, y0, Lp = 90, 300, 420
    x1, y1 = x0 + Lp * cos(th), y0 - Lp * sin(th)
    o += P([(x0, y0), (x1, y1), (x1, y0)], AC, 1.4, fill=AC2, close=True)
    o += A(x1 - 30 * cos(th), y1 + 30 * sin(th), x0 + 40 * cos(th), y0 - 40 * sin(th), AC, 3, 13)
    o += T((x0 + x1) / 2 - 20, (y0 + y1) / 2 - 18, '流動路徑長 *L*（水面上 *u* = 0）', 15, AC, 'end', 'bold')
    o += dim(x1 + 22, y1, x1 + 22, y0, 'Δ*h* = *L* sin θ', INK, 0, 15, 1)
    o += T((x0 + x1) / 2, y0 + 26, '*L* cos θ（水平，不是流動長度）', 14, MUT, 'middle')
    o += T(x0 + 64, y0 - 10, 'θ', 17, INK, 'middle', 'bold')
    o += R(640, 70, 250, 190, KEY2, KEY, 1.4, 8)
    o += T(765, 100, '*i* = Δ*h* / *L*', 17, KEY, 'middle', 'bold')
    o += T(765, 134, '= sin θ', 17, KEY, 'middle', 'bold')
    o += T(765, 170, f"θ = 30° → *i* = {d['i']:.2f}", 15, INK, 'middle')
    o += T(765, 204, f"錯：tan θ = {d['i_wrong']:.3f}", 15, COMP, 'middle', 'bold')
    o += T(765, 236, '（除錯了長度）', 14, COMP, 'middle')
    return svg(W_, H, o, '自由水層的水力坡降')


def fig3_3():
    d = ex2014_1()
    W_, H = 900, 380
    pl = Plot(110, 50, 460, 260, 0, 3, 0, 2.2)
    o = pl.axes([], [0, 0.5, 1.0, 1.5, 2.0], '', 'FS')
    items = [(d['FS_dry'], TENM, '沒有水（對照）'), (d['FS'], KEY2, '平行滲流 cos²β（正解）'), (d['FS_wrong_u'], COMPM, '*u* = γ_{w}*h*_{w}（錯）')]
    for i, (v, c, lab) in enumerate(items):
        x = 0.5 + i
        o += R(pl.X(x - 0.3), pl.Y(v), pl.X(x + 0.3) - pl.X(x - 0.3), pl.Y(0) - pl.Y(v), c, INK, 1.2)
        o += T(pl.X(x), pl.Y(v) - 8, f'{v:.2f}', 17, KEY if i == 1 else INK, 'middle', 'bold')
        o += T(pl.X(x), pl.Y(0) + 24, lab, 14, INK, 'middle')
    o += pl.hline(1.0, 0, 3, COMP, 1.4, '6 4')
    o += R(610, 60, 280, 230, '#fff', STEEL, 1.2, 8)
    o += T(750, 88, 'SM-2014-1 滑動面上', 15, INK, 'middle', 'bold')
    o += T(750, 118, f"σ_{{v}} = {d['sv']:.2f} kPa", 15, INK, 'middle')
    o += T(750, 146, f"*u* = {d['u']:.2f} kPa", 15, AC, 'middle')
    o += T(750, 174, f"σ_{{n}}′ = {d['sn']:.2f} kPa", 15, AC, 'middle')
    o += T(750, 202, f"τ = {d['tau']:.2f} kPa", 15, COMP, 'middle')
    o += T(750, 230, f"τ_{{f}} = {d['tf']:.2f} kPa", 15, TEN, 'middle')
    o += T(750, 266, f"FS = {d['FS']:.2f}", 17, KEY, 'middle', 'bold')
    return svg(W_, H, o, 'SM-2014-1 安全係數比較')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
