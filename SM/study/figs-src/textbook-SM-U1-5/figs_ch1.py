# -*- coding: utf-8 -*-
"""第 1 章：總應力圓 vs 有效圓、三種試驗、流砂。"""
from plot import *  # noqa
from calcs import *  # noqa


def mohr_axes(pl, smax, tmax, sticks, tticks):
    o = pl.axes(sticks, tticks, '*σ* (kPa)', '*τ*', grid=True)
    return o


def circle(pl, s1, s3, c, w=2.6, dash=None, fill=None):
    C0, R = (s1 + s3) / 2, (s1 - s3) / 2
    pts = [pl.pt(C0 + R * math.cos(t), R * math.sin(t)) for t in [i * math.pi / 120 for i in range(121)]]
    o = ''
    if fill:
        o += P(pts, None, fill=fill, close=True, op=0.35)
    return o + P(pts, c, w, dash=dash)


def fig1_1():
    d = ex2018_2()
    W, H = 900, 420
    pl = Plot(80, 50, 600, 300, 0, 200, 0, 100)
    o = mohr_axes(pl, 200, 100, [0, 50, 100, 150, 200], [0, 25, 50, 75, 100])
    o += circle(pl, d['s1'], d['s3'], COMP, 2.8)
    o += circle(pl, d['s1e'], d['s3e'], TEN, 3)
    for phi, c, nm in ((d['phi_cu'], COMP, f"*φ*_{{cu}}={d['phi_cu']:.2f}°"), (d['phi_e'], TEN, f"*φ*′={d['phi_e']:.2f}°")):
        xe = 200 if tan(phi) * 200 <= 100 else 100 / tan(phi)
        o += L(pl.X(0), pl.Y(0), pl.X(xe), pl.Y(xe * tan(phi)), c, 2, '7 4')
        o += T(pl.X(xe) - 6, pl.Y(xe * tan(phi)) - 8, nm, 15, c, 'end', 'bold')
    for s, c in ((d['s3'], COMP), (d['s1'], COMP), (d['s3e'], TEN), (d['s1e'], TEN)):
        o += C(pl.X(s), pl.Y(0), 4.5, c, '#fff', 1.4)
    o += T(pl.X(d['s3e']), pl.Y(0) - 8, '33', 14, TEN, 'middle', 'bold') + T(pl.X(d['s1e']), pl.Y(0) - 8, '118', 14, TEN, 'middle', 'bold')
    o += T(pl.X(d['s3']) + 4, pl.Y(0) - 8, '100', 14, COMP, 'start', 'bold') + T(pl.X(d['s1']), pl.Y(0) - 8, '185', 14, COMP, 'middle', 'bold')
    yy = pl.Y(0) + 40
    o += A(pl.X((d['s1e'] + d['s3e']) / 2), yy, pl.X((d['s1'] + d['s3']) / 2), yy, AC, 2, 10)
    o += T(pl.X((d['s1e'] + d['s1']) / 2 - 30), yy - 6, '平移 *u*_{f}=67', 15, AC, 'middle', 'bold')
    o += box(700, 70, 185, 150, '同大、差 *u*_{f}', ['半徑都 42.5', '水不扛剪力', '只扣正向應力'], KEY2, KEY)
    return svg(W, H, o, '總應力圓與有效應力圓')


def fig1_2():
    W, H = 900, 400
    o = T(180, 34, '試驗', 16, INK, 'middle', 'bold') + T(400, 34, '① 壓密階段', 16, INK, 'middle', 'bold') + T(600, 34, '② 剪切階段', 16, INK, 'middle', 'bold') + T(790, 34, '得到', 16, INK, 'middle', 'bold')
    rows = [('UU 不壓密不排水', False, False, '*S*_{u}（*φ*_{u}=0）', COMP),
            ('CU 壓密不排水', True, False, '*φ*_{cu}，量 *u* → *φ*′', KEY),
            ('CD 壓密排水', True, True, '*c*′、*φ*′（*u*=0）', TEN)]
    for i, (nm, a, b, got, c) in enumerate(rows):
        y = 70 + i * 105
        o += R(40, y, 280, 80, '#fff', c, 1.8, 10) + T(180, y + 46, nm, 16, c, 'middle', 'bold')
        for x, open_ in ((400, a), (600, b)):
            col = TEN if open_ else COMP
            o += C(x, y + 40, 28, TEN2 if open_ else COMP2, col, 2.2)
            if open_:
                o += L(x - 18, y + 40, x + 18, y + 40, col, 4)
            else:
                o += L(x, y + 22, x, y + 58, col, 4)
            o += T(x + 40, y + 46, '開（排水）' if open_ else '關', 14, col, 'start', 'bold')
        o += R(690, y + 10, 200, 60, KEY2 if c == KEY else (TEN2 if c == TEN else COMP2), c, 1.4, 8)
        o += T(790, y + 46, got, 15, c, 'middle', 'bold')
    return svg(W, H, o, '三種三軸試驗')


def fig1_3():
    W, H = 900, 420
    o = ''
    # 砂柱
    x0, y0, w, h = 60, 70, 120, 280
    o += R(x0, y0, w, h, '#fff8e1', INK, 1.5)
    for i in range(5):
        o += A(x0 + 20 + i * 20, y0 + h - 20, x0 + 20 + i * 20, y0 + 30, AC, 1.6, 9)
    o += T(x0 + w / 2, y0 - 12, '向上滲流', 15, AC, 'middle', 'bold')
    o += T(x0 + w / 2, y0 + h + 26, '砂（*γ*_{sat}=19.8）', 14, INK, 'middle')
    # 應力圖
    gsat, gw = 19.8, GW
    gp = gsat - gw
    zmax = 2.0
    px0, pw = 260, 360
    smax = 45
    X = lambda s: px0 + s / smax * pw
    Y = lambda z: y0 + z / zmax * h
    o += A(px0, y0, px0 + pw + 16, y0, INK, 1.5) + A(px0, y0, px0, y0 + h + 16, INK, 1.5)
    for s in (0, 10, 20, 30, 40):
        o += L(X(s), y0, X(s), y0 + h, GRID, 1) + T(X(s), y0 - 8, f'{s}', 14, MUT, 'middle')
    o += T(px0 + pw + 18, y0 + 5, 'kPa', 14, INK) + T(px0 - 8, y0 + h + 8, '*z* (m)', 14, INK, 'end')
    icr = gp / gw
    for i_, c, nm in ((0.0, TEN, '*i*=0'), (0.5 * icr, TEN, '*i*=0.5*i*_{cr}'), (icr, COMP, '*i*=*i*_{cr}')):
        o += L(X(0), Y(0), X((gp - i_ * gw) * zmax), Y(zmax), c, 3 if i_ == icr else 2.4, '7 4' if i_ == icr else None)
        o += T(X((gp - i_ * gw) * zmax) + 8, Y(zmax) - 4, nm, 14, c, 'start', 'bold')
    o += L(X(0), Y(0), X(gsat * zmax), Y(zmax), MUT, 2) + T(X(gsat * zmax) - 6, Y(zmax) - 30, '*σ*', 15, MUT, 'end', 'bold')
    o += T(X(4), Y(0.6), '*σ*′ 線', 15, TEN, 'start', 'bold')
    o += box(650, 80, 235, 170, '*σ*′=(*γ*′−*iγ*_{w})*z*', ['斜率歸零 ⇒', '*i*_{cr}=*γ*′/*γ*_{w}', '=(*G*_{s}−1)/(1+*e*)', f'本例 ≈ {icr:.2f}'], KEY2, KEY)
    return svg(W, H, o, '流砂')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
