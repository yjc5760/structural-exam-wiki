# -*- coding: utf-8 -*-
"""第 3 章：摩擦塊與包絡線、相切三角形、主應力直線、2024-1。"""
from plot import *  # noqa
from calcs import *  # noqa
from figs_ch1 import circle


def fig3_1():
    W, H = 900, 400
    o = ''
    # 左：摩擦塊
    o += hatch_ground(40, 260, 280)
    o += R(110, 200, 120, 60, STEEL3, INK, 1.6)
    o += A(170, 120, 170, 196, COMP, 3, 12) + T(180, 150, '*N*（正向力）', 15, COMP, 'start', 'bold')
    o += A(250, 230, 320, 230, WARN, 3, 12) + T(325, 236, '*T*', 16, WARN, 'start', 'bold')
    o += A(110, 256, 60, 256, TEN, 2.2, 10) + T(50, 248, '摩擦', 14, TEN, 'end', 'bold')
    o += T(180, 310, '*T*_{max}=*c*·面積+*N*tan*φ*', 15, INK, 'middle', 'bold')
    o += T(180, 334, '壓得越重越難推', 14, MUT, 'middle')
    # 右：三條包絡線
    pl = Plot(420, 50, 400, 280, 0, 200, 0, 140)
    o += pl.axes([0, 50, 100, 150, 200], [0, 50, 100], '*σ*', '*τ*')
    o += L(pl.X(0), pl.Y(20), pl.X(200), pl.Y(20 + 200 * tan(25)), WARN, 3)
    o += T(pl.X(200) - 4, pl.Y(20 + 200 * tan(25)) - 8, '*c*′、*φ*′', 15, WARN, 'end', 'bold')
    o += L(pl.X(0), pl.Y(0), pl.X(200), pl.Y(200 * tan(30)), TEN, 2.6, '7 4')
    o += T(pl.X(160), pl.Y(160 * tan(30)) - 34, 'NC 黏土 *c*′=0', 15, TEN, 'end', 'bold')
    o += L(pl.X(0), pl.Y(35), pl.X(200), pl.Y(35), COMP, 2.6, '3 4')
    o += T(pl.X(200), pl.Y(35) + 20, '*φ*_{u}=0（不排水）', 15, COMP, 'end', 'bold')
    o += T(pl.X(10), pl.Y(20) - 8, '*c*', 15, WARN, 'start', 'bold')
    o += T(pl.X(120), pl.Y(8), '線以下安全', 14, MUT, 'middle')
    return svg(W, H, o, '摩擦塊與包絡線')


def fig3_2():
    W, H = 900, 440
    phi, c = 25.0, 20.0
    s3 = 60.0
    s1 = s1_fail(s3, phi, c)
    Cc, R = (s1 + s3) / 2, (s1 - s3) / 2
    xo = -c / tan(phi)
    pl = Plot(110, 60, 620, 310, -60, 250, 0, 155)
    X, Y = pl.X, pl.Y
    o = A(X(-60), Y(0), X(250) + 16, Y(0), INK, 1.5) + A(X(0), Y(0), X(0), Y(155) - 12, INK, 1.5)
    o += T(X(250) + 20, Y(0) + 5, '*σ*', 16, INK) + T(X(0), Y(155) - 20, '*τ*', 16, INK, 'middle')
    o += L(X(xo), Y(0), X(250), Y((250 - xo) * tan(phi)), WARN, 2.8)
    o += circle(pl, s1, s3, COMP, 3)
    tx, ty = Cc - R * sin(phi), R * cos(phi)
    o += P([(X(xo), Y(0)), (X(Cc), Y(0)), (X(tx), Y(ty))], KEY, 2.2, fill=KEY2, close=True, op=0.9)
    o += C(X(tx), Y(ty), 6, KEY, '#fff', 1.8) + C(X(Cc), Y(0), 5, INK, '#fff', 1.5)
    # 直角記號
    ux, uy = (X(Cc) - X(tx)), (Y(0) - Y(ty))
    Ln = math.hypot(ux, uy); ux, uy = ux / Ln * 14, uy / Ln * 14
    vx, vy = (X(xo) - X(tx)), (Y(0) - Y(ty))
    Lv = math.hypot(vx, vy); vx, vy = vx / Lv * 14, vy / Lv * 14
    o += P([(X(tx) + ux, Y(ty) + uy), (X(tx) + ux + vx, Y(ty) + uy + vy), (X(tx) + vx, Y(ty) + vy)], KEY, 1.4)
    o += T(X(xo) + 46, Y(0) - 10, '*φ*', 16, KEY, 'start', 'bold')
    o += T((X(tx) + X(Cc)) / 2 + 10, (Y(ty) + Y(0)) / 2, '*R*', 17, KEY, 'start', 'bold')
    o += dim(X(xo), Y(0) + 28, X(Cc), Y(0) + 28, '', INK)
    o += T((X(xo) + X(Cc)) / 2, Y(0) + 52, '*c*cot*φ*  ＋  *C*', 15, INK, 'middle', 'bold')
    o += T(X(xo), Y(0) - 10, '−*c*cot*φ*', 14, INK, 'middle')
    o += T(X(0) + 6, Y(c) - 6, '*c*', 15, WARN, 'start', 'bold')
    o += T(X(tx) - 8, Y(ty) - 12, '切點', 15, KEY, 'end', 'bold')
    o += curve_arrow([(X(Cc) + 34 * math.cos(a), Y(0) - 34 * math.sin(a)) for a in [i * rad(90 + phi) / 24 for i in range(25)]], COMP, 1.5, 8)
    o += T(X(Cc) + 30, Y(0) - 44, '90°+*φ*', 15, COMP, 'start', 'bold')
    o += box(745, 70, 145, 160, '讀三角形', ['sin*φ*=*R*/(*C*+*c*cot*φ*)', '→ 主應力式', '圓心角→*θ*_{f}', '切點→*σ*_{ff}、*τ*_{ff}'], KEY2, KEY, lsize=14)
    return svg(W, H, o, '相切三角形')


def fig3_3():
    d = ex2025_2()
    W, H = 900, 430
    pl = Plot(90, 50, 560, 320, 0, 220, 0, 400)
    o = pl.axes([0, 50, 100, 150, 200], [0, 100, 200, 300, 400], "*σ*_{3}′ (kN/m²)", "*σ*_{1}′")
    o += pl.curve(lambda x: d['N'] * x + d['K'], 0, 215, KEY, 3)
    N1 = d['s1e1'] / d['s3e1']
    o += pl.curve(lambda x: N1 * x, 0, 200, MUT, 2, dash='7 4')
    for x, y, nm in ((d['s3e1'], d['s1e1'], '試體一 (40, 80)'), (d['s3e2'], d['s1e2'], '試體二 (80, 150)')):
        o += pl.dot(x, y, INK, 6) + T(pl.X(x) + 10, pl.Y(y) + 20, nm, 14, INK, 'start', 'bold')
    o += pl.dot(d['s3_3'], d['s1_3'], KEY, 7)
    o += T(pl.X(d['s3_3']) - 10, pl.Y(d['s1_3']) - 12, 'CD：(200, 360)', 15, KEY, 'end', 'bold')
    o += pl.dot(d['s3_3'], N1 * 200, MUT, 5) + T(pl.X(200) - 10, pl.Y(N1 * 200) - 10, '錯：(200, 400)', 14, MUT, 'end')
    o += pl.vline(200, 0, d['s1_3'], KEY, 1.2)
    o += T(pl.X(4), pl.Y(d['K']) - 8, '截距 10＝2*c*′√*N*_{φ}', 14, KEY, 'start', 'bold')
    o += box(670, 70, 215, 150, '兩點定一線', [f"斜率 *N*_{{φ}}={d['N']:.2f}", '截距 10', f"*φ*′={d['phi']:.2f}°", f"*c*′={d['c']:.2f}"], KEY2, KEY)
    o += T(670, 260, f"CD 軸差 = 360 − 200", 15, KEY, 'start', 'bold')
    o += T(670, 284, f"= {d['ds_3']:.0f} kN/m²", 15, KEY, 'start', 'bold')
    return svg(W, H, o, '主應力式是一條直線')


def fig3_4():
    d = ex2024_1()
    W, H = 900, 440
    pl = Plot(80, 50, 600, 300, -60, 640, 0, 300 * 700 / 600)
    o = A(pl.X(-60), pl.Y(0), pl.X(640) + 14, pl.Y(0), INK, 1.5) + A(pl.X(0), pl.Y(0), pl.X(0), pl.Y(300) - 12, INK, 1.5)
    for s in (0, 100, 200, 300, 400, 500, 600):
        o += L(pl.X(s), pl.Y(0), pl.X(s), pl.Y(0) + 5, INK, 1) + T(pl.X(s), pl.Y(0) + 20, f'{s}', 14, MUT, 'middle')
    for t in (100, 200, 300):
        o += L(pl.X(0) - 5, pl.Y(t), pl.X(0), pl.Y(t), INK, 1) + T(pl.X(0) - 9, pl.Y(t) + 5, f'{t}', 14, MUT, 'end')
    o += T(pl.X(640) + 18, pl.Y(0) + 5, '*σ* (kPa)', 15, INK) + T(pl.X(0), pl.Y(300) - 20, '*τ*', 16, INK, 'middle')
    phi, c = d['phi'], d['c']
    xo = -c / tan(phi)
    o += L(pl.X(xo), pl.Y(0), pl.X(600), pl.Y((600 - xo) * tan(phi)), WARN, 2.6)
    o += circle(pl, d['s1'], d['s3'], COMP, 3)
    o += circle(pl, d['s1b'], d['s3b'], COMP, 2, '7 4')
    o += L(pl.X(d['C']), pl.Y(0), pl.X(d['sff']), pl.Y(d['tff']), KEY, 2)
    o += C(pl.X(d['sff']), pl.Y(d['tff']), 6, KEY, '#fff', 1.8)
    o += L(pl.X(d['sff']), pl.Y(0), pl.X(d['sff']), pl.Y(d['tff']), KEY, 1.2, '4 3') + L(pl.X(d['sff']), pl.Y(d['tff']), pl.X(d['C']), pl.Y(d['tff']), KEY, 1.2, '4 3')
    o += T(pl.X(d['sff']) - 10, pl.Y(d['tff']) - 12, f"({d['sff']:.2f}, {d['tff']:.2f})", 15, KEY, 'end', 'bold')
    o += T((pl.X(d['sff']) + pl.X(d['C'])) / 2, pl.Y(d['tff']) - 8, '*R*sin*φ*', 14, KEY, 'middle')
    o += T(pl.X(d['C']) + 6, pl.Y(d['tff'] / 2), '*R*cos*φ*', 14, KEY, 'start')
    o += T(pl.X(d['s1']), pl.Y(0) - 8, '340', 14, COMP, 'middle', 'bold') + T(pl.X(d['s1b']), pl.Y(0) - 8, '599.46', 14, COMP, 'middle', 'bold')
    o += T(pl.X(560), pl.Y((560 - xo) * tan(phi)) + 26, f"*φ*={phi:.2f}°，*c*=25", 15, WARN, 'end', 'bold')
    o += box(700, 60, 185, 130, '圍壓 100→200', ['軸差 240→399.46', '不是 480', '（*c*≠0 不能比例）'], KEY2, KEY)
    return svg(W, H, o, '2024-1 破壞面應力')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3, 'fig3_4': fig3_4}
