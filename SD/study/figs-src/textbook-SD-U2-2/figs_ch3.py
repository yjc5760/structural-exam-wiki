# -*- coding: utf-8 -*-
"""第 3 章：Fu 對週期、(·)m 修正。"""
from sdfig import *  # noqa
from calcs import Fu, Ra, mod
import math


def fig3_1():
    W, H = 900, 380
    R = 4.8; ra = Ra(R); s = math.sqrt(2 * ra - 1)
    pl = Plot(90, 40, 560, 280, 0, 1.6, 0, 5.2)
    o = pl.axes([0, 0.2, 0.6, 1.0, 1.6], [0, 1, 2, 3, 4, 5], '*T*/*T*_{0}^{D}', '*F*_{u}', xfmt=lambda v: f'{v:g}')
    o += pl.curve(lambda x: Fu(x, 1.0, ra), 0, 1.6, KEY, 3.2, n=400)
    o += pl.hline(R, c=MUT, w=1.2) + T(pl.X(1.58), pl.Y(R) - 8, f'*R* = {R}（若用光全部韌性）', 14, MUT, 'end')
    o += pl.hline(ra, 1.0, 1.6, TEN, 1.4) + T(pl.X(1.3), pl.Y(ra) + 22, f'等位移 *F*_{{u}} = *R*_{{a}} = {ra:.3f}', 15, TEN, 'middle', 'bold')
    o += T(pl.X(0.4), pl.Y(s) - 12, f'等能量 √(2*R*_{{a}}−1) = {s:.3f}', 15, WARN, 'middle', 'bold')
    o += T(pl.X(0.02), pl.Y(1) + 22, '*T* → 0：*F*_{u} = 1', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.8), pl.Y(2.9), '線性內插', 14, MUT, 'middle')
    o += box(665, 40, 225, 300, 'RC 特殊抗彎構架 *R* = 4.8', [f'*R*_{{a}} = 1 + 3.8/1.5 = {ra:.3f}', '極短週期：跟著地面動', '→ 不能折減', '中週期：等能量', '長週期：等位移', '設計地震只准用', '2/3 的「降伏後」韌性', '（臺北盆地 1/2）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'Fu 隨週期')


def fig3_2():
    W, H = 900, 330
    pl = Plot(90, 40, 520, 250, 0, 1.2, 0, 1.2)
    o = pl.axes([0, 0.3, 0.8, 1.2], [0, 0.3, 0.56, 0.84, 1.2], '*S*_{aD}/*F*_{u}', '(*S*_{aD}/*F*_{u})_{m}', yfmt=lambda v: f'{v:.2f}')
    o += pl.curve(lambda x: x, 0, 1.2, MUT, 1.4, dash='6 4')
    o += pl.curve(mod, 0, 1.2, KEY, 3.2, n=400)
    o += pl.dot(0.3, 0.3, COMP, 5) + pl.dot(0.8, 0.56, COMP, 5)
    o += T(pl.X(0.3) + 8, pl.Y(0.3) + 22, '0.3：不修正', 14, COMP, 'start')
    o += T(pl.X(0.8) + 8, pl.Y(0.56) + 22, '0.8：打 7 折', 14, COMP, 'start')
    o += T(pl.X(1.0), pl.Y(1.05), '不修正（虛線）', 14, MUT, 'middle')
    o += box(630, 50, 260, 240, '(·)_{m} 三段', ['≤ 0.3：原值', '0.3～0.8：0.52*x* + 0.144', '≥ 0.8：0.70*x*', '接點：0.52(0.3)+0.144 = 0.3 ✔', '0.52(0.8)+0.144 = 0.56 ✔', '非彈性越深 → 遲滯消能', '→ 等效阻尼 > 5%'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '(SaD/Fu)m 修正')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
