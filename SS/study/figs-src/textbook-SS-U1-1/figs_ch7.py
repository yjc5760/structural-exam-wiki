# -*- coding: utf-8 -*-
"""第 7 章：挫屈的本質與 Euler。"""
from plot import *  # noqa
from calcs import E, H100
import math


def fig7_1():
    W, H = 900, 400
    o = T(225, 28, '(a) 平衡的三種性質', 16, INK, 'middle', 'bold')
    # 三個地形
    for i, (name, kind, c, msg) in enumerate((('穩定', 'valley', TEN, '推開會回來'), ('臨界', 'flat', KEY, '推到哪停哪'), ('不穩定', 'hill', COMP, '一推就滾走'))):
        cx = 80 + i * 145
        base = 190
        if kind == 'valley':
            pts = [(cx - 60 + t, base - 40 + 40 * (1 - ((t - 60) / 60) ** 2) * -1 + 40) for t in range(0, 121, 4)]
            pts = [(cx - 60 + t, base - 45 * ((t - 60) / 60) ** 2) for t in range(0, 121, 4)]
            by = base - 12
        elif kind == 'flat':
            pts = [(cx - 60, base - 20), (cx + 60, base - 20)]
            by = base - 32
        else:
            pts = [(cx - 60 + t, base - 45 + 45 * ((t - 60) / 60) ** 2) for t in range(0, 121, 4)]
            by = base - 57
        o += P(pts, INK, 2.4)
        o += C(cx, by, 11, c, INK, 1.4)
        o += A(cx + 16, by - 26, cx + 50, by - 26, MUT, 1.6, 8, dash='4 3')
        o += T(cx, 240, name, 16, c, 'middle', 'bold') + T(cx, 264, msg, 14, INK, 'middle')
    o += T(225, 310, '挫屈＝筆直的平衡，從「山谷」變成「山頂」', 15, KEY, 'middle', 'bold')
    o += T(225, 336, '載重小於 *P*_{cr}：山谷；等於：平地；大於：山頂', 14, INK, 'middle')
    o += L(450, 20, 450, 390, GRID, 1.5)
    # (b) P–δ
    pl = Plot(510, 60, 330, 260, 0, 1.0, 0, 1.15)
    o += T(675, 28, '(b) 載重–側向變位', 16, INK, 'middle', 'bold')
    o += pl.axes([], [1.0], 'δ', '*P*/*P*_{e}', grid=False, yfmt=lambda v: '1')
    o += P([pl.pt(0, 0), pl.pt(0, 1.0), pl.pt(1.0, 1.0)], AC, 3.2, dash='7 4')
    o += T(pl.X(0.5), pl.Y(1.0) - 10, '理想直柱：到 *P*_{e} 才突然分歧', 14, AC, 'middle', 'bold')
    d0 = 0.04
    pts = [pl.pt(min(1.0, d0 / (1 - p)), p) for p in [i / 200 for i in range(0, 199)] if d0 / (1 - p) <= 1.0]
    o += P(pts, COMP, 3.2)
    o += T(pl.X(0.45), pl.Y(0.6), '真實柱（初始彎曲 δ_{0}）：', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.45), pl.Y(0.6) + 20, 'δ = δ_{0} / (1 − *P*/*P*_{e})', 14, COMP, 'start', 'bold')
    o += T(pl.X(0.45), pl.Y(0.6) + 40, '一開始就在變形、越來越快', 14, INK, 'start')
    return svg(W, H, o, '分歧與穩定')


def fig7_2():
    W, H = 900, 500
    o = T(230, 28, '(a) 切開歪掉的柱子：內力矩 ＝ 推歪力矩', 16, INK, 'middle', 'bold')
    x0, yt, yb, amp = 120, 110, 420, 46
    L_ = yb - yt
    def X(yy):
        return x0 + amp * math.sin(math.pi * (yb - yy) / L_)
    pts = [(X(yt + L_ * i / 100), yt + L_ * i / 100) for i in range(101)]
    o += L(x0, yt, x0, yb, MUT, 1.2, '5 4') + P(pts, STEEL, 8)
    o += pin(x0, yb + 2) + P([(x0, yt - 2), (x0 - 11, yt - 18), (x0 + 11, yt - 18)], INK, 1.5, fill='#fff', close=True)
    o += A(x0, yt - 70, x0, yt - 22, COMP, 3, 12) + T(x0 + 10, yt - 46, '*P*', 17, COMP, 'start', 'bold')
    # 切口 (下半自由體)
    yc = yt + L_ * 0.38
    xc = X(yc)
    o += L(xc - 26, yc, xc + 26, yc, INK, 1.4, '3 3')
    o += dim(x0, yc + 4, xc, yc + 4, '', KEY) + T((x0 + xc) / 2, yc + 26, '*y*', 16, KEY, 'middle', 'bold')
    # 右側：下半段 FBD
    ox = 300
    pts2 = [(ox + (X(yy) - x0), yy) for yy in [yc + (yb - yc) * i / 60 for i in range(61)]]
    o += P(pts2, STEEL, 8) + L(ox, yc - 10, ox, yb, MUT, 1.2, '5 4')
    o += A(ox, yb + 60, ox, yb + 10, COMP, 3, 12) + T(ox + 10, yb + 46, '*P*（支承反力）', 15, COMP, 'start', 'bold')
    xcc = ox + (xc - x0)
    o += A(xcc, yc - 58, xcc, yc - 6, COMP, 3, 12) + T(xcc + 10, yc - 34, '*P*（上半段壓下來）', 15, COMP, 'start', 'bold')
    # 內力矩（弧箭頭）
    arc = [(xcc + 34 * math.cos(math.radians(a)), yc + 34 * math.sin(math.radians(a))) for a in range(200, 340, 6)]
    o += curve_arrow(arc, AC, 2.6, 10)
    o += T(xcc + 40, yc + 4, '*M*', 16, AC, 'start', 'bold')
    o += dim(ox, yb + 2, xcc, yb + 2, '', KEY) if False else ''
    o += R(250, 160, 190, 74, KEY2, KEY, 1.3, 8) if False else ''
    o += T(345, 330, '兩個 *P* 錯開 *y*', 14.5, INK, 'start')
    o += T(345, 352, '→ 力偶 *P*·*y*', 14.5, COMP, 'start', 'bold')
    o += T(345, 374, '→ 由內力矩 *M* 抵抗', 14.5, AC, 'start', 'bold')
    o += L(470, 20, 470, 490, GRID, 1.5)
    # (b) 推導框
    bx = 490
    o += T(690, 28, '(b) 三行推出 Euler', 16, INK, 'middle', 'bold')
    rows = [('① 推歪力矩', '*M* = *P*·*y*', COMP),
            ('② 拉回力矩（梁的曲率）', '*M* = −*EI*·*y*″', AC),
            ('③ 打平', '*EI y*″ + *P y* = 0', KEY),
            ('④ 解是正弦波', '*y* = *a*·sin(*kx*)，*k*² = *P*/*EI*', INK),
            ('⑤ 兩端 *y* = 0：剛好半個波', '*kL* = π', INK)]
    for i, (a, b, c) in enumerate(rows):
        y = 60 + i * 66
        o += R(bx, y, 390, 56, '#fff', c, 1.6, 8)
        o += T(bx + 12, y + 22, a, 14.5, c, 'start', 'bold')
        o += T(bx + 12, y + 45, b, 15.5, INK, 'start')
    o += R(bx, 396, 390, 54, KEY2, KEY, 1.8, 8)
    o += T(bx + 195, 430, '*P*_{e} = π²*EI* / *L*²', 20, KEY, 'middle', 'bold')
    return svg(W, H, o, 'Euler 推導')


def fig7_3():
    W, H = 900, 360
    o = T(225, 28, '(a) 半波長＝挫屈的物理長度', 16, INK, 'middle', 'bold')
    yt, yb = 70, 300
    for i, (n, lab) in enumerate(((1, '無側撐'), (2, '中央一道側撐'), (3, '兩道側撐'))):
        x0 = 90 + i * 125
        pts = [(x0 + 34 * math.sin(n * math.pi * k / 100), yt + (yb - yt) * k / 100) for k in range(101)]
        o += L(x0, yt, x0, yb, MUT, 1.2, '5 4') + P(pts, COMP, 3.6)
        o += C(x0, yt, 5, '#fff', INK, 1.5) + C(x0, yb, 5, '#fff', INK, 1.5)
        for j in range(1, n):
            yy = yt + (yb - yt) * j / n
            o += L(x0 - 26, yy, x0 + 2, yy, AC, 3) + T(x0 - 30, yy + 5, '側撐', 14, AC, 'end')
        o += T(x0, yb + 26, lab, 14, INK, 'middle', 'bold')
        o += T(x0, yb + 48, f'*P* = {n * n}*P*_{{e}}', 15, KEY, 'middle', 'bold')
    o += L(450, 20, 450, 345, GRID, 1.5)
    o += T(675, 28, '(b) 迴轉半徑 *r*：面積「集中」在哪裡', 16, INK, 'middle', 'bold')
    # 兩片薄片
    cx, cy = 675, 170
    o += L(cx - 180, cy, cx + 180, cy, MUT, 1.2, '5 4') + T(cx + 182, cy + 5, '中性軸', 14, MUT, 'start')
    o += R(cx - 120, cy - 80, 240, 14, STEEL, INK, 1.2) + R(cx - 120, cy + 66, 240, 14, STEEL, INK, 1.2)
    o += dim(cx + 140, cy, cx + 140, cy - 73, '', KEY) + T(cx + 150, cy - 34, '*r*', 17, KEY, 'start', 'bold')
    o += dim(cx + 140, cy, cx + 140, cy + 73, '', KEY) + T(cx + 150, cy + 42, '*r*', 17, KEY, 'start', 'bold')
    o += T(cx - 128, cy - 66, '*A*/2', 15, INK, 'end') + T(cx - 128, cy + 80, '*A*/2', 15, INK, 'end')
    o += T(cx, 290, '整個面積 *A* 分成兩半放在 ±*r*：*I* = *A*·*r*²', 15, INK, 'middle')
    o += T(cx, 318, '⇒ *r* = √(*I*/*A*)；*KL*/*r* ＝ 柱有多長 ÷ 斷面有多「胖」', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '半波長與迴轉半徑')


def fig7_4():
    W, H = 900, 400
    pl = Plot(90, 50, 500, 290, 0, 250, 0, 4.0)
    o = pl.axes([0, 50, 100, 150, 200, 250], [0, 1, 2, 2.52, 3.52, 4], '*KL*/*r*', '應力（tf/cm²）',
                yfmt=lambda v: {2.52: 'A36', 3.52: 'A572'}.get(v, f(v)))
    fe = lambda s: math.pi ** 2 * E / s ** 2
    for Fy, c, lab in ((2.52, TEN, 'A36 *F*_{y}'), (3.52, WARN, 'A572 Gr.50 *F*_{y}')):
        o += pl.hline(Fy, 0, math.pi * math.sqrt(E / Fy), c, 3, None)
        o += T(pl.X(4), pl.Y(Fy) - 8, lab, 14.5, c, 'start', 'bold')
    o += pl.curve(fe, 60, 250, AC, 3.4)
    s1 = math.pi * math.sqrt(E / 2.52)
    o += R(pl.X(s1), pl.y0, pl.X(250) - pl.X(s1), pl.h, AC2, None, 0, op=0.6)
    o += T(pl.X(185), pl.Y(2.2), '細長柱區：兩種鋼材', 15, AC, 'middle', 'bold')
    o += T(pl.X(185), pl.Y(2.2) + 22, '強度完全相同', 15, AC, 'middle', 'bold')
    o += T(pl.X(185), pl.Y(2.2) + 44, '（Euler 裡沒有 *F*_{y}）', 14, INK, 'middle')
    o += T(pl.X(110), pl.Y(3.7), '*F*_{e} = π²*E*/(*KL*/*r*)²', 15, AC, 'start', 'bold')
    o += L(610, 20, 610, 380, GRID, 1.5)
    # (b) 同面積不同 I
    o += T(755, 34, '同樣的鋼量（面積相同）', 15, INK, 'middle', 'bold')
    sc = 3.0
    o += C(690, 150, 5 * sc, STEEL, INK, 1.4)
    o += T(690, 205, '實心 *D* = 10', 14, INK, 'middle') + T(690, 228, '*I* = 491', 15, INK, 'middle', 'bold')
    o += C(815, 150, 15 * sc, STEEL, INK, 1.4) + C(815, 150, 14.14 * sc, '#fff', INK, 1.2)
    o += T(815, 222, '圓管 *D* = 30', 14, INK, 'middle') + T(815, 245, '*I* = 8345', 15, KEY, 'middle', 'bold')
    o += T(755, 290, '材料往外攤 → *I* 大 17 倍', 15, KEY, 'middle', 'bold')
    o += T(755, 314, '→ 挫屈強度大 17 倍', 15, KEY, 'middle', 'bold')
    o += T(755, 346, '（面積單位 cm²，均為 78.5）', 14, MUT, 'middle')
    return svg(W, H, o, '讀公式')


def fig7_5():
    W, H = 900, 330
    o = ''
    titles = [('彎曲挫屈', 'H 型、箱型、圓管', '整個斷面平移'), ('扭轉挫屈', '十字形、背對背雙角鋼', '繞軸心旋轉'), ('彎扭挫屈', '單角鋼、T 型、槽鋼', '邊平移邊旋轉')]
    for i, (t, ex, mv) in enumerate(titles):
        cx, cy = 150 + i * 300, 150
        o += T(cx, 30, t, 17, (AC, WARN, COMP)[i], 'middle', 'bold')
        if i == 0:
            shape = [(-50, -60), (50, -60), (50, -48), (6, -48), (6, 48), (50, 48), (50, 60), (-50, 60), (-50, 48), (-6, 48), (-6, -48), (-50, -48)]
            mv_ = lambda p: (p[0] + 34, p[1])
        elif i == 1:
            w = 7
            shape = [(-w, -60), (w, -60), (w, -w), (60, -w), (60, w), (w, w), (w, 60), (-w, 60), (-w, w), (-60, w), (-60, -w), (-w, -w)]
            a = math.radians(22)
            mv_ = lambda p: (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))
        else:
            t_ = 10
            shape = [(-40, -60), (-40 + t_, -60), (-40 + t_, 60 - t_), (60, 60 - t_), (60, 60), (-40, 60)]
            a = math.radians(-18); sx, sy = -40 + t_ / 2, 60 - t_ / 2
            def mv_(p, a=a, sx=sx, sy=sy):
                x, y = p[0] - sx, p[1] - sy
                return (sx + x * math.cos(a) - y * math.sin(a) + 26, sy + x * math.sin(a) + y * math.cos(a) - 6)
        o += P([(cx + x, cy + y) for x, y in shape], MUT, 1.6, fill='none', close=True, dash='5 4')
        o += P([(cx + mv_(p)[0], cy + mv_(p)[1]) for p in shape], (AC, WARN, COMP)[i], 2.4, fill=(AC2, WARN2, COMP2)[i], close=True)
        if i == 2:
            o += C(cx - 35, cy + 55, 4, INK, None) + T(cx - 48, cy + 80, 'S（剪力中心）', 14, INK, 'start')
            o += C(cx - 12, cy + 32, 4, KEY, None) + T(cx - 2, cy + 22, 'C', 14, KEY, 'start', 'bold')
        o += T(cx, 250, mv, 15, INK, 'middle', 'bold') + T(cx, 276, ex, 14, MUT, 'middle')
    o += T(450, 316, '虛線＝原斷面；決定用哪一種的是「斷面的對稱性與扭轉勁度」，不是長度', 14.5, KEY, 'middle', 'bold')
    return svg(W, H, o, '三種挫屈模式')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4, 'fig7_5': fig7_5}
