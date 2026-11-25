# -*- coding: utf-8 -*-
"""第 4 章：反應譜取值、振態樓層力、有效質量。"""
from sdfig import *  # noqa
from calcs import EX, Sa_2022, G
import math


def fig4_1():
    W, H = 900, 340
    pl = Plot(90, 40, 520, 250, 0, 3.5, 0, 0.8)
    o = pl.axes([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5], [0, 0.2, 0.4, 0.6, 0.8], '*T* (s)', '*S*_{a} (*g*)')
    o += pl.curve(lambda t: Sa_2022(max(t, 1e-3)) / G, 0.0, 3.5, KEY, 3, n=500)
    for n, c in ((0, AC), (1, COMP)):
        t, s = EX['T'][n], EX['Sa_g'][n]
        o += pl.dot(t, s, c, 6) + pl.vline(t, 0, s, c)
        o += T(pl.X(t) + (8 if n else -8), pl.Y(s) - 10, f'*T*_{{{n+1}}} = {t:.3f}：{s:.4f}*g*', 15, c, 'start' if n else 'end', 'bold')
    o += T(pl.X(0.65), pl.Y(0.74), '上限 0.7*g*（*T* < 0.643 s）', 14, KEY, 'start')
    o += box(630, 50, 260, 250, '取值與換算', [f'*S*_{{a1}} = {EX["Sa"][0]:.3f} m/s²', f'*S*_{{a2}} = {EX["Sa"][1]:.3f} m/s²', '*S*_{d} = *S*_{a}/ω²：', f'*S*_{{d1}} = {EX["Sd"][0]:.4f} m', f'*S*_{{d2}} = {EX["Sd"][1]:.4f} m', '兩個 *T* 都在 0.45*g*/*T* 段', '上限不控制'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '反應譜取值')


def _bldg(ox, n, title, c):
    F = EX['F'][:, n]; U = EX['U'][:, n]
    s, pts = shear_building(ox, 330, 2, bw=100, sh=110, disp=[U[0] * 120, U[1] * 120], mc=c, mfill='#fff')
    o = T(ox + 60, 28, title, 15.5, c, 'middle', 'bold') + s
    for i, (x, y) in enumerate(pts):
        f_ = F[i]
        L_ = 60 * f_ / 200
        xr = x + 70
        if f_ >= 0:
            o += A(xr, y, xr + L_, y, c, 2.6, 11)
        else:
            o += A(xr - L_, y, xr, y, c, 2.6, 11)
        o += T(xr + abs(L_) + 6 if f_ >= 0 else xr + 6, y - 8, f'{f_:.1f}', 15, c, 'start', 'bold')
        o += T(x - 70, y + 5, f'{U[i]*100:.2f} cm', 14, MUT, 'end')
    return o


def fig4_2():
    W, H = 900, 380
    o = _bldg(110, 0, '第 1 振態：樓層力 (kN)', AC)
    o += L(430, 20, 430, 370, GRID, 1.5)
    o += _bldg(540, 1, '第 2 振態：樓層力 (kN)', COMP)
    o += T(450, 368, '左側灰字：該振態的樓層位移；箭頭：*f*_{n} = Γ_{n}*M*φ_{n}*S*_{an}', 14, MUT, 'middle')
    return svg(W, H, o, '各振態樓層力')


def fig4_3():
    W, H = 900, 210
    o = T(450, 28, '有效質量：誰被地震「點名」', 16, INK, 'middle', 'bold')
    x0, wtot = 120, 660
    r1 = EX['Meff_ratio'][0]
    o += R(x0, 60, wtot * r1, 50, AC, None, 0, 4) + R(x0 + wtot * r1, 60, wtot * (1 - r1), 50, COMP, None, 0, 4)
    o += T(x0 + wtot * r1 / 2, 92, f'第 1 振態 {EX["Meff"][0]:.1f} t（{r1*100:.1f}%）', 16, '#fff', 'middle', 'bold')
    o += T(x0 + wtot + 10, 92, f'{EX["Meff"][1]:.1f} t（{(1-r1)*100:.1f}%）', 15, COMP, 'start', 'bold')
    o += T(450, 150, f'Σ*M*^{{eff}} = {EX["sum_Meff"]:.0f} t = 總質量 200 t ✔', 16, KEY, 'middle', 'bold')
    o += T(450, 182, '規範：取到累計 ≥ 90%（本例第 1 振態就夠，但仍常兩個都算）', 14.5, MUT, 'middle')
    return svg(W, H, o, '有效質量')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
