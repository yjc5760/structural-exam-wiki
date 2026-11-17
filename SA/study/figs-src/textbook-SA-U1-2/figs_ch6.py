# -*- coding: utf-8 -*-
"""第 6 章：彎矩＝彎曲（種子 S4）。數值全部由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import (M12, EI12, XS12, Y12, D12, A12, TH_C_LEFT, Y_C_AREA, M24, XS24, Y24, YC24,
                   X24_MAX, Y24_MAX, Y24_UP)
import math


def fig6_1():
    """一小段梁彎成圓弧：ε = y/ρ → σ = Eε → M = EI/ρ。"""
    W, H = 900, 400
    o = T(W / 2, 32, '種子 S4：彎矩讓一小段梁彎成圓弧，彎得多兇由 *M*/*EI* 決定', 16, KEY, 'middle', 'bold')
    # 圓弧段（M > 0：曲率中心在上方，下緣較長）
    cx, cy, R0 = 230, -120, 340
    th1, th2 = math.radians(258), math.radians(282)
    pt = lambda r, th: (cx + r * math.cos(th), cy - r * math.sin(th))
    for rr, c, w in ((R0 - 40, INK, 2), (R0, AC, 1.4), (R0 + 40, INK, 2)):
        pts = [pt(rr, th1 + (th2 - th1) * i / 40) for i in range(41)]
        o += P(pts, c, w, dash='6 4' if c == AC else None)
    for th in (th1, th2):
        o += L(*pt(R0 - 40, th), *pt(R0 + 40, th), INK, 2)
        a_ = pt(R0 - 40, th); b_ = pt(R0 - 150, th)
        o += L(*a_, *b_, MUT, 1, '4 4')
    o += T(cx, cy + R0 + 72, '中性軸（長度不變）', 14, AC, 'middle')
    o += T(cx + 6, 140, '*ρ*（往上到曲率中心）', 16, MUT, 'middle', 'bold')
    yy = cy + R0 - 4
    o += moment(cx - 140, yy, 22, cw=True, c=KEY) + moment(cx + 140, yy, 22, cw=False, c=KEY)
    o += T(cx - 168, yy - 26, '*M*', 17, KEY, 'end', 'bold') + T(cx + 168, yy - 26, '*M*', 17, KEY, 'start', 'bold')
    o += T(cx, 330, '下緣伸長、上緣縮短（*M* > 0，梁笑）', 15, INK, 'middle')
    # 右側推導
    o += R(470, 70, 410, 300, KEY2, KEY, 1.4, 10)
    rows = [('① 幾何：離中性軸 *y* 的纖維', INK), ('　 應變 *ε* = −*y*/*ρ*（平面保持平面）', INK),
            ('② 材料：*σ* = *Eε* = −*Ey*/*ρ*', INK),
            ('③ 平衡：*M* = −∫*σy* d*A* = (*E*/*ρ*)∫*y*^{2} d*A*', INK),
            ('　 = *EI*/*ρ*', INK), ('⇒ 曲率 *κ* = 1/*ρ* = *M*/*EI*', KEY)]
    for i, (s, c) in enumerate(rows):
        o += T(490, 110 + i * 42, s, 16, c, 'start', 'bold' if c == KEY else None)
    return svg(W, H, o, '彎矩與曲率')


def fig6_2():
    """M 的正負決定凹向；支承決定邊界條件。"""
    W, H = 900, 400
    o = ''
    # 上：笑臉、哭臉
    for k, (lab, sgn, c) in enumerate((('*M* > 0：下緣受拉，凹口向上（笑）', 1, TEN), ('*M* < 0：上緣受拉，凹口向下（哭）', -1, COMP))):
        ox = 40 + k * 430
        pts = [(ox + 40 + 300 * i / 40, 100 - sgn * 40 * (1 - ((i - 20) / 20) ** 2) + (sgn * 40 if sgn > 0 else 0) - (0 if sgn > 0 else 0)) for i in range(41)]
        pts = [(ox + 40 + 300 * i / 40, (114 - 34 * ((i - 20) / 20) ** 2) if sgn > 0 else (80 + 34 * ((i - 20) / 20) ** 2)) for i in range(41)]
        o += P(pts, c, 4)
        o += T(ox + 190, 150, lab, 15, c, 'middle', 'bold')
    o += T(W / 2, 30, '彎矩圖換號的地方＝變形曲線的反曲點（凹向改變）', 16, KEY, 'middle', 'bold')
    # 下：邊界條件表
    rows = [('固定端', '*y* = 0、*θ* = 0', '曲線在這裡水平地「長」出來'),
            ('鉸、滾支承', '*y* = 0', '斜率可以有'),
            ('內鉸', '*y* 連續，*θ* 可以跳', '可以折出尖角（第 2 章圖 2-7）'),
            ('彈簧支承', '*y* = *R*/*k*', '往下縮 *R*/*k*（第 7、8 章）'),
            ('自由端', '沒有條件', '位移、轉角都要算出來')]
    y0 = 190
    o += R(40, y0, 820, 34, STEEL2, None, 0, 6)
    for x, s in ((60, '支承'), (260, '變形曲線要滿足'), (520, '白話')):
        o += T(x, y0 + 23, s, 15, INK, 'start', 'bold')
    for i, (a, b, c) in enumerate(rows):
        yy = y0 + 34 + i * 34
        o += L(40, yy + 34, 860, yy + 34, GRID, 1)
        o += T(60, yy + 23, a, 15, INK, 'start', 'bold') + T(260, yy + 23, b, 15, AC, 'start') + T(520, yy + 23, c, 15, MUT, 'start')
    return svg(W, H, o, '凹向與邊界條件')


def fig6_3():
    """SA-2012-1：M/EI 圖（面積與形心）→ a–c 的轉角與位移。"""
    W, H = 900, 560
    o = ''
    p = Plot(110, 60, 680, 190, 0, 16, -180, 100)
    o += T(40, 40, '(a) *M*/*EI*（以 1/*EI* 計；a–c 段是 2*EI*，高度減半）', 16, KEY, 'start', 'bold')
    o += p.hline(0, c=INK, w=1.2, dash=None)
    k = lambda x: M12(x + 1e-9) / EI12(x)
    o += p.area(lambda x: max(k(x), 0), lambda x: 0, 0, 16, TEN2, 0.9) + p.area(lambda x: 0, lambda x: min(k(x), 0), 0, 16, COMP2, 0.9)
    o += p.curve(k, 0, 15.999, KEY, 2.6)
    o += T(p.X(2), p.Y(40), f'*A*_{{1}} = {A12["F1"]:g}', 15, TEN, 'middle', 'bold')
    o += T(p.X(5.6), p.Y(20), f'*A*_{{2}} = {A12["F2"]:g}', 15, TEN, 'middle', 'bold')
    o += T(p.X(10.6), p.Y(-60), '−320', 15, COMP, 'middle', 'bold') + T(p.X(13.4), p.Y(-60), '−320', 15, COMP, 'middle', 'bold')
    o += T(p.X(0) + 4, p.Y(80) - 8, '80', 15, KEY, 'start', 'bold')
    o += T(p.X(12), p.Y(-160) + 22, '−160', 15, KEY, 'middle', 'bold')
    for x, t in ((0, 'a'), (4, 'b'), (8, 'c'), (12, 'd'), (16, 'e')):
        o += T(p.X(x), p.Y(0) + 20 if x not in (8,) else p.Y(0) - 8, t, 15, MUT, 'middle', 'bold')
    # (b) 變形
    q = Plot(110, 300, 680, 180, 0, 16, D12['ye'] * 1.1, D12['yc'] * 1.45)
    o += T(40, 292, '(b) 變形曲線（數值積分 *κ* = *M*/*EI*，縱向放大）', 16, AC, 'start', 'bold')
    o += q.hline(0, c=MUT, w=1.2, dash='5 4')
    pts = [q.pt(x, y) for x, y in zip(XS12[::40], Y12[::40])] + [q.pt(XS12[-1], Y12[-1])]
    o += P(pts, AC, 3)
    o += q.dot(8, D12['yc'], AC, 6) + q.dot(16, D12['ye'], AC, 6) + q.dot(12, 0, INK, 5)
    o += L(q.X(0), q.Y(0), q.X(8), q.Y(0), KEY, 1.6, '6 4')
    o += A(q.X(8) + 14, q.Y(0), q.X(8) + 14, q.Y(D12['yc']) + 4, KEY, 1.8, 9, both=True)
    o += T(q.X(8) + 22, q.Y(D12['yc'] / 2) + 5, f'*y*_{{c}} = {Y_C_AREA:.0f}/*EI*', 15, KEY, 'start', 'bold')
    o += T(q.X(0) + 6, q.Y(0) + 20, 'a 端水平（固定端切線）', 14, KEY, 'start')
    o += T(q.X(16) - 8, q.Y(D12['ye']) + 6, f'e：{abs(D12["ye"]):.0f}/*EI* 向下', 15, AC, 'end', 'bold')
    o += R(40, 500, 820, 50, KEY2, KEY, 1.3, 8)
    o += T(450, 522, f'a→c 轉角變化 ＝ 面積 {A12["F1"]:g} + {A12["F2"]:g} = {TH_C_LEFT:g}/*EI*；c 對 a 切線的偏離 ＝ 面積對 c 的矩：', 15, INK, 'middle')
    o += T(450, 544, f'{A12["F1"]:g}×6 + {A12["F2"]:g}×(8/3) = 7040/3 ≈ {Y_C_AREA:.0f}/*EI*（a 端切線水平，所以這就是 *y*_{{c}}）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 面積矩')


def fig6_4():
    """SA-2024-1：彎矩圖 → 凹向 → 反曲點、內鉸尖角、最大位移。"""
    W, H = 900, 560
    o = ''
    f = Frame(110, 92, 56.7)
    A_, B_, C_, D_ = f(0, 0), f(4, 0), f(8, 0), f(12, 0)
    o += T(40, 34, '(a) SA-2024-1：A 滾支承＋200 kN-m 逆時針、B 100 kN↓、C 內鉸、D 固定', 16, INK, 'start', 'bold')
    o += member(A_, D_) + hinge(*C_) + roller(*A_)
    o += L(D_[0], D_[1] - 28, D_[0], D_[1] + 28, INK, 3)
    for i in range(7):
        yy = D_[1] - 28 + i * 9.3
        o += L(D_[0], yy, D_[0] + 8, yy + 7, INK, 1)
    o += moment(A_[0] + 4, A_[1], 22, cw=False, c=KEY) + T(A_[0] + 30, A_[1] - 28, '200', 15, KEY, 'start', 'bold')
    o += force(B_, 90, 44, COMP, 2.6, '100', 15, (12, 6), 'start')
    for p, t in ((A_, 'A'), (B_, 'B'), (C_, 'C'), (D_, 'D')):
        o += T(p[0] + (10 if t == 'D' else 0), p[1] + 40, t, 15, MUT, 'middle', 'bold')
    p = Plot(110, 170, 680, 150, 0, 12, -220, 120)
    o += T(40, 162, '(b) 彎矩（kN-m）', 16, KEY, 'start', 'bold')
    o += p.hline(0, c=INK, w=1.2, dash=None)
    o += p.area(lambda x: max(M24(x), 0), lambda x: 0, 0, 12, TEN2, 0.9) + p.area(lambda x: 0, lambda x: min(M24(x), 0), 0, 12, COMP2, 0.9)
    o += p.curve(M24, 0, 12, KEY, 2.6)
    o += T(p.X(0) + 6, p.Y(-200) + 4, '−200', 15, COMP, 'start', 'bold') + T(p.X(4), p.Y(100) - 8, '+100', 15, TEN, 'middle', 'bold')
    o += T(p.X(12) - 6, p.Y(-100) + 18, '−100', 15, COMP, 'end', 'bold')
    xi = 200 / 75
    o += p.dot(xi, 0, AC, 6) + T(p.X(xi) - 6, p.Y(0) - 10, f'*M* = 0 於 {xi:.2f}', 15, AC, 'end', 'bold')
    q = Plot(110, 360, 680, 140, 0, 12, Y24_MAX * 1.15, 60)
    o += T(40, 352, '(c) 變形曲線（向上為正，以 1/*EI* 計，數值積分）', 16, AC, 'start', 'bold')
    o += q.hline(0, c=MUT, w=1.2, dash='5 4')
    pts = [q.pt(x, y) for x, y in zip(XS24[::60], Y24[::60])] + [q.pt(XS24[-1], Y24[-1])]
    o += P(pts, AC, 3)
    o += q.dot(xi, float(Y24[int(len(XS24) * xi / 12)]), AC, 5) + T(q.X(xi) - 10, q.Y(float(Y24[int(len(XS24) * xi / 12)])) + 4, '反曲點', 14, AC, 'end', 'bold')
    o += q.dot(X24_MAX, Y24_MAX, COMP, 6) + T(q.X(X24_MAX) + 8, q.Y(Y24_MAX) + 20, f'最大向下 {abs(Y24_MAX):.0f}/*EI*（*x* = {X24_MAX:.3f}）', 15, COMP, 'start', 'bold')
    o += q.dot(8, YC24, INK, 5) + T(q.X(8) + 8, q.Y(YC24) - 10, f'C：{abs(YC24):.0f}/*EI*（尖角）', 15, INK, 'start', 'bold')
    o += R(40, 512, 820, 40, KEY2, KEY, 1.3, 8)
    o += T(450, 538, f'A 附近 *M* < 0（哭）→ 先往上翹 {Y24_UP:.1f}/*EI*；過了 *x* = 2.67 變笑 → 往下；C 內鉸折一個角，C–D 是懸臂', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2024-1 變形')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3, 'fig6_4': fig6_4}
