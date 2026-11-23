# -*- coding: utf-8 -*-
"""第 1 章：樁的自由體、分項 FS、抗拔累積曲線。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def _pile(o, cx, top, bot, w=34):
    o += R(cx - w / 2, top, w, bot - top, STEEL2, INK, 1.6)
    return o


def fig1_1():
    W, H = 900, 470
    o = ''
    for k, (cx, title, up) in enumerate([(230, '(a) 受壓樁', False), (670, '(b) 抗拔樁', True)]):
        gl = 110
        o += R(cx - 170, gl, 340, 300, SOIL, None)
        o += L(cx - 170, gl, cx + 170, gl, SOILE, 2)
        o += T(cx, 34, title, 17, INK, 'middle', 'bold')
        top, bot = 70, 360
        o = _pile(o, cx, top, bot)
        # 樁頂荷重
        if not up:
            o += A(cx, 18 + 30, cx, top - 2, COMP, 3.2, 13)
            o += T(cx + 14, 54, '*Q* （樁頂荷重）', 15, COMP, 'start', 'bold')
        else:
            o += A(cx, top + 2, cx, 46, COMP, 3.2, 13)
            o += T(cx + 14, 54, '*T* （拉拔力）', 15, COMP, 'start', 'bold')
        # 側摩擦
        for y in range(140, 350, 42):
            if not up:
                o += A(cx - 40, y + 14, cx - 40, y - 14, TEN, 2.2, 9)
                o += A(cx + 40, y + 14, cx + 40, y - 14, TEN, 2.2, 9)
            else:
                o += A(cx - 40, y - 14, cx - 40, y + 14, TEN, 2.2, 9)
                o += A(cx + 40, y - 14, cx + 40, y + 14, TEN, 2.2, 9)
        lab = '*Q*_{s}（摩擦向上）' if not up else '*Q*_{s}（摩擦向下）'
        o += T(cx + 58, 230, lab, 15, TEN, 'start', 'bold')
        # 自重
        o += A(cx - 70, 200, cx - 70, 262, INK, 2, 9)
        o += T(cx - 78, 236, "*W*′", 15, INK, 'end', 'bold')
        # 樁底
        if not up:
            o += A(cx, bot + 50, cx, bot + 3, AC, 3, 12)
            o += T(cx + 14, bot + 40, '*Q*_{p}（端承）', 15, AC, 'start', 'bold')
        else:
            o += T(cx, bot + 30, '樁底拉開：沒有端承', 15, MUT, 'middle')
        # 平衡式
        eq = '*Q* + *W*′ = *Q*_{p} + *Q*_{s}' if not up else '*T* = *Q*_{s} + *W*′'
        o += R(cx - 150, 425, 300, 36, KEY2, KEY, 1.4, 8)
        o += T(cx, 449, eq, 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '受壓樁與抗拔樁的自由體圖')


def fig1_2():
    d = ex2007_3()
    W, H = 900, 400
    pl = Plot(110, 50, 470, 290, 0, 3, 0, 1500)
    o = pl.axes([], [0, 300, 600, 900, 1200, 1500], '', '*Q*（kN）')
    bw = 0.5
    # bar1: Qu = Qp + Qs
    x = 0.5
    o += R(pl.X(x - bw / 2), pl.Y(d['Qp']), pl.X(x + bw / 2) - pl.X(x - bw / 2), pl.Y(0) - pl.Y(d['Qp']), ACM, AC, 1.4)
    o += R(pl.X(x - bw / 2), pl.Y(d['Qp'] + d['Qs']), pl.X(x + bw / 2) - pl.X(x - bw / 2), pl.Y(d['Qp']) - pl.Y(d['Qp'] + d['Qs']), TENM, TEN, 1.4)
    o += T(pl.X(x), pl.Y(d['Qp'] / 2) + 5, f"*Q*_{{p}} {d['Qp']:.2f}", 14, AC, 'middle', 'bold')
    o += T(pl.X(x), pl.Y(d['Qp'] + d['Qs'] / 2) + 5, f"*Q*_{{s}} {d['Qs']:.2f}", 14, TEN, 'middle', 'bold')
    o += T(pl.X(x), pl.Y(0) + 24, '極限 *Q*_{u}', 15, INK, 'middle', 'bold')
    # bar2: 分項
    x = 1.5
    a, b = d['Qp'] / d['FSp'], d['Qs'] / d['FSs']
    o += R(pl.X(x - bw / 2), pl.Y(a), pl.X(x + bw / 2) - pl.X(x - bw / 2), pl.Y(0) - pl.Y(a), ACM, AC, 1.4)
    o += R(pl.X(x - bw / 2), pl.Y(a + b), pl.X(x + bw / 2) - pl.X(x - bw / 2), pl.Y(a) - pl.Y(a + b), TENM, TEN, 1.4)
    o += T(pl.X(x), pl.Y(a + b) - 10, f"{a + b:.2f}", 16, KEY, 'middle', 'bold')
    o += T(pl.X(x), pl.Y(0) + 24, '分項 ÷4、÷3', 15, KEY, 'middle', 'bold')
    # bar3: 整體 /4 和 /3
    x = 2.5
    for val, dash, lab in [(d['Qa_sum3'], None, '÷3'), (d['Qa_sum4'], '5 4', '÷4')]:
        o += L(pl.X(x - bw / 2), pl.Y(val), pl.X(x + bw / 2), pl.Y(val), COMP, 2.4, dash)
        o += T(pl.X(x + bw / 2) + 6, pl.Y(val) + 5, f'{lab} {val:.0f}', 14, COMP, 'start', 'bold')
    o += T(pl.X(x), pl.Y(0) + 24, '先加後除（錯）', 15, COMP, 'middle', 'bold')
    o += R(640, 70, 245, 150, KEY2, KEY, 1.4, 8)
    o += T(762, 98, '同一根樁，三種除法', 15, KEY, 'middle', 'bold')
    o += T(762, 126, '分項才對：412.83 kN', 15, INK, 'middle')
    o += T(762, 152, '先加後除 ÷3 偏大', 15, COMP, 'middle')
    o += T(762, 178, '先加後除 ÷4 偏小', 15, COMP, 'middle')
    o += T(762, 204, '兩個 FS 就分開除', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SM-2007-3 分項安全係數')


def fig1_3():
    d = ex2012_3()
    W, H = 900, 430
    pl = Plot(110, 50, 440, 330, 0, 1400, 0, 18)
    # depth axis downward: use Y inverted mapping manually
    def X(v): return pl.X(v)
    def Y(z): return 50 + z / 18 * 330
    o = ''
    for t in [0, 400, 800, 1200]:
        o += L(X(t), 50, X(t), 380, GRID, 1)
        o += T(X(t), 40, f'{t}', 14, MUT, 'middle')
    for z in [0, 4, 8, 12, 16]:
        o += L(110, Y(z), 550, Y(z), GRID, 1)
        o += T(100, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += A(110, 50, 572, 50, INK, 1.6, 9) + A(110, 50, 110, 398, INK, 1.6, 9)
    o += T(580, 46, '*T*（kN）', 16, INK, 'start')
    o += T(118, 412, '深度 *z*（m）', 15, INK, 'start')
    # layers
    o += R(560, Y(0), 30, Y(8) - Y(0), '#fff3e0', WARN, 1)
    o += R(560, Y(8), 30, Y(18) - Y(8), '#ffe0b2', WARN, 1)
    o += T(598, Y(4) + 5, '黏土 1：α=1、*c*_{u}=45', 14, INK, 'start')
    o += T(598, Y(12) + 5, '黏土 2：α=0.75、*c*_{u}=70', 14, INK, 'start')
    # curve
    def Tz(z):
        if z <= 8:
            return (d['a1'] * d['cu1'] * d['p'] + d['gcp'] * d['Ap']) * z
        return d['T1'] + d['k2'] * (z - 8)
    pts = [(X(Tz(z / 10)), Y(z / 10)) for z in range(0, 171)]
    o += P(pts, KEY, 3)
    o += L(X(1200), 50, X(1200), 380, COMP, 2, '6 4')
    o += T(X(1200) - 6, 72, '需求 1200', 14, COMP, 'end', 'bold')
    o += C(X(d['T1']), Y(8), 5, '#fff', KEY, 2)
    o += T(X(d['T1']) + 10, Y(8) - 6, f"8 m：{d['T1']:.1f}（不夠）", 14, KEY, 'start')
    o += C(X(1200), Y(d['L']), 6, KEY, '#fff', 2)
    o += L(110, Y(d['L']), X(1200), Y(d['L']), KEY, 1.4, '4 3')
    o += T(X(1200) - 10, Y(d['L']) + 26, f"*L* = {d['L']:.2f} m", 16, KEY, 'end', 'bold')
    return svg(W, H, o, 'SM-2012-3 累積抗拔力')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
