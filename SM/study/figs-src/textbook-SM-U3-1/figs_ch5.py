# -*- coding: utf-8 -*-
"""第 5 章：傾斜填土與虛擬牆背、Coulomb 楔體力多邊形、試驗楔極值、M–O 作用點。"""
from plot import *  # noqa
from calcs import *  # noqa

SOIL = '#f1e7d0'
SOILE = '#bfa77a'


def fig5_1():
    W_, H = 900, 400
    o = T(220, 30, '(a) 懸臂牆的虛擬牆背', 16, INK, 'middle', 'bold')
    # cantilever wall: stem x 120-150, base 80-320 at y 330-350
    o += P([(150, 330), (150, 100), (320, 100 - 170 * tan(12)), (380, 100 - 230 * tan(12)), (380, 330)], None, fill=SOIL, close=True)
    o += L(150, 100, 390, 100 - 240 * tan(12), SOILE, 2)
    o += R(120, 90, 30, 240, STEEL3, INK, 1.6)
    o += R(70, 330, 250, 24, STEEL3, INK, 1.6)
    o += L(320, 100 - 170 * tan(12), 320, 330, COMP, 3, '8 5')
    o += T(326, 220, '虛擬牆背', 15, COMP, 'start', 'bold')
    o += T(326, 242, '（過牆踵鉛直面）', 14, COMP, 'start')
    o += T(235, 260, '踵上土重', 15, INK, 'middle', 'bold')
    o += T(235, 280, '算進 Σ*V*', 15, INK, 'middle', 'bold')
    o += A(370, 250, 324, 250 + 46 * tan(12), TEN, 3, 11)
    o += T(372, 276, '*P*_{a} ∥ 填土面', 14, TEN, 'start', 'bold')
    o += T(330, 100 - 180 * tan(12) - 14, 'α', 16, INK, 'start', 'bold')
    # (b) curve
    pl = Plot(530, 60, 320, 270, 0, 28, 0.3, 0.6)
    o += T(690, 30, '(b) 傾斜填土 *K*_{a}（φ = 30°）', 16, INK, 'middle', 'bold')
    o += pl.axes([0, 10, 20, 28], [0.3, 0.4, 0.5, 0.6], 'α', '*K*_{a}')
    o += pl.curve(lambda a: Ka_incl(a, 30), 0, 28, KEY, 3)
    e = ex_incl()
    o += pl.dot(0, e['Ka0'], TEN, 5)
    o += T(pl.X(0) + 8, pl.Y(e['Ka0']) - 8, 'α = 0：1/3', 14, TEN, 'start', 'bold')
    o += pl.dot(20, e['Ka'], KEY, 6)
    o += T(pl.X(20) - 8, pl.Y(e['Ka']) - 10, f"α = 20°：{e['Ka']:.3f}", 14, KEY, 'end', 'bold')
    o += T(pl.X(28), pl.Y(0.58), 'α → φ 時急升', 14, COMP, 'end')
    return svg(W_, H, o, '虛擬牆背與傾斜填土')


def fig5_2():
    W_, H = 900, 440
    o = T(230, 30, '(a) 破壞楔與五個力', 16, INK, 'middle', 'bold')
    A_, B_ = (120, 380), (120, 90)
    rho = 58
    C_ = (A_[0] + (A_[1] - B_[1]) / tan(rho) * 1.0, B_[1] - 0)
    o += P([(B_[0] - 10, B_[1]), (420, B_[1]), (420, 400), (B_[0] - 10, 400)], None, fill=SOIL, close=True)
    o += R(92, 80, 28, 310, STEEL3, INK, 1.6)
    o += P([A_, B_, C_], COMP, 2.4, fill=COMP2, close=True)
    o += T(A_[0] - 10, A_[1] + 16, 'A', 15, INK, 'end', 'bold')
    o += T(C_[0] + 8, C_[1] - 6, 'C', 15, INK, 'start', 'bold')
    o += T(A_[0] + 40, A_[1] - 10, 'ρ', 16, COMP, 'start', 'bold')
    gx, gy = (A_[0] + B_[0] + C_[0]) / 3, (A_[1] + B_[1] + C_[1]) / 3
    o += A(gx, gy, gx, gy + 70, INK, 3, 11)
    o += T(gx + 6, gy + 64, '*W*', 15, INK, 'start', 'bold')
    mx, my = (A_[0] + C_[0]) / 2, (A_[1] + C_[1]) / 2
    Lac = math.hypot(C_[0] - A_[0], C_[1] - A_[1])
    ux, uy = (C_[0] - A_[0]) / Lac, (C_[1] - A_[1]) / Lac      # 沿破壞面往上
    nx, ny = uy, -ux                                         # 指向楔體內（左上）
    if nx > 0:
        nx, ny = -nx, -ny
    t = math.tan(math.radians(30))
    rx, ry = nx + t * ux, ny + t * uy
    rl = math.hypot(rx, ry)
    rx, ry = rx / rl, ry / rl
    o += A(mx - 95 * rx, my - 95 * ry, mx, my, AC, 3, 11)
    o += T(mx - 95 * rx + 8, my - 95 * ry + 6, '*R*', 16, AC, 'start', 'bold')
    sx_, sy_ = mx - 70 * ux - 14 * nx, my - 70 * uy - 14 * ny
    o += A(sx_, sy_, sx_ + 60 * ux, sy_ + 60 * uy, TEN, 2.6, 10)
    o += T(sx_ - 6, sy_ + 4, '*C*', 16, TEN, 'end', 'bold')
    o += A(40, 290, 118, 290 - 78 * tan(15), KEY, 3, 11)
    o += T(40, 280, '*P*', 16, KEY, 'start', 'bold')
    o += T(126, 150, '*C*_{a}', 16, WARN, 'start', 'bold')
    # (b) polygon
    o += T(680, 30, '(b) 力多邊形要閉合', 16, INK, 'middle', 'bold')
    x0, y0 = 600, 80
    pts = [(x0, y0), (x0, y0 + 200)]
    o += A(x0, y0, x0, y0 + 200, INK, 3, 12)
    o += T(x0 - 8, y0 + 100, '*W*', 15, INK, 'end', 'bold')
    p2 = (x0 + 120, y0 + 200 - 60)
    o += A(x0, y0 + 200, p2[0], p2[1], TEN, 2.6, 11)
    o += T((x0 + p2[0]) / 2 + 6, y0 + 196, '*C*', 15, TEN, 'start', 'bold')
    p3 = (p2[0] + 60, p2[1] - 150)
    o += A(p2[0], p2[1], p3[0], p3[1], AC, 2.6, 11)
    o += T(p3[0] + 8, (p2[1] + p3[1]) / 2, '*R*', 15, AC, 'start', 'bold')
    o += A(p3[0], p3[1], x0 + 2, y0, KEY, 3, 12)
    o += T((p3[0] + x0) / 2, y0 - 6, '*P*（未知大小）', 15, KEY, 'middle', 'bold')
    o += R(560, 320, 330, 100, KEY2, KEY, 1.4, 8)
    o += T(725, 348, '方向全知道：*W* 鉛直、*R* 偏 φ、*P* 偏 δ', 14, INK, 'middle')
    o += T(725, 376, '大小已知：*W*、*C*、*C*_{a}', 14, INK, 'middle')
    o += T(725, 404, '閉合 → 解出 *P*、*R*', 15, KEY, 'middle', 'bold')
    return svg(W_, H, o, 'Coulomb 破壞楔與力多邊形')


def fig5_3():
    Pm, rm = trial_wedge_max()
    W_, H = 900, 360
    pl = Plot(100, 50, 520, 260, 35, 85, 0, 120)
    o = pl.axes([35, 45, 55, 60, 65, 75, 85], [0, 40, 80, 120], 'ρ（破壞面與水平夾角，°）', '*P*')
    o += pl.curve(lambda rh: trial_wedge(rh), 30.5, 85, KEY, 3)
    o += pl.dot(rm, Pm, COMP, 6)
    o += pl.vline(rm, 0, Pm, COMP, 1.4, '4 3')
    o += T(pl.X(rm) + 10, pl.Y(Pm) + 4, f'最大 {Pm:.1f} kN/m 在 ρ = {rm:.0f}°', 15, COMP, 'start', 'bold')
    o += R(650, 70, 240, 170, KEY2, KEY, 1.4, 8)
    o += T(770, 98, '*c* = 0、牆背光滑鉛直', 14, KEY, 'middle', 'bold')
    o += T(770, 126, 'γ = 18、*H* = 6、φ = 30°', 14, INK, 'middle')
    o += T(770, 156, '*P*(ρ) = *W* tan(ρ − φ)', 15, INK, 'middle')
    o += T(770, 186, 'Rankine：½γ*H*²*K*_{a} = 108', 15, TEN, 'middle', 'bold')
    o += T(770, 216, 'ρ = 45° + φ/2 = 60°', 15, TEN, 'middle', 'bold')
    return svg(W_, H, o, '試驗楔推力隨破壞面角度')


def fig5_4():
    d = ex2016_4()
    W_, H = 900, 400
    top, bot = 50, 350
    Hm = d['H']
    Y = lambda h: bot - h / Hm * (bot - top)
    o = ''
    o += P([(200, bot), (200 + 0, top), (260, top), (310, bot)], INK, 1.6, fill=STEEL3, close=True)
    o += P([(260, top), (310, bot), (520, bot), (520, top)], None, fill=SOIL, close=True)
    for h, val, c, lab, dy in [(Hm / 3, d['Pa'], TEN, f"*P*_{{a}} = {d['Pa']:.2f}（*H*/3）", 16), (0.6 * Hm, d['dP'], COMP, f"Δ*P*_{{ae}} = {d['dP']:.2f}（0.6*H*）", 5), (d['zbar'], d['Pae'], KEY, f"*P*_{{ae}} = {d['Pae']:.2f}（3.08 m）", -8)]:
        y = Y(h)
        xw = 260 + (top - y) / (top - bot) * 50
        Lr = 130
        xs, ys = xw + Lr * cos(d['ang']), y - Lr * sin(d['ang'])
        o += A(xs, ys, xw + 2, y, c, 3.2 if c == KEY else 2.6, 12)
        o += T(xs + 6, ys + dy, lab, 15, c, 'start', 'bold')
    o += dim(170, Y(0), 170, Y(d['zbar']), f"{d['zbar']:.2f} m", KEY, 0, 15, -1)
    o += R(640, 70, 250, 190, KEY2, KEY, 1.4, 8)
    o += T(765, 98, '2016-4（*k*_{h} = 0.15、*k*_{v} = 0.05）', 14, KEY, 'middle', 'bold')
    o += T(765, 128, f"θ′ = tan⁻¹(*k*_{{h}}/(1−*k*_{{v}})) = {d['th']:.2f}°", 14, INK, 'middle')
    o += T(765, 156, f"*K*_{{a}} = {d['Ka']:.4f}、*K*_{{ae}} = {d['Kae']:.4f}", 14, INK, 'middle')
    o += T(765, 186, '*z̄* = [*P*_{a}(*H*/3) + Δ*P*(0.6*H*)]/*P*_{ae}', 14, INK, 'middle')
    o += T(765, 220, f"= {d['zbar']:.2f} m（介於 2.67 與 4.8）", 15, KEY, 'middle', 'bold')
    return svg(W_, H, o, 'M-O 動態土壓的作用點')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
