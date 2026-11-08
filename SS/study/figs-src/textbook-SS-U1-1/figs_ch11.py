# -*- coding: utf-8 -*-
"""第 11 章：局部挫屈與寬厚比。"""
from plot import *  # noqa
from calcs import E, plate_coef
import math


def _plate(ox, oy, w, h, stiff):
    """俯視板件，受壓方向為水平；stiff=True 上下兩邊有支承，False 只有下邊。"""
    o = R(ox, oy, w, h, '#fafafa', INK, 1.2)
    o += L(ox, oy + h, ox + w, oy + h, AC, 5)
    if stiff:
        o += L(ox, oy, ox + w, oy, AC, 5)
        nb = int(round(w / h))
        for i in range(nb):
            cx = ox + (i + 0.5) * w / nb
            for r in (0.12, 0.25, 0.38):
                o += f'<ellipse cx="{f(cx)}" cy="{f(oy + h / 2)}" rx="{f(r * w / nb)}" ry="{f(r * h)}" fill="none" stroke="{COMP if i % 2 == 0 else WARN}" stroke-width="1.6"/>'
    else:
        for r in (0.2, 0.4, 0.6, 0.8):
            pts = [(ox + w * u, oy + h * (1 - r * math.sin(math.pi * u))) for u in [k / 60 for k in range(61)]]
            o += P(pts, COMP, 1.6)
    o += A(ox - 40, oy + h / 2, ox - 6, oy + h / 2, INK, 2.4, 10) + A(ox + w + 40, oy + h / 2, ox + w + 6, oy + h / 2, INK, 2.4, 10)
    return o


def fig11_1():
    W, H = 900, 400
    o = T(225, 28, '(a) 加勁肢：兩邊都有人扶　*k* ≈ 4', 16, TEN, 'middle', 'bold')
    o += _plate(60, 80, 330, 110, True)
    o += T(225, 220, '起成一格一格、長約 *b* 的小波', 14.5, INK, 'middle')
    o += T(225, 244, '例：H 型鋼腹板、箱型柱壁', 14.5, MUT, 'middle')
    o += L(450, 20, 450, 270, GRID, 1.5)
    o += T(675, 28, '(b) 非加勁肢：一邊自由　*k* ≈ 0.425', 16, COMP, 'middle', 'bold')
    o += _plate(510, 80, 330, 110, False)
    o += T(675, 76, '自由邊（沒有人扶）', 14, COMP, 'middle')
    o += T(675, 220, '自由邊整片翻出，一個長波', 14.5, INK, 'middle')
    o += T(675, 244, '例：H 型鋼翼板的一半、角鋼的肢', 14.5, MUT, 'middle')
    o += R(60, 290, 780, 96, KEY2, KEY, 1.4, 8)
    o += T(450, 318, '柱：*F*_{e} = π²*E* / (*KL*/*r*)²　　⇔　　板：*F*_{cr} = *k*π²*E* / [12(1−ν²)(*b*/*t*)²]', 16, KEY, 'middle', 'bold')
    o += T(450, 348, '*b*/*t* 就是板的細長比；*k* 就是板的 *K*（支承條件）；藍色粗線＝有支承的邊', 15, INK, 'middle')
    o += T(450, 372, '*k* 差約 10 倍 → 臨界應力差 10 倍 → 限值差 √10 ≈ 3 倍', 15, INK, 'middle')
    return svg(W, H, o, '加勁肢與非加勁肢')


def fig11_2():
    W, H = 900, 420
    Fy = 2.52
    pl = Plot(90, 50, 600, 300, 0, 70, 0, 6)
    o = pl.axes([0, 10, 20, 30, 40, 50, 60, 70], [0, 1, 2, 2.52, 3, 4, 5, 6], '*b*/*t*', '*F*_{cr}（tf/cm²）', yfmt=lambda v: '*F*_{y}' if v == 2.52 else f(v))
    o += pl.hline(Fy, 0, 70, TEN, 2.6, None)
    sq = math.sqrt(E / Fy)
    for k, c, code, lab in ((0.425, COMP, 0.56, '非加勁 *k* = 0.425'), (4.0, AC, 1.49, '加勁 *k* = 4')):
        fn = lambda bt, k=k: k * math.pi ** 2 * E / (12 * (1 - 0.09) * bt ** 2) if bt > 0 else 99
        o += pl.curve(fn, 3, 70, c, 3.2)
        bth = plate_coef(k) * sq
        o += pl.dot(bth, Fy, c, 6)
        o += T(pl.X(bth) + 6, pl.Y(Fy) - 10, f'理論 {bth:.1f}', 14, c, 'start', 'bold')
        bc = code * sq
        o += pl.vline(bc, 0, Fy, c, 1.8, '6 4')
        o += T(pl.X(bc), pl.Y(0) + 40 + (0 if k < 1 else 0), f'規範 λ_{{r}} = {bc:.1f}', 14, c, 'middle', 'bold')
    o += T(pl.X(13), pl.Y(4.6), '非加勁', 15, COMP, 'start', 'bold')
    o += T(pl.X(48), pl.Y(3.7), '加勁', 15, AC, 'start', 'bold')
    o += R(705, 80, 185, 190, '#fff', KEY, 1.4, 8)
    for i, s in enumerate(('令 *F*_{cr} = *F*_{y}：', '*b*/*t* = 0.95√*k*·√(*E*/*F*_{y})', '', '非加勁：0.62 → 規範 0.56', '加勁：1.90 → 規範 1.49', '', '規範打 8～9 折', '（殘留應力、初始變形）')):
        o += T(797, 104 + i * 22, s, 14, KEY if i in (1, 6) else INK, 'middle', 'bold' if i in (1, 6) else None)
    o += T(450, 410, 'A36；曲線為彈性板挫屈理論值，與 *F*_{y} 線的交點就是「板會先皺還是先降伏」的分界', 14, MUT, 'middle')
    return svg(W, H, o, '板挫屈與寬厚比限值')


def fig11_3():
    W, H = 900, 300
    o = ''
    def hsec(cx, cy):
        r = ''
        r += L(cx - 70, cy - 70, cx, cy - 70, COMP, 7) + L(cx, cy - 70, cx + 70, cy - 70, COMP, 7)
        r += L(cx - 70, cy + 70, cx, cy + 70, COMP, 7) + L(cx, cy + 70, cx + 70, cy + 70, COMP, 7)
        r += L(cx, cy - 66, cx, cy + 66, AC, 6)
        return r
    def box(cx, cy):
        return R(cx - 60, cy - 70, 120, 140, 'none', AC, 7)
    def ang(cx, cy):
        return L(cx - 50, cy - 70, cx - 50, cy + 70, COMP, 7) + L(cx - 50, cy + 70, cx + 70, cy + 70, COMP, 7)
    def tee(cx, cy):
        return L(cx - 70, cy - 70, cx + 70, cy - 70, COMP, 7) + L(cx, cy - 66, cx, cy + 70, COMP, 6)
    items = [(hsec, 'H 型鋼', '翼板半邊：非加勁', '腹板：加勁'), (box, '箱型', '四壁：全部加勁', ''), (ang, '角鋼', '兩肢：非加勁', ''), (tee, 'T 型鋼', '全部：非加勁', '')]
    for i, (fn, name, a, b) in enumerate(items):
        cx = 115 + i * 225
        o += fn(cx, 120)
        o += T(cx, 30, name, 16, INK, 'middle', 'bold')
        o += T(cx, 230, a, 14.5, COMP if '非' in a else AC, 'middle', 'bold')
        if b:
            o += T(cx, 254, b, 14.5, AC, 'middle', 'bold')
    o += T(450, 288, '紅＝非加勁（一邊自由）、藍＝加勁（兩邊都連著別的板）', 14.5, MUT, 'middle')
    return svg(W, H, o, '斷面元件分類')


ALL = {'fig11_1': fig11_1, 'fig11_2': fig11_2, 'fig11_3': fig11_3}
