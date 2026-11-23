# -*- coding: utf-8 -*-
"""第 2 章：懸臂樁變形與淨壓力、2022-4 數值圖。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig2_1():
    W, H = 900, 440
    o = ''
    x0, y0 = 260, 50
    Y = lambda z: y0 + z * 28
    Hx, D = 6.0, 6.0
    o += R(60, Y(0), x0 - 60, Y(Hx + D) - Y(0), '#efe6d8', None, 0) + R(x0, Y(Hx), 220, Y(Hx + D) - Y(Hx), '#efe6d8', None, 0)
    o += L(60, Y(0), x0, Y(0), INK, 1.6) + T(70, Y(0) - 8, '坑外', 15, INK)
    o += L(x0, Y(Hx), x0 + 220, Y(Hx), INK, 1.6) + T(x0 + 215, Y(Hx) - 8, '坑內', 15, INK, 'end')
    o += L(x0, Y(0), x0, Y(Hx + D), STEEL, 6)
    zO = Hx + 0.8 * D
    o += L(x0 + (zO - 0) * 5, Y(0), x0 + (zO - (Hx + D)) * 5, Y(Hx + D), COMP, 2.2, '6 4')
    o += T(x0 + zO * 5 + 6, Y(0) + 14, '變形後（誇大）', 14, COMP, 'start')
    o += C(x0, Y(zO), 6, KEY, '#fff', 1.8) + T(x0 - 10, Y(zO) + 5, 'O（轉動點）', 15, KEY, 'end', 'bold')
    # 淨壓力圖
    xp = 640
    o += L(xp, Y(0), xp, Y(Hx + D), INK, 2)
    pa3, L3 = 22.0, 0.7
    s = 4.0
    o += P([(xp, Y(0)), (xp - pa3 * s, Y(Hx)), (xp, Y(Hx + L3))], TEN, 2, fill=TEN2, close=True)
    p3, p4 = 40.0, 30.0
    tip = Hx + D
    zc = zO + (tip - zO) * p3 / (p3 + p4)
    o += P([(xp, Y(Hx + L3)), (xp + p3 * s, Y(zO)), (xp, Y(zc))], COMP, 2, fill=COMP2, close=True)
    o += P([(xp, Y(zc)), (xp - p4 * s, Y(tip)), (xp, Y(tip))], WARN, 2, fill=WARN2, close=True)
    o += C(xp, Y(Hx + L3), 5, KEY, '#fff', 1.6) + T(xp + 10, Y(Hx + L3) - 2, 'E', 15, KEY, 'start', 'bold')
    o += T(xp - pa3 * s - 8, Y(Hx * 0.75), '主動（推）', 14, TEN, 'end', 'bold')
    o += T(xp + p3 * s + 8, Y(zO) + 5, '淨被動', 14, COMP, 'start', 'bold')
    o += T(xp - p4 * s - 8, Y(tip) - 4, '反扣', 14, WARN, 'end', 'bold')
    o += dim(xp + 200, Y(Hx), xp + 200, Y(Hx + L3), '', INK) + T(xp + 210, Y(Hx + L3 / 2) + 5, '*L*_{3}', 15, INK)
    o += dim(xp + 200, Y(Hx + L3), xp + 200, Y(tip), '', INK) + T(xp + 210, Y(Hx + D / 2) + 5, '*L*_{4}', 15, INK)
    o += L(xp, Y(Hx), xp + 190, Y(Hx), MUT, 1, '4 3') + T(xp + 186, Y(Hx) - 6, '開挖面', 14, MUT, 'end')
    o += T(xp, Y(tip) + 28, '淨壓力圖（示意）', 14, MUT, 'middle')
    return svg(W, H, o, '懸臂樁淨壓力')


def fig2_2():
    d = ex2022_4()
    W, H = 900, 520
    o = ''
    x0, y0, zs, sc = 330, 40, 26, 5.0
    Y = lambda z: y0 + z * zs
    L1, L2, L3, L4 = d['L1'], d['L2'], d['L3'], d['L4s']
    o += L(x0, Y(0), x0, Y(L1 + L2 + L3 + L4), STEEL, 6)
    o += L(x0, Y(L1), x0 - 300, Y(L1), AC, 1.6, '6 4') + T(x0 - 300, Y(L1) - 6, '▽ 水位（兩側同高）', 14, AC, 'start')
    o += L(x0, Y(L1 + L2), x0 + 300, Y(L1 + L2), INK, 1.4) + T(x0 + 300, Y(L1 + L2) - 6, '開挖面', 14, INK, 'end')
    # 主動壓（左側）
    pts = [(x0, Y(0)), (x0 - d['pa2'] * sc, Y(L1)), (x0 - d['pa3'] * sc, Y(L1 + L2)), (x0, Y(L1 + L2 + L3))]
    o += P(pts, TEN, 2, fill=TEN2, close=True)
    o += T(x0 - d['pa2'] * sc - 6, Y(L1) + 5, f"{d['pa2']:.2f}", 14, TEN, 'end', 'bold')
    o += T(x0 - d['pa3'] * sc - 6, Y(L1 + L2) + 5, f"{d['pa3']:.2f}", 14, TEN, 'end', 'bold')
    zE = L1 + L2 + L3
    o += C(x0, Y(zE), 5, KEY, '#fff', 1.6) + T(x0 + 10, Y(zE) + 5, f"E：*L*_{{3}}={L3:.4f} m", 14, KEY, 'start', 'bold')
    # 淨被動三角形（右側）
    pmax = d['k'] * L4
    sc2 = 1.0
    o += P([(x0, Y(zE)), (x0 + pmax * sc2, Y(zE + L4)), (x0, Y(zE + L4))], COMP, 2, fill=COMP2, close=True)
    o += T(x0 + pmax * sc2 + 8, Y(zE + L4) + 5, f"{pmax:.1f} kPa（另一比例）", 14, COMP, 'start', 'bold')
    o += T(x0 + 60, Y(zE + L4 * 0.62), '淨被動 *γ*′(*K*_{p}−*K*_{a})*z*', 14, COMP, 'start', 'bold')
    # 合力 P
    yP = Y(zE - d['zbar'])
    o += A(x0 - 160, yP, x0 - 4, yP, WARN, 3, 12)
    o += T(x0 - 165, yP - 8, f"*P*={d['P']:.2f}", 15, WARN, 'end', 'bold')
    o += dim(x0 - 230, yP, x0 - 230, Y(zE), '', WARN) + T(x0 - 238, (yP + Y(zE)) / 2 + 5, f"*z̄*={d['zbar']:.3f}", 14, WARN, 'end', 'bold')
    o += C(x0, Y(zE + L4), 5, INK, '#fff', 1.6) + T(x0 - 8, Y(zE + L4) + 22, '樁尖（取矩點）', 14, INK, 'end', 'bold')
    o += box(640, 60, 250, 210, '兩種解法', ['精確（四次式）：', f"*L*_{{4}}={d['L4']:.3f}，*D*={d['DL']:.2f} m", '簡化（對樁尖取矩）：', f"*L*_{{4}}={d['L4s']:.2f}，*D*={d['Ds']:.2f} m", f"×1.2 → {d['Ds12']:.2f} m"], KEY2, KEY)
    return svg(W, H, o, '2022-4 淨壓力')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2}
