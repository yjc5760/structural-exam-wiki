# -*- coding: utf-8 -*-
"""第 2 章：Coulomb 楔體與力三角形、P(ρ) 掃描、M-O 作用點。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig2_1():
    d = ex2016_4()
    W_, H_ = 900, 440
    o = ''
    s = 34
    ox, oy = 170, 370       # A 點（牆踵底）
    X = lambda x: ox + x * s
    Y = lambda y: oy - y * s
    rho, Hh, dx = 62.2, 8.0, 2.0
    Pf, Wt, R, g = coulomb_trial(rho)
    xc = g['xc']
    # 牆（左）
    o += P([(X(-5), Y(0)), (X(0), Y(0)), (X(-dx), Y(Hh)), (X(-5), Y(Hh))], INK, 2, fill=STEEL2, close=True)
    o += L(X(-dx), Y(Hh), X(9), Y(Hh), INK, 1.6)
    o += P([(X(0), Y(0)), (X(-dx), Y(Hh)), (X(xc), Y(Hh))], TEN, 2, fill=TEN2, close=True)
    o += T(X(xc * 0.35), Y(Hh * 0.6), '試驗楔', 15, TEN, 'middle', 'bold')
    o += T(X(1.0) + 6, Y(0.9), f'*ρ*={rho}°', 14, COMP, 'start', 'bold')
    o += T(X(-dx / 2) - 6, Y(Hh / 2), '*β*', 15, KEY, 'end', 'bold')
    o += C(X(0), Y(0), 5, INK, '#fff', 1.4) + T(X(0) + 6, Y(0) + 20, 'A（牆踵）', 14, INK, 'start')
    # 力三角形
    fx, fy = 640, 40
    sc = 0.62
    p1 = (fx, fy)
    p2 = (fx, fy + Wt * sc)                                 # W 往下
    pR = (p2[0] + R * g['rd'][0] * sc, p2[1] - R * g['rd'][1] * sc)
    o += A(*p1, *p2, AC, 3, 12) + T(p1[0] + 10, (p1[1] + p2[1]) / 2, f'*W*={Wt:.0f}', 15, AC, 'start', 'bold')
    o += A(*p2, *pR, COMP, 3, 12) + T((p2[0] + pR[0]) / 2 - 12, (p2[1] + pR[1]) / 2 + 10, '*R*（偏法線 *φ*）', 15, COMP, 'end', 'bold')
    o += A(*pR, *p1, TEN, 3, 12) + T((pR[0] + p1[0]) / 2 - 10, (pR[1] + p1[1]) / 2 - 12, f'*P*={Pf:.1f}（偏法線 *δ*）', 15, TEN, 'end', 'bold')
    o += T(fx + 60, fy + Wt * sc + 36, '頭尾相接必須閉合', 15, KEY, 'middle', 'bold')
    return svg(W_, H_, o, 'Coulomb 楔體')


def fig2_2():
    d = ex2016_4()
    W, H = 900, 400
    pl = Plot(90, 50, 560, 290, 30, 80, 100, 320)
    o = pl.axes([30, 40, 50, 60, 70, 80], [100, 150, 200, 250, 300], '*ρ* (°)', '*P* (kN/m)')
    b, rows = coulomb_scan()
    b2, rows2 = coulomb_scan(kh=0.15, kv=0.05)
    o += P([pl.pt(r, p) for r, p in rows if 100 <= p <= 320], TEN, 3)
    o += P([pl.pt(r, p) for r, p in rows2 if 100 <= p <= 320], COMP, 2.4, dash='7 4')
    o += pl.dot(b[0], b[1], KEY, 6.5) + T(pl.X(b[0]) + 10, pl.Y(b[1]) + 22, f"靜態 max {b[1]:.2f} @ {b[0]:.1f}°", 15, KEY, 'start', 'bold')
    o += pl.dot(b2[0], b2[1], COMP, 6.5) + T(pl.X(b2[0]) - 10, pl.Y(b2[1]) - 12, f"地震 max {b2[1]:.2f} @ {b2[0]:.1f}°", 15, COMP, 'end', 'bold')
    o += box(670, 70, 215, 150, '與公式對照', [f"½*γH*²*K*_{{a}}={d['Pa']:.2f}", f"*P*_{{ae}}={d['Pae']:.2f}", '逐點三力閉合', '＝公式結果'], KEY2, KEY)
    return svg(W, H, o, 'P(ρ) 掃描')


def fig2_3():
    d = ex2016_4()
    W, H = 900, 400
    o = ''
    x0, y0, zs = 420, 40, 38
    Hh = d['H']
    Y = lambda z: y0 + (Hh - z) * zs    # z 從牆底往上
    o += L(x0, Y(0), x0, Y(Hh), STEEL, 6)
    sc = 2.6
    pmax = 2 * d['Pa'] / Hh
    o += P([(x0, Y(Hh)), (x0 - pmax * sc, Y(0)), (x0, Y(0))], TEN, 2, fill=TEN2, close=True)
    pd = 2 * d['dPae'] / Hh
    o += P([(x0, Y(0)), (x0 + pd * sc, Y(Hh)), (x0, Y(Hh))], COMP, 2, fill=COMP2, close=True, op=0.9)
    o += A(x0 - 230, Y(Hh / 3), x0 - 4, Y(Hh / 3), TEN, 2.8, 12) + T(x0 - 234, Y(Hh / 3) - 8, f"*P*_{{a}}={d['Pa']:.2f} @ *H*/3", 15, TEN, 'end', 'bold')
    o += A(x0 + 230, Y(0.6 * Hh), x0 + 4, Y(0.6 * Hh), COMP, 2.8, 12) + T(x0 + 234, Y(0.6 * Hh) - 8, f"Δ*P*_{{ae}}={d['dPae']:.2f} @ 0.6*H*", 15, COMP, 'start', 'bold')
    o += C(x0, Y(d['zbar']), 7, KEY, '#fff', 2) + T(x0 + 12, Y(d['zbar']) + 22, f"合力 {d['Pae']:.2f} @ {d['zbar']:.2f} m", 15, KEY, 'start', 'bold')
    o += T(x0 + 8, Y(0) + 24, '牆底', 14, MUT, 'start')
    o += T(x0 + 40, Y(Hh) + 4, '增量：倒三角形（示意）', 14, COMP, 'start')
    return svg(W, H, o, 'M-O 作用點')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
