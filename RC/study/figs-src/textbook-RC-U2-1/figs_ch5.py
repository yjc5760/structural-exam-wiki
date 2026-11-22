# -*- coding: utf-8 -*-
"""第 5 章：耐震剪力鏈——梁自由體、地震剪力佔比。"""
from figs_common import *  # noqa
from calcs import p2025_2, p2016_2
import math

P25 = p2025_2()
P16 = p2016_2()


def _moment_arc(cx, cy, r, cw, col):
    """畫一個彎矩弧箭頭；cw=True 順時針。"""
    a0, a1 = (200, 340) if cw else (340, 200)
    pts = []
    n = 24
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return curve_arrow(pts, col, 2.4, 11)


def fig5_1():
    W, H = 900, 440
    o = T(450, 24, '梁兩端都形成塑鉸時：剪力由 *M*_{pr} 和重力決定', 16, INK, 'middle', 'bold')
    x0, x1, y0, hb = 150, 750, 120, 60
    o += R(x0, y0, x1 - x0, hb, STEEL2, INK, 1.6)
    for i in range(13):
        xx = x0 + 20 + i * 46.6
        o += A(xx, y0 - 40, xx, y0 - 4, MUT, 1.4, 8)
    o += T(450, y0 - 50, f"*w*_{{u}} = {P25['wu']:.1f} tf/m（1.2*D* + 1.0*L*）", 15, MUT, 'middle', 'bold')
    o += _moment_arc(x0, y0 + hb / 2, 46, True, KEY)
    o += _moment_arc(x1, y0 + hb / 2, 46, True, KEY)
    o += T(x0 - 16, y0 + hb + 30, f"*M*_{{pr}}^{{+}} = {P25['Mpr_pos']/1e5:.2f}", 15, KEY, 'end', 'bold')
    o += T(x1 + 16, y0 + hb + 30, f"*M*_{{pr}}^{{−}} = {P25['Mpr_neg']/1e5:.2f}", 15, KEY, 'start', 'bold')
    o += T(x0 - 16, y0 + hb + 52, '(tf·m)', 14, KEY, 'end')
    o += T(x1 + 16, y0 + hb + 52, '(tf·m)', 14, KEY, 'start')
    # 剪力反力（順時針塑鉸彎矩 → 左端向下、右端向上）
    vl = P25['Vseis'] / 1000 - P25['Vgrav'] / 1000
    o += A(x0 + 30, y0 + hb + 4, x0 + 30, y0 + hb + 100, AC, 2.4, 10)
    o += T(x0 + 40, y0 + hb + 80, f'{vl:.2f} tf', 15, AC, 'start', 'bold')
    o += A(x1 - 30, y0 + hb + 100, x1 - 30, y0 + hb + 4, AC, 2.4, 10)
    o += T(x1 - 40, y0 + hb + 80, f"*V*_{{e}} = {P25['Ve']/1000:.2f} tf", 15, AC, 'end', 'bold')
    o += hdim(x0, x1, y0 + hb + 130, f"*l*_{{n}} = {P25['ln']/100:.0f} m", INK, -1, 15)
    # 剪力組成
    vs, vg = P25['Vseis'] / 1000, P25['Vgrav'] / 1000
    o += R(230, 330, 440, 98, '#fff', AC, 1.6, 9)
    o += T(450, 356, f'地震剪力 (Σ*M*_{{pr}})/*l*_{{n}} = {vs:.2f} tf（兩端相同）', 15, KEY, 'middle', 'bold')
    o += T(450, 382, f'重力剪力 *w*_{{u}}*l*_{{n}}/2 = {vg:.2f} tf（一端加、一端減）', 15, MUT, 'middle', 'bold')
    o += T(450, 410, f"控制端 *V*_{{e}} = {vs:.2f} + {vg:.2f} = {P25['Ve']/1000:.2f} tf", 16, AC, 'middle', 'bold')
    return svg(W, H, o, '梁自由體 Ve')


def fig5_2():
    W, H = 900, 330
    o = T(450, 24, '地震剪力佔總剪力幾成？過一半（且軸壓小）塑鉸區 *V*_{c} = 0', 16, INK, 'middle', 'bold')
    x0, w = 210, 560
    rows = [('RC-2025-2', P25['ratio'], P25['Vseis'] / 1000, P25['Ve'] / 1000, COMP, '→ *V*_{c} = 0'),
            ('RC-2016-2', P16['ratio'], P16['Vseis'] / 1000, P16['Ve'] / 1000, TEN, '→ *V*_{c} 可計入')]
    for i, (lab, r, vs, ve, col, res) in enumerate(rows):
        y = 80 + i * 100
        o += T(x0 - 14, y + 26, lab, 16, INK, 'end', 'bold')
        o += R(x0, y, w, 40, STEEL2, INK, 1.2)
        o += R(x0, y, w * r, 40, col, None, 0, 0, op=0.85)
        o += T(x0 + w * r - 8, y + 26, f'{r*100:.1f}%', 16, '#fff', 'end', 'bold')
        o += T(x0 + w * r + (8 if r < 0.7 else -80), y + 62, f'{vs:.2f} / {ve:.2f} tf', 14, col, 'start', 'bold')
        o += T(x0 + w + 12, y + 26, res, 15, col, 'start', 'bold')
    o += L(x0 + w * 0.5, 64, x0 + w * 0.5, 290, KEY, 2.2, '6 4')
    o += T(x0 + w * 0.5, 306, '門檻 50%', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'Vc=0 判斷')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
