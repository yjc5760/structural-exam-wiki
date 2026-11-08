# -*- coding: utf-8 -*-
"""第 1 章：應力塊四階段、M–φ 曲線、矩形推 S 與 Z、非對稱斷面 ENA／PNA。"""
from plot import *  # noqa
import calcs

D = calcs.example()
R25 = calcs.ex_2025_1()
R23 = calcs.ex_2023_3()
HR = calcs.H_rects(D['d'], D['bf'], D['tw'], D['tf'])


def draw_H(cx, cy, scale, d, bf, tw, tf, fill=STEEL3, c=INK):
    """對稱 H，中心 (cx, cy)。回傳 svg 片段與上下緣 y。"""
    H, B, TW, TF = d * scale, bf * scale, max(tw * scale, 3), tf * scale
    top, bot = cy - H / 2, cy + H / 2
    o = R(cx - B / 2, top, B, TF, fill, c, 1.4)
    o += R(cx - B / 2, bot - TF, B, TF, fill, c, 1.4)
    o += R(cx - TW / 2, top + TF, TW, H - 2 * TF, fill, c, 1.4)
    return o, top, bot


def stress_panel(x0, yc, hh, ratio, sw=52):
    """以 x0 為軸、yc 為中性軸的應力剖面；ratio = φ/φy；壓（上）畫左、拉（下）畫右。"""
    n = 80
    o = ''
    for sgn, col, colM in ((1, COMP, COMPM), (-1, TEN, TENM)):
        pts = [(x0, yc)]
        for i in range(n + 1):
            yy = i / n                         # 0→1 由中性軸到外緣
            s = min(1.0, ratio * yy)
            px = x0 - sgn * s * sw
            py = yc - sgn * yy * hh
            pts.append((px, py))
        pts.append((x0, yc - sgn * hh))
        o += P(pts, col, 1.8, fill=colM, close=True, op=0.9)
    o += L(x0, yc - hh - 10, x0, yc + hh + 10, INK, 1.4)
    o += L(x0 - sw, yc - hh - 6, x0 - sw, yc + hh + 6, MUT, 1, '4 4')
    o += L(x0 + sw, yc - hh - 6, x0 + sw, yc + hh + 6, MUT, 1, '4 4')
    return o


def fig1_1():
    W, H = 900, 420
    yc, hh = 190, 120
    o = ''
    s, top, bot = draw_H(80, yc, hh * 2 / D['d'], D['d'], D['bf'], D['tw'], D['tf'])
    o += s
    o += L(30, yc, 130, yc, AC, 1.4, '6 4') + T(80, bot + 28, 'H700×200', 15, INK, 'middle', 'bold')
    o += T(132, yc - 6, '中性軸', 14, AC, 'start')
    stages = [(0.6, '(a) 彈性', f'*M* = {calcs.M_phi(HR, D["Fy"], 0.6):.2f}*M*_{{y}}', AC),
              (1.0, '(b) 外緣剛降伏', '*M* = *M*_{y} = *F*_{y}*S*_{x}', AC),
              (2.0, '(c) 外圈塑性', f'*M* = {calcs.M_phi(HR, D["Fy"], 2.0):.2f}*M*_{{y}}', WARN),
              (60.0, '(d) 全斷面降伏', '*M* = *M*_{p} = *F*_{y}*Z*_{x}', TEN)]
    for i, (r, t1, t2, c) in enumerate(stages):
        x0 = 280 + i * 172
        o += stress_panel(x0, yc, hh, r)
        o += T(x0, yc + hh + 40, t1, 15, c, 'middle', 'bold')
        o += T(x0, yc + hh + 64, t2, 15, INK, 'middle')
    o += T(280 - 52, 50, '−*F*_{y}', 14, MUT, 'middle') + T(280 + 52, 50, '+*F*_{y}', 14, MUT, 'middle')
    o += T(280 + 3 * 172 + 60, yc - hh + 8, '壓', 15, COMP, 'start', 'bold')
    o += T(280 + 3 * 172 + 60, yc + hh, '拉', 15, TEN, 'start', 'bold')
    o += T(W / 2, 30, '同一個斷面，彎矩越加越大：應力從「一條斜線」長成「兩塊長方形」', 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '應力塊四階段')


def fig1_2():
    W, H = 900, 400
    pl = Plot(90, 50, 560, 280, 0, 8, 0, 1.6)
    o = pl.axes([0, 1, 2, 4, 6, 8], [0, 0.5, 1.0, 1.5], 'φ/φ_{y}', '*M*/*M*_{y}', size=14)
    o += pl.curve(calcs.rect_Mphi, 0, 8, AC, 2.6)
    o += pl.curve(lambda x: calcs.M_phi(HR, D['Fy'], x, 400), 0, 8, COMP, 2.6, n=80)
    o += pl.hline(1.5, c=AC) + pl.hline(D['f'], c=COMP)
    o += pl.dot(1, 1, KEY)
    o += T(pl.X(1) + 10, pl.Y(1) + 22, '外緣剛降伏', 14, KEY, 'start', 'bold')
    o += T(pl.X(8) + 12, pl.Y(1.5) + 5, '矩形 → 1.5', 15, AC, 'start', 'bold')
    o += T(pl.X(8) + 12, pl.Y(D['f']) + 5, f'H700 → {D["f"]:.3f}', 15, COMP, 'start', 'bold')
    o += T(pl.X(4.6), pl.Y(0.55), '曲率再大，彎矩也長不過 *M*_{p}', 15, MUT, 'middle')
    o += T(pl.X(4.6), pl.Y(0.42), '上限 ÷ *M*_{y} ＝ 形狀因子 *f*', 15, MUT, 'middle')
    return svg(W, H, o, '彎矩–曲率曲線')


def fig1_3():
    W, H = 900, 380
    o = ''
    b, h = 90, 220
    for k, (title, mode, c) in enumerate((('降伏彎矩 *M*_{y}：兩個三角形', 'y', AC),
                                         ('塑性彎矩 *M*_{p}：兩個長方形', 'p', TEN))):
        ox = 40 + k * 440
        yt, yc = 70, 70 + h / 2
        o += T(ox + 200, 40, title, 16, c, 'middle', 'bold')
        o += R(ox, yt, b, h, STEEL3, INK, 1.4)
        o += dim(ox, yt + h + 18, ox + b, yt + h + 18, '*b*', INK, 0, 15)
        o += dim(ox - 18, yt, ox - 18, yt + h, '', INK, 0) + T(ox - 26, yc - 10, '*h*', 15, INK, 'end')
        o += L(ox - 6, yc, ox + b + 230, yc, AC, 1.2, '6 4')
        x0, sw = ox + b + 70, 60
        if mode == 'y':
            o += P([(x0, yc), (x0 - sw, yt), (x0, yt)], COMP, 1.6, COMPM, close=True)
            o += P([(x0, yc), (x0 + sw, yt + h), (x0, yt + h)], TEN, 1.6, TENM, close=True)
            yC, yT = yc - h / 3, yc + h / 3
            lab = ('*C* = *F*_{y}·*b*·*h*/4', '力臂 = 2*h*/3')
        else:
            o += R(x0 - sw, yt, sw, h / 2, COMPM, COMP, 1.6)
            o += R(x0, yc, sw, h / 2, TENM, TEN, 1.6)
            yC, yT = yc - h / 4, yc + h / 4
            lab = ('*C* = *F*_{y}·*b*·*h*/2', '力臂 = *h*/2')
        o += L(x0, yt - 8, x0, yt + h + 8, INK, 1.3)
        o += A(x0 - 6, yC, x0 - 56, yC, COMP, 2.6, 11)
        o += A(x0 + 6, yT, x0 + 56, yT, TEN, 2.6, 11)
        o += T(x0 + 76, yT + 22, lab[0].replace('*C*', '*T*'), 14, TEN, 'start')
        o += dim(x0 + 150, yC, x0 + 150, yT, '', INK, 0)
        o += T(x0 + 160, yc + 5, lab[1], 15, INK, 'start', 'bold')
        o += T(x0 + 76, yC - 8, lab[0], 14, COMP, 'start')
    o += T(260, 350, '*M*_{y} = (*F*_{y}*bh*/4)(2*h*/3) = *F*_{y}·*bh*^{2}/6', 16, AC, 'middle', 'bold')
    o += T(700, 350, '*M*_{p} = (*F*_{y}*bh*/2)(*h*/2) = *F*_{y}·*bh*^{2}/4', 16, TEN, 'middle', 'bold')
    return svg(W, H, o, '矩形斷面推 S 與 Z')


def fig1_4():
    W, H = 900, 560
    sc = 3.3                    # px / cm
    base, cx = 430, 150         # 底緣 y、斷面中心 x
    Y = lambda y: base - y * sc
    o = ''
    yp, yb = R23['yp'], R23['ybar']
    o += R(cx - 25 * sc, Y(110), 50 * sc, 5 * sc, ACM, INK, 1.3)          # 上翼
    o += R(cx - 1 * sc, Y(105), 2 * sc, (105 - yp) * sc, ACM, INK, 1.0)    # 腹板上段
    o += R(cx - 1 * sc, Y(yp), 2 * sc, (yp - 5) * sc, WARNM, INK, 1.0)     # 腹板下段
    o += R(cx - 15 * sc, Y(5), 30 * sc, 5 * sc, WARNM, INK, 1.3)          # 下翼
    o += L(cx - 120, Y(yb), cx + 650, Y(yb), AC, 1.8, '7 4')
    o += L(cx - 120, Y(yp), cx + 650, Y(yp), TEN, 1.8, '7 4')
    o += T(cx - 122, Y(yb) + 20, f'ENA {yb:.2f}', 14, AC, 'start', 'bold')
    o += T(cx - 122, Y(yp) - 8, f'PNA {yp:.0f}', 14, TEN, 'start', 'bold')
    o += T(cx + 20, Y(100), '上方 250+50 = 300 cm²', 14, AC, 'start', 'bold')
    o += T(cx + 20, Y(30), '下方 150+150 = 300 cm²', 14, WARN, 'start', 'bold')
    o += T(cx - 15 * sc, base + 26, '單位 cm，依比例；y 自底緣量起', 14, MUT, 'start')
    x1, sw = 540, 70
    ct, cb = R23['ct'], R23['cb']
    o += T(x1, 34, '彈性：繞 ENA', 16, AC, 'middle', 'bold')
    o += L(x1, Y(112), x1, Y(-2), INK, 1.3)
    o += P([(x1, Y(yb)), (x1 - sw * ct / cb, Y(110)), (x1, Y(110))], COMP, 1.6, COMPM, close=True)
    o += P([(x1, Y(yb)), (x1 + sw, Y(0)), (x1, Y(0))], TEN, 1.6, TENM, close=True)
    o += T(x1 - sw * ct / cb - 6, Y(110) + 16, f'{ct / cb:.3f}*F*_{{y}}', 14, COMP, 'end')
    o += T(x1 + sw, Y(0) + 22, '*F*_{y}（先到）', 14, TEN, 'middle', 'bold')
    x2 = 740
    o += T(x2, 34, '塑性：繞 PNA', 16, TEN, 'middle', 'bold')
    o += L(x2, Y(112), x2, Y(-2), INK, 1.3)
    o += R(x2 - sw, Y(110), sw, (110 - yp) * sc, COMPM, COMP, 1.6)
    o += R(x2, Y(yp), sw, yp * sc, TENM, TEN, 1.6)
    o += T(x2 - sw - 6, Y(110) + 16, '*F*_{y}', 14, COMP, 'end')
    o += T(x2 + sw / 2, Y(0) + 22, '*F*_{y}', 14, TEN, 'middle')
    o += box(430, base + 50, 440, 70, f'兩條軸差 {R23["gap"]:.2f} cm', ['ENA：一次矩為零（彈性）　PNA：上下面積相等（塑性）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, '非對稱斷面 ENA 與 PNA')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
