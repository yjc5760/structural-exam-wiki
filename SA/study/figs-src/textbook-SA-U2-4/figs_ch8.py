# -*- coding: utf-8 -*-
"""第 8 章：總整理（種子 → 公式 → 考題、解題流程）。"""
from figs_common import *  # noqa

SEEDS = [('S1', '推一下、量力', KEY), ('S2', '彈簧律 *F*＝*k*Δ', TEN), ('S3', '懸臂 *L*^{3}/3、*L*^{2}/2、*L*', AC),
         ('S4', '投影 *e*＝*cu*＋*sv*', TEAL), ('S5', '先鎖住，再放開', WARN), ('S6', '放手的自由度力＝0', COMP)]
KIDS = [  # (種子, 章, 公式, 考題)
    (0, 3, '[*K*] 每一行＝一次實驗；組裝相加', '全部 13 題'),
    (1, 1, '*EA*/*L*、*GJ*/*L*、*k*_{θ}[1,−1;−1,1]', '2004-4、2019-4、2025-4'),
    (2, 2, '12、6、4、2（梁元素）', '2004-4、2008-4、2018-2…'),
    (2, 5, '固端彎矩 *wL*^{2}/12、*PL*/8', '2018-2、2019-4'),
    (3, 4, '*c*^{2}、*cs*、*s*^{2}；[*T*]^{T}[*k*][*T*]', '2009～2013 桁架'),
    (3, 7, '格床：沿軸扭、垂直軸彎', '2025-4'),
    (4, 5, '{*P*}＝−{*f*_{F}}；製造誤差、沉陷', '2011-4、2018-2'),
    (5, 6, '凝縮 *a*−*b*^{2}/*c*；3*EI*/*L*、3*EI*/*L*^{3}', '2019-4'),
    (5, 6, '側向勁度 84/5、塑鉸側推', '2025-1、2024-4'),
]


def fig8_1():
    W = 900
    sx, sw, sh, sy0, sgap = 20, 250, 44, 70, 62
    kx, kw, kh, ky0, kgap = 340, 540, 38, 66, 42
    H = ky0 + kgap * len(KIDS) + 30
    o = T(sx + sw / 2, 40, '6 顆種子', 17, KEY, 'middle', 'bold')
    o += T(kx + kw / 2, 40, '長出來的公式（第幾章）→ 用在哪幾題', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 44, sh, c, None, 0, 10) + R(sx + 28, y, 16, sh, c, None)
        o += T(sx + 22, y + 28, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 54, y + 28, txt, 15, INK, 'start', 'bold')
    for j, (si, ch, txt, ex) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 56, kh, STEEL2, None, 0, 7)
        o += T(kx + 28, y + 25, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 64, y + 25, txt, 14, INK, 'start', 'bold')
        o += T(kx + kw - 10, y + 25, ex, 14, c, 'end', 'bold')
    return svg(W, int(H), o, '種子樹總整理')


def fig8_2():
    W, H = 900, 520
    o = ''
    def bx(x, y, w, h, t1, t2, c, fill='#fff'):
        q = R(x, y, w, h, fill, c, 2, 10)
        q += T(x + w / 2, y + 26, t1, 15, c, 'middle', 'bold')
        if t2:
            q += T(x + w / 2, y + 50, t2, 14, INK, 'middle')
        return q
    cx, w = 290, 320
    steps = [('① 記帳：數自由度', '節點×3 − 支承 − 不伸縮 − 剛桿（第 3 章）', KEY),
             ('② 寫元素卡', '代號＋2×2；鉸端先凝縮成 3（第 2、6 章）', AC),
             ('③ 對號入座組 [*K*]', '同格相加；查對稱、對角正（第 3 章）', AC),
             ('④ 載重向量（S5）', '{*P*}＝節點力 − 固端力（第 5 章）', WARN)]
    for i, (a, b, c) in enumerate(steps):
        y = 20 + i * 86
        o += bx(cx, y, w, 64, a, b, c)
        if i < 3:
            o += A(cx + w / 2, y + 66, cx + w / 2, y + 84, INK, 2, 9)
    y5 = 20 + 4 * 86
    o += A(cx + w / 2, y5 - 20, 160, y5 + 8, INK, 2, 9) + A(cx + w / 2, y5 - 20, 740, y5 + 8, INK, 2, 9)
    o += T(250, y5 - 4, '題目要「勁度」', 14, MUT, 'end', 'bold') + T(650, y5 - 4, '題目要「位移／內力」', 14, MUT, 'start', 'bold')
    o += bx(20, y5 + 10, 280, 64, '⑤a 凝縮（S6）', '*K*_{aa} − *K*_{ab}*K*_{bb}^{−1}*K*_{ba}（第 6 章）', COMP)
    o += bx(600, y5 + 10, 280, 64, '⑤b 解 {*D*}、回代', '[*k*]{*d*}＋{*f*_{F}}；反力 [*K*_{sf}]{*D*}', COMP)
    o += A(160, y5 + 76, 400, y5 + 102, INK, 2, 9) + A(740, y5 + 76, 500, y5 + 102, INK, 2, 9)
    o += bx(250, y5 + 104, 400, 50, '⑥ 檢查：節點平衡、整體平衡、極限（0、∞）', '', TEN, '#e8f5e9')
    return svg(W, H, o, '矩陣法解題流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
