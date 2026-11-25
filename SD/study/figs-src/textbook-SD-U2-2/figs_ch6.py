# -*- coding: utf-8 -*-
"""第 6 章：扭轉不規則、動力分析放大、軟層。"""
from sdfig import *  # noqa
from calcs import AX_EX
import math


def fig6_1():
    W, H = 900, 360
    o = T(250, 28, '平面：剛心偏離質心，樓板邊平移又轉動', 15.5, INK, 'middle', 'bold')
    x0, y0, a, b = 120, 90, 260, 200
    o += R(x0, y0, a, b, STEEL2, STEEL, 1.6, 0, '6 4')
    d1, d2 = 24, 60
    pts = [(x0 + d2, y0), (x0 + a + d2, y0), (x0 + a + d1, y0 + b), (x0 + d1, y0 + b)]
    o += P(pts, AC, 2.6, fill='none', close=True)
    o += A(x0 + a, y0 + b + 22, x0 + a + d1, y0 + b + 22, COMP, 2.2, 8, both=True) + T(x0 + a + d1 + 10, y0 + b + 28, 'δ_{1}', 15, COMP, 'start', 'bold')
    o += A(x0 + a, y0 - 14, x0 + a + d2, y0 - 14, COMP, 2.2, 8, both=True) + T(x0 + a + d2 + 10, y0 - 8, 'δ_{2}', 15, COMP, 'start', 'bold')
    o += C(x0 + a / 2, y0 + b / 2, 6, KEY, '#fff', 2) + T(x0 + a / 2 + 12, y0 + b / 2 + 5, 'CM', 14, KEY, 'start')
    o += C(x0 + a / 2, y0 + b * 0.8, 6, TEN, '#fff', 2) + T(x0 + a / 2 + 12, y0 + b * 0.8 + 5, 'CR', 14, TEN, 'start')
    o += A(x0 - 60, y0 + b / 2, x0 - 15, y0 + b / 2, WARN, 2.6, 10) + T(x0 - 64, y0 + b / 2 - 10, '地震', 14, WARN, 'end')
    q = AX_EX
    o += box(520, 50, 370, 290, '判定與放大', ['δ_{avg} = (δ_{1} + δ_{2})/2', '扭轉不規則：δ_{max} > 1.2δ_{avg}', f'例 δ = {q["d1"]}、{q["d2"]}：比值 {q["ratio"]:.3f}', '→ 不規則', '*A*_{x} = (δ_{max}/1.2δ_{avg})²', f'= {q["Ax"]:.3f}（1.0 ≤ *A*_{{x}} ≤ 3.0）', '放大意外偏心 *e*_{a} = ±0.05*D*', '判準是「位移比」，不是偏心距'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '扭轉不規則')


def fig6_2():
    W, H = 900, 300
    o = T(450, 26, '動力分析的總橫力要回頭和靜力比', 16, INK, 'middle', 'bold')
    rows = [('靜力 *V*', 100, AC), ('動力 *V*_{d}（SRSS）', 72, WARN), ('規則：放大到 0.9*V*', 90, KEY), ('不規則：放大到 *V*', 100, COMP)]
    for i, (nm, v, c) in enumerate(rows):
        y = 50 + i * 55
        o += T(300, y + 27, nm, 15, c, 'end', 'bold')
        o += R(315, y + 8, v * 4.5, 30, c, None, 0, 4, op=0.85)
        o += T(320 + v * 4.5, y + 29, f'{v}%', 15, c, 'start', 'bold')
    o += T(450, 290, '所有動力分析的內力、位移乘同一個放大比；動力值較大時用動力值', 14.5, MUT, 'middle')
    return svg(W, H, o, '動力分析下限')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
