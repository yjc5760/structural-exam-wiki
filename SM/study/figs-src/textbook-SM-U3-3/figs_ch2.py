# -*- coding: utf-8 -*-
"""第 2 章：無限邊坡切片、FS–β 與 FS–z。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig2_1():
    W_, H = 900, 480
    be = 25
    t = math.tan(r(be))
    o = ''
    x0, y0 = 40, 330
    xe = 620
    ys = lambda x: y0 - (x - x0) * t          # 地表
    zz = 130                                  # 鉛直深度（像素）
    yb = lambda x: ys(x) + zz                 # 滑動面
    o += P([(x0, ys(x0)), (xe, ys(xe)), (xe, yb(xe)), (x0, yb(x0))], SOILE, 1.4, fill=SOIL, close=True)
    o += L(x0, yb(x0), xe, yb(xe), COMP, 3, '9 5')
    o += T(x0 + 420, yb(x0 + 420) + 34, '滑動面（平行坡面、很長）', 15, COMP, 'start', 'bold')
    # slice
    xa, xb = 300, 380
    o += P([(xa, ys(xa)), (xb, ys(xb)), (xb, yb(xb)), (xa, yb(xa))], INK, 2, fill=STEEL2, close=True)
    o += dim(xa, ys(xa) - 30, xb, ys(xb) - 30, '', INK, 0)
    o += T((xa + xb) / 2 - 20, ys((xa + xb) / 2) - 44, '*b*', 16, INK, 'middle', 'bold')
    o += dim(xa - 22, ys(xa), xa - 22, yb(xa), '*z*（鉛直）', INK, 0, 15, 1)
    # weight
    gx = (xa + xb) / 2
    gy = (ys(xa) + yb(xb)) / 2
    o += A(gx, gy, gx, gy + 110, INK, 3, 12)
    o += T(gx + 8, gy + 116, '*W* = γ*zb*', 16, INK, 'start', 'bold')
    # side forces cancel
    o += A(xa - 4, gy - 10, xa + 20, gy - 10 - 24 * t, MUT, 2, 9)
    o += A(xb + 34, gy - 10 - 80 * t - 14 * t, xb + 4, gy - 10 - 80 * t, MUT, 2, 9)
    o += T(xa - 30, ys(xa) - 34, '兩側推力相等、抵銷', 14, MUT, 'end')
    o += T(x0 + 60, y0 - 12, 'β', 17, INK, 'middle', 'bold')
    # box
    o += R(640, 60, 250, 210, KEY2, KEY, 1.4, 8)
    o += T(765, 88, '底面長 *b*/cos β', 15, KEY, 'middle', 'bold')
    o += T(765, 120, '*N* = *W* cos β', 15, AC, 'middle')
    o += T(765, 148, '*T* = *W* sin β', 15, COMP, 'middle')
    o += T(765, 182, '÷ 底面長：', 15, INK, 'middle')
    o += T(765, 212, 'σ = γ*z* cos²β', 16, AC, 'middle', 'bold')
    o += T(765, 244, 'τ = γ*z* sin β cos β', 16, COMP, 'middle', 'bold')
    return svg(W_, H, o, '無限邊坡的一個切片')


def fig2_2():
    d = ex2024_2()
    W_, H = 900, 400
    pl = Plot(80, 60, 330, 270, 15, 50, 0, 3)
    o = T(245, 30, '(a) 砂：FS = tan φ / tan β（φ = 35°）', 16, INK, 'middle', 'bold')
    o += pl.axes([15, 25, 35, 42, 50], [0, 1, 2, 3], 'β', 'FS')
    o += pl.curve(lambda b: tan(35) / tan(b), 15, 50, KEY, 3)
    o += pl.hline(1, 15, 50, COMP, 1.6, '6 4')
    o += pl.dot(35, 1, COMP, 5)
    o += T(pl.X(35) + 8, pl.Y(1) - 10, 'β = φ', 14, COMP, 'start', 'bold')
    o += pl.dot(42, d['FS'], KEY, 6)
    o += T(pl.X(42) - 4, pl.Y(d['FS']) + 24, f"42° → {d['FS']:.2f}", 14, KEY, 'middle', 'bold')
    o += T(pl.X(26), pl.Y(2.3), '乾＝浸水（同一條線）', 15, AC, 'middle', 'bold')
    pl2 = Plot(520, 60, 330, 270, 0, 10, 0, 3)
    o += T(685, 30, '(b) *c*′–φ′：越深越危險（示意）', 16, INK, 'middle', 'bold')
    o += pl2.axes([0, 2, 4, 6, 8, 10], [0, 1, 2, 3], '*z*', 'FS')
    o += pl2.curve(lambda z: cphi_FS(z), 0.6, 10, TEN, 3)
    o += pl2.hline(tan(25) / tan(30), 0, 10, AC, 1.6, '6 4')
    o += T(pl2.X(10), pl2.Y(tan(25) / tan(30)) + 22, f'深處極限 tan φ/tan β = {tan(25) / tan(30):.2f}', 14, AC, 'end', 'bold')
    zc = z_crit()
    o += pl2.dot(zc, 1, COMP, 6)
    o += T(pl2.X(zc) + 8, pl2.Y(1) - 12, f'FS = 1 在 *z* = {zc:.2f} m', 14, COMP, 'start', 'bold')
    return svg(W_, H, o, '無限邊坡 FS 與坡角、深度')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
