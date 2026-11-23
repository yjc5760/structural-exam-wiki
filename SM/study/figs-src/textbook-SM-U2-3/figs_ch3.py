# -*- coding: utf-8 -*-
"""第 3 章：自由端自由體圖、自由端 vs 固定端、地錨位置。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig3_1():
    d = ex2005_1()
    W, H = 900, 520
    o = ''
    x0, y0, zs, sc = 420, 40, 28, 3.0
    Y = lambda z: y0 + z * zs
    Hm, D = d['H'], d['D']
    o += L(x0, Y(0), x0, Y(Hm + D), STEEL, 7)
    o += L(x0 - 330, Y(0), x0, Y(0), INK, 1.4) + L(x0, Y(Hm), x0 + 300, Y(Hm), INK, 1.4) + T(x0 + 300, Y(Hm) - 6, '開挖面', 14, INK, 'end')
    # 主動三角形（左）
    o += P([(x0, Y(0)), (x0 - d['pa'] * sc, Y(Hm)), (x0, Y(Hm))], TEN, 2, fill=TEN2, close=True)
    o += T(x0 - d['pa'] * sc - 6, Y(Hm) + 5, f"{d['pa']:.2f}", 14, TEN, 'end', 'bold')
    yPa = Y(Hm * 2 / 3)
    o += A(x0 - 240, yPa, x0 - 6, yPa, TEN, 3.2, 13) + T(x0 - 245, yPa - 8, f"*P*_{{a}}={d['Pa']:.2f}", 15, TEN, 'end', 'bold')
    # 淨被動矩形（右）
    o += R(x0, Y(Hm), d['pnet'] * sc, D * zs, COMP2, COMP, 1.8)
    yPn = Y(Hm + D / 2)
    o += A(x0 + 200, yPn, x0 + 6, yPn, COMP, 3.2, 13) + T(x0 + 205, yPn + 5, f"18*D*（*p*_{{net}}=18）", 15, COMP, 'start', 'bold')
    # 地錨
    ya = Y(d['ha'])
    o += A(x0 - 4, ya, x0 - 200, ya, WARN, 3.2, 13) + T(x0 - 205, ya + 5, f"*T*={d['T']:.2f}（拉向坑外土中）", 15, WARN, 'end', 'bold')
    o += C(x0, ya, 7, WARN, '#fff', 2) + T(x0 + 12, ya - 8, '取矩點（地錨）', 14, WARN, 'start', 'bold')
    # 力臂
    o += dim(x0 - 270, ya + 16, x0 - 270, yPa, '', TEN) + T(x0 - 278, (ya + yPa) / 2 + 5, '4.5 m', 14, TEN, 'end', 'bold')
    o += dim(x0 + 330, ya, x0 + 330, yPn, '', COMP) + T(x0 + 338, (ya + yPn) / 2 + 5, '7.5+*D*/2', 14, COMP, 'start', 'bold')
    o += dim(x0 - 60, Y(Hm), x0 - 60, Y(Hm + D), '', INK) + T(x0 - 68, Y(Hm + D / 2) + 5, f"*D*={D:.2f}", 15, INK, 'end', 'bold')
    o += T(x0 - 380, Y(Hm * 0.85), '砂 *K*_{a}=0.3073', 14, INK)
    o += T(x0 - 320, Y(Hm + 2), '黏土 *c*_{u}=45', 14, INK)
    return svg(W, H, o, '自由端支撐')


def fig3_2():
    W, H = 900, 460
    o = ''
    for k, (x0, title, fixed) in enumerate(((150, '自由端（樁尖可轉）', False), (600, '固定端（樁尖不轉）', True))):
        y0, Hh, D = 60, 200, 110 if not fixed else 150
        o += T(x0 + 60, 36, title, 16, KEY, 'middle', 'bold')
        o += L(x0, y0, x0, y0 + Hh + D, STEEL, 5)
        o += L(x0, y0 + Hh, x0 + 120, y0 + Hh, INK, 1.2)
        o += A(x0 - 2, y0 + 20, x0 - 60, y0 + 20, WARN, 2.4, 10)
        n = 60
        pts, mpts = [], []
        for i in range(n + 1):
            t = i / n
            if not fixed:
                dx = 26 * math.sin(math.pi * t * 0.9)
                m = 60 * math.sin(math.pi * t * 0.95)
            else:
                dx = 22 * math.sin(math.pi * t) * (1 - t) * 1.6
                m = 60 * math.sin(1.25 * math.pi * t) * (1 - 0.2 * t)
            pts.append((x0 + dx, y0 + t * (Hh + D)))
            mpts.append((x0 - 30 - m, y0 + t * (Hh + D)))
        o += P(pts, COMP, 2.2, dash='6 4')
        o += L(x0 - 30, y0, x0 - 30, y0 + Hh + D, MUT, 1)
        o += P(mpts, KEY, 2.4)
        o += T(x0 - 100, y0 + 40, '彎矩', 14, KEY, 'middle', 'bold')
        if fixed:
            ti = 0.8
            o += C(x0 - 30, y0 + ti * (Hh + D), 6, KEY, '#fff', 1.8)
            o += T(x0 - 40, y0 + ti * (Hh + D) + 5, '反曲點 *M*=0', 14, KEY, 'end', 'bold')
        o += T(x0 + 40, y0 + Hh + D + 30, '淺、彎矩大' if not fixed else '深、彎矩小', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '自由端與固定端')


def fig3_3():
    W, H = 900, 405
    phi = 30.0
    o = ''
    s = 26
    x0, y0 = 160, 60
    Hm, D, da = 7.0, 3.0, 2.0
    X = lambda x: x0 + x * s
    Y = lambda z: y0 + z * s
    o += L(X(-4), Y(0), X(26), Y(0), INK, 1.6)
    o += L(X(0), Y(0), X(0), Y(Hm + D), STEEL, 6)
    o += L(X(-4), Y(Hm), X(0), Y(Hm), INK, 1.2)
    wa = (Hm + D) * tan(45 - phi / 2)
    o += P([(X(0), Y(Hm + D)), (X(wa), Y(0)), (X(0), Y(0))], TEN, 2, fill=TEN2, close=True, op=0.9)
    o += T(X(wa * 0.35), Y((Hm + D) * 0.55), '主動楔', 15, TEN, 'middle', 'bold')
    o += T(X(wa * 0.6) + 8, Y((Hm + D) * 0.55), '45°+*φ*/2', 14, TEN, 'start')
    wp = da * tan(45 + phi / 2)
    xa = wa + wp
    o += L(X(0), Y(da), X(xa), Y(da), WARN, 2.6) + R(X(xa) - 4, Y(da) - 18, 8, 36, WARN, None, 0)
    o += P([(X(xa), Y(da)), (X(xa - wp), Y(0)), (X(xa), Y(0))], COMP, 2, fill=COMP2, close=True, op=0.9)
    o += T(X(xa - wp * 0.4), Y(0) - 10, '被動楔（錨碇板前方）', 14, COMP, 'middle', 'bold')
    o += T(X(xa) + 10, Y(da) + 5, '錨碇板', 14, WARN, 'start', 'bold')
    o += dim(X(0), Y(Hm + D) + 30, X(xa), Y(Hm + D) + 30, '', KEY)
    o += T(X(xa) + 30, Y(Hm + D) + 36, '*x* ≥ (*H*+*D*)tan(45°−*φ*/2)', 15, KEY, 'start', 'bold') + T(X(xa) + 30, Y(Hm + D) + 58, '　＋*d*_{a}tan(45°+*φ*/2)', 15, KEY, 'start', 'bold')
    o += T(X(-0.4), Y(Hm + D / 2), '*D*', 14, INK, 'end') + T(X(-0.4), Y(Hm / 2), '*H*', 14, INK, 'end')
    return svg(W, H, o, '地錨位置')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
