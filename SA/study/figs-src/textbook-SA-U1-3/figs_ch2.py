# -*- coding: utf-8 -*-
"""第 2 章：Müller-Breslau 作圖。變形形狀的每一個縱距都由 calcs.py（平衡求解器）算出，
因此圖上的形狀同時驗證了「形狀＝影響線」。"""
from figs_common import *  # noqa
import calcs as K

Lm, a, b = K.L, K.a, K.b
DEF = KEY        # 變形後形狀（紫）


def fig2_1():
    """虛功證明：狀態①真實力系、狀態②拆掉 A 支承推上 1。"""
    W, H = 900, 556
    ax = Ax(150, 56)
    o = ''
    x = K.X1
    # 狀態 ①
    yb = 120
    o += T(14, 38, '狀態①　真實的梁：單位載重在 *x*，反力 *R*_{*A*}', 16, INK, 'start', 'bold')
    o += beam(ax, yb, 0, Lm, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', 16)])
    o += unit_load(ax(x), yb - 3)
    o += up_arrow(ax(0) - 30, yb + 2, label='*R*_{*A*}', h=46)
    o += up_arrow(ax(Lm) + 30, yb + 2, label='*R*_{*B*}', h=46)
    # 狀態 ②
    y2 = 390
    sy = 100
    o += T(14, 236, '狀態②　拆掉 A 的支承，把 A 往上推 1（梁不彎，只繞 B 轉）', 16, INK, 'start', 'bold')
    o += L(ax(0), y2, ax(Lm), y2, STEEL3, 4, '8 6')
    o += roller(ax(Lm), y2 + 3)
    o += L(ax(0), y2 - sy, ax(Lm), y2, DEF, 5)
    o += A(ax(0) - 22, y2, ax(0) - 22, y2 - sy, DEF, 2.4, 11)
    o += T(ax(0) - 30, y2 - sy / 2 + 5, 'Δ = 1', 16, DEF, 'end', 'bold')
    dx = K.RA_ss(x)
    o += A(ax(x), y2, ax(x), y2 - sy * dx, AC, 2.2, 10)
    o += T(ax(x) + 10, y2 - sy * dx / 2 + 26, f'δ(*x*) = (*L*−*x*)/*L* = {f(dx)}', 16, AC, 'start', 'bold')
    o += L(ax(x), y2 - sy - 14, ax(x), y2 + 10, COMP, 1.2, '5 4')
    # 虛功式
    o += R(40, 438, 820, 104, KEY2, KEY, 1.4, 10)
    o += T(450, 468, '虛功：狀態①的力 × 狀態②的位移 ＝ 0（梁沒彎，內力不作功）', 16, KEY, 'middle', 'bold')
    o += T(450, 498, '*R*_{*A*} × 1　−　1 × δ(*x*)　＋　*R*_{*B*} × 0　＝　0', 17, INK, 'middle', 'bold')
    o += T(450, 528, '⇒　*R*_{*A*}(*x*) ＝ δ(*x*)：推出來的形狀，就是影響線', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'Müller-Breslau 的虛功證明')


def _row_title(o, y, s):
    return o + T(14, y, s, 16, INK, 'start', 'bold')


def fig2_2():
    """三種拆法：反力、剪力、彎矩。"""
    W, H = 900, 720
    ax = Ax(150, 56)
    sy = 90
    o = ''
    # (a) 反力
    y = 150
    o = _row_title(o, 34, '(a) 求 *R*_{*A*}：拆掉 A 的支承，A 上推 1')
    o += L(ax(0), y, ax(Lm), y, STEEL3, 4, '8 6') + roller(ax(Lm), y + 3)
    o += L(ax(0), y - sy, ax(Lm), y, DEF, 5)
    o += T(ax(0) - 12, y - sy + 5, '1', 16, DEF, 'end', 'bold')
    o += T(ax(Lm) + 30, y - 40, '只繞 B 轉', 15, MUT, 'start')
    # (b) 剪力
    y = 360
    o = _row_title(o, 230, '(b) 求 *V*_{*C*}：在 C 切開成「滑塊」（只能上下錯開，不能轉）')
    o += L(ax(0), y, ax(Lm), y, STEEL3, 4, '8 6') + pin(ax(0), y + 3) + roller(ax(Lm), y + 3)
    yl, yr = K.VC_LEFT, K.VC_RIGHT
    o += L(ax(0), y, ax(a), y - sy * yl, DEF, 5) + L(ax(a), y - sy * yr, ax(Lm), y, DEF, 5)
    o += L(ax(a) - 5, y - sy * yl + 6, ax(a) - 5, y - sy * yr - 6, WARN, 2) + L(ax(a) + 5, y - sy * yl + 6, ax(a) + 5, y - sy * yr - 6, WARN, 2)
    o += A(ax(a) + 34, y - sy * yl, ax(a) + 34, y - sy * yr, KEY, 2, 9, both=True)
    o += T(ax(a) + 44, y - sy * (yl + yr) / 2 + 5, '相對錯開 1', 15, KEY, 'start', 'bold')
    o += T(ax(a) - 12, y - sy * yl + 22, f(yl), 15, DEF, 'end', 'bold')
    o += T(ax(a) - 12, y - sy * yr - 8, f'+{f(yr)}', 15, DEF, 'end', 'bold')
    o += T(ax(Lm) + 30, y - 40, '兩段平行', 15, MUT, 'start')
    o += T(ax(Lm) + 30, y - 16, '（滑塊不能轉）', 15, MUT, 'start')
    # (c) 彎矩
    y = 680
    sym = 52
    o = _row_title(o, 490, '(c) 求 *M*_{*C*}：在 C 插一個鉸，讓兩邊相對轉 1 弧度')
    o += L(ax(0), y, ax(Lm), y, STEEL3, 4, '8 6') + pin(ax(0), y + 3) + roller(ax(Lm), y + 3)
    o += L(ax(0), y, ax(a), y - sym * K.MC_PEAK, DEF, 5) + L(ax(a), y - sym * K.MC_PEAK, ax(Lm), y, DEF, 5)
    o += hinge(ax(a), y - sym * K.MC_PEAK, 7, DEF)
    o += T(ax(a), y - sym * K.MC_PEAK - 16, f'頂高 = θ_{{A}}·*a* = {f(K.thA)}×6 = {f(K.MC_PEAK)}', 15, DEF, 'middle', 'bold')
    o += T(ax(2.0), y - 10, f'θ_{{A}} = {f(K.thA)}', 15, AC, 'middle', 'bold')
    o += T(ax(8.1), y - 12, f'θ_{{B}} = {f(K.thB)}', 15, AC, 'middle', 'bold')
    o += T(ax(Lm) + 30, y - 66, 'θ_{*A*} + θ_{*B*} = 1', 15, KEY, 'start', 'bold')
    o += T(ax(Lm) + 30, y - 42, '頂點共用：', 15, MUT, 'start')
    o += T(ax(Lm) + 30, y - 18, 'θ_{*A*}·*a* = θ_{*B*}·*b*', 15, MUT, 'start')
    return svg(W, H, o, '三種拆法')


def fig2_3():
    """作圖規則卡：每一種點，推完以後允許什麼。"""
    W, H = 900, 300
    cw, ch = 170, 250
    cells = [('滾／鉸支承', '位移 = 0', '可以轉折'), ('固定端', '位移 = 0', '斜率也 = 0'),
             ('內鉸', '位移連續', '可以轉折'), ('連續梁段', '位移連續', '不能轉折'), ('懸臂自由端', '不受限', '直線延伸')]
    o = ''
    for k, (nm, l1, l2) in enumerate(cells):
        ox = 10 + k * (cw + 7)
        o += R(ox, 12, cw, ch, '#fff', GRID, 1.4, 10)
        o += T(ox + cw / 2, 40, nm, 16, INK, 'middle', 'bold')
        cx, cy = ox + cw / 2, 140
        if k == 0:
            o += L(cx - 60, cy - 30, cx, cy, DEF, 4) + L(cx, cy, cx + 60, cy - 50, DEF, 4)
            o += pin(cx, cy + 3)
        elif k == 1:
            o += L(cx - 50, cy - 40, cx - 50, cy + 30, INK, 3)
            for i in range(8):
                yy = cy - 40 + i * 10
                o += L(cx - 50, yy, cx - 58, yy + 7, INK, 1)
            o += L(cx - 50, cy, cx + 60, cy, DEF, 4)
            o += T(cx + 4, cy - 14, '保持水平', 14, DEF, 'middle')
        elif k == 2:
            o += L(cx - 60, cy + 10, cx, cy - 30, DEF, 4) + L(cx, cy - 30, cx + 60, cy + 20, DEF, 4)
            o += hinge(cx, cy - 30, 7, DEF)
        elif k == 3:
            o += L(cx - 60, cy + 10, cx + 60, cy - 40, DEF, 4)
            o += L(cx - 60, cy + 10, cx, cy - 30, COMPM, 2, '5 4') + L(cx, cy - 30, cx + 60, cy + 20, COMPM, 2, '5 4')
            o += T(cx + 40, cy + 36, '這樣折不行', 14, COMP, 'middle')
        else:
            o += L(cx - 60, cy + 30, cx + 10, cy - 10, DEF, 4) + L(cx + 10, cy - 10, cx + 65, cy - 41, DEF, 3, '6 4')
            o += roller(cx + 10, cy - 7)
        o += T(ox + cw / 2, 222, l1, 15, MUT, 'middle')
        o += T(ox + cw / 2, 246, l2, 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '作圖規則卡')


def fig2_4():
    """加 3 m 懸臂段：三條影響線都沿直線延伸到 D。"""
    W, H = 900, 720
    ax = Ax(110, 48)          # 13 m → 624 px
    o = ''
    yb = 76
    LD = K.LD
    o += beam(ax, yb, 0, LD, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', -16), (LD, 'D', 16)])
    o += L(ax(a), yb - 12, ax(a), yb + 12, KEY, 3)
    o += T(ax(a), yb - 18, 'C', 16, KEY, 'middle', 'bold')
    o += dim(ax(Lm), yb + 46, ax(LD), yb + 46, '懸臂 3 m', MUT, size=15)
    t = (0, a, Lm, LD)
    o += il(ax, 240, 80, [(0, 1), (Lm, 0), (LD, K.OH_RA_D)], name='IL *R*_{*A*}', ticks=t,
            vals=[(0, 1, '1', 'w'), (LD, K.OH_RA_D, f(K.OH_RA_D), 'e')])
    o += il(ax, 390, 80, [(0, 0), (a, K.VC_LEFT), (a, K.VC_RIGHT), (Lm, 0), (LD, K.OH_VC_D)], name='IL *V*_{*C*}', ticks=t,
            vals=[(a, K.VC_LEFT, f(K.VC_LEFT), (-28, 24)), (a, K.VC_RIGHT, f'+{f(K.VC_RIGHT)}', (30, -10)), (LD, K.OH_VC_D, f(K.OH_VC_D), 'e')])
    o += il(ax, 600, 30, [(0, 0), (a, K.MC_PEAK), (Lm, 0), (LD, K.OH_MC_D)], name='IL *M*_{*C*}', ticks=t,
            vals=[(a, K.MC_PEAK, f'{f(K.MC_PEAK)} m'), (LD, K.OH_MC_D, f'{f(K.OH_MC_D)} m', 'e')])
    o += L(ax(Lm), yb + 30, ax(Lm), 660, STEEL, 1, '3 4')
    o += T(ax(6.5), 700, '懸臂段：B 左邊那一段直線，原樣延長到 D', 15, WARN, 'middle', 'bold')
    return svg(W, H, o, '懸臂段影響線')


def _gax():
    return Ax(130, 38)        # 16 m → 608 px


def fig2_5():
    """SA-2025-2：主從關係。"""
    W, H = 900, 390
    ax = _gax()
    o = ''
    yb = 82
    o += T(14, 30, '原結構（題目）', 16, INK, 'start', 'bold')
    o += beam(ax, yb, 0, 16, [(0, 'fixL'), (8, 'roller'), (16, 'roller')], hinges=[4, 12],
              labels=[(0, 'A', 14), (4, 'B'), (6, 'F'), (8, 'C'), (12, 'D'), (16, 'E', 12)])
    o += L(ax(6), yb - 8, ax(6), yb + 8, KEY, 2)
    o += dim(ax(0), yb + 44, ax(16), yb + 44, '4@4 m = 16 m', MUT, size=15)
    # 拆層
    o += T(14, 172, '拆成三層（誰靠誰站著）', 16, INK, 'start', 'bold')
    y1, y2, y3 = 330, 270, 210
    o += L(ax(0), y1, ax(4), y1, TEN, 6) + fixed_left(ax(0), y1, 50)
    o += T(ax(2), y1 + 34, '主結構：懸臂 AB（自己站得住）', 15, TEN, 'start', 'bold')
    o += L(ax(4), y2, ax(12), y2, AC, 6) + roller(ax(8), y2 + 3)
    o += hinge(ax(4), y2, 6.5, AC) + hinge(ax(12), y2, 6.5, AC)
    o += A(ax(4), y2 + 8, ax(4), y1 - 6, AC, 2, 10)
    o += T(ax(4) + 10, y2 - 14, '從屬：BD 靠 B 點掛在 AB 上、靠 C 撐住', 15, AC, 'start', 'bold')
    o += L(ax(12), y3, ax(16), y3, WARN, 6) + roller(ax(16), y3 + 3)
    o += hinge(ax(12), y3, 6.5, WARN)
    o += A(ax(12), y3 + 8, ax(12), y2 - 6, WARN, 2, 10)
    o += T(ax(12) - 10, y3 - 14, '再從屬：DE 靠 D 掛在 BD 上', 15, WARN, 'end', 'bold')
    o += T(ax(16) + 18, y3 + 50, '載重往下層傳，', 14, MUT, 'start')
    o += T(ax(16) + 18, y3 + 72, '不會往上層傳', 14, MUT, 'start')
    return svg(W, H, o, 'SA-2025-2 主從關係')


def fig2_6():
    """SA-2025-2：五條影響線（平衡求解器逐點算出，與 Müller-Breslau 形狀一致）。"""
    W, H = 900, 1090
    ax = _gax()
    o = ''
    yb = 64
    o += beam(ax, yb, 0, 16, [(0, 'fixL'), (8, 'roller'), (16, 'roller')], hinges=[4, 12],
              labels=[(0, 'A', 14), (4, 'B'), (6, 'F'), (8, 'C'), (12, 'D'), (16, 'E', 12)])
    o += L(ax(6), yb - 8, ax(6), yb + 8, KEY, 2)
    xs = [x for _, x in K.G_PTS]
    T_ = K.G_TABLE
    tk = (0, 4, 6, 8, 12, 16)

    def pts_of(key):
        return [(0, T_[key][0]), (4, T_[key][1]), (8, T_[key][3]), (12, T_[key][4]), (16, T_[key][5])]
    rows = [
        ('RA', 230, 60, 'IL *R*_{*A*}', [(0, 1, '1', 'n'), (4, 1, '1', 'n'), (12, -1, '−1', 's')]),
        ('RC', 470, 60, 'IL *R*_{*C*}', [(8, 1, '1', (-14, -10)), (12, 2, '2', 'n')]),
        ('RE', 590, 60, 'IL *R*_{*E*}', [(16, 1, '1', 'e')]),
        ('MA', 770, 20, 'IL *M*_{*A*}', [(4, 4, '4 m', 'n'), (12, -4, '−4 m', 's')]),
    ]
    for key, base, sy, nm, vals in rows:
        o += il(ax, base, sy, pts_of(key), name=nm, ticks=tk, vals=vals)
    V = K.G_VF
    vf = [(0, 0), (4, V['B']), (6, V['F-']), (6, V['F+']), (8, V['C']), (12, V['D']), (16, V['E'])]
    o += il(ax, 960, 60, vf, name='IL *V*_{*F*}', ticks=tk,
            vals=[(6, V['F-'], '−0.5', (-26, 22)), (6, V['F+'], '+0.5', (28, -8)), (12, V['D'], '−1', (26, 18))])
    for x in (4, 12):
        o += L(ax(x), yb + 14, ax(x), 1050, STEEL, 1, '3 4')
    o += T(ax(4), 1074, '鉸 B', 14, MUT, 'middle')
    o += T(ax(12), 1074, '鉸 D', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2025-2 五條影響線')


def fig2_7():
    """預告：拆一個束制後，靜定變機構（直線），靜不定還站得住（曲線）。"""
    W, H = 900, 380
    ax = Ax(150, 56)
    o = ''
    sy = 100
    y = 150
    o += T(14, 34, '(a) 簡支梁拆掉 B 的支承 → 剩一個鉸，是機構：不彎就能轉', 16, AC, 'start', 'bold')
    o += L(ax(0), y, ax(Lm), y, STEEL3, 4, '8 6') + pin(ax(0), y + 3)
    o += L(ax(0), y, ax(Lm), y - sy, AC, 5)
    o += T(ax(Lm) + 12, y - sy + 5, '1（直線）', 15, AC, 'start', 'bold')
    y = 340
    o += T(14, 214, '(b) A 改成固定端，拆掉 B 的支承 → 還是一根懸臂梁：要動 B 就得彎', 16, COMP, 'start', 'bold')
    o += L(ax(0), y, ax(Lm), y, STEEL3, 4, '8 6') + fixed_left(ax(0), y, 50)
    xs = [i * Lm / 100 for i in range(101)]
    o += P([(ax(x), y - sy * K.RC_prop(x)) for x in xs], COMP, 5)
    o += L(ax(0), y, ax(Lm), y - sy, AC, 1.4, '6 5')
    o += T(ax(Lm) + 12, y - sy + 5, '1（曲線）', 15, COMP, 'start', 'bold')
    o += C(ax(4), y - sy * K.RC_PROP_4, 4, COMP, '#fff', 1.4)
    o += T(ax(4), y - sy * K.RC_PROP_4 + 28, f'{K.RC_PROP_4:.3f}（直線會是 0.4）', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, '折線與曲線的分界')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5,
       'fig2_6': fig2_6, 'fig2_7': fig2_7}
