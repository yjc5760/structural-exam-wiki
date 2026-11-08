# -*- coding: utf-8 -*-
"""第 12 章：合成梁塑性應力分布（SS-2019-2）、PNA 三種位置。"""
from plot import *  # noqa
import calcs

CP = calcs.ex_comp()


def fig12_1():
    W, H = 900, 470
    o = ''
    sc = 5.4                    # px/cm（縱向）
    sx = 1.2                    # px/cm（版寬縮小顯示）
    top, cx = 60, 230
    Y = lambda y: top + y * sc              # y 自版頂往下
    # 版（寬 250 cm 縮小顯示）
    o += R(cx - 125 * sx, Y(0), 250 * sx, 15 * sc, '#eceff1', INK, 1.4)
    o += T(cx, Y(0) - 10, f'混凝土版 *b*_{{e}} = 250 cm（寬度縮小顯示）、*t*_{{s}} = 15 cm', 14, INK, 'middle')
    # 鋼梁 H500×200×10×16（真實比例）
    bx = 2.4
    o += R(cx - 10 * bx * 2.5 / 2.5, Y(15), 20 * bx, 1.6 * sc, STEEL3, INK, 1.2)
    o += R(cx - 0.5 * bx * 2, Y(16.6), 1.0 * bx * 2, 46.8 * sc, STEEL3, INK, 1.2)
    o += R(cx - 10 * bx, Y(63.4), 20 * bx, 1.6 * sc, STEEL3, INK, 1.2)
    o += T(cx + 40, Y(40), 'H500×200×10×16', 14, INK, 'start')
    # PNA
    a = CP['a']
    o += L(cx - 170, Y(a), cx + 520, Y(a), KEY, 1.8, '7 4')
    o += T(cx - 172, Y(a) + 18, f'PNA（版內 *a* = {a:.2f} cm）', 14, KEY, 'start', 'bold')
    # 應力塊
    x0 = 540
    o += L(x0, Y(-4), x0, Y(69), INK, 1.3)
    o += R(x0 - 70, Y(0), 70, a * sc, COMPM, COMP, 1.6)
    o += T(x0 - 76, Y(a / 2) + 5, '0.85*f*′_{c}', 14, COMP, 'end', 'bold')
    o += R(x0, Y(15), 70, 50 * sc, TENM, TEN, 1.6)
    o += T(x0 + 35, Y(60) + 5, '*F*_{y}', 15, TEN, 'middle', 'bold')
    # 合力
    o += A(x0 + 150, Y(a / 2), x0 + 30, Y(a / 2), COMP, 2.6, 11)
    o += T(x0 + 156, Y(a / 2) + 5, f'*C* = {CP["T"]:.0f} tf', 15, COMP, 'start', 'bold')
    o += A(x0 + 30, Y(40), x0 + 150, Y(40), TEN, 2.6, 11)
    o += T(x0 + 156, Y(40) + 5, f'*T* = *A*_{{s}}*F*_{{y}} = {CP["T"]:.0f} tf', 15, TEN, 'start', 'bold')
    o += dim(x0 + 120, Y(a / 2), x0 + 120, Y(40), '', INK, 0)
    o += T(x0 + 128, Y((a / 2 + 40) / 2) + 5, f'{CP["arm"]:.2f} cm', 15, INK, 'start', 'bold')
    o += box(630, Y(47), 260, 72, f'*M*_{{n}} = {CP["T"]:.0f} × {CP["arm"]:.2f} = {CP["Mn"]:.0f} tf·cm', [f'≈ {CP["Mn"] / 100:.1f} tf·m（φ*M*_{{n}} = {CP["phiMn"] / 100:.1f}）'], KEY2, KEY, 16, 15)
    return svg(W, H, o, '合成梁塑性應力分布')


def fig12_2():
    W, H = 900, 300
    o = ''
    cases = [('① PNA 在版內', '*A*_{s}*F*_{y} ≤ 0.85*f*′_{c}*b*_{e}*t*_{s}', 0.4, TEN),
             ('② PNA 在上翼板', '鋼的一部分也受壓', 1.12, WARN),
             ('③ PNA 在腹板', '版很薄、鋼梁很大', 1.6, COMP)]
    for i, (t, s, pna, c) in enumerate(cases):
        ox = 40 + i * 290
        o += T(ox + 110, 30, t, 16, c, 'middle', 'bold')
        o += T(ox + 110, 54, s, 14, MUT, 'middle')
        top = 80
        o += R(ox + 20, top, 180, 30, '#eceff1', INK, 1.2)            # 版（相對高 1）
        o += R(ox + 80, top + 30, 60, 8, STEEL3, INK, 1.2)
        o += R(ox + 106, top + 38, 8, 110, STEEL3, INK, 1.0)
        o += R(ox + 80, top + 148, 60, 8, STEEL3, INK, 1.2)
        yp = top + pna * 30
        o += L(ox + 10, yp, ox + 210, yp, KEY, 2, '6 4')
        o += T(ox + 214, yp + 5, 'PNA', 14, KEY, 'start', 'bold')
        o += T(ox + 110, top + 186, ['混凝土部分受壓', '混凝土全壓＋鋼翼板部分壓', '混凝土全壓＋鋼上半壓'][i], 14, INK, 'middle')
    o += T(W / 2, 290, '判斷方法：比較 *A*_{s}*F*_{y}（鋼全拉）與 0.85*f*′_{c}*b*_{e}*t*_{s}（版全壓）誰大——SS-2019-2 屬於 ①', 15, KEY, 'middle', 'bold')
    return svg(W, H + 10, o, 'PNA 三種位置')


ALL = {'fig12_1': fig12_1, 'fig12_2': fig12_2}
