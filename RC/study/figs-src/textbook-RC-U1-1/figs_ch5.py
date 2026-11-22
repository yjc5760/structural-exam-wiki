# -*- coding: utf-8 -*-
"""第 5 章：雙筋梁——壓力筋降不降伏、扣 0.85f'c、二次式求 c。"""
from figs_common import *  # noqa
from calcs import doubly_demo, rc2024_2, mphi_doubly, ES

Q = doubly_demo()
R2 = rc2024_2()
MD = mphi_doubly()


def fig5_1():
    W, H = 900, 480
    o = T(450, 24, '示範梁加 2-D25 壓力筋、拉力筋改 6-D25（依比例）', 16, INK, 'middle', 'bold')
    y0, sc = 90, 4.6
    b, h, d, dp = 40, 60, 53, Q['dp']
    xs, xa, xf = 175, 420, 600
    for x, t in ((xs, '斷面'), (xa, '應變'), (xf + 110, '內力')):
        o += T(x, y0 - 34, t, 15, INK, 'middle', 'bold')
    o += section(xs, y0, sc, b, h)
    o += bars(xs, y0 + d * sc, sc, b, 6, 2.54, TEN)
    o += bars(xs, y0 + dp * sc, sc, b, 2, 2.54, KEY)
    o += T(xs, y0 + d * sc + 30, f"6-D25　*A*_{{s}} = {Q['As']:.2f}", 14, TEN, 'middle', 'bold')
    o += T(xs, y0 + Q['c'] * sc + 24, f"2-D25　*A*′_{{s}} = {Q['Asp']:.2f}", 14, KEY, 'middle', 'bold')
    o += vdim(xs - b * sc / 2 - 16, y0, y0 + dp * sc, "*d*′ = 6", KEY, -1)
    o += vdim(xs + b * sc / 2 + 16, y0, y0 + d * sc, '*d* = 53', INK, 1)
    c = Q['c']; yc = y0 + c * sc
    o += L(xs - b * sc / 2, yc, xf + 120, yc, MUT, 1.1, '6 4')
    s, k, ex = strain_panel(xa, y0, sc, h, c, [(dp, -Q['eps_p'], f"ε′_{{s}} = {Q['eps_p']:.5f} < ε_{{y}}", KEY), (d, Q['et'], f"ε_{{t}} = {Q['et']:.4f}", TEN)], emax_px=150)
    o += s
    o += T(xa - 10, yc + 20, f"*c* = {c:.2f}", 14, INK, 'end', 'bold')
    wblk = 100
    o += R(xf, y0, wblk, Q['a'] * sc, WARN2, WARN, 1.8)
    o += vdim(xf - 12, y0, y0 + Q['a'] * sc, f"*a* = {Q['a']:.2f}", WARN, -1)
    ya = y0 + Q['a'] / 2 * sc; yp = y0 + dp * sc; yt = y0 + d * sc
    o += A(xf + wblk + 95, ya - 6, xf + wblk + 8, ya - 6, COMP, 3.2, 13)
    o += T(xf + wblk + 100, ya - 1, f"*C*_{{c}} = {Q['Cc']/1000:.1f} tf", 15, COMP, 'start', 'bold')
    o += A(xf + wblk + 95, yp + 14, xf + wblk + 8, yp + 14, KEY, 3.2, 13)
    o += T(xf + wblk + 100, yp + 19, f"*C*_{{s}} = {Q['Cs']/1000:.1f} tf", 15, KEY, 'start', 'bold')
    o += A(xf + wblk + 8, yt, xf + wblk + 95, yt, TEN, 3.2, 13)
    o += T(xf + wblk + 100, yt + 5, f"*T* = {Q['T']/1000:.1f} tf", 15, TEN, 'start', 'bold')
    o += T(450, 466, f"*C*_{{c}} + *C*_{{s}} = {Q['Cc']/1000:.1f} + {Q['Cs']/1000:.1f} = {(Q['Cc']+Q['Cs'])/1000:.1f} tf = *T* ✓　　*M*_{{n}} = {Q['Mn']/1e5:.2f} tf·m", 16, INK, 'middle', 'bold')
    return svg(W, H, o, '雙筋三聯圖')


def fig5_2():
    W, H = 900, 420
    pl = Plot(100, 50, 560, 290, 1, 6, 0, 6500)
    o = pl.axes([1, 2, 3, 4, 5, 6], [0, 2000, 4200, 5600, 6120], '*c*/*d*′', "*f*′_{s}", size=14,
                yfmt=lambda v: {4200: '4200', 5600: '5600', 6120: '6120'}.get(v, f(v)))
    el = lambda r: 6120 * (1 - 1 / r)
    o += pl.curve(el, 1, 6, MUT, 1.8, dash='5 4')
    o += pl.curve(lambda r: min(4200, el(r)), 1, 6, AC, 3.4)
    o += pl.curve(lambda r: min(5600, el(r)), 1, 6, WARN, 2.4, dash='7 4')
    r42 = 1 / (1 - (4200 / ES) / 0.003)
    o += pl.dot(r42, 4200, AC, 6)
    o += T(pl.X(r42) + 8, pl.Y(4200) - 12, f'SD420：*c* ≥ {r42:.2f}*d*′ 才降伏', 15, AC, 'start', 'bold')
    o += T(pl.X(5.9), pl.Y(5600) - 10, '*f*_{y} = 5600：要 *c* ≥ 11.8*d*′', 14, WARN, 'end', 'bold')
    o += T(pl.X(5.9), pl.Y(6120) - 8, '6120 = 0.003*E*_{s}（漸近線）', 14, MUT, 'end')
    pts = [(Q['c'] / Q['dp'], '示範梁', KEY), (R2['c_ded'] / 8.0, 'RC-2024-2', COMP), (17.66 / 6.225, 'RC-2022-1', TEN)]
    for i, (r, lab, col) in enumerate(pts):
        o += pl.dot(r, el(r), col, 6)
        o += T(pl.X(r) + 10, pl.Y(el(r)) + 22 + 0 * i, f'{lab} {r:.2f}', 14, col, 'start', 'bold')
    o += pl.area(lambda r: 6500, lambda r: 0, 1, r42, COMP2, 0.35)
    o += T(pl.X(1.5), pl.Y(6300), '陷阱帶：常見梁的 *c* 都落在這裡', 15, COMP, 'start', 'bold')
    o += box(690, 70, 195, 200, '為什麼常不降伏？', ['*d*′ 約 5～8 cm', '延性好的梁 *c* 淺', '（約 0.2～0.3*d*）', '*c*/*d*′ 常只有 2～3', '＜ 3.19', '→ 壓力筋沒降伏'], KEY2, KEY, 15, 14)
    return svg(W, H, o, "f's-c/d'")


def fig5_3():
    W, H = 900, 330
    o = T(450, 24, '壓力筋埋在應力塊裡：那一小塊混凝土被算了兩次', 16, INK, 'middle', 'bold')
    def panel(x, title, show_bar=True, hole=False, sub=None):
        out = T(x + 110, 64, title, 15, INK, 'middle', 'bold')
        out += R(x, 80, 220, 120, WARN2, WARN, 1.8)
        out += T(x + 110, 100, "0.85*f*′_{c} 填滿 *a*", 14, WARN, 'middle')
        if show_bar:
            for bx in (x + 60, x + 160):
                out += C(bx, 140, 14, KEY if not hole else '#fff', KEY, 2)
                if hole:
                    out += L(bx - 10, 130, bx + 10, 150, KEY, 2) + L(bx - 10, 150, bx + 10, 130, KEY, 2)
        if sub:
            for i, s in enumerate(sub):
                out += T(x + 110, 230 + i * 24, s, 15, INK, 'middle')
        return out
    o += panel(40, '① 混凝土：全寬 × *a*', show_bar=False, sub=['0.85*f*′_{c}·*a*·*b*', '（含鋼筋占的位置）'])
    o += T(285, 145, '＋', 30, INK, 'middle', 'bold')
    o += panel(330, '② 鋼筋：*A*′_{s}*f*′_{s}', sub=['同一個位置', '又算一次'])
    o += T(575, 145, '−', 30, INK, 'middle', 'bold')
    o += panel(620, '③ 退還那塊混凝土', hole=True, sub=["*A*′_{s} × 0.85*f*′_{c}", '（⊗ 是被重複的部分）'])
    o += T(450, 310, "*C*_{s} = *A*′_{s}(*f*′_{s} − 0.85*f*′_{c})　——只在 *a* > *d*′（鋼筋在應力塊裡）時才扣", 16, KEY, 'middle', 'bold')
    return svg(W, H, o, '扣 0.85fc')


def fig5_4():
    W, H = 900, 360
    o = T(450, 24, '同樣 6-D25 拉力筋：加 2-D25 壓力筋買到什麼？', 16, INK, 'middle', 'bold')
    groups = [('*M*_{n}（tf·m）', Q['Mn1'] / 1e5, Q['Mn'] / 1e5, 0.0, 70, AC),
              ('中性軸 *c*（cm）', Q['c1'], Q['c'], 0, 20, WARN),
              ('曲率韌性 μ_{φ}', MD['mu1'], MD['mu'], 0, 5, TEN)]
    x0 = 70
    for i, (name, v1, v2, lo, hi, col) in enumerate(groups):
        gx = x0 + i * 280
        o += T(gx + 100, 66, name, 15, INK, 'middle', 'bold')
        base = 300
        for j, (v, lab) in enumerate(((v1, '單筋'), (v2, '雙筋'))):
            hgt = (v - lo) / (hi - lo) * 200
            bx = gx + 30 + j * 90
            o += R(bx, base - hgt, 60, hgt, col if j else STEEL3, None, 0, 4)
            o += T(bx + 30, base - hgt - 8, f'{v:.2f}', 15, col, 'middle', 'bold')
            o += T(bx + 30, base + 22, lab, 14, INK, 'middle')
        o += L(gx + 15, base, gx + 195, base, INK, 1.4)
        ch = v2 / v1 - 1
        o += T(gx + 100, 344, f'{"+" if ch > 0 else ""}{ch*100:.1f}%', 16, col, 'middle', 'bold')
    return svg(W, H, o, '雙筋效益')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3, 'fig5_4': fig5_4}
