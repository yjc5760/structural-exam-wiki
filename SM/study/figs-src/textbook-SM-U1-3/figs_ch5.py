# -*- coding: utf-8 -*-
"""第 5 章：沉陷三式路徑、三種算法比較、次壓密。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch4 import _logaxes


def fig5_1():
    d = ex2024_3()
    W, H = 900, 440
    o, X, Y = _logaxes(90, 50, 560, 320, math.log10(200), math.log10(450), 0.870, 0.905, [0.875, 0.885, 0.895, 0.905])
    e0 = d['e0']
    eNC = e0 - d['Cc'] * lg(d['pf'] / d['p0'])
    ePc = e0 - d['Cs'] * lg(d['pc'] / d['p0'])
    eOC = ePc - d['Cc'] * lg(d['pf'] / d['pc'])
    # NC 路徑
    o += L(X(d['p0']), Y(e0), X(d['pf']), Y(eNC), COMP, 3)
    # OC 路徑
    o += L(X(d['p0']), Y(e0), X(d['pc']), Y(ePc), KEY, 3) + L(X(d['pc']), Y(ePc), X(d['pf']), Y(eOC), KEY, 3)
    for p, e, c in ((d['p0'], e0, INK), (d['pf'], eNC, COMP), (d['pc'], ePc, KEY), (d['pf'], eOC, KEY)):
        o += C(X(p), Y(e), 5.5, c, '#fff', 1.6)
    for p, nm in ((d['p0'], f"*p*_{{0}}′={d['p0']:.2f}"), (d['pc'], "*p*_{c}′=300"), (d['pf'], f"*p*_{{f}}′={d['pf']:.2f}")):
        o += L(X(p), Y(0.870), X(p), Y(0.905), MUT, 1, '4 3')
        o += T(X(p), Y(0.870) - 8, nm, 14, INK, 'middle')
    # Δe 標示
    xr = X(d['pf']) + 26
    o += dim(xr, Y(e0), xr, Y(eNC), '', COMP) + T(xr + 10, (Y(e0) + Y(eNC)) / 2, f"NC Δ*e*={e0 - eNC:.4f}", 15, COMP, 'start', 'bold')
    xr2 = X(d['pf']) + 26
    o += dim(X(d['pc']) - 14, Y(e0), X(d['pc']) - 14, Y(ePc), '', KEY)
    o += T(X(d['pc']) - 22, Y(e0) - 8, f"淺段 {e0 - ePc:.4f}", 14, KEY, 'end', 'bold')
    o += dim(xr2 + 150, Y(ePc), xr2 + 150, Y(eOC), '', KEY) + T(xr2 + 160, (Y(ePc) + Y(eOC)) / 2 + 5, f"陡段 {ePc - eOC:.4f}", 15, KEY, 'start', 'bold')
    o += L(X(d['pc']), Y(ePc), xr2 + 150, Y(ePc), KEY, 1, '3 3')
    o += L(X(d['pf']), Y(eOC), xr2 + 150, Y(eOC), KEY, 1, '3 3')
    o += T(X(205), Y(0.8785), '紅：NC（*C*_{c}=0.15 全程）', 15, COMP, 'start', 'bold')
    o += T(X(205), Y(0.8785) + 22, '紫：OC（*C*_{s}=0.02 → *C*_{c}）', 15, KEY, 'start', 'bold')
    return svg(W, H, o, '沉陷三式的路徑')


def fig5_2():
    d = ex2024_3()
    W, H = 900, 330
    o = ''
    x0, sc = 260, 40
    rows = [('全用 *C*_{s}（錯）', d['S_allCs'], MUT, None),
            ('OC 兩段（正解）', d['S_OC'], KEY, (d['S_OC1'], d['S_OC2'])),
            ('全用 *C*_{c}（＝NC 情況）', d['S_NC'], COMP, None)]
    for i, (nm, v, c, parts) in enumerate(rows):
        y = 50 + i * 80
        o += T(x0 - 14, y + 26, nm, 16, c, 'end', 'bold')
        if parts:
            o += R(x0, y, parts[0] * sc, 40, AC2, KEY, 1.4) + R(x0 + parts[0] * sc, y, parts[1] * sc, 40, KEY2, KEY, 1.4)
            o += T(x0 + parts[0] * sc + parts[1] * sc / 2, y + 26, f'陡段 {parts[1]:.2f}', 15, KEY, 'middle', 'bold')
            o += T(x0 + 4, y + 62, f'淺段 {parts[0]:.2f}', 14, AC, 'start')
        else:
            o += R(x0, y, v * sc, 40, COMP2 if c == COMP else STEEL2, c, 1.4)
        o += T(x0 + v * sc + 12, y + 27, f'{v:.2f} cm', 17, c, 'start', 'bold')
    o += L(x0, 40, x0, 300, INK, 1.4)
    return svg(W, H, o, '三種算法比較')


def fig5_3():
    W, H = 900, 420
    pl_x0, pl_w = 90, 600
    lmin, lmax = -1.0, 3.0   # log10(t/t50) 範圍示意
    X = lambda lt: pl_x0 + (lt - lmin) / (lmax - lmin) * pl_w
    e_top, de_p, Ca = 0.95, 0.12, 0.015
    Y = lambda e: 50 + (0.97 - e) / (0.97 - 0.78) * 300
    o = A(pl_x0, 350, pl_x0 + pl_w + 16, 350, INK, 1.5) + A(pl_x0, 350, pl_x0, 36, INK, 1.5)
    o += T(pl_x0 + pl_w + 20, 355, 'log *t*', 15, INK) + T(pl_x0, 28, '*e*', 16, INK, 'middle')
    T50 = Tv_from_U(0.5)
    ltp = math.log10(1.2 / T50)    # Tv≈1.2 視為主壓密結束

    def e_of(lt):
        Tv = T50 * 10 ** lt
        e = e_top - de_p * U_exact(Tv)
        if lt > ltp:
            e -= Ca * (lt - ltp)
        return e
    lts = [lmin + i * 0.01 for i in range(int((lmax - lmin) / 0.01) + 1)]
    o += P([(X(lt), Y(e_of(lt))) for lt in lts], INK, 3)
    o += L(X(ltp), Y(0.78), X(ltp), Y(e_of(ltp)) - 30, WARN, 1.5, '6 4') + T(X(ltp), 372, '*t*_{p}', 15, WARN, 'middle', 'bold')
    o += T(X(-0.3), Y(e_top) - 12, '主壓密（水在排）', 15, AC, 'middle', 'bold')
    o += T(X(2.0), Y(e_of(2.0)) + 40, '次壓密：斜率 *C*_{α}', 15, KEY, 'middle', 'bold')
    a, b = 1.6, 2.6
    o += L(X(a), Y(e_of(a)), X(b), Y(e_of(a)), KEY, 1.2, '3 3') + L(X(b), Y(e_of(a)), X(b), Y(e_of(b)), KEY, 1.2, '3 3')
    o += T(X((a + b) / 2), Y(e_of(a)) - 8, '×10', 14, KEY, 'middle') + T(X(b) + 6, (Y(e_of(a)) + Y(e_of(b))) / 2 + 5, '*C*_{α}', 15, KEY, 'start', 'bold')
    o += box(700, 70, 185, 110, '同一種想法', ['*C*_{c}：壓力 ×10', '*C*_{α}：時間 ×10'], KEY2, KEY)
    return svg(W, H, o, '次壓密')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
