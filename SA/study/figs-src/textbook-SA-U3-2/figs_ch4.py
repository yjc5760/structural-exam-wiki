# -*- coding: utf-8 -*-
"""第 4 章：剛性樓板扭轉（SA-2021-4）。座標、勁度、位移、剪力全部 import calcs。"""
from figs_common import *  # noqa
import math
import numpy as np
from calcs import ex2021, cols21

r = ex2021()
KK = {n: (r['kd'] if t == 'd' else r['ke']) for n, (x, y, t) in cols21.items()}


class Plan:
    """平面座標（m，x 右、y 上）→ SVG 像素。"""
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def __call__(self, x, y):
        return (self.ox + self.s * x, self.oy - self.s * y)


def _slab(pl, pts, fill=AC2, c=AC, w=2, dash=None, op=None):
    return P([pl(x, y) for x, y in pts], c, w, fill=fill, close=True, dash=dash, op=op)


def _col(pl, x, y, big, c=INK, fill=STEEL3):
    X, Y = pl(x, y)
    a = 15 if big else 9
    return R(X - a / 2, Y - a / 2, a, a, fill, c, 1.6)


SLAB = [(-3.4, -2.4), (3.4, -2.4), (3.4, 2.4), (-3.4, 2.4)]


def _rot(pts, th, cx=0.0, cy=0.0, u=0.0, v=0.0):
    c, s = math.cos(th), math.sin(th)
    return [(cx + c * (x - cx) - s * (y - cy) + u, cy + s * (x - cx) + c * (y - cy) + v) for x, y in pts]


def fig4_1():
    W, H = 900, 500
    o = ''
    # (a) 剛體繞 O 轉 θ：距離 r 的點走 rθ，方向垂直 r
    o += T(225, 34, '(a) 樓板繞 O 轉一個小角度 θ', 16, INK, 'middle', 'bold')
    pl = Plan(150, 330, 46)
    sl = [(-1.5, -1.6), (5.0, -1.6), (5.0, 3.0), (-1.5, 3.0)]
    th = math.radians(9)                     # 放大示意
    o += _slab(pl, sl, 'none', STEEL, 1.6, '6 5')
    o += _slab(pl, _rot(sl, th), AC2, AC, 2.2, op=0.9)
    O = pl(0, 0)
    o += C(*O, 6, KEY, '#fff', 2) + T(O[0] - 10, O[1] + 22, 'O', 16, KEY, 'end', 'bold')
    qx, qy = 3.8, 2.2
    Q = pl(qx, qy)
    o += L(*O, *Q, INK, 1.8, '5 4')
    o += C(*Q, 5, INK, None)
    o += T(Q[0] + 12, Q[1] + 4, '(*x*, *y*)', 15, INK, 'start', 'bold')
    o += T((O[0] + Q[0]) / 2 + 6, (O[1] + Q[1]) / 2 + 22, '*r*', 17, INK, 'start', 'bold')
    # 分量
    mag = 2.5                                 # 位移箭頭再放大 2.5 倍
    dx = -qy * th * pl.s * mag
    dy = qx * th * pl.s * mag
    Q2 = (Q[0] + dx, Q[1] - dy)
    o += A(*Q, *Q2, COMP, 3, 12)
    o += T(Q2[0] - 8, Q2[1] - 10, '*r*θ（放大）', 16, COMP, 'end', 'bold')
    o += A(Q[0], Q[1], Q[0] + dx, Q[1], AC, 2.4, 10)
    o += T(Q[0] + dx / 2, Q[1] + 22, '−θ*y*', 15, AC, 'middle', 'bold')
    o += A(Q[0] + dx, Q[1], Q[0] + dx, Q[1] - dy, TEN, 2.4, 10)
    o += T(Q[0] + dx - 8, Q[1] - dy / 2 + 14, '+θ*x*', 15, TEN, 'end', 'bold')
    o += arc_arrow(O[0], O[1], 40, 60, 120, KEY, 2.2, 9)
    o += T(O[0] - 26, O[1] - 46, 'θ（逆時針 +）', 15, KEY, 'end', 'bold')
    o += R(40, 410, 370, 78, KEY2, KEY, 1.6, 10)
    o += T(225, 438, '位移 ⊥ *r*，大小 *r*θ（S7）', 15, KEY, 'middle', 'bold')
    o += T(225, 468, '拆成兩向：Δ*x* = −θ*y*，Δ*y* = +θ*x*', 15, KEY, 'middle', 'bold')
    # (b) 整片樓板只有 3 個自由度
    o += T(675, 34, '(b) 剛性樓板：只剩 *u*、*v*、θ', 16, INK, 'middle', 'bold')
    pl2 = Plan(675, 230, 38)
    o += _slab(pl2, SLAB, AC2, AC, 2)
    for n, (x, y, t) in cols21.items():
        o += _col(pl2, x, y, t == 'e')
    Rf = pl2(0, 0)
    o += C(*Rf, 5, KEY, '#fff', 2)
    o += A(Rf[0], Rf[1], Rf[0] + 70, Rf[1], AC, 3, 12) + T(Rf[0] + 76, Rf[1] + 6, '*u*', 17, AC, 'start', 'bold')
    o += A(Rf[0], Rf[1], Rf[0], Rf[1] - 70, TEN, 3, 12) + T(Rf[0] + 8, Rf[1] - 66, '*v*', 17, TEN, 'start', 'bold')
    o += arc_arrow(Rf[0], Rf[1], 32, 190, 330, KEY, 2.4, 10)
    o += T(Rf[0] - 36, Rf[1] + 34, 'θ', 17, KEY, 'end', 'bold')
    for n, (x, y, t) in cols21.items():
        X, Y = pl2(x, y)
        o += T(X + (30 if x > 0 else -30), Y + 5, n, 14, INK, 'start' if x > 0 else 'end', 'bold')
    o += R(490, 360, 370, 128, WARN2, WARN, 1.6, 10)
    o += T(675, 388, '樓板平面內不變形（S4）：', 15, INK, 'middle', 'bold')
    o += T(675, 416, '每根柱頂＝參考點的 (*u*, *v*) ＋ 繞它轉 θ', 15, INK, 'middle')
    o += T(675, 448, '*u*_{*i*} = *u* − θ*y*_{*i*}′', 16, WARN, 'middle', 'bold')
    o += T(675, 476, '*v*_{*i*} = *v* + θ*x*_{*i*}′', 16, WARN, 'middle', 'bold')
    o += L(450, 50, 450, 490, GRID, 1.4)
    return svg(W, H, o, '剛體小轉角與剛性樓板三個自由度')


def fig4_2():
    W, H = 900, 545
    o = ''
    s = 46
    # (a) 只平移 v：各柱出力 k v，合力在哪裡？
    o += T(225, 34, '(a) 只往 *y* 平移：合力落在哪？', 16, INK, 'middle', 'bold')
    pl = Plan(225, 290, s)
    o += _slab(pl, SLAB, '#fafafa', STEEL, 1.6)
    sc = 90 / r['ke']
    for n, (x, y, t) in cols21.items():
        o += _col(pl, x, y, t == 'e')
        X, Y = pl(x, y)
        ln = KK[n] * sc
        o += A(X, Y - 10, X, Y - 10 - ln, TEN, 3, 11)
        o += T(X + (10 if x > 0 else -10), Y - 18 - ln / 2, '5*k*' if t == 'e' else '*k*', 15, TEN, 'start' if x > 0 else 'end', 'bold')
        o += T(X, Y + 26 if y < 0 else Y + 26, n, 14, MUT, 'middle', 'bold')
    xr = r['xr']
    X0, Y0 = pl(xr, 0)
    o += L(X0, pl(0, 2.6)[1], X0, pl(0, -2.6)[1], KEY, 2, '7 5')
    o += C(X0, Y0, 7, KEY, '#fff', 2.4)
    o += T(X0, Y0 + 28, '剛心 CR', 15, KEY, 'middle', 'bold')
    Xc = pl(0, 0)
    o += L(Xc[0], pl(0, 2.6)[1], Xc[0], pl(0, -2.6)[1], MUT, 1.2, '3 4')
    o += dim(Xc[0], pl(0, -2.75)[1], X0, pl(0, -2.75)[1], '', KEY, size=15)
    o += T(Xc[0] - 8, pl(0, -2.75)[1] + 6, f'*x*_{{r}} = {xr:.0f} m', 15, KEY, 'end', 'bold')
    o += R(40, 452, 370, 78, KEY2, KEY, 1.6, 10)
    o += T(225, 480, '*x*_{r} = Σ*k*_{*y*}*x* / Σ*k*_{*y*}', 16, KEY, 'middle', 'bold')
    o += T(225, 510, '= (2×*k*×(−3) + 2×5*k*×3)/12*k* = 2 m', 15, KEY, 'middle')
    # (b) 外力合力在幾何中心 → 對剛心有扭矩
    o += T(675, 34, '(b) 外力在中心、剛心在右 2 m', 16, INK, 'middle', 'bold')
    pl2 = Plan(675, 290, s)
    o += _slab(pl2, SLAB, '#fafafa', STEEL, 1.6)
    for n, (x, y, t) in cols21.items():
        o += _col(pl2, x, y, t == 'e')
        X, Y = pl2(x, y)
        o += A(X - 16, Y + 34, X - 16, Y + 2, COMP, 2.2, 9)
        o += T(X - 20, Y + 30, '27', 14, COMP, 'end', 'bold')
    C0 = pl2(0, 0)
    o += A(C0[0], C0[1] + 60, C0[0], C0[1] - 40, COMP, 3.6, 14)
    o += T(C0[0] - 8, C0[1] - 46, '108 kN', 15, COMP, 'end', 'bold')
    X0, Y0 = pl2(xr, 0)
    o += C(X0, Y0, 7, KEY, '#fff', 2.4) + T(X0 + 10, Y0 + 24, 'CR', 15, KEY, 'start', 'bold')
    o += dim(C0[0], Y0 + 46, X0, Y0 + 46, '*e* = 2 m', KEY, size=15, lab_off=14)
    o += arc_arrow(X0, Y0, 40, 120, 30, KEY, 2.6, 11)
    o += T(X0 + 34, Y0 - 40, '順時針', 15, KEY, 'start', 'bold')
    o += R(490, 452, 370, 78, KEY2, KEY, 1.6, 10)
    o += T(675, 480, '*M*_{t} = *F*(*x*_{F} − *x*_{r}) = 108 × (0 − 2)', 15, KEY, 'middle', 'bold')
    o += T(675, 510, '= −216 kN-m（順時針）', 16, KEY, 'middle', 'bold')
    o += L(450, 50, 450, 535, GRID, 1.4)
    return svg(W, H, o, '剛心與偏心扭矩')


def fig4_3():
    W, H = 900, 520
    o = ''
    o += T(450, 34, '繞剛心轉 θ：每根柱走 *r*′θ（垂直 *r*′），兩個方向都出力', 16, INK, 'middle', 'bold')
    pl = Plan(330, 280, 52)
    o += _slab(pl, SLAB, '#fafafa', STEEL, 1.6)
    xr = r['xr']
    CR = pl(xr, 0)
    th = -1.0                                   # 只取方向（順時針）
    for n, (x, y, t) in cols21.items():
        o += _col(pl, x, y, t == 'e')
        X, Y = pl(x, y)
        xp, yp = r['rel'][n]
        o += L(*CR, X, Y, MUT, 1.4, '5 4')
        dxv, dyv = -th * yp, th * xp            # 位移方向（未縮放）
        sc = 15
        o += A(X, Y, X + dxv * sc, Y - dyv * sc, COMP, 3, 11)
        kname = '5*k*' if t == 'e' else '*k*'
        contrib = KK[n] * (xp ** 2 + yp ** 2) / r['kd']
        lx = X + (20 if x > 0 else -20)
        o += T(lx, Y + (30 if y < 0 else -22), f'{n}：*r*′^{{2}} = {xp ** 2 + yp ** 2:.0f}', 14, INK, 'start' if x > 0 else 'end', 'bold')
        o += T(lx, Y + (50 if y < 0 else -42), f'{kname}*r*′^{{2}} = {contrib:.0f}*k*', 14, KEY, 'start' if x > 0 else 'end', 'bold')
    o += C(*CR, 7, KEY, '#fff', 2.4) + T(CR[0] + 10, CR[1] + 22, 'CR', 15, KEY, 'start', 'bold')
    o += arc_arrow(CR[0], CR[1], 34, 120, 20, KEY, 2.4, 10)
    o += T(CR[0] - 30, CR[1] - 34, 'θ', 17, KEY, 'end', 'bold')
    # 右側：推導框
    bx = 640
    o += R(bx, 80, 240, 300, KEY2, KEY, 1.6, 10)
    lines = [('柱的 *x* 向力 = *k*_{*x*}(−θ*y*′)', INK), ('柱的 *y* 向力 = *k*_{*y*}(θ*x*′)', INK),
             ('對 CR 的力矩：', INK), ('*k*_{*x*}*y*′^{2}θ + *k*_{*y*}*x*′^{2}θ', KEY),
             ('全部加起來：', INK), ('*K*_{θ} = Σ*k*_{*x*}*y*′^{2} + Σ*k*_{*y*}*x*′^{2}', KEY),
             ('= 48*k* + 60*k* = 108*k*', KEY), ('= 270000 kN-m/rad', KEY)]
    for i, (t_, c) in enumerate(lines):
        o += T(bx + 120, 112 + i * 34, t_, 15, c, 'middle', 'bold' if c == KEY else None)
    o += R(60, 448, 820, 56, WARN2, WARN, 1.4, 9)
    o += T(470, 482, '本題每根柱兩個方向的 *k* 相同，所以 *k*(*x*′^{2} + *y*′^{2}) = *k* *r*′^{2}：29*k* + 25*k* + 29*k* + 25*k* = 108*k*', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '扭轉勁度 K_θ 的來源')


def fig4_4():
    W, H = 900, 560
    o = ''
    o += T(450, 34, 'SA-2021-4 結果：平移 3.6 mm ＋ 順時針 0.0008 rad（位移放大 100 倍示意）', 16, INK, 'middle', 'bold')
    pl = Plan(335, 290, 44)
    amp = 100
    th = r['th'] * amp
    v = r['dy'] * amp
    o += _slab(pl, SLAB, 'none', STEEL, 1.6, '6 5')
    newslab = _rot(SLAB, th, r['xr'], 0, 0, v)
    o += _slab(pl, newslab, AC2, AC, 2.2, op=0.85)
    CR = pl(r['xr'], 0)
    o += C(*CR, 6, KEY, '#fff', 2.2) + T(CR[0] + 10, CR[1] + 20, 'CR', 14, KEY, 'start', 'bold')
    for n, (x, y, t) in cols21.items():
        o += _col(pl, x, y, t == 'e', STEEL, '#fff')
        xn, yn = _rot([(x, y)], th, r['xr'], 0, 0, v)[0]
        o += _col(pl, xn, yn, t == 'e')
        X, Y = pl(xn, yn)
        Vx, Vy = r['shear'][n]
        sc = 2.4
        o += A(X, Y, X + Vx * sc, Y, COMP, 2.6, 9)
        o += A(X, Y, X, Y - Vy * sc, TEN, 2.6, 10)
        u_, w_ = r['disp'][n]
        side = 1 if x > 0 else -1
        lx = X + side * 30
        ly = Y + (40 if y < 0 else -76)
        o += T(lx, ly, n, 15, INK, 'start' if side > 0 else 'end', 'bold')
        o += T(lx, ly + 20, f'位移 {u_ * 1000:+.1f}, {w_ * 1000:+.1f} mm', 14, AC, 'start' if side > 0 else 'end', 'bold')
        o += T(lx, ly + 40, f'剪力 {Vx:+.0f}, {Vy:+.0f} kN', 14, COMP, 'start' if side > 0 else 'end', 'bold')
    # 右側說明
    bx = 640
    o += R(bx, 90, 240, 250, '#fff', INK, 1.4, 10)
    o += T(bx + 120, 118, '每根柱（*x*′, *y*′ 量到 CR）', 15, INK, 'middle', 'bold')
    o += T(bx + 120, 150, '*u* = 0 − θ*y*′', 15, AC, 'middle', 'bold')
    o += T(bx + 120, 178, '*v* = 3.6 mm + θ*x*′', 15, AC, 'middle', 'bold')
    o += T(bx + 120, 214, '*V*_{*x*} = *ku*，*V*_{*y*} = *kv*', 15, COMP, 'middle', 'bold')
    o += T(bx + 120, 252, '左邊離 CR 遠（*x*′ = −5）', 14, INK, 'middle')
    o += T(bx + 120, 274, '→ 多走 4 mm，共 7.6 mm', 14, INK, 'middle')
    o += T(bx + 120, 302, '右邊（*x*′ = +1）少走 0.8', 14, INK, 'middle')
    o += T(bx + 120, 324, '→ 2.8 mm', 14, INK, 'middle')
    o += R(60, 470, 820, 76, KEY2, KEY, 1.5, 9)
    o += T(470, 498, 'Σ*V*_{*y*} = 19 + 35 + 19 + 35 = 108 kN（平衡）　Σ*V*_{*x*} = 4 + 20 − 4 − 20 = 0', 15, KEY, 'middle', 'bold')
    o += T(470, 528, '只受 *y* 向力，卻有 *x* 向剪力 ±4、±20 kN：這就是扭轉造成的', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2021-4 剛性樓板位移與柱剪力')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}
