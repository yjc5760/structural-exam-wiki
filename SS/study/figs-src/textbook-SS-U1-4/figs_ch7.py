# -*- coding: utf-8 -*-
"""第 7 章：偏心銲縫群——線圖、形心、J、控制點（SS-2017-4、SS-2004-3、SS-2007-1）。"""
from plot import *  # noqa
from calcs import ss2017_4_points, ss2004_3, ss2007_1
import math

B = ss2017_4_points()
E = ss2004_3()
G = ss2007_1()


def fig7_1():
    W, H = 900, 440
    s = 3.2
    ox, oy = 110, 340
    o = T(330, 28, 'SS-2017-4：⊐ 形銲道（依比例，cm）', 16, INK, 'middle', 'bold')
    o += R(ox - 40, oy - B['dv'] * s - 20, 40, B['dv'] * s + 40, STEEL3, INK, 1.2)
    o += T(ox - 20, oy + 46, '柱', 15, INK, 'middle', 'bold')
    plate = [(ox, oy), (ox, oy - B['dv'] * s), (ox + 100 * s, oy - B['dv'] * s), (ox + 100 * s, oy - B['dv'] * s * 0.7), (ox + B['b'] * s, oy)]
    o += P(plate, STEEL, 1.2, fill=STEEL2, close=True)
    o += L(ox, oy, ox, oy - B['dv'] * s, COMP, 6) + L(ox, oy, ox + B['b'] * s, oy, COMP, 6) + L(ox, oy - B['dv'] * s, ox + B['b'] * s, oy - B['dv'] * s, COMP, 6)
    gx, gy = ox + B['xbar'] * s, oy - B['ybar'] * s
    o += C(gx, gy, 6, KEY, '#fff', 1.6)
    o += T(gx + 10, gy + 22, f'形心 ({B["xbar"]:.0f}, {B["ybar"]:.0f})', 15, KEY, 'start', 'bold')
    px = ox + B['xP'] * s
    o += A(px, oy - B['dv'] * s - 30, px, oy - B['dv'] * s + 10, COMP, 3.4, 12) + T(px + 8, oy - B['dv'] * s - 20, '*P*', 17, COMP, 'start', 'bold')
    o += L(px, oy - B['dv'] * s + 10, px, oy + 10, MUT, 1, '5 4')
    o += dim(gx, oy + 26, px, oy + 26, f'*e* = {B["e"]:.0f}', KEY, 0, 15)
    o += dim(ox, oy + 56, ox + B['b'] * s, oy + 56, '40', INK, 0, 14)
    o += dim(ox + B['b'] * s, oy + 56, px, oy + 56, '50', INK, 0, 14)
    o += dim(ox - 62, oy, ox - 62, oy - B['dv'] * s, '80', INK, 0, 14, side=-1)
    o += R(590, 70, 290, 230, '#fff', KEY, 1.6, 10)
    rows = ['長度加權形心：', '*x̄* = Σ*L*_{i}*x*_{i} / Σ*L*_{i}', '= (40·20 + 80·0 + 40·20) / 160', f'= {B["xbar"]:.0f} cm（速算 *b*²/(2*b* + *d*)）', '*e* 從形心量起：90 − 10 = 80', '不是從銲道邊量 90']
    for i, t in enumerate(rows):
        o += T(735, 100 + i * 34, t, 15, COMP if i == 5 else (KEY if i in (0, 4) else INK), 'middle', 'bold' if i in (0, 4, 5) else None)
    return svg(W, H, o, 'SS-2017-4 銲道群')


def fig7_2():
    W, H = 900, 330
    pl = Plot(250, 60, 500, 200, 0, 200000, 0, 4)
    o = T(450, 28, '*J* = Σ∫*r*² d*L*：每段 = 自身項 + 遠離項（cm³）', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 50000, 100000, 150000, 200000], [], 'cm³', '', size=14, xfmt=lambda v: f'{v/1000:.0f}k')
    rows = [('上水平 40', B['Jh_own'], B['Jh_far']), ('下水平 40', B['Jh_own'], B['Jh_far']), ('垂直 80', B['Jv_own'], B['Jv_far'])]
    x0 = 0
    for i, (nm, own, far) in enumerate(rows):
        yc = pl.Y(3.4 - i * 1.0)
        o += R(pl.X(0), yc - 16, pl.X(own) - pl.X(0), 32, AC2, AC, 1.6)
        o += R(pl.X(own), yc - 16, pl.X(own + far) - pl.X(own), 32, WARN2, WARN, 1.6)
        o += T(pl.X(0) - 10, yc + 5, nm, 15, INK, 'end', 'bold')
        o += T(pl.X(own + far) + 8, yc + 5, f'{own + far:,.0f}', 15, INK, 'start', 'bold')
    o += R(pl.X(0), pl.Y(0.4) - 16, pl.X(B['J']) - pl.X(0), 32, KEY2, KEY, 2)
    o += T(pl.X(0) - 10, pl.Y(0.4) + 5, '合計 *J*', 15, KEY, 'end', 'bold')
    o += T(pl.X(B['J']) - 8, pl.Y(0.4) + 5, f'{B["J"]:,.0f}', 15, KEY, 'end', 'bold')
    o += R(250, 296, 18, 14, AC2, AC, 1.2) + T(274, 309, '自身項 *L*³/12', 14, INK, 'start')
    o += R(450, 296, 18, 14, WARN2, WARN, 1.2) + T(474, 309, '遠離項 *L*·*d*²（平行軸）', 14, INK, 'start')
    return svg(W, H, o, 'J 的組成')


def fig7_3():
    W, H = 900, 450
    s = 3.2
    ox, oy = 150, 330
    o = T(450, 28, 'SS-2017-4 四個角點（每 cm 銲道的力 ÷ *P*，×10⁻³）', 16, INK, 'middle', 'bold')
    o += L(ox, oy, ox, oy - 80 * s, STEEL, 5) + L(ox, oy, ox + 40 * s, oy, STEEL, 5) + L(ox, oy - 80 * s, ox + 40 * s, oy - 80 * s, STEEL, 5)
    gx, gy = ox + B['xbar'] * s, oy - B['ybar'] * s
    o += C(gx, gy, 5, KEY, '#fff', 1.4)
    fs = 3500
    for X, Y, fx, fy, R_, r in B['res']:
        bx, by = ox + X * s, oy - Y * s
        tx, ty = fx, fy + B['fv']
        o += A(bx, by, bx, by + B['fv'] * fs, WARN, 2.2, 8)
        o += A(bx, by + B['fv'] * fs, bx + tx * fs, by + B['fv'] * fs - ty * fs, AC, 2.2, 8)
        crit = R_ > 0.02
        o += A(bx, by, bx + fx * fs, by - fy * fs, COMP, 3.4 if crit else 2, 10)
        if X > 0 and Y > 0:
            lx, ly, an = bx, by - 14, 'middle'
        elif X > 0:
            lx, ly, an = bx + 16, by + 22, 'start'
        elif Y > 0:
            lx, ly, an = bx - 14, by - 10, 'end'
        else:
            lx, ly, an = bx + 16, by + 22, 'start'
        o += T(lx, ly, f'{R_*1000:.2f}', 15, COMP if crit else INK, an, 'bold' if crit else None)
        o += L(gx, gy, bx, by, MUT, 1, '3 3')
    o += R(470, 70, 410, 300, '#fff', KEY, 1.6, 10)
    rows = [f'直接：*P*/160 = {B["fv"]*1000:.2f}（向下，橘）', f'扭矩：*Mr*/*J*，*M* = 80*P*（順時針，藍）',
            f'右端 *r* = {B["res"][0][5]:.0f}：扭矩剪力有向下分量', '　→ 與直接剪力同向相加 → 24.54', f'左端 *r* = {B["res"][2][5]:.1f}：向上分量相消 → 16.36',
            f'每 cm 銲道強度 *q* = {B["q"]:.3f} tf/cm', f'*P*_{{u}} = {B["q"]:.3f} / 0.02454 = {B["Pu"]:.1f} tf']
    for i, t in enumerate(rows):
        o += T(675, 104 + i * 38, t, 15, COMP if i == 6 else INK, 'middle', 'bold' if i in (3, 6) else None)
    return svg(W, H, o, 'SS-2017-4 角點向量')


def fig7_4():
    W, H = 900, 400
    s = 9
    ox, oy = 120, 200
    o = T(260, 28, '(a) SS-2004-3：力線幾乎穿過形心', 16, INK, 'middle', 'bold')
    o += R(ox, oy - 12.5 * s - 10, 20 * s, 25 * s + 20, STEEL2, STEEL, 1.2)
    for (a, b) in E['segs']:
        o += L(ox + a[0] * s, oy - a[1] * s, ox + b[0] * s, oy - b[1] * s, COMP, 6)
    gx, gy = ox + E['xbar'] * s, oy
    o += C(gx, gy, 6, KEY, '#fff', 1.6) + T(gx - 10, gy + 5, '形心', 15, KEY, 'end', 'bold')
    px, py = ox + 17.5 * s, oy - 12.5 * s
    c = 1 / math.sqrt(2)
    o += L(px + 60 * c, py - 60 * c, px - 260 * c, py + 260 * c, MUT, 1.2, '6 4')
    o += A(px + 50 * c, py - 50 * c, px, py, COMP, 3.4, 12) + T(px + 10, py - 30, '*P*_{u}（1:1）', 16, COMP, 'start', 'bold')
    # 形心到力線距離
    vx, vy = gx - px, gy - py
    t = vx * (-c) + vy * (c)
    fx, fy = px + t * (-c), py + t * c
    o += L(gx, gy, fx, fy, KEY, 2.6)
    o += T(fx + 10, fy + 20, f'*e* = {E["e_line"]:.2f} cm', 15, KEY, 'start', 'bold')
    # (b) 長條
    o += T(690, 28, '(b) 有扭矩 vs 沒扭矩', 16, INK, 'middle', 'bold')
    pl = Plot(560, 70, 280, 240, 0, 2, 0, 45)
    o += L(pl.x0, pl.Y(0), pl.x0 + pl.w, pl.Y(0), INK, 1.4)
    for i, (nm, v, cc) in enumerate([('本題 *P*_{u}', E['Pu'], COMP), ('純剪上限', E['P0'], STEEL)]):
        x = pl.X(i + 0.5)
        o += R(x - 36, pl.Y(v), 72, pl.Y(0) - pl.Y(v), '#fff', cc, 2.2, 3)
        o += T(x, pl.Y(v) - 8, f'{v:.1f} tf', 15, cc, 'middle', 'bold')
        o += T(x, pl.Y(0) + 22, nm, 15, INK, 'middle')
    o += T(700, 362, f'*P*_{{0}} = *q*·*L* = {E["q"]:.3f} × 25；本題為上限的 {E["Pu"]/E["P0"]*100:.0f}%', 14, MUT, 'middle')
    o += T(260, 380, f'垂直分量 {E["M_v"]:.2f}*P*_{{u}}（順）− 水平分量 {E["M_h"]:.2f}*P*_{{u}}（逆）= {abs(E["M"]):.2f}*P*_{{u}}', 14, MUT, 'middle')
    return svg(W, H, o, 'SS-2004-3')


def fig7_5():
    W, H = 900, 400
    o = T(450, 28, 'SS-2007-1 平衡銲道：三段銲的合力要落在角鋼形心線上', 16, INK, 'middle', 'bold')
    s = 16
    ox, oy = 180, 70
    o += R(ox, oy, 40 * s * 0.7, 15 * s, STEEL2, INK, 1.2)
    o += L(ox, oy, ox + G['a'] * s * 0.7, oy, COMP, 6)
    o += L(ox, oy + 15 * s, ox + G['b'] * s * 0.7, oy + 15 * s, COMP, 6)
    o += L(ox, oy, ox, oy + 15 * s, COMP, 6)
    o += T(ox + G['a'] * s * 0.35, oy - 10, f'*a* = {G["a"]:.1f} → 12 cm（{G["Fa"]:.2f} tf）', 15, COMP, 'middle', 'bold')
    o += T(ox + G['b'] * s * 0.35, oy + 15 * s + 26, f'*b* = {G["b"]:.1f} → 31 cm（{G["Fb"]:.2f} tf）', 15, COMP, 'middle', 'bold')
    o += T(ox - 10, oy + 7.5 * s + 5, f'端部 {G["F3"]:.2f}', 15, COMP, 'end', 'bold')
    yP = oy + 10 * s
    o += L(ox - 60, yP, ox + 40 * s * 0.7 + 60, yP, KEY, 1.6, '6 4')
    o += A(ox + 40 * s * 0.7 + 20, yP, ox + 40 * s * 0.7 + 90, yP, KEY, 3.4, 12)
    o += T(ox + 40 * s * 0.7 + 96, yP + 5, f'*P* = {G["P"]} tf', 15, KEY, 'start', 'bold')
    o += T(ox + 40 * s * 0.7 + 96, yP + 28, '（形心線，距 *a* 側 10）', 14, KEY, 'start')
    o += T(450, 386, '對 *a* 線取矩：*F*_{b}×15 + *F*_{3}×7.5 = *P*×10 → *F*_{b}；再由 Σ*F* = *P* 得 *F*_{a}', 15, MUT, 'middle')
    return svg(W, H, o, '平衡銲道')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4, 'fig7_5': fig7_5}
