# -*- coding: utf-8 -*-
"""第 3 章：含凝聚力的主動土壓與張力裂縫（2015-2 上層黏土）、φ = 0 的 σv ± 2Su。"""
from plot import *  # noqa
from calcs import *  # noqa


def _depth_axes(o, x0, w, top, bot, zmax, xmin, xmax, xt, xlab, zt):
    Y = lambda z: top + z / zmax * (bot - top)
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * w
    for t in xt:
        o += L(X(t), top, X(t), bot, GRID, 1) + T(X(t), top - 10, f'{t:g}', 14, MUT, 'middle')
    for z in zt:
        o += T(X(xmin) - 8, Y(z) + 5, f'{z:g}', 14, MUT, 'end')
    o += A(X(xmin), top, X(xmax) + 14, top, INK, 1.4, 8)
    o += L(X(0), top, X(0), bot + 10, INK, 1.6)
    o += T(X(xmax) + 18, top + 5, xlab, 15, INK, 'start')
    return o, X, Y


def fig3_1():
    d = ex2015_2()
    W_, H = 900, 430
    top, bot = 60, 380
    o, X, Y = _depth_axes('', 160, 420, top, bot, 4.2, -35, 35, [-30, -15, 0, 15, 30], 'σ_{a}（kPa）', [0, 1, 2, 3, 4])
    o += T(40, bot + 30, '深度 *z*（m）', 14, INK, 'start')
    s = lambda z: d['Ka1'] * d['g1'] * z + d['s0']
    o += P([(X(0), Y(0)), (X(s(0)), Y(0)), (X(0), Y(d['zc']))], None, fill=WARN2, close=True)
    o += P([(X(s(0)), Y(0)), (X(s(4)), Y(4))], WARN, 2, dash='6 4')
    o += P([(X(0), Y(d['zc'])), (X(s(4)), Y(4)), (X(0), Y(4))], TEN, 2.6, fill=TENM, close=True)
    o += T(X(s(0)) - 6, Y(0) + 22, f"{d['s0']:.2f}", 14, WARN, 'end', 'bold')
    o += T(X(-22), Y(2.5), '負值：土要「拉」牆', 15, WARN, 'middle', 'bold')
    o += T(X(-22), Y(2.95), '→ 開裂，歸零', 15, WARN, 'middle', 'bold')
    o += L(X(-35), Y(d['zc']), X(35), Y(d['zc']), COMP, 1.6, '6 4')
    o += T(X(35), Y(d['zc']) - 8, f"*z*_{{c}} = {d['zc']:.3f} m", 15, COMP, 'end', 'bold')
    o += T(X(s(4)) + 8, Y(4) - 4, f"{d['s4a']:.2f}", 14, TEN, 'start', 'bold')
    # crack water
    o += P([(X(0), Y(0)), (X(0), Y(d['zc'])), (X(GW * d['zc']), Y(d['zc']))], AC, 2, dash='4 3')
    o += T(X(GW * d['zc'] / 2) + 30, Y(d['zc'] * 0.55), '裂縫積水（若有）', 14, AC, 'start', 'bold')
    o += R(640, 70, 250, 190, KEY2, KEY, 1.4, 8)
    o += T(765, 98, '2015-2 上層黏土', 15, KEY, 'middle', 'bold')
    o += T(765, 126, '*c* = 20、φ = 20°、γ = 17.5', 14, INK, 'middle')
    o += T(765, 154, f"*K*_{{a}} = {d['Ka1']:.4f}", 15, INK, 'middle')
    o += T(765, 182, '2*c*√*K*_{a} = 28.01', 15, WARN, 'middle')
    o += T(765, 214, '*z*_{c} = 2*c*/(γ√*K*_{a})', 15, COMP, 'middle', 'bold')
    o += T(765, 244, f"積水推力 ½γ_{{w}}*z*_{{c}}² = {d['Pw_crack']:.2f}", 14, AC, 'middle')
    return svg(W_, H, o, '含凝聚力的主動土壓與張力裂縫')


def fig3_2():
    W_, H = 900, 470
    Su, g, Hm = 30.0, 17.5, 8.0
    top, bot = 60, 370
    o, X, Y = _depth_axes('', 140, 560, top, bot, Hm, -70, 220, [-60, 0, 60, 120, 180], 'σ（kPa）', [0, 2, 4, 6, 8])
    o += T(30, bot + 70, '深度 *z*（m）', 14, INK, 'start')
    zc = 2 * Su / g
    o += P([(X(0), Y(0)), (X(-2 * Su), Y(0)), (X(0), Y(zc))], None, fill=WARN2, close=True)
    o += P([(X(0), Y(zc)), (X(g * Hm - 2 * Su), Y(Hm)), (X(0), Y(Hm))], TEN, 2.6, fill=TENM, close=True)
    o += P([(X(2 * Su), Y(0)), (X(g * Hm + 2 * Su), Y(Hm))], COMP, 3)
    o += P([(X(0), Y(0)), (X(g * Hm), Y(Hm))], MUT, 1.6, dash='5 4')
    o += T(X(g * Hm) + 6, Y(Hm) - 30, 'σ_{v}', 15, MUT, 'start')
    o += T(X(g * Hm - 2 * Su) - 8, Y(Hm) + 22, '主動 σ_{v} − 2*S*_{u}', 15, TEN, 'end', 'bold')
    o += T(X(g * Hm + 2 * Su) - 4, Y(Hm) + 22, '被動 σ_{v} + 2*S*_{u}', 15, COMP, 'end', 'bold')
    o += L(X(-70), Y(zc), X(0), Y(zc), WARN, 1.6, '5 4')
    o += T(X(-68), Y(zc) - 8, f'*z*_{{c}} = 2*S*_{{u}}/γ = {zc:.2f}', 14, WARN, 'start', 'bold')
    o += dim(X(g * Hm - 2 * Su), Y(Hm) + 40, X(g * Hm + 2 * Su), Y(Hm) + 40, '兩條線永遠差 4*S*_{u}', KEY, 0, 15, 1)
    o += T(X(160), Y(1.2), '（示意：*S*_{u} = 30、γ = 17.5）', 14, MUT, 'middle')
    return svg(W_, H, o, 'φ = 0 黏土的主被動土壓')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
