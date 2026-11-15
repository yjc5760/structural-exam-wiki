# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步流程、兩條資訊鏈。"""
from plot import *  # noqa

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '平衡：切出的自由體 3 條、節點 2 條', TEN),
    ('S2', '二力桿：力沿著桿走', TEN),
    ('S3', '切一小片 dx 也要平衡', WARN),
    ('S4', '彎矩＝彎曲：κ = *M*/*EI*', AC),
    ('S5', '虛功：外力×位移 = 內力×變形', KEY),
    ('S6', '靜定結構會「讓開」', KEY),
]

# (種子, 章, 長出的東西)
KIDS = [
    (0, '1', '靜不定度 *r*−3−*c*、3*m*+*r*−3*j*−*c*、*m*+*r*−2*j*'),
    (0, '2', '內鉸多一條 Σ*M* = 0、主／附屬結構'),
    (0, '3', '節點法 Σ*F*_{x} = Σ*F*_{y} = 0'),
    (1, '3', '分量比例 *F*/*L* = *F*_{x}/Δ*x*、零力桿三規則'),
    (1, '4', '截面法：取矩點＝另兩桿交點'),
    (2, '5', 'd*V*/d*x* = −*w*、d*M*/d*x* = *V*、面積法'),
    (2, '5', '集中力→剪力跳、集中力矩→彎矩跳'),
    (3, '6', '凹向、反曲點、變形曲線'),
    (3, '7', '共軛梁 *w*^{*} = *M*/*EI*、標準撓度 3‧2‧8、48‧384‧24'),
    (4, '8', '∫*mM*/*EI* d*x*、Σ*nNL*/*EA*、彈簧項'),
    (4, '9', 'Σ*n*·Δ*L*（溫差、誤差）、支承位移項'),
    (5, '9', '剛體位移＋彈性位移、逆向題'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 16, 352, 48
    kx, kw, kh = 470, 418, 36
    sy0, sgap = 74, 86
    ky0, kgap = 62, 42.5
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 30
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
    steps = [('①', '看圖', '自由體圖、變形圖', AC),
             ('②', '白話', '它在描述什麼', TEN),
             ('③', '推導', '從種子三步', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
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
    o += T(W / 2, 186, '全書每一條公式都照這六步寫；讀久了，拿到新公式也會先問「圖在哪？從哪顆種子推？」', 14, MUT, 'middle')
    return svg(W, H, o, '每條公式的六個步驟')


def fig0_3():
    """兩條資訊鏈：內力鏈不含剛度，位移鏈才含。"""
    W, H = 900, 400
    o = ''
    # 左鏈
    def chain(x, title, items, c, c2):
        out = T(x + 190, 34, title, 17, c, 'middle', 'bold')
        y = 52
        for i, (a, b) in enumerate(items):
            out += R(x, y, 380, 56, c2, c, 1.6, 10)
            out += T(x + 190, y + 24, a, 15.5, INK, 'middle', 'bold')
            out += T(x + 190, y + 46, b, 14, MUT, 'middle')
            if i < len(items) - 1:
                out += A(x + 190, y + 58, x + 190, y + 78, c, 2.2, 10)
            y += 80
        return out
    o += chain(20, '① 內力鏈（第 1～5 章）', [
        ('幾何＋支承', '畫自由體圖'),
        ('平衡方程（S1～S3）', '未知數＝方程數，一路解到底'),
        ('反力、桿力、V、M', '完全用不到 E、I、A'),
        ('BMD、桁架桿力表', '位移鏈的輸入')], TEN, TEN2)
    o += chain(500, '② 位移鏈（第 6～9 章）', [
        ('內力 M、N', '從左邊那條鏈拿來'),
        ('除以剛度（S4）', 'κ = M/EI、ε = N/EA，剛度在這裡才出現'),
        ('累積變形（S5）', '共軛梁、單位力法'),
        ('位移、轉角', '沉陷、溫差只走這條（S6）')], AC, AC2)
    o += A(402, 300, 498, 108, KEY, 2.6, 12, dash='7 5')
    o += T(450, 370, '題目給 E、I、A、α，只有在問「位移」時才會用到', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '兩條資訊鏈')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
