# -*- coding: utf-8 -*-
"""第 2 章：拉力桿件的兩種主要破壞（GSY、NSF）與 φ 值。"""
from plot import *  # noqa
from calcs import tension_example, STEELS
import math

D = tension_example()


def fig2_1():
    W, H = 900, 470
    o = T(450, 26, '(a) 拉桿兩端用螺栓接到節點板（示意，螺栓位置依比例）', 15, INK, 'middle', 'bold')
    xa, xb, yc, hh = 60, 840, 92, 40
    # 節點板
    o += R(20, yc - 42, 205, 84, STEEL2, STEEL, 1.2, 4) + R(675, yc - 42, 205, 84, STEEL2, STEEL, 1.2, 4)
    o += T(30, yc + 58, '節點板', 13, MUT, 'start') + T(870, yc + 58, '節點板', 13, MUT, 'end')
    o += R(xa, yc - hh / 2, xb - xa, hh, STEEL3, INK, 1.6, 2)
    o += A(70, yc - 64, 10, yc - 64, TEN, 3, 12) + T(40, yc - 72, '*T*', 16, TEN, 'middle', 'bold')
    o += A(830, yc - 64, 890, yc - 64, TEN, 3, 12) + T(860, yc - 72, '*T*', 16, TEN, 'middle', 'bold')
    sp = 40  # 7 cm 對應 40 px
    lh = [90, 90 + sp, 90 + 2 * sp]          # 左側三孔（最右者最靠桿身）
    rh = [810 - 2 * sp, 810 - sp, 810]
    for x in lh + rh:
        o += C(x, yc, 8, '#fff', INK, 1.6)
    o += L(lh[2], yc - 34, lh[2], yc + 34, COMP, 1.6, '4 3') + T(lh[2], yc - 38, '①', 15, COMP, 'middle', 'bold')
    o += T(450, yc + 6, '桿身：沒有孔，面積 *A*_{g}', 15, INK, 'middle')
    # (b) 應力沿長度
    o += T(450, 192, '(b) 沿桿長的平均拉應力 σ = 力 ÷ 面積（*T* = 30 tf）', 15, INK, 'middle', 'bold')
    pl = Plot(xa, 222, xb - xa, 190, 0, 1, 0, 2.6)
    T0 = 30.0
    sg, sn, se = T0 / D['Ag'], T0 / D['An'], T0 / D['Ae']
    yb = pl.y0 + pl.h
    o += L(xa, yb, xb, yb, INK, 1.4)
    o += T(xa - 6, yb + 5, '0', 13, MUT, 'end')
    # 階梯：力在每顆螺栓處被節點板接走 1/3
    def seg(x1, x2, v, c=TEN):
        return P([(x1, yb), (x1, pl.Y(v)), (x2, pl.Y(v)), (x2, yb)], c, 2.2, fill=TEN2)
    hw = 7
    poly = [(xa, yb)]
    cur = 0
    for i, x in enumerate(lh):
        f_after = T0 * (i + 1) / 3
        poly += [(x - hw, pl.Y(cur / D['Ag']) if cur else yb), (x - hw, pl.Y(f_after / D['An'])), (x + hw, pl.Y(f_after / D['An'])),
                 (x + hw, pl.Y(f_after / D['Ag']))]
        cur = f_after
    half = poly + [(450, pl.Y(sg))]
    full = half + [(900 - x, y) for (x, y) in reversed(half)]
    o += P(full + [(xa, yb)], TEN, 2.4, fill=TEN2, close=True)
    o += L(lh[2] + hw, pl.Y(se), lh[2] + hw + 70, pl.Y(se), COMP, 2, '6 4')
    o += L(lh[2] - hw, pl.Y(se), lh[2] + hw, pl.Y(se), COMP, 3)
    o += T(lh[2] + hw + 76, pl.Y(se) + 5, f'考慮剪力遲滯：*T*/*A*_{{e}} = {se:.2f}（第 4 章）', 14, COMP, 'start', 'bold')
    o += T(lh[2] + hw + 14, pl.Y(sn) - 8, f'① 孔的那一排：*T*/*A*_{{n}} = {sn:.2f}', 14, INK, 'start', 'bold')
    o += T(450, pl.Y(sg) + 26, f'桿身：*T*/*A*_{{g}} = {sg:.2f} tf/cm²', 14, TEN, 'middle', 'bold')
    o += T(450, 456, '應力最高的地方，就是最可能先出事的地方 —— 但「最高」不等於「最先破壞」（見 2.2）', 14, MUT, 'middle')
    return svg(W, H, o, '沿桿長的應力')


def _ss(e):
    """A36 示意應力–應變（tf/cm², 應變 %）。數值依 Fy、Fu 量級設定。"""
    Fy, Fu, E = D['Fy'], D['Fu'], 2040.0
    ey = Fy / E * 100
    if e <= ey:
        return E * e / 100
    if e <= 1.5:
        return Fy
    if e <= 15:
        u = (e - 1.5) / 13.5
        return Fy + (Fu - Fy) * (1 - (1 - u) ** 2)
    u = (e - 15) / 7
    return Fu - 0.55 * u ** 2


def fig2_2():
    W, H = 900, 420
    pl = Plot(90, 50, 640, 300, 0, 24, 0, 4.6)
    o = pl.axes([0, 2, 5, 10, 15, 20], [0, 1, 2, 2.52, 3, 4.1], '應變 ε（%）', '應力（tf/cm²）',
                xfmt=lambda v: f(v), yfmt=lambda v: {2.52: '*F*_{y}=2.52', 4.1: '*F*_{u}=4.10'}.get(v, f(v)))
    o += pl.curve(_ss, 0, 22, INK, 3.4, n=600, clip=False)
    o += pl.dot(22, _ss(22), INK, 5) + T(pl.X(22), pl.Y(_ss(22)) + 26, '斷', 15, INK, 'middle', 'bold')
    # 降伏平台
    o += R(pl.X(0.12), pl.Y(2.52) - 6, pl.X(1.5) - pl.X(0.12), 12, TENM, None, 0, 3, op=0.9)
    o += A(pl.X(3.6), pl.Y(1.75), pl.X(1.0), pl.Y(2.45), TEN, 2, 10)
    o += T(pl.X(3.8), pl.Y(1.75) + 6, '降伏平台：應力不再增加，', 14.5, TEN, 'start', 'bold')
    o += T(pl.X(3.8), pl.Y(1.75) + 26, '應變卻一路長 → 「GSY」用這裡', 14.5, TEN, 'start', 'bold')
    o += pl.dot(15, 4.1, COMP, 6)
    o += T(pl.X(15), pl.Y(4.1) - 14, '最高點 *F*_{u} → 「NSF」用這裡', 14.5, COMP, 'middle', 'bold')
    o += T(pl.X(0.4), pl.Y(0.6), '彈性段只到 0.12%，', 13, MUT, 'start')
    o += T(pl.X(0.4), pl.Y(0.6) + 18, '在這張圖上幾乎是垂直線', 13, MUT, 'start')
    o += T(450, 404, '數值為 A36 的量級示意：*F*_{y} 時應變約 0.12%，平台末端約 1.5%，最高點約 15%，斷裂約 20% 以上', 13, MUT, 'middle')
    return svg(W, H, o, '鋼材應力應變曲線')


def fig2_3():
    W, H = 900, 330
    sc = 520 / 600.0     # px / cm
    x0 = 80
    o = ''
    rows = [('GSY 全斷面降伏', '降伏區＝整根桿身 600 cm', 600, 0.02, TEN, TEN2, 'φ_{t} = 0.90'),
            ('NSF 淨斷面斷裂', '斷裂區＝孔那一排，約 5 cm', 5, 0.10, COMP, COMP2, 'φ_{t} = 0.75')]
    for i, (name, zone, Lz, eps, c, c2, phi) in enumerate(rows):
        y = 70 + i * 135
        o += T(x0, y - 22, name, 16, c, 'start', 'bold') + T(x0 + 175, y - 22, zone, 14, INK, 'start')
        o += R(x0, y, 600 * sc, 30, STEEL2, INK, 1.4, 3)
        if Lz >= 600:
            o += R(x0, y, 600 * sc, 30, c2, c, 1.6, 3)
        else:
            xm = x0 + 300 * sc
            o += R(xm - Lz * sc / 2, y - 3, Lz * sc, 36, c, None, 0, 2)
        o += A(x0 - 6, y + 15, x0 - 44, y + 15, INK, 2.4, 10) + A(x0 + 600 * sc + 6 + 0, y + 15, x0 + 600 * sc + 44, y + 15, INK, 2.4, 10)
        dl = Lz * eps
        w = dl * sc * 5
        xe = x0 + 600 * sc + 52
        o += R(xe, y, max(w, 2.5), 30, c, None, 0, 2, op=0.9)
        o += T(xe + max(w, 2.5) + 10, y + 21, f'伸長 ≈ {dl:g} cm', 15, c, 'start', 'bold')
        o += T(880, y - 22, f'{Lz:g} cm × {eps * 100:g}% = {dl:g} cm', 14, c, 'end', 'bold')
        o += T(x0, y + 58, ('整根都在伸長，肉眼看得到 → 延性、有預警 → ' if i == 0 else '只有一小段在伸長，整根幾乎不動就斷 → 脆性、無預警 → ') + phi,
               14.5, INK, 'start')
    o += T(450, 318, '伸長量（色塊）以相同比例放大 5 倍繪製；應變為量級估算', 13, MUT, 'middle')
    return svg(W, H, o, '降伏區長度與預警')


def fig2_4():
    W, H = 900, 380
    o = ''
    # LRFD 數線
    def X(phi):
        return 120 + (phi - 0.70) / 0.25 * 640
    y1 = 110
    o += T(40, y1 + 5, 'LRFD φ', 16, AC, 'start', 'bold')
    o += A(X(0.70), y1, X(0.96), y1, INK, 1.8)
    for v in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
        o += L(X(v), y1 - 5, X(v), y1 + 5, INK, 1.2) + T(X(v), y1 + 24, f'{v:.2f}', 13, MUT, 'middle')
    pts = [(0.75, '斷裂、塊狀剪力', '銲道、螺栓', COMP), (0.85, '柱挫屈', '（第 10 章）', KEY), (0.90, '降伏', '（梁彎曲也是）', TEN)]
    for v, a, b, c in pts:
        o += C(X(v), y1, 9, c, '#fff', 2)
        o += T(X(v), y1 - 42, a, 14.5, c, 'middle', 'bold') + T(X(v), y1 - 22, b, 13, c, 'middle')
    o += A(X(0.74), 52, X(0.92), 52, MUT, 1.6, 9, dash='5 4')
    o += T(X(0.83), 44, '破壞前預警越明顯、結果越可預測 → φ 越大', 13.5, MUT, 'middle')
    # ASD 數線
    y2 = 270
    o += T(40, y2 + 5, 'ASD Ω', 16, WARN, 'start', 'bold')
    o += T(40, y2 + 25, '＝1.5/φ', 13, WARN, 'start')
    for v, c in ((0.75, COMP), (0.85, KEY), (0.90, TEN)):
        om = 1.5 / v
        o += L(X(v), y1 + 34, X(v), y2 - 34, c, 1.6, '5 4')
        o += T(X(v) + 6, (y1 + y2) / 2 + 4, '÷1.5', 13, c, 'start')
        o += R(X(v) - 58, y2 - 24, 116, 48, '#fff', c, 1.8, 8)
        o += T(X(v), y2 - 3, f'Ω = {om:.2f}', 15, c, 'middle', 'bold')
        sub = {0.75: '容許 0.5*F*_{u}', 0.85: '（柱另有 FS 式）', 0.90: '容許 0.6*F*_{y}'}[v]
        o += T(X(v), y2 + 16, sub, 13.5, INK, 'middle')
    o += R(150, 318, 600, 50, WARN2, WARN, 1.3, 8)
    o += T(450, 340, 'ASD 的容許應力 ＝ LRFD 的 φ × 強度 ÷ 1.5', 15, WARN, 'middle', 'bold')
    o += T(450, 360, '0.90*F*_{y}÷1.5 = 0.6*F*_{y}　　0.75*F*_{u}÷1.5 = 0.5*F*_{u}', 15, INK, 'middle')
    return svg(W, H, o, 'φ 與 Ω')


def fig2_5():
    W, H = 900, 440
    pl = Plot(100, 50, 600, 310, 0.5, 1.0, 0.4, 1.3)
    o = pl.axes([0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.4, 0.6, 0.8, 0.9, 1.0, 1.2], '*A*_{e} / *A*_{g}', '強度 ÷ (*F*_{y}*A*_{g})')
    Fy, Fu = STEELS['A36']
    xc = 1.2 * Fy / Fu
    o += R(pl.X(0.5), pl.y0, pl.X(xc) - pl.X(0.5), pl.h, COMP2, None, 0, op=0.7)
    o += T((pl.X(0.5) + pl.X(xc)) / 2, pl.y0 + 22, 'A36：NSF 控制', 14, COMP, 'middle', 'bold')
    o += T((pl.X(xc) + pl.X(1.0)) / 2, pl.y0 + 22, 'A36：GSY 控制', 14, TEN, 'middle', 'bold')
    o += pl.hline(0.9, 0.5, 1.0, TEN, 3.4, None)
    o += T(pl.X(0.505), pl.Y(0.9) - 10, 'GSY：0.90（水平線）', 14.5, TEN, 'start', 'bold')
    for name, c, dash in (('A36', COMP, None), ('A572-50', WARN, '8 5')):
        Fy, Fu = STEELS[name]
        k = 0.75 * Fu / Fy
        o += P([pl.pt(0.5, 0.5 * k), pl.pt(1.0, k)], c, 3, dash=dash)
        xx = 1.2 * Fy / Fu
        o += pl.dot(xx, 0.9, c, 6)
        o += pl.vline(xx, 0.4, 0.9, c, 1.3, '4 4')
        o += T(pl.X(xx), pl.Y(0.4) + 38, f'{xx:.3f}', 14, c, 'middle', 'bold')
        o += T(pl.X(1.0) + 8, pl.Y(k) + 5, f'NSF（{name}）', 14, c, 'start', 'bold')
    ex = D['ratio']; ey = 0.75 * D['Fu'] / D['Fy'] * ex
    o += C(pl.X(ex), pl.Y(ey), 7, KEY, '#fff', 2)
    o += A(pl.X(ex) - 70, pl.Y(ey) + 100, pl.X(ex) - 8, pl.Y(ey) + 6, KEY, 2, 10)
    o += T(pl.X(ex) - 74, pl.Y(ey) + 118, f'本章範例 {ex:.3f}', 14, KEY, 'end', 'bold')
    o += T(pl.X(ex) - 74, pl.Y(ey) + 136, '< 0.738 → NSF 控制', 14, KEY, 'end', 'bold')
    o += R(720, 250, 170, 104, KEY2, KEY, 1.3, 8)
    o += T(805, 274, '交點：', 14, KEY, 'middle', 'bold')
    o += T(805, 298, '*A*_{e}/*A*_{g} = 1.2 *F*_{y}/*F*_{u}', 14, KEY, 'middle', 'bold')
    o += T(805, 322, 'ASD 也是同一個數', 13, INK, 'middle')
    o += T(805, 342, '（兩邊同除 1.5）', 13, INK, 'middle')
    return svg(W, H, o, '誰控制')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5}
