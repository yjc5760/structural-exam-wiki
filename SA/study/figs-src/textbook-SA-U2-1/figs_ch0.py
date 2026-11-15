# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟流程。"""
from sa_draw import *  # noqa

SEEDS = [
    ('S1', '平衡：切開就要 ΣF = 0、ΣM = 0', FOR),
    ('S2', '功 = 三角形面積：*U* = ½·力·變形', PUR),
    ('S3', '材料律：力 = 勁度×變形（含轉折）', LOAD),
    ('S4', '卡氏：∂*U*/∂*P* = Δ', MOM),
    ('S5', '疊加：*M* = *M*_{0} + *P*·*m*', DEF),
    ('S6', '直線×任意 = 面積×形心縱距', INK),
]

# (seed index, 章, 推出來的東西)
KIDS = [
    (0, '3', '靜不定度 *n*、基本結構不可成機構'),
    (0, '4', '分段彎矩 *M*(*x*)、Macaulay 括號'),
    (1, '1', '彎曲 ∫*M*^{2}/2*EI*、軸力 Σ*N*^{2}*L*/2*EA*'),
    (1, '1', '剪力、扭轉 ∫κ*V*^{2}/2*GA*、∫*T*^{2}/2*GJ*'),
    (2, '1', '彈簧 *R*^{2}/2*k*（*EI*、*EA*、*k* 從這裡來）'),
    (2, '7', '纜索 *N* < 0 ⇒ *N* = 0、極限機構'),
    (3, '2', '虛設力求轉角／位移'),
    (3, '3', '最小功法 ∂*U*/∂*R* = 0'),
    (3, '3', '支承沉陷 ∂*U*/∂*R* = δ'),
    (3, '5', '固端彎矩 *PL*/8、*wL*^{2}/12、*Pab*^{2}/*L*^{2}'),
    (4, '2', '單位力法 δ = ∫*mM*/*EI* *dx* + Σ*nNL*/*EA*'),
    (4, '3', '柔度式 δ_{10} + *R*·*f*_{11} = 0'),
    (5, '4', '圖乘表 *L*/3、*L*/6、*L*/2'),
    (5, '4', '拋物線面積 2/3、形心 3/8'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 372, 50
    kx, kw, kh = 488, 400, 32
    sy0, sgap = 80, 96
    ky0, kgap = 62, 41
    H = 70 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 20
    o = T(sx + sw / 2, 36, '6 顆種子（要記的）', 18, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 18, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.4, 10)
        o += R(sx, y, 50, sh, c, None, 0, 10) + R(sx + 32, y, 18, sh, c, None)
        o += T(sx + 25, y + 31, sid, 16, '#fff', 'middle', 'bold')
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
        o += T(kx + 74, y + 22, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '彎矩圖／能量圖', DEF),
             ('②', '白話', '它在描述什麼', PUR),
             ('③', '推導', '從種子出發', MOM),
             ('④', '極限檢查', '代 0、代 ∞', FOR),
             ('⑤', '給背標籤', '考卷給不給', LOAD),
             ('⑥', '重建卡', '空白紙重畫', INK)]
    bw, gap = 126, 24
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 10 + i * (bw + gap)
        o += R(x, 36, bw, 112, '#fff', c, 2.2, 12)
        o += R(x, 36, bw, 42, c, None, 0, 12) + R(x, 62, bw, 16, c, None)
        o += T(x + bw / 2, 64, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 112, s, 14, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 2, 92, x + bw + gap - 2, 92, INK, 2, 9)
    o += T(W / 2, 184, '全書每一條公式都照這六步走——讀久了，拿到新公式也會先問：圖在哪？從哪顆種子來？', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
