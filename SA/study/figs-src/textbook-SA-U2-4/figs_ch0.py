# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟流程。"""
from plot import *  # noqa

TEAL = '#00838f'

SEEDS = [
    ('S1', '勁度＝推一單位所需的力', KEY),
    ('S2', '彈簧律 *F* = *k*·Δ', TEN),
    ('S3', '懸臂端：*L*^{3}/3、*L*^{2}/2、*L*（÷*EI*）', AC),
    ('S4', '投影：伸長 = *c*·*u* + *s*·*v*', TEAL),
    ('S5', '先鎖住，再放開', WARN),
    ('S6', '沒外力的自由度自己找平衡', COMP),
]

# (種子序號, 章, 長出來的東西)
KIDS = [
    (0, '1', '彈簧元素 *k*[1, −1; −1, 1]、對稱性'),
    (0, '3', '組裝：同一節點的勁度相加'),
    (1, '1', '桁架 *EA*/*L*、扭轉 *GJ*/*L*'),
    (1, '7', '旋轉彈簧、彈簧支承併入 [*K*]'),
    (2, '2', '梁元素 12、6、4、2'),
    (2, '2', '柱側移 12*EI*/*L*^{3}、3*EI*/*L*^{3}'),
    (3, '4', '*c*^{2}、*cs*、*s*^{2}，[*T*]^{T}[*k*][*T*]'),
    (3, '7', '格床：彎曲與扭轉互換'),
    (4, '5', '{*P*} = −{FEM}、回代加固端力'),
    (4, '5', '製造誤差、溫度、支承沉陷'),
    (5, '6', '靜態凝縮 *K*^{*}、修正勁度 3*EI*/*L*'),
    (5, '6', '門型剛架側向勁度 84*EI*/5*L*^{3}'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 16, 372, 48
    kx, kw, kh = 488, 396, 34
    sy0, sgap = 66, 78
    ky0, kgap = 62, 39.5
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 30
    o = T(sx + sw / 2, 36, '6 顆種子（要記的）', 17, KEY, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 30, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 60, y + 30, txt, 15, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 66, kh, STEEL2, None, 0, 7)
        o += T(kx + 33, y + 22, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 76, y + 22.5, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '單位位移的變形', AC),
             ('②', '白話', '它在描述什麼', TEN),
             ('③', '推導', '從種子出發', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
             ('⑤', '給背標籤', '考卷給不給', MUT),
             ('⑥', '重建卡', '30 秒重畫', KEY)]
    bw, gap = 128, 26
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 14 + i * (bw + gap)
        o += R(x, 40, bw, 112, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 118, s, 14, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 3, 96, x + bw + gap - 3, 96, INK, 2.2, 10)
    o += T(W / 2, 186, '全書每一條公式都照這六步走——讀久了，腦袋會自己照這個順序想', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
