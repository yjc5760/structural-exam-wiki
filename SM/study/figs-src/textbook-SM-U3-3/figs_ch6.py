# -*- coding: utf-8 -*-
"""第 6 章：圓弧切片法。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig6_1():
    W_, H = 900, 450
    o = T(240, 24, '(a) 圓弧切成直條（示意）', 16, INK, 'middle', 'bold')
    cx, cy, R0 = 300, 52, 300
    # ground profile: toe at x=60,y=360 ; crest at x=330,y=180; flat to 470
    gy = lambda x: 360 if x < 80 else (360 - (x - 80) * 180 / 250 if x < 330 else 180)
    arc_y = lambda x: cy + math.sqrt(max(R0 ** 2 - (x - cx) ** 2, 0))
    xs = [x for x in range(60, 471, 2)]
    o += P([(40, 360), (80, 360), (330, 180), (480, 180), (480, 420), (40, 420)], SOILE, 1.4, fill=SOIL, close=True)
    # find arc intersections approx
    xl = 70
    xr = 470
    pts = [(x, arc_y(x)) for x in range(xl, xr + 1, 4) if arc_y(x) >= gy(x) - 1]
    o += P(pts, COMP, 3, dash='9 5')
    edges = [100, 170, 240, 310, 380, 450]
    for xe in edges:
        if arc_y(xe) > gy(xe):
            o += L(xe, gy(xe), xe, arc_y(xe), INK, 1.4)
    o += C(cx, cy, 5, KEY, '#fff', 2)
    o += T(cx + 10, cy + 4, 'O', 15, KEY, 'start', 'bold')
    o += L(cx, cy, 345, arc_y(345), KEY, 1.4, '4 3')
    o += T(352, arc_y(345) - 50, 'α_{n}', 16, KEY, 'start', 'bold')
    o += T(140, 404, '切片 n：寬 *b*_{n}', 14, INK, 'start')
    # (b) single slice
    o += T(700, 24, '(b) 一片的自由體（Fellenius）', 16, INK, 'middle', 'bold')
    a = 30
    sx, sy, bw = 640, 120, 120
    top = [(sx, sy), (sx + bw, sy - 30)]
    bl = (sx, sy + 200)
    br = (sx + bw, sy + 200 - bw * tan(a))
    o += P([top[0], top[1], br, bl], INK, 2, fill=STEEL2, close=True)
    mx, my = (bl[0] + br[0]) / 2, (bl[1] + br[1]) / 2
    o += A(mx, sy + 40, mx, sy + 150, INK, 3, 12)
    o += T(mx + 8, sy + 100, '*W*_{n}', 16, INK, 'start', 'bold')
    nx, ny = -sin(a), -cos(a)
    o += A(mx - nx * 100, my - ny * 100, mx, my, AC, 3, 12)
    o += T(mx - nx * 100 - 6, my - ny * 100 + 18, "*N*′ + *u*Δ*L*", 15, AC, 'end', 'bold')
    tx, ty = cos(a), -sin(a)
    o += A(mx, my + 4, mx + tx * 90, my + 4 + ty * 90, TEN, 3, 12)
    o += T(mx + tx * 90 + 8, my + ty * 90 + 24, '*c*′Δ*L* + *N*′ tan φ′', 15, TEN, 'start', 'bold')
    o += T(sx + bw + 10, sy + 60, '切片間力', 14, MUT, 'start')
    o += T(sx + bw + 10, sy + 80, '忽略', 14, MUT, 'start')
    o += T(bl[0] - 8, bl[1] + 22, 'α', 16, INK, 'end', 'bold')
    return svg(W_, H, o, '圓弧切片法與單一切片自由體')


def fig6_2():
    d = ex2021_4()
    W_, H = 900, 400
    pl = Plot(100, 50, 560, 270, 0, 5, 0, 650)
    o = pl.axes([], [0, 200, 400, 600], '', 'kN/m')
    for i, rw in enumerate(d['rows']):
        x = 0.5 + i
        res = rw['cL'] + rw['Nt']
        o += R(pl.X(x - 0.36), pl.Y(res), pl.X(x - 0.02) - pl.X(x - 0.36), pl.Y(0) - pl.Y(res), TENM, TEN, 1)
        o += R(pl.X(x + 0.02), pl.Y(rw['Ws']), pl.X(x + 0.36) - pl.X(x + 0.02), pl.Y(0) - pl.Y(rw['Ws']), COMPM, COMP, 1)
        o += T(pl.X(x - 0.19), pl.Y(res) - 6, f'{res:.0f}', 14, TEN, 'middle', 'bold')
        if rw['Ws'] > 1:
            o += T(pl.X(x + 0.19), pl.Y(rw['Ws']) - 6, f"{rw['Ws']:.0f}", 14, COMP, 'middle', 'bold')
        o += T(pl.X(x), pl.Y(0) + 22, f"片 {i + 1}（α = {rw['a']}°）", 14, INK, 'middle')
    o += R(690, 60, 200, 200, KEY2, KEY, 1.4, 8)
    o += T(790, 88, '綠＝抗、紅＝推', 15, INK, 'middle', 'bold')
    o += T(790, 120, f"Σ抗 = {d['ScL'] + d['SNt']:.1f}", 15, TEN, 'middle', 'bold')
    o += T(790, 150, f"Σ推 = {d['SWs']:.1f}", 15, COMP, 'middle', 'bold')
    o += T(790, 190, f"FS = {d['FS']:.3f}", 18, KEY, 'middle', 'bold')
    o += T(790, 222, '上方片推、下方片擋', 14, INK, 'middle')
    o += T(790, 244, '片 5 只擋不推', 14, INK, 'middle')
    return svg(W_, H, o, 'SM-2021-4 各切片抗力與推力')


def fig6_3():
    d = ex2021_4()
    fs, hist = bishop()
    W_, H = 900, 340
    n = len(hist)
    pl = Plot(100, 50, 520, 230, 0, n, 0.9, 1.15)
    o = pl.axes(list(range(0, n + 1)), [0.9, 1.0, 1.1], '迭代次數', 'FS')
    pts = [pl.pt(0, 1.0)] + [pl.pt(i + 1, v) for i, v in enumerate(hist)]
    o += P(pts, KEY, 3)
    for i, v in enumerate(hist):
        o += pl.dot(i + 1, v, KEY, 4)
    o += pl.dot(0, 1.0, MUT, 4)
    o += T(pl.X(0) + 8, pl.Y(1.0) + 20, '起始猜 1.0', 14, MUT, 'start')
    o += pl.hline(d['FS'], 0, n, TEN, 2, '6 4')
    o += T(pl.X(n), pl.Y(d['FS']) + 22, f"Fellenius {d['FS']:.3f}", 14, TEN, 'end', 'bold')
    o += T(pl.X(n), pl.Y(fs) - 12, f'Bishop 收斂 {fs:.3f}', 14, KEY, 'end', 'bold')
    o += R(650, 70, 240, 140, KEY2, KEY, 1.4, 8)
    o += T(770, 100, 'FS 出現在等號兩邊', 15, KEY, 'middle', 'bold')
    o += T(770, 130, '猜 → 算 → 代回', 15, INK, 'middle')
    o += T(770, 160, f'Bishop 高 {(fs / d["FS"] - 1) * 100:.0f}%', 15, INK, 'middle')
    o += T(770, 190, '（同一量測表，示範）', 14, MUT, 'middle')
    return svg(W_, H, o, 'Bishop 簡化法迭代')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
