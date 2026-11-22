# -*- coding: utf-8 -*-
"""第 0 章：讀法——種子家族樹、四種已知條件同一個引擎。"""
from figs_col import *  # noqa

SEEDS = [
    ('S1', '平面保持平面', '頂 0.003、直線', AC),
    ('S2', '材料律', '鋼筋 ≤ *f*_{y}；0.85*f*′_{c}×*a*', TEN),
    ('S3', '平衡', 'Σ力＝*P*、對形心取矩', KEY),
    ('S4', 'φ 看預警', 'ε_{t} 越大 φ 越大', COMP),
    ('S5', '圍束', '側壓讓混凝土變強', WARN),
    ('S6', '推歪', '*P*×撓度＝多出的彎矩', MUT),
]


def fig0_1():
    W, H = 900, 560
    o = T(450, 26, '6 顆種子 → 本單元 27 條公式（括號內為章號）', 16, INK, 'middle', 'bold')
    xs = [80 + i * 148 for i in range(6)]
    for (k, a, b_, col), x in zip(SEEDS, xs):
        o += R(x - 70, 46, 140, 84, '#fffde7', '#fbc02d', 2, 12)
        o += T(x, 70, k, 16, col, 'middle', 'bold')
        o += T(x, 96, a, 15, INK, 'middle', 'bold')
        o += T(x, 120, b_, 14, MUT, 'middle')
    F = [
        (140, 250, 250, ['ε_{si} = 0.003(*c* − *d*_{i})/*c*', '*P*_{n}、*M*_{n} 四件套  (1)'], ['S1', 'S2', 'S3'], AC2, AC),
        (430, 250, 290, ['給 *e*／給 *c*／給 *P*_{u}／ε_{t} = 0', '互制圖上解一個點  (2)'], ['S1', 'S2', 'S3'], KEY2, KEY),
        (735, 250, 270, ['*P*_{0}、0.80 截頂、*c*_{b}（6120）', '純彎點、整條曲線  (3)'], ['S1', 'S2', 'S3'], TEN2, TEN),
        (130, 420, 230, ['0.65／0.75、過渡內插', 'φ*M*_{n} 峰值在 0.005  (4)'], ['S4', 'S1'], COMP2, COMP),
        (375, 420, 230, ['*f*_{L}、*f*′_{cc}、ρ_{s} 下限', '*A*_{sh}  (5)(8)'], ['S5', 'S3'], WARN2, WARN),
        (615, 420, 220, ['φ_{y}、φ_{u}、μ_{φ}', '兩條中性軸  (6)'], ['S1', 'S2'], AC2, AC),
        (820, 420, 150, ['*P*_{c}、*C*_{m}', 'δ_{ns}  (7)'], ['S6'], STEEL2, MUT),
    ]
    idx = {s[0]: i for i, s in enumerate(SEEDS)}
    for x, y, w, lines, src, fill, col in F:
        for s in src:
            o += L(xs[idx[s]], 130, x, y - 30, SEEDS[idx[s]][3], 1.3, '5 4', op=0.75)
    for x, y, w, lines, src, fill, col in F:
        o += node(x, y, w, 62, lines, fill, col, 14)
    o += node(450, 520, 640, 44, ['第 9 章：總整理＝種子樹＋解題流程＋一頁公式卡＋精選 5 題'], KEY2, KEY, 15, weight='bold')
    return svg(W, H, o, '種子家族樹')


def fig0_2():
    W, H = 900, 360
    o = T(450, 26, '柱題的四種「入口」，都接到同一台引擎：假設 *c* → 應變 → 應力 → 力 → *P*、*M*', 16, INK, 'middle', 'bold')
    ins = [(110, ['給 *c*', '（RC-2021-2）']), (110 + 225, ['ε_{t} = 0 → *c* = *d*_{t}', '（2008-2、2024-3）']),
           (110 + 450, ['給 *P*_{u}', '（RC-2019-2）']), (110 + 675, ['給 *e*', '（RC-2002-2）'])]
    for x, ls in ins:
        o += node(x, 92, 200, 66, ls, KEY2, KEY, 15)
    o += node(450, 210, 760, 70, ['引擎：ε_{si} = 0.003(*c* − *d*_{i})/*c* → *f*_{si} = *E*_{s}ε_{si} ≤ *f*_{y} → 力 → Σ力 = *P*_{n}、Σ力×(*h*/2 − *d*_{i}) = *M*_{n}'], AC2, AC, 15, weight='bold')
    for i, (x, _) in enumerate(ins):
        o += A(x, 126, x if i in (0, 1) else x, 174, KEY, 1.8)
    o += T(110, 152, '直接用', 14, KEY, 'start')
    o += T(335, 152, '直接用', 14, KEY, 'start')
    o += T(560, 152, '解方程式', 14, WARN, 'start', 'bold')
    o += T(785, 152, '試誤', 14, WARN, 'start', 'bold')
    o += node(450, 310, 640, 50, ['輸出：*P*_{n}、*M*_{n}、*e* = *M*_{n}/*P*_{n}、ε_{t} → φ'], TEN2, TEN, 15, weight='bold')
    o += A(450, 246, 450, 284, INK, 1.8)
    return svg(W, H, o, '四種入口')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
