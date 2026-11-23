# -*- coding: utf-8 -*-
"""第 4 章：Peck 三型、2015-3 等值化與包絡線、2011-4 鉸接法。"""
from plot import *  # noqa
from calcs import *  # noqa


def _env(x0, y0, h, w, kind, c, fill):
    if kind == 'sand':
        pts = [(x0, y0), (x0 - w, y0), (x0 - w, y0 + h), (x0, y0 + h)]
    elif kind == 'soft':
        pts = [(x0, y0), (x0 - w, y0 + 0.25 * h), (x0 - w, y0 + h), (x0, y0 + h)]
    else:
        pts = [(x0, y0), (x0 - w, y0 + 0.25 * h), (x0 - w, y0 + 0.75 * h), (x0, y0 + h)]
    return P(pts, c, 2.2, fill=fill, close=True)


def fig4_1():
    W, H = 900, 400
    o = ''
    items = [('sand', '砂', '0.65*γHK*_{a}', '全深定值', AC, AC2),
             ('soft', '軟～中等黏土 *N*_{s}>4', 'max(*γH*−4*c*_{u}, 0.3*γH*)', '0.25*H* 後到底', COMP, COMP2),
             ('hard', '硬裂縫黏土 *N*_{s}≤4', '(0.2～0.4)*γH*', '上下 0.25*H* 漸變', TEN, TEN2)]
    for k, (kind, nm, eq, note, c, fl) in enumerate(items):
        x0 = 230 + k * 290
        y0, h, w = 70, 240, 110
        o += L(x0, y0 - 10, x0, y0 + h + 10, STEEL, 5)
        o += _env(x0, y0, h, w, kind, c, fl)
        o += T(x0 - 60, 40, nm, 15, c, 'middle', 'bold')
        o += T(x0 - 60, y0 + h + 36, eq, 15, c, 'middle', 'bold')
        o += T(x0 - 60, y0 + h + 58, note, 14, INK, 'middle')
        if kind != 'sand':
            o += L(x0 - w - 6, y0 + 0.25 * h, x0 - w - 20, y0 + 0.25 * h, MUT, 1) + T(x0 - w - 22, y0 + 0.25 * h + 5, '0.25*H*', 14, MUT, 'end')
        if kind == 'hard':
            o += T(x0 - w - 22, y0 + 0.75 * h + 5, '0.75*H*', 14, MUT, 'end')
    return svg(W, H, o, 'Peck 三型')


def fig4_2():
    d = ex2015_3()
    W, H = 900, 440
    o = ''
    Y = lambda z: 50 + z * 38
    # 左：土層
    o += R(60, Y(0), 160, Y(3) - Y(0), '#fff8e1', MUT, 1) + T(140, Y(1.5) + 5, '砂 3 m', 15, INK, 'middle', 'bold')
    o += T(140, Y(1.5) + 26, '*γ*=16.5、*φ*=32°', 14, INK, 'middle')
    o += R(60, Y(3), 160, Y(8) - Y(3), '#ede7f6', MUT, 1) + T(140, Y(5.5) + 5, '黏土 5 m', 15, INK, 'middle', 'bold')
    o += T(140, Y(5.5) + 26, '*γ*=17.5、*c*_{u}=30', 14, INK, 'middle')
    o += A(230, Y(4), 290, Y(4), KEY, 2.4, 11)
    o += box(295, Y(2.6), 175, 120, '等值', [f"*γ̄*={d['gbar']:.3f}", f"*c̄*_{{u}}={d['cubar']:.2f}", f"*N*_{{s}}={d['Ns']:.2f}>4"], KEY2, KEY)
    # 右：包絡線
    x0, sc = 760, 3.4
    o += L(x0, Y(0), x0, Y(8), STEEL, 6)
    pa = d['pa']
    o += P([(x0, Y(0)), (x0 - pa * sc, Y(2)), (x0 - pa * sc, Y(8)), (x0, Y(8))], COMP, 2.6, fill=COMP2, close=True)
    o += P([(x0, Y(0)), (x0 - pa * sc, Y(2)), (x0 - pa * sc, Y(6)), (x0, Y(8))], MUT, 1.8, dash='6 4')
    o += T(x0 - pa * sc - 8, Y(2) + 5, f'{pa:.1f}', 15, COMP, 'end', 'bold')
    o += T(x0 - pa * sc - 8, Y(8) + 5, f'{pa:.1f}（到底）', 15, COMP, 'end', 'bold')
    o += T(x0 + 10, Y(2) + 5, '2 m', 14, MUT) + T(x0 + 10, Y(8) + 5, '8 m', 14, MUT)
    o += T(x0 - pa * sc / 2, Y(5), f"*P*={d['P']:.2f}", 15, COMP, 'middle', 'bold')
    o += T(x0 - pa * sc / 2, Y(5) + 22, 'kN/m', 14, COMP, 'middle')
    o += T(x0 - pa * sc - 10, Y(6.4), f"灰虛線（錯：硬黏土型）{d['P_wrong']:.1f}", 14, MUT, 'end')
    o += T(560, Y(8) + 36, 'max(137.0−4×24.55, 0.3×137.0) = 41.1', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '2015-3 等值化與包絡線')


def fig4_3():
    d = ex2011_4()
    W, H = 900, 470
    o = ''
    x0, y0, zs, sc = 470, 50, 52, 3.4
    Y = lambda z: y0 + z * zs
    p = d['pa']
    o += P([(x0, Y(0)), (x0 - p * sc, Y(1.75)), (x0 - p * sc, Y(7)), (x0, Y(7))], COMP, 2, fill=COMP2, close=True)
    o += L(x0, Y(0), x0, Y(7.6), STEEL, 6)
    o += L(x0, Y(7), x0 + 200, Y(7), INK, 1.4) + T(x0 + 200, Y(7) - 6, '坑底（鉸）', 14, INK, 'end')
    for z, nm in ((1, 'A'), (4, 'B'), (6, 'C')):
        o += L(x0, Y(z), x0 + 140, Y(z), WARN, 4) + T(x0 + 146, Y(z) + 5, nm, 16, WARN, 'start', 'bold')
    for z in (4, 6, 7):
        o += C(x0, Y(z), 6, '#fff', KEY, 2)
    o += T(x0 - p * sc - 8, Y(1.75) + 5, f'{p:.2f}', 14, COMP, 'end', 'bold')
    # 分段標示
    segs = [(0, 4, '第一段'), (4, 6, '第二段'), (6, 7, '第三段')]
    for a, b, nm in segs:
        o += L(x0 - 230, Y(a) + 3, x0 - 230, Y(b) - 3, KEY, 3)
        o += T(x0 - 240, (Y(a) + Y(b)) / 2 + 5, nm, 14, KEY, 'end', 'bold')
    # 反力
    rows = [(1, f"*R*_{{A}}={d['RA']:.2f}"), (4, f"{d['RB1']:.2f}+{d['RB2']:.2f}"), (6, f"{d['RB2']:.2f}+{d['RC2']:.2f}")]
    for z, txt in rows:
        o += T(x0 + 175, Y(z) + 5, txt, 14, INK, 'start')
    o += box(690, 40, 200, 150, '× 間距 5 m', [f"*P*_{{A}}={d['PA']:.1f} kN", f"*P*_{{B}}={d['PB']:.1f} kN", f"*P*_{{C}}={d['PC']:.1f} kN", f"*S*≈{d['S']:.0f} cm³/m"], KEY2, KEY)
    return svg(W, H, o, '鉸接法')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
