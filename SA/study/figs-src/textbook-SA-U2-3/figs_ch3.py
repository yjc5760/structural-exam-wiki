# -*- coding: utf-8 -*-
"""第 3 章：固端彎矩。兩個條件（M/EI 總面積 = 0、一次矩 = 0）長出 wL²/12、PL/8、Pab²/L²；
方向判斷（鎖住後看桿件想往哪轉）；疊加（SA-2012-3）。"""
from sa_draw import *  # noqa
import math
import calcs

D3 = calcs.ch3()
EX = calcs.ex2017()


def ffix_shape(xi):
    """兩端固定梁受均布載重的撓度形狀（向上為正，最大值 1）。"""
    return -16 * xi**2 * (1 - xi)**2


def fig3_1():
    W, H = 900, 600
    x0, y0, Lp = 150, 120, 600
    o = T(W / 2, 34, '(a) 兩端夾死、只有均布載重：兩端切線都保持水平', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
    pts = curve_pts(x0, y0, Lp, lambda xi: 0.06 * ffix_shape(xi), Lp)
    o += P(pts, DEF, 4)
    o += udl(x0 + 6, x0 + Lp - 6, y0 - 10, 22, 12, LOAD)
    o += T(x0 + Lp / 2, y0 - 42, '*w*', 18, LOAD, 'middle', 'bold')
    o += wall(x0, y0, 56, 'left') + wall(x0 + Lp, y0, 56, 'right')
    o += moment(x0, y0, 30, False)
    o += moment(x0 + Lp, y0, 30, True)
    o += T(x0 - 6, y0 + 70, '*M*_{F,AB} = −*wL*^{2}/12（逆時針）', 16, MOM, 'start', 'bold')
    o += T(x0 + Lp + 6, y0 + 70, '*M*_{F,BA} = +*wL*^{2}/12（順時針）', 16, MOM, 'end', 'bold')
    o += T(x0 - 30, y0 + 6, 'A', 17, INK, 'end', 'bold') + T(x0 + Lp + 30, y0 + 6, 'B', 17, INK, 'start', 'bold')
    # (b) M/EI 圖拆成兩塊
    o += T(W / 2, 236, '(b) *M*/*EI* 圖 ＝ 簡支拋物線（＋）＋ 兩端彎矩的矩形（−）', 17, INK, 'middle', 'bold')
    m8, m12 = float(D3['udl_Mmax']), float(D3['udl_MF'])
    pl = Plot(x0, 270, Lp, 190, 0, 1, -0.1, 0.15)
    o += pl.area(lambda x: 4 * m8 * x * (1 - x), lambda x: 0, 0, 1, COMPM, 0.55)
    o += P([pl.pt(0, 0), pl.pt(0, -m12), pl.pt(1, -m12), pl.pt(1, 0)], AC, 2, ACM, close=True, op=0.55)
    o += pl.curve(lambda x: 4 * m8 * x * (1 - x), 0, 1, MOM, 2.4)
    o += L(pl.X(0) - 20, pl.Y(0), pl.X(1) + 20, pl.Y(0), INK, 1.4)
    o += T(pl.X(0.5), pl.Y(m8) - 10, '+*wL*^{2}/8', 16, MOM, 'middle', 'bold')
    o += T(pl.X(0.5), pl.Y(0.045), '面積 ＝ (2/3)(*wL*^{2}/8)·*L* ＝ *wL*^{3}/12', 16, MOM, 'middle', 'bold')
    o += T(pl.X(0.5), pl.Y(-m12 / 2) + 6, '面積 ＝ −*M*_{0}·*L*', 16, AC, 'middle', 'bold')
    o += T(pl.X(0) - 10, pl.Y(-m12) + 6, '−*M*_{0}', 16, AC, 'end', 'bold')
    o += R(110, 500, 680, 82, KEY2, PUR, 1.6, 9)
    o += T(W / 2, 532, '兩端切線都水平 → 夾角 0 → *M*/*EI* 總面積 ＝ 0（種子 S2）', 16, INK, 'middle')
    o += T(W / 2, 564, '*M*_{0}·*L* ＝ *wL*^{3}/12　⇒　*M*_{0} ＝ *wL*^{2}/12', 18, PUR, 'middle', 'bold')
    return svg(W, H, o, '均布載重固端彎矩')


def fig3_2():
    W, H = 900, 640
    x0, y0, Lp = 150, 110, 600
    a = float(D3['ecc_a'])
    o = T(W / 2, 34, '(a) 偏心集中載重 *P*，距 A 端 *a*、距 B 端 *b*（圖中 *a* = *L*/4）', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, INK, 4)
    o += wall(x0, y0, 56, 'left') + wall(x0 + Lp, y0, 56, 'right')
    xp = x0 + a * Lp
    o += A(xp, y0 - 60, xp, y0 - 4, LOAD, 2.4, 11)
    o += T(xp + 10, y0 - 46, '*P*', 18, LOAD, 'start', 'bold')
    o += dim(x0, y0 + 40, xp, y0 + 40, '*a*', INK, 0, 16)
    o += dim(xp, y0 + 40, x0 + Lp, y0 + 40, '*b*', INK, 0, 16)
    o += T(x0 - 30, y0 + 6, 'A', 17, INK, 'end', 'bold') + T(x0 + Lp + 30, y0 + 6, 'B', 17, INK, 'start', 'bold')
    MA, MB = float(D3['ecc_MA']), float(D3['ecc_MB'])
    pk = a * (1 - a)
    o += T(W / 2, 214, '(b) 簡支三角形（＋）＋ 端彎矩梯形（−）', 17, INK, 'middle', 'bold')
    pl = Plot(x0, 236, Lp, 210, 0, 1, -0.17, 0.22)
    tri = [pl.pt(0, 0), pl.pt(a, pk), pl.pt(1, 0)]
    o += P(tri, MOM, 2.4, COMPM, close=True, op=0.6)
    o += P([pl.pt(0, 0), pl.pt(0, -MA), pl.pt(1, -MB), pl.pt(1, 0)], AC, 2, ACM, close=True, op=0.55)
    o += L(pl.X(0) - 20, pl.Y(0), pl.X(1) + 20, pl.Y(0), INK, 1.4)
    o += T(pl.X(a) + 10, pl.Y(pk) - 8, '*Pab*/*L*', 16, MOM, 'start', 'bold')
    o += C(pl.X((1 + a) / 3), pl.Y(pk / 3), 6, PUR, '#fff', 1.6)
    o += T(pl.X((1 + a) / 3) + 12, pl.Y(pk / 3) + 6, '形心距 A ＝ (*L*+*a*)/3', 15, PUR, 'start', 'bold')
    o += T(pl.X(0) - 10, pl.Y(-MA) + 6, '−*M*_{A}', 16, AC, 'end', 'bold')
    o += T(pl.X(1) + 10, pl.Y(-MB) + 6, '−*M*_{B}', 16, AC, 'start', 'bold')
    o += R(70, 476, 760, 150, '#fff', STEEL, 1.2, 8)
    o += T(90, 506, '① 總面積 ＝ 0：　(*M*_{A}+*M*_{B})*L*/2 ＝ *Pab*/2　→　*M*_{A}+*M*_{B} ＝ *Pab*/*L*', 16, INK, 'start')
    o += T(90, 538, '② 對 A 的一次矩 ＝ 0（B 點切線偏移 0）：　*M*_{A}+2*M*_{B} ＝ *Pab*(*L*+*a*)/*L*^{2}', 16, INK, 'start')
    o += T(90, 574, '相減：*M*_{B} ＝ *Pa*^{2}*b*/*L*^{2}；　*M*_{A} ＝ *Pab*^{2}/*L*^{2}', 18, PUR, 'start', 'bold')
    o += T(90, 606, '載重靠近哪一端，哪一端的固端彎矩就大（*b* > *a* → *M*_{A} > *M*_{B}）', 16, TEN, 'start', 'bold')
    return svg(W, H, o, '偏心集中載重固端彎矩')


def fig3_3():
    W, H = 900, 520
    o = T(225, 34, '(a) 水平梁、載重往下', 17, INK, 'middle', 'bold')
    o += T(675, 34, '(b) SA-2017-3 右柱 DC、載重往左', 17, INK, 'middle', 'bold')
    o += L(450, 50, 450, H - 20, STEEL, 1.2, '4 4')
    # (a)
    x0, y0, Lp = 60, 220, 330
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
    pts = curve_pts(x0, y0, Lp, lambda xi: 0.12 * ffix_shape(xi), Lp)
    o += P(pts, DEF, 4)
    o += A(x0 + Lp / 2, y0 - 80, x0 + Lp / 2, y0 - 4, LOAD, 2.4, 11)
    o += T(x0 + Lp / 2 + 10, y0 - 64, '*P*', 17, LOAD, 'start', 'bold')
    o += wall(x0, y0, 50, 'left') + wall(x0 + Lp, y0, 50, 'right')
    o += moment(x0, y0, 28, False) + moment(x0 + Lp, y0, 28, True)
    o += T(x0 + 4, y0 + 72, '左端 逆時針 −', 16, MOM, 'start', 'bold')
    o += T(x0 + Lp - 4, y0 + 72, '右端 順時針 +', 16, MOM, 'end', 'bold')
    o += T(225, 340, '梁往下垂，兩端想「往內轉」', 16, INK, 'middle')
    o += T(225, 368, '夾具反過來扳住 →「左負右正」', 16, PUR, 'middle', 'bold')
    o += T(225, 412, '*M*_{F,AB} ＝ −*PL*/8、*M*_{F,BA} ＝ +*PL*/8', 16, MOM, 'middle', 'bold')
    # (b) 柱 DC：D 在下（近端寫在前）
    xc, yD, Hp = 690, 470, 330
    yC = yD - Hp
    o += L(xc, yD, xc, yC, STEEL, 1.4, '6 5')
    cpts = [(xc + 0.12 * Hp * ffix_shape(i / 60), yD - Hp * i / 60) for i in range(61)]
    o += P(cpts, DEF, 4)
    o += fixed_wall(xc, yD, 56) + fixed_wall(xc, yC, 56, top=True)
    o += A(xc + 90, yD - Hp / 2, xc + 6, yD - Hp / 2, LOAD, 2.4, 11)
    o += T(xc + 50, yD - Hp / 2 - 12, '60 kN', 16, LOAD, 'middle', 'bold')
    o += moment(xc, yD, 28, True) + moment(xc, yC, 28, False)
    o += T(xc - 40, yD + 6, 'D', 17, INK, 'end', 'bold') + T(xc - 40, yC + 6, 'C', 17, INK, 'end', 'bold')
    o += T(xc + 40, yD - 8, '*M*_{F,DC} ＝ +30', 16, MOM, 'start', 'bold')
    o += T(xc + 40, yC + 26, '*M*_{F,CD} ＝ −30', 16, MOM, 'start', 'bold')
    o += T(560, 250, '柱中間被推向左', 15, INK, 'middle')
    o += T(560, 274, 'D 端想逆時針轉', 15, INK, 'middle')
    o += T(560, 298, '夾具順時針扳住', 15, PUR, 'middle', 'bold')
    o += T(560, 322, '→ 整組反號', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, '固端彎矩方向判斷')


def fig3_4():
    W, H = 900, 560
    x0, y0, Lp = 150, 110, 600
    o = T(W / 2, 34, '(a) SA-2012-3 頂梁：跨 4*L*，距兩端 *L* 處各一個 *P*', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, INK, 4)
    o += wall(x0, y0, 56, 'left') + wall(x0 + Lp, y0, 56, 'right')
    for fr in (0.25, 0.75):
        xp = x0 + fr * Lp
        o += A(xp, y0 - 60, xp, y0 - 4, LOAD, 2.4, 11)
        o += T(xp + 10, y0 - 44, '*P*', 18, LOAD, 'start', 'bold')
    for i, lab in enumerate(['*L*', '2*L*', '*L*']):
        xa = x0 + Lp * [0, 0.25, 0.75][i]
        xb = x0 + Lp * [0.25, 0.75, 1][i]
        o += dim(xa, y0 + 40, xb, y0 + 40, lab, INK, 0, 16)
    o += T(W / 2, 214, '(b) 對稱捷徑：簡支彎矩圖是梯形，面積 3*PL*^{2}', 17, INK, 'middle', 'bold')
    pl = Plot(x0, 240, Lp, 160, 0, 4, -0.95, 1.25)
    trap = [pl.pt(0, 0), pl.pt(1, 1), pl.pt(3, 1), pl.pt(4, 0)]
    o += P(trap, MOM, 2.4, COMPM, close=True, op=0.6)
    o += P([pl.pt(0, 0), pl.pt(0, -0.75), pl.pt(4, -0.75), pl.pt(4, 0)], AC, 2, ACM, close=True, op=0.55)
    o += L(pl.X(0) - 20, pl.Y(0), pl.X(4) + 20, pl.Y(0), INK, 1.4)
    o += T(pl.X(2), pl.Y(1) - 10, '+*PL*', 16, MOM, 'middle', 'bold')
    o += T(pl.X(2), pl.Y(0.45), '面積 ＝ 3*PL*^{2}', 16, MOM, 'middle', 'bold')
    o += T(pl.X(2), pl.Y(-0.375) + 6, '−*M*_{0}·4*L*', 16, AC, 'middle', 'bold')
    o += R(70, 428, 760, 116, '#fff', STEEL, 1.2, 8)
    o += T(90, 458, '捷徑：*M*_{0} ＝ 3*PL*^{2} ÷ 4*L* ＝ 0.75*PL*', 17, PUR, 'start', 'bold')
    o += T(90, 490, '逐個疊加：*P*·*L*·(3*L*)^{2}/(4*L*)^{2} ＋ *P*·3*L*·*L*^{2}/(4*L*)^{2} ＝ (9/16 + 3/16)*PL* ＝ 0.75*PL*', 16, INK, 'start')
    o += T(90, 522, '兩種算法一致 → *M*_{F,左} ＝ −0.75*PL*、*M*_{F,右} ＝ +0.75*PL*', 16, TEN, 'start', 'bold')
    return svg(W, H, o, '疊加求固端彎矩')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
