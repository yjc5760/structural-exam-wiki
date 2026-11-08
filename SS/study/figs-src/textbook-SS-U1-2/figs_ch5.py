# -*- coding: utf-8 -*-
"""第 5 章：Cb＝最大彎矩 ÷ 加權平均；五種彎矩圖；SS-2024-3 外伸梁。"""
from plot import *  # noqa
import calcs


def fig5_1():
    W = 900
    n = len(calcs.CB_CASES)
    cw, ch = 170, 190
    H = ch + 150
    o = ''
    for i, (name, fn) in enumerate(calcs.CB_CASES):
        x0 = 12 + i * (cw + 6)
        y0 = 70
        cb = calcs.cb_from_fn(fn)
        o += R(x0, 30, cw, ch + 70, '#fff', STEEL, 1.2, 10)
        o += T(x0 + cw / 2, 52, name, 14, INK, 'middle', 'bold')
        bx0, bx1, base, amp = x0 + 14, x0 + cw - 14, y0 + 80, 62
        o += L(bx0, base, bx1, base, INK, 1.6)
        o += T(bx0, base + 18, '×', 18, KEY, 'middle', 'bold') + T(bx1, base + 18, '×', 18, KEY, 'middle', 'bold')
        pts = [(bx0 + (bx1 - bx0) * k / 100, base - amp * fn(k / 100)) for k in range(101)]
        fill = [(bx0, base)] + pts + [(bx1, base)]
        o += P(fill, None, fill=COMP2, close=True)
        o += P(pts, COMP, 2.2)
        for q in (0.25, 0.5, 0.75):
            xx = bx0 + (bx1 - bx0) * q
            o += L(xx, base, xx, base - amp * fn(q), KEY, 1.4, '3 3')
            o += C(xx, base - amp * fn(q), 3.5, KEY, None)
        big = cb > 2.0
        o += T(x0 + cw / 2, y0 + ch + 6, f'*C*_{{b}} = {cb:.3f}' if not big else f'*C*_{{b}} = {cb:.2f}', 17, KEY if cb > 1.01 else COMP, 'middle', 'bold')
    o += T(W / 2, H - 12, '×＝側撐點；紫點＝四分點 A、B、C 的彎矩。彎矩越「不平均」，*C*_{b} 越大', 15, INK, 'middle')
    return svg(W, H, o, '五種彎矩圖的 Cb')


def fig5_2():
    """SS-2024-3：A 鉸、C 滾（3 m）、B 外伸端（再 3 m）受 Pu；側撐只在 A、B → Lb = 6 m。"""
    W, H = 900, 400
    o = ''
    x0, x1, yb = 120, 720, 120
    sc = (x1 - x0) / 6
    X = lambda m: x0 + m * sc
    o += L(X(0), yb, X(6), yb, INK, 5)
    o += pin(X(0), yb + 3)
    o += C(X(3), yb + 11, 8, '#fff', INK, 1.6) + hatch_ground(X(3) - 16, yb + 19, 32)
    o += A(X(6), yb - 70, X(6), yb - 6, COMP, 3, 12) + T(X(6) + 10, yb - 50, '*P*_{u} = 14 tf', 15, COMP, 'start', 'bold')
    for m in (0, 6):
        o += T(X(m), yb - 14, '×', 22, KEY, 'middle', 'bold')
    o += T(X(0), yb + 50, 'A（鉸）', 14, INK, 'middle') + T(X(3), yb + 50, 'C（滾，不側撐）', 14, INK, 'middle') + T(X(6), yb + 50, 'B（外伸端）', 14, INK, 'middle')
    # 彎矩圖（負彎矩畫在下方）
    mb = 250
    Mf = lambda m: (m / 3) * (-42) if m <= 3 else (6 - m) / 3 * (-42)
    pts = [(X(k / 20), mb + abs(Mf(k / 20)) * 2.0) for k in range(121)]
    o += L(X(0), mb, X(6), mb, INK, 1.4)
    o += P([(X(0), mb)] + pts + [(X(6), mb)], None, fill=COMP2, close=True)
    o += P(pts, COMP, 2.4)
    for q, lab in ((1.5, 'A'), (3, 'B'), (4.5, 'C')):
        v = abs(Mf(q))
        o += L(X(q), mb, X(q), mb + v * 2, KEY, 1.4, '3 3') + C(X(q), mb + v * 2, 4, KEY, None)
        o += T(X(q) + 12, mb + v * 2 + (18 if q == 3 else -10), f'*M*_{{{lab}}} = {v:.0f}', 14, KEY, 'start', 'bold')
    o += T(X(0) - 10, mb + 5, '*M*', 15, INK, 'end')
    cb = calcs.ex_2024_3()['Cb']
    o += box(740, 200, 150, 120, '*C*_{b}', ['12.5×42 ÷', '(105+63+168+63)', f'= {cb:.3f}'], KEY2, KEY, 17, 14)
    o += T(X(3), 388, '無側撐段 A→B 長 6 m；四分點在 1.5、3、4.5 m（單位 t·m）', 14, MUT, 'middle')
    return svg(W, H, o, 'SS-2024-3 Cb')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
