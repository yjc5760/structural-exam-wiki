# -*- coding: utf-8 -*-
"""第 0 章：讀法——種子家族樹、獨立基腳五格流程。"""
from figs_common import *  # noqa

SEEDS = [
    ('F1', '兩本帳', '服務／因數', WARN),
    ('F2', '倒懸臂', '柱面固定端', TEN),
    ('F3', '45° 走出去', '柱面、*d*、*d*/2', COMP),
    ('F4', '沿周長拉裂', '三式取小＋λ_{s}', COMP),
    ('F5', '剛性樁帽', '*P*/*n* ± *Mx*/Σ*x*^{2}', KEY),
    ('F6', '1 m 寬的梁', '版帶', TEN),
]


def fig0_1():
    W, H = 900, 470
    o = T(450, 26, '6 顆種子 → 本單元 18 條公式（括號內為章號）', 16, INK, 'middle', 'bold')
    xs = [80 + i * 148 for i in range(6)]
    for (k, a, b_, col), x in zip(SEEDS, xs):
        o += R(x - 68, 46, 136, 84, '#fffde7', '#fbc02d', 2, 12)
        o += T(x, 70, k, 16, col, 'middle', 'bold')
        o += T(x, 96, a, 15, INK, 'middle', 'bold')
        o += T(x, 120, b_, 14, MUT, 'middle')
    F = [
        (110, 250, 200, ['*q* ≤ *q*_{a}（含自重）  (1)', '*q*_{u} = *P*_{u}/*A*（不含）'], ['F1'], WARN2, WARN),
        (330, 250, 220, ['*M*_{u} = *q*_{u}*BL*^{2}/2  (2)', '0.0018*A*_{g}、*s* ≤ 3*h*、45'], ['F2', 'F1'], TEN2, TEN),
        (565, 250, 230, ['單向：*V*_{u} = *q*_{u}*B*(*L* − *d*)  (4)', '2.12ρ_{w}^{1/3}√*f*′_{c}*b*_{w}*d*'], ['F3'], COMP2, COMP),
        (795, 250, 190, ['*b*_{o} = 4(*c*+*d*)  (5)', '1.06／β／α_{s}、λ_{s}'], ['F3', 'F4'], COMP2, COMP),
        (220, 400, 300, ['版剪力筋 0.53λ_{s}、1.59 上限  (6)', '*P*_{i} = *P*/*n* ± *Pex*_{i}/Σ*x*^{2}'], ['F4', 'F5'], KEY2, KEY),
        (640, 400, 330, ['*h*_{min} = ℓ/20、24、28、10  (7)', '*M*_{u} = *C*_{m}*w*_{u}ℓ_{n}^{2}、角隅 ℓ/5'], ['F6'], TEN2, TEN),
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
    o = T(450, 26, '獨立基腳題的五格（只有 ① 用服務載重）', 16, INK, 'middle', 'bold')
    y = 120
    steps = [(95, ['① 驗土壤', '服務載重', '＋自重、覆土'], WARN2, WARN),
             (270, ['② *q*_{u}', '= *P*_{u}/*A*', '（不含自重）'], AC2, AC),
             (445, ['③ 柱面彎矩', '*M*_{u}、*A*_{s}', '0.0018*A*_{g}'], TEN2, TEN),
             (620, ['④ 單向剪力', '距柱面 *d*'], COMP2, COMP),
             (800, ['⑤ 穿孔剪力', '距柱面 *d*/2', '*b*_{o}、三式'], COMP2, COMP)]
    for x, ls, fill, col in steps:
        o += node(x, y, 160, 96, ls, fill, col, 15)
    for x1, x2 in ((175, 190), (350, 365), (525, 540), (700, 720)):
        o += A(x1, y, x2, y, INK, 1.8)
    o += T(95, 200, '第 1 章', 15, WARN, 'middle', 'bold')
    o += T(270, 200, '第 1 章', 15, AC, 'middle', 'bold')
    o += T(445, 200, '第 2 章', 15, TEN, 'middle', 'bold')
    o += T(620, 200, '第 4 章', 15, COMP, 'middle', 'bold')
    o += T(800, 200, '第 5 章', 15, COMP, 'middle', 'bold')
    o += T(450, 255, '②～⑤ 全部用同一個 *q*_{u}；第 3 章說明 ③④⑤ 的斷面為什麼在那裡。', 15, MUT, 'middle')
    return svg(W, H, o, '基腳五格')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
