# -*- coding: utf-8 -*-
"""第 6 章：握裹與伸展長度、搭接位置。"""
from figs_common import *  # noqa
from calcs import p2003_2

D03 = p2003_2()


def fig6_1():
    W, H = 900, 380
    o = T(450, 24, '拉力 = 握裹應力 × 周長 × 長度', 16, INK, 'middle', 'bold')
    x0, y0, w, hh = 50, 120, 330, 120
    o += R(x0, y0, w, hh, STEEL2, INK, 1.4)
    o += L(x0 + 40, y0 + hh / 2, x0 + w + 90, y0 + hh / 2, COMP, 7)
    for i in range(9):
        x = x0 + 60 + i * 30
        o += A(x + 14, y0 + hh / 2 - 12, x - 6, y0 + hh / 2 - 12, AC, 1.6, 7)
        o += A(x + 14, y0 + hh / 2 + 12, x - 6, y0 + hh / 2 + 12, AC, 1.6, 7)
    o += A(x0 + w + 60, y0 + hh / 2, x0 + w + 120, y0 + hh / 2, COMP, 3, 12)
    o += T(x0 + w + 112, y0 + hh / 2 - 16, '*A*_{b}*f*_{y}', 15, COMP, 'middle', 'bold')
    o += T(x0 + 180, y0 - 12, '握裹應力 *u*（沿周長 π*d*_{b}）', 15, AC, 'middle', 'bold')
    o += hdim(x0 + 40, x0 + w, y0 + hh + 18, '*l*_{d}', INK, 1, 15)
    o += T(x0 + 200, y0 + hh + 78, '(π*d*_{b}²/4)*f*_{y} = *u*·π*d*_{b}·*l*_{d}  →  *l*_{d} = *f*_{y}*d*_{b}/(4*u*)', 15, KEY, 'middle', 'bold')
    # 右：長度比較
    gx, gy, k = 560, 90, 1.25
    o += T(gx, gy - 20, 'D29（RC-2003-2）', 15, INK, 'start', 'bold')
    rows = [('圍束指標 = 1', D03['ld_noconf'], MUT), ('上限 2.5：*l*_{d}', D03['ld'], TEN), ('乙級搭接 1.3*l*_{d}', D03['lst'], AC)]
    for i, (lab, v, col) in enumerate(rows):
        y = gy + i * 70
        o += T(gx, y + 4, lab, 14, col, 'start', 'bold')
        o += R(gx, y + 12, v * k, 26, col, None, 0, op=0.8)
        o += T(gx + v * k + 6, y + 31, f'{v:.1f} cm', 15, col, 'start', 'bold')
    o += T(gx, gy + 230, '圍束好 → 劈裂晚 → *u* 高 → *l*_{d} 短', 15, COMP, 'start', 'bold')
    return svg(W, H, o, '握裹')


def fig6_2():
    W, H = 900, 470
    o = T(450, 24, '搭接只准放在保險絲以外', 16, INK, 'middle', 'bold')
    # 梁
    x0, y0, s, hb = 40, 90, 0.62, 60
    ln = 900
    cw = 60
    o += R(x0, y0 - 30, cw * s, hb * s + 60, STEEL3, INK, 1.2)
    o += R(x0 + (cw + ln) * s, y0 - 30, cw * s, hb * s + 60, STEEL3, INK, 1.2)
    bx = x0 + cw * s
    o += R(bx, y0, ln * s, hb * s, STEEL2, INK, 1.4)
    zones = [(0, 2 * hb, COMP), (ln - 2 * hb, ln, COMP), (ln / 2 - 2 * hb, ln / 2 + 2 * hb, COMP)]
    for a, b, col in zones:
        o += R(bx + a * s, y0, (b - a) * s, hb * s, col, None, 0, op=0.35)
    for a, b in ((2 * hb, ln / 2 - 2 * hb), (ln / 2 + 2 * hb, ln - 2 * hb)):
        o += R(bx + a * s, y0, (b - a) * s, hb * s, TEN, None, 0, op=0.35)
    o += R(x0, y0, cw * s, hb * s, COMP, None, 0, op=0.35)
    o += R(x0 + (cw + ln) * s, y0, cw * s, hb * s, COMP, None, 0, op=0.35)
    o += T(bx + hb * s, y0 + hb * s + 22, '2*h*', 15, COMP, 'middle', 'bold')
    o += T(bx + ln / 2 * s, y0 + hb * s + 22, '預期降伏斷面 ±2*h*', 15, COMP, 'middle', 'bold')
    o += T(bx + (ln - hb) * s, y0 + hb * s + 22, '2*h*', 15, COMP, 'middle', 'bold')
    o += T(x0 + cw * s / 2, y0 - 40, '接頭內', 14, COMP, 'middle', 'bold')
    o += T(bx + (2 * hb + ln / 2 - 2 * hb) / 2 * s, y0 - 10, '可搭接', 15, TEN, 'middle', 'bold')
    o += T(bx + (ln / 2 + ln - 2 * hb) / 2 * s, y0 - 10, '可搭接', 15, TEN, 'middle', 'bold')
    o += T(bx + ln / 2 * s, y0 + hb * s + 50, '耐震梁：三個禁區；搭接段閉合箍 *s* ≤ min(*d*/4, 10 cm)', 15, INK, 'middle', 'bold')
    o += T(bx + ln / 2 * s, y0 + hb * s + 76, '（跨中降伏斷面只在分析預期會降伏時才是禁區）', 14, MUT, 'middle')
    # 柱
    cx, ytop, sc = 760, 250, 0.62
    lnc = D03['ln']
    o += R(cx - 60, ytop - 30, 120, 30, STEEL3, INK, 1.2)
    o += R(cx - 60, ytop + lnc * sc, 120, 30, STEEL3, INK, 1.2)
    o += R(cx - 22, ytop, 44, lnc * sc, STEEL2, INK, 1.4)
    z0, z1 = D03['zone']
    o += R(cx - 22, ytop, 44, z0 * sc, COMP, None, 0, op=0.35)
    o += R(cx - 22, ytop + z1 * sc, 44, (lnc - z1) * sc, COMP, None, 0, op=0.35)
    o += R(cx - 22, ytop + z0 * sc, 44, (z1 - z0) * sc, TEN, None, 0, op=0.35)
    o += T(cx + 34, ytop + z0 * sc + 5, f'{z0:.0f}', 14, INK, 'start', 'bold')
    o += T(cx + 34, ytop + z1 * sc + 5, f'{z1:.0f}', 14, INK, 'start', 'bold')
    o += T(cx + 34, ytop + (z0 + z1) / 2 * sc + 5, '中央 1/2', 15, TEN, 'start', 'bold')
    o += T(cx - 34, ytop + 30, '柱端', 15, COMP, 'end', 'bold')
    o += T(cx - 34, ytop + lnc * sc - 20, '柱端', 15, COMP, 'end', 'bold')
    o += T(cx - 90, ytop + lnc * sc / 2, '耐震柱', 15, INK, 'end', 'bold')
    o += T(cx - 90, ytop + lnc * sc / 2 + 24, f'淨高 {lnc:.0f} cm', 14, MUT, 'end')
    o += T(cx - 90, ytop + lnc * sc / 2 + 48, '拉力搭接 1.3*l*_{d}', 14, MUT, 'end')
    return svg(W, H, o, '搭接位置')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
