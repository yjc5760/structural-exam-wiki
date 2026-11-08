# -*- coding: utf-8 -*-
"""第 10 章：耐震梁柱接頭——保險絲（S1 反用）、連續板、節點域（S6）、RBS 與補強式。"""
from plot import *  # noqa
from calcs import seismic_beam, yield_ratio
import math

S = seismic_beam()
YR = yield_ratio()


def fig10_1():
    W, H = 900, 450
    o = T(240, 28, '(a) 箱型柱–H 梁抗彎接頭（示意）', 16, INK, 'middle', 'bold')
    cx0, cw = 70, 130
    o += R(cx0, 50, cw, 370, STEEL2, INK, 1.6)
    o += L(cx0 + 14, 50, cx0 + 14, 420, INK, 1, '5 4') + L(cx0 + cw - 14, 50, cx0 + cw - 14, 420, INK, 1.4)
    yt, yb = 150, 320
    for y in (yt, yb):
        o += R(cx0 + 14, y - 6, cw - 28, 12, KEY2, KEY, 1.6)               # 內橫隔板
    o += T(cx0 + cw / 2, yt - 14, '內橫隔板', 14, KEY, 'middle', 'bold')
    bx = cx0 + cw
    o += R(bx, yt - 8, 260, 16, STEEL3, INK, 1.4) + R(bx, yb - 8, 260, 16, STEEL3, INK, 1.4)
    o += R(bx + 22, yt + 8, 8, yb - yt - 16, STEEL3, INK, 1.0)
    o += R(bx + 30, yt + 8, 230, yb - yt - 16, STEEL2, None)
    # 扇形孔
    for y, sg in ((yt + 8, 1), (yb - 8, -1)):
        o += f'<path d="M{bx + 22},{y} A14,14 0 0,{1 if sg > 0 else 0} {bx + 36},{y + sg * 14}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
    # CJP 記號
    for y in (yt, yb):
        o += P([(bx, y - 8), (bx + 10, y), (bx, y + 8)], COMP, 2.4)
    o += T(bx + 64, yt - 18, '梁翼 CJP（工地）', 14, COMP, 'start', 'bold')
    # 剪力板＋螺栓
    o += R(bx, yt + 40, 70, yb - yt - 80, AC2, AC, 1.4)
    for k in range(3):
        o += C(bx + 46, yt + 62 + k * 22, 5, '#fff', AC, 1.4)
    o += T(bx + 80, (yt + yb) / 2 + 5, '剪力板＋螺栓（傳 *V*）', 14, AC, 'start', 'bold')
    o += A(bx + 250, yt, bx + 300, yt, TEN, 3, 11) + A(bx + 300, yb, bx + 250, yb, COMP, 3, 11)
    o += T(bx + 304, yt + 5, '拉', 15, TEN, 'start', 'bold') + T(bx + 304, yb + 5, '壓', 15, COMP, 'start', 'bold')
    o += T(240, 444, '翼板的拉、壓力（傳 *M*）要經過柱壁 → 隔板 → 對面柱壁', 14, MUT, 'middle')
    # (b) 無連續板
    o += T(700, 28, '(b) 沒有隔板：柱壁被翼板拉凸', 16, INK, 'middle', 'bold')
    x0 = 610
    o += L(x0, 60, x0, 420, INK, 1.4, '5 4')
    pts = [(x0 + 14 * math.exp(-((y - yt) / 40) ** 2) + 0, y) for y in range(60, 421, 4)]
    o += L(x0 + 0, 60, x0 + 0, 420, STEEL, 3)
    bulge = [(x0 + 28 * math.exp(-((y - yt) / 38) ** 2) - 0, y) for y in range(60, 421, 3)]
    o += P(bulge, COMP, 3)
    o += A(x0 + 120, yt, x0 + 40, yt, TEN, 3, 11)
    o += R(x0 + 30, yt - 8, 90, 16, STEEL3, INK, 1.2)
    o += T(x0 + 130, yt + 40, '柱壁面外彎曲', 15, COMP, 'start', 'bold')
    o += T(x0 + 130, yt + 64, '→ 翼板中央應力集中', 14, INK, 'start')
    o += T(x0 + 130, yt + 88, '→ CJP 根部脆斷', 14, INK, 'start')
    o += T(x0 + 130, yb - 20, '節點域過度剪力變形', 15, COMP, 'start', 'bold')
    o += T(x0 + 130, yb + 4, '（菱形變形）', 14, INK, 'start')
    return svg(W, H, o, '梁柱接頭與連續板')


def fig10_2():
    W, H = 900, 440
    half = S['Lc'] / 2
    pl = Plot(110, 60, 600, 290, 0, 1500, 0.4, 1.25)
    o = T(450, 28, f'梁端彎矩是一條斜線：塑鉸離柱面越遠，柱面彎矩越大（示範：淨跨 {S["Lc"]/1000:.0f} m、不計重力）', 15, INK, 'middle', 'bold')
    o += pl.axes([0, 300, 600, 900, 1200, 1500], [0.4, 0.6, 0.8, 1.0, 1.2], '離柱面 *x*（mm）', '*M* / *M*_{p}', size=14)
    # RBS
    sh = S['sh_rbs']; r = S['rbs_ratio']
    o += pl.curve(lambda x: r * (half - x) / (half - sh), 0, 1500, KEY, 2.8)
    o += pl.dot(sh, r, KEY, 6)
    o += T(pl.X(sh) + 10, pl.Y(r) + 24, f'RBS 塑鉸 {r:.2f}*M*_{{p}}（*x* = {sh:.0f}）', 14, KEY, 'start', 'bold')
    o += pl.dot(0, S['face_over_Mp_rbs'], KEY, 6)
    o += T(pl.X(0) + 10, pl.Y(S['face_over_Mp_rbs']) + 4, f'柱面 {S["face_over_Mp_rbs"]:.2f}*M*_{{p}}', 14, KEY, 'start', 'bold')
    # 削弱區強度
    a, b = S['a'], S['b']
    def cap_rbs(x):
        if a <= x <= a + b:
            t = (x - a) / b
            return 1 - (1 - r) * math.sin(math.pi * t)
        return 1.0
    o += pl.curve(cap_rbs, 0, 1500, KEY, 1.6, dash='5 4', n=400)
    # 補強
    ac = S['a_cp']
    o += pl.curve(lambda x: (half - x) / (half - ac), 0, 1500, COMP, 2.8)
    o += pl.dot(ac, 1.0, COMP, 6)
    o += T(pl.X(ac) + 10, pl.Y(1.0) - 12, f'補強式塑鉸 *M*_{{p}}（*x* = {ac:.0f}）', 14, COMP, 'start', 'bold')
    o += pl.dot(0, S['face_over_Mp_cp'], COMP, 6)
    o += T(pl.X(0) + 10, pl.Y(S['face_over_Mp_cp']) - 10, f'柱面 {S["face_over_Mp_cp"]:.2f}*M*_{{p}}', 14, COMP, 'start', 'bold')
    o += pl.hline(1.0, c=TEN, w=1.4)
    o += R(730, 90, 160, 220, '#fff', KEY, 1.6, 10)
    for i, s_ in enumerate(['削弱式（RBS）', '柱面 < *M*_{p}', '銲道受保護', '補強式（蓋板）', '柱面 > *M*_{p}', '要靠蓋板撐住']):
        c = KEY if i < 3 else COMP
        o += T(810, 118 + i * 32, s_, 15 if i in (0, 3) else 14, c, 'middle', 'bold' if i in (0, 3) else None)
    o += T(410, 424, '虛線：RBS 削弱區的強度（示意）；實線：兩種接頭各自的彎矩斜線（以塑鉸彎矩為起點）', 14, MUT, 'middle')
    return svg(W, H, o, 'RBS 與補強式接頭的彎矩')


def fig10_3():
    W, H = 900, 400
    o = T(260, 28, '(a) 把節點域（柱腹板）切出來', 16, INK, 'middle', 'bold')
    x0, y0, w, h = 200, 110, 180, 210
    o += R(x0, y0, w, h, WARN2, WARN, 2)
    o += P([(x0 + 18, y0), (x0 + w + 18, y0), (x0 + w - 18 + 18, y0 + h), (x0 - 18 + 18, y0 + h)], WARN, 1.6, dash='5 4', close=True)
    o += A(x0 - 10, y0, x0 - 110, y0, TEN, 3, 11) + T(x0 - 110, y0 - 10, '*F* = *M*/(*d* − *t*_{f})', 15, TEN, 'start', 'bold')
    o += A(x0 - 110, y0 + h, x0 - 10, y0 + h, COMP, 3, 11) + T(x0 - 110, y0 + h + 24, '*F*', 15, COMP, 'start', 'bold')
    o += A(x0 + w / 2 + 40, y0 - 30, x0 + w / 2 - 40, y0 - 30, INK, 2, 9) + T(x0 + w / 2 + 50, y0 - 25, '*V*_{c}', 15, INK, 'start', 'bold')
    o += T(x0 + w / 2, y0 + h / 2 + 5, '純剪', 16, WARN, 'middle', 'bold')
    o += T(x0 + w / 2, y0 + h + 54, '*V*_{u} = Σ*M*/(*d*_{b} − *t*_{f}) − *V*_{c}', 16, KEY, 'middle', 'bold')
    o += R(500, 70, 380, 270, '#fff', KEY, 1.6, 10)
    rows = [('(b) 示範：SS-2018-3 的梁接到柱', KEY), (f'*M*_{{p}} = *F*_{{y}}*Z* = 2.4 × {S["Z"]/1e3:,.0f} cm³', INK),
            (f'= {S["Mp_tfm"]:.1f} tf·m', INK), (f'*V* = *M*_{{p}}/(*d* − *t*_{{f}}) = {S["Vpz"]:.0f} tf', COMP),
            ('（單側梁、不計 *V*_{c}；*F*_{y} 為假設）', MUT), ('和 8.2 節 *F*_{f} 同一張自由體圖', INK),
            ('薄 → 剪力挫屈 → *t*_{z} ≥ (*d*_{z} + *w*_{z})/90', INK)]
    for i, (t, c) in enumerate(rows):
        o += T(690, 104 + i * 34, t, 15, c, 'middle', 'bold' if c in (KEY, COMP) else None)
    return svg(W, H, o, '節點域剪力')


def fig10_4():
    W, H = 900, 360
    pl = Plot(110, 50, 520, 250, 0, 20, 0, 1.15)
    o = pl.axes([0, 5, 10, 15, 20], [0, 0.5, 0.8, 1.0], '應變（%）', 'σ / *F*_{u}', size=14)
    def curve(yr):
        def fn(e):
            ey = 0.15
            if e < ey:
                return yr * e / ey
            if e < 1.5:
                return yr
            u = min(1, (e - 1.5) / 13.5)
            return yr + (1 - yr) * (1 - (1 - u) ** 2)
        return fn
    o += pl.curve(curve(0.80), 0, 18, TEN, 3, n=400)
    o += pl.curve(curve(0.95), 0, 18, COMP, 3, dash='7 4', n=400)
    o += T(pl.X(17), pl.Y(0.80) + 24, 'SN490B：降伏比 ≤ 0.80', 15, TEN, 'end', 'bold')
    o += T(pl.X(4), pl.Y(0.95) - 12, '降伏比 0.95（A572 可能）', 15, COMP, 'start', 'bold')
    o += R(650, 70, 240, 210, '#fff', KEY, 1.6, 10)
    for i, (s_, c) in enumerate([('降伏後還能多撐多少？', KEY), (f'0.80 → *F*_{{u}}/*F*_{{y}} − 1 = {YR["hardening_room"]*100:.0f}%', TEN),
                                 (f'0.95 → {YR["a572_room"]*100:.0f}%', COMP), ('塑鉸要能擴展、轉動', INK), (f'SN490B *F*_{{y}} 有上限 {YR["sn490b"][1]} MPa', INK), ('→ 保險絲不會「太粗」', INK)]):
        o += T(770, 100 + i * 30, s_, 15 if i == 0 else 14, c, 'middle', 'bold' if c != INK else None)
    o += T(380, 344, '示意曲線：只比較降伏比對「硬化餘裕」的影響', 14, MUT, 'middle')
    return svg(W, H, o, '降伏比')


ALL = {'fig10_1': fig10_1, 'fig10_2': fig10_2, 'fig10_3': fig10_3, 'fig10_4': fig10_4}
