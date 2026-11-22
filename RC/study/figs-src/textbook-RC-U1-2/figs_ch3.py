# -*- coding: utf-8 -*-
"""第 3 章：特徵點與整條曲線。"""
from figs_col import *  # noqa
from calcs import demo, ES

R0 = demo(); D = R0['D']


def fig3_1():
    W, H = 900, 560
    o = T(450, 26, '示範柱的整條標稱互制圖與六個特徵點', 16, INK, 'middle', 'bold')
    pl = Plot(110, 60, 540, 430, 0, 40, -200, 600)
    o += pm_axes(pl, [0, 10, 20, 30, 40], [-200, -100, 0, 100, 200, 300, 400, 500, 600])
    # 壓力控制區上色
    o += pm_curve(pl, D, AC, 3.4)
    o += pl.hline(tf(R0['Pmax']), 0, tfm(R0['s_cap']['M']), COMP, 2.6, None)
    o += T(pl.X(0.5), pl.Y(tf(R0['Pmax'])) + 20, f"0.80*P*_{{0}} = {tf(R0['Pmax']):.1f} 截頂", 14, COMP, 'start', 'bold')
    pts = [(0, tf(R0['P0']), f"① *P*_{{0}} = {tf(R0['P0']):.1f}", INK, 'start', 10, -6),
           (tfm(R0['s32']['M']), tf(R0['s32']['P']), '② ε_{t} = 0', COMP, 'start', 12, -6),
           (tfm(R0['sb']['M']), tf(R0['sb']['P']), f"③ 平衡點 ({tfm(R0['sb']['M']):.1f}, {tf(R0['sb']['P']):.1f})", KEY, 'end', -12, -12),
           (tfm(R0['st']['M']), tf(R0['st']['P']), f"④ ε_{{t}} = 0.005 ({tfm(R0['st']['M']):.1f}, {tf(R0['st']['P']):.1f})", WARN, 'end', -12, -10),
           (tfm(R0['s0']['M']), 0, f"⑤ 純彎 {tfm(R0['s0']['M']):.2f}", TEN, 'end', -12, 18)]
    for M, Pv, lab, col, anc, dx, dy in pts:
        o += pl.dot(M, Pv, col, 7)
        o += T(pl.X(M) + dx, pl.Y(Pv) + dy, lab, 14, col, anc, 'bold')
    # 純拉
    Pt = -D.fy * D.Ast
    o += pl.dot(0, tf(Pt), TEN, 7)
    o += T(pl.X(0) + 12, pl.Y(tf(Pt)) + 5, f'⑥ 純拉 −*f*_{{y}}*A*_{{st}} = {tf(Pt):.1f}', 14, TEN, 'start', 'bold')
    # eb 射線
    eb = R0['sb']['e']
    o += L(pl.X(0), pl.Y(0), pl.X(38), pl.Y(38 * 100 / eb), KEY, 1.4, '6 4')
    o += T(pl.X(2), pl.Y(2 * 100 / eb) - 10, f'*e*_{{b}} = {eb:.1f} cm', 14, KEY, 'start')
    o += box(668, 90, 220, 260, '平衡點把曲線切兩半', ['上半：*e* < *e*_{b}', '拉力筋未降伏', '壓力控制', '', '下半：*e* > *e*_{b}', '拉力筋已降伏', '過渡區／拉力控制'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '整條互制圖')


def fig3_2():
    W, H = 900, 340
    o = T(450, 26, '平衡點的中性軸：兩個應變一上一下，相似三角形一步就出來', 16, INK, 'middle', 'bold')
    y0, sc = 70, 7.0
    xa = 330
    d = D.dt
    cb = R0['cb']
    k = 50 / 0.001
    yb = y0 + d * sc
    o += L(xa, y0 - 6, xa, yb + 10, MUT, 1.2, '4 3')
    xt = xa - k * 0.003; xbb = xa + k * D.ey
    o += P([(xa, y0), (xt, y0), (xa, y0 + cb * sc)], None, fill=COMP2, close=True)
    o += P([(xa, y0 + cb * sc), (xbb, yb), (xa, yb)], None, fill=TEN2, close=True)
    o += L(xt, y0, xbb, yb, INK, 2.4)
    o += T(xt, y0 - 10, '0.003', 15, COMP, 'middle', 'bold')
    o += T(xbb + 8, yb + 5, 'ε_{y} = *f*_{y}/*E*_{s}', 15, TEN, 'start', 'bold')
    o += vdim(xt - 20, y0, y0 + cb * sc, '*c*_{b}', COMP, -1)
    o += vdim(xt - 70, y0, yb, '*d*_{t}', INK, -1)
    o += L(xa - 8, y0 + cb * sc, xa + 8, y0 + cb * sc, INK, 1.5)
    o += box(520, 70, 360, 190, '推導', ['*c*_{b} / *d*_{t} = 0.003 / (0.003 + ε_{y})', '分子分母同乘 *E*_{s}：', '= 0.003*E*_{s} / (0.003*E*_{s} + *f*_{y})', '0.003 × 2.04×10^{6} = 6120', '*c*_{b} = 6120 *d*_{t} / (6120 + *f*_{y})',
                                     f'示範柱：6120×32/10320 = {cb:.2f} cm'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '平衡點')


def fig3_3():
    W, H = 900, 420
    o = T(450, 26, '*M*_{n} 跟著 *c* 走：上升到平衡點為止，之後下降', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 560, 290, 5, 45, 0, 36)
    o += pl.axes([10, 20, 30, 40], [0, 10, 20, 30], '*c*（cm）', '*M*_{n}（tf·m）', size=14)
    o += pl.curve(lambda c: tfm(D.at(c)['M']), 6.0, 45, AC, 3.2)
    o += pl.vline(R0['cb'], 0, 36, KEY, 1.6)
    o += pl.dot(R0['cb'], tfm(R0['Mpk']), KEY, 7)
    o += T(pl.X(R0['cb']) + 10, pl.Y(tfm(R0['Mpk'])) - 10, f"峰值 {tfm(R0['Mpk']):.2f} @ *c* = {R0['c_Mpk']:.2f} = *c*_{{b}}", 14, KEY, 'start', 'bold')
    o += T(pl.X(12), pl.Y(8), '拉力筋已降伏：', 14, TEN, 'middle', 'bold')
    o += T(pl.X(12), pl.Y(8) + 20, '*T* 固定，*C* 長大', 14, TEN, 'middle')
    o += T(pl.X(33), pl.Y(8), '拉力筋未降伏：', 14, COMP, 'middle', 'bold')
    o += T(pl.X(33), pl.Y(8) + 20, '*T* 快速縮水', 14, COMP, 'middle')
    o += box(680, 80, 210, 220, '為什麼', ['*c* < *c*_{b}：拉力筋', '撐在 *f*_{y}，*c* 加大', '壓力區越大 → *M* 增加', '', '*c* > *c*_{b}：拉力筋', '應力跟著 *c* 下降', '→ *M* 減少'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'Mn 峰值')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
