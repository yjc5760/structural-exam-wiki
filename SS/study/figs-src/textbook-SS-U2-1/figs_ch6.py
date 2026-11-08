# -*- coding: utf-8 -*-
"""第 6 章：上下限夾擠、彎矩圖檢查（正解 vs 跨中錯解）、三個載重等級、門型剛架三種機構。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    W, H = 900, 330
    x0, x1 = 80, 820
    lo, hi = 7.5, 12.8
    X = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    y = 170
    o = A(x0, y, x1 + 20, y, INK, 1.8, 10)
    for t in (8, 9, 10, 11, 12):
        o += L(X(t), y - 5, X(t), y + 5, INK, 1.2) + T(X(t), y + 26, f'{t}', 14, MUT, 'middle')
    o += T(x1 + 24, y + 26, '*w*·*L*^{2}/*M*_{p}', 14, INK, 'end')
    o += L(X(COEF_PC_U), 40, X(COEF_PC_U), 300, KEY, 2.4, '6 4')
    o += T(X(COEF_PC_U), 320, f'真正的 *w*_{{u}} = {COEF_PC_U:.3f}', 15, KEY, 'middle', 'bold')
    ups = [(UB_DEMO[0][1], f'鉸在 0.3*L* → {UB_DEMO[0][1]:.2f}'), (UB_DEMO[1][1], f'← 鉸在跨中 12.00')]
    for i, (v, t) in enumerate(ups):
        yy = 70 + i * 40
        o += A(X(v), yy, X(v), y - 8, COMP, 2.2, 10)
        o += T(X(v) + 8 if i == 0 else X(UB_DEMO[0][1]) + 10, yy + 4, t, 14, COMP, 'start', 'bold')
    o += T(x0, 52, '機構法（上限）：任何猜的機構 → 從上面逼近', 15, COMP, 'start', 'bold')
    lows = [(8.0, '彈性第一鉸 → 8'), (LB_DEMO, f'固端 −*M*_{{p}}、跨內 {prop_span_max(LB_DEMO)[0]:.2f}*M*_{{p}} → 11')]
    for i, (v, t) in enumerate(lows):
        yy = 270 - i * 40
        o += A(X(v), yy, X(v), y + 36, TEN, 2.2, 10)
        o += T(X(v) + (8 if i == 0 else -8), yy + 4, t, 14, TEN, 'start' if i == 0 else 'end', 'bold')
    o += T(x0, 300, '靜力法（下限）：任何 |*M*| ≤ *M*_{p} 的平衡彎矩圖 → 從下面逼近', 15, TEN, 'start', 'bold')
    return svg(W, H, o, '上限與下限夾住真正的崩塌載重')


def fig6_2():
    W, H = 900, 400
    pl = Plot(90, 40, 560, 300, 0, 1, -1.2, 1.2)
    o = pl.axes([0, 0.25, X_PROP, 0.5, 0.75, 1], [-1, -0.5, 0, 0.5, 1], '*x*/*L*', '*M*/*M*_{p}', size=14,
                xfmt=lambda v: f'{v:.3f}' if abs(v - X_PROP) < 1e-6 else f'{v:g}')
    o += pl.hline(1, c=KEY, w=1.4) + pl.hline(-1, c=KEY, w=1.4) + pl.hline(0, c=INK, w=1, dash=None)
    for wc, c, dash in ((COEF_PC_U, COMP, None), (wu_prop(0.5), WARN, '8 5')):
        o += pl.curve(lambda x, wc=wc: (wc / 2 - 1) * x - wc * x * x / 2, 0, 1, c, 3, dash, clip=False)
    o += pl.dot(X_PROP, 1, COMP, 6)
    mx, xm = WRONG_MAX
    o += pl.dot(xm, mx, WARN, 5)
    o += T(pl.X(xm) + 10, pl.Y(mx) - 12, f'跨中鉸的機構：最大 {mx:.3f}*M*_{{p}} ＞ *M*_{{p}} ✘', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.05), pl.Y(-0.4), f'正解（鉸在 0.414*L*）：最大剛好 = *M*_{{p}} ✔', 14, COMP, 'start', 'bold')
    o += R(680, 90, 210, 190, KEY2, KEY, 1.4, 10)
    for i, s in enumerate(['機構法的答案', '畫出彎矩圖', '處處 |*M*| ≤ *M*_{p}', '→ 也是下限', '→ 就是正解（唯一性）']):
        o += T(785, 122 + i * 32, s, 15, KEY if i >= 3 else INK, 'middle', 'bold' if i >= 3 else None)
    return svg(W, H, o, '以彎矩圖檢查崩塌機構')


def fig6_3():
    W, H = 900, 300
    x0, bw = 250, 560
    mx = W20_COLL
    rows = [('第一根纖維降伏 8*M*_{y}/*L*^{2}', W20_YIELD, AC), ('第一個鉸（固端）8*M*_{p}/*L*^{2}', W20_HINGE1, WARN), ('崩塌 11.66*M*_{p}/*L*^{2}', W20_COLL, COMP)]
    o = T(450, 30, 'SS-2020-2（*L* = 8 m）三個載重等級', 16, INK, 'middle', 'bold')
    for i, (t, v, c) in enumerate(rows):
        y = 60 + i * 66
        o += T(x0 - 12, y + 28, t, 14, INK, 'end')
        o += R(x0, y + 8, v / mx * bw, 34, c, None, 0, 5)
        o += T(x0 + v / mx * bw - 8, y + 31, f'{v:.2f} tf/m', 15, '#fff', 'end', 'bold')
    o += T(x0, 280, f'× *f* = {W20_HINGE1 / W20_YIELD:.3f}（斷面儲備）', 15, AC, 'start', 'bold')
    o += T(x0 + 290, 280, f'× {W20_COLL / W20_HINGE1:.3f}（彎矩重分配）', 15, COMP, 'start', 'bold')
    return svg(W, H, o, 'SS-2020-2 三個載重等級')


def _frame(x, y, w, h, kind, lam):
    o = ''
    base = [(x, y), (x, y - h), (x + w, y - h), (x + w, y)]
    o += P(base, STEEL, 1.4, dash='5 4')
    d = 30
    if kind == 'beam':
        pts = [(x, y), (x, y - h), (x + w / 2, y - h + d), (x + w, y - h), (x + w, y)]
        hs = [(x, y - h), (x + w / 2, y - h + d), (x + w, y - h)]
    elif kind == 'sway':
        pts = [(x, y), (x + d, y - h), (x + w + d, y - h), (x + w, y)]
        hs = [(x, y), (x + d, y - h), (x + w + d, y - h), (x + w, y)]
    else:
        pts = [(x, y), (x + d, y - h), (x + w / 2 + d, y - h + d * 1.4), (x + w + d, y - h), (x + w, y)]
        hs = [(x, y), (x + w / 2 + d, y - h + d * 1.4), (x + w + d, y - h), (x + w, y)]
    o += P(pts, COMP, 3.2)
    o += hatch_ground(x - 16, y, 32) + hatch_ground(x + w - 16, y, 32)
    for hx, hy in hs:
        o += C(hx, hy, 7, '#fff', COMP, 2.4)
    o += A(x + w / 2, y - h - 50, x + w / 2, y - h - 8, WARN, 2.2, 10) + T(x + w / 2 + 8, y - h - 34, '*P*', 15, WARN, 'start', 'bold')
    o += A(x - 50, y - h, x - 8, y - h, WARN, 2.2, 10) + T(x - 44, y - h - 10, '*H*', 15, WARN, 'start', 'bold')
    return o


def fig6_4():
    W, H = 900, 400
    r = portal(**PF_EX)
    items = [('beam', '① 梁機構（3 鉸）', '*P*·(*L*/2)*θ* = 4*M*_{p}*θ*', r['beam']),
             ('sway', '② 側移機構（4 鉸）', '*H*·*hθ* = 4*M*_{p}*θ*', r['sway']),
             ('comb', '③ 組合機構（4 鉸）', '*H*·*hθ* + *P*·(*L*/2)*θ* = 6*M*_{p}*θ*', r['comb'])]
    o = ''
    for i, (k, t, eq, lam) in enumerate(items):
        x0 = 70 + i * 290
        o += T(x0 + 85, 40, t, 15, INK, 'middle', 'bold')
        o += _frame(x0, 260, 170, 150, k, lam)
        o += T(x0 + 85, 300, eq, 14, INK, 'middle')
        best = lam == min(r.values())
        o += R(x0 - 5, 318, 180, 34, KEY2 if best else STEEL2, None, 0, 8)
        o += T(x0 + 85, 341, f'載重倍數 λ = {lam:.3f}' + (' ← 控制' if best else ''), 15, KEY if best else INK, 'middle', 'bold')
    o += T(450, 388, f'自訂示範：柱腳固定、等斷面 *M*_{{p}} = {PF_EX["Mp"]:,.0f} tf·cm、*L* = 6 m、*h* = 4 m、*P* = {PF_EX["P"]:g} tf、*H* = {PF_EX["H"]:g} tf', 14, MUT, 'middle')
    return svg(W, H, o, '門型剛架三種崩塌機構')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
