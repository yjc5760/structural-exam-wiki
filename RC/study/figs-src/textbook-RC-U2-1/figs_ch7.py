# -*- coding: utf-8 -*-
"""第 7 章：剪力摩擦四步、STM 桁架與各元件上限。"""
from figs_common import *  # noqa
from calcs import p2017_2, p2009_3
import math

P17 = p2017_2()
P09 = p2009_3()


def _teeth(x, y, w, amp, n, up=True):
    pts = []
    for i in range(n * 2 + 1):
        xx = x + w * i / (n * 2)
        yy = y + (0 if i % 2 == 0 else (-amp if up else amp))
        pts.append((xx, yy))
    return pts


def fig7_1():
    W, H = 900, 380
    o = T(450, 24, '剪力摩擦：要滑動就得撐開，撐開就把鋼筋拉緊', 16, INK, 'middle', 'bold')
    titles = ['① 粗糙介面受剪', '② 滑動 δ → 張開 *w*', '③ 鋼筋拉到 *f*_{y}', '④ 夾緊 → 摩擦']
    for k in range(4):
        cx = 115 + k * 225
        x, w = cx - 85, 170
        yi = 190
        gap = 0 if k == 0 else 12
        sl = 0 if k == 0 else 10
        top = _teeth(x + sl, yi - gap, w, 10, 5)
        bot = _teeth(x, yi, w, 10, 5)
        o += P([(x + sl, 90)] + top + [(x + sl + w, 90)], INK, 1.6, fill=STEEL2, close=True)
        o += P([(x, 290)] + bot + [(x + w, 290)], INK, 1.6, fill=STEEL3, close=True)
        # 鋼筋
        o += L(cx + sl / 2, 110, cx, 270, TEN if k >= 2 else STEEL, 3.5 if k >= 2 else 2.5)
        o += T(cx, 320, titles[k], 15, INK, 'middle', 'bold')
        if k == 0:
            o += A(x - 6, 130, x + 40, 130, WARN, 2.2, 9) + A(x + w + 6, 250, x + w - 40, 250, WARN, 2.2, 9)
            o += T(x + 4, 120, '*V*', 16, WARN, 'start', 'bold')
        if k == 1:
            o += A(x + w + 4, 150, x + w + 22, 150, WARN, 2, 8)
            o += T(x + w + 13, 138, 'δ', 15, WARN, 'middle', 'bold')
            o += A(cx + 60, yi - 26, cx + 60, yi - 48, AC, 1.8, 8) + A(cx + 60, yi + 10, cx + 60, yi + 30, AC, 1.8, 8)
            o += T(cx + 68, yi - 30, '*w*', 15, AC, 'start', 'bold')
        if k == 2:
            o += A(cx, 112, cx, 82, TEN, 2.4, 9) + A(cx, 268, cx, 298, TEN, 2.4, 9)
            o += T(cx + 18, 96, '*A*_{vf}*f*_{y}', 15, TEN, 'start', 'bold')
        if k == 3:
            o += A(cx - 50, 100, cx - 50, 166, COMP, 2.2, 9) + A(cx - 50, 280, cx - 50, 214, COMP, 2.2, 9)
            o += T(cx - 58, 140, '*N*', 15, COMP, 'end', 'bold')
            o += A(x + 30, yi - 18, x + 100, yi - 18, KEY, 2.4, 9)
            o += T(cx + 2, 350, 'μ*N* = μ*A*_{vf}*f*_{y}', 15, KEY, 'middle', 'bold')
    for k in range(3):
        o += A(115 + k * 225 + 95, 190, 115 + k * 225 + 128, 190, MUT, 1.8, 9)
    return svg(W, H, o, '剪力摩擦四步')


def fig7_2():
    W, H = 900, 420
    o = T(450, 24, 'RC-2009-3 深梁：壓拉桿模式（φ = 1）', 16, INK, 'middle', 'bold')
    sc = 2.4
    x0, y0 = 50, 90
    Lb, h = 170, P09['h']
    o += R(x0, y0, Lb * sc, h * sc, STEEL2, INK, 1.4)
    # 支承與載重鈑：20-30-20-30-20-30-20
    segs = [20, 30, 20, 30, 20, 30, 20]
    xs = [0]
    for s_ in segs:
        xs.append(xs[-1] + s_)
    for i in (0, 6):
        o += R(x0 + xs[i] * sc, y0 + h * sc, 20 * sc, 8, INK, INK, 1)
    for i in (2, 4):
        o += R(x0 + xs[i] * sc, y0 - 8, 20 * sc, 8, INK, INK, 1)
        o += A(x0 + (xs[i] + 10) * sc, y0 - 50, x0 + (xs[i] + 10) * sc, y0 - 10, COMP, 2.6, 10)
        o += T(x0 + (xs[i] + 10) * sc + 8, y0 - 30, '*P*/2', 15, COMP, 'start', 'bold')
    ytop = y0 + 10 * sc
    ybot = y0 + (h - 10) * sc
    nl = (x0 + 10 * sc, ybot); nr = (x0 + 160 * sc, ybot)
    tl = (x0 + 60 * sc, ytop); tr = (x0 + 110 * sc, ytop)
    o += L(*nl, *nr, TEN, 4)
    o += L(*nl, *tl, COMP, 6, op=0.6) + L(*nr, *tr, COMP, 6, op=0.6)
    o += L(*tl, *tr, COMP, 5, op=0.6)
    for p_ in (nl, nr, tl, tr):
        o += C(p_[0], p_[1], 6, '#fff', INK, 1.6)
    o += T((nl[0] + tl[0]) / 2 - 14, (nl[1] + tl[1]) / 2, '−0.707*P*', 15, COMP, 'end', 'bold')
    o += T((nl[0] + nr[0]) / 2, ybot + 24, '+0.5*P*（6-D19）', 15, TEN, 'middle', 'bold')
    o += T((tl[0] + tr[0]) / 2, ytop + 22, '−0.5*P*', 15, COMP, 'middle', 'bold')
    o += vdim(x0 + Lb * sc + 14, ytop, ybot, f"*z* = {P09['z']:.0f}", INK, 1, 15)
    o += T(x0 + Lb * sc / 2, y0 + h * sc + 44, f"*a* = {P09['a']:.0f} cm，θ = {P09['theta']:.0f}°，*w*_{{s}} = {P09['ws']:.2f} cm", 15, INK, 'middle')
    # 右：上限長條圖
    bx, by, bw = 560, 80, 230
    k = bw / 180
    items = [('瓶形壓桿 β_{s}=0.75', P09['P_strut'], COMP), ('CCT 節點 β_{n}=0.8', P09['P_cct'], WARN), ('拉力桿降伏', P09['P_tie'], TEN), ('CCC 節點／水平壓桿', P09['P_ccc'], MUT)]
    o += T(bx, by - 10, '各元件的 *P* 上限（tf）', 15, INK, 'start', 'bold')
    for i, (lab, v, col) in enumerate(items):
        y = by + 14 + i * 70
        o += T(bx, y + 4, lab, 14, col, 'start', 'bold')
        o += R(bx, y + 14, v / 1000 * k, 26, col, None, 0, 0, op=0.8 if i == 0 else 0.45)
        o += T(bx + v / 1000 * k + 6, y + 33, f'{v/1000:.1f}', 15, col, 'start', 'bold')
    o += T(bx, by + 310, f"→ *P*_{{max}} = {P09['Pmax']/1000:.1f} tf（壓桿控制，脆性）", 15, COMP, 'start', 'bold')
    return svg(W, H, o, 'STM 深梁')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
