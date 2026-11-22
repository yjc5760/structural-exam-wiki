# -*- coding: utf-8 -*-
"""第 4 章：最小鋼筋量——開裂即斷裂。"""
from figs_common import *  # noqa
from calcs import demo_beam, mn_rect
import math

D = demo_beam()


def fig4_1():
    W, H = 900, 430
    o = T(450, 24, '同一個 40×60 斷面，鋼筋很少的時候：開裂後鋼筋接得住嗎？', 16, INK, 'middle', 'bold')
    # 左：開裂前後的應力分布示意
    x0, y0, sc = 70, 80, 4.2
    o += section(x0 + 84, y0, sc, 40, 60)
    o += T(x0 + 84, y0 - 12, '開裂前（S6 之前）', 15, INK, 'middle', 'bold')
    xs = x0 + 270
    hh = 60 * sc
    o += L(xs, y0, xs, y0 + hh, MUT, 1.2)
    o += P([(xs, y0), (xs - 60, y0), (xs, y0 + hh / 2)], COMP, 2, fill=COMP2, close=True)
    o += P([(xs, y0 + hh / 2), (xs + 60, y0 + hh), (xs, y0 + hh)], TEN, 2, fill=TEN2, close=True)
    o += T(xs + 64, y0 + hh + 5, '*f*_{r}', 16, TEN, 'start', 'bold')
    o += T(xs - 60, y0 + hh + 34, '混凝土自己受拉', 14, TEN, 'start')
    # 右：圖表
    pl = Plot(450, 70, 330, 280, 0, 10, 0, 20)
    o += pl.axes([0, 2, 4, 6, 8, 10], [0, 5, 10, 15, 20], '*A*_{s}', '(tf·m)', size=14)
    o += T(pl.X(10) + 20, pl.Y(0) + 26, '(cm²)', 14, MUT, 'start')
    o += pl.curve(lambda A: 0.9 * mn_rect(A) / 1e5, 0, 10, AC, 3.2)
    mcr = D['Mcr'] / 1e5
    o += pl.hline(mcr, 0, 10, COMP, 2, '6 4')
    o += T(pl.X(0.3), pl.Y(mcr) - 8, f"*M*_{{cr}} = {mcr:.2f}", 14, COMP, 'start', 'bold')
    o += pl.hline(1.2 * mcr, 0, 10, WARN, 1.6, '3 3')
    o += T(pl.X(0.3), pl.Y(1.2 * mcr) - 8, f"1.2*M*_{{cr}} = {1.2*mcr:.2f}", 14, WARN, 'start', 'bold')
    Ax = mcr * 1e5 / (4200 * (D['d'] - 2))
    o += pl.vline(D['Asmin'], 0, 20, TEN, 1.6)
    o += pl.dot(D['Asmin'], 0.9 * D['Mn_min'] / 1e5, TEN, 6)
    o += T(pl.X(D['Asmin']) + 8, pl.Y(0.9 * D['Mn_min'] / 1e5) + 22, f"*A*_{{s,min}} = {D['Asmin']:.2f}", 14, TEN, 'start', 'bold')
    o += T(pl.X(D['Asmin']) + 8, pl.Y(0.9 * D['Mn_min'] / 1e5) + 42, f"φ*M*_{{n}} = {0.9*D['Mn_min']/1e5:.2f}", 14, TEN, 'start', 'bold')
    o += T(pl.X(6.5), pl.Y(5.5), 'φ*M*_{n}', 16, AC, 'start', 'bold')
    o += pl.area(lambda A: min(20, mcr), lambda A: 0.9 * mn_rect(A) / 1e5, 0.01, 4.0, COMP2, 0.7)
    o += T(pl.X(1.3), pl.Y(mcr) + 28, '危險區', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, 'Mcr 與 As,min')


def fig4_2():
    W, H = 900, 380
    pl = Plot(110, 50, 560, 270, 140, 560, 10, 20)
    o = pl.axes([140, 210, 280, 350, 420, 490, 560], [10, 12, 14, 16, 18, 20], "*f*′_{c}", 'ρ_{min}·*f*_{y}', size=14)
    o += pl.curve(lambda fc: 0.8 * math.sqrt(fc), 140, 560, AC, 3)
    o += pl.curve(lambda fc: 14, 140, 560, TEN, 3)
    o += pl.curve(lambda fc: max(14, 0.8 * math.sqrt(fc)), 140, 560, KEY, 6, op=0.35)
    fx = (14 / 0.8) ** 2
    o += pl.dot(fx, 14, KEY, 6)
    o += T(pl.X(fx), pl.Y(14) + 28, f"交點 *f*′_{{c}} = (14/0.8)^{{2}} ≈ {fx:.0f}", 15, KEY, 'middle', 'bold')
    o += T(pl.X(170), pl.Y(14) - 10, '14（定值）', 15, TEN, 'start', 'bold')
    o += T(pl.X(540), pl.Y(0.8 * math.sqrt(540)) - 12, '0.8√*f*′_{c}', 15, AC, 'end', 'bold')
    o += box(700, 70, 185, 200, '取大（紫色粗線）', ['常見 210～280：', '14/*f*_{y} 控制', '350 以上：', '0.8√*f*′_{c}/*f*_{y} 控制', '兩個都算，', '心裡知道誰會贏'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'As,min 兩式')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
