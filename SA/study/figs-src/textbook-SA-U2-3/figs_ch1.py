# -*- coding: utf-8 -*-
"""第 1 章：剛體運動不產生彎矩（S3）、θ 與 ψ 的定義、符號約定、SA-2017-3 未知量盤點。"""
from sa_draw import *  # noqa
import math
import calcs


def fig1_1():
    W, H = 900, 330
    o = ''
    titles = ['(a) 整根平移', '(b) 整根轉動', '(c) 切線離開了弦']
    results = [('不彎 → *M* = 0', FOR), ('不彎 → *M* = 0', FOR), ('彎了 → *M* ≠ 0', MOM)]
    Lp = 210
    for k in range(3):
        x0 = 40 + k * 300
        y0 = 120
        o += T(x0 + Lp / 2, 40, titles[k], 17, INK, 'middle', 'bold')
        o += L(x0, y0, x0 + Lp, y0, STEEL, 2.2, '6 5')
        o += T(x0 - 6, y0 - 10, 'A', 15, MUT, 'end') + T(x0 + Lp + 6, y0 - 10, 'B', 15, MUT, 'start')
        if k == 0:
            o += L(x0, y0 + 46, x0 + Lp, y0 + 46, DEF, 4)
            o += A(x0 + Lp / 2, y0 + 6, x0 + Lp / 2, y0 + 40, MUT, 1.4, 8)
            o += T(x0 + Lp / 2, 215, '切線 ∥ 弦，夾角 0', 15, DEF, 'middle')
        elif k == 1:
            a = math.radians(14)
            o += L(x0, y0, x0 + Lp * math.cos(a), y0 + Lp * math.sin(a), DEF, 4)
            o += angle_arc(x0, y0, 70, 0, 14, MUT, 1.4)
            o += T(x0 + 78, y0 + 12, 'ψ', 16, MUT, 'start', italic=True)
            o += T(x0 + Lp / 2, 215, '切線跟著弦一起轉，夾角 0', 15, DEF, 'middle')
        else:
            fn = calcs.member_curve(0.55, 0.0, 0, -0.18)
            pts = curve_pts(x0, y0, Lp, fn, Lp)
            o += P(pts, DEF, 4)
            yB = pts[-1][1]
            o += L(x0, y0, x0 + Lp, yB, PUR, 1.8, '7 5')
            o += L(x0, y0, x0 + 110, y0 + 110 * 0.55, DEF, 1.4)
            aps = math.degrees(math.atan((yB - y0) / Lp))
            ath = math.degrees(math.atan(0.55))
            o += angle_arc(x0, y0, 96, aps, ath, MOM, 3)
            o += T(x0 + 104, y0 + 40, 'θ − ψ', 16, MOM, 'start', 'bold')
            o += T(x0 + Lp - 6, yB + 26, '弦', 15, PUR, 'end')
            o += T(x0 + Lp / 2, 215, '切線和弦之間有夾角', 15, MOM, 'middle')
        o += T(x0 + Lp / 2, 262, results[k][0], 18, results[k][1], 'middle', 'bold')
    o += R(150, 284, 600, 36, KEY2, PUR, 1.4, 8)
    o += T(450, 308, '彎矩只看「切線相對於弦」轉了多少：θ − ψ', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, '剛體運動不產生彎矩')


def fig1_2():
    W, H = 900, 380
    x0, y0, Lp = 110, 110, 600
    thA, thB, d = 0.46, 0.10, 0.20
    fn = calcs.member_curve(thA, thB, 0, -d)
    pts = curve_pts(x0, y0, Lp, fn, Lp)
    xB, yB = pts[-1]
    o = L(x0 - 30, y0, x0 + Lp + 70, y0, STEEL, 1.6, '6 5')
    o += T(x0 + Lp + 74, y0 + 5, '原桿軸', 14, MUT, 'start')
    o += L(x0, y0, xB, yB, PUR, 2, '8 5')
    o += T(x0 + Lp * 0.66, y0 + Lp * 0.66 * d - 16, '弦（兩端點連線）', 15, PUR, 'middle', 'bold')
    o += P(pts, DEF, 4)
    o += T(x0 + Lp * 0.40, y0 + 150, '彈性曲線', 15, DEF, 'middle', 'bold')
    o += joint(x0, y0) + joint(xB, yB)
    o += T(x0 - 10, y0 - 10, 'A', 17, INK, 'end', 'bold') + T(xB + 2, yB + 30, 'B', 17, INK, 'middle', 'bold')
    o += C(x0 + Lp, y0, 4, '#fff', MUT, 1.2) + T(x0 + Lp + 8, y0 - 8, 'B（原位置）', 14, MUT, 'start')
    # A 端切線與角度
    o += L(x0, y0, x0 + 170, y0 + 170 * thA, DEF, 1.6)
    aT = math.degrees(math.atan(thA)); aP = math.degrees(math.atan(d))
    o += angle_arc(x0, y0, 150, 0, aT, DEF, 2.6)
    o += T(x0 + 150 * math.cos(math.radians(aT)) + 12, y0 + 150 * math.sin(math.radians(aT)) + 14, 'θ_{A}（切線）', 16, DEF, 'start', 'bold')
    o += angle_arc(x0, y0, 250, 0, aP, PUR, 2.6)
    o += T(x0 + 258, y0 - 8, 'ψ（弦）', 16, PUR, 'start', 'bold')
    # B 端切線
    o += L(xB - 130, yB - 130 * thB, xB + 110, yB + 110 * thB, DEF, 1.6)
    o += L(xB, yB, xB + 120, yB, STEEL, 1.2, '4 4')
    aB = math.degrees(math.atan(thB))
    o += angle_arc(xB, yB, 100, 0, aB, DEF, 2.6)
    o += T(xB + 108, yB + 24, 'θ_{B}', 16, DEF, 'start', 'bold')
    # Δ 尺寸
    o += dim(x0 + Lp + 46, y0, x0 + Lp + 46, yB, '', INK, 0)
    o += T(x0 + Lp + 58, (y0 + yB) / 2 + 6, 'Δ', 17, INK, 'start', italic=True)
    o += dim(x0, y0 - 46, x0 + Lp, y0 - 46, '', INK)
    o += T(x0 + Lp / 2, y0 - 54, '*L*', 17, INK, 'middle')
    o += R(110, 288, 680, 80, '#fff', STEEL, 1.2, 8)
    o += T(130, 316, '● θ：節點的「切線」轉了多少（節點轉角，每個剛節點一個）', 15, DEF, 'start')
    o += T(130, 344, '● ψ = Δ/*L*：「弦」轉了多少（弦轉角，由兩端點的相對側移決定）', 15, PUR, 'start')
    return svg(W, H, o, 'θ 與 ψ 的定義')


def fig1_3():
    W, H = 900, 420
    o = ''
    # 左：約定
    x0, y0, Lp = 60, 120, 300
    o += T(x0 + Lp / 2, 40, '(a) 約定：桿端一律順時針為正', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, INK, 5)
    o += moment(x0, y0, 30, True) + moment(x0 + Lp, y0, 30, True)
    o += T(x0, y0 + 62, '+*M*_{AB}', 17, MOM, 'middle', 'bold') + T(x0 + Lp, y0 + 62, '+*M*_{BA}', 17, MOM, 'middle', 'bold')
    o += T(x0 + 10, y0 - 40, 'A', 16, INK, 'start') + T(x0 + Lp - 10, y0 - 40, 'B', 16, INK, 'end')
    o += T(x0 + Lp / 2, y0 + 110, 'θ、ψ 也一樣：順時針為正', 16, DEF, 'middle')
    o += T(x0 + Lp / 2, y0 + 140, '→ 主式裡只剩一個減號（−3ψ）', 16, PUR, 'middle', 'bold')
    # 右：兩端固定梁受均布載重
    x1, y1, L2 = 500, 120, 320
    o += T(x1 + L2 / 2, 40, '(b) 換成彎矩圖：左端照抄、右端變號', 17, INK, 'middle', 'bold')
    o += wall(x1, y1, 60, 'left') + wall(x1 + L2, y1, 60, 'right')
    o += L(x1, y1, x1 + L2, y1, INK, 5)
    o += udl(x1 + 6, x1 + L2 - 6, y1 - 6, 22, 10, LOAD, '*w*')
    o += moment(x1 + 2, y1, 30, False, start=35) + moment(x1 + L2 - 2, y1, 30, True, start=145)
    o += T(x1 - 16, y1 + 66, '*M*_{AB} = −*wL*^{2}/12', 15, MOM, 'start', 'bold')
    o += T(x1 + L2 + 16, y1 + 66, '*M*_{BA} = +*wL*^{2}/12', 15, MOM, 'end', 'bold')
    # 彎矩圖（正彎矩＝下緣受拉，畫在基線上方為正）
    pl = Plot(x1, 245, L2, 110, 0, 1, -1 / 12, 1 / 24)
    yb = pl.Y(0)
    fn = lambda xi: -1 / 12 + xi / 2 - xi**2 / 2
    o += bmd(pl, fn)
    o += T(x1 - 8, pl.Y(-1 / 12) + 6, '−', 18, MOM, 'end', 'bold')
    o += T(x1 + L2 + 8, pl.Y(-1 / 12) + 6, '−', 18, MOM, 'start', 'bold')
    o += T(x1 + L2 / 2, pl.Y(1 / 24) - 8, '+*wL*^{2}/24', 15, MOM, 'middle')
    o += T(x1 + L2 / 2, 390, '彎矩圖（正＝下緣受拉）：兩端都是 −*wL*^{2}/12', 15, INK, 'middle')
    o += T(x1 + 30, 228, '照抄 −', 15, PUR, 'start', 'bold') + T(x1 + L2 - 30, 228, '+ 變 −', 15, PUR, 'end', 'bold')
    return svg(W, H, o, '符號約定與彎矩圖換算')


def fig1_4():
    W, H = 900, 470
    e = calcs.ex2017()
    sh = calcs.ex2017_shape()
    s = 58                               # 1 m = 58 px
    ox, oy = 150, 400                    # A 點
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    Lc, Lb = e['Lc'], e['Lb']
    o = ''
    # 變形（虛線）
    for k in ('AB', 'BC', 'DC'):
        o += P([(X(x), Y(y)) for x, y in sh[k]], DEF, 2, dash='7 5')
    # 構架
    o += L(X(0), Y(0), X(0), Y(Lc), INK, 5) + L(X(0), Y(Lc), X(Lb), Y(Lc), INK, 5) + L(X(Lb), Y(Lc), X(Lb), Y(0), INK, 5)
    o += pin(X(0), Y(0)) + pin(X(Lb), Y(0))
    o += T(X(0) - 26, Y(0) + 6, 'A', 17, INK, 'end', 'bold') + T(X(Lb) + 26, Y(0) + 6, 'D', 17, INK, 'start', 'bold')
    o += T(X(0) - 24, Y(Lc) - 26, 'B', 17, INK, 'end', 'bold') + T(X(Lb) + 24, Y(Lc) - 26, 'C', 17, INK, 'start', 'bold')
    # 載重
    o += udl(X(0) + 6, X(Lb) - 6, Y(Lc) - 4, 26, 12, LOAD, '45 kN/m')
    o += A(X(Lb) + 110, Y(Lc), X(Lb) + 8, Y(Lc), LOAD, 2.6, 12) + T(X(Lb) + 60, Y(Lc) + 24, '60 kN', 15, LOAD, 'middle', 'bold')
    o += A(X(Lb) + 110, Y(2), X(Lb) + 8, Y(2), LOAD, 2.6, 12) + T(X(Lb) + 60, Y(2) + 24, '60 kN', 15, LOAD, 'middle', 'bold')
    # 尺寸
    o += dim(X(0), Y(0) + 48, X(Lb), Y(0) + 48, '6 m', INK, 0, 15)
    o += dim(X(0) - 70, Y(0), X(0) - 70, Y(Lc), '', INK)
    o += T(X(0) - 80, Y(Lc / 2) + 5, '4 m', 15, INK, 'end')
    o += dim(X(Lb) + 150, Y(0), X(Lb) + 150, Y(2), '', INK) + T(X(Lb) + 160, Y(1) + 5, '2 m', 15, INK, 'start')
    # 未知數標記（畫在框內角落，避開載重）
    o += moment(X(0) + 34, Y(Lc) + 34, 17, True, PUR, 2.4, start=200, span=250)
    o += moment(X(Lb) - 34, Y(Lc) + 34, 17, True, PUR, 2.4, start=200, span=250)
    o += T(X(0) + 60, Y(Lc) + 42, 'θ_{B}', 17, PUR, 'start', 'bold')
    o += T(X(Lb) - 60, Y(Lc) + 42, 'θ_{C}', 17, PUR, 'end', 'bold')
    o += A(X(1.6), Y(Lc) - 66, X(0.4), Y(Lc) - 66, PUR, 2.4, 11)
    o += T(X(1.0), Y(Lc) - 76, 'Δ（ψ = Δ/4）', 16, PUR, 'middle', 'bold')
    o += T(X(0) + 16, Y(0.45), 'θ_{A}：鉸，可消去', 15, MUT, 'start')
    o += T(X(Lb) - 16, Y(0.45), 'θ_{D}：鉸，可消去', 15, MUT, 'end')
    o += T(X(Lb / 2), Y(2.2), '藍色虛線＝真正的變形', 15, DEF, 'middle')
    o += T(X(Lb / 2), Y(2.2) + 22, '（依勘誤後答案繪製，放大）', 14, DEF, 'middle')
    return svg(W, H, o, 'SA-2017-3 未知量盤點')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
