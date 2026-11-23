# -*- coding: utf-8 -*-
"""第 2 章：單位重母式（γ 隨 S 線性）、零空氣孔隙曲線。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig2_1():
    d = ex2004_1()
    e, Gs = d['e'], d['Gs']
    W_, H = 900, 380
    pl = Plot(100, 50, 480, 270, 0, 1, 8, 28)
    o = pl.axes([0, 0.25, 0.5, 0.75, 1.0], [8, 12, 16, 20, 24, 28], '*S*', 'γ（kN/m³）')
    o += pl.curve(lambda S: gamma(Gs, e, S), 0, 1, KEY, 3.2)
    o += pl.dot(0, d['gd'], AC, 6)
    o += T(pl.X(0) + 10, pl.Y(d['gd']) + 22, f"*S* = 0：γ_{{d}} = {d['gd']:.2f}", 14, AC, 'start', 'bold')
    o += pl.dot(1, d['gsat'], AC, 6)
    o += T(pl.X(1) - 8, pl.Y(d['gsat']) - 12, f"*S* = 1：γ_{{sat}} = {d['gsat']:.2f}", 14, AC, 'end', 'bold')
    o += pl.dot(d['S'], d['gt'], KEY, 6)
    o += T(pl.X(d['S']) - 10, pl.Y(d['gt']) + 26, f"*S* = {d['S'] * 100:.1f}%：γ_{{t}} = {d['gt']:.2f}", 14, KEY, 'end', 'bold')
    o += pl.hline(d['gp'], 0, 1, COMP, 1.6, '6 4')
    o += T(pl.X(0.5), pl.Y(d['gp']) + 22, f"γ′ = γ_{{sat}} − γ_{{w}} = {d['gp']:.2f}（水下）", 14, COMP, 'middle', 'bold')
    o += pl.hline(Gs * GW, 0, 1, MUT, 1.2, '3 3')
    o += T(pl.X(0.02), pl.Y(Gs * GW) - 8, f'上限 *G*_{{s}}γ_{{w}} = {Gs * GW:.1f}（*e* → 0）', 14, MUT, 'start')
    o += R(610, 70, 280, 170, KEY2, KEY, 1.4, 8)
    o += T(750, 98, '一條母式，四個特例', 15, KEY, 'middle', 'bold')
    o += T(750, 130, 'γ = (*G*_{s} + *Se*)γ_{w}/(1 + *e*)', 15, INK, 'middle')
    o += T(750, 160, '固定 *e*：γ 對 *S* 是直線', 15, INK, 'middle')
    o += T(750, 190, '左端 γ_{d}、右端 γ_{sat}', 15, INK, 'middle')
    o += T(750, 220, '（2004-1：*G*_{s} = 2.70、*e* = 0.538）', 14, MUT, 'middle')
    return svg(W_, H, o, '單位重隨飽和度變化')


def fig2_2():
    d = ex2004_1()
    Gs = d['Gs']
    W_, H = 900, 400
    pl = Plot(100, 50, 500, 280, 0.10, 0.26, 15, 21)
    o = pl.axes([0.10, 0.14, 0.18, 0.22, 0.26], [15, 16, 17, 18, 19, 20, 21], '*w*', 'γ_{d}', xfmt=lambda t: f'{t * 100:.0f}%')
    o += pl.curve(lambda w: zav(w, Gs), 0.10, 0.26, AC, 3.2)
    o += pl.curve(lambda w: gd_S(w, Gs, 0.95), 0.10, 0.26, MUT, 1.6, '6 4')
    o += pl.curve(lambda w: gd_S(w, Gs, 0.90266), 0.10, 0.26, MUT, 1.6, '3 3')
    o += T(pl.X(0.115), pl.Y(zav(0.115, Gs)) - 8, '*S* = 100%（零空氣孔隙）', 14, AC, 'start', 'bold')
    o += pl.dot(0.18, d['gd'], KEY, 6)
    o += pl.dot(0.18, d['gd2'], COMP, 6)
    o += pl.dot(0.18, d['gzav'], AC, 5)
    for k, (yv, txt, c) in enumerate([(d['gzav'], f"上限 {d['gzav']:.2f}（*S* = 100%）", AC),
                                      (d['gd2'], f"再夯 {d['gd2']:.2f}（*S* = 95%）", COMP),
                                      (d['gd'], f"夯實前 {d['gd']:.2f}（*S* = 90.3%）", KEY)]):
        ly = pl.Y(16.9 - k * 0.5)
        o += L(pl.X(0.18), pl.Y(yv), pl.X(0.105) + 215, ly - 5, c, 1, '2 2')
        o += T(pl.X(0.105), ly, txt, 14, c, 'start', 'bold')
    o += R(630, 80, 260, 150, KEY2, KEY, 1.4, 8)
    o += T(760, 108, '同一含水量往上夯', 15, KEY, 'middle', 'bold')
    o += T(760, 138, '只能沿鉛直線往上', 15, INK, 'middle')
    o += T(760, 166, '最多碰到 ZAV 就停', 15, INK, 'middle')
    o += T(760, 196, 'γ_{zav} = *G*_{s}γ_{w}/(1 + *wG*_{s})', 15, INK, 'middle')
    return svg(W_, H, o, '零空氣孔隙曲線與 2004-1')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
