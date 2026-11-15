# -*- coding: utf-8 -*-
"""第 2 章：剪力建築。位移、層剪力全部 import calcs。"""
from figs_common import *  # noqa
from calcs import ex2020, ex2022, ex2023, K20_story, k22, k22_tall

r23 = ex2023()
r22 = ex2022()
r20 = ex2020()


def fig2_1():
    W, H = 900, 480
    o = ''
    yb = 410
    hs = 100
    # (a) 一般構架：每個節點有轉角
    o += T(225, 34, '(a) 梁有彈性：節點會轉', 16, INK, 'middle', 'bold')
    xl, xr = 110, 320
    for i in range(3):
        y1, y2 = yb - i * hs, yb - (i + 1) * hs
        o += L(xl, y1, xl, y2, INK, 3) + L(xr, y1, xr, y2, INK, 3)
        o += L(xl, y2, xr, y2, INK, 3)
    o += base_fixed(xl, yb + 2, 46) + base_fixed(xr, yb + 2, 46)
    for i in range(1, 4):
        y = yb - i * hs
        for x in (xl, xr):
            o += node(x, y, 5)
            o += arc_arrow(x, y, 17, -60, 200, WARN, 2, 8)
        o += T(xl - 26, y - 14, 'θ', 15, WARN, 'end', 'bold')
        o += A(xr + 34, y, xr + 78, y, AC, 2.6, 11)
        o += T(xr + 84, y + 5, f'*u*_{{{i}}}', 16, AC, 'start', 'bold')
    o += R(40, 432, 370, 38, WARN2, WARN, 1.4, 8)
    o += T(225, 457, '自由度：3 個 *u* ＋ 6 個 θ ＝ 9', 15, INK, 'middle', 'bold')
    # (b) 剪力建築：梁 I＝∞
    o += T(675, 34, '(b) 梁 *I* = ∞：節點不轉', 16, INK, 'middle', 'bold')
    xl, xr = 530, 710
    D = r23['D']                       # 一、二、三層層間位移（9:7:4）
    disp = [0.0, D[0], D[0] + D[1], D.sum()]
    sc = 55 / D.sum()
    for i in range(3):
        y1, y2 = yb - i * hs, yb - (i + 1) * hs
        for x in (xl, xr):
            o += L(x, yb, x, yb - 3 * hs, STEEL, 1.6, '6 5') if i == 0 else ''
            o += col_ff(x, y1, y2, disp[i] * sc, disp[i + 1] * sc, AC, 3)
        o += rigid_beam(xl - 6 + disp[i + 1] * sc, xr + 6 + disp[i + 1] * sc, y2, INK, 10)
        o += A(xr + 36 + disp[i + 1] * sc, y2, xr + 80 + disp[i + 1] * sc, y2, AC, 2.6, 11)
        o += T(xr + 86 + disp[i + 1] * sc, y2 + 5, f'*u*_{{{i + 1}}}', 16, AC, 'start', 'bold')
        o += lock(xl + disp[i + 1] * sc - 22, y2 + 22, WARN, 10)
    o += base_fixed(xl, yb + 2, 46) + base_fixed(xr, yb + 2, 46)
    o += R(490, 432, 370, 38, AC2, AC, 1.4, 8)
    o += T(675, 457, '自由度：只剩 3 個 *u*（每層一個）', 15, INK, 'middle', 'bold')
    o += L(450, 50, 450, 470, GRID, 1.4)
    return svg(W, H, o, '一般構架與剪力建築的自由度')


def fig2_2():
    W, H = 900, 500
    o = ''
    F = [600, 900, 1200]
    V = r23['V']
    yb, hs = 430, 110
    # 左：整棟，切面在第 2 層
    xl, xr = 90, 230
    o += T(165, 34, '(a) 在第 2 層水平切一刀', 16, INK, 'middle', 'bold')
    for i in range(3):
        y1, y2 = yb - i * hs, yb - (i + 1) * hs
        o += L(xl, y1, xl, y2, INK, 3) + L(xr, y1, xr, y2, INK, 3)
        o += rigid_beam(xl - 6, xr + 6, y2, INK, 9)
        o += A(xl - 70, y2, xl - 10, y2, COMP, 3, 12)
        o += T(xl - 74, y2 - 10, f'{F[i]:.0f}', 15, COMP, 'start', 'bold')
    o += base_fixed(xl, yb + 2, 46) + base_fixed(xr, yb + 2, 46)
    yc = yb - 1.5 * hs
    o += L(30, yc, 290, yc, COMP, 2.2, '8 5')
    # 中：切面以上的自由體
    o += T(440, 34, '(b) 切面以上的自由體', 16, INK, 'middle', 'bold')
    xl2, xr2 = 380, 520
    top = yb - 3 * hs
    for i in (1, 2):
        y2 = yb - (i + 1) * hs
        o += A(xl2 - 70, y2, xl2 - 10, y2, COMP, 3, 12)
        o += T(xl2 - 74, y2 - 10, f'{F[i]:.0f}', 15, COMP, 'start', 'bold')
        o += rigid_beam(xl2 - 6, xr2 + 6, y2, INK, 9)
    for x in (xl2, xr2):
        o += L(x, top, x, yc, INK, 3)
        o += A(x + 34, yc + 2, x - 2, yc + 2, TEN, 3, 12)
    o += T((xl2 + xr2) / 2, yc + 34, '柱剪力合計 = 900 + 1200 = 2100 kN', 15, TEN, 'middle', 'bold')
    o += T((xl2 + xr2) / 2, yc + 60, '（向左，擋住上面的外力）', 14, MUT, 'middle')
    o += R(318, 380, 250, 66, KEY2, KEY, 1.6, 10)
    o += T(443, 406, 'Σ*F*_{x} = 0：', 15, KEY, 'middle', 'bold')
    o += T(443, 432, '*V*_{2} = *F*_{2} + *F*_{3}', 16, KEY, 'middle', 'bold')
    # 右：層剪力圖
    px, pw = 640, 230
    o += T(745, 34, '(c) 層剪力：由上往下累加', 16, INK, 'middle', 'bold')
    sc = pw / 2800
    for i in range(3):
        y1, y2 = yb - i * hs, yb - (i + 1) * hs
        o += R(px, y2 + 8, V[i] * sc, hs - 16, COMP2, COMP, 1.6, 4)
        o += T(px + V[i] * sc - 8, (y1 + y2) / 2 + 6, f'*V*_{{{i + 1}}} = {V[i]:.0f}', 15, COMP, 'end', 'bold')
        o += L(px - 6, y2, px + 6, y2, INK, 1.4)
    o += L(px, yb, px, yb - 3 * hs - 10, INK, 1.8)
    o += hatch_ground(px - 30, yb, 60)
    o += T(745, yb + 44, '比例 9 : 7 : 4（一、二、三層）', 15, KEY, 'middle', 'bold')
    o += L(300, 50, 300, 490, GRID, 1.2) + L(590, 50, 590, 490, GRID, 1.2)
    return svg(W, H, o, '水平切一刀求層剪力')


def fig2_3():
    W, H = 900, 560
    o = ''
    # (a) 同一層：並聯
    o += T(200, 34, '(a) 同一層的柱：並聯', 16, INK, 'middle', 'bold')
    wx, bx = 60, 300
    o += vwall_line(wx, 150, 160)
    o += R(bx, 80, 22, 140, '#fff', INK, 2.4, 3)
    for j, y in enumerate((100, 150, 200)):
        o += spring(wx, y, bx, TEN)
        o += T((wx + bx) / 2, y - 14, f'*k*_{{{j + 1}}}', 15, TEN, 'middle', 'bold')
    o += A(bx + 30, 150, bx + 70, 150, COMP, 3, 12)
    o += T(bx + 50, 136, '*V*', 16, COMP, 'middle', 'bold')
    o += T(200, 250, '樓板剛性 → 每根柱的 Δ 都一樣', 15, MUT, 'middle')
    o += R(80, 266, 240, 40, KEY2, KEY, 1.5, 8)
    o += T(200, 292, '*K* = *k*_{1} + *k*_{2} + *k*_{3}', 16, KEY, 'middle', 'bold')
    # (b) 上下層：串聯
    o += T(660, 34, '(b) 上下層：串聯', 16, INK, 'middle', 'bold')
    xs = [460, 560, 660, 760]
    o += vwall_line(xs[0] - 10, 140, 70)
    for i in range(3):
        o += spring(xs[i] - 10 if i == 0 else xs[i] + 14, 140, xs[i + 1] - 14, TEN)
        o += T((xs[i] + xs[i + 1]) / 2, 120, f'*K*_{{{i + 1}}}', 15, TEN, 'middle', 'bold')
        o += roller_block(xs[i + 1], 140, 28, 26)
        o += T((xs[i] + xs[i + 1]) / 2, 182, f'*V*_{{{i + 1}}}', 15, COMP, 'middle', 'bold')
    o += T(660, 214, '每支彈簧的力＝該層層剪力', 15, MUT, 'middle')
    o += R(500, 230, 330, 76, KEY2, KEY, 1.5, 8)
    o += T(665, 258, 'Δ_{*i*} = *V*_{*i*} / *K*_{*i*}', 16, KEY, 'middle', 'bold')
    o += T(665, 288, 'Δ_{頂} = Δ_{1} + Δ_{2} + Δ_{3}', 16, KEY, 'middle', 'bold')
    o += L(20, 326, 880, 326, GRID, 1.4)
    # (c) SA-2023-4：層間位移依層剪力分配
    D = r23['D'] * 100
    De = r23['D_even'] * 100
    o += T(450, 360, '(c) SA-2023-4：各層 *K* 相同，頂層 6 cm 依層剪力 9 : 7 : 4 分給三層', 16, INK, 'middle', 'bold')
    bx0, sc = 200, 95
    for i in range(3):
        y = 384 + i * 52
        o += T(bx0 - 14, y + 26, f'第 {i + 1} 層', 15, INK, 'end', 'bold')
        o += R(bx0, y + 6, D[i] * sc, 24, AC, None, 0, 4)
        o += T(bx0 + D[i] * sc + 8, y + 25, f'{D[i]:.1f} cm', 15, AC, 'start', 'bold')
        o += R(560, y + 6, De[i] * sc, 24, STEEL3, None, 0, 4)
        o += T(560 + De[i] * sc + 8, y + 25, f'{De[i]:.1f} cm', 15, MUT, 'start')
    o += T(bx0 + 120, 548, '正解：依 *V*_{*i*} 比例', 15, AC, 'middle', 'bold')
    o += T(660, 548, '錯解：平均分', 15, MUT, 'middle', 'bold')
    return svg(W, H, o, '並聯、串聯與層間位移分配')


def vwall_line(x, y, h, c=INK):
    """垂直固定牆（斜線在左）。"""
    o = L(x, y - h / 2, x, y + h / 2, c, 3)
    n = max(4, int(h / 9))
    for i in range(n + 1):
        yy = y - h / 2 + h * i / n
        o += L(x, yy, x - 8, yy + 7, c, 1)
    return o


def _two_story(x0, push, title):
    """2020-4 二層構架；push=1 推頂層、2 推一樓（另一層鎖住）。"""
    o = ''
    yb, hs, bw = 420, 130, 150
    xl, xr = x0, x0 + bw
    d = 40
    u_top = d if push == 1 else 0
    u_1 = d if push == 2 else 0
    o += T(x0 + bw / 2 + 40, 34, title, 16, INK, 'middle', 'bold')
    y1, y2 = yb - hs, yb - 2 * hs
    for x in (xl, xr):
        o += L(x, yb, x, y2, STEEL, 1.6, '6 5')
        o += col_ff(x, yb, y1, 0, u_1, AC, 3)
        o += col_ff(x, y1, y2, u_1, u_top, AC, 3)
    o += rigid_beam(xl - 6 + u_1, xr + 6 + u_1, y1, INK, 10)
    o += rigid_beam(xl - 6 + u_top, xr + 6 + u_top, y2, INK, 10)
    o += base_fixed(xl, yb + 2, 46) + base_fixed(xr, yb + 2, 46)
    K = K20_story
    if push == 1:
        o += A(xr + 30 + u_top, y2, xr + 80 + u_top, y2, COMP, 3, 12)
        o += T(xr + 30 + u_top, y2 - 16, f'+*K*_{{2}} = {K:.0f}', 15, COMP, 'start', 'bold')
        o += A(xr + 80, y1, xr + 30, y1, COMP, 3, 12)
        o += T(xr + 30, y1 - 16, f'−*K*_{{2}} = −{K:.0f}', 15, COMP, 'start', 'bold')
        o += lock(xl - 26, y1 + 2)
        o += dim(xl, y2 - 30, xl + u_top, y2 - 30, '1', AC, size=15, lab_off=-12)
    else:
        o += A(xr + 30 + u_1, y1, xr + 80 + u_1, y1, COMP, 3, 12)
        o += T(xr + 30 + u_1, y1 - 16, f'*K*_{{1}} + *K*_{{2}} = {2 * K:.0f}', 15, COMP, 'start', 'bold')
        o += A(xr + 80, y2, xr + 30, y2, COMP, 3, 12)
        o += T(xr + 30, y2 - 16, f'−*K*_{{2}} = −{K:.0f}', 15, COMP, 'start', 'bold')
        o += lock(xl - 26, y2 + 2)
        o += dim(xl, y1 + 30, xl + u_1, y1 + 30, '1', AC, size=15, lab_off=12)
    o += T(xl - 50, y2 + 5, '頂', 15, MUT, 'end')
    o += T(xl - 50, y1 + 5, '一樓', 15, MUT, 'end')
    return o


def fig2_4():
    W, H = 900, 560
    o = _two_story(110, 1, '(a) 只推頂層 1，一樓鎖住')
    o += _two_story(560, 2, '(b) 只推一樓 1，頂層鎖住')
    o += L(450, 50, 450, 450, GRID, 1.4)
    o += R(170, 470, 560, 78, KEY2, KEY, 1.6, 10)
    o += T(450, 498, '(a) 寫成第 1 行、(b) 寫成第 2 行（自由度順序：頂層、一樓）', 15, KEY, 'middle', 'bold')
    o += T(450, 530, '[*K*_{f}] = 30000 [ 2  −2 ; −2  4 ] kN/m', 17, KEY, 'middle', 'bold')
    return svg(W, H, o, '推一下量力，組出剪力建築勁度矩陣')


def fig2_5():
    W, H = 900, 560
    o = ''
    D = r22['D']
    yb, hs = 450, 100
    s4 = 95                                  # 4 m 的像素
    lv = [yb - i * hs for i in range(4)]

    def frame(x0, disp, sc, deformed):
        o = ''
        xs = [x0 + i * s4 for i in range(4)]
        u = [0.0] + [d * sc for d in disp] if deformed else [0.0] * 4
        # 柱
        for j, x in enumerate(xs):
            if j < 2:
                o += col_ff(x, lv[0], lv[1], u[0], u[1], AC if deformed else INK, 3)
                o += col_ff(x, lv[1], lv[2], u[1], u[2], AC if deformed else INK, 3)
            else:
                o += col_ff(x, lv[0], lv[2], u[0], u[2], WARN if deformed else WARN, 3.4)
            o += col_ff(x, lv[2], lv[3], u[2], u[3], AC if deformed else INK, 3)
            o += base_fixed(x, yb + 2, 40)
        o += rigid_beam(xs[0] - 6 + u[1], xs[1] + 6 + u[1], lv[1], INK, 9)
        o += rigid_beam(xs[0] - 6 + u[2], xs[3] + 6 + u[2], lv[2], INK, 9)
        o += rigid_beam(xs[0] - 6 + u[3], xs[3] + 6 + u[3], lv[3], INK, 9)
        return o, xs, u

    # (a) 幾何、載重、切面
    x0 = 120
    o += T(260, 34, '(a) 題目：m、n 是 7.2 m 的挑高柱', 16, INK, 'middle', 'bold')
    fr, xs, _ = frame(x0, D, 0, False)
    o += fr
    for i, (F, nm) in enumerate(((100, 'b'), (200, 'c'), (300, 'd'))):
        y = lv[i + 1]
        o += A(x0 - 82, y, x0 - 10, y, COMP, 3, 12)
        o += T(x0 - 86, y - 10, f'{F}', 15, COMP, 'start', 'bold')
        o += T(x0 + 10, y - 12, nm, 15, INK, 'start', 'bold')
    for j, nm in enumerate('aemn'):
        o += T(xs[j], yb + 30, nm, 15, INK, 'middle', 'bold')
    for k, (ys, txt) in enumerate(((yb - 0.5 * hs, '切①：切到 a、e、m、n'), (yb - 1.5 * hs, '切②：切到 2 根標準柱＋m、n'))):
        o += L(x0 - 30, ys, xs[3] + 26, ys, COMP, 1.8, '7 5')
        o += T(xs[3] + 30, ys + 5, '①' if k == 0 else '②', 16, COMP, 'start', 'bold')
    o += T(260, yb + 62, 'm、n 柱跨兩層：切①、切② 都會切到它', 15, WARN, 'middle', 'bold')
    # (b) 變形
    x1 = 530
    sc = 2.4 / 0.001                          # 每 mm 2.4 px
    o += T(705, 34, '(b) 解出的側移（放大示意）', 16, INK, 'middle', 'bold')
    for j in range(4):
        o += L(x1 + j * s4, yb, x1 + j * s4, lv[3], STEEL, 1.2, '5 5')
    fr, xs2, u = frame(x1, D, sc, True)
    o += fr
    for i in range(3):
        o += T((xs2[1] + xs2[2]) / 2 + u[i + 1], lv[i + 1] - 14, f'{D[i] * 1000:.1f} mm', 15, AC, 'middle', 'bold')
    o += T(xs2[0], yb + 30, f'a：{r22["Ha"]:.0f} kN、{r22["Ma"]:.0f} kN-m', 14, COMP, 'start', 'bold')
    o += T(xs2[2] - 20, yb + 52, f'm：{r22["Hm"]:.0f} kN、{r22["Mm"]:.0f} kN-m', 14, WARN, 'start', 'bold')
    o += T(705, yb + 80, f'平衡：2 × {r22["Ha"]:.0f} + 2 × {r22["Hm"]:.0f} = {r22["base_sum"]:.0f} kN', 15, KEY, 'middle', 'bold')
    o += L(470, 50, 470, 550, GRID, 1.4)
    return svg(W, H, o, 'SA-2022-4 挑高柱剪力建築')


import numpy as np  # noqa: E402

ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5}
