# -*- coding: utf-8 -*-
"""第 2 章：板挫屈三種邊界、板挫屈曲線兩線取小、三種斷面的 M–θ、FLB 內插、ASD 直線。"""
from plot import *  # noqa
import math
import calcs

D = calcs.example()
R12 = calcs.ex_2012_1()


def fig2_1():
    """三種板：懸臂翼板、柱腹板（均勻壓）、梁腹板（彎曲）。上排：邊界與應力；下排：橫向挫屈形狀。"""
    W, H = 900, 430
    o = ''
    cols = [('(a) 翼板外伸肢', '一邊自由', 'uni', 'free', calcs.K_PLATE['一邊自由（懸臂翼板）'], COMP),
            ('(b) 柱的腹板', '兩邊支撐、均勻受壓', 'uni', 'ss', calcs.K_PLATE['兩邊簡支、均勻受壓（柱腹板）'], WARN),
            ('(c) 梁的腹板', '兩邊支撐、一半受拉', 'bend', 'ss', calcs.K_PLATE['兩邊簡支、純彎曲（梁腹板）'], AC)]
    for i, (t1, t2, load, bc, k, c) in enumerate(cols):
        ox = 30 + i * 295
        o += T(ox + 125, 30, t1, 16, c, 'middle', 'bold')
        o += T(ox + 125, 54, t2, 14, MUT, 'middle')
        # 板（正視，寬 b 為縱向）
        px, py, pw, ph = ox + 95, 104, 60, 170
        o += R(px, py, pw, ph, STEEL2, INK, 1.4)
        # 支撐邊
        o += L(px, py, px, py + ph, INK, 4)                 # 左邊一定支撐（與腹板或翼板相連）
        if bc == 'ss':
            o += L(px + pw, py, px + pw, py + ph, INK, 4)
        else:
            o += L(px + pw, py, px + pw, py + ph, MUT, 1.4, '5 4')
            o += T(px + pw + 8, py + ph / 2, '自由邊', 14, MUT, 'start')
        # 端部壓力（上下邊）箭頭：大小隨寬度位置
        for j in range(5):
            xx = px + 6 + j * (pw - 12) / 4
            sfrac = 1.0 if load == 'uni' else 1 - 2 * j / 4           # +1 壓、−1 拉
            ln = 22 * abs(sfrac)
            if ln < 3:
                continue
            cc = COMP if sfrac > 0 else TEN
            if sfrac > 0:
                o += A(xx, py - ln - 4, xx, py - 2, cc, 1.8, 8) + A(xx, py + ph + ln + 4, xx, py + ph + 2, cc, 1.8, 8)
            else:
                o += A(xx, py - 2, xx, py - ln - 4, cc, 1.8, 8) + A(xx, py + ph + 2, xx, py + ph + ln + 4, cc, 1.8, 8)
        # 橫向挫屈形狀（板寬方向的出平面變位）
        bx, by, bw = ox + 70, 345, 110
        o += L(bx, by, bx + bw, by, MUT, 1.2)
        pts = []
        for j in range(41):
            u = j / 40
            if bc == 'free':
                w = u
            elif load == 'uni':
                w = math.sin(math.pi * u)
            else:
                w = math.sin(math.pi * u) * (1.15 - u) * 1.3
            pts.append((bx + u * bw, by - 36 * w))
        o += P(pts, c, 2.6)
        o += T(bx + bw / 2, by + 24, '橫斷面的挫屈形狀', 14, MUT, 'middle')
        o += T(ox + 125, by + 56, f'*k* = {k}', 17, c, 'middle', 'bold')
    o += T(W / 2, H - 6, '同樣寬厚比：*k* 越大越難皺。自由邊最怕、受拉區會拉住受壓區', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '三種板的挫屈係數')


def fig2_2():
    """板挫屈應力 vs b/t，兩線取小；Fy 不同 → 交點 ∝ 1/√Fy。"""
    W, H = 900, 400
    k = 0.425
    pl = Plot(90, 40, 560, 290, 0, 24, 0, 6)
    o = pl.axes([0, 4, 8, 12, 16, 20, 24], [0, 1, 2, 3, 4, 5, 6], '*b*/*t*', '*F*_{cr}（tf/cm²）', size=14)
    fcr = lambda lam: k * math.pi ** 2 * calcs.E / (12 * (1 - calcs.NU ** 2) * lam ** 2)
    o += pl.curve(fcr, calcs.plate_coef(k) * math.sqrt(calcs.E / 6.0), 24, AC, 2.4)
    for Fy, cc in ((3.5, COMP), (2.5, TEN)):
        lam = calcs.plate_coef(k) * math.sqrt(calcs.E / Fy)
        o += pl.hline(Fy, 0, lam, cc, 2.4, None)
        o += pl.dot(lam, Fy, cc)
        o += pl.vline(lam, 0, Fy, cc, 1.2)
        o += T(pl.X(lam) + 8, pl.Y(Fy) - 10, f'{lam:.1f}', 15, cc, 'start', 'bold')
        o += T(pl.X(0.4), pl.Y(Fy) - 8, f'*F*_{{y}} = {Fy}', 14, cc, 'start')
    o += T(pl.X(13), pl.Y(5.0), '板的 Euler：*F*_{cr} ∝ *E*/(*b*/*t*)^{2}', 15, AC, 'start', 'bold')
    o += box(670, 60, 220, 150, '交點 ∝ 1/√*F*_{y}', ['*F*_{y} 越高，', '交點越往左', '→ 高強度鋼', '更要厚板'], KEY2, KEY, 16, 14)
    o += T(pl.X(12), pl.Y(0) + 46, '（一邊自由 *k* = 0.425 的彈性理論；規範係數另含試驗修正）', 14, MUT, 'middle')
    return svg(W, H, o, '板挫屈兩線取小')


def fig2_3():
    """三種斷面的彎矩–轉角行為（示意）。"""
    W, H = 900, 400
    pl = Plot(90, 40, 560, 290, 0, 10, 0, 1.25)
    o = pl.axes([0, 1, 3, 5, 7, 9], [0, D['Mr'] / D['Mp'], 1.0], 'θ/θ_{p}', '*M*/*M*_{p}', size=14,
                yfmt=lambda v: '1' if v == 1 else ('0' if v == 0 else '*M*_{r}'))

    def elastic_then(top, th_peak, drop_rate, th_end):
        def g(t):
            if t <= th_peak * top:
                return t / th_peak if t / th_peak < top else top
            if t <= th_end:
                return top
            return max(0.0, top - drop_rate * (t - th_end))
        return g

    mr = D['Mr'] / D['Mp']
    compact = elastic_then(1.0, 1.0, 0.12, 6.0)
    noncomp = elastic_then(0.83, 1.0, 0.25, 1.4)
    slender = elastic_then(0.48, 1.0, 0.25, 0.48)
    o += pl.hline(1.0, c=TEN) + pl.hline(mr, c=WARN)
    o += pl.curve(compact, 0, 10, TEN, 2.8)
    o += pl.curve(noncomp, 0, 6, WARN, 2.8)
    o += pl.curve(slender, 0, 3.5, COMP, 2.8)
    o += T(pl.X(3.5), pl.Y(1.0) - 26, '結實：到 *M*_{p} 還能再轉 3 倍以上', 15, TEN, 'middle', 'bold')
    o += T(pl.X(4.0), pl.Y(0.73), '非結實：*M*_{r}～*M*_{p} 之間就皺', 15, WARN, 'start', 'bold')
    o += T(pl.X(3.6), pl.Y(0.30), '細長：還沒到 *M*_{r} 就皺', 15, COMP, 'start', 'bold')
    o += box(670, 60, 220, 180, '三種斷面＝', ['三種「先後順序」', '', '先到 *M*_{p} 再皺', '先皺、但過了 *M*_{r}', '還沒到 *M*_{r} 就皺'], KEY2, KEY, 16, 14)
    o += T(pl.X(5), pl.Y(0) + 46, '（曲線形狀為示意；縱軸 *M*_{r} 位置用貫穿範例 H700 的 *M*_{r}/*M*_{p}）', 14, MUT, 'middle')
    return svg(W, H, o, '三種斷面的彎矩轉角')


def fig2_4():
    """FLB：Mn vs λ，SS-2012-1 數值（SI）。"""
    W, H = 900, 410
    r = R12
    lp, lr = r['lp'], r['lr']
    pl = Plot(100, 40, 560, 290, 0, 30, 0, 1000)
    o = pl.axes([0, lp, lr, 30], [0, 200, 400, 600, 800, 1000], 'λ = *b*_{f}/2*t*_{f}', '*M*_{n}（kN·m）', size=14,
                xfmt=lambda v: {0: '0', 30: '30'}.get(v, f'{v:.2f}' if v < 10 else f'{v:.1f}'))

    def mn(lam):
        if lam <= lp:
            return r['Mp']
        if lam <= lr:
            return r['Mp'] - (r['Mp'] - r['Mr']) * (lam - lp) / (lr - lp)
        return r['Mr'] * (lr / lam) ** 2
    o += pl.curve(mn, 0, lr, KEY, 3)
    o += pl.curve(mn, lr, 30, COMP, 2.4, dash='7 5')
    o += pl.hline(r['Mp'], c=TEN) + pl.hline(r['Mr'], c=WARN)
    o += T(pl.X(30) + 10, pl.Y(r['Mp']) + 5, f'*M*_{{p}} {r["Mp"]:.1f}', 15, TEN, 'start', 'bold')
    o += T(pl.X(30) + 10, pl.Y(r['Mr']) + 5, f'*M*_{{r}} {r["Mr"]:.1f}', 15, WARN, 'start', 'bold')
    o += pl.dot(r['lf'], r['Mn'], COMP, 6)
    o += A(pl.X(5), pl.Y(560), pl.X(r['lf']) - 4, pl.Y(r['Mn']) + 8, COMP, 1.8, 9)
    o += T(pl.X(1), pl.Y(520), f'SS-2012-1：λ = {r["lf"]:.2f}', 15, COMP, 'start', 'bold')
    o += T(pl.X(1), pl.Y(520) + 22, f'*M*_{{n}} = {r["Mn"]:.1f}', 15, COMP, 'start', 'bold')
    o += T(pl.X(lp / 2), pl.Y(r['Mp']) - 14, '平台', 15, KEY, 'middle', 'bold')
    o += T(pl.X((lp + lr) / 2) + 20, pl.Y((r['Mp'] + r['Mr']) / 2) - 18, '直線', 15, KEY, 'start', 'bold')
    o += T(pl.X(25), pl.Y(r['Mr'] * (lr / 25) ** 2) - 16, '曲線（細長）', 15, COMP, 'middle')
    o += box(690, 150, 200, 110, '種子 S4', ['平台＋直線＋曲線', '第 4 章 LTB 同一個樣子'], KEY2, KEY, 16, 14)
    return svg(W, H, o, 'FLB 內插')


def fig2_5():
    """ASD 非結實翼板：0.66Fy → 0.60Fy 的直線，與規範式重合。"""
    W, H = 900, 360
    Fy = D['Fy']
    lp, lr = 17 / math.sqrt(Fy), 25 / math.sqrt(Fy)
    pl = Plot(100, 40, 560, 240, 6, 16, 0.58, 0.68)
    o = pl.axes([6, lp, lr, 16], [0.58, 0.60, 0.62, 0.64, 0.66, 0.68], 'λ', '*F*_{b}/*F*_{y}', size=14,
                xfmt=lambda v: f'{v:.2f}' if v not in (6, 16) else f(v))
    o += pl.curve(lambda l: calcs.asd_flb(l, Fy) / Fy, 6, 16, WARN, 3.2)
    o += pl.curve(lambda l: calcs.asd_flb_code(l, Fy) / Fy, lp, lr, KEY, 2, dash='6 5')
    o += T(pl.X(7), pl.Y(0.66) - 10, '0.66*F*_{y}（結實）', 15, WARN, 'start', 'bold')
    o += T(pl.X(13.6), pl.Y(0.60) - 10, '0.60*F*_{y}', 15, WARN, 'start', 'bold')
    o += box(680, 70, 210, 130, '虛線＝規範式', ['*F*_{y}(0.79 − 0.0076λ√*F*_{y})', '和兩端點拉直線', '完全重合'], KEY2, KEY, 15, 14)
    o += T(pl.X(11), pl.Y(0.58) + 46, f'（*F*_{{y}} = {Fy} tf/cm²；λ_{{p}} = 17/√*F*_{{y}}，λ_{{r}} = 25/√*F*_{{y}}）', 14, MUT, 'middle')
    return svg(W, H, o, 'ASD 非結實翼板')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3, 'fig2_4': fig2_4, 'fig2_5': fig2_5}
