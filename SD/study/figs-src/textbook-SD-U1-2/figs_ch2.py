# -*- coding: utf-8 -*-
"""第 2 章：轉動慣量、剛性桿 2DOF、倒擺。"""
from sdfig import *  # noqa
from calcs import inv_pend_V, Q2024_2
import math


def fig2_1():
    W, H = 900, 300
    o = ''
    items = [('細桿繞中心', '*mL*²/12'), ('細桿繞端點', '*mL*²/3'), ('矩形板繞中心', '*m*(*a*²+*b*²)/12'), ('平行軸', '*I*_{O} = *I*_{G} + *md*²')]
    for i, (t, f_) in enumerate(items):
        x0 = 20 + i * 220
        o += T(x0 + 100, 30, t, 15.5, INK, 'middle', 'bold')
        cy = 140
        if i == 0:
            o += L(x0 + 20, cy, x0 + 180, cy, STEEL, 9) + C(x0 + 100, cy, 6, KEY, '#fff', 2)
            o += curve_arrow([(x0 + 100 + 30 * math.cos(a), cy - 30 * math.sin(a)) for a in [math.radians(d) for d in range(30, 160, 10)]], KEY, 1.8)
        elif i == 1:
            o += L(x0 + 20, cy, x0 + 180, cy, STEEL, 9) + C(x0 + 20, cy, 6, KEY, '#fff', 2)
            o += curve_arrow([(x0 + 20 + 30 * math.cos(a), cy - 30 * math.sin(a)) for a in [math.radians(d) for d in range(10, 150, 10)]], KEY, 1.8)
        elif i == 2:
            o += R(x0 + 40, cy - 45, 120, 90, STEEL2, STEEL, 2, 2) + C(x0 + 100, cy, 6, KEY, '#fff', 2)
            o += T(x0 + 100, cy + 68, '*a*', 15, MUT, 'middle') + T(x0 + 172, cy + 5, '*b*', 15, MUT, 'start')
        else:
            o += C(x0 + 60, cy + 20, 26, STEEL2, STEEL, 2) + C(x0 + 60, cy + 20, 4, INK, INK, 1)
            o += C(x0 + 150, cy - 30, 6, KEY, '#fff', 2)
            o += L(x0 + 60, cy + 20, x0 + 150, cy - 30, MUT, 1.3, '4 3')
            o += T(x0 + 112, cy - 12, '*d*', 15, MUT, 'start') + T(x0 + 60, cy + 66, 'G', 15, INK, 'middle') + T(x0 + 160, cy - 40, 'O', 15, KEY, 'start')
        o += R(x0 + 10, 220, 180, 40, KEY2, KEY, 1.4, 8) + T(x0 + 100, 246, f_, 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '常用轉動慣量')


def fig2_2():
    W, H = 900, 380
    o = T(160, 30, '倒擺＋水平彈簧（2010-1）', 16, INK, 'middle', 'bold')
    bx, by, Lp = 150, 320, 220
    th = math.radians(14)
    o += pin(bx, by)
    xa, ya = bx + Lp * math.sin(th), by - Lp * math.cos(th)
    o += L(bx, by, bx, by - Lp - 20, GRID, 1.4, '5 4')
    o += L(bx, by, xa, ya, STEEL, 7) + C(xa, ya, 16, AC2, AC, 2.4) + T(xa, ya + 6, '*m*', 16, AC, 'middle', 'bold')
    o += spring(xa + 16, ya, 300, ya) + L(300, ya - 25, 300, ya + 25, INK, 3)
    o += A(xa, ya + 20, xa, ya + 70, COMP, 2.4, 10) + T(xa + 8, ya + 62, '*mg*', 15, COMP, 'start', 'bold')
    o += T(bx + 20, by - 60, 'θ', 16, KEY, 'start', italic=True)
    o += T(260, ya - 18, '*k*', 15, INK, 'middle')
    o += T(bx - 20, by - Lp / 2, '*L*', 15, MUT, 'end')
    pl = Plot(420, 60, 300, 250, -0.6, 0.6, 0.85, 1.12)
    o += pl.axes([-0.6, -0.3, 0, 0.3, 0.6], [0.9, 1.0, 1.1], 'θ', '*V*/(*mgL*)', yfmt=lambda t: f'{t:.1f}')
    for r, c in ((1.6, TEN), (1.0, KEY), (0.55, COMP)):
        o += pl.curve(lambda t, r=r: inv_pend_V(t, r), -0.6, 0.6, c, 2.6)
    o += T(pl.X(0.22), pl.Y(1.10), '*r* = 1.6：谷（穩定）', 14, TEN, 'middle', 'bold')
    o += T(pl.X(0.0), pl.Y(1.02) - 4, '*r* = 1：平', 14, KEY, 'middle', 'bold')
    o += T(pl.X(0.22), pl.Y(0.875), '*r* = 0.55：峰（倒）', 14, COMP, 'middle', 'bold')
    o += box(735, 60, 155, 260, '*r* = *kL*/(*mg*)', ['*V* = *mgL* cos θ', '+ ½*k*(*L* sin θ)²', '曲率 = *kL*² − *mgL*', '重力給', '「負勁度」', '*k* > *mg*/*L*', '才穩定'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '倒擺與位能')


def fig2_3():
    W, H = 900, 330
    o = T(300, 30, '剛性桿（均勻質量 *m*、長 *L*）＋兩端彈簧（2024-2）', 16, INK, 'middle', 'bold')
    x1, x2, y0 = 120, 520, 200
    u1, u2 = 30, -45
    o += L(x1, y0, x2, y0, GRID, 1.4, '5 4')
    o += L(x1, y0 - u1, x2, y0 - u2, STEEL, 9)
    for x, u, k in ((x1, u1, '*k*_{1}'), (x2, u2, '*k*_{2}')):
        o += spring(x, y0 + 100, x, y0 - u, n=5, amp=8) + hatch_ground(x - 25, y0 + 100, 50)
        o += T(x + 16, y0 + 60, k, 15, INK, 'start')
    o += A(x1 - 40, y0, x1 - 40, y0 - u1, KEY, 2, 9) + T(x1 - 46, y0 - u1 / 2 + 5, '*u*_{1}', 15, KEY, 'end', 'bold')
    o += A(x2 + 40, y0, x2 + 40, y0 - u2, KEY, 2, 9) + T(x2 + 46, y0 - u2 / 2 + 5, '*u*_{2}', 15, KEY, 'start', 'bold')
    xm, ym = (x1 + x2) / 2, y0 - (u1 + u2) / 2
    o += C(xm, ym, 6, AC, '#fff', 2) + T(xm - 40, ym - 34, 'G：*v̄* = (*u*_{1}+*u*_{2})/2', 15, AC, 'middle', 'bold')
    o += T(xm + 20, ym + 70, 'θ = (*u*_{2}−*u*_{1})/*L*', 15, AC, 'start', 'bold')
    o += A(xm + 60, ym - 70, xm + 60, ym - 32, COMP, 2.4, 10) + T(xm + 68, ym - 56, '*p*_{t}', 15, COMP, 'start', 'bold')
    o += box(640, 60, 250, 240, '動能 → 質量矩陣', ['*T* = ½*mv̄*² + ½(*mL*²/12)θ̇²', '= (*m*/6)(*u̇*_{1}² + *u̇*_{1}*u̇*_{2} + *u̇*_{2}²)', '*M* = (*m*/6)[2 1; 1 2]', f'（calcs 驗算 *M*_{{11}} = {Q2024_2["M"][0,0]:.4f}*m*）', '非對角項 *m*/6：', '一端動，另一端', '也被慣性拖著'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '剛性桿兩自由度')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
