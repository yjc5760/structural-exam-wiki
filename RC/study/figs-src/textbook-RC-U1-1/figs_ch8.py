# -*- coding: utf-8 -*-
"""第 8 章：設計——從載重到 As。"""
from figs_common import *  # noqa
from calcs import design_demo, demo_beam, mn_rect, DB, rc2016_1

G = design_demo()
D = demo_beam()
R16 = rc2016_1()


def beam_panel(o, x0, x1, y, w_lab, kind):
    o += L(x0, y, x1, y, INK, 5)
    if kind == 'ss':
        o += pin(x0, y + 3) + pin(x1, y + 3)
    else:
        o += L(x0, y - 30, x0, y + 30, INK, 3) + L(x1, y - 30, x1, y + 30, INK, 3)
        for k in range(7):
            o += L(x0, y - 30 + k * 10, x0 - 8, y - 22 + k * 10, INK, 1)
            o += L(x1, y - 30 + k * 10, x1 + 8, y - 22 + k * 10, INK, 1)
    n = 12
    for i in range(n + 1):
        xx = x0 + (x1 - x0) * i / n
        o += A(xx, y - 42, xx, y - 6, WARN, 1.4, 7)
    o += L(x0, y - 42, x1, y - 42, WARN, 1.6)
    o += T((x0 + x1) / 2, y - 50, w_lab, 15, WARN, 'middle', 'bold')
    return o


def fig8_1():
    W, H = 900, 430
    o = T(225, 24, '(a) 示範梁：簡支 *L* = 7 m', 16, INK, 'middle', 'bold')
    o += T(675, 24, '(b) RC-2016-1：兩端固定 *L* = 7.5 m', 16, INK, 'middle', 'bold')
    x0, x1, y = 60, 390, 110
    o = beam_panel(o, x0, x1, y, f"*w*_{{u}} = 1.2×{G['wD']} + 1.6×{G['wL']} = {G['w']:.2f} tf/m", 'ss')
    yb = 215
    sc = 3.0
    pts = [(x0 + (x1 - x0) * i / 100, yb + sc * G['w'] * 7 ** 2 / 2 * (i / 100) * (1 - i / 100)) for i in range(101)]
    o += P([(x0, yb)] + pts + [(x1, yb)], AC, 2.4, fill=AC2, close=True)
    o += L(x0, yb, x1, yb, INK, 1.2)
    o += T((x0 + x1) / 2, yb + sc * G['Mu_tfm'] + 26, f"*M*_{{u}} = *w*_{{u}}*L*^{{2}}/8 = {G['Mu_tfm']:.2f} tf·m", 15, AC, 'middle', 'bold')
    # (b)
    x0, x1 = 500, 850
    o = beam_panel(o, x0, x1, y, '*w*_{D} = 2、*w*_{L} = 1 tf/m', 'ff')
    w = 1.2 * 2 + 1.6 * 1
    Lb = 7.5
    sc2 = 3.0
    def m(t):
        x = t * Lb
        return w * x * (Lb - x) / 2 - w * Lb ** 2 / 12
    pts = [(x0 + (x1 - x0) * i / 100, yb + sc2 * m(i / 100)) for i in range(101)]
    o += P([(x0, yb)] + pts + [(x1, yb)], AC, 2.4, fill=AC2, close=True)
    o += L(x0, yb, x1, yb, INK, 1.2)
    o += T(x0 + 6, yb - sc2 * w * Lb ** 2 / 12 - 8, f"端 −*wL*^{{2}}/12 = −{w*Lb**2/12:.2f}", 14, COMP, 'start', 'bold')
    o += T((x0 + x1) / 2, yb + sc2 * w * Lb ** 2 / 24 + 24, f"中 +*wL*^{{2}}/24 = {w*Lb**2/24:.2f}", 14, AC, 'middle', 'bold')
    o += T(675, 400, f"檢查：{w*Lb**2/12:.2f} + {w*Lb**2/24:.2f} = {w*Lb**2/8:.2f} = *wL*^{{2}}/8 ✓", 15, KEY, 'middle', 'bold')
    o += T(225, 400, f"（1.4*D* 只有 {G['Mu14']:.2f}，不控制）", 15, MUT, 'middle')
    return svg(W, H, o, '彎矩圖')


def fig8_2():
    W, H = 900, 400
    pl = Plot(100, 50, 560, 280, 0, 30, 0, 55)
    o = pl.axes([0, 5, 10, 15, 20, 25, 30], [0, 10, 20, 30, 40, 50], '*A*_{s}', 'φ*M*_{n}', size=14)
    o += T(pl.X(30) + 20, pl.Y(0) + 26, '(cm²)', 14, MUT, 'start')
    o += T(pl.X(0) + 40, pl.Y(55) - 10, '(tf·m)', 14, MUT, 'start')
    o += pl.curve(lambda A: 0.9 * mn_rect(A) / 1e5, 0, 30, AC, 3.4)
    o += pl.hline(G['Mu_tfm'], 0, 30, COMP, 2, '6 4')
    o += T(pl.X(1), pl.Y(G['Mu_tfm']) - 8, f"*M*_{{u}} = {G['Mu_tfm']:.2f}", 15, COMP, 'start', 'bold')
    o += pl.vline(G['As_req'], 0, G['Mu_tfm'], COMP, 1.4)
    o += pl.dot(G['As_req'], G['Mu_tfm'], COMP, 6)
    o += T(pl.X(G['As_req']) - 8, pl.Y(4), f"需要 {G['As_req']:.2f}", 15, COMP, 'end', 'bold')
    o += pl.vline(D['As'], 0, D['phiMn'] / 1e5, KEY, 1.4)
    o += pl.dot(D['As'], D['phiMn'] / 1e5, KEY, 6)
    o += T(pl.X(D['As']) + 8, pl.Y(4), f"4-D25 = {D['As']:.2f}", 15, KEY, 'start', 'bold')
    o += T(pl.X(D['As']) + 10, pl.Y(D['phiMn'] / 1e5) - 12, f"φ*M*_{{n}} = {D['phiMn']/1e5:.2f}", 15, KEY, 'start', 'bold')
    o += box(690, 70, 195, 200, '設計＝反查這條線', ['給 *M*_{u}，', '找曲線與水平線的交點', '；曲線本身就是', '第 2 章的分析式。', '二次式、迭代都只是', '找交點的方法'], AC2, AC, 15, 14)
    return svg(W, H, o, '反查 As')


def fig8_3():
    W, H = 900, 410
    o = T(450, 24, '4-D25 排得下嗎？（40 cm 寬，梁底部 18 cm 的局部，依比例）', 16, INK, 'middle', 'bold')
    sc = 12.0
    x0, y0 = 450 - 20 * sc, 56
    hb = 18
    yb0 = y0 + hb * sc
    o += P([(x0, y0), (x0, yb0), (x0 + 40 * sc, yb0), (x0 + 40 * sc, y0)], INK, 1.6, fill=STEEL2)
    o += L(x0, y0, x0 + 40 * sc, y0, MUT, 1.2, '8 5')
    cov, st = 4.0, DB['D10']
    xi, xo = x0 + (cov + st / 2) * sc, x0 + (40 - cov - st / 2) * sc
    ys = yb0 - (cov + st / 2) * sc
    o += P([(xi, y0), (xi, ys), (xo, ys), (xo, y0)], MUT, st * sc)
    s_ = G['clear4']
    xx = cov + st + DB['D25'] / 2
    yb = hb - cov - st - DB['D25'] / 2
    xs = []
    for i in range(4):
        xs.append(xx)
        o += C(x0 + xx * sc, y0 + yb * sc, DB['D25'] / 2 * sc, TEN, '#fff', 1.2)
        xx += DB['D25'] + s_
    o += hdim(x0 + (xs[0] + DB['D25'] / 2) * sc, x0 + (xs[1] - DB['D25'] / 2) * sc, y0 + yb * sc - 34, f"淨距 {s_:.2f}", KEY, -1, weight='bold')
    o += vdim(x0 - 14, yb0 - cov * sc, yb0, '保護層 4', INK, -1)
    o += T(x0 + 40 * sc + 12, y0 + 36, '箍筋 D10', 14, MUT, 'start')
    o += T(x0 + 40 * sc + 12, y0 + yb * sc + 5, f"形心距底 {G['h_chk']:.2f}", 14, TEN, 'start', 'bold')
    o += T(x0 + 40 * sc + 12, y0 + yb * sc + 27, '→ *d* ≈ 53.8', 14, TEN, 'start', 'bold')
    o += T(450, 340, f"最小淨距 = max(2.5 cm, *d*_{{b}} = 2.54, 4/3 粒徑) → 取 2.54（粒徑 1.9 cm 時 4/3×1.9 = 2.53）", 15, INK, 'middle')
    o += T(450, 374, f"每排最多 {G['nmax']} 根 D25；4 根淨距 {s_:.2f} ✓；排不下就改兩排 → *d* 變小 → 回頭重算", 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '排筋')


def fig8_4():
    W, H = 900, 640
    o = T(450, 24, '設計題＝先射一箭（猜 *A*_{s}），再用分析流程驗靶', 16, INK, 'middle', 'bold')
    x = 330
    o += node(x, 70, 360, 46, ['① 載重組合 → *M*_{u}（取最大）'], WARN2, WARN, 15)
    o += A(x, 93, x, 117, INK, 1.8)
    o += node(x, 145, 360, 54, ['② 假設 φ = 0.9，解 *a* 或迭代 *jd*', '→ *A*_{s,req}'], AC2, AC, 15)
    o += A(x, 172, x, 196, INK, 1.8)
    o += node(x, 220, 360, 46, ['③ 選鋼筋（根數、排數）→ 實際 *d*、*d*_{t}'], AC2, AC, 15)
    o += A(x, 243, x, 267, INK, 1.8)
    o += node(x, 300, 300, 64, ['④ 排得下？'], WARN2, WARN, 15, shape='dia')
    o += A(x, 332, x, 356, INK, 1.8) + T(x + 8, 348, '是', 14, TEN, 'start', 'bold')
    o += node(x, 390, 300, 64, ['⑤ 分析：*a*、*c*、ε_{t}'], AC2, AC, 15)
    o += A(x, 422, x, 446, INK, 1.8)
    o += node(x, 480, 300, 64, ['⑥ ε_{t} ≥ 0.005？'], WARN2, WARN, 15, shape='dia')
    o += A(x, 512, x, 536, INK, 1.8) + T(x + 8, 528, '是', 14, TEN, 'start', 'bold')
    o += node(x, 570, 360, 54, ['⑦ φ*M*_{n} ≥ *M*_{u}？ *A*_{s} ≥ *A*_{s,min}？', '→ 完成'], TEN2, TEN, 15)
    # 否 分支
    o += arrow_path([(x + 150, 300), (600, 300), (600, 220), (x + 182, 220)], COMP, '否：改兩排、*d* 變小', 610, 266, 'start')
    o += arrow_path([(x + 150, 480), (800, 480), (800, 145), (x + 182, 145)], COMP, '否：加深斷面／加壓力筋', 790, 410, 'end')
    o += arrow_path([(x - 180, 570), (90, 570), (90, 145), (x - 182, 145)], COMP, '不足：加筋', 98, 360, 'start')
    return svg(W, H, o, '設計流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2, 'fig8_3': fig8_3, 'fig8_4': fig8_4}
