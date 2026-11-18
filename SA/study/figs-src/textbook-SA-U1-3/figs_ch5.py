# -*- coding: utf-8 -*-
"""第 5 章：靜不定影響線 ＝ v(x)/f_ii。曲線一律由 calcs.py 的閉合解取樣，
閉合解已在 calcs.py 內與有限元素（fe.py）逐點比對。"""
from figs_common import *  # noqa
import calcs as K

LP = K.LP
DEF = KEY


def fixR(X, y, h=50, c=INK):
    """右端固定牆。"""
    o = L(X, y - h / 2, X, y + h / 2, c, 3)
    for i in range(8):
        yy = y - h / 2 + i * h / 7
        o += L(X, yy, X + 8, yy - 7, c, 1)
    return o


def dense(fn, x1, x2, n=200, breaks=()):
    return il_curve(None, 0, 0, fn, x1, x2, n=n, breaks=breaks)


def fig5_1():
    """柔度法＋互易：三個狀態。"""
    W, H = 900, 760
    ax = Ax(150, 56)
    o = ''
    x = 4.0
    # 狀態①
    y = 110
    o += T(14, 36, '狀態①　真實的梁（A 固定、C 滾支承）：單位載重在 *x*，C 出多少力？', 16, INK, 'start', 'bold')
    o += beam(ax, y, 0, LP, [(0, 'fixL'), (LP, 'roller')], labels=[(0, 'A', 16), (LP, 'C', -16)])
    o += unit_load(ax(x), y - 3, label='1')
    o += up_arrow(ax(LP) + 30, y + 2, label='*R*_{*C*} = ?', h=46)
    # 狀態②
    y = 300
    sy = 0.30
    o += T(14, 214, '狀態②　拿掉 C 的支承（基本結構＝懸臂），同一個 1 在 *x*：C 往下掉 Δ_{*C*0}(*x*)', 16, INK, 'start', 'bold')
    o += L(ax(0), y, ax(LP), y, STEEL3, 4, '8 6') + fixed_left(ax(0), y, 50)
    def dn(xx):   # 懸臂受 x 處向下 1 的撓度（向下為正）×EI
        return xx ** 2 * (3 * x - xx) / 6 if xx <= x else x ** 2 * (3 * xx - x) / 6
    pts = [(ax(t), y + sy * dn(t)) for t in np.linspace(0, LP, 120)]
    o += P(pts, COMP, 4.5)
    o += unit_load(ax(x), y + sy * dn(x) - 3, label='1', h=40)
    d0 = dn(LP)
    o += A(ax(LP) + 26, y, ax(LP) + 26, y + sy * d0, COMP, 2, 9)
    o += T(ax(LP) + 34, y + sy * d0 / 2 + 5, 'Δ_{*C*0}(*x*)', 16, COMP, 'start', 'bold')
    # 狀態③
    y = 560
    o += T(14, 420, '狀態③　同一根懸臂，改在 C 向上推 1：整根梁彎成 *v*(*x*)，C 升 *f*_{*CC*}', 16, INK, 'start', 'bold')
    o += L(ax(0), y, ax(LP), y, STEEL3, 4, '8 6') + fixed_left(ax(0), y, 50)
    pts = [(ax(t), y - sy * K.pc_v(t)) for t in np.linspace(0, LP, 120)]
    o += P(pts, DEF, 4.5)
    o += A(ax(LP), y - sy * K.PC_F + 50, ax(LP), y - sy * K.PC_F - 2, DEF, 2.6, 11)
    o += T(ax(LP) + 10, y - sy * K.PC_F + 50, '1', 16, DEF, 'start', 'bold')
    o += T(ax(LP) + 12, y - sy * K.PC_F + 8, '*f*_{*CC*}', 16, DEF, 'start', 'bold')
    o += A(ax(x), y, ax(x), y - sy * K.pc_v(x), AC, 2, 9)
    o += T(ax(x) + 8, y - sy * K.pc_v(x) / 2 + 12, '*v*(*x*)', 16, AC, 'start', 'bold')
    o += L(ax(x), 80, ax(x), y + 10, COMP, 1, '4 4')
    o += R(40, 610, 820, 136, KEY2, KEY, 1.4, 10)
    o += T(450, 640, '諧和：C 實際不動 ⇒ *R*_{*C*}·*f*_{*CC*} ＝ Δ_{*C*0}(*x*)', 16, KEY, 'middle', 'bold')
    o += T(450, 672, '互易（種子 S4）：「在 *x* 推、量 C」＝「在 C 推、量 *x*」 ⇒ Δ_{*C*0}(*x*) ＝ *v*(*x*)', 16, INK, 'middle', 'bold')
    o += T(450, 708, '⇒　*R*_{*C*}(*x*) ＝ *v*(*x*) ／ *f*_{*CC*}', 19, KEY, 'middle', 'bold')
    o += T(450, 734, '狀態③的形狀就是影響線，只要把 C 那一點「縮放成 1」', 15, INK, 'middle')
    return svg(W, H, o, '靜不定影響線的三個狀態')


def fig5_2():
    """撐竿懸臂（SA-2003-4 的梁）：v(x) 與正規化後的 R_C 影響線。"""
    W, H = 900, 520
    ax = Ax(150, 56)
    o = ''
    yb = 64
    o += beam(ax, yb, 0, LP, [(0, 'fixL'), (LP, 'roller')], labels=[(0, 'A', 16), (5, 'B'), (LP, 'C', -16)])
    tk = (0, 2.5, 5, 7.5, 10)
    base, sy = 260, 0.42
    pts = dense(K.pc_v, 0, LP)
    o += il(ax, base, sy, pts, c=DEF, pfill=KEY2, ticks=tk, vals=[(LP, K.PC_F, '333.3/*EI*', 'e')])
    o += T(14, base - 90, '*v*(*x*)·*EI*', 16, DEF, 'start', 'bold')
    o += T(14, base - 66, '（懸臂受 C 向上 1）', 15, MUT, 'start')
    o += T(ax(3), base - 64, '*v* = *x*²(3*L* − *x*)/6*EI*', 16, DEF, 'middle', 'bold')
    base, sy = 470, 160
    pts = dense(K.pc_RC, 0, LP)
    o += L(ax(0), base, ax(LP), base - sy, AC, 1.5, '6 5')
    vals = [(xx, K.pc_RC(xx), f'{K.pc_RC(xx):.3f}'.rstrip('0'), 'n') for xx in (2.5, 5, 7.5)]
    vals += [(4, K.RC_PROP_4, '0.208', (26, 22)), (LP, 1, '1', 'e')]
    vals[2] = (7.5, K.pc_RC(7.5), '0.633', (34, 18))
    o += il(ax, base, sy, pts, ticks=tk, vals=vals, name='IL *R*_{*C*}', name_x=14)
    o += T(ax(0.4), base - sy * 0.62, '虛線：簡支梁 *x*/*L*（對照）', 15, AC, 'start')
    o += T(ax(LP) + 14, base - sy - 30, '÷ *f*_{*CC*} = 333.3/*EI*', 15, KEY, 'start', 'bold')
    return svg(W, H, o, 'R_C 影響線')


def fig5_3():
    """SA-2003-4：B 點剪力、彎矩影響線（曲線）與簡支梁對照（虛線）。"""
    W, H = 900, 690
    ax = Ax(150, 56)
    o = ''
    yb = 64
    o += beam(ax, yb, 0, LP, [(0, 'fixL'), (LP, 'roller')], labels=[(0, 'A', 16), (LP, 'C', -16)])
    o += L(ax(5), yb - 12, ax(5), yb + 12, KEY, 3) + T(ax(5), yb - 18, 'B', 16, KEY, 'middle', 'bold')
    tk = (0, 5, 10)
    # V_B
    base, sy = 260, 130
    simp = [(0, 0), (5, -0.5), (5, 0.5), (10, 0)]
    o += P([(ax(xx), base - sy * v) for xx, v in simp], STEEL, 2, dash='6 5')
    pts = dense(K.pc_VB, 0, LP, breaks=(5,))
    o += il(ax, base, sy, pts, ticks=tk, name='IL *V*_{*B*}', name_x=14,
            vals=[(5 - 1e-9, K.PC_VB[0], '−5/16', (-34, 26)), (5 + 1e-9, K.PC_VB[1], '+11/16', (40, -4))])
    o += T(ax(7.6), base - sy * 0.5 - 30, '灰虛線：簡支梁 ∓0.5', 15, MUT, 'start')
    # M_B
    base, sy = 610, 90
    simp = [(0, 0), (5, 2.5), (10, 0)]
    o += P([(ax(xx), base - sy * v) for xx, v in simp], STEEL, 2, dash='6 5')
    pts = dense(K.pc_MB, 0, LP)
    o += il(ax, base, sy, pts, ticks=tk, name='IL *M*_{*B*}', name_x=14,
            vals=[(5, K.PC_MB_PEAK, '25/16 m', (54, 14))])
    o += T(ax(5) + 14, base - sy * 2.5 + 6, '簡支 2.5 m', 15, MUT, 'start')
    o += T(ax(0) + 4, base + 28, 'A：固定端，曲線斜率 0', 15, KEY, 'start', 'bold')
    return svg(W, H, o, 'SA-2003-4 V_B、M_B 影響線')


def fig5_4():
    """SA-2016-2：剛架的基本結構、C 推 1 的變形、m_C 彎矩圖與 f_CC 組成。"""
    W, H = 900, 520
    o = ''
    # (a) 題目
    s = 170
    F = Frame(90, 330, s)
    A_, B_, C_ = F(0, 0), F(0, 1), F(1, 1)
    o += T(14, 30, '(a) 題目：A 固定、C 滾支承，柱高 *L*、梁長 *L*', 16, INK, 'start', 'bold')
    o += member(A_, B_, INK, 5) + member(B_, C_, INK, 5)
    o += fixed_bottom(A_[0], A_[1], 56) + roller(C_[0], C_[1] + 3)
    o += T(A_[0] - 16, A_[1] - 6, 'A', 16, INK, 'end', 'bold') + T(B_[0] - 14, B_[1] - 6, 'B', 16, INK, 'end', 'bold')
    o += T(C_[0] + 14, C_[1] - 8, 'C', 16, INK, 'start', 'bold')
    o += T(F(0.5, 1)[0], F(0.5, 1)[1] - 50, '移動載重在 B–C', 15, COMP, 'middle', 'bold')
    for k in range(5):
        xx = F(0.15 + 0.18 * k, 1)[0]
        o += A(xx, B_[1] - 40, xx, B_[1] - 4, COMP, 1.6, 8)
    # (b) 變形
    F2 = Frame(390, 330, s)
    o += T(380, 30, '(b) 拿掉 C、在 C 向上推 1（放大畫）', 16, INK, 'start', 'bold')
    a_, b_, c_ = F2(0, 0), F2(0, 1), F2(1, 1)
    o += P([a_, b_, c_], STEEL3, 3, dash='7 5')
    sc = 0.22
    col = [F2(-sc * 0.5 * t ** 2, t) for t in np.linspace(0, 1, 40)]
    beam_pts = [F2(-sc * 0.5 + xx * (1 - 0 * sc), 1 + sc * K.fr16_v(xx)) for xx in np.linspace(0, 1, 60)]
    o += P(col, DEF, 4.5) + P(beam_pts, DEF, 4.5)
    o += fixed_bottom(a_[0], a_[1], 56)
    o += A(c_[0] + 30, c_[1] + 2, c_[0] + 30, beam_pts[-1][1] + 2, DEF, 2.4, 10)
    o += T(c_[0] + 38, (c_[1] + beam_pts[-1][1]) / 2 + 5, '*f*_{*CC*}', 16, DEF, 'start', 'bold')
    o += A(b_[0] - 4, b_[1] + 22, col[-1][0] - 2, b_[1] + 22, COMP, 2, 9)
    o += T(b_[0] + 6, b_[1] + 44, '柱頂側移', 15, COMP, 'start', 'bold')
    o += T(F2(0.05, 0.45)[0] + 12, F2(0.05, 0.45)[1], '柱：單曲率', 15, DEF, 'start', 'bold')
    # (c) m_C 與 f_CC 組成
    o += R(40, 384, 820, 124, KEY2, KEY, 1.4, 10)
    o += T(450, 412, '*m*_{*C*}（C 向上 1）：梁段 = *L* − *x*（三角形）；柱段 = *L*（定值，力臂永遠是 *L*）', 16, INK, 'middle', 'bold')
    o += T(450, 444, '*f*_{*CC*} = ∫*m*²/*EI* = *L*³/3*EI*（梁）＋ *L*³/*EI*（柱）＝ 4*L*³/3*EI*', 17, KEY, 'middle', 'bold')
    o += T(450, 476, '柱佔 75%：漏掉柱段，*f*_{*CC*} 小 4 倍、影響線整條算錯', 16, COMP, 'middle', 'bold')
    return svg(W, H, o, 'SA-2016-2 剛架')


def fig5_5():
    """SA-2016-2：V_C 影響線（曲線）與簡支直線 x/L。"""
    W, H = 900, 400
    ax = Ax(150, 600)        # L=1 → 600 px
    o = ''
    base, sy = 330, 250
    o += L(ax(0), base, ax(1), base - sy, STEEL, 2, '6 5')
    pts = dense(K.fr16_IL, 0, 1)
    vals = [(0.25, K.FR16_TAB[0.25], '107/512 = 0.209', (-10, -14)), (0.5, K.FR16_TAB[0.5], '29/64 = 0.453', (36, 26)),
            (0.75, K.FR16_TAB[0.75], '369/512 = 0.721', (56, 24)), (1, 1, '1', 'e')]
    o += il(ax, base, sy, pts, ticks=(0, .25, .5, .75, 1), vals=vals, name='IL *V*_{*C*}', name_x=14)
    o += T(ax(0), base + 26, 'B', 15, MUT, 'middle') + T(ax(1), base + 26, 'C', 15, MUT, 'middle')
    for t, s in ((0.25, '*L*/4'), (0.5, '*L*/2'), (0.75, '3*L*/4')):
        o += T(ax(t), base + 26, s, 15, MUT, 'middle')
    o += T(ax(0.22), base - sy * 0.62, '灰虛線：B 若是鉸 → *x*/*L*', 15, MUT, 'start')
    o += T(ax(0.03), 40, '*V*_{*C*}(*x*) = (6*L*²*x* + 3*Lx*² − *x*³) / 8*L*³', 17, KEY, 'start', 'bold')
    o += T(ax(0.03), 68, '曲線恆在直線下方：剛接的 B 把載重「吸」回柱子', 15, INK, 'start')
    return svg(W, H, o, 'SA-2016-2 V_C 影響線')


def fig5_6():
    """SA-2020-3：f_bb 的兩個來源（剛體＋彎曲）。"""
    W, H = 900, 600
    ax = Ax(110, 90)        # 7 m → 630 px
    o = ''
    yb = 70
    o += T(14, 30, '(a) 題目：a 鉸、b 滾、c 內鉸、d 固定；cd 段 1.5*EI*', 16, INK, 'start', 'bold')
    o += L(ax(0), yb, ax(4), yb, INK, 5) + L(ax(4), yb, ax(7), yb, INK, 8)
    o += pin(ax(0), yb + 3) + roller(ax(2), yb + 3) + hinge(ax(4), yb, 7) + fixR(ax(7), yb)
    for x, nm in ((0, 'a'), (2, 'b'), (4, 'c'), (7, 'd')):
        o += T(ax(x) - (16 if x == 7 else 0), yb - 18, nm, 16, INK, 'middle', 'bold')
    o += dim(ax(0), yb + 44, ax(2), yb + 44, '2 m', MUT, size=15) + dim(ax(2), yb + 44, ax(4), yb + 44, '2 m', MUT, size=15)
    o += dim(ax(4), yb + 44, ax(7), yb + 44, '3 m', MUT, size=15)
    # (b) 剛體部分
    sy = 26
    base = 290
    o += T(14, 172, '(b) 拿掉 b、在 b 推上 1：ac 兩端各被往下拉 0.5 → c 的支撐（懸臂 cd）被頂起 3/*EI*', 16, INK, 'start', 'bold')
    o += L(ax(0), base, ax(7), base, STEEL3, 3, '8 6')
    rig = lambda xx: 0.75 * xx if xx <= 4 else K.v20(xx)
    o += P([(ax(t), base - sy * rig(t)) for t in np.linspace(0, 7, 141)], WARN, 3.5)
    o += T(ax(2.8), base - 8, '剛體轉動：b 升 1.5', 15, WARN, 'middle', 'bold')
    o += T(ax(4) + 10, base - sy * 3 - 8, 'c 升 3', 15, WARN, 'start', 'bold')
    o += T(ax(5.6), base + 24, '懸臂 cd：端點受 0.5 → 上翹', 15, MUT, 'middle')
    # (c) 彎曲部分＋合成
    base = 470
    o += T(14, 352, '(c) 再加上 ac 自己的彎曲（簡支 4 m、中點受 1）：b 再升 4³/48 = 4/3', 16, INK, 'start', 'bold')
    o += L(ax(0), base, ax(7), base, STEEL3, 3, '8 6')
    o += P([(ax(t), base - sy * rig(t)) for t in np.linspace(0, 7, 141)], WARN, 2, dash='6 4')
    o += P([(ax(t), base - sy * K.v20(t)) for t in np.linspace(0, 7, 141)], DEF, 4.5)
    o += A(ax(2) - 18, base, ax(2) - 18, base - sy * K.F20, DEF, 2, 9)
    o += T(ax(2) - 26, base - sy * K.F20 / 2 + 5, '*f*_{*bb*}', 16, DEF, 'end', 'bold')
    o += C(ax(4), base - sy * K.v20(4), 6.5, '#fff', DEF, 2)
    o += T(ax(4) + 12, base - sy * K.v20(4) - 10, 'c 處折一下（內鉸）', 15, DEF, 'start', 'bold')
    o += R(40, 520, 820, 66, KEY2, KEY, 1.4, 10)
    o += T(450, 548, '*f*_{*bb*}·*EI* ＝ 1.5（剛體）＋ 4/3（彎曲）＝ 17/6', 17, KEY, 'middle', 'bold')
    o += T(450, 574, '每一段的 *v*(*x*) 也是「剛體直線＋簡支彎曲」兩項相加，不必解微分方程', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2020-3 f_bb')


def fig5_7():
    """SA-2020-3：R_b 影響線，最大 19/17 > 1。"""
    W, H = 900, 420
    ax = Ax(110, 90)
    o = ''
    yb = 50
    o += L(ax(0), yb, ax(4), yb, INK, 4) + L(ax(4), yb, ax(7), yb, INK, 7)
    o += pin(ax(0), yb + 3) + roller(ax(2), yb + 3) + hinge(ax(4), yb, 6.5)
    o += fixR(ax(7), yb, 44)
    for x, nm in ((0, 'a'), (2, 'b'), (4, 'c'), (7, 'd')):
        o += T(ax(x) - (16 if x == 7 else 0), yb - 14, nm, 15, INK, 'middle', 'bold')
    base, sy = 350, 200
    o += L(ax(0), base - sy, ax(7), base - sy, STEEL, 1.2, '5 5')
    o += T(ax(7) + 8, base - sy + 5, '1', 15, MUT, 'start')
    pts = dense(K.il20, 0, 7, breaks=())
    vals = [(2, 1, '1', (-14, -12)), (3, K.IL20_MAX, '最大 19/17 = 1.118（x = 3 m）', (10, -16)),
            (4, K.IL20_C, '18/17', (34, 4))]
    o += il(ax, base, sy, pts, ticks=(0, 1, 2, 3, 4, 5, 6, 7), vals=vals, name='IL *R*_{*b*}', name_x=8)
    for x in (0, 2, 3, 4, 7):
        o += T(ax(x), base + 24, f'{x}', 14, MUT, 'middle')
    o += T(ax(5.6), base - sy * 0.5, 'cd 段：懸臂撓曲線', 15, AC, 'start', 'bold')
    return svg(W, H, o, 'SA-2020-3 R_b 影響線')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4, 'fig5_5': fig5_5,
       'fig5_6': fig5_6, 'fig5_7': fig5_7}
