# -*- coding: utf-8 -*-
"""第 5 章：兩端固定梁以兩個多餘力的最小功法推 Pab²/L²；均布＝集中力的疊加 → wL²/12；三張標準彎矩圖；SA-2017-2 內鉸通式曲線。"""
from sa_draw import *  # noqa
import math
import calcs

C5 = calcs.C5
ENE = PUR


def fig5_1():
    W, H = 900, 520
    o = ''
    x0, Lpx = 150, 460
    a_frac = 0.38
    # (a) 原結構
    yb = 70
    o += T(60, yb + 6, '(a)', 16, INK, 'middle', 'bold')
    o += wall(x0, yb, 44, 'left') + wall(x0 + Lpx, yb, 44, 'right') + L(x0, yb, x0 + Lpx, yb, INK, 4)
    xp = x0 + a_frac * Lpx
    o += A(xp, yb - 48, xp, yb - 4, LOAD, 2.4, 10) + T(xp + 8, yb - 28, '*P*', 16, LOAD, 'start', 'bold')
    o += dim(x0, yb + 26, xp, yb + 26, '', MUT) + dim(xp, yb + 26, x0 + Lpx, yb + 26, '', MUT)
    o += T((x0 + xp) / 2, yb + 50, '*a*', 16, MUT, 'middle') + T((xp + x0 + Lpx) / 2, yb + 50, '*b*', 16, MUT, 'middle')
    o += T(x0 - 10, yb - 30, 'A', 15, INK, 'end', 'bold') + T(x0 + Lpx + 12, yb - 30, 'C', 15, INK, 'start', 'bold')
    o += T(x0 + Lpx + 40, yb + 6, '兩端固定：*n* = 2', 15, PUR, 'start', 'bold')
    # (b) 基本結構：懸臂＋R＋MC
    yb = 190
    o += T(60, yb + 6, '(b)', 16, INK, 'middle', 'bold')
    o += wall(x0, yb, 44, 'left') + L(x0, yb, x0 + Lpx, yb, INK, 4)
    o += A(xp, yb - 48, xp, yb - 4, LOAD, 2.4, 10) + T(xp + 8, yb - 28, '*P*', 16, LOAD, 'start', 'bold')
    o += A(x0 + Lpx, yb + 46, x0 + Lpx, yb + 4, FOR, 2.4, 10) + T(x0 + Lpx - 8, yb + 46, '*R*', 16, FOR, 'end', 'bold')
    o += moment(x0 + Lpx, yb, 24, cw=False, c=FOR, start=110, span=220) + T(x0 + Lpx + 30, yb - 24, '*M*_{C}', 16, FOR, 'start', 'bold')
    o += A(x0 + Lpx - 10, yb + 62, x0 + Lpx - 90, yb + 62, MUT, 1.3, 8) + T(x0 + Lpx - 96, yb + 68, '*x*', 15, MUT, 'end')
    # (c) m1、m2
    pl1 = Plot(x0, 290, Lpx, 70, -1, 0, -0.1, 1.1)
    o += bmd(pl1, lambda u: -u, -1, 0, FOR, TENM) + T(x0 - 14, pl1.Y(0) + 5, '*m*_{1} = *x*', 16, FOR, 'end', 'bold')
    o += T(pl1.X(-1) + 6, pl1.Y(1) - 6, '*L*', 15, FOR, 'start', 'bold')
    pl2 = Plot(x0, 380, Lpx, 46, -1, 0, -0.1, 1.2)
    o += bmd(pl2, lambda u: 1.0, -1, 0, FOR, TENM) + T(x0 - 14, pl2.Y(0) + 5, '*m*_{2} = 1', 16, FOR, 'end', 'bold')
    o += T(x0 + Lpx + 16, pl1.Y(0.3), '*f*_{11} = ∫*x*^{2} = *L*^{3}/3', 15, INK, 'start')
    o += T(x0 + Lpx + 16, pl1.Y(0.3) + 24, '*f*_{12} = ∫*x* = *L*^{2}/2', 15, INK, 'start')
    o += T(x0 + Lpx + 16, pl2.Y(0.5), '*f*_{22} = ∫1 = *L*', 15, INK, 'start')
    o += R(60, 446, 780, 66, KEY2, PUR, 1.4, 10)
    o += T(450, 472, '∂*U*/∂*R* = 0、∂*U*/∂*M*_{C} = 0　⇒　兩條聯立方程', 16, PUR, 'middle', 'bold')
    o += T(450, 500, '*M*_{C} = −*Pa*^{2}*b*/*L*^{2}（C 端）　*M*_{A} = −*Pab*^{2}/*L*^{2}（A 端）', 17, PUR, 'middle', 'bold')
    return svg(W, H, o, '兩個多餘力推固端彎矩')


def fig5_2():
    W, H = 900, 470
    o = ''
    x0, Lpx = 150, 560
    yb = 80
    o += wall(x0, yb, 44, 'left') + wall(x0 + Lpx, yb, 44, 'right') + L(x0, yb, x0 + Lpx, yb, INK, 4)
    n = 18
    ai = 6
    for i in range(n):
        xx = x0 + Lpx * (i + 0.5) / n
        c = KEY if i == ai else LOAD
        o += A(xx, yb - 36, xx, yb - 3, c, 2.2 if i == ai else 1.3, 8 if i == ai else 6)
    xa = x0 + Lpx * (ai + 0.5) / n
    o += T(xa, yb - 44, '*dP* = *w*·*da*', 15, KEY, 'middle', 'bold')
    o += dim(x0, yb + 26, xa, yb + 26, '', MUT) + T((x0 + xa) / 2, yb + 48, '*a*', 16, MUT, 'middle')
    o += T(x0 - 10, yb - 30, 'A', 15, INK, 'end', 'bold')
    pl = Plot(x0, 186, Lpx, 196, 0, 1, 0, 0.16)
    g = lambda a: a * (1 - a) ** 2
    o += pl.axes([0, 1 / 3, 0.5, 1], [0, 0.05, 0.1, 0.15], '*a*/*L*', '', size=14,
                 xfmt=lambda t: {0: '0', 1 / 3: '⅓', 0.5: '½', 1: '1'}[t], yfmt=lambda t: f(t))
    o += pl.area(g, lambda a: 0, 0, 1, KEY2, 0.9)
    o += pl.curve(g, 0, 1, PUR, 3)
    o += T(pl.X(0.02), pl.Y(0.16) - 24, '每一顆 *dP* 給 A 端的固端彎矩：*dP*·*ab*^{2}/*L*^{2}（÷ *wL*^{2} 後）', 15, PUR, 'start', 'bold')
    o += pl.dot(1 / 3, g(1 / 3), PUR) + T(pl.X(1 / 3) + 34, pl.Y(g(1 / 3)) + 34, '最大在 *a* = *L*/3', 15, PUR, 'start')
    o += T(pl.X(0.55), pl.Y(0.04), '面積 = 1/12', 20, PUR, 'middle', 'bold')
    o += R(110, 418, 680, 40, KEY2, PUR, 1.4, 8)
    o += T(450, 444, '*M*_{A} = ∫_{0}^{*L*} *w*·*a*(*L* − *a*)^{2}/*L*^{2} *da* = *wL*^{2}/12　（S5：均布＝一排集中力）', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '均布由集中力疊加')


def _ff_row(x0, y, Lpx, fn, lo, hi, ticks, title, load):
    o = T(x0 + Lpx / 2, y - 6, title, 16, INK, 'middle', 'bold')
    yb = y + 32
    o += wall(x0, yb, 30, 'left') + wall(x0 + Lpx, yb, 30, 'right') + L(x0, yb, x0 + Lpx, yb, INK, 3.4)
    if load == 'mid':
        o += A(x0 + Lpx / 2, yb - 30, x0 + Lpx / 2, yb - 3, LOAD, 2.2, 9)
    elif load == 'udl':
        o += udl(x0 + 2, x0 + Lpx - 2, yb - 3, 16, 7, LOAD)
    else:
        o += A(x0 + Lpx * 0.3, yb - 30, x0 + Lpx * 0.3, yb - 3, LOAD, 2.2, 9)
    pl = Plot(x0, yb + 26, Lpx, 120, 0, 1, lo, hi)
    o += bmd(pl, fn, 0, 1)
    for xx, t, dy, anc in ticks:
        o += T(pl.X(xx), pl.Y(fn(xx)) + dy, t, 15, MOM, anc, 'bold')
    return o


def fig5_3():
    W, H = 900, 300
    o = ''
    Lpx = 230
    r1 = lambda t: -0.125 + 0.5 * min(t, 1 - t)                                      # PL/8
    r2 = lambda t: -1 / 12 + t * (1 - t) / 2                                          # wL²/12
    a = 0.3
    r3 = lambda t: (-a * (1 - a) ** 2 * (1 - t) - a * a * (1 - a) * t) + (a * (1 - a) * (t / a if t < a else (1 - t) / (1 - a)))
    o += _ff_row(30, 30, Lpx, r1, -0.15, 0.15, [(0.0, '−*PL*/8', 22, 'start'), (0.5, '+*PL*/8', -10, 'middle')], '跨中集中 *P*', 'mid')
    o += _ff_row(330, 30, Lpx, r2, -0.15, 0.15, [(0.0, '−*wL*^{2}/12', 22, 'start'), (0.5, '+*wL*^{2}/24', -10, 'middle')], '全跨均布 *w*', 'udl')
    o += _ff_row(630, 30, Lpx, r3, -0.17, 0.17, [(0.0, '−*Pab*^{2}/*L*^{2}', 24, 'start'), (1.0, '−*Pa*^{2}*b*/*L*^{2}', 24, 'end')], '偏心集中 *P*（*a* = 0.3*L*）', 'off')
    o += T(450, 288, '近載重的那一端彎矩比較大：*ab*^{2} 裡平方的是「遠的那段」，A 端離載重近（*a* 小）時 *b* 大、*M*_{A} 大', 15, MUT, 'middle')
    return svg(W, H, o, '三張標準固端彎矩圖')


def fig5_4():
    W, H = 900, 440
    fa, fb = C5['17_fa'], C5['17_fb']
    pl = Plot(100, 50, 470, 300, 0, 1, 0, 0.15)
    o = pl.axes([0, 0.25, 0.4, 0.5, 0.75, 1], [0, 1 / 24, 1 / 12, 1 / 8, 0.15], '*m*/*L*', '|*M*|/*wL*^{2}', size=14,
                yfmt=lambda t: {0: '0', 1 / 24: '1/24', 1 / 12: '1/12', 1 / 8: '1/8', 0.15: '0.15'}[t])
    o += pl.hline(1 / 12, c=MUT, w=1.6) + T(pl.X(1) + 6, pl.Y(1 / 12) + 5, '無內鉸 1/12', 14, MUT, 'start')
    o += pl.hline(1 / 8, c=MUT, w=1.2) + T(pl.X(1) + 6, pl.Y(1 / 8) + 5, '1/8', 14, MUT, 'start')
    o += pl.curve(lambda t: fa(max(t, 1e-6)), 0.0005, 0.9995, MOM, 3)
    o += pl.curve(lambda t: fb(max(t, 1e-6)), 0.0005, 0.9995, AC, 3)
    o += T(pl.X(0.86), pl.Y(fa(0.86)) - 14, '|*M*_{a}|', 16, MOM, 'middle', 'bold')
    o += T(pl.X(0.12), pl.Y(fb(0.12)) - 14, '|*M*_{b}|', 16, AC, 'middle', 'bold')
    o += pl.dot(0.5, 0.125, PUR) + L(pl.X(0.5), pl.Y(0.125) + 6, pl.X(0.5), pl.Y(0.035), PUR, 1.2, '3 3') + T(pl.X(0.5), pl.Y(0.03) + 4, '*m* = *n*：兩端都是 *wL*^{2}/8', 15, PUR, 'middle', 'bold')
    r = C5['17_r04']
    o += pl.dot(0.4, r[0], MOM, 4) + pl.dot(0.4, r[1], AC, 4)
    o += T(pl.X(0.4) - 8, pl.Y(r[0]) + 4, f'{r[0]:.4f}', 14, MOM, 'end') + T(pl.X(0.4) - 8, pl.Y(r[1]) + 16, f'{r[1]:.4f}', 14, AC, 'end')
    bx = 686
    o += R(bx, 60, 204, 290, KEY2, PUR, 1.4, 10)
    yy = 90
    for s, c, wgt, sz in [('能拿來驗算的極限', PUR, 'bold', 15), ('', INK, None, 4),
                          ('*m* → 0（鉸在 a 端）', INK, 'bold', 15), ('*M*_{a} → 0', MOM, None, 15), ('*M*_{b} → *wL*^{2}/8', AC, None, 15),
                          ('＝一端鉸、一端固定', MUT, None, 14), ('', INK, None, 4),
                          ('*m* = *n*（鉸在中央）', INK, 'bold', 15), ('兩端 *wL*^{2}/8', PUR, None, 15), ('＝兩根懸臂各扛一半', MUT, None, 14), ('', INK, None, 4),
                          ('✗ 不會回到 1/12', MOM, 'bold', 15)]:
        if s:
            o += T(bx + 102, yy, s, sz, c, 'middle', wgt)
        yy += sz + 9 if s else 4
    o += T(450, 400, 'SA-2017-2 通式（最小功法推得，calcs.py 以 sympy 重解核對差值為 0）', 15, MUT, 'middle')
    o += T(450, 424, '內鉸不一定讓固端彎矩變小：中段某些位置反而比 *wL*^{2}/12 大 50%', 15, INK, 'middle', 'bold')
    return svg(W, H, o, 'SA-2017-2 通式曲線')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
