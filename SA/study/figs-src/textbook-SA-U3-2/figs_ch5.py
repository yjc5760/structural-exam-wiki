# -*- coding: utf-8 -*-
"""第 5 章：范倫迪爾桁架（SA-2019-2）。所有內力 import calcs.ex2019。"""
from figs_common import *  # noqa
import numpy as np
from calcs import ex2019, ff_shape, Lp19, h19, P19, NP19

r = ex2019()
NODES_B = 'ABCDE'
NODES_T = 'FGHIJ'


class Tr:
    def __init__(self, x0, yb, s):
        self.x0, self.yb, self.s = x0, yb, s

    def __call__(self, x, y):
        return (self.x0 + self.s * x, self.yb - self.s * y)


def chord_ff(p0, p1, d0, d1, c=AC, w=3, n=50):
    """水平桿兩端不轉、兩端垂直位移 d0、d1（像素，向下 +）：S 形。"""
    (x0, y0), (x1, y1) = p0, p1
    return P([(x0 + (x1 - x0) * i / n, y0 + d0 + (d1 - d0) * ff_shape(i / n)) for i in range(n + 1)], c, w)


def hinge(x, y, r_=5, c=INK):
    return C(x, y, r_, '#fff', c, 1.8)


def _truss(tr, w=3, c=INK, hinges=False):
    o = ''
    for i in range(NP19):
        for y in (0, h19):
            o += L(*tr(i * Lp19, y), *tr((i + 1) * Lp19, y), c, w)
    for j in range(NP19 + 1):
        o += L(*tr(j * Lp19, 0), *tr(j * Lp19, h19), c, w)
    if hinges:
        for i in range(NP19):
            for y in (0, h19):
                o += hinge(*tr((i + 0.5) * Lp19, y), 5, TEAL)
        for j in range(NP19 + 1):
            o += hinge(*tr(j * Lp19, h19 / 2), 5, TEAL)
    return o


def fig5_1():
    W, H = 900, 470
    o = ''
    d = 46
    # (a) 有斜桿
    o += T(225, 34, '(a) 一般桁架：斜桿用軸力扛剪力', 16, INK, 'middle', 'bold')
    x0, x1, yt, yb = 120, 320, 110, 330
    o += L(x0, yt, x1, yt, INK, 3) + L(x0, yb, x1, yb, INK, 3)
    o += L(x0, yt, x0, yb, INK, 3) + L(x1, yt, x1, yb, INK, 3)
    o += L(x0, yt, x1, yb, TEN, 4)
    o += R(x0 - 26, yt - 14, 14, yb - yt + 28, STEEL2, INK, 1.5)
    o += A(x1 + 30, yt - 60, x1 + 30, yt - 4, COMP, 3, 12)
    o += T(x1 + 38, yt - 34, '*V*', 17, COMP, 'start', 'bold')
    o += T((x0 + x1) / 2 + 30, (yt + yb) / 2 + 14, '斜桿受拉', 15, TEN, 'start', 'bold')
    o += T(225, 400, '三角形不會變形：桿件只有軸力', 15, MUT, 'middle')
    # (b) 范倫迪爾
    o += T(675, 34, '(b) 范倫迪爾：沒有斜桿，弦桿彎成 S 形', 16, INK, 'middle', 'bold')
    x0, x1 = 570, 770
    o += R(x0 - 26, yt - 14, 14, yb - yt + 28, STEEL2, INK, 1.5)
    o += L(x0, yt, x1, yt, STEEL, 1.4, '6 5') + L(x0, yb, x1, yb, STEEL, 1.4, '6 5')
    o += chord_ff((x0, yt), (x1, yt), 0, d, AC, 3.4)
    o += chord_ff((x0, yb), (x1, yb), 0, d, AC, 3.4)
    o += L(x0, yt, x0, yb, INK, 3) + L(x1, yt + d, x1, yb + d, INK, 3)
    for y in (yt, yb):
        o += C((x0 + x1) / 2, y + d / 2, 6, KEY, '#fff', 2)
    o += T((x0 + x1) / 2 + 10, yt + d / 2 - 12, '反曲點 *M* = 0', 15, KEY, 'start', 'bold')
    o += A(x1 + 30, yt + d - 60, x1 + 30, yt + d - 4, COMP, 3, 12)
    o += T(x1 + 38, yt + d - 34, '*V*', 17, COMP, 'start', 'bold')
    o += T(675, 400, '節點剛接：弦桿兩端不轉 → 雙曲率', 15, MUT, 'middle')
    o += R(130, 418, 640, 42, KEY2, KEY, 1.4, 8)
    o += T(450, 446, '剪力只能靠上下弦的彎曲來扛：所以它其實是一個「躺下來的剛架」', 15, KEY, 'middle', 'bold')
    o += L(450, 50, 450, 410, GRID, 1.4)
    return svg(W, H, o, '桁架與范倫迪爾桁架')


def fig5_2():
    W, H = 900, 730
    o = ''
    tr = Tr(150, 320, 36)
    o += T(450, 30, '(a) 每根桿中點放一個鉸（S5），在格間中點直切', 16, INK, 'middle', 'bold')
    o += _truss(tr, 3, INK, True)
    o += pin(*tr(0, 0))
    Ex, Ey = tr(16, 0)
    o += P([(Ex, Ey), (Ex - 11, Ey + 15), (Ex + 11, Ey + 15)], INK, 1.5, fill='#fff', close=True)
    o += C(Ex - 6, Ey + 20, 4, '#fff', INK, 1.3) + C(Ex + 6, Ey + 20, 4, '#fff', INK, 1.3) + hatch_ground(Ex - 17, Ey + 24, 34)
    for j, nm in enumerate(NODES_B):
        X, Y = tr(j * Lp19, 0)
        o += T(X + 8, Y - 8, nm, 15, INK, 'start', 'bold')
    for j, nm in enumerate(NODES_T):
        X, Y = tr(j * Lp19, h19)
        o += T(X, Y - 12, nm, 15, INK, 'middle', 'bold')
    for j in (1, 2, 3):
        X, Y = tr(j * Lp19, 0)
        o += A(X, Y + 6, X, Y + 46, COMP, 3, 12)
        o += T(X + 8, Y + 44, '100', 14, COMP, 'start', 'bold')
    for j in (0, 4):
        X, Y = tr(j * Lp19, 0)
        o += A(X, Y + 76, X, Y + 32, TEN, 3, 12)
        o += T(X + (10 if j == 0 else -10), Y + 70, '150', 14, TEN, 'start' if j == 0 else 'end', 'bold')
    for i in range(NP19):
        X, _ = tr((i + 0.5) * Lp19, 0)
        o += L(X, tr(0, h19)[1] - 28, X, tr(0, 0)[1] + 14, COMP, 1.6, '6 5')
        o += T(X, tr(0, h19)[1] - 34, '①②③④'[i], 16, COMP, 'middle', 'bold')
    o += dim(tr(16, 0)[0] + 40, tr(0, 0)[1], tr(16, 0)[0] + 40, tr(0, h19)[1], '6 m', INK, size=14, lab_off=10)
    o += T(tr(2, 0)[0], tr(0, 0)[1] + 50, '格間 4 m × 4', 14, MUT, 'middle')
    # (b) 整體剪力、彎矩（像一根簡支梁）
    o += T(450, 440, '(b) 把整座桁架當一根 16 m 的簡支梁：格間中點的 *V*、*M*', 16, INK, 'middle', 'bold')
    xs = np.arange(NP19 + 1) * Lp19
    pv = Plot(150, 470, 576, 90, 0, 16, -180, 180)
    pm = Plot(150, 590, 576, 110, 0, 16, 0, 900)
    o += L(pv.X(0), pv.Y(0), pv.X(16), pv.Y(0), INK, 1.4)
    pts = [pv.pt(0, 0)]
    for i in range(NP19):
        pts += [pv.pt(xs[i], r['Vg'][i]), pv.pt(xs[i + 1], r['Vg'][i])]
    pts += [pv.pt(16, 0)]
    o += P(pts, COMP, 2.4, fill=COMP2)
    for i in range(NP19):
        v = r['Vg'][i]
        o += T(pv.X(r['xm'][i]), pv.Y(v) + (-6 if v > 0 else 18), f'*V* = {v:+.0f}', 14, COMP, 'middle', 'bold')
    o += T(pv.X(0) - 12, pv.Y(0) + 5, '*V*', 16, COMP, 'end', 'bold')
    Mn = [0, 600, 800, 600, 0]
    mpts = [(pm.X(x), pm.y0 + pm.h * (m / 900)) for x, m in zip(xs, Mn)]
    o += P([(pm.X(0), pm.y0)] + mpts + [(pm.X(16), pm.y0)], TEN, 2.4, fill=TEN2)
    o += L(pm.X(0), pm.y0, pm.X(16), pm.y0, INK, 1.4)
    for i in range(NP19):
        m = r['Mg'][i]
        X, Y = pm.X(r['xm'][i]), pm.y0 + pm.h * (m / 900)
        o += C(X, Y, 5, KEY, '#fff', 2)
        o += T(X, Y + 22, f'{m:.0f}', 15, KEY, 'middle', 'bold')
    o += T(pm.X(0) - 12, pm.y0 + 5, '*M*', 16, TEN, 'end', 'bold')
    o += T(800, 630, '紫點：切面處', 14, KEY, 'start', 'bold')
    o += T(800, 652, '的整體彎矩', 14, KEY, 'start', 'bold')
    o += T(800, 674, '（kN-m）', 14, KEY, 'start', 'bold')
    return svg(W, H, o, '范倫迪爾桁架的鉸與整體剪力彎矩')


def fig5_3():
    W, H = 900, 540
    o = ''
    o += T(450, 34, '在格間 ② 中點切開，取左半部：彎矩只能由上下弦的軸力偶扛', 16, INK, 'middle', 'bold')
    tr = Tr(170, 390, 42)
    # 左半部：A..B..(6)，F..G..(6)，腹桿 AF、BG
    o += L(*tr(0, 0), *tr(6, 0), INK, 3) + L(*tr(0, h19), *tr(6, h19), INK, 3)
    o += L(*tr(0, 0), *tr(0, h19), INK, 3) + L(*tr(4, 0), *tr(4, h19), INK, 3)
    for y in (0, h19):
        o += hinge(*tr(2, y), 5, TEAL) + hinge(*tr(6, y), 6, TEAL)
    for x in (0, 4):
        o += hinge(*tr(x, h19 / 2), 5, TEAL)
    for nm, (x, y) in (('A', (0, 0)), ('B', (4, 0)), ('F', (0, h19)), ('G', (4, h19))):
        X, Y = tr(x, y)
        o += T(X - 8, Y + (24 if y == 0 else -10), nm, 15, INK, 'end', 'bold')
    X, Y = tr(0, 0)
    o += A(X, Y + 60, X, Y + 6, TEN, 3, 12) + T(X + 10, Y + 54, '150', 15, TEN, 'start', 'bold')
    X, Y = tr(4, 0)
    o += A(X, Y + 6, X, Y + 56, COMP, 3, 12) + T(X + 10, Y + 54, '100', 15, COMP, 'start', 'bold')
    # 切口的力
    Xt, Yt = tr(6, h19)
    Xb, Yb = tr(6, 0)
    o += A(Xt + 76, Yt, Xt + 8, Yt, COMP, 3.4, 13)
    o += T(Xt + 82, Yt + 6, '*N*_{上} = 116.67（壓）', 15, COMP, 'start', 'bold')
    o += A(Xb + 8, Yb, Xb + 76, Yb, TEN, 3.4, 13)
    o += T(Xb + 82, Yb + 6, '*N*_{下} = 116.67（拉）', 15, TEN, 'start', 'bold')
    for (X, Y) in ((Xt, Yt), (Xb, Yb)):
        o += A(X, Y + 8, X, Y + 46, AC, 2.6, 10)
    o += T(Xt + 8, Yt + 46, '25', 14, AC, 'start', 'bold')
    o += T(Xb + 8, Yb + 46, '25', 14, AC, 'start', 'bold')
    o += L(Xb + 30, Yb - 4, Xb + 30, Yt + 4, MUT, 1.1)
    o += T(Xb + 36, (Yb + Yt) / 2 + 5, '*h* = 6 m', 14, MUT, 'start')
    # 右側推導
    bx = 630
    o += R(bx, 100, 250, 250, KEY2, KEY, 1.6, 10)
    lines = [('對下弦切口取力矩：', INK, None), ('150 × 6 − 100 × 2', KEY, 'bold'), ('= *N*_{上} × 6', KEY, 'bold'),
             ('*M* = 700 → *N*_{上} = 116.67', KEY, 'bold'), ('Σ*F*_{*x*} = 0 → *N*_{下} 等大反向', INK, None),
             ('Σ*F*_{*y*}：150 − 100 = 50', INK, None), ('上下弦各 25（5.4 節）', INK, None)]
    for i, (t_, c, wgt) in enumerate(lines):
        o += T(bx + 125, 132 + i * 31, t_, 15, c, 'middle', wgt)
    o += R(110, 484, 680, 46, WARN2, WARN, 1.4, 8)
    o += T(450, 513, '切在反曲點（鉸）上：切口只有軸力和剪力，沒有彎矩——未知數變少', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '格間中點切面：弦桿軸力偶')


def fig5_4():
    W, H = 900, 560
    o = ''
    o += T(450, 34, '取節點 G（切到相鄰三根桿的中點）：三條平衡式各解一個未知數', 16, INK, 'middle', 'bold')
    tr = Tr(140, 400, 60)                 # 局部座標：G 在 (4, 6) → 只畫 x 2..6、y 3..6
    def p(x, y):
        return tr(x - 1.0, y - 3.0)
    o += L(*p(2, 6), *p(6, 6), INK, 4) + L(*p(4, 6), *p(4, 3), INK, 4)
    o += C(*p(4, 6), 6, INK, '#fff', 2) + T(p(4, 6)[0] + 10, p(4, 6)[1] - 14, 'G', 16, INK, 'start', 'bold')
    for q in ((2, 6), (6, 6), (4, 3)):
        o += hinge(*p(*q), 6, TEAL)
    # 左切口：壓力 50 推向右、剪力 75 向上
    X, Y = p(2, 6)
    o += A(X - 70, Y, X - 8, Y, COMP, 3, 12) + T(X - 74, Y - 10, '50 壓', 15, COMP, 'end', 'bold')
    o += A(X, Y + 70, X, Y + 8, AC, 3, 12) + T(X + 10, Y + 62, '75', 15, AC, 'start', 'bold')
    # 右切口：壓力 116.67 推向左、剪力 25 向下
    X, Y = p(6, 6)
    o += A(X + 76, Y, X + 8, Y, COMP, 3, 12) + T(X + 80, Y - 10, '116.67 壓', 15, COMP, 'start', 'bold')
    o += A(X, Y + 8, X, Y + 58, AC, 3, 12) + T(X + 10, Y + 54, '25', 15, AC, 'start', 'bold')
    # 下切口：腹桿拉力 50 向下、剪力 66.67 向右
    X, Y = p(4, 3)
    o += A(X, Y + 8, X, Y + 62, TEN, 3, 12) + T(X + 10, Y + 58, '*N*_{GB} = 50（拉）', 15, TEN, 'start', 'bold')
    o += A(X - 76, Y, X - 8, Y, KEY, 3, 12) + T(X - 80, Y + 6, '*V*_{GB} = 66.67', 15, KEY, 'end', 'bold')
    o += T(p(3, 6)[0], p(3, 6)[1] - 14, '2 m', 14, MUT, 'middle') + T(p(5, 6)[0], p(5, 6)[1] - 14, '2 m', 14, MUT, 'middle')
    o += T(p(4, 4.5)[0] + 12, p(4, 4.5)[1], '3 m', 14, MUT, 'start')
    # 右側三條式
    bx = 630
    o += R(bx, 80, 255, 300, KEY2, KEY, 1.6, 10)
    lines = [('① Σ*F*_{*x*} = 0：', INK, 'bold'), ('50 − 116.67 + *V*_{GB} = 0', KEY, None), ('→ *V*_{GB} = 66.67（軸力差）', KEY, 'bold'),
             ('② Σ*M*_{G} = 0：', INK, 'bold'), ('75×2 + *V*_{GH}×2 = 66.67×3', KEY, None), ('→ *V*_{GH} = 25', KEY, 'bold'),
             ('③ Σ*F*_{*y*} = 0：', INK, 'bold'), ('75 − 25 − *N*_{GB} = 0', KEY, None), ('→ *N*_{GB} = 50（拉）', KEY, 'bold')]
    for i, (t_, c, wgt) in enumerate(lines):
        o += T(bx + 127, 110 + i * 31, t_, 15, c, 'middle', wgt)
    o += R(60, 506, 820, 44, WARN2, WARN, 1.4, 8)
    o += T(470, 534, '從 F 開始一個節點一個節點往右推；每個節點只剩三個未知數（腹桿 *V*、*N* 與右邊弦桿 *V*）', 15, INK, 'middle', 'bold')
    return svg(W, H, o, '節點 G 自由體')


def fig5_5():
    W, H = 900, 1000
    o = ''
    s = 34
    # (a) 軸力圖
    tr = Tr(160, 310, s)
    o += T(450, 34, '(a) 軸力圖（kN）：上弦全壓、下弦全拉、外柱壓、內柱拉', 16, INK, 'middle', 'bold')
    for i in range(NP19):
        for y, Nv_, c in ((h19, r['Ntop'][i], COMP), (0, r['Nbot'][i], TEN)):
            o += L(*tr(i * Lp19, y), *tr((i + 1) * Lp19, y), c, 2 + abs(Nv_) / 20)
            X, Y = tr((i + 0.5) * Lp19, y)
            o += T(X, Y + (-12 if y > 0 else 26), f'{Nv_:+.2f}'.replace('.00', ''), 15, c, 'middle', 'bold')
    for j in range(NP19 + 1):
        Nv_ = r['Nv'][j]
        c = TEN if Nv_ > 0 else COMP
        o += L(*tr(j * Lp19, 0), *tr(j * Lp19, h19), c, 2 + abs(Nv_) / 20)
        X, Y = tr(j * Lp19, h19 / 2)
        o += T(X + (10 if j < 4 else -10), Y + 5, f'{Nv_:+.0f}', 15, c, 'start' if j < 4 else 'end', 'bold')
    for j, nm in enumerate(NODES_B):
        X, Y = tr(j * Lp19, 0)
        o += T(X - 6, Y + 18, nm, 14, MUT, 'end')
    for j, nm in enumerate(NODES_T):
        X, Y = tr(j * Lp19, h19)
        o += T(X - 6, Y - 6, nm, 14, MUT, 'end')
    ms = 0.2                                    # 每 kN-m 的像素
    # (b) 弦桿彎矩
    tr = Tr(160, 640, s)
    o += T(450, 370, '(b) 弦桿彎矩（kN-m，畫在受拉側）：過中點的反對稱直線', 16, INK, 'middle', 'bold')
    o += _truss(tr, 1.4, STEEL, False)
    for i in range(NP19):
        for y, Vc in ((h19, r['Vtop'][i]), (0, r['Vbot'][i])):
            o += L(*tr(i * Lp19, y), *tr((i + 1) * Lp19, y), INK, 2.6)
            x0 = i * Lp19
            pts, base = [], []
            for k in range(21):
                sx = Lp19 * k / 20
                X, Y = tr(x0 + sx, y)
                pts.append((X, Y + Vc * (sx - Lp19 / 2) * ms))
                base.append((X, Y))
            o += P(pts + base[::-1], None, fill=COMP2, close=True) + P(pts, COMP, 2)
            for end, sx in ((0, 0.0), (1, Lp19)):
                M = Vc * (sx - Lp19 / 2)
                X, Y = tr(x0 + sx, y)
                o += T(X + (8 if end == 0 else -8), Y + M * ms + (-7 if M < 0 else 19), f'{abs(M):.0f}', 14, COMP, 'start' if end == 0 else 'end', 'bold')
    # (c) 腹桿彎矩
    tr = Tr(160, 940, s)
    o += T(450, 712, '(c) 腹桿彎矩（kN-m）：外柱 150、次外柱 200、中柱 0', 16, INK, 'middle', 'bold')
    o += _truss(tr, 1.4, STEEL, False)
    for j in range(NP19 + 1):
        Vv = r['Vv'][j]
        o += L(*tr(j * Lp19, 0), *tr(j * Lp19, h19), INK, 2.6)
        if abs(Vv) < 1e-9:
            X, Y = tr(j * Lp19, h19 / 2)
            o += T(X + 8, Y + 5, '0', 15, KEY, 'start', 'bold')
            continue
        pts, base = [], []
        for k in range(21):
            sy = h19 * k / 20
            X, Y = tr(j * Lp19, sy)
            pts.append((X - Vv * (sy - h19 / 2) * ms, Y))
            base.append((X, Y))
        o += P(pts + base[::-1], None, fill=COMP2, close=True) + P(pts, COMP, 2)
        for sy in (0.0, h19):
            dx = -Vv * (sy - h19 / 2) * ms
            X, Y = tr(j * Lp19, sy)
            o += T(X + dx + (-6 if dx < 0 else 6), Y + (16 if sy == h19 else -6), f'{abs(Vv) * h19 / 2:.0f}', 14, COMP, 'end' if dx < 0 else 'start', 'bold')
    o += R(110, 956, 680, 38, KEY2, KEY, 1.4, 8)
    o += T(450, 981, '中間 CH 兩側的上弦剪力 +25、−25 相反，腹桿剪力 0 → 不受彎', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, 'SA-2019-2 軸力圖與彎矩圖')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4, 'fig5_5': fig5_5}
