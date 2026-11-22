# -*- coding: utf-8 -*-
"""第 8 章：總整理——種子樹、決策流程。"""
from figs_common import *  # noqa
from figs_ch0 import SEEDS


def fig8_1():
    W, H = 900, 640
    o = T(450, 24, '7 顆種子 → 14 條要能寫出來的式子', 16, INK, 'middle', 'bold')
    sx, sy0, sdy = 90, 70, 78
    for i, (k, a, b_, col) in enumerate(SEEDS):
        y = sy0 + i * sdy
        o += R(sx - 70, y, 140, 58, '#fffde7', '#fbc02d', 2, 10)
        o += T(sx - 58, y + 25, k, 16, col, 'start', 'bold')
        o += T(sx - 22, y + 25, a, 14, INK, 'start', 'bold')
        o += T(sx - 22, y + 47, b_, 14, MUT, 'start')
    F = [
        ('*V*_{c} = 0.53√*f*′_{c}*b*_{w}*d*', ['V1', 'V2'], '1'),
        ('+*N*_{u}/6*A*_{g}（壓正拉負，≥ 0）', ['V1', 'V2'], '2'),
        ('2.1ρ_{w}^{1/3}√*f*′_{c}（取大）≤ 1.33', ['V2'], '2'),
        ('*V*_{s} = *A*_{v}*f*_{yt}*d*/*s*', ['V3'], '3'),
        ('*s*_{max}：*d*/2 → *d*/4（1.06）', ['V3', 'V4'], '3'),
        ('*V*_{s} ≤ 2.12√*f*′_{c}*b*_{w}*d*', ['V4'], '3'),
        ('*A*_{v,min} = max(0.2√*f*′_{c}, 3.5)*b*_{w}*s*/*f*_{yt}', ['V3', 'V2'], '3'),
        ('臨界斷面：支承面外 *d*（三條件）', ['V5'], '4'),
        ('*V*_{e} = Σ*M*_{pr}/*l*_{n} ± *w*_{u}*l*_{n}/2', ['V3'], '5'),
        ('*V*_{c} = 0：*V*_{E} ≥ 0.5*V*_{u} 且 *N*_{u} 小', ['V1'], '5'),
        ('*T*_{th} = 0.265√*f*′_{c}*A*_{cp}^{2}/*p*_{cp}', ['V7', 'V2'], '6'),
        ('√(*v*^{2}+τ_{t}^{2}) ≤ φ(*v*_{c}+2.12√*f*′_{c})', ['V7', 'V4'], '6'),
        ('*V*_{n} = μ*A*_{vf}*f*_{y} ≤ min(0.2*f*′_{c}, 55)*A*_{c}', ['V6'], '7'),
        ('STM：0.85β*f*′_{c}、*A*_{st}*f*_{y}', ['V5'], '7'),
    ]
    fx, fy0, fdy = 520, 64, 40
    idx = {s[0]: i for i, s in enumerate(SEEDS)}
    for j, (txt, src, ch) in enumerate(F):
        y = fy0 + j * fdy
        for s in src:
            i = idx[s]
            o += L(sx + 70, sy0 + i * sdy + 29, fx - 150, y + 14, SEEDS[i][3], 1.3, op=0.7)
    for j, (txt, src, ch) in enumerate(F):
        y = fy0 + j * fdy
        o += R(fx - 150, y, 470, 30, '#fff', STEEL, 1, 6)
        o += T(fx - 140, y + 21, txt, 14, INK, 'start')
        o += T(fx + 340, y + 21, ch, 15, AC, 'end', 'bold')
    o += T(fx + 340, fy0 - 8, '章', 14, AC, 'end', 'bold')
    return svg(W, H, o, '全書種子樹')


def fig8_2():
    W, H = 900, 700
    o = T(450, 24, '剪力題決策流程', 16, INK, 'middle', 'bold')
    cx = 330
    o += node(cx, 70, 230, 44, ['讀題：找 *b*_{w}、*d*、載重位置'], AC2, AC, 15)
    o += node(cx, 150, 230, 64, ['深梁？', '*a* ≤ 2*h* 或 *l*_{n} ≤ 4*h*'], WARN2, WARN, 14, 'dia')
    o += node(700, 150, 210, 50, ['STM（第 7 章）'], KEY2, KEY, 15)
    o += node(cx, 245, 230, 64, ['耐震塑鉸區？'], WARN2, WARN, 15, 'dia')
    o += node(700, 245, 230, 66, ['*V*_{u} = *V*_{e}（*M*_{pr}）', '比值 ≥ 50% → *V*_{c} = 0'], COMP2, COMP, 14)
    o += node(cx, 340, 250, 70, ['三條件都成立？', '受壓、頂載、無集中'], WARN2, WARN, 14, 'dia')
    o += node(700, 330, 220, 44, ['*V*_{u} 取距支承面 *d*'], TEN2, TEN, 15)
    o += node(700, 380, 220, 40, ['否：取支承面'], COMP2, COMP, 14)
    o += node(cx, 440, 230, 56, ['有軸力？'], WARN2, WARN, 15, 'dia')
    o += node(700, 440, 220, 44, ['+*N*_{u}/6*A*_{g}（第 2 章）'], AC2, AC, 15)
    o += node(cx, 525, 230, 56, ['*T*_{u} ≥ φ*T*_{th}？'], WARN2, WARN, 15, 'dia')
    o += node(700, 525, 240, 50, ['合成上限＋*A*_{t}/*s* 疊加'], AC2, AC, 15)
    o += node(cx, 610, 360, 50, ['*V*_{s} = *V*_{u}/φ − *V*_{c} → *s* → *s*_{max}、上限、*A*_{v,min}'], TEN2, TEN, 15, weight='bold')
    for y1, y2 in ((92, 118), (182, 213), (277, 308), (372, 412), (468, 497), (553, 585)):
        o += A(cx, y1, cx, y2, INK, 1.8)
    o += A(cx + 115, 150, 595, 150, KEY, 1.8)
    o += T(cx + 135, 142, '是', 14, KEY, 'start', 'bold')
    o += A(cx + 115, 245, 585, 245, COMP, 1.8)
    o += T(cx + 135, 237, '是', 14, COMP, 'start', 'bold')
    o += A(cx + 115, 336, 590, 330, TEN, 1.8)
    o += T(cx + 135, 326, '是', 14, TEN, 'start', 'bold')
    o += A(cx + 100, 352, 590, 380, COMP, 1.6)
    o += T(cx + 150, 384, '否', 14, COMP, 'start', 'bold')
    o += A(cx + 115, 440, 590, 440, AC, 1.8)
    o += T(cx + 135, 432, '是', 14, AC, 'start', 'bold')
    o += A(cx + 115, 525, 580, 525, AC, 1.8)
    o += T(cx + 135, 517, '是', 14, AC, 'start', 'bold')
    o += T(cx - 10, 205, '否', 14, INK, 'end', 'bold')
    o += T(cx - 10, 298, '否', 14, INK, 'end', 'bold')
    o += T(cx - 10, 490, '否／算完', 14, INK, 'end', 'bold')
    o += T(cx - 10, 572, '否／算完', 14, INK, 'end', 'bold')
    o += arrow_path([(810, 245), (870, 245), (870, 610), (510, 610)], COMP)
    o += T(450, 670, '介面剪力（新舊混凝土、植筋）另走第 7 章 μ*A*_{vf}*f*_{y}。', 15, MUT, 'middle')
    return svg(W, H, o, '決策流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
