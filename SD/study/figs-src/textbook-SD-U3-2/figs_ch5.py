# -*- coding: utf-8 -*-
"""第 5 章：斜撐阻尼器、速度型三種變位、BRB vs FVD。"""
from sdfig import *  # noqa
from calcs import Q2018_1, Q2012
import math


def fig5_1():
    W, H = 900, 380
    o = T(230, 26, '斜撐黏滯阻尼器：位移分解', 15.5, INK, 'middle', 'bold')
    x0, yb, Lw, Hh, d = 70, 320, 300, 200, 40
    o += hatch_ground(x0 - 20, yb, Lw + 40)
    o += L(x0, yb, x0, yb - Hh, STEEL, 3, '5 4') + L(x0 + Lw, yb, x0 + Lw, yb - Hh, STEEL, 3, '5 4') + L(x0, yb - Hh, x0 + Lw, yb - Hh, STEEL, 3, '5 4')
    o += L(x0, yb, x0 + d, yb - Hh, AC, 4) + L(x0 + Lw, yb, x0 + Lw + d, yb - Hh, AC, 4) + L(x0 + d, yb - Hh, x0 + Lw + d, yb - Hh, AC, 5)
    mx, my = x0 + Lw * 0.5, yb - Hh * 0.5
    o += L(x0, yb, mx - 22, my + 15, INK, 3) + L(mx + 22, my - 15, x0 + Lw + d, yb - Hh, INK, 3)
    o += R(mx - 26, my - 14, 52, 28, WARN2, WARN, 2, 4) + T(mx, my + 6, '*C*', 15, WARN, 'middle', 'bold')
    o += A(x0 + Lw, yb - Hh - 22, x0 + Lw + d, yb - Hh - 22, COMP, 2.4, 9) + T(x0 + Lw + d / 2, yb - Hh - 30, 'Δ', 15, COMP, 'middle', 'bold')
    o += T(x0 + 40, yb - 10, 'θ', 15, INK, 'start', 'bold')
    o += T(230, 362, '斜撐伸長 δ = Δcosθ、阻尼力水平分量 *F*_{d}cosθ', 14.5, KEY, 'middle', 'bold')
    o += box(470, 40, 420, 310, '一條鏈：cos²θ', ['阻尼器速度 δ̇ = *u̇*cosθ', '阻尼器力 *F*_{d} = *C*δ̇ = *Cu̇*cosθ', '水平分量 *F*_{d}cosθ = (*C*cos²θ)*u̇*', '⇒ *c*_{eff} = *C*cos²θ', 'ξ_{d} = *c*_{eff}/(2*m*ω)', f'2018-1：tanθ = 3/6，cos²θ = {Q2018_1["cos2"]:.1f}', f'*C* = 2(0.05)*m*ω/0.8 = {Q2018_1["C"]:.1f} kN·s/m', f'2012-2：cos²30° = 0.75，ξ_{{d}} = {Q2012["xid"]*100:.2f}%'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '斜撐阻尼器')


def fig5_2():
    W, H = 900, 380
    pl = Plot(80, 40, 560, 290, 0, 2 * math.pi, -1.9, 1.3)
    o = pl.axes([0], [-1, 0, 1], 'ω*t*', '', grid=False, yfmt=lambda v: f'{v:g}')
    o += pl.curve(lambda t: math.sin(t), 0, 2 * math.pi, AC, 3)
    o += pl.curve(lambda t: math.cos(t), 0, 2 * math.pi, WARN, 3)
    o += pl.curve(lambda t: math.sin(t) + 0.6 * math.cos(t), 0, 2 * math.pi, KEY, 2.4, dash='6 4')
    for t, lab, c in ((math.pi / 2, '最大變位', AC), (math.pi, '最大速度', WARN)):
        o += L(pl.X(t), pl.Y(-1.3), pl.X(t), pl.Y(1.25), c, 1.6, '4 3')
        o += T(pl.X(t), pl.Y(1.25) - 6, lab, 14.5, c, 'middle', 'bold')
    t3 = math.atan2(1, 0.6)
    o += L(pl.X(t3), pl.Y(-1.3), pl.X(t3), pl.Y(1.25), KEY, 1.6, '4 3') + T(pl.X(t3) - 8, pl.Y(-0.6), '最大加速度', 14.5, KEY, 'end', 'bold')
    o += T(pl.X(0.1), pl.Y(-1.7), '— 位移 *u*（彈性力）', 14.5, AC, 'start', 'bold')
    o += T(pl.X(2.2), pl.Y(-1.7), '— 速度（阻尼力）', 14.5, WARN, 'start', 'bold')
    o += T(pl.X(3.9), pl.Y(-1.7), '--- 總力 *ku* + *cu̇* = −*mü*', 14.5, KEY, 'start', 'bold')
    o += box(670, 40, 220, 300, '三種情況', ['① 最大變位：', '　彈性力最大、阻尼力 0', '② 最大速度：', '　阻尼力最大、彈性力 0', '③ 最大加速度：', '　兩者合力最大', '構材取三者包絡'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '速度型三種變位情況')


def fig5_3():
    W, H = 900, 360
    o = ''
    for j, (ttl, col, col2) in enumerate((('BRB：位移型（雙線性）', WARN, WARN2), ('黏滯阻尼器：速度型（橢圓）', TEN, TEN2))):
        ox = 20 + j * 450
        pl = Plot(ox + 50, 50, 340, 220, -1.3, 1.3, -1.3, 1.3)
        o += T(ox + 220, 30, ttl, 15.5, col, 'middle', 'bold')
        o += pl.axes([0], [0], '*u*', '*F*', grid=False)
        if j == 0:
            pts = [(-1, -1.05), (-0.8, -0.55), (1, 1.05), (0.8, 0.55), (-1, -1.05)]
            pts = [(-1, -1.1), (-0.65, -0.35), (1, 1.1), (0.65, 0.35), (-1, -1.1)]
            o += P([pl.pt(*p) for p in pts], col, 0, fill=col2, close=True) + P([pl.pt(*p) for p in pts], col, 3)
            o += T(ox + 220, 318, '拉壓都降伏、迴圈飽滿；加勁度', 14.5, col, 'middle', 'bold')
            o += T(ox + 220, 342, '缺點：震後殘餘變形、低週疲勞需更換', 14, MUT, 'middle')
        else:
            pts = [pl.pt(math.cos(t), math.sin(t)) for t in [i * 2 * math.pi / 100 for i in range(101)]]
            o += P(pts, col, 0, fill=col2, close=True) + P(pts, col, 3)
            o += T(ox + 220, 318, '小震也消能、不加勁度（力與位移差 90°）', 14.5, col, 'middle', 'bold')
            o += T(ox + 220, 342, '缺點：造價高、漏油維護、要做三種情況檢核', 14, MUT, 'middle')
    return svg(W, H, o, 'BRB vs FVD')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
