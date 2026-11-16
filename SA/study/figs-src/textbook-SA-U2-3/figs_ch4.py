# -*- coding: utf-8 -*-
"""第 4 章：遠端鉸接。遠端夾死 vs 遠端鬆開（4 → 3）；修正固端彎矩＝鎖住＋放開遠端；SA-2017-3 兩根鉸底柱。"""
from sa_draw import *  # noqa
import math
import calcs
from figs_ch2 import rot_wall

D4 = calcs.ch4()
EX = calcs.ex2017()


def fig4_1():
    W, H = 900, 560
    x0, Lp, th = 140, 420, 0.28
    o = ''
    rows = [
        (130, '(a) 遠端夾死：近端轉 θ 要出 4*EI*θ/*L*，遠端被傳 2*EI*θ/*L*', calcs.member_curve(th, 0), 'fix'),
        (370, '(b) 遠端是鉸：遠端跟著轉，近端只要出 3*EI*θ/*L*', calcs.member_curve(th, -th / 2), 'pin'),
    ]
    for y0, title, fn, kind in rows:
        o += T(W / 2, y0 - 84, title, 17, INK, 'middle', 'bold')
        pts = curve_pts(x0, y0, Lp, fn, Lp)
        o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
        o += P(pts, DEF, 4)
        o += rot_wall(x0, y0, math.degrees(math.atan(th)), 'left', 50)
        o += moment(x0, y0, 32, True)
        o += angle_arc(x0, y0, 110, 0, math.degrees(math.atan(th)), DEF, 2.2)
        o += T(x0 + 118, y0 + 30, 'θ', 17, DEF, 'start', 'bold')
        o += T(x0 - 30, y0 + 6, 'A', 17, INK, 'end', 'bold')
        if kind == 'fix':
            o += wall(x0 + Lp, y0, 50, 'right') + moment(x0 + Lp, y0, 24, True)
            o += T(x0 - 12, y0 - 44, '4*EI*θ/*L*', 17, MOM, 'start', 'bold')
            o += T(x0 + Lp + 14, y0 - 40, '2*EI*θ/*L*', 17, MOM, 'end', 'bold')
            o += T(x0 + Lp + 34, y0 + 6, 'B', 17, INK, 'start', 'bold')
        else:
            o += roller(x0 + Lp, y0 + 2)
            o += T(x0 - 12, y0 - 44, '3*EI*θ/*L*', 17, MOM, 'start', 'bold')
            o += T(x0 + Lp + 4, y0 - 26, '*M*_{B} ＝ 0', 17, MOM, 'end', 'bold')
            o += T(x0 + Lp + 26, y0 + 6, 'B', 17, INK, 'start', 'bold')
            thB = th / 2
            o += L(x0 + Lp, y0, x0 + Lp - 160, y0 + 160 * thB, DEF, 1.4, '3 3')
            o += angle_arc(x0 + Lp, y0, 90, 180, 180 - math.degrees(math.atan(thB)), DEF, 2.2)
            o += T(x0 + Lp - 98, y0 + 2, 'θ/2', 16, DEF, 'end', 'bold')
    bx = 645
    o += R(bx, 200, 235, 310, KEY2, PUR, 1.6, 10)
    o += T(bx + 110, 240, '從第 2 章直接讀', 16, PUR, 'middle', 'bold')
    o += T(bx + 110, 276, '簡支梁一端加 *M*：', 15, INK, 'middle')
    o += T(bx + 110, 304, 'θ ＝ *ML*/3*EI*', 17, INK, 'middle', 'bold')
    o += T(bx + 110, 340, '移項', 15, MUT, 'middle')
    o += T(bx + 110, 376, '*M* ＝ 3*EI*θ/*L*', 18, PUR, 'middle', 'bold')
    o += T(bx + 110, 420, '遠端鬆開 → 勁度', 15, INK, 'middle')
    o += T(bx + 110, 448, '4 變 3（少 1/4）', 17, PUR, 'middle', 'bold')
    o += T(bx + 110, 486, '遠端轉 θ/2 反方向', 15, DEF, 'middle')
    return svg(W, H, o, '遠端夾死與遠端鉸接')


def fig4_2():
    W = 900
    rows = [
        ('① 兩端鎖住', '', '−1/12', '+1/12', 'lock'),
        ('② 放開 B 端', '+', '−1/24', '−1/12', 'release'),
        ('③ 相加＝修正固端彎矩', '=', '−1/8', '0', 'sum'),
    ]
    rh, top = 118, 70
    H = top + rh * len(rows) + 70
    x0, Lp = 290, 280
    o = T(130, 40, '狀態', 16, MUT, 'middle', 'bold')
    o += T(x0 + Lp / 2, 40, '變形（放大）', 16, MUT, 'middle', 'bold')
    o += T(680, 40, '*M*_{AB}', 17, MOM, 'middle', 'bold') + T(820, 40, '*M*_{BA}', 17, MOM, 'middle', 'bold')
    o += T(750, 62, '（單位 *wL*^{2}）', 15, MUT, 'middle')
    for i, (name, op, ma, mb, kind) in enumerate(rows):
        yc = top + rh * i + 58
        if i == 2:
            o += L(20, yc - 62, W - 20, yc - 62, STEEL, 1.4)
        o += T(14, yc + 6, op, 26, INK, 'start', 'bold')
        o += T(140, yc + 6, name, 15, INK, 'middle', 'bold')
        o += L(x0, yc, x0 + Lp, yc, STEEL, 1.2, '5 4')
        if kind == 'lock':
            fn = lambda xi: 0.05 * (-16) * xi**2 * (1 - xi)**2
            o += udl(x0 + 4, x0 + Lp - 4, yc - 8, 18, 9, LOAD)
            o += wall(x0, yc, 42, 'left') + wall(x0 + Lp, yc, 42, 'right')
            o += moment(x0, yc, 22, False) + moment(x0 + Lp, yc, 22, True)
        elif kind == 'release':
            fB = calcs.member_curve(0, -0.12)
            fn = lambda xi: 0.6 * fB(xi)
            o += wall(x0, yc, 42, 'left') + roller(x0 + Lp, yc + 2)
            o += moment(x0 + Lp, yc, 22, False, c=WARN) + moment(x0, yc, 22, False)
            o += T(x0 + Lp + 30, yc - 26, '−*M*_{F,BA}', 15, WARN, 'start', 'bold')
            o += T(x0 + 10, yc + 46, '傳過來一半', 15, MOM, 'start', 'bold')
        else:
            fn = lambda xi: 0.05 * (-48 / 3) * (xi**2 * (1 - xi) * (3 - 2 * xi) / 1.5) * 0.9
            o += udl(x0 + 4, x0 + Lp - 4, yc - 8, 18, 9, LOAD)
            o += wall(x0, yc, 42, 'left') + roller(x0 + Lp, yc + 2)
            o += moment(x0, yc, 22, False)
        pts = curve_pts(x0, yc, Lp, fn, Lp)
        o += P(pts, DEF, 3.4)
        col = PUR if kind == 'sum' else MOM
        o += T(680, yc + 6, ma, 18, col, 'middle', 'bold')
        o += T(820, yc + 6, mb, 18, col, 'middle', 'bold')
    yb = top + rh * len(rows) + 30
    o += T(W / 2, yb, '*M̄*_{F,AB} ＝ *M*_{F,AB} − ½*M*_{F,BA} ＝ −*wL*^{2}/12 − *wL*^{2}/24 ＝ −*wL*^{2}/8', 18, PUR, 'middle', 'bold')
    return svg(W, int(H), o, '修正固端彎矩＝鎖住＋放開遠端')


def fig4_3():
    W, H = 900, 520
    s = 62
    ox, oy = 150, 450
    A_ = (ox, oy); B_ = (ox, oy - 4 * s); C_ = (ox + 6 * s, oy - 4 * s); D_ = (ox + 6 * s, oy)
    o = T(W / 2, 34, 'SA-2017-3：兩根柱的柱底都是鉸 → 兩根柱都用 3*EI*/*L* 修正式', 17, INK, 'middle', 'bold')
    o += L(*A_, *B_, INK, 4) + L(*B_, *C_, INK, 4) + L(*D_, *C_, INK, 4)
    o += pin(*A_) + pin(*D_)
    o += hinge(*A_, MOM) + hinge(*D_, MOM)
    o += joint(*B_) + joint(*C_)
    o += udl(B_[0] + 4, C_[0] - 4, B_[1] - 6, 20, 10, LOAD, '45 kN/m')
    o += A(C_[0] + 80, C_[1], C_[0] + 6, C_[1], LOAD, 2.2, 10)
    o += T(C_[0] + 44, C_[1] - 10, '60', 15, LOAD, 'middle', 'bold')
    mid = (D_[1] + C_[1]) / 2
    o += A(D_[0] + 80, mid, D_[0] + 6, mid, LOAD, 2.2, 10)
    o += T(D_[0] + 44, mid - 10, '60', 15, LOAD, 'middle', 'bold')
    o += T(A_[0] - 22, A_[1] - 6, 'A', 17, INK, 'end', 'bold') + T(B_[0] - 14, B_[1] - 8, 'B', 17, INK, 'end', 'bold')
    o += T(C_[0] + 10, C_[1] + 26, 'C', 17, INK, 'start', 'bold') + T(D_[0] + 22, D_[1] - 6, 'D', 17, INK, 'start', 'bold')
    o += T(A_[0] + 14, A_[1] - 30, '*M*_{AB} ＝ 0', 15, MOM, 'start', 'bold')
    o += T(D_[0] - 14, D_[1] - 30, '*M*_{DC} ＝ 0', 15, MOM, 'end', 'bold')
    bx = 610
    o += R(bx, 90, 270, 400, '#fff', STEEL, 1.2, 9)
    lines = [
        ('柱 AB（無桿上載重）', INK, 15, True),
        ('*M*_{BA} ＝ (3*EI*/4)(θ_{B} − ψ)', MOM, 16, True),
        ('', INK, 10, False),
        ('柱 DC（中點 60 kN 向左）', INK, 15, True),
        ('*M*_{F,DC} ＝ +30、*M*_{F,CD} ＝ −30', LOAD, 15, False),
        ('*M̄*_{F,CD} ＝ −30 − ½(+30) ＝ −45', PUR, 15, True),
        ('*M*_{CD} ＝ (3*EI*/4)(θ_{C} − ψ) − 45', MOM, 16, True),
        ('', INK, 10, False),
        ('未知數只剩 θ_{B}、θ_{C}、ψ', TEN, 15, True),
        ('θ_{A}、θ_{D} 最後再反求', TEN, 15, False),
    ]
    yy = 124
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 16, yy, txt, sz, c, 'start', 'bold' if b else None)
        yy += 36 if txt else 14
    return svg(W, H, o, 'SA-2017-3 鉸底柱修正式')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
