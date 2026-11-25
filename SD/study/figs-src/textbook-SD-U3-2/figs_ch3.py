# -*- coding: utf-8 -*-
"""第 3 章：等值阻尼（能量比）、B 係數、2023-4 三種迴圈。"""
from sdfig import *  # noqa
from calcs import B_TAB, TAB4, Q2008
import math


def fig3_1():
    W, H = 900, 380
    pl = Plot(90, 40, 420, 290, -1.25, 1.25, -1.25, 1.25)
    o = pl.axes([-1, 0, 1], [-1, 0, 1], '*u*', '*F*', grid=False, xfmt=lambda v: {-1: '−*u*_{0}', 0: '0', 1: '*u*_{0}'}[v], yfmt=lambda v: '')
    ell = [pl.pt(math.cos(t), 0.55 * math.cos(t) + 0.45 * math.sin(t)) for t in [i * 2 * math.pi / 120 for i in range(121)]]
    o += P(ell, TEN, 0, fill=TEN2, close=True) + P(ell, TEN, 3)
    o += P([pl.pt(0, 0), pl.pt(1, 0.55), pl.pt(1, 0)], AC, 0, fill=AC2, close=True)
    o += L(pl.X(-1.1), pl.Y(-0.6), pl.X(1.1), pl.Y(0.6), AC, 2.4)
    o += T(pl.X(-0.45), pl.Y(0.55), '*E*_{D}：一圈的面積', 15, TEN, 'middle', 'bold')
    o += T(pl.X(0.72), pl.Y(0.14), '*E*_{So}', 15, AC, 'middle', 'bold')
    o += T(pl.X(1.12), pl.Y(0.66), '*k*', 15, AC, 'start', 'bold')
    o += box(560, 40, 330, 300, '能量等值', ['真實迴圈 ↔ 黏滯橢圓：', '每圈吃掉同樣的能量', '彈性儲能 *E*_{So} = ½*ku*_{0}²', '黏滯：*E*_{D} = π*c*ω*u*_{0}²', '⇒ ξ = *c*/(2*m*ω_{n})', '= *E*_{D}/(4π*E*_{So}) · ω_{n}/ω', '雙線性：*A*_{TD}/(2π*K*_{eD}*D*²)', '（ω = ω_{n} 時括號項 = 1）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '等值阻尼能量比')


def fig3_2():
    W, H = 900, 360
    pl = Plot(90, 40, 410, 260, 0, 52, 0.6, 1.9)
    o = pl.axes([0, 10, 20, 30, 40, 50], [0.8, 1.0, 1.25, 1.5, 1.75], 'ξ (%)', '*B*', yfmt=lambda v: f'{v:g}')
    o += P([pl.pt(x, b) for x, b in B_TAB], KEY, 3)
    for x, b in B_TAB:
        o += pl.dot(x, b, KEY, 5)
        o += T(pl.X(x) - 6, pl.Y(b) - 8, f'{b:g}', 14, KEY, 'end')
    o += T(pl.X(26), pl.Y(1.08), '阻尼加倍、效果遞減', 15, WARN, 'middle', 'bold')
    o += box(570, 40, 320, 270, '*B* 怎麼用', ['設計譜除以 *B*：*S*_{a}/*B*', '*B* 越大 → 反應越小', '5% → 1.0（基準）', '10% → 1.25、20% → 1.5', '2008-3：共振時 2%→20%', f'位移比 = {Q2008["ratio"]:.2f}（MF = 1/2ξ）', '*T*_{n}/*T*_{f} = 1.5 時只剩 0.90', '→ 阻尼只在共振附近有效'], KEY2, KEY, 15, 14.5)
    o += T(310, 345, '圖中為 *B*_{1}（長週期）表值；*B*_{S}（短週期）略大（10% 1.33、20% 1.6）', 14, MUT, 'middle')
    return svg(W, H, o, 'B 係數')


def fig3_3():
    W, H = 900, 400
    o = ''
    titles = [('(a) 黏滯 *c* = 5：橢圓', TEN), ('(b) 速率無關：橢圓', KEY), ('(c) 摩擦 ±0.4π：矩形', WARN)]
    for j, (ttl, col) in enumerate(titles):
        ox = 15 + j * 295
        pl = Plot(ox + 30, 60, 240, 170, -1.3, 1.3, -1.3, 1.3)
        o += T(ox + 150, 34, ttl, 15, col, 'middle', 'bold')
        o += pl.axes([0], [0], '*u*', '*F*', grid=False)
        if j < 2:
            pts = [pl.pt(math.cos(t), math.sin(t)) for t in [i * 2 * math.pi / 100 for i in range(101)]]
        else:
            pts = [pl.pt(*p) for p in ((-1, -1), (-1, 1), (1, 1), (1, -1), (-1, -1))]
        col2 = {TEN: TEN2, KEY: KEY2, WARN: WARN2}[col]
        o += P(pts, col, 0, fill=col2, close=True) + P(pts, col, 3)
        lab = ['半高 5ω̄ρ', '半高 20πρ', '半高 0.4π'][j]
        o += T(pl.X(0) + 6, pl.Y(1.15), lab, 14, col, 'start', 'bold')
    rows = [('ω̄ = 2π, ρ = 0.01', (2 * math.pi, 0.01)), ('ω̄ = 2π, ρ = 0.02', (2 * math.pi, 0.02)), ('ω̄ = 4π, ρ = 0.01', (4 * math.pi, 0.01)), ('ω̄ = 4π, ρ = 0.02', (4 * math.pi, 0.02))]
    y = 272
    o += T(140, y, '組合', 14.5, INK, 'middle', 'bold') + T(370, y, '(a)', 14.5, TEN, 'middle', 'bold') + T(580, y, '(b)', 14.5, KEY, 'middle', 'bold') + T(790, y, '(c)', 14.5, WARN, 'middle', 'bold')
    for i, (lab, key) in enumerate(rows):
        yy = y + 26 * (i + 1)
        a, b, c = TAB4[key]
        o += T(140, yy, lab, 14.5, INK, 'middle') + T(370, yy, f'{a*100:.1f}%', 14.5, TEN, 'middle') + T(580, yy, f'{b*100:.1f}%', 14.5, KEY, 'middle') + T(790, yy, f'{c*100:.1f}%', 14.5, WARN, 'middle')
    return svg(W, H, o, '2023-4 三種迴圈')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
