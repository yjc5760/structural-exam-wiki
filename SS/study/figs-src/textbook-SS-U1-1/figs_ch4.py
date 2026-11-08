# -*- coding: utf-8 -*-
"""第 4 章：剪力遲滯 U。"""
from plot import *  # noqa
from calcs import tension_example, ss2025_2, ss2025_2_wrong, L_opt
import math

D = tension_example()


def fig4_1():
    W, H = 900, 430
    o = T(150, 28, '(a) 斷面（依比例）', 16, INK, 'middle', 'bold')
    sc = 17
    ox, oy = 60, 80     # 連接肢的背面（貼節點板那一面）在 x=ox
    # 節點板（垂直、在左）
    o += R(ox - 14, oy - 20, 14, 10 * sc + 40, STEEL2, STEEL, 1.2)
    o += T(ox - 14, oy - 28, '節點板', 14, MUT, 'start')
    # 角鋼：連接肢（垂直，厚 1）＋外伸肢（水平，在下）
    o += P([(ox, oy), (ox + 1 * sc, oy), (ox + 1 * sc, oy + 9 * sc), (ox + 10 * sc, oy + 9 * sc), (ox + 10 * sc, oy + 10 * sc), (ox, oy + 10 * sc)],
           INK, 1.6, fill=STEEL3, close=True)
    o += C(ox + 0.5 * sc, oy + 4.5 * sc, 5, COMP, '#fff', 1.4)
    gx = ox + D['xbar'] * sc
    o += C(gx, oy + 10 * sc - D['xbar'] * sc, 5, KEY, '#fff', 1.6)
    o += T(gx + 8, oy + 10 * sc - D['xbar'] * sc - 8, '形心', 14, KEY, 'start', 'bold')
    o += dim(ox, oy + 10 * sc + 22, gx, oy + 10 * sc + 22, '', KEY)
    o += T(gx + 8, oy + 10 * sc + 28, 'x̄ = 2.82', 15, KEY, 'start', 'bold')
    o += L(gx, oy, gx, oy + 10 * sc + 22, KEY, 1, '4 3')
    o += T(ox + 5 * sc, oy + 10 * sc + 62, 'L100×100×10', 14, INK, 'middle')
    o += T(ox + 1 * sc + 6, oy + 4.5 * sc + 5, '← 螺栓', 14, COMP, 'start')
    o += L(300, 20, 300, 410, GRID, 1.5)
    # (b) 外伸肢俯視：力線擴散
    o += T(600, 28, '(b) 外伸肢俯視：力要走一段路才攤滿整肢', 16, INK, 'middle', 'bold')
    sx = 16
    x0, yc = 360, 110
    Lpx = D['Lc'] * sx            # 第一顆到最後一顆
    # 連接肢（帶螺栓）投影線
    o += R(x0, yc - 8, Lpx + 3.5 * sx + 170, 16, STEEL2, STEEL, 1)
    for i in range(3):
        o += C(x0 + 3.5 * sx + i * 7 * sx, yc, 6, '#fff', COMP, 1.6)
    o += T(x0 - 6, yc + 5, '連接肢', 14, MUT, 'end')
    # 外伸肢：寬 10 cm → 往下
    wl = 10 * 16
    o += R(x0, yc + 8, Lpx + 3.5 * sx + 170, wl, '#fafafa', INK, 1.2)
    o += T(x0 - 6, yc + 8 + wl / 2, '外伸肢', 14, MUT, 'end')
    # 力線：從螺栓區域出發，向右擴散到整個寬度
    xs = x0 + 3.5 * sx
    xe = xs + Lpx
    for k in range(1, 7):
        frac = k / 6
        ytgt = yc + 8 + wl * frac
        pts = []
        for i in range(41):
            u = i / 40
            xx = xs + (xe - xs + 150) * u
            yy = yc + 8 + (ytgt - yc - 8) * (1 - (1 - min(1, u * (1.0 + 0.6 * frac))) ** 2)
            pts.append((xx, yy))
        o += P(pts, WARN, 1.6, op=0.85)
    o += A(xe + 170, yc + 8 + wl / 2, xe + 215, yc + 8 + wl / 2, TEN, 2.6, 11)
    o += T(xe + 192, yc + wl / 2 - 6, '*T*', 16, TEN, 'middle', 'bold')
    o += dim(xs, yc - 30, xe, yc - 30, '', INK)
    o += T((xs + xe) / 2, yc - 38, '接合長度 *L* = 2 × 7 = 14', 15, INK, 'middle', 'bold')
    o += R(xs, yc + 8, (xe - xs), wl * 0.62, COMP2, None, 0, op=0.55)
    o += T(xs + 12, yc + 8 + wl * 0.62 - 10, '力還沒到的地方', 14, COMP, 'start', 'bold')
    o += R(330, 330, 560, 80, KEY2, KEY, 1.4, 8)
    o += T(610, 356, '力線要往旁邊移 x̄、只有 *L* 的距離可以移', 15, KEY, 'middle', 'bold')
    o += T(610, 382, '「坡度」＝ x̄ / *L* = 2.82 / 14 = 0.20 → 有效比例 *U* = 1 − 0.20 = 0.80', 15, INK, 'middle')
    return svg(W, H, o, '剪力遲滯幾何')


def fig4_2():
    W, H = 900, 400
    pl = Plot(100, 50, 600, 280, 0, 12, 0, 1.05)
    o = pl.axes([0, 1, 2, 3, 4, 5, 6, 8, 10, 12], [0, 0.25, 0.5, 0.8, 1.0], '*L* / x̄', '*U*')
    o += pl.curve(lambda r: max(0, 1 - 1 / r) if r > 0 else 0, 1.0, 12, WARN, 3.4)
    o += pl.hline(1.0, 0, 12, MUT, 1.3, '5 4')
    o += T(pl.X(12) - 4, pl.Y(1.0) - 8, '*U* → 1（接合無限長）', 15, MUT, 'end')
    r = D['Lc'] / D['xbar']
    o += pl.dot(r, D['U'], KEY, 6)
    o += T(pl.X(r) + 10, pl.Y(D['U']) + 22, f'本例 *L*/x̄ = {r:.2f} → *U* = {D["U"]:.2f}', 15, KEY, 'start', 'bold')
    o += pl.dot(2, 0.5, WARN, 5) + T(pl.X(2) + 10, pl.Y(0.5) + 18, '*L* = 2x̄ → *U* = 0.5', 14, WARN, 'start', 'bold')
    o += T(pl.X(0.15), pl.Y(0.15), '*L* ≤ x̄：公式失去意義', 14, MUT, 'start')
    o += R(715, 120, 175, 110, '#fff', KEY, 1.4, 8)
    o += T(802, 146, '曲線＝ 1 − 1/(*L*/x̄)', 14, KEY, 'middle', 'bold')
    o += T(802, 172, '接合加長一倍', 14, INK, 'middle')
    o += T(802, 194, '「沒出力」的比例', 14, INK, 'middle')
    o += T(802, 216, '就減半', 14, INK, 'middle')
    return svg(W, H, o, 'U 與 L/x̄')


def fig4_3():
    W, H = 900, 430
    pl = Plot(100, 50, 520, 300, 0, 4, 0, 10)
    o = pl.axes([0, 1, 1.5, 2, 3, 4], [0, 2, 4, 6, 8, 9, 10], '板寬 *L*（cm）', '容許拉力 *P*（tf）')
    o += R(pl.X(3), pl.y0, pl.X(4) - pl.X(3), pl.h, '#eceff1', None, 0, op=0.9)
    o += T((pl.X(3) + pl.X(4)) / 2, pl.Y(5), '*l* < *w*', 15, MUT, 'middle', 'bold')
    o += T((pl.X(3) + pl.X(4)) / 2, pl.Y(5) + 22, '規範不允許', 14, MUT, 'middle')
    # U 階梯標示
    for a, b, u in ((0, 1.5, '1.00'), (1.5, 2, '0.87'), (2, 3, '0.75')):
        o += T((pl.X(a) + pl.X(b)) / 2, pl.Y(9.6), f'*U*={u}', 14, WARN, 'middle', 'bold')
        o += pl.vline(b, 0, 10, WARN, 1, '3 4')
    # NSF 分段
    for a, b in ((0, 1.5), (1.5, 2), (2, 3)):
        o += P([pl.pt(x, ss2025_2(x)['Pnsf']) for x in (a + 1e-6, b)], COMP, 2.6, dash='7 4')
    o += T(pl.X(0.08), pl.Y(8.3), '*P*_{NSF} = 0.5*F*_{u}·*U*·2*L*（紅虛線）', 14.5, COMP, 'start', 'bold')
    o += P([pl.pt(0, 0), pl.pt(3, 9)], TEN, 3.4)
    o += T(pl.X(1.45), pl.Y(1.6), '*P*_{GY} = 0.6*F*_{y}·2*L* = 3.0*L*', 14.5, TEN, 'start', 'bold')
    o += pl.dot(3, 9, KEY, 7)
    o += T(pl.X(3) + 12, pl.Y(9) + 5, '(3, 9.00)', 15, KEY, 'start', 'bold')
    o += pl.curve(ss2025_2_wrong, 0.01, 3, MUT, 2.4, dash='3 4')
    o += T(pl.X(2.98), pl.Y(6.15) + 24, '錯解 6.15', 14, MUT, 'end', 'bold')
    o += R(640, 60, 250, 250, '#fff', KEY, 1.4, 8)
    lines = [('SS-2025-2（ASD）', KEY, True), ('板厚 2 cm、兩側縱向銲', INK, False), ('銲長 *l* = 3 cm 固定', INK, False),
             ('① *U* 查 *l*/*w* 階梯', INK, False), ('② 規範要求 *l* ≥ *w*', INK, False), ('　→ *L* ≤ 3 cm', INK, False),
             ('③ 每段都 GY 控制', INK, False), ('→ *L*_{max} = 3 cm', KEY, True), ('→ *P*_{max} = 9.00 tf', KEY, True)]
    for i, (s, c, b) in enumerate(lines):
        o += T(655, 86 + i * 25, s, 14.5, c, 'start', 'bold' if b else None)
    o += T(450, 420, '灰虛線：把 x̄ 取成板寬一半硬套 *U* = 1 − x̄/*l*，最大值只有 6.15 tf（低估 32%）', 14, MUT, 'middle')
    return svg(W, H, o, 'SS-2025-2')


def fig4_4():
    W, H = 900, 410
    Ag, Fy, Fu, xb = D['Ag'], D['Fy'], D['Fu'], D['xbar']
    pl = Plot(100, 50, 560, 290, 3, 25, 0, 55)
    o = pl.axes([3, 5, 10, 15, 20, 25], [0, 10, 20, 30, 40, 43.1, 50], '銲道長度 *L*（cm）', 'φ*P*_{n}（tf）')
    g = 0.9 * Fy * Ag
    o += pl.hline(g, 3, 25, TEN, 3.4, None)
    o += T(pl.X(24.5), pl.Y(g) - 10, f'GSY 0.9*F*_{{y}}*A*_{{g}} = {g:.1f}（與 *L* 無關）', 14.5, TEN, 'end', 'bold')
    o += pl.curve(lambda L: 0.75 * Fu * (1 - xb / L) * Ag, 3, 25, COMP, 3.4)
    o += T(pl.X(12.5), pl.Y(37), 'NSF 0.75*F*_{u}(1 − x̄/*L*)*A*_{g}', 14.5, COMP, 'start', 'bold')
    Lo = L_opt(xb, Fy, Fu)
    o += pl.dot(Lo, g, KEY, 7)
    o += pl.vline(Lo, 0, g, KEY, 1.4, '4 4')
    o += T(pl.X(Lo), pl.Y(0) + 40, f'*L*_{{opt}} = {Lo:.1f}', 15, KEY, 'middle', 'bold')
    o += T(pl.X(4.5), pl.Y(14), '太短：NSF 控制', 14.5, COMP, 'start', 'bold')
    o += T(pl.X(4.5), pl.Y(14) + 20, '斷面浪費', 14.5, COMP, 'start')
    o += T(pl.X(18), pl.Y(26), '再長也沒用：', 14.5, TEN, 'start', 'bold')
    o += T(pl.X(18), pl.Y(26) + 20, '被 GSY 卡住', 14.5, TEN, 'start')
    o += R(680, 130, 210, 150, KEY2, KEY, 1.4, 8)
    o += T(785, 154, '令兩者相等：', 14.5, KEY, 'middle', 'bold')
    o += T(785, 180, '0.75*F*_{u}(1 − x̄/*L*) = 0.9*F*_{y}', 14, KEY, 'middle')
    o += T(785, 208, '*L* = x̄ / (1 − 1.2*F*_{y}/*F*_{u})', 14.5, KEY, 'middle', 'bold')
    o += T(785, 236, f'= 2.82/(1 − 0.738) = {Lo:.1f}', 14, INK, 'middle')
    o += T(785, 262, 'ASD 也相同（同除 1.5）', 14, INK, 'middle')
    return svg(W, H, o, '最經濟銲道長度')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}
