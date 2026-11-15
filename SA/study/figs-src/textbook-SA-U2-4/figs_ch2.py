# -*- coding: utf-8 -*-
"""第 2 章：梁元素的四個數字。變形形狀一律由 Hermite 形狀函數（calcs.hermite）算出。"""
from figs_common import *  # noqa
from calcs import modified_and_sway, portal_symbolic


def _cant_panel(x0, kind):
    o = ''
    bx, by, Lp = x0 + 40, 128, 300
    title = '(a) 自由端受力 *V*' if kind == 'V' else '(b) 自由端受彎矩 *M*'
    o += T(x0 + 210, 34, title, 16, INK, 'middle', 'bold')
    o += vwall(bx, by, 70)
    o += L(bx, by, bx + Lp, by, STEEL, 2, '6 5')
    sc = 56
    fn = (lambda xi: xi**2 * (3 - xi) / 2) if kind == 'V' else (lambda xi: xi**2)
    pts = [(bx + Lp * i / 80, by - sc * fn(i / 80)) for i in range(81)]
    o += P(pts, AC, 3.2)
    tx, ty = bx + Lp, by - sc
    if kind == 'V':
        o += A(tx, ty + 62, tx, ty + 8, COMP, 3, 12)
        o += T(tx + 10, ty + 58, '*V*', 17, COMP, 'start', 'bold')
    else:
        o += arc_arrow(tx, ty, 26, -60, 200, COMP, 2.6, 11)
        o += T(tx + 26, ty + 26, '*M*', 17, COMP, 'start', 'bold')
    o += dim(tx + 46, by, tx + 46, ty, '', AC)
    o += T(tx - 6, by + 26, 'Δ', 16, AC, 'middle', 'bold', italic=True)
    # M/EI 圖
    gy, gh = 290, 62
    o += L(bx, gy, bx + Lp, gy, INK, 1.4)
    if kind == 'V':
        o += P([(bx, gy), (bx, gy - gh), (bx + Lp, gy)], AC, 1.8, fill=AC2, close=True)
        o += T(bx + 8, gy - gh - 10, '*VL*/*EI*', 15, AC, 'start', 'bold')
        cxp = bx + Lp / 3
        o += C(cxp, gy - gh / 3, 5, KEY, '#fff', 1.4)
        o += dim(cxp, gy + 22, bx + Lp, gy + 22, '力臂 2*L*/3', KEY, size=15, lab_off=12)
        o += T(x0 + 210, gy + 88, '面積 *VL*^{2}/2*EI* ＝ θ', 16, INK, 'middle', 'bold')
        o += T(x0 + 210, gy + 118, '面積 × 2*L*/3 ＝ Δ ＝ *VL*^{3}/3*EI*', 16, KEY, 'middle', 'bold')
    else:
        o += R(bx, gy - gh, Lp, gh, AC2, AC, 1.8)
        o += T(bx + 8, gy - gh - 10, '*M*/*EI*', 15, AC, 'start', 'bold')
        cxp = bx + Lp / 2
        o += C(cxp, gy - gh / 2, 5, KEY, '#fff', 1.4)
        o += dim(cxp, gy + 22, bx + Lp, gy + 22, '力臂 *L*/2', KEY, size=15, lab_off=12)
        o += T(x0 + 210, gy + 88, '面積 *ML*/*EI* ＝ θ', 16, INK, 'middle', 'bold')
        o += T(x0 + 210, gy + 118, '面積 × *L*/2 ＝ Δ ＝ *ML*^{2}/2*EI*', 16, KEY, 'middle', 'bold')
    return o


def fig2_1():
    W, H = 900, 430
    o = _cant_panel(0, 'V') + _cant_panel(450, 'M')
    o += L(450, 20, 450, 420, GRID, 1.2)
    return svg(W, H, o, '懸臂梁自由端的四個變形')


def _tip_panel(x0, kind):
    o = ''
    bx, by, Lp = x0 + 40, 150, 300
    if kind == 'v':
        o += T(x0 + 210, 34, '(a) 推 1：自由端上移 1、轉角鎖住', 16, INK, 'middle', 'bold')
        co = (0, 0, 0.2, 0)
    else:
        o += T(x0 + 210, 34, '(b) 轉 1：自由端轉 1、平移鎖住', 16, INK, 'middle', 'bold')
        co = (0, 0, 0, 0.32)
    o += vwall(bx, by, 70)
    o += L(bx, by, bx + Lp, by, STEEL, 2, '6 5')
    o += beam_shape(bx, by, Lp, co, Lp, AC, 3.2)
    tx = bx + Lp
    ty = by - Lp * co[2]
    if kind == 'v':
        o += lock(tx + 52, ty + 4)
        o += T(tx + 52, ty + 30, '鎖轉角', 14, WARN, 'middle')
        o += A(tx, ty + 74, tx, ty + 10, COMP, 3, 12)
        o += T(tx - 10, ty + 92, '*V* = 12*EI*/*L*^{3}', 16, COMP, 'end', 'bold')
        o += arc_arrow(tx, ty, 30, 160, -40, COMP, 2.6, 11)
        o += T(tx - 40, ty - 22, '*M* = −6*EI*/*L*^{2}（順時針）', 16, COMP, 'end', 'bold')
        o += dim(tx + 96, by, tx + 96, ty, '1', AC, size=15, lab_off=10, side=-1)
    else:
        o += lock(tx + 6, ty + 62)
        o += T(tx + 22, ty + 66, '鎖平移', 14, WARN, 'start')
        o += arc_arrow(tx, ty, 30, -70, 160, COMP, 2.6, 11)
        o += T(tx - 30, ty - 36, '*M* = 4*EI*/*L*', 16, COMP, 'end', 'bold')
        o += A(tx + 40, ty - 60, tx + 40, ty - 6, COMP, 3, 12)
        o += T(tx + 30, ty - 70, '*V* = −6*EI*/*L*^{2}（向下）', 16, COMP, 'end', 'bold')
        a = math.atan(0.32)
        o += L(tx - 80 * math.cos(a), ty + 80 * math.sin(a), tx + 40 * math.cos(a), ty - 40 * math.sin(a), AC, 1.3, '4 3')
        o += T(tx - 92, ty + 38, '斜率 1', 15, AC, 'end')
    return o


def fig2_2():
    W, H = 900, 300
    o = _tip_panel(0, 'v') + _tip_panel(450, 'th')
    o += L(450, 20, 450, 290, GRID, 1.2)
    o += T(450, 280, '', 14)
    return svg(W, H, o, '反過來問：要多少力才能推 1 或轉 1')


def fig2_3():
    W, H = 900, 400
    o = ''
    bx, by, Lp = 150, 120, 480
    o += vwall(bx, by, 70)
    o += L(bx, by, bx + Lp, by, STEEL, 2, '6 5')
    o += beam_shape(bx, by, Lp, (0, 0, 0, 0.32), Lp, AC, 3.2)
    tx = bx + Lp
    o += arc_arrow(tx, by, 30, -70, 160, COMP, 2.6, 11)
    o += T(tx + 34, by - 18, '*M*_{2} = 4', 17, COMP, 'start', 'bold')
    o += A(tx + 54, by + 4, tx + 54, by + 58, COMP, 3, 12)
    o += T(tx + 64, by + 54, '*V*_{2} = 6（向下）', 16, COMP, 'start', 'bold')
    o += arc_arrow(bx + 4, by, 30, -70, 160, KEY, 2.6, 11)
    o += T(bx - 30, by - 30, '*M*_{1} = ?', 17, KEY, 'end', 'bold')
    o += A(bx + 40, by + 70, bx + 40, by + 12, KEY, 3, 12)
    o += T(bx + 50, by + 76, '*V*_{1} = ?', 16, KEY, 'start', 'bold')
    o += T(bx + Lp / 2, 40, '單位：*EI*/*L*（彎矩）、*EI*/*L*^{2}（剪力）；逆時針、向上為正', 15, MUT, 'middle')
    # 彎矩圖：−2 → +4，零點在 L/3
    gy, sc = 300, 15
    o += L(bx, gy, bx + Lp, gy, INK, 1.4)
    x0 = bx + Lp / 3
    o += P([(bx, gy), (bx, gy + 2 * sc), (x0, gy)], WARN, 1.6, fill=WARN2, close=True)
    o += P([(x0, gy), (bx + Lp, gy - 4 * sc), (bx + Lp, gy)], AC, 1.6, fill=AC2, close=True)
    o += T(bx - 8, gy + 2 * sc + 6, '−2', 16, WARN, 'end', 'bold')
    o += T(bx + Lp + 8, gy - 4 * sc + 6, '+4', 16, AC, 'start', 'bold')
    o += C(x0, gy, 5, KEY, '#fff', 1.4)
    o += dim(bx, gy + 48, x0, gy + 48, '*L*/3（反曲點）', KEY, size=15, lab_off=12)
    o += T(bx + Lp * 0.66, gy + 40, '梁內彎矩：直線（無跨間載重）', 15, MUT, 'middle')
    o += R(660, 290, 226, 70, KEY2, KEY, 1.6, 9)
    o += T(773, 318, '遠端拿到一半', 16, KEY, 'middle', 'bold')
    o += T(773, 346, '*M*_{1} = 2 ＝ 4 × 1/2', 16, INK, 'middle', 'bold')
    return svg(W, H, o, '平衡補出 2EI/L')


def _unit_panel(x0, y0, idx):
    """idx 0..3：推 v1、θ1、v2、θ2；畫形狀與四個端力（×EI/L³，彎矩含 L）。"""
    names = ['推 *v*_{1} = 1', '轉 θ_{1} = 1', '推 *v*_{2} = 1', '轉 θ_{2} = 1']
    cols = [('12', '6*L*', '−12', '6*L*'), ('6*L*', '4*L*^{2}', '−6*L*', '2*L*^{2}'),
            ('−12', '−6*L*', '12', '−6*L*'), ('6*L*', '2*L*^{2}', '−6*L*', '4*L*^{2}')]
    co = [(0.2, 0, 0, 0), (0, 0.3, 0, 0), (0, 0, 0.2, 0), (0, 0, 0, 0.3)][idx]
    o = T(x0 + 215, y0 + 24, f'{"①②③④"[idx]} {names[idx]}（其他鎖住）→ 第 {idx + 1} 行', 16, INK, 'middle', 'bold')
    bx, by, Lp = x0 + 95, y0 + 100, 240
    o += L(bx, by, bx + Lp, by, STEEL, 2, '6 5')
    o += beam_shape(bx, by, Lp, co, Lp, AC, 3)
    o += node(bx, by - Lp * co[0], 5) + node(bx + Lp, by - Lp * co[2], 5)
    V1, M1, V2, M2 = cols[idx]
    def lab(x, y, s, anchor):
        neg = s.startswith('−')
        return T(x, y, s, 16, COMP, anchor, 'bold')
    o += T(bx - 14, by - 10, '*V*_{1}', 14, MUT, 'end') + lab(bx - 14, by + 14, V1, 'end')
    o += T(bx - 14, by + 38, '*M*_{1}', 14, MUT, 'end') + lab(bx - 14, by + 60, M1, 'end')
    o += T(bx + Lp + 14, by - 10, '*V*_{2}', 14, MUT, 'start') + lab(bx + Lp + 14, by + 14, V2, 'start')
    o += T(bx + Lp + 14, by + 38, '*M*_{2}', 14, MUT, 'start') + lab(bx + Lp + 14, by + 60, M2, 'start')
    return o


def fig2_4():
    W, H = 900, 400
    o = ''
    for i in range(4):
        o += _unit_panel((i % 2) * 450, (i // 2) * 190, i)
    o += L(450, 10, 450, 390, GRID, 1.2) + L(10, 190, 890, 190, GRID, 1.2)
    o += T(450, 396, '', 14)
    return svg(W, H, o, '四個單位變形 = 梁元素 4×4 的四行')


def _col_panel(x0, kind):
    o = ''
    by, ty = 330, 110
    cx = x0 + 70
    H = by - ty
    titles = {'ff': '(a) 底固定、頂鎖轉', 'fr': '(b) 底固定、頂自由轉', 'pf': '(c) 底鉸、頂鎖轉', 'pp': '(d) 兩端都鉸'}
    vals = {'ff': '12*EI*/*L*^{3}', 'fr': '3*EI*/*L*^{3}', 'pf': '3*EI*/*L*^{3}', 'pp': '0（機構）'}
    fns = {'ff': lambda e: 3 * e**2 - 2 * e**3, 'fr': lambda e: (3 * e**2 - e**3) / 2,
           'pf': lambda e: (3 * e - e**3) / 2, 'pp': lambda e: e}
    o += T(x0 + 105, 34, titles[kind], 16, INK, 'middle', 'bold')
    o += L(cx, by, cx, ty, STEEL, 2, '6 5')
    sc = 62
    pts = [(cx + sc * fns[kind](i / 80), by - H * i / 80) for i in range(81)]
    o += P(pts, AC, 3.2)
    if kind in ('ff', 'fr'):
        o += fixed_wall(cx, by, 56)
    else:
        o += pin(cx, by)
    tx = cx + sc
    if kind in ('ff', 'pf'):
        o += R(tx - 26, ty - 8, 52, 8, WARN, None)
        o += T(tx + 30, ty - 12, '鎖轉', 14, WARN, 'start')
    elif kind == 'pp':
        o += C(tx, ty, 6, '#fff', INK, 1.8)
    o += A(tx + 8, ty + 36, tx + 56, ty + 36, COMP, 3, 12)
    o += T(tx + 40, ty + 62, '*k*', 17, COMP, 'middle', 'bold')
    o += R(x0 + 12, 372, 186, 40, KEY2 if kind != 'pp' else STEEL2, KEY if kind != 'pp' else MUT, 1.6, 9)
    o += T(x0 + 105, 398, '*k* = ' + vals[kind], 16, KEY if kind != 'pp' else MUT, 'middle', 'bold')
    return o


def fig2_5():
    W, H = 900, 430
    o = ''
    for i, k in enumerate(('ff', 'fr', 'pf', 'pp')):
        o += _col_panel(10 + i * 222, k)
        if i:
            o += L(10 + i * 222, 20, 10 + i * 222, 420, GRID, 1.2)
    return svg(W, H, o, '柱的側移勁度四種情形')


def fig2_6():
    W, H = 900, 400
    o = ''
    ax, ay, s = 90, 330, 230
    B, Cn, D = (ax, ay - s), (ax + s, ay - s), (ax + s, ay)
    o += L(ax, ay, *B, INK, 5) + L(*B, *Cn, INK, 5) + L(*D, *Cn, INK, 5)
    o += fixed_wall(ax, ay, 56) + fixed_wall(D[0], D[1], 56)
    for (p, n, dx, dy) in ((B, 'B', 20, 30), (Cn, 'C', -20, 30), ((ax, ay), 'A', -20, 30), (D, 'D', 20, 30)):
        o += T(p[0] + dx, p[1] + dy, n, 17, INK, 'middle', 'bold')
    o += arc_arrow(B[0], B[1], 26, -60, 200, AC, 2.4, 10) + T(B[0] - 26, B[1] - 34, 'θ_{B}', 16, AC, 'end', 'bold')
    o += arc_arrow(Cn[0], Cn[1], 26, -20, 240, AC, 2.4, 10) + T(Cn[0] + 26, Cn[1] - 34, 'θ_{C}', 16, AC, 'start', 'bold')
    o += A(Cn[0] + 10, Cn[1] + 34, Cn[0] + 66, Cn[1] + 34, AC, 3, 12) + T(Cn[0] + 72, Cn[1] + 40, 'Δ', 17, AC, 'start', 'bold', italic=True)
    o += A(Cn[0] + 10, Cn[1] - 2, Cn[0] + 60, Cn[1] - 2, COMP, 2.6, 11) + T(Cn[0] + 66, Cn[1] + 2, '*P*', 16, COMP, 'start', 'bold')
    o += T(ax - 14, ay - s / 2, '*EI*, *L*', 15, MUT, 'end') + T(ax + s / 2, B[1] - 14, '*EI*, *L*', 15, MUT, 'middle')
    o += T(ax + s / 2, 30, 'SA-2025-1 門型剛架（自由度 θ_{B}、θ_{C}、Δ）', 16, INK, 'middle', 'bold')
    # 右側兩個元素卡
    def card(x, y, w, title, rows, hdr, c):
        q = R(x, y, w, 76 + 32 * len(rows), '#fff', c, 1.8, 10)
        q += T(x + w / 2, y + 28, title, 16, c, 'middle', 'bold')
        cw = (w - 90) / len(hdr)
        for j, hname in enumerate(hdr):
            q += T(x + 90 + cw * (j + 0.5), y + 56, hname, 15, MUT, 'middle', 'bold')
        for i, (rname, vals) in enumerate(rows):
            yy = y + 56 + 32 * (i + 1)
            q += T(x + 60, yy, rname, 15, MUT, 'end', 'bold')
            for j, v in enumerate(vals):
                q += T(x + 90 + cw * (j + 0.5), yy, v, 16, INK, 'middle', 'bold')
        return q
    o += card(430, 56, 450, '柱（底固定）：頂端 (Δ, θ) 的 2×2',
              [('Δ', ('12*EI*/*L*^{3}', '6*EI*/*L*^{2}')), ('θ', ('6*EI*/*L*^{2}', '4*EI*/*L*'))],
              ('Δ 推 1', 'θ 轉 1'), AC)
    o += card(430, 226, 450, '梁（兩端無側向相對位移）：(θ_{B}, θ_{C})',
              [('θ_{B}', ('4*EI*/*L*', '2*EI*/*L*')), ('θ_{C}', ('2*EI*/*L*', '4*EI*/*L*'))],
              ('θ_{B} 轉 1', 'θ_{C} 轉 1'), TEN)
    return svg(W, H, o, '門型剛架拆成三個元素')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5, 'fig2_6': fig2_6}
