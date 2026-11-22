# -*- coding: utf-8 -*-
"""第 11 章：等效載重與載重平衡。"""
from figs_ps import *  # noqa
from calcs import rc2020_4

RR = rc2020_4()


def fig11_1():
    W, H = 900, 420
    o = T(450, 26, '種子 P5：把鋼腱拿掉，換成它推混凝土的力（簡支、兩端在形心、下垂量 *f*）', 16, INK, 'middle', 'bold')
    x0, x1, yg = 120, 680, 200
    o += R(x0, yg - 50, x1 - x0, 100, STEEL2, INK, 1.4)
    o += L(x0 - 10, yg, x1 + 10, yg, KEY, 1.2, '6 4')
    f = 40
    pts = [(x0 + (x1 - x0) * i / 60, yg + 4 * f * (i / 60) * (1 - i / 60)) for i in range(61)]
    o += P(pts, TEN, 3, dash='7 4')
    o += vdim(400 + 30, yg, yg + f, '*f*', TEN, 1)
    for i in range(1, 14):
        xx = x0 + (x1 - x0) * i / 14
        o += A(xx, yg + 90, xx, yg + 54, COMP, 1.8, 8)
    o += T(400, yg + 118, '*w*_{p} = 8*Pf*/*L*^{2}（向上、均布）', 16, COMP, 'middle', 'bold')
    for xe, s in ((x0, 1), (x1, -1)):
        o += A(xe - 60 * s, yg, xe - 4 * s, yg, KEY, 3, 11)
        o += A(xe, yg - 70, xe, yg - 54, KEY, 2.4, 10)
    o += T(x0 - 64, yg - 10, '*P* cosθ', 15, KEY, 'end', 'bold')
    o += T(x0 + 10, yg - 76, '*P* sinθ', 14, KEY, 'start', 'bold')
    o += box(700, 120, 190, 220, '自成平衡', ['向上：*w*_{p}·*L*', '= 8*Pf*/*L*', '向下：2*P* sinθ', '≈ 2*P*·4*f*/*L*', '= 8*Pf*/*L* ✔', '（不需要支承）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '等效載重')


def fig11_2():
    W, H = 900, 420
    o = T(450, 26, 'RC-2020-4：鋼腱形狀 × *P*_{e} 和外載彎矩圖一模一樣 → 全斷面只受均勻軸壓', 16, INK, 'middle', 'bold')
    pl = Plot(110, 70, 600, 280, 0, 3000, 40, -40)
    o += pl.axes([0, 750, 1500, 2250, 3000], [-40, -20, 0, 20, 40], '*x*（cm）', '*e*（cm，下為正）', yfmt=lambda v: f'{v:g}'.replace('-', '−'), size=14)
    L = 1500.0; w = 16.0; Pe = RR['Pe']
    def Mext(x):
        xx = x if x <= L else 2 * L - x
        return 3 * w * L / 8 * xx - w * xx ** 2 / 2
    def e(x):
        xx = x if x <= L else 2 * L - x
        # 通過 (0,0)、(L/2,17.5)、(L,-35) 的拋物線
        a = (-35 - 2 * 2 * 17.5) / L ** 2 * 1.0
        # 用三點：e = A x^2 + B x
        A_ = (2 * (-35) - 4 * 17.5) / L ** 2
        B_ = (4 * 17.5 - (-35)) / L
        return A_ * xx ** 2 + B_ * xx
    o += pl.curve(lambda x: Mext(x) / Pe, 0, 3000, COMP, 6, clip=False, op=0.35)
    o += pl.curve(e, 0, 3000, TEN, 2.6, clip=False)
    for x, lab in ((0, 'A'), (750, 'D'), (1500, 'B'), (2250, 'E'), (3000, 'C')):
        o += T(pl.X(x) + (12 if x == 0 else 0), pl.Y(0) - 10, lab, 15, INK, 'middle', 'bold')
    o += pl.dot(750, 17.5, TEN, 6)
    o += T(pl.X(750), pl.Y(17.5) + 24, '*e*_{D} = 17.5（跨中）', 14, TEN, 'middle', 'bold')
    o += T(pl.X(1500) + 10, pl.Y(-35) - 4, '*e*_{B} = −35', 14, TEN, 'start', 'bold')
    o += box(730, 80, 160, 280, '對照', ['綠細線：鋼腱 *e*(*x*)', '粉粗線：*M*_{ext}/*P*_{e}', '兩者重合', '', f"*P*_{{e}} = 45/0.35", f"= {RR['Pe']/1000:.1f} tf", f"*e*_{{D}} = 22.5/{RR['Pe']/1000:.1f}", f"= {RR['eD']:.1f} cm"], KEY2, KEY, 15, 14)
    return svg(W, H, o, '載重平衡')


ALL = {'fig11_1': fig11_1, 'fig11_2': fig11_2}
