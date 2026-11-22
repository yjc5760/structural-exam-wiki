# -*- coding: utf-8 -*-
"""第 5 章：梁柱接頭自由體、有效寬度、使用率。"""
from figs_common import *  # noqa
from calcs import frame2012, p2005_3, p2018_2, p2003_3

F12 = frame2012()
P05, P18, P03 = p2005_3(), p2018_2(), p2003_3()


def fig5_1():
    W, H = 900, 440
    o = T(450, 24, '外接頭：取接頭中央以上的半塊', 16, INK, 'middle', 'bold')
    cx, cy = 300, 230
    # 柱
    o += R(cx - 60, 50, 120, 360, STEEL2, INK, 1.4)
    # 梁（右側）
    o += R(cx + 60, cy - 60, 250, 70, STEEL2, INK, 1.4)
    # 接頭區
    o += R(cx - 60, cy - 60, 120, 120, STEEL3, INK, 1.6)
    # 切面
    o += L(cx - 90, cy, cx + 90, cy, COMP, 2.4, '7 5')
    o += T(cx - 96, cy + 5, '切面', 15, COMP, 'end', 'bold')
    # 頂筋
    o += L(cx - 45, cy - 50, cx + 300, cy - 50, TEN, 3)
    o += L(cx - 45, cy - 50, cx - 45, cy + 20, TEN, 3)
    o += A(cx + 200, cy - 50, cx + 300, cy - 50, TEN, 3, 12)
    o += T(cx + 250, cy - 66, f"*T*_{{1}} = 1.25*f*_{{y}}*A*_{{s}} = {F12['T1']:.2f}", 15, TEN, 'middle', 'bold')
    # Vcol
    o += A(cx + 30, 80, cx - 40, 80, AC, 2.6, 11)
    o += T(cx + 70, 86, f"*V*_{{col}} = {F12['Vcol']:.2f}", 15, AC, 'start', 'bold')
    # Vjh 在切面
    o += A(cx + 50, cy + 16, cx - 50, cy + 16, COMP, 2.6, 11)
    o += T(cx, cy + 40, '*V*_{jh}', 15, COMP, 'middle', 'bold')
    # 右：平衡式
    o += R(560, 250, 310, 160, KEY2, KEY, 1.6, 10)
    o += T(580, 280, '上半塊水平平衡：', 15, INK, 'start', 'bold')
    o += T(580, 312, '*V*_{jh} = *T*_{1} + *C*_{2} − *V*_{col}', 15, KEY, 'start', 'bold')
    o += T(580, 342, f"= {F12['T1']:.2f} + 0 − {F12['Vcol']:.2f}", 15, INK, 'start')
    o += T(580, 372, f"= {F12['Vjh']:.2f} tf", 16, COMP, 'start', 'bold')
    o += T(580, 398, '（外接頭 *C*_{2} = 0）', 14, MUT, 'start')
    return svg(W, H, o, '接頭自由體')


def fig5_2():
    W, H = 900, 450
    o = T(450, 24, '有效寬 *b*_{j} 與四道考古題的使用率', 16, INK, 'middle', 'bold')
    # 平面圖
    x0, y0, s = 70, 110, 3.6
    bc, bw, xoff = 60, 30, 10
    o += R(x0, y0, bc * s, bc * s, STEEL2, INK, 1.6)
    o += T(x0 + bc * s / 2, y0 + bc * s / 2 + 5, '柱 *b*_{c}', 15, INK, 'middle', 'bold')
    bx = x0 + xoff * s
    o += R(bx, y0 + bc * s, bw * s, 60, STEEL3, INK, 1.4)
    o += T(bx + bw * s / 2, y0 + bc * s + 36, '梁 *b*_{w}', 15, INK, 'middle', 'bold')
    o += R(bx - 8, y0, bw * s + 16, bc * s, KEY, KEY, 1.4, op=0.18)
    o += hdim(x0, bx, y0 - 14, '*x*', MUT, -1, 15)
    o += vdim(x0 + bc * s + 14, y0, y0 + bc * s, '*h*', MUT, 1, 15)
    o += T(x0 + bc * s / 2 + 30, y0 + bc * s + 96, '*b*_{j} = min(*b*_{w} + *h*, *b*_{w} + 2*x*, *b*_{c})', 15, KEY, 'middle', 'bold')
    o += A(x0 + bc * s / 2, y0 - 46, x0 + bc * s / 2, y0 - 22, MUT, 1.6, 8)
    o += T(x0 + bc * s / 2, y0 - 52, '剪力方向 ↓', 14, MUT, 'middle')
    # 使用率條
    rows = [('RC-2012-4', F12['util'], TEN), ('RC-2005-3', P05['util'], TEN), ('RC-2018-2', P18['ratio'], COMP),
            ('RC-2003-3 偏心', P03['ratio'], COMP), ('RC-2003-3 置中', P03['Vu'] / P03['phiVn_center'], TEN)]
    gx, gy, k = 520, 80, 140
    for i, (lab, v, col) in enumerate(rows):
        y = gy + i * 56
        o += T(gx - 10, y + 22, lab, 14, INK, 'end', 'bold')
        o += R(gx, y + 4, v * k, 26, col, None, 0, op=0.8)
        o += T(gx + max(v, 1.0) * k + 8, y + 23, f'{v:.2f}', 15, col, 'start', 'bold')
    o += L(gx + k, gy - 6, gx + k, gy + 5 * 56, INK, 1.6, '5 4')
    o += T(gx + k, gy + 5 * 56 + 22, '1.0', 14, INK, 'middle', 'bold')
    return svg(W, H, o, '有效寬')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
