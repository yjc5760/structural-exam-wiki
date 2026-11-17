# -*- coding: utf-8 -*-
"""第 9 章：非外力成因（種子 S5、S6）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import (N242, B242, U242C, U242E, R242C, R242E, dCD242, dDE242, dT242, CHK242, EA242,
                   N15, B15, U15, R15u, c0, c1, err15, sup15, T15,
                   ROT23, DE23_RIGID, DE23_P, P23, EI23)
from figs_ch3 import truss, labels, sgn
from fractions import Fraction as Fr
import math


def frac(v, den=100):
    q = Fr(v).limit_denominator(den)
    s = f'{abs(q.numerator)}/{q.denominator}' if q.denominator != 1 else f'{abs(q.numerator)}'
    return ('−' if q < 0 else '+') + s


def fig9_1():
    """種子 S6：靜定結構會讓開（SA-2023-1 的梁繞 B 轉）。"""
    W, H = 900, 380
    o = T(W / 2, 30, '種子 S6：靜定結構沒有多餘的束制 → 沉陷、溫差、誤差只讓它「讓開」，不產生內力', 16, KEY, 'middle', 'bold')
    f = Frame(110, 150, 56)
    A_, B_, C_, D_, E_ = (f(x, 0) for x in (0, 2, 6, 10, 12))
    F_ = f(6, 4 * 0.45)   # 柱高 4 m（圖上縮短）
    o += member(A_, E_, STEEL, 4) + member(C_, F_, STEEL, 4)
    o += roller(*B_) + pin(*D_)
    ph = 0.07                                  # 放大後的轉角（真實 0.000375 rad）

    def rot(x, y):
        dx, dy = x - 2, y
        return f(2 + dx * math.cos(ph) + dy * math.sin(ph), -dx * math.sin(ph) + dy * math.cos(ph))
    o += P([rot(0, 0), rot(12, 0)], AC, 3, dash='8 5') + P([rot(6, 0), rot(6, 4 * 0.45)], AC, 3, dash='8 5')
    fy = lambda x: rot(x, 0)[1]
    for p, t in ((A_, 'A'), (B_, 'B'), (C_, 'C'), (D_, 'D'), (E_, 'E')):
        o += T(p[0], p[1] - 14, t, 15, KEY, 'middle', 'bold')
    o += T(F_[0] + 10, F_[1] + 4, 'F', 15, KEY, 'start', 'bold')
    o += A(D_[0] + 30, D_[1], D_[0] + 30, fy(10), COMP, 2, 9) + T(D_[0] + 38, (D_[1] + fy(10)) / 2 + 5, '3 mm', 15, COMP, 'start', 'bold')
    o += A(E_[0] + 24, E_[1], E_[0] + 24, fy(12), AC, 2, 9) + T(E_[0] + 32, (E_[1] + fy(12)) / 2 + 12, f'{DE23_RIGID * 1000:g} mm', 15, AC, 'start', 'bold')
    o += T(450, 250, '（虛線：放大後的剛體轉動，繞 B 轉 0.003/8 = 0.000375 rad；梁、柱都沒有彎）', 14, MUT, 'middle')
    o += R(40, 276, 820, 92, KEY2, KEY, 1.3, 8)
    o += T(450, 302, '為什麼沒有內力？外力為 0 → 只用平衡（S1）就能算出全部反力與內力 → 全部是 0。', 15, INK, 'middle')
    o += T(450, 328, '沒有內力就沒有彈性變形，所以 Σ*nNL*/*EA*、∫*mM*/*EI* d*x* 這一項是 0；只剩幾何。', 15, INK, 'middle')
    o += T(450, 354, '靜不定結構才會「打架」產生內力（下一個單元 U2）。', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '靜定結構讓開')


def fig9_2():
    """SA-2024-2：兩個單位力、兩條方程。"""
    W, H = 900, 470
    o = T(W / 2, 30, 'SA-2024-2：只有 CD、DE 會變長短，F 下沉 12 mm', 16, INK, 'middle', 'bold')
    f = Frame(60, 200, 27)
    o += truss(f, N242, B242)
    P_ = {k: f(*v) for k, v in N242.items()}
    for b in ('CD', 'DE'):
        o += L(*P_[b[0]], *P_[b[1]], WARN, 7)
    for k_, (x, y) in P_.items():
        o += C(x, y, 4.5, '#fff', INK, 1.4)
    o += roller(*P_['B']) + pin(*P_['F'])
    o += labels(f, N242, {k: (0, 22 if v[1] == 0 else -12) for k, v in N242.items() if k in 'ABCDEFGHJKLN'}, 15)
    o += T((P_['C'][0] + P_['D'][0]) / 2, P_['C'][1] + 40, 'δ（誤差）', 15, WARN, 'middle', 'bold')
    o += T((P_['D'][0] + P_['E'][0]) / 2, P_['D'][1] + 40, 'αΔ*T* *L*', 15, WARN, 'middle', 'bold')
    o += A(P_['F'][0] + 26, P_['F'][1] + 26, P_['F'][0] + 26, P_['F'][1] + 62, COMP, 2.2, 9) + T(P_['F'][0] + 32, P_['F'][1] + 56, '12 mm', 15, COMP, 'start', 'bold')
    o += R(735, 60, 155, 180, KEY2, KEY, 1.3, 8)
    o += T(812, 86, '單位力 → *n*', 15, KEY, 'middle', 'bold')
    o += T(748, 116, f'C 1↓：*n*_{{CD}} = {abs(U242C["CD"]):g}', 15, INK, 'start')
    o += T(748, 142, f'　　 *n*_{{DE}} = 1/3', 15, INK, 'start')
    o += T(748, 168, f'　　 *R̄*_{{F}} = {R242C[("F", 1)]:g}', 15, INK, 'start')
    o += T(748, 196, f'E 1↓：*n* = 1/3、1', 15, INK, 'start')
    o += T(748, 222, f'　　 *R̄*_{{F}} = {R242E[("F", 1)]:g}', 15, INK, 'start')
    o += R(40, 300, 820, 160, '#fff', KEY, 1.5, 8)
    o += T(450, 326, '1·Δ + *R̄*_{F}·(−12) = *n*_{CD}·δ + *n*_{DE}·Δ*L*_{DE}　（向下為正、反力向上為正）', 15, INK, 'middle')
    o += T(450, 356, 'C：4.8 − 0.25×12 = δ + Δ*L*_{DE}/3 = 1.8　　E：6.4 − 0.75×12 = δ/3 + Δ*L*_{DE} = −2.6', 15, INK, 'middle')
    o += T(450, 388, (f'⇒ δ = {dCD242:+.1f} mm（過長）、Δ*L*_{{DE}} = {dDE242:.1f} mm ⇒ Δ*T* = {dDE242:.1f}/(1.5×10^{{-5}}×4000) = {dT242:.0f} ℃（降溫）').replace('-3.6', '−3.6').replace('= -60', '= −60'), 15, KEY, 'middle', 'bold')
    o += T(450, 418, f'*E*、*A*（*EA* = {EA242:g} kN）沒用到：沒有外力 → 內力全 0 → Σ*nNL*/*EA* = 0', 15, COMP, 'middle', 'bold')
    o += T(450, 446, f'反向檢查（幾何相容直接算）：C、E 下沉 {CHK242[0]:.1f}、{CHK242[1]:.1f} mm ✔'.replace(' ✔', ''), 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2024-2')


def fig9_3():
    """SA-2015-1：D 點位移是 T 的一次函數，令它為 0。"""
    W, H = 900, 430
    o = T(W / 2, 30, 'SA-2015-1：三個原因疊加，D 點位移是 *T* 的一次函數', 16, INK, 'middle', 'bold')
    f = Frame(80, 220, 30)
    o += truss(f, N15, B15)
    P_ = {k: f(*v) for k, v in N15.items()}
    o += L(*P_['B'], *P_['D'], WARN, 7)
    for k_, (x, y) in P_.items():
        o += C(x, y, 5, '#fff', INK, 1.4)
    o += pin(*P_['A']) + roller(*P_['C'])
    o += labels(f, N15, dict(A=(-14, -10), C=(0, 46), D=(14, -10), B=(0, -14)), 15)
    o += force(P_['D'], 90, 40, COMP, 2.4, '50', 15, (12, 6), 'start')
    o += A(P_['B'][0] - 4, P_['B'][1], P_['B'][0] - 50, P_['B'][1], KEY, 2.4, 10) + T(P_['B'][0] - 54, P_['B'][1] + 5, '*T*', 16, KEY, 'end', 'bold')
    o += T((P_['B'][0] + P_['D'][0]) / 2 + 14, (P_['B'][1] + P_['D'][1]) / 2 - 6, '短 5 mm', 14, WARN, 'start', 'bold')
    o += T(P_['C'][0] + 24, P_['C'][1] + 30, '沉 4 mm', 14, COMP, 'start', 'bold')
    p = Plot(440, 80, 400, 220, 0, 250, -10, 15)
    lin = lambda T_: (c0 + c1 * T_ + err15 - sup15) * 1000
    o += p.axes([0, 50, 100, 150, 200, 250], [-10, -5, 0, 5, 10, 15], '*T*', 'Δ_{D}（mm）', xfmt=lambda t: f'{t:g}', yfmt=lambda t: f'{t:g}', size=14)
    o += p.curve(lin, 0, 250, KEY, 2.6)
    o += p.hline(0, c=INK, w=1.2, dash=None)
    o += p.dot(T15, 0, COMP, 6) + T(p.X(T15) - 10, p.Y(0) + 24, f'*T* = {T15:.2f}', 15, COMP, 'end', 'bold')
    o += T(p.X(12), p.Y(lin(0)) + 4, f'*T* = 0：{lin(0):.2f} mm（向下）', 15, KEY, 'start', 'bold')
    o += R(40, 320, 820, 100, KEY2, KEY, 1.3, 8)
    o += T(450, 346, f'1·Δ_{{D}} + *R̄*_{{C}}(−0.004) = Σ*nNL*/*EA* + *n*_{{BD}}(−0.005)；*R̄*_{{C}} = 2、*n*_{{BD}} = 5/3', 15, INK, 'middle')
    o += T(450, 374, f'Σ*nNL*/*EA* = ({c0 * 2e5:.0f} − 179*T*/12)/(2×10^{{5}})；令 Δ_{{D}} = 0：', 15, INK, 'middle')
    o += T(450, 402, f'*T* = 31600/179 ≈ {T15:.2f} kN', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2015-1')


def fig9_4():
    """SA-2023-1：剛體位移向下、P 的彈性位移向上，相消。"""
    W, H = 900, 400
    o = T(W / 2, 30, 'SA-2023-1：E 點＝D 沉陷的剛體位移（向下）＋ *P* 造成的彈性位移（向上）', 16, INK, 'middle', 'bold')
    p = Plot(110, 80, 560, 210, 0, 50, -7, 5)
    tot = lambda P_: (DE23_RIGID + DE23_P * P_) * 1000
    o += p.axes([0, 10, 20, 30, 40, 50], [-6, -4, -2, 0, 2, 4], '*P*', 'Δ_{E}（mm，向下為正）', xfmt=lambda t: f'{t:g}', yfmt=lambda t: f'{t:g}', size=14)
    o += p.hline(0, c=INK, w=1.2, dash=None)
    o += p.curve(lambda P_: DE23_RIGID * 1000, 0, 50, COMP, 2, '6 4')
    o += p.curve(lambda P_: DE23_P * P_ * 1000, 0, 50, AC, 2, '3 3')
    o += p.curve(tot, 0, 50, KEY, 2.8)
    o += p.dot(P23, 0, KEY, 6) + T(p.X(P23) + 8, p.Y(0) - 12, f'*P* = {P23:.3f}', 15, KEY, 'start', 'bold')
    o += T(p.X(30), p.Y(3.75) - 10, '剛體 3.75（與 *P* 無關）', 15, COMP, 'start', 'bold')
    o += T(p.X(32), p.Y(-4.27) + 26, '彈性 −8*P*/3*EI*', 15, AC, 'start', 'bold')
    o += R(690, 70, 200, 220, KEY2, KEY, 1.3, 8)
    for i, s in enumerate(['*P* 移到 C：', '水平力＋順時針 4*P*', '（柱 CF 高 4 m）', 'E 點 1↓：', '*m* = −0.25(*x*−2)', '（B 到 D 段）', '∫*mM* = −8*P*/3']):
        o += T(704, 98 + i * 28, s, 15, INK, 'start')
    o += R(40, 310, 820, 80, '#fff', KEY, 1.5, 8)
    o += T(450, 338, f'剛體：0.003 × 10/8 = {DE23_RIGID * 1000:g} mm；彈性：8*P*/(3×20000) 向上', 15, INK, 'middle')
    o += T(450, 368, f'令總和 = 0：8*P*/60000 = 0.00375 ⇒ *P* = {P23:.3f} kN', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2023-1')


ALL = {'fig9_1': fig9_1, 'fig9_2': fig9_2, 'fig9_3': fig9_3, 'fig9_4': fig9_4}
