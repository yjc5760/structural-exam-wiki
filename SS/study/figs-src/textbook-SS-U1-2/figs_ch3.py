# -*- coding: utf-8 -*-
"""第 3 章：LTB 的樣子、壓翼板＝側向的柱、Mcr 兩條拉回路徑、強軸 vs 弱軸。"""
from plot import *  # noqa
import math
import calcs

D = calcs.ex_ltb()


def rot(pts, cx, cy, ang, dx=0):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + dx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def H_poly(cx, cy, d, bf, tw, tf):
    """H 斷面外框（多邊形），中心 (cx, cy)。"""
    t, b = cy - d / 2, cy + d / 2
    l, r = cx - bf / 2, cx + bf / 2
    wl, wr = cx - tw / 2, cx + tw / 2
    return [(l, t), (r, t), (r, t + tf), (wr, t + tf), (wr, b - tf), (r, b - tf), (r, b), (l, b), (l, b - tf),
            (wl, b - tf), (wl, t + tf), (l, t + tf)]


def fig3_1():
    W, H = 900, 440
    o = ''
    # (a) 俯視圖：兩端側撐，壓翼板側向挫屈成半個正弦波，拉翼板幾乎不動
    x0, x1, yc = 40, 520, 150
    o += T((x0 + x1) / 2, 34, '(a) 從上往下看（俯視）', 16, INK, 'middle', 'bold')
    o += L(x0, yc, x1, yc, MUT, 1.2, '6 4')
    pts_c = [(x0 + (x1 - x0) * i / 60, yc - 60 * math.sin(math.pi * i / 60)) for i in range(61)]
    pts_t = [(x0 + (x1 - x0) * i / 60, yc - 14 * math.sin(math.pi * i / 60)) for i in range(61)]
    o += P(pts_c, COMP, 3.4) + P(pts_t, TEN, 2.4, dash='8 5')
    for xx in (x0, x1):
        o += T(xx, yc + 6, '×', 22, KEY, 'middle', 'bold')
    o += T(x0, yc + 34, '側撐', 14, KEY, 'middle') + T(x1, yc + 34, '側撐', 14, KEY, 'middle')
    o += T((x0 + x1) / 2, yc - 72, '壓翼板：往旁邊歪（像柱一樣挫屈）', 15, COMP, 'middle', 'bold')
    o += T((x0 + x1) / 2, yc + 34, '拉翼板：被拉直，幾乎不動', 15, TEN, 'middle', 'bold')
    o += dim(x0, yc + 62, x1, yc + 62, '*L*_{b}（側撐間距）', INK, 0, 15)
    # (b) 跨中斷面：原位置（灰）＋側移扭轉後（紅）
    cx, cy = 720, 160
    hp = H_poly(cx, cy, 170, 70, 7, 12)
    o += T(cx, 34, '(b) 跨中斷面', 16, INK, 'middle', 'bold')
    o += P(hp, STEEL, 1.4, STEEL3, close=True)
    o += P(rot(hp, cx, cy + 85, -0.32, 0), COMP, 2.2, COMP2, close=True, op=0.85)
    o += curve_arrow([(cx + 70, cy - 70), (cx + 95, cy - 40), (cx + 100, cy - 5)], KEY, 2, 9)
    o += T(cx + 108, cy - 34, '扭', 15, KEY, 'start', 'bold')
    o += A(cx - 50, cy - 98, cx - 110, cy - 98, COMP, 2.4, 10)
    o += T(cx - 118, cy - 93, '側移', 14, COMP, 'end', 'bold')
    o += T(cx, cy + 118, '側向位移＋扭轉同時發生', 15, INK, 'middle')
    o += T(cx, cy + 140, '→ 側向「扭轉」挫屈', 15, INK, 'middle', 'bold')
    # (c) 壓翼板＝柱
    bx, by = 100, 330
    o += T(bx - 60, by - 14, '(c) 把壓翼板單獨拿出來', 16, INK, 'start', 'bold')
    o += R(bx, by + 10, 420, 18, COMP2, COMP, 1.6)
    o += A(bx - 54, by + 19, bx - 4, by + 19, COMP, 3, 12) + A(bx + 474, by + 19, bx + 424, by + 19, COMP, 3, 12)
    o += T(bx - 30, by + 52, '*C* = *M*/*h*_{0}', 15, COMP, 'middle', 'bold')
    o += T(bx + 210, by + 62, '一根長 *L*_{b}、受壓 *C* 的柱，只能往「弱的方向」（側向）挫屈', 15, INK, 'middle')
    o += box(600, 318, 285, 100, '種子 S3', ['壓翼板是一根側向的柱', '拉翼板拉著它 → 一起扭'], KEY2, KEY, 16, 15)
    return svg(W, H, o, 'LTB 的樣子')


def fig3_2():
    """H700：Mcr 兩條拉回路徑與合成（Cb=1）。"""
    W, H = 900, 420
    d = calcs.example()
    pl = Plot(100, 40, 560, 300, 1, 12, 0, 30000)
    o = pl.axes([2, 4, 6, 8, 10, 12], [0, 5000, 10000, 15000, 20000, 25000, 30000], '*L*_{b}（m）', '*M*（tf·cm）', size=14,
                yfmt=lambda v: f'{v / 1000:.0f}k' if v else '0')
    sv = lambda L: calcs.mcr_basic(L * 100, d['Iy'], d['J'], d['Cw'])[1]
    wp = lambda L: calcs.mcr_basic(L * 100, d['Iy'], d['J'], d['Cw'])[2]
    tot = lambda L: calcs.mcr_basic(L * 100, d['Iy'], d['J'], d['Cw'])[0]
    st = lambda fn: next(x / 100 for x in range(100, 1200) if fn(x / 100) <= 30000)
    o += pl.curve(wp, st(wp), 12, AC, 2.2, dash='8 5')
    o += pl.curve(sv, st(sv), 12, WARN, 2.2, dash='3 4')
    o += pl.curve(tot, st(tot), 12, COMP, 3)
    o += pl.hline(d['Mp'], c=TEN) + pl.hline(d['Mr'], c=WARN)
    o += T(pl.X(12) + 8, pl.Y(d['Mp']) + 5, '*M*_{p}', 15, TEN, 'start', 'bold')
    o += T(pl.X(12) + 8, pl.Y(d['Mr']) + 5, '*M*_{r}', 15, WARN, 'start', 'bold')
    o += T(pl.X(3.1), pl.Y(28000), '翹曲（翼板當柱）∝ 1/*L*_{b}^{2}', 15, AC, 'start', 'bold')
    o += T(pl.X(9.0), pl.Y(7600), '合成 *M*_{cr}', 15, COMP, 'start', 'bold')
    m8 = tot(8)
    o += pl.dot(8, m8, COMP)
    o += T(pl.X(8) + 8, pl.Y(m8) + 26, f'{m8:.0f}', 14, COMP, 'start')
    o += box(690, 60, 200, 230, '兩條路平方相加', ['*M*_{cr}^{2} = *M*_{扭}^{2} + *M*_{翹}^{2}', '', '', '', '', '短梁：翹曲主導', '長梁：扭轉主導'], KEY2, KEY, 16, 14)
    for i, (c, dsh, t) in enumerate(((AC, '8 5', '翹曲 ∝ 1/*L*_{b}^{2}'), (WARN, '3 4', '扭轉 ∝ 1/*L*_{b}'), (COMP, None, '合成 *M*_{cr}'))):
        yy = 135 + i * 24
        o += L(705, yy - 5, 740, yy - 5, c, 2.6, dsh) + T(748, yy, t, 14, c, 'start', 'bold')
    return svg(W, H, o, 'Mcr 兩條拉回路徑')


def fig3_3():
    W, H = 900, 330
    o = ''
    d = calcs.example()
    for k, (title, ang, msg1, msg2, c) in enumerate((('強軸彎曲', 0, '側向（弱軸）勁度小', '→ 可以往旁邊逃：會 LTB', COMP),
                                                     ('弱軸彎曲', math.pi / 2, '旁邊是強軸（硬 42 倍）', '→ 無處可逃：不會 LTB', TEN))):
        cx, cy = 140 + k * 400, 160
        o += T(cx + 100, 34, title, 17, c, 'middle', 'bold')
        hp = H_poly(cx, cy, 160, 70, 7, 12)
        o += P(rot(hp, cx, cy, ang), INK, 1.6, STEEL3, close=True)
        # 彎曲方向箭頭（垂直載重）
        o += A(cx, cy - 120, cx, cy - 92, INK, 2.6, 11)
        o += T(cx + 10, cy - 106, '載重', 14, INK, 'start')
        # 逃逸方向（側向）
        o += A(cx + 52, cy, cx + 100, cy, c, 2.4, 10, dash='5 4' if k else None)
        o += A(cx - 52, cy, cx - 100, cy, c, 2.4, 10, dash='5 4' if k else None)
        o += T(cx + 120, cy - 20, msg1, 15, INK, 'start')
        o += T(cx + 120, cy + 8, msg2, 15, c, 'start', 'bold')
    o += T(W / 2, 300, f'H700×200：*I*_{{x}}/*I*_{{y}} = {d["Ix"]:.0f}/{d["Iy"]:.0f} = {d["Ix"] / d["Iy"]:.0f}　挫屈總是往「比較軟」的方向', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '強軸與弱軸')


ALL = {'fig3_1': fig3_1, 'fig3_2': fig3_2, 'fig3_3': fig3_3}
