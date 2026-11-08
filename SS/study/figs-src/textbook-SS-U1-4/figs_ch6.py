# -*- coding: utf-8 -*-
"""第 6 章：偏心螺栓群——繞形心轉（S5），SS-2002-4。"""
from plot import *  # noqa
from calcs import ss2002_4
import math

D = ss2002_4()


def fig6_1():
    W, H = 900, 460
    o = T(225, 28, '(a) 板子繞形心轉一個小角度', 16, INK, 'middle', 'bold')
    cx, cy, s = 225, 230, 12
    o += R(cx - 90, cy - 170, 180, 340, STEEL2, INK, 1.2, 4)
    o += C(cx, cy, 5, KEY, '#fff', 1.4) + T(cx + 10, cy - 10, 'O', 15, KEY, 'start', 'bold')
    fs = 4.0   # 每 cm 半徑對應 px 長
    for x, y in D['pts']:
        bx, by = cx + x * s, cy - y * s
        o += C(bx, by, 9, '#fff', INK, 1.6)
        o += L(cx, cy, bx, by, MUT, 1, '3 3')
        # 順時針轉：位移 ⊥ r，大小 ∝ r
        r = math.hypot(x, y)
        ux, uy = y / r, -x / r          # 順時針方向（數學座標）
        o += A(bx, by, bx + ux * r * fs, by - uy * r * fs, AC, 2.2, 8)
    o += T(cx, cy + 200, '箭頭 ⊥ 半徑、長度 ∝ 半徑', 15, AC, 'middle', 'bold')
    # (b) 推導圖示
    o += T(670, 28, '(b) 一條式子把它們接起來', 16, INK, 'middle', 'bold')
    o += R(470, 60, 400, 300, '#fff', KEY, 1.6, 12)
    lines = [('剛體轉 θ：每顆的位移 = θ·*r*_{i}', INK),
             ('螺栓都一樣硬：力 *R*_{i} = *k*·*r*_{i}', INK),
             ('力矩平衡：Σ *R*_{i}·*r*_{i} = *M*', INK),
             ('→ *k*·Σ*r*_{i}² = *M* → *k* = *M*/*I*_{p}', KEY),
             ('*R*_{M,i} = *M r*_{i} / *I*_{p}', COMP),
             ('*I*_{p} = Σ(*x*_{i}² + *y*_{i}²)', COMP)]
    for i, (t, c) in enumerate(lines):
        o += T(670, 104 + i * 44, t, 17 if c == COMP else 15, c, 'middle', 'bold' if c != INK else None)
    o += T(670, 390, '和材料力學 τ = *Tr*/*J* 是同一件事', 15, MUT, 'middle')
    return svg(W, H, o, '繞形心轉的螺栓群')


def fig6_2():
    W, H = 900, 420
    o = T(260, 28, '(a) 力臂是形心到「力線」的垂直距離', 16, INK, 'middle', 'bold')
    cx, cy, s = 150, 260, 9
    for x, y in D['pts']:
        o += C(cx + x * s, cy - y * s, 7, '#fff', INK, 1.4)
    o += C(cx, cy, 5, KEY, '#fff', 1.4) + T(cx - 10, cy + 5, 'O', 15, KEY, 'end', 'bold')
    px, py = cx + D['xP'] * s, cy - D['yP'] * s
    ux, uy = D['Px'] / D['P'], D['Py'] / D['P']
    # 力線
    o += L(px - ux * 160, py + uy * 160, px + ux * 380, py - uy * 380, MUT, 1.2, '6 4')
    o += A(px, py, px + ux * 90, py - uy * 90, COMP, 3.4, 12)
    o += T(px + 8, py - 10, '*P* = 20 tf（3:4）', 15, COMP, 'start', 'bold')
    o += C(px, py, 5, COMP, '#fff', 1.4)
    # 垂足
    t = -(D['xP'] * ux + D['yP'] * uy)
    fx, fy = D['xP'] + t * ux, D['yP'] + t * uy
    o += L(cx, cy, cx + fx * s, cy - fy * s, KEY, 2.6)
    o += T((cx + cx + fx * s) / 2 - 30, (cy + cy - fy * s) / 2 + 26, f'*e* = {D["e"]:.1f}', 16, KEY, 'start', 'bold')
    o += T(px, py + 30, f'作用點 ({D["xP"]}, {D["yP"]})', 14, MUT, 'middle')
    # (b) 分量取矩長條
    o += T(700, 28, '(b) 分量取矩：兩個方向互相抵銷', 16, INK, 'middle', 'bold')
    pl = Plot(560, 70, 300, 260, 0, 4, 0, 600)
    o += L(pl.x0, pl.Y(0), pl.x0 + pl.w, pl.Y(0), INK, 1.4)
    bars = [(f'16×{D["xP"]}', abs(D['M_y_part']), '順', WARN), (f'12×{D["yP"]}', abs(D['M_x_part']), '逆', AC),
            ('淨值', abs(D['M']), '順', KEY), ('錯：20×28.5', D['M_wrong'], '', COMP)]
    for i, (nm, v, d, c) in enumerate(bars):
        x = pl.X(i + 0.5)
        o += R(x - 26, pl.Y(v), 52, pl.Y(0) - pl.Y(v), '#fff', c, 2.2, 3, dash='5 3' if i == 3 else None)
        o += T(x, pl.Y(v) - 8, f'{v:.0f}', 15, c, 'middle', 'bold')
        o += T(x, pl.Y(0) + 22, nm, 14, INK, 'middle')
        if d:
            o += T(x, pl.Y(0) + 42, f'（{d}時針）', 14, MUT, 'middle')
    o += T(700, 404, '單位 tf·cm。只用作用點座標當力臂（570）會高估一倍以上', 14, MUT, 'middle')
    return svg(W, H, o, 'SS-2002-4 的扭矩')


def fig6_3():
    W, H = 900, 560
    o = T(450, 28, 'SS-2002-4：每顆螺栓 = 直接剪力（橘）+ 扭矩剪力（藍）→ 合力（紅）', 16, INK, 'middle', 'bold')
    cx, cy, s, fs = 280, 270, 17, 11
    o += R(cx - 110, cy - 220, 220, 440, STEEL2, INK, 1.0, 4)
    o += C(cx, cy, 5, KEY, '#fff', 1.4)
    rmax = D['Rmax']
    for x, y, fx, fy, R_ in D['res']:
        bx, by = cx + x * s * 1.5, cy - y * s
        o += C(bx, by, 9, '#fff', INK, 1.4)
        dx, dy = D['Px'] / D['n'], D['Py'] / D['n']
        tx, ty = fx - dx, fy - dy
        o += A(bx, by, bx + dx * fs, by - dy * fs, WARN, 2.2, 8)
        o += A(bx + dx * fs, by - dy * fs, bx + fx * fs, by - fy * fs, AC, 2.2, 8)
        crit = abs(R_ - rmax) < 1e-9
        o += A(bx, by, bx + fx * fs, by - fy * fs, COMP, 3.4 if crit else 2, 10)
        lx = bx + (16 if x > 0 else -16)
        o += T(lx, by - 14, f'{R_:.2f}', 15 if crit else 14, COMP if crit else INK, 'start' if x > 0 else 'end', 'bold' if crit else None)
    o += R(560, 80, 320, 250, '#fff', KEY, 1.6, 10)
    rows = [f'*I*_{{p}} = 98 + 490 = {D["Ip"]:.0f} cm²', f'*M* = {abs(D["M"]):.0f} tf·cm（順時針）',
            f'直接剪力 (−1.5, −2.0) tf', f'角點扭矩剪力 {D["RM_corner"]:.2f} tf', '四個角點一樣遠，', '只有右下角和直接剪力同向']
    for i, t in enumerate(rows):
        o += T(720, 112 + i * 36, t, 15, KEY if i >= 4 else INK, 'middle', 'bold' if i >= 4 else None)
    o += T(450, 548, f'最大 *R* = {rmax:.2f} tf ≤ 單剪容許 {D["Rv"]:.3f} tf（比值 {D["ratio"]:.2f}）→ 足夠', 16, COMP, 'middle', 'bold')
    return svg(W, H, o, 'SS-2002-4 螺栓合力')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
