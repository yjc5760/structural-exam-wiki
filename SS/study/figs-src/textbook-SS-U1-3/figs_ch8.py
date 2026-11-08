# -*- coding: utf-8 -*-
"""第 8 章：LRFD H1 互制。曲線與點全部由 calcs.py 算出。"""
from plot import *  # noqa
from calcs import ex2014, ex2014_cap, ex2020_H1, ex2012, ex2022, H1_curve_M, Mpc_ratio_strong


def fig8_1():
    d = ex2014(); c12 = ex2012(); c22 = ex2022()
    W_, H = 900, 470
    pl = Plot(90, 50, 500, 360, 0, 1.1, 0, 1.1)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0], [0, 0.2, 0.4, 0.6, 0.8, 1.0],
                'Σ*M*_{u}/φ_{b}*M*_{n}', '*P*_{u}/φ_{c}*P*_{n}', size=14)
    o += pl.area(lambda m: (1 - 8 / 9 * m) if m <= 0.9 else 2 * (1 - m), lambda m: 0, 0, 1.0, KEY2, 0.7)
    o += P([pl.pt(0, 1), pl.pt(1, 0)], MUT, 1.6, dash='6 5')
    o += P([pl.pt(0, 1), pl.pt(0.9, 0.2), pl.pt(1, 0)], KEY, 3.6)
    o += pl.hline(0.2, 0, 0.9, c=MUT, w=1.1, dash='3 4') + pl.vline(0.9, 0, 0.2, c=MUT, w=1.1, dash='3 4')
    for (x, y, lab, dx, anc) in ((0, 1, 'A (0, 1)', 10, 'start'), (0.9, 0.2, 'B (0.9, 0.2)', 10, 'start'), (1, 0, 'C (1, 0)', 6, 'start')):
        o += pl.dot(x, y, KEY, 6) + T(pl.X(x) + dx, pl.Y(y) - 10, lab, 15, KEY, anc, 'bold')
    o += T(pl.X(0.42), pl.Y(0.66), '斜率 −8/9（較平）', 14, KEY, 'start')
    o += T(pl.X(0.96) + 4, pl.Y(0.11), '−2（較陡）', 14, KEY, 'start')
    o += T(pl.X(0.62), pl.Y(0.5) + 4, '虛線：*P* + *M* = 1', 14, MUT, 'start')
    pts = [(d['Mux'] / d['phiMn'], d['Pu_ratio'], '2014-4', COMP),
           (c12['mx'] + c12['my'], c12['pr'], '2012-3', AC),
           (c22['m2'] + c22['m3'], c22['pr'], '2022-1', TEN)]
    for x, y, lab, col in pts:
        o += pl.dot(x, y, col, 6) + T(pl.X(x) - 10, pl.Y(y) + 22, lab, 14, col, 'end', 'bold')
    lx = 612
    o += R(lx, 60, 278, 250, '#fff', GRID, 1.2, 8)
    o += T(lx + 139, 88, '三題的需求點', 15, INK, 'middle', 'bold')
    rows = [('2014-4', d['Pu_ratio'], d['Mux'] / d['phiMn'], ex2014_cap()['H1'], COMP),
            ('2012-3', c12['pr'], c12['mx'] + c12['my'], c12['H1'], AC),
            ('2022-1', c22['pr'], c22['m2'] + c22['m3'], c22['H1'], TEN)]
    o += T(lx + 14, 116, '題號　*P*比　Σ*M*比　H1', 14, MUT, 'start')
    for k, (n, p, m, h, col) in enumerate(rows):
        o += T(lx + 14, 146 + k * 30, f'{n}　{p:.3f}　{m:.3f}　{h:.3f}', 14.5, col, 'start', 'bold')
    o += T(lx + 139, 248, '點在紫色區內 ⇒ OK', 15, KEY, 'middle', 'bold')
    o += T(lx + 139, 276, '三題都 *P*比 ≥ 0.2，用上段', 14, INK, 'middle')
    return svg(W_, H, o, 'H1 互制圖')


def fig8_2():
    W_, H = 900, 450
    pl = Plot(90, 50, 500, 340, 0, 1.2, 0, 1.1)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], [0, 0.2, 0.4, 0.6, 0.8, 1.0], '*M*/*M*_{p}', '*P*/*P*_{y}', size=14)
    # 斷面全塑性曲線（W 型鋼強軸近似）：M/Mp = min(1, 1.18(1-p))
    o += P([pl.pt(Mpc_ratio_strong(i / 100), i / 100) for i in range(101)], TEN, 3.4)
    o += P([pl.pt(0, 1), pl.pt(1, 0)], MUT, 1.8, dash='6 5')
    o += P([pl.pt(0, 1), pl.pt(0.9, 0.2), pl.pt(1, 0)], KEY, 3.2)
    o += T(pl.X(1.02), pl.Y(0.42), '斷面真正撐得住', 15, TEN, 'start', 'bold')
    o += T(pl.X(1.02), pl.Y(0.42) + 22, '1.18(1 − *P*/*P*_{y}) ≤ 1', 14, TEN, 'start')
    o += T(pl.X(0.15), pl.Y(0.35), '直線 *P* + *M* = 1', 14, MUT, 'start')
    o += T(pl.X(0.15), pl.Y(0.35) + 22, '（太保守）', 14, MUT, 'start')
    o += T(pl.X(0.55), pl.Y(0.72), 'H1 兩段', 15, KEY, 'start', 'bold')
    lx = 640
    o += R(lx, 60, 250, 300, KEY2, KEY, 1.4, 8)
    o += T(lx + 125, 88, '種子 S6 的兩個事實', 15, KEY, 'middle', 'bold')
    for k, s in enumerate(['① 真正的容量曲線往外凸', '　⇒ 兩端點連直線一定安全', '② 軸力小時，彎矩幾乎', '　不被折減（綠線平台）', '⇒ 下段改用較寬的線', '　*P*/2 + *M* = 1', '⇒ 上段取 *P* + (8/9)*M* = 1']):
        o += T(lx + 16, 124 + k * 30, s, 14, INK if k < 4 else KEY, 'start', 'bold' if k >= 4 else None)
    o += T(450, 438, '粗短柱示意（*P*_{n} ≈ *P*_{y}、φ 取 1）；細長柱的 *P*_{n} 由柱曲線決定、*M* 由 *B*_{1}、*B*_{2} 放大', 14, MUT, 'middle')
    return svg(W_, H, o, '為什麼是兩段')


def fig8_3():
    r = ex2020_H1()
    W_, H = 900, 420
    pl = Plot(90, 50, 420, 320, 0, 0.5, 0, 0.5)
    o = pl.axes([0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 0.1, 0.2, 0.3, 0.4, 0.5], '*M*_{ux}/φ_{b}*M*_{nx}', '*M*_{uy}/φ_{b}*M*_{ny}', size=14)
    lim = 9 / 8 * (1 - r['pr'])
    o += pl.area(lambda m: lim - m, lambda m: 0, 0, lim, KEY2, 0.7)
    o += P([pl.pt(0, lim), pl.pt(lim, 0)], KEY, 3.2)
    o += pl.vline(r['mx'], 0, r['my_allow'], c=COMP, w=1.4)
    o += pl.dot(r['mx'], r['my_allow'], COMP, 7)
    o += T(pl.X(r['mx']) + 12, pl.Y(r['my_allow']) - 10, f'({r["mx"]:.3f}, {r["my_allow"]:.3f})', 15, COMP, 'start', 'bold')
    o += T(pl.X(0.02), pl.Y(lim) - 10, f'兩軸比之和 ≤ (9/8)(1 − {r["pr"]:.3f}) = {lim:.3f}', 14, KEY, 'start', 'bold')
    o += R(540, 60, 345, 300, '#fff', COMP, 1.6, 10)
    lines = [('SS-2020-3 反求 *M*_{wy}', COMP, 'bold'),
             (f'*P*_{{u}}/φ_{{c}}*P*_{{n}} = 240/{r["phiPn"]:.1f} = {r["pr"]:.3f}', INK, None),
             (f'強軸：1.017×960/{r["phiMnx"]:.0f} = {r["mx"]:.3f}', INK, None),
             (f'弱軸可用：{lim:.3f} − {r["mx"]:.3f} = {r["my_allow"]:.3f}', INK, None),
             (f'*M*_{{uy}} = {r["my_allow"]:.3f}×{r["phiMny"]:.0f} = {r["Muy"]:.0f} tf·cm', INK, None),
             ('（*B*_{1y} = 1.0，不再放大）', MUT, None),
             (f'*M*_{{wy}} = {r["Muy"]:.0f} ÷ 1.6 ÷ 100 = {r["Mwy"]:.2f} tf·m', KEY, 'bold')]
    for k, (s, c, w) in enumerate(lines):
        o += T(556, 94 + k * 38, s, 15 if w else 14.5, c, 'start', w)
    return svg(W_, H, o, '雙軸反求')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3}
