# -*- coding: utf-8 -*-
"""第 4 章：e–log σ′ 折線、Casagrande、Schmertmann。"""
from plot import *  # noqa
from calcs import *  # noqa


def _logaxes(x0, y0, w, h, lmin, lmax, emin, emax, eticks):
    X = lambda p: x0 + (math.log10(p) - lmin) / (lmax - lmin) * w
    Y = lambda e: y0 + (emax - e) / (emax - emin) * h
    o = A(x0, y0 + h, x0 + w + 16, y0 + h, INK, 1.5) + A(x0, y0 + h, x0, y0 - 14, INK, 1.5)
    dec = int(math.floor(lmin))
    while dec <= lmax:
        for m in range(1, 10):
            p = m * 10 ** dec
            if lmin <= math.log10(p) <= lmax:
                o += L(X(p), y0, X(p), y0 + h, GRID, 1.6 if m == 1 else 0.8)
                if m == 1:
                    o += T(X(p), y0 + h + 20, f'{p:g}', 14, MUT, 'middle')
        dec += 1
    for e in eticks:
        o += L(x0 - 5, Y(e), x0, Y(e), INK, 1.2) + T(x0 - 9, Y(e) + 5, f'{e:.2f}', 14, MUT, 'end')
    o += T(x0 + w + 20, y0 + h + 5, "*σ*′ (kPa, log)", 14, INK) + T(x0, y0 - 22, '*e*', 16, INK, 'middle')
    return o, X, Y


def fig4_1():
    d = ELOG
    W, H = 900, 440
    o, X, Y = _logaxes(90, 50, 560, 320, 1.0, 3.0, 0.40, 0.95, [0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
    o += P([(X(p), Y(elog_curve(p))) for p in [10 ** (1.3 + i * 0.01) for i in range(171)]], INK, 3)
    o += L(X(d['pc']), Y(0.40), X(d['pc']), Y(elog_curve(d['pc'])) - 10, KEY, 1.6, '6 4')
    o += T(X(d['pc']), Y(0.40) - 8, "*p*_{c}′", 16, KEY, 'middle', 'bold')
    o += T(X(40), Y(elog_curve(40)) - 14, '斜率 *C*_{s}（淺）', 15, AC, 'middle', 'bold')
    o += T(X(330), Y(elog_curve(330)) - 14, '斜率 *C*_{c}（陡）', 15, COMP, 'start', 'bold')
    # 三支箭頭（偏移畫在曲線下方）
    cases = [(30, 80, AC, '①'), (150, 500, COMP, '②'), (50, 300, KEY, '③')]
    off = [0.035, 0.035, 0.075]
    for (a, b, c, nm), of in zip(cases, off):
        pts = [(X(p), Y(elog_curve(p) - of)) for p in [a * (b / a) ** (i / 60) for i in range(61)]]
        o += curve_arrow(pts, c, 2.6, 11)
        o += T(pts[0][0] - 6, pts[0][1] + 18, nm, 16, c, 'end', 'bold')
    o += box(670, 60, 215, 175, '三種走法', ['① 全在左：只 *C*_{s}', '② 全在右：只 *C*_{c}', '③ 跨過 *p*_{c}′：', '　先 *C*_{s} 後 *C*_{c}'], KEY2, KEY)
    o += T(670, 275, '先比三個數：', 15, INK, 'start', 'bold')
    o += T(670, 299, "*p*_{0}′、*p*_{c}′、*p*_{0}′+Δ*p*", 15, INK)
    return svg(W, H, o, 'e–log σ′ 兩條直線')


def fig4_2():
    d = CAS
    q = d['px']
    W, H = 900, 450
    o, X, Y = _logaxes(q['x0'], q['y0'], q['w'], q['h'], q['lmin'], q['lmax'], q['emin'], q['emax'], [0.45, 0.55, 0.65, 0.75, 0.85, 0.95])
    o += P([(X(p), Y(e_lab(p))) for p in [10 ** (1.1 + i * 0.01) for i in range(186)]], INK, 3)
    c = casagrande()
    xA, yA = c['A']
    # 原始壓縮線延伸
    pe = d['pc'] * 10 ** ((d['epc'] - 0.93) / d['Cc'])
    o += L(*c['P1'], X(pe), Y(0.93), COMP, 1.8, '7 4')
    # 水平線、切線、平分線
    o += L(xA, yA, xA + 230, yA, AC, 1.8)
    tx, ty = math.cos(c['ang_t']), math.sin(c['ang_t'])
    o += L(xA - 60 * tx, yA - 60 * ty, xA + 200 * tx, yA + 200 * ty, TEN, 1.8)
    bx, by = math.cos(c['ang_b']), math.sin(c['ang_b'])
    xi, yi = c['I']
    o += L(xA, yA, xi + 40 * bx, yi + 40 * by, KEY, 2.2)
    o += C(xA, yA, 6, INK, '#fff', 1.6)
    o += C(xi, yi, 7, KEY, '#fff', 1.8)
    o += L(xi, yi, xi, q['y0'] + q['h'], KEY, 1.4, '4 3')
    o += T(xA - 14, yA + 26, '① A（最彎）', 15, INK, 'end', 'bold')
    o += T(xA + 236, yA + 5, '② 水平', 15, AC)
    o += T(xA + 200 * tx + 6, yA + 200 * ty + 14, '③ 切線', 15, TEN)
    o += T(xi + 44 * bx + 6, yi + 44 * by + 8, '④ 平分線', 15, KEY, 'start', 'bold')
    o += T(X(560), Y(d['epc'] - d['Cc'] * math.log10(5.6)) + 30, '⑤ 原始壓縮線延伸', 15, COMP)
    o += T(xi, q['y0'] + q['h'] - 10, f"*p*_{{c}}′≈{c['pc_est']:.0f}", 15, KEY, 'middle', 'bold')
    o += box(660, 60, 225, 120, '口訣', ['最彎處 → 一平一切', '→ 對分 → 碰延長線'], KEY2, KEY)
    return svg(W, H, o, 'Casagrande 作圖')


def fig4_3():
    s = schmertmann()
    W, H = 900, 440
    o, X, Y = _logaxes(90, 50, 560, 320, 1.0, 3.5, 0.30, 1.00, [0.40, 0.55, 0.70, 0.85, 1.00])
    # 現地線
    o += L(X(s['p0']), Y(s['e0']), X(s['p_end']), Y(s['e_end']), KEY, 3)
    # 擾動試驗曲線：較平較圓，最後收到 (p_end, e_end)
    Cc_lab = 0.30
    def e_dist(p):
        x = math.log10(p / 60.0)
        w = 0.35
        sw = w * math.log(1 + math.exp(x / w))
        return 0.93 - 0.05 * x - (Cc_lab - 0.05) * sw
    # 讓曲線在 p_end 處等於 e_end：平移修正
    shift = s['e_end'] - e_dist(s['p_end'])
    ps = [10 ** (1.2 + i * 0.01) for i in range(int((math.log10(s['p_end']) - 1.2) / 0.01) + 1)]
    o += P([(X(p), Y(e_dist(p) + shift * (math.log10(p) - 1.2) / (math.log10(s['p_end']) - 1.2))) for p in ps], MUT, 2.4, dash='8 5')
    o += L(90, Y(s['e_end']), X(s['p_end']), Y(s['e_end']), COMP, 1.3, '4 3')
    o += T(96, Y(s['e_end']) - 8, f"*e*=0.42*e*_{{0}}={s['e_end']:.3f}", 15, COMP, 'start', 'bold')
    o += L(90, Y(s['e0']), X(s['p0']), Y(s['e0']), KEY, 1.3, '4 3')
    o += C(X(s['p0']), Y(s['e0']), 6.5, KEY, '#fff', 1.8) + C(X(s['p_end']), Y(s['e_end']), 6.5, COMP, '#fff', 1.8)
    o += T(X(s['p0']) + 10, Y(s['e0']) - 10, f"現地起點 (*p*_{{0}}′, *e*_{{0}}={s['e0']:.2f})", 15, KEY, 'start', 'bold')
    o += T(X(400) + 10, Y(s['e0'] - s['Cc_field'] * math.log10(400 / s['p0'])) - 8, '現地原始壓縮線（陡）', 15, KEY, 'start', 'bold')
    o += T(X(30), Y(0.83), '擾動試驗曲線', 15, MUT, 'start', 'bold')
    o += T(X(30), Y(0.83) + 20, '（較平、較圓）', 14, MUT, 'start')
    o += box(670, 60, 215, 150, '重建步驟', ['1 點：(*p*_{0}′, *e*_{0})', '2 點：試驗線上', '　*e*=0.42*e*_{0}', '連直線 → *C*_{c,field}'], KEY2, KEY)
    return svg(W, H, o, 'Schmertmann 擾動修正')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
