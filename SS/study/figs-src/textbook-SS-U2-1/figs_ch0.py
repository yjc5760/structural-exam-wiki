# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、五步驟、全書地圖（一條因果鏈）。"""
from plot import *  # noqa
from calcs import *  # noqa

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '鋼是兩段線＋平面保持平面', TEN),
    ('S2', '中性軸由 Σ*F* = 0 決定', AC),
    ('S3', '彎矩 = 力偶 = 力 × 力臂', AC),
    ('S4', '塑性鉸：*M* 卡在 *M*_{p} 還能轉', COMP),
    ('S5', '虛功：外力做的功 = 鉸吸收的功', COMP),
    ('S6', '機構法高估、靜力法低估', KEY),
]

# (seed index, 章, 長出來的東西)
KIDS = [
    (0, '1', '最外緣先到 *F*_{y} → *M*_{y} = *F*_{y}*S*_{min}'),
    (1, '1', 'ENA：一次矩為零 → 形心'),
    (2, '1', '*I*_{x} = Σ(*bh*^{3}/12 + *Ad*^{2})、*S* = *I*/*c*'),
    (1, '2', 'PNA：上下面積各 *A*/2'),
    (2, '2', '*Z* = (*A*/2)(ȳ_{t} + ȳ_{c})、*M*_{p} = *F*_{y}*Z*'),
    (0, '2', '*M*_{p} 是漸近線、*f* = *Z*/*S*'),
    (2, '3', 'H 型 *Z*_{x} 封閉式、圓管 (*D*^{3} − *d*^{3})/6'),
    (3, '4', '鉸的位置、鉸數 = 靜不定度 + 1'),
    (3, '4', '前提：結實斷面＋充分側撐'),
    (4, '5', '8、16、6、8 與 11.66 *M*_{p}/*L*^{2}'),
    (5, '5', 'd*w*/d*x* = 0 → 鉸距簡支端 0.414*L*'),
    (5, '6', '上下限、唯一性、|*M*| ≤ *M*_{p} 檢查'),
    (4, '6', '連續梁、門型剛架的三種機構'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 16, 330, 50
    kx, kw, kh = 462, 424, 34
    sy0, sgap = 72, 84
    ky0, kgap = 62, 39
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 30
    o = T(sx + sw / 2, 36, '6 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 31, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 60, y + 31, txt, 15, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 64, kh, STEEL2, None, 0, 7)
        o += T(kx + 32, y + 22, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 72, y + 22.5, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 190
    steps = [('①', '看圖', '應力塊／機構圖', AC),
             ('②', '第一性原理', '平衡、平面、能量', TEN),
             ('③', '三步推導', '每一步一件事', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
             ('⑤', '30 秒重建卡', '空白紙重畫一次', PUR)]
    bw, gap = 152, 30
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 14 + i * (bw + gap)
        o += R(x, 40, bw, 110, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 112, s, 14, INK, 'middle')
        if i < 4:
            o += A(x + bw + 3, 95, x + bw + gap - 3, 95, INK, 2.2, 10)
    o += T(W / 2, 180, '全書每一條公式都照這五步走——讀久了，腦袋會自己照這個順序想', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的五個步驟')


def _mini_ss(x, y):
    """小小的 σ–ε 兩段線圖示。"""
    o = A(x, y + 50, x + 120, y + 50, INK, 1.4, 7) + A(x, y + 50, x, y - 8, INK, 1.4, 7)
    o += P([(x, y + 50), (x + 28, y + 6), (x + 112, y + 6)], TEN, 3)
    o += T(x - 6, y + 10, '*F*_{y}', 14, TEN, 'end')
    o += T(x + 120, y + 70, 'ε', 14, MUT, 'end')
    return o


def _mini_section(x, y):
    """小小的應力塊：上壓下拉兩塊矩形。"""
    o = R(x + 30, y - 8, 12, 64, STEEL3, INK, 1)
    o += R(x + 50, y - 8, 46, 30, COMP2, COMP, 1.4) + R(x + 50, y + 26, 46, 30, TEN2, TEN, 1.4)
    o += L(x + 22, y + 24, x + 104, y + 24, KEY, 1.6, '5 3')
    o += A(x + 80, y + 7, x + 112, y + 7, COMP, 2, 8) + A(x + 112, y + 41, x + 80, y + 41, TEN, 2, 8)
    return o


def _mini_hinge(x, y):
    o = L(x, y + 30, x + 120, y + 30, INK, 5)
    o += C(x + 60, y + 30, 9, '#fff', COMP, 2.6)
    o += curve_arrow([(x + 38, y + 6), (x + 60, y - 2), (x + 82, y + 6)], COMP, 1.8, 8)
    o += T(x + 60, y + 64, '*M* = *M*_{p}', 14, COMP, 'middle', 'bold')
    return o


def _mini_mech(x, y):
    o = L(x, y + 16, x + 124, y + 16, STEEL, 1.4, '4 3')
    o += P([(x, y + 16), (x + 52, y + 46), (x + 124, y + 16)], COMP, 3)
    o += C(x + 52, y + 46, 6, '#fff', COMP, 2.2) + C(x + 124, y + 16, 6, '#fff', COMP, 2.2)
    for i in range(7):
        xx = x + 6 + i * 18
        o += A(xx, y - 10, xx, y + 8, WARN, 1.4, 7)
    return o


def fig0_3():
    W, H = 900, 330
    stages = [('材料', '鋼的兩段線', 'S1', '第 1 章', _mini_ss, TEN),
              ('斷面', '*M*_{y}、*M*_{p}、*Z*', 'S1–S3', '第 1–3 章', _mini_section, AC),
              ('構材', '塑性鉸', 'S4', '第 4 章', _mini_hinge, COMP),
              ('結構', '崩塌載重 *w*_{u}', 'S5、S6', '第 5–6 章', _mini_mech, KEY)]
    bw, gap = 200, 26
    o = ''
    for i, (t, s, sd, ch, fn, c) in enumerate(stages):
        x = 12 + i * (bw + gap)
        o += R(x, 20, bw, 250, '#fff', c, 2.2, 14)
        o += R(x, 20, bw, 44, c, None, 0, 14) + R(x, 50, bw, 14, c, None)
        o += T(x + bw / 2, 50, t, 18, '#fff', 'middle', 'bold')
        o += fn(x + 40, 100)
        o += T(x + bw / 2, 206, s, 16, INK, 'middle', 'bold')
        o += T(x + bw / 2, 232, f'種子 {sd}', 14, c, 'middle', 'bold')
        o += T(x + bw / 2, 256, ch, 14, MUT, 'middle')
        if i < 3:
            o += A(x + bw + 2, 145, x + bw + gap - 2, 145, INK, 2.4, 11)
    o += T(W / 2, 312, '由小到大：一個點降伏 → 一個斷面用完 → 一個鉸會轉 → 夠多的鉸讓結構變成機構', 15, MUT, 'middle')
    return svg(W, H, o, '全書地圖：材料到結構的因果鏈')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
