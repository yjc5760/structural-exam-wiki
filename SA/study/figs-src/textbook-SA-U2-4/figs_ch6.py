# -*- coding: utf-8 -*-
"""第 6 章：靜態凝縮與側向勁度。變形由 Frame（Hermite）算出，曲線與數值取自 calcs。"""
from figs_common import *  # noqa
from calcs import portal_symbolic, portal_limits, pushover_2024, sp, L_

PN = {'A': (0, 0), 'B': (0, 1), 'C': (1, 1), 'D': (1, 0)}
PM = [('A', 'B'), ('B', 'C'), ('D', 'C')]


def _portal(x0, y0, sc, th, amp, lock_rot):
    fr = Frame(PN, PM, x0, y0, sc)
    o = fr.undeformed() + fixed_wall(*fr.P('A'), 46) + fixed_wall(*fr.P('D'), 46)
    D = {'B': (1, 0, th), 'C': (1, 0, th)}
    o += fr.deformed(D, amp, AC, 3.4)
    if lock_rot:
        for nm in ('B', 'C'):
            x, y = fr.P(nm); x += amp * sc
            o += lock(x + (-20 if nm == 'B' else 20), y - 16)
    cx, cy = fr.P('C')
    o += A(cx + amp * sc + 14, cy, cx + amp * sc + 60, cy, COMP, 3, 12)
    return fr, o


def fig6_1():
    W, H = 900, 400
    th = float(portal_symbolic()['th_per_delta'].subs(L_, 1))
    o = ''
    fr, q = _portal(90, 300, 200, 0.0, 0.16, True)
    o += q + T(190, 36, '(a) 轉角鎖住：*k* ＝ 12 ＋ 12 ＝ 24', 16, INK, 'middle', 'bold')
    o += T(190, 64, '（第 3 章的 *K*_{33}，梁等於無限剛）', 14, MUT, 'middle')
    fr2, q2 = _portal(540, 300, 200, th, 0.16, False)
    o += q2 + T(640, 36, '(b) 放手讓 B、C 自己轉：*k* ＝ 84/5 ＝ 16.8', 16, INK, 'middle', 'bold')
    o += T(640, 64, f'B、C 自己轉到 θ ＝ −{abs(th):.1f} Δ/*L*（順時針），讓節點彎矩＝0', 14, KEY, 'middle')
    bx, by = fr2.P('B'); bx += 0.16 * 200
    o += arc_arrow(bx, by, 26, 120, -10, KEY, 2.4, 10)
    cx, cy = fr2.P('C'); cx += 0.16 * 200
    o += arc_arrow(cx, cy, 26, 120, -10, KEY, 2.4, 10)
    o += L(450, 20, 450, 330, GRID, 1.2)
    o += R(120, 340, 660, 48, KEY2, KEY, 1.6, 9)
    o += T(450, 370, '🌱 S6：沒有外力的自由度，會自己轉到「力＝0」為止 → 勁度變小', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '凝縮：放手的自由度自己找平衡')


def fig6_2():
    W, H = 900, 380
    pl = portal_limits()
    rho = sp.Symbol('rho', nonnegative=True)
    fn = sp.lambdify(rho, pl['k'])
    pt = Plot(110, 50, 560, 250, 0, 6, 0, 26)
    o = pt.axes([0, 1, 2, 3, 4, 5, 6], [0, 6, 12, 16.8, 24], 'ρ', '*k*·*L*^{3}/*EI*_{c}', yfmt=lambda v: f(v))
    o += pt.hline(24, c=MUT) + T(pt.X(6) + 8, pt.Y(24) + 5, '24（梁無限剛）', 15, MUT, 'start', 'bold')
    o += pt.hline(6, c=MUT) + T(pt.X(6) + 8, pt.Y(6) + 5, '6（梁無勁度）', 15, MUT, 'start', 'bold')
    o += pt.curve(lambda r: float(fn(r)), 0, 6, AC, 3.2)
    o += pt.dot(1, 16.8, KEY, 7)
    o += T(pt.X(1) + 12, pt.Y(16.8) + 26, 'ρ＝1：84/5＝16.8（SA-2025-1）', 15, KEY, 'start', 'bold')
    o += pt.dot(0, 6, AC, 6)
    o += T(pt.X(3.2), pt.Y(9), 'ρ ＝ (*EI*_{b}/*L*_{b}) ÷ (*EI*_{c}/*L*_{c})', 15, INK, 'middle', 'bold')
    o += T(pt.X(3.2), pt.Y(3), '梁越硬，柱頂越轉不動，越接近 24', 14, MUT, 'middle')
    return svg(W, H, o, '側向勁度與梁柱勁度比')


def fig6_3():
    W, H = 900, 320
    o = ''
    x0, y0, s = 60, 70, 84
    blocks = [('*K*_{aa}', 0, 0, AC2, AC), ('*K*_{ab}', 1, 0, STEEL2, MUT), ('*K*_{ba}', 0, 1, STEEL2, MUT), ('*K*_{bb}', 1, 1, KEY2, KEY)]
    for t, j, i, fill, c in blocks:
        o += R(x0 + j * s, y0 + i * s, s, s, fill, c, 1.8)
        o += T(x0 + j * s + s / 2, y0 + i * s + s / 2 + 6, t, 18, c, 'middle', 'bold')
    vx = x0 + 2 * s + 16
    o += R(vx, y0, 60, s, AC2, AC, 1.8) + T(vx + 30, y0 + s / 2 + 6, '*D*_{a}', 17, AC, 'middle', 'bold')
    o += R(vx, y0 + s, 60, s, KEY2, KEY, 1.8) + T(vx + 30, y0 + s * 1.5 + 6, '*D*_{b}', 17, KEY, 'middle', 'bold')
    o += T(vx + 84, y0 + s + 8, '＝', 22, INK, 'middle', 'bold')
    ox = vx + 108
    o += R(ox, y0, 60, s, AC2, AC, 1.8) + T(ox + 30, y0 + s / 2 + 6, '*P*_{a}', 17, AC, 'middle', 'bold')
    o += R(ox, y0 + s, 60, s, KEY2, KEY, 1.8) + T(ox + 30, y0 + s * 1.5 + 6, '0', 19, KEY, 'middle', 'bold')
    o += T(x0 - 10, y0 + s / 2 + 6, 'a 留下', 15, AC, 'end', 'bold')
    o += T(x0 - 10, y0 + s * 1.5 + 6, 'b 放手', 15, KEY, 'end', 'bold')
    o += T(ox + 74, y0 + s * 1.5 + 6, '← S6', 15, KEY, 'start', 'bold')
    bx = 520
    st = [('① 下半列', '[*K*_{ba}]{*D*_{a}} ＋ [*K*_{bb}]{*D*_{b}} ＝ 0', KEY),
          ('② 解出放手的那幾個', '{*D*_{b}} ＝ −[*K*_{bb}]^{−1}[*K*_{ba}]{*D*_{a}}', KEY),
          ('③ 代回上半列', '[*K*^{*}] ＝ [*K*_{aa}] − [*K*_{ab}][*K*_{bb}]^{−1}[*K*_{ba}]', AC)]
    for i, (a, b, c) in enumerate(st):
        y = 40 + i * 86
        o += R(bx, y, 370, 70, '#fff', c, 1.8, 10)
        o += T(bx + 16, y + 26, a, 15, c, 'start', 'bold')
        o += T(bx + 16, y + 54, b, 15, INK, 'start', 'bold')
    o += T(250, 296, '一個自由度時：*k*^{*} ＝ *a* − *b*^{2}/*c*（減掉的永遠是正的 → 凝縮後只會變軟）', 15, MUT, 'middle')
    return svg(W, H, o, '靜態凝縮＝分塊消去')


def _stage_icon(x0, y0, stage):
    sc = 38
    fr = Frame({'A': (0, 0), 'B': (0, 2), 'C': (1, 2), 'D': (1, 0)}, [('A', 'B'), ('B', 'C'), ('D', 'C')], x0, y0, sc)
    o = fr.solid(INK, 3) + fixed_wall(*fr.P('A'), 34) + fixed_wall(*fr.P('D'), 34)
    if stage >= 2:
        bx, by = fr.P('B'); cx, cy = fr.P('C')
        o += plastic_hinge(bx + 7, by, 6) + plastic_hinge(cx - 7, cy, 6)
    if stage >= 3:
        o += plastic_hinge(*fr.P('A'), 6) + plastic_hinge(*fr.P('D'), 6)
    return o


def fig6_4():
    W, H = 900, 420
    po = pushover_2024()
    D1, D2 = po['D1'] * 1000, po['D2'] * 1000
    pt = Plot(100, 60, 470, 270, 0, 50, 0, 140)
    o = pt.axes([0, 10, 20, 30, 40, 50], [0, 25, 50, 75, 100, 125], 'Δ (mm)', '*P* (kN)')
    pts = [(0, 0), (D1, po['P1']), (D2, po['P2']), (50, po['P2'])]
    o += P([pt.pt(*p) for p in pts], AC, 3.4)
    o += pt.dot(D1, po['P1'], COMP, 6) + pt.dot(D2, po['P2'], COMP, 6)
    o += T(pt.X(D1) + 10, pt.Y(po['P1']) + 26, f'① ({D1:.2f}, {po["P1"]:.0f})', 15, COMP, 'start', 'bold')
    o += T(pt.X(D2) - 8, pt.Y(po['P2']) - 14, f'② ({D2:.2f}, {po["P2"]:.2f})', 15, COMP, 'end', 'bold')
    o += T(pt.X(1.5), pt.Y(80), f'{po["kt1"]:.1f} kN/m', 14, AC, 'start', 'bold')
    o += T(pt.X(D1) + 26, pt.Y(108) + 18, f'{po["kt2"]:.1f}', 14, AC, 'start', 'bold')
    o += T(pt.X(42), pt.Y(po['P2']) + 26, '勁度 0（機構）', 14, AC, 'middle', 'bold')
    # 右側三階段
    xs = 640
    labs = [('彈性', f'*k* ＝ {po["k1"]:.1f}*EI*/*L*^{{3}}', '梁端最先到 300'),
            ('梁端塑鉸', f'*k* ＝ {po["k2"]:.1f}*EI*/*L*^{{3}}', '柱底最先到 580'),
            ('＋柱底塑鉸', '*k* ＝ 0', '側移機構')]
    for i, (a, b, c) in enumerate(labs):
        y = 40 + i * 125
        o += _stage_icon(xs + 20, y + 100, i + 1)
        o += T(xs + 96, y + 30, a, 15, INK, 'start', 'bold')
        o += T(xs + 96, y + 58, b, 15, AC, 'start', 'bold')
        o += T(xs + 96, y + 84, c, 14, MUT, 'start')
    o += T(330, 410, '紅點＝塑鉸（彎矩固定、可自由轉）＝在 [*K*] 裡把那一端「放手」', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2024-4 側推曲線')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
