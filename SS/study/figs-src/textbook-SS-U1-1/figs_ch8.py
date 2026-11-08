# -*- coding: utf-8 -*-
"""第 8 章：有效長度 K、對位圖 G、梁遠端修正、靠桿效應。"""
from plot import *  # noqa
from calcs import K_sway, K_braced
import math

KL0 = 4.4934094579  # tan(kL)=kL 的最小正根


def _mode(case, u):
    """u: 0(底)→1(頂)；回傳正規化側向變位（最大值約 1）。"""
    if case == 'pp':
        return math.sin(math.pi * u)
    if case == 'ff':
        return (1 - math.cos(2 * math.pi * u)) / 2
    if case == 'fp':   # 底固接、頂鉸接
        k = KL0
        y = math.sin(k * u) - k * math.cos(k * u) - k * u + k
        return y / 6.0
    if case == 'fr':   # 底固接、頂自由
        return 1 - math.cos(math.pi * u / 2)


def _ip(case):
    return {'pp': [0, 1], 'ff': [0.25, 0.75], 'fp': [1 - math.pi / KL0, 1], 'fr': [0, 2]}[case]


def fig8_1():
    W, H = 900, 500
    yb, yt = 400, 110
    Lp = yb - yt
    cases = [('pp', '兩端鉸接', '1.0', '1.0'), ('ff', '兩端固接', '0.5', '0.65'), ('fp', '一固一鉸', '0.699', '0.80'), ('fr', '一固一自由', '2.0', '2.10')]
    o = ''
    mx = max(abs(_mode('fp', i / 200)) for i in range(201))
    for i, (cs, name, kt, kd) in enumerate(cases):
        x0 = 95 + i * 210
        amp = 46
        scale = 1 / mx if cs == 'fp' else 1
        o += T(x0 + 20, 32, name, 16, INK, 'middle', 'bold')
        o += L(x0, yb, x0, yt, MUT, 1.2, '5 4')
        if cs == 'fr':
            yfix = yb - Lp / 2            # 固定端在中間；實柱往上，鏡射往下
            xs = lambda u: x0 + amp * (1 - math.cos(math.pi * u / 2))
            real = [(xs(u), yfix - Lp / 2 * u) for u in [k / 50 for k in range(51)]]
            mir = [(xs(u), yfix - Lp / 2 * u) for u in [-k / 50 for k in range(51)]]
            o += L(x0 + amp, yb, x0 + amp, yt, MUT, 1, '3 4')
            o += P(mir, MUT, 2.6, dash='6 4')
            o += P(real, COMP, 4)
            o += fixed_wall(x0 - 4, yfix + 2, 40)
            o += T(x0 + amp + 12, yfix - Lp / 4, '實際 *L*', 14, INK, 'start')
            o += T(x0 + amp + 12, yfix + Lp / 4, '鏡射補完', 14, MUT, 'start')
            ipy = [yb, yt]
        else:
            pts = [(x0 + amp * scale * _mode(cs, u), yb - Lp * u) for u in [k / 100 for k in range(101)]]
            o += P(pts, COMP, 4)
            if cs in ('pp',):
                o += pin(x0, yb + 2) + P([(x0, yt - 2), (x0 - 10, yt - 16), (x0 + 10, yt - 16)], INK, 1.5, fill='#fff', close=True)
            if cs == 'ff':
                o += fixed_wall(x0, yb + 2, 44) + fixed_wall(x0, yt - 2, 44, top=True)
            if cs == 'fp':
                o += fixed_wall(x0, yb + 2, 44) + P([(x0, yt - 2), (x0 - 10, yt - 16), (x0 + 10, yt - 16)], INK, 1.5, fill='#fff', close=True)
            ipy = [yb - Lp * u for u in _ip(cs)]
        for yy in ipy:
            xx = x0 + (0 if cs not in ('ff', 'fr') else (amp if cs == 'fr' else amp * _mode(cs, (yb - yy) / Lp)))
            o += C(xx, yy, 6, KEY, '#fff', 1.6)
        xd = x0 - 34
        o += dim(xd, ipy[0], xd, ipy[1], '', KEY)
        o += T(xd - 8, (ipy[0] + ipy[1]) / 2 + 5, '*KL*', 15, KEY, 'end', 'bold')
        o += T(x0 + 20, 456, f'理論 *K* = {kt}', 15, KEY, 'middle', 'bold')
        o += T(x0 + 20, 482, f'設計 *K* = {kd}', 15, COMP, 'middle', 'bold')
    o += T(450, 66, '紫點＝反曲點（彎矩為零）；兩個紫點之間就是一根「兩端鉸接柱」', 14.5, KEY, 'middle')
    return svg(W, H, o, '有效長度 K')


def _portal(ox, sway):
    o = ''
    h, b = 220, 220
    yb, yt = 330, 330 - h
    xl, xr = ox + 40, ox + 40 + b
    o += L(xl, yb, xl, yt, MUT, 1.2, '5 4') + L(xr, yb, xr, yt, MUT, 1.2, '5 4') + L(xl, yt, xr, yt, MUT, 1.2, '5 4')
    if sway:
        d = 52
        col = lambda x0: [(x0 + d * (1 - math.cos(math.pi * u / 2)) if False else x0 + d * (u - math.sin(math.pi * u) / math.pi * 0.0), yb - h * u) for u in [k / 60 for k in range(61)]]
        # 柱底鉸、頂部固接於剛性梁、頂可側移：模態 = 一固一自由（倒過來）
        pts = lambda x0: [(x0 + d * math.sin(math.pi * u / 2), yb - h * u) for u in [k / 60 for k in range(61)]]
        o += P(pts(xl), COMP, 4) + P(pts(xr), COMP, 4)
        o += L(xl + d, yt, xr + d, yt, INK, 7)
        o += A(xr + d + 14, yt, xr + d + 54, yt, MUT, 2, 9) + T(xr + d + 20, yt - 12, 'Δ', 16, MUT, 'start', italic=True)
        o += T(ox + 150, 30, '無斜撐（可側移）', 17, COMP, 'middle', 'bold')
        o += T(ox + 150, 384, '*K* = 2.0：柱高只有半個波', 16, COMP, 'middle', 'bold')
        o += T(ox + 150, 408, '（鏡射補完是 2*h* 的鉸接柱）', 14, INK, 'middle')
    else:
        # 底鉸、頂固（剛性梁不轉、不側移）：一固一鉸，反曲點距頂 0.3h
        pts = lambda x0, s: [(x0 + s * 30 * _mode('fp', 1 - u) / 0.9, yb - h * u) for u in [k / 60 for k in range(61)]]
        o += P(pts(xl, 1), COMP, 4) + P(pts(xr, -1), COMP, 4)
        o += L(xl, yt, xr, yt, INK, 7)
        o += L(xr + 20, yt + 8, xr + 70, yt + 70, AC, 4) + L(xl - 20, yt + 8, xl - 70, yt + 70, AC, 0) if False else ''
        o += L(xl, yt, xr, yb, AC, 3, '8 5')
        o += T((xl + xr) / 2 + 30, (yt + yb) / 2 - 4, '斜撐', 15, AC, 'start', 'bold')
        o += T(ox + 150, 30, '有斜撐（不可側移）', 17, TEN, 'middle', 'bold')
        o += T(ox + 150, 384, '*K* ≈ 0.7：S 形彎曲', 16, TEN, 'middle', 'bold')
        o += T(ox + 150, 408, '（底鉸、頂固）', 14, INK, 'middle')
    o += pin(xl, yb + 2) + pin(xr, yb + 2)
    o += T(xl - 10, yt - 14, '剛性梁', 14, MUT, 'start')
    return o


def fig8_2():
    W, H = 900, 425
    o = _portal(60, False) + L(450, 20, 450, 415, GRID, 1.5) + _portal(500, True)
    return svg(W, H, o, '有側移與無側移')


def fig8_3():
    W, H = 900, 420
    pl = Plot(90, 50, 560, 300, 0, 10, 0, 3.2)
    o = pl.axes([0, 1, 2, 4, 6, 8, 10], [0, 0.5, 1, 1.5, 2, 2.5, 3], '*G*（柱頂與柱底相同）', '*K*')
    o += pl.curve(lambda g: K_sway(max(g, 1e-6), max(g, 1e-6)), 0, 10, COMP, 3.4, n=120)
    o += pl.curve(lambda g: K_braced(max(g, 1e-6), max(g, 1e-6)), 0, 10, TEN, 3.4, n=120)
    o += T(pl.X(5.2), pl.Y(K_sway(7, 7)) - 6, '有側移：*K* ≥ 1', 15, COMP, 'middle', 'bold')
    o += T(pl.X(7), pl.Y(K_braced(7, 7)) - 14, '無側移：0.5 ≤ *K* ≤ 1', 15, TEN, 'middle', 'bold')
    o += pl.hline(1.0, 0, 10, MUT, 1.2, '5 4')
    o += pl.vline(1, 0, 3.2, KEY, 1.3, '4 4') + pl.vline(10, 0, 3.2, KEY, 1.3, '4 4')
    o += T(pl.X(1) + 6, pl.Y(3.0), '固接端 *G*=1', 14, KEY, 'start', 'bold')
    o += T(pl.X(10) - 6, pl.Y(3.0), '鉸接端 *G*=10', 14, KEY, 'end', 'bold')
    o += T(pl.X(0.2), pl.Y(0.2), '*G* → 0：梁無限硬（理想固接）', 14, MUT, 'start')
    o += R(665, 60, 230, 250, '#fff', KEY, 1.4, 8)
    lines = [('*G* = Σ(*I*/*L*)_{柱} / Σ(*I*/*L*)_{梁}', KEY, True), ('', INK, False), ('*G* 大＝梁擋不住', INK, False), ('　→ 節點像鉸接 → *K* 大', INK, False),
             ('*G* 小＝梁很硬', INK, False), ('　→ 節點像固接 → *K* 小', INK, False), ('', INK, False), ('柱頂 *G*=1、柱底鉸 *G*=10：', INK, False)]
    for i, (s, c, b) in enumerate(lines):
        o += T(682, 96 + i * 22, s, 14, c, 'start', 'bold' if b else None)
    o += T(682, 96 + 8 * 22, f'有側移 *K* = {K_sway(1, 10):.2f}', 14, COMP, 'start', 'bold')
    o += T(682, 96 + 9 * 22 - 4, '', 14, INK, 'start')
    o += T(450, 405, '曲線由對位圖背後的勁度方程式逐點解出（方程式見 8.4 節，不必背）', 14, MUT, 'middle')
    return svg(W, H, o, 'K 與 G')


def _beam(ox, oy, kind):
    """近端（左）轉 θ（順時針）時的梁變形；回傳 SVG。"""
    Lb = 200
    def y(u):
        if kind == 'fixed':      # 遠端固接：y = θL(u − 2u² + u³)
            return u - 2 * u ** 2 + u ** 3
        if kind == 'pinned':     # 遠端鉸接
            return u - 1.5 * u ** 2 + 0.5 * u ** 3
        if kind == 'single':     # 兩端反向轉（對稱、單曲率）
            return u - u ** 2
        if kind == 'double':     # 兩端同向轉（反對稱、雙曲率）
            return u - 3 * u ** 2 + 2 * u ** 3
    amp = 90
    o = L(ox, oy, ox + Lb, oy, MUT, 1.1, '5 4')
    o += P([(ox + Lb * u, oy + amp * y(u)) for u in [k / 60 for k in range(61)]], AC, 4)
    o += C(ox, oy, 5, KEY, '#fff', 1.4)
    o += C(ox + Lb, oy, 5, '#fff', INK, 1.4)
    return o


def fig8_4():
    W, H = 900, 400
    rows = [('fixed', '遠端固接', '4*EI*/*L*', TEN), ('pinned', '遠端鉸接', '3*EI*/*L*', TEN),
            ('single', '兩端反向轉（無側移構架）', '2*EI*/*L*', WARN), ('double', '兩端同向轉（有側移構架）', '6*EI*/*L*', COMP)]
    o = T(450, 28, '近端轉一個角度 θ，要用多大的彎矩？（梁的轉動勁度）', 16, INK, 'middle', 'bold')
    for i, (k, name, stiff, c) in enumerate(rows):
        x0 = 50 + (i % 2) * 430
        y0 = 80 + (i // 2) * 150
        o += _beam(x0, y0, k)
        o += T(x0 + 220, y0 - 8, name, 15, c, 'start', 'bold')
        o += T(x0 + 220, y0 + 20, f'*M* = {stiff} · θ', 16, INK, 'start', 'bold')
    o += R(40, 300, 820, 88, KEY2, KEY, 1.4, 8)
    o += T(450, 324, '對位圖假設：無側移構架的梁是「反向轉」2*EI*/*L*；有側移構架的梁是「同向轉」6*EI*/*L*', 14.5, KEY, 'middle', 'bold')
    o += T(450, 350, '無側移：遠端鉸 3/2 = ×1.5、遠端固 4/2 = ×2.0', 15, TEN, 'middle', 'bold')
    o += T(450, 374, '有側移：遠端鉸 3/6 = ×0.5、遠端固 4/6 = ×2/3', 15, COMP, 'middle', 'bold')
    return svg(W, H, o, '梁遠端修正')


def fig8_5():
    W, H = 900, 420
    o = ''
    yb, h = 340, 220
    yt = yb - h
    d = 40
    xa, xc = 140, 400
    # 抗側柱 AB（底固接）
    pts = [(xa + d * (1 - math.cos(math.pi * u / 2)), yb - h * u) for u in [k / 60 for k in range(61)]]
    o += L(xa, yb, xa, yt, MUT, 1.2, '5 4') + P(pts, AC, 5) + fixed_wall(xa, yb + 2, 50)
    # 靠桿 CD（兩端鉸、直線傾斜）
    o += L(xc, yb, xc, yt, MUT, 1.2, '5 4') + L(xc, yb, xc + d, yt, STEEL, 6)
    o += pin(xc, yb + 2) + C(xc + d, yt, 6, '#fff', INK, 1.6)
    o += L(xa + d, yt, xc + d, yt, INK, 3)  # 連桿
    o += T((xa + xc) / 2 + d, yt - 10, '剛性連桿（樓板）', 14, MUT, 'middle')
    o += A(xa + d, yt - 70, xa + d, yt - 8, COMP, 3, 12) + T(xa + d + 8, yt - 46, '*P*_{1}', 16, COMP, 'start', 'bold')
    o += A(xc + d, yt - 70, xc + d, yt - 8, COMP, 3, 12) + T(xc + d + 8, yt - 46, '*P*_{2}', 16, COMP, 'start', 'bold')
    o += T(xa, yb + 40, 'AB 抗側柱', 15, AC, 'middle', 'bold') + T(xc, yb + 40, 'CD 靠桿', 15, INK, 'middle', 'bold')
    o += T(xc + 70, yt + 80, '兩端鉸接：側向勁度 0', 14, INK, 'start')
    o += A(xc + d - 8, yt + 18, xa + d + 60, yt + 18, KEY, 2.6, 12)
    o += T((xa + xc) / 2 + 30, yt + 40, '*P*_{2}·Δ/*h* 推給 AB', 15, KEY, 'middle', 'bold')
    o += L(560, 20, 560, 400, GRID, 1.5)
    rows = ['① 靠桿傾斜 Δ，*P*_{2} 產生 *P*_{2}Δ', '② 它自己沒有勁度，只能用', '　 水平力 *P*_{2}Δ/*h* 推連桿', '③ 這份力全部由 AB 承擔',
            '④ 整層穩定：*P*_{1} + *P*_{2} ≤ *P*_{eK,AB}', '⑤ 對 AB 而言：', '　 *K*′ = *K* √((*P*_{1}+*P*_{2})/*P*_{1})', '', '*P*_{1} = *P*_{2} 時 *K*′ = √2 *K*', '（SS-2013-2：1.78 → 2.51）']
    for i, s in enumerate(rows):
        o += T(580, 62 + i * 31, s, 15, KEY if i in (6, 8) else INK, 'start', 'bold' if i in (6, 8, 9) else None)
    return svg(W, H, o, '靠桿效應')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3, 'fig8_4': fig8_4, 'fig8_5': fig8_5}
