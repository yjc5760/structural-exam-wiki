# -*- coding: utf-8 -*-
"""第 3 章：拉力接合端（精簡）——SS-2024-2 開槽圓管、插銷接合。"""
from plot import *  # noqa
from calcs import ss2024_2, ss2022_2
import math

D = ss2024_2()
PN = ss2022_2()


def fig3_1():
    W, H = 900, 430
    o = T(215, 28, '(a) 以板為界的半圓管：形心離板多遠', 16, INK, 'middle', 'bold')
    cx, cy, RR = 215, 220, 130
    # 圓管
    o += C(cx, cy, RR, 'none', STEEL, 14)
    # 上半圓強調（一支板負責的半圓管，以水平板為界）
    pts = [(cx + RR * math.cos(math.pi * i / 80), cy - RR * math.sin(math.pi * i / 80)) for i in range(81)]
    o += P(pts, AC, 14, op=0.55)
    # 十字板
    o += R(cx - RR - 26, cy - 6, 2 * RR + 52, 12, STEEL3, INK, 1.2)
    o += R(cx - 6, cy - RR - 26, 12, 2 * RR + 52, STEEL3, INK, 1.2)
    xb = D['xbar'] / D['D'] * 2 * RR
    o += C(cx, cy - xb, 6, KEY, '#fff', 1.6)
    o += L(cx + 20, cy - 2, cx + 20, cy - xb, KEY, 1.6) + head(cx + 20, cy - xb, -math.pi / 2, KEY, 8)
    o += T(cx + 28, cy - xb / 2 + 5, f'*x̄* = *D*/π = {D["xbar"]:.2f} cm', 15, KEY, 'start', 'bold')
    o += T(cx, cy + RR + 50, f'*D* = {D["D"]} cm，管厚 {D["t"]:.0f} cm', 15, INK, 'middle')
    o += T(cx - RR + 10, cy - RR + 6, '半圓管', 15, AC, 'end', 'bold')
    # (b) U 曲線
    o += T(655, 28, '(b) *U* = 1 − *x̄*/*L*：銲道越長越好', 16, INK, 'middle', 'bold')
    pl = Plot(470, 70, 380, 270, 0.5, 1.6, 0, 1.0)
    o += pl.axes([0.5, 0.8, 1.0, 1.3, 1.6], [0, 0.25, 0.5, 0.75, 1.0], '*L*/*D*', '*U*', size=14)
    r = D['xbar'] / D['D']
    o += pl.curve(lambda x: 1 - r / x, 0.5, 1.3, AC, 3)
    o += pl.curve(lambda x: 1 - r / x, 1.3, 1.6, AC, 1.6, dash='5 4')
    o += pl.hline(1.0, 1.3, 1.6, TEN, 3, None)
    o += T(pl.X(1.45), pl.Y(1.0) - 10, '*L* ≥ 1.3*D*：*U* = 1', 14, TEN, 'middle', 'bold')
    o += pl.dot(1.0, D['U'], COMP, 6)
    o += T(pl.X(1.0) + 10, pl.Y(D['U']) + 24, f'SS-2024-2：*L* = *D* → *U* = {D["U"]:.3f}', 15, COMP, 'start', 'bold')
    o += T(655, 408, '形心是「沒出力那一半」的代表點；路越短，越多人沒出力', 14, MUT, 'middle')
    return svg(W, H, o, '開槽圓管的剪力遲滯')


def fig3_2():
    W, H = 900, 300
    pl = Plot(240, 50, 520, 180, 0, 320, 0, 3)
    o = T(450, 26, 'SS-2024-2 圓管端部：三站取最小（LRFD，tf）', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 50, 100, 150, 200, 250, 300], [], 'tf', '', size=14)
    items = [('全斷面降伏 GSY', D['GSY']), ('淨斷面斷裂 NSF', D['NSF']), ('管壁沿銲道剪撕', D['tear'])]
    for i, (nm, v) in enumerate(items):
        yc = pl.Y(2.5 - i)
        c = COMP if v == D['phiTn'] else STEEL
        o += R(pl.X(0), yc - 18, pl.X(v) - pl.X(0), 36, COMP2 if c == COMP else STEEL2, c, 1.8, 3)
        o += T(pl.X(0) - 10, yc + 5, nm, 15, INK, 'end', 'bold')
        o += T(pl.X(v) + 8, yc + 5, f'{v:.1f}', 15, c, 'start', 'bold')
    o += T(450, 286, f'*A*_{{n}} 扣 4 道槽 = {D["An"]:.1f}；*A*_{{e}} = *UA*_{{n}} = {D["Ae"]:.1f} cm² → NSF 控制', 15, MUT, 'middle')
    return svg(W, H, o, 'SS-2024-2 三個極限狀態')


def fig3_3():
    W, H = 900, 380
    s = 0.9
    o = T(300, 28, '插銷接合板（SS-2022-2 尺寸，mm）', 16, INK, 'middle', 'bold')
    px, py = 120, 70
    bw, bl = PN['b'] * s, 300 * s
    o += R(px, py, bl, bw, STEEL2, INK, 1.6)
    cx = px + (PN['a'] + PN['dp'] / 2) * s
    cy = py + (PN['a'] + PN['dp'] / 2) * s
    r = PN['dp'] / 2 * s
    o += C(cx, cy, r, '#fff', INK, 1.6)
    o += A(px + bl + 10, py + bw / 2, px + bl + 70, py + bw / 2, TEN, 3, 11) + T(px + bl + 76, py + bw / 2 + 5, '*P*', 16, TEN, 'start', 'bold')
    # 受拉有效寬 be（孔兩側）
    be = PN['be'] * s
    o += R(cx - 4, cy - r - be, 8, be, TEN, None, 0) + R(cx - 4, cy + r, 8, be, TEN, None, 0)
    o += T(cx + 10, cy - r - be / 2 + 5, f'*b*_{{e}} = {PN["be"]:.0f}', 15, TEN, 'start', 'bold')
    # 剪出面（往板端，左側）
    o += L(px, cy - r * 0.7, cx, cy - r * 0.7, COMP, 2.6, '6 4') + L(px, cy + r * 0.7, cx, cy + r * 0.7, COMP, 2.6, '6 4')
    o += T(px + 4, cy - r * 0.7 - 8, '剪出面', 15, COMP, 'start', 'bold')
    o += dim(px, py - 14, cx - r, py - 14, f'*a* = {PN["a"]:.0f}', INK, 0, 14, side=-1)
    o += dim(cx - r, py - 14, cx + r, py - 14, f'*d* = {PN["dp"]:.0f}', INK, 0, 14, side=-1)
    # 右側清單
    o += R(560, 70, 320, 240, '#fff', KEY, 1.6, 10)
    o += T(720, 98, '四站（ASD，kN）', 16, KEY, 'middle', 'bold')
    rows = [('全斷面降伏', PN['Pa1']), ('有效寬斷裂 *F*_{u}(2*tb*_{e})', PN['Pa2']),
            ('剪出 0.6*F*_{u}*A*_{sf}', PN['Pa3']), ('插銷承壓 1.8*F*_{y}*A*_{pb}', PN['Pa4'])]
    for i, (nm, v) in enumerate(rows):
        c = COMP if v == min(x for _, x in rows) else INK
        o += T(580, 136 + i * 40, nm, 15, c, 'start', 'bold' if c == COMP else None)
        o += T(860, 136 + i * 40, f'{v:.0f}', 15, c, 'end', 'bold')
    o += T(720, 296, f'服務載重 *P* = {PN["P"]:.0f} kN', 15, MUT, 'middle')
    o += T(450, 362, '同一條換手鏈：孔兩側拉斷、孔前方剪出、孔壁壓壞——只是孔很大、螺栓換成插銷', 15, MUT, 'middle')
    return svg(W, H, o, '插銷接合的四站')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
