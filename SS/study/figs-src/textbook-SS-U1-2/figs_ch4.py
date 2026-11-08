# -*- coding: utf-8 -*-
"""第 4 章：LTB 三區段（貫穿範例 H700）、Lr 由 Mcr＝Mr 解出、印錯的分母。"""
from plot import *  # noqa
import calcs


def span(fn, a, b, lo, hi, n=2000):
    xs = [a + (b - a) * i / n for i in range(n + 1)]
    ok = [x for x in xs if lo <= fn(x) <= hi]
    return ok[0], ok[-1]

D = calcs.ex_ltb()


def mn(L, Cb=1.0):
    return calcs.mn_ltb(L * 100, D['Mp'], D['Mr'], D['Lp'], D['Lr'], D['Sx'], D['X1'], D['X2'], D['ry'], Cb) / 100


def fig4_1():
    W, H = 900, 450
    pl = Plot(100, 50, 580, 300, 0, 10, 0, 180)
    o = pl.axes([0, D['Lp'] / 100, D['Lr'] / 100, 8, 10], [0, 40, 80, 120, 160], '*L*_{b}（m）', '*M*_{n}（tf·m）', size=14,
                xfmt=lambda v: f'{v:.2f}' if v not in (0, 8, 10) else f(v))
    Lp, Lr = D['Lp'] / 100, D['Lr'] / 100
    o += R(pl.X(0), pl.Y(180), pl.X(Lp) - pl.X(0), pl.Y(0) - pl.Y(180), TEN2, None, 0, op=0.7)
    o += R(pl.X(Lp), pl.Y(180), pl.X(Lr) - pl.X(Lp), pl.Y(0) - pl.Y(180), WARN2, None, 0, op=0.7)
    o += R(pl.X(Lr), pl.Y(180), pl.X(10) - pl.X(Lr), pl.Y(0) - pl.Y(180), COMP2, None, 0, op=0.5)
    o += T(pl.X(Lp / 2), pl.Y(172), '塑性', 15, TEN, 'middle', 'bold')
    o += T(pl.X((Lp + Lr) / 2), pl.Y(172), '非彈性（直線）', 15, WARN, 'middle', 'bold')
    o += T(pl.X(8), pl.Y(172), '彈性（*M*_{cr}）', 15, COMP, 'middle', 'bold')
    mc = lambda L: calcs.mcr_x(L * 100, D['Sx'], D['X1'], D['X2'], D['ry']) / 100
    a, b = span(mc, 0.5, 10, 0, 180)
    o += pl.curve(mc, a, b, AC, 1.6, dash='5 4')
    o += pl.curve(lambda L: mn(L, 1.7), 0, 10, KEY, 2.2, dash='9 5')
    o += pl.curve(mn, 0, 10, COMP, 3.2)
    o += pl.hline(D['Mp'] / 100, c=TEN) + pl.hline(D['Mr'] / 100, c=WARN)
    o += T(pl.X(10) + 8, pl.Y(D['Mp'] / 100) + 5, f'*M*_{{p}} {D["Mp"] / 100:.1f}', 15, TEN, 'start', 'bold')
    o += T(pl.X(10) + 8, pl.Y(D['Mr'] / 100) + 5, f'*M*_{{r}} {D["Mr"] / 100:.1f}', 15, WARN, 'start', 'bold')
    o += T(pl.X(2.2), pl.Y(48), '理想 *M*_{cr}', 14, AC, 'start')
    o += T(pl.X(7.4), pl.Y(118), '*C*_{b} = 1.7', 15, KEY, 'start', 'bold')
    pts = [(1.0, mn(1.0), '(一)'), (5.0, mn(5.0), '(二)'), (8.0, mn(8.0, 1.7), '(三) *C*_{b}=1.7')]
    for x, y, lab in pts:
        o += pl.dot(x, y, KEY, 6)
        o += T(pl.X(x) + 8, pl.Y(y) + (24 if x < 2 else -10), f'{lab} {y:.1f}', 14, KEY, 'start', 'bold')
    o += box(705, 210, 185, 120, 'SS-2007-3', [f'(一) φ*M*_{{n}} = {0.9 * mn(1):.1f}', f'(二) φ*M*_{{n}} = {0.9 * mn(5):.1f}', f'(三) φ*M*_{{n}} = {0.9 * mn(8, 1.7):.1f}'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'LTB 三區段')


def fig4_2():
    """Lr＝Mcr 曲線碰到 Mr 那一點。"""
    W, H = 900, 360
    pl = Plot(100, 40, 560, 250, 3, 9, 60, 180)
    o = pl.axes([3, 4, 5, D['Lr'] / 100, 7, 8, 9], [60, 90, 120, 150, 180], '*L*_{b}（m）', '*M*（tf·m）', size=14,
                xfmt=lambda v: f'{v:.2f}' if abs(v - D['Lr'] / 100) < 1e-6 else f(v))
    mc = lambda L: calcs.mcr_x(L * 100, D['Sx'], D['X1'], D['X2'], D['ry']) / 100
    a, b = span(mc, 3, 9, 60, 180)
    o += pl.curve(mc, a, b, AC, 2.8)
    o += pl.hline(D['Mr'] / 100, c=WARN, w=2.2, dash=None)
    o += pl.dot(D['Lr'] / 100, D['Mr'] / 100, KEY, 7)
    o += pl.vline(D['Lr'] / 100, 60, D['Mr'] / 100, KEY, 1.4)
    o += T(pl.X(3.2), pl.Y(D['Mr'] / 100) - 10, f'*M*_{{r}} = *F*_{{L}}*S*_{{x}} = {D["Mr"] / 100:.1f}', 15, WARN, 'start', 'bold')
    o += T(pl.X(4.0), pl.Y(170), '*M*_{cr}（*C*_{b}=1）', 15, AC, 'start', 'bold')
    o += T(pl.X(D['Lr'] / 100) + 10, pl.Y(D['Mr'] / 100) + 24, f'*L*_{{r}} = {D["Lr"]:.1f} cm', 15, KEY, 'start', 'bold')
    o += box(690, 60, 200, 150, '*L*_{r} 的定義', ['彈性挫屈剛好發生在', '「外緣第一次降伏」', '', '*M*_{cr}(*L*_{r}) = *M*_{r}', '→ 解二次方程'], KEY2, KEY, 16, 14)
    return svg(W, H, o, 'Lr 的由來')


def fig4_3():
    """印錯分母：Lr−Lb 取代 Lr−Lp。"""
    W, H = 900, 360
    Lp, Lr = D['Lp'] / 100, D['Lr'] / 100
    pl = Plot(100, 40, 560, 260, 1.5, 6, -200, 200)
    o = pl.axes([Lp, 3, 4, 5, Lr], [-200, -100, 0, 100, 200], '*L*_{b}（m）', 'φ*M*_{n}（tf·m）', size=14,
                xfmt=lambda v: f'{v:.2f}' if v in (Lp, Lr) else f(v))
    good = lambda L: 0.9 * (D['Mp'] - (D['Mp'] - D['Mr']) * (L - Lp) / (Lr - Lp)) / 100
    bad = lambda L: 0.9 * (D['Mp'] - (D['Mp'] - D['Mr']) * (L - Lp) / (Lr - L)) / 100
    o += pl.hline(0, c=MUT, dash=None, w=1)
    o += pl.curve(good, Lp, Lr, KEY, 3)
    a, b = span(bad, Lp, 5.6, -200, 200)
    o += pl.curve(bad, a, b, COMP, 2.6, dash='8 5')
    o += pl.dot(5, good(5), KEY, 6) + pl.dot(5, bad(5), COMP, 6)
    o += T(pl.X(5) + 10, pl.Y(good(5)) - 10, f'正確 {good(5):.1f}', 15, KEY, 'start', 'bold')
    o += T(pl.X(5) - 10, pl.Y(bad(5)) + 6, f'印錯 {bad(5):.1f}', 15, COMP, 'end', 'bold')
    o += box(680, 60, 210, 150, '代端點就抓到', ['正確分母 *L*_{r} − *L*_{p}', '代 *L*_{r} 得 *M*_{r} ✓', '', '印錯分母 *L*_{r} − *L*_{b}', '代 *L*_{r} → 無窮大 ✗'], KEY2, KEY, 16, 14)
    return svg(W, H, o, '印錯的分母')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
