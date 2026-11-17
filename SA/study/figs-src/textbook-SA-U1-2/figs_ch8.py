# -*- coding: utf-8 -*-
"""第 8 章：虛功與單位力法（種子 S5）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import (N17, B17, F17, F17u, DC17, M12, EI12, m12_ye, YE12_UL, TE12_UL,
                   N03_2, DC03_2, DD43_AB, DD43_BD, DD43_SP, DD43, DB43, DC43, RC43)
from figs_ch3 import truss, labels, sgn, legend
import math


def fig8_1():
    """虛功：虛的力系 × 真的變形。"""
    W, H = 900, 400
    o = T(W / 2, 30, '種子 S5：把「虛的、平衡的力」放到「真的變形」上，外功＝內功', 16, KEY, 'middle', 'bold')
    for k, (title, c, c2) in enumerate((('虛力系統（只要平衡）', KEY, KEY2), ('真實系統（只要相容）', AC, AC2))):
        ox = 30 + k * 430
        o += R(ox, 50, 410, 220, c2, c, 1.4, 10)
        o += T(ox + 205, 76, title, 16, c, 'middle', 'bold')
        f = Frame(ox + 50, 190, 38)
        a_, b_ = f(0, 0), f(8, 0)
        o += L(a_[0], a_[1], b_[0], b_[1], INK, 4.5) + pin(*a_) + roller(*b_)
        mid = f(5, 0)
        if k == 0:
            o += A(mid[0], mid[1] - 50, mid[0], mid[1] - 4, KEY, 3, 12) + T(mid[0] + 8, mid[1] - 36, '1', 18, KEY, 'start', 'bold')
            o += T(ox + 205, 244, '內力 *n*、*m*、彈簧力 *f*（由 S1 算）', 15, INK, 'middle')
        else:
            pts = [(a_[0] + (b_[0] - a_[0]) * i / 40, a_[1] + 34 * math.sin(math.pi * i / 40)) for i in range(41)]
            o += P(pts, AC, 2.4, dash='6 4')
            o += A(mid[0] + 30, mid[1] - 6, mid[0] + 30, mid[1] + 30, AC, 2, 9) + T(mid[0] + 38, mid[1] + 24, 'Δ', 17, AC, 'start', 'bold')
            o += T(ox + 205, 244, '變形 Δ*L*、*κ* = *M*/*EI*、彈簧縮 *F*/*k*', 15, INK, 'middle')
    o += R(60, 290, 780, 96, '#fff', KEY, 1.6, 10)
    o += T(450, 320, '1 · Δ ＝ Σ *n* · Δ*L* ＋ ∫ *m* · *κ* d*x* ＋ Σ *f* · δ_{彈簧}', 18, KEY, 'middle', 'bold')
    o += T(450, 356, '＝ Σ *nNL*/*EA* ＋ ∫ *mM*/*EI* d*x* ＋ Σ *fF*/*k*', 18, INK, 'middle', 'bold')
    return svg(W, H, o, '虛功原理')


def fig8_2():
    """SA-2017-1：真實桿力 N 與虛擬桿力 n（C 點 1 kN →）。"""
    W, H = 900, 450
    o = ''
    for k, (Fd, title, scale) in enumerate(((F17, '真實 *N*（kN）', 1), (F17u, '虛擬 *n*（C 點 1 →）', 1))):
        ox = 140 + k * 430
        f = Frame(ox, 360, 36)
        vals = {}
        for b in B17:
            v = Fd[b]
            if abs(v) < 1e-9:
                vals[b] = '0'
            elif k == 1 and abs(abs(v) - 4 / 3) < 1e-6:
                vals[b] = ('+' if v > 0 else '−') + '4/3'
            elif k == 1 and abs(abs(v) - 5 / 3) < 1e-6:
                vals[b] = ('+' if v > 0 else '−') + '5/3'
            else:
                vals[b] = sgn(v)
        voff = dict(AB=(-34, 0), BC=(-34, 0), BD=(0, -18), AD=(20, 18), CD=(30, -6), DE=(32, 6))
        o += truss(f, N17, B17, Fd, vals=vals, voff=voff)
        P_ = {kk: f(*v) for kk, v in N17.items()}
        o += pin(*P_['A']) + pin(*P_['E'])
        o += labels(f, N17, dict(A=(-26, 0), B=(-18, 26), C=(-18, -12), D=(18, -14), E=(26, 0)))
        if k == 0:
            o += force(P_['C'], 180, 50, COMP, 2.6, '12', 15, (-6, -8)) + force(P_['B'], 180, 50, COMP, 2.6, '9', 15, (-6, -8))
        else:
            o += force(P_['C'], 180, 50, KEY, 2.6, '1', 15, (-6, -8))
        o += T(ox + 90, 46, title, 16, KEY if k else INK, 'middle', 'bold')
    o += legend(160, 430)
    return svg(W, H, o, 'SA-2017-1 真實與虛擬')


def fig8_3():
    """SA-2012-1：真實 M 與虛擬 m（e 點 1↓），逐段相乘。"""
    W, H = 900, 470
    o = ''
    p = Plot(110, 50, 680, 150, 0, 16, -200, 200)
    o += T(40, 40, '(a) 真實 *M*（kN-m）', 16, KEY, 'start', 'bold')
    o += p.hline(0, c=INK, w=1.2, dash=None)
    o += p.area(lambda x: max(M12(x), 0), lambda x: 0, 0, 16, TEN2, 0.9) + p.area(lambda x: 0, lambda x: min(M12(x), 0), 0, 16, COMP2, 0.9)
    o += p.curve(lambda x: M12(x + 1e-9), 0, 16, KEY, 2.4)
    o += T(p.X(2), p.Y(160) + 22, '+160（2*EI*）', 15, TEN, 'middle', 'bold') + T(p.X(12), p.Y(-160) - 8, '−160', 15, COMP, 'middle', 'bold')
    q = Plot(110, 250, 680, 130, 0, 16, -6, 10)
    o += T(40, 240, '(b) 虛擬 *m*（e 點 1 kN↓）', 16, AC, 'start', 'bold')
    o += q.hline(0, c=INK, w=1.2, dash=None)
    o += q.area(lambda x: max(m12_ye(x), 0), lambda x: 0, 0, 16, AC2, 0.9) + q.area(lambda x: 0, lambda x: min(m12_ye(x), 0), 0, 16, AC2, 0.9)
    o += q.curve(m12_ye, 0, 16, AC, 2.4)
    o += T(q.X(0) + 6, q.Y(8) - 6, '+8', 15, AC, 'start', 'bold') + T(q.X(12) - 12, q.Y(-4) + 6, '−4', 15, AC, 'end', 'bold')
    for x, t in ((0, 'a'), (4, 'b'), (8, 'c'), (12, 'd'), (16, 'e')):
        o += L(p.X(x), 50, p.X(x), 380, GRID, 1, '4 4') + T(p.X(x), 400, t, 15, MUT, 'middle', 'bold')
    segs = [('a–b', 1920), ('b–c', 1280 / 3), ('c–d', 2560 / 3), ('d–e', 2560 / 3)]
    for i, (n, v) in enumerate(segs):
        o += T(p.X(2 + 4 * i), 426, f'{v:.1f}', 15, KEY, 'middle', 'bold')
    o += T(40, 426, '∫*mM*/*EI*', 15, KEY, 'start', 'bold')
    o += T(450, 458, f'合計 = {YE12_UL:.2f}/*EI* = 12160/3*EI*（向下）——與共軛梁相同', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 單位力法')


def fig8_4():
    """SA-2003-2：剛梁＋三根連桿。"""
    W, H = 900, 400
    o = T(W / 2, 30, 'SA-2003-2：剛梁不變形，只有連桿伸縮會讓 C 動', 16, INK, 'middle', 'bold')
    f = Frame(150, 300, 52)
    A_, B_, C_ = f(0, 3), f(4, 3), f(8, 3)
    D_, E_ = f(0, 0), f(4, 0)
    o += L(A_[0], A_[1] - 5, C_[0], C_[1] - 5, INK, 2) + L(A_[0], A_[1] + 5, C_[0], C_[1] + 5, INK, 2)
    o += L(A_[0], A_[1], D_[0], D_[1], TEN, 6) + L(B_[0], B_[1], E_[0], E_[1], COMP, 8) + L(A_[0], A_[1], E_[0], E_[1], STEEL, 2.4, '7 5')
    o += pin(*D_) + pin(*E_) + C(*A_, 6, '#fff', INK, 1.6) + C(*B_, 6, '#fff', INK, 1.6)
    o += force(C_, 90, 50, COMP, 2.6, '*F*', 16, (12, 6), 'start')
    for p, t, dx, dy in ((A_, 'A', -16, -14), (B_, 'B', 0, -16), (C_, 'C', 16, -14), (D_, 'D', -20, 4), (E_, 'E', 20, 4)):
        o += T(p[0] + dx, p[1] + dy, t, 16, KEY, 'middle', 'bold')
    o += T((A_[0] + D_[0]) / 2 - 12, (A_[1] + D_[1]) / 2, '+*F*', 16, TEN, 'end', 'bold')
    o += T((B_[0] + E_[0]) / 2 + 12, (B_[1] + E_[1]) / 2, '−2*F*', 16, COMP, 'start', 'bold')
    o += T((A_[0] + E_[0]) / 2 + 8, (A_[1] + E_[1]) / 2 + 26, '0', 16, MUT, 'start', 'bold')
    o += dim(A_[0], 330, B_[0], 330, '4λ', MUT, 0, 14) + dim(B_[0], 330, C_[0], 330, '4λ', MUT, 0, 14)
    o += R(600, 70, 290, 270, KEY2, KEY, 1.4, 10)
    rows = ['虛擬：C 點 1↓ ⇒ *n* = *N*/*F*', 'AD：*n* = 1、*N* = *F*、*L* = 3λ', 'BE：*n* = −2、*N* = −2*F*、*L* = 3λ',
            'AE：*n* = *N* = 0', 'Σ*nNL*/*EA* = (3 + 12)*F*λ/*EA*', f'= {DC03_2:g}*F*λ/*EA*（向下）']
    for i, s in enumerate(rows):
        o += T(616, 104 + i * 38, s, 15, KEY if i == 5 else INK, 'start', 'bold' if i == 5 else None)
    return svg(W, H, o, 'SA-2003-2')


def fig8_5():
    """SA-2004-3：D 點位移的三項。"""
    W, H = 900, 360
    o = T(W / 2, 30, 'SA-2004-3：D 點垂直位移＝三項加總（mm，向下為正）', 16, INK, 'middle', 'bold')
    items = [('AB 懸臂彎曲（2*EI*）', DD43_AB * 1000, COMP, COMP2), ('BCD 彎曲（*EI*）', DD43_BD * 1000, AC, AC2),
             ('彈簧 *fF*/*k*', DD43_SP * 1000, WARN, WARN2), ('合計', DD43 * 1000, KEY, KEY2)]
    x0 = 560
    sc = 4.2
    o += L(x0, 60, x0, 300, INK, 1.4)
    for i, (n, v, c, c2) in enumerate(items):
        y = 70 + i * 56
        w = v * sc
        o += R(min(x0, x0 + w), y, abs(w), 36, c2, c, 1.6, 4)
        o += T(60, y + 24, n, 15, c, 'start', 'bold')
        o += T(x0 + w + (8 if w > 0 else -8), y + 24, f'{v:+.2f}'.replace('-', '−'), 15, c, 'start' if w > 0 else 'end', 'bold')
    o += R(40, 300, 820, 50, '#fff', GRID, 1.2, 8)
    o += T(450, 322, f'AB 項為負：虛擬系統把 B 點往上拉（*n* 方向與真實相反）；彈簧：虛擬 5/3 與真實 {RC43:g} t 同為受壓 → 正', 15, INK, 'middle')
    o += T(450, 342, f'（對照題解：*B* 下沉 {DB43 * 1000:g} mm、*C* 下沉 {DC43 * 1000:g} mm 當「支承位移」處理，結果相同 25.84 mm）', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2004-3 三項')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3, 'fig8_4': fig8_4, 'fig8_5': fig8_5}
