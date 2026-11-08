# -*- coding: utf-8 -*-
"""第 0 章：種子公式家族樹、五步驟流程。"""
from plot import *  # noqa

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '應力 = 力 ÷ 面積', TEN),
    ('S2', '純剪降伏 τ_{y} = *F*_{y}/√3 ≈ 0.6*F*_{y}', WARN),
    ('S3', '力要走路：*U* = 1 − x̄/*L*', TEN),
    ('S4', '推歪力矩 *P*·*y* = 拉回力矩 *EI*·*y*″', COMP),
    ('S5', '*K* = 兩反曲點的距離 ÷ *L*', COMP),
    ('S6', 'λ_{c}² = *F*_{y} / *F*_{e}', KEY),
    ('S7', '數字錨點 0.877、1.5、½、5/3→23/12', KEY),
]

# (seed index, 章, 推出來的東西)
KIDS = [
    (0, '2', '*F*_{y}*A*_{g}、*F*_{u}*A*_{e}（兩種破壞取小）'),
    (0, '3', '扣孔 *A*_{n}、錯列 *s*^{2}/4*g*'),
    (0, '5', '塊狀剪力兩式（面積 × 應力）'),
    (1, '5', '所有的 0.6：塊剪、腹板剪、銲道'),
    (2, '4', '*A*_{e} = *UA*_{n}、最經濟接合長度'),
    (3, '7', '*P*_{e} = π²*EI*/(*KL*)²、*F*_{e}、*r*'),
    (3, '9', '切線模數 *E*_{t}、有效 *I*_{e}'),
    (3, '11', '板的挫屈 → 寬厚比 *b*/*t*'),
    (4, '8', '*K* = 0.5／0.7／1／2、*G* 值、側移'),
    (5, '10', 'λ_{c} 定義、1.5 ⇔ *KL*/*r* = 134'),
    (5, '10', '*C*_{c} = √(2π²*E*/*F*_{y})'),
    (6, '10', '0.658、0.877/λ²、CRC 拋物線、FS'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 20, 330, 46
    kx, kw, kh = 470, 410, 34
    sy0, sgap = 70, 70
    ky0, kgap = 62, 40.5
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 40
    o = T(sx + sw / 2, 36, '7 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 29, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 60, y + 29, txt, 14.5, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 62, kh, STEEL2, None, 0, 7)
        o += T(kx + 31, y + 22, f'第{ch}章', 12, MUT, 'middle', 'bold')
        o += T(kx + 72, y + 22.5, txt, 13.5, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 190
    steps = [('①', '看圖', '力向量／自由體圖', AC),
             ('②', '第一性原理', '平衡、變形、材料', TEN),
             ('③', '三步推導', '每一步都有圖', COMP),
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


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
