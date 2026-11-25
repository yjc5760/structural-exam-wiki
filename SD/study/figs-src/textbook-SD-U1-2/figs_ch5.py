# -*- coding: utf-8 -*-
"""第 5 章：形狀函數、Rayleigh 上界、軸壓幾何勁度、簡支梁振態。"""
from sdfig import *  # noqa
from calcs import GEN, EXACT_CANT, Q2013_3, PI
import math

B1 = 1.8751040687
SIG = (math.cosh(B1) + math.cos(B1)) / (math.sinh(B1) + math.sin(B1))


def exact_mode(s):
    f_ = lambda x: math.cosh(B1 * x) - math.cos(B1 * x) - SIG * (math.sinh(B1 * x) - math.sin(B1 * x))
    return f_(s) / f_(1.0)


def fig5_1():
    W, H = 900, 380
    pl = Plot(120, 40, 360, 300, 0, 1.05, 0, 1)
    o = pl.axes([0, 0.5, 1], [0, 0.5, 1], 'ψ', '*x*/*L*')
    shapes = [(lambda s: s * s, '*x*²/*L*²', WARN), (lambda s: s * s * (1.5 - s / 2), 'Ψ（端點集中力撓度）', KEY),
              (lambda s: (6 * s * s - 4 * s ** 3 + s ** 4) / 3, '均佈載重撓度', TEN), (exact_mode, '真正的第 1 振態', AC)]
    for fn, nm, c in shapes:
        pts = [pl.pt(fn(i / 100), i / 100) for i in range(101)]
        o += P(pts, c, 2.6 if c != AC else 3.2, dash='7 4' if c == AC else None)
    o += fixed_wall(pl.X(0), pl.Y(0) + 2, 40)
    for i, (fn, nm, c) in enumerate(shapes):
        o += L(520, 80 + i * 40, 560, 80 + i * 40, c, 3, '7 4' if c == AC else None) + T(570, 85 + i * 40, nm, 15, c, 'start', 'bold')
    o += T(520, 270, '四條都滿足懸臂的幾何邊界：', 14.5, INK, 'start')
    o += T(520, 296, 'ψ(0) = 0、ψ′(0) = 0', 15, KEY, 'start', 'bold')
    o += T(520, 322, '端點都正規化為 1', 14.5, INK, 'start')
    return svg(W, H, o, '懸臂柱的假設形狀')


def fig5_2():
    W, H = 900, 300
    items = [('*x*²/*L*²', GEN['x²/L²']['w'], WARN), ('Ψ（集中力撓度）', GEN['Ψ（端點集中力撓度）']['w'], KEY), ('均佈載重撓度', GEN['均佈載重撓度']['w'], TEN), ('精確', EXACT_CANT, AC)]
    x0, x1, vmin, vmax = 280, 720, 3.0, 4.6
    X = lambda v: x0 + (v - vmin) / (vmax - vmin) * (x1 - x0)
    o = T(450, 26, '均勻懸臂梁（無端點質量）：ω_{1} ≈ *c*√(*EI*/*mL*⁴) 的係數 *c*', 15.5, INK, 'middle', 'bold')
    for i, (nm, v, c) in enumerate(items):
        y = 50 + i * 52
        o += T(x0 - 12, y + 26, nm, 15, c, 'end', 'bold')
        o += R(x0, y + 8, X(v) - x0, 28, c, None, 0, 4, op=0.85)
        o += T(X(v) + 8, y + 28, f'{v:.3f}（+{(v/EXACT_CANT-1)*100:.1f}%）' if c != AC else f'{v:.3f}', 15, c, 'start', 'bold')
    o += L(X(EXACT_CANT), 45, X(EXACT_CANT), 260, AC, 1.4, '5 4')
    o += T(x0, 280, f'橫軸起點 {vmin}', 14, MUT, 'start')
    return svg(W, H, o, 'Rayleigh 上界比較')


def fig5_3():
    W, H = 900, 340
    pl = Plot(90, 40, 450, 250, 0, 1, 0, 4)
    o = pl.axes([0, 0.25, 0.5, 0.75, 1], [0, 1, 2, 3, 4], '*N*/*N*_{cr}', '*T*/*T*_{0}')
    o += pl.curve(lambda n: 1 / math.sqrt(1 - n) if n < 0.999 else 9, 0, 0.97, COMP, 3)
    o += pl.curve(lambda n: 1 - n, 0, 1, AC, 2.2, dash='6 4')
    for n in (0.5, 0.75):
        v = 1 / math.sqrt(1 - n)
        o += pl.dot(n, v, KEY, 5) + T(pl.X(n) - 8, pl.Y(v) - 8, f'{v:.2f}', 15, KEY, 'end', 'bold')
    o += T(pl.X(0.05), pl.Y(0.6), '(ω/ω_{0})² = 1 − *N*/*N*_{cr}', 15, AC, 'start', 'bold')
    o += T(pl.X(0.82), pl.Y(3.6), '挫屈：*T* → ∞', 15, COMP, 'start', 'bold')
    o += box(600, 50, 290, 250, '軸壓讓柱子變軟（2002-2）', ['*k*^{*} = ∫*EI*(ψ″)² − *N*∫(ψ′)²', '正弦形狀：', '*k*^{*} = (π⁴*EI*/2*L*³)(1 − *N*/*N*_{cr})', '*N*_{cr} = π²*EI*/*L*²', '*T* = *T*_{0}/√(1 − *N*/*N*_{cr})', '勁度歸零 = 挫屈'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '軸壓與週期')


def fig5_4():
    W, H = 900, 330
    o = T(450, 26, '簡支梁的振態 φ_{n} = sin(*n*π*x*/*L*)，ω_{n} = *n*²π²√(*EI*/*mL*⁴)', 15.5, INK, 'middle', 'bold')
    for j, n in enumerate((1, 2, 3)):
        y = 90 + j * 80
        xl, xr = 120, 620
        o += L(xl, y, xr, y, GRID, 1.2)
        o += pin(xl, y + 20) if False else C(xl, y, 5, INK, INK, 1) + C(xr, y, 5, INK, INK, 1)
        pts = [(xl + (xr - xl) * i / 200, y - 30 * math.sin(n * PI * i / 200)) for i in range(201)]
        o += P(pts, [AC, KEY, COMP][j], 2.8)
        o += T(90, y + 5, f'*n* = {n}', 15, [AC, KEY, COMP][j], 'end', 'bold')
        o += T(650, y + 5, f'ω_{{{n}}} ∝ {n*n}', 15, [AC, KEY, COMP][j], 'start', 'bold')
        o += T(760, y + 5, f'中點 sin({n}π/2) = {round(math.sin(n*PI/2)):+d}' if n != 2 else '中點 = 0', 14.5, INK, 'start')
    o += T(450, 320, '中點力 *P*(*t*) 的模態力 *Q*_{n} = *P* sin(*n*π/2)：偶數振態完全不被激發（2023-1）', 14.5, MUT, 'middle')
    return svg(W, H, o, '簡支梁振態')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
