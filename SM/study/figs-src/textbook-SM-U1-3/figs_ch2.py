# -*- coding: utf-8 -*-
"""第 2 章：夯實曲線、能量、CBR 反推。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig2_1():
    d = ex2017_2()
    W, H = 900, 450
    pl = Plot(90, 50, 560, 330, 6, 22, 16.0, 20.5)
    o = pl.axes([6, 8, 10, 12, 14, 16, 18, 20, 22], [16, 17, 18, 19, 20], '*w* (%)', '*γ*_{d} (kN/m³)')
    o += pl.curve(lambda w: gzav(w / 100), 10.9, 22, AC, 3)
    o += pl.curve(lambda w: gS(w / 100, 0.8), 8.8, 19.3, ACM, 2.2, dash='7 5')
    fn = lambda w: d['a'] * w * w + d['b'] * w + d['c']
    o += pl.curve(fn, 9.0, 17.2, INK, 2.6)
    for w, g in CMP17:
        o += pl.dot(w, g, INK, 5.5)
    o += pl.dot(d['wopt'], d['gmax'], KEY, 7)
    o += pl.vline(d['wopt'], 16, d['gmax'], KEY, 1.3) + pl.hline(d['gmax'], 6, d['wopt'], KEY, 1.3)
    o += T(pl.X(d['wopt']) + 10, pl.Y(d['gmax']) - 12, f"峰：{d['gmax']:.2f}，OMC {d['wopt']:.1f}%", 15, KEY, 'start', 'bold')
    o += T(pl.X(18.6), pl.Y(gzav(0.186)) - 14, '*S*=100%（零空氣）', 15, AC, 'start', 'bold')
    o += T(pl.X(17.6), pl.Y(gS(0.176, 0.8)) + 22, '*S*=80%', 15, AC, 'start')
    o += box(675, 70, 210, 150, '兩個力量', ['乾側：水＝潤滑', '→ 越加越密', '濕側：水＝佔位', '→ 被 *S* 線壓住'], KEY2, KEY)
    o += T(675, 260, '試驗點高於藍線', 15, COMP, 'start', 'bold')
    o += T(675, 282, '＝*S*>100%，數據錯', 15, COMP, 'start')
    return svg(W, H, o, '夯實曲線與零空氣曲線')


def _cmp(w, a0, slope, S=0.9, p=10):
    g1 = a0 + slope * w
    g2 = gS(w / 100, S)
    return (g1 ** -p + g2 ** -p) ** (-1 / p)


def fig2_2():
    W, H = 900, 440
    pl = Plot(90, 50, 560, 320, 4, 26, 14.5, 21.5)
    o = pl.axes([4, 8, 12, 16, 20, 24], [15, 17, 19, 21], '*w* (%)', '*γ*_{d} (kN/m³)')
    o += pl.curve(lambda w: gzav(w / 100), 8.7, 26, AC, 3)
    std = lambda w: _cmp(w, 13.2, 0.30)
    mod = lambda w: _cmp(w, 15.6, 0.30)
    o += pl.curve(std, 5, 25, INK, 2.6)
    o += pl.curve(mod, 5, 25, COMP, 2.8)
    pk = []
    for fn, c, nm in ((std, INK, '標準'), (mod, COMP, '改良')):
        ws = [5 + i * 0.01 for i in range(2001)]
        wm = max(ws, key=fn)
        pk.append((wm, fn(wm)))
        o += pl.dot(wm, fn(wm), c, 6)
    o += L(pl.X(pk[1][0]) - 30, pl.Y(pk[1][1]) - 18, pl.X(pk[0][0]) + 40, pl.Y(pk[0][1]) + 24, KEY, 2, '6 4')
    o += A(pl.X(pk[0][0]), pl.Y(pk[0][1]), pl.X(pk[1][0]) + 4, pl.Y(pk[1][1]) + 3, KEY, 2.4, 12)
    o += T(pl.X(pk[1][0]) - 12, pl.Y(pk[1][1]) - 16, '改良（≈4.5 倍能量）', 15, COMP, 'end', 'bold')
    o += T(pl.X(pk[0][0]) + 16, pl.Y(pk[0][1]) + 34, '標準', 15, INK, 'start', 'bold')
    o += T(pl.X(22.3), pl.Y(gzav(0.223)) - 10, '零空氣', 15, AC, 'start', 'bold')
    o += box(670, 70, 215, 170, '能量↑', ['乾側整條抬高', '濕側幾乎不動', '峰往左上', '*γ*_{d,max}↑、OMC↓'], KEY2, KEY)
    o += T(670, 280, f"標準峰 *w*≈{pk[0][0]:.1f}%", 14, INK)
    o += T(670, 302, f"改良峰 *w*≈{pk[1][0]:.1f}%（示意）", 14, COMP)
    return svg(W, H, o, '夯實能量的影響')


def fig2_3():
    d = ex2017_2()
    W, H = 900, 640
    top = Plot(100, 50, 560, 220, 7, 19, 17.0, 19.0)
    o = top.axes([8, 10, 12, 14, 16, 18], [17, 18, 19], '*w* (%)', '*γ*_{d}')
    pts = CMP17
    o += P([top.pt(w, g) for w, g in pts], INK, 2.2)
    for w, g in pts:
        o += top.dot(w, g, INK, 5)
    bot = Plot(100, 360, 560, 200, 7, 19, 4, 14)
    o += bot.axes([8, 10, 12, 14, 16, 18], [4, 6, 8, 10, 12, 14], '*w* (%)', 'CBR')
    cb = [(10, 9.0), (12, 12.0), (16, 11.0), (18, 7.0)]
    o += P([bot.pt(w, c) for w, c in cb], AC, 2.2)
    for w, c in cb:
        o += bot.dot(w, c, AC, 5)
    o += bot.hline(10, 7, 19, COMP, 1.8, '7 4') + T(bot.X(18.9), bot.Y(10) - 8, 'CBR=10', 15, COMP, 'end', 'bold')
    wd = 10 + 2 * (10 - 9) / 3
    ww = 16 + 2 * (11 - 10) / 4
    for w, g, c, lab in ((wd, d['gdry'], TEN, '乾側'), (ww, d['gwet'], WARN, '濕側')):
        o += L(bot.X(w), bot.Y(10), top.X(w), top.Y(g), c, 1.6, '5 4')
        o += bot.dot(w, 10, c, 6) + top.dot(w, g, c, 6.5)
        o += T(bot.X(w) + (14 if lab == '乾側' else -14), bot.Y(10) + 42, f'{lab} {w:.2f}%', 15, c, 'start' if lab == '乾側' else 'end', 'bold')
    o += T(top.X(wd) - 8, top.Y(d['gdry']) - 12, f"{d['gdry']:.2f}", 15, TEN, 'end', 'bold')
    o += T(top.X(ww) + 10, top.Y(d['gwet']) + 22, f"{d['gwet']:.2f}", 15, WARN, 'start', 'bold')
    o += box(690, 80, 195, 160, '要求取較高', [f"max({d['gdry']:.2f}, {d['gwet']:.2f})", f"＝{d['req']:.2f}", f"÷ {18.66:.2f}", f"R.C.＝{d['RC']:.1f}%"], KEY2, KEY)
    o += T(690, 420, '同一 *γ*_{d}，乾側', 15, INK)
    o += T(690, 442, 'CBR 比濕側低', 15, INK)
    o += T(690, 470, '→ 取低值會不合格', 15, COMP, 'start', 'bold')
    return svg(W, H, o, 'CBR 反推工地密度')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
