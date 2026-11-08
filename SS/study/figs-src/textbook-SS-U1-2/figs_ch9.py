# -*- coding: utf-8 -*-
"""第 9 章：剪力流＝切一刀的水平平衡；SS-2019-4 蓋板斷續銲。"""
from plot import *  # noqa
import calcs

W9 = calcs.ex_2019_4()


def fig9_1():
    W, H = 900, 400
    o = ''
    # (a) 梁段 dx，左 M、右 M+dM
    x0, x1, yt, yb = 80, 330, 90, 290
    o += T((x0 + x1) / 2, 40, '(a) 一小段梁 d*x*', 16, INK, 'middle', 'bold')
    o += R(x0, yt, x1 - x0, yb - yt, STEEL2, INK, 1.4)
    o += R(x0, yt, x1 - x0, 34, COMP2, COMP, 1.6)
    o += L(x0 - 20, (yt + yb) / 2, x1 + 20, (yt + yb) / 2, AC, 1.2, '6 4')
    o += curve_arrow([(x0 - 10, yt + 40), (x0 - 34, (yt + yb) / 2), (x0 - 10, yb - 40)], INK, 2, 9)
    o += curve_arrow([(x1 + 10, yb - 40), (x1 + 34, (yt + yb) / 2), (x1 + 10, yt + 40)], INK, 2.6, 10)
    o += T(x0 - 40, (yt + yb) / 2 + 5, '*M*', 16, INK, 'end', 'bold')
    o += T(x1 + 42, (yt + yb) / 2 + 5, '*M*+d*M*', 16, INK, 'start', 'bold')
    o += L(x0, yt + 34, x1, yt + 34, COMP, 2.2, '4 3')
    o += T((x0 + x1) / 2, yt + 22, '切下這一塊（面積 *A*′）', 14, COMP, 'middle', 'bold')
    o += T((x0 + x1) / 2, yb + 30, 'd*M* = *V*·d*x*', 15, INK, 'middle')
    # (b) 切下的那一塊自由體
    bx0, bx1, by0, by1 = 520, 740, 120, 190
    o += T((bx0 + bx1) / 2, 40, '(b) 切下那一塊的水平平衡', 16, INK, 'middle', 'bold')
    o += R(bx0, by0, bx1 - bx0, by1 - by0, COMP2, COMP, 1.8)
    for k in range(3):
        yy = by0 + 15 + k * 20
        o += A(bx0 - 50, yy, bx0 - 4, yy, COMP, 2, 8)
        o += A(bx1 + 60, yy, bx1 + 4, yy, COMP, 2.6, 9)
    o += T(bx0 - 56, by0 + 38, '*F*', 16, COMP, 'end', 'bold')
    o += T(bx1 + 64, by0 + 38, '*F*+d*F*', 16, COMP, 'start', 'bold')
    for k in range(6):
        xx = bx0 + 14 + k * 36
        o += A(xx + 30, by1 + 8, xx, by1 + 8, WARN, 2.2, 8)
    o += T((bx0 + bx1) / 2, by1 + 34, '切面上的剪力 *q*·d*x*（往回拉）', 15, WARN, 'middle', 'bold')
    o += box(470, 260, 400, 120, '三步', ['*F* = ∫σd*A* = (*M*/*I*)·*Q*　（*Q*＝*A*′ 對中性軸的一次矩）', 'd*F* = (d*M*/*I*)·*Q* = *q*·d*x*', '⇒ *q* = *VQ*/*I*　、　τ = *q*/*t*'], KEY2, KEY, 16, 15)
    return svg(W, H, o, '剪力流的自由體')


def fig9_2():
    W, H = 900, 430
    sc = 5.0
    base, cx = 380, 220
    Y = lambda y: base - y * sc
    o = ''
    # H500×200×9×16 + PL25×300 在上
    o += R(cx - 10 * sc, Y(1.6), 20 * sc, 1.6 * sc, STEEL3, INK, 1.2)
    o += R(cx - 0.45 * sc, Y(48.4), 0.9 * sc, 46.8 * sc, STEEL3, INK, 1.2)
    o += R(cx - 10 * sc, Y(50), 20 * sc, 1.6 * sc, STEEL3, INK, 1.2)
    o += R(cx - 15 * sc, Y(52.5), 30 * sc, 2.5 * sc, COMPM, COMP, 1.8)
    ybar = 35.87
    o += L(cx - 120, Y(ybar), cx + 160, Y(ybar), AC, 1.8, '7 4')
    o += T(cx - 122, Y(ybar) - 8, f'ENA {ybar:.2f}', 14, AC, 'start', 'bold')
    o += T(cx + 84, Y(52.5) + 2, '蓋板 PL25×300', 14, COMP, 'start', 'bold')
    o += T(cx + 84, Y(52.5) + 22, '*Q* = 75 × 15.38 = 1153.5 cm³', 14, COMP, 'start')
    o += dim(cx - 90, Y(ybar), cx - 90, Y(51.25), '', INK, 0)
    o += T(cx - 98, Y((ybar + 51.25) / 2) + 5, '15.38', 14, INK, 'end')
    o += C(cx - 10 * sc, Y(50) - 2, 4, WARN, None) + C(cx + 10 * sc, Y(50) - 2, 4, WARN, None)
    o += T(cx, base + 30, 'H500×200×9×16 ＋ 上蓋板（單位 cm，依比例；y 自 H 底）', 14, MUT, 'middle')
    # 斷續銲平面
    px0, py = 520, 120
    o += T(705, 60, '俯視：雙面斷續銲', 16, INK, 'middle', 'bold')
    o += R(px0, py - 30, 360, 60, COMP2, COMP, 1.4)
    for k in range(4):
        x = px0 + 20 + k * 90
        o += R(x, py - 34, 26, 8, WARN, None, 0, 2) + R(x, py + 26, 26, 8, WARN, None, 0, 2)
    o += dim(px0 + 20, py + 56, px0 + 110, py + 56, '*s* = 15 cm', INK, 0, 14)
    o += T(px0 + 33, py - 44, '*L*', 15, WARN, 'middle', 'bold')
    o += box(520, 220, 360, 150, '一段 *s* 要傳的力 ≤ 銲道能傳的力', [f'*q* = 50×1153.5/75510 = {W9["q"]:.4f} tf/cm', f'*q*·*s* = {W9["Fs"]:.2f} tf', f'2×0.75×0.6×4.9×{W9["te"]:.3f} = {W9["phiRn"]:.3f} tf/cm', f'*L* ≥ {W9["Fs"]:.2f}/{W9["phiRn"]:.3f} = {W9["L"]:.2f} cm → 5 cm'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'SS-2019-4 蓋板斷續銲')


ALL = {'fig9_1': fig9_1, 'fig9_2': fig9_2}
