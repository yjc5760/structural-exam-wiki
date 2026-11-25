# -*- coding: utf-8 -*-
"""第 4 章：衝量、Duhamel、半正弦脈衝、震波譜。"""
from sdfig import *  # noqa
from calcs import PUL, PUL_T, EX, P03, shock_spectrum_halfsine, PI
import math
import numpy as np


def fig4_1():
    W, H = 900, 400
    o = T(225, 28, '(a) 敲一下：衝量變成初速', 16, INK, 'middle', 'bold')
    pl = Plot(60, 60, 330, 110, 0, 1.6, 0, 1.2)
    o += pl.axes([0, 0.5, 1, 1.5], [0, 1], '*t*/*T*', '*p*', grid=False)
    o += pl.area(lambda t: 1.0 if t <= 0.06 else 0, lambda t: 0, 0, 0.06, WARNM, 0.9)
    o += T(pl.X(0.07) + 4, pl.Y(0.85), '面積 = 衝量 *I*', 15, WARN, 'start', 'bold')
    pl2 = Plot(60, 245, 330, 115, 0, 1.6, -1.1, 1.1)
    o += pl2.axes([0, 0.5, 1, 1.5], [-1, 0, 1], '*t*/*T*', '*u*', grid=False)
    o += pl2.curve(lambda t: math.sin(2 * PI * t) * math.exp(-0.05 * 2 * PI * t), 0, 1.6, AC, 2.6)
    o += A(pl2.X(0), pl2.Y(0), pl2.X(0.1), pl2.Y(0.6), KEY, 2, 9)
    o += T(pl2.X(0.12), pl2.Y(0.95), '起步斜率 = *I*/*m*', 15, KEY, 'start', 'bold')
    o += T(pl2.X(0.95), pl2.Y(-0.92), '*u* = *I*/(*m*ω_{D})·e^{−ξω*t*} sin ω_{D}*t*', 14, AC, 'middle')
    o += L(450, 20, 450, 390, GRID, 1.5)
    o += T(675, 28, '(b) 任意外力 = 一串小衝量（Duhamel）', 16, INK, 'middle', 'bold')
    pr = Plot(500, 60, 360, 110, 0, 1.6, 0, 1.2)
    fp = lambda t: math.sin(PI * t / 0.8) if t <= 0.8 else 0
    o += pr.axes([0, 0.5, 1, 1.5], [0, 1], 'τ', '*p*(τ)', grid=False)
    o += pr.curve(fp, 0, 1.6, WARN, 2.2)
    for k_ in range(8):
        tau = 0.05 + 0.1 * k_
        o += R(pr.X(tau - 0.04), pr.Y(fp(tau)), pr.X(tau + 0.04) - pr.X(tau - 0.04), pr.Y(0) - pr.Y(fp(tau)), WARNM, None, 0, op=0.8)
    pr2 = Plot(500, 245, 360, 115, 0, 1.6, -1.0, 1.0)
    o += pr2.axes([0, 0.5, 1, 1.5], [0, 1], '*t*', '*u*', grid=False)
    for k_, c in ((1, STEEL), (3, STEEL), (5, STEEL)):
        tau = 0.05 + 0.1 * k_
        a = fp(tau) * 0.1 * 2.5
        o += pr2.curve(lambda t, tau=tau, a=a: a * math.sin(2 * PI * (t - tau)) if t > tau else 0, 0, 1.6, c, 1.4, dash='4 3')
    def duh(t, n=400):
        s = 0; d = t / n if t > 0 else 0
        for i in range(n):
            tau = (i + 0.5) * d
            s += fp(tau) * math.sin(2 * PI * (t - tau)) * d
        return s * 2.5
    o += pr2.curve(duh, 0, 1.6, AC, 2.6, n=160)
    o += T(pr2.X(1.2), pr2.Y(0.85), '每塊衝量各引起一個小振動', 14, MUT, 'middle')
    o += T(pr2.X(0.3), pr2.Y(-0.75), '全部疊加 = 實線', 15, AC, 'middle', 'bold')
    return svg(W, H, o, '衝量與 Duhamel')


def fig4_2():
    W, H = 900, 430
    t, u = PUL_T
    pl = Plot(90, 40, 540, 110, 0, 0.8, 0, 1.2)
    o = pl.axes([0, 0.1, 0.2, 0.4, 0.6, 0.8], [0, 1], '*t* (s)', '*p* (10^{5} N)')
    o += pl.curve(lambda x: math.sin(PI * x / 0.1) if x <= 0.1 else 0, 0, 0.8, WARN, 2.6, n=400)
    o += T(pl.X(0.12), pl.Y(0.9), '半正弦：*p*_{0} = 100 kN、*t*_{d} = 0.1 s', 15, WARN, 'start', 'bold')
    p2 = Plot(90, 220, 540, 170, 0, 0.8, -6, 7)
    o += p2.axes([0, 0.1, 0.2, 0.4, 0.6, 0.8], [-6, -3, 0, 3, 6], '*t* (s)', '*u* (cm)')
    tt = t[t <= 0.8]; uu = u[:len(tt)] * 100
    o += P([p2.pt(a, b) for a, b in zip(tt[::20], uu[::20])], AC, 2.6)
    o += p2.vline(0.1, -6, 7, KEY, 1.4)
    o += p2.dot(PUL['td'], PUL['u_td'] * 100, KEY, 5)
    o += T(p2.X(0.1) + 8, p2.Y(PUL['u_td'] * 100) + 22, f'*u*(*t*_{{d}}) = {PUL["u_td"]*100:.2f}', 15, KEY, 'start')
    o += p2.dot(PUL['t_at_max'], PUL['umax_damped'] * 100, COMP, 6)
    o += T(p2.X(PUL['t_at_max']) + 10, p2.Y(PUL['umax_damped'] * 100) - 6, f'最大 {PUL["umax_damped"]*100:.2f} cm（*t* = {PUL["t_at_max"]:.3f} s）', 15, COMP, 'start', 'bold')
    o += p2.hline(PUL['umax_undamped'] * 100, 0.12, 0.8, MUT, 1.2)
    o += T(p2.X(0.79), p2.Y(PUL['umax_undamped'] * 100) - 6, f'不計阻尼 {PUL["umax_undamped"]*100:.2f}', 14, MUT, 'end')
    o += box(712, 60, 180, 330, '兩階段', ['① 0 ≤ *t* ≤ *t*_{d}', '外力作用中', '（強迫振動）', '', '② *t* > *t*_{d}', '以 *u*(*t*_{d})、*u̇*(*t*_{d})', '為初始條件的', '自由振動', '', '最大值在②'], KEY2, KEY, 16, 15)
    return svg(W, H, o, '半正弦脈衝反應')


def fig4_3():
    W, H = 900, 380
    xs = [0.02, 0.05, 0.08, 0.1, 0.13, 0.159, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    ys = [shock_spectrum_halfsine(x) for x in xs]
    pl = Plot(90, 40, 560, 280, 0, 2.0, 0, 2.0)
    o = pl.axes([0, 0.25, 0.5, 1, 1.5, 2], [0, 0.5, 1, 1.5, 2], '*t*_{d}/*T*', '*u*_{max}/*u*_{st}')
    o += pl.area(lambda x: 2, lambda x: 0, 0, 0.25, TEN2, 0.7)
    o += P([pl.pt(a, b) for a, b in zip(xs, ys)], COMP, 3)
    o += pl.curve(lambda x: 4 * x, 0, 0.5, WARN, 2.2, dash='7 5')
    o += pl.dot(PUL['td_T'], shock_spectrum_halfsine(PUL['td_T']), KEY, 6)
    o += T(pl.X(PUL['td_T']) + 10, pl.Y(0.55) + 26, f'2021-2：{PUL["td_T"]:.3f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.125), pl.Y(1.85), '衝量區', 15, TEN, 'middle', 'bold')
    o += T(pl.X(0.5) + 6, pl.Y(1.95), '衝量近似 4*t*_{d}/*T*', 15, WARN, 'start', 'bold')
    o += T(pl.X(1.45), pl.Y(1.78), '精確（無阻尼）', 15, COMP, 'middle', 'bold')
    o += R(670, 60, 220, 230, KEY2, KEY, 1.4, 8)
    o += T(780, 88, '*t*_{d}/*T* ≲ 0.25', 16, KEY, 'middle', 'bold')
    o += T(780, 118, '只看面積（衝量）', 15, INK, 'middle')
    o += T(780, 144, '形狀、峰值不重要', 15, INK, 'middle')
    o += T(780, 184, '*t*_{d}/*T* ≈ 0.5～1', 16, KEY, 'middle', 'bold')
    o += T(780, 214, '最大放大約 1.77', 15, INK, 'middle')
    o += T(780, 244, '要分段精算', 15, INK, 'middle')
    return svg(W, H, o, '半正弦脈衝的震波譜')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
