# -*- coding: utf-8 -*-
"""第 4 章：單向剪力——ρw 立方根、λs、三題結論翻轉。"""
from figs_common import *  # noqa
from calcs import footing, f2007_3, f2017_3, lam_s
import math

F25 = footing()
F07 = f2007_3()
F17 = f2017_3()


def fig4_1():
    W, H = 900, 380
    pl = Plot(110, 50, 520, 270, 0, 2.0, 0, 0.7)
    o = pl.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], 'ρ_{w}', '係數', size=14, xfmt=lambda v: f'{v:.1f}', yfmt=lambda v: f'{v:.1f}')
    o += T(pl.X(2.0) + 18, pl.Y(0) + 26, '(%)', 14, MUT, 'start')
    o += R(pl.X(0.2), pl.Y(0.7), pl.X(0.4) - pl.X(0.2), pl.Y(0) - pl.Y(0.7), WARN2, None, 0, op=0.8)
    o += T((pl.X(0.2) + pl.X(0.4)) / 2, pl.Y(0.66), '基腳', 14, WARN, 'middle', 'bold')
    o += pl.curve(lambda r: 2.12 * (r / 100) ** (1 / 3), 0.002, 2.0, AC, 3)
    o += pl.hline(0.53, 0, 2.0, COMP, 3, None)
    rx = (0.53 / 2.12) ** 3 * 100
    o += pl.dot(rx, 0.53, KEY, 6)
    o += T(pl.X(rx), pl.Y(0.53) + 26, f'交點 {rx:.2f}%', 15, KEY, 'middle', 'bold')
    o += T(pl.X(0.55), pl.Y(0.53) - 10, '舊式 0.53', 15, COMP, 'start', 'bold')
    o += T(pl.X(1.95), pl.Y(2.12 * 0.0195 ** (1 / 3)) - 10, '現行 2.12ρ_{w}^{1/3}', 15, AC, 'end', 'bold')
    for F_, lab, dy in ((F17, 'RC-2017-3', 28), (F25, '2007-3／2025-1', -14)):
        r = F_['rho'] * 100
        v = 2.12 * F_['rho'] ** (1 / 3)
        o += pl.dot(r, v, AC, 5)
        o += T(pl.X(r) + 8, pl.Y(v) + dy, f'{lab} {v:.3f}', 14, AC, 'start', 'bold')
    o += box(665, 70, 220, 190, '基腳的現實', ['ρ_{w} = 0.2～0.4%', '新式只有舊式的', '五到六成', '→ 2007-3、2017-3', '結論翻轉'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '單向剪力係數')


def fig4_2():
    W, H = 900, 360
    pl = Plot(110, 50, 560, 250, 0, 100, 0.5, 1.05)
    o = pl.axes([0, 25, 50, 75, 100], [0.5, 0.6, 0.7, 0.8, 0.9, 1.0], '*d*', 'λ_{s}', size=14, yfmt=lambda v: f'{v:.1f}')
    o += T(pl.X(100) + 18, pl.Y(0.5) + 26, '(cm)', 14, MUT, 'start')
    o += pl.curve(lam_s, 0.5, 100, KEY, 3.2)
    pts = [(35, 'RC-2020-3 樓版', COMP, 8, -12, 'start'), (45, 'RC-2021-3 樁帽', COMP, -10, 24, 'end'), (50, '示範基腳', MUT, 8, -12, 'start'), (69.96, 'RC-2017-3 基腳', MUT, 8, -12, 'start')]
    for d, lab, col, dx, dy, anc in pts:
        v = lam_s(d)
        o += pl.dot(d, v, col, 5)
        o += T(pl.X(d) + dx, pl.Y(v) + dy, f'{lab} {v:.3f}', 14, col, anc, 'bold')
    o += pl.vline(25, 0.5, 1.0, MUT, 1.2)
    o += T(pl.X(25) - 6, pl.Y(0.56), '*d* ≤ 25：λ_{s} = 1', 14, MUT, 'end', 'bold')
    o += box(700, 70, 185, 170, '誰要乘', ['樓版：要', '樁帽：要', '獨立基腳：', '可取 1', '（13.2.6.2）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'λs')


def fig4_3():
    W, H = 900, 385
    o = T(450, 24, '單向剪力：需求 vs 現行式 vs 舊式（tf）', 16, INK, 'middle', 'bold')
    rows = [('RC-2007-3', F07['Vu1'], F07['phiVc1'], F07['phiVc1_old']),
            ('RC-2017-3', F17['Vu1'], F17['phiVc1'], F17['phiVc1_old']),
            ('示範基腳 2025-1', F25['Vu1'], F25['phiVc1'], F25['phiVc1_old'])]
    x0, y0, k = 230, 60, 3.4
    for i, (lab, vu, vn, vo) in enumerate(rows):
        y = y0 + i * 95
        o += T(x0 - 14, y + 36, lab, 15, INK, 'end', 'bold')
        o += R(x0, y + 4, vo * k, 20, '#fff', MUT, 1.2, dash='5 3')
        o += T(x0 + vo * k + 6, y + 20, f'舊 {vo:.2f}', 14, MUT, 'start')
        o += R(x0, y + 28, vu * k, 20, STEEL3, INK, 1)
        o += T(x0 + vu * k + 6, y + 44, f'*V*_{{u1}} {vu:.2f}', 14, INK, 'start', 'bold')
        ok = vn >= vu
        o += R(x0, y + 52, vn * k, 20, TEN if ok else COMP, None, 0, op=0.85)
        o += T(x0 + vn * k + 6, y + 68, f"φ*V*_{{c}} {vn:.2f} {'≥' if ok else '<'} *V*_{{u1}}", 14, TEN if ok else COMP, 'start', 'bold')
    o += T(450, 370, '綠＝現行式足夠、紅＝現行式不足；虛框＝舊式 0.53√*f*′_{c}*b*_{w}*d*（三題都「足夠」）', 14, MUT, 'middle')
    return svg(W, H, o, '單向剪力翻轉')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
