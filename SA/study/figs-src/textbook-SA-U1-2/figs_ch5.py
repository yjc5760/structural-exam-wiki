# -*- coding: utf-8 -*-
"""第 5 章：內力圖（種子 S3）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import M12, V12, R12, M04, V04, X04_VZERO, M04_MAX, X04_INFL, M0201, V0201
import math


def fig5_1():
    """切一小片 dx：左右兩面的 V、M 與分布載重。"""
    W, H = 900, 380
    o = ''
    x1, x2, yt, yb = 300, 600, 150, 250
    o += R(x1, yt, x2 - x1, yb - yt, STEEL2, INK, 1.8)
    o += udl(x1 + 6, x2 - 6, yt, COMP, 34, 8, '*w*·d*x*', 16)
    # 左面：V 向上、M 順時針（下緣受拉為正）
    o += A(x1 - 14, yb + 30, x1 - 14, yt + 8, WARN, 2.8, 12) + T(x1 - 24, yb + 26, '*V*', 18, WARN, 'end', 'bold')
    o += moment(x1 - 4, (yt + yb) / 2, 34, cw=True, c=KEY, start=250, span=140)
    o += T(x1 - 70, (yt + yb) / 2 - 30, '*M*', 18, KEY, 'end', 'bold')
    # 右面：V+dV 向下、M+dM 順時針
    o += A(x2 + 14, yt - 30, x2 + 14, yb - 8, WARN, 2.8, 12) + T(x2 + 24, yt - 24, '*V* + d*V*', 18, WARN, 'start', 'bold')
    o += moment(x2 + 4, (yt + yb) / 2, 34, cw=False, c=KEY, start=-70, span=140)
    o += T(x2 + 70, (yt + yb) / 2 - 30, '*M* + d*M*', 18, KEY, 'start', 'bold')
    o += dim(x1, yb + 40, x2, yb + 40, 'd*x*', MUT, 0, 16)
    o += T(W / 2, 40, '種子 S3：這一小片也要平衡（正號：下緣受拉的 *M*、左面向上的 *V*）', 16, KEY, 'middle', 'bold')
    o += R(40, 316, 400, 54, TEN2, TEN, 1.4, 8)
    o += T(240, 349, 'Σ*F*_{y}：*V* − *w*d*x* − (*V*+d*V*) = 0 ⇒ d*V*/d*x* = −*w*', 15, INK, 'middle')
    o += R(460, 316, 400, 54, KEY2, KEY, 1.4, 8)
    o += T(660, 349, 'Σ*M*_{右面}：d*M* − *V*d*x* = 0 ⇒ d*M*/d*x* = *V*', 15, INK, 'middle')
    return svg(W, H, o, '微小段平衡')


def _beam_row(o, x0, y, s, segs, supports, loads):
    """畫一根水平梁（座標 m → px）。"""
    return o


def fig5_2():
    """SA-2012-1：載重／剪力／彎矩三聯，坡度關係。"""
    W, H = 900, 640
    o = ''
    f = Frame(110, 90, 42)
    a, b, c, d, e = (f(x, 0) for x in (0, 4, 8, 12, 16))
    o += T(40, 34, '(a) 載重與反力（*R*_{a} = 0、*M*_{a} = 160 順時針、*R*_{d} = 80）', 16, INK, 'start', 'bold')
    o += fixed_left(a[0], a[1]) + L(a[0], a[1], c[0], c[1], INK, 7) + member(c, e) + hinge(*c) + roller(*d)
    o += force(b, 90, 40, COMP, 2.6, '40', 15, (14, 6), 'start') + force(e, 90, 40, COMP, 2.6, '40', 15, (14, 6), 'start')
    o += A(d[0] + 34, d[1] + 52, d[0] + 34, d[1] + 10, TEN, 2.4, 10) + T(d[0] + 42, d[1] + 48, '80', 15, TEN, 'start', 'bold')
    for p, t in ((a, 'a'), (b, 'b'), (c, 'c'), (d, 'd'), (e, 'e')):
        o += T(p[0] + (14 if t == 'a' else 0) - (22 if t == 'd' else 0), p[1] + 26, t, 15, MUT, 'middle', 'bold')
    pv = Plot(110, 190, 672, 150, 0, 16, -60, 60)
    o += T(40, 182, '(b) 剪力 *V*（kN）：沒有分布載重 → 每段水平；集中力 → 跳', 16, WARN, 'start', 'bold')
    o += pv.hline(0, c=INK, w=1.2, dash=None)
    o += pv.area(lambda x: max(V12(x), 0), lambda x: 0, 0, 16, WARN2, 0.9) + pv.area(lambda x: 0, lambda x: min(V12(x), 0), 0, 16, WARN2, 0.9)
    pts = []
    for (x1, x2) in ((0, 4), (4, 12), (12, 16)):
        v = V12((x1 + x2) / 2)
        pts += [pv.pt(x1, v), pv.pt(x2, v)]
    o += P(pts, WARN, 2.6)
    o += T(pv.X(2), pv.Y(0) - 10, '0', 15, WARN, 'middle', 'bold')
    o += T(pv.X(8), pv.Y(-40) + 22, '−40', 15, WARN, 'middle', 'bold')
    o += T(pv.X(14), pv.Y(40) - 10, '+40', 15, WARN, 'middle', 'bold')
    pm = Plot(110, 400, 672, 170, 0, 16, -200, 200)
    o += T(40, 392, '(c) 彎矩 *M*（kN-m）：坡度＝剪力；Δ*M*＝剪力圖面積', 16, KEY, 'start', 'bold')
    o += pm.hline(0, c=INK, w=1.2, dash=None)
    o += pm.area(lambda x: max(M12(x), 0), lambda x: 0, 0, 16, TEN2, 0.9) + pm.area(lambda x: 0, lambda x: min(M12(x), 0), 0, 16, COMP2, 0.9)
    o += pm.curve(lambda x: M12(x + 1e-9), 0, 16, KEY, 2.6)
    o += T(pm.X(2), pm.Y(160) + 24, '+160（坡度 0）', 15, TEN, 'middle', 'bold')
    o += T(pm.X(8) + 8, pm.Y(0) - 12, 'c：0', 15, AC, 'start', 'bold')
    o += T(pm.X(12), pm.Y(-160) + 24, '−160', 15, COMP, 'middle', 'bold')
    for x in (4, 8, 12):
        o += L(pv.X(x), 190, pv.X(x), 570, GRID, 1.2, '4 4')
    o += R(40, 590, 820, 40, KEY2, KEY, 1.3, 8)
    o += T(450, 616, 'b→c：剪力面積 −40×4 = −160 → *M* 從 160 降到 0；c→d：再 −160 → −160；d→e：+40×4 → 回到 0 ✔'.replace(' ✔', ''), 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 三聯圖')


def fig5_3():
    """SA-2004-1 梁 BCD：均布載重 → 剪力直線、彎矩拋物線。"""
    W, H = 900, 600
    o = ''
    f = Frame(150, 100, 100)
    B_, C_, D_ = f(0, 0), f(4, 0), f(6, 0)
    o += T(40, 34, '(a) 梁 BCD（2 t/m 全長；B 端鉸力 3 t 向上、C 滾支承 9 t）', 16, INK, 'start', 'bold')
    o += member(B_, D_) + hinge(*B_) + roller(*C_)
    o += udl(B_[0] + 4, D_[0], B_[1], COMP, 26, 18, '2 t/m', 15)
    o += A(B_[0] - 30, B_[1] + 50, B_[0] - 30, B_[1] + 8, TEN, 2.4, 10) + T(B_[0] - 38, B_[1] + 46, '3', 15, TEN, 'end', 'bold')
    o += A(C_[0] + 34, C_[1] + 56, C_[0] + 34, C_[1] + 14, TEN, 2.4, 10) + T(C_[0] + 42, C_[1] + 52, '9', 15, TEN, 'start', 'bold')
    for p, t in ((B_, 'B'), (C_, 'C'), (D_, 'D')):
        o += T(p[0], p[1] + 36 if t != 'C' else p[1] + 52, t, 15, MUT, 'middle', 'bold')
    pv = Plot(150, 190, 600, 150, 0, 6, -6, 6)
    o += T(40, 182, '(b) 剪力：坡度 = −*w* = −2', 16, WARN, 'start', 'bold')
    o += pv.hline(0, c=INK, w=1.2, dash=None)
    o += pv.curve(lambda x: V04(x), 0, 3.9999, WARN, 2.6) + pv.curve(lambda x: V04(x), 4.0001, 6, WARN, 2.6)
    o += L(pv.X(4), pv.Y(V04(3.9999)), pv.X(4), pv.Y(V04(4.0001)), WARN, 2.6)
    o += pv.dot(X04_VZERO, 0, KEY, 6)
    o += T(pv.X(X04_VZERO) + 8, pv.Y(0) - 12, f'*V* = 0 於 *x* = {X04_VZERO:g}', 15, KEY, 'start', 'bold')
    o += T(pv.X(0) + 6, pv.Y(3) - 6, '+3', 15, WARN, 'start', 'bold')
    o += T(pv.X(4) - 8, pv.Y(-5) + 18, '−5', 15, WARN, 'end', 'bold')
    o += T(pv.X(4) + 8, pv.Y(4) - 4, '+4（C 跳 9）', 15, WARN, 'start', 'bold')
    pm = Plot(150, 400, 600, 130, 0, 6, -4.5, 3)
    o += T(40, 392, '(c) 彎矩：拋物線，頂點在 *V* = 0 處', 16, KEY, 'start', 'bold')
    o += pm.hline(0, c=INK, w=1.2, dash=None)
    o += pm.area(lambda x: max(M04(x), 0), lambda x: 0, 0, 6, TEN2, 0.9) + pm.area(lambda x: 0, lambda x: min(M04(x), 0), 0, 6, COMP2, 0.9)
    o += pm.curve(M04, 0, 6, KEY, 2.6)
    o += pm.dot(X04_VZERO, M04_MAX, KEY, 6) + T(pm.X(X04_VZERO), pm.Y(M04_MAX) + 32, f'{M04_MAX:g} t-m', 15, TEN, 'middle', 'bold')
    o += pm.dot(X04_INFL, 0, AC, 6) + T(pm.X(X04_INFL) + 6, pm.Y(0) - 12, f'反曲點 *x* = {X04_INFL:g}', 15, AC, 'start', 'bold')
    o += T(pm.X(4), pm.Y(-4) + 24, '−4（C）', 15, COMP, 'middle', 'bold')
    for x in (X04_VZERO, 4):
        o += L(pv.X(x), 190, pv.X(x), 530, GRID, 1.2, '4 4')
    o += R(40, 550, 820, 40, KEY2, KEY, 1.3, 8)
    o += T(450, 576, f'最大正彎矩在剪力為 0 的 *x* = {X04_VZERO:g}（不在 B–C 中點 2 m）：*M* = 3(1.5) − 1.5² = {M04_MAX:g}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2004-1 梁')


def fig5_4():
    """集中力 → 剪力跳；集中力偶 → 彎矩跳。"""
    W, H = 900, 360
    o = ''
    for k, (title, sub) in enumerate((('集中力 *P*：剪力跳 *P*', '彎矩只轉折（坡度變）'), ('集中力偶 *M*_{0}：彎矩跳 *M*_{0}', '剪力不變'))):
        ox = 20 + k * 440
        o += R(ox, 14, 420, 330, '#fff', GRID, 1.4, 10)
        o += T(ox + 210, 44, title, 16, KEY if k else WARN, 'middle', 'bold')
        o += T(ox + 210, 70, sub, 15, MUT, 'middle')
        x1, x2, yt, yb = ox + 150, ox + 270, 130, 200
        o += R(x1, yt, x2 - x1, yb - yt, STEEL2, INK, 1.6)
        mx = (x1 + x2) / 2
        if k == 0:
            o += A(mx, yt - 50, mx, yt - 4, COMP, 2.8, 12) + T(mx + 10, yt - 36, '*P*', 17, COMP, 'start', 'bold')
            o += A(x1 - 12, yb + 22, x1 - 12, yt + 6, WARN, 2.6, 11) + T(x1 - 20, yb + 18, '*V*_{左}', 16, WARN, 'end', 'bold')
            o += A(x2 + 12, yt - 22, x2 + 12, yb - 6, WARN, 2.6, 11) + T(x2 + 20, yt - 14, '*V*_{右}', 16, WARN, 'start', 'bold')
            o += R(ox + 30, 252, 360, 70, WARN2, WARN, 1.3, 8)
            o += T(ox + 210, 280, '片寬 → 0：*V*_{左} − *P* − *V*_{右} = 0', 15, INK, 'middle')
            o += T(ox + 210, 308, '⇒ 往右走，剪力往下跳 *P*', 15, WARN, 'middle', 'bold')
        else:
            o += moment(mx, (yt + yb) / 2, 26, cw=True, c=KEY, start=150, span=250)
            o += T(mx, yt - 22, '*M*_{0}（順時針）', 16, KEY, 'middle', 'bold')
            o += moment(x1 - 4, (yt + yb) / 2, 28, cw=True, c=KEY, start=250, span=140)
            o += T(x1 - 60, yt - 4, '*M*_{左}', 16, KEY, 'end', 'bold')
            o += moment(x2 + 4, (yt + yb) / 2, 28, cw=False, c=KEY, start=-70, span=140)
            o += T(x2 + 60, yt - 4, '*M*_{右}', 16, KEY, 'start', 'bold')
            o += R(ox + 30, 252, 360, 70, KEY2, KEY, 1.3, 8)
            o += T(ox + 210, 280, '片寬 → 0：−*M*_{左} − *M*_{0} + *M*_{右} = 0', 15, INK, 'middle')
            o += T(ox + 210, 308, '⇒ 順時針力偶讓 *M* 往上跳 *M*_{0}', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '跳躍規則')


def fig5_5():
    """SA-2002-1 梁 C–F：鉸旁力偶、分布力偶段的坡度。"""
    W, H = 900, 470
    o = ''
    f = Frame(130, 96, 100)
    C_, D_, E_, F_ = f(0, 0), f(2, 0), f(3, 0), f(6, 0)
    o += T(40, 34, '(a) SA-2002-1 的梁 C–F（F 為內鉸；鉸對梁向上 29/3 kN）', 16, INK, 'start', 'bold')
    o += member(C_, F_) + hinge(*F_)
    for i in range(5):
        xx = C_[0] + 20 + i * 38
        o += moment(xx, C_[1], 13, cw=True, c=KEY)
    o += T((C_[0] + D_[0]) / 2, C_[1] - 30, '2 kN-m/m（順時針）', 15, KEY, 'middle', 'bold')
    o += force(E_, 90, 40, COMP, 2.6, '8', 15, (12, 6), 'start')
    o += moment(F_[0] - 26, F_[1], 18, cw=False, c=KEY, start=200, span=230) + T(F_[0] - 30, F_[1] - 30, '4（逆時針，梁端）', 15, KEY, 'end', 'bold')
    o += A(F_[0], F_[1] + 52, F_[0], F_[1] + 10, TEN, 2.4, 10) + T(F_[0] + 8, F_[1] + 48, '29/3', 15, TEN, 'start', 'bold')
    for p, t in ((C_, 'C'), (D_, 'D'), (E_, 'E'), (F_, 'F')):
        o += T(p[0] - (16 if t == 'F' else 0), p[1] + 32, t, 15, MUT, 'middle', 'bold')
    pm = Plot(130, 170, 600, 200, 0, 6, 0, 40)
    o += T(40, 168, '(b) 彎矩（下緣受拉為正）', 16, KEY, 'start', 'bold')
    o += pm.area(lambda x: M0201(x), lambda x: 0, 0, 6, TEN2, 0.9)
    o += pm.curve(M0201, 0, 6, KEY, 2.6)
    o += L(pm.X(6), pm.Y(0), pm.X(6), pm.Y(M0201(5.9999)), KEY, 2.6)
    for x, lab, dy, anc in ((0, f'{M0201(0):g}', -10, 'start'), (2, f'{M0201(2):.2f}', -12, 'middle'), (3, f'{M0201(3):g}', -12, 'start'),
                            (6, f'{round(M0201(5.9999), 2):g}', -10, 'end')):
        o += pm.dot(x, M0201(x - 1e-9 if x == 6 else x), KEY, 5) + T(pm.X(x) + (8 if anc == 'start' else (-8 if anc == 'end' else 0)), pm.Y(M0201(x - 1e-9 if x == 6 else x)) + dy, lab, 15, KEY, anc, 'bold')
    o += T(pm.X(6) + 8, pm.Y(2), '鉸：0', 15, AC, 'start', 'bold')
    o += R(40, 392, 820, 70, KEY2, KEY, 1.3, 8)
    o += T(450, 418, '鉸本身 *M* = 0，緊鄰鉸的梁端卻是 4：那個 4 就是外加力偶造成的「跳」。E→F 坡度 = *V* = −29/3；', 15, INK, 'middle')
    o += T(450, 444, 'C→D 有分布力偶，坡度 = *V* + 2 = −5/3 + 2 = +1/3（同一小片的力矩平衡多一項）', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2002-1 梁彎矩')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4, 'fig5_5': fig5_5}
