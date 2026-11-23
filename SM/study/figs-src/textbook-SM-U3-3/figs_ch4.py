# -*- coding: utf-8 -*-
"""第 4 章：擬靜態地震力分解、FS–kh 與地錨。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig4_1():
    d = ex2008_4()
    W_, H = 900, 460
    sc = 34
    ox, oy = 90, 400
    P2 = lambda x, y: (ox + x * sc, oy - y * sc)
    A_ = (0, 0)
    B_ = (d['LAB'] * cos(70), d['LAB'] * sin(70))
    C_ = (d['LAC'] * cos(40), d['LAC'] * sin(40))
    o = ''
    o += P([P2(-2, 0), P2(*A_), P2(*B_), P2(*C_), P2(15, C_[1] + (15 - C_[0]) * tan(5)), P2(15, -1.5), P2(-2, -1.5)], SOILE, 1.4, fill=SOIL, close=True)
    o += P([P2(*A_), P2(*B_), P2(*C_)], COMP, 2.2, fill=COMP2, close=True)
    o += L(*P2(*A_), *P2(*C_), COMP, 3)
    for nm, pt, dx, dy in [('A', A_, -16, 18), ('B', B_, -10, -10), ('C', C_, 8, -10)]:
        x, y = P2(*pt)
        o += T(x + dx, y + dy, nm, 17, INK, 'middle', 'bold')
    gx = (A_[0] + B_[0] + C_[0]) / 3
    gy = (A_[1] + B_[1] + C_[1]) / 3
    G = P2(gx, gy)
    Lw = 120
    o += A(G[0], G[1], G[0], G[1] + Lw, INK, 3, 12)
    o += T(G[0] + 8, G[1] + Lw + 6, f"*W* = {d['W']:.2f}", 15, INK, 'start', 'bold')
    Lk = Lw * d['kh']
    o += A(G[0], G[1], G[0] - Lk * 2.2, G[1], COMP, 3, 12)
    o += T(G[0] - Lk * 2.2 - 6, G[1] - 8, f"*k*_{{h}}*W* = {d['Fh']:.2f}", 15, COMP, 'end', 'bold')
    # direction of AC downslope (screen): toward A
    ux, uy = -cos(40), sin(40)
    nx, ny = sin(40), cos(40)        # into plane (screen, down-right)
    sx, sy = P2(*C_)
    mx, my = (P2(*A_)[0] + sx) / 2, (P2(*A_)[1] + sy) / 2
    # anchor perpendicular into plane from the slope face side
    ax0, ay0 = mx - nx * 70 + 40 * ux, my - ny * 70 + 40 * uy
    o += A(ax0, ay0, mx + nx * 40 + 40 * ux, my + ny * 40 + 40 * uy, WARN, 3.2, 12)
    o += T(mx + nx * 40 + 40 * ux + 14, my + ny * 40 + 40 * uy - 4, '地錨 ⊥ 滑動面', 15, WARN, 'start', 'bold')
    o += T(P2(3.2, 1.2)[0] + 40, P2(3.2, 1.2)[1] + 30, '40°', 16, COMP, 'start', 'bold')
    o += R(600, 40, 290, 250, KEY2, KEY, 1.4, 8)
    o += T(745, 68, '沿 AC 拆兩個力', 16, KEY, 'middle', 'bold')
    o += T(745, 100, '推：*W* sin 40° + *k*_{h}*W* cos 40°', 15, COMP, 'middle')
    o += T(745, 126, f"= {d['Td']:.2f}", 15, COMP, 'middle', 'bold')
    o += T(745, 158, '壓：*W* cos 40° − *k*_{h}*W* sin 40°', 15, AC, 'middle')
    o += T(745, 184, f"= {d['N']:.2f}", 15, AC, 'middle', 'bold')
    o += T(745, 218, f"*L*_{{AC}} = {d['LAC']:.3f} m", 15, INK, 'middle')
    o += T(745, 250, f"FS = {d['FS']:.2f}", 18, KEY, 'middle', 'bold')
    o += T(745, 278, '地震力：推變多、壓變少', 14, INK, 'middle')
    return svg(W_, H, o, 'SM-2008-4 擬靜態地震力分解')


def fig4_2():
    d = ex2008_4()
    W_, H = 900, 380
    def FS(kh, P=0.0):
        Td = d['W'] * sin(40) + kh * d['W'] * cos(40)
        N = d['W'] * cos(40) - kh * d['W'] * sin(40) + P
        return (d['c'] * d['LAC'] + N * tan(d['phi'])) / Td
    pl = Plot(80, 60, 330, 260, 0, 0.3, 0, 1.4)
    o = T(245, 30, '(a) FS 隨 *k*_{h} 下降', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 0.1, 0.2, 0.3], [0, 0.4, 0.8, 1.2], '*k*_{h}', 'FS')
    o += pl.curve(lambda k: FS(k), 0, 0.3, KEY, 3)
    o += pl.curve(lambda k: (d['c'] * d['LAC'] + d['N0'] * tan(d['phi'])) / (d['W'] * sin(40) + k * d['W'] * cos(40)), 0, 0.3, COMP, 2, '6 4')
    o += pl.dot(0, d['FS0'], KEY, 5)
    o += T(pl.X(0) + 10, pl.Y(d['FS0']) - 10, f"常時 {d['FS0']:.2f}", 14, KEY, 'start', 'bold')
    o += pl.dot(0.2, d['FS'], KEY, 6)
    o += T(pl.X(0.2) - 6, pl.Y(d['FS']) + 26, f"0.2 → {d['FS']:.2f}", 14, KEY, 'end', 'bold')
    o += T(pl.X(0.3), pl.Y(0.92) - 22, '紅虛線：只加推力（錯）', 14, COMP, 'end')
    pl2 = Plot(520, 60, 330, 260, 0, 500, 0, 1.4)
    o += T(685, 30, '(b) 每公尺地錨力 *P* 與 FS', 16, INK, 'middle', 'bold')
    o += pl2.axes([0, 100, 200, 300, 400, 500], [0, 0.4, 0.8, 1.2], '*P*', 'FS')
    o += pl2.curve(lambda P: FS(0.2, P), 0, 500, WARN, 3)
    o += pl2.hline(1.2, 0, 500, COMP, 1.6, '6 4')
    o += pl2.dot(d['P'], 1.2, WARN, 6)
    o += pl2.vline(d['P'], 0, 1.2, WARN, 1.4, '4 3')
    o += T(pl2.X(d['P']) - 8, pl2.Y(0.3), f"*P* = {d['P']:.2f} kN/m", 14, WARN, 'end', 'bold')
    o += T(pl2.X(d['P']) - 8, pl2.Y(0.15), f"× 2 m = {d['Tanchor']:.2f} kN/支", 14, WARN, 'end', 'bold')
    return svg(W_, H, o, 'SM-2008-4 地震係數與地錨力')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
