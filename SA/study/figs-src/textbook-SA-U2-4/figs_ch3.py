# -*- coding: utf-8 -*-
"""第 3 章：自由度盤點與組裝。變形一律由節點位移＋Hermite（figs_common.Frame）算出。"""
from figs_common import *  # noqa
from calcs import portal_symbolic, rigid_bar_2012, sp, L_, EI

PORTAL_N = {'A': (0, 0), 'B': (0, 1), 'C': (1, 1), 'D': (1, 0)}
PORTAL_M = [('A', 'B'), ('B', 'C'), ('D', 'C')]


def _dof_marks(x, y, kill, side, c_ok=AC):
    """節點三個自由度：→、↑、↺（畫在節點外側 side＝−1 左、+1 右）；kill 中的畫灰色。"""
    o = ''
    cols = [c_ok if k not in kill else ('#b0bec5') for k in range(3)]
    if side < 0:
        o += A(x - 58, y, x - 10, y, cols[0], 2.6, 11)
    else:
        o += A(x + 10, y, x + 58, y, cols[0], 2.6, 11)
    o += A(x, y - 10, x, y - 56, cols[1], 2.6, 11)
    a0, a1 = (100, 230) if side < 0 else (-50, 80)
    o += arc_arrow(x, y, 30, a0, a1, cols[2], 2.4, 10)
    return o


def _x(x, y, c=WARN, s=8):
    return L(x - s, y - s, x + s, y + s, c, 3) + L(x - s, y + s, x + s, y - s, c, 3)


def fig3_1():
    W, H = 900, 420
    fr = Frame(PORTAL_N, PORTAL_M, 130, 350, 230)
    o = fr.solid(INK, 5)
    o += fixed_wall(*fr.P('A'), 56) + fixed_wall(*fr.P('D'), 56)
    for nm, (dx, dy) in {'A': (-46, 4), 'B': (-30, 34), 'C': (30, 34), 'D': (46, 4)}.items():
        x, y = fr.P(nm)
        o += T(x + dx, y + dy, nm, 17, INK, 'middle', 'bold')
    # A、D：三個都被支承鎖死（只畫 X）
    for nm in ('A', 'D'):
        x, y = fr.P(nm)
        o += _x(x - 18, y - 24) + _x(x + 18, y - 24) + _x(x, y - 46)
    bx, by = fr.P('B'); cx, cy = fr.P('C')
    o += _dof_marks(bx, by, {1}, -1) + _dof_marks(cx, cy, {1}, 1)
    o += T(bx + 8, by - 64, '柱不縮短', 14, MUT, 'start')
    o += T(cx - 8, cy - 64, '柱不縮短', 14, MUT, 'end')
    o += T((bx + cx) / 2, by + 30, '梁不伸長 → *u*_{B} ＝ *u*_{C} ＝ Δ', 14, MUT, 'middle')
    o += T((bx + cx) / 2, 30, '圓弧＝轉角，箭頭＝平移；灰色＝被約束吃掉', 14, MUT, 'middle')
    # 右側帳本
    x0, y0 = 520, 60
    o += R(x0, y0, 360, 300, '#fff', KEY, 2, 12)
    o += T(x0 + 180, y0 + 34, '自由度帳本', 17, KEY, 'middle', 'bold')
    rows = [('4 個節點 × 3', '12', INK), ('− 支承 A、D（固定端各 3）', '− 6', WARN),
            ('− 兩柱不縮短（*v*_{B}、*v*_{C}＝0）', '− 2', MUT), ('− 梁不伸長（*u*_{B}＝*u*_{C}）', '− 1', MUT)]
    for i, (a, b, c) in enumerate(rows):
        yy = y0 + 78 + i * 42
        o += T(x0 + 22, yy, a, 15, c, 'start', 'bold')
        o += T(x0 + 336, yy, b, 17, c, 'end', 'bold')
    o += L(x0 + 22, y0 + 228, x0 + 338, y0 + 228, INK, 1.6)
    o += T(x0 + 22, y0 + 260, '剩下 → θ_{B}、θ_{C}、Δ', 16, AC, 'start', 'bold')
    o += T(x0 + 336, y0 + 260, '3', 19, AC, 'end', 'bold')
    return svg(W, H, o, '門型剛架的自由度盤點')


def fig3_2():
    W, H = 900, 400
    o = ''
    cards = [('柱 AB', ('Δ', 'θ_{B}'), (('12', '6'), ('6', '4')), AC, 40),
             ('梁 BC', ('θ_{B}', 'θ_{C}'), (('4', '2'), ('2', '4')), TEN, 165),
             ('柱 DC', ('Δ', 'θ_{C}'), (('12', '6'), ('6', '4')), TEAL, 290)]
    for name, hd, vals, c, y in cards:
        o += R(30, y, 250, 108, '#fff', c, 2, 10)
        o += T(48, y + 26, name, 16, c, 'start', 'bold')
        o += T(270, y + 26, '代號 (' + '、'.join(hd) + ')', 14, MUT, 'end')
        for i in range(2):
            for j in range(2):
                o += R(140 + j * 64, y + 40 + i * 32, 64, 32, '#fff', c, 1)
                o += T(172 + j * 64, y + 62 + i * 32, vals[i][j], 15, c, 'middle', 'bold')
            o += T(130, y + 62 + i * 32, hd[i], 14, MUT, 'end', 'bold')
        o += A(290, y + 54, 420, 160 + (y - 165) * 0.35, c, 2, 10, dash='6 4')
    # 3×3 結果
    order = ('θ_{B}', 'θ_{C}', 'Δ')
    cells = [['4 + 4', '2', '6'], ['2', '4 + 4', '6'], ['6', '6', '12 + 12']]
    col = [[KEY2, '#e8f5e9', AC2], ['#e8f5e9', KEY2, '#e0f2f1'], [AC2, '#e0f2f1', KEY2]]
    o += mat_grid(500, 110, cells, 112, 52, hdr=order, rowhdr=order, colors=col, size=16)
    o += T(668, 68, '結構 [K]：照代號把數字丟進格子、同格相加', 15, INK, 'middle', 'bold')
    o += T(668, 300, '單位：轉角對轉角 ×*EI*/*L*、交叉 ×*EI*/*L*^{2}、Δ 對 Δ ×*EI*/*L*^{3}', 14, MUT, 'middle')
    o += R(520, 320, 300, 54, KEY2, KEY, 1.6, 9)
    o += T(670, 353, '紫色格＝兩個元素同時碰到', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '組裝：代號對號入座')


def _unit_portal(x0, kind):
    fr = Frame(PORTAL_N, PORTAL_M, x0 + 44, 300, 150)
    o = fr.undeformed() + fixed_wall(*fr.P('A'), 46) + fixed_wall(*fr.P('D'), 46)
    if kind == 'D':
        D = {'B': (1, 0, 0), 'C': (1, 0, 0)}; amp = 0.2
        title = '③ 推 Δ＝1（轉角鎖住）'
        lab = [('B', '6', -1), ('C', '6', 1)]; F = '24'
    elif kind == 'B':
        D = {'B': (0, 0, 1)}; amp = 0.28
        title = '① 轉 θ_{B}＝1（其他鎖住）'
        lab = [('B', '8', -1), ('C', '2', 1)]; F = '6'
    else:
        D = {'C': (0, 0, 1)}; amp = 0.28
        title = '② 轉 θ_{C}＝1（其他鎖住）'
        lab = [('B', '2', -1), ('C', '8', 1)]; F = '6'
    o += fr.deformed(D, amp, AC, 3.2)
    o += T(x0 + 145, 40, title, 16, INK, 'middle', 'bold')
    for nm, v, sd in lab:
        x, y = fr.P(nm)
        x += D.get(nm, (0, 0, 0))[0] * amp * fr.sc
        o += arc_arrow(x, y, 20, -60, 200, COMP, 2.2, 9)
        o += T(x + sd * 30, y - 28, v, 17, COMP, 'middle', 'bold')
    cx, cy = fr.P('C'); cx += D.get('C', (0, 0, 0))[0] * amp * fr.sc
    o += A(cx + 14, cy + 34, cx + 52, cy + 34, COMP, 2.6, 10)
    o += T(cx + 33, cy + 60, F, 17, COMP, 'middle', 'bold')
    return o


def fig3_3():
    W, H = 900, 400
    o = ''
    for i, k in enumerate(('B', 'C', 'D')):
        o += _unit_portal(i * 300, k)
        if i:
            o += L(i * 300, 20, i * 300, 330, GRID, 1.2)
    o += R(110, 340, 680, 48, KEY2, KEY, 1.6, 9)
    o += T(450, 371, '紅字＝把這個形狀「扶住」所需的力：彎矩 ×*EI*/*L*（Δ 那格 ×*EI*/*L*^{2}）、水平力 ×*EI*/*L*^{2}（Δ 那格 ×*EI*/*L*^{3}）', 14, KEY, 'middle', 'bold')
    return svg(W, H, o, '[K] 的三行就是三次單位位移實驗')


def fig3_4():
    W, H = 900, 400
    N = {'a': (0, 0), 'b': (0, 1), 'c': (0.5, 1), 'd': (1, 1)}
    fr = Frame(N, [('a', 'b'), ('b', 'c'), ('c', 'd')], 110, 340, 250)
    o = fr.undeformed()
    o += fixed_wall(*fr.P('a'), 50) + pin(*fr.P('d'))
    phi = 0.26
    D = {'c': (0, 0.5 * phi, -phi), 'd': (0, 0, -phi)}
    o += fr.deformed({'c': D['c']}, 1.0, AC, 3.2) if False else ''
    # 只畫 ab（不動）、bc（Hermite）與剛桿 cd（直線轉動）
    sub = Frame(N, [('b', 'c')], 110, 340, 250)
    o += L(*fr.P('a'), *fr.P('b'), INK, 4)
    o += sub.deformed(D, 1.0, AC, 3.4)
    cx, cy = fr.S(0.5, 1 + 0.5 * phi); dx, dy = fr.P('d')
    o += L(cx, cy, dx, dy, '#455a64', 9)
    o += T((cx + dx) / 2 + 6, (cy + dy) / 2 - 16, '*EI*＝∞', 15, '#455a64', 'start', 'bold')
    o += arc_arrow(dx, dy, 34, 150, 95, KEY, 2.4, 10)
    o += T(dx + 14, dy - 40, '*r*_{2}（剛桿轉角）', 15, KEY, 'start', 'bold')
    o += L(cx, fr.P('c')[1], cx, cy, AC, 1.4, '3 3')
    o += T(cx - 4, fr.P('c')[1] + 60, '↑ *v*_{c}＝*r*_{2}·*L*/2', 15, AC, 'start', 'bold')
    for nm, dxy in {'a': (-34, -8), 'b': (-22, 4), 'd': (26, 30)}.items():
        x, y = fr.P(nm); o += T(x + dxy[0], y + dxy[1], nm, 17, INK, 'middle', 'bold')
    o += T(fr.P('c')[0] - 10, fr.P('c')[1] + 30, 'c', 17, INK, 'end', 'bold')
    o += T(fr.S(0.2, 1)[0], fr.S(0.2, 1)[1] + 30, '*EI*, *L*/2', 14, MUT, 'middle')
    o += T(fr.P('a')[0] - 14, fr.S(0, 0.5)[1], '*EI*, *L*', 14, MUT, 'end')
    K = rigid_bar_2012()
    k = [[int(sp.simplify(K[i, j] * L_ / EI)) for j in range(2)] for i in range(2)]
    o += R(530, 70, 350, 270, '#fff', KEY, 2, 12)
    o += T(705, 104, 'SA-2012-4：剛桿把兩件事綁在一起', 16, KEY, 'middle', 'bold')
    o += T(550, 146, 'c 跟著剛桿轉：θ_{c} ＝ *r*_{2}', 15, INK, 'start', 'bold')
    o += T(550, 180, 'c 被剛桿抬高：*v*_{c} ＝ *r*_{2} × *L*/2', 15, INK, 'start', 'bold')
    o += T(550, 214, '→ 原本 3 個未知數，只剩 1 個', 15, AC, 'start', 'bold')
    o += T(705, 262, f'[*K*] ＝ (*EI*/*L*)·[{k[0][0]}  {k[0][1]} ; {k[1][0]}  {k[1][1]}]', 17, KEY, 'middle', 'bold')
    o += T(705, 296, '（兩個轉角都以順時針為正）', 14, MUT, 'middle')
    o += T(705, 322, '數值：calcs.rigid_bar_2012()', 14, MUT, 'middle')
    return svg(W, H, o, '剛性桿的約束')


def fig3_5():
    W, H = 900, 300
    o = ''
    x0, y0, s = 180, 60, 92
    blocks = [('*K*_{ff}', 0, 0, AC2, AC), ('*K*_{fs}', 1, 0, STEEL2, MUT), ('*K*_{sf}', 0, 1, WARN2, WARN), ('*K*_{ss}', 1, 1, STEEL2, MUT)]
    for t, j, i, fill, c in blocks:
        o += R(x0 + j * s, y0 + i * s, s, s, fill, c, 1.8)
        o += T(x0 + j * s + s / 2, y0 + i * s + s / 2 + 6, t, 18, c, 'middle', 'bold')
    vx = x0 + 2 * s + 22
    o += R(vx, y0, 70, s, AC2, AC, 1.8) + T(vx + 35, y0 + s / 2 + 6, '*D*_{f}', 18, AC, 'middle', 'bold')
    o += R(vx, y0 + s, 70, s, STEEL2, MUT, 1.8) + T(vx + 35, y0 + s * 1.5 + 6, '0', 18, MUT, 'middle', 'bold')
    o += T(vx + 98, y0 + s + 6, '＝', 22, INK, 'middle', 'bold')
    ox = vx + 126
    o += R(ox, y0, 70, s, AC2, AC, 1.8) + T(ox + 35, y0 + s / 2 + 6, '*P*_{f}', 18, AC, 'middle', 'bold')
    o += R(ox, y0 + s, 70, s, WARN2, WARN, 1.8) + T(ox + 35, y0 + s * 1.5 + 6, '*R*_{s}', 18, WARN, 'middle', 'bold')
    o += T(x0 - 16, y0 + s / 2 + 6, 'f（自由）', 15, AC, 'end', 'bold')
    o += T(x0 - 16, y0 + s * 1.5 + 6, 's（支承）', 15, WARN, 'end', 'bold')
    o += T(x0 + s, y0 - 14, '先自由、後支承地排', 14, MUT, 'middle')
    o += R(590, 70, 290, 64, AC2, AC, 1.6, 9)
    o += T(735, 98, '上半：[*K*_{ff}]{*D*_{f}} ＝ {*P*_{f}}', 15, AC, 'middle', 'bold')
    o += T(735, 122, '→ 先解位移', 14, INK, 'middle')
    o += R(590, 160, 290, 64, WARN2, WARN, 1.6, 9)
    o += T(735, 188, '下半：{*R*_{s}} ＝ [*K*_{sf}]{*D*_{f}}', 15, WARN, 'middle', 'bold')
    o += T(735, 212, '→ 再乘一次就是反力', 14, INK, 'middle')
    o += T(450, 286, '支承位移為 0 → 右邊那一欄（*K*_{fs}、*K*_{ss}）乘到 0，可以整欄不寫', 14, MUT, 'middle')
    return svg(W, H, o, '分割：自由度在上、支承在下')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4, 'fig3_5': fig3_5}
