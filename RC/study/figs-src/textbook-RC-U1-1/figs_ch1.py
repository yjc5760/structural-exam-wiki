# -*- coding: utf-8 -*-
"""第 1 章：極限狀態的斷面——平面保持平面、0.003、鋼筋彈塑性、等值應力塊、β1。"""
from figs_common import *  # noqa
from calcs import demo_beam, hognestad, stress_block_equiv, beta1, block_compare, ES

D = demo_beam()


def fig1_1():
    W, H = 900, 400
    sc = 4.6
    y0 = 70
    o = T(450, 26, '示範梁在極限狀態：頂緣壓到 0.003 的那一瞬間（依比例）', 16, INK, 'middle', 'bold')
    xs = 150
    o += section(xs, y0, sc, D['b'], D['h'])
    o += bars(xs, y0 + D['d'] * sc, sc, D['b'], 4, 2.54, TEN)
    o += T(xs, y0 - 12, '斷面 40×60', 15, INK, 'middle', 'bold')
    o += vdim(xs + D['b'] * sc / 2 + 16, y0, y0 + D['d'] * sc, '*d* = 53', INK, 1)
    o += L(xs - D['b'] * sc / 2 - 12, y0 + D['c'] * sc, 520, y0 + D['c'] * sc, MUT, 1.2, '6 4')
    o += T(xs - D['b'] * sc / 2 - 16, y0 + D['c'] * sc + 5, '中性軸', 14, MUT, 'end')
    xa = 430
    s, k, ex = strain_panel(xa, y0, sc, D['h'], D['c'], [(D['d'], D['et'], f"ε_{{t}} = {D['et']:.4f}", TEN)], emax_px=170)
    o += s
    o += T(xa, y0 + D['h'] * sc + 30, '應變（直線＝種子 S1）', 15, INK, 'middle', 'bold')
    # 相似三角形標示
    yc = y0 + D['c'] * sc
    o += vdim(xa - k * 0.003 - 18, y0, yc, '*c*', COMP, -1)
    o += vdim(xa + 22, yc, y0 + D['d'] * sc, '*d* − *c*', TEN, 1)
    o += box(640, 110, 240, 190, '相似三角形', ['ε 與「到中性軸的距離」', '成正比：', 'ε_{t} / (*d* − *c*) = 0.003 / *c*', f"*c* = {D['c']:.2f} cm（第 2 章）", f"→ ε_{{t}} = {D['et']:.4f}"], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '平面保持平面')


def fig1_2():
    W, H = 900, 400
    o = T(225, 26, '(a) 混凝土（受壓）', 16, INK, 'middle', 'bold')
    o += T(680, 26, '(b) 鋼筋 SD420（拉、壓相同）', 16, INK, 'middle', 'bold')
    fc = D['fc']
    pl = Plot(70, 60, 330, 260, 0, 0.0036, 0, 300)
    o += pl.axes([0, 0.001, 0.002, 0.003], [0, 140, 280], 'ε', 'σ', xfmt=lambda v: f'{v:.3f}' if v else '0',
                 yfmt=lambda v: {280: "*f*′_{c}"}.get(v, f(v)))
    o += pl.curve(lambda e: hognestad(e, fc), 0, 0.003, COMP, 3.2)
    o += pl.curve(lambda e: hognestad(e, fc), 0.003, 0.0035, COMP, 2, dash='5 4')
    o += pl.vline(0.003, 0, hognestad(0.003, fc), COMP, 1.6)
    o += pl.dot(0.003, hognestad(0.003, fc), COMP, 6)
    o += T(pl.X(0.003) + 4, pl.Y(hognestad(0.003, fc)) - 16, '0.003 壓碎', 15, COMP, 'middle', 'bold')
    o += T(pl.X(0.002), pl.Y(285) - 4, '峰值約 0.002', 14, MUT, 'middle')
    o += T(pl.X(0.0012), pl.Y(80), '曲線：用 S5', 14, COMP, 'start')
    o += T(pl.X(0.0012), pl.Y(80) + 20, '換成長方形', 14, COMP, 'start')
    ey = D['fy'] / ES
    p2 = Plot(520, 60, 330, 260, 0, 0.010, 0, 5000)
    o += p2.axes([0, ey, 0.005, 0.010], [0, 4200], 'ε', 'σ', xfmt=lambda v: {0: '0', 0.005: '0.005', 0.010: '0.010'}.get(v, 'ε_{y}'),
                 yfmt=lambda v: {4200: '*f*_{y}'}.get(v, '0'))
    o += P([p2.pt(0, 0), p2.pt(ey, 4200), p2.pt(0.010, 4200)], TEN, 3.2)
    o += T(p2.X(ey) + 10, p2.Y(2200), f'斜率 *E*_{{s}} = 2.04×10^{{6}}', 14, TEN, 'start')
    o += T(p2.X(ey) + 10, p2.Y(2200) + 22, f'ε_{{y}} = 4200/2.04×10^{{6}} = {ey:.5f}', 14, TEN, 'start')
    o += T(p2.X(0.0065), p2.Y(4200) - 12, '降伏後：力不再增加', 14, TEN, 'middle', 'bold')
    o += T(p2.X(0.0065), p2.Y(4200) + 26, '只會越拉越長（有預警）', 14, MUT, 'middle')
    o += T(450, 382, '左邊管「極限在哪」（0.003）；右邊管「鋼筋出多少力」（*A*_{s}*f*_{y} 或 *A*_{s}*E*_{s}ε）。', 15, INK, 'middle')
    return svg(W, H, o, '材料律')


def fig1_3():
    W, H = 900, 450
    E = stress_block_equiv(D['fc'])
    B = block_compare()
    sc = 13.0     # 1 cm → 13 px，只畫壓力區附近
    c = D['c']; a = D['a']
    y0 = 90
    o = T(450, 26, '把彎曲的壓應力分布換成一塊長方形（示範梁的壓力區，深度依比例）', 16, INK, 'middle', 'bold')
    cols = [(150, '(a) 應變'), (450, '(b) 曲線模型的應力'), (750, '(c) 規範等值應力塊')]
    for x, t in cols:
        o += T(x, 60, t, 15, INK, 'middle', 'bold')
        o += L(x - 120, y0, x - 120, y0 + c * sc + 30, INK, 1.4)
    yc = y0 + c * sc
    # (a) 應變三角形
    x = 30
    o += P([(x, y0), (x + 180, y0), (x, yc)], COMP, 2, fill=COMP2, close=True)
    o += T(x + 184, y0 + 5, '0.003', 15, COMP, 'start', 'bold')
    o += T(x + 126, y0 + c * sc / 3 + 5, '0.002', 14, MUT, 'start')
    o += L(x, y0 + c * sc / 3, x + 120, y0 + c * sc / 3, MUT, 1, '3 3')
    o += L(x - 6, yc, 870, yc, MUT, 1.2, '6 4')
    o += T(x, yc + 22, f"中性軸（*c* = {c:.2f} cm）", 14, MUT, 'start')
    # (b) 曲線
    x = 330
    kx = 200 / D['fc']
    pts = [(x, y0)]
    for i in range(101):
        yy = c * i / 100
        e = 0.003 * (1 - yy / c)
        pts.append((x + kx * hognestad(e, D['fc']), y0 + yy * sc))
    pts.append((x, yc))
    o += P(pts, COMP, 2.4, fill=COMP2, close=True)
    o += L(x + kx * D['fc'], y0 - 4, x + kx * D['fc'], yc, MUT, 1, '3 3')
    o += T(x + kx * D['fc'], y0 - 8, "*f*′_{c}", 14, MUT, 'middle')
    yk = y0 + E['k2'] * c * sc
    o += A(x + 245, yk, x + 20, yk, KEY, 3, 12)
    o += T(x + 160, yk - 10, '合力 *C*', 15, KEY, 'middle', 'bold')
    o += T(x + 10, yc + 50, f"平均應力 {E['k1k3']:.2f}*f*′_{{c}}，合力位置 {E['k2']:.2f}*c*", 14, INK, 'start')
    # (c) Whitney
    x = 630
    o += R(x, y0, kx * 0.85 * D['fc'], a * sc, WARN2, WARN, 2)
    o += L(x + kx * D['fc'], y0 - 4, x + kx * D['fc'], yc, MUT, 1, '3 3')
    o += T(x + kx * 0.85 * D['fc'] / 2, y0 - 8, "0.85*f*′_{c}", 15, WARN, 'middle', 'bold')
    o += vdim(x + kx * 0.85 * D['fc'] + 14, y0, y0 + a * sc, '*a* = β_{1}*c*', WARN, 1)
    ya = y0 + a / 2 * sc
    o += A(x + 160, ya, x + 12, ya, KEY, 3, 12)
    o += T(x + 86, ya - 10, '合力 *C*', 15, KEY, 'middle', 'bold')
    o += T(x + 10, yc + 50, '平均 0.85×0.85 = 0.72*f*′_{c}，位置 0.425*c*', 14, INK, 'start')
    o += box(110, 360, 680, 74, '兩種模型算示範梁的力臂', [f"曲線模型 *z* = {B['z_model']:.2f} cm、規範應力塊 *z* = *d* − *a*/2 = {B['z_code']:.2f} cm：*M*_{{n}} 只差 {B['diff']*100:.1f}%"], KEY2, KEY, 15, 15)
    return svg(W, H, o, '等值應力塊')


def fig1_4():
    W, H = 900, 380
    pl = Plot(100, 60, 560, 250, 140, 700, 0.6, 0.9)
    o = pl.axes([210, 280, 350, 420, 490, 560, 630], [0.65, 0.7, 0.75, 0.8, 0.85], "*f*′_{c}", 'β_{1}',
                yfmt=lambda v: f'{v:.2f}', size=14)
    o += pl.curve(beta1, 140, 700, AC, 3.4, n=400)
    for fc in (280, 560):
        o += pl.dot(fc, beta1(fc), KEY, 6)
    o += T(pl.X(280), pl.Y(0.85) - 14, '高原：≤ 280 取 0.85', 15, KEY, 'middle', 'bold')
    o += T(pl.X(560) + 8, pl.Y(0.65) - 14, '地板：≥ 560 取 0.65', 15, KEY, 'start', 'bold')
    for fc in (350, 420):
        o += pl.dot(fc, beta1(fc), AC, 5)
        o += T(pl.X(fc) + 10, pl.Y(beta1(fc)) - 8, f'{fc} → {beta1(fc):.2f}', 14, AC, 'start', 'bold')
    o += box(690, 80, 190, 170, '中間怎麼走？', ['兩個端點連直線：', '280 → 560 降 0.20', '每 +70 降 0.05', '（MPa：28／56，', '每 7 MPa 降 0.05）'], AC2, AC, 15, 14)
    o += T(380, 360, '0.85 那個「應力」永遠是 0.85*f*′_{c}；β_{1} 只管 *a* = β_{1}*c* 的深度換算', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, 'β1')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
