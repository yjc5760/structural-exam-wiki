# -*- coding: utf-8 -*-
"""第 7 章：共軛梁（種子 S4 × 種子 S3）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
import numpy as np
from calcs import (M12, EI12, A12, Rc_conj, Vd_up_on_left, TH_E_CONJ, Y_E_CONJ, Y_C_AREA, STD, AREA_N,
                   Rb22, Fs22, Db22, Dc22_rigid, Dc22_el, Dc22, ds22, De22, Mc22,
                   M24, XS24, Y24, YC24, X24_MAX, Y24_MAX, X24_EXACT, Y24_EXACT, EIMIN24, RA24, VC24)
import math


def fig7_1():
    """兩條一模一樣的鏈。"""
    W, H = 900, 320
    o = T(W / 2, 32, '同一組微分方程，換個名字而已', 17, INK, 'middle', 'bold')
    rows = [(70, '真實梁（第 5 章，S3）', ['載重 *w*', '剪力 *V*', '彎矩 *M*'], ['d*V*/d*x* = −*w*', 'd*M*/d*x* = *V*'], WARN, WARN2),
            (190, '變形（第 6 章，S4）', ['曲率 *M*/*EI*', '轉角 *θ*', '位移 *y*'], ['d*θ*/d*x* = *M*/*EI*', 'd*y*/d*x* = *θ*'], AC, AC2)]
    for y, title, boxes, eqs, c, c2 in rows:
        o += T(40, y + 34, title, 15, c, 'start', 'bold')
        for i, b in enumerate(boxes):
            x = 260 + i * 220
            o += R(x, y + 8, 150, 46, c2, c, 1.6, 9) + T(x + 75, y + 37, b, 16, INK, 'middle', 'bold')
            if i < 2:
                o += A(x + 154, y + 31, x + 214, y + 31, c, 2, 10)
                o += T(x + 184, y - 2, eqs[i], 14, c, 'middle')
    o += R(150, 268, 600, 42, KEY2, KEY, 1.5, 9)
    o += T(450, 295, '把 *M*/*EI* 當成「載重」放到一根假想梁上 ⇒ 它的剪力＝*θ*、彎矩＝*y*', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '共軛梁類比')


def _sup(o, x, y, kind):
    if kind == 'fix_l':
        o += fixed_left(x, y, 44)
    elif kind == 'fix_r':
        o += L(x, y - 22, x, y + 22, INK, 3)
        for i in range(6):
            yy = y - 22 + i * 8.8
            o += L(x, yy, x + 8, yy + 7, INK, 1)
    elif kind == 'pin':
        o += pin(x, y, INK, 9)
    elif kind == 'roller':
        o += roller(x, y, INK, 9)
    elif kind == 'hinge':
        o += hinge(x, y, 6)
    return o


def fig7_2():
    """支承的對應：真實梁的位移條件 ↔ 共軛梁的力條件。"""
    W, H = 900, 470
    o = T(W / 2, 30, '支承怎麼換：*y* ↔ *M*^{*}、*θ* ↔ *V*^{*}，條件照抄', 17, INK, 'middle', 'bold')
    rows = [('固定端', 'fix_l', '*y* = 0、*θ* = 0', '自由端', None, '*M*^{*} = 0、*V*^{*} = 0'),
            ('自由端', None, '*y*、*θ* ≠ 0', '固定端', 'fix_r', '*M*^{*}、*V*^{*} ≠ 0'),
            ('端點鉸／滾', 'pin', '*y* = 0、*θ* ≠ 0', '端點鉸／滾', 'pin', '*M*^{*} = 0、*V*^{*} ≠ 0'),
            ('中間支承', 'roller', '*y* = 0、*θ* 連續', '內鉸', 'hinge', '*M*^{*} = 0、*V*^{*} 連續'),
            ('內鉸', 'hinge', '*y* 連續、*θ* 可跳', '中間支承', 'roller', '*M*^{*} 連續、*V*^{*} 可跳')]
    o += T(150, 70, '真實梁', 16, AC, 'middle', 'bold') + T(650, 70, '共軛梁', 16, KEY, 'middle', 'bold')
    for i, (a, ka, ca, b, kb, cb) in enumerate(rows):
        y = 110 + i * 70
        o += R(30, y - 26, 840, 60, '#fff', GRID, 1, 8)
        o += L(60, y, 200, y, INK, 4)
        if ka:
            o = _sup(o, 60 if ka == 'fix_l' else 130, y, ka)
        o += T(220, y - 2, a, 15, INK, 'start', 'bold') + T(220, y + 22, ca, 14, AC, 'start')
        o += A(420, y, 480, y, KEY, 2, 10)
        o += L(520, y, 660, y, INK, 4)
        if kb:
            o = _sup(o, 660 if kb == 'fix_r' else 590, y, kb)
        o += T(680, y - 2, b, 15, INK, 'start', 'bold') + T(680, y + 22, cb, 14, KEY, 'start')
    return svg(W, H, o, '共軛梁支承對應')


def fig7_3():
    """標準撓度：懸臂集中力、簡支均布，從共軛梁推出係數。"""
    W, H = 900, 470
    o = ''
    # (a) 懸臂
    o += T(220, 30, '(a) 懸臂＋端點 *P* → 共軛梁', 16, INK, 'middle', 'bold')
    x0, x1, yb = 60, 380, 150
    o += L(x0, yb, x1, yb, INK, 4) + fixed_wall(x0, yb, 1) if False else ''
    o += L(x0, yb, x1, yb, INK, 4)
    o += L(x0, yb - 26, x0, yb + 26, INK, 3)
    for i in range(6):
        yy = yb - 26 + i * 10.4
        o += L(x0, yy, x0 - 8, yy + 7, INK, 1)
    o += force((x1, yb), 90, 40, COMP, 2.6, '*P*', 16, (12, 6), 'start')
    o += T(x0 - 14, yb + 46, '真實：左固定、右自由', 14, MUT, 'start')
    yc = 300
    o += L(x0, yc, x1, yc, INK, 4)
    o += L(x1, yc - 26, x1, yc + 26, INK, 3)
    for i in range(6):
        yy = yc - 26 + i * 10.4
        o += L(x1, yy, x1 + 8, yy + 7, INK, 1)
    o += P([(x0, yc), (x0, yc + 70), (x1, yc)], COMP, 1.6, fill=COMP2, close=True)
    o += T(x0 + 6, yc + 90, '*PL*/*EI*', 15, COMP, 'start', 'bold')
    o += T(x1 - 6, yc - 40, '共軛：左自由、右固定', 14, MUT, 'end')
    gx = x0 + (x1 - x0) / 3
    o += L(gx, yc + 4, gx, yc + 40, KEY, 1.4, '4 3') + T(gx + 6, yc + 52, '形心', 14, KEY, 'start')
    o += dim(gx, yc - 20, x1, yc - 20, '2*L*/3', KEY, 0, 14)
    o += R(40, 400, 360, 60, KEY2, KEY, 1.3, 8)
    o += T(220, 424, '*θ* = *V*^{*} = (1/2)(*PL*/*EI*)*L* = *PL*^{2}/2*EI*', 15, INK, 'middle')
    o += T(220, 450, '*δ* = *M*^{*} = (*PL*^{2}/2*EI*)(2*L*/3) = *PL*^{3}/3*EI*', 15, KEY, 'middle', 'bold')
    # (b) 簡支均布
    o += T(670, 30, '(b) 簡支＋均布 *w* → 共軛梁', 16, INK, 'middle', 'bold')
    a0, a1 = 480, 860
    o += L(a0, yb, a1, yb, INK, 4) + pin(a0, yb, INK, 9) + roller(a1, yb, INK, 9)
    o += udl(a0, a1, yb, COMP, 24, 12, '*w*', 15)
    o += L(a0, yc, a1, yc, INK, 4) + pin(a0, yc, INK, 9) + roller(a1, yc, INK, 9)
    pts = [(a0 + (a1 - a0) * i / 40, yc - 70 * 4 * (i / 40) * (1 - i / 40)) for i in range(41)]
    o += P(pts + [(a1, yc)], AC, 1.6, fill=AC2, close=True)
    o += T((a0 + a1) / 2, yc - 80, '*wL*^{2}/8*EI*（拋物線）', 15, AC, 'middle', 'bold')
    o += R(470, 400, 410, 60, KEY2, KEY, 1.3, 8)
    o += T(675, 424, '半邊面積 (2/3)(*L*/2)(*wL*^{2}/8*EI*)，形心距中點 3*L*/16', 15, INK, 'middle')
    o += T(675, 450, '*δ*_{mid} = *A*(*L*/2 − 3*L*/16) = 5*wL*^{4}/384*EI*', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '標準撓度推導')


def fig7_4():
    """SA-2012-1 共軛梁：a' 自由、c' 內支承、d' 內鉸、e' 固定。"""
    W, H = 900, 455
    o = T(W / 2, 30, "SA-2012-1 的共軛梁：載重＝*M*/*EI*（向上為正），支承照圖 7-2 換", 16, INK, 'middle', 'bold')
    f = Frame(110, 230, 42)
    a, b, c, d, e = (f(x, 0) for x in (0, 4, 8, 12, 16))
    o += member(a, e)
    o += roller(*c)
    o += L(e[0], e[1] - 26, e[0], e[1] + 26, INK, 3)
    for i in range(6):
        yy = e[1] - 26 + i * 10.4
        o += L(e[0], yy, e[0] + 8, yy + 7, INK, 1)
    k = lambda x: M12(x + 1e-9) / EI12(x)
    sc = 0.5
    pts = [f(x, 0) for x in (0, 4, 8, 12, 16)]
    top = [(f(x, 0)[0], f(x, 0)[1] - k(x) * sc) for x in (0, 4, 8, 12, 15.999)]
    o += P([pts[0], top[0], top[1], top[2]], TEN, 1.4, fill=TEN2, close=True)
    o += P([pts[2], top[3], top[4], pts[4]], COMP, 1.4, fill=COMP2, close=True)
    for xx, Fv, lab in ((A12['x1'], A12['F1'], '320'), (A12['x2'], A12['F2'], '160'), (A12['x3'], A12['F3'], '320'), (A12['x4'], A12['F4'], '320')):
        p = f(xx, 0)
        if Fv > 0:
            o += A(p[0], p[1] + 48, p[0], p[1] + 6, TEN, 2.4, 10) + T(p[0] + 6, p[1] + 58, lab + '↑', 15, TEN, 'middle', 'bold')
        else:
            o += A(p[0], p[1] - 110, p[0], p[1] - 6, COMP, 2.4, 10) + T(p[0], p[1] - 116, lab + '↓', 15, COMP, 'middle', 'bold')
    o += hinge(*d)
    for p, t in ((a, "a′ 自由"), (c, "c′ 內支承"), (d, "d′ 內鉸"), (e, "e′ 固定")):
        o += T(p[0], p[1] + 98, t, 15, KEY, 'middle', 'bold')
    o += R(40, 345, 820, 100, KEY2, KEY, 1.3, 8)
    o += T(450, 371, f"左段 a′–d′ 對 d′ 取矩（d′ 是鉸）：*R*_{{c′}} = −{abs(Rc_conj):g}；左段 Σ*F*：右段在 d′ 受 {Vd_up_on_left:g} 向下", 15, INK, 'middle')
    o += T(450, 399, f"右段 d′–e′：*V*^{{*}}_{{e}} = −{Vd_up_on_left:g} − 320 = −{abs(TH_E_CONJ):g} ⇒ *θ*_{{e}} = {abs(TH_E_CONJ):g}/*EI*（順時針）", 15, KEY, 'middle', 'bold')
    o += T(450, 427, f"*M*^{{*}}_{{e}} = −{Vd_up_on_left:g}×4 − 320×(8/3) = −12160/3 ⇒ *y*_{{e}} = {abs(Y_E_CONJ):.0f}/*EI*（向下）", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 共軛梁')


def fig7_5():
    """SA-2022-1：c 點位移＝剛體 8 ＋ 彈性 4；彈簧壓 4 → e 沉陷 8。"""
    W, H = 900, 430
    o = T(W / 2, 30, 'SA-2022-1：位移一塊一塊加起來（mm）', 17, INK, 'middle', 'bold')
    f = Frame(140, 110, 42)
    d_, c_, b_, a_ = f(0, 0), f(5, 0), f(10, 0), f(15, 0)
    o += member(d_, a_) + hinge(*b_) + roller(*d_)
    o += L(a_[0], a_[1] - 26, a_[0], a_[1] + 26, INK, 3)
    for i in range(6):
        yy = a_[1] - 26 + i * 10.4
        o += L(a_[0], yy, a_[0] + 8, yy + 7, INK, 1)
    o += spring_v(c_[0], c_[1] + 4, c_[1] + 70)
    o += force(c_, 90, 40, COMP, 2.4, '72', 15, (12, 4), 'start') + force(b_, 90, 40, COMP, 2.4, '72', 15, (12, 4), 'start')
    for p, t in ((d_, 'd'), (c_, 'c'), (b_, 'b'), (a_, 'a')):
        o += T(p[0] - 14, p[1] - 12, t, 15, MUT, 'middle', 'bold')
    o += T(c_[0] + 22, c_[1] + 52, '*k*', 16, INK, 'start', 'bold', True) + T(c_[0] + 10, c_[1] + 92, 'e', 15, MUT, 'start', 'bold')
    # 變形（放大）
    s = 4.5
    y0 = 225
    xs = [f(x, 0)[0] for x in (0, 5, 10, 15)]
    o += L(xs[0], y0, xs[3], y0, MUT, 1.2, '5 4')
    rig = [(xs[0], y0), (xs[2], y0 + Db22 * 1000 * s)]
    o += P(rig, KEY, 1.6, dash='6 4')
    def ydb(x):        # d(0)–b(10)：剛體直線＋中點集中 24 kN 的簡支彈性撓度（mm）
        xx = x if x <= 5 else 10 - x
        el = 24 * xx * (3 * 100 - 4 * xx * xx) / (48 * 250000) * 1000
        return Db22 * 1000 * x / 10 + el

    def yba(x):        # b(10)–a(15)：懸臂，自由端 b 受 96 kN
        sx = 15 - x
        return 96 * sx * sx * (3 * 5 - sx) / (6 * 250000) * 1000
    curve = [(f(x, 0)[0], y0 + ydb(x) * s) for x in np.linspace(0, 10, 41)] + [(f(x, 0)[0], y0 + yba(x) * s) for x in np.linspace(10, 15, 21)]
    o += P(curve, AC, 2.6)
    o += A(xs[1] + 12, y0, xs[1] + 12, y0 + Dc22_rigid * 1000 * s, KEY, 1.6, 8, both=True)
    o += T(xs[1] + 18, y0 + Dc22_rigid * 1000 * s / 2 + 5, f'剛體 {Dc22_rigid * 1000:g}', 14, KEY, 'start', 'bold')
    o += A(xs[1] - 12, y0 + Dc22_rigid * 1000 * s, xs[1] - 12, y0 + Dc22 * 1000 * s, AC, 1.6, 8, both=True)
    o += T(xs[1] - 18, y0 + Dc22 * 1000 * s + 14, f'彈性 {Dc22_el * 1000:g}', 14, AC, 'end', 'bold')
    o += T(xs[2] + 14, y0 + Db22 * 1000 * s - 4, f'b：{Db22 * 1000:g}（懸臂 *PL*^{{3}}/3*EI*）', 14, INK, 'start', 'bold')
    o += R(40, 340, 820, 80, KEY2, KEY, 1.3, 8)
    o += T(450, 366, f'b–a 懸臂：*R*_{{b}} = 480/5 = {Rb22:g} kN → Δ_{{b}} = {Rb22:g}×5³/(3×250000) = {Db22 * 1000:g}；彈簧 *F* = {Fs22:g} kN（受壓）', 15, INK, 'middle')
    o += T(450, 394, f'Δ_{{c}} = {Dc22_rigid * 1000:g} + {Dc22_el * 1000:g} = {Dc22 * 1000:g}；彈簧縮 {Fs22:g}/6000 = {ds22 * 1000:g} ⇒ e 沉陷 = {Dc22 * 1000:g} − {ds22 * 1000:g} = {De22 * 1000:g} mm', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2022-1 位移疊加')


def fig7_6():
    """SA-2024-1：AC 段＝剛體轉動（C 被懸臂拉下）＋共軛簡支梁的彈性位移。"""
    W, H = 900, 400
    o = T(W / 2, 30, 'SA-2024-1：A–C 段的位移＝剛體直線 ＋ 自己的彎曲（以 1/*EI* 計，向下為正）', 16, INK, 'middle', 'bold')
    n8 = int(len(XS24) * 8 / 12)
    xs, ys = XS24[:n8 + 1], -Y24[:n8 + 1]
    rig = lambda x: -YC24 * x / 8
    p = Plot(110, 70, 620, 230, 0, 8, -60, 700)
    o += p.axes([0, 2, 4, 6, 8], [0, 200, 400, 600], '*x*', '', xfmt=lambda t: f'{t:g}', yfmt=lambda t: f'{t:g}', size=14)
    o += p.curve(rig, 0, 8, KEY, 2, '6 4')
    o += P([p.pt(x, y - rig(x)) for x, y in zip(xs[::40], ys[::40])], TEN, 2, dash='3 3')
    o += P([p.pt(x, y) for x, y in zip(xs[::40], ys[::40])], AC, 3)
    o += p.dot(X24_MAX, -Y24_MAX, COMP, 6)
    o += T(p.X(X24_MAX), p.Y(-Y24_MAX) - 14, f'{abs(Y24_MAX):.1f}（*x* = {X24_MAX:.3f}）', 15, COMP, 'middle', 'bold')
    o += T(p.X(8) - 6, p.Y(-YC24) + 22, f'C：1600/3 = {abs(YC24):.1f}', 15, KEY, 'end', 'bold')
    o += T(p.X(1.2), p.Y(80) - 6, '剛體（虛線）', 15, KEY, 'start', 'bold')
    o += T(p.X(3.2), p.Y(150) + 26, '彈性（點線）', 15, TEN, 'start', 'bold')
    o += R(745, 70, 145, 230, KEY2, KEY, 1.3, 8)
    for i, s in enumerate(['*R*_{A} = 75', 'C 鉸力 25', 'Δ_{C} = 25·4³/3', '　 = 1600/3', 'θ = 0 於', f'*x* = 8 − 4/√3', f'= {X24_EXACT:.3f}']):
        o += T(760, 100 + i * 28, s, 15, INK, 'start')
    o += R(40, 320, 820, 70, '#fff', KEY, 1.5, 8)
    o += T(450, 346, f'*EI* *y*_{{max}} = 1600/3 + 1600/(9√3) = {Y24_EXACT:.2f} kN-m³ ≤ *EI* × 0.04 m', 15, INK, 'middle')
    o += T(450, 374, f'⇒ *EI*_{{min}} = {Y24_EXACT:.2f}/0.04 = {EIMIN24:.0f} kN-m²', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2024-1 最小 EI')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4, 'fig7_5': fig7_5, 'fig7_6': fig7_6}
