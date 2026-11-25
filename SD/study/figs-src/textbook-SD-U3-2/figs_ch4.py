# -*- coding: utf-8 -*-
"""第 4 章：隔震設計程序、迭代收斂、D'_D。"""
from sdfig import *  # noqa
from calcs import LRB, LRB_HIST
import math


def fig4_1():
    rows = [
        ('1', '假設 *D*（第一次可用 *D* = 0.2 m 或 *S*_{D1} 估）', AC),
        ('2', '*K*_{eD} = *n*[*Q*/*D* + *k*_{d}]（全部支承）', KEY),
        ('3', '*T*_{eD} = 2π√(*W*/(*K*_{eD}*g*))', KEY),
        ('4', '*A*_{TD} = 4*nQ*(*D* − *D*_{y})、ξ_{eD} = *A*_{TD}/(2π*K*_{eD}*D*²)', TEN),
        ('5', '查 *B*（依 *T*_{eD} 取 *B*_{S} 或 *B*_{1}）', TEN),
        ('6', '*D*_{D} = *gS*_{aD}*T*_{eD}²/(4π²*B*)', WARN),
        ('7', '|*D*_{D} − *D*| 夠小？否 → *D* = *D*_{D} 回到 2', COMP),
    ]
    return flow(rows, W=900, bh=44, gap=12, title='隔震設計位移的迭代（2014-2 要寫出的步驟）')


def fig4_2():
    W, H = 900, 360
    hs = LRB_HIST
    n = len(hs)
    pl = Plot(100, 40, 410, 260, 0.5, n + 0.5, 0.198, 0.210)
    o = pl.axes(list(range(1, n + 1)), [0.200, 0.205, 0.210], '迭代次數', '*D* (m)', yfmt=lambda v: f'{v:.3f}')
    o += P([pl.pt(i + 1, h['D']) for i, h in enumerate(hs)], AC, 2.4, dash='6 4')
    o += P([pl.pt(i + 1, h['Dn']) for i, h in enumerate(hs)], WARN, 3)
    for i, h in enumerate(hs):
        o += pl.dot(i + 1, h['D'], AC, 5) + pl.dot(i + 1, h['Dn'], WARN, 5)
    o += T(pl.X(1.5), pl.Y(0.2005), '假設 *D*', 14.5, AC, 'start', 'bold')
    o += T(pl.X(1.5), pl.Y(0.1992), '算得 *D*_{D}', 14.5, WARN, 'start', 'bold')
    f = hs[-1]
    o += box(560, 40, 330, 280, f'收斂（{n} 次）', [f'*W* = {LRB["W"]:.0f} kN、*F*_{{y}} = {LRB["Fy"]:.0f} kN', f'*k*_{{o}} = {LRB["ko"]:.0f} kN/m、α = {LRB["alpha"]}', f'*S*_{{D1}} = {LRB["SD1"]}（長週期段 *S*_{{aD}} = *S*_{{D1}}/*T*）', f'*D*_{{D}} = {f["D"]:.3f} m', f'*K*_{{eD}} = {f["K"]:.0f} kN/m', f'*T*_{{eD}} = {f["T"]:.2f} s', f'ξ_{{eD}} = {f["xi"]*100:.1f}%  → *B* = {f["B"]:.2f}'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '迭代收斂')


def fig4_3():
    W, H = 900, 340
    pl = Plot(90, 40, 410, 240, 0, 1.0, 0, 1.6)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0, 0.5, 1.0, 1.5], '*T*/*T*_{eD}', '÷ *D*_{D}', yfmt=lambda v: f'{v:g}')
    o += pl.curve(lambda r: math.sqrt(1 + r * r), 0, 1, AC, 3)
    o += pl.curve(lambda r: 1 / math.sqrt(1 + r * r), 0, 1, WARN, 3)
    o += pl.curve(lambda r: r * r / math.sqrt(1 + r * r), 0, 1, TEN, 3)
    o += T(pl.X(0.55), pl.Y(1.36), '總位移 √(1+*r*²)', 14.5, AC, 'start', 'bold')
    o += T(pl.X(0.62), pl.Y(0.92), '隔震層 *D*′_{D}', 14.5, WARN, 'start', 'bold')
    o += T(pl.X(0.62), pl.Y(0.18), '上部變形', 14.5, TEN, 'start', 'bold')
    o += pl.dot(0.2, 1 / math.sqrt(1.04), WARN, 5) + T(pl.X(0.2), pl.Y(0.88), f'{1/math.sqrt(1.04):.3f}', 14, WARN, 'middle', 'bold')
    o += box(570, 40, 320, 250, '為什麼 *D*′_{D} < *D*_{D}', ['串聯：*T*_{sys} = *T*_{eD}√(1+*r*²)', '長週期段 *S*_{d} ∝ *T*', '⇒ 總位移 = *D*_{D}√(1+*r*²)', '隔震層分到 *k*/(*k*+*k*_{b})', '= 1/(1+*r*²)', '⇒ *D*′_{D} = *D*_{D}/√(1+*r*²)', '規範 9.3.4 下限計算可用'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, "D'_D")


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
