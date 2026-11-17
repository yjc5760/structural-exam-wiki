# -*- coding: utf-8 -*-
"""第 9 章：對稱／反對稱降維。鏡像規則（S5）、被對稱軸切過的梁 2EI/L 與 6EI/L、SA-2020-2、SA-2021-2、SA-2015-3。"""
from sa_draw import *  # noqa
import math
import calcs

D9 = calcs.ch9()


def fmt1(v, nd=1):
    return f'{float(v):.{nd}f}'.replace('-', '−')


def defl(p1, p2, d1, d2, th1, th2, X, Y, extra=None, n=50):
    """任意方向桿件的彈性曲線（世界座標 y 向上、m）。d＝端點位移 (u, v)，θ 順時針為正。
    extra(ξ)：桿上載重造成的額外橫向位移（沿局部法向 n＝e 逆轉 90°，m）。回傳螢幕點列。"""
    Lm = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    ex, ey = (p2[0] - p1[0]) / Lm, (p2[1] - p1[1]) / Lm
    nx, ny = -ey, ex
    v1 = d1[0] * nx + d1[1] * ny
    v2 = d2[0] * nx + d2[1] * ny
    a1 = d1[0] * ex + d1[1] * ey
    a2 = d2[0] * ex + d2[1] * ey
    pts = []
    for i in range(n + 1):
        xi = i / n
        v = calcs.hermite(xi, v1, -th1, v2, -th2, Lm)
        if extra:
            v += extra(xi)
        a = a1 + (a2 - a1) * xi
        x = p1[0] + ex * (xi * Lm + a) + nx * v
        y = p1[1] + ey * (xi * Lm + a) + ny * v
        pts.append((X(x), Y(y)))
    return pts


def frame_panel(ox, oy, s, th, D, sag=0.0):
    """門型剛架（柱高 4、梁 6，柱底固定）的變形，回傳 SVG。th＝(θB, θC)，D＝側移（m，向右）。"""
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    o = L(X(0), Y(0), X(0), Y(4), STEEL, 1.6, '6 5') + L(X(0), Y(4), X(6), Y(4), STEEL, 1.6, '6 5') + L(X(6), Y(4), X(6), Y(0), STEEL, 1.6, '6 5')
    udl_sag = (lambda xi: -sag * 16 * xi * xi * (1 - xi) ** 2) if sag else None
    o += P(defl((0, 0), (0, 4), (0, 0), (D, 0), 0, th[0], X, Y), DEF, 4)
    o += P(defl((0, 4), (6, 4), (D, 0), (D, 0), th[0], th[1], X, Y, udl_sag), DEF, 4)
    o += P(defl((6, 0), (6, 4), (0, 0), (D, 0), 0, th[1], X, Y), DEF, 4)
    o += fixed_wall(X(0), Y(0), 40) + fixed_wall(X(6), Y(0), 40)
    o += L(X(3), Y(-0.6), X(3), Y(5.2), PUR, 1.4, '3 5')
    return o


def fig9_1():
    W, H = 900, 520
    o = T(W / 2, 32, '種子 S5：對稱結構照鏡子 —— 順時針變逆時針、向右變向左', 17, INK, 'middle', 'bold')
    s = 40
    # (a) 對稱：梁受均布
    ox, oy = 90, 300
    o += frame_panel(ox, oy, s, (0.09, -0.09), 0.0, sag=0.06)
    o += udl(ox + 6, ox + 6 * s - 6, oy - 4 * s - 10, 20, 10, LOAD, '')
    o += T(ox + 3 * s, 72, '(a) 對稱載重', 17, INK, 'middle', 'bold')
    o += T(ox - 10, oy - 4 * s - 34, 'θ_{B}', 16, DEF, 'end', 'bold') + T(ox + 6 * s + 10, oy - 4 * s - 34, 'θ_{C} ＝ −θ_{B}', 16, DEF, 'start', 'bold')
    # (b) 反對稱：側推
    ox2 = 520
    D = 0.5
    o += frame_panel(ox2, oy, s, (0.6 * D / 4, 0.6 * D / 4), D)
    o += A(ox2 - 70, oy - 4 * s, ox2 - 8, oy - 4 * s, LOAD, 2.4, 11)
    o += T(ox2 + 3 * s, 72, '(b) 反對稱載重', 17, INK, 'middle', 'bold')
    o += T(ox2 - 10, oy - 4 * s - 34, 'θ_{B}', 16, DEF, 'end', 'bold') + T(ox2 + 6 * s + 10, oy - 4 * s - 34, 'θ_{C} ＝ θ_{B}', 16, DEF, 'start', 'bold')
    o += T(ox2 + 3 * s + 40, oy - 2 * s, 'Δ ≠ 0', 16, PUR, 'start', 'bold')
    o += T(ox + 3 * s + 40, oy - 2 * s, 'Δ ＝ 0', 16, PUR, 'start', 'bold')
    # 規則表
    bx, by = 40, 350
    o += R(bx, by, 820, 156, '#fff', STEEL, 1.2, 8)
    rows = [
        ('', '對稱載重', '反對稱載重'),
        ('鏡像兩點的轉角', 'θ\' ＝ −θ', 'θ\' ＝ θ'),
        ('對稱軸上的點', '不轉、不水平移動', '不垂直移動'),
        ('整體側移', '沒有（ψ_{柱} ＝ 0）', '有（要層剪力方程）'),
    ]
    xs = [bx + 30, bx + 330, bx + 590]
    for i, r in enumerate(rows):
        yy = by + 32 + i * 36
        for j, t in enumerate(r):
            o += T(xs[j], yy, t, 15 if i else 16, (PUR if i == 0 else INK), 'start', 'bold' if (i == 0 or j == 0) else None)
    return svg(W, H, o, '對稱與反對稱變形')


def fig9_2():
    W, H = 900, 470
    o = T(W / 2, 32, '被對稱軸切過的梁：另一端的 θ 已知 → 勁度從 4 變成 2 或 6', 17, INK, 'middle', 'bold')
    x0, Lp, th = 110, 300, 0.24
    rows = [
        (140, '(a) 對稱：θ_{遠} ＝ −θ　單曲率', calcs.member_curve(th, -th), '2*EI*θ/*L*', '*M* ＝ (2*EI*/*L*)(2θ − θ)'),
        (330, '(b) 反對稱：θ_{遠} ＝ +θ　S 形、跨中反曲', calcs.member_curve(th, th), '6*EI*θ/*L*', '*M* ＝ (2*EI*/*L*)(2θ + θ)'),
    ]
    for y0, ttl, fn, res, eq in rows:
        o += T(x0, y0 - 70, ttl, 16, INK, 'start', 'bold')
        o += L(x0, y0, x0 + Lp, y0, STEEL, 1.4, '6 5')
        o += P(curve_pts(x0, y0, Lp, fn, Lp * 0.9), DEF, 4)
        o += joint(x0, y0) + joint(x0 + Lp, y0)
        o += L(x0 + Lp / 2, y0 - 50, x0 + Lp / 2, y0 + 60, PUR, 1.4, '3 5')
        o += moment(x0, y0, 26, True) + T(x0 - 36, y0 + 6, res, 15, MOM, 'end', 'bold')
        o += T(x0 + Lp + 30, y0 - 6, eq, 16, INK, 'start')
        o += T(x0 + Lp + 30, y0 + 24, '→ ' + res, 16, PUR, 'start', 'bold')
    o += R(40, 400, 820, 56, KEY2, PUR, 1.4, 8)
    o += T(W / 2, 434, '只要記：主式 2(2θ_{近} + θ_{遠})，遠端代 −θ 得 2、代 +θ 得 6。對稱軸上有柱或節點 → 那一點 θ ＝ 0', 15, PUR, 'middle', 'bold')
    return svg(W, H, o, '對稱軸切過的梁')


def fig9_3():
    W, H = 900, 560
    o = T(W / 2, 32, 'SA-2020-2：左右對稱 ＋ 上下兩層一模一樣 → 只剩 θ_{b}、Δ', 17, INK, 'middle', 'bold')
    s = 30
    ox, oy = 80, 370
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    EI = 120.0
    th, Dv = float(D9['s20_t']) / EI, float(D9['s20_D']) / EI
    sagP = lambda xi: -(12 * 4 ** 3 / (48 * EI)) * ((xi * xi * (3 - 4 * xi)) if xi <= 0.5 else ((1 - xi) ** 2 * (3 - 4 * (1 - xi))))
    for yl in (0, 4):
        o += L(X(0), Y(yl), X(12), Y(yl), STEEL, 1.4, '6 5')
        o += P(defl((0, yl), (4, yl), (0, 0), (0, -Dv), 0, th, X, Y), DEF, 3.6)
        o += P(defl((4, yl), (8, yl), (0, -Dv), (0, -Dv), th, -th, X, Y, sagP), DEF, 3.6)
        o += P(defl((8, yl), (12, yl), (0, -Dv), (0, 0), -th, 0, X, Y), DEF, 3.6)
        o += wall(X(0), Y(yl), 40, 'left') + wall(X(12), Y(yl), 40, 'right')
        o += A(X(6), Y(yl) - 60, X(6), Y(yl) - 10, LOAD, 2.2, 10) + T(X(6) + 8, Y(yl) - 44, '12 kN', 14, LOAD, 'start', 'bold')
    for xc, th_ in ((4, th), (8, -th)):
        o += L(X(xc), Y(0), X(xc), Y(4), STEEL, 1.4, '6 5')
        o += P(defl((xc, 0), (xc, 4), (0, -Dv), (0, -Dv), th_, th_, X, Y), DEF, 3.6)
    for (x, y, nm, dx, dy) in ((0, 4, 'a', -26, 6), (4, 4, 'b', -10, -18), (8, 4, 'c', 10, -18), (12, 4, 'd', 26, 6),
                               (0, 0, 'e', -26, 6), (4, 0, 'f', -10, 30), (8, 0, 'g', 10, 30), (12, 0, 'h', 26, 6)):
        o += T(X(x) + dx, Y(y) + dy, nm, 16, INK, 'middle', 'bold')
    o += L(X(6), Y(-0.8), X(6), Y(5.2), PUR, 1.4, '3 5')
    o += T(X(6), Y(-0.8) + 20, '對稱軸', 14, PUR, 'middle', 'bold')
    o += dim(X(0), Y(0) + 70, X(4), Y(0) + 70, '4', MUT, 0, 14) + dim(X(4), Y(0) + 70, X(8), Y(0) + 70, '4', MUT, 0, 14) + dim(X(8), Y(0) + 70, X(12), Y(0) + 70, '4', MUT, 0, 14)
    bx = 480
    o += R(bx, 64, 400, 470, '#fff', STEEL, 1.2, 9)
    lines = [
        ('● 左右對稱：θ_{c} ＝ −θ_{b}；b、c 同沉 Δ；沒有水平側移', INK, 15, False),
        ('● 兩層一模一樣：猜 θ_{f} ＝ θ_{b}、*v*_{f} ＝ *v*_{b}', INK, 15, False),
        ('　→ 柱 bf 兩端同沉：ψ ＝ 0、軸力 ＝ 0', INK, 15, False),
        ('　→ 代回下層的方程，和上層完全一樣 ✔', INK, 15, False),
        ('● 未知數：6 個 → θ_{b}、Δ 兩個', PUR, 15, True),
        ('', INK, 6, False),
        ('*M*_{bc} ＝ ½*EI*(2θ_{b} − θ_{b}) − 6　（2*EI*/*L*）', INK, 15, False),
        ('*M*_{bf} ＝ ½*EI*(2θ_{b} + θ_{b}) ＝ 1.5*EI*θ_{b}　（6*EI*/*L*）', INK, 15, False),
        ('節點 b 轉：3*EI*θ_{b} − 0.375*EI*Δ ＝ 6', PUR, 15, True),
        ('節點 b 垂直：(*M*_{ab}+*M*_{ba})/4 + 6 ＝ 0', PUR, 15, True),
        ('　（bc 兩端彎矩反號 → 剪力就是 *V*_{0} ＝ 6）', MUT, 14, False),
        ('', INK, 6, False),
        (f'*EI*θ_{{b}} ＝ {int(D9["s20_t"])}、*EI*Δ ＝ {int(D9["s20_D"])}', MOM, 15, True),
        (f'θ_{{b}} ＝ 4.0×10^{{−4}} rad（順）、Δ ＝ {fmt1(D9["s20_v_mm"], 2)} mm（下）', MOM, 15, True),
        (f'*M*_{{ab}} ＝ {fmt1(D9["s20_Mab"], 0)}、*M*_{{ba}} ＝ {fmt1(D9["s20_Mba"], 0)} kN·m', MOM, 15, True),
    ]
    yy = 94
    for txt, c, sz, b in lines:
        if txt:
            o += T(bx + 14, yy, txt, sz, c, 'start', 'bold' if b else None)
        yy += 31 if txt else 8
    return svg(W, H, o, 'SA-2020-2 雙重對稱')


def fig9_4():
    W, H = 900, 490
    o = T(W / 2, 32, 'SA-2021-2：水平力沿不伸縮的梁可以平移 → 拆成兩邊各 12，變成反對稱', 17, INK, 'middle', 'bold')
    s = 38
    ox, oy = 110, 260
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    EI = 200.0
    th, ph, ps = (float(D9[k]) / EI for k in ('s21_t', 's21_p', 's21_s'))
    Dh = 3 * ps
    tha = -th / 2
    o += L(X(0), Y(3), X(12), Y(3), STEEL, 1.4, '6 5') + L(X(3), Y(0), X(9), Y(0), STEEL, 1.4, '6 5')
    o += L(X(3), Y(0), X(3), Y(3), STEEL, 1.4, '6 5') + L(X(9), Y(0), X(9), Y(3), STEEL, 1.4, '6 5')
    o += P(defl((0, 3), (3, 3), (Dh, 0), (Dh, 0), tha, th, X, Y), DEF, 3.6)
    o += P(defl((3, 3), (9, 3), (Dh, 0), (Dh, 0), th, th, X, Y), DEF, 3.6)
    o += P(defl((9, 3), (12, 3), (Dh, 0), (Dh, 0), th, tha, X, Y), DEF, 3.6)
    o += P(defl((3, 0), (3, 3), (0, 0), (Dh, 0), ph, th, X, Y), DEF, 3.6)
    o += P(defl((9, 0), (9, 3), (0, 0), (Dh, 0), ph, th, X, Y), DEF, 3.6)
    o += P(defl((3, 0), (9, 0), (0, 0), (0, 0), ph, ph, X, Y), DEF, 3.6)
    o += roller(X(0), Y(3) + 2) + roller(X(12), Y(3) + 2) + pin(X(3), Y(0) + 2) + roller(X(9), Y(0) + 2)
    o += A(X(12) + 8, Y(3), X(12) + 88, Y(3), LOAD, 2.6, 12) + T(X(12) + 50, Y(3) - 12, '24 kN', 15, LOAD, 'middle', 'bold')
    for (x, y, nm, dx, dy) in ((0, 3, 'a', -18, -10), (3, 3, 'b', -14, -14), (9, 3, 'e', 14, -14), (12, 3, 'f', 0, -16),
                               (3, 0, 'c', -22, 6), (9, 0, 'd', 24, 6)):
        o += T(X(x) + dx, Y(y) + dy, nm, 16, INK, 'middle', 'bold')
    o += L(X(6), Y(-1), X(6), Y(4.3), PUR, 1.4, '3 5')
    o += T(X(6), Y(1.6), '反對稱軸', 14, PUR, 'middle', 'bold')
    o += T(X(3) - 14, Y(0.5), 'φ', 16, DEF, 'end', 'bold') + T(X(3) - 14, Y(2.5), 'θ', 16, DEF, 'end', 'bold')
    o += T(X(9) + 14, Y(0.5), 'φ', 16, DEF, 'start', 'bold') + T(X(9) + 14, Y(2.5), 'θ', 16, DEF, 'start', 'bold')
    bx, by = 40, 310
    o += R(bx, by, 820, 166, '#fff', STEEL, 1.2, 8)
    lines = [
        ('● f 點的 24 kN ＝ a、f 各 12（梁不伸縮）；c 的水平反力同理拆到 c、d → 結構＋載重反對稱', INK, False),
        ('● θ_{b} ＝ θ_{e} ＝ θ、θ_{c} ＝ θ_{d} ＝ φ、兩柱 ψ ＝ Δ/3；梁 be、cd 被軸切過 → 6*EI*/*L*（2*EI*/6 × 3）', INK, False),
        ('● 三條方程：節點 b、節點 c、層剪力（每根柱 *M*_{bc}+*M*_{cb} ＝ −24×3/2 ＝ −36）', PUR, True),
        (f'● *EI*θ ＝ {int(D9["s21_t"])}、*EI*φ ＝ {int(D9["s21_p"])}、*EI*ψ ＝ {int(D9["s21_s"])} → θ_{{b}} ＝ 5.0×10^{{−4}} rad、Δ ＝ {fmt1(D9["s21_D_mm"], 2)} mm（右）', MOM, True),
        (f'● *M*_{{bc}} ＝ {fmt1(D9["s21_Mbc"], 0)}、*M*_{{cb}} ＝ {fmt1(D9["s21_Mcb"], 0)}（柱底由 cd 梁提供，框角剛接；2026-11-08 勘誤）', MOM, True),
    ]
    for i, (txt, c, b) in enumerate(lines):
        o += T(bx + 14, by + 30 + i * 31, txt, 15, c, 'start', 'bold' if b else None)
    return svg(W, H, o, 'SA-2021-2 反對稱')


def fig9_5():
    W, H = 900, 640
    o = T(W / 2, 32, 'SA-2015-3：對稱於中柱 → θ_{D} ＝ 0、沒有側移、中柱零彎矩；內鉸 C 自己會沉', 17, INK, 'middle', 'bold')
    s = 50
    ox, oy = 450, 340
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    EI = 60.0
    t, dl = float(D9['s15_t']) / EI, float(D9['s15_d']) / EI
    o += L(X(-4), Y(4), X(4), Y(4), STEEL, 1.4, '6 5')
    for xc in (-4, 0, 4):
        o += L(X(xc), Y(0), X(xc), Y(4), STEEL, 1.4, '6 5') + fixed_wall(X(xc), Y(0), 40)
    # 變形：先畫左半，右半照鏡子（S5）
    psi1, psi2 = dl / 1, -dl / 3
    thC1 = (3 * psi1 - t) / 2 - (4 * 1 / 12) * 1 / (4 * EI)        # M_CB = 0（完整式＋固端彎矩）反求 C 端轉角
    thC2 = 1.5 * psi2 + 9 / (4 * EI)                              # M_CD = 0：(2EI/3)(2θ − 3ψ) − 3 = 0
    sag = lambda Lm: (lambda xi: -4 * Lm ** 4 / (24 * EI) * xi * xi * (1 - xi) ** 2)
    left = [defl((-4, 0), (-4, 4), (0, 0), (0, 0), 0, t, X, Y),
            defl((-4, 4), (-3, 4), (0, 0), (0, -dl), t, thC1, X, Y, sag(1)),
            defl((-3, 4), (0, 4), (0, -dl), (0, 0), thC2, 0, X, Y, sag(3))]
    for pts in left:
        o += P(pts, DEF, 3.6)
        o += P([(2 * X(0) - x, y) for x, y in pts], DEF, 3.6)
    o += hinge(X(-3), Y(4 - dl), INK) + hinge(X(3), Y(4 - dl), INK)
    o += udl(X(-4) + 4, X(4) - 4, Y(4) - 40, 18, 16, LOAD, '4 kN/m')
    for (x, nm, dx) in ((-4, 'B', -16), (-3, 'C', 0), (0, 'D', 14), (3, 'E', 0), (4, 'F', 16)):
        o += T(X(x) + dx, Y(4) + 34, nm, 16, INK, 'middle', 'bold')
    o += T(X(-4) - 30, Y(0) + 6, 'A', 16, INK, 'end', 'bold') + T(X(0) + 30, Y(0) + 6, 'G', 16, INK, 'start', 'bold') + T(X(4) + 30, Y(0) + 6, 'H', 16, INK, 'start', 'bold')
    o += T(X(-3), Y(4) + 58, 'δ', 16, PUR, 'middle', 'bold')
    o += T(X(0) + 14, Y(2), '*M* ＝ 0', 15, MOM, 'start', 'bold')
    # 梁彎矩圖
    pl = Plot(150, 440, 600, 150, -4, 4, -8, 3)
    MB, MD = float(-D9['s15_MBA']), float(-D9['s15_MDC'])
    def M(x):
        u = abs(x)
        if u >= 3:      # BC 段（u：3→4 對應 C→B）
            z = 4 - u   # 距 B
            return MB * (1 - z) + 4 * z * (1 - z) / 2
        z = 3 - u       # 距 D … 由 D(0) 到 C(3)
        xc = u          # 距 D
        return MD * (1 - xc / 3) + 4 * xc * (3 - xc) / 2
    o += bmd(pl, M, -4, 4)
    o += T(150, 418, '梁 B–F 彎矩圖（下緣受拉為正，kN·m）', 15, INK, 'start', 'bold')
    o += T(pl.X(-4) - 6, pl.Y(MB) + 18, fmt1(MB, 2), 14, MOM, 'end', 'bold')
    o += T(pl.X(0), pl.Y(MD) + 20, fmt1(MD, 2), 14, MOM, 'middle', 'bold')
    xm = float(3 - D9['s15_xmax'])
    o += T(pl.X(-xm), pl.Y(float(D9['s15_Mmax'])) - 10, '+' + fmt1(D9['s15_Mmax'], 2), 14, MOM, 'middle', 'bold')
    o += T(pl.X(-3), pl.Y(0) - 10, '0', 14, MOM, 'middle', 'bold') + T(pl.X(3), pl.Y(0) - 10, '0', 14, MOM, 'middle', 'bold')
    return svg(W, H, o, 'SA-2015-3 對稱與內鉸')


ALL = {'fig9_1': fig9_1, 'fig9_2': fig9_2, 'fig9_3': fig9_3, 'fig9_4': fig9_4, 'fig9_5': fig9_5}
