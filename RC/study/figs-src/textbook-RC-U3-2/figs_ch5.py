# -*- coding: utf-8 -*-
"""第 5 章：穿孔剪力——剪力面、三式取小、三題比較。"""
from figs_common import *  # noqa
from calcs import footing, f2007_3, f2017_3
import math

F25 = footing()
F07 = f2007_3()
F17 = f2017_3()


def fig5_1():
    W, H = 900, 380
    o = T(450, 24, '穿孔剪力面：繞柱一圈、攤平成 *b*_{o} × *d*', 16, INK, 'middle', 'bold')
    sc = 1.6
    B, c, d, h = 300, F25['c'], F25['d'], F25['h']
    x0, y0 = 40, 120
    o += R(x0, y0, B * sc * 0.8, h * sc, STEEL2, INK, 1.6)
    xm = x0 + B * sc * 0.4
    o += R(xm - c * sc / 2, y0 - 60, c * sc, 60, STEEL3, INK, 1.6)
    ys = y0 + d * sc
    o += L(x0, ys, x0 + B * sc * 0.8, ys, INK, 2.6)
    for sg in (-1, 1):
        xf = xm + sg * c * sc / 2
        o += L(xf, y0, xf + sg * d * sc, ys, COMP, 2.8)
        xc = xm + sg * (c / 2 + d / 2) * sc
        o += L(xc, y0 - 6, xc, ys + 6, COMP, 2.2, '5 3')
    o += hdim(xm - (c / 2 + d / 2) * sc, xm + (c / 2 + d / 2) * sc, ys + 34, f'*c* + *d* = {c+d:.0f}', COMP, 1, 15)
    o += T(x0 + 6, 100, '剖面', 15, INK, 'start', 'bold')
    o += A(xm, y0 - 88, xm, y0 - 64, AC, 2.6, 10)
    o += T(xm + 10, y0 - 70, '*P*_{u}', 15, AC, 'start', 'bold')
    # 右：攤平
    rx, ry = 470, 140
    bw = F25['bo'] * 0.95
    o += T(rx + bw / 2, 70, '攤平的剪力面', 15, INK, 'middle', 'bold')
    o += R(rx, ry, bw, d * 1.6, COMP2, COMP, 2)
    for k in range(1, 4):
        o += L(rx + bw * k / 4, ry, rx + bw * k / 4, ry + d * 1.6, COMP, 1, '4 3')
    o += hdim(rx, rx + bw, ry + d * 1.6 + 20, f"*b*_{{o}} = 4(*c*+*d*) = {F25['bo']:.0f}", INK, 1, 15)
    o += vdim(rx + bw + 14, ry, ry + d * 1.6, f'*d* = {d:.0f}', INK, 1, 15)
    o += T(rx + bw / 2, ry + d * 1.6 + 84, f"√*f*′_{{c}}*b*_{{o}}*d* = {F25['sqbod']/1000:.2f} tf", 15, KEY, 'middle', 'bold')
    o += T(rx + bw / 2, ry + 40, '四面都被版子圍住', 15, COMP, 'middle', 'bold')
    o += T(rx + bw / 2, ry + 62, '→ 係數 1.06 = 2 × 0.53', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, '穿孔剪力面')


def fig5_2():
    W, H = 900, 380
    o = T(450, 24, '三式取小：兩種「太細長」都讓係數往 0.53 掉', 16, INK, 'middle', 'bold')
    p1 = Plot(80, 60, 330, 250, 1, 6, 0.4, 1.8)
    o += p1.axes([1, 2, 3, 4, 5, 6], [0.4, 0.8, 1.2, 1.6], 'β', '', size=14, yfmt=lambda v: f'{v:.1f}')
    o += p1.curve(lambda b: 0.53 * (1 + 2 / b), 1, 6, WARN, 2.6)
    o += p1.hline(1.06, 1, 6, COMP, 2.6, None)
    o += p1.hline(0.53, 1, 6, MUT, 1.2)
    o += p1.curve(lambda b: min(1.06, 0.53 * (1 + 2 / b)), 1, 6, KEY, 6, op=0.35)
    o += p1.dot(2, 1.06, KEY, 6)
    o += T(p1.X(2) + 8, p1.Y(1.06) - 12, 'β = 2', 15, KEY, 'start', 'bold')
    o += T(p1.X(1.1), p1.Y(1.59) + 4, '0.53(1+2/β)', 14, WARN, 'start', 'bold')
    o += T(p1.X(5.9), p1.Y(0.53) - 8, '→ 0.53', 14, MUT, 'end')
    o += p1.dot(1, 1.06, AC, 5)
    o += T(p1.X(1) + 8, p1.Y(1.06) + 22, '示範基腳', 14, AC, 'start', 'bold')
    p2 = Plot(510, 60, 330, 250, 0, 60, 0.4, 1.8)
    o += p2.axes([0, 10, 20, 30, 40, 50, 60], [0.4, 0.8, 1.2, 1.6], '*b*_{o}/*d*', '', size=14, yfmt=lambda v: f'{v:.1f}')
    o += p2.curve(lambda r: 0.265 * (2 + 40 / r), 8.4, 60, WARN, 2.6)
    o += p2.hline(1.06, 0, 60, COMP, 2.6, None)
    o += p2.hline(0.53, 0, 60, MUT, 1.2)
    o += p2.curve(lambda r: min(1.06, 0.265 * (2 + 40 / r)), 3, 60, KEY, 6, op=0.35)
    o += p2.dot(20, 1.06, KEY, 6)
    o += T(p2.X(20) + 8, p2.Y(1.06) - 12, '*b*_{o}/*d* = 20', 15, KEY, 'start', 'bold')
    o += T(p2.X(16), p2.Y(1.5), '0.265(2+40*d*/*b*_{o})', 14, WARN, 'start', 'bold')
    bd = F25['bo'] / F25['d']
    o += p2.dot(bd, 1.06, AC, 5)
    o += T(p2.X(bd) + 2, p2.Y(1.06) + 22, f'示範 {bd:.1f}', 14, AC, 'start', 'bold')
    o += T(p2.X(59), p2.Y(0.53) - 8, '→ 0.53', 14, MUT, 'end')
    o += T(245, 352, '柱太扁', 15, INK, 'middle', 'bold') + T(675, 352, '周長太長（內柱 α_{s} = 40）', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '三式取小')


def fig5_3():
    W, H = 900, 385
    o = T(450, 24, '穿孔剪力：需求 vs φ*V*_{c}（tf）', 16, INK, 'middle', 'bold')
    rows = [('RC-2007-3', F07['Vu2'], F07['phiVc2'], F07['phiVc2_lams']),
            ('RC-2017-3', F17['Vu2'], F17['phiVc2'], None),
            ('示範基腳 2025-1', F25['Vu2'], F25['phiVc2'], F25['phiVc2_lams'])]
    x0, y0, k = 230, 60, 1.45
    for i, (lab, vu, vn, vl) in enumerate(rows):
        y = y0 + i * 95
        o += T(x0 - 14, y + 36, lab, 15, INK, 'end', 'bold')
        o += R(x0, y + 8, vu * k, 22, STEEL3, INK, 1)
        o += T(x0 + vu * k + 6, y + 25, f'*V*_{{u2}} {vu:.2f}', 14, INK, 'start', 'bold')
        ok = vn >= vu
        o += R(x0, y + 36, vn * k, 22, TEN if ok else COMP, None, 0, op=0.85)
        o += T(x0 + vn * k + 6, y + 53, f"φ*V*_{{c}} {vn:.2f}", 14, TEN if ok else COMP, 'start', 'bold')
        if vl:
            o += R(x0, y + 64, vl * k, 18, '#fff', KEY, 1.4, dash='5 3')
            o += T(x0 + vl * k + 6, y + 78, f'若乘 λ_{{s}}：{vl:.2f}', 14, KEY, 'start')
    o += T(450, 370, '綠＝足夠、紅＝不足（RC-2017-3 差 1%）；紫虛框＝自行乘 λ_{s}（基腳規範允許不乘）', 14, MUT, 'middle')
    return svg(W, H, o, '穿孔三題')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
