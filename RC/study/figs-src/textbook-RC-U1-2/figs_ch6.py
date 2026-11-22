# -*- coding: utf-8 -*-
"""第 6 章：柱曲率韌性。"""
from figs_col import *  # noqa
from calcs import rc2011_3, mu_phi_2011

R3 = rc2011_3()


def fig6_1():
    W, H = 900, 460
    o = T(450, 26, 'RC-2011-3：同一個軸力 *N* = 206.0 tf 下的兩張應變圖', 16, INK, 'middle', 'bold')
    y0, sc = 92, 4.5
    h, d = 60, 54
    for k, (xa, title, cdep, top, col, lab) in enumerate([
            (250, '(a) 降伏：最外拉力筋到 ε_{y}', R3['k'], R3['ec_y'], AC, f"φ_{{y}} = ε_{{y}}/(*d* − *kd*) = {R3['phy']*1e5:.3f}×10^{{-5}}"),
            (650, '(b) 極限：頂緣到 0.003', R3['cu'], 0.003, COMP, f"φ_{{u}} = 0.003/*c* = {R3['phu']*1e4:.3f}×10^{{-4}}")]):
        o += T(xa, 54, title, 15, INK, 'middle', 'bold')
        o += R(xa - 150, y0, 40, h * sc, STEEL2, INK, 1.2)
        kk = 60 / 0.003
        xz = xa
        yb = y0 + h * sc
        o += L(xz, y0, xz, yb, MUT, 1.2, '4 3')
        bot = -top * (h - cdep) / cdep
        xt = xz - kk * top; xb = xz - kk * bot
        o += P([(xz, y0), (xt, y0), (xz, y0 + cdep * sc)], None, fill=COMP2, close=True)
        o += P([(xz, y0 + cdep * sc), (xb, yb), (xz, yb)], None, fill=TEN2, close=True)
        o += L(xt, y0, xb, yb, col, 2.6)
        o += T(xt - 6, y0 - 4, f'{top:.5f}'.rstrip('0'), 14, COMP, 'end', 'bold')
        ed = -top * (d - cdep) / cdep
        o += C(xz - kk * ed, y0 + d * sc, 4, TEN, '#fff', 1)
        o += T(xz - kk * ed + 8, y0 + d * sc + 5, f'{-ed:.5f}', 14, TEN, 'start', 'bold')
        o += L(xz - 160, y0 + cdep * sc, xz + 10, y0 + cdep * sc, MUT, 1.2, '6 4')
        o += T(xz - 160, y0 + cdep * sc - 6, (f"*kd* = {cdep:.2f}" if k == 0 else f"*c* = {cdep:.2f}"), 14, col, 'start', 'bold')
        o += T(xa, yb + 30, lab, 14, col, 'middle', 'bold')
    o += T(450, 445, f"μ_{{φ}} = φ_{{u}}/φ_{{y}} = {R3['mu']:.2f}　（(a) 用彈性三角形應力、(b) 用 Whitney 應力塊，不可混用）", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '兩條中性軸')


def fig6_2():
    W, H = 900, 400
    o = T(450, 26, '同一根柱，軸力越大，曲率韌性越差（RC-2011-3 斷面逐點算出）', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 560, 280, 0, 300, 0, 8)
    o += pl.axes([0, 50, 100, 150, 200, 250, 300], [0, 2, 4, 6, 8], '*N*（tf）', 'μ_{φ}', size=14)
    o += pl.curve(lambda N: mu_phi_2011(N * 1000)['mu'], 0, 300, AC, 3.2, n=60)
    o += pl.dot(R3['N'] / 1000, R3['mu'], COMP, 7)
    o += T(pl.X(R3['N'] / 1000) + 10, pl.Y(R3['mu']) - 12, f"本題 *N* = {R3['N']/1000:.1f}：{R3['mu']:.2f}", 14, COMP, 'start', 'bold')
    m0 = mu_phi_2011(0.0)['mu']
    o += pl.dot(0, m0, TEN, 7)
    o += T(pl.X(0) + 12, pl.Y(m0) + 5, f'純彎 {m0:.2f}', 14, TEN, 'start', 'bold')
    o += box(680, 80, 210, 220, '為什麼', ['軸力把中性軸往下推', '*c* 變大 → φ_{u} 變小', '*kd* 也變大 → φ_{y}', '變大', '兩頭夾擊', '→ μ_{φ} 下降'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'μφ 隨軸力')


def fig6_3():
    W, H = 900, 380
    o = T(450, 26, '塑鉸模型：把曲率分布換成「彈性三角形＋底部一塊 *L*_{p} 長的矩形」', 16, INK, 'middle', 'bold')
    x0, y0, Lpx, Lpx_p = 120, 70, 260, 50
    o += R(x0, y0, 40, Lpx, STEEL2, INK, 1.4)
    o += fixed_wall(x0 + 20, y0 + Lpx, 100)
    o += A(x0 - 40, y0 + 10, x0 - 4, y0 + 10, COMP, 2.6, 10)
    o += T(x0 - 44, y0 + 15, '*V*', 15, COMP, 'end', 'bold')
    o += T(x0 + 20, y0 - 10, '懸臂柱 *L*', 14, INK, 'middle', 'bold')
    xa = 360
    yb = y0 + Lpx
    o += L(xa, y0, xa, yb, INK, 1.4)
    o += P([(xa, y0), (xa + 80, yb), (xa, yb)], AC, 2, fill=AC2, close=True)
    o += R(xa, yb - Lpx_p, 240, Lpx_p, WARN2, WARN, 2)
    o += T(xa + 84, yb + 22, 'φ_{y}', 15, AC, 'middle', 'bold')
    o += T(xa + 240, yb + 22, 'φ_{u}', 15, WARN, 'middle', 'bold')
    o += vdim(xa + 250, yb - Lpx_p, yb, '*L*_{p}', WARN, 1)
    o += T(xa + 120, yb - Lpx_p - 10, '塑性曲率 φ_{u} − φ_{y}', 14, WARN, 'middle', 'bold')
    o += box(660, 70, 230, 270, '積分曲率得位移', ['Δ_{y} = φ_{y}*L*^{2}/3', 'θ_{p} = (φ_{u} − φ_{y})*L*_{p}', 'Δ_{p} = θ_{p}(*L* − *L*_{p}/2)', '', 'μ_{Δ} = 1 + 3(μ_{φ} − 1)', '× (*L*_{p}/*L*)(1 − *L*_{p}/2*L*)'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '塑鉸模型')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
