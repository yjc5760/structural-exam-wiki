# -*- coding: utf-8 -*-
"""第 2 章：螺栓——剪斷、承壓、剪出；範例 A（SS-2012-4）。"""
from plot import *  # noqa
from calcs import bolt_A325, bearing_general, ss2012_4
import math

B = bolt_A325()
G = bearing_general()
D = ss2012_4()
D23 = ss2012_4(dh_net=23)


def fig2_1():
    W, H = 900, 400
    o = T(220, 28, '(a) 純剪的莫爾圓', 16, INK, 'middle', 'bold')
    cx, cy, r = 220, 210, 110
    o += A(cx - 175, cy, cx + 180, cy, INK, 1.6, 9) + T(cx + 184, cy + 5, 'σ', 17, INK, 'start', 'italic')
    o += A(cx, cy + 122, cx, cy - 160, INK, 1.6, 9) + T(cx + 8, cy - 150, 'τ', 17, INK, 'start', 'italic')
    o += C(cx, cy, r, WARN2, WARN, 2.6)
    o += C(cx + r, cy, 6, KEY, '#fff', 1.5) + C(cx - r, cy, 6, KEY, '#fff', 1.5)
    o += T(cx + r + 6, cy + 26, 'σ_{1} = +τ', 15, KEY, 'start', 'bold')
    o += T(cx - r - 6, cy + 26, 'σ_{2} = −τ', 15, KEY, 'end', 'bold')
    o += C(cx, cy - r, 5, WARN, '#fff', 1.5) + T(cx + 10, cy - r - 8, '純剪 (0, τ)', 15, WARN, 'start', 'bold')
    o += R(40, 338, 360, 54, KEY2, KEY, 1.4, 8)
    o += T(220, 360, 'von Mises：σ_{1}² − σ_{1}σ_{2} + σ_{2}² = *F*²', 15, INK, 'middle')
    o += T(220, 384, '→ 3τ² = *F*² → τ = *F*/√3 = 0.577*F*', 15, KEY, 'middle', 'bold')
    # (b) 螺栓剪力強度的分解
    o += T(670, 28, '(b) 螺栓標稱剪力強度從 0.6*F*_{u} 長出來', 16, INK, 'middle', 'bold')
    pl = Plot(520, 70, 340, 250, 0, 3, 0, 6)
    Fu = B['Fu']
    vals = [(0.6 * Fu, '0.6*F*_{u}', '純剪斷裂', WARN), (B['Fnv_X'], '0.5*F*_{u}', 'X：螺紋不在剪力面', TEN), (B['Fnv_N'], '0.4*F*_{u}', 'N：螺紋在剪力面', AC)]
    o += L(pl.x0, pl.Y(0), pl.x0 + pl.w, pl.Y(0), INK, 1.4)
    for i, (v, lab, sub, c) in enumerate(vals):
        x = pl.X(i + 0.5)
        o += R(x - 40, pl.Y(v), 80, pl.Y(0) - pl.Y(v), '#fff', c, 2.2, 3)
        o += T(x, pl.Y(v) - 10, f'{v:.2f}', 16, c, 'middle', 'bold')
        o += T(x, pl.Y(v) + 26, lab, 15, c, 'middle', 'bold')
        o += T(x, pl.Y(0) + 22, sub.split('：')[0], 15, INK, 'middle', 'bold')
    o += T(pl.X(1.0), pl.Y(0.6 * Fu) - 44, f'× {B["k_long"]:.2f}', 15, MUT, 'middle', 'bold') + T(pl.X(1.0), pl.Y(0.6 * Fu) - 26, '長接頭不均', 14, MUT, 'middle')
    o += T(pl.X(2.0), pl.Y(B['Fnv_X']) - 44, f'× {B["k_thread"]:.1f}', 15, MUT, 'middle', 'bold') + T(pl.X(2.0), pl.Y(B['Fnv_X']) - 26, '螺紋根部', 14, MUT, 'middle')
    o += T(670, 360, f'A325：*F*_{{u}} ≈ {Fu:.1f} tf/cm²（120 ksi）', 15, INK, 'middle')
    o += T(670, 384, '單位 tf/cm²；兩個折減係數是試驗取值', 14, MUT, 'middle')
    return svg(W, H, o, '純剪與螺栓剪力強度')


def fig2_2():
    W, H = 900, 400
    o = ''
    # (a) 單剪
    o += T(150, 28, '(a) 單剪 *m* = 1', 16, INK, 'middle', 'bold')
    x0, y0 = 60, 120
    o += R(x0, y0, 180, 30, STEEL3, INK, 1.4) + R(x0 + 60, y0 + 30, 180, 30, STEEL2, INK, 1.4)
    bx = x0 + 120
    o += R(bx - 12, y0 - 18, 24, 96, '#fff', INK, 1.6, 2)
    o += L(bx - 40, y0 + 30, bx + 40, y0 + 30, COMP, 2.6, '6 4')
    o += A(x0 + 10, y0 + 15, x0 - 40, y0 + 15, TEN, 3, 11) + A(x0 + 230, y0 + 45, x0 + 280, y0 + 45, TEN, 3, 11)
    o += T(bx + 46, y0 + 36, '剪力面', 15, COMP, 'start', 'bold')
    # (b) 雙剪
    o += T(450, 28, '(b) 雙剪 *m* = 2', 16, INK, 'middle', 'bold')
    x1, y1 = 360, 100
    o += R(x1, y1, 180, 26, STEEL2, INK, 1.4) + R(x1 - 40, y1 + 26, 180, 30, STEEL3, INK, 1.4) + R(x1, y1 + 56, 180, 26, STEEL2, INK, 1.4)
    bx = x1 + 90
    o += R(bx - 12, y1 - 18, 24, 118, '#fff', INK, 1.6, 2)
    for yy in (y1 + 26, y1 + 56):
        o += L(bx - 40, yy, bx + 40, yy, COMP, 2.6, '6 4')
    o += A(x1 - 30, y1 + 41, x1 - 80, y1 + 41, TEN, 3, 11) + A(x1 + 170, y1 + 13, x1 + 220, y1 + 13, TEN, 3, 11) + A(x1 + 170, y1 + 69, x1 + 220, y1 + 69, TEN, 3, 11)
    o += T(bx + 22, y1 - 6, '兩個剪力面', 15, COMP, 'start', 'bold')
    o += T(450, 250, '同一根螺栓，雙剪的強度是單剪的 2 倍', 15, KEY, 'middle', 'bold')
    o += T(150, 250, '強度 = *F*_{nv} × *A*_{b} × 剪力面數 *m*', 15, KEY, 'middle', 'bold')
    # (c) 剪力面上的螺栓斷面
    o += T(760, 28, '(c) 剪力面切到哪裡', 16, INK, 'middle', 'bold')
    for k, (cx, lab, sub) in enumerate([(700, 'X', '螺桿（全斷面）'), (830, 'N', '螺紋（根部較細）')]):
        cy, r = 130, 44
        o += C(cx, cy, r, TEN2 if k == 0 else '#fff', TEN if k == 0 else MUT, 2)
        if k == 1:
            o += C(cx, cy, r * math.sqrt(0.8), AC2, AC, 2)
            o += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r)}" fill="none" stroke="{MUT}" stroke-width="1.4" stroke-dasharray="4 3"/>'
        o += T(cx, cy + 6, lab, 20, TEN if k == 0 else AC, 'middle', 'bold')
        o += T(cx, cy + 74, sub, 14, INK, 'middle')
    o += T(765, 250, '螺紋根部面積約 0.8 倍 → N 打 8 折', 15, KEY, 'middle', 'bold')
    # 底部說明
    o += R(40, 290, 820, 92, KEY2, KEY, 1.4, 10)
    o += T(450, 320, 'LRFD：φ*R*_{n} = 0.75 × *F*_{nv} × *A*_{b} × *m*', 17, INK, 'middle', 'bold')
    o += T(450, 352, f'A325：*F*_{{nv}} = {B["Fnv_X"]:.2f}（X）、{B["Fnv_N"]:.2f}（N）tf/cm²；SS-2012-4 題給 330 MPa = 0.4 × 120 ksi（N）', 15, INK, 'middle')
    return svg(W, H, o, '螺栓的剪力面')


def fig2_3():
    W, H = 900, 450
    o = T(240, 28, '(a) 螺栓往下推：撕出一條「塞子」', 16, INK, 'middle', 'bold')
    s = 3.0      # px/mm
    px, py = 120, 60
    pw, ph = 240, 330
    o += R(px, py, pw, ph, STEEL2, INK, 1.6)
    db, dh = D['db'], D['dh']
    cx = px + pw / 2
    holes = [(py + ph - D['Le'] * s, '邊緣孔'), (py + ph - (D['Le'] + D['s']) * s, '內部孔')]
    for k, (cy, nm) in enumerate(holes):
        o += C(cx, cy, dh / 2 * s, '#fff', INK, 1.6)
        cb = cy + (dh - db) / 2 * s
        o += C(cx, cb, db / 2 * s, ACM, AC, 1.4)
        o += A(cx, cb - 10, cx, cb + db / 2 * s - 6, AC, 2.4, 9)
        bot = py + ph if k == 0 else holes[0][0] - dh / 2 * s
        top = cy + dh / 2 * s
        o += R(cx - db / 2 * s, top, db * s, bot - top, COMP2, None, 0)
        o += L(cx - db / 2 * s, cy, cx - db / 2 * s, bot, COMP, 2.6, '6 4')
        o += L(cx + db / 2 * s, cy, cx + db / 2 * s, bot, COMP, 2.6, '6 4')
        o += dim(cx + dh / 2 * s + 30, top, cx + dh / 2 * s + 30, bot, '', COMP)
        lc = D['Lc_edge'] if k == 0 else D['Lc_int']
        o += T(cx + dh / 2 * s + 40, (top + bot) / 2 + 5, f'*L*_{{c}} = {lc:.0f} mm', 15, COMP, 'start', 'bold')
        o += T(px - 10, cy + 5, nm, 15, INK, 'end', 'bold')
    o += T(px + pw / 2, py + ph + 26, '自由邊（剪力往這邊推）', 14, MUT, 'middle')
    o += T(240, 438, '兩條剪出線 × 0.6*F*_{u} × *L*_{c}*t* = 1.2*L*_{c}*tF*_{u}', 15, KEY, 'middle', 'bold')
    # (b) 承壓：投影面積 d·t
    o += T(680, 28, '(b) 孔壁被壓扁：投影面積 *d* × *t*', 16, INK, 'middle', 'bold')
    x0, y0, tt, ww = 560, 90, 70, 240
    o += R(x0, y0, ww, tt, STEEL2, INK, 1.6)
    hx = x0 + 120
    o += R(hx - 33, y0 - 30, 66, tt + 60, ACM, AC, 1.6, 3)
    for i in range(7):
        yy = y0 + 6 + i * (tt - 12) / 6
        o += A(hx + 33 + 52, yy, hx + 35, yy, WARN, 1.8, 8)
    o += T(hx + 92, y0 + tt / 2 + 5, '壓應力', 15, WARN, 'start', 'bold')
    o += dim(hx - 33, y0 + tt + 44, hx + 33, y0 + tt + 44, '*d*', INK, 0, 15)
    o += dim(x0 - 16, y0, x0 - 16, y0 + tt, '*t*', INK, 0, 15, side=-1)
    o += R(560, 270, 280, 120, '#fff', KEY, 1.6, 9)
    o += T(700, 298, '孔變形 6 mm 時的承壓', 15, KEY, 'middle', 'bold')
    o += T(700, 324, '≈ 2.4*F*_{u} × *d* × *t*（試驗值）', 15, INK, 'middle')
    o += T(700, 352, '→ 承壓上限 2.4*dtF*_{u}', 15, COMP, 'middle', 'bold')
    o += T(700, 378, '不是推導，是規範取的變形上限', 14, MUT, 'middle')
    return svg(W, H, o, '承壓的兩種機制')


def fig2_4():
    W, H = 900, 420
    pl = Plot(110, 50, 600, 290, 0, 3, 0, 3)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 0.6, 1.2, 1.8, 2.4, 3], '*L*_{c}/*d*', '*R*_{n} / (*d t F*_{u})', size=14)
    o += pl.curve(lambda x: 1.2 * x, 0, 2.5, COMP, 2, dash='6 4', clip=True)
    o += pl.curve(lambda x: min(1.2 * x, 2.4), 0, 3, INK, 3.4)
    o += pl.hline(2.4, 0, 3, AC, 1.8, '6 4')
    o += T(pl.X(2.95), pl.Y(2.4) - 10, '上限 2.4（孔變形）', 15, AC, 'end', 'bold')
    o += T(pl.X(0.4), pl.Y(1.05), '剪出 1.2*L*_{c}/*d*', 15, COMP, 'middle', 'bold')
    xc = G['Lc_cross_over_d']
    o += pl.dot(xc, 2.4, KEY, 6) + pl.vline(xc, 0, 2.4, KEY, 1.4)
    o += T(pl.X(xc) + 8, pl.Y(0.3), '*L*_{c} = 2*d*', 15, KEY, 'start', 'bold')
    e = D['Lc_edge'] / D['db']; i = D['Lc_int'] / D['db']
    o += pl.dot(e, 1.2 * e, WARN, 6) + T(pl.X(e) + 10, pl.Y(1.2 * e) + 22, f'邊緣孔 {e:.2f} → {1.2*e:.2f}', 15, WARN, 'start', 'bold')
    o += pl.dot(i, min(1.2 * i, 2.4), WARN, 6) + T(pl.X(i) - 10, pl.Y(1.2 * i) - 16, f'內部孔 {i:.1f} → {1.2*i:.2f}', 15, WARN, 'end', 'bold')
    o += R(730, 120, 160, 150, KEY2, KEY, 1.4, 8)
    o += T(810, 146, 'SS-2012-4', 15, KEY, 'middle', 'bold')
    o += T(810, 172, '*d* = 20 mm', 15, INK, 'middle')
    o += T(810, 198, '邊緣孔：剪出控制', 14, INK, 'middle')
    o += T(810, 222, '內部孔：仍是剪出', 14, INK, 'middle')
    o += T(810, 246, '（差一點到上限）', 14, MUT, 'middle')
    o += T(450, 400, '剪出線越長，強度越高；長到 *L*_{c} = 2*d* 以後由孔變形上限 2.4 管', 15, MUT, 'middle')
    return svg(W, H, o, '承壓強度與淨距')


def fig2_5():
    W, H = 900, 560
    s = 2.0
    o = ''
    for k in range(2):
        px = 120 + k * 440
        py = 70
        pw, ph = D['w'] * s, D['h'] * s
        title = '(a) 剪力降伏與剪力斷裂' if k == 0 else '(b) 塊狀剪力（題解未檢核）'
        o += T(px + pw / 2 + 40, 30, title, 16, INK, 'middle', 'bold')
        # 柱面
        o += R(px - 30, py - 30, 30, ph + 60, STEEL3, INK, 1.4)
        o += T(px - 15, py + ph + 54, '柱', 15, INK, 'middle', 'bold')
        o += R(px, py, pw, ph, STEEL2, INK, 1.8)
        bx = px + D['x_bolt'] * s
        ys = [py + D['Le'] * s + j * D['s'] * s for j in range(D['n'])]
        if k == 0:
            o += L(bx, py, bx, py + ph, COMP, 3, '7 4')
            o += L(px + 12, py, px + 12, py + ph, TEN, 3, '2 5')
        else:
            top = ys[0]
            o += P([(px + pw, top), (bx, top), (bx, py + ph)], None, fill=COMP2, close=False)
            o += P([(bx, top), (px + pw, top), (px + pw, py + ph), (bx, py + ph)], None, fill=COMP2, close=True)
            o += L(bx, top, bx, py + ph, COMP, 3, '7 4')
            o += L(bx, top, px + pw, top, AC, 3, '7 4')
        for y in ys:
            o += C(bx, y, D['dh'] / 2 * s, '#fff', INK, 1.5)
        o += dim(px, py + ph + 18, bx, py + ph + 18, '40', INK, 0, 14)
        o += dim(bx, py + ph + 18, px + pw, py + ph + 18, '40', INK, 0, 14)
        o += dim(px + pw + 18, py, px + pw + 18, ys[0], '30', INK, 0, 14, side=-1)
        o += dim(px + pw + 18, ys[0], px + pw + 18, ys[1], '60', INK, 0, 14, side=-1)
        o += dim(px + pw + 18, ys[1], px + pw + 18, ys[2], '60', INK, 0, 14, side=-1)
        o += dim(px + pw + 18, ys[2], px + pw + 18, py + ph, '30', INK, 0, 14, side=-1)
        o += A(bx + 50, py + ph / 2 - 30, bx + 50, py + ph / 2 + 30, AC, 2.6, 10)
    # (a) 說明
    o += T(330, 500, f'紅：沿螺栓線剪斷，扣 3 孔 → *A*_{{nv}} = {D["Anv_t"]:.0f}*t*', 15, COMP, 'middle', 'bold')
    o += T(330, 528, f'綠：靠柱面全斷面降伏 → *A*_{{gv}} = {D["Agv_t"]:.0f}*t*', 15, TEN, 'middle', 'bold')
    # (b) 說明
    o += T(740, 500, f'剪力面 *A*_{{gv}} = {D["bs_Agv_t"]:.0f}*t*、*A*_{{nv}} = {D["bs_Anv_t"]:.0f}*t*', 15, COMP, 'middle', 'bold')
    o += T(740, 526, f'拉力面 *A*_{{nt}} = (40 − 11)*t* = {D["bs_Ant_t"]:.0f}*t*', 15, AC, 'middle', 'bold')
    o += T(740, 552, '剪力面扣 2.5 孔、拉力面扣 0.5 孔', 15, INK, 'middle')
    return svg(W, H, o, 'SS-2012-4 剪力板的三種斷面')


def fig2_6():
    W, H = 900, 380
    pl = Plot(170, 60, 560, 230, 0, 11, 0, 5)
    o = T(450, 30, '每個板件極限狀態都和 *t* 成正比 → 直接比「所需板厚」', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 2, 4, 6, 8, 10], [], 'mm', '', size=14)
    tl = D['t_list']
    tmax = D['t_req']
    for i, (nm, v) in enumerate(tl):
        yc = pl.Y(4.4 - i)
        c = COMP if abs(v - tmax) < 1e-9 else STEEL
        o += R(pl.X(0), yc - 17, pl.X(v) - pl.X(0), 34, COMP2 if c == COMP else STEEL2, c, 1.8, 3)
        o += T(pl.X(0) - 10, yc + 5, nm, 15, INK, 'end', 'bold')
        xv = pl.X(max(v, D23['t_rup'])) + 10 if c == COMP else pl.X(v) + 8
        o += T(xv, yc + 5, f'{v:.2f}', 15, c, 'start', 'bold')
    o += pl.vline(D['t_use'], 0, 5, TEN, 2.6, '7 5')
    o += T(pl.X(D['t_use']), pl.y0 - 6, f'採用 *t* = {D["t_use"]:.0f} mm', 15, TEN, 'middle', 'bold')
    o += L(pl.X(D23['t_rup']), pl.Y(4.4 - 3) - 22, pl.X(D23['t_rup']), pl.Y(4.4 - 3) + 22, KEY, 2.4)
    o += T(pl.X(D23['t_rup']) - 4, pl.Y(4.4 - 3) + 40, f'孔徑取 *d* + 3 = 23 mm：{D23["t_rup"]:.2f}', 14, KEY, 'end', 'bold')
    o += T(450, 362, '控制的是剪力斷裂；孔徑用 22 或 23 mm，答案都是 10 mm', 15, MUT, 'middle')
    return svg(W, H, o, 'SS-2012-4 所需板厚')


def fig2_7():
    W, H = 900, 380
    pl = Plot(110, 50, 520, 270, 0, 5, 0, 9)
    o = pl.axes([0, 1, 2, 3, 4, 5], [0, 2, 4, 6.3, 8.2], '*f*_{v}', '*F*_{t}', size=14,
                yfmt=lambda v: {6.3: '6.3', 8.2: '8.2'}.get(v, f(v)))
    a, b, cap = B['int_a'], B['int_b'], B['int_cap']
    o += pl.curve(lambda x: a - b * x, 0, a / b, COMP, 1.8, dash='6 4')
    o += pl.curve(lambda x: min(cap, a - b * x), 0, a / b, INK, 3.4)
    o += pl.curve(lambda x: cap * math.sqrt(max(0, 1 - (x / B['Fnv_X']) ** 2)), 0, B['Fnv_X'], AC, 2.2, dash='3 4', n=200)
    o += L(pl.X(0) + 6, pl.Y(cap) - 4, pl.X(1.25), pl.Y(7.0) - 5, KEY, 1.2) + pl.dot(0, cap, KEY, 6) + T(pl.X(1.3), pl.Y(7.0), f'純拉 0.75*F*_{{u}} = {cap:.1f}', 15, KEY, 'start', 'bold')
    o += pl.dot(B['int_fv_at_zero'], 0, KEY, 6) + T(pl.X(3.7), pl.Y(0.3), f'{B["int_fv_at_zero"]:.2f} ≈ *F*_{{nv}}(X) = {B["Fnv_X"]:.2f}', 15, KEY, 'end', 'bold')
    o += T(pl.X(2.6), pl.Y(5.6), '試驗：近似橢圓', 15, AC, 'start', 'bold')
    o += R(650, 90, 240, 150, KEY2, KEY, 1.4, 8)
    o += T(770, 116, '*F*_{t} = 8.2 − 1.9*f*_{v} ≤ 6.3', 15, INK, 'middle', 'bold')
    o += T(770, 144, '（tf/cm²，A325 承壓型）', 14, MUT, 'middle')
    o += T(770, 172, f'*f*_{{v}} < {B["int_fv_at_cap"]:.1f}：拉力不折減', 14, INK, 'middle')
    o += T(770, 198, '之後直線往下', 14, INK, 'middle')
    o += T(770, 224, '剪得越多，能拉的越少', 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '拉剪互制')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4,
       'fig2_5': fig2_5, 'fig2_6': fig2_6, 'fig2_7': fig2_7}
