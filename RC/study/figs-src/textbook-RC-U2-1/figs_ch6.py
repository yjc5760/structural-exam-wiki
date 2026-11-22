# -*- coding: utf-8 -*-
"""第 6 章：剪力＋扭力——薄壁管剪流、扭力門檻與偏心、扭剪共用箍筋。"""
from figs_common import *  # noqa
from calcs import p2023_3, p2018_1
import math

P23 = p2023_3()
P18 = p2018_1()


def fig6_1():
    W, H = 900, 400
    o = T(450, 24, '實心斷面 ≈ 薄壁管：剪流 *q* 繞一圈，*T* = *q* × 2*A*_{o}', 16, INK, 'middle', 'bold')
    x0, y0, bw, bh, t = 120, 70, 210, 300, 34
    o += R(x0, y0, bw, bh, STEEL2, INK, 1.6)
    o += R(x0 + t, y0 + t, bw - 2 * t, bh - 2 * t, '#fff', INK, 1.2, dash='5 4')
    o += T(x0 + bw / 2, y0 + bh / 2 - 10, '中心', 15, MUT, 'middle')
    o += T(x0 + bw / 2, y0 + bh / 2 + 12, '幾乎不出力', 15, MUT, 'middle')
    cx0, cy0, cw, ch = x0 + t / 2, y0 + t / 2, bw - t, bh - t
    o += R(cx0, cy0, cw, ch, 'none', WARN, 2, dash='2 3')
    # 剪流箭頭（逆時針）
    for i in range(3):
        xx = cx0 + 30 + i * 60
        o += A(xx + 30, cy0, xx, cy0, WARN, 2.2, 9)
        o += A(xx, cy0 + ch, xx + 30, cy0 + ch, WARN, 2.2, 9)
    for i in range(4):
        yy = cy0 + 40 + i * 62
        o += A(cx0, yy, cx0, yy + 30, WARN, 2.2, 9)
        o += A(cx0 + cw, yy + 30, cx0 + cw, yy, WARN, 2.2, 9)
    o += T(x0 + bw + 10, y0 + 60, '*q*', 18, WARN, 'start', 'bold')
    o += dim(x0 + bw + 30, y0, x0 + bw + 30, y0 + t, '', INK)
    o += T(x0 + bw + 40, y0 + t / 2 + 6, '*t*', 16, INK, 'start', 'bold')
    # 右：力矩推導示意
    px, py, pw, ph = 520, 90, 260, 220
    o += R(px, py, pw, ph, 'none', WARN, 2.2)
    gx, gy = px + pw / 2, py + ph / 2
    o += C(gx, gy, 5, INK, '#fff', 1)
    o += T(gx + 8, gy + 18, '形心', 14, INK, 'start')
    sx1, sx2 = px + pw - 0, py + 60
    o += P([(gx, gy), (px + pw, py + 60), (px + pw, py + 120)], None, fill=KEY2, close=True)
    o += P([(gx, gy), (px + pw, py + 60), (px + pw, py + 120)], KEY, 1.6, close=True)
    o += A(px + pw + 26, py + 120, px + pw + 26, py + 60, WARN, 2.4, 9)
    o += T(px + pw + 34, py + 96, '*q*·*ds*', 15, WARN, 'start', 'bold')
    o += L(gx, gy, px + pw, gy, INK, 1.4, '4 3')
    o += T((gx + px + pw) / 2, gy + 20, '*r*', 16, INK, 'middle', 'bold')
    o += T(px + pw / 2, py + ph + 34, '力矩 *q*·*ds*·*r* = *q* × (三角形面積 × 2)', 15, KEY, 'middle', 'bold')
    o += T(px + pw / 2, py + ph + 58, '繞一圈：*T* = *q* × 2*A*_{o}', 16, KEY, 'middle', 'bold')
    o += T(px + pw / 2, py - 12, '*A*_{o}＝剪流路徑圍成的面積', 15, WARN, 'middle', 'bold')
    return svg(W, H, o, '薄壁管剪流')


def fig6_2():
    W, H = 900, 400
    pl = Plot(110, 50, 520, 290, 0, 14, 0, 1.2)
    o = pl.axes([0, 2, 4, 6, 8, 10, 12, 14], [0, 0.3, 0.6, 0.9, 1.2], '*e*', '*T*_{u}', size=14, yfmt=lambda v: f'{v:.1f}')
    o += T(pl.X(14) + 18, pl.Y(0) + 26, '(cm)', 14, MUT, 'start')
    o += T(pl.X(0) + 34, pl.Y(1.2) - 22, '(tf·m)', 14, MUT, 'start')
    V = P23['Vu'] / 1000
    th = P23['phiTth'] / 1e5
    tw = P23['Tth_wrong'] / 1e5
    o += pl.area(lambda e: th, lambda e: 0, 0, 14, TEN2, 0.6)
    o += pl.curve(lambda e: V * e / 100, 0, 14, AC, 3)
    o += pl.hline(th, 0, 14, TEN, 2.4, None)
    o += pl.hline(tw, 0, 14, MUT, 1.8, '6 4')
    o += pl.dot(P23['emax'], th, KEY, 6)
    o += pl.vline(P23['emax'], 0, th, KEY, 1.6)
    o += T(pl.X(P23['emax']) + 8, pl.Y(0) - 14, f"*e*_{{max}} = {P23['emax']:.2f}", 15, KEY, 'start', 'bold')
    o += pl.dot(P23['e_wrong'], tw, MUT, 5)
    o += T(pl.X(P23['e_wrong']) + 6, pl.Y(tw) - 10, f"誤用 1/12：{P23['e_wrong']:.2f}", 14, MUT, 'start', 'bold')
    o += T(pl.X(0.3), pl.Y(th) - 10, f'φ*T*_{{th}} = {th:.3f}', 15, TEN, 'start', 'bold')
    o += T(pl.X(1.0), pl.Y(th / 2), '扭力可忽略', 15, TEN, 'start', 'bold')
    o += T(pl.X(13.5), pl.Y(V * 13.5 / 100) - 12, f'*T*_{{u}} = *V*_{{u}}·*e*（*V*_{{u}} = {V:.2f} tf）', 14, AC, 'end', 'bold')
    o += box(660, 80, 225, 200, 'RC-2023-3', [f"*A*_{{cp}} = {P23['Acp']:.0f} cm²", f"*p*_{{cp}} = {P23['pcp']:.0f} cm", f"*T*_{{th}} = {P23['Tth']/1e5:.3f} tf·m", f"*T*_{{cr}} = {P23['Tcr']/1e5:.3f} tf·m", '（*T*_{th} = *T*_{cr}/4）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '扭力門檻與偏心')


def fig6_3():
    W, H = 900, 400
    o = T(450, 24, '外圍箍的一肢：扭力 *A*_{t}/*s* ＋ 分到的剪力 *A*_{v}/(4*s*)', 16, INK, 'middle', 'bold')
    sc = 5.2
    x0, y0, b = 80, 70, P18['b']
    o += R(x0, y0, b * sc, b * sc, STEEL2, INK, 1.6)
    cv = P18['cover'] + P18['dbt'] / 2
    o += R(x0 + cv * sc, y0 + cv * sc, (b - 2 * cv) * sc, (b - 2 * cv) * sc, 'none', COMP, 3.2, 6)
    for f_ in (1 / 3, 2 / 3):
        xx = x0 + cv * sc + (b - 2 * cv) * sc * f_
        o += L(xx, y0 + cv * sc, xx, y0 + (b - cv) * sc, TEN, 2.4)
    o += T(x0 + b * sc / 2, y0 + b * sc + 30, '紅＝外圍閉合箍（抗扭＋抗剪）', 14, COMP, 'middle', 'bold')
    o += T(x0 + b * sc / 2, y0 + b * sc + 52, '綠＝繫筋（只抗剪）', 14, TEN, 'middle', 'bold')
    o += T(x0 - 8, y0 + 18, f'{b:.0f}×{b:.0f}', 15, INK, 'end', 'bold')
    # 右：長條圖
    bx, by, bw = 470, 110, 300
    k = bw / 0.10
    at, av4 = P18['At_s'], P18['Av_s'] / 4
    o += T(bx, by - 18, '外圍箍一肢（cm²/cm）', 15, COMP, 'start', 'bold')
    o += R(bx, by, at * k, 40, COMP2, COMP, 1.4)
    o += R(bx + at * k, by, av4 * k, 40, TEN2, TEN, 1.4)
    o += T(bx + at * k / 2, by + 26, f'{at:.4f}', 14, COMP, 'middle', 'bold')
    o += T(bx + at * k + av4 * k + 8, by + 26, f'+{av4:.4f} = {at+av4:.4f}', 14, INK, 'start', 'bold')
    o += T(bx, by + 64, '扭力', 14, COMP, 'start') + T(bx + at * k + 4, by + 64, '剪力', 14, TEN, 'start')
    o += T(bx, by + 116, '繫筋一肢', 15, TEN, 'start', 'bold')
    o += R(bx, by + 128, av4 * k, 40, TEN2, TEN, 1.4)
    o += T(bx + av4 * k + 8, by + 154, f'{av4:.4f}', 14, TEN, 'start', 'bold')
    o += box(bx, by + 196, 380, 70, '', [], '#fff', KEY)
    o += T(bx + 190, by + 222, f"D13：*s* ≤ {P18['Ab']:.3f} / {at+av4:.4f} = {P18['s']:.1f} cm", 15, KEY, 'middle', 'bold')
    o += T(bx + 190, by + 248, '→ 4 肢 D13 @15 cm', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '扭剪共用箍筋')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
