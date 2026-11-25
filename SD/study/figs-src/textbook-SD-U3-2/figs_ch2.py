# -*- coding: utf-8 -*-
"""第 2 章：雙線性鉛心橡膠迴圈、摩擦單擺。"""
from sdfig import *  # noqa
from calcs import LRB, LRB_HIST, Q2018
import math


def fig2_1():
    W, H = 900, 380
    h = LRB_HIST[-1]
    D, Q, kd, Dy, ko = h['D'], LRB['Q'], LRB['kd'], LRB['Dy'], LRB['ko']
    Fy = LRB['Fy']; Fmax = Q + kd * D
    pl = Plot(110, 40, 460, 290, -0.25, 0.25, -1100, 1100)
    o = pl.axes([-0.2, -0.1, 0, 0.1, 0.2], [-1000, -500, 0, 500, 1000], '*D* (m)', '*F* (kN)', grid=False)
    loop = [(-D, -Fmax), (-D + 2 * Dy, -Fmax + 2 * Fy), (D, Fmax), (D - 2 * Dy, Fmax - 2 * Fy), (-D, -Fmax)]
    o += P([pl.pt(*p) for p in loop], WARN, 0, fill=WARN2, close=True)
    o += P([pl.pt(*p) for p in loop], WARN, 3)
    o += L(pl.X(-D), pl.Y(-Fmax), pl.X(D), pl.Y(Fmax), KEY, 2, '7 5')
    o += pl.dot(D, Fmax, KEY, 5)
    o += T(pl.X(D) - 8, pl.Y(Fmax) - 10, f'(*D*, *F*_{{max}}) = ({D:.3f}, {Fmax:.0f})', 14, KEY, 'end', 'bold')
    o += T(pl.X(0) - 8, pl.Y(Q) - 8, f'*Q* = {Q:.0f}', 14, WARN, 'end', 'bold') + pl.dot(0, Q, WARN, 4)
    o += T(pl.X(0.02), pl.Y(-200), '*A*_{TD}（橘色面積）', 14, WARN, 'start', 'bold')
    o += T(pl.X(-0.24), pl.Y(900), '割線 *K*_{eD}（紫虛線）', 14, KEY, 'start', 'bold')
    o += box(600, 40, 290, 300, '雙線性迴圈的幾何', ['初始勁度 *k*_{o}、降伏後 *k*_{d} = α*k*_{o}', '*D*_{y} = *F*_{y}/*k*_{o}', '特性強度 *Q* = *F*_{y}(1 − α)', '*F*_{max} = *Q* + *k*_{d}*D*', '*K*_{eD} = *F*_{max}/*D* = *Q*/*D* + *k*_{d}', '面積 = 平行四邊形', '*A*_{TD} = 4*Q*(*D* − *D*_{y})', '（*n* 顆支承再乘 *n*）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '雙線性迴圈')


def fig2_2():
    W, H = 900, 380
    o = T(220, 26, '(a) 碗裡的滑塊', 15.5, INK, 'middle', 'bold')
    cx, cy, R0 = 220, -80, 360
    arc = [(cx + R0 * math.sin(a), cy + R0 * math.cos(a)) for a in [math.radians(d) for d in range(-28, 29, 2)]]
    o += P(arc, INK, 3)
    o += C(cx, cy + R0 - 2, 3, INK, INK, 1)
    th = math.radians(14)
    sx, sy = cx + R0 * math.sin(th), cy + R0 * math.cos(th)
    o += L(cx, 30, sx, sy, MUT, 1.2, '4 3') + L(cx, 30, cx, cy + R0, MUT, 1.2, '4 3')
    o += T(cx + 8, 90, '*R*', 15, MUT, 'start')
    o += R(sx - 22, sy - 30, 44, 24, AC2, AC, 2, 3)
    o += A(sx, sy - 18, sx, sy + 50, COMP, 2.4, 10) + T(sx + 6, sy + 44, '*W*', 15, COMP, 'start', 'bold')
    o += A(sx, sy - 18, sx - 60, sy - 18, KEY, 2.4, 10) + T(sx - 64, sy - 24, '*W*·*x*/*R*', 15, KEY, 'end', 'bold')
    o += A(sx + 22, sy - 10, sx + 70, sy - 10, TEN, 2, 9) + T(sx + 74, sy - 4, 'μ*W*（與速度反向）', 14, TEN, 'start', 'bold')
    o += T(220, 340, '像單擺：回復力 ∝ *W*/*R* · *x*、質量 *W*/*g*', 14, MUT, 'middle')
    o += T(220, 362, '⇒ ω² = *g*/*R*，*T* = 2π√(*R*/*g*)（與 *W* 無關）', 14.5, KEY, 'middle', 'bold')
    o += L(450, 20, 450, 370, GRID, 1.5)
    o += T(675, 26, '(b) FPS 的遲滯迴圈', 15.5, INK, 'middle', 'bold')
    pl = Plot(510, 60, 330, 230, -1, 1, -1, 1)
    o += pl.axes([0], [0], '*x*', '*F*/*W*', grid=False)
    mu, kr = 0.3, 0.45
    loop = [(-1, -kr - mu), (-1, -kr + mu), (1, kr + mu), (1, kr - mu), (-1, -kr - mu)]
    o += P([pl.pt(*p) for p in loop], TEN, 0, fill=TEN2, close=True) + P([pl.pt(*p) for p in loop], TEN, 3)
    o += pl.dot(0, mu, TEN, 4) + pl.dot(0, -mu, TEN, 4) + T(pl.X(0) - 8, pl.Y(mu) - 8, '+μ', 15, TEN, 'end', 'bold') + T(pl.X(0) + 8, pl.Y(-mu) + 20, '−μ', 15, TEN, 'start', 'bold')
    o += T(pl.X(0.55), pl.Y(0.85), '斜率 1/*R*', 15, KEY, 'middle', 'bold')
    o += T(675, 340, f'2018-4：*D*/*R* + μ = 0.08 → *R* = {Q2018["R"]/100:.1f} m、μ = {Q2018["mu"]:.3f}', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '摩擦單擺')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
