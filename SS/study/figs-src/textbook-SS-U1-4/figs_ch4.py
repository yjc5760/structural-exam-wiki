# -*- coding: utf-8 -*-
"""第 4 章：摩阻型 vs 承壓型（S7）。"""
from plot import *  # noqa
from calcs import slip_M20

S = slip_M20()


def fig4_1():
    W, H = 900, 380
    o = ''
    for k, (title, slip) in enumerate([('(a) 摩阻型：鎖緊 → 夾緊力 → 摩擦', False), ('(b) 承壓型：滑了才頂到孔壁', True)]):
        ox = 30 + k * 450
        o += T(ox + 200, 28, title, 16, INK, 'middle', 'bold')
        y0 = 90
        sh = 22 if slip else 0
        o += R(ox + 20, y0, 300, 34, STEEL2, INK, 1.4)                   # 上板
        o += R(ox + 80, y0 + 34, 300, 34, STEEL3, INK, 1.4)              # 下板
        bx = ox + 200
        # 孔（上下板孔位置差 sh）
        o += R(bx - 18, y0, 36, 34, '#fff', INK, 1)
        o += R(bx - 18 + sh, y0 + 34, 36, 34, '#fff', INK, 1)
        o += R(bx - 12 + sh * 0.5, y0 - 24, 24, 116, ACM, AC, 1.6, 3)   # 螺桿
        o += R(bx - 26 + sh * 0.5, y0 - 34, 52, 12, AC, None) + R(bx - 26 + sh * 0.5, y0 + 90, 52, 12, AC, None)
        o += A(ox + 30, y0 + 17, ox - 10, y0 + 17, TEN, 3, 11) + A(ox + 370, y0 + 51, ox + 410, y0 + 51, TEN, 3, 11)
        if not slip:
            for xx in (ox + 110, ox + 150, ox + 250, ox + 290):
                o += A(xx + 16, y0 + 34, xx - 16, y0 + 34, COMP, 2.2, 8)
            o += T(ox + 200, y0 + 150, '接觸面摩擦 = μ × *T*_{b}', 16, COMP, 'middle', 'bold')
            o += T(ox + 200, y0 + 178, '螺桿只受拉，不受剪；孔壁不承壓', 15, INK, 'middle')
            o += A(bx + 34, y0 - 28, bx + 34, y0 - 6, KEY, 2.2, 8) + A(bx + 34, y0 + 96, bx + 34, y0 + 74, KEY, 2.2, 8)
            o += T(bx + 44, y0 - 20, '夾緊 *T*_{b}', 15, KEY, 'start', 'bold')
        else:
            o += L(bx - 40, y0 + 34, bx + 40, y0 + 34, COMP, 2.6, '6 4')
            o += T(ox + 200, y0 + 150, '螺桿被剪（剪力面）、孔壁被壓', 16, COMP, 'middle', 'bold')
            o += T(ox + 200, y0 + 178, '孔比螺桿大約 2 mm：要先滑過這段間隙', 15, INK, 'middle')
    o += R(60, 300, 780, 64, KEY2, KEY, 1.4, 10)
    o += T(450, 326, '同一顆高強度螺栓：鎖緊時是摩阻型（靠夾緊力），滑動之後就變成承壓型（靠螺桿與孔壁）', 15, INK, 'middle')
    o += T(450, 352, '摩阻型的「極限」是滑動——不是破壞；所以 φ = 1.0', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '摩阻型與承壓型的傳力機制')


def fig4_2():
    W, H = 900, 430
    pl = Plot(110, 50, 560, 300, 0, 6, 0, 1.25)
    o = pl.axes([0, 1, 2, 3, 4, 5, 6], [0, 0.5, 1.0], '變位（mm）', '力 ÷ 強度', size=14)
    o += pl.curve(lambda x: min(1.2, 0.6 * x), 0, 2, COMP, 3.2)
    o += T(pl.X(1.0) - 6, pl.Y(0.95), '銲道', 16, COMP, 'end', 'bold')

    def slipc(x):
        if x < 0.25:
            return 0.5 * x / 0.25
        if x < 2.2:
            return 0.5 + 0.01 * (x - 0.25)
        return min(1.0, 0.52 + 0.35 * (x - 2.2))
    o += pl.curve(slipc, 0, 6, AC, 3.2, n=600)
    o += T(pl.X(1.2), pl.Y(0.52) - 10, '摩阻型：先不動，滑動後平台', 15, AC, 'middle', 'bold')

    def bear(x):
        if x < 2.0:
            return 0.03 * x
        return min(1.0, 0.06 + 0.32 * (x - 2.0))
    o += pl.curve(bear, 0, 6, WARN, 3.2, dash='8 5', n=600)
    o += T(pl.X(4.2), pl.Y(0.55), '承壓型：先滑過孔隙', 15, WARN, 'start', 'bold')
    o += T(pl.X(4.2), pl.Y(0.55) + 22, '才開始出力', 15, WARN, 'start', 'bold')
    o += pl.vline(0.25, 0, 1.25, KEY, 1.6, '4 4')
    o += T(pl.X(0.25) + 6, pl.Y(1.18), '使用載重的變位量級', 14, KEY, 'start', 'bold')
    o += R(690, 80, 200, 200, '#fff', KEY, 1.6, 10)
    o += T(790, 106, '能不能一起出力？', 15, KEY, 'middle', 'bold')
    for i, s in enumerate(['看同一個小變位下', '兩條曲線都已上升：', '銲道＋摩阻型 → 可以', '銲道＋承壓型 → 不行', '（銲道先吃滿載重）']):
        o += T(790, 136 + i * 26, s, 14, INK if i < 2 or i == 4 else (TEN if i == 2 else COMP), 'middle', 'bold' if i in (2, 3) else None)
    o += T(450, 410, '示意曲線：只表達「誰先出力」的順序，不是試驗數據', 14, MUT, 'middle')
    return svg(W, H, o, '荷重–滑動曲線（示意）')


def fig4_3():
    W, H = 900, 300
    pl = Plot(250, 50, 500, 180, 0, 11, 0, 3)
    o = T(450, 26, '同一顆 M20 A325、單剪：三種算法的設計強度（tf/顆）', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 2, 4, 6, 8, 10], [], 'tf', '', size=14)
    items = [('摩阻型 1.13μ*T*_{b}', S['Rstr'], AC), ('承壓型 N 0.75*F*_{nv}*A*_{b}', S['bear_N'], WARN), ('承壓型 X', S['bear_X'], WARN)]
    for i, (nm, v, c) in enumerate(items):
        yc = pl.Y(2.5 - i)
        o += R(pl.X(0), yc - 17, pl.X(v) - pl.X(0), 34, '#fff', c, 2, 3)
        o += T(pl.X(0) - 10, yc + 5, nm, 15, INK, 'end', 'bold')
        o += T(pl.X(v) + 8, yc + 5, f'{v:.2f}', 15, c, 'start', 'bold')
    o += T(450, 284, f'摩阻型每顆只有承壓型 N 的 {S["slip_over_N"]*100:.0f}%：買的是「不滑」，不是更強', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '每顆螺栓強度比較')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
