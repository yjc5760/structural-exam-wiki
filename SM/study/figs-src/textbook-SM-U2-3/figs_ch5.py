# -*- coding: utf-8 -*-
"""第 5 章：隆起機制、Bjerrum–Eide Nc、圓弧力矩法。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig5_1():
    W, H = 900, 420
    o = ''
    xw, yg, yb = 450, 70, 190
    o += R(80, yg, xw - 80, 320, '#efe6d8', None, 0) + R(xw, yb, 380, 200, '#efe6d8', None, 0)
    o += L(80, yg, xw, yg, INK, 1.6) + L(xw, yb, 830, yb, INK, 1.6)
    o += L(xw, yg - 10, xw, yb + 40, STEEL, 6)
    o += T(100, yg - 10, '坑外', 15, INK) + T(820, yb - 10, '坑內', 15, INK, 'end')
    for k in range(5):
        x = 200 + k * 50
        o += A(x, yg - 40, x, yg - 4, TEN, 2.2, 10)
    o += T(300, yg - 46, '超載 *q*', 15, TEN, 'middle', 'bold')
    o += R(180, yg, 260, yb - yg, TEN2, TEN, 1.6, dash='6 4')
    o += T(310, (yg + yb) / 2 + 5, '土柱 *γH*', 15, TEN, 'middle', 'bold')
    for k in range(4):
        x = 210 + k * 70
        o += A(x, yb - 10, x, yb + 30, TEN, 2.6, 11)
    # 滑動面：從坑外 180 向下彎到坑內
    cx, cy, Rr = xw, yb, 270
    pts = [(cx + Rr * math.cos(t), cy + Rr * math.sin(t) * 0.62) for t in [math.pi - i * math.pi / 60 for i in range(61)]]
    o += P(pts, COMP, 2.6, dash='8 5')
    for x in (560, 640, 720):
        o += A(x, yb + 30, x, yb - 18, COMP, 2.6, 11)
    o += T(650, yb - 26, '隆起', 15, COMP, 'middle', 'bold')
    o += T(cx, cy + Rr * 0.62 + 24, '滑動面上抵抗 *S*_{u}', 15, COMP, 'middle', 'bold')
    o += box(600, 10, 280, 100, '倒過來的基礎', ['*FS*=*N*_{c}*S*_{u}/(*γH*+*q*)', '*N*_{c}=*π*+2（Prandtl）'], KEY2, KEY)
    return svg(W, H, o, '隆起機制')


def fig5_2():
    d = ex2015_3()
    W, H = 900, 420
    pl = Plot(90, 50, 560, 300, 0, 3, 4.5, 10)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [5, 6, 7, 8, 9, 10], '*D*/*B*', '*N*_{c}')
    for bl, c in ((0.0, AC), (0.4, KEY), (1.0, COMP)):
        cap = 7.5 * (1 + 0.2 * bl)
        o += pl.curve(lambda x: min(5 * (1 + 0.2 * bl) * (1 + 0.2 * x), cap), 0, 3, c, 2.6)
        o += pl.hline(cap, 0, 3, c, 1.2)
        o += T(pl.X(2.95), pl.Y(cap) - 6, f'*B*/*L*={bl:g}', 14, c, 'end', 'bold')
    db = d['H'] / d['B']
    o += pl.dot(db, d['Nc'], KEY, 7)
    o += T(pl.X(db) + 10, pl.Y(d['Nc']) + 22, f"2015-3：*N*_{{c}}={d['Nc']:.2f}", 15, KEY, 'start', 'bold')
    o += pl.hline(5.14, 0, 3, MUT, 1.2, '3 3') + T(pl.X(0.05), pl.Y(5.14) + 18, '二維 5.14', 14, MUT, 'start')
    o += box(670, 70, 215, 160, '本例', [f"*N*_{{c}}={d['Nc']:.2f}（上限 {d['Nc_max']:.1f}）", f"*FS*={d['FS']:.2f}", f"用二維：{d['FS_2D']:.2f}", '差 33%'], KEY2, KEY)
    return svg(W, H, o, 'Bjerrum–Eide Nc')


def fig5_3():
    d = ex2017_4_heave()
    W, H = 900, 470
    o = ''
    s = 22
    xw, y0 = 380, 40
    X = lambda x: xw + x * s
    Y = lambda z: y0 + z * s     # z: GL 深度
    o += R(X(-13), Y(0), 13 * s, 17 * s, '#efe6d8', None, 0) + R(X(0), Y(8), 14 * s, 9 * s, '#efe6d8', None, 0)
    o += L(X(-13), Y(0), X(0), Y(0), INK, 1.6) + L(X(0), Y(8), X(14), Y(8), INK, 1.6)
    o += L(X(0), Y(0), X(0), Y(14), STEEL, 6)
    o += L(X(0), Y(3.5), X(6), Y(3.5), WARN, 4) + T(X(6) + 6, Y(3.5) + 5, '最下階支撐（圓心）', 14, WARN, 'start', 'bold')
    o += C(X(0), Y(3.5), 6, WARN, '#fff', 2)
    R_ = d['X']
    a = d['alpha']
    # 坑外弧：從圓心水平往左（角 π）往下到正下方（3π/2 in math coords → screen down）
    pts = [(X(R_ * math.cos(t)), Y(3.5 + R_ * math.sin(t))) for t in [math.pi - i * (math.pi / 2) / 30 for i in range(31)]]
    pts2 = [(X(R_ * math.sin(t)), Y(3.5 + R_ * math.cos(t))) for t in [i * a / 30 for i in range(31)]]
    o += P(pts, COMP, 2.6, dash='8 5') + P(pts2, COMP, 2.6, dash='8 5')
    o += L(X(0), Y(3.5), X(-R_), Y(3.5), MUT, 1, '4 3') + L(X(0), Y(3.5), X(0), Y(3.5 + R_), MUT, 1, '4 3')
    o += L(X(0), Y(3.5), X(R_ * math.sin(a)), Y(3.5 + R_ * math.cos(a)), KEY, 1.6)
    o += T(X(R_ * math.sin(a) / 2) + 8, Y(3.5 + R_ * math.cos(a) / 2) - 6, f"*X*={R_:.1f}", 14, KEY, 'start', 'bold')
    o += T(X(1.3), Y(5.6), f"*α*={deg(a):.2f}°", 14, KEY, 'start', 'bold')
    o += T(X(-6), Y(3.5) - 8, '*π*/2', 14, COMP, 'middle', 'bold')
    o += dim(X(-1.2), Y(3.5), X(-1.2), Y(8), '', INK) + T(X(-1.5), Y(5.8), '*ℓ*=4.5', 14, INK, 'end')
    o += dim(X(-1.2), Y(8), X(-1.2), Y(14), '', INK) + T(X(-1.5), Y(11), '*D*=6.0', 14, INK, 'end')
    o += T(X(-12.5), Y(1.4), '土柱 *γH*=14.39、*q*=1', 14, TEN, 'start', 'bold')
    o += box(620, 300, 270, 140, '力矩比', ['*M*_{r}=*S*_{u}*X*²(*π*/2+*α*)', '*M*_{d}=(*γH*+*q*)*X*²/2', f"*FS*={d['FS']:.2f}"], KEY2, KEY)
    return svg(W, H, o, '圓弧力矩法')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
