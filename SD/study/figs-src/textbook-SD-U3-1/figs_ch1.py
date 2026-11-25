# -*- coding: utf-8 -*-
"""第 1 章：短柱、柱剪力、懸臂梁法。"""
from sdfig import *  # noqa
from calcs import V17, H17, CM
import math


def fig1_1():
    W, H = 900, 400
    o = T(300, 26, '2017-3：剛性梁、四根同 *EI* 柱、不同高度的窗台牆', 15.5, INK, 'middle', 'bold')
    xs = [80, 230, 380, 530]; yb, yt = 330, 110
    lh = yb - yt
    o += hatch_ground(50, yb, 520)
    o += R(60, yt - 22, 500, 22, STEEL3, INK, 1.4) + A(560, yt - 11, 620, yt - 11, COMP, 2.6, 11) + T(626, yt - 6, '*V*', 16, COMP, 'start', 'bold')
    walls = [(0, 1, 0.5), (1, 2, 0.25)]
    for a, b, hw in walls:
        o += R(xs[a] + 6, yb - lh * hw, xs[b] - xs[a] - 12, lh * hw, '#d7ccc8', '#8d6e63', 1.2)
    o += T((xs[0] + xs[1]) / 2, yb - lh * 0.25 + 5, '牆 ℓ/2', 14, '#5d4037', 'middle')
    o += T((xs[1] + xs[2]) / 2, yb - lh * 0.125 + 5, 'ℓ/4', 14, '#5d4037', 'middle')
    for i, x in enumerate(xs):
        heff = H17[i + 1]
        o += L(x, yb, x, yt, STEEL, 6)
        o += L(x, yt, x, yt + lh * heff, COMP, 6)
        o += T(x, yb + 24, f'{i+1}', 15, INK, 'middle', 'bold')
        o += T(x + 10, yt + lh * heff / 2, f'{heff:g}ℓ', 14, COMP, 'start', 'bold')
    o += T(300, 380, '紅色＝有效柱高（從牆頂量到梁底）', 14, COMP, 'middle')
    for i in range(4):
        y = 120 + i * 50
        v = V17[i + 1]
        o += T(690, y + 18, f'柱 {i+1}', 14, INK, 'end')
        o += R(700, y, v * 330, 26, COMP, None, 0, 4, op=0.85)
        o += T(706 + v * 330, y + 19, f'{v:.3f}*V*', 14, COMP, 'start', 'bold')
    o += T(780, 90, '剪力分配', 15.5, KEY, 'middle', 'bold')
    o += T(780, 345, '*k* ∝ 1/*h*³：8、8、2.37、1', 14, KEY, 'middle')
    return svg(W, H, o, '短柱與剪力分配')


def fig1_2():
    W, H = 900, 370
    o = T(170, 26, '柱的自由體圖', 15.5, INK, 'middle', 'bold')
    x0, yt, yb = 160, 70, 290
    o += L(x0, yb, x0, yt, STEEL, 8)
    o += curve_arrow([(x0 + 26 * math.cos(a), yt - 26 * math.sin(a)) for a in [math.radians(d) for d in range(210, 340, 10)]], KEY, 2)
    o += curve_arrow([(x0 + 26 * math.cos(a), yb - 26 * math.sin(a)) for a in [math.radians(d) for d in range(30, 160, 10)]], KEY, 2)
    o += T(x0 + 34, yt + 6, '*M*_{top}', 15, KEY, 'start', 'bold') + T(x0 + 34, yb - 22, '*M*_{bot}', 15, KEY, 'start', 'bold')
    o += A(x0 - 60, yt, x0 - 6, yt, COMP, 2.6, 11) + A(x0 + 6, yb, x0 + 60, yb, COMP, 2.6, 11)
    o += T(x0 - 64, yt + 5, '*V*', 15, COMP, 'end', 'bold') + T(x0 + 64, yb + 26, '*V*', 15, COMP, 'start', 'bold')
    o += dim(x0 - 90, yb, x0 - 90, yt, '*h*', MUT)
    o += T(170, 355, '對柱底取力矩：*Vh* = *M*_{top} + *M*_{bot}', 14.5, INK, 'middle', 'bold')
    pl = Plot(400, 40, 300, 250, 0.2, 1.0, 0, 6)
    o += pl.axes([0.25, 0.5, 0.75, 1.0], [0, 2, 4, 6], '*h*_{eff}/*h*', '*V*', grid=False)
    o += pl.curve(lambda r: 2 / r, 0.34, 1.0, COMP, 3)
    o += pl.hline(3.4, c=TEN, dash=None, w=2.6)
    o += T(pl.X(0.62), pl.Y(5.3), '彎矩降伏時的剪力 2*M*_{p}/*h*_{eff}', 14, COMP, 'middle', 'bold')
    o += T(pl.X(0.98), pl.Y(3.4) - 8, '剪力強度 *V*_{n}', 14, TEN, 'end', 'bold')
    rx = 2 / 3.4
    o += pl.dot(rx, 3.4, KEY, 6) + pl.vline(rx, 0, 3.4, KEY)
    o += T(pl.X(rx) - 8, pl.Y(0.6), '短於此 → 剪力先破壞', 14, KEY, 'end', 'bold')
    o += box(720, 50, 170, 240, '短柱', ['*h*_{eff} 變一半', '勁度 × 8', '分到更多力', '撓曲降伏所需', '剪力 × 2', '→ 剪力脆性破壞'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '柱剪力與短柱')


def fig1_3():
    W, H = 900, 360
    o = T(300, 26, '懸臂梁法（2015-4）：單層兩跨、*P* = 20 tf', 15.5, INK, 'middle', 'bold')
    sc = 23; x0 = 120; yb, yt = 300, 150
    xs = [x0 + x * sc for x in CM['x']]
    o += L(xs[0], yt, xs[2], yt, STEEL3, 7)
    for i, x in enumerate(xs):
        o += fixed_wall(x, yb, 40) + L(x, yb, x, yt, STEEL, 6)
        o += C(x, (yb + yt) / 2, 5, '#fff', KEY, 2)
        n = CM['N'][i]
        L_ = abs(n) * 22
        if n < 0:
            o += A(x + 14, yb - 30, x + 14, yb - 30 - L_, AC, 2.4, 9)
        else:
            o += A(x + 14, yb - 30 - L_, x + 14, yb - 30, COMP, 2.4, 9)
        o += T(x + 20, yb - 30 - L_ / 2 + 5, f'{n:+.2f}', 14, AC if n < 0 else COMP, 'start', 'bold')
    for xm, Lm in ((xs[0] + 7 * sc / 2, 7), (xs[1] + 10 * sc / 2, 10)):
        o += C(xm, yt, 5, '#fff', KEY, 2)
    o += A(xs[0] - 60, yt, xs[0] - 6, yt, COMP, 2.8, 11) + T(xs[0] - 64, yt - 8, '20 tf', 14, COMP, 'end', 'bold')
    xb = x0 + CM['xbar'] * sc
    o += L(xb, yt - 40, xb, yb + 20, KEY, 1.4, '5 4') + T(xb, yt - 46, f'x̄ = {CM["xbar"]:.0f} m', 14, KEY, 'middle', 'bold')
    o += T(300, 340, '白圈＝反曲點（柱、梁中點）；箭頭＝柱軸力（tf，負為拉）', 14, MUT, 'middle')
    o += box(600, 50, 290, 280, '三個假設、三步', ['① 反曲點在柱、梁中點', '② 柱軸力 ∝ 距形心距離', '③ 反曲點以上 *M* = 20 × 2 = 40', 'Σ*d*² = 64 + 1 + 81 = 146', '*N*_{i} = 40*d*_{i}/146', f'梁剪力 {CM["Vb"][0]:.2f}、{CM["Vb"][1]:.2f}', f'梁端 *M* {CM["Mb"][0]:.2f}、{CM["Mb"][1]:.2f}', f'柱剪力 {CM["Vc"][0]:.2f}、{CM["Vc"][1]:.2f}、{CM["Vc"][2]:.2f}', '和 = 20 ✔'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '懸臂梁法')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
