# -*- coding: utf-8 -*-
"""第 3 章：有效應力剖面、降水、2:1 法。"""
from plot import *  # noqa
from calcs import *  # noqa


def _profile_plot(x0, y0, w, h, zmax, smax):
    """深度往下為正的座標：回傳 (X(s), Y(z)) 函式。"""
    X = lambda s: x0 + s / smax * w
    Y = lambda z: y0 + z / zmax * h
    return X, Y


def fig3_1():
    d = ex2021_2()
    W, H = 900, 470
    # 左：土層柱
    o = ''
    Yc = lambda z: 50 + z * 52
    lay = [(0, 1, '#fff8e1', '乾砂 16.5'), (1, 2, '#e3f2fd', '飽和砂 18.5'), (2, 7, '#ede7f6', '黏土 20.0（*C*_{c}=0.5、*e*_{0}=0.9）')]
    for a, b, fc, nm in lay:
        o += R(40, Yc(a), 150, Yc(b) - Yc(a), fc, MUT, 1)
    o += T(115, Yc(0.5) + 5, '乾砂 16.5', 14, INK, 'middle') + T(115, Yc(1.5) + 5, '飽和砂 18.5', 14, INK, 'middle')
    o += T(115, Yc(3.2) + 5, '黏土', 15, INK, 'middle', 'bold') + T(115, Yc(3.2) + 26, '*γ*_{sat}=20', 14, INK, 'middle')
    o += L(40, Yc(1), 190, Yc(1), AC, 2, '6 4') + T(186, Yc(1) - 5, '▽', 14, AC, 'end')
    o += L(40, Yc(4.5), 190, Yc(4.5), KEY, 1.3, '3 3') + T(115, Yc(4.5) + 22, '中點 4.5 m', 14, KEY, 'middle', 'bold')
    for z in range(0, 8):
        o += T(32, Yc(z) + 5, f'{z}', 14, MUT, 'end')
    # 右：應力圖
    x0, w = 260, 430
    smax = 140
    X = lambda s: x0 + s / smax * w
    o += A(x0, Yc(0), x0 + w + 20, Yc(0), INK, 1.5) + A(x0, Yc(0), x0, Yc(7) + 20, INK, 1.5)
    for s in (0, 20, 40, 60, 80, 100, 120):
        o += L(X(s), Yc(0), X(s), Yc(7), GRID, 1) + T(X(s), Yc(0) - 8, f'{s}', 14, MUT, 'middle')
    o += T(x0 + w + 24, Yc(0) + 5, 'kPa', 14, INK)
    o += T(x0 - 8, Yc(7) + 30, '深度 (m)', 14, INK, 'end')
    sig = lambda z: 16.5 * min(z, 1) + 18.5 * max(0, min(z, 2) - 1) + 20 * max(0, z - 2)
    u = lambda z: GW * max(0, z - 1)
    zs = [i * 0.05 for i in range(141)]
    o += P([(X(sig(z)), Yc(z)) for z in zs], MUT, 2.6)
    o += P([(X(u(z)), Yc(z)) for z in zs], AC, 2.6)
    o += P([(X(sig(z) - u(z)), Yc(z)) for z in zs], TEN, 3)
    zm = d['zmid']
    for val, c, nm, dx in ((d['sig'], MUT, '*σ*', 10), (d['u'], AC, '*u*', -10), (d['p0'], TEN, '*σ*′', 10)):
        o += C(X(val), Yc(zm), 5.5, c, '#fff', 1.6)
    o += T(X(d['sig']) + 10, Yc(zm) - 8, f"*σ*={d['sig']:.2f}", 15, MUT, 'start', 'bold')
    o += T(X(d['u']) - 10, Yc(zm) + 24, f"*u*={d['u']:.2f}", 15, AC, 'end', 'bold')
    o += T(X(d['p0']) + 10, Yc(zm) + 24, f"*p*_{{0}}′={d['p0']+1e-9:.2f}", 15, TEN, 'start', 'bold')
    o += A(X(d['p0']), Yc(zm) - 32, X(d['sig']), Yc(zm) - 32, AC, 1.6, 9, both=True)
    o += T((X(d['p0']) + X(d['sig'])) / 2, Yc(zm) - 40, '差＝*u*', 14, AC, 'middle')
    o += T(X(sig(6.6)) + 8, Yc(6.6), '總應力', 14, MUT, 'start')
    o += T(X(u(6.6)) - 8, Yc(6.6), '水壓', 14, AC, 'end')
    o += T(X(sig(6.2) - u(6.2)) + 8, Yc(6.2) + 18, '有效應力', 14, TEN, 'start', 'bold')
    o += box(712, 330, 175, 90, '忘了扣 *u*', [f"*p*_{{0}}′ 誤為 {d['p0_wrong']:.0f}", f"*S*_{{c}}: {d['Sc']:.2f}→{d['Sc_wrong']:.2f} cm"], COMP2, COMP)
    return svg(W, H, o, '有效應力剖面')


def fig3_2():
    d = ex2024_3()
    W, H = 900, 530
    Yc = lambda z: 40 + z * 14.5
    x0, w, smax = 230, 520, 420
    X = lambda s: x0 + s / smax * w
    o = ''
    lay = [(0, 8, '#fff8e1', '覆土'), (8, 20, '#e3f2fd', '砂'), (20, 30, '#ede7f6', '黏土')]
    for a, b, fc, nm in lay:
        o += R(60, Yc(a), 120, Yc(b) - Yc(a), fc, MUT, 1) + T(120, (Yc(a) + Yc(b)) / 2 + 5, nm, 15, INK, 'middle', 'bold')
    o += L(60, Yc(2), 180, Yc(2), AC, 2, '6 4') + T(54, Yc(2) + 5, '前 ▽2', 14, AC, 'end')
    o += L(60, Yc(18), 180, Yc(18), COMP, 2, '6 4') + T(54, Yc(18) + 5, '後 ▽18', 14, COMP, 'end')
    for z in (0, 10, 20, 30):
        o += T(216, Yc(z) + 5, f'{z} m', 14, MUT, 'end')
    o += A(x0, Yc(0), x0 + w + 20, Yc(0), INK, 1.5) + A(x0, Yc(0), x0, Yc(30) + 18, INK, 1.5)
    for s in range(0, 401, 100):
        o += L(X(s), Yc(0), X(s), Yc(30), GRID, 1) + T(X(s), Yc(0) - 8, f'{s}', 14, MUT, 'middle')
    o += T(x0 + w + 24, Yc(0) + 5, "*σ*′ (kPa)", 14, INK)

    def sp(z, after, wrong=False):
        if not after:
            g = [(0, 2, 16.0), (2, 8, 19.68 - GW), (8, 20, 18.29 - GW), (20, 30, 21.78 - GW)]
        elif wrong:
            return sp(z, False) + (GW * min(max(z - 2, 0), 16))
        else:
            g = [(0, 8, 16.0), (8, 18, d['g_sand_d']), (18, 20, 18.29 - GW), (20, 30, 21.78 - GW)]
        s = 0
        for a, b, gg in g:
            if z > a:
                s += gg * (min(z, b) - a)
        return s
    zs = [i * 0.1 for i in range(301)]
    o += P([(X(sp(z, False)), Yc(z)) for z in zs], TENM, 3)
    o += P([(X(sp(z, True)), Yc(z)) for z in zs], TEN, 3.2)
    o += P([(X(sp(z, True, True)), Yc(z)) for z in zs if z <= 21], COMP, 2, dash='7 5')
    o += L(X(d['pc']), Yc(20), X(d['pc']), Yc(30), KEY, 1.8, '6 4') + T(X(d['pc']) + 6, Yc(29.5), "*p*_{c}′=300", 14, KEY, 'start', 'bold')
    for z, a, b in ((20, d['pC0'], d['pC1']), (25, d['p0'], d['pf'])):
        o += C(X(a), Yc(z), 5, TENM, '#fff', 1.5) + C(X(b), Yc(z), 5.5, TEN, '#fff', 1.6)
        o += A(X(a) + 6, Yc(z), X(b) - 7, Yc(z), TEN, 1.8, 9)
    o += T(X(d['pC0']) - 8, Yc(20) - 8, f"C {d['pC0']:.2f}", 14, TEN, 'end', 'bold')
    o += T(X(d['pC1']) + 16, Yc(20) + 20, f"{d['pC1']:.2f}", 14, TEN, 'start', 'bold')
    o += T(X(d['p0']) - 8, Yc(25) + 5, f"D {d['p0']:.2f}", 14, TEN, 'end', 'bold')
    o += T(X(d['pf']) + 14, Yc(25) + 5, f"{d['pf']:.2f}", 14, TEN, 'start', 'bold')
    o += T(X(sp(12, True, True)) + 10, Yc(12), f"錯：水位上用 *γ*_{{sat}}（C 點 +{d['dp_wrong']:.2f}）", 14, COMP, 'start')
    o += box(640, 70, 235, 110, '黏土內處處相同', [f"Δ*σ*′＝{d['dp']:.2f} kPa", '水壓少 156.96', '土變輕 49.98'], KEY2, KEY)
    return svg(W, H, o, '降水前後有效應力')


def fig3_3():
    d = ex2011_3()
    W, H = 900, 440
    o = ''
    s = 42   # px per m
    xc, yb = 220, 70
    B = d['B']
    o += R(xc - B / 2 * s, yb - 18, B * s, 18, STEEL3, INK, 1.4) + A(xc, yb - 60, xc, yb - 20, COMP, 2.6, 12) + T(xc + 10, yb - 40, '*Q*=1000 kN', 15, COMP, 'start', 'bold')
    Y = lambda z: yb + z * s * 1.65
    o += R(40, Y(d['zt']), 360, Y(d['zb']) - Y(d['zt']), '#ede7f6', None, 0)
    o += T(50, Y(d['zt']) + 22, '黏土 3 m', 15, INK, 'start', 'bold')
    for z in (d['zt'], d['zb']):
        o += L(40, Y(z), 400, Y(z), MUT, 1)
    zb = 5.0
    o += P([(xc - B / 2 * s, yb), (xc - (B + zb) / 2 * s, Y(zb)), (xc + (B + zb) / 2 * s, Y(zb)), (xc + B / 2 * s, yb)], WARN, 1.8, dash='7 4')
    o += T(xc + (B + 1.0) / 2 * s + 6, Y(1.0), '2', 14, WARN) + T(xc + (B + 1.0) / 2 * s + 16, Y(1.0) + 18, '1', 14, WARN)
    for z, v, nm in ((d['zt'], d['dt'], '頂'), ((d['zt'] + d['zb']) / 2, d['dm'], '中'), (d['zb'], d['db'], '底')):
        o += L(xc - (B + z) / 2 * s, Y(z), xc + (B + z) / 2 * s, Y(z), WARN, 2.4)
    # 右圖
    pl = Plot(500, 60, 300, 320, 0, 120, 0, 5)
    Yp = lambda z: 60 + z / 5 * 320
    X = pl.X
    o += A(500, 60, 820, 60, INK, 1.5) + A(500, 60, 500, 400, INK, 1.5)
    for v in (0, 40, 80, 120):
        o += L(X(v), 60, X(v), 380, GRID, 1) + T(X(v), 50, f'{v}', 14, MUT, 'middle')
    for z in (0, 1, 2, 3, 4, 5):
        o += T(492, Yp(z) + 5, f'{z}', 14, MUT, 'end')
    o += T(824, 65, 'Δ*p* (kPa)', 14, INK) + T(492, 420, '基底下 *z* (m)', 14, INK, 'end')
    o += R(500, Yp(d['zt']), 320, Yp(d['zb']) - Yp(d['zt']), '#ede7f6', None, 0, op=0.6)
    f = lambda z: d['Q'] / (d['B'] + z) ** 2
    zs = [0.6 + i * 0.022 for i in range(200)]
    o += P([(X(min(f(z), 120)), Yp(z)) for z in zs if f(z) <= 120], WARN, 3)
    for z, v, nm, anc in ((d['zt'], d['dt'], '頂', 'end'), ((d['zt'] + d['zb']) / 2, d['dm'], '中', 'end'), (d['zb'], d['db'], '底', 'start')):
        o += C(X(v), Yp(z), 5, WARN, '#fff', 1.5)
        o += T(X(v) + (12 if anc == 'start' else -10), Yp(z) + (18 if nm == '頂' else 5), f'{nm} {v:.2f}', 14, WARN, anc, 'bold')
    o += L(X(d['davg']), Yp(d['zt']), X(d['davg']), Yp(d['zb']), KEY, 2.4, '6 4')
    o += T(X(d['davg']) + 6, Yp(d['zb']) - 10, f"平均 {d['davg']:.2f}", 15, KEY, 'start', 'bold')
    return svg(W, H, o, '2:1 法與層平均')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
