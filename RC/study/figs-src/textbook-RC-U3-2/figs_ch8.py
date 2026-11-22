# -*- coding: utf-8 -*-
"""第 8 章：總整理——種子樹、決策流程。"""
from figs_common import *  # noqa
from figs_ch0 import SEEDS


def fig8_1():
    W, H = 900, 620
    o = T(450, 24, '6 顆種子 → 13 條要能寫出來的式子', 16, INK, 'middle', 'bold')
    sx, sy0, sdy = 90, 70, 88
    for i, (k, a, b_, col) in enumerate(SEEDS):
        y = sy0 + i * sdy
        o += R(sx - 70, y, 140, 62, '#fffde7', '#fbc02d', 2, 10)
        o += T(sx - 58, y + 26, k, 16, col, 'start', 'bold')
        o += T(sx - 22, y + 26, a, 14, INK, 'start', 'bold')
        o += T(sx - 58, y + 50, b_, 14, MUT, 'start')
    F = [
        ('*q* = (*P*_{D}+*P*_{L}+*W*_{f}+*W*_{s})/*A* ≤ *q*_{a}', ['F1'], '1'),
        ('*q*_{u} = *P*_{u}/*A*（不含自重）', ['F1'], '1'),
        ('*M*_{u} = *q*_{u}*BL*^{2}/2，*L* = (*B*−*c*)/2', ['F2'], '2'),
        ('0.0018*A*_{g}、*s* ≤ min(3*h*, 45)', ['F2', 'F6'], '2'),
        ('*V*_{u1} = *q*_{u}*B*(*L*−*d*)', ['F3'], '3'),
        ('*b*_{o} = 4(*c*+*d*)、*V*_{u2} = *P*_{u}−*q*_{u}(*c*+*d*)^{2}', ['F3'], '3'),
        ('2.12λ_{s}ρ_{w}^{1/3}√*f*′_{c}*b*_{w}*d*（基腳 λ_{s} = 1）', ['F3'], '4'),
        ('min{1.06, 0.53(1+2/β), 0.265(2+α_{s}*d*/*b*_{o})}', ['F4'], '5'),
        ('λ_{s} = √(2/(1+0.04*d*))', ['F4'], '5'),
        ('剪力筋：0.53λ_{s}、*A*_{v}*f*_{yt}*d*/*s*、1.59 上限', ['F4'], '6'),
        ('*P*_{i} = *P*/*n* ± *Pex*_{i}/Σ*x*^{2}', ['F5'], '6'),
        ('*h*_{min} = ℓ/20、24、28、10', ['F6'], '7'),
        ('*M*_{u} = *C*_{m}*w*_{u}ℓ_{n}^{2}；角隅 ℓ/5', ['F6'], '7'),
    ]
    fx, fy0, fdy = 520, 64, 42
    idx = {s[0]: i for i, s in enumerate(SEEDS)}
    for j, (txt, src, ch) in enumerate(F):
        y = fy0 + j * fdy
        for s in src:
            i = idx[s]
            o += L(sx + 70, sy0 + i * sdy + 31, fx - 150, y + 15, SEEDS[i][3], 1.3, op=0.7)
    for j, (txt, src, ch) in enumerate(F):
        y = fy0 + j * fdy
        o += R(fx - 150, y, 470, 32, '#fff', STEEL, 1, 6)
        o += T(fx - 140, y + 22, txt, 14, INK, 'start')
        o += T(fx + 340, y + 22, ch, 15, AC, 'end', 'bold')
    o += T(fx + 340, fy0 - 8, '章', 14, AC, 'end', 'bold')
    return svg(W, H, o, '全書種子樹')


def fig8_2():
    W, H = 900, 560
    o = T(450, 24, '樓版與基腳題決策流程', 16, INK, 'middle', 'bold')
    o += node(450, 70, 300, 44, ['讀題：什麼構件？'], AC2, AC, 15, weight='bold')
    # 三條路
    o += node(150, 150, 220, 50, ['樓版'], TEN2, TEN, 15, weight='bold')
    o += node(450, 150, 220, 50, ['獨立基腳'], WARN2, WARN, 15, weight='bold')
    o += node(750, 150, 220, 50, ['樁帽'], KEY2, KEY, 15, weight='bold')
    for x in (150, 450, 750):
        o += A(450 if x == 450 else 450 + (x - 450) * 0.1, 92, x, 124, INK, 1.6)
    # 樓版
    o += node(150, 235, 230, 50, ['單向版：*h*_{min}、*C*_{m}'], TEN2, TEN, 14)
    o += node(150, 305, 230, 50, ['*A*_{s} ≥ 0.0018*bh*'], TEN2, TEN, 14)
    o += node(150, 375, 230, 56, ['無梁版：穿孔', '（要乘 λ_{s}）'], COMP2, COMP, 14)
    o += node(150, 455, 230, 56, ['不足 → 剪力筋', '0.53λ_{s}、1.59 上限'], COMP2, COMP, 14)
    for y1, y2 in ((175, 210), (260, 280), (330, 347), (403, 427)):
        o += A(150, y1, 150, y2, INK, 1.6)
    # 基腳
    labs = [['① 服務帳驗土'], ['② *q*_{u} = *P*_{u}/*A*'], ['③ 柱面 *M*_{u}、0.0018'], ['④ 單向（距 *d*）'], ['⑤ 穿孔（距 *d*/2，λ_{s} = 1）']]
    for i, ls in enumerate(labs):
        o += node(450, 225 + i * 62, 250, 44, ls, WARN2 if i == 0 else (COMP2 if i >= 3 else AC2), WARN if i == 0 else (COMP if i >= 3 else AC), 14)
        if i:
            o += A(450, 225 + (i - 1) * 62 + 22, 450, 225 + i * 62 - 22, INK, 1.6)
    o += A(450, 175, 450, 203, INK, 1.6)
    o += T(450, 535, '不足 → 加厚（最有效）', 14, COMP, 'middle', 'bold')
    # 樁帽
    o += node(750, 235, 240, 56, ['*P*_{i} = *P*/*n* ± *Pex*_{i}/Σ*x*^{2}', '壓、拉上限'], KEY2, KEY, 14)
    o += node(750, 320, 240, 56, ['柱周穿孔', '（λ_{s} 要乘）'], COMP2, COMP, 14)
    o += node(750, 405, 240, 56, ['角隅樁穿孔', 'α_{s} = 20、1/4 圓周長'], COMP2, COMP, 14)
    for y1, y2 in ((175, 207), (263, 292), (348, 377)):
        o += A(750, y1, 750, y2, INK, 1.6)
    return svg(W, H, o, '決策流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
