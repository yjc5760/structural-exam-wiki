# -*- coding: utf-8 -*-
"""第 4 章：Macaulay 分段、種子 S6（面積×形心縱距）、圖乘表、拋物線 2/3 與 3/8、Simpson、SA-2016-3、SA-2014-4 拆圖。"""
from sa_draw import *  # noqa
import math
import calcs
from fractions import Fraction as Fr

C3, C3X, C4 = calcs.C3, calcs.C3X, calcs.C4
ENE = PUR


def _row(pl, fn, a, b, c, fill, label, x0):
    o = bmd(pl, fn, a, b, c, fill)
    o += T(x0 - 14, pl.Y(0) + 5, label, 16, c, 'end', 'bold')
    return o


# ------------------------------------------------------------------ 圖 4-1 Macaulay：開關打開
def fig4_1():
    W, H = 900, 560
    x0, Lpx = 170, 520
    Cy = float(C3X['13_Cy'])
    o = ''
    yb = 64
    # 梁 BC：B 在左、C 在右，x 自 C 往左
    o += L(x0, yb, x0 + Lpx, yb, INK, 4) + pin(x0 + Lpx, yb)
    o += T(x0 - 8, yb + 6, 'B', 16, INK, 'end', 'bold') + T(x0 + Lpx + 18, yb + 6, 'C', 16, INK, 'start', 'bold')
    o += A(x0 + Lpx / 2, yb - 50, x0 + Lpx / 2, yb - 4, LOAD, 2.4, 10) + T(x0 + Lpx / 2 + 8, yb - 30, '20 kN', 15, LOAD, 'start', 'bold')
    o += A(x0 + Lpx + 44, yb + 46, x0 + Lpx + 44, yb + 4, FOR, 2.2, 9) + T(x0 + Lpx + 52, yb + 46, '*C*_{y} = 55/7', 15, FOR, 'start', 'bold')
    o += A(x0 + Lpx - 10, yb + 50, x0 + Lpx - 90, yb + 50, MUT, 1.3, 8) + T(x0 + Lpx - 96, yb + 56, '*x*', 15, MUT, 'end')
    rows = [
        (180, '*C*_{y}·*x*', lambda x: Cy * x, FOR, TENM, -110, 90, [(10, f'{Cy*10:.2f}', -10)], '一直都在'),
        (320, '−20⟨*x* − 5⟩', lambda x: -20 * max(0.0, x - 5), LOAD, WARNM, -110, 90, [(10, '−100', 22)], '*x* < 5：開關關著＝0'),
        (460, '*M*', lambda x: Cy * x - 20 * max(0.0, x - 5), MOM, '#ef9a9a', -110, 90,
         [(5, f'{Cy*5:.2f}', -10), (10, f'{Cy*10-100:.2f}'.replace('-', '−'), 22)], '相加＝一條式子'),
    ]
    for y, lab, fn, c, fill, ymin, ymax, ticks, note in rows:
        pl = Plot(x0, y - 70, Lpx, 100, -10, 0, ymin, ymax)
        o += _row(pl, lambda u, fn=fn: fn(-u), -10, 0, c, fill, lab, x0)
        for xm, t, dy in ticks:
            o += T(pl.X(-xm), pl.Y(fn(xm)) + dy, t, 15, c, 'middle' if xm != 10 else 'start', 'bold')
        o += T(x0 + Lpx + 16, pl.Y(0) + 5, note, 15, INK, 'start')
        o += L(pl.X(-5), pl.Y(ymin * 0.9), pl.X(-5), pl.Y(ymax * 0.9), STEEL, 1.1, '4 4')
    o += T(x0 + Lpx / 2, 530, '*x* = 5：開關在這裡打開（載重作用點）', 15, MUT, 'middle')
    o += T(x0 + Lpx / 2, 552, '*M*_{BC} = *C*_{y}*x* − 20⟨*x* − 5⟩，⟨*u*⟩ = *u*（*u* ≥ 0）、0（*u* < 0）', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, 'Macaulay 括號')


# ------------------------------------------------------------------ 圖 4-2 種子 S6
def fig4_2():
    W, H = 900, 450
    Lm = 6.0
    Mf = lambda x: 6 * x - x * x + 2      # 任意形狀（示意）：拋物線＋常數
    mf = lambda x: 1 + x / 3              # 直線
    n = 6000
    dx = Lm / n
    xs = [(i + 0.5) * dx for i in range(n)]
    Aa = sum(Mf(x) for x in xs) * dx
    xb = sum(x * Mf(x) for x in xs) * dx / Aa
    exact = sum(Mf(x) * mf(x) for x in xs) * dx
    x0, Lpx = 140, 460
    o = ''
    pl = Plot(x0, 40, Lpx, 170, 0, Lm, 0, 12)
    o += pl.area(Mf, lambda x: 0, 0, Lm, '#ef9a9a', 0.45)
    o += pl.curve(Mf, 0, Lm, MOM, 2.6) + L(pl.X(0), pl.Y(0), pl.X(Lm), pl.Y(0), INK, 1.4)
    o += T(x0 - 14, pl.Y(4), '*M*', 17, MOM, 'end', 'bold')
    o += T(pl.X(1.4), pl.Y(3.6), '面積 *A*', 16, ENE, 'middle', 'bold')
    o += C(pl.X(xb), pl.Y(4.6), 6, ENE, '#fff', 2)
    o += T(pl.X(xb) + 10, pl.Y(4.6) - 8, '形心', 15, ENE, 'start', 'bold')
    pm = Plot(x0, 260, Lpx, 110, 0, Lm, 0, 3.4)
    o += P([pm.pt(0, 0), pm.pt(0, mf(0)), pm.pt(Lm, mf(Lm)), pm.pt(Lm, 0)], None, fill=TENM, close=True, op=0.4)
    o += pm.curve(mf, 0, Lm, FOR, 2.6) + L(pm.X(0), pm.Y(0), pm.X(Lm), pm.Y(0), INK, 1.4)
    o += T(x0 - 14, pm.Y(1.4), '*m*', 17, FOR, 'end', 'bold')
    o += L(pl.X(xb), pl.Y(4.6), pm.X(xb), pm.Y(mf(xb)), ENE, 1.6, '6 4')
    o += C(pm.X(xb), pm.Y(mf(xb)), 5, FOR, '#fff', 1.8)
    o += T(pm.X(xb) + 10, pm.Y(mf(xb)) - 10, '*m*(*x̄*)', 16, FOR, 'start', 'bold')
    o += T(pm.X(xb), pm.Y(0) + 22, '*x̄*', 16, ENE, 'middle', 'bold')
    bx = 640
    o += R(bx, 50, 248, 320, KEY2, PUR, 1.4, 10)
    yy = 82
    for s, c, wgt, sz in [('為什麼可以這樣算？', PUR, 'bold', 16), ('', INK, None, 4),
                          ('*m* 是直線：*m* = *c*_{0} + *c*_{1}*x*', INK, None, 15),
                          ('∫*Mm* = *c*_{0}∫*M* + *c*_{1}∫*xM*', INK, None, 15),
                          ('= *c*_{0}*A* + *c*_{1}*A* *x̄*', INK, None, 15), ('= *A*(*c*_{0} + *c*_{1}*x̄*)', INK, None, 15),
                          ('= *A*·*m*(*x̄*)', PUR, 'bold', 17), ('', INK, None, 8),
                          (f'本圖：*A* = {Aa:.1f}，*x̄* = {xb:.2f}', MUT, None, 14),
                          (f'*A*·*m*(*x̄*) = {Aa*mf(xb):.1f}', MUT, None, 14),
                          (f'直接積分 = {exact:.1f} ✔', FOR, 'bold', 14)]:
        if s:
            o += T(bx + 124, yy, s, sz, c, 'middle', wgt)
        yy += sz + 11 if s else 6
    o += R(140, 402, 620, 36, KEY2, PUR, 1.2, 8)
    o += T(450, 426, '種子 S6：直線 × 任意 = 面積 × 形心處的直線高度（*M* 可以是任何形狀）', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, '種子 S6')


# ------------------------------------------------------------------ 圖 4-3 圖乘表
def _icon(x, y, w, h, kind, c, fill):
    if kind == 'rect':
        pts = [(x, y + h), (x, y), (x + w, y), (x + w, y + h)]
    elif kind == 'triR':
        pts = [(x, y + h), (x + w, y), (x + w, y + h)]
    elif kind == 'triL':
        pts = [(x, y + h), (x, y), (x + w, y + h)]
    else:   # parab
        pts = [(x + w * i / 30, y + h - h * 4 * (i / 30) * (1 - i / 30)) for i in range(31)]
    o = P(pts, None, fill=fill, close=True, op=0.55) + P(pts, c, 2)
    o += L(x, y + h, x + w, y + h, INK, 1.2)
    return o


def fig4_3():
    W, H = 900, 500
    o = ''
    x0, cw = 220, 222
    y0, rh = 110, 86
    cols = [('rect', '*c*'), ('triR', '*c*（右端）'), ('triL', '*c*（左端）')]
    rows = [('rect', '*a*'), ('triR', '*a*（右端）'), ('triL', '*a*（左端）'), ('parab', '*a*（中央）')]
    vals = [['*L*·*ac*', '½*L*·*ac*', '½*L*·*ac*'],
            ['½*L*·*ac*', '⅓*L*·*ac*', '⅙*L*·*ac*'],
            ['½*L*·*ac*', '⅙*L*·*ac*', '⅓*L*·*ac*'],
            ['⅔*L*·*ac*', '⅓*L*·*ac*', '⅓*L*·*ac*']]
    hl = {(1, 1): '同側三角', (1, 2): '反側三角', (3, 0): '拋物線'}
    o += T(x0 / 2, 60, '*M* ＼ *m*', 17, INK, 'middle', 'bold')
    for j, (k, lab) in enumerate(cols):
        cx = x0 + j * cw
        o += R(cx, 24, cw, y0 - 24, '#e8f5e9', STEEL, 1)
        o += _icon(cx + 30, 36, 70, 44, k, FOR, TENM) + T(cx + 112, 66, lab, 15, FOR, 'start', 'bold')
    for i, (k, lab) in enumerate(rows):
        cy = y0 + i * rh
        o += R(10, cy, x0 - 10, rh, '#ffebee', STEEL, 1)
        o += _icon(24, cy + 20, 70, 46, k, MOM, '#ef9a9a') + T(104, cy + 50, lab, 15, MOM, 'start', 'bold')
        for j in range(3):
            cx = x0 + j * cw
            key = (i, j)
            o += R(cx, cy, cw, rh, KEY2 if key in hl else '#fff', STEEL, 1)
            o += T(cx + cw / 2, cy + rh / 2 + 7, vals[i][j], 20, PUR if key in hl else INK, 'middle', 'bold')
    o += R(10, 466 - 4, 880, 34, '#fffde7', '#fbc02d', 1.2, 8)
    o += T(450, 486, '梯形（左 *a*、右 *b*）×梯形（左 *c*、右 *d*）＝ *L*/6·(2*ac* + *ad* + *bc* + 2*bd*)：上表全部是它的特例', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '圖乘表')


# ------------------------------------------------------------------ 圖 4-4 拋物線 2/3、3/8 與 Simpson
def fig4_4():
    W, H = 900, 450
    w, Lm, h = float(C4['par_w']), float(C4['par_L']), float(C4['par_h'])
    Mf = lambda x: w * x * (Lm - x) / 2
    o = T(250, 30, '(a) 簡支梁均布載重的彎矩圖（*w* = 2、*L* = 12）', 16, INK, 'middle', 'bold')
    pl = Plot(40, 60, 420, 220, 0, 12, 0, 40)
    o += L(pl.X(0), pl.Y(0), pl.X(12), pl.Y(0), INK, 1.4)
    # 右半：曲線下 2/3、上方 1/3
    o += P([pl.pt(6, 0)] + [pl.pt(6 + 6 * i / 40, Mf(6 + 6 * i / 40)) for i in range(41)], None, fill='#ef9a9a', close=True, op=0.5)
    o += P([pl.pt(6, h)] + [pl.pt(6 + 6 * i / 40, Mf(6 + 6 * i / 40)) for i in range(41)] + [pl.pt(12, h)], None, fill=STEEL3, close=True, op=0.7)
    o += pl.area(Mf, lambda x: 0, 0, 6, '#ef9a9a', 0.22)
    o += pl.curve(Mf, 0, 12, MOM, 2.6)
    o += L(pl.X(6), pl.Y(h), pl.X(12), pl.Y(h), STEEL, 1.4, '5 4') + L(pl.X(12), pl.Y(h), pl.X(12), pl.Y(0), STEEL, 1.4, '5 4')
    o += L(pl.X(6), pl.Y(0), pl.X(6), pl.Y(h), INK, 1.2, '4 4')
    o += T(pl.X(6), pl.Y(h) - 10, '頂點 *h* = *wL*^{2}/8 = 36', 15, MOM, 'middle', 'bold')
    xb = 6 + float(C4['par_xbar_half'])
    o += C(pl.X(xb), pl.Y(12), 6, ENE, '#fff', 2) + L(pl.X(xb), pl.Y(0), pl.X(xb), pl.Y(12) + 6, ENE, 1.4, '4 3')
    o += T(pl.X(8.9), pl.Y(17), '⅔*bh*', 18, ENE, 'middle', 'bold')
    o += T(pl.X(11.1), pl.Y(31), '⅓', 18, MUT, 'middle', 'bold')
    o += dim(pl.X(6), pl.Y(0) + 26, pl.X(xb), pl.Y(0) + 26, '', ENE) + T((pl.X(6) + pl.X(xb)) / 2, pl.Y(0) + 50, '⅜*b*', 16, ENE, 'middle', 'bold')
    o += dim(pl.X(6), pl.Y(0) + 64, pl.X(12), pl.Y(0) + 64, '', MUT) + T(pl.X(9), pl.Y(0) + 88, '*b* = 6', 15, MUT, 'middle')
    o += T(pl.X(2.5), pl.Y(0) + 40, '全跨：⅔*Lh* = *wL*^{3}/12', 15, MOM, 'middle', 'bold')
    # (b) Simpson
    bx = 500
    o += T(bx + 195, 30, '(b) 一條公式全包：Simpson', 16, INK, 'middle', 'bold')
    o += R(bx, 52, 390, 300, KEY2, PUR, 1.4, 10)
    yy = 88
    for s, c, wgt, sz in [('∫*Mm* *dx* = *L*/6·(*M*_{左}*m*_{左} + 4*M*_{中}*m*_{中} + *M*_{右}*m*_{右})', PUR, 'bold', 15),
                          ('只要 *M*·*m* 不超過三次式就「完全正確」', INK, None, 15),
                          ('（拋物線×直線＝三次，剛好可以）', MUT, None, 14), ('', INK, None, 6),
                          ('驗算 1：三角×三角（同側）', INK, 'bold', 15),
                          ('*L*/6·(0 + 4·½*a*·½*c* + *ac*) = ⅓*Lac* ✔', FOR, None, 15),
                          ('驗算 2：拋物線×三角', INK, 'bold', 15),
                          ('*L*/6·(0 + 4·*h*·½ + 0) = ⅓*Lh*', FOR, None, 15),
                          (f'代 *h* = 36、*L* = 12：{float(C4["par_x_tri"]):.0f} ✔（直接積分 {float(C4["par_x_tri_direct"]):.0f}）', FOR, None, 15),
                          ('驗算 3：拋物線×常數 1', INK, 'bold', 15),
                          ('*L*/6·(0 + 4*h* + 0) = ⅔*Lh* ✔', FOR, None, 15)]:
        if s:
            o += T(bx + 195, yy, s, sz, c, 'middle', wgt)
        yy += sz + 11 if s else 6
    o += R(40, 396, 820, 40, '#fffde7', '#fbc02d', 1.2, 8)
    o += T(450, 422, '記法：拋物線「肚子」佔外框 ⅔，形心離頂點 ⅜*b*（比一半 ½ 近一點，因為肚子靠頂點那邊比較胖）', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '拋物線與 Simpson')


# ------------------------------------------------------------------ 圖 4-5 SA-2016-3：柱 CD
def fig4_5():
    W, H = 900, 500
    Mt, Mb, Lc = float(C4['16_Mt']), float(C4['16_Mb']), float(C4['16_L'])
    Mf = lambda y: Mt + (Mb - Mt) * y / Lc
    mf = lambda y: y
    x0, Lpx = 150, 520
    o = T(x0 + Lpx / 2, 28, '把柱 CD 放倒來看：*y* 從 C（左）往 D（右），左側受拉為正', 15, MUT, 'middle')
    pl = Plot(x0, 50, Lpx, 140, 0, 20, -30, 22)
    o += _row(pl, Mf, 0, 20, MOM, '#ef9a9a', '*M*', x0)
    o += T(pl.X(0) + 6, pl.Y(Mt) + 22, '−25.3（C）', 15, MOM, 'start', 'bold')
    o += T(pl.X(20) - 4, pl.Y(Mb) - 10, '+17.0（D）', 15, MOM, 'end', 'bold')
    y0 = float(C4['16_y0'])
    o += pl.dot(y0, 0, MOM, 4) + T(pl.X(y0), pl.Y(0) + 24, f'{y0:.2f}', 14, MOM, 'middle')
    pm = Plot(x0, 230, Lpx, 110, 0, 20, 0, 22)
    o += _row(pm, mf, 0, 20, FOR, TENM, '*m*', x0)
    o += T(pm.X(20) - 4, pm.Y(20) - 8, '20', 15, FOR, 'end', 'bold') + T(pm.X(10), pm.Y(10) - 12, '10', 15, FOR, 'middle', 'bold')
    o += T(x0 + Lpx + 16, pl.Y(0) + 5, '直線（梯形）', 15, INK, 'start') + T(x0 + Lpx + 16, pm.Y(5), 'C 向右單位力', 15, INK, 'start')
    o += T(x0 + Lpx + 16, pm.Y(5) + 20, '*m* = *y*', 15, FOR, 'start', 'bold')
    o += R(60, 372, 780, 116, KEY2, PUR, 1.4, 10)
    o += T(450, 400, '梯形公式（*a* = −25.3、*b* = 17.0、*c* = 0、*d* = 20）：', 15, INK, 'middle', 'bold')
    o += T(450, 428, '*EI*·Δ_{Cx} = 20/6·[0 + (−25.3)(20) + 0 + 2(17.0)(20)] = 20/6 × 174 = 580', 16, PUR, 'middle', 'bold')
    o += T(450, 456, 'Simpson：20/6·[0 + 4(−4.15)(10) + 17.0×20] = 580 ✔　兩種寫法同一個數', 15, INK, 'middle')
    o += T(450, 480, 'Δ_{Cx} = 580/*EI*（向右）；θ_{C} = *M* 圖淨面積 = −83 ⇒ 83/*EI*（逆時針）', 15, FOR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2016-3 圖乘')


# ------------------------------------------------------------------ 圖 4-6 SA-2014-4 拆圖
def fig4_6():
    W, H = 900, 520
    x0, Lpx = 150, 480
    R_ = float(C3['R'])
    o = T(x0 + Lpx / 2, 26, '*x* 自 C（右）量；A 在左', 15, MUT, 'middle')
    specs = [
        (40, '*R* 的三角形', lambda x: R_ * x, MOM, '#ef9a9a', -10, 85, [(12, '75', -10)], '0 → 12*R* = 75'),
        (150, '載重的三角形', lambda x: -20 * max(0.0, x - 6), MOM, '#ef9a9a', -130, 10, [(12, '−120', 24)], '只在 BA 段'),
        (280, '*m*_{2} = 1', lambda x: 1.0, FOR, TENM, -0.3, 1.5, [], '求 θ_{C}'),
        (370, '*m*_{1} = *x*', lambda x: x, FOR, TENM, -2, 14, [(12, '12', -10)], '求 *R*（向上單位力）'),
    ]
    for y, lab, fn, c, fill, ymin, ymax, ticks, note in specs:
        hh = 70 if y != 280 else 50
        pl = Plot(x0, y, Lpx, hh, -12, 0, ymin, ymax)
        o += _row(pl, lambda u, fn=fn: fn(-u), -12, 0, c, fill, lab, x0)
        for xm, t, dy in ticks:
            o += T(pl.X(-xm) + 6, pl.Y(fn(xm)) + dy, t, 15, c, 'start', 'bold')
        o += T(x0 + Lpx + 14, pl.Y(0) + 5, note, 15, INK, 'start')
    o += R(60, 452, 780, 60, KEY2, PUR, 1.4, 10)
    o += T(450, 476, 'θ：½·12·75 × 1 ＋ ½·6·(−120) × 1 = 450 − 360 = 90　|　*f*_{11}：⅓·12·12·12 = 576', 15, PUR, 'middle', 'bold')
    o += T(450, 500, 'δ_{10}：載重三角形 × *m*_{1}（6→12 的梯形）= 6/6·[2·0·6 + 0·12 + (−120)·6 + 2(−120)(12)] = −3600', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2014-4 拆圖')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4, 'fig4_5': fig4_5, 'fig4_6': fig4_6}
