# -*- coding: utf-8 -*-
"""第 2 章：莫爾圓推 Ka、Kp；Ka、Kp 隨 φ。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig2_1():
    d = mohr_demo()
    W_, H = 900, 400
    sc = 2.1
    ox, oy = 70, 330
    X = lambda s: ox + s * sc
    Y = lambda t: oy - t * sc
    o = ''
    o += A(ox, oy, X(340), oy, INK, 1.6, 9) + A(ox, oy, ox, Y(140), INK, 1.6, 9)
    o += T(X(340) + 6, oy + 5, 'σ′', 16, INK, 'start')
    o += T(ox, Y(140) - 10, 'τ', 16, INK, 'middle')
    for s in (0, 50, 100, 200, 300):
        o += L(X(s), oy, X(s), oy + 5, INK, 1) + T(X(s), oy + 22, f'{s}', 14, MUT, 'middle')
    o += L(ox, oy, X(235), Y(235 * tan(30)), KEY, 2.4)
    o += T(X(235) + 8, Y(235 * tan(30)) + 4, '破壞線 τ = σ′ tan φ', 15, KEY, 'start', 'bold')
    def circ(a, b, c, w, dash=None):
        cx, rr = (a + b) / 2, (b - a) / 2
        pts = [(X(cx + rr * math.cos(math.pi * i / 90)), Y(rr * math.sin(math.pi * i / 90))) for i in range(91)]
        return P(pts, c, w, dash=dash)
    o += circ(d['sa'], d['sv'], TEN, 3)
    o += circ(d['s0'], d['sv'], AC, 2, '6 4')
    o += circ(d['sv'], d['sp'], COMP, 3)
    o += C(X(d['sv']), oy, 6, INK, '#fff', 2)
    o += T(X(d['sv']), oy + 42, 'σ_{v}′ = 100（固定）', 15, INK, 'middle', 'bold')
    o += C(X(d['sa']), oy, 5, TEN, '#fff', 2)
    o += T(X(d['sa']), oy + 42, f"σ_{{a}} = {d['sa']:.1f}", 15, TEN, 'middle', 'bold')
    o += C(X(d['s0']), oy, 5, AC, '#fff', 2)
    o += C(X(d['sp']), oy, 5, COMP, '#fff', 2)
    o += T(X(d['sp']), oy + 42, f"σ_{{p}} = {d['sp']:.0f}", 15, COMP, 'middle', 'bold')
    o += T(X(66), Y(52), '主動圓', 15, TEN, 'middle', 'bold')
    o += T(X(200), Y(112), '被動圓', 15, COMP, 'middle', 'bold')
    o += T(X(75), Y(10) - 2, '*K*_{0}', 14, AC, 'middle', 'bold')
    o += R(700, 60, 190, 160, KEY2, KEY, 1.4, 8)
    o += T(795, 88, 'φ = 30°、*c* = 0', 15, KEY, 'middle', 'bold')
    o += T(795, 118, '*K*_{a} = 33.3/100 = 1/3', 15, TEN, 'middle')
    o += T(795, 146, '*K*_{0} = 50/100 = 0.5', 15, AC, 'middle')
    o += T(795, 174, '*K*_{p} = 300/100 = 3', 15, COMP, 'middle')
    o += T(795, 204, '*K*_{p} = 1/*K*_{a}', 15, INK, 'middle', 'bold')
    return svg(W_, H, o, '莫爾圓推導 Rankine 主被動土壓')


def fig2_2():
    W_, H = 900, 380
    pl = Plot(100, 50, 520, 270, 20, 40, 0, 1.0)
    o = T(360, 30, '(左軸) *K*_{a} 與 *K*_{0}', 15, INK, 'middle', 'bold')
    o += pl.axes([20, 25, 30, 35, 40], [0, 0.25, 0.5, 0.75, 1.0], 'φ（°）', '*K*')
    o += pl.curve(Ka, 20, 40, TEN, 3)
    o += pl.curve(lambda p: K0(p), 20, 40, AC, 2.4, '6 4')
    o += pl.dot(30, Ka(30), TEN, 6)
    o += T(pl.X(30) + 8, pl.Y(Ka(30)) + 22, '30° → 1/3', 14, TEN, 'start', 'bold')
    o += pl.dot(35, Ka(35), TEN, 5)
    o += T(pl.X(35) + 8, pl.Y(Ka(35)) + 20, f'35° → {Ka(35):.3f}', 14, TEN, 'start', 'bold')
    o += T(pl.X(21), pl.Y(K0(21)) - 10, '*K*_{0} = 1 − sin φ', 14, AC, 'start', 'bold')
    o += T(pl.X(21), pl.Y(0.12), '*K*_{a} = tan²(45° − φ/2)', 14, TEN, 'start', 'bold')
    o += R(650, 80, 240, 160, KEY2, KEY, 1.4, 8)
    o += T(770, 108, '同一個 φ', 15, KEY, 'middle', 'bold')
    for i, ph in enumerate((25, 30, 35)):
        o += T(770, 138 + i * 30, f'{ph}°：*K*_{{a}} {Ka(ph):.3f}、*K*_{{p}} {Kp(ph):.2f}', 15, INK, 'middle')
    return svg(W_, H, o, 'Ka、K0 隨 φ')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
