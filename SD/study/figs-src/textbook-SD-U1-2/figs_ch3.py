# -*- coding: utf-8 -*-
"""第 3 章：剪力屋單位位移、門形構架靜態濃縮、剛性樓版。"""
from sdfig import *  # noqa
from calcs import K3, portal_Kstar, PORTAL
import math


def fig3_1():
    W, H = 900, 400
    o = ''
    for j in range(3):
        x0 = 50 + j * 285
        disp = [0, 0, 0]; disp[j] = 40
        s, pts = shear_building(x0, 330, 3, bw=100, sh=85, disp=disp, klabels=['*k*', '*k*', '*k*'] if j == 0 else None)
        o += s
        o += T(x0 + 70, 26, f'令 *u*_{{{j+1}}} = 1、其他 = 0', 15.5, KEY, 'middle', 'bold')
        col = K3[:, j]
        for i in range(3):
            y = 330 - (i + 1) * 85 - 3
            v = col[i]
            if abs(v) > 1e-9:
                xr = x0 + 112 + disp[i]
                c = COMP if v > 0 else AC
                if v > 0:
                    o += A(xr + 4, y, xr + 44, y, c, 2.4, 10)
                else:
                    o += A(xr + 44, y, xr + 4, y, c, 2.4, 10)
                o += T(xr + 50, y + 5, f'{v:+.0f}*k*', 15, c, 'start', 'bold')
        o += T(x0 + 70, 380, f'第 {j+1} 欄 = [{", ".join(f"{v:.0f}" for v in col)}]*k*', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '剪力屋勁度矩陣：單位位移法')


def fig3_2():
    W, H = 900, 390
    o = T(200, 28, '門形構架三自由度（2017-2）', 16, INK, 'middle', 'bold')
    xl, xr, yb, yt = 70, 330, 330, 150
    o += fixed_wall(xl, yb, 50) + fixed_wall(xr, yb, 50)
    o += L(xl, yb, xl, yt, STEEL, 6) + L(xr, yb, xr, yt, STEEL, 6) + L(xl, yt, xr, yt, STEEL3, 9)
    o += T(xl - 10, (yb + yt) / 2, '*EI*_{1}', 15, INK, 'end') + T((xl + xr) / 2, yt + 28, '*EI*_{2}、*m*', 15, INK, 'middle')
    o += A(xr + 10, yt - 60, xr + 60, yt - 60, KEY, 2.4, 10) + T(xr + 64, yt - 55, '*v*_{1}', 15, KEY, 'start', 'bold')
    for x, n in ((xl, 2), (xr, 3)):
        o += curve_arrow([(x + 22 * math.cos(a), yt - 22 * math.sin(a)) for a in [math.radians(d) for d in range(200, 340, 10)]], WARN, 1.8)
        o += T(x + (-26 if n == 2 else 26), yt - 32, f'*v*_{{{n}}}', 15, WARN, 'end' if n == 2 else 'start', 'bold')
    o += T(200, 365, '只有 *v*_{1} 有質量；*v*_{2}、*v*_{3} 沒有轉動慣量', 14.5, MUT, 'middle')
    pl = Plot(480, 50, 300, 270, 0, 4, 0, 26)
    o += pl.axes([0, 1, 2, 3, 4], [0, 6, 12, 18, 24], 'ρ', '*K*^{*} *h*³/*EI*_{1}')
    o += pl.curve(portal_Kstar, 0, 4, KEY, 3)
    o += pl.hline(24, c=TEN, w=1.4) + pl.hline(6, c=COMP, w=1.4)
    o += T(pl.X(4), pl.Y(24) - 8, '梁無限硬：24', 14, TEN, 'end', 'bold')
    o += T(pl.X(4), pl.Y(6) + 22, '梁無勁度：6', 14, COMP, 'end', 'bold')
    o += pl.dot(1, portal_Kstar(1), KEY, 5) + T(pl.X(1) + 8, pl.Y(portal_Kstar(1)) + 22, f'ρ = 1：{portal_Kstar(1):.1f}', 14, KEY, 'start')
    o += T(800, 120, 'ρ = (*EI*_{2}/ℓ)', 14, INK, 'start') + T(800, 145, '÷ (*EI*_{1}/*h*)', 14, INK, 'start')
    return svg(W, H, o, '門形構架與靜態濃縮')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2}
