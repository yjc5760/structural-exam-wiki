# -*- coding: utf-8 -*-
"""第 12 章：超靜定——二次彎矩、C 線、同位鋼腱（RC-2024-4）。"""
from figs_ps import *  # noqa
from calcs import rc2024_4

Q = rc2024_4()


def fig12_1():
    W, H = 900, 430
    o = T(450, 26, 'RC-2024-4：等效載重放到受撐懸臂梁上——只有多餘支承 B 擋住變形，才長出反力', 16, INK, 'middle', 'bold')
    x0, x1, y = 130, 690, 200
    o += R(x0, y - 20, x1 - x0, 40, STEEL2, INK, 1.4)
    o += L(x0, y - 70, x0, y + 70, INK, 4)
    for i in range(8):
        o += L(x0, y - 70 + i * 20, x0 - 10, y - 60 + i * 20, INK, 1)
    o += P([(x1, y + 20), (x1 - 12, y + 40), (x1 + 12, y + 40)], INK, 1.5, fill='#fff', close=True)
    o += C(x1 - 6, y + 45, 4, '#fff', INK, 1.2) + C(x1 + 6, y + 45, 4, '#fff', INK, 1.2)
    o += L(x1 - 20, y + 50, x1 + 20, y + 50, INK, 1.5)
    for i in range(1, 15):
        xx = x0 + (x1 - x0) * i / 15
        o += A(xx, y + 70, xx, y + 24, COMP, 1.6, 8)
    o += T((x0 + x1) / 2, y + 96, f"跨內 *w* = −*Pe*″ = {Q['w']:.4f} tf/m 向上（合力 22.0 tf）", 14, COMP, 'middle', 'bold')
    o += A(x0 + 14, y - 80, x0 + 14, y - 24, KEY, 2.6, 11)
    o += T(x0 + 22, y - 84, f"錨碇 {Q['VA']:.1f} tf↓", 14, KEY, 'start', 'bold')
    o += A(x1 - 14, y - 80, x1 - 14, y - 24, KEY, 2.6, 11)
    o += T(x1 - 22, y - 84, f"錨碇 {Q['VB']:.1f} tf↓", 14, KEY, 'end', 'bold')
    import math
    pts = [(x0 + 40 + 26 * math.cos(t), y - 44 + 26 * math.sin(t)) for t in [math.pi * (1.0 - 1.4 * i / 30) for i in range(31)]]
    o += curve_arrow(pts, KEY, 2, 9)
    o += T(x0 + 76, y - 40, f"錨碇彎矩 {Q['MA']:.0f} tf·m", 14, KEY, 'start', 'bold')
    o += T(x0, y + 132, 'A（固定）：13.5 tf 與 30 tf·m 直接進支承，不使梁變形', 14, INK, 'start')
    o += T(x1, y + 156, f"B（輥）：*R*_{{B}} = 8.5（錨碇正上方）− 3*wL*/8 = 8.5 − 8.25 = {Q['RB']:.2f} tf ↑", 14, INK, 'end', 'bold')
    o += box(712, 70, 180, 160, '自平衡檢查', ['Σ*F* = 22.0 − 13.5', '− 8.5 = 0 ✔', 'Σ*M*_{A} = 132 − 102', '− 30 = 0 ✔'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '受撐懸臂等效載重')


def fig12_2():
    W, H = 900, 440
    o = T(450, 26, 'RC-2024-4：鋼腱（綠）、C 線（紫）；兩者只差 *M*_{2}/*P*，而 *M*_{2} 在支承間是直線', 16, INK, 'middle', 'bold')
    pl = Plot(110, 70, 510, 260, 0, 12, 30, -32)
    o += pl.axes([0, 3, 6, 9, 12], [-30, -20, -10, 0, 10, 20, 30], '*x*（m）', '*e*（cm，下為正）', yfmt=lambda v: f'{v:g}'.replace('-', '−'), size=14)
    o += pl.curve(Q['e'], 0, 12, TEN, 3, clip=False)
    o += pl.curve(Q['eC'], 0, 12, KEY, 3, dash='8 5', clip=False)
    o += pl.hline(0, 0, 12, INK, 1.2, None)
    o += pl.dot(0, Q['e'](0), TEN, 6); o += pl.dot(0, Q['eC'](0), KEY, 6)
    o += T(pl.X(1.2), pl.Y(-25) + 5, '← 鋼腱 −25', 14, TEN, 'start', 'bold')
    o += T(pl.X(0) + 12, pl.Y(Q['eC'](0)) - 4, '−27.5', 14, KEY, 'start', 'bold')
    o += pl.dot(6, 15, TEN, 6); o += pl.dot(6, Q['eC'](6), KEY, 6)
    o += T(pl.X(6), pl.Y(15) + 24, '+15', 14, TEN, 'middle', 'bold')
    o += T(pl.X(6), pl.Y(Q['eC'](6)) - 10, '+13.75', 14, KEY, 'middle', 'bold')
    o += pl.dot(3, 0, KEY, 6)
    o += T(pl.X(3) + 10, pl.Y(0) - 12, 'C 線穿過形心（*x* = 3）', 14, KEY, 'start', 'bold')
    o += box(710, 80, 180, 280, '三種彎矩', ['*M*_{1} = −*Pe*（主）', '*M*_{2} = *R*_{B}(*L* − *x*)', '　　= 0.25(12 − *x*)', '*M* = *M*_{1} + *M*_{2}', '', '*e*_{C} = *e* − *M*_{2}/*P*', 'A 端差 3.0/120', '= 2.5 cm'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'C 線')


ALL = {'fig12_1': fig12_1, 'fig12_2': fig12_2}
