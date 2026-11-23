# -*- coding: utf-8 -*-
"""第 1 章：斜面上的磚、楔體幾何、凝聚力的份量。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def _rot(x, y, cx, cy, ang):
    a = math.radians(ang)
    return cx + (x - cx) * math.cos(a) + (y - cy) * math.sin(a), cy - (x - cx) * math.sin(a) + (y - cy) * math.cos(a)


def fig1_1():
    W_, H = 900, 430
    th = 30
    o = ''
    # incline from (60,380) up to right
    x0, y0, Lp = 60, 380, 520
    x1, y1 = x0 + Lp * math.cos(r(th)), y0 - Lp * math.sin(r(th))
    o += P([(x0, y0), (x1, y1), (x1, y0)], SOILE, 1.6, fill=SOIL, close=True)
    o += T(x0 + 70, y0 - 10, 'θ', 17, INK, 'middle', 'bold')
    # block centred at s=300 along slope
    s = 290
    cx, cy = x0 + s * math.cos(r(th)), y0 - s * math.sin(r(th))
    bw, bh = 110, 66
    pts = []
    for dx, dy in [(-bw / 2, 0), (bw / 2, 0), (bw / 2, -bh), (-bw / 2, -bh)]:
        px = cx + dx * math.cos(r(th)) + dy * math.sin(r(th))
        py = cy - dx * math.sin(r(th)) + dy * math.cos(r(th))
        pts.append((px, py))
    o += P(pts, INK, 1.8, fill=STEEL2, close=True)
    gx = cx - (bh / 2) * math.sin(r(th))
    gy = cy - (bh / 2) * math.cos(r(th))
    Lw = 130
    o += A(gx, gy, gx, gy + Lw, INK, 3, 12)
    o += T(gx + 10, gy + Lw + 4, '*W*', 17, INK, 'start', 'bold')
    # components
    ux, uy = -math.cos(r(th)), math.sin(r(th))   # down-slope
    nx, ny = math.sin(r(th)), math.cos(r(th))    # into slope
    ls, ln = Lw * math.sin(r(th)), Lw * math.cos(r(th))
    o += A(gx, gy, gx + ux * ls, gy + uy * ls, COMP, 3, 12)
    o += T(gx + ux * ls - 8, gy + uy * ls - 10, '*W* sin θ（推）', 16, COMP, 'end', 'bold')
    o += A(gx, gy, gx + nx * ln, gy + ny * ln, AC, 3, 12)
    o += T(gx + nx * ln + 10, gy + ny * ln + 4, '*W* cos θ（壓）', 16, AC, 'start', 'bold')
    o += L(gx + ux * ls, gy + uy * ls, gx, gy + Lw, MUT, 1, '4 3')
    o += L(gx + nx * ln, gy + ny * ln, gx, gy + Lw, MUT, 1, '4 3')
    # resisting along slope up at base
    bx, by = cx + 60 * math.cos(r(th)), cy - 60 * math.sin(r(th))
    o += A(bx, by + 12, bx + 80 * math.cos(r(th)), by + 12 - 80 * math.sin(r(th)), TEN, 3, 12)
    o += T(bx + 90 * math.cos(r(th)) + 6, by - 30 * math.sin(r(th)) - 40, '*cL* + *N* tan φ（拉住）', 16, TEN, 'start', 'bold')
    o += R(600, 270, 285, 120, KEY2, KEY, 1.4, 8)
    o += T(742, 300, 'FS = 抗力 ÷ 推力', 17, KEY, 'middle', 'bold')
    o += T(742, 334, '(*cL* + *W* cos θ tan φ)', 16, INK, 'middle')
    o += L(640, 344, 844, 344, INK, 1.2)
    o += T(742, 370, '*W* sin θ', 16, INK, 'middle')
    return svg(W_, H, o, '斜面上的磚：重量拆成推與壓')


def fig1_2():
    d = ex2023_2()
    W_, H = 900, 400
    sc = 34
    ox, oy = 120, 350
    X = lambda x: ox + x * sc
    Y = lambda y: oy - y * sc
    Hh = d['H']
    xt = Hh / tan(d['alpha'])        # 坡肩
    xf = Hh / tan(d['theta'])        # 破壞面頂
    o = ''
    o += P([(X(-3), Y(0)), (X(0), Y(0)), (X(xt), Y(Hh)), (X(16), Y(Hh)), (X(16), Y(-1.5)), (X(-3), Y(-1.5))], SOILE, 1.6, fill=SOIL, close=True)
    o += P([(X(0), Y(0)), (X(xt), Y(Hh)), (X(xf), Y(Hh))], COMP, 2.4, fill=COMP2, close=True)
    o += L(X(0), Y(0), X(xf), Y(Hh), COMP, 3)
    # centroid
    gx = (0 + xt + xf) / 3
    gy = (0 + Hh + Hh) / 3
    o += A(X(gx), Y(gy), X(gx), Y(gy) + 90, INK, 3, 12)
    o += T(X(gx) - 10, Y(gy) + 80, f"*W* = {d['W']:.2f}", 15, INK, 'end', 'bold')
    o += dim(X(xt), Y(Hh) - 22, X(xf), Y(Hh) - 22, f"*b* = {d['b']:.3f}", INK, 0, 15, -1)
    o += dim(X(14.6), Y(0), X(14.6), Y(Hh), '*H* = 8', INK, 0, 15, -1)
    o += T(X(xf * 0.72) + 14, Y(Hh * 0.72) + 26, f"*L* = {d['L']:.3f}", 15, COMP, 'start', 'bold')
    o += T(X(0) + 46, Y(0) - 10, '45°', 16, COMP, 'start', 'bold')
    o += T(X(0) + 18, Y(0) - 46, '60°', 16, INK, 'start', 'bold')
    o += R(640, 60, 245, 140, KEY2, KEY, 1.4, 8)
    o += T(762, 88, '楔體三步', 16, KEY, 'middle', 'bold')
    o += T(762, 116, '① *b* = *H*(cot θ − cot α)', 15, INK, 'middle')
    o += T(762, 144, '② *W* = ½*bH*γ', 15, INK, 'middle')
    o += T(762, 172, '③ *L* = *H*/sin θ', 15, INK, 'middle')
    return svg(W_, H, o, 'SM-2023-2 楔形滑動幾何')


def fig1_3():
    d = ex2023_2()
    W_, H = 900, 360
    pl = Plot(110, 40, 520, 260, 0, 2, 0, 800)
    o = pl.axes([], [0, 200, 400, 600, 800], '', 'kN/m')
    cL1, cL2, Nt = d['c1'] * d['L'], d['c2'] * d['L'], d['N'] * tan(d['phi'])
    for i, (cl, lab, fs) in enumerate([(cL1, '*c* = 50 kPa', d['FS1']), (cL2, '雨後 *c* = 5 kPa', d['FS2'])]):
        x = 0.5 + i
        x1, x2 = pl.X(x - 0.32), pl.X(x - 0.02)
        o += R(x1, pl.Y(Nt), x2 - x1, pl.Y(0) - pl.Y(Nt), ACM, AC, 1.2)
        o += R(x1, pl.Y(Nt + cl), x2 - x1, pl.Y(Nt) - pl.Y(Nt + cl), TENM, TEN, 1.2)
        x3, x4 = pl.X(x + 0.02), pl.X(x + 0.32)
        o += R(x3, pl.Y(d['T']), x4 - x3, pl.Y(0) - pl.Y(d['T']), COMPM, COMP, 1.2)
        o += T(pl.X(x), pl.Y(0) + 24, lab, 15, INK, 'middle', 'bold')
        o += T((x1 + x2) / 2, pl.Y(Nt + cl) - 8, f'抗 {Nt + cl:.1f}', 14, TEN, 'middle', 'bold')
        o += T((x3 + x4) / 2, pl.Y(d['T']) - 8, f"推 {d['T']:.1f}", 14, COMP, 'middle', 'bold')
        o += T(pl.X(x), pl.Y(760) + (0 if i == 0 else 0), f'FS = {fs:.2f}', 17, KEY, 'middle', 'bold')
    o += R(660, 70, 225, 150, KEY2, KEY, 1.4, 8)
    o += T(772, 98, '綠＝*cL*（凝聚力）', 15, TEN, 'middle', 'bold')
    o += T(772, 126, '藍＝*N* tan φ', 15, AC, 'middle', 'bold')
    o += T(772, 154, '紅＝*W* sin θ', 15, COMP, 'middle', 'bold')
    o += T(772, 186, f"晴天 *c* 佔抗力 {d['share_c1'] * 100:.0f}%", 15, INK, 'middle')
    return svg(W_, H, o, 'SM-2023-2 凝聚力在抗力中的份量')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
