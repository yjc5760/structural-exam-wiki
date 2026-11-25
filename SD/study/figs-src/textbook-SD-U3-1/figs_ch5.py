# -*- coding: utf-8 -*-
"""第 5 章：螺箍筋圍束。"""
from sdfig import *  # noqa
from calcs import SP
import math


def fig5_1():
    W, H = 900, 360
    cx, cy, R0 = 200, 190, 140
    Rc = R0 * SP['Dc'] / SP['D']
    o = T(200, 26, '圓柱斷面（2009-4）', 15.5, INK, 'middle', 'bold')
    o += C(cx, cy, R0, STEEL2, STEEL, 1.6)
    o += C(cx, cy, Rc, '#fff', WARN, 3)
    for i in range(9):
        a = 2 * math.pi * i / 9
        o += C(cx + (Rc - 14) * math.cos(a), cy + (Rc - 14) * math.sin(a), 7, INK, INK, 1)
    for i in range(8):
        a = 2 * math.pi * i / 8 + 0.2
        o += A(cx + (Rc + 2) * math.cos(a), cy + (Rc + 2) * math.sin(a), cx + (Rc - 34) * math.cos(a), cy + (Rc - 34) * math.sin(a), COMP, 1.8, 8)
    o += T(cx, cy + 6, '核心 *A*_{c}', 15, KEY, 'middle', 'bold')
    o += T(cx + R0 - 6, cy - R0 + 14, '保護層', 14, MUT, 'start')
    o += T(cx, cy + R0 + 26, f'外徑 {SP["D"]:.0f} cm、核心 {SP["Dc"]:.0f} cm、9-D25、D13@{SP["s"]}', 14, INK, 'middle')
    o += box(400, 40, 490, 300, '保護層剝落掉的強度，用圍束補回來', ['保護層損失：0.85*f*′_{c}(*A*_{g} − *A*_{c})', '圍束側壓（半圓自由體）：*f*_{2} = ρ_{s}*f*_{yt}/2', '核心增加強度 ≈ 4.1*f*_{2}*A*_{c} ≈ 2ρ_{s}*f*_{yt}*A*_{c}', '相等 ⇒ ρ_{s} ≈ 0.41(*A*_{g}/*A*_{c} − 1)*f*′_{c}/*f*_{yt}', '規範取 0.45（含裕度）', f'需求 {SP["req1"]*100:.3f}%、下限 0.12*f*′_{{c}}/*f*_{{yt}} = {SP["req2"]*100:.2f}%', f'實配 π*d*_{{s}}*A*_{{sp}}/(*A*_{{c}}*s*) = {SP["act"]*100:.3f}% ✔'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '螺箍筋圍束')


ALL = {'fig5_1': fig5_1}
