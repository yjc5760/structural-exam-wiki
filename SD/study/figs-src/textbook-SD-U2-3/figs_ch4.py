# -*- coding: utf-8 -*-
"""第 4 章：三軸反應譜上的規範譜。"""
from sdfig import *  # noqa
from calcs import SPEC, PI
import math

G = 9.81


def code_Sa(T):
    SDS, SD1 = SPEC['SDS'], SPEC['SD1']; T0 = SD1 / SDS
    if T <= 0.2 * T0:
        return SDS * (0.4 + 3 * T / T0)
    if T <= T0:
        return SDS
    return SD1 / T


def fig4_1():
    W, H = 900, 420
    pl = Plot(90, 40, 560, 320, -2, 1, -3, 0.5)
    o = pl.axes([-2, -1, 0, 1], [-3, -2, -1, 0], '*T* (s)', '*S*_{v} (m/s)', xfmt=lambda t: f'{10**t:g}', yfmt=lambda t: f'{10**t:g}')

    def seg(c0, sl, col):
        xa = max(pl.xmin, (pl.ymin - c0) / sl if sl > 0 else (pl.ymax - c0) / sl)
        xb = min(pl.xmax, (pl.ymax - c0) / sl if sl > 0 else (pl.ymin - c0) / sl)
        return L(pl.X(xa), pl.Y(c0 + sl * xa), pl.X(xb), pl.Y(c0 + sl * xb), col, 1.1, '5 4') if xb > xa else ''
    for Sd in (1e-4, 1e-3, 1e-2, 1e-1, 1.0):
        o += seg(math.log10(2 * PI * Sd), -1, AC)
    for Sa in (0.1, 1, 10, 100):
        o += seg(math.log10(Sa / (2 * PI)), 1, COMP)
    T0 = SPEC['SD1'] / SPEC['SDS']
    sv = lambda x: math.log10(code_Sa(10 ** x) * G * 10 ** x / (2 * PI))
    cols = [(-2, math.log10(0.2 * T0), TEN), (math.log10(0.2 * T0), math.log10(T0), KEY), (math.log10(T0), 1, WARN)]
    for a, b, c in cols:
        o += pl.curve(sv, a, b, c, 3.4, n=200)
    o += T(pl.X(-1.85), pl.Y(-2.0), '較短週期（上升）', 14, TEN, 'start', 'bold')
    o += T(pl.X(-0.55), pl.Y(-1.0), '*S*_{a} 定值：斜率 +1', 14, KEY, 'middle', 'bold')
    o += T(pl.X(0.55), pl.Y(0.05), '*S*_{v} 定值：水平', 14, WARN, 'middle', 'bold')
    o += T(pl.X(0.97), pl.Y(-2.7), '藍虛：等 *S*_{d}（斜率 −1）', 14, AC, 'end')
    o += T(pl.X(-1.97), pl.Y(0.38), '紅虛：等 *S*_{a}（斜率 +1）', 14, COMP, 'start')
    o += box(665, 40, 225, 330, '取對數變加減', ['*S*_{v} = *TS*_{a}/2π', '→ log*S*_{v} = log*T* + log*S*_{a} − log2π', '*S*_{v} = 2π*S*_{d}/*T*', '→ log*S*_{v} = −log*T* + …', '所以四個量畫在', '同一張圖上', 'Newmark：', 'b–c *S*_{a} 定值', 'c–d *S*_{v} 定值', 'd–e *S*_{d} 定值', '規範譜沒有 d–e 段'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '三軸反應譜與規範譜')


ALL = {'fig4_1': fig4_1}
