# -*- coding: utf-8 -*-
"""第 3 章：淨斷面 An（扣孔、錯列 s²/4g）。"""
from plot import *  # noqa
from calcs import stagger, tension_example
import math

S = stagger()
D = tension_example()


def fig3_1():
    W, H = 900, 360
    o = T(225, 28, '(a) 孔的剖面（M20，放大繪製）', 16, INK, 'middle', 'bold')
    sc = 60  # px per cm
    cx, y0, t = 225, 120, 1.0 * sc
    db, dh, dd = 2.0, 2.15, 2.3
    # 板
    o += R(cx - 3.3 * sc, y0, 6.6 * sc, t, STEEL3, INK, 1.4)
    # 損傷區 + 孔
    o += R(cx - dd / 2 * sc, y0, dd * sc, t, WARNM, None, 0)
    o += R(cx - dh / 2 * sc, y0 - 1, dh * sc, t + 2, '#fff', None, 0)
    o += L(cx - dh / 2 * sc, y0, cx - dh / 2 * sc, y0 + t, INK, 1.4) + L(cx + dh / 2 * sc, y0, cx + dh / 2 * sc, y0 + t, INK, 1.4)
    # 螺栓桿
    o += R(cx - db / 2 * sc, y0 - 34, db * sc, t + 68, STEEL, INK, 1.2, 3)
    o += dim(cx - db / 2 * sc, y0 + t + 52, cx + db / 2 * sc, y0 + t + 52, '螺栓 *d*_{b} = 2.0', INK, size=14)
    o += dim(cx - dh / 2 * sc, y0 - 50, cx + dh / 2 * sc, y0 - 50, '', AC)
    o += T(cx, y0 - 60, '孔徑 ≈ *d*_{b} + 0.15', 14, AC, 'middle', 'bold')
    o += dim(cx - dd / 2 * sc, y0 + t + 100, cx + dd / 2 * sc, y0 + t + 100, '扣除寬 *d* ≈ *d*_{b} + 0.3 = 2.3 cm', COMP, size=15, weight='bold')
    o += A(cx + 1.6 * sc, y0 + t + 30, cx + 1.12 * sc, y0 + t / 2 + 6, WARN, 1.8, 9)
    o += T(cx + 1.65 * sc, y0 + t + 44, '孔緣受損 ≈ 0.075', 14, WARN, 'start', 'bold')
    o += L(450, 20, 450, 340, GRID, 1.5)
    # (b) 淨斷面
    o += T(675, 28, '(b) 穿過孔的斷面：把孔「挖掉」', 16, INK, 'middle', 'bold')
    x0, yb = 500, 150
    wpx = 340
    o += R(x0, yb, wpx, 40, TEN2, TEN, 1.6)
    hx = x0 + wpx * 0.55
    o += R(hx - 2.3 / 10 * wpx / 2, yb, 2.3 / 10 * wpx, 40, '#fff', COMP, 1.6, dash='5 3')
    o += T(hx, yb + 26, '扣', 15, COMP, 'middle', 'bold')
    o += dim(x0, yb - 18, x0 + wpx, yb - 18, '肢寬 10 cm', INK, size=14, side=-1)
    o += T(x0 + wpx + 8, yb + 26, '*t* = 1.0', 14, INK, 'start')
    o += T(675, 236, '*A*_{n} = *A*_{g} − *n* · *d* · *t*', 17, KEY, 'middle', 'bold')
    o += T(675, 266, f'L100×100×10：19.0 − 1 × 2.3 × 1.0 = {D["An"]:.1f} cm²', 15, INK, 'middle')
    o += T(675, 300, '只扣「同一個斷面上」的孔', 14, MUT, 'middle')
    return svg(W, H, o, '孔的扣除寬')


def _plate(ox, oy, sc, s, highlight):
    """板寬 18、規線 3/9/15；第 1、3 線在 x=0，第 2 線在 x=s。"""
    bg, g, d = S['bg'], S['g'], S['d']
    o = R(ox - 2 * sc, oy, (s + 6) * sc, bg * sc, STEEL2, INK, 1.4)
    pts = {1: (0, 3), 2: (s, 9), 3: (0, 15)}
    for k, (x, y) in pts.items():
        o += C(ox + x * sc, oy + y * sc, d / 2 * sc, '#fff', INK, 1.5)
    P1, P2, P3 = [(ox + x * sc, oy + y * sc) for x, y in pts.values()]
    top, bot = (ox, oy), (ox, oy + bg * sc)
    if highlight == 'straight':
        o += P([top, P1, P3, bot], COMP, 3.2)
    else:
        o += P([top, P1, P2, P3, bot], AC, 3.2)
    return o, (P1, P2, P3)


def fig3_2():
    W, H = 900, 440
    sc = 13
    o = ''
    for i, (hl, title, c) in enumerate((('straight', '① 直線路徑：穿 2 孔', COMP), ('zig', '② 鋸齒路徑：穿 3 孔、2 段斜線', AC))):
        ox, oy = 90 + i * 300, 92
        o += T(ox + 40, 34, title, 16, c, 'middle', 'bold')
        p, (P1, P2, P3) = _plate(ox, oy, sc, S['s'], hl)
        o += p
        o += A(ox + (S['s'] + 4.4) * sc, oy + 9 * sc, ox + (S['s'] + 8) * sc, oy + 9 * sc, TEN, 2.6, 11)
        if i == 1:
            o += dim(P1[0], oy - 14, P2[0], oy - 14, '*s* = 7', INK, size=14, side=-1)
            o += dim(ox + (S['s'] + 4.2) * sc, P1[1], ox + (S['s'] + 4.2) * sc, P2[1], '*g* = 6', INK, size=14, side=-1)
    o += T(170, 352, f'*A*_{{n}} = (18 − 2 × 2.3) *t* = {S["straight"]:.1f} *t*', 15, COMP, 'middle', 'bold')
    o += T(470, 352, f'(18 − 3 × 2.3 + 2 × *s*^{{2}}/4*g*) *t*', 15, AC, 'middle', 'bold')
    o += T(470, 376, f'= (18 − 6.9 + {2 * S["credit"]:.2f}) *t* = {S["zig"]:.2f} *t*', 15, AC, 'middle', 'bold')
    o += R(640, 120, 250, 150, KEY2, KEY, 1.4, 8)
    o += T(765, 146, '取所有路徑中最小者', 15, KEY, 'middle', 'bold')
    o += T(765, 172, '鋸齒多扣一孔（−2.3）', 14, INK, 'middle')
    o += T(765, 194, f'但兩段斜線補回 +{2 * S["credit"]:.2f}', 14, INK, 'middle')
    o += T(765, 216, f'補的比扣的多 → ① 控制', 14, KEY, 'middle', 'bold')
    o += T(765, 248, '單位 cm，依比例繪製', 14, MUT, 'middle')
    o += T(450, 424, '受力方向 →（綠箭頭）；斜線的「長度 *s*」沿受力方向量，「規距 *g*」垂直受力方向量', 14, MUT, 'middle')
    return svg(W, H, o, '錯列螺栓的兩條路徑')


def fig3_3():
    W, H = 900, 380
    o = T(225, 28, '(a) 斜線段的幾何', 16, INK, 'middle', 'bold')
    ox, oy, sc = 90, 80, 30
    g, s = 6, 7
    A_, B_ = (ox, oy), (ox + s * sc, oy + g * sc)
    o += C(*A_, 2.3 / 2 * sc, '#fff', INK, 1.5) + C(*B_, 2.3 / 2 * sc, '#fff', INK, 1.5)
    o += L(A_[0], A_[1], A_[0], B_[1], MUT, 1.5, '6 4')
    o += L(A_[0], B_[1], B_[0], B_[1], MUT, 1.5, '6 4')
    o += L(*A_, *B_, AC, 3.4)
    o += T(A_[0] - 10, (A_[1] + B_[1]) / 2, '*g*', 17, INK, 'end', 'bold')
    o += T((A_[0] + B_[0]) / 2, B_[1] + 26, '*s*（沿受力方向）', 15, INK, 'middle', 'bold')
    o += T((A_[0] + B_[0]) / 2 + 20, (A_[1] + B_[1]) / 2 - 12, '斜線', 15, AC, 'start', 'bold')
    o += A(ox + s * sc + 40, oy + 90, ox + s * sc + 100, oy + 90, TEN, 2.6, 11)
    o += T(225, 320, '直線只走 *g*；斜線比較長，而且斜線上', 15, INK, 'middle')
    o += T(225, 344, '同時有拉應力和剪應力 → 比較不容易斷', 15, INK, 'middle')
    o += L(450, 20, 450, 360, GRID, 1.5)
    o += T(675, 28, '(b) Cochrane 的補償項：只跟 *s*、*g* 有關', 16, INK, 'middle', 'bold')
    o += T(675, 78, '每一段斜線，淨寬補回', 15, INK, 'middle')
    o += T(675, 118, '*s*^{2} / 4*g*', 26, KEY, 'middle', 'bold')
    rows = [('*s* 變大（斜得平緩）', '補回變多', '→ 不危險'),
            ('*g* 變大（排得開）', '補回變少', '→ 近直線'),
            ('*s* → 0（並排）', '補回 0', '→ 多扣一孔')]
    for i, (a, b, c) in enumerate(rows):
        y = 170 + i * 52
        o += R(482, y - 22, 386, 42, '#fff', STEEL, 1.1, 7)
        o += T(492, y + 4, a, 14.5, INK, 'start', 'bold') + T(672, y + 4, b, 14.5, AC, 'start', 'bold') + T(760, y + 4, c, 14, MUT, 'start')
    o += T(675, 344, '記法：「斜線多走的路（≈ *s*^{2}/2*g*）打對折」', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 's²/4g 的意義')


def fig3_4():
    W, H = 900, 400
    pl = Plot(100, 50, 580, 280, 3, 11, 11, 18)
    o = pl.axes([3, 4, 5, 6, 7, 8, 9, 10, 11], [11, 12, 13, 14, 15, 16, 17, 18], '*s*（cm）', '淨寬 × *t*（cm）')
    sc_ = S['s_crit']
    o += R(pl.X(3), pl.y0, pl.X(sc_) - pl.X(3), pl.h, '#e3f2fd', None, 0, op=0.7)
    o += T((pl.X(3) + pl.X(sc_)) / 2, pl.y0 + 24, '鋸齒 ② 控制', 15, AC, 'middle', 'bold')
    o += T((pl.X(sc_) + pl.X(11)) / 2, pl.y0 + 24, '直線 ① 控制', 15, COMP, 'middle', 'bold')
    o += pl.hline(S['straight'], 3, 11, COMP, 3.2, None)
    o += T(pl.X(11) + 8, pl.Y(S['straight']) + 5, '① 直線 13.4', 15, COMP, 'start', 'bold')
    o += pl.curve(lambda s: stagger(s)['zig'], 3, 9.0, AC, 3.2)
    o += T(pl.X(10.2), pl.Y(stagger(10.2)['zig']) - 10, '② 鋸齒', 15, AC, 'end', 'bold')
    o += pl.dot(sc_, S['straight'], KEY, 6)
    o += pl.vline(sc_, 11, S['straight'], KEY, 1.3, '4 4')
    o += T(pl.X(sc_), pl.Y(11) + 40, f'{sc_:.2f}', 15, KEY, 'middle', 'bold')
    o += pl.dot(7, S['zig'], AC, 5) + T(pl.X(7) - 8, pl.Y(S['zig']) - 10, f'本例 *s*=7：{S["zig"]:.2f}', 14, AC, 'end')
    o += R(700, 60, 190, 120, KEY2, KEY, 1.4, 8)
    o += T(795, 84, '交點：', 15, KEY, 'middle', 'bold')
    o += T(795, 110, '2·*s*^{2}/4*g* = *d*', 15, KEY, 'middle', 'bold')
    o += T(795, 136, '⇒ *s* = √(2*gd*)', 15, KEY, 'middle', 'bold')
    o += T(795, 162, f'= √(2×6×2.3) = {sc_:.2f}', 14, INK, 'middle')
    return svg(W, H, o, '鋸齒與直線的交點')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
