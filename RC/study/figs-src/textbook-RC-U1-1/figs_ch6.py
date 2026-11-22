# -*- coding: utf-8 -*-
"""第 6 章：T 形梁——有效翼板寬、a ≤ hf 判別、翼腹分解、負彎矩。"""
from figs_common import *  # noqa
from calcs import tbeam_demo, rc2020_1
import math

TB = tbeam_demo()
R0 = rc2020_1()


def fig6_1():
    W, H = 900, 480
    o = T(450, 24, '樓版與梁一起澆置：翼板的壓應力離腹板越遠越小（剪力遲滯）', 16, INK, 'middle', 'bold')
    # 剖面：三根梁，中心距 400 cm
    sc = 0.85  # px/cm
    xc = 450; y0 = 130
    hf, bw, s = 12 * 2.2, 40 * sc, 400 * sc
    o += R(xc - s * 1.25, y0, s * 2.5, hf, STEEL2, INK, 1.2)
    for k in (-1, 0, 1):
        o += R(xc + k * s - bw / 2, y0 + hf, bw, 70, STEEL2, INK, 1.2)
    o += hdim(xc - s, xc, y0 + hf + 92, '梁中心距 400', INK, 1)
    # 應力分布（示意，曲線由函數計算）
    lam = 70.0
    def sig(xcm):
        u = abs(xcm)
        return 1.0 if u <= 20 else 1 / (1 + ((u - 20) / lam) ** 2)
    base = y0 - 6
    amp = 46
    pts = [(xc - 200 * sc, base)]
    for i in range(401):
        xx = -200 + 400 * i / 400
        pts.append((xc + xx * sc, base - amp * sig(xx)))
    pts.append((xc + 200 * sc, base))
    o += P(pts, COMP, 2.2, fill=COMP2, close=True)
    area = sum(sig(-200 + 400 * (i + 0.5) / 4000) for i in range(4000)) * 400 / 4000
    be_eq = area
    o += R(xc - be_eq * sc / 2, base - amp, be_eq * sc, amp, 'none', AC, 2.4, dash='6 4')
    o += T(xc + be_eq * sc / 2 + 8, base - amp + 16, f'等面積長方形：寬 ≈ {be_eq:.0f} cm', 14, AC, 'start', 'bold')
    o += T(40, base - 36, '真實的翼板壓應力', 14, COMP, 'start', 'bold') + T(40, base - 14, '（示意曲線）', 14, COMP, 'start')
    # 三條件
    yb = 340
    rows = [(f"① 跨度/4 = 800/4 = {TB['be1']:.0f}", '跨度短 → 力來不及攤開', TB['be1']),
            (f"② *b*_{{w}} + 16*h*_{{f}} = 40 + 192 = {TB['be2']:.0f}", '翼板薄 → 傳不遠', TB['be2']),
            (f"③ 梁中心距 = {TB['be3']:.0f}", '不能和鄰梁搶同一塊版', TB['be3'])]
    for i, (a, b_, v) in enumerate(rows):
        y = yb + i * 40
        col = KEY if v == TB['be'] else MUT
        o += T(60, y, a, 15, col, 'start', 'bold' if v == TB['be'] else None)
        o += T(470, y, b_, 15, INK, 'start')
    o += T(450, yb + 128, f"示範 T 梁（跨度 8 m、梁距 4 m、*h*_{{f}} = 12）：*b*_{{e}} = min = {TB['be']:.0f} cm", 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '有效翼板寬')


def tsec(o, x, y0, sc, be, bw, hf, h, a, cap, color):
    o += section(x, y0, sc, bw, h, be, hf)
    if a <= hf:
        o += R(x - be * sc / 2, y0, be * sc, a * sc, color, None, 0, 0, op=0.55)
    else:
        o += R(x - be * sc / 2, y0, be * sc, hf * sc, color, None, 0, 0, op=0.55)
        o += R(x - bw * sc / 2, y0, bw * sc, a * sc, color, None, 0, 0, op=0.55)
    o += L(x - be * sc / 2 - 8, y0 + a * sc, x + be * sc / 2 + 8, y0 + a * sc, color, 2, '5 3')
    o += T(x, y0 + h * sc + 28, cap, 15, INK, 'middle', 'bold')
    return o


def fig6_2():
    W, H = 900, 420
    o = T(450, 24, '分岔只問一件事：應力塊深度 *a* 有沒有超過翼板厚 *h*_{f}', 16, INK, 'middle', 'bold')
    sc = 1.05
    o = tsec(o, 225, 80, 1.8, 200, 40, 12, 60, TB['a'], '', WARN)
    o += T(225, 80 + 60 * 1.8 + 30, f"示範 T 梁：*a* = {TB['a']:.2f} ≤ *h*_{{f}} = 12", 15, TEN, 'middle', 'bold')
    o += T(225, 80 + 60 * 1.8 + 54, '→ 就是寬 *b*_{e} 的矩形梁', 15, TEN, 'middle', 'bold')
    sc2 = 2.2
    o = tsec(o, 680, 80, sc2, 125, 50, 10, 70, R0['aw'], '', WARN)
    o += T(680, 80 + 70 * sc2 + 30, f"RC-2020-1：*a* = {R0['aw']:.2f} > *h*_{{f}} = 10", 15, COMP, 'middle', 'bold')
    o += T(680, 80 + 70 * sc2 + 54, '→ 拆成翼板懸出＋腹板', 15, COMP, 'middle', 'bold')
    o += L(450, 60, 450, 380, GRID, 2)
    return svg(W, H, o, 'a 與 hf')


def fig6_3():
    W, H = 900, 330
    o = T(450, 24, 'RC-2020-1：*a* > *h*_{f} 時把壓力拆成兩塊（依比例，*b*_{e} = 125、*b*_{w} = 50）', 16, INK, 'middle', 'bold')
    sc = 2.4
    x0, y0 = 240, 80
    be, bw, hf, d = 125, 50, 10, 64
    aw = R0['aw']
    # 翼板懸出兩塊
    o += section(x0, y0, sc, bw, 70, be, hf)
    o += R(x0 - be * sc / 2, y0, (be - bw) * sc / 2, hf * sc, TEN, None, 0, 0, op=0.55)
    o += R(x0 + bw * sc / 2, y0, (be - bw) * sc / 2, hf * sc, TEN, None, 0, 0, op=0.55)
    o += R(x0 - bw * sc / 2, y0, bw * sc, aw * sc, WARN, None, 0, 0, op=0.55)
    o += T(x0 - be * sc / 2 + 45, y0 - 10, '翼板懸出', 14, TEN, 'middle', 'bold')
    o += T(x0 + be * sc / 2 - 45, y0 - 10, '翼板懸出', 14, TEN, 'middle', 'bold')
    o += T(x0, y0 + aw * sc / 2 + 30, '腹板', 14, WARN, 'middle', 'bold')
    o += bars(x0, y0 + d * sc, sc, bw, 4, 3.2, INK, cover=8)
    o += vdim(x0 + be * sc / 2 + 14, y0, y0 + hf * sc, '*h*_{f} = 10', TEN, 1)
    o += vdim(x0 + be * sc / 2 + 96, y0, y0 + aw * sc, f'*a*_{{w}} = {aw:.2f}', WARN, 1)
    o += vdim(x0 - bw * sc / 2 - 14, y0 + hf * sc + 4, y0 + d * sc, '*d* = 64（自頂面）', INK, -1)
    # 力
    xf = 640
    yf = y0 + hf / 2 * sc - 8; yw = y0 + aw / 2 * sc + 14; yt = y0 + d * sc
    o += A(xf + 110, yf, xf, yf, TEN, 3.2, 13)
    o += T(xf + 116, yf + 5, f"*C*_{{f}} = {R0['Cf']/1000:.1f} tf", 15, TEN, 'start', 'bold')
    o += A(xf + 110, yw, xf, yw, WARN, 3.2, 13)
    o += T(xf + 116, yw + 5, f"*C*_{{w}} = {(R0['As']*4200-R0['Cf'])/1000:.1f} tf", 15, WARN, 'start', 'bold')
    o += A(xf, yt, xf + 110, yt, INK, 3.2, 13)
    o += T(xf + 116, yt + 5, f"*T* = {R0['As']*4.2:.1f} tf", 15, INK, 'start', 'bold')
    o += vdim(xf - 20, yf, yt, '*d* − *h*_{f}/2 = 59', TEN, -1)
    o += vdim(xf + 60, yw, yt, f"*d* − *a*_{{w}}/2 = {d - aw/2:.2f}", WARN, 1)
    o += T(450, 312, f"*A*_{{sf}} = *C*_{{f}}/*f*_{{y}} = {R0['Asf']:.2f}、*A*_{{sw}} = {R0['Asw']:.2f} → *A*_{{s}} = {R0['As']:.2f} cm²", 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '翼腹分解')


def fig6_4():
    W, H = 900, 400
    o = T(450, 24, '同一根 T 梁：跨中正彎矩 vs. 支承處負彎矩（6-D25，依比例）', 16, INK, 'middle', 'bold')
    sc = 1.3
    # 跨中
    x1, y0 = 230, 90
    o += section(x1, y0, sc, 40, 60, 200, 12)
    o += R(x1 - 100 * sc, y0, 200 * sc, TB['a'] * sc, WARN, None, 0, 0, op=0.7)
    o += bars(x1, y0 + 53 * sc, sc, 40, 6, 2.54, TEN, cover=5)
    o += T(x1, y0 - 14, '跨中（下拉上壓）', 15, INK, 'middle', 'bold')
    o += T(x1, y0 + 60 * sc + 34, f"壓力區在翼板：*b*_{{e}} = 200、*a* = {TB['a']:.2f}", 15, TEN, 'middle', 'bold')
    o += T(x1, y0 + 60 * sc + 58, f"*M*_{{n}} = {TB['Mn']/1e5:.2f} tf·m", 15, TEN, 'middle', 'bold')
    # 支承
    x2 = 670
    o += section(x2, y0, sc, 40, 60, 200, 12)
    o += R(x2 - 20 * sc, y0 + (60 - TB['a_neg']) * sc, 40 * sc, TB['a_neg'] * sc, WARN, None, 0, 0, op=0.7)
    o += bars(x2, y0 + 7 * sc, sc, 40, 6, 2.54, TEN, cover=5)
    o += T(x2, y0 - 14, '支承（上拉下壓）', 15, INK, 'middle', 'bold')
    o += T(x2, y0 + 60 * sc + 34, f"壓力區在腹板底：寬 *b*_{{w}} = 40、*a* = {TB['a_neg']:.2f}", 15, COMP, 'middle', 'bold')
    o += T(x2, y0 + 60 * sc + 58, f"*M*_{{n}} = {TB['Mn_neg']/1e5:.2f} tf·m（就是 40×60 矩形梁）", 15, COMP, 'middle', 'bold')
    o += T(x2, y0 + 60 * sc + 82, '翼板在受拉側、開裂：不計', 15, COMP, 'middle')
    o += L(450, 60, 450, 330, GRID, 2)
    o += T(450, 380, '判斷準則永遠是「壓力區長什麼樣子」，不是斷面外形', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '負彎矩 T 梁')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
