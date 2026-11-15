# -*- coding: utf-8 -*-
"""第 2 章：搭便車證明（S4）、疊加 M = M0 + Q·m（S5）、四種虛設力、懸臂梁範例三張彎矩圖。"""
from sa_draw import *  # noqa
import math
import calcs

C2 = calcs.C2
ENE = PUR


def _cant(x0, y0, Lp, defl=0.0, c=INK, w=4):
    """左端固定的懸臂梁；defl：自由端下垂像素（三次曲線示意）。"""
    o = wall(x0, y0, 54, 'left')
    pts = [(x0 + Lp * t, y0 + defl * (3 * t * t - t ** 3) / 2) for t in [i / 60 for i in range(61)]]
    o += P(pts, c, w)
    return o, pts


def fig2_1():
    W, H = 900, 400
    o = ''
    # (a) 先放 dP
    x0, y0, Lp = 40, 110, 230
    o += T(x0 + Lp / 2, 34, '(a) 先放小力 *dP*', 16, INK, 'middle', 'bold')
    b, pts = _cant(x0, y0, Lp, 6, AC)
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '5 4') + b
    xi, yi = pts[-1]
    o += A(xi, yi - 44, xi, yi - 4, KEY, 1.8, 8) + T(xi + 6, yi - 30, '*dP*', 15, KEY, 'start', 'bold')
    o += T(x0 + Lp / 2, y0 + 70, '自己的三角形極小，忽略', 14, MUT, 'middle')
    # (b) 再加原載重
    x0 = 330
    o += T(x0 + Lp / 2, 34, '(b) 再加原載重 *P*', 16, INK, 'middle', 'bold')
    b, pts = _cant(x0, y0, Lp, 70, AC)
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '5 4') + b
    xi, yi = pts[-1]
    xp, yp = pts[-7]
    o += A(xp, yp - 64, xp, yp - 4, LOAD, 2.6, 11) + T(xp - 8, yp - 44, '*P*', 16, LOAD, 'end', 'bold')
    o += A(xi + 2, yi - 44, xi + 2, yi - 5, KEY, 1.8, 8) + T(xi + 8, yi - 30, '*dP*', 15, KEY, 'start', 'bold')
    o += dim(xi + 48, y0, xi + 48, yi, '', AC) + T(xi + 58, (y0 + yi) / 2 + 6, 'Δ_{i}', 16, AC, 'start', 'bold')
    o += T(x0 + Lp / 2, y0 + 120, '*dP* 被載著走 Δ_{i}', 15, KEY, 'middle', 'bold')
    o += T(x0 + Lp / 2, y0 + 144, '功 = 矩形 *dP*·Δ_{i}（沒有 ½）', 15, KEY, 'middle')
    # (c) 力-變形圖
    pl = Plot(660, 70, 190, 220, 0, 1, 0, 1)
    o += T(755, 34, '(c) *i* 點的力–變形圖', 16, INK, 'middle', 'bold')
    o += A(pl.X(0), pl.Y(0), pl.X(1) + 14, pl.Y(0), INK, 1.4, 8) + A(pl.X(0), pl.Y(0), pl.X(0), pl.Y(1) - 10, INK, 1.4, 8)
    Pv, dv = 0.70, 0.78
    o += P([pl.pt(0, 0), pl.pt(dv, Pv), pl.pt(dv, 0)], None, fill=KEY2, close=True)
    o += P([pl.pt(0, Pv), pl.pt(dv, Pv), pl.pt(dv, Pv + 0.09), pl.pt(0, Pv + 0.09)], KEY, 1.4, fill='#e1bee7', close=True)
    o += L(pl.X(0), pl.Y(0), pl.X(dv), pl.Y(Pv), AC, 2.6)
    o += T(pl.X(dv * 0.62), pl.Y(Pv * 0.28), '*U*', 17, ENE, 'middle', 'bold')
    o += T(pl.X(0) - 6, pl.Y(Pv) + 5, '*P*', 15, LOAD, 'end', 'bold')
    o += T(pl.X(0) - 6, pl.Y(Pv + 0.09) - 3, '+*dP*', 14, KEY, 'end', 'bold')
    o += T(pl.X(dv), pl.Y(0) + 20, 'Δ_{i}', 15, AC, 'middle', 'bold')
    o += T(pl.X(dv / 2), pl.Y(Pv + 0.09) - 10, '多出 Δ_{i}·*dP*', 14, KEY, 'middle', 'bold')
    o += R(150, 318, 600, 64, KEY2, PUR, 1.4, 10)
    o += T(450, 344, '能量只看最後狀態：*U* + Δ_{i}·*dP* = *U* + (∂*U*/∂*P*)·*dP*', 16, PUR, 'middle', 'bold')
    o += T(450, 370, '⇒ Δ_{i} = ∂*U*/∂*P*_{i}', 17, PUR, 'middle', 'bold')
    return svg(W, H, o, '卡氏定理搭便車證明')


def _beam_row(y, Lpx, x0, label, fn, ymin, ymax, c, fill, ticks, note, h=90):
    """畫一列彎矩圖：fn(x_m) 下緣受拉為正；x 由 C（右端）往左量，故 X 座標反向。"""
    pl = Plot(x0, y, Lpx, h, -12, 0, ymin, ymax)   # 用 −x 讓 C 在右
    g = lambda u: fn(-u)
    o = bmd(pl, g, -12, 0, c, fill)
    o += T(x0 - 14, pl.Y(0) + 5, label, 16, c, 'end', 'bold')
    for xm, txt, dy in ticks:
        o += T(pl.X(-xm), pl.Y(fn(xm)) + dy, txt, 15, c, 'middle', 'bold')
    o += T(x0 + Lpx + 18, pl.Y(0) + 5, note, 15, INK, 'start')
    return o, pl


def fig2_2():
    W, H = 900, 470
    x0, Lpx = 150, 480
    o = ''
    # 懸臂梁示意
    yb = 60
    o += wall(x0, yb, 44, 'left') + L(x0, yb, x0 + Lpx, yb, INK, 4)
    o += A(x0 + Lpx / 2, yb - 44, x0 + Lpx / 2, yb - 4, LOAD, 2.4, 10) + T(x0 + Lpx / 2 + 8, yb - 26, '20 kN', 15, LOAD, 'start', 'bold')
    o += A(x0 + Lpx, yb - 44, x0 + Lpx, yb - 4, FOR, 2.4, 10) + T(x0 + Lpx + 8, yb - 26, '*Q*', 16, FOR, 'start', 'bold')
    o += T(x0 - 8, yb - 30, 'A', 16, INK, 'end', 'bold') + T(x0 + Lpx / 2, yb + 24, 'B', 15, INK, 'middle', 'bold')
    o += T(x0 + Lpx + 8, yb + 24, 'C', 16, INK, 'start', 'bold')
    o += A(x0 + Lpx, yb + 40, x0 + Lpx - 60, yb + 40, MUT, 1.3, 8) + T(x0 + Lpx - 66, yb + 46, '*x*', 15, MUT, 'end')
    r1, _ = _beam_row(130, Lpx, x0, '*M*_{0}', lambda x: calcs.M_real(x), -130, 10, MOM, '#ef9a9a',
                      [(12, '−120', 24)], '20 kN 造成的')
    r2, _ = _beam_row(250, Lpx, x0, '*m*', lambda x: -x, -13, 1, FOR, TENM,
                      [(12, '−12', 24)], 'C 端單位力造成的')
    o += r1 + r2
    o += T(x0 + Lpx / 2, 225, '+', 26, INK, 'middle', 'bold')
    o += R(150, 370, 600, 84, KEY2, PUR, 1.4, 10)
    o += T(450, 398, '*M* = *M*_{0} + *Q*·*m*', 18, PUR, 'middle', 'bold')
    o += T(450, 430, '⇒ ∂*M*/∂*Q* = *m*（把單位力的彎矩圖拿出來）', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '疊加 M = M0 + Q m')


def fig2_3():
    W, H = 900, 300
    o = ''
    titles = ['(a) 垂直位移', '(b) 轉角', '(c) 兩點相對位移', '(d) 鉸兩側相對轉角']
    for k in range(4):
        x0 = 20 + k * 222
        cx = x0 + 100
        o += T(cx, 36, titles[k], 16, INK, 'middle', 'bold')
        yb = 140
        if k in (0, 1):
            o += L(x0 + 10, yb, x0 + 190, yb, INK, 4)
            o += pin(x0 + 10, yb) + roller(x0 + 190, yb)
            if k == 0:
                o += A(cx, yb - 56, cx, yb - 4, FOR, 2.6, 11) + T(cx + 8, yb - 34, '*Q*', 16, FOR, 'start', 'bold')
            else:
                o += moment(cx, yb, 26, cw=False, c=FOR) + T(cx, yb - 36, '*Q*', 16, FOR, 'middle', 'bold')
        elif k == 2:
            # 桁架兩節點相對位移：一對力
            pa, pb = (x0 + 30, yb + 40), (x0 + 170, yb - 40)
            o += L(pa[0], pa[1], pb[0], pb[1], STEEL, 1.6, '5 4')
            o += C(pa[0], pa[1], 6, '#fff', INK) + C(pb[0], pb[1], 6, '#fff', INK)
            ux, uy = (pb[0] - pa[0]) / 161, (pb[1] - pa[1]) / 161
            o += A(pa[0] + ux * 8, pa[1] + uy * 8, pa[0] + ux * 54, pa[1] + uy * 54, FOR, 2.4, 10)
            o += A(pb[0] - ux * 8, pb[1] - uy * 8, pb[0] - ux * 54, pb[1] - uy * 54, FOR, 2.4, 10)
            o += T(pa[0] - 8, pa[1] + 26, '*Q*', 16, FOR, 'start', 'bold') + T(pb[0] + 6, pb[1] - 10, '*Q*', 16, FOR, 'start', 'bold')
        else:
            o += L(x0 + 10, yb, cx - 6, yb, INK, 4) + L(cx + 6, yb, x0 + 190, yb, INK, 4)
            o += hinge(cx, yb)
            o += moment(cx - 34, yb, 20, cw=True, c=FOR, start=140, span=220)
            o += moment(cx + 34, yb, 20, cw=False, c=FOR, start=40, span=220)
            o += T(cx - 34, yb - 30, '*Q*', 15, FOR, 'middle', 'bold') + T(cx + 34, yb - 30, '*Q*', 15, FOR, 'middle', 'bold')
        res = ['加力 → Δ', '加力偶 → θ', '一對反向力', '一對反向力偶'][k]
        o += T(cx, 236, res, 15, PUR, 'middle', 'bold')
    o += T(450, 284, '求什麼、在哪裡、往哪個方向，就把 *Q* 放在那裡、朝那個方向', 15, MUT, 'middle')
    return svg(W, H, o, '四種虛設力')


def fig2_4():
    W, H = 900, 500
    x0, Lpx = 150, 480
    o = ''
    yb = 60
    o += wall(x0, yb, 44, 'left') + L(x0, yb, x0 + Lpx, yb, INK, 4)
    o += A(x0 + Lpx / 2, yb - 44, x0 + Lpx / 2, yb - 4, LOAD, 2.4, 10) + T(x0 + Lpx / 2 + 8, yb - 26, '20 kN', 15, LOAD, 'start', 'bold')
    o += T(x0 - 8, yb - 30, 'A', 16, INK, 'end', 'bold') + T(x0 + Lpx / 2, yb + 24, 'B', 15, INK, 'middle', 'bold')
    o += T(x0 + Lpx + 8, yb + 6, 'C', 16, INK, 'start', 'bold')
    o += dim(x0, yb + 30, x0 + Lpx / 2, yb + 30, '', MUT) + dim(x0 + Lpx / 2, yb + 30, x0 + Lpx, yb + 30, '', MUT)
    o += T(x0 + Lpx / 4, yb + 52, '6 m', 14, MUT, 'middle') + T(x0 + 3 * Lpx / 4, yb + 52, '6 m', 14, MUT, 'middle')
    r1, _ = _beam_row(140, Lpx, x0, '*M*', lambda x: calcs.M_real(x), -130, 10, MOM, '#ef9a9a',
                      [(12, '−120', 24)], '*M* = −20(*x* − 6)')
    r2, _ = _beam_row(260, Lpx, x0, '*m*_{1}', lambda x: -x, -13, 1, FOR, TENM,
                      [(12, '−12', 24)], 'C 向下單位力')
    r3, _ = _beam_row(380, Lpx, x0, '*m*_{2}', lambda x: 1.0, -1.2, 1.4, FOR, TENM,
                      [(6, '+1', -10)], 'C 逆時針單位力偶', h=60)
    o += r1 + r2 + r3
    o += R(150, 456, 600, 38, KEY2, PUR, 1.4, 8)
    o += T(450, 481, f"δ_{C} = {C2['dC']}/*EI*（向下）　θ_{C} = {-C2['thC_ccw']}/*EI*（順時針）", 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '懸臂梁範例彎矩圖')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4}
