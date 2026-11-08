# -*- coding: utf-8 -*-
"""第 7 章：耐震構架的加嚴。數值由 calcs.seismic() 算出。"""
from plot import *  # noqa
from calcs import *  # noqa
import math

S = seismic()


def fig7_1():
    W, H = 900, 360
    o = T(450, 26, '種子 S7：一條鏈子，只准保險絲那一環先降伏', 16, INK, 'middle', 'bold')
    links = [('柱', COMP, '強柱弱梁'), ('節點域', AC, '*t*_{z} 不挫屈'), ('銲道／接頭', COMP, '≥ 1.1*R*_{y}*M*_{p}'),
             ('梁塑鉸', KEY, '保險絲'), ('梁其餘段', AC, '側撐')]
    x = 60; y = 150
    for i, (n, c, s) in enumerate(links):
        fuse = n == '梁塑鉸'
        o += f'<ellipse cx="{x + 70}" cy="{y}" rx="70" ry="38" fill="{KEY2 if fuse else "#fff"}" stroke="{c}" stroke-width="{5 if fuse else 3}"/>'
        o += T(x + 70, y + 6, n, 16, c, 'middle', 'bold')
        o += T(x + 70, y + 68, s, 14.5, INK, 'middle')
        x += 160
    o += A(40, y, 10, y, INK, 3, 12) + A(860, y, 890, y, INK, 3, 12)
    o += R(80, 250, 740, 86, '#fff', INK, 1.2, 10)
    o += T(450, 278, '保險絲（梁塑鉸）要「真的會降伏、而且轉得夠」：降伏比 ≤ 0.80、0.03 rad、側撐', 15, KEY, 'middle', 'bold')
    o += T(450, 306, '其他環要「比保險絲的實際強度還強」：*R*_{y} 超強、SN-C、UT 100%、移除背銲條', 15, COMP, 'middle', 'bold')
    o += T(450, 328, f'範例梁 H600：*M*_{{p}} = {S["Mp"]:.0f} kN·m；設 *R*_{{y}} = {S["Ry"]}（假設）→ 接頭需 1.1*R*_{{y}}*M*_{{p}} ≈ {S["Mpr"]:.0f} kN·m', 14, MUT, 'middle')
    return svg(W, H, o, '容量設計鏈')


def fig7_2():
    W, H = 900, 380
    pl = Plot(90, 56, 500, 250, 40, 200, 0, 12)
    o = T(340, 26, '節點域 (*d*_{z}+*w*_{z})/*t*_{z} ≤ 90：先讓它降伏，挫屈要晚很多', 16, INK, 'middle', 'bold')
    o += pl.axes([40, 60, 90, 120, 150, 200], [0, 1, 4, 8, 12], '', 'τ_{cr}／τ_{y}', size=14)
    o += T(pl.X(120), pl.y0 + pl.h + 42, '(*d*_{z}+*w*_{z})／*t*_{z}', 14, INK, 'middle')
    o += pl.curve(lambda r: panel_tau_ratio(r), 40, 200, AC, 3.2)
    o += pl.hline(1.0, 40, 200, COMP, 1.6)
    o += pl.vline(90, 0, 12, KEY, 2, '7 4')
    o += pl.dot(90, S['tau90'], KEY, 7)
    o += T(pl.X(92), pl.Y(S['tau90']) - 12, f'90 → 彈性挫屈約 {S["tau90"]:.1f}τ_{{y}}', 14, KEY, 'start', 'bold')
    o += T(pl.X(198), pl.Y(1.0) - 8, 'τ_{y} = 0.6*F*_{y}', 14, COMP, 'end', 'bold')
    o += T(pl.X(60), pl.Y(10.8), '彈性剪力挫屈（正方形板 *k* = 9.34，SN490 *F*_{y} = 325）', 14, AC, 'start')
    ex = (S['dz'] + S['wz']) / S['tz']
    o += A(pl.X(118), pl.Y(8.6), pl.X(41), pl.Y(8.6), TEN, 2, 10, dash='6 4')
    o += T(pl.X(121), pl.Y(8.6) + 5, f'範例柱板 50 mm：比值 {ex:.0f}', 14, TEN, 'start', 'bold')
    o += T(pl.X(121), pl.Y(8.6) + 24, '（在圖左外，遠低於 90）', 14, TEN, 'start')
    o += R(620, 64, 268, 242, KEY2, KEY, 1.4, 10)
    rows = [('為什麼不是 τcr = τy？', KEY, True), ('', INK, False), ('節點域要進入剪力降伏', INK, False), ('並來回大變形消能', INK, False),
            ('→ 挫屈必須延後到', INK, False), ('很大的塑性應變之後', INK, False), ('', INK, False), ('90 是試驗校準的數字', COMP, True), ('方向可推、數值要背', COMP, True)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(754, 92 + i * 23, s, 14.5, c, 'middle', 'bold' if b else None)
    return svg(W, H, o, '節點域厚度')


def fig7_3():
    W, H = 900, 360
    o = T(450, 26, '層狀撕裂：厚板「板厚方向」是最弱的那一刀', 16, INK, 'middle', 'bold')
    x0, y0, w, h = 120, 120, 420, 120
    o += R(x0, y0, w, h, STEEL2, INK, 1.4)
    import random
    random.seed(3)
    for k in range(5):
        yy = y0 + 18 + k * 21
        for j in range(7):
            xx = x0 + 30 + j * 55 + random.uniform(-10, 10)
            o += L(xx, yy, xx + random.uniform(18, 32), yy, MUT, 2.4)
    o += T(x0 + w / 2, y0 + h + 24, '軋延時夾雜物被壓成「平行板面」的薄片', 14, MUT, 'middle')
    # 立板＋銲道，拉力往上（板厚方向）
    sx = x0 + 180
    o += R(sx, 54, 50, y0 - 54, STEEL3, INK, 1.4)
    o += P([(sx, y0), (sx - 30, y0), (sx, y0 - 30)], COMP, 1, fill=COMPM, close=True)
    o += P([(sx + 50, y0), (sx + 80, y0), (sx + 50, y0 - 30)], COMP, 1, fill=COMPM, close=True)
    o += A(sx + 25, 80, sx + 25, 40, COMP, 3, 12)
    o += T(sx + 40, 52, '銲接收縮＋梁翼拉力', 14, COMP, 'start', 'bold')
    o += T(sx + 40, 70, '＝板厚方向（Z 向）拉', 14, COMP, 'start')
    # 撕裂階梯
    pts = [(sx - 20, y0 + 8), (sx + 20, y0 + 8), (sx + 20, y0 + 29), (sx + 70, y0 + 29), (sx + 70, y0 + 50), (sx + 120, y0 + 50)]
    o += P(pts, COMP, 3)
    o += T(sx + 126, y0 + 56, '沿夾雜層階梯狀剝開', 14, COMP, 'start', 'bold')
    o += R(600, 64, 288, 252, KEY2, KEY, 1.4, 10)
    rows = [('防治（四招）', KEY, True), ('', INK, False), ('① Z 向鋼材 SN-C', INK, True), ('（Z 向斷面收縮率 ≥ 25%）', INK, False),
            ('② 銲接順序降低拘束', INK, False), ('③ 奶油層（buttering）', INK, False), ('④ 改接頭細節，', INK, False), ('不讓拉力走板厚方向', INK, False),
            ('', INK, False), ('箱型柱板厚 ≥ 40 mm', COMP, True), ('→ 須用 SN400C／SN490C', COMP, True)]
    for i, (s, c, b) in enumerate(rows):
        if s:
            o += T(744, 90 + i * 21, s, 14.5, c, 'middle', 'bold' if b else None)
    return svg(W, H, o, '層狀撕裂')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3}
