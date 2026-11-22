# -*- coding: utf-8 -*-
"""第 0 章：讀法——種子家族樹、先強度後需求。"""
from figs_common import *  # noqa

SEEDS = [
    ('E1', '保險絲', '選誰先壞', KEY),
    ('E2', '超強', '1.25*f*_{y}、φ = 1', WARN),
    ('E3', '自由體', '梁、柱、接頭', COMP),
    ('E4', '反覆磨損', '*V*_{c} = 0', COMP),
    ('E5', '核心撐斷面', '*A*_{g}/*A*_{ch} − 1', TEN),
    ('E6', '縱筋小柱', '6*d*_{b}', TEN),
    ('E7', '韌性', 'φ × *L* = θ', AC),
]


def fig0_1():
    W, H = 900, 480
    o = T(450, 26, '7 顆種子 → 本單元 27 條公式（括號內為章號）', 16, INK, 'middle', 'bold')
    xs = [66 + i * 128 for i in range(7)]
    for (k, a, b_, col), x in zip(SEEDS, xs):
        o += R(x - 58, 46, 116, 84, '#fffde7', '#fbc02d', 2, 12)
        o += T(x, 70, k, 16, col, 'middle', 'bold')
        o += T(x, 96, a, 15, INK, 'middle', 'bold')
        o += T(x, 120, b_, 14, MUT, 'middle')
    F = [
        (120, 250, 210, ['*M*_{pr} = *A*_{s}(1.25*f*_{y})(*d* − *a*/2)', '*V*_{e}（梁）  (2)'], ['E1', 'E2', 'E3'], WARN2, WARN),
        (350, 250, 210, ['*V*_{c} = 0 兩條件  (2)', '塑鉸區 2*h*、*d*/4、6*d*_{b}'], ['E4', 'E6'], COMP2, COMP),
        (580, 250, 220, ['*A*_{sh} 兩式、*l*_{o}  (3)', '*s* ≤ min(*b*/4, 6*d*_{b}, *s*_{o})'], ['E5', 'E6'], TEN2, TEN),
        (800, 250, 170, ['μ_{φ}、μ_{θ}、μ_{Δ}', '*L*_{p}  (1)'], ['E7'], AC2, AC),
        (200, 400, 260, ['Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}', '*V*_{col} = Σ*M*_{pr}/*l*_{n}  (4)'], ['E1', 'E3'], KEY2, KEY),
        (470, 400, 250, ['*V*_{jh} = *T*_{1} + *C*_{2} − *V*_{col}', 'γ√*f*′_{c}*A*_{j}、φ = 0.85  (5)'], ['E2', 'E3'], COMP2, COMP),
        (750, 400, 250, ['ℓ_{d}、1.3ℓ_{d}、中段 *l*_{n}/2  (6)', '剪力牆 α_{c}、0.0025  (7)'], ['E1'], STEEL2, INK),
    ]
    idx = {s[0]: i for i, s in enumerate(SEEDS)}
    for x, y, w, lines, src, fill, col in F:
        for s in src:
            o += L(xs[idx[s]], 130, x, y - 31, SEEDS[idx[s]][3], 1.3, '5 4', op=0.75)
    for x, y, w, lines, src, fill, col in F:
        o += node(x, y, w, 62, lines, fill, col, 14)
    return svg(W, H, o, '種子家族樹')


def fig0_2():
    W, H = 900, 300
    o = T(450, 26, '先強度、後需求：一條保險絲鏈', 16, INK, 'middle', 'bold')
    y = 120
    steps = [(95, ['① 梁端', '*M*_{pr}', '（1.25*f*_{y}）'], WARN2, WARN),
             (275, ['② 梁剪力', '*V*_{e}', '*V*_{c} = 0？'], COMP2, COMP),
             (455, ['③ 柱', 'Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}', '*V*_{col}'], KEY2, KEY),
             (635, ['④ 接頭', '*V*_{jh} = *T* − *V*_{col}'], COMP2, COMP),
             (815, ['⑤ 構造細則', '*A*_{sh}、*l*_{o}', '6*d*_{b}、搭接'], TEN2, TEN)]
    for x, ls, fill, col in steps:
        o += node(x, y, 165, 96, ls, fill, col, 14)
    for x1, x2 in ((178, 192), (358, 372), (538, 552), (718, 732)):
        o += A(x1, y, x2, y, INK, 1.8)
    for x, t in ((95, '第 2 章'), (275, '第 2 章'), (455, '第 4 章'), (635, '第 5 章'), (815, '第 3、6 章')):
        o += T(x, 200, t, 15, INK, 'middle', 'bold')
    o += T(450, 255, '不是「分析出多少力就配多少筋」，而是「保險絲最多有多強，其他構件就要撐到多少」。', 15, MUT, 'middle')
    return svg(W, H, o, '先強度後需求')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
