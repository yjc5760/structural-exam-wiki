# -*- coding: utf-8 -*-
"""第 6 章：無側移結構。節點自由體（ΣM=0）、桿端剪力＝簡支剪力＋端彎矩力偶、SA-2019-3 等量沉陷、SA-2021-1 彈簧與內鉸。"""
from sa_draw import *  # noqa
import calcs

D6 = calcs.ch6()


def fig6_1():
    W, H = 900, 420
    o = T(W / 2, 34, '切下節點 B：桿件給節點的彎矩，方向和「桿端彎矩」相反', 17, INK, 'middle', 'bold')
    cx, cy = 450, 210
    o += L(cx - 230, cy, cx - 40, cy, INK, 6) + L(cx + 40, cy, cx + 230, cy, INK, 6)
    o += L(cx, cy + 40, cx, cy + 170, INK, 6)
    o += C(cx, cy, 26, '#fff', INK, 2.4)
    o += T(cx, cy + 6, 'B', 17, INK, 'middle', 'bold')
    o += moment(cx - 70, cy, 28, True) + T(cx - 70, cy - 44, '*M*_{BA}', 16, MOM, 'middle', 'bold')
    o += moment(cx + 70, cy, 28, True) + T(cx + 70, cy - 44, '*M*_{BC}', 16, MOM, 'middle', 'bold')
    o += moment(cx, cy, 52, False, c=PUR, start=200, span=110)
    o += T(cx + 2, cy - 62, '節點受 逆時針', 15, PUR, 'middle', 'bold')
    o += T(cx - 150, cy + 34, '桿 BA', 15, MUT, 'middle') + T(cx + 150, cy + 34, '桿 BC', 15, MUT, 'middle')
    o += R(600, 280, 280, 120, KEY2, PUR, 1.6, 9)
    o += T(740, 312, '節點平衡', 16, PUR, 'middle', 'bold')
    o += T(740, 346, 'Σ*M*_{桿端} ＝ *M*_{外}', 17, INK, 'middle', 'bold')
    o += T(740, 378, '（沒有外加彎矩就 ＝ 0）', 15, MUT, 'middle')
    o += T(150, 300, '每個 θ', 16, TEN, 'middle', 'bold')
    o += T(150, 328, '配一條 Σ*M* ＝ 0', 16, TEN, 'middle', 'bold')
    return svg(W, H, o, '節點彎矩平衡')


def fig6_2():
    W, H = 900, 470
    o = T(W / 2, 34, '桿端剪力 ＝ 簡支剪力 *V*_{0} ＋ 端彎矩造成的一對力', 17, INK, 'middle', 'bold')
    x0, x1, y = 170, 730, 190
    o += L(x0, y, x1, y, INK, 6)
    o += udl(x0 + 6, x1 - 6, y - 8, 22, 12, LOAD, '*w*')
    o += moment(x0, y, 30, True) + moment(x1, y, 30, True)
    o += T(x0 - 40, y - 34, '*M*_{AB}', 16, MOM, 'end', 'bold') + T(x1 + 40, y - 34, '*M*_{BA}', 16, MOM, 'start', 'bold')
    o += A(x0, y + 120, x0, y + 12, TEN, 2.4, 11) + A(x1, y + 120, x1, y + 12, TEN, 2.4, 11)
    o += T(x0 - 10, y + 100, '*V*_{A}', 17, TEN, 'end', 'bold') + T(x1 + 10, y + 100, '*V*_{B}', 17, TEN, 'start', 'bold')
    o += T(x0 - 14, y + 8, 'A', 17, INK, 'end', 'bold') + T(x1 + 14, y + 8, 'B', 17, INK, 'start', 'bold')
    o += R(70, 340, 760, 112, '#fff', STEEL, 1.2, 8)
    o += T(90, 372, '對 B 取力矩：*V*_{A}·*L* ＝ *wL*^{2}/2 − (*M*_{AB} + *M*_{BA})', 16, INK, 'start')
    o += T(90, 404, '*V*_{A} ＝ *V*_{0} − (*M*_{AB}+*M*_{BA})/*L*，　*V*_{B} ＝ *V*_{0} + (*M*_{AB}+*M*_{BA})/*L*', 17, PUR, 'start', 'bold')
    o += T(90, 436, '端彎矩合起來是順時針 → 需要一對逆時針的力：左端往下、右端往上', 16, TEN, 'start', 'bold')
    return svg(W, H, o, '桿端剪力')


def fig6_3():
    W, H = 900, 400
    o = T(W / 2, 34, 'SA-2019-3：三跨連續梁（各跨 *L*）受 *w*，B、C 等量沉陷 Δ', 17, INK, 'middle', 'bold')
    x0, Lp, y = 90, 240, 160
    xs = [x0 + Lp * i for i in range(4)]
    o += L(xs[0], y, xs[3], y, STEEL, 1.4, '6 5')
    o += udl(xs[0] + 4, xs[3] - 4, y - 8, 20, 21, LOAD, '*w*')
    dpx = 40
    pts = []
    for i in range(241):
        x = xs[0] + 3 * Lp * i / 240
        s = (x - xs[0]) / Lp
        if s <= 1:
            v = dpx * (3 * s * s - 2 * s ** 3) * 0 + dpx * s  # 簡化：A 到 B 線性下沉＋彎曲示意
            v = dpx * (1.5 * s - 0.5 * s ** 3)
        elif s <= 2:
            v = dpx
        else:
            t = 3 - s
            v = dpx * (1.5 * t - 0.5 * t ** 3)
        pts.append((x, y + v))
    o += P(pts, DEF, 3.6)
    o += pin(xs[0], y + 2) + roller(xs[3], y + 2)
    for i in (1, 2):
        o += roller(xs[i], y + dpx + 2)
        o += A(xs[i] + 22, y, xs[i] + 22, y + dpx, PUR, 1.6, 8, both=True)
        o += T(xs[i] + 30, y + dpx / 2 + 6, 'Δ', 16, PUR, 'start', 'bold')
    for i, nm in enumerate('ABCD'):
        o += T(xs[i], y - 46 if i in (0, 3) else y - 46, nm, 17, INK, 'middle', 'bold')
    o += R(60, 270, 780, 112, '#fff', STEEL, 1.2, 8)
    o += T(80, 300, '對稱 → θ_{C} ＝ −θ_{B}、BC 兩端一起沉 → ψ_{BC} ＝ 0；A 鉸 → AB 用修正式，ψ_{AB} ＝ Δ/*L*', 16, INK, 'start')
    o += T(80, 332, '節點 B：5*EI*θ_{B}/*L* − 3*EI*Δ/*L*^{2} + *wL*^{2}/24 ＝ 0 → *M*_{BA} ＝ *wL*^{2}/10 − 6*EI*Δ/5*L*^{2}', 16, INK, 'start')
    o += T(80, 364, '*R*_{A} ＝ *wL*/2 − *M*_{BA}/*L* 增加 6*EI*Δ/5*L*^{3} ＝ 0.1*wL*　⇒　Δ ＝ *wL*^{4}/12*EI*', 17, PUR, 'start', 'bold')
    return svg(W, H, o, '等量沉陷的連續梁')


def fig6_4():
    W, H = 900, 520
    o = T(W / 2, 34, 'SA-2021-1：b 點彈簧 *k*＝15000、c 內鉸、d 固定（*EI*＝10000）', 17, INK, 'middle', 'bold')
    sc = 66
    x0, y = 110, 150
    xa, xb, xc, xd = x0, x0 + 4 * sc, x0 + 8 * sc, x0 + 10 * sc
    o += L(xa, y, xd, y, INK, 5)
    o += roller(xa, y + 2)
    o += wall(xd, y, 56, 'right')
    o += hinge(xc, y)
    # 彈簧
    pts = [(xb, y + 4), (xb, y + 14)]
    for i in range(6):
        pts.append((xb + (10 if i % 2 == 0 else -10), y + 18 + i * 9))
    pts += [(xb, y + 72), (xb, y + 82)]
    o += P(pts, INK, 1.8)
    o += hatch_ground(xb - 20, y + 82, 40)
    for xp in ((xa + xb) / 2, xb):
        o += A(xp, y - 64, xp, y - 6, LOAD, 2.2, 10)
        o += T(xp + 8, y - 48, '36', 15, LOAD, 'start', 'bold')
    for x, nm, dx, dy in ((xa, 'a', -26, 6), (xb, 'b', 0, -72), (xc, 'c', 0, 36), (xd, 'd', -22, 40)):
        o += T(x + dx, y + dy, nm, 17, INK, 'middle', 'bold')
    o += dim(xa, y + 112, xb, y + 112, '4', MUT, 0, 15) + dim(xb, y + 112, xc, y + 112, '4', MUT, 0, 15)
    o += dim(xc, y + 112, xd, y + 112, '2', MUT, 0, 15)
    o += R(40, 300, 820, 204, '#fff', STEEL, 1.2, 8)
    lines = [
        ('● 未知數：θ_{b}、Δ_{b}（彈簧壓縮）、Δ_{c}（內鉸位移）→ 三條方程', INK, False),
        ('● ab、bc 都以外端鉸為遠端用 3*EI*/*L*；cd 懸臂當 c 的彈簧 *k*_{c} ＝ 3*EI*/2^{3} ＝ 3750', INK, False),
        ('● 節點 b 力平衡：*k*Δ_{b} ＝ 36 + 18 + *M*_{ba}/4 − *M*_{bc}/4 ＝ 54 + *M*_{ba}/2（兩邊同號相加，不抵銷）', INK, False),
        ('● 解：Δ_{b} ＝ 3.80 mm（彈簧力 57 kN）、θ_{b} ＝ −0.00185 rad（逆時針）、*M*_{ba} ＝ +6、*M*_{bc} ＝ −6', PUR, True),
        ('● 彈簧 ＝ 一個「未知的沉陷」＋ 一條力平衡方程', TEN, True),
    ]
    for i, (s, c, b) in enumerate(lines):
        o += T(58, 332 + i * 36, s, 15.5, c, 'start', 'bold' if b else None)
    return svg(W, H, o, '彈簧支承與內鉸')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
