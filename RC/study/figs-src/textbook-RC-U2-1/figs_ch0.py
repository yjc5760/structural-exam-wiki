# -*- coding: utf-8 -*-
"""第 0 章：讀法——種子家族樹、剪力設計五格節奏。"""
from figs_common import *  # noqa

SEEDS = [
    ('V1', '45° 主拉', '剪＝斜拉', COMP),
    ('V2', '∝ √*f*′_{c}', '開裂強度', COMP),
    ('V3', '桁架類比', '*d*/*s* 根箍筋', TEN),
    ('V4', '*V*_{c} 當尺', '1、2、4 倍', KEY),
    ('V5', '力要走路', '壓桿進支承', WARN),
    ('V6', '撐開→夾緊', '摩擦剪力', WARN),
    ('V7', '剪流 *q*', '*T*/2*A*_{o}', COMP),
]


def fig0_1():
    W, H = 900, 560
    o = T(450, 26, '7 顆種子 → 本單元 24 條公式（括號內為章號）', 16, INK, 'middle', 'bold')
    xs = [66 + i * 128 for i in range(7)]
    for (k, a, b_, col), x in zip(SEEDS, xs):
        o += R(x - 58, 46, 116, 84, '#fffde7', '#fbc02d', 2, 12)
        o += T(x, 70, k, 16, col, 'middle', 'bold')
        o += T(x, 96, a, 15, INK, 'middle', 'bold')
        o += T(x, 120, b_, 14, MUT, 'middle')
    F = [
        (130, 250, 230, ['*V*_{c} = 0.53√*f*′_{c} *b*_{w}*d*  (1)', '單位：= √*f*′_{c}/6 (MPa)'], ['V1', 'V2'], COMP2, COMP),
        (380, 250, 240, ['軸力 ±*N*_{u}/6*A*_{g}  (2)', 'ρ_{w}^{1/3} 式、上限 1.33'], ['V1', 'V2'], COMP2, COMP),
        (640, 250, 250, ['*V*_{s} = *A*_{v}*f*_{yt}*d*/*s*  (3)', '1.06 → *d*/4、2.12 上限'], ['V3', 'V4'], TEN2, TEN),
        (130, 400, 230, ['*A*_{v,min}：0.2√*f*′_{c}、3.5  (3)', '開裂後箍筋接得住'], ['V3', 'V2'], TEN2, TEN),
        (380, 400, 240, ['臨界斷面 = 支承面外 *d*  (4)', '三個例外不可偏移'], ['V5'], WARN2, WARN),
        (640, 400, 250, ['*T*_{th} = 0.265√*f*′_{c} *A*_{cp}^{2}/*p*_{cp}  (6)', '扭剪合成上限'], ['V7', 'V2'], AC2, AC),
        (835, 400, 110, ['μ*A*_{vf}*f*_{y}', 'STM  (7)'], ['V6', 'V5'], KEY2, KEY),
    ]
    idx = {s[0]: i for i, s in enumerate(SEEDS)}
    for x, y, w, lines, src, fill, col in F:
        for s in src:
            o += L(xs[idx[s]], 130, x, y - 31, SEEDS[idx[s]][3], 1.3, '5 4', op=0.75)
    for x, y, w, lines, src, fill, col in F:
        o += node(x, y, w, 62, lines, fill, col, 14)
    o += node(450, 520, 640, 44, ['第 5 章耐震：需求改由 *M*_{pr} 決定（*V*_{e}），*V*_{c} 可能歸零——不需新種子'], WARN2, WARN, 15, weight='bold')
    o += A(450, 432, 450, 496, WARN, 1.8)
    return svg(W, H, o, '種子家族樹')


def fig0_2():
    W, H = 900, 300
    o = T(450, 26, '每一題剪力設計都是這五格', 16, INK, 'middle', 'bold')
    y = 120
    steps = [(95, ['① 取 *V*_{u}', '臨界斷面', '或 *M*_{pr}'], WARN2, WARN),
             (270, ['② 混凝土', '*V*_{c}', '（可能 = 0）'], COMP2, COMP),
             (445, ['③ 剩下的', '*V*_{s} = *V*_{u}/φ − *V*_{c}'], TEN2, TEN),
             (620, ['④ 間距', '*s* = *A*_{v}*f*_{yt}*d*/*V*_{s}'], TEN2, TEN),
             (800, ['⑤ 三條檢查', '*s*_{max}、*V*_{s} 上限', '*A*_{v,min}'], KEY2, KEY)]
    for x, ls, fill, col in steps:
        o += node(x, y, 160, 96, ls, fill, col, 15)
    for x1, x2 in ((175, 190), (350, 365), (525, 540), (700, 720)):
        o += A(x1, y, x2, y, INK, 1.8)
    o += T(95, 200, '第 4、5 章', 15, WARN, 'middle', 'bold')
    o += T(270, 200, '第 1、2 章', 15, COMP, 'middle', 'bold')
    o += T(532, 200, '第 3 章', 15, TEN, 'middle', 'bold')
    o += T(800, 200, '第 3 章', 15, KEY, 'middle', 'bold')
    o += T(450, 250, '扭力（第 6 章）只是在 ③④ 多了一份 *A*_{t}/*s*，還要多一條 ⑤ 的合成上限。', 15, MUT, 'middle')
    return svg(W, H, o, '剪力設計五格')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
