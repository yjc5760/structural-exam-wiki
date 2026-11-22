# -*- coding: utf-8 -*-
"""第 10 章：直線 vs 曲線鋼腱。"""
from figs_ps import *  # noqa
from calcs import rc2010_4

RR = rc2010_4(); W = RR['W']


def fig10_1():
    Wd, H = 900, 440
    o = T(450, 26, 'RC-2010-4：沿梁長的偏心可行區（綠），直線鋼腱被梁端卡住，曲線鋼腱可以跟著彎矩走', 16, INK, 'middle', 'bold')
    L = 1500.0; Pi = 200000.0; Pe = W['Pe']; A = W['A']; S = W['S']; al = W['al']
    wG = W['wG']; wL = 15.0
    MG = lambda x: wG * x * (L - x) / 2
    MT = lambda x: (wG + wL) * x * (L - x) / 2
    eup = lambda x: (Pi / A + MG(x) / S + al['ti']) * S / Pi
    elo = lambda x: (MT(x) / S - al['tU'] - Pe / A) * S / Pe
    pl = Plot(110, 70, 520, 300, 0, 1500, 40, -40)
    # y 軸向下為正 → 用 ymin=40,ymax=-40 讓下方為正值
    o += pl.axes([0, 375, 750, 1125, 1500], [-40, -20, 0, 20, 40], '*x*（cm）', '*e*（cm，下為正）', yfmt=lambda v: f'{v:g}'.replace('-', '−'), size=14)
    pts = [pl.pt(1500 * i / 200, eup(1500 * i / 200)) for i in range(201)] + [pl.pt(1500 * i / 200, max(elo(1500 * i / 200), -40)) for i in range(200, -1, -1)]
    o += P(pts, None, fill=TEN2, close=True, op=0.9)
    o += pl.curve(eup, 0, 1500, COMP, 2.4, clip=False)
    o += pl.curve(lambda x: max(elo(x), -40), 0, 1500, AC, 2.4, clip=False)
    o += pl.hline(RR['es'], 0, 1500, WARN, 3, None)
    ec = RR['ec']
    o += pl.curve(lambda x: 4 * ec * x * (L - x) / L ** 2, 0, 1500, KEY, 3, dash='8 5', clip=False)
    o += T(pl.X(1490), pl.Y(RR['es']) - 8, f"直線 {RR['es']:.2f}", 14, WARN, 'end', 'bold')
    o += T(pl.X(750), pl.Y(27), f"曲線鋼腱跨中 *e* = {ec:.2f}", 14, KEY, 'middle', 'bold')
    o += T(pl.X(1120), pl.Y(eup(1120)) + 22, '上限（傳遞頂拉）', 14, COMP, 'start', 'bold')
    o += T(pl.X(1490), pl.Y(elo(1460)) - 8, '下限（使用底拉）', 14, AC, 'end', 'bold')
    o += box(706, 80, 186, 290, '差多少', [f"Δ*e* = {ec:.2f} − {RR['es']:.2f}", f"= {ec - RR['es']:.2f} = *M*_{{G}}/*P*_{{i}}", f"Δ*M* = *P*_{{e}}Δ*e* = {tfm(RR['dM']):.2f}", '= η*M*_{G} tf·m', '', f"曲線 *M*_{{L}} ≤ {tfm(RR['MLc']):.2f}", f"直線 *M*_{{L}} ≤ {tfm(RR['MLs']):.2f}"], KEY2, KEY, 15, 14.5)
    return svg(Wd, H, o, '直線與曲線鋼腱')


ALL = {'fig10_1': fig10_1}
