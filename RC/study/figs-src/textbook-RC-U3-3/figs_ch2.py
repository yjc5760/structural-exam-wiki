# -*- coding: utf-8 -*-
"""第 2 章：超強、梁自由體、交叉裂縫與 Vc=0。"""
from figs_common import *  # noqa
from calcs import frame2012, p2025_2, p2016_2
import math

F12 = frame2012()
P25 = p2025_2()
P16 = p2016_2()


def fig2_1():
    W, H = 900, 380
    o = T(450, 24, '保險絲比標示的強：算別人要撐多少時，用 1.25*f*_{y}', 16, INK, 'middle', 'bold')
    pl = Plot(80, 60, 380, 260, 0, 0.06, 0, 1.45)
    o += pl.axes([], [], 'ε', '*f*_{s}/*f*_{y}', grid=False, size=14)
    ey = 0.00206
    pts = [pl.pt(0, 0), pl.pt(ey * 1.12, 1.12), pl.pt(0.012, 1.12)]
    for i in range(1, 41):
        e = 0.012 + (0.055 - 0.012) * i / 40
        pts.append(pl.pt(e, 1.12 + 0.28 * math.sin(math.pi / 2 * (e - 0.012) / 0.043)))
    o += P(pts, INK, 2.6)
    o += pl.hline(1.0, 0, 0.06, MUT, 1.4, '6 4')
    o += T(pl.X(0.059), pl.Y(1.0) + 20, '標稱 *f*_{y}', 14, MUT, 'end', 'bold')
    o += R(pl.X(0.0), pl.Y(1.29), pl.X(0.06) - pl.X(0), pl.Y(1.21) - pl.Y(1.29), KEY2, None, 0, op=0.9)
    o += pl.hline(1.25, 0, 0.06, KEY, 2, None)
    o += T(pl.X(0.002), pl.Y(1.25) - 10, '1.25*f*_{y}', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.015), pl.Y(0.8), '實際降伏常比標稱高', 14, INK, 'start')
    o += T(pl.X(0.035), pl.Y(1.38) - 6, '應變硬化', 14, INK, 'start')
    # 右：比較長條
    bx, by = 530, 90
    k = 3.6
    mn = F12['Mn_neg']
    items = [('φ*M*_{n}（一般設計）', 0.9 * mn, MUT), ('*M*_{n}', mn, AC), ('*M*_{pr}（1.25*f*_{y}、φ = 1）', F12['Mpr_neg'], KEY)]
    o += T(bx, by - 20, '示範梁頂筋受拉（tf·m）', 15, INK, 'start', 'bold')
    for i, (lab, v, col) in enumerate(items):
        y = by + i * 70
        o += T(bx, y + 4, lab, 14, col, 'start', 'bold')
        o += R(bx, y + 14, v * k, 26, col, None, 0, 0, op=0.8)
        o += T(bx + v * k + 6, y + 33, f'{v:.2f}', 15, col, 'start', 'bold')
    o += T(bx, by + 230, f"*M*_{{pr}}/φ*M*_{{n}} = {F12['Mpr_neg']/(0.9*mn):.2f}", 16, KEY, 'start', 'bold')
    return svg(W, H, o, '超強')


def _arc(cx, cy, r, col):
    pts = []
    for i in range(25):
        a = math.radians(200 + 140 * i / 24)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return curve_arrow(pts, col, 2.4, 11)


def fig2_2():
    W, H = 900, 400
    o = T(450, 24, '梁兩端形成塑鉸：剪力由 *M*_{pr} 和重力決定', 16, INK, 'middle', 'bold')
    x0, x1, y0, hb = 150, 750, 130, 60
    o += R(x0, y0, x1 - x0, hb, STEEL2, INK, 1.6)
    for i in range(13):
        xx = x0 + 20 + i * 46.6
        o += A(xx, y0 - 40, xx, y0 - 4, MUT, 1.4, 8)
    o += T(450, y0 - 50, f"*w*_{{u}} = {P25['wu']:.1f} tf/m（1.2*D* + 1.0*L*）", 15, MUT, 'middle', 'bold')
    o += _arc(x0, y0 + hb / 2, 46, KEY) + _arc(x1, y0 + hb / 2, 46, KEY)
    o += T(x0 - 16, y0 + hb + 30, f"*M*_{{pr}}^{{+}} = {P25['Mpr_pos']:.2f}", 15, KEY, 'end', 'bold')
    o += T(x1 + 16, y0 + hb + 30, f"*M*_{{pr}}^{{−}} = {P25['Mpr_neg']:.2f}", 15, KEY, 'start', 'bold')
    o += T(x0 - 16, y0 + hb + 52, '底筋受拉', 14, KEY, 'end') + T(x1 + 16, y0 + hb + 52, '頂筋受拉', 14, KEY, 'start')
    o += A(x0 + 30, y0 + hb + 4, x0 + 30, y0 + hb + 100, AC, 2.4, 10)
    o += T(x0 + 40, y0 + hb + 80, f"{P25['Ve_other']:.2f} tf", 15, AC, 'start', 'bold')
    o += A(x1 - 30, y0 + hb + 100, x1 - 30, y0 + hb + 4, AC, 2.4, 10)
    o += T(x1 - 40, y0 + hb + 80, f"*V*_{{e}} = {P25['Ve']:.2f} tf", 15, AC, 'end', 'bold')
    o += hdim(x0, x1, y0 + hb + 128, f"*l*_{{n}} = {P25['ln']/100:.0f} m", INK, -1, 15)
    o += R(230, 330, 440, 60, '#fff', AC, 1.6, 9)
    o += T(450, 355, f"地震 Σ*M*_{{pr}}/*l*_{{n}} = {P25['Vseis']:.2f}（兩端相同）", 15, KEY, 'middle', 'bold')
    o += T(450, 380, f"重力 *w*_{{u}}*l*_{{n}}/2 = {P25['Vgrav']:.2f}（一端加、一端減）", 15, MUT, 'middle', 'bold')
    return svg(W, H, o, '梁自由體')


def fig2_3():
    W, H = 900, 330
    o = T(450, 24, '塑鉸區的交叉裂縫 → 混凝土剪力靠不住', 16, INK, 'middle', 'bold')
    x0, y0, bw, bh = 40, 80, 300, 120
    o += R(x0 - 30, y0 - 30, 30, bh + 60, STEEL3, INK, 1.4)
    o += R(x0, y0, bw, bh, STEEL2, INK, 1.6)
    for i in range(5):
        xa = x0 + 30 + i * 45
        o += L(xa, y0 + bh - 8, xa + 70, y0 + 8, COMP, 2)
        o += L(xa, y0 + 8, xa + 70, y0 + bh - 8, AC, 2)
    o += T(x0 + bw / 2, y0 + bh + 30, '紅：往右推裂的；藍：往左推裂的', 14, INK, 'middle')
    o += T(x0 + bw / 2, y0 + bh + 54, '骨材咬合被磨光', 14, COMP, 'middle', 'bold')
    # 右：比例
    bx, w = 470, 300
    rows = [('RC-2025-2', P25['ratio'], COMP, '→ *V*_{c} = 0'), ('RC-2016-2', P16['ratio'], TEN, '→ *V*_{c} 計入')]
    for i, (lab, r, col, res) in enumerate(rows):
        y = 90 + i * 90
        o += T(bx - 12, y + 26, lab, 15, INK, 'end', 'bold')
        o += R(bx, y, w, 40, STEEL2, INK, 1.2)
        o += R(bx, y, w * r, 40, col, None, 0, op=0.85)
        o += T(bx + w * r - 8, y + 26, f'{r*100:.1f}%', 15, '#fff', 'end', 'bold')
        o += T(bx + w + 12, y + 26, res, 15, col, 'start', 'bold')
    o += L(bx + w * 0.5, 74, bx + w * 0.5, 290, KEY, 2, '6 4')
    o += T(bx + w * 0.5, 308, '50%', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'Vc=0')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
