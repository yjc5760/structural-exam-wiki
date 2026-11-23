# -*- coding: utf-8 -*-
"""第 3 章：α 趨勢、Nq 與 ql 封頂、反求樁長的阻抗分布、雙層樁。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig3_1():
    W, H = 900, 380
    pl = Plot(100, 50, 520, 270, 0, 2.2, 0, 1.2)
    o = pl.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], '*c*_{u}/*p*_{a}', 'α')
    pts = [(0.1, 1.0), (0.6, 0.62), (2.0, 0.35)]
    o += P([pl.pt(0, 1.0)] + [pl.pt(x, y) for x, y in pts], MUT, 2, dash='6 5')
    for (x, y), lab, anc in zip(pts, ['≤0.1 → 1.0（表的上端）', '0.6 → 0.62（113 年）', '≥2 → 約 0.35（表的下端）'], ['start', 'start', 'end']):
        o += pl.dot(x, y, KEY, 6)
        o += T(pl.X(x) + (10 if anc == 'start' else 0), pl.Y(y) - 14, lab, 14, KEY, anc, 'bold')
    o += R(650, 80, 235, 150, KEY2, KEY, 1.4, 8)
    o += T(767, 108, '只記方向', 16, KEY, 'middle', 'bold')
    o += T(767, 138, '黏土越硬，α 越小', 15, INK, 'middle')
    o += T(767, 166, '軟土：整圈黏住', 15, INK, 'middle')
    o += T(767, 194, '硬土：只黏一部分', 15, INK, 'middle')
    o += T(767, 220, '數值考卷會給', 15, TEN, 'middle', 'bold')
    return svg(W, H, o, 'α 與 cu/pa 的趨勢')


def fig3_2():
    d = ex2024_4()
    W, H = 900, 400
    # (a) Nq 曲線
    pl = Plot(80, 60, 340, 270, 25, 40, 0, 70)
    o = T(250, 30, '(a) *N*_{q} 隨 φ 急速變大', 16, INK, 'middle', 'bold')
    o += pl.axes([25, 30, 35, 40], [0, 20, 40, 60], 'φ', '*N*_{q}')
    nq = lambda ph: math.exp(math.pi * math.tan(math.radians(ph))) * math.tan(math.radians(45 + ph / 2)) ** 2
    o += pl.curve(nq, 25, 40, AC, 3)
    o += pl.dot(36, nq(36), KEY, 6)
    o += T(pl.X(36) - 8, pl.Y(nq(36)) - 12, f'36° → {nq(36):.2f}', 14, KEY, 'end', 'bold')
    o += pl.dot(30, nq(30), AC, 5)
    o += T(pl.X(30) + 10, pl.Y(nq(30)) + 24, f'30° → {nq(30):.1f}', 14, AC, 'start')
    # (b) bar
    x0 = 560
    o += T(720, 30, '(b) 2024-4 樁底：取小的那個', 16, INK, 'middle', 'bold')
    pl2 = Plot(x0, 60, 280, 270, 0, 2, 0, 3200)
    o += pl2.axes([], [0, 800, 1600, 2400, 3200], '', '*q*（kPa）')
    for i, (v, c, lab) in enumerate([(d['qpN'], COMPM, "*q*′*N*_{q}^{*}"), (d['ql'], ACM, '*q*_{l} 上限')]):
        x = 0.5 + i
        o += R(pl2.X(x - 0.3), pl2.Y(v), pl2.X(x + 0.3) - pl2.X(x - 0.3), pl2.Y(0) - pl2.Y(v), c, INK, 1.2)
        o += T(pl2.X(x), pl2.Y(v) - 8, f'{v:.1f}', 15, INK, 'middle', 'bold')
        o += T(pl2.X(x), pl2.Y(0) + 24, lab, 15, INK, 'middle')
    o += pl2.hline(d['ql'], 0, 2, KEY, 2, '6 4')
    return svg(W, H, o, 'Nq 與樁底上限 ql')


def _profile(o, x0, w, fmax, Lc, Lp, zmax, top, bot, lab, c, label_vals):
    Y = lambda z: top + z / zmax * (bot - top)
    X = lambda v: x0 + v / 50 * w
    for t in (0, 25, 50):
        o += L_(X(t), top, X(t), bot)
        o += T(X(t), top - 10, f'{t}', 14, MUT, 'middle')
    o += A(x0, top, x0 + w + 14, top, INK, 1.6, 9) + A(x0, top, x0, bot + 14, INK, 1.6, 9)
    o += T(x0 + w + 18, top + 5, '*f*_{s}', 15, INK, 'start')
    if Lc is None:
        pts = [(X(0), Y(0)), (X(fmax), Y(0)), (X(fmax), Y(Lp)), (X(0), Y(Lp))]
    else:
        pts = [(X(0), Y(0)), (X(fmax), Y(Lc)), (X(fmax), Y(Lp)), (X(0), Y(Lp))]
        o += L(x0 - 6, Y(Lc), x0 + w, Y(Lc), WARN, 1.8, '7 4')
        o += T(x0 + w, Y(Lc) - 8, f'*L*_{{c}} = 15*D* = {Lc:g} m', 14, WARN, 'end', 'bold')
    o += P(pts, c, 2.6, fill=TEN2, close=True)
    o += L(x0 - 8, Y(Lp), x0 + w, Y(Lp), INK, 1.2, '3 3')
    o += T(x0 + w, Y(Lp) + 22, f'樁底 *L* = {Lp:.2f} m', 15, KEY, 'end', 'bold')
    o += T(X(fmax) + 6, Y(Lp * 0.55), f'{fmax:.2f} kPa', 14, c, 'start', 'bold')
    o += T(x0 + w / 2, bot + 50, lab, 16, INK, 'middle', 'bold')
    for z in label_vals:
        o += T(x0 - 8, Y(z) + 5, f'{z}', 14, MUT, 'end')
    return o


def L_(x1, y1, x2, y2):
    return L(x1, y1, x2, y2, GRID, 1)


def fig3_3():
    d = ex2024_4()
    W, H = 900, 520
    top, bot, zmax = 60, 430, 55
    o = _profile('', 90, 260, d['fs_c'], None, d['L_c'], zmax, top, bot, '(a) 黏土：*f*_{s} = α*c*_{u} 與深度無關', TEN, [0, 10, 20, 30, 40, 50])
    o = _profile(o, 530, 260, d['fmax'], d['Lcr'], d['L_s'], zmax, top, bot, '(b) 飽和砂：三角形＋矩形', TEN, [0, 10, 20, 30, 40, 50])
    o += T(20, bot + 20, '深度', 14, INK, 'start')
    return svg(W, H, o, 'SM-2024-4 樁身阻抗分布')


def fig3_4():
    d = ex2021_3()
    W, H = 900, 420
    top, bot, zmax = 60, 360, 12.5
    Y = lambda z: top + z / zmax * (bot - top)
    x0, w = 150, 420
    X = lambda v: x0 + v / 80 * w
    o = ''
    for t in (0, 20, 40, 60, 80):
        o += L(X(t), top, X(t), bot, GRID, 1) + T(X(t), top - 10, f'{t}', 14, MUT, 'middle')
    for z in (0, 3, 6, 9, 12):
        o += T(x0 - 8, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += A(x0, top, x0 + w + 14, top, INK, 1.6, 9) + A(x0, top, x0, bot + 14, INK, 1.6, 9)
    o += T(x0 + w + 18, top + 5, '*f*_{s}（kPa）', 15, INK, 'start')
    o += R(40, Y(0), 60, Y(6) - Y(0), '#fff3e0', WARN, 1) + T(70, Y(3) + 5, '砂', 15, INK, 'middle', 'bold')
    o += R(40, Y(6), 60, Y(12) - Y(6), '#e3f2fd', AC, 1) + T(70, Y(9) + 5, '黏土', 15, INK, 'middle', 'bold')
    f6 = d['K'] * d['sv6'] * math.tan(math.radians(d['dlt']))
    o += P([(X(0), Y(0)), (X(f6), Y(6)), (X(0), Y(6))], TEN, 2.4, fill=TENM, close=True)
    o += P([(X(0), Y(6)), (X(d['fs2']), Y(6)), (X(d['fs2']), Y(12)), (X(0), Y(12))], TEN, 2.4, fill=TEN2, close=True)
    o += T(X(f6) + 8, Y(6) - 8, f'{f6:.2f}', 14, TEN, 'start', 'bold')
    o += T(X(d['fs2']) + 8, Y(9), f"α*c*_{{u}} = {d['fs2']:.0f}", 15, TEN, 'start', 'bold')
    o += R(640, 90, 245, 170, KEY2, KEY, 1.4, 8)
    o += T(762, 118, '同一根樁、兩套語言', 15, KEY, 'middle', 'bold')
    o += T(762, 148, f"砂：*Q*_{{s1}} = {d['Qs1']:.2f}", 15, INK, 'middle')
    o += T(762, 176, f"黏土：*Q*_{{s2}} = {d['Qs2']:.2f}", 15, INK, 'middle')
    o += T(762, 204, f"端承：*Q*_{{p}} = {d['Qp']:.2f}", 15, AC, 'middle')
    o += T(762, 236, f"*Q*_{{a}} = {d['Qa']:.2f} kN", 16, KEY, 'middle', 'bold')
    o += L(x0 - 6, Y(0), x0 + w, Y(0), AC, 2)
    o += T(x0 + w, Y(0) + 22, '水位在地表 → 砂用 γ′', 14, AC, 'end', 'bold')
    return svg(W, H, o, 'SM-2021-3 雙層樁的摩擦分布')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
