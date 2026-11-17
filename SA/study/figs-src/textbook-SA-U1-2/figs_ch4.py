# -*- coding: utf-8 -*-
"""第 4 章：桁架 II（截面法、取矩點、K 型與三鉸桁架、移動載重）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import (N14, B14, F14, R14, IL_CD_14, il_cd_formula, M_beam14, CHORD14, ARM_IJ_D,
                   N03, B03, F03, R03, CUT03_BAD, CUT03_OK, A03, B03b,
                   N0202, B0202, F0202, R0202t, ABCDE_0202, N13, F13, R13, S2)
from figs_ch3 import truss, labels, legend, sgn, _ends
from fractions import Fraction as Fr
import math


def frac(v, den=1000):
    q = Fr(v).limit_denominator(den)
    s = f'{abs(q.numerator)}/{q.denominator}' if q.denominator != 1 else f'{abs(q.numerator)}'
    return ('−' if q < 0 else '') + s


def cutline(x, y1, y2, c=WARN):
    pts = []
    n = 12
    for i in range(n + 1):
        y = y1 + (y2 - y1) * i / n
        pts.append((x + (5 if i % 2 else -5), y))
    return P(pts, c, 2.2, dash='7 4')


# ───────────────────────────────────────────── 4.1 SA-2014-1
def fig4_1():
    """SA-2014-1：一刀切三根桿。"""
    W, H = 900, 400
    f = Frame(90, 300, 10)
    o = T(W / 2, 30, 'SA-2014-1：在 C、D 之間切一刀，剛好切斷 IJ、ID、CD 三根桿', 17, INK, 'middle', 'bold')
    o += truss(f, N14, B14)
    P_ = {k: f(*v) for k, v in N14.items()}
    for b in ('IJ', 'ID', 'CD'):
        p, q = _ends(b, N14)
        o += L(*P_[p], *P_[q], WARN, 5.5)
    for k, (x, y) in P_.items():
        o += C(x, y, 5, '#fff', INK, 1.5)
    o += pin(*P_['A']) + roller(*P_['G'])
    o += force(P_['C'], 90, 52, COMP, 2.8, '*P*', 17, (14, 10), 'start')
    xc = f(30, 0)[0]
    o += cutline(xc, f(0, 25)[1], f(0, -4)[1])
    o += labels(f, N14, dict(A=(-18, 4), B=(0, 24), C=(14, 24), D=(0, 26), E=(0, 24), F=(0, 24), G=(18, 4),
                             H=(-12, -10), I=(-8, -12), J=(0, -12), K=(8, -12), L=(12, -10)))
    for i in range(6):
        o += dim(f(12 * i, 0)[0], 352, f(12 * (i + 1), 0)[0], 352, '12', MUT, 0, 14)
    o += T(f(72, 0)[0] + 16, 357, 'm', 14, MUT, 'start')
    for k, h in (('H', 12), ('I', 17), ('J', 22)):
        o += T(P_[k][0] - 4, P_[k][1] + 34 + (0 if k != 'J' else 10), f'{h}', 14, AC, 'end')
    o += R(20, 48, 250, 98, KEY2, KEY, 1.4, 10)
    o += T(145, 70, '切出來的左半部＝一個自由體', 15, KEY, 'middle', 'bold')
    o += T(145, 94, 'S1 給 3 條方程', 15, INK, 'middle')
    o += T(145, 116, '切斷 3 根桿 → 3 個未知', 15, INK, 'middle')
    o += T(145, 138, '剛好解完', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2014-1 截面')


def fig4_2():
    """左自由體：對 I 取矩求 CD；對 D 取矩求 IJ（把力滑到 J 再分解）。"""
    W, H = 900, 530
    o = ''
    s = 10
    for k, (ox, title) in enumerate(((50, '(a) 對 I 取矩：IJ、ID 都通過 I，消失'), (475, '(b) 對 D 取矩：把 *F*_{IJ} 滑到 J 再拆'))):
        s = 10 if k == 0 else 8.6
        f = Frame(ox, 330, s)
        nodes = {n: N14[n] for n in 'ABCHI'}
        bars = ['AH', 'HI', 'AB', 'BC', 'BH', 'CI', 'HC']
        o += T(ox + 200, 32, title, 16, INK, 'middle', 'bold')
        o += truss(f, nodes, bars)
        P_ = {n: f(*v) for n, v in nodes.items()}
        o += pin(*P_['A'])
        o += force(P_['C'], 90, 44, COMP, 2.6, '*P*', 16, (12, 8), 'start')
        ax, ay = P_['A']
        o += A(ax + 22, ay + 62, ax + 22, ay + 26, TEN, 2.6, 11) + T(ax + 30, ay + 60, '2*P*/3', 15, TEN, 'start', 'bold')
        # 切斷桿的力（拉：離開自由體）
        I_, C_ = P_['I'], P_['C']
        ux, uy = 12 / 13, -5 / 13
        if k == 0:
            o += A(I_[0], I_[1], I_[0] + 60 * ux, I_[1] + 60 * uy, WARN, 2.8, 12)
            o += T(I_[0] + 64 * ux + 4, I_[1] + 60 * uy - 6, '*F*_{IJ}', 15, WARN, 'start', 'bold')
        dl = math.hypot(12, 17)
        o += A(I_[0], I_[1], I_[0] + 62 * 12 / dl, I_[1] + 62 * 17 / dl, WARN, 2.8, 12)
        o += T(I_[0] + 62 * 12 / dl + 6, I_[1] + 62 * 17 / dl + 4, '*F*_{ID}', 15, WARN, 'start', 'bold')
        o += A(C_[0], C_[1], C_[0] + 62, C_[1], WARN, 2.8, 12)
        o += T(C_[0] + 66, C_[1] + 22, '*F*_{CD}', 15, WARN, 'start', 'bold')
        o += labels(f, nodes, dict(A=(-16, -6), B=(0, 24), C=(-12, 24), H=(-12, -10), I=(-10, -14)))
        if k == 0:
            o += C(*I_, 11, 'none', KEY, 2.4)
            o += dim(I_[0] + 100, I_[1], C_[0] + 100, C_[1], '17', KEY, 0, 15, side=1, weight='bold')
            o += L(I_[0], I_[1], I_[0] + 106, I_[1], KEY, 1, '3 3') + L(C_[0] + 70, C_[1], C_[0] + 106, C_[1], KEY, 1, '3 3')
            o += dim(ax, ay + 80, I_[0], ay + 80, '24', MUT, 0, 14)
            o += R(ox, 446, 400, 70, KEY2, KEY, 1.3, 8)
            o += T(ox + 200, 472, 'Σ*M*_{I} = −(2*P*/3)(24) + 17 *F*_{CD} = 0', 15, INK, 'middle')
            o += T(ox + 200, 500, f'*F*_{{CD}} = 16*P*/17 = {frac(F14["CD"])} *P*（拉）', 15, KEY, 'middle', 'bold')
        else:
            Dp = f(36, 0); Jp = f(36, 22)
            o += C(*Dp, 11, 'none', KEY, 2.4) + C(*Dp, 5, KEY, '#fff', 1.4) + T(Dp[0] + 14, Dp[1] + 22, 'D', 16, KEY, 'start', 'bold')
            o += L(*I_, *Jp, WARN, 1.5, '6 4') + C(*Jp, 4, WARN, None) + T(Jp[0] - 10, Jp[1] - 8, 'J', 16, KEY, 'end', 'bold')
            o += L(*Jp, *Dp, KEY, 1.2, '3 4')
            o += A(Jp[0], Jp[1], Jp[0] + 50, Jp[1], WARN, 2.4, 11)
            o += A(Jp[0], Jp[1], Jp[0], Jp[1] - 40, MUT, 2.0, 10)
            o += T(Jp[0] + 2, Jp[1] + 24, '12/13·*F*_{IJ}', 14, WARN, 'start', 'bold')
            o += T(Jp[0] + 8, Jp[1] - 28, '5/13·*F*_{IJ}', 14, MUT, 'start')
            o += T(Jp[0] - 8, Dp[1] - 44, '作用線', 14, MUT, 'end') + T(Jp[0] - 8, Dp[1] - 24, '通過 D', 14, MUT, 'end')
            o += T(Jp[0] - 50, Jp[1] - 4, '*F*_{IJ}', 15, WARN, 'end', 'bold')
            o += dim(Dp[0] + 64, Dp[1], Jp[0] + 64, Jp[1], '', KEY, 0, 15) + T(Dp[0] + 72, (Dp[1] + Jp[1]) / 2 + 20, '22', 15, KEY, 'start', 'bold')
            o += R(ox, 446, 410, 70, KEY2, KEY, 1.3, 8)
            o += T(ox + 205, 472, 'Σ*M*_{D} = −24*P* + 12*P* − 22·(12/13)*F*_{IJ} = 0', 15, INK, 'middle')
            o += T(ox + 205, 500, f'*F*_{{IJ}} = −13*P*/22 = {frac(F14["IJ"])} *P*（壓）', 15, KEY, 'middle', 'bold')
    o += L(455, 50, 455, 410, GRID, 1.5)
    return svg(W, H, o, '截面法取矩點')


def fig4_3():
    """桁架＝挖空的梁：下弦桿力 = 簡支梁 M(取矩點) / 取矩點高度。"""
    W, H = 900, 520
    o = T(W / 2, 30, '桁架就是挖空的梁：下弦桿力 ＝ 同跨簡支梁在「取矩點」的彎矩 ÷ 那一點的高度', 16, INK, 'middle', 'bold')
    f = Frame(110, 270, 9.4)
    vals = {b: frac(F14[b]) + ' P' for b, _ in CHORD14}
    o += truss(f, N14, B14, F14, fmax=1.1, vals=vals, voff={b: (0, 22) for b, _ in CHORD14}, wmax=7)
    P_ = {k: f(*v) for k, v in N14.items()}
    o += pin(*P_['A']) + roller(*P_['G'])
    o += force(P_['C'], 90, 40, COMP, 2.6, '*P*', 16, (12, 10), 'start')
    for b, c in CHORD14:
        o += C(*P_[c], 9, 'none', KEY, 2.2)
    o += labels(f, N14, dict(H=(-12, -12), I=(-6, -14), K=(6, -14), L=(12, -12), C=(-14, 20)))
    # 彎矩圖
    pl = Plot(110, 340, 72 * 9.4, 120, 0, 72, 0, 18)
    o += pl.area(lambda x: M_beam14(x) * 1.0, lambda x: 0, 0, 72, KEY2, 0.9)
    o += pl.curve(lambda x: M_beam14(x), 0, 72, KEY, 2.4)
    o += L(pl.X(0), pl.Y(0), pl.X(72), pl.Y(0), INK, 1.4)
    o += T(pl.X(0) - 10, pl.Y(0) + 5, '0', 14, MUT, 'end')
    o += T(pl.X(24), pl.Y(16) - 10, '*M*_{max} = 16*P*（C 點）', 15, KEY, 'middle', 'bold')
    for b, c in CHORD14:
        x, h = N14[c]
        m = M_beam14(x)
        o += L(pl.X(x), pl.Y(m), P_[c][0], P_[c][1], KEY, 1, '3 4')
        o += pl.dot(x, m, KEY, 5)
        if x != 24:
            o += T(pl.X(x) + 10, pl.Y(m) - 8, f'{frac(m)}*P*', 15, KEY, 'start', 'bold')
    o += T(pl.X(0) - 10, pl.Y(18) + 4, '*M*', 15, KEY, 'end', 'bold')
    rows = []
    for b, c in CHORD14:
        x, h = N14[c]
        m = M_beam14(x)
        rows.append(f'{b}：取矩點 {c}，*M* = {frac(m)}*P*，*h* = {h} → {frac(m / h)}*P*')
    o += R(110, 476, 680, 36, '#fff', GRID, 1.2, 8)
    o += T(450, 500, '　'.join(r.split('：')[0] + '＝' + r.split('→ ')[1] for r in rows) + '（全部與節點法相同）', 15, INK, 'middle')
    return svg(W, H, o, '桁架與梁的類比')


# ───────────────────────────────────────────── 4.3 K 型 SA-2003-3
def fig4_4():
    W, H = 900, 560
    f = Frame(130, 300, 20)
    o = T(W / 2, 30, 'SA-2003-3（K 型細分）：直切常常切到 4 根；換個地方切，剛好 3 根', 17, INK, 'middle', 'bold')
    names = {A03: 'a', B03b: 'b'}
    show = {A03: f'a = {sgn(F03[A03])}', B03b: 'b = +1.5√2', 'U1U2': sgn(F03['U1U2']), 'L0M1': '−2.5√2',
            'M1U1': '−1.5√2', 'M1L1': '+√2'}
    voff = {A03: (0, -16), B03b: (34, -16), 'U1U2': (0, -18), 'L0M1': (-36, 0), 'M1U1': (-36, -4), 'M1L1': (-18, 14)}
    o += truss(f, N03, [''.join(b) for b in B03], F03, fmax=3.6, vals=show, voff=voff)
    P_ = {k: f(*v) for k, v in N03.items()}
    o += pin(*P_['L0']) + roller(*P_['L4'])
    for n in ('L1', 'L2'):
        x, y = P_[n]
        o += A(x, y + 8, x, y + 50, COMP, 2.6, 11) + T(x + 8, y + 46, '2 t', 15, COMP, 'start', 'bold')
    o += labels(f, N03, dict(L0=(-20, 4), L1=(-14, 22), L2=(16, 22), L3=(0, 24), L4=(22, 4), M1=(-22, -2), M2=(4, 24),
                             M3=(-4, 24), M4=(22, -2), U1=(-12, -12), U2=(0, -14), U3=(12, -12)), 15)
    # 切線
    x6, x14 = f(6, 0)[0], f(14, 0)[0]
    o += cutline(x6, f(0, 10)[1], f(0, -1.2)[1], COMP)
    o += T(x6, f(0, 10)[1] - 8, '切到 4 根', 15, COMP, 'middle', 'bold')
    o += cutline(x14, f(0, 10)[1], f(0, -1.2)[1], WARN)
    o += T(x14, f(0, 10)[1] - 8, '切到 3 根', 15, WARN, 'middle', 'bold')
    o += C(*P_['L2'], 12, 'none', KEY, 2.4)
    o += legend(130, 540)
    o += R(40, 388, 820, 128, '#fff', GRID, 1.4, 10)
    o += T(450, 414, '路線（每一步只有 1～2 個未知）', 15, KEY, 'middle', 'bold')
    rows = ['① 截面 x = 12～16，對 L2 取矩', f'　 → U1U2 = {sgn(F03["U1U2"])} t（壓）', '② 節點 U1 → b = +1.5√2 t（拉）',
            '③ 節點 L0 → L0M1 = −2.5√2 t', '④ 節點 M1：Σ*F*_{y} → M1L1 = +√2', f'　 Σ*F*_{{x}} → a = {sgn(F03[A03])} t（壓）']
    for i, s in enumerate(rows):
        o += T(70 + (i // 3) * 400, 444 + (i % 3) * 28, s, 15, INK, 'start')
    return svg(W, H, o, 'SA-2003-3 K 型桁架')


# ───────────────────────────────────────────── 4.4 三鉸桁架
def fig4_5():
    """SA-2002-2：a～e。左半用節點、右半用截面（對 G 取矩）。"""
    W, H = 900, 530
    f = Frame(110, 360, 19)
    o = T(W / 2, 30, 'SA-2002-2：反力先靠中間鉸 C（第 2 章），再左邊走節點、右邊切截面', 17, INK, 'middle', 'bold')
    show = {}
    for k, b in ABCDE_0202.items():
        show[b] = f'{k} = {frac(F0202[b], 100)}'
    voff = dict(DF=(0, -20), DE=(-6, 20), AE=(-28, 10), CH=(30, -20), CG=(10, 22))
    o += truss(f, N0202, B0202, F0202, fmax=45, vals=show, voff=voff)
    P_ = {k: f(*v) for k, v in N0202.items()}
    o += pin(*P_['A']) + pin(*P_['B'])
    for k in 'DFCHI':
        o += force(P_[k], 90, 40, COMP, 2.4, '20', 15, (12, 6), 'start')
    o += force(P_['D'], 180, 46, COMP, 2.4, '16', 15, (-6, -8))
    o += labels(f, N0202, dict(A=(-20, 4), B=(20, 4), D=(-20, 20), F=(-12, 22), C=(14, 22), H=(12, 22), I=(20, 20), E=(-6, 24), G=(8, 24)))
    o += C(*P_['G'], 12, 'none', KEY, 2.4)
    xc = f(17.6, 0)[0]
    o += cutline(xc, f(0, 14.5)[1], f(0, 4)[1], WARN)
    ax, ay = P_['A']; bx, by = P_['B']
    o += T(ax - 6, ay + 44, f'*A*_{{x}} = {frac(R0202t[("A", 0)], 10)} →、*A*_{{y}} = {frac(R0202t[("A", 1)])} ↑', 15, TEN, 'start', 'bold')
    o += T(bx + 6, by + 44, f'*B*_{{x}} = {frac(-R0202t[("B", 0)], 10)} ←、*B*_{{y}} = {frac(R0202t[("B", 1)])} ↑', 15, TEN, 'end', 'bold')
    o += R(110, 430, 330, 60, '#fff', GRID, 1.2, 8)
    o += T(275, 454, '左：節點 A → c；節點 D → b、a', 15, INK, 'middle')
    o += T(275, 478, '（每站 2 個未知）', 15, MUT, 'middle')
    o += R(460, 430, 400, 60, KEY2, KEY, 1.2, 8)
    o += T(660, 454, '右半部切 CH、CG：對 G 取矩 → d', 15, KEY, 'middle', 'bold')
    o += T(660, 478, 'Σ*F*_{y} → e（CH 水平，沒有垂直分量）', 15, INK, 'middle')
    o += legend(110, 515)
    return svg(W, H, o, 'SA-2002-2 a～e')


def fig4_6():
    """SA-2013-1：左半部只切 de、ke 兩根 → ΣFy 直接得 ke（＝梁的剪力）。"""
    W, H = 900, 480
    f = Frame(150, 400, 10)
    o = T(W / 2, 30, 'SA-2013-1：從 e 剪開，左半部只切到 de、ke；de 是水平的', 17, INK, 'middle', 'bold')
    nodes = {n: N13[n] for n in 'albkcd'}
    bars = ['cd', 'cb', 'ba', 'ck', 'dk', 'bk', 'bl', 'lk', 'al']
    o += truss(f, nodes, bars)
    P_ = {k: f(*v) for k, v in nodes.items()}
    o += pin(*P_['a'])
    for k, w in dict(c=5, d=10).items():
        o += force(P_[k], 90, 38, COMP, 2.4, str(w), 15, (12, 4), 'start')
    ax, ay = P_['a']
    o += A(ax - 60, ay + 30, ax - 14, ay + 30, TEN, 2.6, 11) + T(ax - 64, ay + 35, f'{R13[("a", 0)]:g}', 15, TEN, 'end', 'bold')
    o += A(ax + 22, ay + 66, ax + 22, ay + 24, TEN, 2.6, 11) + T(ax + 30, ay + 62, f'{R13[("a", 1)]:g}', 15, TEN, 'start', 'bold')
    d_, k_ = P_['d'], P_['k']
    o += A(d_[0], d_[1], d_[0] + 56, d_[1], WARN, 2.8, 12) + T(d_[0] + 66, d_[1] + 5, '*F*_{de}', 15, WARN, 'start', 'bold')
    o += A(k_[0], k_[1], k_[0] + 44, k_[1] - 44, WARN, 2.8, 12) + T(k_[0] + 58, k_[1] - 40, '*F*_{ke}', 15, WARN, 'start', 'bold')
    o += labels(f, nodes, dict(a=(-18, 6), l=(16, 18), b=(-16, 6), k=(14, 22), c=(-16, -6), d=(-12, -12)))
    o += cutline(f(15, 0)[0] + 4, f(0, 35)[1], f(0, 15)[1])
    o += R(440, 110, 450, 200, KEY2, KEY, 1.4, 10)
    o += T(665, 138, '左半部 Σ*F*_{y} = 0（de 沒有垂直分量）', 15, KEY, 'middle', 'bold')
    o += T(665, 172, '22 − 5 − 10 + *F*_{ke}/√2 = 0', 15, INK, 'middle')
    o += T(665, 204, f'*F*_{{ke}} = −7√2 ≈ −{abs(F13["ke"]):.2f} kN（壓）', 15, KEY, 'middle', 'bold')
    o += T(665, 242, '22 − 5 − 10 ＝ 7 就是這個斷面的「梁剪力」', 15, INK, 'middle')
    o += T(665, 270, '斜腹桿的垂直分量負責扛剪力', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2013-1 截面')


# ───────────────────────────────────────────── 4.5 移動載重
def fig4_7():
    W, H = 900, 420
    o = T(W / 2, 30, 'SA-2014-1：*P* 走到哪一個節點時，CD 桿受力最大？', 17, INK, 'middle', 'bold')
    pl = Plot(110, 70, 620, 260, 0, 72, 0, 1.0)
    o += pl.axes([0, 12, 24, 36, 48, 60, 72], [0, 0.25, 0.5, 0.75, 1.0], '*x*（m）', '*F*_{CD}/*P*',
                 xfmt=lambda t: f'{t:g}', yfmt=lambda t: f'{t:g}', size=14)
    o += pl.curve(il_cd_formula, 0, 72, KEY, 2.6)
    o += pl.vline(30, 0, 1.0, WARN, 1.6, '7 4')
    o += T(pl.X(30) + 6, pl.Y(0.98), '截面（C、D 之間）', 14, WARN, 'start', 'bold')
    for nm, x in zip('BCDEF', (12, 24, 36, 48, 60)):
        v = IL_CD_14[nm]
        o += pl.dot(x, v, COMP if nm == 'C' else KEY, 6)
        if nm == 'C':
            o += T(pl.X(x) - 12, pl.Y(v) - 10, f'{nm}：{frac(v, 100)}', 15, COMP, 'end', 'bold')
        elif nm == 'B':
            o += T(pl.X(x) + 14, pl.Y(v) + 22, f'{nm}：{frac(v, 100)}', 15, KEY, 'start', 'bold')
        else:
            o += T(pl.X(x) + 10, pl.Y(v) - 14, f'{nm}：{frac(v, 100)}', 15, KEY, 'start', 'bold')
    o += T(pl.X(4), pl.Y(0.42), '2*x*/51', 15, KEY, 'middle', 'bold')
    o += T(pl.X(38), pl.Y(0.42), '(72 − *x*)/51', 15, KEY, 'start', 'bold')
    o += R(748, 80, 145, 170, KEY2, KEY, 1.3, 10)
    o += T(820, 106, '載重在右', 15, KEY, 'middle', 'bold')
    o += T(820, 130, '→ 用左半部', 15, INK, 'middle')
    o += T(820, 170, '載重在左', 15, KEY, 'middle', 'bold')
    o += T(820, 194, '→ 用右半部', 15, INK, 'middle')
    o += T(820, 232, '自由體上沒有 *P*', 14, MUT, 'middle')
    o += T(450, 400, f'最大值 {frac(IL_CD_14["C"], 100)} *P*（拉），*P* 在 C；就是「簡支梁在 *x* = 24 的彎矩影響線」÷ 17', 15, INK, 'middle')
    return svg(W, H, o, 'CD 桿影響線')


def fig4_8():
    """選方法的流程。"""
    W, H = 900, 330
    o = ''
    o += R(20, 125, 190, 80, KEY2, KEY, 1.8, 10)
    o += T(115, 156, '先數、先求反力', 16, KEY, 'middle', 'bold') + T(115, 182, '（三鉸 → 中間鉸）', 15, INK, 'middle')
    rows = [(20, '要全部桿力', '節點法：從只剩 2 個未知的節點走；走不動就帶變數', TEN, TEN2),
            (100, '只要中間某 1～3 根', '截面法：切 3 根，對另兩根交點取矩；兩根平行 → Σ*F*', WARN, WARN2),
            (180, '切哪裡都 ≥ 4 根（K 型）', '先切一處 3 根求出一根，再用節點法走過去', AC, AC2),
            (260, '載重會移動', '每個位置用「沒有 *P* 的那一半」取矩，畫成影響線', COMP, COMP2)]
    for y, a, b, c, c2 in rows:
        o += A(212, 165, 268, y + 26, INK, 1.8, 10)
        o += R(272, y, 610, 54, c2, c, 1.6, 10)
        o += T(290, y + 33, a, 15, c, 'start', 'bold')
        o += T(480, y + 33, b, 15, INK, 'start')
    return svg(W, H, o, '桁架解法選擇')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4, 'fig4_5': fig4_5,
       'fig4_6': fig4_6, 'fig4_7': fig4_7, 'fig4_8': fig4_8}
