# -*- coding: utf-8 -*-
"""第 7 章：有側移剛架。切開整層（層剪力方程）、柱側移勁度 12 與 3、短柱、SA-2017-3 收尾、SA-2022-2、SA-2024-3。"""
from sa_draw import *  # noqa
import math
import calcs

D7 = calcs.ch7()
EX = calcs.ex2017()


def fmt1(v, nd=1):
    s = f'{float(v):.{nd}f}'
    return s.replace('-', '−')


def col_curve(xb, yb, hpx, shape, dpx, n=60):
    """垂直柱：柱底 (xb, yb)、向上 hpx 像素；shape(ξ) 為水平位移（以柱頂側移為 1），dpx 為柱頂側移像素（向右為正）。"""
    return [(xb + dpx * shape(i / n), yb - hpx * i / n) for i in range(n + 1)]


FF = lambda s: 3 * s * s - 2 * s ** 3          # 兩端固定、柱頂不轉
PF = lambda s: (3 * s - s ** 3) / 2             # 柱底鉸、柱頂不轉


def fig7_1():
    W, H = 900, 560
    o = T(W / 2, 32, '切開整層：柱頂推梁的力，用柱的兩端彎矩來寫', 17, INK, 'middle', 'bold')
    # (a) 門型剛架與切口
    s = 46
    ox, oy = 110, 430
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    hh, bb = 5, 6
    o += L(X(0), Y(0), X(0), Y(hh), INK, 5) + L(X(bb), Y(0), X(bb), Y(hh), INK, 5) + L(X(0), Y(hh), X(bb), Y(hh), INK, 5)
    o += fixed_wall(X(0), Y(0), 44) + fixed_wall(X(bb), Y(0), 44)
    o += A(X(0) - 92, Y(hh), X(0) - 8, Y(hh), LOAD, 2.6, 12) + T(X(0) - 54, Y(hh) - 14, '*P*', 18, LOAD, 'middle', 'bold')
    o += L(X(-0.9), Y(hh - 0.9), X(bb + 0.9), Y(hh - 0.9), PUR, 2, '9 6')
    o += T(X(bb / 2), Y(hh - 0.9) - 12, '切開整層', 16, PUR, 'middle', 'bold')
    o += T(X(0) + 12, Y(hh / 2), '柱 1', 15, MUT, 'start') + T(X(bb) - 12, Y(hh / 2), '柱 2', 15, MUT, 'end')
    o += T(X(bb / 2), Y(0) + 40, '(a) 一層一個 Δ，一個 Δ 配一條「整層水平平衡」', 15, INK, 'middle')
    # (b) 柱的自由體
    cx, ctop, cbot = 560, 110, 400
    o += T(cx, 72, '(b) 切下一根柱（無桿上載重）', 16, INK, 'middle', 'bold')
    o += L(cx, ctop, cx, cbot, INK, 6)
    o += moment(cx, ctop + 46, 26, True) + T(cx - 36, ctop + 52, '*M*_{上}', 16, MOM, 'end', 'bold')
    o += moment(cx, cbot - 46, 26, True) + T(cx - 36, cbot - 40, '*M*_{下}', 16, MOM, 'end', 'bold')
    o += A(cx + 100, ctop, cx + 8, ctop, FOR, 2.4, 11) + T(cx + 106, ctop + 6, '*H*', 17, FOR, 'start', 'bold')
    o += A(cx - 100, cbot, cx - 8, cbot, FOR, 2.4, 11) + T(cx - 106, cbot - 12, '*H*', 17, FOR, 'end', 'bold')
    o += dim(cx + 60, cbot, cx + 60, ctop, '', MUT, 0) + T(cx + 70, (ctop + cbot) / 2 + 6, '*h*', 17, MUT, 'start', italic=True)
    o += T(cx, cbot + 40, '對柱底取矩（順時針為正）：', 15, INK, 'middle')
    o += T(cx, cbot + 66, '*M*_{上} + *M*_{下} − *H*·*h* ＝ 0', 16, INK, 'middle', 'bold')
    # (c) 結論框
    bx, by = 700, 96
    o += R(bx, by, 190, 330, KEY2, PUR, 1.6, 10)
    o += T(bx + 95, by + 30, '梁受到柱頂', 15, INK, 'middle')
    o += T(bx + 95, by + 54, '向右的推力', 15, INK, 'middle')
    o += T(bx + 95, by + 92, '(*M*_{上}+*M*_{下})/*h*', 17, PUR, 'middle', 'bold')
    o += L(bx + 20, by + 118, bx + 170, by + 118, PUR, 1, '4 4')
    o += T(bx + 95, by + 148, '整層水平平衡：', 15, INK, 'middle')
    o += T(bx + 95, by + 180, 'Σ(*M*_{上}+*M*_{下})', 16, PUR, 'middle', 'bold')
    o += T(bx + 95, by + 206, '＝ −*P*·*h*', 17, PUR, 'middle', 'bold')
    o += L(bx + 20, by + 230, bx + 170, by + 230, PUR, 1, '4 4')
    o += T(bx + 95, by + 260, '外力在別的高度：', 15, INK, 'middle')
    o += T(bx + 95, by + 290, '−Σ *P*_{x}·*y*', 17, PUR, 'middle', 'bold')
    o += T(bx + 95, by + 316, '（*y* 從柱底量）', 14, MUT, 'middle')
    o += T(cx, 515, '*H* 是梁拉柱頂的力（向左），反過來柱頂推梁 *H*（向右）；柱底反力也是 *H*（向右）', 14, MUT, 'middle')
    return svg(W, H, o, '層剪力方程')


def fig7_2():
    W, H = 900, 590
    o = T(W / 2, 32, '柱子被錯動 Δ（柱頂不轉）：剪力 ＝ 勁度 × Δ', 17, INK, 'middle', 'bold')
    hp, dp = 220, 60
    yb = 360
    cases = [
        (120, '兩端固定', FF, '6*EI*Δ/*h*^{2}', '6*EI*Δ/*h*^{2}', '12*EI*Δ/*h*^{3}', 'fix'),
        (400, '柱底鉸', PF, '3*EI*Δ/*h*^{2}', '0', '3*EI*Δ/*h*^{3}', 'pin'),
    ]
    for xb, ttl, fn, mt, mb, vv, kind in cases:
        o += T(xb + 40, 66, ttl, 17, INK, 'middle', 'bold')
        o += L(xb, yb, xb, yb - hp, STEEL, 1.4, '6 5')
        o += P(col_curve(xb, yb, hp, fn, dp), DEF, 4)
        o += L(xb + dp - 40, yb - hp, xb + dp + 40, yb - hp, INK, 6)      # 剛性梁（不轉）
        if kind == 'fix':
            o += fixed_wall(xb, yb, 50)
            o += moment(xb, yb - 4, 22, False, MOM, 2) + T(xb + 30, yb - 22, mb, 15, MOM, 'start', 'bold')
        else:
            o += pin(xb, yb)
            o += T(xb + 18, yb - 14, '*M* ＝ 0', 15, MOM, 'start', 'bold')
        o += moment(xb + dp, yb - hp + 4, 22, False, MOM, 2) + T(xb + dp + 30, yb - hp + 30, mt, 15, MOM, 'start', 'bold')
        o += A(xb + dp + 120, yb - hp, xb + dp + 46, yb - hp, FOR, 2.4, 11)
        o += T(xb + dp + 126, yb - hp + 6, vv, 16, FOR, 'start', 'bold')
        o += A(xb, yb - hp - 30, xb + dp, yb - hp - 30, PUR, 1.6, 8)
        o += T(xb + dp / 2, yb - hp - 40, 'Δ', 16, PUR, 'middle', 'bold')
    o += R(40, 410, 820, 160, '#fff', STEEL, 1.2, 8)
    o += T(60, 442, '● 主式代 θ ＝ 0、ψ ＝ Δ/*h*：*M* ＝ (2*EI*/*h*)(−3Δ/*h*) ＝ −6*EI*Δ/*h*^{2}，兩端一樣 → 剪力 2×6/*h* ＝ 12*EI*Δ/*h*^{3}', 15, INK, 'start')
    o += T(60, 474, '● 柱底鉸用修正式：*M*_{上} ＝ (3*EI*/*h*)(−Δ/*h*) ＝ −3*EI*Δ/*h*^{2}，柱底 0 → 剪力 3*EI*Δ/*h*^{3}', 15, INK, 'start')
    o += T(60, 506, '● 數字從哪來：12 ＝ 6 ＋ 6（第 2 章的 −3ψ 乘 2）；3 ＝ 3EI/L 的 3（第 4 章）', 15, INK, 'start')
    o += T(60, 542, '● 前提是「柱頂不轉」（梁比柱硬很多）。梁有彈性時，柱的勁度落在 3 和 12 之間（7.7 節）', 15, PUR, 'start', 'bold')
    return svg(W, H, o, '柱側移勁度 12 與 3')


def fig7_3():
    W, H = 900, 470
    o = T(W / 2, 32, '短柱：同一根梁、同樣的 Δ，柱長減半 → 剪力變 8 倍', 17, INK, 'middle', 'bold')
    s = 52
    ox, oy = 110, 380
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    h1, h2 = 4, 2
    dp = 34
    # 長柱（左）與短柱（右，柱底墊高 2 m）
    o += L(X(0), Y(0), X(0), Y(h1), STEEL, 1.4, '6 5') + L(X(6), Y(h1 - h2), X(6), Y(h1), STEEL, 1.4, '6 5')
    o += P(col_curve(X(0), Y(0), s * h1, FF, dp), DEF, 4)
    o += P(col_curve(X(6), Y(h1 - h2), s * h2, FF, dp), DEF, 4)
    o += L(X(0) + dp, Y(h1), X(6) + dp, Y(h1), INK, 7)
    o += fixed_wall(X(0), Y(0), 46)
    o += R(X(6) - 40, Y(h1 - h2), 80, s * (h1 - h2), STEEL2, STEEL, 1.2) + fixed_wall(X(6), Y(0), 90)
    o += T(X(6), Y(0.9), '矮牆／基礎墊高', 14, MUT, 'middle')
    o += A(X(0) - 100, Y(h1), X(0) + dp - 8, Y(h1), LOAD, 2.6, 12) + T(X(0) - 60, Y(h1) - 14, f'{int(D7["sc_V1"] + D7["sc_V2"])} kN', 15, LOAD, 'middle', 'bold')
    o += T(X(0) - 12, Y(2), '*h* ＝ 4', 15, INK, 'end', italic=True)
    o += T(X(6) - 14, Y(3), '*h* ＝ 2', 15, INK, 'end', italic=True)
    o += T(X(0) + 30, Y(h1) + 40, f'*V* ＝ {int(D7["sc_V1"])}', 16, FOR, 'start', 'bold')
    o += T(X(6) + 40, Y(h1) + 40, f'*V* ＝ {int(D7["sc_V2"])}', 16, FOR, 'start', 'bold')
    # 右：計算框
    bx = 540
    o += R(bx, 80, 340, 300, KEY2, PUR, 1.6, 10)
    lines = [
        ('梁很硬 → 兩柱 Δ 相同、柱頂不轉', INK, 15, False),
        ('*k* ＝ 12*EI*/*h*^{3}', PUR, 17, True),
        (f'長柱 12/4^{{3}} ＝ {calcs.fmt(D7["sc_k1"]).split(" ")[0]}　短柱 12/2^{{3}} ＝ {calcs.fmt(D7["sc_k2"]).split(" ")[0]}', INK, 15, False),
        (f'勁度比 ＝ 2^{{3}} ＝ {int(D7["sc_ratio"])}', PUR, 17, True),
        (f'剪力照勁度分：{int(D7["sc_V1"])} ：{int(D7["sc_V2"])}', FOR, 16, True),
        (f'柱端彎矩 6*EI*Δ/*h*^{{2}}：{int(D7["sc_M1"])} ：{int(D7["sc_M2"])}', MOM, 16, True),
        ('→ 短柱先壞（耐震的「短柱效應」）', LOAD, 15, True),
    ]
    yy = 116
    for txt, c, sz, b in lines:
        o += T(bx + 170, yy, txt, sz, c, 'middle', 'bold' if b else None)
        yy += 38
    o += T(W / 2, 450, '數字都從同一條主式來：剪力 ∝ 1/*h*^{3}，柱端彎矩 ∝ 1/*h*^{2}', 15, MUT, 'middle')
    return svg(W, H, o, '短柱效應')


def fig7_4():
    W, H = 900, 520
    o = T(W / 2, 32, 'SA-2017-3 層剪力方程：右端 ＝ −Σ（水平外力 × 距柱底高度）', 17, INK, 'middle', 'bold')
    s = 50
    ox, oy = 70, 440
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    o += L(X(0), Y(0), X(0), Y(4), INK, 5) + L(X(0), Y(4), X(6), Y(4), INK, 5) + L(X(6), Y(4), X(6), Y(0), INK, 5)
    o += pin(X(0), Y(0)) + pin(X(6), Y(0))
    o += udl(X(0) + 6, X(6) - 6, Y(4) - 4, 24, 12, LOAD, '45 kN/m')
    for y in (4, 2):
        o += A(X(6) + 100, Y(y), X(6) + 8, Y(y), LOAD, 2.6, 12)
        o += T(X(6) + 54, Y(y) - 12, '60', 15, LOAD, 'middle', 'bold')
        o += L(X(6) + 120, Y(y), X(6) + 150, Y(y), MUT, 1, '3 3')
    o += dim(X(6) + 150, Y(0), X(6) + 150, Y(2), '', MUT) + T(X(6) + 160, Y(1) + 5, '2', 15, MUT, 'start')
    o += dim(X(6) + 186, Y(0), X(6) + 186, Y(4), '', MUT) + T(X(6) + 196, Y(3) + 5, '4', 15, MUT, 'start')
    o += T(X(0) - 18, Y(4) - 10, 'B', 17, INK, 'end', 'bold') + T(X(6) - 14, Y(4) + 28, 'C', 17, INK, 'end', 'bold')
    o += T(X(0) - 22, Y(0) + 6, 'A', 17, INK, 'end', 'bold') + T(X(6) + 22, Y(0) + 6, 'D', 17, INK, 'start', 'bold')
    o += T(X(3), Y(2.4), '梁上的 45 kN/m 是垂直的，', 15, MUT, 'middle')
    o += T(X(3), Y(2.4) + 22, '不進層剪力方程', 15, MUT, 'middle')
    bx = 610
    o += R(bx, 70, 270, 400, KEY2, PUR, 1.6, 10)
    lines = [
        ('柱底同高程，兩柱同高 4 m', INK, 15, False),
        ('', INK, 6, False),
        ('Σ(*M*_{上}+*M*_{下}) ＝ −Σ *P*_{x}·*y*', PUR, 16, True),
        ('', INK, 6, False),
        ('C 點 60 ←：−60 × 4 ＝ −240', LOAD, 15, False),
        ('柱中 60 ←：−60 × 2 ＝ −120', LOAD, 15, False),
        ('', INK, 6, False),
        ('*M*_{AB}+*M*_{BA}+*M*_{DC}+*M*_{CD}', INK, 15, False),
        (f'＝ +{int(D7["s17_rhs"])}', PUR, 18, True),
        ('', INK, 6, False),
        ('鉸底 *M*_{AB} ＝ *M*_{DC} ＝ 0', INK, 15, False),
        (f'⇒ *M*_{{BA}} + *M*_{{CD}} ＝ {int(D7["s17_rhs"])}', PUR, 17, True),
    ]
    yy = 104
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 135, yy, txt, sz, c, 'middle', 'bold' if b else None)
        yy += 32 if txt else 8
    o += T(W / 2, 500, '和題解「對柱頂取矩、H_{A} + H_{D} ＝ 120」寫法不同，結果一模一樣', 15, MUT, 'middle')
    return svg(W, H, o, 'SA-2017-3 層剪力方程')


def fig7_5():
    W, H = 900, 540
    o = T(W / 2, 32, 'SA-2017-3 答案：變形（放大）與桿端彎矩（kN·m，順時針為正）', 17, INK, 'middle', 'bold')
    sh = calcs.ex2017_shape()
    s = 54
    ox, oy = 190, 430
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    o += L(X(0), Y(0), X(0), Y(4), STEEL, 2.4, '6 5') + L(X(0), Y(4), X(6), Y(4), STEEL, 2.4, '6 5') + L(X(6), Y(4), X(6), Y(0), STEEL, 2.4, '6 5')
    for k in ('AB', 'BC', 'DC'):
        o += P([(X(x), Y(y)) for x, y in sh[k]], DEF, 4)
    o += pin(X(0), Y(0)) + pin(X(6), Y(0))
    D = sh['D']
    o += A(X(3), Y(4) - 60, X(3 + D), Y(4) - 60, PUR, 2.2, 10)
    o += T(X(3 + D / 2), Y(4) - 72, f'EIΔ ＝ {fmt1(EX["EIDelta"], 0)}（向左）', 15, PUR, 'middle', 'bold')
    f2 = lambda v: fmt1(v, 2)
    o += T(X(0) - 70, Y(4) + 34, f'*M*_{{BA}} ＝ +{f2(EX["M_BA"])}', 15, MOM, 'end', 'bold')
    o += T(X(0) + 20, Y(4) + 62, f'*M*_{{BC}} ＝ {f2(EX["M_BC"])}', 15, MOM, 'start', 'bold')
    o += T(X(6) - 20, Y(4) + 62, f'*M*_{{CB}} ＝ {f2(EX["M_CB"])}', 15, MOM, 'end', 'bold')
    o += T(X(6) + 26, Y(4) + 34, f'*M*_{{CD}} ＝ +{f2(EX["M_CD"])}', 15, MOM, 'start', 'bold')
    o += T(X(0) - 40, Y(0) + 34, '*M*_{AB} ＝ 0', 15, MOM, 'end') + T(X(6) + 40, Y(0) + 34, '*M*_{DC} ＝ 0', 15, MOM, 'start')
    o += A(X(0) - 4, Y(0) - 24, X(0) + 70, Y(0) - 24, FOR, 2.2, 10)
    o += T(X(0) + 78, Y(0) - 18, f'*H*_{{A}} ＝ {fmt1(D7["s17_HA"], 2)}', 15, FOR, 'start', 'bold')
    o += A(X(6) + 4, Y(0) - 24, X(6) + 78, Y(0) - 24, FOR, 2.2, 10)
    o += T(X(6) + 86, Y(0) - 18, f'*H*_{{D}} ＝ {fmt1(D7["s17_HD"], 2)}', 15, FOR, 'start', 'bold')
    o += T(X(3), Y(1.6), f'左柱扛 {fmt1(D7["s17_HA"], 1)}、右柱扛 {fmt1(D7["s17_HD"], 1)}', 15, FOR, 'middle', 'bold')
    o += T(X(3), Y(1.6) + 24, '合計 120 ✔', 15, FOR, 'middle', 'bold')
    o += T(X(3), Y(0) + 70, '藍線＝真實變形（EI 取 3600 放大）；θ_{A}、θ_{D}、θ_{B}、θ_{C} 全部是逆時針', 15, DEF, 'middle')
    return svg(W, H, o, 'SA-2017-3 答案')


def fig7_6():
    W, H = 900, 540
    o = T(W / 2, 32, 'SA-2022-2：e 是「倒掛」在柱頂的鉸 → 兩根柱的 ψ 一正一負', 17, INK, 'middle', 'bold')
    s = 46
    ox, oy = 150, 470
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    # a(0,0) c(0,4) d(4,4) e(4,8)
    dp = 30
    o += L(X(0), Y(0), X(0), Y(4), STEEL, 1.6, '6 5') + L(X(0), Y(4), X(4), Y(4), STEEL, 1.6, '6 5') + L(X(4), Y(4), X(4), Y(8), STEEL, 1.6, '6 5')
    o += L(X(0), Y(0), X(0) + dp, Y(4), DEF, 4) + L(X(0) + dp, Y(4), X(4) + dp, Y(4), DEF, 4) + L(X(4) + dp, Y(4), X(4), Y(8), DEF, 4)
    o += pin(X(0), Y(0))
    # 倒掛鉸：三角形朝下
    xe, ye = X(4), Y(8)
    o += P([(xe, ye), (xe - 11, ye - 16), (xe + 11, ye - 16)], INK, 1.5, fill='#fff', close=True)
    o += hatch_ground(xe - 18, ye - 16, 36, INK, down=False)
    for (x, y) in ((0, 2), (4, 6)):
        o += A(X(x) - 80, Y(y), X(x) - 6, Y(y), LOAD, 2.4, 11) + T(X(x) - 50, Y(y) - 12, '30', 15, LOAD, 'middle', 'bold')
    o += T(X(0) - 18, Y(0) + 6, 'a', 17, INK, 'end', 'bold') + T(X(0) - 16, Y(4) - 8, 'c', 17, INK, 'end', 'bold')
    o += T(X(4) + 40, Y(4) + 24, 'd', 17, INK, 'start', 'bold') + T(X(4) + 22, Y(8) - 14, 'e', 17, INK, 'start', 'bold')
    o += T(X(0) + 26, Y(0.8), 'b', 16, INK, 'start', 'bold')
    o += C(X(0) + dp / 2, Y(2), 4, INK, INK)
    o += T(X(0) + 34, Y(2.6), 'ψ_{ac} ＝ +Δ/4', 15, DEF, 'start', 'bold')
    o += T(X(4) - 12, Y(7.3), 'ψ_{de} ＝ −Δ/4', 15, DEF, 'end', 'bold')
    o += A(X(2), Y(4) + 34, X(2) + dp, Y(4) + 34, PUR, 1.8, 8) + T(X(2) + dp + 8, Y(4) + 40, 'Δ', 16, PUR, 'start', 'bold')
    bx = 440
    o += R(bx, 64, 440, 450, '#fff', STEEL, 1.2, 9)
    lines = [
        ('● 柱 ac：下端 a 不動、上端 c 右移 → 弦順時針', INK, 15, False),
        ('● 柱 de：下端 d 右移、上端 e 不動 → 弦逆時針', INK, 15, False),
        ('● 兩柱頂底不同高程 → 用「剛體虛功」列側移方程：', INK, 15, False),
        ('　(*M*_{ac}+*M*_{ca})(+¼) + (*M*_{de}+*M*_{ed})(−¼)', PUR, 15, True),
        ('　　+ 30·½ + 30·½ ＝ 0', PUR, 15, True),
        (f'　⇒ *M*_{{ca}} − *M*_{{de}} ＝ {fmt1(D7["s22_rhs"], 0)}', PUR, 16, True),
        (f'● 解：*K*θ_{{c}} ＝ {int(D7["s22_x"])}、*K*θ_{{d}} ＝ {fmt1(D7["s22_y"], 0)}、*K*Δ ＝ {int(D7["s22_z"])}（*K* ＝ *EI*/4）', INK, 15, False),
        (f'● Δ_{{c}} ＝ {int(D7["s22_z"])}/10000 m ＝ {int(D7["s22_Dc_mm"])} mm（向右）', TEN, 16, True),
        (f'● 梁 cd：*M*_{{cd}} ＝ +{int(D7["s22_Mcd"])}、*M*_{{dc}} ＝ {fmt1(D7["s22_Mdc"], 0)} → 全梁定值 60', MOM, 15, True),
        ('　（下緣受拉，題解 2026-08-26 勘誤）', MOM, 14, False),
        ('● b 點 ＝ 弦帶著走 Δ/2 ＋ 柱自己彎：', INK, 15, False),
        (f'　11.5 ＋ ({int(D7["s22_el_P"])}+{int(D7["s22_el_M"])})/*EI* ＝ 11.5 ＋ 2.5 ＝ {int(D7["s22_Db_mm"])} mm', TEN, 16, True),
    ]
    yy = 96
    for txt, c, sz, b in lines:
        o += T(bx + 16, yy, txt, sz, c, 'start', 'bold' if b else None)
        yy += 35
    return svg(W, H, o, 'SA-2022-2 兩柱 ψ 反號')


def fig7_7():
    W, H = 900, 470
    o = T(W / 2, 32, 'SA-2024-3：梁的勁度決定柱頂能不能轉（*k* ＝ *L*_{b}/*L*）', 17, INK, 'middle', 'bold')
    s24 = D7['s24']
    # 左：側移勁度係數 PL/(K_cψ) 對 k
    pl = Plot(90, 90, 330, 260, 0, 6, 0, 16)
    o += pl.axes([0, 1, 2, 3, 4, 5, 6], [0, 3, 6, 9, 12, 15], '*k*', '', size=14)
    o += T(90, 72, '側移勁度（×*EI*/*L*^{3}）', 15, INK, 'start', 'bold')
    o += pl.hline(15, 0, 6, MUT, 1.2) + pl.hline(6, 0, 6, MUT, 1.2)
    o += T(pl.X(6) - 4, pl.Y(15) - 8, '梁無限硬：12＋3 ＝ 15', 14, MUT, 'end')
    o += T(pl.X(6) - 4, pl.Y(6) + 22, '梁無勁度：3＋3 ＝ 6', 14, MUT, 'end')
    o += pl.curve(lambda k: float(s24(Fr(max(k, 1e-9)).limit_denominator(10**6))['PL']), 0.001, 6, DEF, 3)
    o += pl.dot(1.5, 9, PUR, 6) + T(pl.X(1.5) + 12, pl.Y(9) - 10, '*k* ＝ 1.5 → 9', 15, PUR, 'start', 'bold')
    # 右：比值 (2k+3)/3
    pr = Plot(530, 90, 330, 260, 0, 4, 0, 4)
    o += pr.axes([0, 1, 2, 3, 4], [0, 1, 2, 3, 4], '*k*', '', size=14)
    o += T(530, 72, '柱最大／梁最大 ＝ (2*k*+3)/3', 15, INK, 'start', 'bold')
    o += pr.curve(lambda k: (2 * k + 3) / 3, 0, 4, MOM, 3)
    o += pr.curve(lambda k: (k + 3) / 3, 0, 4, STEEL, 2, dash='6 5')
    o += pr.hline(2, 0, 4, PUR, 1.4)
    o += pr.dot(1.5, 2, PUR, 6) + T(pr.X(1.5) - 10, pr.Y(2) - 14, '*k* ＝ 3/2 ✔', 15, PUR, 'end', 'bold')
    o += pr.dot(3, 2, STEEL, 5) + T(pr.X(3) + 8, pr.Y(2) + 26, '當成剛接：3 ✘', 14, MUT, 'start')
    o += T(W / 2, 400, 'C 角是內鉸：梁 C 端、柱 C 端都用 3*EI*/*L*，未知數只剩 θ_{B}、ψ；比值和 *P* 無關，不用解層剪力方程', 15, INK, 'middle')
    o += T(W / 2, 432, '極限檢查：*k* → 0 柱頂被鎖死（左柱 12、右柱 3）；*k* → ∞ 柱頂自由轉（兩柱都像懸臂 3）', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, 'SA-2024-3 勁度與比值')


from fractions import Fraction as Fr  # noqa: E402

ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4, 'fig7_5': fig7_5,
       'fig7_6': fig7_6, 'fig7_7': fig7_7}
