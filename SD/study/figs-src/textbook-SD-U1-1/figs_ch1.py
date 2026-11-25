# -*- coding: utf-8 -*-
"""第 1 章：自由體圖、圓周投影、T 的方向性。"""
from sdfig import *  # noqa
from calcs import EX, PI
import math


def fig1_1():
    W, H = 900, 400
    o = T(225, 30, '(a) 受外力 *p*(*t*)：四個力打平', 16, INK, 'middle', 'bold')
    # 台車
    yg = 230
    o += cart(150, yg, 120, 76, '*m*', AC, AC2, wall_x=40)
    o += A(270, yg - 50, 350, yg - 50, COMP, 3, 12) + T(358, yg - 45, '*p*(*t*)', 17, COMP, 'start', 'bold')
    o += A(150, yg - 140, 230, yg - 140, MUT, 1.6, 9, dash='5 4') + T(240, yg - 135, '*u*（向右為正）', 15, MUT, 'start')
    # FBD
    yb = 300
    o += R(150, yb - 34, 120, 52, AC2, AC, 1.6, 6) + T(210, yb - 2, '*m*', 18, AC, 'middle', 'bold')
    o += A(270, yb - 8, 340, yb - 8, COMP, 2.6, 11) + T(345, yb - 3, '*p*', 16, COMP, 'start', 'bold')
    o += A(150, yb - 24, 70, yb - 24, AC, 2.4, 11) + T(64, yb - 19, '*ku*', 15, AC, 'end')
    o += A(150, yb + 4, 70, yb + 4, TEN, 2.4, 11) + T(64, yb + 10, '*cu̇*', 15, TEN, 'end')
    o += A(210, yb + 18, 150, yb + 50, KEY, 2.4, 11, dash='6 4') + T(144, yb + 58, '慣性力 *mü*', 15, KEY, 'end')
    o += T(225, 392, '*p* − *ku* − *cu̇* = *mü* ⇒ *mü* + *cu̇* + *ku* = *p*', 15, INK, 'middle', 'bold')
    o += L(450, 20, 450, 390, GRID, 1.5)
    # (b) 基礎激振
    o += T(675, 30, '(b) 地面動 *x*_{g}(*t*)：外力換成 −*mü*_{g}', 16, INK, 'middle', 'bold')
    yg2 = 230
    o += hatch_ground(470, yg2, 410, INK)
    o += R(480, yg2 - 6, 390, 6, STEEL3, None)
    o += A(560, yg2 + 26, 630, yg2 + 26, WARN, 2.4, 10) + T(640, yg2 + 31, '*x*_{g}', 16, WARN, 'start', 'bold')
    o += L(500, yg2 - 6, 500, yg2 - 116, INK, 3)
    o += spring(500, yg2 - 66, 640, yg2 - 66) + T(570, yg2 - 82, '*k*', 16, INK, 'middle')
    o += dashpot(500, yg2 - 32, 640) + T(570, yg2 + 0, '*c*', 16, INK, 'middle')
    o += R(640, yg2 - 96, 110, 76, AC2, AC, 2, 6) + T(695, yg2 - 52, '*m*', 18, AC, 'middle', 'bold')
    o += A(640, yg2 - 128, 730, yg2 - 128, MUT, 1.6, 9, dash='5 4') + T(738, yg2 - 123, '*x*（絕對）', 15, MUT, 'start')
    o += T(675, 300, '彈簧、阻尼只感受「相對」 *u* = *x* − *x*_{g}', 15, INK, 'middle')
    o += T(675, 328, '慣性只感受「絕對」 *mẍ* = *m*(*ü* + *ü*_{g})', 15, INK, 'middle')
    o += R(500, 346, 350, 38, KEY2, KEY, 1.5, 8)
    o += T(675, 371, '*mü* + *cu̇* + *ku* = −*mü*_{g}(*t*)', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '自由體圖與基礎激振')


def fig1_2():
    W, H = 900, 360
    cx, cy, R0 = 200, 185, 120
    o = T(200, 30, '圓周上等速轉的點', 16, INK, 'middle', 'bold')
    o += C(cx, cy, R0, 'none', STEEL, 1.6)
    o += L(cx - R0 - 20, cy, cx + R0 + 20, cy, GRID, 1.2) + L(cx, cy - R0 - 20, cx, cy + R0 + 20, GRID, 1.2)
    th = math.radians(40)
    px, py = cx + R0 * math.cos(th), cy - R0 * math.sin(th)
    o += L(cx, cy, px, py, AC, 2.4) + C(px, py, 7, AC, '#fff', 2)
    o += P([(cx + 34 * math.cos(t), cy - 34 * math.sin(t)) for t in [i * th / 20 for i in range(21)]], KEY, 1.8)
    o += T(cx + 44, cy - 10, 'ω*t*', 15, KEY, 'start')
    o += L(px, py, px, cy, MUT, 1.3, '4 3')
    o += C(px, cy, 6, COMP, '#fff', 2)
    o += T(px + 8, cy + 22, '投影 *u* = *A* cos ω*t*', 15, COMP, 'start', 'bold')
    o += T(cx - 8, cy - R0 - 8, '*A*', 15, AC, 'end')
    # 向心加速度箭頭
    o += A(px, py, px - 0.42 * (px - cx), py - 0.42 * (py - cy), WARN, 2.2, 10)
    o += T(px - 34, py - 4, 'ω²*A*', 15, WARN, 'end')
    # 右：推導框
    o += box(430, 70, 440, 200, '投影點的加速度＝向心加速度的投影', [
        '位置 *u* = *A* cos ω*t*',
        '加速度 *ü* = −ω²*A* cos ω*t* = −ω²*u*',
        '代入 *mü* + *ku* = 0：',
        '(−*m*ω² + *k*)*u* = 0 對所有 *t* 成立',
        '⇒ ω² = *k*/*m*',
        '「回復力 ÷ 質量」就是轉速的平方'], KEY2, KEY, 15.5, 15)
    return svg(W, H, o, '圓周運動投影得到 ω')


def fig1_3():
    W, H = 900, 360
    pl = Plot(90, 50, 520, 250, 0.5, 4, 0, 2.2)
    o = pl.axes([0.5, 1, 2, 3, 4], [0, 0.5, 1, 1.5, 2], '*n*', '*T*/*T*_{0}')
    o += pl.curve(lambda n: math.sqrt(n), 0.5, 4, WARN, 3)
    o += pl.curve(lambda n: 1 / math.sqrt(n), 0.5, 4, AC, 3)
    o += pl.dot(1, 1, KEY, 6)
    o += pl.dot(2, math.sqrt(2), WARN, 5) + pl.dot(2, 1 / math.sqrt(2), AC, 5)
    o += T(pl.X(2) + 10, pl.Y(math.sqrt(2)) - 8, '1.41', 15, WARN, 'start', 'bold')
    o += T(pl.X(2) + 10, pl.Y(1 / math.sqrt(2)) + 22, '0.71', 15, AC, 'start', 'bold')
    o += T(pl.X(3.3), pl.Y(1.95), '質量 × *n*', 16, WARN, 'middle', 'bold')
    o += T(pl.X(3.3), pl.Y(0.35), '勁度 × *n*', 16, AC, 'middle', 'bold')
    o += R(640, 70, 245, 200, KEY2, KEY, 1.4, 8)
    o += T(762, 98, '*T* = 2π√(*m*/*k*)', 16, KEY, 'middle', 'bold')
    o += T(762, 130, '越重 → 越慢（週期長）', 15, INK, 'middle')
    o += T(762, 158, '越硬 → 越快（週期短）', 15, INK, 'middle')
    o += T(762, 194, '兩倍只變 √2 倍', 15, INK, 'middle')
    o += T(762, 222, '加質量 1.44 倍', 15, INK, 'middle')
    o += T(762, 248, '週期才變 1.2 倍', 15, INK, 'middle')
    return svg(W, H, o, '週期與勁度質量的方向性')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
