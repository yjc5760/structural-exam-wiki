# -*- coding: utf-8 -*-
"""第 7 章：彎矩–曲率與曲率韌性 μφ。"""
from figs_common import *  # noqa
from calcs import mphi, mphi_doubly, AB, ES

M28 = mphi(280)
M21 = mphi(210)


def fig7_1():
    W, H = 900, 440
    pl = Plot(100, 50, 600, 300, 0, 32, 0, 50)
    o = pl.axes([0, 5, 10, 15, 20, 25, 30], [0, 10, 20, 30, 40, 50], 'φ', '*M*', size=14)
    o += T(pl.X(32) + 20, pl.Y(0) + 26, '(×10^{−5} 1/cm)', 14, MUT, 'start')
    o += T(pl.X(0) + 24, pl.Y(50) - 10, '(tf·m)', 14, MUT, 'start')
    for M, col, lab in ((M21, WARN, "*f*′_{c} = 210"), (M28, AC, "*f*′_{c} = 280")):
        pts = [(0, 0), (M['phcr'] * 1e5, M['Mcr'] / 1e5), (M['phy'] * 1e5, M['My'] / 1e5), (M['phu'] * 1e5, M['Mn'] / 1e5)]
        o += P([pl.pt(x, y) for x, y in pts], col, 3)
        for x, y in pts[1:]:
            o += pl.dot(x, y, col, 5)
        o += T(pl.X(pts[-1][0]), pl.Y(pts[-1][1]) + (28 if col == WARN else -14), f"{lab}：μ_{{φ}} = {M['mu']:.2f}", 15, col, 'end', 'bold')
    o += T(pl.X(M28['phcr'] * 1e5) + 10, pl.Y(M28['Mcr'] / 1e5) + 6, '① 開裂 *M*_{cr}', 14, INK, 'start')
    o += T(pl.X(M28['phy'] * 1e5) + 8, pl.Y(M28['My'] / 1e5) + 26, '② 降伏 φ_{y}', 14, INK, 'start')
    o += T(pl.X(M28['phu'] * 1e5) + 4, pl.Y(M28['Mn'] / 1e5) + 30, '③ 極限 φ_{u}', 14, INK, 'middle')
    o += box(715, 70, 175, 220, '看橫軸，不是縱軸', ['*M*_{y} 與 *M*_{n} 兩種', '*f*′_{c} 幾乎一樣高', '差別全在 φ_{u}', '＝0.003/*c*：', '*f*′_{c} 越高、*c* 越淺', '→ 能彎得越多'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'M-φ')


def fig7_2():
    W, H = 900, 400
    o = T(450, 24, '降伏那一刻：開裂斷面仍是彈性，用「轉換斷面」找中性軸 *kd*（示範梁，依比例）', 16, INK, 'middle', 'bold')
    sc = 4.6; y0 = 80
    xs = 170
    o += section(xs, y0, sc, 40, 60)
    kd = M28['kd']
    o += R(xs - 20 * sc, y0, 40 * sc, kd * sc, AC2, AC, 1.6)
    o += R(xs - 20 * sc, y0 + kd * sc, 40 * sc, (60 - kd) * sc, '#fafafa', MUT, 1, dash='4 3')
    o += T(xs, y0 + (kd + 20) * sc, '開裂：不計（S6）', 14, MUT, 'middle')
    # 轉換鋼筋：寬 nAs/厚度示意
    tk = 4.6
    wv = M28['n'] * 20.27 / tk  # 以 4.6 cm 厚的長條表示 nAs（面積依比例）
    o += R(xs - wv * sc / 2, y0 + (53 - tk / 2) * sc, wv * sc, tk * sc, TEN, None, 0, 2, op=0.85)
    o += T(xs, y0 + 60 * sc + 24, f"*nA*_{{s}} = {M28['n']:.2f} × 20.27 = {M28['n']*20.27:.0f} cm²", 14, TEN, 'middle', 'bold')
    o += vdim(xs + 20 * sc + 14, y0, y0 + kd * sc, f"*kd* = {kd:.2f}", AC, 1, weight='bold')
    # 應力
    xa = 520
    o += L(xa, y0, xa, y0 + 60 * sc, MUT, 1, '4 3')
    o += P([(xa, y0), (xa - 100, y0), (xa, y0 + kd * sc)], AC, 2, fill=AC2, close=True)
    o += T(xa - 100, y0 - 8, '三角形（彈性）', 14, AC, 'middle', 'bold')
    o += A(xa, y0 + 53 * sc, xa + 110, y0 + 53 * sc, TEN, 3, 12)
    o += T(xa + 116, y0 + 53 * sc + 5, '*A*_{s}*f*_{y}', 15, TEN, 'start', 'bold')
    o += A(xa + 70, y0 + kd / 3 * sc, xa - 30, y0 + kd / 3 * sc, AC, 3, 12)
    o += T(xa + 76, y0 + kd / 3 * sc + 5, '作用在 *kd*/3', 14, AC, 'start', 'bold')
    o += box(640, 150, 245, 150, '一次矩相等（形心條件）', ['*b*(*kd*)^{2}/2 = *nA*_{s}(*d* − *kd*)', f"*n* = *E*_{{s}}/*E*_{{c}} = {M28['n']:.2f}", f"*k* = {M28['k']:.3f}"], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '轉換斷面')


def fig7_3():
    W, H = 900, 480
    o = T(450, 24, '兩個狀態、兩條應變線、兩個不同的中性軸（示範梁，依比例）', 16, INK, 'middle', 'bold')
    y0, sc = 100, 4.6
    for x, M, ttl, col in ((240, 'y', '降伏：φ_{y} = ε_{y}/(*d* − *kd*)', AC), (580, 'u', '極限：φ_{u} = 0.003/*c*', COMP)):
        o += T(x, 56, ttl, 15, col, 'middle', 'bold')
        if M == 'y':
            kd = M28['kd']; et = M28['ey']; top = M28['ec_top']
            s, k, ex = strain_panel(x, y0, sc, 60, kd, [(53, et, f"ε_{{y}} = {et:.5f}", TEN)], emax_px=120, ecu=top, ecu_label=f'{top:.5f}')
            o += s
            o += T(x - 10, y0 + kd * sc + 5, f'*kd* = {kd:.2f}', 14, col, 'end', 'bold')
            o += T(x, y0 + 60 * sc + 34, f"φ_{{y}} = {et:.5f}/({53}−{kd:.2f}) = {M28['phy']*1e5:.2f}×10^{{−5}}", 14, col, 'middle', 'bold')
        else:
            c = M28['c']
            s, k, ex = strain_panel(x, y0, sc, 60, c, [(53, M28['phu'] * (53 - c), f"ε_{{t}} = {M28['phu']*(53-c):.4f}", TEN)], emax_px=160)
            o += s
            o += T(x - 10, y0 + c * sc + 5, f'*c* = {c:.2f}', 14, col, 'end', 'bold')
            o += T(x, y0 + 60 * sc + 34, f"φ_{{u}} = 0.003/{c:.2f} = {M28['phu']*1e5:.2f}×10^{{−5}}", 14, col, 'middle', 'bold')
    o += T(450, 466, f"μ_{{φ}} = φ_{{u}}/φ_{{y}} = {M28['phu']*1e5:.2f}/{M28['phy']*1e5:.2f} = {M28['mu']:.2f}", 16, KEY, 'middle', 'bold')
    return svg(W, H, o, 'φy 與 φu')


def fig7_4():
    W, H = 900, 400
    pl = Plot(100, 50, 560, 280, 5, 40, 0, 14)
    o = pl.axes([5, 10, 15, 20, 25, 30, 35, 40], [0, 2, 4, 6, 8, 10, 12], '*A*_{s}', 'μ_{φ}', size=14)
    o += T(pl.X(40) + 20, pl.Y(0) + 26, '(cm²)', 14, MUT, 'start')
    for i, (fc, col) in enumerate(((350, TEN), (280, AC), (210, WARN))):
        a0 = 5.0
        while mphi(fc, As=a0)['mu'] > 13.5:
            a0 += 0.05
        o += pl.curve(lambda A, fc=fc: mphi(fc, As=A)['mu'], a0, 38, col, 3)
        yl = pl.Y(12.5 - i * 1.3)
        o += L(pl.X(29), yl - 5, pl.X(31.5), yl - 5, col, 3) + T(pl.X(32), yl, f"*f*′_{{c}} = {fc}", 14, col, 'start', 'bold')
    o += pl.dot(20.27, M28['mu'], KEY, 6)
    o += T(pl.X(20.27) + 10, pl.Y(M28['mu']) - 10, f"示範梁 {M28['mu']:.2f}", 14, KEY, 'start', 'bold')
    o += box(700, 60, 185, 220, '強度與韌性互相拉扯', ['*A*_{s} 加倍：', '*M*_{n} 差不多加倍，', 'μ_{φ} 卻掉一大半', '*f*′_{c} 提高：', '*M*_{n} 幾乎不變，', 'μ_{φ} 明顯上升'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'μφ-As')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3, 'fig7_4': fig7_4}
