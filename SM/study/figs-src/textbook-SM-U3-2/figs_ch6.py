# -*- coding: utf-8 -*-
"""第 6 章：加勁牆兩區、五種內穩定模式、2016-3 外穩定。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    W, H = 900, 420
    o = ''
    phi = 32.0
    x0, y0, Hh, Lr = 140, 60, 300, 420
    o += R(x0 - 16, y0, 16, Hh, STEEL3, INK, 1.6)
    o += L(x0, y0, x0 + 640, y0, INK, 1.6)
    o += hatch_ground(x0 - 80, y0 + Hh, 760)
    wx = Hh * tan(45 - phi / 2)
    o += P([(x0, y0 + Hh), (x0 + wx, y0), (x0, y0)], TEN, 1.8, fill=TEN2, close=True, op=0.9)
    o += L(x0, y0 + Hh, x0 + wx, y0, COMP, 2.4, '8 5')
    n = 6
    for k in range(n):
        y = y0 + 30 + k * (Hh - 40) / (n - 1)
        o += L(x0, y, x0 + Lr, y, WARN, 3)
        xf = x0 + (y0 + Hh - y) * tan(45 - phi / 2)
        if k == 2:
            o += dim(xf, y - 14, x0 + Lr, y - 14, '', KEY) + T((xf + x0 + Lr) / 2, y - 22, '*L*_{e}（錨定段）', 14, KEY, 'middle', 'bold')
    o += T(x0 + wx * 0.3, y0 + Hh * 0.55, '主動區', 15, TEN, 'middle', 'bold')
    o += T(x0 + wx + 40, y0 + Hh * 0.82, '抵抗區（錨定）', 15, KEY, 'start', 'bold')
    o += T(x0 + wx * 0.55 + 8, y0 + Hh * 0.45, '45°+*φ*/2', 14, COMP, 'start', 'bold')
    o += T(x0 - 22, y0 + Hh / 2, '面板', 15, INK, 'end', 'bold')
    o += dim(x0 + Lr + 30, y0 + 30, x0 + Lr + 30, y0 + 30 + (Hh - 40) / (n - 1), '', INK) + T(x0 + Lr + 38, y0 + 30 + (Hh - 40) / (n - 1) / 2 + 5, '*S*_{v}', 15, INK)
    o += box(640, 140, 245, 150, '每根拉筋', ['拉力 *T*=*σ*_{h}*S*_{v}', '拉斷：*T*_{ult}/*T*', '拔出：', '2*L*_{e}*σ*_{v}′tan*φ*_{r}/*T*'], KEY2, KEY)
    return svg(W, H, o, '加勁牆兩區')


def _mini(x, y, title, kind):
    o = R(x, y, 160, 170, '#fff', MUT, 1.2, 10)
    o += T(x + 80, y + 22, title, 14, KEY, 'middle', 'bold')
    fx = x + 30
    o += R(fx - 8, y + 40, 8, 110, STEEL3, INK, 1.2)
    ys = [y + 60, y + 95, y + 130]
    for k, yy in enumerate(ys):
        if kind == 'break' and k == 2:
            o += L(fx, yy, fx + 50, yy, WARN, 3) + L(fx + 62, yy, fx + 110, yy, WARN, 3)
            o += T(fx + 56, yy + 18, '斷', 14, COMP, 'middle', 'bold')
        elif kind == 'pull' and k == 0:
            o += L(fx - 30, yy, fx + 70, yy, WARN, 3) + A(fx + 20, yy - 12, fx - 20, yy - 12, COMP, 2, 8)
        elif kind == 'conn' and k == 1:
            o += L(fx + 8, yy, fx + 110, yy, WARN, 3) + C(fx + 2, yy, 5, COMP2, COMP, 1.6)
        else:
            o += L(fx, yy, fx + 110, yy, WARN, 3)
    if kind == 'bulge':
        o += P([(fx - 8, y + 70), (fx - 22, y + 95), (fx - 8, y + 120)], COMP, 2.4)
    if kind == 'slide':
        o += L(fx - 20, y + 130, fx + 120, y + 130, COMP, 2.4, '6 3') + A(fx + 60, y + 118, fx + 10, y + 118, COMP, 2, 8)
    return o


def fig6_2():
    W, H = 900, 230
    o = ''
    items = [('① 拉斷', 'break'), ('② 拔出', 'pull'), ('③ 面板連接', 'conn'), ('④ 面板鼓出', 'bulge'), ('⑤ 沿加勁層滑', 'slide')]
    for k, (t, kind) in enumerate(items):
        o += _mini(20 + k * 176, 20, t, kind)
    return svg(W, H, o, '五種內穩定模式')


def fig6_3():
    d = ex2016_3()
    W, H = 900, 330
    pl = Plot(130, 40, 520, 240, 0, 4, 0, 3)
    o = ''
    rows = [('傾覆', d['FS_OT'], 2.0), ('滑動', d['FS_SL'], 1.5), ('承載', d['FS_BC'], 3.0)]
    for k, (nm, v, th) in enumerate(rows):
        y = 60 + k * 80
        o += T(120, y + 24, nm, 16, INK, 'end', 'bold')
        ok = v >= th
        c = TEN if ok else COMP
        o += R(130, y, v * 130, 36, TEN2 if ok else COMP2, c, 1.6)
        o += T(130 + v * 130 + 8, y + 24, f'{v:.2f}' + ('（適宜）' if ok else '（不足）'), 15, c, 'start', 'bold')
        o += L(130 + th * 130, y - 8, 130 + th * 130, y + 44, KEY, 2, '5 3')
        o += T(130 + th * 130, y - 12, f'門檻 {th}', 14, KEY, 'middle')
    return svg(W, H, o, '2016-3 外穩定')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
