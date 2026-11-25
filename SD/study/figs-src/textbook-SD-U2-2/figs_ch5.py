# -*- coding: utf-8 -*-
"""第 5 章：倒三角形、2025-1 樓層力與層剪力、經驗週期。"""
from sdfig import *  # noqa
from calcs import Q2025, CT
import math


def fig5_1():
    W, H = 900, 400
    n, sh, x0, yb = 6, 52, 110, 360
    disp = [8 * (i + 1) for i in range(n)]
    s, pts = shear_building(x0, yb, n, bw=110, sh=sh, disp=disp)
    o = T(170, 28, '第 1 振態 ≈ 直線 φ ∝ *h*', 15.5, INK, 'middle', 'bold') + s
    for i, (x, y) in enumerate(pts):
        L_ = 18 * (i + 1)
        o += A(x + 75, y, x + 75 + L_, y, AC, 2.4, 10)
    o += A(pts[-1][0] + 75, pts[-1][1] - 22, pts[-1][0] + 75 + 40, pts[-1][1] - 22, COMP, 3, 11) + T(pts[-1][0] + 125, pts[-1][1] - 17, '*F*_{t}', 16, COMP, 'start', 'bold')
    o += box(470, 50, 420, 320, '倒三角形從哪裡來', ['慣性力 *F*_{i} = *m*_{i}*ü*_{i} ∝ *m*_{i}φ_{i}', '假設 1：只有第 1 振態', '假設 2：φ_{i} ∝ 高度 *h*_{i}', '⇒ *F*_{i} ∝ *w*_{i}*h*_{i}', '總和要等於 *V* − *F*_{t}：', '*F*_{x} = (*V*−*F*_{t})·*w*_{x}*h*_{x}/Σ*w*_{i}*h*_{i}', '*T* 長 → 高振態變重要、', '第 1 振態上彎 → 頂層補 *F*_{t}', '*F*_{t} 從 *V* 挖出，不是外加'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '豎向分配的來源')


def fig5_2():
    W, H = 900, 380
    F, Vs = Q2025['F'], Q2025['Vs']
    o = T(230, 26, '樓層力 *F*_{i}（kN）', 15.5, AC, 'middle', 'bold') + T(680, 26, '層剪力 *V*_{i}（kN）', 15.5, KEY, 'middle', 'bold')
    for i in range(8):
        y = 340 - i * 38
        o += T(40, y + 5, f'{i+1}F', 14, MUT, 'start')
        base = F[i] - (Q2025['Ft'] if i == 7 else 0)
        o += R(90, y - 12, base * 28, 22, AC, None, 0, 3, op=0.85)
        if i == 7:
            o += R(90 + base * 28, y - 12, Q2025['Ft'] * 28, 22, COMP, None, 0, 3, op=0.85)
        o += T(96 + F[i] * 28, y + 5, f'{F[i]:.3f}', 14, AC if i < 7 else COMP, 'start', 'bold')
        o += R(480, y - 12, Vs[i] * 11, 22, KEY, None, 0, 3, op=0.8)
        o += T(486 + Vs[i] * 11, y + 5, f'{Vs[i]:.2f}', 14, KEY, 'start', 'bold')
    o += T(230, 372, f'頂層含 *F*_{{t}} = {Q2025["Ft"]:.3f}（紅）', 14, COMP, 'middle')
    o += T(680, 372, f'*M*_{{0}} = Σ*F*_{{i}}*h*_{{i}} = {Q2025["M0"]:.1f} kN·m', 14, KEY, 'middle')
    return svg(W, H, o, '2025-1 樓層力與層剪力')


def fig5_3():
    W, H = 900, 320
    pl = Plot(90, 40, 520, 240, 0, 60, 0, 2.0)
    o = pl.axes([0, 10, 20, 30, 40, 50, 60], [0, 0.5, 1, 1.5, 2], '*h*_{n} (m)', '*T* (s)')
    for (nm, c), col in zip(CT.items(), (KEY, AC, TEN)):
        o += pl.curve(lambda h, c=c: c * h ** 0.75, 0, 60, col, 2.6)
        o += T(pl.X(58), pl.Y(c * 58 ** 0.75) - 8, f'{nm} {c}', 14, col, 'end', 'bold')
    o += pl.dot(39.2, 0.070 * 39.2 ** 0.75, COMP, 6) + T(pl.X(39.2) + 8, pl.Y(0.070 * 39.2 ** 0.75) + 24, '2005-3：39.2 m → 1.097 s', 14, COMP, 'start', 'bold')
    o += box(630, 50, 260, 230, '*T* = *C*_{t}*h*_{n}^{3/4}', ['經驗式：量測統計', '鋼構架最柔 0.085', 'RC 構架 0.070', '其他（牆、斜撐）0.050', '只用來算靜力 *V*', '（動力分析另算）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '經驗週期')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
