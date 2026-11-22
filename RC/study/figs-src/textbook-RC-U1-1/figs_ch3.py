# -*- coding: utf-8 -*-
"""第 3 章：延性的量尺——c/dt、εt、φ、ρb、As,max。"""
from figs_common import *  # noqa
from calcs import demo_beam, phi_of, sweep_As, phi_peak, ES, beta1

D = demo_beam()


def fig3_1():
    W, H = 900, 460
    o = T(450, 24, '同一支梁（*d*_{t} = 53），只改鋼筋量：應變線繞著頂緣 0.003 旋轉', 16, INK, 'middle', 'bold')
    y0, sc = 70, 6.0
    xa = 330
    kx = 26000  # px per strain
    yd = y0 + 53 * sc
    o += L(xa, y0 - 10, xa, yd + 20, INK, 1.4)
    o += L(xa - 0.003 * kx - 20, y0, xa + 0.0125 * kx, y0, MUT, 1, '3 3')
    o += L(xa - 0.003 * kx - 20, yd, xa + 0.0125 * kx + 10, yd, TEN, 1.4, '6 4')
    o += T(xa + 0.0125 * kx + 14, yd + 5, '拉力筋 *d*_{t}', 14, TEN, 'start', 'bold')
    o += C(xa - 0.003 * kx, y0, 6, COMP, '#fff', 1.4)
    o += T(xa - 0.003 * kx, y0 - 12, '0.003（樞紐）', 15, COMP, 'middle', 'bold')
    ey = 4200 / ES
    cases = [(ey, '平衡 ε_{t} = ε_{y}', COMP), (0.005, '拉力控制界限 0.005', KEY), (D['et'], f"示範梁 {D['et']:.4f}", TEN)]
    for i, (et, lab, col) in enumerate(cases):
        c = 0.003 / (0.003 + et) * 53
        yc = y0 + c * sc
        xb = xa + et * kx
        o += L(xa - 0.003 * kx, y0, xb, yd, col, 2.6)
        o += C(xb, yd, 5, col, '#fff', 1.2)
        o += C(xa, yc, 5, col, '#fff', 1.2)
        o += L(xa, yc, xa - 115 - i * 0, yc, col, 1, '3 3')
        o += T(xa - 120, yc + 5, f'*c* = {c:.1f}（{c/53:.3f}*d*_{{t}}）', 14, col, 'end', 'bold')
        o += T(xb, yd + 24 + 20 * i, lab, 14, col, 'middle', 'bold')
    o += box(675, 80, 215, 200, '萬用鑰匙', ['相似三角形（S1、S2）：', '*c*/*d*_{t} = 0.003/(0.003+ε_{t})', '指定一個 ε_{t}，', '中性軸深度就定了；', '再用 *C* = *T*（S3）', '翻成鋼筋量'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'c/dt 樞紐')


def fig3_2():
    W, H = 900, 430
    pl = Plot(100, 80, 600, 260, 0.0, 0.009, 0.6, 0.95)
    o = pl.axes([0, 0.002, 0.004, 0.005, 0.006, 0.008], [0.65, 0.7, 0.8, 0.9], 'ε_{t}', 'φ',
                xfmt=lambda v: f'{v:.3f}' if v else '0', yfmt=lambda v: f'{v:.2f}', size=14)
    o += pl.area(lambda e: 0.95, lambda e: 0.6, 0.002, 0.005, COMP2, 0.6)
    o += T(pl.X(0.0035), pl.Y(0.94) + 4, '過渡區', 15, COMP, 'middle', 'bold')
    o += pl.curve(lambda e: phi_of(e, 4200), 0, 0.009, AC, 3.4, n=600)
    o += pl.curve(lambda e: phi_of(e, 6900), 0, 0.009, WARN, 2.4, dash='7 4', n=600)
    o += T(pl.X(0.0005), pl.Y(0.65) - 10, '壓力控制 0.65', 15, AC, 'start', 'bold')
    o += T(pl.X(0.0068), pl.Y(0.90) - 12, '拉力控制 0.90', 15, AC, 'middle', 'bold')
    o += pl.dot(0.004, phi_of(0.004), AC, 5)
    o += T(pl.X(0.004) + 10, pl.Y(phi_of(0.004)) + 18, f'0.004 → {phi_of(0.004):.3f}', 14, AC, 'start', 'bold')
    o += T(pl.X(0.0072), pl.Y(0.78), 'SD690：起點 0.00338、', 14, WARN, 'middle')
    o += T(pl.X(0.0072), pl.Y(0.78) + 20, '終點 0.00638（虛線）', 14, WARN, 'middle')
    # 上緣 c/dt 刻度
    for e in (0.002, 0.003, 0.005, 0.008):
        cd = 0.003 / (0.003 + e)
        o += L(pl.X(e), pl.y0 - 4, pl.X(e), pl.y0 + 4, MUT, 1.2)
        o += T(pl.X(e), pl.y0 - 10, f'{cd:.3f}', 14, MUT, 'middle')
    o += T(pl.X(0.009) + 10, pl.y0 - 10, '*c*/*d*_{t}', 14, MUT, 'start')
    o += box(720, 120, 170, 170, '為什麼這樣排？', ['鋼筋先拉長＝', '有預警 → 0.90', '混凝土先碎＝', '沒預警 → 0.65', '中間：直線內插'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'φ-εt')


def fig3_3():
    W, H = 900, 400
    pl = Plot(100, 50, 560, 280, 2800, 7000, 0.25, 0.55)
    o = pl.axes([2800, 3500, 4200, 4900, 5600, 6300, 7000], [0.3, 0.35, 0.4, 0.45, 0.5], '*f*_{y}', '*c*_{max}/*d*',
                yfmt=lambda v: f'{v:.2f}', size=14)
    o += pl.curve(lambda fy: 0.75 * 6120 / (6120 + fy), 2800, 7000, WARN, 2.6, dash='8 4')
    o += pl.curve(lambda fy: 3 / 7, 2800, 7000, MUT, 2.4, dash='4 4')
    o += pl.curve(lambda fy: 0.003 / (0.006 + fy / ES), 2800, 7000, COMP, 3.4)
    o += pl.dot(4200, 3 / 8, KEY, 6)
    o += L(pl.X(4200), pl.Y(3 / 8), pl.X(3700), pl.Y(0.335), KEY, 1.2) + T(pl.X(3650), pl.Y(0.335) + 18, 'SD420 取 ε_{ty} = 0.002 → 3/8', 14, KEY, 'middle', 'bold')
    o += T(pl.X(2850), pl.Y(0.75 * 6120 / (6120 + 2850)) - 10, '0.75ρ_{b}（ACI 318-99）', 14, WARN, 'start', 'bold')
    o += T(pl.X(6950), pl.Y(3 / 7) - 10, 'ε_{t} ≥ 0.004 → 3/7（401-100）', 14, MUT, 'end', 'bold')
    o += T(pl.X(6950), pl.Y(0.003 / (0.006 + 6950 / ES)) + 24, '現行：拉力控制 ε_{t} ≥ ε_{ty} + 0.003', 14, COMP, 'end', 'bold')
    o += box(690, 70, 195, 190, '三代都是同一件事', ['限制 *c*/*d*：', '中性軸不准太深', '＝鋼筋不准太多', '＝破壞前鋼筋', '一定要拉得夠長', '現行最嚴'], AC2, AC, 15, 14)
    return svg(W, H, o, '三代上限')


def fig3_4():
    W, H = 900, 470
    S = sweep_As(n=600)
    pk = phi_peak()
    pl = Plot(100, 60, 600, 320, 0, 70, 0, 110)
    o = pl.axes([0, 10, 20, 30, 40, 50, 60, 70], [0, 20, 40, 60, 80, 100], '*A*_{s}', '（tf·m）', size=14)
    o += T(pl.X(70) + 18, pl.Y(0) + 26, '(cm²)', 14, MUT, 'start')
    o += pl.area(lambda x: 110, lambda x: 0, D['Asmax'], D['Asb'], COMP2, 0.45)
    o += pl.area(lambda x: 110, lambda x: 0, D['Asb'], 70, '#ffcdd2', 0.55)
    pts_mn = [pl.pt(r[0], r[3] / 1e5) for r in S if r[0] <= 70]
    pts_pm = [pl.pt(r[0], r[4] / 1e5) for r in S if r[0] <= 70]
    o += P(pts_mn, MUT, 2.4, dash='7 4')
    o += P(pts_pm, AC, 3.4)
    o += T(pl.X(46), pl.Y(96), '*M*_{n}', 16, MUT, 'middle', 'bold')
    o += T(pl.X(52), pl.Y(58), 'φ*M*_{n}', 16, AC, 'middle', 'bold')
    for As, lab, col in ((D['Asmin'], '*A*_{s,min}', TEN), (D['As'], '示範梁', KEY), (D['Asmax'], '*A*_{s,max}', COMP), (D['Asb'], '*A*_{sb}', COMP)):
        o += pl.vline(As, 0, 104, col, 1.4)
        o += T(pl.X(As), pl.Y(104) - 6, lab, 14, col, 'middle', 'bold')
    o += T(pl.X((D['Asmax'] + D['Asb']) / 2), pl.Y(18), '過渡區', 15, COMP, 'middle', 'bold')
    o += T(pl.X((D['Asmax'] + D['Asb']) / 2), pl.Y(18) + 20, '（梁禁用）', 14, COMP, 'middle')
    o += T(pl.X((D['Asb'] + 70) / 2), pl.Y(18), '過筋', 15, COMP, 'middle', 'bold')
    o += T(pl.X((D['Asb'] + 70) / 2), pl.Y(18) + 20, '鋼筋不降伏', 14, COMP, 'middle')
    o += pl.dot(D['Asmax'], D['phiMn_lim'] / 1e5 if 'phiMn_lim' in D else 0.9 * D['Mn_max'] / 1e5, COMP, 6)
    o += pl.dot(pk['As_ey'], pk['phiMn_ey'] / 1e5, COMP, 5)
    o += box(715, 80, 175, 250, '多放 58% 鋼筋', [f"*A*_{{s,max}} {D['Asmax']:.1f} →", f"*A*_{{sb}} {D['Asb']:.1f} cm²：", f"*M*_{{n}} +{(pk['Mn_ey']/D['Mn_max']-1)*100:.0f}%", f"φ*M*_{{n}} 只 +{(pk['phiMn_ey']/(0.9*D['Mn_max'])-1)*100:.1f}%", 'φ 從 0.90 掉到', '0.65 左右，', '多放的鋼筋', '幾乎白放'], WARN2, WARN, 15, 14)
    return svg(W, H, o, 'φMn-As')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
