# -*- coding: utf-8 -*-
"""第 2 章：崩塌機構、側推曲線、塑性彎矩。"""
from sdfig import *  # noqa
from calcs import PA, PB
import math


def _frame(ox, title, top_pin_left):
    o = T(ox + 150, 26, title, 15.5, INK, 'middle', 'bold')
    xl, xr, yb, yt = ox + 60, ox + 240, 300, 100
    D = 34
    o += R(xl - 10 + D, yt - 16, xr - xl + 20, 16, STEEL3, INK, 1.4)
    o += A(xr + 20 + D, yt - 8, xr + 70 + D, yt - 8, COMP, 2.6, 11) + T(xr + 76 + D, yt - 3, '*V*', 16, COMP, 'start', 'bold')
    for x, pinned in ((xl, top_pin_left), (xr, False)):
        o += fixed_wall(x, yb, 46)
        if pinned:
            pts = [(x + D * (3 * s * s - s ** 3) / 2, yb - (yb - yt) * s) for s in [i / 40 for i in range(41)]]
        else:
            pts = [(x + D * (3 * s * s - 2 * s ** 3), yb - (yb - yt) * s) for s in [i / 40 for i in range(41)]]
        o += P(pts, STEEL, 6)
        o += C(x, yb - 4, 8, COMP, '#fff', 2)
        if pinned:
            o += C(x + D, yt + 2, 7, '#fff', INK, 2)
        else:
            o += C(x + D, yt + 6, 8, COMP, '#fff', 2)
    return o


def fig2_1():
    W, H = 900, 360
    o = _frame(0, '(a) 左柱頂鉸接：3*M*_{p}/*L*', True)
    o += L(450, 20, 450, 350, GRID, 1.5)
    o += _frame(450, '(b) 兩柱頂固接：4*M*_{p}/*L*', False)
    o += T(225, 340, '紅點＝塑鉸（3 個）；白圈＝結構鉸', 14, MUT, 'middle')
    o += T(675, 340, '紅點＝塑鉸（4 個）', 14, MUT, 'middle')
    return svg(W, H, o, '兩種剪力房屋的崩塌機構')


def fig2_2():
    W, H = 900, 340
    pl = Plot(90, 40, 520, 250, 0, 0.6, 0, 4.6)
    o = pl.axes([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], [0, 1, 2, 3, 4], 'Δ（*M*_{p}*L*²/*EI*）', '*V*（*M*_{p}/*L*）')
    o += P([pl.pt(a, b) for a, b in PA], AC, 3)
    o += P([pl.pt(a, b) for a, b in PB], COMP, 3)
    for a, b in PA[1:3]:
        o += pl.dot(a, b, AC, 5)
    o += pl.dot(*PB[1], COMP, 5)
    o += T(pl.X(0.45), pl.Y(4.0) - 10, '(b) 24*EI*/*L*³、4*M*_{p}/*L*', 15, COMP, 'middle', 'bold')
    o += T(pl.X(0.45), pl.Y(3.0) + 24, '(a) 15*EI*/*L*³、3*M*_{p}/*L*', 15, AC, 'middle', 'bold')
    o += T(pl.X(0.17) + 8, pl.Y(2.5) + 18, '固-固柱先降伏', 14, AC, 'start')
    o += box(630, 50, 260, 250, '比較', ['頻率比 √(15/24) = 0.791', '崩塌側力比 3/4', '(a) 塑鉸分兩階段出現', '剛度、強度都較低', '(b) 較剛、較強', '但兩柱同時降伏', '設計重點：讓塑鉸', '出現在預定位置'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '側力–位移曲線')


def fig2_3():
    W, H = 900, 300
    o = T(220, 26, '方形斷面全塑性', 15.5, INK, 'middle', 'bold')
    x0, y0, b = 140, 60, 180
    o += R(x0, y0, b, b, STEEL2, INK, 1.6)
    o += L(x0 - 20, y0 + b / 2, x0 + b + 20, y0 + b / 2, KEY, 1.4, '5 4')
    o += R(x0 + b + 40, y0, 60, b / 2, COMP2, COMP, 1.4) + R(x0 + b + 40, y0 + b / 2, 60, b / 2, TEN2, TEN, 1.4)
    o += T(x0 + b + 70, y0 + b / 4 + 5, '−σ_{y}', 15, COMP, 'middle', 'bold') + T(x0 + b + 70, y0 + 3 * b / 4 + 5, '+σ_{y}', 15, TEN, 'middle', 'bold')
    o += dim(x0, y0 + b + 16, x0 + b, y0 + b + 16, '*b*', MUT)
    o += box(470, 40, 420, 240, '*M*_{p} = σ_{y}*Z*', ['每半邊合力 σ_{y} · *b* · *b*/2', '力臂 = *b*/2（兩合力相距）', '*M*_{p} = σ_{y}*b*²/2 · *b*/2 = σ_{y}*b*³/4', '*Z* = *b*³/4（彈性 *S* = *b*³/6）', '形狀因子 *Z*/*S* = 1.5', '固-固柱崩塌剪力 2*M*_{p}/*L*', '固-鉸柱 *M*_{p}/*L*'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '方形斷面塑性彎矩')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
