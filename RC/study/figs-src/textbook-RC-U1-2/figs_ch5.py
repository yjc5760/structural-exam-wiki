# -*- coding: utf-8 -*-
"""第 5 章：圍束——半圓自由體、保護層損失 vs 核心增益、加大柱、剪力摩擦。"""
from figs_col import *  # noqa
from calcs import rc2010_1, rc2017_1, rc2017_2, fc_2017
import math

RR = rc2010_1()


def fig5_1():
    W, H = 900, 430
    o = T(450, 26, '把螺旋筋切成兩半：兩支 *A*_{sp}*f*_{yt} 拉住整片側壓 *f*_{L}', 16, INK, 'middle', 'bold')
    # (a) 平面：圓
    cx, cy, r = 200, 220, 120
    o += C(cx, cy, r + 18, STEEL2, INK, 1.4)
    o += C(cx, cy, r, '#fff8e1', WARN, 3)
    o += T(cx, cy + r + 46, '(a) 平面：保護層（灰）、核心（黃）', 14, INK, 'middle', 'bold')
    for k in range(12):
        t = 2 * math.pi * k / 12
        o += A(cx + (r - 4) * math.cos(t), cy + (r - 4) * math.sin(t), cx + (r - 34) * math.cos(t), cy + (r - 34) * math.sin(t), WARN, 2, 8)
    o += T(cx, cy + 5, '*f*_{L}（往內推）', 15, WARN, 'middle', 'bold')
    # (b) 半圓自由體
    x0, y0, rr = 600, 230, 120
    pts = [(x0 + rr * math.cos(math.pi + math.pi * i / 60), y0 + rr * math.sin(math.pi + math.pi * i / 60)) for i in range(61)]
    o += P(pts + [(x0 + rr, y0), (x0 - rr, y0)], WARN, 3, fill='#fff8e1', close=True)
    for k in range(1, 8):
        xx = x0 - rr + 2 * rr * k / 8
        ytop = y0 - math.sqrt(max(rr ** 2 - (xx - x0) ** 2, 0))
        o += A(xx, y0 - 6, xx, ytop + 8, KEY, 1.8, 8)
    o += T(x0, y0 - rr - 14, '核心往外推螺旋筋：合力 *f*_{L}·*d*_{s}·*s*（向上）', 14, KEY, 'middle', 'bold')
    o += A(x0 - rr, y0 + 6, x0 - rr, y0 + 70, TEN, 3.2, 12)
    o += A(x0 + rr, y0 + 6, x0 + rr, y0 + 70, TEN, 3.2, 12)
    o += T(x0 - rr, y0 + 92, '*A*_{sp}*f*_{yt}', 15, TEN, 'middle', 'bold')
    o += T(x0 + rr, y0 + 92, '*A*_{sp}*f*_{yt}', 15, TEN, 'middle', 'bold')
    o += hdim(x0 - rr, x0 + rr, y0 + 20, '*d*_{s}', INK, 1)
    o += T(x0, y0 + 128, '(b) 半圓自由體（一個螺距 *s* 的高度）', 14, INK, 'middle', 'bold')
    o += T(x0, y0 + 152, '2*A*_{sp}*f*_{yt} = *f*_{L}·*d*_{s}·*s*', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '螺旋筋半圓自由體')


def fig5_2():
    W, H = 900, 400
    o = T(450, 26, 'RC-2010-1：剝掉保護層損失多少、核心變強補回多少（tf）', 16, INK, 'middle', 'bold')
    core = 0.85 * 350 * (RR['Ach'] - RR['Ast']) / 1000
    steel = 4200 * RR['Ast'] / 1000
    shell = RR['loss'] / 1000; gain = RR['gain'] / 1000
    rows = [('*P*_{y}（全斷面）', [(core, AC2, AC, f'核心 {core:.0f}'), (shell, STEEL3, MUT, f'保護層 {shell:.1f}'), (steel, TEN2, TEN, f'鋼筋 {steel:.0f}')]),
            ('*P*_{u}（剝落後）', [(core, AC2, AC, f'核心 {core:.0f}'), (gain, WARN2, WARN, f'圍束增益 {gain:.1f}'), (steel, TEN2, TEN, f'鋼筋 {steel:.0f}')])]
    k = 600 / 1800
    for i, (lab, segs) in enumerate(rows):
        y = 100 + i * 110
        o += T(180, y + 34, lab, 15, INK, 'end', 'bold')
        x = 200
        for v, fill, col, t in segs:
            o += R_(x, y, v * k, 56, fill, col)
            if v * k < 120:
                o += T(x + v * k / 2, y - 8, t, 14, col, 'middle', 'bold')
            else:
                o += T(x + v * k / 2, y + 34, t, 14, col, 'middle', 'bold')
            x += v * k
        tot = sum(v for v, *_ in segs)
        o += T(x + 10, y + 34, f'= {tot:.0f}', 15, INK, 'start', 'bold')
    o += box(200, 310, 600, 70, '規範的想法', [f'圍束增益 ≥ 保護層損失 → ρ_{{s}} 下限；本題 *s* = 8 cm：{gain:.1f} > {shell:.1f} ✔'], KEY2, KEY, 15, 15)
    return svg(W, H, o, '損失與增益')


def R_(x, y, w, h, fill, c):
    return R(x, y, w, h, fill, c, 1.4)


def fig5_3():
    W, H = 900, 400
    S = rc2017_1()
    o = T(450, 26, 'RC-2017-1：考卷用自訂雙折線取代 Whitney，*e* = 0 的軸力取 *P*(ε) 峰值', 16, INK, 'middle', 'bold')
    pl = Plot(90, 80, 330, 240, 0, 0.0032, 0, 230)
    o += pl.axes([0, 0.001, 0.002, 0.003], [0, 168, 210], 'ε', '*f*_{c}', xfmt=lambda v: f'{v:.3f}' if v else '0', size=14)
    o += pl.curve(lambda e: fc_2017(e), 0, 0.003, COMP, 3.2)
    o += T(pl.X(0.0016), pl.Y(105), '考卷圖 2', 14, COMP, 'start', 'bold')
    p2 = Plot(530, 80, 330, 240, 0.001, 0.0032, 400, 950)
    o += p2.axes([0.001, 0.002, 0.003], [400, 600, 800, 900], 'ε', '*P*（tf）', xfmt=lambda v: f'{v:.3f}', size=14)
    o += p2.curve(lambda e: S['P'](e) / 1000, 0.00125, 0.003, AC, 3.2)
    o += p2.dot(S['e_pk'], S['Ppk'] / 1000, KEY, 7)
    o += T(p2.X(S['e_pk']) + 10, p2.Y(S['Ppk'] / 1000) - 10, f"峰值 {S['Ppk']/1000:.1f}（ε = ε_{{y}}）", 14, KEY, 'start', 'bold')
    o += p2.dot(0.003, S['P003'] / 1000, MUT, 6)
    o += T(p2.X(0.003) - 6, p2.Y(S['P003'] / 1000) + 24, f"ε = 0.003：{S['P003']/1000:.1f}", 14, MUT, 'end')
    o += T(450, 372, '應力塊只是工具：考卷換了材料律，引擎（S1＋S3）照用，只把 S2 換掉。', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '加大柱雙折線')


def fig5_4():
    W, H = 900, 400
    Q = rc2017_2()
    o = T(450, 26, '剪力摩擦：介面一滑就張開，植筋被拉到 *f*_{y}，夾緊力 × μ ＝ 摩擦力', 16, INK, 'middle', 'bold')
    # 鋸齒介面
    y0 = 200
    xs = [100 + 30 * i for i in range(15)]
    top = []
    for i, x in enumerate(xs):
        top.append((x, y0 - (12 if i % 2 else 0)))
    o += P(top + [(xs[-1], 90), (100, 90)], INK, 1.6, fill=STEEL2, close=True)
    bot = [(x, y + 16) for x, y in top]
    o += P(bot + [(xs[-1], 310), (100, 310)], INK, 1.6, fill='#fff8e1', close=True)
    o += T(430, 120, '舊柱', 15, INK, 'start', 'bold')
    o += T(430, 290, '新混凝土', 15, INK, 'start', 'bold')
    for x in (160, 280, 400):
        o += L(x, 110, x, 290, TEN, 4)
        o += A(x + 14, 140, x + 14, 104, TEN, 2, 9)
        o += A(x + 14, 260, x + 14, 296, TEN, 2, 9)
    o += T(280, 80, '植筋 *A*_{vf}（綠）：被拉到 *f*_{y}', 14, TEN, 'middle', 'bold')
    o += A(250, y0 + 40, 380, y0 + 40, WARN, 3, 12)
    o += T(250, y0 + 64, '*V*（滑動）', 15, WARN, 'start', 'bold')
    o += T(250, y0 - 30, '↕ 鋸齒爬坡 → 張開', 14, KEY, 'start', 'bold')
    o += box(560, 150, 320, 210, 'RC-2017-2', ['*V*_{n} = μ *A*_{vf} *f*_{y}（μ = 1.0 粗糙面）', f"*V*_{{u}} = {Q['Vu']/1000:.1f} tf（翼側壓力合力）", f"*A*_{{vf}} = *V*_{{u}}/(φμ*f*_{{y}}) = {Q['Avf']:.2f} cm²", f"/3.871 → {Q['n']} 支（每個介面）", '另檢 *V*_{n} ≤ 0.2*f*′_{c}*A*_{c}'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '剪力摩擦')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
