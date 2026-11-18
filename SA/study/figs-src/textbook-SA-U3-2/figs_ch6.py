# -*- coding: utf-8 -*-
"""第 6 章：偏心斜撐連梁轉角（SA-2023-4）。幾何、層剪力、位移、γ 全部 import calcs。"""
from figs_common import *  # noqa
import math
import numpy as np
from calcs import ex2023, ex2023_more, F23, h23, e23, L1_23, L2_23

r = ex2023()
rm = ex2023_more()
LS = L1_23 + e23 + L2_23
RIG = '#fde7d4'


def _rot(p, th, c):
    """點 p 繞 c 轉 th（數學座標，逆時針 +）。"""
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(th) - y * math.sin(th), c[1] + x * math.sin(th) + y * math.cos(th))


def _hermite(p0, p1, s0, s1, n=40):
    """局部座標 x 右 y 上的三次 Hermite 曲線（端點斜率 s0、s1＝dy/dx）。"""
    (x0, y0), (x1, y1) = p0, p1
    d = x1 - x0
    out = []
    for i in range(n + 1):
        t = i / n
        h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        out.append((x0 + d * t, h00 * y0 + h10 * d * s0 + h01 * y1 + h11 * d * s1))
    return out


def fig6_1():
    W, H = 900, 540
    o = ''
    s = 28
    x0, yb = 120, 450
    def p(x, y):
        return (x0 + s * x, yb - s * y)
    o += T(260, 34, 'SA-2023-4：三層偏心斜撐構架', 16, INK, 'middle', 'bold')
    for i in range(3):
        y0, y1 = i * h23, (i + 1) * h23
        o += P([p(0, y0), p(0, y1), p(L1_23, y1)], WARN, 1.4, fill=RIG, close=True)
        o += P([p(LS, y0), p(LS, y1), p(L1_23 + e23, y1)], WARN, 1.4, fill=RIG, close=True)
        o += L(*p(0, y0), *p(0, y1), INK, 3) + L(*p(LS, y0), *p(LS, y1), INK, 3)
        o += L(*p(0, y1), *p(L1_23, y1), INK, 3) + L(*p(L1_23 + e23, y1), *p(LS, y1), INK, 3)
        o += L(*p(0, y0), *p(L1_23, y1), INK, 2.4) + L(*p(LS, y0), *p(L1_23 + e23, y1), INK, 2.4)
        o += L(*p(L1_23, y1), *p(L1_23 + e23, y1), KEY, 6)
        X, Y = p(L1_23 + e23 / 2, y1)
        o += T(X, Y - 12, f'連梁{i + 1}', 14, KEY, 'middle', 'bold')
        Fv = F23[i] / 2
        for xx, side in ((0, -1), (LS, 1)):
            X, Y = p(xx, y1)
            if side < 0:
                o += A(X - 62, Y, X - 6, Y, COMP, 2.6, 11) + T(X - 66, Y - 8, f'{Fv:.0f}', 14, COMP, 'start', 'bold')
            else:
                o += A(X + 6, Y, X + 62, Y, COMP, 2.6, 11) + T(X + 12, Y - 8, f'{Fv:.0f}', 14, COMP, 'start', 'bold')
    o += hatch_ground(p(0, 0)[0] - 30, yb, s * LS + 60)
    o += dim(*p(0, 0), *p(L1_23, 0), '4 m', INK, off=26, size=14, lab_off=10)
    o += dim(*p(L1_23 + e23, 0), *p(LS, 0), '4 m', INK, off=26, size=14, lab_off=10)
    X1, _ = p(L1_23, 0)
    X2, _ = p(L1_23 + e23, 0)
    o += T((X1 + X2) / 2, yb + 70, '*e* = 0.6', 14, KEY, 'middle', 'bold')
    o += L(X1, yb + 44, X1, yb + 54, INK, 1) + L(X2, yb + 44, X2, yb + 54, INK, 1)
    o += T(p(LS, 0)[0] + 20, yb - 6, '每層 *h* = 4 m', 14, INK, 'start', 'bold')
    # 右側圖例
    bx = 520
    o += R(bx, 90, 360, 54, RIG, WARN, 1.4, 8)
    o += T(bx + 180, 123, '網底三角形：剛性區域（S4，整塊轉）', 15, WARN, 'middle', 'bold')
    o += R(bx, 160, 360, 54, KEY2, KEY, 1.4, 8)
    o += T(bx + 180, 193, '紫色粗線：連梁（唯一會變形的地方）', 15, KEY, 'middle', 'bold')
    o += R(bx, 230, 360, 54, COMP2, COMP, 1.4, 8)
    o += T(bx + 180, 263, '兩端各一個力，每層合計＝兩端相加', 15, COMP, 'middle', 'bold')
    o += R(bx, 300, 360, 130, '#fff', INK, 1.4, 8)
    o += T(bx + 180, 330, '題目給：頂層位移 6 cm、尺寸', 15, INK, 'middle', 'bold')
    o += T(bx + 180, 360, '題目沒給：EI 數值、柱與斜撐斷面', 15, INK, 'middle')
    o += T(bx + 180, 392, '「不需經過精確分析」', 15, KEY, 'middle', 'bold')
    o += T(bx + 180, 416, '→ 只能靠比例與幾何', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2023-4 偏心斜撐構架')


def fig6_2():
    W, H = 900, 520
    o = ''
    o += T(450, 34, '一層樓側移 Δ：兩個剛性三角形各繞自己的底角轉 θ = Δ/*h*（θ 放大示意）', 16, INK, 'middle', 'bold')
    s = 62
    x0, yb = 160, 400
    def p(x, y):
        return (x0 + s * x, yb - s * y)
    th = -0.09                                   # 向右側移＝順時針（數學座標負）
    cL, cR = (0.0, 0.0), (LS, 0.0)
    triL = [(0, 0), (0, h23), (L1_23, h23)]
    triR = [(LS, 0), (LS, h23), (L1_23 + e23, h23)]
    # 原位置
    for tri in (triL, triR):
        o += P([p(*q) for q in tri], STEEL, 1.6, close=True, dash='6 5')
    o += L(*p(L1_23, h23), *p(L1_23 + e23, h23), STEEL, 4, '6 5')
    # 轉動後
    nL = [_rot(q, th, cL) for q in triL]
    nR = [_rot(q, th, cR) for q in triR]
    for tri in (nL, nR):
        o += P([p(*q) for q in tri], WARN, 2.4, fill=RIG, close=True, op=0.95)
    a, b = nL[2], nR[2]
    curve = _hermite(a, b, math.tan(th), math.tan(th))
    o += P([p(*q) for q in curve], KEY, 5)
    o += C(*p(*cL), 6, INK, '#fff', 2) + C(*p(*cR), 6, INK, '#fff', 2)
    o += hatch_ground(p(0, 0)[0] - 30, yb + 6, s * LS + 60)
    o += T(p(0, 0)[0] - 10, yb + 30, '轉心', 14, MUT, 'end')
    # 標註：柱頂水平走 hθ＝Δ
    X0, Y0 = p(0, h23)
    X1, Y1 = p(*nL[1])
    o += A(X0, Y0 - 26, X1, Y0 - 26, AC, 2.4, 10)
    o += T((X0 + X1) / 2, Y0 - 34, 'Δ = *h*θ', 15, AC, 'middle', 'bold')
    # 連梁左端：往下 L1θ
    XA0, YA0 = p(L1_23, h23)
    XA, YA = p(*a)
    o += L(XA0, YA0, XA, YA0, STEEL, 1.2, '3 3')
    o += A(XA - 30, YA0, XA - 30, YA, COMP, 2.4, 10)
    o += T(XA - 38, (YA0 + YA) / 2 + 6, '往下 *L*_{1}θ', 15, COMP, 'end', 'bold')
    XB0, YB0 = p(L1_23 + e23, h23)
    XB, YB = p(*b)
    o += A(XB + 30, YB0, XB + 30, YB, TEN, 2.4, 10)
    o += T(XB + 38, (YB0 + YB) / 2 + 6, '往上 *L*_{2}θ', 15, TEN, 'start', 'bold')
    # 轉角弧
    o += arc_arrow(*p(*cL), 70, 70, 50, INK, 2, 9)
    o += T(p(*cL)[0] + 30, p(*cL)[1] - 70, 'θ', 17, INK, 'start', 'bold')
    o += arc_arrow(*p(*cR), 70, 150, 130, INK, 2, 9)
    o += T(p(*cR)[0] - 30, p(*cR)[1] - 70, 'θ', 17, INK, 'end', 'bold')
    o += R(150, 452, 600, 58, KEY2, KEY, 1.5, 9)
    o += T(450, 476, '兩端水平都走 Δ（樓板不伸縮）；垂直方向一個下、一個上：', 15, KEY, 'middle', 'bold')
    o += T(450, 500, '連梁兩端的相對垂直位移 = (*L*_{1} + *L*_{2})θ', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '剛性三角形轉動的運動學')


def fig6_3():
    W, H = 900, 470
    o = ''
    o += T(450, 34, '放大看連梁：端點切線跟著三角形順時針轉 θ，弦卻逆時針轉 α', 16, INK, 'middle', 'bold')
    th = 0.11
    alpha = (L1_23 + L2_23) / e23 * th * 0.32      # 只為示意縮小，比例關係見下方式子
    s = 1
    cx, cy = 450, 250
    half = 190
    A0 = (cx - half, cy + half * math.tan(alpha))
    B0 = (cx + half, cy - half * math.tan(alpha))
    o += L(cx - half - 60, cy, cx + half + 60, cy, STEEL, 1.4, '6 5')
    o += T(cx + half + 64, cy + 5, '原來的梁軸', 14, MUT, 'start')
    # 連梁 S 形：端點斜率 = tan(−θ)（螢幕 y 向下所以取正號）
    pts = []
    n = 40
    d = B0[0] - A0[0]
    for i in range(n + 1):
        t = i / n
        h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
        y = h00 * A0[1] + h10 * d * math.tan(th) + h01 * B0[1] + h11 * d * math.tan(th)
        pts.append((A0[0] + d * t, y))
    o += P(pts, KEY, 6)
    o += L(*A0, *B0, INK, 1.6, '7 5')
    for (X, Y) in (A0, B0):
        o += L(X - 80, Y - 80 * math.tan(th), X + 80, Y + 80 * math.tan(th), WARN, 2.4)
        o += C(X, Y, 5, INK, '#fff', 2)
    # 角度弧：在右端
    X, Y = B0
    def arc(r_, a0, a1, c):
        q = [(X + r_ * math.cos(math.radians(a0 + (a1 - a0) * k / 20)), Y - r_ * math.sin(math.radians(a0 + (a1 - a0) * k / 20))) for k in range(21)]
        return P(q, c, 2.2)
    chord_deg = math.degrees(alpha)
    tan_deg = -math.degrees(th)
    o += L(X, Y, X + 110, Y, STEEL, 1.2, '4 4')
    o += L(X, Y, X + 150 * math.cos(alpha), Y - 150 * math.sin(alpha), INK, 1.4, '7 5')
    o += arc(96, 0, chord_deg, INK)
    o += T(X + 104, Y - 10, 'α', 16, INK, 'start', 'bold')
    o += arc(70, tan_deg, 0, WARN)
    o += T(X + 76, Y + 22, 'θ', 16, WARN, 'start', 'bold')
    o += arc(132, tan_deg, chord_deg, KEY)
    o += T(X + 128, Y - 46, 'γ = α + θ', 17, KEY, 'start', 'bold')
    o += T(A0[0] - 90, A0[1] + 6, '左端', 14, WARN, 'end', 'bold')
    o += T(B0[0] - 20, B0[1] - 26, '右端', 14, WARN, 'end', 'bold')
    o += T(cx - 10, cy - 40, '弦（虛線）', 14, INK, 'end')
    o += R(110, 384, 680, 76, KEY2, KEY, 1.5, 9)
    o += T(450, 412, 'α = (*L*_{1} + *L*_{2})θ / *e*（弦轉角，逆時針）；端點切線 −θ（順時針）', 15, KEY, 'middle', 'bold')
    o += T(450, 442, 'γ = α + θ = (*L*_{1} + *e* + *L*_{2})θ / *e* = (*L*/*e*)θ', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '連梁轉角 γ 的幾何')


def fig6_4():
    W, H = 900, 430
    o = ''
    o += T(450, 32, 'SA-2023-4 一路算下來：層剪力 → 層間位移 → θ → γ（紫）；灰虛線＝「平均分」的錯解', 16, INK, 'middle', 'bold')
    rows = [2, 1, 0]                       # 由上往下：3 樓、2 樓、1 樓
    y0, rh = 110, 84
    cols = [(60, '層剪力 *V*（kN）', r['V'], None, 3000, '{:.0f}', COMP),
            (300, '層間位移 Δ（cm）', r['D'] * 100, r['D_even'] * 100, 3.0, '{:.1f}', AC),
            (540, '連梁轉角 γ（rad）', r['gamma'], rm['g_even'], 0.11, '{:.5f}', KEY)]
    bw = 190
    for (x, title, vals, wrong, vmax, fmt, c) in cols:
        o += T(x + bw / 2 + 20, 70, title, 15, INK, 'middle', 'bold')
        o += L(x + 40, y0 - 14, x + 40, y0 + 3 * rh - 20, INK, 1.4)
        for k, i in enumerate(rows):
            yy = y0 + k * rh
            o += T(x + 32, yy + 26, f'{i + 1}F', 14, MUT, 'end')
            w = vals[i] / vmax * bw
            o += R(x + 40, yy + 8, w, 30, c, None, 0, 4, op=0.85)
            wl = max(w, wrong[i] / vmax * bw + 2) if wrong is not None else w
            o += T(x + 46 + wl, yy + 30, fmt.format(vals[i]), 14, c, 'start', 'bold')
            if wrong is not None:
                ww = wrong[i] / vmax * bw
                o += L(x + 40 + ww, yy + 2, x + 40 + ww, yy + 46, MUT, 2, '5 4')
    o += R(60, 360, 780, 60, KEY2, KEY, 1.5, 9)
    o += T(450, 386, '比例 9 : 7 : 4 → Δ = 2.7、2.1、1.2 cm → θ = Δ/4 → γ = (8.6/0.6)θ', 15, KEY, 'middle', 'bold')
    o += T(450, 410, '平均分（每層 2 cm）會得到三層都 0.0717 rad：底層低估、頂層高估', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2023-4 各層連梁轉角')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
