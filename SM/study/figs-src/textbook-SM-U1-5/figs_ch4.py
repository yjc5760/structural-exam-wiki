# -*- coding: utf-8 -*-
"""第 4 章：活塞模型、飽和 UU、由 φ′ 推 Su。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import circle


def _piston(x, y, label, shear=False):
    o = R(x, y, 150, 200, '#fff', INK, 2)
    o += R(x + 3, y + 60, 144, 137, ACM, None, 0, op=0.7)
    o += R(x - 10, y + 40, 170, 20, STEEL3, INK, 1.6)
    # 彈簧（鋸齒）
    pts = []
    for i in range(13):
        pts.append((x + 75 + (14 if i % 2 else -14), y + 64 + i * 10.5))
    o += P([(x + 75, y + 60)] + pts + [(x + 75, y + 197)], TEN, 2.4)
    o += A(x + 75, y - 30, x + 75, y + 36, COMP, 3, 12)
    o += T(x + 85, y - 10, 'Δ*σ*', 16, COMP, 'start', 'bold')
    # 閥
    o += L(x + 150, y + 170, x + 190, y + 170, INK, 3) + C(x + 175, y + 170, 9, COMP2, COMP, 2)
    o += L(x + 175, y + 162, x + 175, y + 178, COMP, 3)
    o += T(x + 195, y + 175, '閥關', 14, COMP, 'start', 'bold')
    o += T(x + 20, y + 120, '水', 16, AC, 'start', 'bold')
    o += T(x + 98, y + 150, '骨架', 15, TEN, 'start', 'bold')
    o += T(x + 75, y + 232, label, 15, INK, 'middle', 'bold')
    return o


def fig4_1():
    W, H = 900, 440
    o = _piston(70, 90, '(a) 等向加壓：Δ*u*=*B*Δ*σ*_{3}，*B*≈1')
    o += _piston(470, 90, '(b) 剪切：Δ*u* 再加 *AB*Δ*q*')
    o += T(545, 360, '鬆土想縮→擠水→*A*>0', 14, TEN, 'middle')
    o += T(545, 382, '密土想脹→吸水→*A*<0', 14, AC, 'middle')
    o += box(720, 70, 170, 150, '水比骨架硬', ['不排水時', '壓力先給水', '骨架（*σ*′）', '幾乎不變'], KEY2, KEY)
    return svg(W, H, o, '活塞模型')


def fig4_2():
    W, H = 900, 400
    pl = Plot(80, 60, 600, 270, 0, 400, 0, 180)
    o = pl.axes([0, 100, 200, 300, 400], [0, 50, 100, 150], '*σ* (kPa)', '*τ*')
    Su = 45.0
    o += circle(pl, 2 * Su + 20, 20, TEN, 3)
    for s3 in (0, 100, 200, 300):
        o += circle(pl, s3 + 2 * Su, s3, COMP, 2.2, '7 4')
    o += L(pl.X(0), pl.Y(Su), pl.X(400), pl.Y(Su), WARN, 2.6)
    o += T(pl.X(395), pl.Y(Su) - 10, '*τ*_{f}=*c*_{u}=*S*_{u}（*φ*_{u}=0）', 15, WARN, 'end', 'bold')
    o += T(pl.X(45), pl.Y(Su) + 28, '有效應力圓（共同一個）', 14, TEN, 'start', 'bold')
    o += T(pl.X(0) + 6, pl.Y(0) + 40, '單壓 *σ*_{3}=0 → *S*_{u}=*q*_{u}/2', 14, COMP, 'start', 'bold')
    o += box(700, 70, 185, 140, '圍壓全給水', ['*B*=1', '*σ*′ 不變', '→ 圓一樣大', '→ 切線水平'], KEY2, KEY)
    return svg(W, H, o, '飽和 UU')


def fig4_3():
    W, H = 900, 420
    sv0, phi = 100.0, 30.0
    pl = Plot(80, 50, 560, 300, 0, 320, 0, 320 * 300 / 560)
    o = pl.axes([0, 50, 100, 150, 200, 250, 300], [0, 50, 100, 150], "*σ*′", '*τ*')
    o += L(pl.X(0), pl.Y(0), pl.X(300), pl.Y(300 * tan(phi)), WARN, 2.4)
    o += pl.vline(sv0, 0, 150, MUT, 1.3) + T(pl.X(sv0), pl.Y(0) + 40, '*σ*_{v0}′', 15, INK, 'middle', 'bold')
    cols = [(1.0, COMP), (0.5, KEY), (0.0, AC)]
    for Af, c in cols:
        Su = su_from_phi(sv0, phi, Af)
        s1 = sv0 + 2 * (1 - Af) * Su
        s3 = sv0 - 2 * Af * Su
        o += circle(pl, s1, s3, c, 2.6)
        k = cols.index((Af, c))
        o += L(668, 250 + k * 28, 692, 250 + k * 28, c, 3) + T(698, 255 + k * 28, f'*A*_{{f}}={Af:g}：比值 {Su / sv0:.2f}', 14, c, 'start', 'bold')
    o += box(690, 50, 200, 160, '同一起點', ['*A*_{f}=1：*σ*_{1}′ 固定', '*A*_{f}=0.5：圓心固定', '*A*_{f}=0：*σ*_{3}′ 固定', '擠水越多越弱'], KEY2, KEY)
    return svg(W, H, o, '由 φ′ 推 Su')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
