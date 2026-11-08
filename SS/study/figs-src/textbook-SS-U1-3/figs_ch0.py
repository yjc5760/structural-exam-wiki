# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、六步驟、全書兩條腿總圖。"""
from plot import *  # noqa
from calcs import ex2014

PUR = '#7b1fa2'

SEEDS = [
    ('S1', '推歪 *P*·*y* ＝ 拉回 *EI*·*y*″', COMP),
    ('S2', '放大 ＝ 1 + α + α² + … ＝ 1/(1−α)', COMP),
    ('S3', '等值均勻彎矩：單曲率幫倒忙', KEY),
    ('S4', '拆兩次：加假想支撐，再拿掉', AC),
    ('S5', '節點上：柱想轉 ÷ 梁擋住', AC),
    ('S6', '利用率相加 ≤ 1', TEN),
]

# (seed index, 章, 長出來的東西)
KIDS = [
    (0, '1', '*P*_{e} = π²*EI*/(*KL*)²、*P*_{eK} = *P*_{e}/*K*²'),
    (0, '1', '*P*_{e1} = *A*_{g}*F*_{y}/λ_{c}²（捷徑）'),
    (1, '2', '放大外殼 1/(1 − *P*_{u}/*P*_{e1})'),
    (1, '2', '*B*_{2} 側移角版、*F*′_{e} = *F*_{e}÷(23/12)'),
    (2, '3', '*C*_{m} = 0.6 − 0.4 *M*_{1}/*M*_{2}、正負號'),
    (2, '3', '*B*_{1} 台灣版（0.64／0.32）'),
    (3, '4', '*M*_{u} = *B*_{1}*M*_{nt} + *B*_{2}*M*_{lt}'),
    (3, '4', '*B*_{2} = 1/(1 − Σ*P*_{u}/Σ*P*_{eK})、靠桿'),
    (4, '5', '*G* = Σ(*I*/*L*)_{柱}/Σ(*I*/*L*)_{梁}'),
    (4, '5', '梁遠端修正、萊梅厥 *K*′'),
    (5, '8', 'H1 兩段：0.2 分界、8/9'),
    (5, '9', 'ASD 強度式、穩定式、0.15'),
    (5, '10', '強柱弱梁：柱側扣軸壓'),
]


def fig0_1():
    W = 900
    sx, sw, sh = 14, 360, 46
    kx, kw, kh = 480, 406, 34
    sy0, sgap = 70, 84
    ky0, kgap = 62, 39
    H = 60 + max(len(SEEDS) * sgap, len(KIDS) * kgap) + 30
    o = T(sx + sw / 2, 36, '6 顆種子（要記的）', 17, PUR, 'middle', 'bold')
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
        o += T(kx + 74, y + 22.5, txt, 14, INK, 'start')
    return svg(W, int(H), o, '種子公式家族樹')


def fig0_2():
    W, H = 900, 200
    steps = [('①', '看圖', '自由體圖、變形', AC),
             ('②', '白話', '防哪一種破壞', TEN),
             ('③', '推導', '從種子三步', COMP),
             ('④', '極限檢查', '代 0、代 ∞', WARN),
             ('⑤', '給背標籤', '考卷印不印', MUT),
             ('⑥', '重建卡', '空白紙重畫', PUR)]
    bw, gap = 128, 20
    o = ''
    for i, (n, t, s, c) in enumerate(steps):
        x = 12 + i * (bw + gap)
        o += R(x, 40, bw, 110, '#fff', c, 2.2, 12)
        o += R(x, 40, bw, 40, c, None, 0, 12) + R(x, 66, bw, 14, c, None)
        o += T(x + bw / 2, 67, f'{n} {t}', 16, '#fff', 'middle', 'bold')
        o += T(x + bw / 2, 114, s, 14, INK, 'middle')
        if i < len(steps) - 1:
            o += A(x + bw + 2, 95, x + bw + gap - 2, 95, MUT, 2, 8)
    o += T(450, 186, '每一條公式都照這六步走；第 ⑥ 步的重建卡是考前要反覆畫的東西', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '六步驟')


def fig0_3():
    """全書兩條腿：需求端（被放大）＋容量端（U1-1、U1-2）→ 互制收帳。數字取自 SS-2014-4。"""
    d = ex2014()
    W, H = 900, 470
    o = T(225, 30, '需求端：彎矩被軸力「養大」', 17, COMP, 'middle', 'bold')
    o += T(675, 30, '容量端：柱和梁各撐多少', 17, TEN, 'middle', 'bold')
    o += T(225, 52, '上冊 第 1～5 章', 14, MUT, 'middle')
    o += T(675, 52, '下冊 第 7 章（向 U1-1、U1-2 借）', 14, MUT, 'middle')
    # 需求端流程
    def blk(x, y, w, h, t1, t2, c, fill):
        s = R(x, y, w, h, fill, c, 1.8, 10)
        s += T(x + w / 2, y + 26, t1, 15.5, c, 'middle', 'bold')
        if t2:
            s += T(x + w / 2, y + 50, t2, 14, INK, 'middle')
        return s
    o += blk(70, 70, 310, 62, '一階分析（不管二階）', '得到 *M*_{nt}、*M*_{lt}、*P*_{u}', INK, '#fafafa')
    o += A(225, 134, 225, 156, INK, 2, 9)
    o += blk(30, 160, 180, 70, '× *B*_{1}（P-δ）', f'本例 = {d["B1"]:.2f}', COMP, COMP2)
    o += blk(240, 160, 180, 70, '× *B*_{2}（P-Δ）', f'本例 = {d["B2"]:.3f}', COMP, COMP2)
    o += A(120, 232, 200, 262, COMP, 2, 9) + A(330, 232, 250, 262, COMP, 2, 9)
    o += blk(60, 266, 330, 62, '*M*_{u} = *B*_{1}*M*_{nt} + *B*_{2}*M*_{lt}', f'本例 = {d["Mux"]:.1f} kN·m', COMP, '#fff')
    # 容量端
    o += blk(500, 110, 160, 92, '柱：φ_{c}*P*_{n}', f'{d["phiPn"]:.0f} kN', TEN, TEN2)
    o += blk(690, 110, 180, 92, '梁：φ_{b}*M*_{n}', f'{d["phiMn"]:.1f} kN·m', TEN, TEN2)
    o += T(580, 188, '（U1-1 柱曲線）', 14, MUT, 'middle')
    o += T(780, 188, '（U1-2 *F*_{y}*Z*）', 14, MUT, 'middle')
    # 互制
    o += R(250, 366, 400, 78, KEY2, KEY, 2.2, 12)
    o += T(450, 394, '互制收帳：利用率相加 ≤ 1（第 8、9 章）', 16, KEY, 'middle', 'bold')
    o += T(450, 424, f'本例 {d["Pu_ratio"]:.3f} + (8/9)×{d["Mux"] / d["phiMn"]:.3f} = {d["H1"]:.3f} ≤ 1.0', 15, INK, 'middle')
    o += A(225, 330, 360, 364, COMP, 2.4, 10)
    o += A(580, 202, 520, 364, TEN, 2.4, 10)
    o += A(780, 202, 560, 364, TEN, 2.4, 10)
    o += L(450, 66, 450, 250, GRID, 1.5, '6 5')
    return svg(W, H, o, '全書兩條腿')


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2, 'fig0_3': fig0_3}
