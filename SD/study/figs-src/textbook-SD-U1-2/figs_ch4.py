# -*- coding: utf-8 -*-
"""第 4 章：影響向量、電梯、路面。"""
from sdfig import *  # noqa
from calcs import elevator, PI
import math


def fig4_1():
    W, H = 900, 390
    o = T(150, 28, '(a) 剪力屋：地面平移 1', 15.5, INK, 'middle', 'bold')
    s, pts = shear_building(80, 320, 3, bw=110, sh=80, disp=[30, 30, 30])
    o += s
    o += A(70, 345, 110, 345, WARN, 2.4, 10) + T(116, 350, '*u*_{g} = 1', 15, WARN, 'start', 'bold')
    for i, (x, y) in enumerate(pts):
        o += T(x + 80, y + 5, '1', 15, KEY, 'start', 'bold')
    o += T(150, 380, 'ι = {1, 1, 1}', 16, KEY, 'middle', 'bold')
    o += L(300, 20, 300, 380, GRID, 1.5)
    o += T(450, 28, '(b) 剛性樓版：沿對角線', 15.5, INK, 'middle', 'bold')
    cx, cy, a = 450, 200, 150
    o += R(cx - a / 2, cy - a / 2, a, a, STEEL2, STEEL, 2)
    for (x, y, nm) in ((cx - a / 2, cy + a / 2, 'D'), (cx + a / 2, cy - a / 2, 'B'), (cx - a / 2, cy - a / 2, 'A'), (cx + a / 2, cy + a / 2, 'C')):
        o += C(x, y, 5, INK, INK, 1) + T(x + (-10 if x < cx else 10), y + (18 if y > cy else -8), nm, 15, INK, 'end' if x < cx else 'start')
    o += A(cx - 40, cy + 40, cx + 40, cy - 40, WARN, 3, 12) + T(cx + 46, cy - 40, '地動 DB 方向', 14, WARN, 'start', 'bold')
    o += T(450, 330, '每個角點自由度取', 14.5, INK, 'middle') + T(450, 352, '單位向量在其方向的分量', 14.5, INK, 'middle')
    o += T(450, 380, 'e = (1/√2){1, 1, 1}（2003-4）', 15, KEY, 'middle', 'bold')
    o += L(600, 20, 600, 380, GRID, 1.5)
    o += T(750, 28, '(c) 地面轉動 θ_{g} = 1', 15.5, INK, 'middle', 'bold')
    bx, by = 680, 320
    o += hatch_ground(640, by, 220)
    th = math.radians(8)
    tops = [(bx, by - 220), (bx + 120, by - 220)]
    o += L(bx, by, bx, by - 220, GRID, 1.2, '5 4')
    o += L(bx, by, bx + 220 * math.sin(th), by - 220 * math.cos(th), STEEL, 6)
    o += L(bx + 220 * math.sin(th), by - 220 * math.cos(th), bx + 220 * math.sin(th) + 120, by - 220 * math.cos(th) - 120 * math.sin(th), STEEL, 6)
    o += C(bx + 220 * math.sin(th), by - 220 * math.cos(th), 9, AC2, AC, 2)
    o += T(bx - 10, by - 110, '*h*', 15, MUT, 'end')
    o += T(750, 352, '水平位移 = 高度 × 1', 14.5, INK, 'middle')
    o += T(750, 380, 'ι_{θ} = 各質量的高度（2004-4）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '影響向量')


def fig4_2():
    W, H = 900, 340
    pl = Plot(90, 40, 560, 250, 0, 3, 0, 3.2)
    o = pl.axes([0, 1, 2, 3], [0, 1, 2, 3], '*t*/*T*', '*u*/(*vT*)', grid=True)
    w = 2 * PI
    o += pl.curve(lambda t: t, 0, 3, MUT, 1.6, dash='6 4')
    o += pl.curve(lambda t: elevator(t, w, 1.0), 0, 3, AC, 2.8, n=400)
    o += T(pl.X(0.25), pl.Y(2.6), '彈簧上端 *vt*（虛線）', 15, MUT, 'start')
    o += T(pl.X(1.05), pl.Y(0.6), '電梯 *u* = *vt* − (*v*/ω) sin ω*t*', 15, AC, 'start', 'bold')
    o += box(665, 50, 225, 250, '2011-3 電梯', ['*mü* + *ku* = *kvt*', '（從靜平衡量，*mg* 消去）', '特解 *u*_{p} = *vt*', '靜止起動：*u̇*(0) = 0', '⇒ 齊次解補 −(*v*/ω) sin ω*t*', '速度在 0～2*v* 間振盪'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '電梯等速上升')


def fig4_3():
    W, H = 900, 300
    o = T(300, 28, '汽車等速 *v* 行經正弦路面（2011-2）', 16, INK, 'middle', 'bold')
    y0 = 220
    pts = [(40 + i * 5, y0 - 18 * math.sin(2 * PI * (i * 5) / 240)) for i in range(111)]
    o += P(pts, INK, 2)
    xc = 280
    yc = y0 - 18 * math.sin(2 * PI * (xc - 40) / 240)
    o += C(xc, yc - 8, 8, '#fff', INK, 1.8)
    o += spring(xc - 20, yc - 16, xc - 20, yc - 90, n=4, amp=7)
    o += L(xc + 20, yc - 16, xc + 20, yc - 40, INK, 1.8) + R(xc + 10, yc - 60, 20, 22, '#fff', INK, 1.6) + L(xc + 20, yc - 50, xc + 20, yc - 90, INK, 1.8)
    o += R(xc - 50, yc - 130, 100, 40, AC2, AC, 2, 5) + T(xc, yc - 104, '*m*', 16, AC, 'middle', 'bold')
    o += A(xc + 60, yc - 110, xc + 120, yc - 110, COMP, 2.4, 10) + T(xc + 126, yc - 105, '*v*', 16, COMP, 'start', 'bold')
    o += dim(40, y0 + 40, 280, y0 + 40, '*L*（波長）', MUT)
    o += box(600, 50, 290, 220, '外力頻率從路面來', ['*x* = *vt*：*u*_{g} = *u*_{g0} sin(2π*vt*/*L*)', '*ω̄* = 2π*v*/*L*', '共振：*ω̄* = ω_{n}', '*v*_{res} = ω_{n}*L*/(2π)', '相對座標右端 −*mü*_{g}', '絕對座標右端 *cu̇*_{g} + *ku*_{g}'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '路面激振')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
