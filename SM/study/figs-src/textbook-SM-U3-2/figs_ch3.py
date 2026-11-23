# -*- coding: utf-8 -*-
"""第 3 章：2016-4 自由體圖、2018-4 虛擬牆背。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig3_1():
    d = ex2016_4()
    W, H = 900, 460
    o = ''
    s = 44
    ox, oy = 220, 400
    X = lambda x: ox + x * s
    Y = lambda y: oy - y * s
    o += P([(X(0), Y(0)), (X(5), Y(0)), (X(3), Y(8)), (X(0), Y(8))], INK, 2, fill=STEEL2, close=True)
    o += L(X(3), Y(0), X(3), Y(8), MUT, 1, '4 3')
    o += L(X(3), Y(8), X(9), Y(8), INK, 1.4) + T(X(8.8), Y(8) - 6, '背填土', 14, INK, 'end')
    o += hatch_ground(X(-2), Y(0), 9 * s)
    o += C(X(0), Y(0), 6, KEY, '#fff', 2) + T(X(0) - 8, Y(0) + 22, '牆趾（原點）', 14, KEY, 'end', 'bold')
    o += A(X(1.5), Y(5.2), X(1.5), Y(3.2), AC, 2.8, 12) + T(X(1.5) + 8, Y(5.0), f"*W*_{{1}}={d['W1']:.0f}", 15, AC, 'start', 'bold')
    o += A(X(3.667), Y(3.4), X(3.667), Y(1.6), AC, 2.8, 12) + T(X(3.667) + 8, Y(3.2), f"*W*_{{2}}={d['W2']:.0f}", 15, AC, 'start', 'bold')
    # Pa
    xp, yp = d['xpa'], d['H'] / 3
    ang = rad(d['ang'])
    Lr = 150
    sx, sy = X(xp) + Lr * math.cos(ang), Y(yp) - Lr * math.sin(ang)
    o += A(sx, sy, X(xp) + 3, Y(yp) - 2, TEN, 3.2, 13)
    o += T(sx + 6, sy - 6, f"*P*_{{a}}={d['Pa']:.2f}", 15, TEN, 'start', 'bold')
    o += T(sx + 6, sy + 16, f"與水平 {d['ang']:.2f}°", 14, TEN, 'start')
    o += A(X(xp) + 130, Y(yp) + 46, X(xp) + 4, Y(yp) + 46, TEN, 2, 10, dash='5 3') + T(X(xp) + 134, Y(yp) + 51, f"*P*_{{ah}}={d['Pah']:.2f}", 14, TEN, 'start')
    o += A(X(xp) + 40, Y(yp) - 70, X(xp) + 40, Y(yp) - 4, TEN, 2, 10, dash='5 3') + T(X(xp) + 46, Y(yp) - 60, f"*P*_{{av}}={d['Pav']:.2f}", 14, TEN, 'start')
    o += C(X(xp), Y(yp), 5, TEN, '#fff', 1.6)
    o += dim(X(0), Y(0) + 30, X(xp), Y(0) + 30, '', MUT) + T(X(xp / 2), Y(0) + 50, f'{xp:.3f}', 14, MUT, 'middle')
    o += dim(X(-0.8), Y(0), X(-0.8), Y(yp), '', MUT) + T(X(-0.9), Y(yp / 2) + 5, '2.667', 14, MUT, 'end')
    o += box(650, 40, 235, 140, '帳', [f"Σ*V*={d['V']:.2f}", f"Σ*M*_{{R}}={d['MR']:.1f}", f"Σ*M*_{{O}}={d['MO']:.1f}"], KEY2, KEY)
    return svg(W, H, o, '2016-4 自由體圖')


def fig3_2():
    d = ex2018_4()
    W, H = 900, 500
    o = ''
    s = 40
    ox, oy = 170, 440
    X = lambda x: ox + x * s
    Y = lambda y: oy - y * s
    t, B = d['t'], d['B']
    # 底版、牆身
    o += R(X(0), Y(t), B * s, t * s, STEEL2, INK, 1.6)
    o += P([(X(1.5), Y(t)), (X(2.1), Y(t)), (X(2.1), Y(t + 7.5)), (X(1.7), Y(t + 7.5))], INK, 1.6, fill=STEEL2, close=True)
    # 踵上土
    hb = d['heel'] * tan(d['alpha'])
    o += P([(X(2.1), Y(t)), (X(B), Y(t)), (X(B), Y(t + 7.5 + hb)), (X(2.1), Y(t + 7.5))], '#8d6e63', 1.2, fill='#efe6d8', close=True)
    o += T(X(3.85), Y(t + 3.5), '*W*_{4} 踵上土', 15, '#5d4037', 'middle', 'bold')
    o += T(X(3.9), Y(t + 7.5) + 2, '*W*_{5}', 14, '#5d4037', 'middle')
    o += R(X(0), Y(t + 0.79), 1.5 * s, 0.79 * s, '#efe6d8', None, 0) + T(X(0.75), Y(t + 0.4) + 5, '*W*_{6}', 14, '#5d4037', 'middle')
    # 地表
    o += L(X(2.1), Y(t + 7.5), X(B + 2.5), Y(t + 7.5 + (B + 2.5 - 2.1) * tan(d['alpha'])), INK, 1.6)
    # 虛擬牆背
    o += L(X(B), Y(0), X(B), Y(t + 7.5 + hb), KEY, 2.4, '7 4')
    o += T(X(B) + 8, Y(d['Hp'] / 2), f"虛擬牆背 *H*′={d['Hp']:.3f}", 15, KEY, 'start', 'bold')
    # Pa 平行地表
    yp = d['Hp'] / 3
    a = rad(d['alpha'])
    Lr = 170
    sx, sy = X(B) + Lr * math.cos(a), Y(yp) - Lr * math.sin(a)
    o += A(sx, sy, X(B) + 3, Y(yp), TEN, 3.2, 13)
    o += T(sx + 6, sy + 18, f"*P*_{{a}}={d['Pa']:.2f}（平行 12° 地表）", 15, TEN, 'start', 'bold')
    o += dim(X(B) + 30, Y(0), X(B) + 30, Y(yp), '', TEN) + T(X(B) + 38, Y(yp / 2) + 5, f"{yp:.3f}", 14, TEN, 'start')
    o += C(X(0), Y(0), 6, KEY, '#fff', 2) + T(X(0) - 6, Y(0) + 20, '牆趾', 14, KEY, 'end', 'bold')
    o += dim(X(0), Y(0) + 26, X(1.5), Y(0) + 26, '1.5', MUT, size=14) + dim(X(2.1), Y(0) + 26, X(B), Y(0) + 26, '3.5', MUT, size=14)
    o += box(650, 320, 240, 150, '帳（kN/m）', [f"Σ*V*={d['V']:.2f}", f"Σ*M*_{{R}}={d['MR']:.1f}", f"Σ*M*_{{O}}={d['MO']:.1f}", f"*K*_{{a}}={d['Ka']:.4f}"], KEY2, KEY)
    return svg(W, H, o, '虛擬牆背')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
