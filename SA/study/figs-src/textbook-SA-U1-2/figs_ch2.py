# -*- coding: utf-8 -*-
"""第 2 章：內鉸。所有數值由 calcs.py 算出。"""
from draw import *  # noqa
from calcs import R12, M12, XS12, Y12, D12, R04, X04_VZERO, M04_MAX, R0202, R0201, R0201_bad
import math
from figs_ch1 import PTS0202


def fmt(v, d=0):
    v = 0.0 if abs(v) < 1e-9 else v
    s = f'{v:.{d}f}'
    return s


def fig2_1():
    """在內鉸切開：兩邊互傳 Fx、Fy，不傳 M。"""
    W, H = 900, 330
    o = ''
    f = Frame(60, 110, 46)
    a, c, d, e = f(0, 0), f(8, 0), f(12, 0), f(16, 0)
    o += T(W / 2, 30, '(a) 一根有內鉸的梁', 16, INK, 'middle', 'bold')
    o += fixed_left(a[0], a[1]) + member(a, c) + member(c, e) + hinge(*c) + roller(*d)
    o += T(c[0], c[1] - 16, '內鉸', 15, AC, 'middle', 'bold')
    # (b) 切開
    y = 250
    o += T(W / 2, 182, '(b) 在鉸切開：鉸只能傳力，不能傳彎矩', 16, INK, 'middle', 'bold')
    xl1, xl2 = 60, 400
    xr1, xr2 = 500, 840
    o += fixed_left(xl1, y) + L(xl1, y, xl2, y, INK, 4.5) + C(xl2, y, 5, '#fff', INK, 1.6)
    o += L(xr1, y, xr2, y, INK, 4.5) + C(xr1, y, 5, '#fff', INK, 1.6) + roller(xr1 + 170, y)
    o += A(xl2, y + 52, xl2, y + 8, WARN, 2.6, 11) + T(xl2 - 10, y + 52, '*F*_{y}', 16, WARN, 'end', 'bold')
    o += A(xl2 - 52, y, xl2 - 8, y, WARN, 2.6, 11) + T(xl2 - 56, y - 10, '*F*_{x}', 16, WARN, 'end', 'bold')
    o += A(xr1, y - 52, xr1, y - 8, WARN, 2.6, 11) + T(xr1 + 10, y - 44, '*F*_{y}', 16, WARN, 'start', 'bold')
    o += A(xr1 + 52, y, xr1 + 8, y, WARN, 2.6, 11) + T(xr1 + 58, y - 10, '*F*_{x}', 16, WARN, 'start', 'bold')
    o += R(395, 286, 110, 34, KEY2, KEY, 1.3, 8) + T(450, 309, '*M* = 0', 16, KEY, 'middle', 'bold')
    o += T(W / 2, y - 14, '大小相等、方向相反', 14, WARN, 'middle')
    return svg(W, H, o, '內鉸切開')


def fig2_2():
    """SA-2012-1：先解附屬 c–e，再解主結構 a–c。"""
    W, H = 900, 560
    o = ''
    s = 46
    # (a) 全梁
    f = Frame(80, 108, s)
    a, b, c, d, e = (f(x, 0) for x in (0, 4, 8, 12, 16))
    o += T(60, 32, '(a) SA-2012-1：a 固定、c 內鉸、d 滾支承', 16, INK, 'start', 'bold')
    o += fixed_left(a[0], a[1]) + L(a[0], a[1], c[0], c[1], INK, 7) + member(c, e) + hinge(*c) + roller(*d)
    o += force(b, 90, 46, COMP, 2.6, '40 kN', 15, (0, -8)) + force(e, 90, 46, COMP, 2.6, '40 kN', 15, (0, -8))
    for p, t in ((a, 'a'), (b, 'b'), (c, 'c'), (d, 'd'), (e, 'e')):
        o += T(p[0] + (12 if t == 'a' else 0), p[1] + 30 + (14 if t == 'd' else 0), t, 16, INK, 'middle', 'bold')
    o += T(f(6, 0)[0], a[1] - 14, '2EI', 15, MUT, 'middle')
    o += T(f(14, 0)[0], a[1] - 14, 'EI', 15, MUT, 'middle')
    for x0, x1 in ((0, 4), (4, 8), (8, 12), (12, 16)):
        o += dim(f(x0, 0)[0], 160, f(x1, 0)[0], 160, '4 m', MUT, 0, 14)
    # (b) 附屬 c–e
    g = Frame(80, 290, s)
    c2, d2, e2 = g(0, 0), g(4, 0), g(8, 0)
    o += T(60, 220, '(b) 先解附屬結構 c–e（自己站不住）', 16, AC, 'start', 'bold')
    o += member(c2, e2) + C(c2[0], c2[1], 5, '#fff', INK, 1.6) + roller(*d2)
    o += force(e2, 90, 46, COMP, 2.6, '40', 15, (0, -8))
    o += A(c2[0], c2[1] - 52, c2[0], c2[1] - 6, WARN, 2.6, 11) + T(c2[0] - 8, c2[1] - 40, f'{abs(R12["Vc"]):.0f}', 16, WARN, 'end', 'bold')
    o += A(d2[0] + 34, d2[1] + 56, d2[0] + 34, d2[1] + 6, TEN, 2.6, 11) + T(d2[0] + 42, d2[1] + 54, f'*R*_{{d}} = {R12["Rd"]:.0f}', 16, TEN, 'start', 'bold')
    o += T(80, 380, f'Σ*M*_{{c}} = 0：*R*_{{d}}·4 = 40·8 → *R*_{{d}} = {R12["Rd"]:.0f}', 15, INK, 'start')
    o += T(80, 404, f'Σ*F*_{{y}} = 0：鉸對 c–e 的力 = {abs(R12["Vc"]):.0f} kN 向下', 15, INK, 'start')
    # (c) 主 a–c
    h = Frame(500, 290, s)
    a3, b3, c3 = h(0, 0), h(4, 0), h(8, 0)
    o += T(480, 220, '(c) 再解主結構 a–c（懸臂）', 16, TEN, 'start', 'bold')
    o += fixed_left(a3[0], a3[1]) + L(a3[0], a3[1], c3[0], c3[1], INK, 7) + C(c3[0], c3[1], 5, '#fff', INK, 1.6)
    o += force(b3, 90, 46, COMP, 2.6, '40', 15, (0, -8))
    o += A(c3[0], c3[1] + 54, c3[0], c3[1] + 6, WARN, 2.6, 11) + T(c3[0] - 8, c3[1] + 50, f'{abs(R12["Vc"]):.0f}（反作用）', 15, WARN, 'end', 'bold')
    o += moment(a3[0] + 22, a3[1], 22, cw=True, c=TEN, start=150, span=230)
    o += T(a3[0] + 46, a3[1] + 44, f'*M*_{{a}} = {abs(R12["Ma"]):.0f}（順時針）', 15, TEN, 'start', 'bold')
    o += T(500, 380, f'Σ*F*_{{y}} = 0：*R*_{{a}} − 40 + 40 = 0 → *R*_{{a}} = {abs(R12["Ra"]):.0f}', 15, INK, 'start')
    o += T(500, 404, f'Σ*M*_{{a}} = 0：*M*_{{a}} = 40·4 − 40·8 = −{abs(R12["Ma"]):.0f}', 15, INK, 'start')
    # 驗算
    o += R(60, 440, 780, 96, KEY2, KEY, 1.4, 10)
    o += T(450, 470, '回頭用整體驗算（S1 一條沒用到的方程）', 16, KEY, 'middle', 'bold')
    o += T(450, 498, f'Σ*F*_{{y}}：*R*_{{a}} + *R*_{{d}} − 40 − 40 = {abs(R12["Ra"]):.0f} + {R12["Rd"]:.0f} − 80 = 0 ✓', 15, INK, 'middle')
    o += T(450, 522, f'Σ*M*_{{a}}：*M*_{{a}} − 40·4 + 80·12 − 40·16 = −160 − 160 + 960 − 640 = 0 ✓', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2012-1 主附屬拆解')


def fig2_3():
    """SA-2012-1 的彎矩圖（預告第 5 章），c 點 M = 0。"""
    W, H = 900, 300
    p = Plot(90, 40, 720, 200, 0, 16, -200, 200)
    o = p.axes([0, 4, 8, 12, 16], [-160, 0, 160], '*x* (m)', '*M* (kN-m)', xfmt=lambda t: f'{t:g}')
    o += p.area(lambda x: max(M12(x), 0), lambda x: 0, 0, 16, TEN2, 0.9)
    o += p.area(lambda x: 0, lambda x: min(M12(x), 0), 0, 16, COMP2, 0.9)
    o += p.curve(lambda x: M12(x + 1e-9), 0, 16, KEY, 2.6)
    o += p.dot(8, 0, AC, 7)
    o += T(p.X(8) + 12, p.Y(0) - 14, 'c（內鉸）：*M* = 0', 15, AC, 'start', 'bold')
    o += T(p.X(2), p.Y(160) - 10, '+160（下緣受拉）', 15, TEN, 'middle', 'bold')
    o += T(p.X(12) + 16, p.Y(-160) + 6, '−160（上緣受拉）', 15, COMP, 'start', 'bold')
    for x, t in ((0, 'a'), (4, 'b'), (12, 'd'), (16, 'e')):
        o += T(p.X(x), p.Y(0) + (-10 if x in (12, 16) else 22), t, 15, MUT, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 彎矩圖')


def fig2_4():
    """SA-2004-1：附屬梁 BCD 先解，柱 AB 上半段零內力。"""
    W, H = 900, 530
    o = ''
    s = 46
    # 左：整體
    f = Frame(90, 330, s)
    A_, B_, C_, D_ = f(0, 0), f(0, 4), f(4, 4), f(6, 4)
    o += T(200, 30, '(a) SA-2004-1（單位 t、m）', 16, INK, 'middle', 'bold')
    o += member(A_, B_) + member(B_, D_) + hinge(*B_) + roller(*C_) + fixed_bottom(A_[0], A_[1], 50)
    o += udl(B_[0] + 8, D_[0], B_[1] - 6, COMP, 24, label='2 t/m')
    o += force(f(0, 2), 180, 44, COMP, 2.6, '4 t', 15, (-6, -8))
    for p, t, dx, dy in ((A_, 'A', -18, -4), (B_, 'B', -18, 22), (C_, 'C', 16, 40), (D_, 'D', 14, 22)):
        o += T(p[0] + dx, p[1] + dy, t, 16, INK, 'middle', 'bold')
    o += dim(B_[0], 376, C_[0], 376, '4 m', MUT, 0, 14) + dim(C_[0], 376, D_[0], 376, '2 m', MUT, 0, 14)
    # 右上：梁 BCD
    g = Frame(500, 120, s)
    B2, C2, D2 = g(0, 0), g(4, 0), g(6, 0)
    o += T(640, 30, '(b) 先解附屬梁 BCD', 16, AC, 'middle', 'bold')
    o += member(B2, D2) + C(B2[0], B2[1], 5, '#fff', INK, 1.6) + roller(*C2)
    o += udl(B2[0] + 8, D2[0], B2[1] - 6, COMP, 24)
    o += A(B2[0], B2[1] + 52, B2[0], B2[1] + 6, WARN, 2.6, 11) + T(B2[0] + 8, B2[1] + 50, f'*B*_{{y}} = {R04["By"]:.0f}', 15, WARN, 'start', 'bold')
    o += A(C2[0] + 30, C2[1] + 56, C2[0] + 30, C2[1] + 6, TEN, 2.6, 11) + T(C2[0] + 38, C2[1] + 54, f'*C*_{{y}} = {R04["Cy"]:.0f}', 15, TEN, 'start', 'bold')
    o += T(500, 210, f'Σ*M*_{{B}}：4*C*_{{y}} = 12 × 3 → *C*_{{y}} = {R04["Cy"]:.0f}；*B*_{{x}} = {abs(R04["Bx"]):.0f}', 15, INK, 'start')
    # 右下：柱 AB
    h = Frame(560, 500, 36)
    A3, B3 = h(0, 0), h(0, 4)
    o += T(700, 262, '(c) 再解主結構：柱 AB', 16, TEN, 'middle', 'bold')
    o += L(A3[0], A3[1], B3[0], B3[1], INK, 4.5) + C(B3[0], B3[1], 5, '#fff', INK, 1.6) + fixed_bottom(A3[0], A3[1], 46)
    o += force(h(0, 2), 180, 40, COMP, 2.4, '4', 15, (-6, -6))
    o += A(B3[0], B3[1] - 50, B3[0], B3[1] - 8, WARN, 2.4, 10)
    o += T(B3[0] + 10, B3[1] - 30, f'{R04["By"]:.0f}（向下壓柱頂）', 15, WARN, 'start', 'bold')
    o += L(B3[0] - 6, B3[1] + 2, B3[0] - 6, h(0, 2)[1] - 2, AC, 8, op=0.35)
    o += T(B3[0] + 14, (B3[1] + h(0, 2)[1]) / 2 + 6, '柱上半段：*V* = *M* = 0', 15, AC, 'start', 'bold')
    o += T(A3[0] + 30, A3[1] - 10, f'*M*_{{A}} = 4 × 2 = {R04["MA"]:.0f}', 15, TEN, 'start', 'bold')
    return svg(W, H, o, 'SA-2004-1 主附屬拆解')


def fig2_5():
    """SA-2002-2：三鉸型桁架，左半部對 C 取矩求水平反力。"""
    W, H = 900, 440
    f = Frame(120, 350, 20)
    P_ = {k: f(*v) for k, v in PTS0202.items()}
    bars = ['DA', 'DF', 'FC', 'DE', 'FE', 'EC', 'AE']
    o = T(W / 2, 30, 'SA-2002-2 左半部（從 C 切開；單位 T、m）', 17, INK, 'middle', 'bold')
    for bar in bars:
        p, q = P_[bar[0]], P_[bar[1]]
        o += L(p[0], p[1], q[0], q[1], STEEL, 5)
    for k in 'ADFEC':
        o += C(*P_[k], 5, KEY, '#fff', 1.2)
    o += pin(*P_['A'])
    for k, (dx, dy) in dict(A=(-18, 4), D=(-18, -6), F=(0, -48), E=(16, 20), C=(16, -16)).items():
        o += T(P_[k][0] + dx, P_[k][1] + dy, k, 16, KEY, 'middle', 'bold')
    o += force(P_['D'], 90, 40, COMP, 2.4, '20', 15, (14, 4)) + force(P_['F'], 90, 40, COMP, 2.4, '20', 15, (14, 4))
    o += force(P_['D'], 180, 44, COMP, 2.4, '16', 15, (-8, -6))
    ax, ay = P_['A']
    o += A(ax - 64, ay + 32, ax - 14, ay + 32, TEN, 2.6, 11) + T(ax - 70, ay + 37, '*A*_{x}', 16, TEN, 'end', 'bold')
    o += A(ax + 28, ay + 66, ax + 28, ay + 24, TEN, 2.6, 11) + T(ax + 36, ay + 64, f'*A*_{{y}} = {R0202["Ay"]}', 15, TEN, 'start', 'bold')
    cx, cy = P_['C']
    o += C(cx, cy, 12, 'none', KEY, 2.2)
    o += T(cx + 20, cy + 30, '切斷 FC、EC：兩根都通過 C', 15, WARN, 'start')
    o += T(cx + 20, cy + 52, '對 C 取矩，它們全部消失', 15, WARN, 'start')
    o += R(450, 200, 430, 150, KEY2, KEY, 1.4, 10)
    o += T(665, 228, 'Σ*M*_{C}（左半部）= 0', 16, KEY, 'middle', 'bold')
    o += T(665, 256, '*A*_{x}·12 − *A*_{y}·16 + 20·16 + 20·8 = 0', 15, INK, 'middle')
    o += T(665, 282, f'*A*_{{x}} = (16·{R0202["Ay"]} − 480)/12 = {R0202["Ax"]} T', 15, INK, 'middle')
    o += T(665, 308, f'整體 Σ*F*_{{x}}：*B*_{{x}} = {-R0202["Bx"]} T（向左）', 15, INK, 'middle')
    o += T(665, 334, '（16 T 在 C 的高度，對 C 沒有力臂）', 14, MUT, 'middle')
    return svg(W, H, o, 'SA-2002-2 三鉸桁架')


def fig2_6():
    """SA-2002-1：F 鉸兩側的力偶各屬於各自的自由體。"""
    W, H = 900, 450
    o = ''
    f = Frame(90, 360, 46)
    A_, B_, C_, E_, F_, G_, H_ = f(0, 0), f(0, 2), f(0, 4), f(3, 4), f(6, 4), f(6, 2), f(6, 0)
    o += T(220, 30, '(a) SA-2002-1（kN、m）', 16, INK, 'middle', 'bold')
    o += member(A_, C_) + member(C_, F_) + member(F_, H_) + hinge(*F_) + pin(*A_) + pin(*H_)
    o += force(C_, 180, 46, COMP, 2.4, '10', 15, (-6, -8))
    o += force(E_, 90, 44, COMP, 2.4, '8', 15, (12, 6))
    o += moment(B_[0], B_[1], 18, cw=False, c=KEY, start=-60, span=250) + T(B_[0] + 24, B_[1] + 6, '6', 15, KEY, 'start', 'bold')
    o += T((C_[0] + f(2, 4)[0]) / 2, C_[1] + 26, '2 kN-m/m ↻', 14, KEY, 'middle')
    o += moment(F_[0] - 26, F_[1], 15, cw=False, c=KEY, start=-80, span=260) + T(F_[0] - 30, F_[1] - 24, '4↺', 15, KEY, 'end', 'bold')
    o += moment(F_[0], F_[1] + 30, 15, cw=True, c=WARN, start=160, span=260) + T(F_[0] + 20, F_[1] + 36, '4↻', 15, WARN, 'start', 'bold')
    o += udl_h(H_[0], G_[1], H_[1] - 4, COMP, 24, label='2 kN/m', to_left=True)
    for p, t, dx, dy in ((A_, 'A', -18, -2), (B_, 'B', -30, 5), (C_, 'C', -14, -12), (E_, 'E', 0, 28), (F_, 'F', 18, -12), (H_, 'H', -18, -2)):
        o += T(p[0] + dx, p[1] + dy, t, 16, INK, 'middle', 'bold')
    # (b) 右分離體
    g = Frame(560, 350, 52)
    F2, G2, H2 = g(0, 4), g(0, 2), g(0, 0)
    o += T(680, 30, '(b) 右分離體：只有柱 FH', 16, WARN, 'middle', 'bold')
    o += L(F2[0], F2[1], H2[0], H2[1], INK, 4.5) + C(F2[0], F2[1], 5, '#fff', INK, 1.6) + pin(*H2)
    o += moment(F2[0], F2[1] + 32, 15, cw=True, c=WARN, start=160, span=260) + T(F2[0] + 20, F2[1] + 38, '4↻ 柱頂的力偶', 15, WARN, 'start', 'bold')
    o += A(F2[0] - 56, F2[1], F2[0] - 8, F2[1], WARN, 2.4, 10) + T(F2[0] - 60, F2[1] + 5, '*P*', 16, WARN, 'end', 'bold')
    o += udl_h(H2[0], G2[1], H2[1] - 4, COMP, 24, label='合力 4 kN，距 H 1 m', to_left=True)
    o += R(470, 372, 420, 64, KEY2, KEY, 1.4, 8)
    o += T(680, 397, 'Σ*M*_{H} = −4*P* − 4 + 4 × 1 = 0', 16, KEY, 'middle', 'bold')
    o += T(680, 424, f'⇒ *P* = {fmt(R0201["Fx"])}（梁端那個 4↺ 不在這個自由體上）', 15, INK, 'middle')
    return svg(W, H, o, 'SA-2002-1 鉸旁力偶')


def fig2_7():
    """SA-2012-1 的變形曲線（數值積分，放大顯示），c 點斜率跳躍。"""
    W, H = 900, 330
    yc, ye = D12['yc'], D12['ye']
    p = Plot(90, 40, 720, 220, 0, 16, ye * 1.15, yc * 1.6)
    o = p.axes([0, 4, 8, 12, 16], [0], '*x* (m)', '', xfmt=lambda t: f'{t:g}', yfmt=lambda t: '0')
    pts = [p.pt(x, y) for x, y in zip(XS12[::40], Y12[::40])] + [p.pt(XS12[-1], Y12[-1])]
    o += P(pts, AC, 3)
    o += p.dot(8, yc, AC, 6) + p.dot(16, ye, AC, 6) + p.dot(12, 0, INK, 5)
    o += T(p.X(8), p.Y(yc) - 14, f'c：向上 {yc:.0f}/*EI*', 15, AC, 'middle', 'bold')
    o += T(p.X(16) - 14, p.Y(ye) + 4, f'e：向下 {abs(ye):.0f}/*EI*', 15, AC, 'end', 'bold')
    o += T(p.X(12) + 8, p.Y(0) - 10, 'd', 15, INK, 'start', 'bold')
    o += T(p.X(0) + 8, p.Y(0) - 12, 'a：水平', 15, INK, 'start', 'bold')
    # 斜率標示
    for th, sgn in ((D12['thc_left'], -1), (D12['thc_right'], 1)):
        x0, y0 = 8, yc
        dx = 1.6 * sgn
        o += L(p.X(x0), p.Y(y0), p.X(x0 + dx), p.Y(y0 + th * dx), KEY, 1.8, '6 4')
    o += T(p.X(1), p.Y(ye * 0.55), f'c 點：左斜率 +{D12["thc_left"]:.0f}/*EI*，右斜率 {D12["thc_right"]:.0f}/*EI*', 15, KEY, 'start', 'bold')
    o += T(W / 2, 318, '內鉸：位移連續，斜率可以跳（尖角）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2012-1 變形曲線')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4,
       'fig2_5': fig2_5, 'fig2_6': fig2_6, 'fig2_7': fig2_7}
