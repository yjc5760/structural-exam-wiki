# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟流程。"""
from plot import *  # noqa

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '換手鏈：最弱的一站決定強度', KEY),
    ('S2', '強度 = 應力 × 真正斷掉的面', TEN),
    ('S3', '純剪 τ = *F*/√3 ≈ 0.6*F*', WARN),
    ('S4', '45° 最窄：喉厚 = *w*/√2', AC),
    ('S5', '繞形心轉：力 ∝ *r*、方向 ⊥ *r*', AC),
    ('S6', '切一刀：不平衡的力靠接合補', TEN),
    ('S7', '摩擦 = μ × 夾緊力', WARN),
]

# (種子序號, 章, 長出來的東西)
KIDS = [
    (0, '1', '極限狀態清單、取最小值'),
    (0, '1', 'φ 排序 0.75／0.90／1.0、Ω = 1.5/φ'),
    (0, '10', '保險絲：強柱弱梁、RBS、塑鉸外移'),
    (1, '2', '螺栓剪力 *F*_{nv}*A*_{b}*m*'),
    (1, '2', '承壓 1.2*L*_{c}*tF*_{u} ≤ 2.4*dtF*_{u}'),
    (1, '2', '剪力板的剪力降伏、剪力斷裂'),
    (2, '2', '0.5*F*_{u}、0.4*F*_{u}（螺栓）、所有 0.6'),
    (2, '5', '0.6*F*_{EXX}、ASD 0.3*F*_{EXX}'),
    (3, '5', '*t*_{e} = 0.707*w*、由 *t*_{e} 反算 *w*'),
    (3, '5', '銲道方向性：規範為何忽略'),
    (4, '6', '螺栓群 *I*_{p} = Σ*r*^{2}、*R*_{M} = *Mr*/*I*_{p}'),
    (4, '7', '銲縫線圖 *J*、長度加權形心'),
    (4, '7', '控制點：看向量和，不看最遠'),
    (5, '8', '剪力流 *q* = *VQ*/*I*、斷續銲間距'),
    (5, '8', '翼板力偶 *F*_{f} = *M*_{f}/(*d* − *t*_{f})'),
    (6, '4', '摩阻型 1.13μ*T*_{b}*N*_{s}*N*_{b}、φ = 1.0'),
    (6, '4', '摩阻型可與銲接分擔、承壓型不行'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 360, 46
    kx, kw, kh = 470, 416, 32
    ky0, kgap = 62, 39
    H = int(ky0 + len(KIDS) * kgap + 30)
    sgap = (len(KIDS) * kgap - sh) / (len(SEEDS) - 1) * 0.98
    sy0 = ky0 - 4
    o = T(sx + sw / 2, 36, '7 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 29, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 60, y + 29, txt, 15, INK, 'start', 'bold')
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
        o += T(kx + 76, y + 22, txt, 14, INK, 'start')
    return svg(W, H, o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '力往哪裡走', AC),
             ('②', '白話', '防哪一種破壞', TEN),
             ('③', '推導', '從種子三步', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
             ('⑤', '給背標籤', '考卷給不給', MUT),
             ('⑥', '重建卡', '空白紙重畫', PUR)]
    bw, gap = 124, 24
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 10 + i * (bw + gap)
        o += R(x, 40, bw, 110, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 114, s, 15, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 3, 95, x + bw + gap - 3, 95, INK, 2.2, 10)
    o += T(W / 2, 186, '全書每一條公式都照這六步走——讀久了，腦袋會自己照這個順序想', 15, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
