# -*- coding: utf-8 -*-
"""第 5 章：振態正交、Rayleigh 商、Rayleigh 阻尼、三軸譜。"""
from sdfig import *  # noqa
from calcs import Q2016, Q2025, Q2023, SP, PI
import math


def fig5_1():
    W, H = 900, 400
    shapes = [((1, 2, 3), '第 1 振態', AC), ((-1, -1, 2), '第 2 振態', KEY), ((1, -1, 1), '第 3 振態', COMP)]
    o = ''
    yb, sh = 340, 85
    for j, (ph, name, c) in enumerate(shapes):
        x0 = 90 + j * 210
        o += T(x0 + 40, 30, name, 16, c, 'middle', 'bold')
        o += L(x0 + 40, yb, x0 + 40, yb - 3 * sh, GRID, 1.5, '5 4')
        pts = [(x0 + 40, yb)] + [(x0 + 40 + 26 * ph[i], yb - (i + 1) * sh) for i in range(3)]
        o += P(pts, c, 2.8)
        for i in range(3):
            o += C(pts[i + 1][0], pts[i + 1][1], 9, c, '#fff', 2)
            o += T(pts[i + 1][0] + (16 if ph[i] >= 0 else -16), pts[i + 1][1] + 5, f'{ph[i]:+d}' if ph[i] else '0', 15, c, 'start' if ph[i] >= 0 else 'end', 'bold')
        o += hatch_ground(x0, yb, 80)
    o += T(30, yb - 3 * sh + 5, '1000', 15, INK, 'start') + T(30, yb - 2 * sh + 5, 'β', 16, INK, 'start', italic=True) + T(30, yb - sh + 5, 'α', 16, INK, 'start', italic=True)
    o += box(700, 50, 190, 300, '質量正交', ['φ_{1}^{T}*M*φ_{2} = 0：', '−α − 2β + 6000 = 0', 'φ_{1}^{T}*M*φ_{3} = 0：', 'α − 2β + 3000 = 0', '', f'α = {Q2016["alpha"]:.0f} kg', f'β = {Q2016["beta"]:.0f} kg'], KEY2, KEY, 16, 15)
    return svg(W, H, o, '三個振態與質量正交')


def fig5_2():
    W, H = 900, 330
    items = [('均勻 [1, 1]', Q2023['RQ_uni'], WARN), ('直線 [1, 2]', Q2023['RQ_lin'], KEY), ('重量當側力的靜變形', Q2023['RQ_w'], TEN), ('精確 ω_{1}', Q2023['w'][0], AC)]
    pl = Plot(300, 40, 420, 240, 2.5, 3.3, 0, 4)
    o = T(150, 30, '假設形狀', 16, INK, 'middle', 'bold')
    for i, (name, v, c) in enumerate(items):
        y = 70 + i * 60
        o += T(280, y + 26, name, 15, c, 'end', 'bold')
        o += R(300, y + 6, pl.X(v) - 300, 30, c, None, 0, 4, op=0.85)
        o += T(pl.X(v) + 8, y + 27, f'{v:.3f}', 15, c, 'start', 'bold')
    o += L(pl.X(Q2023['w'][0]), 60, pl.X(Q2023['w'][0]), 310, AC, 1.4, '5 4')
    o += T(300, 320, '橫軸起點 2.5 rad/s', 14, MUT, 'start')
    o += box(740, 60, 150, 200, '上界', ['任何形狀', '都 ≥ 精確值', '越像真振態', '越接近'], KEY2, KEY, 16, 15)
    return svg(W, H, o, 'Rayleigh 商的上界性質')


def fig5_3():
    W, H = 900, 380
    a0, a1 = Q2025['a0'], Q2025['a1']
    pl = Plot(90, 40, 560, 280, 0, 60, 0, 0.1)
    o = pl.axes([0, 10, 20, 30, 40, 50, 60], [0, 0.025, 0.05, 0.075, 0.1], 'ω (rad/s)', 'ξ', yfmt=lambda t: f'{t:.3f}')
    o += pl.curve(lambda w: a0 / (2 * w), 5.6, 60, TEN, 2, dash='6 4')
    o += pl.curve(lambda w: a1 * w / 2, 0, 60, AC, 2, dash='6 4')
    o += pl.curve(lambda w: a0 / (2 * w) + a1 * w / 2, 6.3, 60, KEY, 3)
    for w_, lab, c in ((Q2025['w'][0], 'ω_{1}', COMP), (Q2025['w'][1], 'ω_{2}', WARN), (Q2025['w'][2], 'ω_{3}', COMP)):
        z = a0 / (2 * w_) + a1 * w_ / 2
        o += pl.dot(w_, z, c, 6)
        o += T(pl.X(w_), pl.Y(z) + 26, f'{lab}: {z:.4f}', 15, c, 'middle', 'bold')
    o += T(pl.X(9), pl.Y(0.08), '質量項 *a*_{0}/2ω', 15, TEN, 'start', 'bold')
    o += T(pl.X(52), pl.Y(0.056), '勁度項 *a*_{1}ω/2', 15, AC, 'middle', 'bold')
    o += box(670, 60, 220, 250, '兩點夾住、中間下凹', [f'*a*_{{0}} = {a0:.3f} s^{{−1}}', f'*a*_{{1}} = {a1*1000:.3f}×10^{{−3}} s', f'ξ_{{2}} = {Q2025["z2"]:.4f}', '最低點 ω = √(ω_{1}ω_{3})', f'= {Q2025["wmin"]:.1f} rad/s', '兩點之外：阻尼偏大'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'Rayleigh 阻尼曲線')


def fig5_4():
    W, H = 900, 420
    # log-log：x = log10 T，y = log10 Sv
    pl = Plot(90, 40, 560, 320, -1.5, 1, -2, 0.5)
    o = pl.axes([-1, 0, 1], [-2, -1, 0], '*T* (s)', '*S*_{v} (m/s)', xfmt=lambda t: f'{10**t:g}', yfmt=lambda t: f'{10**t:g}')
    # 常數 Sd 線：Sv = 2π Sd / T → log Sv = log(2πSd) − log T（斜率 −1）
    def seg(c0, sl, col):
        xa = max(pl.xmin, (pl.ymin - c0) / sl if sl > 0 else (pl.ymax - c0) / sl)
        xb = min(pl.xmax, (pl.ymax - c0) / sl if sl > 0 else (pl.ymin - c0) / sl)
        if xb <= xa:
            return ''
        return L(pl.X(xa), pl.Y(c0 + sl * xa), pl.X(xb), pl.Y(c0 + sl * xb), col, 1.2, '5 4')
    for Sd in (0.001, 0.01, 0.1, 1.0):
        o += seg(math.log10(2 * PI * Sd), -1, AC)
    for Sa in (0.1, 1.0, 10.0):
        o += seg(math.log10(Sa / (2 * PI)), 1, COMP)
    # 一條示意譜：Sa 定值段（短週期）→ Sv 定值段 → Sd 定值段
    def spec(x):
        T_ = 10 ** x
        Sa = 2.5 * 9.81 * 0.4
        sv1 = Sa * T_ / (2 * PI)
        sv2 = SP['Sv']
        sv3 = 2 * PI * 0.35 / T_
        return math.log10(min(sv1, sv2, sv3))
    o += pl.curve(spec, -1.5, 1, KEY, 3.2)
    o += pl.dot(math.log10(SP['T']), math.log10(SP['Sv']), WARN, 6)
    o += T(pl.X(0) + 10, pl.Y(math.log10(SP['Sv'])) + 34, f'*T* = 1 s：*S*_{{v}} = {SP["Sv"]:.2f}', 14, WARN, 'start', 'bold')
    o += T(pl.X(-1.45), pl.Y(-1.55) + 2, '斜率 +1：*S*_{a} 定值', 15, COMP, 'start', 'bold')
    o += T(pl.X(0.95), pl.Y(-1.25), '斜率 −1：*S*_{d} 定值', 15, AC, 'end', 'bold')
    o += box(670, 60, 220, 260, '三軸一起讀', ['*S*_{v} = ω*S*_{d}', '*S*_{a} = ω*S*_{v} = ω²*S*_{d}', '紅虛線：等 *S*_{a}', '藍虛線：等 *S*_{d}', f'例 *T* = 1 s、0.5*g*：', f'*S*_{{d}} = {SP["Sd"]*100:.1f} cm', f'*S*_{{v}} = {SP["Sv"]*100:.0f} cm/s'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '三軸反應譜')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
