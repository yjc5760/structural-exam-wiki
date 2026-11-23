# -*- coding: utf-8 -*-
"""第 6 章：等時線、U–Tv、比例法、貫穿範例沉陷曲線。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    W, H = 900, 480
    x0, y0, w, h = 120, 50, 460, 360
    X = lambda r: x0 + r * w
    Y = lambda zr: y0 + zr * h      # zr = z/H（0 頂、1 底）
    o = R(x0, y0, w, h, '#ede7f6', None, 0, op=0.5)
    o += hatch_ground(x0, y0, w, AC, down=False) + T(x0 + w + 8, y0 + 5, '砂（排水）', 15, AC)
    o += hatch_ground(x0, y0 + h, w, AC) + T(x0 + w + 8, y0 + h + 5, '砂（排水）', 15, AC)
    o += L(x0, Y(0.5), x0 + w, Y(0.5), KEY, 1.6, '7 4') + T(x0 + w + 8, Y(0.5) + 5, '分水嶺', 15, KEY, 'start', 'bold')
    for r in (0, 0.25, 0.5, 0.75, 1.0):
        o += T(X(r), y0 + h + 26, f'{r:g}', 14, MUT, 'middle')
    o += T(X(0.5), y0 + h + 48, '*u*/*u*_{0}', 15, INK, 'middle')
    o += T(x0 - 10, Y(0) + 5, '0', 14, MUT, 'end') + T(x0 - 10, Y(0.5) + 5, '*H*/2', 14, MUT, 'end') + T(x0 - 10, Y(1) + 5, '*H*', 14, MUT, 'end')
    cols = [(0.02, COMP), (0.08, WARN), (0.2, TEN), (0.4, AC), (0.8, KEY)]
    for Tv, c in cols:
        pts = []
        for i in range(201):
            zr = i / 200
            zz = zr * 2 if zr <= 0.5 else (1 - zr) * 2   # z/Hdr，由最近排水面量
            pts.append((X(u_iso(zz, Tv)), Y(zr)))
        o += P(pts, c, 2.6)
        k = cols.index((Tv, c))
        o += L(712, 312 + k * 26, 742, 312 + k * 26, c, 3) + T(750, 317 + k * 26, f'*T*_{{v}}={Tv:g}（*U*={U_exact(Tv) * 100:.0f}%）', 14, c, 'start', 'bold')
    o += box(700, 110, 185, 160, '讀圖', ['曲線下面積', '＝還沒排的水', '*U*＝1−面積比', '中央最慢'], KEY2, KEY)
    return svg(W, H, o, '等時線')


def fig6_2():
    W, H = 900, 440
    lmin, lmax = -3, 0.5
    pl = Plot(90, 50, 560, 320, lmin, lmax, 0, 1.0)
    o = pl.axes([-3, -2, -1, 0], [0, 0.2, 0.4, 0.6, 0.8, 1.0], 'log*T*_{v}', '*U*', xfmt=lambda t: f'10^{{{int(t)}}}' if t != 0 else '1', yfmt=lambda u: f'{int(u * 100)}%')
    o += pl.curve(lambda lt: U_exact(10 ** lt), lmin, lmax, INK, 4)
    o += pl.curve(lambda lt: math.sqrt(4 * 10 ** lt / math.pi), lmin, math.log10(0.40), COMP, 2.4, dash='7 4')
    def Ulog(lt):
        Tv = 10 ** lt
        return 1 - 10 ** (-(Tv + 0.085) / 0.933)
    o += pl.curve(Ulog, math.log10(0.15), lmax, WARN, 2.4, dash='7 4')
    o += pl.hline(0.6, lmin, lmax, KEY, 1.3)
    o += T(pl.X(-2.95), pl.Y(0.6) - 8, '*U*=60% 交棒', 14, KEY, 'start', 'bold')
    for U, nm in ((0.5, '*T*_{50}=0.197'), (0.9, '*T*_{90}=0.848')):
        Tv = Tv_from_U(U)
        o += pl.dot(math.log10(Tv), U, KEY, 6)
        o += T(pl.X(math.log10(Tv)) - 10, pl.Y(U) - 6, nm, 15, KEY, 'end', 'bold')
    o += T(pl.X(-2.0), pl.Y(0.25), '*π**U*^{2}/4（早期）', 15, COMP, 'start', 'bold')
    o += T(pl.X(-0.75), pl.Y(0.98) - 4, '−0.933log(1−*U*)−0.085', 14, WARN, 'end', 'bold')
    o += box(670, 70, 215, 180, '從哪裡來', ['早期：半無限擴散', '*U*=2√(*T*_{v}/*π*)', '晚期：只剩第一項', '(8/*π*^{2})*e*^{−*π*²*T*v/4}', '→ 取 log'], KEY2, KEY)
    return svg(W, H, o, 'U–Tv 精確解與兩段式')


def fig6_3():
    d = ex2018_1()
    W, H = 900, 430
    pl = Plot(90, 50, 580, 310, 0, 1500, 0, 800)
    o = pl.axes([0, 365, 730, 1095, 1460], [0, 200, 400, 600, 800], '*t* (天)', '*S* (mm)')
    k = d['k']
    o += pl.curve(lambda t: d['Smax'] * U_from_Tv(k * t), 1, 1500, INK, 3)
    o += pl.curve(lambda t: d['S200'] * math.sqrt(t / 200), 1, 1500, COMP, 2.2, dash='7 4')
    o += pl.hline(d['Smax'], 0, 1500, MUT, 1.2) + T(pl.X(20), pl.Y(d['Smax']) - 8, f"*S*_{{∞}}={d['Smax']:.0f}", 15, MUT, 'start', 'bold')
    t60 = Tv_from_U(0.6) / k
    o += pl.vline(t60, 0, 800, KEY, 1.3) + T(pl.X(t60) + 6, pl.Y(60), f'*U*=60%（約 {t60:.0f} 天）', 14, KEY, 'start', 'bold')
    o += pl.dot(200, 234, AC, 6) + T(pl.X(200) + 10, pl.Y(234) + 22, '200 天 234 mm', 14, AC, 'start', 'bold')
    for yr, t, Tv, U, S in d['rows']:
        o += pl.dot(t, S, INK, 5.5)
        o += T(pl.X(t) + 8, pl.Y(S) + 22, f'{S:.1f}', 14, INK, 'start', 'bold')
    for yr, S in d['wrong'][2:]:
        o += C(pl.X(365 * yr), pl.Y(S), 5, COMP, '#fff', 1.4)
        o += T(pl.X(365 * yr) - 8, pl.Y(S) - 10, f'{S:.1f}', 14, COMP, 'end')
    o += T(pl.X(1490), pl.Y(d['S200'] * math.sqrt(1490 / 200)) + 2, '√*t* 外推（錯）', 14, COMP, 'start')
    return svg(W, H, o, '比例法')


def fig6_4():
    d = ex2021_2()
    W, H = 900, 420
    pl = Plot(90, 50, 580, 300, 0, 1800, 0, 70)
    o = pl.axes([0, 300, 600, 900, 1200, 1500, 1800], [0, 10, 20, 30, 40, 50, 60, 70], '*t* (天)', '*S* (cm)')
    f = lambda t, Hdr: d['Sc'] * U_from_Tv(d['cv'] * t * 86400 / Hdr ** 2)
    o += pl.curve(lambda t: f(t, 250), 0.5, 1800, INK, 3)
    o += pl.curve(lambda t: f(t, 500), 0.5, 1800, COMP, 2.2, dash='7 4')
    o += pl.hline(d['Sc'], 0, 1800, MUT, 1.2) + T(pl.X(1790), pl.Y(d['Sc']) - 8, f"*S*_{{c}}={d['Sc']:.2f}", 15, MUT, 'end', 'bold')
    for days, Tv, U, S in d['steps']:
        o += pl.dot(days, S, AC, 5.5)
    o += T(pl.X(30), pl.Y(66.5), '30／60／90 天（藍點）：14.31、20.24、24.79 cm', 14, AC, 'start', 'bold')
    o += pl.hline(50, 0, d['t50cm'], KEY, 1.3) + pl.vline(d['t50cm'], 0, 50, KEY, 1.3)
    o += pl.dot(d['t50cm'], 50, KEY, 6.5) + T(pl.X(d['t50cm']) + 10, pl.Y(50) + 22, '50 cm：約 414 天', 15, KEY, 'start', 'bold')
    o += pl.dot(d['t50cm_wrongHdr'], 50, COMP, 6) + T(pl.X(d['t50cm_wrongHdr']) + 8, pl.Y(50) + 22, '誤取 *H*_{dr}=5 m：約 1658 天', 14, COMP, 'start')
    return svg(W, H, o, '貫穿範例沉陷曲線')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
