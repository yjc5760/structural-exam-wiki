# -*- coding: utf-8 -*-
"""第 1 章：Rankine 莫爾圓、4cu−γH、水土分開。"""
from plot import *  # noqa
from calcs import *  # noqa


def circle(pl, s1, s3, c, w=2.6, dash=None):
    C0, R = (s1 + s3) / 2, abs(s1 - s3) / 2
    pts = [pl.pt(C0 + R * math.cos(t), R * math.sin(t)) for t in [i * math.pi / 120 for i in range(121)]]
    return P(pts, c, w, dash=dash)


def fig1_1():
    W, H = 900, 380
    sv, phi = 100.0, 30.0
    pl = Plot(70, 50, 640, 240, 0, 320, 0, 120)
    o = pl.axes([0, 50, 100, 150, 200, 250, 300], [0, 50, 100], '*σ* (kPa)', '*τ*')
    o += L(pl.X(0), pl.Y(0), pl.X(120 / tan(phi)), pl.Y(120), WARN, 2.4)
    sa, sp = Ka(phi) * sv, Kp(phi) * sv
    o += circle(pl, sv, 0.5 * sv, MUT, 2, '5 4')
    o += circle(pl, sv, sa, TEN, 3) + circle(pl, sp, sv, COMP, 3)
    o += C(pl.X(sv), pl.Y(0), 6, KEY, '#fff', 1.8) + T(pl.X(sv), pl.Y(0) + 40, '*σ*_{v}=100', 15, KEY, 'middle', 'bold')
    o += C(pl.X(sa), pl.Y(0), 5, TEN, '#fff', 1.6) + T(pl.X(sa), pl.Y(0) - 8, f'{sa:.1f}', 14, TEN, 'middle', 'bold')
    o += C(pl.X(sp), pl.Y(0), 5, COMP, '#fff', 1.6) + T(pl.X(sp), pl.Y(0) - 8, f'{sp:.0f}', 14, COMP, 'middle', 'bold')
    o += T(pl.X(sa) + 4, pl.Y(36), '主動', 15, TEN, 'start', 'bold')
    o += T(pl.X(200), pl.Y(30), '被動', 15, COMP, 'middle', 'bold')
    o += T(pl.X(75), pl.Y(-4) + 20, '*K*_{0}', 14, MUT, 'middle')
    o += box(725, 60, 165, 160, '同一個 *σ*_{v}', ['外移：*σ*_{h}↓', '→ 主動 *K*_{a}=1/3', '內推：*σ*_{h}↑', '→ 被動 *K*_{p}=3'], KEY2, KEY)
    return svg(W, H, o, 'Rankine 莫爾圓')


def fig1_2():
    d = ex2005_1()
    W, H = 900, 470
    o = ''
    x0, y0 = 360, 40
    sc = 1.6      # px per kPa（全圖同一比例）
    zs = 26       # px per m
    Hm, Dm = d['H'], 6.0
    Y = lambda z: y0 + z * zs
    # 牆
    o += L(x0, Y(0), x0, Y(Hm + Dm), INK, 5)
    o += T(x0 - 220, Y(0.6), '坑外（主動側）', 15, TEN, 'start', 'bold')
    o += T(x0 + 20, Y(2.0), '坑內（被動側）', 15, COMP, 'start', 'bold')
    o += L(x0, Y(Hm), x0 + 300, Y(Hm), INK, 1.4) + T(x0 + 300, Y(Hm) - 6, '開挖面', 14, INK, 'end')
    # 砂段主動三角形（畫在左側）
    o += P([(x0, Y(0)), (x0 - d['pa'] * sc, Y(Hm)), (x0, Y(Hm))], TEN, 2, fill=TEN2, close=True)
    o += T(x0 - d['pa'] * sc - 6, Y(Hm) - 6, f"{d['pa']:.2f}", 14, TEN, 'end', 'bold')
    # 開挖面下：兩側
    cu, gs, gc = d['cu'], d['gs'], 17.0
    for zp in (0, Dm):
        pass
    act = lambda z: gs * Hm + gc * z - 2 * cu
    pas = lambda z: gc * z + 2 * cu
    sc2 = sc
    pts_a = [(x0 - act(z) * sc2, Y(Hm + z)) for z in (0, Dm)]
    pts_p = [(x0 + pas(z) * sc2, Y(Hm + z)) for z in (0, Dm)]
    o += P([(x0, Y(Hm)), pts_a[0], pts_a[1], (x0, Y(Hm + Dm))], TEN, 2, fill=TEN2, close=True, op=0.9)
    o += P([(x0, Y(Hm)), pts_p[0], pts_p[1], (x0, Y(Hm + Dm))], COMP, 2, fill=COMP2, close=True, op=0.9)
    o += T(pts_a[1][0] - 4, pts_a[1][1] + 18, '*γ*_{s}*H*+*γ*_{c}*z*′−2*c*_{u}', 14, TEN, 'start', 'bold')
    o += T(pts_p[1][0] - 4, pts_p[1][1] + 18, '*γ*_{c}*z*′+2*c*_{u}', 14, COMP, 'end', 'bold')
    # 右側：淨被動矩形
    xr = 730
    o += L(xr, Y(Hm), xr, Y(Hm + Dm), INK, 3)
    o += R(xr, Y(Hm), d['pnet'] * sc, Dm * zs, COMP2, COMP, 1.8)
    o += T(xr + d['pnet'] * sc + 8, Y(Hm + Dm / 2), f"{d['pnet']:.0f} kPa", 15, COMP, 'start', 'bold')
    o += T(xr - 30, Y(Hm) - 52, '淨被動（相減）', 15, KEY, 'start', 'bold')
    o += T(xr - 30, Y(Hm) - 30, '*γ*_{c}*z*′ 抵銷', 15, KEY, 'start', 'bold')
    o += T(xr - 30, Y(Hm) - 8, '4*c*_{u}−*γH*', 15, KEY, 'start', 'bold')
    o += A(690, Y(Hm + Dm / 2), xr - 10, Y(Hm + Dm / 2), KEY, 2, 10)
    o += T(x0 - 300, Y(Hm / 2), '砂 9 m', 15, INK, 'start') + T(x0 - 300, Y(Hm / 2) + 22, '*K*_{a}=0.3073', 14, INK, 'start')
    o += T(x0 - 300, Y(Hm + 2.0), '黏土 *c*_{u}=45', 15, INK, 'start')
    return svg(W, H, o, '淨被動 4cu−γH')


def fig1_3():
    d = water_error()
    W, H = 900, 400
    o = ''
    x0, y0, zs, sc = 120, 50, 50, 5.0
    z = 6.0
    gp = 19.0 - GW
    Y = lambda zz: y0 + zz * zs
    o += L(x0, Y(0), x0, Y(z), INK, 4)
    soil = Ka(30) * gp * z
    water = GW * z
    o += P([(x0, Y(0)), (x0 + soil * sc, Y(z)), (x0, Y(z))], TEN, 2, fill=TEN2, close=True)
    o += P([(x0 + soil * sc * 0, Y(0)), (x0 + soil * sc, Y(z)), (x0 + (soil + water) * sc, Y(z))], AC, 2, fill=AC2, close=True)
    o += L(x0, Y(0), x0 + (soil + water) * sc, Y(z), AC, 2)
    o += L(x0, Y(0), x0 + d['wrong'] * sc, Y(z), COMP, 2.4, '7 4')
    o += T(x0 + soil * sc / 2, Y(z) + 24, f'骨架 {soil:.2f}', 14, TEN, 'middle', 'bold')
    o += T(x0 + soil * sc + water * sc / 2, Y(z) + 24, f'水 {water:.2f}', 14, AC, 'middle', 'bold')
    o += T(x0 + (soil + water) * sc + 8, Y(z) - 4, f"正確 {d['right']:.2f}", 15, AC, 'start', 'bold')
    o += T(x0 + d['wrong'] * sc + 8, Y(z * 0.75), f"錯：*K*_{{a}}*γ*_{{sat}}*z*＝{d['wrong']:.2f}", 15, COMP, 'start', 'bold')
    o += T(x0 - 10, Y(0) + 5, '0', 14, MUT, 'end') + T(x0 - 10, Y(z) + 5, '6 m', 14, MUT, 'end')
    o += box(620, 60, 265, 180, '水的 *K*＝1', ['砂：*K*_{a}*γ*′*z*＋*γ*_{w}*z*', '黏土（總應力）：', '*σ*_{v}−2*c*_{u}，不另加水', f"錯法只剩 {d['ratio'] * 100:.0f}%"], KEY2, KEY)
    return svg(W, H, o, '水土分開')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
