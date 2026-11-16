# -*- coding: utf-8 -*-
"""第 5 章：非均勻斷面。單位彎矩圖除以 EI(x) → 柔度 f；均勻梁與 SA-2025-3 的係數對照。"""
from sa_draw import *  # noqa
import calcs

D5 = calcs.ch5()
DU = calcs.ch5(calcs.UNIFORM)


def fig5_1():
    W, H = 900, 640
    x0, y0, Lp = 150, 110, 600
    o = T(W / 2, 34, '(a) SA-2025-3：三段各 *L*/3，剛度 *EI*、2*EI*、*EI*；跨中 *P*', 17, INK, 'middle', 'bold')
    for i, (w, lab) in enumerate([(6, '*EI*'), (14, '2*EI*'), (6, '*EI*')]):
        xa = x0 + Lp * i / 3
        o += L(xa, y0, xa + Lp / 3, y0, INK, w, cap='butt')
        o += T(xa + Lp / 6, y0 + 36, lab, 17, INK, 'middle', 'bold')
        o += dim(xa, y0 + 60, xa + Lp / 3, y0 + 60, '*L*/3', MUT, 0, 15)
    o += A(x0 + Lp / 2, y0 - 66, x0 + Lp / 2, y0 - 10, LOAD, 2.4, 11)
    o += T(x0 + Lp / 2 + 12, y0 - 48, '*P*', 18, LOAD, 'start', 'bold')
    o += moment(x0, y0, 28, True) + moment(x0 + Lp, y0, 28, True)
    o += T(x0 - 36, y0 - 28, '*M*_{AB}', 16, MOM, 'end', 'bold') + T(x0 + Lp + 36, y0 - 28, '*M*_{BA}', 16, MOM, 'start', 'bold')
    o += T(W / 2, 236, '(b) A 端加單位彎矩：彎矩圖 1−*u*，除以 *EI*(*u*) 後中段減半', 17, INK, 'middle', 'bold')
    pl = Plot(x0, 262, Lp, 170, 0, 1, 0, 1.08)
    o += pl.area(lambda u: 1 - u, lambda u: 0, 0, 1, '#ffcdd2', 0.5)
    o += pl.curve(lambda u: 1 - u, 0, 1, MOM, 1.6, '6 4')
    fm = lambda u: (1 - u) / (2 if 1 / 3 <= u < 2 / 3 else 1)
    pts = []
    for i in range(301):
        u = i / 300
        pts.append(pl.pt(u, fm(u)))
    o += P([pl.pt(0, 0)] + pts + [pl.pt(1, 0)], MOM, 2.6, COMPM, close=True, op=0.75)
    o += L(pl.X(0) - 20, pl.Y(0), pl.X(1) + 20, pl.Y(0), INK, 1.4)
    o += T(pl.X(0) - 10, pl.Y(1) + 6, '1/*EI*', 16, MOM, 'end', 'bold')
    o += T(pl.X(0.5), pl.Y(0.5) - 34, '中段 ÷2', 16, PUR, 'middle', 'bold')
    o += T(pl.X(0.86), pl.Y(0.55), '虛線＝均勻梁', 15, MUT, 'middle')
    o += R(60, 460, 780, 166, '#fff', STEEL, 1.2, 8)
    o += T(80, 492, '● 近端柔度 *f*_{AA} ＝ *L*∫(1−*u*)^{2}/*EI* d*u* ＝ 47/162 · *L*/*EI*（均勻梁 1/3）', 16, INK, 'start')
    o += T(80, 524, '● 交叉柔度 *f*_{AB} ＝ −*L*∫*u*(1−*u*)/*EI* d*u* ＝ −41/324 · *L*/*EI*（均勻梁 −1/6，必為負）', 16, INK, 'start')
    o += T(80, 556, '● 鎖住遠端：*k*_{AA} ＝ *f*_{BB}/*D*、*k*_{AB} ＝ −*f*_{AB}/*D*，*D* ＝ *f*_{AA}*f*_{BB} − *f*_{AB}^{2}', 16, INK, 'start')
    o += T(80, 596, '和第 2 章同一招：彎矩面積（＝虛功）算柔度，再鎖住一端求勁度', 16, PUR, 'start', 'bold')
    return svg(W, H, o, '非均勻斷面的柔度')


def fig5_2():
    W, H = 900, 460
    items = [('近端勁度 *k*_{AA}', float(DU['kAA']), float(D5['kAA']), '4', '4.26'),
             ('遠端勁度 *k*_{AB}', float(DU['kAB']), float(D5['kAB']), '2', '1.86'),
             ('傳遞係數 *C*×10', float(DU['C']) * 10, float(D5['C']) * 10, '0.5', '0.436'),
             ('固端彎矩 |*M*_{F}|/*PL*×40', float(-DU['MF_AB']) * 40, float(-D5['MF_AB']) * 40, '1/8', '13/120')]
    o = T(W / 2, 34, '均勻梁（灰）vs SA-2025-3 中段加倍（紫）', 17, INK, 'middle', 'bold')
    x0, bw, scale = 300, 30, 70
    for i, (lab, u, v, ut, vt) in enumerate(items):
        y = 90 + i * 88
        o += T(x0 - 20, y + 26, lab, 16, INK, 'end', 'bold')
        o += R(x0, y, u * scale, bw, STEEL3, STEEL, 1)
        o += T(x0 + u * scale + 10, y + 21, ut, 15, MUT, 'start')
        o += R(x0, y + bw + 4, v * scale, bw, KEY2, PUR, 1.4)
        o += T(x0 + v * scale + 10, y + bw + 25, vt, 15, PUR, 'start', 'bold')
    o += T(W / 2, 438, '中段變硬 → 近端勁度變大、傳得比較少（*C* < ½）、固端彎矩往中段跑而變小', 16, TEN, 'middle', 'bold')
    return svg(W, H, o, '非均勻斷面係數對照')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
