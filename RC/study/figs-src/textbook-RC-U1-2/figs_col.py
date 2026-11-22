# -*- coding: utf-8 -*-
"""RC-U1-2 共用圖元：柱斷面＋應變＋力三聯圖、P-M 互制圖。所有尺寸依實際 cm 比例、數值來自 calcs.py。"""
from figs_common import *  # noqa
from calcs import tf, tfm, ECU


def col_section(x0, y0, sc, K, nbars, cols=None, label=True):
    """畫柱斷面（壓力面在上）。nbars：每層根數（與 C.layers 同序）。"""
    o = R(x0 - K.b * sc / 2, y0, K.b * sc, K.h * sc, STEEL2, INK, 1.6)
    cov = K.layers[0][0]
    for i, (d, A) in enumerate(K.layers):
        n = nbars[i]
        col = (cols[i] if cols else INK)
        if n == 1:
            xs = [x0]
        else:
            span = (K.b - 2 * cov) * sc
            xs = [x0 - span / 2 + span * j / (n - 1) for j in range(n)]
        for xx in xs:
            o += C_(xx, y0 + d * sc, max(2.54 * sc / 2, 5), col)
    return o


def C_(x, y, r, col):
    return C(x, y, r, col, '#fff', 1.2)


def layer_color(r):
    if r['eps'] > 1e-9:
        return COMP
    if r['eps'] < -1e-9:
        return TEN
    return MUT


def tri_panel(K, s, nbars, title, W=900, H=400, sc=None, show_e=True, note=None, y0=78):
    """斷面｜應變｜力 三聯圖。"""
    sc = sc or min(250 / K.h, 5.5)
    o = T(W / 2, 28, title, 16, INK, 'middle', 'bold')
    xs = 150
    cols = [layer_color(r) for r in s['rows']]
    o += col_section(xs, y0, sc, K, nbars, cols)
    o += T(xs, y0 - 14, f'斷面 {K.b:g}×{K.h:g}', 15, INK, 'middle', 'bold')
    yb = y0 + K.h * sc
    # 形心線
    yg = y0 + K.h / 2 * sc
    o += L(xs - K.b * sc / 2 - 10, yg, W - 30, yg, KEY, 1.2, '2 4')
    o += T(W - 30, yg - 6, '形心', 14, KEY, 'end')
    # 中性軸
    c = s['c']
    yc = y0 + min(c, K.h + 8) * sc
    if c <= K.h:
        o += L(xs - K.b * sc / 2 - 10, yc, 600, yc, MUT, 1.2, '6 4')
        o += T(xs + K.b * sc / 2 + 8, yc + 18, f'*c* = {c:.2f}', 14, MUT, 'start')
    else:
        o += T(xs, yb + 26, f'*c* = {c:.2f} > *h*（全斷面受壓）', 14, MUT, 'middle')
    # 應變
    xa = 400
    big = max(ECU, max(abs(r['eps']) for r in s['rows']))
    k = 120 / big
    def ex(d):
        return xa + k * (-ECU * (c - d) / c)   # 壓向左、拉向右
    o += L(xa, y0 - 6, xa, yb + 6, MUT, 1.2, '4 3')
    xt = ex(0); xbm = ex(K.h)
    poly = [(xa, y0), (xt, y0), (xbm, yb), (xa, yb)]
    o += P(poly, None, fill=COMP2 if c >= K.h else '#f5f5f5', close=True, op=0.9)
    o += L(xt, y0, xbm, yb, INK, 2.2)
    o += T(xt, y0 - 8, '0.003', 15, COMP, 'middle', 'bold')
    for r, col in zip(s['rows'], cols):
        yy = y0 + r['d'] * sc
        xx = ex(r['d'])
        o += L(xa, yy, xx, yy, col, 2.4) + C(xx, yy, 4, col, '#fff', 1)
        lab = f"{abs(r['eps']):.6f}".rstrip('0') if abs(r['eps']) > 1e-9 else '0'
        if r['yld'] and abs(r['eps']) > 1e-9:
            lab += ' 降伏'
        anc = 'end' if xx < xa else 'start'
        o += T(xx + (-14 if xx < xa else 10), yy - 6, lab, 14, col, anc, 'bold')
    o += T(xa, yb + 30, '應變（壓左、拉右）', 14, INK, 'middle', 'bold')
    # 力
    xf = 650
    o += L(xf, y0 - 6, xf, yb + 6, INK, 1.4)
    Fs = [s['Cc']] + [abs(r['F']) for r in s['rows']]
    kf = 110 / max(Fs)
    ya = y0 + s['a'] / 2 * sc
    # 應力塊
    o += R(xf - 10, y0, 10, s['a'] * sc, WARN2, WARN, 1.2)
    lc = max(kf * s['Cc'], 20)
    o += A(xf + lc + 6, ya, xf + 4, ya, COMP, 3, 11)
    o += T(xf + lc + 10, ya - 5, f"*C*_{{c}} {tf(s['Cc']):.1f}", 14, COMP, 'start', 'bold')
    for r, col in zip(s['rows'], cols):
        yy = y0 + r['d'] * sc
        if abs(r['F']) < 1:
            o += T(xf + 10, yy + 5, '0', 14, MUT, 'start', 'bold')
            continue
        l = max(kf * abs(r['F']), 18)
        if r['F'] > 0:
            o += A(xf + l + 6, yy, xf + 4, yy, col, 2.6, 10)
        else:
            o += A(xf + 4, yy, xf + l + 6, yy, col, 2.6, 10)
        near = abs(r['d'] - s['a'] / 2) < 4
        o += T(xf + l + 10, yy + (20 if near else -5), f"{tf(abs(r['F'])):.1f}", 14, col, 'start', 'bold')
    o += T(xf + 60, yb + 30, '力（tf，←壓 →拉）', 14, INK, 'middle', 'bold')
    if note:
        o += T(W / 2, yb + 62, note, 15, KEY, 'middle', 'bold')
    return svg(W, H, o, title)


def pm_axes(pl, xt, yt, xl='*M*_{n}（tf·m）', yl='*P*_{n}（tf）'):
    return pl.axes(xt, yt, xl, yl, size=14)


def pm_curve(pl, K, color=AC, w=3, design=False, dash=None, cap=True, n=200):
    pts = K.curve(n)
    xy = []
    P0 = K.P0()
    for M, Pv, ph, c in pts:
        if design:
            fac = ph
            Pd = fac * Pv
            if cap:
                Pd = min(Pd, 0.65 * 0.80 * P0)
            xy.append(pl.pt(tfm(fac * M), tf(Pd)))
        else:
            xy.append(pl.pt(tfm(M), tf(Pv)))
    return P(xy, color, w, dash=dash)
