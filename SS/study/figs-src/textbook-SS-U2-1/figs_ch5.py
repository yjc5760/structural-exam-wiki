# -*- coding: utf-8 -*-
"""第 5 章：四種基本機構、固端-簡支均佈的機構幾何、w_u(x) 曲線找最低點。"""
from plot import *  # noqa
from calcs import *  # noqa


def _support(x, y, kind, side):
    if kind == 'pin':
        return pin(x, y + 2)
    # fixed：牆
    xx = x - 12 if side == 'L' else x
    o = R(xx, y - 30, 12, 60, STEEL3, INK, 1.2)
    return o


def _mech(x0, y0, w, left, right, a, load, title, eq, res):
    """a：跨內鉸位置（0~1），load：'P' 或 'w'。"""
    o = T(x0 + w / 2, y0 - 70, title, 15, INK, 'middle', 'bold')
    d = 46
    o += L(x0, y0, x0 + w, y0, STEEL, 1.4, '5 4')
    xh = x0 + a * w
    o += P([(x0, y0), (xh, y0 + d), (x0 + w, y0)], COMP, 3.2)
    o += _support(x0, y0, left, 'L') + _support(x0 + w, y0, right, 'R')
    if load == 'P':
        o += A(xh, y0 - 52, xh, y0 - 6, WARN, 2.6, 11)
        o += T(xh + 8, y0 - 36, '*P*', 15, WARN, 'start', 'bold')
    else:
        for i in range(11):
            xx = x0 + 6 + i * (w - 12) / 10
            o += A(xx, y0 - 34, xx, y0 - 6, WARN, 1.4, 7)
        o += T(x0 + w + 6, y0 - 24, '*w*', 15, WARN, 'start', 'bold')
    th1 = '*θ*'
    o += C(xh, y0 + d, 7, '#fff', COMP, 2.4)
    o += T(xh, y0 + d + 26, '2*θ*' if abs(a - 0.5) < 1e-6 else '', 15, COMP, 'middle', 'bold')
    if left == 'fix':
        o += C(x0 + 2, y0, 7, '#fff', COMP, 2.4) + T(x0 + 14, y0 + 34, th1, 15, COMP, 'start', 'bold')
    if right == 'fix':
        o += C(x0 + w - 2, y0, 7, '#fff', COMP, 2.4) + T(x0 + w - 14, y0 + 34, th1, 15, COMP, 'end', 'bold')
    o += T(xh + 10, y0 + d / 2 + 4, '*δ* = *θL*/2', 14, MUT, 'start')
    o += T(x0 + w / 2, y0 + 100, eq, 14, INK, 'middle')
    o += R(x0 + w / 2 - 110, y0 + 114, 220, 32, KEY2, None, 0, 8)
    o += T(x0 + w / 2, y0 + 136, res, 16, KEY, 'middle', 'bold')
    return o


def fig5_1():
    W, H = 900, 560
    o = ''
    cfg = [
        ('pin', 'pin', 'P', '① 簡支＋跨中 *P*', '*P*·*θL*/2 = *M*_{p}·2*θ*', '*P*_{u} = 4*M*_{p}/*L*'),
        ('fix', 'pin', 'P', '② 固端-簡支＋跨中 *P*', '*P*·*θL*/2 = *M*_{p}(*θ* + 2*θ*)', '*P*_{u} = 6*M*_{p}/*L*'),
        ('fix', 'fix', 'P', '③ 兩端固定＋跨中 *P*', '*P*·*θL*/2 = *M*_{p}(*θ* + 2*θ* + *θ*)', '*P*_{u} = 8*M*_{p}/*L*'),
        ('fix', 'fix', 'w', '④ 兩端固定＋均佈 *w*', '*w*·*L*·(*θL*/2)/2 = *M*_{p}·4*θ*', '*w*_{u} = 16*M*_{p}/*L*^{2}'),
    ]
    for i, c in enumerate(cfg):
        x0 = 60 + (i % 2) * 440
        y0 = 110 + (i // 2) * 270
        o += _mech(x0, y0, 340, *c[:2], 0.5, *c[2:])
    return svg(W, H, o, '四種基本崩塌機構與虛功')


def fig5_2():
    W, H = 900, 380
    x0, y0, w = 90, 130, 640
    xh = x0 + X_PROP * w
    d = 90
    o = L(x0, y0, x0 + w, y0, STEEL, 1.4, '5 4')
    o += P([(x0, y0), (xh, y0 + d), (x0 + w, y0)], COMP, 3.4)
    o += pin(x0, y0 + 2)
    o += R(x0 + w, y0 - 40, 14, 80, STEEL3, INK, 1.2)
    for i in range(17):
        xx = x0 + 6 + i * (w - 12) / 16
        o += A(xx, y0 - 46, xx, y0 - 6, WARN, 1.5, 8)
    o += T(x0 + w / 2, y0 - 58, '*w*（全跨）', 15, WARN, 'middle', 'bold')
    o += T(x0 - 8, y0 - 14, 'A 簡支', 15, INK, 'end', 'bold')
    o += T(x0 + w + 20, y0 - 50, 'B 固定', 15, INK, 'start', 'bold')
    o += C(xh, y0 + d, 8, '#fff', COMP, 2.6) + C(x0 + w - 3, y0, 8, '#fff', COMP, 2.6)
    o += dim(xh + 1, y0, xh + 1, y0 + d, '*δ*', INK, 0, 16, 1)
    o += dim(x0, y0 + d + 40, xh, y0 + d + 40, '*x*', INK, 0, 16, 1)
    o += dim(xh, y0 + d + 40, x0 + w, y0 + d + 40, '*L* − *x*', INK, 0, 16, 1)
    o += T(x0 + 60, y0 + 30, '*θ*_{1} = *δ*/*x*', 15, AC, 'start', 'bold')
    o += T(x0 + w - 90, y0 + 30, '*θ*_{2} = *δ*/(*L* − *x*)', 15, AC, 'end', 'bold')
    o += T(xh, y0 + d + 26, '跨內鉸轉 *θ*_{1} + *θ*_{2}', 15, COMP, 'middle', 'bold')
    o += T(x0 + w + 20, y0 + 30, '轉 *θ*_{2}', 15, COMP, 'start', 'bold')
    o += T(450, 350, '外功 = *w* × (三角形面積 *Lδ*/2)　　內功 = *M*_{p}[(*θ*_{1} + *θ*_{2}) + *θ*_{2}]', 16, INK, 'middle', 'bold')
    return svg(W, H, o, '固端-簡支梁均佈載重的崩塌機構幾何')


def fig5_3():
    W, H = 900, 400
    pl = Plot(90, 40, 560, 290, 0.1, 0.9, 6, 30)
    o = pl.axes([0.1, 0.25, X_PROP, 0.5, 0.75, 0.9], [8, 11.66, 16, 20, 24, 28], '*x*/*L*', '*w*_{u}*L*^{2}/*M*_{p}', size=14,
                xfmt=lambda v: f'{v:.3f}' if abs(v - X_PROP) < 1e-6 else f'{v:g}', yfmt=lambda v: f'{v:g}')
    o += pl.hline(COEF_SS_U, c=AC, w=1.6) + pl.hline(COEF_FF_U, c=TEN, w=1.6)
    o += pl.curve(wu_prop, 0.1, 0.85, COMP, 3.4)
    o += pl.dot(X_PROP, COEF_PC_U, KEY, 7)
    o += pl.dot(0.5, wu_prop(0.5), WARN, 5)
    o += T(pl.X(X_PROP) - 6, pl.Y(COEF_PC_U) + 30, f'最低點 (0.414, {COEF_PC_U:.3f})', 15, KEY, 'middle', 'bold')
    o += T(pl.X(0.5) + 12, pl.Y(wu_prop(0.5)) + 8, f'跨中 → {wu_prop(0.5):.0f}（高估 {(wu_prop(0.5) / COEF_PC_U - 1) * 100:.1f}%）', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.88), pl.Y(8) - 8, '簡支 8', 14, AC, 'end', 'bold')
    o += T(pl.X(0.88), pl.Y(16) - 8, '兩端固定 16', 14, TEN, 'end', 'bold')
    o += R(680, 70, 210, 170, KEY2, KEY, 1.4, 10)
    for i, s in enumerate(['每一個 *x* 都是一個', '「假設的機構」', '都給出 *w*_{u} 的上限', '→ 取最小的那個', '（種子 S6）']):
        o += T(785, 100 + i * 30, s, 15, KEY if i == 3 else INK, 'middle', 'bold' if i == 3 else None)
    return svg(W, H, o, '固端-簡支均佈：w_u 隨鉸位置變化')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
