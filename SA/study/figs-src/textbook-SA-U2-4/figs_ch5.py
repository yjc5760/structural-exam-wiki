# -*- coding: utf-8 -*-
"""第 5 章：載重向量與回代。變形＝Hermite（節點位移）＋固端梁的局部撓度；數值取自 calcs。"""
from figs_common import *  # noqa
from calcs import zframe_2018, fabrication_2011, fem_by_area, sp, L_, EI

ZN = {'A': (0, 1), 'B': (0, 0), 'C': (1, 0), 'D': (1, -1)}
ZM = [('A', 'B'), ('B', 'C'), ('D', 'C')]


def _zD():
    z = zframe_2018()
    sub = {sp.Symbol('P', positive=True): 1, L_: 1, EI: 1}
    u, tB, tC = [float(v.subs(sub)) for v in z['D']]
    return u, tB, tC


def _beam_particular(xi):
    """兩端固定梁中央集中力 P＝1（EI＝L＝1）的撓度（向上為正）。"""
    x = xi if xi <= 0.5 else 1 - xi
    return -x**2 * (3 - 4 * x) / 48


def _zframe(x0, y0, sc, mode, amp=5.0):
    fr = Frame(ZN, ZM, x0, y0, sc)
    o = fr.undeformed()
    o += fixed_wall(*fr.P('A'), 50, top=True) + fixed_wall(*fr.P('D'), 50)
    u, tB, tC = _zD()
    if mode in ('real', 'release'):
        D = {'B': (u, 0, tB), 'C': (u, 0, tC)}
        o += Frame(ZN, [('A', 'B'), ('D', 'C')], x0, y0, sc).deformed(D, amp, AC, 3.2)
    bx, by = fr.P('B')
    pts = []
    for k in range(61):
        xi = k / 60
        N = hermite(xi)
        v = 0.0
        if mode in ('real', 'release'):
            v += tB * N[1] + tC * N[3]
        if mode in ('real', 'lock'):
            v += _beam_particular(xi)
        uu = u if mode in ('real', 'release') else 0.0
        pts.append((bx + (xi + uu * amp) * sc, by - v * amp * sc))
    o += P(pts, AC, 3.2)
    if mode == 'lock':
        o += Frame(ZN, [('A', 'B'), ('D', 'C')], x0, y0, sc).solid(AC, 3.2)
    return fr, o


def fig5_1():
    W, H = 900, 400
    o = ''
    titles = {'real': '(a) 真實：*P* 在梁中央', 'lock': '(b) 先鎖住 B、C', 'release': '(c) 再放開：節點受 −固端力'}
    for i, mode in enumerate(('real', 'lock', 'release')):
        x0 = 80 + i * 300
        fr, q = _zframe(x0, 200, 115, mode)
        o += q + T(x0 + 60, 30, titles[mode], 15, INK, 'middle', 'bold')
        bx, by = fr.P('B'); cx, cy = fr.P('C')
        mx = (bx + cx) / 2
        if mode in ('real', 'lock'):
            o += A(mx, by - 64, mx, by - 14, COMP, 2.8, 11) + T(mx + 8, by - 52, '*P*', 16, COMP, 'start', 'bold')
        if mode == 'lock':
            o += lock(bx - 22, by - 16) + lock(cx + 22, cy - 16)
            o += arc_arrow(bx, by, 24, -30, 130, WARN, 2.2, 9) + T(bx - 8, by + 48, '+*PL*/8', 14, WARN, 'end', 'bold')
            o += arc_arrow(cx, cy, 24, 210, 50, WARN, 2.2, 9) + T(cx + 8, cy + 48, '−*PL*/8', 14, WARN, 'start', 'bold')
        if mode == 'release':
            o += arc_arrow(bx, by, 24, 130, -30, KEY, 2.4, 10) + T(bx - 8, by + 48, '−*PL*/8', 14, KEY, 'end', 'bold')
            o += arc_arrow(cx, cy, 24, 50, 210, KEY, 2.4, 10) + T(cx + 8, cy + 48, '+*PL*/8', 14, KEY, 'start', 'bold')
        if i < 2:
            o += T(x0 + 220, 210, '＝' if i == 0 else '＋', 30, INK, 'middle', 'bold')
    o += R(110, 340, 680, 46, KEY2, KEY, 1.6, 9)
    o += T(450, 369, '(b) 的鎖要出固端彎矩（橘）；(c) 把它反向加在節點上（紫）→ {*P*} ＝ −{固端力}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '先鎖住，再放開')


def _fem_panel(x0, kind):
    o = T(x0 + 210, 32, '(a) 均布 *w*' if kind == 'w' else '(b) 中央集中力 *P*', 16, INK, 'middle', 'bold')
    bx, Lp, gy = x0 + 50, 320, 170
    o += L(bx, gy, bx + Lp, gy, INK, 1.4)
    if kind == 'w':
        top = 80
        pts = [(bx + Lp * k / 60, gy - top * 4 * (k / 60) * (1 - k / 60)) for k in range(61)]
        o += P(pts + [(bx + Lp, gy)], AC, 1.8, fill=AC2, close=True)
        h = top * 2 / 3
        o += T(bx + Lp / 2, gy - top - 12, '簡支 *wL*^{2}/8', 15, AC, 'middle', 'bold')
        o += T(bx + Lp / 2, gy - 34, '面積 *wL*^{3}/12', 15, AC, 'middle', 'bold')
        res = '*M*_{端} ＝ *wL*^{2}/12'
    else:
        top = 80
        o += P([(bx, gy), (bx + Lp / 2, gy - top), (bx + Lp, gy)], AC, 1.8, fill=AC2, close=True)
        h = top / 2
        o += T(bx + Lp / 2, gy - top - 12, '簡支 *PL*/4', 15, AC, 'middle', 'bold')
        o += T(bx + Lp / 2, gy - 26, '面積 *PL*^{2}/8', 15, AC, 'middle', 'bold')
        res = '*M*_{端} ＝ *PL*/8'
    o += R(bx, gy, Lp, h, WARN2, WARN, 1.8)
    o += T(bx + Lp / 2, gy + h / 2 + 6, '端彎矩 × *L*（面積相同、號相反）', 15, WARN, 'middle', 'bold')
    o += R(x0 + 70, 270, 280, 46, KEY2, KEY, 1.6, 9)
    o += T(x0 + 210, 300, res, 17, KEY, 'middle', 'bold')
    return o


def fig5_2():
    W, H = 900, 330
    o = _fem_panel(0, 'w') + _fem_panel(450, 'P')
    o += L(450, 20, 450, 320, GRID, 1.2)
    return svg(W, H, o, '固端彎矩：M/EI 圖總面積為零')


def fig5_3():
    W, H = 900, 380
    fr = Frame(ZN, ZM, 130, 200, 140)
    o = fr.solid(INK, 5) + fixed_wall(*fr.P('A'), 56, top=True) + fixed_wall(*fr.P('D'), 56)
    bx, by = fr.P('B'); cx, cy = fr.P('C')
    for nm, (dx, dy) in {'A': (-26, 28), 'B': (-12, -14), 'C': (-18, 28), 'D': (28, -12)}.items():
        x, y = fr.P(nm); o += T(x + dx, y + dy, nm, 17, INK, 'middle', 'bold')
    mx = (bx + cx) / 2
    o += A(mx, by - 64, mx, by - 8, COMP, 3, 12) + T(mx + 8, by - 50, '*P*', 16, COMP, 'start', 'bold')
    o += A(cx + 14, cy + 40, cx + 70, cy + 40, AC, 2.6, 11) + T(cx + 76, cy + 46, '*D*_{1}＝*u*', 15, AC, 'start', 'bold')
    o += arc_arrow(bx, by, 26, 200, 330, AC, 2.4, 10) + T(bx - 24, by + 46, '*D*_{2}＝θ_{B}', 15, AC, 'end', 'bold')
    o += arc_arrow(cx, cy, 26, 10, 160, AC, 2.4, 10) + T(cx + 30, cy - 22, '*D*_{3}＝θ_{C}', 15, AC, 'start', 'bold')
    o += T(fr.S(-0.05, 0.5)[0], fr.S(0, 0.5)[1], '*EI*, *L*', 14, MUT, 'end')
    o += T(mx, by + 28, '*EI*, *L*', 14, MUT, 'middle')
    o += R(520, 50, 360, 280, '#fff', KEY, 2, 12)
    o += T(700, 82, '等效節點載重 {*P*} ＝ −{固端力}', 16, KEY, 'middle', 'bold')
    rows = [('*D*_{1}', '0', '梁上載重是垂直的，沒有水平分量'),
            ('*D*_{2}', '−*PL*/8', 'B 端固端 +*PL*/8 → 反號'),
            ('*D*_{3}', '+*PL*/8', 'C 端固端 −*PL*/8 → 反號')]
    for i, (a, b, c) in enumerate(rows):
        y = 130 + i * 62
        o += T(546, y, a, 16, AC, 'start', 'bold') + T(650, y, b, 17, KEY, 'middle', 'bold')
        o += T(546, y + 26, c, 14, MUT, 'start')
    o += T(700, 316, '（逆時針為正；固端彎矩的方向見圖 5-1(b)）', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2018-2 自由度與等效節點載重')


def fig5_4():
    W, H = 900, 400
    o = ''
    fr, q = _zframe(150, 210, 150, 'real', amp=6.0)
    o += q + T(225, 30, '(a) 變形（放大 6 倍）', 15, INK, 'middle', 'bold')
    o += A(fr.P('B')[0] - 30, 230, fr.P('B')[0] - 80, 230, AC, 2.4, 10)
    o += T(fr.P('B')[0] - 30, 258, '*u*＝−*PL*^{3}/48*EI*（向左）', 14, AC, 'middle', 'bold')
    o += T(24, 312, 'θ_{B}＝−*PL*^{2}/24*EI*（順時針）', 14, AC, 'start', 'bold')
    o += T(24, 336, 'θ_{C}＝＋*PL*^{2}/24*EI*（逆時針）', 14, AC, 'start', 'bold')
    # (b) BMD
    x0 = 560
    fr2 = Frame(ZN, ZM, x0, 210, 150)
    o += fr2.solid(INK, 3) + fixed_wall(*fr2.P('A'), 46, top=True) + fixed_wall(*fr2.P('D'), 46)
    o += T(x0 + 85, 34, '(b) 彎矩圖（畫在受拉側，×*PL*）', 15, INK, 'middle', 'bold')
    k = 150 * 1.2
    m1, m5 = 1 / 24 * k, 5 / 24 * k
    ax, ay = fr2.P('A'); bx, by = fr2.P('B'); cx, cy = fr2.P('C'); dx, dy = fr2.P('D')
    o += P([(ax, ay), (ax + m1, ay), (bx + m1, by), (bx, by)], WARN, 1.6, fill=WARN2, close=True, op=0.9)
    o += P([(cx, cy), (cx + m1, cy), (dx + m1, dy), (dx, dy)], WARN, 1.6, fill=WARN2, close=True, op=0.9)
    mx = (bx + cx) / 2
    # 梁：端點上方 PL/24（上拉）→ 跨中下方 5PL/24
    x_zero1 = bx + (cx - bx) / 2 * (1 / 6)
    o += P([(bx, by), (bx, by - m1), (x_zero1, by)], COMP, 1.6, fill=COMP2, close=True)
    o += P([(cx, cy), (cx, cy - m1), (cx - (x_zero1 - bx), cy)], COMP, 1.6, fill=COMP2, close=True)
    o += P([(x_zero1, by), (mx, by + m5), (cx - (x_zero1 - bx), cy)], AC, 1.6, fill=AC2, close=True)
    o += T(ax + m1 + 8, (ay + by) / 2, '1/24', 15, WARN, 'start', 'bold')
    o += T(dx + m1 + 8, (cy + dy) / 2, '1/24', 15, WARN, 'start', 'bold')
    o += T(bx + 6, by - m1 - 10, '1/24', 15, COMP, 'start', 'bold')
    o += T(cx - 6, cy - m1 - 10, '1/24', 15, COMP, 'end', 'bold')
    o += T(mx, by + m5 + 22, '5/24（下緣受拉）', 15, AC, 'middle', 'bold')
    o += T(x0 + 85, 386, '柱：全長等彎矩 → 柱剪力 0（沒有側力，合理）', 14, MUT, 'middle')
    o += L(450, 20, 450, 390, GRID, 1.2)
    return svg(W, H, o, 'SA-2018-2 變形與彎矩圖')


def fig5_5():
    W, H = 900, 400
    fb = fabrication_2011()
    N = {'A': (3, 4), 'B': (0, 4), 'C': (0, 0), 'D': (6, 0)}
    o = ''
    titles = ['(a) 鎖住 A，硬把 AC 拉長 0.02 m 接上', '(b) 放開：A 受 −(鎖的反力)', '(c) 疊加後的桿力（kN，拉＋）']
    for p in range(3):
        x0 = 30 + p * 295
        sc = 36
        S = lambda q, x0=x0: (x0 + 30 + q[0] * sc, 306 - q[1] * sc)
        o += T(x0 + 138, 34, titles[p], 14, INK, 'middle', 'bold')
        for nm in ('B', 'C', 'D'):
            col = INK
            if p == 2:
                Nf = fb['N']['A' + nm]; col = COMP if Nf > 0 else AC
                wdt = 3 + 4 * abs(Nf) / 20
            else:
                wdt = 5 if (p == 0 and nm == 'C') else 3
                col = COMP if (p == 0 and nm == 'C') else STEEL
            o += L(*S(N['A']), *S(N[nm]), col, wdt)
        o += pin(*S(N['C'])) + pin(*S(N['D']))
        bx, by = S(N['B'])
        o += P([(bx, by), (bx - 16, by - 11), (bx - 16, by + 11)], INK, 1.5, fill='#fff', close=True)
        o += L(bx - 16, by - 18, bx - 16, by + 18, INK, 2)
        ax, ay = S(N['A'])
        if p == 0:
            o += lock(ax + 4, ay - 18)
            o += T((ax + S(N['C'])[0]) / 2 - 10, (ay + S(N['C'])[1]) / 2, '*T*_{0}＝40', 15, COMP, 'end', 'bold')
            o += A(ax, ay, ax + 0.6 * 60, ay - 0.8 * 60, WARN, 2.6, 11)
            o += T(ax + 40, ay - 58, '鎖出 (24, 32)', 14, WARN, 'start', 'bold')
        if p == 1:
            o += A(ax, ay, ax - 0.6 * 60, ay + 0.8 * 60, KEY, 2.8, 11)
            o += T(ax - 30, ay + 66, '(−24, −32)', 14, KEY, 'end', 'bold')
            Dx, Dy = fb['D']
            amp = 4000
            o += A(ax + 50, ay - 60, ax + 50 + Dx * amp, ay - 60 - Dy * amp, AC, 2.6, 10)
            o += T(ax + 60, ay - 66, 'A 的位移', 14, AC, 'start', 'bold')
            o += T(ax + 60, ay - 44, f'({Dx * 1000:.2f}, {Dy * 1000:.1f}) mm', 14, AC, 'start', 'bold')
        if p == 2:
            labs = {'B': (-6, -12, 'end'), 'C': (-14, 0, 'end'), 'D': (14, 0, 'start')}
            for nm, (dx_, dy_, an) in labs.items():
                xm = (ax + S(N[nm])[0]) / 2; ym = (ay + S(N[nm])[1]) / 2
                Nf = fb['N']['A' + nm]
                o += T(xm + dx_, ym + dy_, f'{Nf:+.2f}', 15, COMP if Nf > 0 else AC, an, 'bold')
        o += node(ax, ay, 6)
        if p:
            o += T(ax - 12, ay - 12, 'A', 15, INK, 'end', 'bold')
        if p:
            o += L(x0 - 8, 20, x0 - 8, 390, GRID, 1.2)
    o += R(140, 352, 620, 40, KEY2, KEY, 1.6, 9)
    o += T(450, 378, 'AC ＝ *k e* ＋ *T*_{0} ＝ −26.03 ＋ 40 ＝ ＋13.97（別忘了加回 *T*_{0}）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2011-4 製造誤差')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4, 'fig5_5': fig5_5}
