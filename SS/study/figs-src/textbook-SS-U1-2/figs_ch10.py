# -*- coding: utf-8 -*-
"""第 10 章：彎矩面積法推三個撓度係數；三線檢核長條圖。"""
from plot import *  # noqa
import calcs

DF = calcs.ex_defl()
S2 = calcs.ex_synth2()


def fig10_1():
    W, H = 900, 380
    cases = [('均佈 *w*', lambda t: 4 * t * (1 - t), '面積 = (2/3)(*wL*^{2}/8)(*L*/2)', '形心 5*L*/16', '5/384', AC),
             ('跨中 *P*', lambda t: 1 - abs(2 * t - 1), '面積 = (1/2)(*PL*/4)(*L*/2)', '形心 *L*/3', '1/48', WARN),
             ('三分點雙 *P*', lambda t: min(1.0, 3 * t, 3 * (1 - t)), '三角＋矩形', '23*L*/72 加權', '23/648', COMP)]
    o = ''
    cw = 280
    for i, (name, fn, a1, a2, coef, c) in enumerate(cases):
        x0 = 20 + i * (cw + 12)
        o += R(x0, 20, cw, 330, '#fff', STEEL, 1.2, 10)
        o += T(x0 + cw / 2, 46, name, 16, c, 'middle', 'bold')
        bx0, bx1, base, amp = x0 + 20, x0 + cw - 20, 170, 90
        o += L(bx0, base, bx1, base, INK, 1.6)
        pts = [(bx0 + (bx1 - bx0) * k / 120, base - amp * fn(k / 120)) for k in range(121)]
        o += P([(bx0, base)] + pts + [(bx1, base)], None, fill=COMP2, close=True, op=0.6)
        half = [(bx0 + (bx1 - bx0) * k / 120, base - amp * fn(k / 120)) for k in range(61)]
        o += P([(bx0, base)] + half + [((bx0 + bx1) / 2, base)], c, 1.6, fill=(AC2 if c == AC else WARN2 if c == WARN else COMP2), close=True)
        o += P(pts, INK, 1.4)
        o += L((bx0 + bx1) / 2, base - amp - 10, (bx0 + bx1) / 2, base + 10, MUT, 1.2, '4 3')
        o += T(x0 + cw / 2, base + 30, '*M*/*EI* 圖；著色＝半跨', 14, MUT, 'middle')
        o += T(x0 + cw / 2, base + 64, a1, 14, INK, 'middle')
        o += T(x0 + cw / 2, base + 88, a2, 14, INK, 'middle')
        o += T(x0 + cw / 2, base + 128, f'δ 係數 = {coef}', 17, c, 'middle', 'bold')
    o += T(W / 2, 372, '跨中撓度 ＝ 半跨 *M*/*EI* 面積 × 該面積形心到支承的距離（對稱簡支梁的彎矩面積法）', 15, KEY, 'middle', 'bold')
    return svg(W, H + 10, o, '撓度係數')


def fig10_2():
    W, H = 900, 400
    rows = [('SS-2015-1（BH920，*L*=8.4 m）', [DF['flex2015'], DF['shear2015'], DF['use2015']]),
            ('綜合練習（H700，*L*=10 m）', [S2['uM'], S2['uV'], S2['uD']])]
    labs = [('強度 *M*_{u}/φ*M*_{n}', COMP), ('剪力 *V*_{u}/φ*V*_{n}', WARN), ('撓度 δ_{L}/(*L*/360)', AC)]
    o = ''
    pl = Plot(330, 40, 460, 300, 0, 1.2, 0, 6)
    o += L(pl.X(1.0), 30, pl.X(1.0), 350, KEY, 2, '6 4') + T(pl.X(1.0), 26, '1.0（用滿）', 14, KEY, 'middle', 'bold')
    for t in (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2):
        o += T(pl.X(t), 372, f(t), 14, MUT, 'middle') + L(pl.X(t), 347, pl.X(t), 352, INK, 1)
    o += L(pl.X(0), 347, pl.X(1.2), 347, INK, 1.4)
    y = 50
    for name, vals in rows:
        o += T(20, y + 4, name, 15, INK, 'start', 'bold')
        y += 14
        for (lab, c), v in zip(labs, vals):
            o += T(320, y + 20, lab, 14, c, 'end')
            o += R(pl.X(0), y + 6, pl.X(v) - pl.X(0), 22, c, None, 0, 4, op=0.85)
            o += T(pl.X(v) + 6, y + 23, f'{v * 100:.1f}%', 14, c, 'start', 'bold')
            y += 36
        y += 22
    return svg(W, H, o, '三線檢核')


ALL = {'fig10_1': fig10_1, 'fig10_2': fig10_2}
