# -*- coding: utf-8 -*-
"""第 3 章：桁架類比、以 Vc 為刻度的尺、示範梁剪力分區。"""
from figs_common import *  # noqa
from calcs import demo, p2020_2, p2006_1
import math

D = demo()
P20 = p2020_2()
P06 = p2006_1()


def fig3_1():
    W, H = 900, 390
    o = T(450, 24, '沿一條 45° 裂縫切開，數穿過它的箍筋', 16, INK, 'middle', 'bold')
    sc = 3.0
    x0, y0 = 110, 70
    Lseg, h, d = 170, D['h'], D['d']
    o += R(x0, y0, Lseg * sc, h * sc, STEEL2, INK, 1.6)
    ys = y0 + d * sc
    o += L(x0, ys, x0 + Lseg * sc, ys, INK, 3.5)
    o += T(x0 + Lseg * sc - 6, ys + 22, '縱筋', 14, INK, 'end')
    # 裂縫：由 (xc0, ys) 到 (xc0+d, ys-d)
    xc0 = x0 + 50 * sc
    xc1 = xc0 + d * sc
    yc1 = y0 + 4
    o += L(xc0, ys, xc1 - 4, yc1, COMP, 3.2)
    o += T(xc0 - 6, ys - 14, '斜裂縫', 15, COMP, 'end', 'bold')
    # 箍筋
    s = D['s_use']
    n = 0
    k = 0
    while True:
        xx = x0 + 15 * sc + k * s * sc
        if xx > x0 + (Lseg - 5) * sc:
            break
        cross = xc0 < xx < xc1
        o += L(xx, y0 + 6 * sc, xx, ys + 3, TEN if cross else STEEL, 3 if cross else 1.6)
        if cross:
            n += 1
            yy = ys - (xx - xc0)
            o += C(xx, yy, 4.5, TEN, '#fff', 1.2)
        k += 1
    # 尺寸：裂縫水平長 d
    o += hdim(xc0, xc1, ys + 46, f'水平投影 ≈ *d* = {d:.0f} cm', INK, 1, 15)
    o += vdim(x0 - 20, y0, ys, f'*d* = {d:.0f}', INK, -1, 15)
    o += hdim(x0 + 15 * sc + 1 * s * sc, x0 + 15 * sc + 2 * s * sc, y0 - 12, f'*s* = {s:.0f}', TEN, -1, 15)
    # 自由體力
    o += A(x0 - 85, y0 + 40, x0 - 85, y0 + 140, AC, 2.4, 10)
    o += T(x0 - 91, y0 + 98, '*V*', 18, AC, 'end', 'bold')
    tx = x0 + Lseg * sc + 60
    o += box(tx - 10, 120, 175, 210, '本圖（示範梁）', [f'*d*/*s* = {d:.0f}/{s:.0f} = {n} 根', f'每組 *A*_{{v}}*f*_{{yt}}', f'= {D["Av"]*D["fyt"]/1000:.1f} tf', f'*V*_{{s}} = {n} × {D["Av"]*D["fyt"]/1000:.1f}', f'= {D["Vs_use"]/1000:.1f} tf'], TEN2, TEN, 15, 14)
    o += T(x0 + Lseg * sc / 2, y0 + h * sc + 70, '綠色＝穿過裂縫的箍筋（拉桿）；裂縫之間的混凝土條＝斜壓桿', 15, INK, 'middle')
    return svg(W, H, o, '桁架類比')


def fig3_2():
    W, H = 900, 330
    o = T(450, 24, '以 *V*_{c} 為刻度：*V*_{s} 落在第幾格？', 16, INK, 'middle', 'bold')
    x0, x1, y = 80, 820, 120
    u = (x1 - x0) / 5
    zones = [(0, 2, TEN2, TEN, '*s* ≤ min(*d*/2, 60)'), (2, 4, WARN2, WARN, '*s* ≤ min(*d*/4, 30)'), (4, 5, COMP2, COMP, '放大斷面')]
    for a, b, fill, col, lab in zones:
        o += R(x0 + a * u, y - 30, (b - a) * u, 60, fill, col, 1.6)
        o += T(x0 + (a + b) / 2 * u, y + 6, lab, 15, col, 'middle', 'bold')
    for i in range(6):
        xx = x0 + i * u
        o += L(xx, y + 30, xx, y + 44, INK, 1.6)
        lab = ['0', '1*V*_{c}', '2*V*_{c}', '3*V*_{c}', '4*V*_{c}', '5*V*_{c}'][i]
        o += T(xx, y + 64, lab, 15, INK, 'middle')
    o += T(x0 + 2 * u, y + 88, '1.06√*f*′_{c}*b*_{w}*d*', 14, WARN, 'middle', 'bold')
    o += T(x0 + 4 * u, y + 88, '2.12√*f*′_{c}*b*_{w}*d*', 14, COMP, 'middle', 'bold')
    pts = [(D['Vs'] / D['Vc'], '示範梁', AC, -1), (P06['Vs'] / P06['Vc'], 'RC-2006-1', KEY, 1), (P20['Vs'] / P20['Vc'], 'RC-2020-2', COMP, -1)]
    for r, lab, col, side in pts:
        xx = x0 + r * u
        if side < 0:
            o += A(xx, y - 66, xx, y - 32, col, 2, 9)
            o += T(xx, y - 74, f'{lab} {r:.2f}', 15, col, 'middle', 'bold')
        else:
            o += A(xx, y + 150, xx, y + 100, col, 2, 9)
            o += T(xx, y + 172, f'{lab} {r:.2f}', 15, col, 'middle', 'bold')
    o += T(450, 315, '所有門檻都是 0.53 的倍數：1.06 = 2 × 0.53，2.12 = 4 × 0.53', 15, MUT, 'middle')
    return svg(W, H, o, 'Vc 尺')


def fig3_3():
    W, H = 900, 420
    pl = Plot(100, 50, 560, 300, 0, 400, 0, 40)
    o = pl.axes([0, 60, 100, 200, 300, 400], [0, 10, 20, 30, 40], '*x*', '*V*', size=14)
    o += T(pl.X(400) + 18, pl.Y(0) + 26, '(cm，自支承面)', 14, MUT, 'start')
    o += T(pl.X(0) + 30, pl.Y(40) - 22, '(tf)', 14, MUT, 'start')
    w = D['wu'] * 10 / 1000  # tf/cm
    V0 = D['Vsup'] / 1000
    f = lambda x: V0 - w * x
    pv, hv = D['phiVc'] / 1000, D['half_phiVc'] / 1000
    o += pl.area(f, lambda x: pv, 0, D['x_phiVc'], TEN2, 0.9)
    o += pl.area(lambda x: min(f(x), pv), lambda x: hv, D['x_phiVc'], D['x_halfphiVc'], WARN2, 0.9)
    o += pl.curve(f, 0, 400, INK, 3)
    o += pl.hline(pv, 0, 400, TEN, 2, None)
    o += pl.hline(hv, 0, 400, WARN, 2, None)
    cap = D['phiVn_use'] / 1000
    o += pl.hline(cap, 0, 120, AC, 2, '7 4')
    o += T(pl.X(122), pl.Y(cap) + 5, f'φ*V*_{{n}}（D10@10）= {cap:.2f}', 14, AC, 'start', 'bold')
    o += pl.vline(60, 0, f(60), KEY, 1.8)
    o += pl.dot(60, f(60), KEY, 6)
    o += T(pl.X(66), pl.Y(22), '臨界斷面', 14, KEY, 'start', 'bold') + T(pl.X(66), pl.Y(18), f'*V*_{{u}} = {f(60):.2f}', 14, KEY, 'start', 'bold')
    o += T(pl.X(2), pl.Y(V0) - 8, f'{V0:.2f}', 14, INK, 'start')
    o += T(pl.X(398), pl.Y(pv) - 8, f'φ*V*_{{c}} = {pv:.2f}', 14, TEN, 'end', 'bold')
    o += T(pl.X(398), pl.Y(hv) - 8, f'0.5φ*V*_{{c}} = {hv:.2f}', 14, WARN, 'end', 'bold')
    o += pl.vline(D['x_phiVc'], 0, pv, TEN, 1.2)
    o += pl.vline(D['x_halfphiVc'], 0, hv, WARN, 1.2)
    o += T(pl.X(D['x_phiVc']), pl.Y(0) + 40, f"{D['x_phiVc']:.0f}", 14, TEN, 'middle', 'bold')
    o += T(pl.X(D['x_halfphiVc']), pl.Y(0) + 40, f"{D['x_halfphiVc']:.0f}", 14, WARN, 'middle', 'bold')
    o += box(690, 70, 200, 230, '三區', ['*V*_{u} > φ*V*_{c}：', '計算區（綠底）', '0.5φ*V*_{c} < *V*_{u} ≤ φ*V*_{c}：', '最少量區（橘底）', '*V*_{u} ≤ 0.5φ*V*_{c}：', '免配區', '（跨中）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '示範梁剪力分區')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
