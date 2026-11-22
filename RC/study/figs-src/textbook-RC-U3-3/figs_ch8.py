# -*- coding: utf-8 -*-
"""第 8 章：總整理——種子樹、耐震設計流程。"""
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
        ('能力設計：強度 → 需求', ['E1'], '1'),
        ('μ_{φ}、θ = φ*L*、*L*_{p}', ['E7'], '1'),
        ('*M*_{pr} = *A*_{s}(1.25*f*_{y})(*d* − *a*/2)', ['E2'], '2'),
        ('*V*_{e} = Σ*M*_{pr}/*l*_{n} ± *w*_{u}*l*_{n}/2', ['E1', 'E3'], '2'),
        ('*V*_{c} = 0：*V*_{E} ≥ 0.5*V*_{u} 且 *N*_{u} 小', ['E4'], '2'),
        ('梁 2*h*：*s* ≤ min(*d*/4, 6*d*_{b}, 15)', ['E6', 'E1'], '2'),
        ('*A*_{sh} 兩式（交於 *A*_{g}/*A*_{ch} = 1.3）', ['E5'], '3'),
        ('*l*_{o}、*s* ≤ min(*b*/4, 6*d*_{b}, *s*_{o})', ['E1', 'E5', 'E6'], '3'),
        ('Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}', ['E1', 'E3'], '4'),
        ('*V*_{col} = Σ*M*_{pr}/*l*_{n}', ['E3'], '4'),
        ('*V*_{jh} = *T*_{1} + *C*_{2} − *V*_{col}', ['E2', 'E3'], '5'),
        ('0.85γ√*f*′_{c}*b*_{j}*h*，γ = 5.3/3.9/3.2', ['E3'], '5'),
        ('ℓ_{d}、1.3ℓ_{d}、柱中央 1/2', ['E5', 'E1'], '6'),
        ('牆 *A*_{cv}(α_{c}√*f*′_{c} + ρ_{t}*f*_{y})、邊界 0.2*f*′_{c}', ['E5', 'E6'], '7'),
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
    W, H = 900, 660
    o = T(450, 24, '特殊抗彎矩構架：每一步的需求來自上一步的強度', 16, INK, 'middle', 'bold')
    cx = 300
    steps = [
        (80, ['① 結構分析 → 梁縱筋（*M*_{u} ≤ φ*M*_{n}）'], AC2, AC, '一般撓曲設計'),
        (165, ['② 梁端 *M*_{pr}（1.25*f*_{y}、φ = 1）'], WARN2, WARN, 'RC-2012-2'),
        (250, ['③ 梁 *V*_{e} → *V*_{c} = 0？→ 塑鉸區箍筋'], COMP2, COMP, 'RC-2025-2、2016-2'),
        (335, ['④ 強柱弱梁 Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}'], KEY2, KEY, '（觀念）'),
        (420, ['⑤ 柱 *V*_{col} = Σ*M*_{pr}/*l*_{n}；*l*_{o}、*A*_{sh}'], TEN2, TEN, 'RC-2012-3、2013-2'),
        (505, ['⑥ 接頭 *V*_{jh} = *T* + *C* − *V*_{col} ≤ φγ√*f*′_{c}*A*_{j}'], COMP2, COMP, 'RC-2012-4、2018-2'),
        (590, ['⑦ 錨定與搭接：避開塑鉸區、1.3ℓ_{d}'], STEEL2, INK, 'RC-2003-2、2010-2'),
    ]
    for y, lines, fill, col, ex in steps:
        o += node(cx, y, 440, 50, lines, fill, col, 15)
        o += T(620, y + 5, ex, 15, MUT, 'start', 'bold')
    for (y1, *_), (y2, *_) in zip(steps, steps[1:]):
        o += A(cx, y1 + 26, cx, y2 - 26, INK, 1.8)
    # 強度 → 需求 的紫色回饋箭頭（M_pr 往下供給 ③⑤⑥）
    o += arrow_path([(cx - 222, 165), (40, 165), (40, 250), (cx - 222, 250)], KEY)
    o += arrow_path([(40, 250), (40, 420), (cx - 222, 420)], KEY)
    o += arrow_path([(40, 420), (40, 505), (cx - 222, 505)], KEY)
    o += T(30, 335, '*M*_{pr}', 15, KEY, 'end', 'bold')
    o += T(620, 52, '考古題', 15, INK, 'start', 'bold')
    return svg(W, H, o, '耐震設計流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
