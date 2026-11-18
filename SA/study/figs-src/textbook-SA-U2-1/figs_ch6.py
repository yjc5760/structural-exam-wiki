# -*- coding: utf-8 -*-
"""第 6 章：SA-2012-2 桁架＋彈簧（桿力圖、X 隨 EA/Ks 的變化）、SA-2006-1 梁＋桁架（α = EI/EA 掃描）。"""
from sa_draw import *  # noqa
import math
import calcs

C6 = calcs.C6
TEN_C = AC      # 拉
CMP_C = COMP    # 壓


def spring_v(x, ytop, ybot, c=INK, n=6, wdt=9):
    pts = [(x, ytop), (x, ytop + 6)]
    seg = (ybot - ytop - 12) / n
    for i in range(n):
        pts.append((x + (wdt if i % 2 == 0 else -wdt), ytop + 6 + seg * (i + 0.5)))
    pts += [(x, ybot - 6), (x, ybot)]
    return P(pts, c, 1.8)


def fig6_1():
    W, H = 900, 510
    sc = 70
    ox, oy = 150, 350
    pt = lambda X, Y: (ox + X * sc, oy - Y * sc)
    N = {'a': pt(0, 0), 'b': pt(4, 0), 'c': pt(8, 0), 'd': pt(4, 4)}
    Fv = {k: float(v) for k, v in C6['12_forces'].items()}
    o = ''
    for nm, (p, q) in {'ab': ('a', 'b'), 'bc': ('b', 'c'), 'ad': ('a', 'd'), 'cd': ('c', 'd'), 'bd': ('b', 'd')}.items():
        v = Fv[nm]
        c = TEN_C if v > 0 else CMP_C
        w = 2.5 + abs(v) / 4.5
        (x1, y1), (x2, y2) = N[p], N[q]
        o += L(x1, y1, x2, y2, c, w, op=0.85)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = {'ab': (0, 26), 'bc': (0, 26), 'ad': (-48, -6), 'cd': (48, -6), 'bd': (-8, 0)}[nm]
        anc = 'end' if nm in ('ad', 'bd') else ('start' if nm == 'cd' else 'middle')
        lab = f'{v:+.2f}'.replace('-', '−')
        o += T(mx + dx, my + dy, lab, 15, c, anc, 'bold')
    for k, (x, y) in N.items():
        o += C(x, y, 6, '#fff', INK, 1.8)
    o += pin(*N['a']) + roller(*N['c'])
    bx, by = N['b']
    o += spring_v(bx, by + 6, by + 70, INK) + hatch_ground(bx - 22, by + 70, 44)
    o += A(bx + 26, by + 56, bx + 26, by + 14, FOR, 2.4, 10) + T(bx + 34, by + 48, '*X* = 22.12', 15, FOR, 'start', 'bold')
    o += T(bx - 16, by + 48, '*K*_{s}', 15, INK, 'end', 'bold')
    dx_, dy_ = N['d']
    o += A(dx_, dy_ - 60, dx_, dy_ - 8, LOAD, 2.6, 11) + T(dx_ + 8, dy_ - 40, '40 kN', 15, LOAD, 'start', 'bold')
    o += A(dx_ + 8, dy_, dx_ + 70, dy_, LOAD, 2.6, 11) + T(dx_ + 76, dy_ + 5, '20 kN', 15, LOAD, 'start', 'bold')
    for k, (x, y) in N.items():
        off = {'a': (-14, 6, 'end'), 'b': (14, -10, 'start'), 'c': (14, 6, 'start'), 'd': (-12, -10, 'end')}[k]
        o += T(x + off[0], y + off[1], k, 16, INK, off[2], 'bold')
    o += dim(N['a'][0], oy + 96, N['b'][0], oy + 96, '4 m', MUT, size=14) + dim(N['b'][0], oy + 96, N['c'][0], oy + 96, '4 m', MUT, size=14)
    bx0 = 720
    o += R(bx0 - 10, 80, 180, 210, KEY2, PUR, 1.4, 10)
    yy = 108
    for s, c, wgt in [('桿力（kN）', PUR, 'bold'), ('藍：拉（+）', TEN_C, 'bold'), ('紅：壓（−）', CMP_C, 'bold'), ('線寬 ∝ |力|', MUT, None),
                      ('', INK, None), ('*EA* = 10000 kN', INK, None), ('*K*_{s} = 2500 kN/m', INK, None), ('*EA*/*K*_{s} = 4 m', PUR, 'bold')]:
        if s:
            o += T(bx0 + 80, yy, s, 15, c, 'middle', wgt)
        yy += 24 if s else 8
    o += T(450, 500, '豎桿 bd 的壓力 22.12 kN，正好等於彈簧往上頂 b 的力 *X*（節點 b 垂直平衡）', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2012-2 桁架＋彈簧')


def fig6_2():
    W, H = 900, 400
    fX = C6['12_fX']
    pl = Plot(110, 50, 560, 260, 0, 40, 0, 32)
    o = pl.axes([0, 4, 10, 20, 30, 40], [0, 10, 20, 22.12, 29.71], '*EA*/*K*_{s}（m）', '*X*（kN）', size=14,
                yfmt=lambda t: {22.12: '22.12', 29.71: '29.71'}.get(t, f(t)))
    o += pl.curve(lambda r: float(fX(r)), 0, 40, PUR, 3)
    o += pl.dot(0, float(C6['12_X_rigid']), MOM) + T(pl.X(0) + 12, pl.Y(29.71) - 8, '*K*_{s} → ∞：剛性支承 29.71', 15, MOM, 'start', 'bold')
    o += pl.dot(4, float(C6['12_X']), FOR) + pl.vline(4, 0, 22.12, FOR, 1.2) + T(pl.X(4) + 12, pl.Y(22.12) - 6, '本題 4 m：22.12', 15, FOR, 'start', 'bold')
    o += T(pl.X(33), pl.Y(15), '*K*_{s} → 0：*X* → 0', 15, AC, 'middle', 'bold')
    o += T(pl.X(33), pl.Y(15) + 20, '（彈簧等於不存在）', 14, MUT, 'middle')
    bx = 700
    o += R(bx, 60, 188, 240, KEY2, PUR, 1.4, 10)
    yy = 90
    for s, c, wgt, sz in [('彈簧＝一根桿件', PUR, 'bold', 16), ('', INK, None, 4),
                          ('桿：*N*^{2}·*L*/2*EA*', INK, None, 15), ('簧：*X*^{2}·(1/*K*_{s})/2', INK, None, 15), ('', INK, None, 4),
                          ('同乘 *EA*：彈簧像一根', INK, None, 15), ('長 *EA*/*K*_{s} 的桿', PUR, 'bold', 15), ('', INK, None, 4),
                          ('(6 + 4√2 + *EA*/*K*_{s})*X*', INK, None, 15), ('= 120 + 160√2', INK, None, 15)]:
        if s:
            o += T(bx + 94, yy, s, sz, c, 'middle', wgt)
        yy += sz + 9 if s else 4
    o += T(450, 380, '彈簧越軟（*EA*/*K*_{s} 越大），分到的力越少；兩個極限各對應一題「沒有彈簧」的題目', 15, INK, 'middle')
    return svg(W, H, o, '彈簧勁度掃描')


def fig6_3():
    W, H = 900, 430
    fRD, fDJ = C6['06_fRD'], C6['06_fDJ']
    lg = lambda a: math.log10(a)
    o = ''
    for k, (ttl, fn, lo, hi, ticks, c, lab0, labinf, unit) in enumerate([
        ('(a) *R*_{D}（kN）', fRD, 7, 14, [8, 10, 12, 14], MOM, '8.125', '12.93', ''),
        ('(b) Δ_{J}·*EA*', fDJ, 300, 620, [300, 400, 500, 600], AC, '573.4', '341.4', '')]):
        x0 = 80 + k * 430
        pl = Plot(x0, 60, 330, 250, -3, 3, lo, hi)
        o += T(x0 + 165, 34, ttl, 16, INK, 'middle', 'bold')
        o += pl.axes([-3, -2, -1, 0, 1, 2, 3], ticks, 'α', '', size=14,
                     xfmt=lambda t: {-3: '10^{−3}', -2: '0.01', -1: '0.1', 0: '1', 1: '10', 2: '100', 3: '10^{3}'}[t], yfmt=lambda t: f(t))
        o += pl.curve(lambda u: float(fn(10 ** u)), -3, 3, c, 3)
        o += pl.vline(-2, lo, float(fn(0.01)), MUT, 1.2)
        o += pl.dot(-2, float(fn(0.01)), c)
        o += T(pl.X(-2) + 8, pl.Y(float(fn(0.01))) + (22 if k == 0 else -12), '實際斷面 α ≈ 0.01', 14, MUT, 'start')
        o += T(pl.X(-3) + 4, pl.Y(float(fn(1e-3))) + (-10 if k == 0 else 22), f'α → 0：{lab0}', 14, c, 'start', 'bold')
        o += T(pl.X(3) - 4, pl.Y(float(fn(1e3))) + (22 if k == 0 else 26), f'α → ∞：{labinf}', 14, c, 'end', 'bold')
    o += R(60, 352, 780, 66, KEY2, PUR, 1.4, 10)
    o += T(450, 378, 'α = *EI*/*EA*（m²）：α → 0 是「桁架不會變形」、α → ∞ 是「梁不會彎」', 15, PUR, 'middle', 'bold')
    o += T(450, 404, '答案一定落在兩個極限之間（Δ_{J}·*EA* 介於 341.4～573.4）——通式兩端都對，中間就不會錯太遠', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2006-1 α 掃描')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
