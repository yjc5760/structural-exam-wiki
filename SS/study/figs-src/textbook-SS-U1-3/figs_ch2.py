# -*- coding: utf-8 -*-
"""第 2 章：放大係數 1/(1−α) — 幾何級數、曲線、整層 B2、ASD 的 F'e。數字取自 calcs.py。"""
from plot import *  # noqa
from calcs import ex2014, amp, amp_sec, series_terms, W
import math

A_DEMO = 0.5          # 示意用的 α（放大到看得清楚）


def fig2_1():
    W_, H = 900, 440
    o = T(200, 30, '(a) 一輪一輪疊上去（α = 0.5 示意）', 16, INK, 'middle', 'bold')
    xc, yt, yb = 90, 110, 380
    o += L(xc, yt - 10, xc, yb + 10, MUT, 1.2, '6 5')
    terms = series_terms(A_DEMO, 4)
    cols = [AC, COMP, COMPM, '#f8bbd0']
    acc = 0
    sc = 62     # 1.0 的撓度畫成 62 px
    labs = ['δ_{0}：一階', '+αδ_{0}：第 1 輪', '+α²δ_{0}：第 2 輪', '+α³δ_{0}：…']
    for k, t in enumerate(terms):
        acc += t
        o += P([(xc + sc * acc * math.sin(math.pi * i / 80), yt + (yb - yt) * i / 80) for i in range(81)], cols[k], 4 if k == 0 else 3,
               dash=None if k == 0 else '7 4')
        o += T(xc + sc * 2 + 22, yt + (yb - yt) / 2 - 50 + k * 34, labs[k], 14.5, (AC, COMP, '#e57373', '#e57373')[k], 'start', 'bold' if k < 2 else None)
    o += P([(xc, yt), (xc - 10, yt - 15), (xc + 10, yt - 15)], INK, 1.5, '#fff', close=True)
    o += pin(xc, yb)
    o += A(xc, yt - 50, xc, yt - 18, COMP, 3, 12) + T(xc + 12, yt - 30, '*P*', 16, COMP, 'start', 'bold')
    # (b) 堆疊長條
    o += L(470, 20, 470, 430, GRID, 1.5)
    o += T(680, 30, '(b) 累計撓度 ÷ δ_{0}', 16, INK, 'middle', 'bold')
    bx, bw = 490, 320          # 2.0 對應 bw
    s = 0
    yy = 70
    cumul = []
    for k, t in enumerate(series_terms(A_DEMO, 6)):
        s += t
        cumul.append(s)
    for k, t in enumerate(series_terms(A_DEMO, 6)):
        x = bx + bw * (cumul[k] - t) / 2.0
        o += R(x, yy + k * 44, bw * t / 2.0, 30, COMP if k else AC, '#fff', 1, 3, op=0.9 if k else 0.85)
        o += T(bx + bw + 14, yy + k * 44 + 21, f'{cumul[k]:.3f}', 15, INK, 'start', 'bold' if k == 0 else None)
    o += L(bx, yy - 8, bx, yy + 6 * 44, INK, 1.4)
    o += L(bx + bw, yy - 14, bx + bw, yy + 6 * 44 + 4, KEY, 2.2, '6 4')
    o += T(bx + bw, yy + 6 * 44 + 24, '極限 1/(1 − α) = 2', 15, KEY, 'end', 'bold')
    o += R(492, 384, 380, 46, KEY2, KEY, 1.4, 8)
    o += T(682, 413, '1 + α + α² + … ＝ 1/(1 − α)', 17, KEY, 'middle', 'bold')
    return svg(W_, H, o, '幾何級數')


def fig2_2():
    d = ex2014()
    W_, H = 900, 450
    pl = Plot(90, 50, 560, 330, 0, 1.0, 1.0, 6.0)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], [1, 2, 3, 4, 5, 6], 'α = *P*/*P*_{e}', '放大倍數', size=14)
    a_sec6 = 4 / math.pi ** 2 * math.acos(1 / 6) ** 2      # sec(π√α/2) = 6 的 α
    o += pl.curve(lambda a: amp_sec(a), 0, a_sec6, KEY, 2.2, dash='7 5', clip=False)
    o += pl.curve(lambda a: amp(a), 0, 1 - 1 / 6, COMP, 3.6, clip=False)
    o += pl.vline(1.0, c=INK, dash='4 4')
    o += T(pl.X(1.0) - 8, pl.Y(1.35), 'α → 1：*P* = *P*_{e}，挫屈', 14, INK, 'end')
    o += pl.dot(0.5, 2.0, COMP, 6)
    o += T(pl.X(0.5) - 12, pl.Y(2.0) - 12, 'α = 0.5 → 放大 2 倍', 14, COMP, 'end', 'bold')
    # 範例兩點（靠近原點，用引線拉出）
    for a, lab, yl in ((d['alpha1'], f'*P*_{{u}}/*P*_{{e1}} = {d["alpha1"]:.3f} → {d["amp1"]:.3f}', 3.35),
                       (d['alpha2'], f'α_{{2}} = {d["alpha2"]:.3f} → *B*_{{2}} = {d["B2"]:.3f}', 2.75)):
        o += pl.dot(a, amp(a), AC, 5)
        o += L(pl.X(a), pl.Y(amp(a)), pl.X(0.16), pl.Y(yl), AC, 1.2)
        o += T(pl.X(0.165), pl.Y(yl) + 5, lab, 14, AC, 'start', 'bold')
    o += T(pl.X(0.165), pl.Y(3.95) + 5, 'SS-2014-4 的兩個 α：', 14, INK, 'start')
    # 圖例
    o += R(670, 70, 220, 132, '#fff', GRID, 1.2, 8)
    o += L(684, 98, 724, 98, COMP, 3.6) + T(732, 103, '1/(1 − α)', 15, COMP, 'start', 'bold')
    o += L(684, 132, 724, 132, KEY, 2.2, '7 5') + T(732, 137, '兩端等值彎矩', 14, KEY, 'start')
    o += T(732, 158, '的精確解', 14, KEY, 'start')
    o += T(732, 182, 'sec(π√α/2)', 14, KEY, 'start')
    o += R(670, 230, 220, 120, KEY2, KEY, 1.4, 8)
    o += T(780, 256, '三個極限', 15, KEY, 'middle', 'bold')
    o += T(780, 282, 'α = 0 → 1（純梁）', 14, INK, 'middle')
    o += T(780, 306, 'α = 0.5 → 2', 14, INK, 'middle')
    o += T(780, 330, 'α → 1 → ∞（挫屈）', 14, INK, 'middle')
    return svg(W_, H, o, '放大曲線')


def fig2_3():
    d = ex2014()
    W_, H = 900, 400
    o = T(220, 30, '整層樓：側移也是一輪一輪疊', 16, AC, 'middle', 'bold')
    xl, xr, yt, yb, D = 90, 330, 110, 330, 46
    o += L(xl, yt, xl, yb, MUT, 1.2, '6 5') + L(xr, yt, xr, yb, MUT, 1.2, '6 5') + L(xl, yt, xr, yt, MUT, 1.2, '6 5')
    o += L(xl + D, yt, xl, yb, AC, 5) + L(xr + D, yt, xr, yb, AC, 5) + L(xl + D, yt, xr + D, yt, STEEL, 9)
    o += pin(xl, yb) + pin(xr, yb)
    o += A(xl - 60, yt, xl + D - 10, yt, AC, 3.2, 12) + T(xl - 58, yt - 12, 'Σ*H*', 16, AC, 'start', 'bold')
    for x in (xl + D, xr + D):
        o += A(x, yt - 64, x, yt - 8, COMP, 3, 12)
    o += T((xl + xr) / 2 + D, yt - 50, 'Σ*P*', 16, COMP, 'middle', 'bold')
    o += dim(xr, yt + 26, xr + D, yt + 26, '', MUT)
    o += T(xr + D / 2, yt + 50, 'Δ', 16, MUT, 'middle', italic=True)
    o += dim(xr + D + 40, yt, xr + D + 40, yb, '*L*', MUT, size=15)
    o += A(xl - 60, yt + 46, xl - 4, yt + 46, COMP, 2.6, 11, dash='6 4')
    o += T(xl - 62, yt + 76, '等效側力 Σ*P*Δ/*L*', 14, COMP, 'start', 'bold')
    o += L(450, 20, 450, 390, GRID, 1.5)
    # 推導框
    o += R(470, 50, 415, 300, '#fff', AC, 1.6, 10)
    lines = [('① 一階：Σ*H* 推出 Δ_{0}', INK, None),
             ('   樓層勁度 *k* = Σ*H*/Δ_{0}', INK, None),
             ('② 柱頂 Σ*P* 錯開 Δ ⇒ 多一個', INK, None),
             ('   側力 Σ*P*Δ/*L*，又多推 Σ*P*Δ/(*kL*)', INK, None),
             ('③ 每輪是前一輪的 α_{2} 倍：', INK, None),
             ('α_{2} = Σ*P*Δ_{0} / (Σ*H*·*L*)', COMP, 'bold'),
             ('⇒ *B*_{2} = 1/(1 − α_{2})', KEY, 'bold')]
    for i, (s, c, w) in enumerate(lines):
        o += T(490, 84 + i * 38, s, 15 if w else 14.5, c, 'start', w)
    o += R(470, 360, 415, 34, KEY2, None, 0, 6)
    o += T(678, 383, f'本例：9000×18.75 / (600×3750) = {d["alpha2"]:.3f} → *B*_{{2}} = {d["B2"]:.3f}', 14, KEY, 'middle', 'bold')
    return svg(W_, H, o, '整層的 B2')


def fig2_4():
    d = ex2014()
    W_, H = 900, 250
    pl = Plot(70, 70, 760, 70, 0, 1200, 0, 1)
    o = T(450, 30, f'同一支 W14×90 的強軸（*K*_{{x}}*L*/*r*_{{x}} = {d["KLr_x"]:.2f}）：ASD 把 *F*_{{e}} 先打個 23/12 折', 16, INK, 'middle', 'bold')
    o += L(pl.X(0), pl.Y(0), pl.X(1200), pl.Y(0), INK, 1.6)
    for t in range(0, 1201, 200):
        o += L(pl.X(t), pl.Y(0), pl.X(t), pl.Y(0) + 6, INK, 1.2) + T(pl.X(t), pl.Y(0) + 26, str(t), 14, MUT, 'middle')
    o += T(pl.X(1200) + 6, pl.Y(0) + 5, 'MPa', 14, MUT, 'start')
    for v, lab, c, up in ((W['Fy'], f'*F*_{{y}} = {W["Fy"]:.0f}', TEN, 1),
                          (d['Fpe_x'], f'*F*′_{{e}} = {d["Fpe_x"]:.0f}', WARN, 1),
                          (d['Fe_x'], f'*F*_{{e}} = {d["Fe_x"]:.0f}', AC, 1)):
        o += L(pl.X(v), pl.Y(0), pl.X(v), pl.Y(0) - 46, c, 3)
        o += C(pl.X(v), pl.Y(0) - 46, 5, c, '#fff', 1.4)
        o += T(pl.X(v), pl.Y(0) - 58, lab, 15, c, 'middle', 'bold')
    o += curve_arrow([(pl.X(d['Fe_x']), pl.Y(0) + 40), ((pl.X(d['Fe_x']) + pl.X(d['Fpe_x'])) / 2, pl.Y(0) + 62),
                      (pl.X(d['Fpe_x']), pl.Y(0) + 40)], WARN, 2.2)
    o += T((pl.X(d['Fe_x']) + pl.X(d['Fpe_x'])) / 2, pl.Y(0) + 88, '÷ 23/12（ASD 細長柱的安全係數）', 15, WARN, 'middle', 'bold')
    return svg(W_, H, o, 'Fe 與 F′e')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4}
