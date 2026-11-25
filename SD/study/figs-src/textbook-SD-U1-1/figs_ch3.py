# -*- coding: utf-8 -*-
"""第 3 章：相量三角形、Rd 與相位、傳導率、TMD。"""
from sdfig import *  # noqa
from calcs import Rd, phase, TR, EX, H, Q2009, TMD, TMDR, tmd_response, PI
import math


def _phasor(ox, r, xi, title, scale):
    """相量圖：kU（右）、mω̄²U（左，下移一層）、cω̄U（上），合力 p0（紅）。以 p0 = 1、p0/k = 1 為準。"""
    U = Rd(r, xi)
    kU = U; mU = r * r * U; cU = 2 * xi * r * U
    o = T(ox + 140, 30, title, 16, INK, 'middle', 'bold')
    y0 = 260
    x0 = ox + 140 - (kU - mU) * scale / 2
    x1 = x0 + kU * scale
    x2 = x1 - mU * scale
    y2 = y0 - cU * scale
    dy = 14
    o += A(x0, y0, x1, y0, AC, 3, 12)
    o += L(x1, y0, x1, y0 + dy, MUT, 1, '3 3')
    o += A(x1, y0 + dy, x2, y0 + dy, KEY, 3, 12)
    o += L(x2, y0 + dy, x2, y0, MUT, 1, '3 3')
    o += A(x2, y0, x2, y2, TEN, 3, 12)
    off = -10 if abs(x2 - x0) < 5 else 0
    o += A(x0 + off, y0, x2 + off, y2, COMP, 3.4, 13)
    o += T((x0 + x1) / 2, y0 - 8, '*kU*', 15, AC, 'middle', 'bold')
    o += T((x1 + x2) / 2, y0 + dy + 24, '*m*ω̄²*U*', 15, KEY, 'middle', 'bold')
    o += T(x2 + 8, (y0 + y2) / 2 + 6, '*c*ω̄*U*', 15, TEN, 'start', 'bold')
    o += T((x0 + x2) / 2 + off - 10, (y0 + y2) / 2 - 8, '*p*_{0}', 16, COMP, 'end', 'bold')
    o += T(ox + 140, 330, f'*U*/(*p*_{{0}}/*k*) = {U:.2f}', 15, INK, 'middle')
    o += T(ox + 140, 356, f'相位 φ = {math.degrees(phase(r, xi)):.0f}°', 15, INK, 'middle')
    return o


def fig3_1():
    W, H_ = 900, 380
    xi = 0.3
    o = _phasor(0, 0.5, xi, '(a) *r* = 0.5：彈簧主撐', 150)
    o += L(300, 20, 300, 370, GRID, 1.5)
    o += _phasor(300, 1.0, xi, '(b) *r* = 1：只剩阻尼擋', 92)
    o += L(600, 20, 600, 370, GRID, 1.5)
    o += _phasor(600, 2.0, xi, '(c) *r* = 2：慣性主撐', 160)
    return svg(W, H_, o, '相量三角形')


def fig3_2():
    W, H_ = 900, 470
    pl = Plot(90, 40, 520, 250, 0, 3, 0, 11)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5, 3], [0, 2, 4, 6, 8, 10], '*r*', '*R*_{d}')
    cols = {0.05: COMP, 0.1: KEY, 0.2: AC, 0.5: TEN, 0.707: WARN}
    for xi, c in cols.items():
        o += pl.curve(lambda r, xi=xi: Rd(r, xi), 0, 3, c, 2.4, n=600)
    o += pl.hline(1, c=MUT, w=1.2)
    o += T(pl.X(1.05), pl.Y(10.2), 'ξ = 0.05（峰值 10）', 15, COMP, 'start', 'bold')
    o += T(pl.X(1.1), pl.Y(5.0), '0.1（5）', 15, KEY, 'start', 'bold')
    o += T(pl.X(1.2), pl.Y(2.8), '0.2（2.5）', 15, AC, 'start', 'bold')
    o += T(pl.X(0.36), pl.Y(1.75), '0.5', 15, TEN, 'start', 'bold')
    o += T(pl.X(0.15), pl.Y(0.4), '0.707', 15, WARN, 'start', 'bold')
    o += T(pl.X(2.2), pl.Y(1.6), '→ 1/*r*²（質量不跟）', 15, INK, 'middle')
    o += T(pl.X(0.02), pl.Y(1) - 8, '靜力 = 1', 14, MUT, 'start')
    # 相位小圖
    p2 = Plot(90, 345, 520, 90, 0, 3, 0, 180)
    o += p2.axes([0, 1, 2, 3], [0, 90, 180], '*r*', '', size=14)
    o += T(70, 330, 'φ（度）', 15, INK, 'start')
    for xi, c in ((0.05, COMP), (0.2, AC), (0.707, WARN)):
        o += p2.curve(lambda r, xi=xi: math.degrees(phase(r, xi)), 0, 3, c, 2.2, n=400)
    o += box(650, 60, 235, 240, '共振 *r* = 1', ['彈簧與慣性抵銷', '*R*_{d} = 1/(2ξ)', 'ξ = 0.05 → 10 倍', '相位剛好 90°', '（不論 ξ 多少）'], KEY2, KEY, 16, 15)
    o += box(650, 320, 235, 120, '三段', ['*r* ≪ 1：靠勁度', '*r* ≈ 1：靠阻尼', '*r* ≫ 1：靠質量'], AC2, AC, 15, 15)
    return svg(W, H_, o, '動力放大因子與相位')


def fig3_3():
    W, H_ = 900, 400
    pl = Plot(90, 40, 560, 300, 0, 3.5, 0, 4)
    o = pl.axes([0, 0.5, 1, math.sqrt(2), 2, 2.5, 3, 3.5], [0, 1, 2, 3, 4], '*r*', '*TR*', xfmt=lambda t: '√2' if abs(t - math.sqrt(2)) < 1e-6 else f(t))
    o += pl.area(lambda r: 4, lambda r: 0, math.sqrt(2), 3.5, TEN2, 0.6)
    for xi, c in ((0.0, COMP), (0.1, KEY), (0.3, AC), (0.7, TEN)):
        o += pl.curve(lambda r, xi=xi: TR(r, xi) if abs(1 - r * r) > 1e-3 or xi > 0 else 9, 0, 3.5, c, 2.4, n=800)
    o += pl.vline(math.sqrt(2), c=KEY, w=1.6)
    o += pl.hline(1, c=MUT, w=1.2)
    o += pl.dot(math.sqrt(2), 1, KEY, 6)
    o += T(pl.X(2.6), pl.Y(3.6), '隔振區 *TR* < 1', 16, TEN, 'middle', 'bold')
    o += T(pl.X(2.45), pl.Y(0.36) - 8, 'ξ = 0', 15, COMP, 'start', 'bold')
    o += T(pl.X(2.9), pl.Y(0.62), '0.3', 15, AC, 'start', 'bold')
    o += T(pl.X(3.0), pl.Y(0.95) - 10, '0.7', 15, TEN, 'start', 'bold')
    o += T(pl.X(1.17), pl.Y(3.0), '0.1', 15, KEY, 'start', 'bold')
    o += T(pl.X(Q2009['r']) if Q2009['r'] < 3.5 else 0, 0, '', 14)
    o += R(670, 60, 220, 250, KEY2, KEY, 1.4, 8)
    o += T(780, 88, '*r* = √2 必過 *TR* = 1', 15, KEY, 'middle', 'bold')
    o += T(780, 118, '（與 ξ 無關）', 15, INK, 'middle')
    o += T(780, 152, '*r* < √2：裝彈簧', 15, INK, 'middle')
    o += T(780, 178, '反而放大傳力', 15, INK, 'middle')
    o += T(780, 212, '*r* > √2：阻尼越大', 15, INK, 'middle')
    o += T(780, 238, '傳力反而越大', 15, INK, 'middle')
    o += T(780, 278, '2009-2：*r* = √15', 15, COMP, 'middle', 'bold')
    return svg(W, H_, o, '傳導率')


def fig3_4():
    W, H_ = 900, 380
    pl = Plot(90, 40, 560, 280, 0.7, 1.3, 0, 26)
    o = pl.axes([0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3], [0, 5, 10, 15, 20, 25], '*r*', '主結構 *U*/(*p*_{0}/*K*)')
    o += pl.curve(lambda r: tmd_response(r, with_tmd=False), 0.7, 1.3, MUT, 2.2, n=600, dash='7 5')
    o += pl.curve(lambda r: tmd_response(r), 0.7, 1.3, KEY, 3, n=600)
    o += T(pl.X(1.02), pl.Y(24.5), f'無 TMD：峰值 {TMDR["peak_without"]:.0f}', 15, MUT, 'start', 'bold')
    o += T(pl.X(1.1), pl.Y(7.5), f'加 TMD：兩個矮峰 {TMDR["peak_with"]:.1f}', 15, KEY, 'start', 'bold')
    m = TMD[0.05]
    o += box(670, 60, 220, 250, 'μ = 0.05（主結構 ξ = 2%）', [f'*f*_{{opt}} = 1/(1+μ) = {m["f"]:.3f}', f'ξ_{{d,opt}} = {m["xi"]:.3f}', '原本一個高峰', '被拆成兩個矮峰', '小質量的彈簧力', '抵銷外力'], KEY2, KEY, 14, 15)
    return svg(W, H_, o, 'TMD 頻率反應')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
