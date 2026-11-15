# -*- coding: utf-8 -*-
"""第 1 章：影響線是什麼。所有縱距由 calcs.py 算出，梁與影響線共用同一條 x 比例尺（依比例）。"""
from figs_common import *  # noqa
import calcs as K

Lm, a, b = K.L, K.a, K.b


def fig1_1():
    """彎矩圖 vs 影響線：同一根梁、同一個數字 1.2，讀在不同位置。"""
    W, H = 900, 430
    o = ''
    for side in (0, 1):
        ox = 14 + side * 446
        o += R(ox, 10, 426, 410, '#fff', GRID, 1.4, 12)
        ax = Ax(ox + 40, 34)                  # 10 m → 340 px
        yb = 120
        o += beam(ax, yb, 0, Lm, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -4), (Lm, 'B', 4)], lab_dy=-14)
        base, sy = 330, 50
        if side == 0:
            o += T(ox + 213, 40, '彎矩圖 BMD：載重固定', 17, INK, 'middle', 'bold')
            o += unit_load(ax(K.X1), yb - 2, label='*P*（不動）', h=44)
            o += L(ax(a), yb - 10, ax(a), yb + 10, KEY, 2)
            o += T(ax(a) + 6, yb + 30, '看 *s* = 6', 15, KEY, 'start', 'bold')
            pk = K.X1 * (Lm - K.X1) / Lm
            mC = K.BMD_at_C
            pts = [(0, 0), (K.X1, pk), (Lm, 0)]
            o += il(ax, base, sy, pts, c=KEY, pfill=KEY2, vals=[(K.X1, pk, f'*Pab*/*L* = {f(pk)}*P*'), (a, mC, f'{f(mC)}*P*', 'e')], ticks=(0, Lm))
            o += L(ax(a), base, ax(a), base - sy * mC, KEY, 1.2, '4 3')
            o += T(ax(Lm) + 18, base + 5, '*s*', 17, INK, 'start', 'bold')
            o += T(ox + 213, 372, '橫軸 *s* ＝「斷面」在哪', 16, KEY, 'middle', 'bold')
            o += T(ox + 213, 400, '縱座標：力×長度（kN·m）', 15, MUT, 'middle')
        else:
            o += T(ox + 213, 40, '影響線 IL：斷面固定', 17, INK, 'middle', 'bold')
            o += L(ax(a), yb - 12, ax(a), yb + 12, KEY, 3)
            o += T(ax(a), yb + 32, '斷面 C（不動）', 15, KEY, 'middle', 'bold')
            o += unit_load(ax(K.X1), yb - 2, label='1（到處跑）', h=44)
            o += A(ax(K.X1) - 12, yb - 24, ax(K.X1) - 52, yb - 24, COMP, 1.8, 9)
            o += A(ax(K.X1) + 12, yb - 24, ax(K.X1) + 52, yb - 24, COMP, 1.8, 9)
            pts = [(0, 0), (a, K.MC_PEAK), (Lm, 0)]
            o += il(ax, base, sy, pts, vals=[(a, K.MC_PEAK, f'*ab*/*L* = {f(K.MC_PEAK)} m'), (K.X1, K.MC_ss(K.X1), f'{f(K.MC_ss(K.X1))} m', 'w')], ticks=(0, Lm))
            o += L(ax(K.X1), base, ax(K.X1), base - sy * K.MC_ss(K.X1), AC, 1.2, '4 3')
            o += T(ax(Lm) + 18, base + 5, '*x*', 17, INK, 'start', 'bold')
            o += T(ox + 213, 372, '橫軸 *x* ＝「單位載重」在哪', 16, AC, 'middle', 'bold')
            o += T(ox + 213, 400, '縱座標：長度（m）＝每單位載重的彎矩', 15, MUT, 'middle')
    return svg(W, H, o, '彎矩圖與影響線的差別')


def fig1_2():
    """反力影響線：對 B 取矩。"""
    W, H = 900, 520
    ax = Ax(150, 56)
    o = ''
    yb = 90
    x = K.X1
    o += beam(ax, yb, 0, Lm, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', 16)])
    o += unit_load(ax(x), yb - 3)
    o += up_arrow(ax(0) - 30, yb + 2, label='*R*_{*A*}', h=46)
    o += up_arrow(ax(Lm) + 30, yb + 2, label='*R*_{*B*}', h=46)
    o += dim(ax(0), yb + 96, ax(x), yb + 96, '*x*', MUT, size=16, side=1)
    o += dim(ax(x), yb + 96, ax(Lm), yb + 96, '*L* − *x*', MUT, size=16, side=1)
    o += C(ax(Lm), yb, 9, 'none', KEY, 2.4)
    o += T(ax(Lm) + 52, yb - 30, '對 B 取矩：', 15, KEY, 'start', 'bold')
    o += T(ax(Lm) + 52, yb - 8, '*R*_{*B*} 力臂 0', 15, KEY, 'start', 'bold')
    # IL
    o += il(ax, 340, 70, [(0, 1), (Lm, 0)], vals=[(0, 1, '1', 'w'), (x, K.RA_ss(x), f'{f(K.RA_ss(x))}', (24, -12))], ticks=(0, x, Lm),
            name='IL *R*_{*A*}')
    o += il(ax, 470, 70, [(0, 0), (Lm, 1)], c=TEN, pfill=TEN2, vals=[(Lm, 1, '1', 'e'), (x, K.RB_ss(x), f'{f(K.RB_ss(x))}', (-22, -12))], ticks=(0, x, Lm),
            name='IL *R*_{*B*}')
    o += L(ax(x), yb + 4, ax(x), 482, COMP, 1.2, '5 4')
    o += T(ax(Lm) + 40, 340, '直線：', 15, INK, 'start', 'bold')
    o += T(ax(Lm) + 40, 364, '1 → 0', 15, AC, 'start', 'bold')
    o += T(ax(Lm) + 40, 470, '兩條相加', 15, INK, 'start', 'bold')
    o += T(ax(Lm) + 40, 494, '處處 = 1', 15, TEN, 'start', 'bold')
    return svg(W, H, o, '反力影響線')


def fig1_3():
    """剪力影響線：載重在切口左／右，各取不含載重的那一塊。"""
    W, H = 900, 560
    ax = Ax(150, 56)
    o = ''
    rows = [(96, 3.0, '(a) 載重在 C 左邊：取右段', '*V*_{*C*} = −*R*_{*B*} = −*x*/*L*'),
            (250, 8.0, '(b) 載重在 C 右邊：取左段', '*V*_{*C*} = +*R*_{*A*} = 1 − *x*/*L*')]
    for yb, x, title, eq in rows:
        o += T(14, yb - 52, title, 16, INK, 'start', 'bold')
        keep_right = x < a
        # 被丟掉的那段淡色、保留的那段深色
        o += L(ax(0), yb, ax(a), yb, INK if not keep_right else STEEL3, 5)
        o += L(ax(a), yb, ax(Lm), yb, INK if keep_right else STEEL3, 5)
        o += pin(ax(0), yb + 3, INK if not keep_right else STEEL3)
        o += roller(ax(Lm), yb + 3, INK if keep_right else STEEL3)
        o += L(ax(a), yb - 26, ax(a), yb + 26, KEY, 1.6, '5 4')
        o += T(ax(a), yb - 32, 'C', 16, KEY, 'middle', 'bold')
        o += unit_load(ax(x), yb - 3, c=COMP if not keep_right else COMPM)
        if keep_right:
            o += up_arrow(ax(Lm) + 30, yb + 2, label='*R*_{*B*}', h=46)
            o += A(ax(a) + 12, yb + 30, ax(a) + 12, yb + 4, WARN, 2.6, 11)    # 右段左切面上的正 V：向上
            o += T(ax(a) + 22, yb + 26, '*V*', 16, WARN, 'start', 'bold')
        else:
            o += up_arrow(ax(0) - 30, yb + 2, label='*R*_{*A*}', h=46)
            o += A(ax(a) - 12, yb - 30, ax(a) - 12, yb - 4, WARN, 2.6, 11)    # 左段右切面上的正 V：向下
            o += T(ax(a) - 22, yb - 12, '*V*', 16, WARN, 'end', 'bold')
        o += T(ax(Lm) + 30, yb - 20, eq, 15, WARN, 'start', 'bold')
    # IL
    base, sy = 470, 90
    pts = [(0, 0), (a, K.VC_LEFT), (a, K.VC_RIGHT), (Lm, 0)]
    o += il(ax, base, sy, pts, vals=[(a, K.VC_LEFT, f'{f(K.VC_LEFT)}', (-30, 26)), (a, K.VC_RIGHT, f'+{f(K.VC_RIGHT)}', (32, -10))], ticks=(0, a, Lm),
            name='IL *V*_{*C*}')
    # 延長線顯示兩段平行
    o += L(ax(a), base - sy * K.VC_LEFT, ax(Lm), base - sy * (K.VC_LEFT - (Lm - a) / Lm), AC, 1.3, '5 4')
    o += L(ax(0), base - sy * 1.0, ax(a), base - sy * K.VC_RIGHT, AC, 1.3, '5 4')
    o += T(ax(0) + 6, base - sy * 1.0 - 8, '1', 15, AC, 'start', 'bold')
    o += A(ax(a) + 70, base - sy * K.VC_LEFT, ax(a) + 70, base - sy * K.VC_RIGHT, KEY, 2, 9, both=True)
    o += T(ax(a) + 80, base - sy * (K.VC_LEFT + K.VC_RIGHT) / 2 + 5, '跳 1', 16, KEY, 'start', 'bold')
    o += T(ax(Lm) + 30, base - 30, '兩段平行', 15, INK, 'start', 'bold')
    o += T(ax(Lm) + 30, base - 6, '（斜率都是 −1/*L*）', 15, INK, 'start')
    return svg(W, H, o, '剪力影響線')


def fig1_4():
    """彎矩影響線：兩條延長線交叉法。"""
    W, H = 900, 450
    ax = Ax(150, 56)
    o = ''
    yb = 70
    o += beam(ax, yb, 0, Lm, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', 16)])
    o += L(ax(a), yb - 12, ax(a), yb + 12, KEY, 3)
    o += T(ax(a), yb - 18, 'C', 16, KEY, 'middle', 'bold')
    o += dim(ax(0), yb + 44, ax(a), yb + 44, '*a* = 6', MUT, size=15)
    o += dim(ax(a), yb + 44, ax(Lm), yb + 44, '*b* = 4', MUT, size=15)
    base, sy = 420, 38
    Y = lambda v: base - sy * v
    o += L(ax(0) - 10, base, ax(Lm) + 14, base, MUT, 1.3)
    # 兩條延長線
    o += L(ax(0), Y(0), ax(Lm), Y(b), TEN, 1.6, '7 5')
    o += L(ax(Lm), Y(0), ax(0), Y(a), WARN, 1.6, '7 5')
    o += L(ax(0), Y(0), ax(0), Y(a), WARN, 2.2) + L(ax(Lm), Y(0), ax(Lm), Y(b), TEN, 2.2)
    o += T(ax(0) - 10, Y(a) + 5, '*a* = 6', 16, WARN, 'end', 'bold')
    o += T(ax(Lm) + 10, Y(b) + 5, '*b* = 4', 16, TEN, 'start', 'bold')
    pts = [(0, 0), (a, K.MC_PEAK), (Lm, 0)]
    o += P([(ax(x), Y(v)) for x, v in pts] , None, fill=POS2, close=True, op=0.8)
    o += P([(ax(x), Y(v)) for x, v in pts], AC, 3)
    o += C(ax(a), Y(K.MC_PEAK), 5, AC, '#fff', 1.4)
    o += T(ax(a), Y(K.MC_PEAK) - 24, f'*ab*/*L* = {f(K.MC_PEAK)} m', 16, AC, 'middle', 'bold')
    o += T(ax(2.0), Y(0.8) - 26, '載重在 C 左：*M*_{*C*} = *R*_{*B*}·*b*', 15, TEN, 'middle', 'bold')
    o += T(ax(6.4), Y(5.6), '載重在 C 右：', 15, WARN, 'start', 'bold')
    o += T(ax(6.4), Y(5.6) + 22, '*M*_{*C*} = *R*_{*A*}·*a*', 15, WARN, 'start', 'bold')
    o += T(14, base + 5, 'IL *M*_{*C*}', 16, INK, 'start', 'bold')
    return svg(W, H, o, '彎矩影響線的交叉法')


def fig1_5():
    """例 1-1：50 kN 停在 x = 3，三條影響線各讀一次。"""
    W, H = 900, 600
    ax = Ax(150, 56)
    o = ''
    yb = 90
    x = K.X1
    o += beam(ax, yb, 0, Lm, [(0, 'pin'), (Lm, 'roller')], labels=[(0, 'A', -16), (Lm, 'B', 16)])
    o += L(ax(a), yb - 12, ax(a), yb + 12, KEY, 3)
    o += T(ax(a), yb - 18, 'C', 16, KEY, 'middle', 'bold')
    o += unit_load(ax(x), yb - 3, label=f'{f(K.P1)} kN', h=50)
    rows = [
        (240, 90, [(0, 1), (Lm, 0)], 'IL *R*_{*A*}', K.EX1['etaRA'], f"× 50 = {f(K.EX1['RA'])} kN"),
        (370, 90, [(0, 0), (a, K.VC_LEFT), (a, K.VC_RIGHT), (Lm, 0)], 'IL *V*_{*C*}', K.EX1['etaVC'], f"× 50 = {f(K.EX1['VC'])} kN"),
        (570, 40, [(0, 0), (a, K.MC_PEAK), (Lm, 0)], 'IL *M*_{*C*}', K.EX1['etaMC'], f"× 50 = {f(K.EX1['MC'])} kN·m"),
    ]
    for base, sy, pts, nm, eta, res in rows:
        o += il(ax, base, sy, pts, name=nm, ticks=(0, x, a, Lm),
                vals=[(x, eta, f'{f(eta)}', (-26, -12) if eta > 0 else (-26, 24))])
        o += T(ax(Lm) + 26, base - 8, res, 16, KEY, 'start', 'bold')
    o += L(ax(x), yb + 20, ax(x), 585, COMP, 1.4, '5 4')
    return svg(W, H, o, '例 1-1 讀影響線')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4, 'fig1_5': fig1_5}
