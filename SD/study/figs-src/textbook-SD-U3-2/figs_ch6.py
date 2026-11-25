# -*- coding: utf-8 -*-
"""第 6 章：TMD。"""
from sdfig import *  # noqa
from calcs import tmd_response, TMD
import math


def fig6_1():
    W, H = 900, 380
    pl = Plot(90, 40, 480, 280, 0.7, 1.3, 0, 27)
    o = pl.axes([0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3], [0, 5, 10, 15, 20, 25], '*r* = ω/ω_{n}', '|*X*|/(*F*_{0}/*K*)', yfmt=lambda v: f'{v:g}', xfmt=lambda v: f'{v:g}')
    o += pl.curve(lambda r: min(tmd_response(r, with_tmd=False), 27), 0.7, 1.3, MUT, 2.4, n=600, dash='6 4')
    cols = {0.01: AC, 0.02: TEN, 0.05: COMP}
    for mu, c in cols.items():
        o += pl.curve(lambda r, mu=mu: tmd_response(r, mu=mu), 0.7, 1.3, c, 3, n=600)
    o += T(pl.X(1.0) + 8, pl.Y(25), '無 TMD（ξ = 2%）峰值 25', 14.5, MUT, 'start', 'bold')
    o += T(pl.X(1.17), pl.Y(11), 'μ = 1%：9.7', 14.5, AC, 'start', 'bold')
    o += T(pl.X(1.17), pl.Y(8.6), 'μ = 2%：7.7', 14.5, TEN, 'start', 'bold')
    o += T(pl.X(1.17), pl.Y(6.2), 'μ = 5%：5.4', 14.5, COMP, 'start', 'bold')
    o += box(600, 40, 290, 300, '最佳調頻（Den Hartog）', ['*f*_{opt} = ω_{d}/ω_{n} = 1/(1+μ)', 'ξ_{d,opt} = √(3μ/(8(1+μ)³))', f'μ = 1%：*f* = {TMD[0.01]["f"]:.3f}、ξ_{{d}} = {TMD[0.01]["xi"]*100:.1f}%', f'μ = 2%：*f* = {TMD[0.02]["f"]:.3f}、ξ_{{d}} = {TMD[0.02]["xi"]*100:.1f}%', f'μ = 5%：*f* = {TMD[0.05]["f"]:.3f}、ξ_{{d}} = {TMD[0.05]["xi"]*100:.1f}%', '一個高峰 → 兩個矮峰', '調偏了效果大打折扣'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'TMD 頻率反應')


def fig6_2():
    W, H = 900, 300
    o = T(450, 26, '無阻尼吸振器（2006-4）：*k*_{d}/*m*_{d} = ω² ⇒ 主結構不動', 15.5, INK, 'middle', 'bold')
    o += cart(150, 230, 170, 90, '*M*', AC, AC2, ks=True, cs=False, wall_x=60)
    o += R(470, 148, 110, 70, COMP2, COMP, 2, 6) + C(495, 224, 6, '#fff', INK, 1.5) + C(555, 224, 6, '#fff', INK, 1.5) + T(525, 190, '*m*_{d}', 20, COMP, 'middle', 'bold') + hatch_ground(320, 230, 300)
    o += spring(320, 183, 470, 183, n=6, amp=8, c=COMP)
    o += T(395, 168, '*k*_{d}', 15, COMP, 'middle', 'bold')
    o += A(160, 110, 230, 110, WARN, 2.4, 9) + T(160, 100, '*F*_{0}sinω*t*', 15, WARN, 'start', 'bold')
    o += A(390, 150, 326, 150, COMP, 2.4, 9) + T(330, 132, '作用在 *M* 的彈簧力 = −*F*_{0}sinω*t*', 14.5, COMP, 'start', 'bold')
    o += T(450, 280, '吸振器的彈簧力剛好抵銷外力；*X*_{0} = 0、*m*_{d} 振幅 = −*F*_{0}/*k*_{d}', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '無阻尼吸振器')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
