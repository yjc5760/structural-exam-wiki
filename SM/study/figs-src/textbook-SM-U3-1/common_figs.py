# -*- coding: utf-8 -*-
"""四本 SM 教科書共用的第 0 章圖：種子家族樹、五步驟。每個工作資料夾各放一份副本。"""
from plot import *  # noqa

PUR = '#7b1fa2'


def seed_tree(SEEDS, KIDS, title_l='種子（要記的）', title_r='長出來的公式（不用背，會推）'):
    W = 900
    sx, sw, sh = 16, 350, 50
    kx, kw, kh = 470, 414, 34
    sgap = 74
    kgap = 40.5
    nS, nK = len(SEEDS), len(KIDS)
    Hs = nS * sgap
    Hk = nK * kgap
    Hc = max(Hs, Hk)
    sy0 = 60 + (Hc - Hs) / 2 + 8
    ky0 = 60 + (Hc - Hk) / 2
    H = 60 + Hc + 30
    o = T(sx + sw / 2, 36, title_l, 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, title_r, 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 31, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 58, y + 31, txt, 14.5, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 62, kh, STEEL2, None, 0, 7)
        o += T(kx + 31, y + 23, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 70, y + 23, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def five_steps(s1='自由體圖／剖面', s2='平衡、有效應力、摩擦'):
    W, H = 900, 190
    steps = [('①', '看圖', s1, AC),
             ('②', '第一性原理', s2, TEN),
             ('③', '三步推導', '每一步只做一件事', COMP),
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


def flow(boxes, title=''):
    """直式流程圖：boxes = [(標題, 說明, 顏色), ...]，每個框一行。"""
    W = 900
    bh, gap = 58, 26
    H = 30 + len(boxes) * (bh + gap)
    o = ''
    for i, (t, s, c) in enumerate(boxes):
        y = 16 + i * (bh + gap)
        o += R(60, y, 780, bh, '#fff', c, 2, 10)
        o += R(60, y, 210, bh, c, None, 0, 10) + R(250, y, 20, bh, c, None)
        o += T(165, y + 36, t, 16, '#fff', 'middle', 'bold')
        o += T(288, y + 36, s, 15, INK, 'start')
        if i < len(boxes) - 1:
            o += A(450, y + bh + 2, 450, y + bh + gap - 2, INK, 2, 9)
    return svg(W, int(H), o, title or '解題流程')
