# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟流程。"""
from sa_draw import *  # noqa

SEEDS = [
    ('S1', '平衡：切開就要 ΣF = 0、ΣM = 0', FOR),
    ('S2', '彎矩面積：轉角 = *M*/*EI* 圖面積', DEF),
    ('S3', '彎矩只認「相對於弦」的轉角 θ − ψ', DEF),
    ('S4', '疊加：先全部鎖住，再一個一個放開', LOAD),
    ('S5', '鏡像：對稱結構 → 變形也對稱', PUR),
    ('S6', '桿長不變：節點只能垂直桿軸移動', INK),
]

# (seed index, 章, 推出來的東西)
KIDS = [
    (0, '6', '節點彎矩平衡 Σ*M*_{節點} = 0'),
    (0, '6', '桿端剪力 *V* = (*M*_{AB}+*M*_{BA})/*L* + *V*_{0}'),
    (0, '7', '層剪力方程（側移方程）'),
    (1, '2', '端轉角 *ML*/3*EI*、*ML*/6*EI* → 4、2、½'),
    (1, '3', '簡支梁端轉角 *wL*^{3}/24*EI*、*PL*^{2}/16*EI*'),
    (1, '4', '遠端鉸接 3*EI*/*L*'),
    (1, '5', '非均勻斷面的廣義式（柔度積分）'),
    (1, '7', '柱側移勁度 12*EI*/*L*^{3}、3*EI*/*L*^{3}'),
    (2, '2', '主式裡的 −3ψ'),
    (2, '3', '支承沉陷 6*EI*Δ/*L*^{2}'),
    (3, '2', '傾角變位式 = 鎖住 + 放開'),
    (3, '3', '*wL*^{2}/12、*PL*/8、*Pab*^{2}/*L*^{2}'),
    (3, '4', '修正固端彎矩、*wL*^{2}/8、3*PL*/16'),
    (4, '9', '對稱軸 θ = 0、ψ = 0；反對稱 θ 相等'),
    (5, '8', '斜桿 ψ 的比例（位移圖）'),
    (5, '8', '用虛功列側移方程'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 372, 50
    kx, kw, kh = 488, 400, 32
    sy0, sgap = 86, 104
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
    steps = [('①', '看圖', '變形／自由體圖', DEF),
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
