# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟、梁強度的逐級扣減。"""
from plot import *  # noqa
import calcs

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '應力塊：三角形 → 矩形', TEN),
    ('S2', '板也會推歪：推歪＝拉回', COMP),
    ('S3', '壓翼板是一根側向的柱', COMP),
    ('S4', '三段＝平台＋直線＋曲線，取小', KEY),
    ('S5', '彎矩梯度是紅利', AC),
    ('S6', 'τ_{y} = *F*_{y}/√3 ≈ 0.6*F*_{y}', WARN),
    ('S7', '剪力流＝切一刀的水平平衡', WARN),
    ('S8', '撓度＝曲率的積分', AC),
]

KIDS = [
    (0, '1', '*M*_{y}=*F*_{y}*S*_{x}、*M*_{p}=*F*_{y}*Z*_{x}、形狀因子'),
    (0, '1', 'PNA 等面積、*Z* 半面積法、平行軸'),
    (0, '12', '合成梁 *C*=*T* 找 PNA'),
    (1, '2', 'λ ∝ √(*E*/*F*_{y}) → 17、25、170、260'),
    (1, '8', '腹板剪力挫屈 *k*_{v}、*C*_{v}'),
    (2, '3', '*M*_{cr} 兩項 → *X*_{1}、*X*_{2}'),
    (2, '11', '弱軸沒有 LTB、1.5*F*_{y}*S*_{y}'),
    (3, '2', 'FLB 內插（λ 版）'),
    (3, '4', 'LTB 三區段、*L*_{p}、*L*_{r}、*M*_{r}'),
    (3, '6', 'ASD：*L*_{c}、*L*_{u}、0.66→0.6*F*_{y}'),
    (4, '5', '*C*_{b} 四分點式、常見載重'),
    (5, '8', '*V*_{n} = 0.6*F*_{y}*A*_{w}'),
    (6, '9', '*q* = *VQ*/*I*、蓋板銲道'),
    (7, '10', '5*wL*^{4}/384*EI*、*L*/360'),
    (7, '13', '塑性分析虛功法'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 330, 44
    kx, kw, kh = 452, 434, 34
    sy0, sgap = 62, 74
    ky0, kgap = 56, 39.5
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 30
    o = T(sx + sw / 2, 34, '8 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 34, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 28, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 60, y + 28, txt, 15, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 70, kh, STEEL2, None, 0, 7)
        o += T(kx + 35, y + 22, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 80, y + 22.5, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '應力塊、自由體', AC),
             ('②', '白話', '防哪一種破壞', TEN),
             ('③', '推導', '一行一件事', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
             ('⑤', '給背標籤', '考卷印不印', MUT),
             ('⑥', '重建卡', '30 秒重畫', PUR)]
    bw, gap = 124, 24
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 12 + i * (bw + gap)
        o += R(x, 40, bw, 112, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 118, s, 14, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 3, 96, x + bw + gap - 3, 96, INK, 2.2, 10)
    o += T(W / 2, 186, '全書每一條公式都照這六步走——讀久了，拿到新公式腦袋會自己照這個順序想', 15, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


def fig0_3():
    """逐級扣減：同一支 H700×200，Lb = 5 m、Cb = 1。"""
    d = calcs.example()
    vals = [('*M*_{p}', d['Mp'] / 100, TEN, '斷面本錢\n*F*_{y}*Z*_{x}', '第1章'),
            ('局部挫屈後', d['Mp'] / 100, COMP, '結實：不扣', '第2章'),
            ('LTB 後 *M*_{n}', d['Mn5'] / 100, COMP, '*L*_{b}=5 m', '第3–5章'),
            ('φ_{b}*M*_{n}', calcs.PHI_B * d['Mn5'] / 100, KEY, '×0.90', '第4章')]
    W, H = 900, 400
    pl = Plot(110, 60, 600, 270, 0, 4, 0, 180)
    o = pl.axes([], [0, 40, 80, 120, 160], '', '*M*（tf·m）', size=14)
    bw = 0.56
    for i, (lab, v, c, note, ch) in enumerate(vals):
        x0 = i + 0.22
        o += R(pl.X(x0), pl.Y(v), pl.X(x0 + bw) - pl.X(x0), pl.Y(0) - pl.Y(v), c, None, 0, 4, op=0.85)
        o += T(pl.X(x0 + bw / 2), pl.Y(v) - 10, f'{v:.1f}', 16, c, 'middle', 'bold')
        o += T(pl.X(x0 + bw / 2), pl.Y(0) + 24, lab, 15, INK, 'middle', 'bold')
        o += T(pl.X(x0 + bw / 2), pl.Y(0) + 46, ch, 14, MUT, 'middle')
        if i:
            o += L(pl.X(x0 - 1 + bw), pl.Y(vals[i - 1][1]), pl.X(x0), pl.Y(vals[i - 1][1]), MUT, 1.3, '4 4')
    o += box(730, 70, 160, 250, '一路扣下去', ['先算本錢 *M*_{p}', '翼板會不會先皺？', '整根會不會側翻？', '最後乘 φ_{b}', '', '剪力、撓度', '是另外兩條線', '（下冊）'], KEY2, KEY, 16, 14)
    return svg(W, H, o, '梁強度逐級扣減')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
