# -*- coding: utf-8 -*-
"""第 6 章：互易定理。數值全部取自 calcs.py（含有限元素交叉驗算）。"""
from figs_common import *  # noqa
import calcs as K
from fractions import Fraction as Fr

DEF = KEY


def fig6_1():
    """Betti／Maxwell：同一根簡支梁兩個狀態，力與位移位置互換。"""
    W, H = 900, 590
    ax = Ax(150, 56)
    o = ''
    sy = 3.2
    i_, j_ = 3.0, 6.0
    rows = [(150, i_, j_, '狀態Ⓐ：1 在 *i*（3 m），量 *j*（6 m）的下垂 *f*_{*ji*}', COMP),
            (350, j_, i_, '狀態Ⓑ：1 在 *j*（6 m），量 *i*（3 m）的下垂 *f*_{*ij*}', AC)]
    for y, xp, xm, title, c in rows:
        o += T(14, y - 106, title, 16, INK, 'start', 'bold')
        o += L(ax(0), y, ax(10), y, STEEL3, 4, '8 6') + pin(ax(0), y + 3) + roller(ax(10), y + 3)
        pts = [(ax(t), y + sy * K.ss_defl(xp, t)) for t in np.linspace(0, 10, 120)]
        o += P(pts, c, 4.5)
        o += unit_load(ax(xp), y + sy * K.ss_defl(xp, xp) - 3, c=c, h=46)
        d = K.ss_defl(xp, xm)
        o += L(ax(xm), y - 30, ax(xm), y + sy * d + 18, INK, 1, '4 4')
        o += C(ax(xm), y + sy * d, 5, '#fff', INK, 1.6)
        o += T(ax(xm) + 10, y + sy * d + 28, f'{f(d)}/*EI*', 16, INK, 'start', 'bold')
        o += T(ax(i_), y - 40, '*i*', 16, MUT, 'middle', 'bold') if xp != i_ else ''
        o += T(ax(j_), y - 40, '*j*', 16, MUT, 'middle', 'bold') if xp != j_ else ''
    o += R(40, 460, 820, 116, KEY2, KEY, 1.4, 10)
    o += T(450, 490, 'Ⓐ 的力 × Ⓑ 的位移：1 × *f*_{*ij*}　　Ⓑ 的力 × Ⓐ 的位移：1 × *f*_{*ji*}', 16, INK, 'middle', 'bold')
    o += T(450, 524, '兩者都等於 ∫ *M*_{Ⓐ}*M*_{Ⓑ} / *EI* *dx*（對 Ⓐ、Ⓑ 對稱）　⇒　*f*_{*ij*} = *f*_{*ji*}', 17, KEY, 'middle', 'bold')
    o += T(450, 558, f'數字：兩個都是 {f(K.BETTI_63)}/*EI*（由有限元素直接算出，不是用公式湊的）', 15, INK, 'middle')
    return svg(W, H, o, '互易定理')


def fig6_2():
    """SA-2018-4：橋梁＋斜撐；C 受向下 1 時的對稱變形。"""
    W, H = 900, 610
    F = Frame(110, 160, 34)          # 20 m → 680 px
    o = ''
    o += T(14, 30, '(a) 題目：A、E 滾支承；斜撐 BF、DG 下端固定；*EI* = 800 kN·m²（全部）', 16, INK, 'start', 'bold')
    A_, B_, C_, D_, E_ = (F(x, 0) for x in (0, 5, 10, 15, 20))
    F_, G_ = F(2, -4), F(18, -4)
    o += member(A_, E_, INK, 5) + member(F_, B_, INK, 4) + member(G_, D_, INK, 4)
    o += roller(A_[0], A_[1] + 3) + roller(E_[0], E_[1] + 3)
    o += fixed_bottom(F_[0], F_[1], 46) + fixed_bottom(G_[0], G_[1], 46)
    for p, nm, dx in ((A_, 'A', 0), (B_, 'B', 0), (C_, 'C', 0), (D_, 'D', 0), (E_, 'E', 0)):
        o += T(p[0] + dx, p[1] - 14, nm, 16, INK, 'middle', 'bold')
    o += T(F_[0] - 14, F_[1] - 6, 'F', 16, INK, 'end', 'bold') + T(G_[0] + 14, G_[1] - 6, 'G', 16, INK, 'start', 'bold')
    o += dim(A_[0], 70, E_[0], 70, '4 @ 5 m', MUT, size=15)
    o += T(F(3.5, -2)[0] - 14, F(3.5, -2)[1] + 4, '斜撐 5 m（3:4）', 15, MUT, 'end')
    # (b) 變形
    o += T(14, 350, '(b) C 受向下 1：對稱 ⇒ B、D 不能平移（斜撐不計軸變），只能轉 θ_{*B*} = 1/1024', 16, INK, 'start', 'bold')
    y0 = 450
    ax = Ax(110, 34)
    sc = 7000
    o += L(ax(0), y0, ax(20), y0, STEEL3, 3, '8 6')
    o += P([(ax(t), y0 + sc * K.v18(t)) for t in np.linspace(0, 20, 241)], DEF, 4.5)
    for x, nm in ((0, 'A'), (5, 'B'), (15, 'D'), (20, 'E')):
        o += C(ax(x), y0, 5, '#fff', INK, 1.6) + T(ax(x), y0 - 14, nm, 15, INK, 'middle', 'bold')
    o += unit_load(ax(10), y0 + sc * K.v18(10) - 3, h=44)
    o += T(ax(2.9), y0 + sc * K.V18_MIN - 14, '外跨被翹起', 15, DEF, 'middle', 'bold')
    o += T(ax(11.2), y0 + sc * K.V18_C + 18, '*v*_{*C*} = 55/6144 m', 15, DEF, 'start', 'bold')
    o += R(40, 548, 820, 50, KEY2, KEY, 1.3, 9)
    o += T(450, 579, '節點 B 的轉動勁度：3*EI*/5（AB，A 端滾）＋ 4*EI*/5（BF，F 端固定）＋ 2*EI*/10（BD，對稱）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2018-4 結構與變形')


def fig6_3():
    """SA-2018-4：C 點向下位移影響線（m/kN）。"""
    W, H = 900, 420
    ax = Ax(110, 34)
    o = ''
    yb = 50
    o += L(ax(0), yb, ax(20), yb, INK, 4)
    for x, nm in ((0, 'A'), (5, 'B'), (10, 'C'), (15, 'D'), (20, 'E')):
        o += C(ax(x), yb, 4.5, '#fff', INK, 1.4) + T(ax(x), yb - 14, nm, 15, INK, 'middle', 'bold')
    base, sy = 300, 24000
    pts = dense18()
    vals = [(10, K.V18_C, '8.95×10⁻³', 'n'), (K.V18_MIN_X, K.V18_MIN, '−0.94×10⁻³', (0, 26)),
            (20 - K.V18_MIN_X, K.V18_MIN, '−0.94×10⁻³', (0, 26))]
    o += il(ax, base, sy, pts, ticks=(0, 5, 10, 15, 20), vals=vals, name='IL *v*_{*C*}', name_x=8)
    o += T(14, base + 46, '（m/kN，向下為正）', 14, MUT, 'start')
    o += T(ax(K.V18_MIN_X), base + 66, 'x = 5/√3 = 2.887', 14, MUT, 'middle')
    o += T(ax(20 - K.V18_MIN_X), base + 66, 'x = 17.113', 14, MUT, 'middle')
    o += T(ax(12.6), 140, '＝ 圖 6-2(b) 的撓度曲線本身', 16, KEY, 'start', 'bold')
    o += T(ax(12.6), 166, '不除任何東西', 16, KEY, 'start', 'bold')
    return svg(W, H, o, 'SA-2018-4 位移影響線')


def dense18():
    return [(t, K.v18(t)) for t in np.linspace(0, 20, 401)]


T21_LAB = {'a': (-14, 8), 'b': (0, 28), 'c': (0, 28), 'd': (0, 28), 'e': (14, 8), 'f': (0, -14), 'g': (0, -14), 'h': (0, -14)}


def fig6_4():
    """SA-2021-3：兩端鉸支桁架；基本結構把 e 改成滾支承。"""
    W, H = 900, 470
    o = ''
    F1 = Frame(60, 200, 30)          # 12 m → 360 px
    o += T(14, 30, '(a) 題目：a、e 皆為鉸支承（1 度靜不定）', 16, INK, 'start', 'bold')
    o += truss_draw(F1, K.T21, K.T21_MEM, {'a': 'pin', 'e': 'pin'}, T21_LAB, {('a', 'b'): (TEN, 5), ('b', 'g'): (WARN, 5)})
    o += dim(F1(0, 0)[0], 250, F1(12, 0)[0], 250, '4 @ 3 m', MUT, size=15)
    F2 = Frame(490, 200, 30)
    o += T(470, 30, '(b) 基本結構：e 改滾支承，兩端施一對 1 往外拉', 16, INK, 'start', 'bold')
    hl = {m: (COMP, 5) for m in [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]}
    o += truss_draw(F2, K.T21, K.T21_MEM, {'a': 'pin', 'e': 'roller'}, T21_LAB, hl)
    o += A(F2(0, 0)[0] - 8, F2(0, 0)[1] - 22, F2(0, 0)[0] - 54, F2(0, 0)[1] - 22, KEY, 2.4, 10)
    o += A(F2(12, 0)[0] + 8, F2(12, 0)[1] - 22, F2(12, 0)[0] + 54, F2(12, 0)[1] - 22, KEY, 2.4, 10)
    o += T(F2(0, 0)[0] - 30, F2(0, 0)[1] - 30, '1', 15, KEY, 'middle', 'bold') + T(F2(12, 0)[0] + 30, F2(12, 0)[1] - 30, '1', 15, KEY, 'middle', 'bold')
    o += T(F2(6, 0)[0], 260, '只有下弦四根受拉 *u* = 1（紅）', 15, COMP, 'middle', 'bold')
    o += R(40, 290, 820, 168, KEY2, KEY, 1.4, 10)
    o += T(450, 320, '*f*_{*ee*} = Σ *u*²*L*/*EA* = 4 × 3/*EA* = 12/*EA*', 17, KEY, 'middle', 'bold')
    o += T(450, 352, '單位載重在節點 *i*：e 往外滑 *v*_{*i*} = Σ *u*·*S*⁰·*L*/*EA* = 3 × (下弦四根 *S*⁰ 之和)/*EA*', 16, INK, 'middle', 'bold')
    o += T(450, 384, f'*v*_{{b}}, *v*_{{c}}, *v*_{{d}} = {f(K.T21_VE[1])}, {f(K.T21_VE[2])}, {f(K.T21_VE[3])}（×1/*EA*）', 16, INK, 'middle')
    o += T(450, 418, '鉸支承把它推回來：*H*(*x*) = *v*(*x*) / *f*_{*ee*}　（又是除以自身柔度）', 17, KEY, 'middle', 'bold')
    o += T(450, 444, '互易：*v*_{*i*} 也是「兩端拉 1 時節點 *i* 的下垂」——拆、推、量、除，和第 5 章完全相同', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2021-3 基本結構')


def fig6_5():
    """SA-2021-3：H_a、S_ab、S_bg 影響線（S_ab 對照靜定值）。"""
    W, H = 900, 820
    ax = Ax(150, 50)                 # 12 m → 600 px
    o = ''
    yb = 50
    o += L(ax(0), yb, ax(12), yb, INK, 4)
    for x, nm in zip(K.T21_X, K.T21_LN):
        o += C(ax(x), yb, 4.5, '#fff', INK, 1.4) + T(ax(x), yb - 14, nm, 15, INK, 'middle', 'bold')
    tk = K.T21_X

    def fr(v):
        return str(Fr(v).limit_denominator(64)).replace('-', '−')
    base, sy = 230, 200
    o += il(ax, base, sy, list(zip(tk, K.T21_HA)), name='IL *H*_{*a*}', name_x=14, ticks=tk,
            vals=[(x, v, fr(v), 'n') for x, v in zip(tk[1:4], K.T21_HA[1:4])])
    o += T(ax(12) + 14, base - 40, '向右（推力）', 15, MUT, 'start')
    base, sy = 470, 220
    o += P([(ax(x), base - sy * v) for x, v in zip(tk, K.T21_SAB0)], STEEL, 2, dash='6 5')
    o += T(ax(3) + 8, base - sy * K.T21_SAB0[1] - 6, '灰虛線：靜定 *S*⁰（9/16）', 15, MUT, 'start')
    o += il(ax, base, sy, list(zip(tk, K.T21_SAB)), name='IL *S*_{*ab*}', name_x=14, ticks=tk,
            vals=[(3, K.T21_SAB[1], '3/16', (0, -14)), (6, K.T21_SAB[2], '−3/16', 's'), (9, K.T21_SAB[3], '−3/16', 's')])
    o += T(ax(12) + 14, base - 40, '= *S*⁰ − *H*', 15, KEY, 'start', 'bold')
    base, sy = 660, 160
    o += il(ax, base, sy, list(zip(tk, K.T21_SBG)), name='IL *S*_{*bg*}', name_x=14, ticks=tk,
            vals=[(3, K.T21_SBG[1], '5/16', 'n'), (6, K.T21_SBG[2], '−5/8', 's'), (9, K.T21_SBG[3], '−5/16', 's')])
    o += T(ax(12) + 14, base - 40, '= *S*⁰（推力', 15, KEY, 'start', 'bold')
    o += T(ax(12) + 14, base - 16, '不影響斜桿）', 15, KEY, 'start', 'bold')
    return svg(W, H, o, 'SA-2021-3 影響線')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4, 'fig6_5': fig6_5}
