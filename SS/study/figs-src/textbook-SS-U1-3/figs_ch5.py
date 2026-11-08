# -*- coding: utf-8 -*-
"""第 5 章：G 值、梁遠端修正、對位圖方程式逐點解。"""
from plot import *  # noqa
from calcs import K_sway, K_braced, ex2013, FAR_END
import math


def _arc(cx, cy, r, a0, a1, c, w=2.6):
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / 24)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / 24))) for i in range(25)]
    return curve_arrow(pts, c, w, 11)


def fig5_1():
    W_, H = 900, 380
    o = T(220, 32, '節點上的蹺蹺板', 16, INK, 'middle', 'bold')
    cx, cy = 220, 190
    o += L(cx, cy - 130, cx, cy + 130, AC, 7)          # 柱
    o += L(cx - 170, cy, cx + 170, cy, STEEL, 9)       # 梁
    o += C(cx, cy, 9, '#fff', INK, 2)
    o += _arc(cx, cy, 52, 200, 330, COMP, 3)
    o += T(cx - 60, cy - 60, '柱想轉', 15, COMP, 'end', 'bold')
    o += _arc(cx, cy, 52, 20, -100, TEN, 3)
    o += T(cx + 62, cy + 70, '梁擋住', 15, TEN, 'start', 'bold')
    o += T(cx + 14, cy - 110, '柱 Σ*EI*/*L*', 14, AC, 'start')
    o += T(cx + 100, cy - 14, '梁 Σ*EI*/*L*', 14, MUT, 'middle')
    o += L(450, 20, 450, 370, GRID, 1.5)
    o += R(470, 50, 415, 120, KEY2, KEY, 1.6, 10)
    o += T(677, 84, '*G* = Σ(*I*/*L*)_{柱} ÷ Σ(*I*/*L*)_{梁}', 17, KEY, 'middle', 'bold')
    o += T(677, 116, '分子是想推歪的（柱），分母是擋住的（梁）', 14, INK, 'middle')
    o += T(677, 144, '同一節點、上下柱與左右梁都要加', 14, MUT, 'middle')
    o += R(470, 190, 200, 160, TEN2, TEN, 1.4, 8)
    o += T(570, 218, '*G* → 0', 16, TEN, 'middle', 'bold')
    o += T(570, 246, '梁無限硬 ⇒ 固接', 14, INK, 'middle')
    o += T(570, 276, '設計取 *G* = 1.0', 15, TEN, 'middle', 'bold')
    o += T(570, 302, '（真實基礎不會全固）', 14, MUT, 'middle')
    o += R(685, 190, 200, 160, COMP2, COMP, 1.4, 8)
    o += T(785, 218, '*G* → ∞', 16, COMP, 'middle', 'bold')
    o += T(785, 246, '沒有梁 ⇒ 鉸接', 14, INK, 'middle')
    o += T(785, 276, '設計取 *G* = 10', 15, COMP, 'middle', 'bold')
    o += T(785, 302, '（真實鉸接仍有摩擦）', 14, MUT, 'middle')
    return svg(W_, H, o, 'G 值')


def _hermite(t, th1, th2):
    """長度 1 的梁，兩端撓度 0、轉角 th1、th2 的形狀。"""
    return th1 * (t - 2 * t * t + t ** 3) + th2 * (-t * t + t ** 3)


def _beam(ox, oy, th_far, label, coef, ratio, c, far):
    o = ''
    Lp = 170
    o += L(ox, oy, ox + Lp, oy, MUT, 1, '5 4')
    pts = [(ox + Lp * i / 60, oy - 70 * _hermite(i / 60, 1.0, th_far)) for i in range(61)]
    o += P(pts, c, 4)
    o += C(ox, oy, 6, '#fff', INK, 1.6)
    if far == 'pin':
        o += pin(ox + Lp, oy + 2, s=9)
    elif far == 'fix':
        o += L(ox + Lp, oy - 22, ox + Lp, oy + 22, INK, 3)
        for i in range(5):
            o += L(ox + Lp, oy - 20 + i * 10, ox + Lp + 7, oy - 26 + i * 10, INK, 1)
    o += T(ox + Lp / 2, oy + 44, label, 14, INK, 'middle')
    o += T(ox + Lp / 2, oy + 68, f'{coef}*EI*/*L*', 16, c, 'middle', 'bold')
    if ratio:
        o += T(ox + Lp / 2, oy + 92, ratio, 15, KEY, 'middle', 'bold')
    return o


def fig5_2():
    W_, H = 900, 480
    o = T(30, 36, '有側移對位圖', 16, AC, 'start', 'bold')
    o += T(30, 58, '假設梁兩端同向轉（S 形）', 14, MUT, 'start')
    o += _beam(40, 140, 1.0, '假設：遠端同轉', FAR_END['sway_assumed'], '基準', AC, None)
    o += _beam(330, 140, -0.5, '遠端鉸接', FAR_END['sway_far_pin'], '× 1/2', AC, 'pin')
    o += _beam(620, 140, 0.0, '遠端固接', FAR_END['sway_far_fixed'], '× 2/3', AC, 'fix')
    o += L(20, 250, 880, 250, GRID, 1.5)
    o += T(30, 280, '無側移對位圖', 16, COMP, 'start', 'bold')
    o += T(30, 302, '假設梁兩端反向轉（一個弧）', 14, MUT, 'start')
    o += _beam(40, 370, -1.0, '假設：遠端反轉', FAR_END['braced_assumed'], '基準', COMP, None)
    o += _beam(330, 370, -0.5, '遠端鉸接', FAR_END['braced_far_pin'], '× 1.5', COMP, 'pin')
    o += _beam(620, 370, 0.0, '遠端固接', FAR_END['braced_far_fixed'], '× 2', COMP, 'fix')
    return svg(W_, H, o, '梁遠端修正')


LOGT = [0.1, 0.2, 0.5, 1, 2, 5, 10, 50]


def fig5_3():
    d = ex2013()
    W_, H = 900, 460
    lg = math.log10
    pl = Plot(90, 50, 560, 340, lg(0.1), lg(50), 0.4, 3.4)
    o = pl.axes([lg(t) for t in LOGT], [0.5, 1.0, 1.5, 2.0, 2.5, 3.0], '*G*', '*K*', size=14,
                xfmt=lambda t: f(round(10 ** t, 2)))
    def cv(fn, c, w, dash=None):
        pts = []
        for i in range(121):
            x = lg(0.1) + (lg(50) - lg(0.1)) * i / 120
            k = fn(10 ** x)
            if k > 3.35:
                break
            pts.append(pl.pt(x, k))
        return P(pts, c, w, dash=dash)
    o += cv(lambda G: K_sway(G, G), AC, 3.4)
    o += cv(lambda G: K_sway(G, 10), AC, 2.2, '8 5')
    o += cv(lambda G: K_braced(G, G), COMP, 3.4)
    o += pl.hline(1.0, c=INK, w=1.2)
    o += pl.dot(lg(d['G_B']), d['K'], KEY, 6) + pl.dot(lg(d['G_B_raw']), d['K_raw'], MUT, 5)
    o += T(pl.X(lg(d['G_B'])) - 4, pl.Y(2.32), f'2013-4：*G*_{{B}} = 1.5 → *K* = {d["K"]:.2f}', 14, KEY, 'end', 'bold')
    o += T(pl.X(lg(d['G_B_raw'])) - 8, pl.Y(d['K_raw']) - 12, f'未修正 0.75 → {d["K_raw"]:.2f}', 14, MUT, 'end')
    o += T(pl.X(lg(40)), pl.Y(3.25), '有側移', 14, AC, 'end', 'bold')
    o += T(pl.X(lg(40)), pl.Y(1.12), '無側移', 14, COMP, 'end', 'bold')
    lx = 668
    o += R(lx, 60, 222, 132, '#fff', GRID, 1.2, 8)
    o += L(lx + 12, 88, lx + 52, 88, AC, 3.4) + T(lx + 60, 93, '有側移 *G*_{A} = *G*_{B}', 14, AC, 'start')
    o += L(lx + 12, 122, lx + 52, 122, AC, 2.2, '8 5') + T(lx + 60, 127, '有側移 *G*_{B} = 10', 14, AC, 'start')
    o += L(lx + 12, 156, lx + 52, 156, COMP, 3.4) + T(lx + 60, 161, '無側移 *G*_{A} = *G*_{B}', 14, COMP, 'start')
    o += R(lx, 210, 222, 150, KEY2, KEY, 1.4, 8)
    o += T(lx + 111, 236, '四個端點', 15, KEY, 'middle', 'bold')
    o += T(lx + 111, 262, '無側移：0.5 ～ 1.0', 14, INK, 'middle')
    o += T(lx + 111, 288, '有側移：1.0 ～ ∞', 14, INK, 'middle')
    o += T(lx + 111, 318, '*G* 越大（梁越軟）', 14, INK, 'middle')
    o += T(lx + 111, 342, '*K* 越大', 14, INK, 'middle')
    return svg(W_, H, o, 'K–G 曲線')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
