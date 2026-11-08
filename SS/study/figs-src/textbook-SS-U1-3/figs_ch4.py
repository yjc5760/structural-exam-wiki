# -*- coding: utf-8 -*-
"""第 4 章：拆兩次（Mnt／Mlt）、Mu 組合、靠桿、SS-2013-4。數字取自 calcs.py。"""
from plot import *  # noqa
from calcs import ex2014, ex2014_wrong, ex_leaning, ex2013, LOAD
import math


def _frame(ox, sway, roller, loads, title, c, D=0):
    """單跨門型構架。sway：柱頂側移量（px）；roller：是否畫假想支撐；loads：('P','H','R')。"""
    o = T(ox + 120, 34, title, 15.5, c, 'middle', 'bold')
    xl, xr, yt, yb = ox + 55, ox + 185, 120, 300
    if D:
        o += L(xl, yt, xl, yb, MUT, 1, '5 5') + L(xr, yt, xr, yb, MUT, 1, '5 5')
    o += L(xl + D, yt, xl, yb, AC, 5) + L(xr + D, yt, xr, yb, AC, 5) + L(xl + D, yt, xr + D, yt, STEEL, 8)
    o += fixed_wall(xl, yb, 46) + fixed_wall(xr, yb, 46)
    if 'P' in loads:
        o += A(xl + D, yt - 54, xl + D, yt - 8, COMP, 2.8, 11) + A(xr + D, yt - 54, xr + D, yt - 8, COMP, 2.8, 11)
        o += T((xl + xr) / 2 + D, yt - 34, '*P*', 16, COMP, 'middle', 'bold')
    if 'H' in loads:
        o += A(xl - 58 + D, yt, xl + D - 8, yt, AC, 3, 12) + T(xl - 56 + D, yt - 12, '*H*', 16, AC, 'start', 'bold')
    if 'R' in loads:
        o += A(xr + 62, yt + 22, xr + 10, yt + 22, KEY, 3, 12) + T(xr + 62, yt + 48, '*R*（反向加回）', 14, KEY, 'end', 'bold')
    if roller:
        o += C(xr + 16, yt, 7, '#fff', KEY, 2) + L(xr + 24, yt - 18, xr + 24, yt + 18, KEY, 3)
        for i in range(5):
            o += L(xr + 24, yt - 16 + i * 8, xr + 31, yt - 20 + i * 8, KEY, 1.2)
        o += T(xr + 36, yt - 26, '假想支撐', 14, KEY, 'start', 'bold')
    return o


def fig4_1():
    W_, H = 900, 400
    o = _frame(0, 0, False, 'PH', '原結構', INK, D=22)
    o += T(290, 210, '＝', 30, INK, 'middle', 'bold')
    o += _frame(305, 0, True, 'P', '① 加假想支撐（不側移）', COMP)
    o += T(600, 210, '＋', 30, INK, 'middle', 'bold')
    o += _frame(620, 0, False, 'HR', '② 拿掉支撐（只側移）', AC, D=22)
    o += R(330, 330, 260, 56, COMP2, COMP, 1.4, 8)
    o += T(460, 354, '得 *M*_{nt} → 乘 *B*_{1}', 15, COMP, 'middle', 'bold')
    o += T(460, 377, '（P-δ，構材自己的事）', 14, INK, 'middle')
    o += R(630, 330, 260, 56, AC2, AC, 1.4, 8)
    o += T(760, 354, '得 *M*_{lt} → 乘 *B*_{2}', 15, AC, 'middle', 'bold')
    o += T(760, 377, '（P-Δ，整層的事）', 14, INK, 'middle')
    o += T(120, 360, '一階分析是線性的，', 14, MUT, 'middle')
    o += T(120, 382, '可以拆開再相加', 14, MUT, 'middle')
    return svg(W_, H, o, '拆兩次')


def fig4_2():
    d, w = ex2014(), ex2014_wrong()
    q = LOAD
    W_, H = 900, 430
    o = T(450, 30, 'SS-2014-4 柱頂（*M*_{nt} = 110、*M*_{lt} = 200 kN·m）的 *M*_{u}', 16, INK, 'middle', 'bold')
    x0, sc = 300, 1.45            # 1 kN·m = 1.45 px
    rows = [('正解：*B*_{1}*M*_{nt} + *B*_{2}*M*_{lt}', [(d['B1'] * q['Mnt_a'], COMP), (d['B2'] * q['Mlt'], AC)], d['Mux_a'], KEY, True),
            ('先加再放大：*B*_{2}(*M*_{nt}+*M*_{lt})', [(w['sum_then_amp'], STEEL)], w['sum_then_amp'], MUT, False),
            ('沒乘 *B*_{2}', [(w['no_B2'], STEEL)], w['no_B2'], MUT, False),
            ('*B*_{1} = 0.358 照乘', [(w['B1_raw_used'], STEEL)], w['B1_raw_used'], MUT, False),
            ('取了柱底（70 那端）', [(d['Mux_b'], STEEL)], d['Mux_b'], MUT, False)]
    for k, (lab, segs, tot, c, ok) in enumerate(rows):
        y = 64 + k * 62
        o += T(x0 - 12, y + 22, lab, 14.5, c if ok else INK, 'end', 'bold' if ok else None)
        x = x0
        for v, cc in segs:
            o += R(x, y, v * sc, 32, cc, '#fff' if ok else None, 1, 3, op=0.9)
            x += v * sc
        o += T(800, y + 23, f'{tot:.1f}', 16, c, 'start', 'bold')
        if not ok:
            o += T(856, y + 23, f'{(tot / d["Mux_a"] - 1) * 100:+.0f}%', 14, COMP, 'start')
    o += T(x0 + d['B1'] * q['Mnt_a'] * sc / 2, 64 + 54, f'{d["B1"]:.2f}×110', 14, COMP, 'middle')
    o += T(x0 + (d['B1'] * q['Mnt_a'] + d['B2'] * q['Mlt'] / 2) * sc, 64 + 54, f'{d["B2"]:.3f}×200 = {d["B2"] * q["Mlt"]:.1f}', 14, AC, 'middle')
    o += L(x0 + d['Mux_a'] * sc, 56, x0 + d['Mux_a'] * sc, 380, KEY, 1.4, '5 4')
    o += R(150, 384, 600, 38, KEY2, KEY, 1.3, 8)
    o += T(450, 409, '四種錯法各差 −22%～+3%；方向錯了，互制比就跟著錯', 14.5, KEY, 'middle', 'bold')
    return svg(W_, H, o, 'Mu 組合')


def fig4_3():
    lv = ex_leaning()
    W_, H = 900, 400
    o = T(250, 32, '靠桿：只壓下來，不幫忙擋側移', 16, INK, 'middle', 'bold')
    xs = [70, 210, 350]
    yt, yb, D = 110, 300, 34
    for i, x in enumerate(xs):
        lean = i == 2
        c = WARN if lean else AC
        o += L(x, yt, x, yb, MUT, 1, '5 5')
        o += L(x + D, yt, x, yb, c, 5)
        if lean:
            o += C(x + D, yt, 6, '#fff', c, 2) + C(x, yb - 6, 6, '#fff', c, 2) + pin(x, yb)
        else:
            o += fixed_wall(x, yb, 46)
        o += A(x + D, yt - 52, x + D, yt - 8, COMP, 2.8, 11)
    o += L(xs[0] + D, yt, xs[2] + D, yt, STEEL, 8)
    o += C(xs[2] + D - 14, yt, 5, '#fff', INK, 1.6)
    o += T(xs[2] + D + 14, yt - 36, '兩端鉸接', 14, WARN, 'start', 'bold')
    o += T((xs[0] + xs[1]) / 2 + D, yb + 40, '抗側力柱：提供 Σ*P*_{eK}', 14, AC, 'middle', 'bold')
    o += T(xs[2] + D, yb + 40, '靠桿：*P*_{eK} = 0', 14, WARN, 'middle', 'bold')
    o += T(250, 378, '每根柱頂都有 *P*，全部算進 Σ*P*_{u}', 14, COMP, 'middle', 'bold')
    o += L(500, 20, 500, 390, GRID, 1.5)
    o += R(520, 60, 365, 280, '#fff', KEY, 1.6, 10)
    o += T(702, 90, '以 SS-2014-4 的樓層勁度示範', 15, KEY, 'middle', 'bold')
    o += T(702, 118, f'Σ*P*_{{e,story}} = {lv["S"]:,.0f} kN', 14.5, INK, 'middle')
    o += T(702, 160, f'Σ*P*_{{u}} = 9000（全部）', 14.5, INK, 'middle')
    o += T(702, 186, f'→ *B*_{{2}} = {lv["B2_full"]:.3f}', 16, KEY, 'middle', 'bold')
    o += T(702, 228, f'若漏掉一半（靠桿的 4500）', 14.5, INK, 'middle')
    o += T(702, 254, f'→ *B*_{{2}} = {lv["B2_half"]:.3f}', 16, COMP, 'middle', 'bold')
    o += T(702, 296, f'放大的部分 {(lv["B2_half"] - 1) / (lv["B2_full"] - 1) * 100:.0f}% 而已：少了一半', 14.5, COMP, 'middle', 'bold')
    return svg(W_, H, o, '靠桿')


def fig4_4():
    W_, H = 900, 400
    o = T(240, 32, 'SS-2013-4：只有一根柱', 16, INK, 'middle', 'bold')
    xa, xb, xd, yt, yb = 50, 240, 430, 120, 300
    o += L(xa, yt, xd, yt, STEEL, 8)
    o += L(xb, yt, xb, yb, AC, 6)
    for x in (xa, xd):
        o += P([(x, yt + 4), (x - 10, yt + 20), (x + 10, yt + 20)], INK, 1.5, '#fff', close=True)
        o += C(x - 5, yt + 25, 4, '#fff', INK, 1.3) + C(x + 5, yt + 25, 4, '#fff', INK, 1.3)
        o += hatch_ground(x - 16, yt + 30, 32)
    o += pin(xb, yb)
    o += A(xa - 50, yt - 22, xa - 4, yt - 22, AC, 3, 12) + T(xa - 50, yt - 32, '*H*', 16, AC, 'start', 'bold')
    o += A(xb, yt - 60, xb, yt - 8, COMP, 3, 12) + T(xb + 10, yt - 38, '*P*', 16, COMP, 'start', 'bold')
    for x, t in ((xa, 'A'), (xb, 'B'), (xd, 'D')):
        o += T(x, yt - 12 if t != 'B' else yt + 26, t, 15, INK, 'middle', 'bold') if t != 'B' else T(xb - 14, yt + 24, 'B', 15, INK, 'end', 'bold')
    o += T(xb - 14, yb - 4, 'C', 15, INK, 'end', 'bold')
    o += dim(xa, yt + 52, xb, yt + 52, '1.5*L*', MUT, size=14) + dim(xb, yt + 52, xd, yt + 52, '1.5*L*', MUT, size=14)
    o += dim(xb + 40, yt, xb + 40, yb, '*L*', MUT, size=14)
    o += T(240, 360, 'A、D 是梁端的滾支承，不是柱', 14.5, COMP, 'middle', 'bold')
    o += T(240, 384, '水平力只能經柱 BC 傳到 C', 14, INK, 'middle')
    o += L(480, 20, 480, 390, GRID, 1.5)
    o += R(500, 50, 385, 330, '#fff', KEY, 1.6, 10)
    lines = [('① 加假想支撐、只放 *P*：', INK, None),
             ('   *P* 與柱同軸、梁對稱 ⇒ θ_{B} = 0', INK, None),
             ('   ⇒ *M*_{nt} = 0', COMP, 'bold'),
             ('② 拿掉支撐、只放 *H*：', INK, None),
             ('   柱 BC 自由體對 C 取矩', INK, None),
             ('   ⇒ *M*_{lt} = *HL*（柱頂）', AC, 'bold'),
             ('③ *M*_{u} = *B*_{1}·0 + *B*_{2}·*HL* = *B*_{2}*HL*', KEY, 'bold'),
             ('   Σ*P*_{u} = *P*，Σ*P*_{eK} 只有一根柱', INK, None),
             ('   （*K* 由對位圖，第 5 章）', MUT, None)]
    for i, (s, c, w) in enumerate(lines):
        o += T(516, 84 + i * 34, s, 15 if w else 14.5, c, 'start', w)
    return svg(W_, H, o, 'SS-2013-4 拆解')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3, 'fig4_4': fig4_4}
