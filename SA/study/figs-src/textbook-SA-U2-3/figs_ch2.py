# -*- coding: utf-8 -*-
"""第 2 章：彎矩面積 → 1/3、1/6；疊加五格圖；θA 狀態 4、2、½；ψ 狀態 −6；主式解剖圖。"""
from sa_draw import *  # noqa
import math
import calcs

D2 = calcs.ch2()


def rot_wall(x, y, ang, side='left', h=50, c=INK):
    """可轉動的夾具：與桿軸切線垂直的短牆。ang＝切線方向（度，螢幕座標）。"""
    a = math.radians(ang)
    nx, ny = -math.sin(a), math.cos(a)          # 垂直切線
    tx, ty = math.cos(a), math.sin(a)
    sgn = -1 if side == 'left' else 1
    o = L(x - nx * h / 2, y - ny * h / 2, x + nx * h / 2, y + ny * h / 2, c, 3)
    for i in range(7):
        s = -h / 2 + h * i / 6
        px, py = x + nx * s, y + ny * s
        o += L(px, py, px + sgn * tx * 8 + nx * 6, py + sgn * ty * 8 + ny * 6, c, 1)
    return o


def fig2_1():
    W, H = 900, 590
    x0, y0, Lp = 140, 110, 600
    amp = 0.55                                    # 撓度放大（M L/EI 取 0.55 rad 的量級）
    fn = calcs.member_curve(float(D2['near']), -float(D2['far']))
    pts = curve_pts(x0, y0, Lp, lambda xi: amp * fn(xi), Lp)
    o = T(W / 2, 34, '(a) 簡支梁 A 端加一個順時針彎矩 *M*', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.6, '6 5')
    o += P(pts, DEF, 4)
    o += pin(x0, y0 + 2) + roller(x0 + Lp, y0 + 2)
    o += moment(x0, y0, 32, True)
    o += T(x0 - 44, y0 - 18, '*M*', 18, MOM, 'end', 'bold')
    o += T(x0 - 8, y0 + 50, 'A', 17, INK, 'end', 'bold') + T(x0 + Lp + 20, y0 + 30, 'B', 17, INK, 'start', 'bold')
    # A 端切線延伸到 B 的鉛直線
    thA = amp * float(D2['near'])
    yT = y0 + Lp * thA
    o += L(x0, y0, x0 + Lp, yT, DEF, 1.5, '3 3')
    o += L(x0 + Lp, y0, x0 + Lp, yT + 10, STEEL, 1, '2 3')
    o += A(x0 + Lp + 60, yT, x0 + Lp + 60, y0 + 2, PUR, 1.6, 8, both=True)
    o += T(x0 + Lp + 70, (y0 + yT) / 2 + 6, '*t*_{BA}', 17, PUR, 'start', 'bold')
    o += angle_arc(x0, y0, 120, 0, math.degrees(math.atan(thA)), DEF, 2.4)
    o += T(x0 + 128, y0 + 30, 'θ_{A}', 17, DEF, 'start', 'bold')
    o += T(x0 + Lp * 0.62, yT - 30, 'A 點切線', 15, DEF, 'middle')
    # B 端切線
    thB = amp * float(D2['far'])
    o += L(x0 + Lp, y0, x0 + Lp - 260, y0 + 260 * thB, DEF, 1.5, '3 3')
    o += angle_arc(x0 + Lp, y0, 90, 180, 180 - math.degrees(math.atan(thB)), DEF, 2.4)
    o += T(x0 + Lp - 100, y0 + 4, 'θ_{B}', 17, DEF, 'end', 'bold')
    # M/EI 圖
    yb, hM = 420, 110
    o += T(W / 2, 282, '(b) *M*/*EI* 圖：三角形，面積 = ½·(*M*/*EI*)·*L*', 17, INK, 'middle', 'bold')
    o += P([(x0, yb), (x0, yb - hM), (x0 + Lp, yb)], MOM, 2.4, COMP2, close=True)
    o += L(x0 - 20, yb, x0 + Lp + 20, yb, INK, 1.4)
    o += T(x0 - 10, yb - hM + 6, '*M*/*EI*', 16, MOM, 'end', 'bold')
    xc = x0 + Lp / 3
    o += C(xc, yb - hM / 3, 6, PUR, '#fff', 1.6)
    o += T(xc + 12, yb - hM / 3 - 8, '形心', 15, PUR, 'start', 'bold')
    o += dim(x0, yb + 30, xc, yb + 30, '*L*/3', INK, 0, 16)
    o += dim(xc, yb + 30, x0 + Lp, yb + 30, '2*L*/3', INK, 0, 16)
    o += R(60, 482, 780, 100, '#fff', STEEL, 1.2, 8)
    o += T(80, 512, '● *t*_{BA} = 面積 × 形心到 B = (*ML*/2*EI*)(2*L*/3) = *ML*^{2}/3*EI*  →  θ_{A} = *t*_{BA}/*L* = *ML*/3*EI*', 16, INK, 'start')
    o += T(80, 540, '● *t*_{AB} = 面積 × 形心到 A = (*ML*/2*EI*)(*L*/3) = *ML*^{2}/6*EI*  →  θ_{B} = *ML*/6*EI*（反方向）', 16, INK, 'start')
    o += T(80, 568, '近端轉 1/3、遠端轉 1/6：遠端剛好是近端的一半', 16, PUR, 'start', 'bold')
    return svg(W, H, o, '彎矩面積法求端轉角')


def fig2_2():
    W = 900
    rows = [
        ('實際的桿件', '', dict(th=(0.22, -0.10), d=0.12, load=True, walls=(None, None)), '*M*_{AB} = ?', '*M*_{BA} = ?'),
        ('① 全部鎖住', '=', dict(th=(0, 0), d=0, load=True, walls=('L', 'R')), '*M*_{F,AB}', '*M*_{F,BA}'),
        ('② 只放開 θ_{A}', '+', dict(th=(0.22, 0), d=0, load=False, walls=('rL', 'R')), '4*EI*θ_{A}/*L*', '2*EI*θ_{A}/*L*'),
        ('③ 只放開 θ_{B}', '+', dict(th=(0, 0.15), d=0, load=False, walls=('L', 'rR')), '2*EI*θ_{B}/*L*', '4*EI*θ_{B}/*L*'),
        ('④ 只放開 ψ', '+', dict(th=(0, 0), d=0.12, load=False, walls=('L', 'R')), '−6*EI*ψ/*L*', '−6*EI*ψ/*L*'),
    ]
    rh, top = 96, 64
    H = top + rh * len(rows) + 20
    x0, Lp = 230, 300
    o = T(140, 36, '狀態', 16, MUT, 'middle', 'bold')
    o += T(x0 + Lp / 2, 36, '變形（放大）', 16, MUT, 'middle', 'bold')
    o += T(660, 36, '*M*_{AB}', 17, MOM, 'middle', 'bold') + T(810, 36, '*M*_{BA}', 17, MOM, 'middle', 'bold')
    for i, (name, op, g, ma, mb) in enumerate(rows):
        yc = top + rh * i + 40
        if i == 1:
            o += L(20, yc - 50, W - 20, yc - 50, STEEL, 1.4)
        o += T(20, yc + 6, op, 26, INK, 'start', 'bold')
        o += T(140, yc + 6, name, 15, INK, 'middle', 'bold')
        thA, thB = g['th']
        fn = calcs.member_curve(thA, thB, 0, -g['d'])
        bow = (lambda xi: -0.05 * 16 * xi**2 * (1 - xi)**2) if g['load'] else (lambda xi: 0)
        pts = curve_pts(x0, yc, Lp, lambda xi: fn(xi) + bow(xi), Lp)
        o += L(x0, yc, x0 + Lp, yc, STEEL, 1.2, '5 4')
        o += P(pts, DEF, 3.4)
        if g['load']:
            o += udl(x0 + 4, x0 + Lp - 4, yc - 8, 18, 9, LOAD)
        wa, wb = g['walls']
        if wa == 'L':
            o += wall(x0, pts[0][1], 40, 'left')
        elif wa == 'rL':
            o += rot_wall(x0, pts[0][1], math.degrees(math.atan(thA)), 'left', 40)
        if wb == 'R':
            o += wall(x0 + Lp, pts[-1][1], 40, 'right')
        elif wb == 'rR':
            o += rot_wall(x0 + Lp, pts[-1][1], math.degrees(math.atan(thB)), 'right', 40)
        if i == 0:
            o += joint(x0, yc) + joint(x0 + Lp, pts[-1][1])
        o += T(660, yc + 6, ma, 16, MOM if i else MUT, 'middle', 'bold')
        o += T(810, yc + 6, mb, 16, MOM if i else MUT, 'middle', 'bold')
    return svg(W, int(H), o, '疊加：鎖住加放開')


def fig2_3():
    W, H = 900, 470
    x0, y0, Lp = 150, 120, 560
    th = 0.30
    fn = calcs.member_curve(th, 0)
    pts = curve_pts(x0, y0, Lp, fn, Lp)
    o = T(W / 2, 34, '(a) B 端鎖死，只讓 A 端順時針轉 θ_{A}', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
    o += P(pts, DEF, 4)
    o += rot_wall(x0, y0, math.degrees(math.atan(th)), 'left', 54)
    o += wall(x0 + Lp, y0, 54, 'right')
    o += angle_arc(x0, y0, 120, 0, math.degrees(math.atan(th)), DEF, 2.4)
    o += L(x0, y0, x0 + 170, y0 + 170 * th, DEF, 1.4, '3 3')
    o += T(x0 + 128, y0 + 32, 'θ_{A}', 17, DEF, 'start', 'bold')
    o += moment(x0, y0, 34, True)
    o += moment(x0 + Lp, y0, 26, True)
    o += T(x0 - 20, y0 - 50, '*M*_{A} = 4*EI*θ_{A}/*L*', 17, MOM, 'start', 'bold')
    o += T(x0 + Lp + 10, y0 - 46, '*M*_{B} = 2*EI*θ_{A}/*L*', 17, MOM, 'end', 'bold')
    o += T(x0 - 12, y0 + 64, 'A', 17, INK, 'end', 'bold') + T(x0 + Lp + 22, y0 + 50, 'B', 17, INK, 'start', 'bold')
    # 彎矩圖：A 端 +4、B 端 −2（正＝下緣受拉）
    pl = Plot(x0, 260, Lp, 150, 0, 1, -2.4, 4.4)
    yb = pl.Y(0)
    fM = lambda xi: 4 - 6 * xi
    o += T(W / 2, 246, '(b) 彎矩圖（單位 *EI*θ_{A}/*L*；正＝下緣受拉）', 17, INK, 'middle', 'bold')
    o += bmd(pl, fM)
    o += T(x0 - 10, pl.Y(4) + 6, '+4', 17, MOM, 'end', 'bold')
    o += T(x0 + Lp + 10, pl.Y(-2) + 6, '−2', 17, MOM, 'start', 'bold')
    xi0 = float(D2['k_near'] / (D2['k_near'] + D2['k_far']))
    o += C(pl.X(xi0), yb, 6, PUR, '#fff', 1.6)
    o += T(pl.X(xi0), yb - 16, '反曲點（距 A 2*L*/3）', 15, PUR, 'middle', 'bold')
    o += R(150, 428, 600, 34, KEY2, PUR, 1.4, 8)
    o += T(450, 451, '遠端得到近端的一半：傳遞係數 = 2/4 = ½', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, 'θA 狀態：4EI/L 與 2EI/L')


def fig2_4():
    W, H = 900, 470
    x0, y0, Lp = 150, 110, 560
    d = 0.14
    fn = calcs.member_curve(0, 0, 0, -d)
    pts = curve_pts(x0, y0, Lp, fn, Lp)
    yB = pts[-1][1]
    o = T(W / 2, 34, '(a) 兩端都不准轉，只讓 B 端往下移 Δ（弦順時針轉 ψ = Δ/*L*）', 17, INK, 'middle', 'bold')
    o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
    o += L(x0, y0, x0 + Lp, yB, PUR, 2, '8 5')
    o += P(pts, DEF, 4)
    o += wall(x0, y0, 54, 'left') + wall(x0 + Lp, yB, 54, 'right')
    aps = math.degrees(math.atan(d))
    o += angle_arc(x0, y0, 130, 0, aps, PUR, 2.4)
    o += T(x0 + 138, y0 + 28, 'ψ', 17, PUR, 'start', 'bold', italic=True)
    o += angle_arc(x0 + Lp, yB, 130, 180, 180 + aps, PUR, 2.4)
    o += T(x0 + Lp - 138, yB - 12, 'ψ', 17, PUR, 'end', 'bold', italic=True)
    o += moment(x0, y0, 30, False, start=35)
    o += moment(x0 + Lp, yB, 30, False, start=35)
    o += T(x0 - 16, y0 - 46, '−6*EI*ψ/*L*', 17, MOM, 'start', 'bold')
    o += T(x0 + Lp + 24, yB - 50, '−6*EI*ψ/*L*', 17, MOM, 'end', 'bold')
    o += T(x0 + Lp * 0.5, y0 + 92, '切線（水平）相對於弦，兩端都轉了 −ψ', 15, DEF, 'middle')
    o += dim(x0 + Lp + 50, y0, x0 + Lp + 50, yB, '', INK) + T(x0 + Lp + 60, (y0 + yB) / 2 + 6, 'Δ', 17, INK, 'start', italic=True)
    pl = Plot(x0, 250, Lp, 150, 0, 1, -6.6, 6.6)
    yb = pl.Y(0)
    fM = lambda xi: -6 + 12 * xi
    o += T(W / 2, 240, '(b) 彎矩圖（單位 *EI*ψ/*L*；正＝下緣受拉）', 17, INK, 'middle', 'bold')
    o += bmd(pl, fM)
    o += T(x0 - 10, pl.Y(-6) + 6, '−6', 17, MOM, 'end', 'bold')
    o += T(x0 + Lp + 10, pl.Y(6) + 6, '+6', 17, MOM, 'start', 'bold')
    o += C(pl.X(0.5), yb, 6, PUR, '#fff', 1.6)
    o += T(pl.X(0.5) + 12, yb + 24, '反曲點在中點', 15, PUR, 'start', 'bold')
    o += R(130, 428, 640, 34, KEY2, PUR, 1.4, 8)
    o += T(450, 451, '把 θ 換成 θ − ψ：−(4 + 2)ψ = −6ψ，兩端相同', 16, PUR, 'middle', 'bold')
    return svg(W, H, o, 'ψ 狀態：−6EIψ/L')


def fig2_5():
    W, H = 900, 300
    parts = [
        ('*M*_{AB}', 70, INK, None),
        ('=', 136, INK, None),
        ('2*EI*/*L*', 210, MOM, ('4*EI*/*L* 的一半', '提出來')),
        ('( 2θ_{A}', 336, DEF, ('近端轉：4', '（÷2 → 2）')),
        ('+ θ_{B}', 466, DEF, ('遠端傳來：2', '（÷2 → 1）')),
        ('− 3ψ )', 596, PUR, ('弦帶兩端轉 6', '（÷2 → 3）')),
        ('+ *M*_{F,AB}', 770, LOAD, ('鎖住時的彎矩', '（第 3 章）')),
    ]
    o = R(20, 40, 860, 70, '#fff', STEEL, 1.4, 12)
    for txt, x, c, lab in parts:
        o += T(x, 86, txt, 26, c, 'middle', 'bold')
        if lab:
            o += L(x, 100, x, 150, c, 1.6, '3 3')
            o += R(x - 64, 152, 128, 62, '#fff', c, 1.6, 8)
            o += T(x, 176, lab[0], 14, c, 'middle', 'bold')
            o += T(x, 200, lab[1], 14, INK, 'middle')
    o += T(450, 248, '種子：S2（4、2 從 1/3、1/6 算出）＋ S3（θ 換成 θ − ψ）＋ S4（鎖住＋放開）', 16, PUR, 'middle', 'bold')
    o += T(450, 278, '檢查：整根剛體轉動 θ_{A} = θ_{B} = ψ  →  2θ + θ − 3θ = 0，彎矩為零', 15, FOR, 'middle')
    return svg(W, H, o, '傾角變位式的解剖圖')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5}
