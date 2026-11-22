# -*- coding: utf-8 -*-
"""第 1 章：一個 c 決定一切——應變線繞頂點轉、材料律與挖洞、對形心取矩。"""
from figs_col import *  # noqa
from calcs import demo, ES

R0 = demo(); D = R0['D']


def fig1_1():
    W, H = 900, 450
    o = T(450, 26, '應變直線繞著「頂緣 0.003」轉動：*c* 一變，每一層鋼筋的應變全部跟著變', 16, INK, 'middle', 'bold')
    sc = 6.5; y0 = 70
    xs = 160
    o += col_section(xs, y0, sc, D, [3, 2, 3])
    o += T(xs, y0 - 12, '示範柱 40×40', 15, INK, 'middle', 'bold')
    for d, _ in D.layers:
        o += L(xs + D.b * sc / 2, y0 + d * sc, 860, y0 + d * sc, GRID, 1, '3 3')
        o += T(xs + D.b * sc / 2 + 6, y0 + d * sc - 5, f'{d:g}', 14, MUT, 'start')
    xa = 560
    k = 70 / 0.003
    yb = y0 + D.h * sc
    o += L(xa, y0 - 10, xa, yb + 10, MUT, 1.4, '4 3')
    o += T(xa, yb + 30, 'ε = 0', 14, MUT, 'middle')
    cases = [(R0['c0'], TEN, '純彎'), (R0['cb'], KEY, '平衡'), (32.0, COMP, 'ε_{t} = 0'), (80.0, AC, '*c* = 80')]
    xt = xa - k * 0.003
    for c, col, lab in cases:
        ebot = -0.003 * (c - D.h) / c
        xb = xa - k * (0.003 * (c - D.h) / c)
        o += L(xt, y0, xb, yb, col, 2.6)
        o += T(xb + (8 if xb > xa else -8), yb + (16 if lab != '*c* = 80' else 16), lab, 14, col, 'start' if xb > xa else 'end', 'bold')
    o += C(xt, y0, 7, KEY2, KEY, 2.4)
    o += T(xt - 10, y0 - 10, '0.003（轉軸）', 15, COMP, 'end', 'bold')
    o += T(xa - 110, yb + 30, '← 壓', 14, COMP, 'middle', 'bold')
    o += T(xa + 140, yb + 30, '拉 →', 14, TEN, 'middle', 'bold')
    o += box(690, 60, 200, 150, '相似三角形', ['ε_{si} / (*c* − *d*_{i})', '= 0.003 / *c*', '一個 *c* → 每一層', '應變全部確定'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '應變線繞頂點轉')


def fig1_2():
    W, H = 900, 420
    o = T(225, 26, '(a) 鋼筋：拉、壓都是先斜後平', 16, INK, 'middle', 'bold')
    o += T(675, 26, '(b) 壓力區的鋼筋要「挖洞」', 16, INK, 'middle', 'bold')
    ey = D.ey
    pl = Plot(70, 60, 320, 280, -0.006, 0.006, -5200, 5200)
    o += pl.axes([-0.006, -ey, 0, ey, 0.006], [-4200, 0, 4200], 'ε', '*f*_{s}',
                 xfmt=lambda v: {0: '0', ey: 'ε_{y}', -ey: '−ε_{y}'}.get(v, ''), yfmt=lambda v: {4200: '*f*_{y}', -4200: '−*f*_{y}'}.get(v, '0'))
    o += P([pl.pt(-0.006, -4200), pl.pt(-ey, -4200), pl.pt(ey, 4200), pl.pt(0.006, 4200)], INK, 3.2)
    o += T(pl.X(0.0035), pl.Y(4200) - 12, '壓（正）', 14, COMP, 'middle', 'bold')
    o += T(pl.X(-0.0035), pl.Y(-4200) + 26, '拉（負）', 14, TEN, 'middle', 'bold')
    o += T(pl.X(0.0012), pl.Y(1500), '*E*_{s}ε', 14, INK, 'start')
    o += T(230, 398, 'ε_{y} = 4200/2.04×10^{6} = 0.002059', 15, INK, 'middle', 'bold')
    # (b) 挖洞
    x0, y0, sc = 520, 70, 7.5
    a = 27.2
    o += R(x0, y0, 40 * sc / 2.2, 40 * sc * 0.75, STEEL2, INK, 1.4)
    wb = 40 * sc / 2.2
    o += R(x0, y0, wb, a * sc * 0.75, WARN2, WARN, 1.6, op=0.9)
    yb = y0 + 8 * sc * 0.75
    o += C(x0 + wb / 2, yb, 11, COMP, '#fff', 1.4)
    o += T(x0 + wb + 12, y0 + 20, '應力塊 0.85*f*′_{c}×*a*×*b*', 14, WARN, 'start', 'bold')
    o += T(x0 + wb + 12, y0 + 40, '（已把鋼筋那一小塊算進去）', 14, MUT, 'start')
    o += A(x0 + wb + 110, yb + 40, x0 + wb / 2 + 12, yb + 6, COMP, 2, 10)
    o += T(x0 + wb + 114, yb + 46, '這根鋼筋占的面積', 14, COMP, 'start', 'bold')
    o += box(x0 - 10, 250, 370, 110, '同一個位置不能算兩次', ['淨力 = *A*_{s}(*f*_{s} − 0.85*f*′_{c})', f'#8 降伏：5.07×(4200 − 238) = {5.07*(4200-238)/1000:.2f} tf/根', '只在鋼筋落在 *a* 以內且受壓時才扣'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '材料律與挖洞')


def fig1_3():
    s = R0['s32']
    return tri_panel(D, s, [3, 2, 3], f"示範柱在 *c* = 32 cm（RC-2024-3：拉力筋應變為零）",
                     H=450, note=f"*P*_{{n}} = {tf(s['P']):.2f} tf　*M*_{{n}} = {tfm(s['M']):.2f} tf·m　*e* = {s['e']:.2f} cm")


def fig1_4():
    W, H = 900, 380
    s = R0['s32']
    o = T(450, 26, '偏心的軸力 ＝ 形心上的軸力 ＋ 一個彎矩 *P*·*e*（柱的立面）', 16, INK, 'middle', 'bold')
    sc = 4.0
    def column(xc, lab):
        oo = R(xc - 20 * sc, 90, 40 * sc, 220, STEEL2, INK, 1.4)
        oo += L(xc, 80, xc, 320, KEY, 1.4, '4 3')
        oo += T(xc, 345, lab, 15, INK, 'middle', 'bold')
        return oo
    x1 = 190
    o += column(x1, '(a) 軸力作用在偏心 *e*')
    xp = x1 - s['e'] * sc
    o += A(xp, 40, xp, 88, COMP, 3, 12)
    o += T(xp - 8, 58, '*P*_{n}', 16, COMP, 'end', 'bold')
    o += hdim(xp, x1, 74, '', INK, -1)
    o += T((xp + x1) / 2 + 30, 70, f"*e* = {s['e']:.2f}", 14, INK, 'start')
    o += T(x1 - 20 * sc + 4, 110, '壓力面', 14, COMP, 'start')
    o += T(450, 200, '＝', 30, INK, 'middle', 'bold')
    x2 = 650
    o += column(x2, '(b) 形心上的 *P*_{n} ＋ *M*_{n} = *P*_{n}*e*')
    o += A(x2, 40, x2, 88, COMP, 3, 12)
    o += T(x2 + 8, 58, '*P*_{n}', 16, COMP, 'start', 'bold')
    import math as _m
    pts = [(x2 + 70 * _m.cos(t), 150 + 40 * _m.sin(t)) for t in [(-0.2 - 2.6 * i / 30) for i in range(31)]]
    o += curve_arrow(pts, KEY, 2.4, 11)
    o += T(x2 + 100, 140, '*M*_{n}', 16, KEY, 'start', 'bold')
    o += T(450, 372, f"示範柱 *c* = 32：*M*_{{n}} = {tf(s['P']):.2f} × {s['e']:.2f} / 100 = {tfm(s['M']):.2f} tf·m", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '對形心取矩')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
