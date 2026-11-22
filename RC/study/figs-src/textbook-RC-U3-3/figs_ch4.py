# -*- coding: utf-8 -*-
"""第 4 章：接頭彎矩平衡、柱設計剪力。"""
from figs_common import *  # noqa
from calcs import frame2012
import math

F12 = frame2012()


def _arc(cx, cy, r, a0, a1, col):
    pts = []
    for i in range(25):
        a = math.radians(a0 + (a1 - a0) * i / 24)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return curve_arrow(pts, col, 2.4, 10)


def fig4_1():
    W, H = 900, 450
    o = T(450, 24, '接頭自由體：柱端彎矩和 = 梁端彎矩和', 16, INK, 'middle', 'bold')
    cx, cy = 220, 210
    o += R(cx - 40, cy - 40, 80, 80, STEEL3, INK, 1.6)
    o += R(cx - 30, cy - 170, 60, 130, STEEL2, INK, 1.4)
    o += R(cx - 30, cy + 40, 60, 130, STEEL2, INK, 1.4)
    o += R(cx - 170, cy - 30, 130, 60, STEEL2, INK, 1.4)
    o += R(cx + 40, cy - 30, 130, 60, STEEL2, INK, 1.4)
    o += _arc(cx - 105, cy, 38, 120, 240, KEY) + _arc(cx + 105, cy, 38, -60, 60, KEY)
    o += T(cx - 150, cy - 50, '*M*_{b,l}', 15, KEY, 'middle', 'bold')
    o += T(cx + 150, cy - 50, '*M*_{b,r}', 15, KEY, 'middle', 'bold')
    o += _arc(cx, cy - 105, 38, 210, 330, AC) + _arc(cx, cy + 105, 38, 30, 150, AC)
    o += T(cx + 50, cy - 140, '*M*_{c,上}', 15, AC, 'start', 'bold')
    o += T(cx + 50, cy + 150, '*M*_{c,下}', 15, AC, 'start', 'bold')
    o += T(cx, cy + 222, 'Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}', 16, INK, 'middle', 'bold')
    # 右：1.2 vs Mpr/Mn
    bx, by, k = 520, 110, 240
    o += T(bx, by - 30, '1.2 買到什麼？（以 *M*_{nb} = 1 計）', 15, INK, 'start', 'bold')
    rows = [('梁標稱 *M*_{nb}', 1.0, AC), ('柱至少 1.2*M*_{nb}', 1.2, TEN), (f"梁實際 *M*_{{pr}}（示範梁）", F12['Mpr_neg'] / F12['Mn_neg'], KEY)]
    for i, (lab, v, col) in enumerate(rows):
        y = by + i * 70
        o += T(bx, y, lab, 14, col, 'start', 'bold')
        o += R(bx, y + 10, v * k, 26, col, None, 0, op=0.8)
        o += T(bx + v * k + 6, y + 29, f'{v:.2f}', 15, col, 'start', 'bold')
    o += T(bx, by + 230, '柱的兩成餘裕，幾乎被梁的超強吃掉', 15, COMP, 'start', 'bold')
    o += T(bx, by + 254, '→ 柱端仍要圍束（第 3 章）', 15, COMP, 'start', 'bold')
    return svg(W, H, o, '強柱弱梁')


def fig4_2():
    W, H = 900, 430
    o = T(450, 24, '柱剪力：同一接頭的梁 *M*_{pr}，上下柱各分一半', 16, INK, 'middle', 'bold')
    x0, ytop, ybot = 200, 90, 360
    o += R(x0 - 25, ytop, 50, ybot - ytop, STEEL2, INK, 1.6)
    o += R(x0 - 45, ytop - 40, 90, 40, STEEL3, INK, 1.2) + R(x0 - 45, ybot, 90, 40, STEEL3, INK, 1.2)
    o += T(x0 + 55, ytop - 14, '接頭', 14, MUT, 'start') + T(x0 + 55, ybot + 26, '接頭', 14, MUT, 'start')
    m = F12['Mcol_each']
    o += _arc(x0, ytop + 16, 36, 200, 340, AC) + _arc(x0, ybot - 16, 36, 20, 160, AC)
    o += T(x0 - 50, ytop + 40, f'{m:.2f}', 15, AC, 'end', 'bold')
    o += T(x0 - 50, ybot - 50, f'{m:.2f}', 15, AC, 'end', 'bold')
    o += A(x0 + 60, ytop + 30, x0 + 30, ytop + 30, COMP, 2.4, 10)
    o += A(x0 - 60, ybot - 30, x0 - 30, ybot - 30, COMP, 2.4, 10)
    o += T(x0 + 64, ytop + 36, '*V*_{col}', 15, COMP, 'start', 'bold')
    o += vdim(x0 + 120, ytop, ybot, f"*l*_{{n}} = {F12['ln_col']/100:.1f} m", INK, 1, 15)
    o += L(x0 - 40, (ytop + ybot) / 2, x0 + 40, (ytop + ybot) / 2, MUT, 1.2, '4 3')
    o += T(x0 - 44, (ytop + ybot) / 2 + 5, '反曲點', 14, MUT, 'end')
    # 右：計算框
    o += R(470, 90, 400, 270, KEY2, KEY, 1.6, 10)
    lines = [('單跨構架：每個接頭只有一根梁', INK), (f"Σ*M*_{{pr}} = *M*_{{pr}}^{{−}} = {F12['Mpr_neg']:.2f} tf·m", KEY),
             (f"上下柱各分一半：{m:.2f}", AC), (f"*V*_{{col}} = ({m:.2f} + {m:.2f})/{F12['ln_col']/100:.1f}", COMP),
             (f"= {F12['Vcol']:.2f} tf", COMP), (f"舊解 2*M*_{{pr}}/*l*_{{n}} = {F12['Vcol_wrong']:.2f}（高估一倍）", MUT),
             (f"檢查：*V*_{{col}}·*l*_{{n}} = {F12['Vcol']*F12['ln_col']/100:.1f} = 一個接頭", TEN)]
    for i, (t, col) in enumerate(lines):
        o += T(490, 124 + i * 34, t, 15, col, 'start', 'bold' if i in (4,) else None)
    return svg(W, H, o, '柱剪力')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
