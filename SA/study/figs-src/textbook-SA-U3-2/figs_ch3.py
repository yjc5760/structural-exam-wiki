# -*- coding: utf-8 -*-
"""第 3 章：牆–構架互制。形狀與力分布全部 import calcs（SA-2018-1 示意模型、SA-2020-4）。"""
from figs_common import *  # noqa
import numpy as np
from calcs import ex2018, ex2020, ex2020_more, wall_flex, N18, k20, EI20, h20

r18 = ex2018()
r20 = ex2020()
r20m = ex2020_more()
WALL = BROWN
WALL2 = '#efebe9'
EI18 = 5 / 12


def _wall_curve(F, EI, n=N18, m=160):
    """懸臂牆在樓層力 F（第 1..n 層）作用下的連續撓度 w(z)，z 以層高為單位。"""
    def w(z):
        s = 0.0
        for b, Fb in enumerate(F, start=1):
            a, bb = min(z, b), max(z, b)
            s += Fb * (a ** 2 * (3 * bb - a) if z <= b else b ** 2 * (3 * z - b)) / (6 * EI)
        return s
    return [(z, w(z)) for z in np.linspace(0, n, m + 1)]


def fig3_1():
    W, H = 900, 580
    o = ''
    uf = np.concatenate([[0], r18['u_f'] / r18['u_f'][-1]])
    wa = _wall_curve(np.ones(N18), EI18)
    wa = [(z, v / wa[-1][1]) for z, v in wa]
    wc = _wall_curve(r18['Fw'], EI18)
    wc = [(z, v / wc[-1][1]) for z, v in wc]
    zs = np.arange(N18 + 1)

    def panel(px, title, show_comb):
        p = Plot(px, 80, 300, 360, 0, 1.0, 0, 8)
        s = T(px + 150, 36, title, 16, INK, 'middle', 'bold')
        s += p.axes([0, 0.5, 1.0], [0, 2, 4, 6, 8], '*u*/*u*_{頂}', '樓層', size=14)
        op = 0.35 if show_comb else None
        s += P([p.pt(u, z) for u, z in zip(uf, zs)], TEN, 3, op=op)
        s += P([p.pt(v, z) for z, v in wa], WALL, 3, op=op)
        for u, z in zip(uf[1:], zs[1:]):
            s += C(p.X(u), p.Y(z), 4, TEN, None) if not show_comb else ''
        if show_comb:
            uc = np.concatenate([[0], r18['u'] / r18['u'][-1]])
            s += P([p.pt(v, z) for z, v in wc], KEY, 3.4)
            for u, z in zip(uc[1:], zs[1:]):
                s += C(p.X(u), p.Y(z), 4.5, KEY, None)
        return s, p

    s, p = panel(70, '(a) 各自單獨受力：長相不同', False)
    o += s
    o += T(p.X(0.56), p.Y(1.5), '構架（剪力型）', 15, TEN, 'start', 'bold')
    o += T(p.X(0.56), p.Y(1.5) + 20, '底部走最快', 14, TEN, 'start')
    o += T(p.X(0.50), p.Y(6.4), '剪力牆（撓曲型）', 15, WALL, 'end', 'bold')
    o += T(p.X(0.50), p.Y(6.4) + 20, '頂部走最快', 14, WALL, 'end')
    s, p = panel(530, '(b) 用連桿綁在一起：被迫同一條線', True)
    o += s
    o += T(p.X(0.55), p.Y(4.3), '合體（紫）', 15, KEY, 'start', 'bold')
    # 下部：構架被拉回；上部：牆被拉回
    yb1 = p.Y(1.0)
    o += A(p.X(uf[1]) + 4, yb1 + 22, p.X(r18['u'][0] / r18['u'][-1]) + 2, yb1 + 22, COMP, 2.4, 10)
    o += T(p.X(uf[1]) + 10, yb1 + 28, '下部：構架被牆拉回', 14, COMP, 'start', 'bold')
    o += R(548, 486, 300, 74, KEY2, KEY, 1.4, 8)
    o += T(698, 512, '形狀介於兩者之間：', 15, KEY, 'middle', 'bold')
    o += T(698, 538, '下段像牆、上段像構架', 15, KEY, 'middle', 'bold')
    o += R(84, 486, 300, 74, WARN2, WARN, 1.4, 8)
    o += T(234, 512, '兩條線都以頂層位移 = 1 畫', 15, INK, 'middle', 'bold')
    o += T(234, 538, '比的是「長相」，不是大小', 15, INK, 'middle')
    o += L(465, 50, 465, 570, GRID, 1.4)
    return svg(W, H, o, '剪力型與撓曲型變形長相')


def fig3_2():
    W, H = 900, 630
    o = ''
    yb, hs = 520, 52
    ys = [yb - (i + 1) * hs for i in range(N18)]
    # ── 結構示意 ──
    o += T(110, 34, '題目（示意）', 16, INK, 'middle', 'bold')
    xa, xb, xw1, xw2 = 34, 94, 124, 164
    for x in (xa, xb):
        o += L(x, yb, x, ys[-1], INK, 2.4)
    for i, y in enumerate(ys):
        o += L(xa, y, xb, y, INK, 2.4)
        o += L(xb, y, xw1, y, MUT, 1.6) + C(xb + 3, y, 2.6, '#fff', MUT, 1.2) + C(xw1 - 3, y, 2.6, '#fff', MUT, 1.2)
    o += R(xw1, ys[-1], xw2 - xw1, yb - ys[-1], WALL2, WALL, 2)
    for k in range(9):
        y0 = ys[-1] + k * (yb - ys[-1]) / 9
        o += L(xw1, y0 + 20, xw2, y0, WALL, 0.8, op=0.6)
    o += hatch_ground(20, yb, 160)
    o += T(64, yb + 26, '構架', 14, TEN, 'middle', 'bold')
    o += T(144, yb + 26, '剪力牆', 14, WALL, 'middle', 'bold')
    o += T(110, yb + 50, '連桿只傳軸力', 14, MUT, 'middle')
    # ── 兩個力分布面板 ──
    sc = 44
    for (ax, title, Fv, c) in ((370, '(a) 構架分到的樓層力', r18['Ff'], TEN),
                               (660, '(b) 剪力牆分到的樓層力', r18['Fw'], WALL)):
        o += T(ax + 20, 34, title, 16, INK, 'middle', 'bold')
        o += L(ax, yb + 6, ax, ys[-1] - 20, INK, 1.6)
        o += hatch_ground(ax - 24, yb + 6, 48)
        for i, y in enumerate(ys):
            o += A(ax, y - 8, ax + sc, y - 8, MUT, 1.6, 8, dash='5 4')
            v = Fv[i]
            if abs(v) * sc > 9:
                o += A(ax, y + 6, ax + v * sc, y + 6, c, 3.4, 11)
            else:
                o += L(ax, y + 6, ax + v * sc, y + 6, c, 3.4)
            tx = ax + v * sc + (8 if v >= 0 else -8)
            o += T(tx, y + (12 if v >= 0 else 18), f'{v:+.2f}*F*', 14, COMP if v < 0 else c, 'start' if v >= 0 else 'end', 'bold')
            o += T(ax - 6, y - 3, f'{i + 1}F', 14, MUT, 'end')
    o += A(470, 64, 510, 64, MUT, 1.6, 8, dash='5 4')
    o += T(516, 69, '虛線＝外力 *F*（量尺）', 14, MUT, 'start')
    o += R(250, 568, 620, 50, KEY2, KEY, 1.5, 9)
    o += T(560, 599, '每一層：構架 + 牆 = *F*；底層牆約 3.4*F*、構架反向；頂層構架 1.35*F*、牆反向', 15, KEY, 'middle', 'bold')
    o += L(215, 50, 215, 560, GRID, 1.4)
    return svg(W, H, o, 'SA-2018-1 牆與構架的樓層力分布')


def fig3_3():
    W, H = 900, 520
    o = ''
    # (a) 三種情形的位移
    p = Plot(80, 90, 330, 300, 0, 9, 0, 2)
    o += T(245, 36, '(a) SA-2020-4 各樓位移（mm）', 16, INK, 'middle', 'bold')
    o += p.axes([0, 2, 4, 6, 8], [0, 1, 2], 'mm', '', size=14, yfmt=lambda t: ['地面', '一樓', '頂層'][int(t)])
    cases = [(np.concatenate([[0], r20['D_frame_alone'][::-1] * 1000]), TEN, '構架單獨 2、3'),
             (np.concatenate([[0], r20m['D_wall_alone'][::-1] * 1000]), WALL, '牆單獨 3、8'),
             (np.concatenate([[0], r20['D'][::-1] * 1000]), KEY, '合體 1、2')]
    lab_y = [(4.9, 1.45), (6.2, 0.62), (0.9, 1.9)]
    for (u, c, lab), (lx, ly) in zip(cases, lab_y):
        o += P([p.pt(x, z) for x, z in zip(u, (0, 1, 2))], c, 3.2)
        for x, z in zip(u[1:], (1, 2)):
            o += C(p.X(x), p.Y(z), 5, c, None)
    o += T(p.X(3.4), p.Y(1.62), '構架單獨 2、3', 15, TEN, 'start', 'bold')
    o += T(p.X(5.6), p.Y(1.25), '牆單獨 3、8', 15, WALL, 'start', 'bold')
    o += T(p.X(1.9), p.Y(2) - 12, '合體 1、2', 15, KEY, 'end', 'bold')
    o += T(245, 450, '構架：一樓已走 2/3 → 底部最斜（剪力型）', 14, TEN, 'middle', 'bold')
    o += T(245, 476, '牆：一樓只走 3/8 → 頂部最斜（撓曲型）', 14, WALL, 'middle', 'bold')
    # (b) 一行相加看出是哪一型
    o += T(680, 36, '(b) 看 [*K*] 頂層那一行相加', 16, INK, 'middle', 'bold')
    o += T(680, 64, '（推頂層 1、一樓鎖住，地面要出多少力？）', 14, MUT, 'middle')
    bx = 500
    for k, (title, col, s, c, msg1, msg2) in enumerate((
            ('構架 [*K*_{f}]', '+2 ， −2', r20m['Kf_colsum'][0], TEN, '和 = 0 → 地面不出力', '只有頂層那段柱變形 → 剪力型'),
            ('剪力牆 [*K*_{w}]', '+1 ， −2', r20m['Kw_colsum'][0], WALL, '和 = −1 ≠ 0 → 地面要出力', '一樓以下也跟著彎 → 撓曲型'))):
        y = 96 + k * 176
        o += R(bx, y, 360, 150, '#fff', c, 2, 10)
        o += R(bx, y, 360, 38, c, None, 0, 10) + R(bx, y + 24, 360, 14, c, None)
        o += T(bx + 180, y + 26, title, 16, '#fff', 'middle', 'bold')
        o += T(bx + 180, y + 72, f'第 1 行（×30000）：{col}', 15, INK, 'middle', 'bold')
        o += T(bx + 180, y + 102, msg1, 15, COMP if s != 0 else c, 'middle', 'bold')
        o += T(bx + 180, y + 130, msg2, 14, INK, 'middle')
    o += R(500, 452, 360, 50, KEY2, KEY, 1.4, 8)
    o += T(680, 483, '題目只給矩陣，也能一眼看出牆是撓曲型', 15, KEY, 'middle', 'bold')
    o += L(450, 50, 450, 510, GRID, 1.4)
    return svg(W, H, o, 'SA-2020-4 三種位移與勁度矩陣型態判別')


def fig3_4():
    W, H = 900, 560
    o = ''
    yb, hs = 450, 140
    y1, y2 = yb - hs, yb - 2 * hs
    xl, xr = 90, 210
    xw1, xw2 = 380, 430
    o += T(235, 34, '(a) 把連桿切開：構架與牆各自平衡', 16, INK, 'middle', 'bold')
    # 構架
    for x in (xl, xr):
        o += L(x, yb, x, y2, INK, 3)
    o += rigid_beam(xl - 6, xr + 6, y1, INK, 9) + rigid_beam(xl - 6, xr + 6, y2, INK, 9)
    o += base_fixed(xl, yb + 2, 40) + base_fixed(xr, yb + 2, 40)
    for y, nm in ((y2, 'a'), (y1, 'd')):
        o += A(xl - 76, y, xl - 10, y, COMP, 3, 12)
        o += T(xl - 80, y - 10, '60', 15, COMP, 'start', 'bold')
        o += T(xl + 8, y - 12, nm, 14, INK, 'start', 'bold')
    o += T(xr - 14, y2 - 12, 'b', 14, INK, 'end', 'bold')
    o += T(xr - 14, y1 - 12, 'e', 14, INK, 'end', 'bold')
    o += T(xl, yb + 28, 'g', 14, INK, 'middle', 'bold') + T(xr, yb + 28, 'h', 14, INK, 'middle', 'bold')
    # 連桿切口
    o += C(xr + 18, y2, 4, '#fff', MUT, 1.4) + C(xr + 18, y1, 4, '#fff', MUT, 1.4)
    o += T(xr + 26, y2 - 12, 'bc = 0', 15, MUT, 'start', 'bold')
    o += A(xr + 76, y1, xr + 24, y1, WARN, 3.2, 12)
    o += T(xr + 26, y1 - 14, 'ef：60', 15, WARN, 'start', 'bold')
    # 牆
    o += R(xw1, y2 - 6, xw2 - xw1, yb - y2 + 6, WALL2, WALL, 2)
    for k in range(7):
        y0 = y2 + k * (yb - y2) / 7
        o += L(xw1, y0 + 22, xw2, y0, WALL, 0.8, op=0.6)
    o += hatch_ground(xw1 - 16, yb, 82)
    o += C(xw1 - 14, y2, 4, '#fff', MUT, 1.4) + C(xw1 - 14, y1, 4, '#fff', MUT, 1.4)
    o += T(xw1 - 22, y2 + 24, 'c', 14, INK, 'end', 'bold') + T(xw1 - 22, y1 + 24, 'f', 14, INK, 'end', 'bold')
    o += A(xw1 - 62, y1, xw1 - 20, y1, WARN, 3.2, 12)
    o += T(xw1 - 48, y1 - 14, '60', 15, WARN, 'middle', 'bold')
    # 基底剪力
    for x in (xl, xr):
        o += A(x + 30, yb + 46, x - 4, yb + 46, TEN, 2.6, 10)
        o += T(x + 34, yb + 52, '30', 14, TEN, 'start', 'bold')
    o += A(xw1 + 60, yb + 46, xw1 + 12, yb + 46, WALL, 2.6, 10)
    o += T(xw1 + 64, yb + 52, '60', 14, WALL, 'start', 'bold')
    o += T(235, yb + 86, '構架底 30 + 30 ＋ 牆底 60 ＝ 120 ＝ 60 + 60（平衡）', 15, KEY, 'middle', 'bold')
    o += T(235, 66, '構架淨受：頂層 60、一樓 60 − 60 = 0', 14, TEN, 'middle', 'bold')
    o += T(235, 88, '牆淨受：頂層 0、一樓 60 → [*K*_{w}]{Δ}', 14, WALL, 'middle', 'bold')
    # (b) eh 柱
    o += T(690, 34, '(b) eh 柱（一樓右柱）', 16, INK, 'middle', 'bold')
    xc, ycb, yct = 690, 396, 186
    d = 46
    o += L(xc, ycb, xc, yct, STEEL, 1.6, '6 5')
    o += col_ff(xc, ycb, yct, 0, d, AC, 3.4)
    o += rigid_beam(xc - 40 + d, xc + 40 + d, yct, INK, 9)
    o += base_fixed(xc, ycb + 2, 50)
    o += A(xc + d - 76, yct + 26, xc + d - 8, yct + 26, COMP, 2.6, 11)
    o += T(xc + d - 80, yct + 32, '*V* = 30 kN', 15, COMP, 'end', 'bold')
    o += A(xc + 76, ycb - 22, xc + 8, ycb - 22, COMP, 2.6, 11)
    o += T(xc + 80, ycb - 16, '30 kN', 15, COMP, 'start', 'bold')
    o += arc_arrow(xc + d, yct, 28, -30, 100, KEY, 2.4, 10)
    o += T(xc + d + 34, yct - 22, '48 kN-m', 15, KEY, 'start', 'bold')
    o += arc_arrow(xc, ycb, 26, 110, 230, KEY, 2.4, 10)
    o += T(xc - 34, ycb - 30, '48 kN-m', 15, KEY, 'end', 'bold')
    o += T(xc, ycb + 50, '兩端彎矩都是逆時針（作用在柱上）', 14, MUT, 'middle')
    o += C(xc + d / 2, (ycb + yct) / 2, 6, KEY, '#fff', 2)
    o += T(xc + d / 2 + 12, (ycb + yct) / 2 + 5, '反曲點', 14, KEY, 'start')
    o += R(560, 470, 300, 76, KEY2, KEY, 1.4, 8)
    o += T(710, 496, f'*V* = *k*Δ_{{2}} = {k20:.0f} × 0.001 = 30', 15, KEY, 'middle', 'bold')
    o += T(710, 526, '*M* = *Vh*/2 = 30 × 3.2/2 = 48', 15, KEY, 'middle', 'bold')
    o += L(500, 50, 500, 550, GRID, 1.4)
    return svg(W, H, o, 'SA-2020-4 連桿力與 eh 柱')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
