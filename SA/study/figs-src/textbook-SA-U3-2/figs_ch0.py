# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟流程。"""
from figs_common import *  # noqa

SEEDS = [
    ('S1', '懸臂端：δ = *V*ℓ^{3}/3*EI*', AC),
    ('S2', '並聯加 *k*、串聯加 Δ', TEN),
    ('S3', '切一刀：切面以上外力 = Σ柱剪力', COMP),
    ('S4', '剛性＝刪掉自由度', WARN),
    ('S5', '反曲點：*M* = 0，可當鉸', TEAL),
    ('S6', '剪力型 vs 撓曲型的變形長相', BROWN),
    ('S7', '剛體轉 θ：距離 *r* 處走 *r*θ', KEY),
]

# (種子序號, 章, 長出來的東西)
KIDS = [
    (0, '1', '柱側移勁度 12*EI*/*h*^{3}'),
    (0, '1', '柱底鉸接 3*EI*/*h*^{3}、挑高柱 *k*/8'),
    (4, '1', '柱端彎矩 6*EI*Δ/*h*^{2} = *Vh*/2'),
    (1, '2', '層勁度 *K* = Σ*k*、Δ_{頂} = Σ*V*/*K*'),
    (2, '2', '層剪力 *V*_{i} = Σ*F*、挑高柱方程式'),
    (3, '2', '剪力建築：每層一個自由度、[*K*_{f}]'),
    (1, '3', '牆＋構架：[*K*] = [*K*_{f}] + [*K*_{w}]'),
    (5, '3', '互制：下部牆扛、上部構架扛'),
    (3, '4', '剛性樓板只剩 *u*、*v*、θ'),
    (6, '4', '剛心、*K*_{θ} = Σ*k* *d*^{2}、各柱位移'),
    (4, '5', '范倫迪爾：中點放鉸、變靜定'),
    (2, '5', '弦桿軸力 *N* = ±*M*/*h*、節點平衡'),
    (6, '6', '連梁轉角 γ = (*L*/*e*)θ'),
    (1, '6', '層間位移依層剪力比例分配'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 382, 48
    kx, kw, kh = 494, 392, 34
    sy0, sgap = 66, 82
    ky0, kgap = 62, 41
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 26
    o = T(sx + sw / 2, 36, '7 顆種子（要記的）', 17, KEY, 'middle', 'bold')
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
    steps = [('①', '看圖', '變形或切面圖', AC),
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
