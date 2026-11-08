# -*- coding: utf-8 -*-
"""第 8 章：梁的接合——切一刀看平衡（S6）。SS-2018-3、SS-2019-4、SS-2020-4。"""
from plot import *  # noqa
from calcs import ss2018_3, ss2019_4, ss2020_4
import math

A18 = ss2018_3()
A19 = ss2019_4()
A20 = ss2020_4()


def fig8_1():
    W, H = 900, 460
    s = 0.62
    ox, oy = 140, 60
    d, bf, tf, tw = A18['d'], A18['bf'], A18['tf'], A18['tw']
    o = T(250, 28, '(a) H500×200×9×16 與彎曲應力（依比例）', 16, INK, 'middle', 'bold')
    cx = ox + bf * s / 2
    o += R(ox, oy, bf * s, tf * s, STEEL3, INK, 1.2) + R(ox, oy + (d - tf) * s, bf * s, tf * s, STEEL3, INK, 1.2)
    o += R(cx - tw * s / 2, oy + tf * s, tw * s, (d - 2 * tf) * s, STEEL3, INK, 1.0)
    # 應力分布（線性）
    sx = ox + bf * s + 150
    ymid = oy + d * s / 2
    smax = 100
    o += L(sx, oy, sx, oy + d * s, INK, 1.4)
    o += P([(sx, oy), (sx + smax, oy), (sx - smax, oy + d * s), (sx, oy + d * s)], None, fill=WARN2, close=True)
    o += L(sx + smax, oy, sx - smax, oy + d * s, WARN, 2.4)
    o += T(sx + smax + 6, oy + 14, '拉', 15, WARN, 'start', 'bold')
    o += T(sx - smax, oy + d * s + 22, '壓', 15, WARN, 'middle', 'bold')
    o += A(cx + 70, oy + tf * s / 2, cx + 130, oy + tf * s / 2, TEN, 3, 11)
    o += A(cx + 130, oy + (d - tf / 2) * s, cx + 70, oy + (d - tf / 2) * s, COMP, 3, 11)
    o += T(cx + 66, oy + tf * s / 2 - 10, '*F*_{f}', 16, TEN, 'end', 'bold')
    o += T(cx + 66, oy + (d - tf / 2) * s + 24, '*F*_{f}', 16, COMP, 'end', 'bold')
    o += dim(ox - 26, oy + tf * s / 2, ox - 26, oy + (d - tf / 2) * s, '*d* − *t*_{f} = 484', INK, 0, 14, side=-1)
    o += T(250, 446, '平面保持平面 → 同一個曲率 → 各部分分到的彎矩 ∝ 自己的 *I*', 15, KEY, 'middle', 'bold')
    # (b) 分配
    o += R(560, 70, 320, 290, '#fff', KEY, 1.6, 10)
    rows = [(f'*I*_{{f}}（兩翼板）= {A18["If"]/1e6:.1f} × 10⁶ mm⁴', INK),
            (f'*I*_{{w}}（腹板）= {A18["Iw"]/1e6:.1f} × 10⁶ mm⁴', INK),
            (f'*M*_{{f}} = 150 × *I*_{{f}}/*I* = {A18["Mf"]:.1f} kNm', TEN),
            (f'*M*_{{w}} = 150 × *I*_{{w}}/*I* = {A18["Mw"]:.1f} kNm', TEN),
            ('考卷直接給 124.5 / 25.5（一致）', MUT),
            (f'*F*_{{f}} = *M*_{{f}}/(*d* − *t*_{{f}}) = {A18["Ff"]:.1f} kN', COMP)]
    for i, (t, c) in enumerate(rows):
        o += T(720, 106 + i * 42, t, 15, c, 'middle', 'bold' if c in (TEN, COMP) else None)
    return svg(W, H, o, '翼板力偶與腹板分擔')


def fig8_2():
    W, H = 900, 360
    pl = Plot(110, 50, 300, 260, 0, 140, 0, 140)
    o = T(260, 28, '(a) 腹板銲道最外點：兩個方向的剪應力', 16, INK, 'middle', 'bold')
    ox, oy, sc = 150, 300, 1.7
    t1, t2, t = A18['tau1'], A18['tau2'], A18['tau']
    o += A(ox, oy, ox + t1 * sc, oy, WARN, 3, 11) + T(ox + t1 * sc / 2, oy + 24, f'τ_{{w1}} = *M*_{{w}}/*S*_{{w}} = {t1:.1f}', 15, WARN, 'middle', 'bold')
    o += A(ox + t1 * sc, oy, ox + t1 * sc, oy - t2 * sc, AC, 3, 11) + T(ox + t1 * sc + 8, oy - t2 * sc / 2 + 5, f'τ_{{w2}} = *Q*/*A*_{{w}} = {t2:.1f}', 15, AC, 'start', 'bold')
    o += A(ox, oy, ox + t1 * sc, oy - t2 * sc, COMP, 3.6, 12)
    o += T(ox + t1 * sc / 2 - 10, oy - t2 * sc / 2 - 16, f'τ = {t:.1f}', 16, COMP, 'middle', 'bold')
    # 容許圓弧
    fa = A18['fa']
    pts = [(ox + fa * sc * math.cos(a), oy - fa * sc * math.sin(a)) for a in [i * math.pi / 2 / 60 for i in range(61)]]
    o += P(pts, TEN, 2, dash='6 4')
    o += T(ox + fa * sc * 0.72 - 6, oy - fa * sc * 0.72 - 8, f'容許 *f*_{{a}} = {fa}', 15, TEN, 'end', 'bold')
    o += T(260, 100, '單位 N/mm²（ASD）', 14, MUT, 'middle')
    o += R(500, 70, 380, 240, '#fff', KEY, 1.6, 10)
    rows = [('(b) 6 mm 銲腳不夠，反算 *w*', KEY), (f'τ ∝ 1/*w*（喉厚 0.707*w* 在分母）', INK),
            (f'*w*_{{req}} = 6 × {t:.1f}/{fa} = {A18["w_req"]:.2f} mm', COMP), ('→ 取 9 mm', COMP),
            ('只拿 τ_{w1} 比 *f*_{a} 會漏掉剪力', INK), ('（考卷只給 τ_{w1}）', MUT)]
    for i, (s_, c) in enumerate(rows):
        o += T(690, 104 + i * 38, s_, 16 if i == 0 else 15, c, 'middle', 'bold' if c in (KEY, COMP) else None)
    return svg(W, H, o, '腹板銲道組合應力')


def fig8_3():
    W, H = 900, 460
    o = T(450, 28, 'SS-2019-4：切開蓋板，看它的左右兩端差多少力', 16, INK, 'middle', 'bold')
    # 左：斷面
    s = 4.0
    ox, oy = 90, 70
    bp, tp, H_, bf, tf, tw = A19['bp'], A19['tp'], A19['H'], A19['bf'], A19['tf'], A19['tw']
    cx = ox + bp * s / 2
    o += R(cx - bp * s / 2, oy, bp * s, tp * s, KEY2, KEY, 1.6)
    top = oy + tp * s
    o += R(cx - bf * s / 2, top, bf * s, tf * s, STEEL3, INK, 1.2)
    sh = 1.0  # 斷面高度縮放（只畫上半）
    hw = 18
    o += R(cx - tw * s / 2, top + tf * s, tw * s, hw * s, STEEL3, INK, 1.0)
    o += T(cx, top + tf * s + hw * s + 22, '（下半省略）', 14, MUT, 'middle')
    yna = oy + (H_ + tp - A19['ybar']) * s
    o += L(cx - bp * s / 2 - 10, yna, cx + bp * s / 2 + 10, yna, KEY, 1.6, '6 4')
    o += T(cx + bp * s / 2 + 14, yna + 5, '中性軸', 14, KEY, 'start', 'bold')
    o += dim(cx + bp * s / 2 + 30, oy + tp * s / 2, cx + bp * s / 2 + 30, yna, f'{A19["H"] + tp / 2 - A19["ybar"]:.2f}', INK, 0, 14)
    for xs in (-1, 1):
        x = cx + xs * bf * s / 2
        o += P([(x, top), (x + xs * 10, top), (x, top - 10)], None, fill=COMP, close=True)
    o += T(cx, oy - 10, '蓋板 PL25×300', 15, KEY, 'middle', 'bold')
    o += T(cx, 330, f'*Q* = 75 × {A19["H"] + tp / 2 - A19["ybar"]:.2f} = {A19["Q"]:.0f} cm³', 15, INK, 'middle')
    o += T(cx, 356, f'*I* = {A19["I"]:,.0f} cm⁴', 15, INK, 'middle')
    # 右：側視自由體
    px, py, Lp = 370, 120, 420
    o += R(px, py, Lp, 40, KEY2, KEY, 1.6)
    o += A(px - 70, py + 20, px - 6, py + 20, COMP, 3, 11) + T(px - 40, py - 4, '*C*', 16, COMP, 'middle', 'bold')
    o += A(px + Lp + 70, py + 20, px + Lp + 6, py + 20, COMP, 3.6, 12) + T(px + Lp + 38, py - 4, '*C* + Δ*C*', 16, COMP, 'middle', 'bold')
    for i in range(4):
        x0 = px + 20 + i * 110
        o += R(x0, py + 40, 37, 10, COMP, None)
        o += A(x0 - 12, py + 58, x0 + 52, py + 58, AC, 2, 8)
    o += T(px + Lp / 2, py + 92, '銲道（每段 *L*、中心距 *s* = 15 cm）把 Δ*C* 補回來', 15, AC, 'middle', 'bold')
    o += dim(px + 20 + 18, py - 18, px + 130 + 18, py - 18, '*s* = 15', INK, 0, 14, side=-1)
    rows = [f'Δ*C*/Δ*x* = (Δ*M*/Δ*x*)·*Q*/*I* = *VQ*/*I* = *q* = {A19["q"]:.4f} tf/cm',
            f'每段負責 *q*·*s* = {A19["Fs"]:.2f} tf',
            f'雙面 8 mm：每 cm {A19["cap_per_cm"]:.3f} tf → *L* = {A19["L"]:.2f} → 5 cm',
            f'構造：*L* ≥ 4*w* 且 ≥ 40 mm → {A19["Lmin"]:.0f} cm，未控制']
    for i, t in enumerate(rows):
        o += T(px + Lp / 2, 260 + i * 34, t, 15, COMP if i == 2 else INK, 'middle', 'bold' if i == 2 else None)
    return svg(W, H, o, '剪力流與斷續銲')


def fig8_4():
    W, H = 900, 490
    o = T(260, 28, '(a) SS-2020-4 腹板續接：每側一列 6 顆（雙剪）', 16, INK, 'middle', 'bold')
    cx, cy, s, fs = 200, 260, 7, 4
    o += R(cx - 60, cy - 24 * s, 120, 48 * s, STEEL2, INK, 1.2)
    o += L(cx + 40, cy - 26 * s, cx + 40, cy + 26 * s, MUT, 1.2, '6 4')
    o += T(cx + 44, cy - 24 * s - 6, '續接縫', 14, MUT, 'start')
    o += dim(cx, cy + 24 * s + 18, cx + 40, cy + 24 * s + 18, '*e* = 5', INK, 0, 14)
    ys = [20, 12, 4, -4, -12, -20]
    for y in ys:
        by = cy - y * s
        o += C(cx, by, 7, '#fff', INK, 1.4)
        fh = A20['M'] * y / A20['Sy2']
        o += A(cx, by, cx, by + A20['fv'] * fs, WARN, 2, 8)
        o += A(cx, by + A20['fv'] * fs, cx + fh * fs, by + A20['fv'] * fs, AC, 2, 8)
        o += A(cx, by, cx + fh * fs, by + A20['fv'] * fs, COMP, 2.8 if abs(y) == 20 else 1.6, 9)
    o += T(cx - 70, cy - 20 * s + 5, f'{A20["R"]:.2f}', 15, COMP, 'end', 'bold')
    o += T(cx - 70, cy + 20 * s + 5, f'{A20["R"]:.2f}', 15, COMP, 'end', 'bold')
    o += R(480, 70, 400, 290, '#fff', KEY, 1.6, 10)
    rows = [('(b) 第 6 章的特例：只有一行（*x* = 0）', KEY), (f'*I*_{{p}} = Σ*y*² = 2(4² + 12² + 20²) = {A20["Sy2"]}', INK),
            (f'*M* = *V*·*e* = 70 × 5 = {A20["M"]:.0f} tf·cm', INK), (f'直接 *V*/*n* = {A20["fv"]:.2f}（向下，橘）', WARN),
            (f'扭矩 *M y*_{{max}}/Σ*y*² = {A20["fh"]:.2f}（水平，藍）', AC), (f'*R* = √(11.67² + 6.25²) = {A20["R"]:.2f} tf', COMP),
            (f'雙剪 A490：*A*_{{b}} ≥ {A20["Ab_req"]:.3f} cm² → M20', INK)]
    for i, (t, c) in enumerate(rows):
        o += T(680, 104 + i * 37, t, 15, c, 'middle', 'bold' if c in (KEY, COMP) else None)
    return svg(W, H, o, 'SS-2020-4 腹板續接螺栓')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3, 'fig8_4': fig8_4}
