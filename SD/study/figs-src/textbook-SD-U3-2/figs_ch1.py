# -*- coding: utf-8 -*-
"""第 1 章：譜的兩端、隔震 2DOF。"""
from sdfig import *  # noqa
from calcs import Sa_demo, Sd_demo, ISO, Q2011F
import math


def fig1_1():
    W, H = 900, 360
    o = ''
    for j, (ttl, fn, ymax, yl, col, key) in enumerate((('加速度譜：力變小', Sa_demo, 1.0, '*S*_{a} (*g*)', COMP, 'Sa'), ('位移譜：位移變大', lambda t: Sd_demo(t), 40, '*S*_{d} (cm)', AC, 'Sd'))):
        ox = 20 + j * 450
        pl = Plot(ox + 60, 50, 320, 240, 0, 3.5, 0, ymax)
        o += T(ox + 230, 26, ttl, 15.5, col, 'middle', 'bold')
        o += pl.axes([0, 1, 2, 3], [0, ymax / 2, ymax], '*T* (s)', yl, yfmt=lambda v: f'{v:g}')
        o += pl.curve(fn, 0.01, 3.5, col, 3, n=300)
        for T_, c, lab in ((ISO['T_fixed'], KEY, '固定基礎'), (ISO['T_iso'], TEN, '隔震')):
            v = fn(T_)
            o += pl.dot(T_, v, c, 6)
            o += (T(pl.X(T_) + 8, pl.Y(v) - 10, f'{lab} {v:.2f}', 14, c, 'start', 'bold') if j == 0 else T(pl.X(T_) + (12 if T_ < 1 else -12), pl.Y(v) + (-4 if T_ < 1 else -14), f'{lab} {v:.1f}', 14, c, 'start' if T_ < 1 else 'end', 'bold'))
        if j == 0:
            o += A(pl.X(0.6), pl.Y(0.85), pl.X(2.3), pl.Y(0.3), KEY, 2, 10, dash='6 4')
        else:
            o += A(pl.X(0.6), pl.Y(8), pl.X(2.3), pl.Y(26), KEY, 2, 10, dash='6 4')
    o += T(450, 345, '示範 *S*_{DS} = 0.8、*S*_{D1} = 0.45：週期 0.5 → 2.5 s，力剩 0.18/0.8 = 23%，位移卻從 5 cm 變 28 cm', 14, MUT, 'middle')
    return svg(W, H, o, '譜的兩端')


def fig1_2():
    W, H = 900, 360
    o = T(200, 26, '隔震 2DOF（2011-1）', 15.5, INK, 'middle', 'bold')
    x0, yb = 110, 300
    o += hatch_ground(x0 - 30, yb + 20, 230)
    U = Q2011F['U'][0]
    sc = 3
    ub, uu = U[1] * sc, U[0] * sc
    o += R(x0 - 10 + ub, yb - 10, 180, 20, WARN2, WARN, 2, 3) + T(x0 + 80 + ub, yb + 6, '基礎層 200 tf', 14, WARN, 'middle', 'bold')
    for xx in (x0 + 20, x0 + 140):
        o += spring(xx, yb + 20, xx + ub, yb + 10, n=3, amp=6, c=WARN)
    for cx in (x0, x0 + 160):
        o += L(cx + ub, yb - 10, cx + uu, yb - 160, STEEL, 5)
    o += R(x0 - 10 + uu, yb - 175, 180, 18, AC2, AC, 2, 3) + T(x0 + 80 + uu, yb - 184, '上部 300 tf', 14, AC, 'middle', 'bold')
    o += T(x0 + 80, yb + 50, f'第 1 振態：隔震層位移 {U[1]:.1f} cm、層間僅 {U[0]-U[1]:.2f} cm', 14, KEY, 'middle', 'bold')
    o += box(430, 50, 460, 290, '隔震振態 ≈ 整棟平移', ['*T*_{1} = 2.0 s（ξ = 10%）、*T*_{2} = 0.25 s（ξ = 5%）', 'φ_{1} = {1.041, 1.000}（上部、基礎）', f'Γ_{{1}} = {Q2011F["G"][0]:.3f}：有效質量 {Q2011F["Meff"][0]/500*100:.1f}%', '隔震振態用 *B*_{1}（長週期）', '上部振態用 *B*_{S}（短週期）', f'SRSS：隔震位移 {Q2011F["iso"]:.1f} cm', f'層間位移 {Q2011F["drift"]:.3f} cm', f'隔震層剪力 {Q2011F["Vb_srss"]:.0f} tf'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '隔震 2DOF')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
