# -*- coding: utf-8 -*-
"""第 1 章：一根柱就是一支彈簧。變形形狀、彎矩分布全部由 calcs 的函數算出。"""
from figs_common import *  # noqa
from calcs import ff_moment, ex2020, k20, k22, k22_tall, h20


def _cant_rel(s):
    """懸臂（根部 s=0、尖端 s=1）受尖端力的相對撓度形狀 (3s²−s³)/2，尖端＝1。"""
    return (3 * s ** 2 - s ** 3) / 2


def fig1_1():
    W, H = 900, 480
    o = ''
    yb, yt = 390, 130
    D = 64                                    # 柱頂側移（像素，放大示意）
    # ── (a) 側移形狀 ──
    x = 120
    o += T(150, 34, '(a) 柱頂跟著剛性梁平移 Δ', 16, INK, 'middle', 'bold')
    o += L(x, yb, x, yt, STEEL, 2, '6 5')
    o += R(x - 40, yt - 5, 80, 10, 'none', STEEL, 1.5, 2, dash='5 4')
    o += col_ff(x, yb, yt, 0, D, AC, 3.4)
    o += rigid_beam(x - 40 + D, x + 40 + D, yt, INK, 10)
    o += T(x + D + 46, yt + 5, '梁 *I* = ∞', 15, WARN, 'start', 'bold')
    o += base_fixed(x, yb + 2, 56)
    o += A(x + D - 18, yt - 24, x + D + 42, yt - 24, COMP, 3, 12)
    o += T(x + D + 50, yt - 18, '*V*', 17, COMP, 'start', 'bold')
    o += dim(x, yt - 56, x + D, yt - 56, 'Δ', AC, size=16, lab_off=-14)
    ym = (yb + yt) / 2
    o += C(x + D / 2, ym, 7, KEY, '#fff', 2)
    o += T(x + D / 2 + 14, ym + 5, '反曲點', 15, KEY, 'start', 'bold')
    o += T(x + D / 2 + 14, ym + 26, '*M* = 0', 15, KEY, 'start')
    o += dim(x - 46, yb, x - 46, yt, '*h*', INK, size=16, lab_off=14)
    o += T(x + 8, yb - 20, '底不轉', 14, WARN, 'start')
    o += T(x + D + 8, yt + 30, '頂不轉', 14, WARN, 'start')
    # ── (b) 彎矩圖 ──
    x0 = 455
    sc = 62
    o += T(450, 34, '(b) 彎矩：上下相反、中間為 0', 16, INK, 'middle', 'bold')
    o += L(x0, yb, x0, yt, INK, 2)
    pts = [(x0 + sc * ff_moment(i / 40), yb + (yt - yb) * i / 40) for i in range(41)]
    o += P([(x0, yb)] + pts + [(x0, yt)], None, fill=COMP2, close=True)
    o += P(pts, COMP, 2.6)
    o += T(x0 + sc + 8, yb + 6, '*M* = *Vh*/2', 15, COMP, 'start', 'bold')
    o += T(x0 - sc - 8, yt + 6, '*M* = *Vh*/2', 15, COMP, 'end', 'bold')
    o += C(x0, ym, 7, KEY, '#fff', 2)
    o += T(x0 + 14, ym - 8, '0', 16, KEY, 'start', 'bold')
    o += T(450, yb + 46, '直線：剪力 *V* 沿柱高不變', 15, MUT, 'middle')
    o += T(450, yb + 70, '斜率 = *V*', 15, MUT, 'middle')
    # ── (c) 從反曲點切開：兩支 h/2 懸臂 ──
    xc = 690
    d = D / 2
    o += T(750, 34, '(c) 從反曲點切開＝兩支懸臂', 16, INK, 'middle', 'bold')
    gap = 18
    ymL, ymU = ym + gap, ym - gap
    # 下半支：根在柱底
    o += L(xc, yb, xc, ymL, STEEL, 2, '6 5')
    o += P([(xc + d * _cant_rel(i / 40), yb + (ymL - yb) * i / 40) for i in range(41)], AC, 3.4)
    o += base_fixed(xc, yb + 2, 56)
    o += A(xc + d - 44, ymL, xc + d - 6, ymL, COMP, 2.6, 11)
    o += T(xc + d - 50, ymL + 5, '*V*', 16, COMP, 'end', 'bold')
    o += T(xc + d + 12, (yb + ymL) / 2 + 10, 'δ', 17, AC, 'start', 'bold')
    o += dim(xc, ymL + 16, xc + d, ymL + 16, '', AC)
    # 上半支：根在柱頂（隨梁平移 Δ）
    o += L(xc + D, yt, xc + D, ymU, STEEL, 2, '6 5')
    o += P([(xc + D - d * _cant_rel(i / 40), yt + (ymU - yt) * i / 40) for i in range(41)], AC, 3.4)
    o += rigid_beam(xc + D - 40, xc + D + 40, yt, INK, 10)
    o += A(xc + d + 44, ymU, xc + d + 6, ymU, COMP, 2.6, 11)
    o += T(xc + d + 50, ymU + 5, '*V*', 16, COMP, 'start', 'bold')
    o += T(xc + D - d - 14, (yt + ymU) / 2 - 2, 'δ', 17, AC, 'end', 'bold')
    o += dim(xc + d, ymU - 16, xc + D, ymU - 16, '', AC)
    o += T(xc + 96, yb - 40, '長度 *h*/2', 15, INK, 'start')
    o += T(xc + 112, yt + 44, '長度 *h*/2', 15, INK, 'start')
    o += R(612, yb + 26, 276, 56, KEY2, KEY, 1.6, 10)
    o += T(750, yb + 50, 'Δ = 2δ = 2 · *V*(*h*/2)^{3}/3*EI*', 15, KEY, 'middle', 'bold')
    o += T(750, yb + 73, '= *Vh*^{3}/12*EI*', 15, KEY, 'middle', 'bold')
    o += L(305, 50, 305, H - 14, GRID, 1.4) + L(600, 50, 600, H - 14, GRID, 1.4)
    return svg(W, H, o, '兩端不轉的柱：側移、彎矩、從反曲點切開')


def fig1_3():
    W, H = 900, 450
    o = ''
    yb = 390
    hp = 125                                   # h 對應像素
    D = 44
    cols = [(90, hp, 'ff', '(a) 兩端不轉', '高 *h*'),
            (250, hp, 'pin', '(b) 柱底鉸接', '高 *h*'),
            (440, 2 * hp, 'ff', '(c) 挑高柱', '高 2*h*')]
    for x, hh, kind, ttl, hl in cols:
        yt = yb - hh
        o += T(x + 20, 34, ttl, 16, INK, 'middle', 'bold')
        o += L(x, yb, x, yt, STEEL, 2, '6 5')
        if kind == 'ff':
            o += col_ff(x, yb, yt, 0, D, AC, 3.2)
            o += base_fixed(x, yb + 2, 50)
            ym = (yb + yt) / 2
            o += C(x + D / 2, ym, 6, KEY, '#fff', 2)
        else:
            o += col_pin_base(x, yb, yt, D, AC, 3.2)
            o += pin(x, yb + 1)
            o += C(x, yb - 2, 6, KEY, '#fff', 2)
        o += rigid_beam(x - 30 + D, x + 30 + D, yt, INK, 9)
        o += dim(x - 34, yb, x - 34, yt, hl, INK, size=15, lab_off=12, side=-1)
    o += T(250, 72, '紫點＝反曲點（*M* = 0）', 15, KEY, 'middle')
    # 長條圖
    px, pw = 560, 300
    vals = [('(a)', 12, '12', AC), ('(b)', 3, '3', TEN), ('(c)', 1.5, '1.5 = 12/8', WARN)]
    o += T(px + pw / 2 - 10, 34, '側向勁度 *k*（單位 *EI*/*h*^{3}）', 16, INK, 'middle', 'bold')
    sc = pw / 12.5
    for i, (lab, v, txt, c) in enumerate(vals):
        y = 90 + i * 92
        o += T(px - 8, y + 30, lab, 16, INK, 'end', 'bold')
        o += R(px, y + 8, v * sc, 36, c, None, 0, 5)
        o += T(px + v * sc + 8, y + 33, txt, 16, c, 'start', 'bold')
    o += L(px, 80, px, 330, INK, 1.6)
    o += R(px - 6, 346, 316, 70, KEY2, KEY, 1.6, 10)
    o += T(px + 152, 372, '反曲點跑到鉸 → 懸臂長 *h*：÷4', 15, KEY, 'middle', 'bold')
    o += T(px + 152, 398, '柱高加倍 → *h*^{3} 變 8 倍：÷8', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '三種柱的側向勁度比較')


def fig1_2():
    r = ex2020()
    V, M = r['V_eh'], r['M_eh']
    W, H = 900, 430
    o = ''
    x, yb, yt = 200, 350, 90
    D = 40
    o += T(220, 34, '(a) eh 柱的自由體圖（SA-2020-4）', 16, INK, 'middle', 'bold')
    o += col_ff(x, yb, yt, 0, D, ACM, 2.2, '6 4')
    o += L(x, yb, x, yt, INK, 6)
    o += A(x + 8, yt, x + 100, yt, COMP, 3.2, 13)
    o += T(x + 106, yt + 6, f'*V* = {V:.0f} kN', 16, COMP, 'start', 'bold')
    o += A(x - 8, yb, x - 100, yb, COMP, 3.2, 13)
    o += T(x - 106, yb + 6, f'{V:.0f} kN', 16, COMP, 'end', 'bold')
    o += arc_arrow(x, yt, 30, -150, 120, COMP, 2.6, 11)
    o += T(x - 38, yt - 26, f'*M* = {M:.0f}', 16, COMP, 'end', 'bold')
    o += arc_arrow(x, yb, 30, 30, 300, COMP, 2.6, 11)
    o += T(x + 38, yb + 34, f'*M* = {M:.0f}', 16, COMP, 'start', 'bold')
    o += dim(x + 240, yb, x + 240, yt, f'*h* = {h20:g} m', INK, size=15, lab_off=12, side=-1)
    o += T(x + 46, (yb + yt) / 2 + 5, '逆時針', 15, MUT, 'start')
    o += T(x + 46, (yb + yt) / 2 + 27, '兩端同向', 15, MUT, 'start')
    # 右：力矩平衡
    bx = 490
    o += R(bx, 70, 390, 280, '#fff', KEY, 1.8, 12)
    o += T(bx + 195, 100, '(b) 對柱底取力矩，平衡', 16, KEY, 'middle', 'bold')
    o += T(bx + 24, 142, '剪力偶（順時針）：', 15, INK)
    o += T(bx + 60, 172, f'*V* · *h* = {V:.0f} × {h20:g} = {V * h20:.0f} kN-m', 16, COMP, 'start', 'bold')
    o += T(bx + 24, 214, '兩端彎矩（逆時針）：', 15, INK)
    o += T(bx + 60, 244, f'2*M* = 2 × {M:.0f} = {2 * M:.0f} kN-m', 16, COMP, 'start', 'bold')
    o += L(bx + 24, 268, bx + 366, 268, GRID, 1.4)
    o += T(bx + 195, 300, '兩者相等 → *M* = *Vh*/2', 17, KEY, 'middle', 'bold')
    o += T(bx + 195, 330, '（兩端同大，是反對稱給的）', 15, MUT, 'middle')
    o += T(450, 405, '藍色虛線：側移形狀（Δ = 1 mm，放大示意）', 14, MUT, 'middle')
    return svg(W, H, o, 'eh 柱自由體圖與力矩平衡')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
