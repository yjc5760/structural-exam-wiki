# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步流程、全書地圖（折線世界 → 曲線世界）。"""
from figs_common import *  # noqa
import calcs as K

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '橫軸是「載重在哪」', AC),
    ('S2', '平衡：剪一刀，靜定量對 *x* 是直線', TEN),
    ('S3', 'Müller-Breslau：拆、推 1、看形狀', PUR),
    ('S4', '互易：*f*_{*ij*} = *f*_{*ji*}', WARN),
    ('S5', '彎矩＝彎曲：κ = *M*/*EI*', COMP),
    ('S6', '疊加：效應 = Σ 載重 × 縱距', '#455a64'),
]

KIDS = [
    (0, '1', '縱距的單位：反力無因次、彎矩是 m'),
    (0, '1', '讀圖：效應 = *P* × η'),
    (1, '1', '*R*_{*A*} = (*L*−*x*)/*L*、*V* 跳 1、峰值 *ab*/*L*'),
    (1, '3', '桁架截面法：桿力影響線'),
    (2, '2', '靜定 = 剛體轉動 → 折線'),
    (2, '2', '內鉸可轉折、懸臂段直線延伸'),
    (3, '5', 'IL = *v*(*x*)/*f*_{*ii*}（一定要除）'),
    (3, '6', '位移影響線、靜不定桁架'),
    (4, '5', '撓度曲線的數值 → 曲線段縱距'),
    (4, '7', '共軛梁法、三彎矩方程'),
    (5, '3', '節間直線（縱梁是簡支梁）'),
    (5, '4', 'Σ*P*η、*w* × 正面積、輪壓臨界位置'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 370, 48
    kx, kw, kh = 484, 404, 36
    sy0, sgap = 72, 84
    ky0, kgap = 60, 42
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 26
    o = T(sx + sw / 2, 36, '6 顆種子（要記的）', 17, PUR, 'middle', 'bold')
    o += T(kx + kw / 2, 36, '長出來的公式（不用背，會推）', 17, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 10)
        o += R(sx, y, 48, sh, c, None, 0, 10) + R(sx + 30, y, 18, sh, c, None)
        o += T(sx + 24, y + 30, sid, 15, '#fff', 'middle', 'bold')
        o += T(sx + 58, y + 30, txt, 15, INK, 'start', 'bold')
    for j, (si, ch, txt) in enumerate(KIDS):
        y = ky0 + j * kgap
        x1, y1, c = spos[si]
        x2, y2 = kx, y + kh / 2
        mx = (x1 + x2) / 2
        o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".75"/>'
        o += head(x2, y2, 0, c, 8)
        o += R(kx, y, kw, kh, '#fafafa', STEEL, 1.1, 7)
        o += R(kx, y, 62, kh, STEEL2, None, 0, 7)
        o += T(kx + 31, y + 24, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(kx + 70, y + 24, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '單位載重、變形形狀', AC),
             ('②', '白話', '它在描述什麼', TEN),
             ('③', '推導', '從種子三步', COMP),
             ('④', '極限檢查', '代 0、代 *L*', WARN),
             ('⑤', '給背標籤', '考卷會不會印', '#455a64'),
             ('⑥', '重建卡', '空白紙重畫', PUR)]
    bw, gap = 128, 26
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 10 + i * (bw + gap)
        o += R(x, 36, bw, 116, '#fff', c, 2.2, 12)
        o += R(x, 36, bw, 42, c, None, 0, 12) + R(x, 62, bw, 16, c, None)
        o += T(x + bw / 2, 64, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 118, s, 14, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 3, 94, x + bw + gap - 3, 94, INK, 2.2, 10)
    o += T(W / 2, 186, '全書每一條公式都照這六步寫；拿到新題目也先問：「圖在哪？從哪顆種子推？」', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


def fig0_3():
    """全書地圖：同一根 10 m 梁，上排靜定（折線），下排把左端改成固定端（曲線）。"""
    W, H = 900, 560
    o = ''
    ax = Ax(250, 52)            # 10 m → 520 px
    # ---- 上排：靜定
    o += R(10, 14, 880, 250, '#f7fbff', ACM, 1.4, 12)
    o += T(28, 44, '第 1～4 章　折線世界（靜定）', 17, AC, 'start', 'bold')
    o += T(28, 74, '拆掉一個束制 → 變成機構', 15, INK, 'start')
    o += T(28, 98, '→ 各段只會剛體轉動', 15, INK, 'start')
    o += T(28, 122, '→ 影響線是直線', 15, AC, 'start', 'bold')
    yb = 108
    o += beam(ax, yb, 0, K.L, [(0, 'pin'), (K.L, 'roller')], labels=[(0, 'A'), (K.L, 'B'), (K.a, 'C')])
    o += L(ax(K.a), yb - 8, ax(K.a), yb + 8, KEY, 2)
    o += il(ax, 236, 34, [(0, 0), (K.a, K.MC_PEAK), (K.L, 0)], vals=[(K.a, K.MC_PEAK, f'*ab*/*L* = {f(K.MC_PEAK)} m')],
            ticks=(0, K.a, K.L))
    o += T(ax(K.L) + 22, 241, '*M*_{*C*}', 16, INK, 'start', 'bold')
    o += T(28, 236, '第 1 章：用平衡算', 14, MUT, 'start')
    o += T(28, 256, '第 2 章：用形狀畫', 14, MUT, 'start')
    # ---- 下排：靜不定
    o += R(10, 284, 880, 262, '#fff8f8', COMPM, 1.4, 12)
    o += T(28, 314, '第 5～7 章　曲線世界（靜不定）', 17, COMP, 'start', 'bold')
    o += T(28, 344, '拆掉一個束制 → 還站得住', 15, INK, 'start')
    o += T(28, 368, '→ 推它一下就得彎', 15, INK, 'start')
    o += T(28, 392, '→ 影響線是曲線', 15, COMP, 'start', 'bold')
    o += T(28, 416, '　 而且要除以 *f*_{*ii*}', 15, COMP, 'start', 'bold')
    yb2 = 372
    o += beam(ax, yb2, 0, K.L, [(0, 'fixL'), (K.L, 'roller')], labels=[(0, 'A', 16), (K.L, 'B')])
    xs = [i * K.L / 100 for i in range(101)]
    base = 522
    sy = 92
    pts = [(ax(x), base - sy * K.RC_prop(x)) for x in xs]
    o += P([(ax(0), base)] + pts + [(ax(K.L), base)], None, fill=POS2, close=True, op=0.8)
    o += L(ax(0) - 10, base, ax(K.L) + 14, base, MUT, 1.3)
    o += P(pts, COMP, 2.8)
    x4 = 4.0
    o += C(ax(x4), base - sy * K.RC_PROP_4, 4, COMP, '#fff', 1.4)
    o += T(ax(x4), base - sy * K.RC_PROP_4 - 12, f'{K.RC_PROP_4:.3f}', 15, COMP, 'middle', 'bold')
    o += T(ax(K.L) + 12, base - sy + 5, '1', 15, COMP, 'start', 'bold')
    o += T(ax(K.L) + 30, base + 5, '*R*_{*B*}', 16, INK, 'start', 'bold')
    o += T(28, 512, '第 5 章：同一根梁，', 14, MUT, 'start')
    o += T(28, 532, '一端改成固定', 14, MUT, 'start')
    return svg(W, H, o, '全書地圖：折線到曲線')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
