# -*- coding: utf-8 -*-
"""第 3 章：柱圍束——保護層與核心、Ash 兩式、縱筋挫屈、so。"""
from figs_common import *  # noqa
from calcs import frame2012, p2013_2
import math

F12 = frame2012()
P13 = p2013_2()


def fig3_1():
    W, H = 900, 400
    o = T(450, 24, '保護層剝落 → 核心要補回；兩式在 *A*_{g}/*A*_{ch} = 1.3 交叉', 16, INK, 'middle', 'bold')
    x0, y0, s = 60, 70, 4.8
    b, bc = P13['b'], P13['hc']
    o += R(x0, y0, b * s, b * s, '#eceff1', INK, 1.6)
    for i in range(-int(b * s), int(b * s), 12):
        o += L(x0 + max(0, i), y0 + max(0, -i), x0 + min(b * s, i + b * s), y0 + min(b * s, b * s - i), '#b0bec5', 1)
    c0 = (b - bc) / 2 * s
    o += R(x0 + c0, y0 + c0, bc * s, bc * s, STEEL2, TEN, 2.6, dash='7 4')
    for k in range(4):
        cx = x0 + b * s / 2
        cy = y0 + b * s / 2
    o += A(x0 + c0 - 2, y0 + b * s / 2, x0 + c0 + 30, y0 + b * s / 2, TEN, 2.2, 9)
    o += A(x0 + c0 + bc * s + 2, y0 + b * s / 2, x0 + c0 + bc * s - 30, y0 + b * s / 2, TEN, 2.2, 9)
    o += A(x0 + b * s * 0.3, y0 + c0 - 2, x0 + b * s * 0.3, y0 + c0 + 30, TEN, 2.2, 9)
    o += A(x0 + b * s * 0.3, y0 + c0 + bc * s + 2, x0 + b * s * 0.3, y0 + c0 + bc * s - 30, TEN, 2.2, 9)
    o += T(x0 + b * s / 2, y0 + b * s / 2 + 5, '核心 *A*_{ch}', 15, TEN, 'middle', 'bold')
    o += T(x0 + b * s / 2, y0 + b * s / 2 + 26, '側壓 *f*_{l}', 14, TEN, 'middle')
    o += T(x0 + b * s / 2, y0 + b * s + 26, '斜線＝保護層（會剝落）', 14, MUT, 'middle')
    o += hdim(x0 + c0, x0 + c0 + bc * s, y0 + c0 + bc * s - 14, f'*b*_{{c}} = {bc:.0f}', TEN, -1, 14)
    # 右：兩式
    pl = Plot(450, 80, 370, 240, 1.0, 1.8, 0, 0.3)
    o += pl.axes([1.0, 1.2, 1.4, 1.6, 1.8], [0, 0.1, 0.2, 0.3], '*A*_{g}/*A*_{ch}', '係數', size=14, xfmt=lambda v: f'{v:.1f}', yfmt=lambda v: f'{v:.1f}')
    o += pl.curve(lambda r: 0.3 * (r - 1), 1.0, 1.8, AC, 3)
    o += pl.hline(0.09, 1.0, 1.8, COMP, 3, None)
    o += pl.curve(lambda r: max(0.09, 0.3 * (r - 1)), 1.0, 1.8, KEY, 6, op=0.35)
    o += pl.dot(1.3, 0.09, KEY, 6)
    o += T(pl.X(1.3) - 8, pl.Y(0.09) - 12, '1.3', 15, KEY, 'end', 'bold')
    o += T(pl.X(1.75), pl.Y(0.3 * 0.75) - 10, '0.3(*A*_{g}/*A*_{ch} − 1)', 14, AC, 'end', 'bold')
    o += T(pl.X(1.02), pl.Y(0.09) - 10, '0.09', 14, COMP, 'start', 'bold')
    for r, lab, dy in ((P13['AgAch'], 'RC-2013-2', -12), (F12['AgAch'], '2012-3', 44)):
        v = max(0.09, 0.3 * (r - 1))
        o += pl.dot(r, v, INK, 5)
        o += T(pl.X(r) + 6, pl.Y(v) + dy, f'{lab}（{r:.3f}）', 14, INK, 'start', 'bold')
    return svg(W, H, o, 'Ash 兩式')


def fig3_2():
    W, H = 900, 390
    o = T(450, 24, '縱筋在兩支箍筋之間像一根小柱', 16, INK, 'middle', 'bold')
    x0, y0 = 120, 70
    sp = 90
    for i in range(4):
        y = y0 + i * sp
        o += L(x0 - 50, y, x0 + 90, y, TEN, 4)
    o += L(x0, y0 - 10, x0, y0 + 3 * sp + 10, MUT, 1.2, '4 3')
    pts = []
    for j in range(61):
        t = j / 60
        y = y0 + sp + sp * t
        pts.append((x0 - 26 * math.sin(math.pi * t), y))
    o += P([(x0, y0 - 10), (x0, y0 + sp)] + pts + [(x0, y0 + 3 * sp + 10)], COMP, 4)
    o += A(x0 + 40, y0 + sp + 20, x0 + 40, y0 + sp - 4, INK, 1.6, 8) + A(x0 + 40, y0 + 2 * sp - 20, x0 + 40, y0 + 2 * sp + 4, INK, 1.6, 8)
    o += T(x0 + 50, y0 + 1.5 * sp + 5, '*s* ≤ 6*d*_{b}', 16, KEY, 'start', 'bold')
    o += T(x0 - 36, y0 + 1.5 * sp + 5, '挫屈', 15, COMP, 'end', 'bold')
    o += T(x0 + 20, y0 + 3 * sp + 34, '綠＝箍筋；紅＝縱筋', 14, MUT, 'middle')
    # 右：so
    pl = Plot(430, 60, 380, 250, 0, 35, 8, 16)
    o += pl.axes([0, 5, 10, 15, 20, 25, 30, 35], [8, 10, 12, 14, 16], '*h*_{x}', '*s*_{o}', size=14)
    o += T(pl.X(35) + 18, pl.Y(8) + 26, '(cm)', 14, MUT, 'start')
    o += pl.curve(lambda h: min(15, max(10, 10 + (35 - h) / 3)), 0, 35, KEY, 3.2)
    o += T(pl.X(2), pl.Y(15) - 10, '上限 15', 14, KEY, 'start', 'bold')
    o += T(pl.X(33), pl.Y(10) - 10, '35 時 = 10', 14, KEY, 'end', 'bold')
    for hx, lab, dy in ((P13['hx'], 'RC-2013-2', 24), (F12['hx'], 'RC-2012-3', -12)):
        o += pl.dot(hx, 15, INK, 5)
        o += T(pl.X(hx), pl.Y(15) + dy, f'{lab} {hx:.2f}', 14, INK, 'middle', 'bold')
    o += T(pl.X(17.5), pl.Y(8) + 48, '*s*_{o} = 10 + (35 − *h*_{x})/3', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '縱筋挫屈與 so')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
