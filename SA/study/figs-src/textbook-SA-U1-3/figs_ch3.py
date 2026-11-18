# -*- coding: utf-8 -*-
"""第 3 章：桁架影響線。桁架幾何取自題目正本判讀清單；每一個縱距都由 calcs.py 的桁架求解器
（直接勁度法）逐節點算出，並與截面法閉合解比對過（calcs.py 內 assert）。"""
from figs_common import *  # noqa
import calcs as K
from fractions import Fraction as Fr


def fr(v, d=64):
    s = str(Fr(v).limit_denominator(d))
    return s.replace('-', '−')


def fig3_1():
    """縱梁是簡支梁：節間內的載重分給兩個節點 → 影響線在節間是直線。"""
    W, H = 900, 640
    ax = Ax(110, 17)                     # 40 m → 680 px
    o = ''
    o += T(14, 30, '(a) 載重不是直接壓在桁架上：橋面 → 縱梁 → 橫梁 → 下弦節點', 16, INK, 'start', 'bold')
    yb = 150
    # 下弦與節點
    o += L(ax(0), yb, ax(40), yb, INK, 4)
    for x, nm in zip(K.T4_X, K.T4_LN):
        o += C(ax(x), yb, 5, '#fff', INK, 1.6)
        o += T(ax(x), yb + 30, nm, 16, INK, 'middle', 'bold')
    # 縱梁（每節間一根簡支小梁），畫在下弦上方
    ys = yb - 34
    for x0 in (0, 10, 20, 30):
        o += L(ax(x0) + 6, ys, ax(x0 + 10) - 6, ys, STEEL, 6)
        o += P([(ax(x0) + 8, ys + 4), (ax(x0) + 2, ys + 14), (ax(x0) + 14, ys + 14)], STEEL, 1.2, fill='#fff', close=True)
        o += P([(ax(x0 + 10) - 8, ys + 4), (ax(x0 + 10) - 14, ys + 14), (ax(x0 + 10) - 2, ys + 14)], STEEL, 1.2, fill='#fff', close=True)
    o += T(ax(35), ys - 14, '縱梁（每格一根簡支梁）', 15, MUT, 'middle')
    # 單位載重在 13 m
    x = K.DECK_X
    o += unit_load(ax(x), ys - 4, h=46)
    o += dim(ax(10), ys - 70, ax(x), ys - 70, '3 m', MUT, size=15)
    o += dim(ax(x), ys - 70, ax(20), ys - 70, '7 m', MUT, size=15)
    s1, s2 = K.DECK_SHARE
    o += A(ax(10), yb + 42, ax(10), yb + 42 + 60 * s1, COMP, 2.6, 11)
    o += T(ax(10) + 10, yb + 42 + 60 * s1 - 4, f'{f(s1)}（= 7/10）', 15, COMP, 'start', 'bold')
    o += A(ax(20), yb + 42, ax(20), yb + 42 + 60 * s2, COMP, 2.6, 11)
    o += T(ax(20) + 10, yb + 42 + 60 * s2 - 2, f'{f(s2)}（= 3/10）', 15, COMP, 'start', 'bold')
    o += T(ax(30), yb + 70, '桁架只在節點 b、c 受力', 15, COMP, 'start', 'bold')
    # (b) 影響線：節間內必為直線
    o += T(14, 300, '(b) 所以任何量的影響線，在一個節間內都是「兩端節點值的直線」', 16, INK, 'start', 'bold')
    base, sy = 470, 110
    beamV = lambda xx: -xx / 40 if xx < 15 else 1 - xx / 40          # 若載重直接壓在梁上、斷面在 15 m
    pts_dir = [(0, 0), (15, beamV(15 - 1e-9)), (15, beamV(15 + 1e-9)), (40, 0)]
    o += P([(ax(xx), base - sy * yy) for xx, yy in pts_dir], STEEL, 2, dash='6 5')
    pts = [(xx, K.t4_Vpanel(xx)) for xx in K.T4_X]
    o += il(ax, base, sy, pts, name='', ticks=K.T4_X,
            vals=[(10, K.t4_Vpanel(10), '−0.25', (-34, 16)), (20, K.t4_Vpanel(20), '+0.5', (0, -12))])
    o += T(ax(15) - 10, base - sy * 0.625 - 8, '灰虛線：若載重直接壓在梁上，斷面處跳 1', 15, MUT, 'end')
    o += C(ax(40 / 3), base, 4, AC, '#fff', 1.4)
    o += A(ax(22), base + 52, ax(40 / 3) + 6, base + 6, AC, 1.6, 9)
    o += T(ax(22) + 4, base + 64, '節間內是直線，在 13.3 m 通過 0', 15, AC, 'start', 'bold')
    o += T(14, base - 60, 'b–c 節間', 15, INK, 'start', 'bold')
    o += T(14, base - 38, '的剪力', 15, INK, 'start', 'bold')
    for xx, nm in zip(K.T4_X, K.T4_LN):
        o += T(ax(xx), base + 24 if xx != 10 else base + 50, nm, 15, MUT, 'middle')
    o += L(ax(10), 170, ax(10), base + 34, STEEL, 1, '3 4') + L(ax(20), 170, ax(20), base + 10, STEEL, 1, '3 4')
    o += R(110, 560, 680, 64, KEY2, KEY, 1.3, 9)
    o += T(450, 586, '載重在節間 → 分給兩節點 (1−*t*)、*t* →  η = (1−*t*)·η_{*i*} + *t*·η_{*j*}', 16, KEY, 'middle', 'bold')
    o += T(450, 612, '這就是「節間直線內插」：它不是規定，是縱梁簡支的結果', 15, INK, 'middle')
    return svg(W, H, o, '縱梁是簡支梁')


T4F = None


def _t4frame(y0):
    return Frame(110, y0, 15.5)        # 40 m → 620 px


def fig3_2():
    """SA-2004-2：截面法把桿力影響線變成梁的影響線。"""
    W, H = 900, 1140
    F = _t4frame(230)
    ax = Ax(110, 15.5)
    o = ''
    lab = {'a': (-16, 6), 'b': (0, 28), 'c': (0, 28), 'd': (0, 28), 'e': (16, 6),
           'B': (0, -14), 'C': (0, -14), 'D': (0, -14)}
    hl = {('b', 'c'): (TEN, 5), ('B', 'C'): (COMP, 5), ('B', 'c'): (WARN, 5)}
    o += truss_draw(F, K.T4, K.T4_MEM, {'a': 'pin', 'e': 'roller'}, lab, hl)
    X15 = F(15, 0)[0]
    o += cut_line(X15, 50, 262, '截面', dy=-8)
    o += C(F(10, 10)[0], F(10, 10)[1], 9, 'none', KEY, 2.4)
    o += T(F(10, 10)[0] - 20, F(10, 10)[1] - 30, '矩心 B → 求 bc', 15, KEY, 'end', 'bold')
    o += C(F(20, 0)[0], F(20, 0)[1], 9, 'none', COMP, 2.4)
    o += T(F(21, 0)[0] + 4, F(20, 0)[1] + 26, '矩心 c → BC', 15, COMP, 'start', 'bold')
    o += T(F(16, 7.6)[0], F(16, 7.6)[1], 'Σ*F*_{*y*} → 求 Bc', 15, WARN, 'start', 'bold')
    o += dim(F(0, 0)[0], 300, F(40, 0)[0], 300, '4 @ 10 m = 40 m', MUT, size=15)
    o += dim(F(40, 0)[0] + 40, F(40, 0)[1], F(40, 10)[0] + 40, F(40, 10)[1], '10 m', MUT, size=15, side=-1)
    tk = K.T4_X
    rows = [
        (410, 90, [(x, K.t4_Ra(x)) for x in tk], 'IL *R*_{*a*}', [(0, 1, '1', 'w')], '= 1 − *x*/40'),
        (580, 120, [(x, K.t4_Nbc(x)) for x in tk], 'IL *N*_{*bc*}', [(10, .75, '0.75', 'n')], '= *M*_{*b*}/10（拉）'),
        (680, 80, [(x, K.t4_NBC(x)) for x in tk], 'IL *N*_{*BC*}', [(20, -1, '−1.0', 's')], '= −*M*_{*c*}/10（壓）'),
        (1000, 140, [(x, K.t4_NBc(x)) for x in tk], 'IL *N*_{*Bc*}',
         [(10, K.T4_NBc_b, '−0.354', 's'), (20, K.T4_NBc_c, '+0.707', 'n')], '= √2 × 節間剪力'),
    ]
    for base, sy, pts, nm, vals, note in rows:
        o += il(ax, base, sy, pts, name=nm, ticks=tk, vals=vals)
        o += T(ax(40) + 20, base - 22, note, 15, MUT, 'start')
    o += C(ax(K.T4_NBc_zero), 1000, 4, AC, '#fff', 1.4)
    o += T(ax(K.T4_NBc_zero) + 6, 1030, '13.3 m 變號', 15, AC, 'start', 'bold')
    for x in (10, 20):
        o += L(ax(x), 320, ax(x), 1090, STEEL, 1, '3 4')
    o += T(ax(10), 1118, 'b', 15, MUT, 'middle') + T(ax(20), 1118, 'c', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2004-2 桿力影響線')


def fig3_3():
    """SA-2014-1：上弦傾斜也一樣，力矩中心在 I。"""
    W, H = 900, 560
    F = Frame(110, 250, 9.4)            # 72 m → 677 px
    ax = Ax(110, 9.4)
    o = ''
    lab = {n: (0, 28) for n in 'BCDEF'}
    lab.update({'A': (-16, 6), 'G': (16, 6), 'H': (-14, -10), 'I': (-12, -14), 'J': (0, -14), 'K': (12, -14), 'L': (14, -10)})
    o += truss_draw(F, K.T14, K.T14_MEM, {'A': 'pin', 'G': 'roller'}, lab, {('C', 'D'): (TEN, 5), ('I', 'D'): (WARN, 4), ('I', 'J'): (COMP, 4)})
    o += cut_line(F(30, 0)[0], 26, 268, '截面')
    Ix, Iy = F(24, 17)
    o += C(Ix, Iy, 10, 'none', KEY, 2.4)
    o += A(Ix - 70, Iy - 26, Ix - 12, Iy - 6, KEY, 2, 9)
    o += T(Ix - 76, Iy - 30, '矩心 I（IJ、ID 交點）', 15, KEY, 'end', 'bold')
    o += L(Ix, Iy + 10, Ix, F(24, 0)[1], KEY, 1.2, '3 3')
    o += T(Ix - 8, F(24, 8)[1], '17 m', 15, KEY, 'end', 'bold')
    o += dim(F(0, 0)[0], 300, F(72, 0)[0], 300, '6 @ 12 m = 72 m', MUT, size=15)
    base, sy = 470, 130
    pts = [(x, K.t14_NCD(x)) for x in K.T14_X]
    vals = [(x, K.t14_NCD(x), fr(K.t14_NCD(x), 17), 'n') for x in K.T14_X[1:6]]
    o += il(ax, base, sy, pts, name='', ticks=K.T14_X, vals=vals, vsize=16)
    o += T(14, base - 40, 'IL *N*_{*CD*}', 16, INK, 'start', 'bold')
    o += T(14, base - 16, '（×*P*，拉）', 15, MUT, 'start')
    o += T(ax(48), base - 120, '= *M*_{梁, *x*=24} ÷ 17', 16, KEY, 'start', 'bold')
    o += T(ax(48), base - 96, '最大在 C：16/17 *P*', 16, TEN, 'start', 'bold')
    for x, nm in zip(K.T14_X, K.T14_LN):
        o += T(ax(x), base + 26, nm, 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2014-1 CD 桿影響線')


def _t22nodes():
    return {f'{k}': v for k, v in K.T22.items()}


T22_LAB = {'B0': (-14, 8, 'a'), 'B2': (0, 28, 'm'), 'B3': (0, 28, 'n'), 'B4': (0, 44, 'b'), 'B6': (0, 44, 'c'),
           'B7': (0, 28, 'd'), 'B10': (16, 8, 'e'), 'T2': (0, -14, 'k')}


def fig3_4():
    """SA-2022-3：無斜桿嵌板＝剪力滑塊，d＝等效內鉸 → 等效 Gerber 梁 → Müller-Breslau。"""
    W, H = 900, 940
    F = Frame(110, 160, 22)             # 30 m → 660 px
    ax = Ax(110, 22)
    o = ''
    o += T(14, 30, '(a) 題目的桁架（a、b、c 滾支承，e 鉸支承）', 16, INK, 'start', 'bold')
    hl = {('B2', 'B3'): (TEN, 5), ('T2', 'B3'): (WARN, 5)}
    o += truss_draw(F, K.T22, K.T22_MEM, {'B0': 'roller', 'B4': 'roller', 'B6': 'roller', 'B10': 'pin'}, T22_LAB, hl, w=2.2, jr=3)
    o += R(F(12, 4)[0] + 6, F(12, 4)[1] + 10, F(15, 0)[0] - F(12, 4)[0] - 12, 66, '#fff3e0', WARN, 1.4, 6, op=0.9)
    o += T(F(13.5, 2)[0], F(13.5, 2)[1] + 6, '無斜桿', 15, WARN, 'middle', 'bold')
    o += C(F(22.5, 4)[0], F(22.5, 4)[1], 12, 'none', COMP, 2, )
    o += T(F(22.5, 4)[0], F(22.5, 4)[1] - 18, '沒上弦', 15, COMP, 'middle', 'bold')
    # (b) 等效梁
    o += T(14, 290, '(b) 把它看成一根梁：無斜桿那格只能傳彎矩 → 「滑塊」；21–24 只有交於 d 的兩桿 → d 是「鉸」', 15, INK, 'start', 'bold')
    yb = 360
    o += L(ax(0), yb, ax(13.2), yb, INK, 5) + L(ax(13.8), yb, ax(30), yb, INK, 5)
    o += L(ax(13.2), yb - 14, ax(13.2), yb + 14, WARN, 3) + L(ax(13.8), yb - 14, ax(13.8), yb + 14, WARN, 3)
    o += T(ax(13.5), yb - 22, '滑塊', 15, WARN, 'middle', 'bold')
    o += hinge(ax(21), yb, 7, COMP)
    o += T(ax(21), yb - 18, 'd 鉸', 15, COMP, 'middle', 'bold')
    for x, k in ((0, 'r'), (12, 'r'), (18, 'r'), (30, 'p')):
        o += roller(ax(x), yb + 3) if k == 'r' else pin(ax(x), yb + 3)
    for x, nm in ((0, 'a'), (12, 'b'), (18, 'c'), (30, 'e')):
        o += T(ax(x), yb + 50, nm, 16, INK, 'middle', 'bold')
    # (c) Müller-Breslau：R_c
    sy = 70
    o += T(14, 452, '(c) 求 *R*_{*c*}：推 c 上去 1', 16, AC, 'start', 'bold')
    base = 560
    o += L(ax(0), base, ax(30), base, STEEL3, 3, '8 6')
    pts = [(x, K.eqbeam22(x)[2]) for x in K.T22_X]
    o += P([(ax(x), base - sy * v) for x, v in pts], KEY, 4.5)
    o += T(ax(5), base - 14, 'a、b 兩支承擋住 → 0', 15, MUT, 'middle')
    o += T(ax(18), base - sy - 16, '滑塊右邊整段平移 1', 15, KEY, 'middle', 'bold')
    o += T(ax(26.5), base - sy * 0.5 - 8, '繞 e 轉回 0', 15, KEY, 'start', 'bold')
    o += T(ax(13.5), base + 24, '節間直線', 14, MUT, 'middle')
    # (d) Müller-Breslau：R_a
    o += T(14, 640, '(d) 求 *R*_{*a*}：推 a 上去 1', 16, AC, 'start', 'bold')
    base = 760
    sy = 90
    o += L(ax(0), base, ax(30), base, STEEL3, 3, '8 6')
    pts = [(x, K.eqbeam22(x)[0]) for x in K.T22_X]
    o += P([(ax(x), base - sy * v) for x, v in pts], KEY, 4.5)
    o += T(ax(0) - 10, base - sy + 5, '1', 15, KEY, 'end', 'bold')
    o += T(ax(8.5), base - 78, '繞 b 轉：斜率 −1/12', 15, KEY, 'middle', 'bold')
    o += T(ax(15), base - sy * 0.25 - 12, '+1/4', 15, KEY, 'middle', 'bold')
    o += T(ax(21), base + sy * 0.25 + 24, '−1/4', 15, KEY, 'middle', 'bold')
    o += T(ax(18), base + 72, '滑塊：兩邊平行（同斜率），且要過 c 的 0', 15, WARN, 'middle', 'bold')
    o += R(110, 866, 680, 56, KEY2, KEY, 1.3, 9)
    o += T(450, 900, '第 2 章的 Müller-Breslau 原封不動：桁架的「沒有斜桿」＝滑塊、「只剩交於一點的桿」＝鉸', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2022-3 等效梁')


def fig3_5():
    """SA-2022-3 題目所求五條影響線（桁架求解器逐節點算出）。"""
    W, H = 900, 1120
    ax = Ax(110, 22)
    o = ''
    yb = 50
    o += L(ax(0), yb, ax(30), yb, INK, 4)
    for x, nm in ((0, 'a'), (6, 'm'), (9, 'n'), (12, 'b'), (18, 'c'), (21, 'd'), (30, 'e')):
        o += C(ax(x), yb, 4.5, '#fff', INK, 1.4)
        o += T(ax(x), yb - 14, nm, 16, INK, 'middle', 'bold')
    tk = K.T22_X
    TB = K.T22_TAB

    def pts(k):
        return list(zip(tk, TB[k]))
    rows = [
        ('Ra', 200, 100, 'IL *R*_{*a*}', [(0, 1, '1', 'w'), (15, .25, '1/4', 'n'), (21, -.25, '−1/4', 's')]),
        ('Rb', 390, 100, 'IL *R*_{*b*}', [(12, 1, '1', 'n'), (15, -.25, '−1/4', 's'), (21, .25, '1/4', 'n')]),
        ('Rc', 600, 100, 'IL *R*_{*c*}', [(15, 1, '1', (-14, -10)), (21, 1, '1', (14, -10))]),
        ('Nmn', 800, 130, 'IL *N*_{*mn*}', [(6, .75, '3/4', 'n'), (15, .375, '3/8', 'n'), (21, -.375, '−3/8', 's')]),
        ('Nnk', 990, 130, 'IL *N*_{*nk*}', [(6, -.625, '−5/8', 's'), (9, .3125, '5/16', 'n'), (15, .3125, '5/16', 'n'), (21, -.3125, '−5/16', 's')]),
    ]
    for k, base, sy, nm, vals in rows:
        o += il(ax, base, sy, pts(k), name=nm, ticks=tk, vals=vals)
    o += C(ax(8), 990, 4, AC, '#fff', 1.4)
    o += T(ax(8) - 6, 1020, '8 m', 14, AC, 'end', 'bold')
    for x in (12, 15, 21):
        o += L(ax(x), 64, ax(x), 1080, STEEL, 1, '3 4')
    o += T(ax(13.5), 1106, '12–15 無斜桿', 14, MUT, 'middle')
    o += T(ax(21) + 8, 1106, 'd', 14, MUT, 'start')
    return svg(W, H, o, 'SA-2022-3 五條影響線')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4, 'fig3_5': fig3_5}
