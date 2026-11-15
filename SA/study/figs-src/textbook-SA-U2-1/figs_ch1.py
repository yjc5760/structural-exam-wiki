# -*- coding: utf-8 -*-
"""第 1 章：功＝三角形（S2）、材料律與轉折（S3）、三種構件同一個三角形、彎曲小段、剪力比例、SA-2014-4 CD 柱。"""
from sa_draw import *  # noqa
import math
import calcs

C1 = calcs.C1
ENE = PUR          # 能量（面積）用紫色


def fig1_1():
    W, H = 900, 400
    k, Pv, d = C1['k'], C1['P'], C1['delta']
    pl = Plot(110, 50, 420, 270, 0, 0.5, 0, 25)
    o = pl.axes([0, 0.1, 0.2, 0.3, 0.4, 0.5], [0, 5, 10, 15, 20, 25], 'Δ (m)', '力 P (kN)', size=14)
    # 矩形（錯誤）
    o += P([pl.pt(0, 0), pl.pt(0, Pv), pl.pt(d, Pv), pl.pt(d, 0)], WARN, 1.8, fill=WARN2, dash='7 5', close=True, op=0.9)
    # 三角形（正確）
    o += P([pl.pt(0, 0), pl.pt(d, Pv), pl.pt(d, 0)], None, fill=KEY2, close=True)
    o += pl.curve(lambda x: k * x, 0, d, AC, 3)
    o += pl.dot(d, Pv, AC)
    o += T(pl.X(d * 0.66), pl.Y(Pv * 0.30), '½·P·Δ = ' + f(C1['W_slow']), 16, ENE, 'middle', 'bold')
    o += T(pl.X(d * 0.22), pl.Y(Pv * 0.80), '矩形 P·Δ = ' + f(C1['W_rect']), 15, WARN, 'middle', 'bold')
    o += T(pl.X(d) + 10, pl.Y(Pv) - 6, f'({f(d)}, {f(Pv)})', 14, AC, 'start')
    # 右側：彈簧示意＋說明
    x0 = 640
    o += fixed_wall(x0 + 60, 70, 90, INK, top=True)
    zig = [(x0 + 60, 70)]
    for i in range(1, 9):
        zig.append((x0 + 60 + (14 if i % 2 else -14), 70 + i * 12))
    zig.append((x0 + 60, 70 + 9 * 12 + 4))
    o += P(zig, INK, 2)
    o += R(x0 + 35, 182, 50, 30, STEEL2, INK, 1.5, 4)
    o += A(x0 + 60, 214, x0 + 60, 262, WARN, 2.6, 11)
    o += T(x0 + 72, 250, '*P*', 17, WARN, 'start', italic=False)
    o += T(x0 + 100, 135, '*k* = 50 kN/m', 15, INK, 'start')
    o += R(560, 292, 320, 92, KEY2, PUR, 1.4, 10)
    o += T(720, 320, '慢慢加載：力從 0 長到 P', 15, PUR, 'middle', 'bold')
    o += T(720, 346, '平均力 = P/2', 15, PUR, 'middle')
    o += T(720, 371, '功 = 三角形面積 = ½PΔ', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, '功等於三角形面積')


def fig1_2():
    W, H = 900, 330
    o = ''
    titles = ['(a) 一般構件（直線）', '(b) 纜索：不能受壓', '(c) 到強度就走平', ]
    for k in range(3):
        x0 = 30 + k * 296
        pl = Plot(x0 + 30, 70, 220, 170, -1, 1, -1, 1)
        o += T(x0 + 140, 34, titles[k], 16, INK, 'middle', 'bold')
        # 軸（十字）
        o += A(pl.X(-1), pl.Y(0), pl.X(1) + 12, pl.Y(0), INK, 1.4, 8)
        o += A(pl.X(0), pl.Y(-1), pl.X(0), pl.Y(1) - 12, INK, 1.4, 8)
        o += T(pl.X(1) + 8, pl.Y(0) + 22, '變形', 14, MUT, 'end')
        o += T(pl.X(0) + 8, pl.Y(1) - 4, '力', 14, MUT, 'start')
        o += T(pl.X(0.55), pl.Y(-0.12) + 14, '拉', 14, TEN, 'middle')
        o += T(pl.X(-0.55), pl.Y(-0.12) + 14, '壓', 14, COMP, 'middle')
        if k == 0:
            o += pl.curve(lambda x: 0.8 * x, -1, 1, AC, 3)
            o += T(pl.X(0.5) + 8, pl.Y(0.55), '斜率 = 勁度', 14, AC, 'start')
        elif k == 1:
            o += pl.curve(lambda x: 0.8 * x, 0, 1, AC, 3)
            o += pl.curve(lambda x: 0.0, -1, 0, COMP, 4)
            o += T(pl.X(-0.5), pl.Y(0.30), '鬆掉：力 = 0', 14, COMP, 'middle', 'bold')
        else:
            o += pl.curve(lambda x: max(-0.6, min(0.6, 0.8 * x)), -1, 1, AC, 3)
            o += pl.hline(0.6, 0, 1, KEY, 1.3)
            o += T(pl.X(0.62), pl.Y(0.6) - 10, '強度', 14, KEY, 'middle', 'bold')
    o += R(120, 276, 660, 40, KEY2, PUR, 1.4, 8)
    o += T(450, 302, '第 1～6 章只用 (a)；(b)、(c) 的轉折留到第 7 章', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, '三種力與變形的關係')


def _mini_tri(x0, y0, w, h, flab, dlab, c):
    o = A(x0, y0 + h, x0 + w + 14, y0 + h, INK, 1.3, 8) + A(x0, y0 + h, x0, y0 - 10, INK, 1.3, 8)
    o += P([(x0, y0 + h), (x0 + w * 0.8, y0 + 12), (x0 + w * 0.8, y0 + h)], None, fill=KEY2, close=True)
    o += L(x0, y0 + h, x0 + w * 0.8, y0 + 12, c, 2.6)
    o += L(x0 + w * 0.8, y0 + 12, x0 + w * 0.8, y0 + h, MUT, 1, '4 3')
    o += T(x0 - 6, y0 + 18, flab, 15, c, 'end', 'bold')
    o += T(x0 + w * 0.8, y0 + h + 20, dlab, 15, AC, 'middle')
    o += T(x0 + w * 0.52, y0 + h - 12, '½', 15, PUR, 'middle', 'bold')
    return o


def fig1_3():
    W, H = 900, 470
    o = ''
    cols = [
        ('軸力桿', '*N*', 'Δ = *NL*/*EA*', '*U* = *N*^{2}*L*/2*EA*'),
        ('彈簧', '*R*', 'δ = *R*/*k*', '*U* = *R*^{2}/2*k*'),
        ('彎曲小段 *dx*', '*M*', '*d*θ = *M dx*/*EI*', '*dU* = *M*^{2}*dx*/2*EI*'),
    ]
    for k, (name, flab, dlab, res) in enumerate(cols):
        cx = 150 + k * 300
        o += T(cx, 34, name, 17, INK, 'middle', 'bold')
        if k == 0:
            o += R(cx - 90, 82, 160, 26, STEEL2, INK, 1.4, 3)
            o += L(cx + 70, 82, cx + 70, 108, AC, 1.4, '4 3')
            o += R(cx - 90, 82, 180, 26, 'none', AC, 1.4, 3, dash='5 4')
            o += A(cx - 90, 95, cx - 130, 95, TEN, 2.4, 10) + A(cx + 90, 95, cx + 130, 95, TEN, 2.4, 10)
            o += T(cx - 130, 125, '*N*', 16, TEN, 'middle') + T(cx + 130, 125, '*N*', 16, TEN, 'middle')
            o += dim(cx + 70, 140, cx + 90, 140, '', AC) + T(cx + 80, 162, 'Δ', 16, AC, 'middle')
        elif k == 1:
            zig = [(cx - 100, 95)]
            for i in range(1, 9):
                zig.append((cx - 100 + i * 20, 95 + (12 if i % 2 else -12)))
            zig.append((cx + 80, 95))
            o += P(zig, INK, 2)
            o += A(cx - 100, 95, cx - 135, 95, TEN, 2.4, 10) + A(cx + 80, 95, cx + 120, 95, TEN, 2.4, 10)
            o += T(cx - 135, 125, '*R*', 16, TEN, 'middle') + T(cx + 120, 125, '*R*', 16, TEN, 'middle')
            o += T(cx - 10, 140, '勁度 *k*', 15, INK, 'middle')
        else:
            # 小段：兩切面相對轉動
            o += P([(cx - 50, 70), (cx + 50, 70), (cx + 58, 124), (cx - 58, 124)], INK, 1.6, fill=STEEL2, close=True)
            o += moment(cx - 78, 97, 22, cw=True, c=MOM, start=200, span=160)
            o += moment(cx + 78, 97, 22, cw=False, c=MOM, start=-20, span=160)
            o += T(cx - 104, 140, '*M*', 16, MOM, 'middle') + T(cx + 104, 140, '*M*', 16, MOM, 'middle')
            o += T(cx, 150, '*d*θ', 16, AC, 'middle')
        o += _mini_tri(cx - 80, 200, 170, 120, flab, dlab.split(' = ')[0], [TEN, TEN, MOM][k])
        o += T(cx, 372, dlab, 15, AC, 'middle')
        o += R(cx - 125, 390, 250, 40, KEY2, PUR, 1.4, 8)
        o += T(cx, 416, res, 16, PUR, 'middle', 'bold')
    o += T(450, 458, '同一個模子：力^{2} ÷（2 × 勁度）', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '三種構件同一個三角形')


def fig1_4():
    W, H = 900, 330
    cx, cy = 300, 170
    # 原段（虛線）與彎曲後
    o = R(cx - 110, cy - 50, 220, 100, 'none', STEEL, 1.4, 0, dash='6 5')
    a = math.radians(9)
    def face(x, sgn):
        # 以中性軸為中心轉 sgn*a
        dx, dy = -50 * math.sin(sgn * a), 50 * math.cos(sgn * a)
        return (x + dx, cy - dy), (x - dx, cy + dy)
    tl, bl = face(cx - 110, -1)
    tr, br = face(cx + 110, 1)
    o += P([tl, tr, br, bl], INK, 2, fill=STEEL2, close=True)
    o += L(cx - 110, cy, cx + 110, cy, MUT, 1.2, '4 3')
    o += T(cx, cy - 8, '中性軸', 14, MUT, 'middle')
    o += moment(cx - 160, cy, 30, cw=True, c=MOM, start=200, span=160)
    o += moment(cx + 160, cy, 30, cw=False, c=MOM, start=-20, span=160)
    o += T(cx - 196, cy + 6, '*M*', 18, MOM, 'end') + T(cx + 196, cy + 6, '*M*', 18, MOM, 'start')
    o += dim(cx - 110, cy + 92, cx + 110, cy + 92, '*dx*', INK)
    # 每個切面相對原位置轉 dθ/2（小弧標示）
    for xf, top, sgn in ((cx - 110, tl, -1), (cx + 110, tr, 1)):
        a0 = -90
        a1 = -90 + sgn * 9
        o += angle_arc(xf, cy, 38, min(a0, a1), max(a0, a1), AC, 2.2)
        o += T(xf + sgn * 30, cy - 58, '*d*θ/2', 15, AC, 'middle', 'bold')
    o += T(cx, 40, '兩切面相對轉 *d*θ = κ *dx*', 16, AC, 'middle', 'bold')
    o += T(cx, cy + 72, '下緣拉長', 14, TEN, 'middle') + T(cx, cy - 64, '上緣縮短', 14, COMP, 'middle')
    # 右邊三角形
    o += _mini_tri(640, 110, 180, 130, '*M*', '*d*θ', MOM)
    o += R(580, 22, 300, 64, KEY2, PUR, 1.4, 8)
    o += T(730, 48, '*dU* = ½ *M* *d*θ', 16, PUR, 'middle', 'bold')
    o += T(730, 74, '*d*θ = *M dx*/*EI* → *M*^{2}*dx*/2*EI*', 15, PUR, 'middle')
    return svg(W, H, o, '彎曲小段的應變能')


def fig1_5():
    W, H = 900, 360
    pl = Plot(120, 50, 600, 240, 0, 20, 0, 0.25)
    xt = [0, 2, 5, 10, 15, 20]
    o = pl.axes(xt, [0, 0.05, 0.10, 0.15, 0.20, 0.25], '*L*/*h*', '*U*_{V} / *U*_{M}', size=14,
                yfmt=lambda v: f'{v*100:.0f}%')
    fn = lambda x: min(0.25, C1['coef'] / x ** 2) if x > 0 else 0.25
    o += pl.area(fn, lambda x: 0, 1.77, 20, KEY2, 0.7)
    o += pl.curve(fn, 1.77, 20, PUR, 3)
    for Lh, c in ((2, COMP), (5, WARN), (10, TEN)):
        v = C1['ratio_LH'][Lh]
        o += pl.dot(Lh, v, c)
        o += T(pl.X(Lh) + 12, pl.Y(v) - 8, f'{Lh} → {v*100:.1f}%', 15, c, 'start', 'bold')
    o += pl.vline(10, 0, 0.12, TEN, 1.3)
    o += T(pl.X(14.5), pl.Y(0.17), '一般梁 *L*/*h* ≥ 10：< 1%，可忽略', 15, TEN, 'middle', 'bold')
    o += T(pl.X(14.5), pl.Y(0.21), '*U*_{V}/*U*_{M} ≈ 0.78 (*h*/*L*)^{2}', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '剪力能量占彎曲能量比例')


def fig1_6():
    W, H = 900, 430
    # 左：剛架
    s = 22  # px per m
    Ax, Ay = 60, 90
    Cx, Cy = Ax + 12 * s, Ay
    Dx, Dy = Cx, Ay + 12 * s
    o = wall(Ax, Ay, 60, 'left')
    o += L(Ax, Ay, Cx, Cy, INK, 4) + L(Cx, Cy, Dx, Dy, INK, 6)
    o += roller(Dx, Dy)
    o += joint(Ax + 6 * s, Ay, INK, 4.5)
    o += A(Ax + 6 * s, Ay - 52, Ax + 6 * s, Ay - 6, LOAD, 2.6, 11)
    o += T(Ax + 6 * s + 8, Ay - 36, '20 kN', 15, LOAD, 'start', 'bold')
    o += T(Ax - 6, Ay - 36, 'A', 16, INK, 'start', 'bold') + T(Ax + 6 * s, Ay + 26, 'B', 16, INK, 'middle', 'bold')
    o += T(Cx + 10, Cy - 10, 'C', 16, INK, 'start', 'bold') + T(Dx + 22, Dy + 8, 'D', 16, INK, 'start', 'bold')
    o += T(Ax + 3 * s, Ay + 26, '*EI*', 15, INK, 'middle') + T(Cx - 12, Ay + 6 * s, '2*EI*', 15, MOM, 'end', 'bold')
    o += dim(Ax, Ay + 52, Ax + 6 * s, Ay + 52, '6 m', MUT) + dim(Ax + 6 * s, Ay + 52, Cx, Ay + 52, '6 m', MUT)
    o += dim(Cx + 60, Cy, Cx + 60, Dy, '12 m', MUT, side=1)
    o += A(Dx, Dy + 72, Dx, Dy + 34, FOR, 2.4, 10) + T(Dx - 10, Dy + 66, '*R*', 16, FOR, 'end', 'bold')
    o += T(Dx + 26, Dy + 56, '*D*_{x} = 0', 15, FOR, 'start', 'bold')
    # 右：柱下半段自由體
    bx, top, bot = 620, 110, 330
    o += T(bx, 50, 'CD 柱下半段（切在高度 *y*）', 16, INK, 'middle', 'bold')
    o += L(bx, top, bx, bot, INK, 6)
    o += L(bx - 26, top, bx + 26, top, INK, 1.5, '4 3')
    o += roller(bx, bot)
    o += A(bx, bot + 72, bx, bot + 34, FOR, 2.4, 10) + T(bx - 10, bot + 66, '*R*', 16, FOR, 'end', 'bold')
    o += A(bx, top - 50, bx, top - 4, TEN, 2.2, 10) + T(bx + 10, top - 26, '*N* = *R*（壓）', 15, TEN, 'start', 'bold')
    o += T(bx + 34, top + 10, '*V* = 0', 15, TEN, 'start') + T(bx + 34, top + 36, '*M* = 0', 15, MOM, 'start', 'bold')
    o += dim(bx - 50, top, bx - 50, bot, '*y*', MUT, side=-1)
    o += R(700, 190, 190, 110, KEY2, PUR, 1.4, 10)
    o += T(795, 218, 'Σ*M*_{切口} = *R* × 0', 15, PUR, 'middle', 'bold')
    o += T(795, 246, '→ *M*_{CD} ≡ 0', 15, PUR, 'middle', 'bold')
    o += T(795, 274, '2*EI* 用不到', 15, MOM, 'middle', 'bold')
    return svg(W, H, o, 'SA-2014-4 CD 柱沒有彎矩')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4, 'fig1_5': fig1_5, 'fig1_6': fig1_6}
