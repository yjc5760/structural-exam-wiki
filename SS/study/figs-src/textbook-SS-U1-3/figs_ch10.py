# -*- coding: utf-8 -*-
"""第 10 章：直接分析法（假想水平力、τb、1.6）與強柱弱梁。"""
from plot import *  # noqa
from calcs import tau_b, crc_tangent, alpha_asd, Mpc_ratio_strong
import math


def fig10_1():
    W_, H = 900, 420
    o = T(220, 32, '(a) 真的歪 *L*/500', 16, INK, 'middle', 'bold')
    xb, yb, yt, D = 180, 320, 90, 46       # D 放大顯示
    o += L(xb, yt - 10, xb, yb, MUT, 1.2, '6 5')
    o += L(xb + D, yt, xb, yb, AC, 6) + pin(xb, yb)
    o += A(xb + D, yt - 60, xb + D, yt - 6, COMP, 3, 12) + T(xb + D + 10, yt - 34, '*Y*（該層重力）', 15, COMP, 'start', 'bold')
    o += dim(xb, yt + 20, xb + D, yt + 20, '', MUT)
    o += T(xb - 8, yt + 26, 'Δ_{0} = *L*/500', 15, MUT, 'end')
    o += T(220, 384, '傾倒力矩 *Y*·Δ_{0} = *Y**L*/500', 15, INK, 'middle', 'bold')
    o += T(450, 210, '＝', 30, INK, 'middle', 'bold')
    o += T(680, 32, '(b) 擺正，改加一個側力', 16, INK, 'middle', 'bold')
    xb2 = 640
    o += L(xb2, yt, xb2, yb, AC, 6) + pin(xb2, yb)
    o += A(xb2, yt - 60, xb2, yt - 6, COMP, 3, 12) + T(xb2 + 10, yt - 34, '*Y*', 15, COMP, 'start', 'bold')
    o += A(xb2 - 90, yt, xb2 - 6, yt, KEY, 3.4, 13) + T(xb2 - 92, yt - 12, '*N*_{i}', 16, KEY, 'start', 'bold')
    o += dim(xb2 + 40, yt, xb2 + 40, yb, '*L*', MUT, size=15)
    o += T(680, 380, '*N*_{i}·*L* = *Y**L*/500', 15, INK, 'middle', 'bold')
    o += T(680, 406, '⇒ *N*_{i} = 0.002 *Y*_{i}', 17, KEY, 'middle', 'bold')
    return svg(W_, H, o, '假想水平力')


def fig10_2():
    W_, H = 900, 400
    pl = Plot(70, 60, 330, 260, 0, 1, 0, 1.05)
    o = T(235, 32, '(a) τ_{b}：軸力大，勁度再打折', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 0.25, 0.5, 0.75, 1.0], [0, 0.5, 1.0], 'α*P*_{r}/*P*_{y}', 'τ_{b}', size=14)
    o += pl.curve(crc_tangent, 0, 1, MUT, 1.6, dash='5 4')
    o += pl.curve(tau_b, 0, 1, COMP, 3.4)
    o += pl.vline(0.5, c=INK, w=1.1, dash='3 4')
    o += T(pl.X(0.52), pl.Y(0.3), '4*p*(1 − *p*)', 15, COMP, 'start', 'bold')
    o += T(pl.X(0.03), pl.Y(0.9), '*p* ≤ 0.5：τ_{b} = 1', 14, COMP, 'start')
    o += T(pl.X(0.03), pl.Y(0.55), '灰虛：CRC 柱曲線', 14, MUT, 'start')
    o += T(pl.X(0.03), pl.Y(0.55) + 20, '的 *E*_{t}/*E*', 14, MUT, 'start')
    o += L(450, 20, 450, 390, GRID, 1.5)
    pl2 = Plot(510, 60, 330, 260, 0, 10, 1.1, 1.7)
    o += T(675, 32, '(b) ASD 載重要乘幾倍才到 LRFD？', 16, INK, 'middle', 'bold')
    o += pl2.axes([0, 2, 4, 6, 8, 10], [1.2, 1.4, 1.6], '*L*/*D*', '倍數', size=14)
    o += pl2.curve(alpha_asd, 0, 10, AC, 3.4)
    o += pl2.hline(1.6, c=KEY, w=1.6, dash='6 4')
    o += T(pl2.X(10), pl2.Y(1.6) - 8, '取上限 1.6', 15, KEY, 'end', 'bold')
    o += T(pl2.X(0.3), pl2.Y(1.25), '(1.2*D* + 1.6*L*)/(*D* + *L*)', 14, AC, 'start')
    o += T(675, 376, '活載重越多越接近 1.6；取上限較保守', 14, MUT, 'middle')
    return svg(W_, H, o, 'τb 與 1.6')


def fig10_3():
    W_, H = 900, 420
    o = T(220, 32, '兩種倒法', 16, INK, 'middle', 'bold')

    def frame(ox, beam_hinge):
        s = ''
        xs = [ox + 20, ox + 120, ox + 220]
        ys = [330, 250, 170, 90]
        D = [0, 20, 40, 60] if beam_hinge else [0, 60, 60, 60]
        for j in range(3):
            for i in range(3):
                s += L(xs[j] + D[i], ys[i], xs[j] + D[i + 1], ys[i + 1], AC, 4)
        for i in range(1, 4):
            s += L(xs[0] + D[i], ys[i], xs[2] + D[i], ys[i], STEEL, 5)
        for x in xs:
            s += fixed_wall(x, ys[0], 30)
        if beam_hinge:
            for i in range(1, 4):
                for j in range(3):
                    for dx in (12, -12):
                        if (j == 0 and dx < 0) or (j == 2 and dx > 0):
                            continue
                        s += C(xs[j] + D[i] + dx, ys[i], 5, KEY, '#fff', 1.2)
            for x in xs:
                s += C(x, ys[0] - 10, 5, KEY, '#fff', 1.2)
        else:
            for x in xs:
                s += C(x, ys[0] - 10, 5, COMP, '#fff', 1.2) + C(x + 60, ys[1] + 10, 5, COMP, '#fff', 1.2)
        return s
    o += frame(10, True) + frame(265, False)
    o += T(130, 372, '強柱弱梁：鉸在梁端', 15, KEY, 'middle', 'bold')
    o += T(130, 396, '整棟一起變形、慢慢消能', 14, INK, 'middle')
    o += T(385, 372, '弱柱：一層的柱上下都鉸', 15, COMP, 'middle', 'bold')
    o += T(385, 396, '那一層整層倒（層崩塌）', 14, INK, 'middle')
    o += L(548, 20, 548, 410, GRID, 1.5)
    o += R(558, 60, 330, 320, KEY2, KEY, 1.6, 10)
    lines = [('我國式 (13.6-3)', KEY, 'bold'),
             ('Σ*Z*_{c}(*F*_{yc} − *P*_{uc}/*A*_{g})', INK, 'bold'),
             ('　≥ 1.25 Σ*Z*_{b}*F*_{yb}', INK, 'bold'),
             ('柱側：軸力吃掉一部分 *F*_{y}', COMP, None),
             ('*M*_{pc} ≈ *M*_{p}(1 − *P*/*P*_{y})', INK, None),
             ('　= *Z*(*F*_{y} − *P*/*A*)（種子 S6 直線）', INK, None),
             ('梁側：梁實際比標稱強', TEN, None),
             ('（材料超強＋應變硬化）× 1.25', INK, None)]
    for k, (s, c, w) in enumerate(lines):
        o += T(572, 94 + k * 36, s, 15 if w else 14.5, c, 'start', w)
    return svg(W_, H, o, '強柱弱梁')


ALL = {'fig10_1': fig10_1, 'fig10_2': fig10_2, 'fig10_3': fig10_3}
