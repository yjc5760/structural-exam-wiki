# -*- coding: utf-8 -*-
"""第 2 章：軸力修正——莫爾圓左右移、Vc–Nu 直線、ρw 第二式。"""
from figs_common import *  # noqa
from calcs import mohr, crack_angle, p2010_3, p2014_3, PHI_V
import math

P10 = p2010_3()
P14 = p2014_3()


def fig2_1():
    W, H = 900, 470
    o = T(450, 24, '同一個剪應力 τ：軸壓、無軸力、軸拉', 16, INK, 'middle', 'bold')
    cases = [(-1.0, '軸壓 σ = −τ', COMP), (0.0, '無軸力', INK), (1.0, '軸拉 σ = +τ', TEN)]
    for i, (sg, lab, col) in enumerate(cases):
        cx0 = 150 + i * 300
        pl = Plot(cx0 - 120, 60, 240, 190, -2.0, 2.0, -1.6, 1.6)
        o += L(pl.X(-2.0), pl.Y(0), pl.X(2.0), pl.Y(0), MUT, 1.2)
        o += L(pl.X(0), pl.Y(1.6), pl.X(0), pl.Y(-1.6), MUT, 1.2)
        c = sg / 2; r = math.sqrt(c * c + 1)
        pts = [pl.pt(c + r * math.cos(t / 120 * 2 * math.pi), r * math.sin(t / 120 * 2 * math.pi)) for t in range(121)]
        o += P(pts, KEY, 2.4)
        s1, s2, th = mohr(sg, 1)
        o += pl.dot(s1, 0, TEN, 6) + pl.dot(c, 0, KEY, 3.5)
        o += T(pl.X(s1) + (6 if i < 2 else -6), pl.Y(0) - 10 if i < 2 else pl.Y(0) + 26, f'σ_{{1}} = {s1:.2f}τ', 14, TEN, 'start' if i < 2 else 'end', 'bold')
        o += T(cx0, 58, lab, 15, col, 'middle', 'bold')
        # 下：梁段與裂縫
        bx, by, bw_, bh_ = cx0 - 110, 300, 220, 90
        o += R(bx, by, bw_, bh_, STEEL2, INK, 1.4)
        ang = crack_angle(sg, 1)
        dx = bh_ / math.tan(math.radians(ang))
        for k in range(3):
            xs = bx + 22 + k * 48
            xe = min(xs + dx * 0.85, bx + bw_ - 8)
            t = (xe - xs) / (dx * 0.85)
            o += L(xs, by + bh_ - 6, xe, by + bh_ - 6 - t * (bh_ - 16), COMP, 2.2)
        if sg < 0:
            o += A(bx - 34, by + bh_ / 2, bx - 4, by + bh_ / 2, COMP, 2, 9) + A(bx + bw_ + 34, by + bh_ / 2, bx + bw_ + 4, by + bh_ / 2, COMP, 2, 9)
        elif sg > 0:
            o += A(bx - 4, by + bh_ / 2, bx - 34, by + bh_ / 2, TEN, 2, 9) + A(bx + bw_ + 4, by + bh_ / 2, bx + bw_ + 34, by + bh_ / 2, TEN, 2, 9)
        o += T(cx0, by + bh_ + 30, f'裂縫與梁軸夾 {ang:.1f}°', 15, col, 'middle', 'bold')
        o += T(cx0, by + bh_ + 54, ['較平緩', '基準', '較陡'][i], 14, MUT, 'middle')
    return svg(W, H, o, '軸力與莫爾圓')


def fig2_2():
    W, H = 900, 400
    pl = Plot(110, 50, 520, 280, -40, 40, 0, 20)
    o = pl.axes([-40, -30, -20, -10, 0, 10, 20, 30, 40], [0, 5, 10, 15, 20], '*N*_{u}', 'φ*V*_{c}', size=14)
    o += T(pl.X(40) + 18, pl.Y(0) + 26, '(tf，壓為正)', 14, MUT, 'start')
    o += T(pl.X(-40) + 40, pl.Y(20) - 22, '(tf)', 14, MUT, 'start')
    fc, bw, d, Ag = P10['fc'], P10['bw'], P10['d'], P10['Ag']
    base = 0.53 * math.sqrt(fc) * bw * d

    def cur(N):
        return PHI_V * max(0, (0.53 * math.sqrt(fc) + N * 1000 / (6 * Ag)) * bw * d) / 1000

    def old(N):
        k = (1 + N * 1000 / (140 * Ag)) if N >= 0 else max(0, 1 + N * 1000 / (35 * Ag))
        return PHI_V * base * k / 1000
    o += pl.curve(old, -40, 40, MUT, 2.2, dash='7 5')
    o += pl.curve(cur, -40, 40, COMP, 3.2)
    for k, N in (('c', -30), ('a', 0), ('b', 30)):
        v = P10['cases'][k]['phiVc'] / 1000
        o += pl.dot(N, v, COMP, 6)
        o += T(pl.X(N), pl.Y(v) - 14, f'{v:.2f}', 15, COMP, 'middle', 'bold')
    o += pl.dot(30, P10['old_b'] / 1000, MUT, 5) + pl.dot(-30, P10['old_c'] / 1000, MUT, 5)
    o += T(pl.X(30) + 8, pl.Y(P10['old_b'] / 1000) + 20, f"舊 {P10['old_b']/1000:.2f}", 14, MUT, 'start')
    o += T(pl.X(-30) + 8, pl.Y(P10['old_c'] / 1000) + 20, f"舊 {P10['old_c']/1000:.2f}", 14, MUT, 'start')
    o += pl.hline(20, -40, 40, WARN, 1.6, '4 3')
    o += T(pl.X(-38), pl.Y(20) + 18, '*V*_{u} = 20 tf', 14, WARN, 'start', 'bold')
    o += box(660, 80, 225, 180, '現行式', ['φ[0.53√*f*′_{c} + *N*_{u}/6*A*_{g}]*b*_{w}*d*', '一條直線', '壓拉對稱', '（紅實線）', '灰虛線：舊 140／35'], COMP2, COMP, 15, 14)
    return svg(W, H, o, 'Vc 與軸力')


def fig2_3():
    W, H = 900, 380
    pl = Plot(110, 50, 520, 270, 0, 4, 0, 1.6)
    o = pl.axes([0, 1, 2, 3, 4], [0, 0.4, 0.8, 1.2, 1.6], 'ρ_{w}', '*V*_{c}/√*f*′_{c}*b*_{w}*d*', size=14, yfmt=lambda v: f'{v:.1f}')
    o += T(pl.X(4) + 18, pl.Y(0) + 26, '(%)', 14, MUT, 'start')
    o += pl.curve(lambda r: 2.1 * (r / 100) ** (1 / 3), 0.001, 4, AC, 3)
    o += pl.hline(0.53, 0, 4, COMP, 3, None)
    o += pl.hline(1.33, 0, 4, MUT, 1.6, '6 4')
    o += T(pl.X(0.1), pl.Y(1.33) - 10, '上限 1.33', 15, MUT, 'start', 'bold')
    rx = (0.53 / 2.1) ** 3 * 100
    o += pl.vline(rx, 0, 0.53, KEY, 1.6)
    o += pl.dot(rx, 0.53, KEY, 6)
    o += T(pl.X(rx) + 8, pl.Y(0.53) + 34, f'交點 ρ_{{w}} = {rx:.2f}%', 15, KEY, 'start', 'bold')
    o += T(pl.X(0.05), pl.Y(0.53) - 10, '簡化式 0.53', 15, COMP, 'start', 'bold')
    o += T(pl.X(3.9), pl.Y(2.1 * 0.039 ** (1 / 3)) - 12, '2.1ρ_{w}^{1/3}', 15, AC, 'end', 'bold')
    rw = P14['rho'] * 100
    o += pl.dot(rw, 2.1 * P14['rho13'], AC, 5)
    o += T(pl.X(rw) - 6, pl.Y(2.1 * P14['rho13']) + 28, f'RC-2014-3：{rw:.2f}%', 14, AC, 'end')
    o += box(665, 70, 220, 170, '取大', ['ρ_{w} < 1.61%：', '簡化式控制', '（一般梁幾乎都是）', 'ρ_{w} > 1.61%：', '第二式控制'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'ρw 第二式')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
