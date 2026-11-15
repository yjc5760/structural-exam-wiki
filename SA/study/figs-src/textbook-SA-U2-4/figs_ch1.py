# -*- coding: utf-8 -*-
"""第 1 章：勁度是量出來的。所有幾何由程式算出。"""
from figs_common import *  # noqa


def _chain_row(y, push, title):
    """牆—k1—節點1—k2—節點2；push=None/1/2 表示推動哪一個節点一單位（50px）。"""
    o = ''
    wx = 46; n1, n2 = 230, 430; sh = 54
    x1 = n1 + (sh if push == 1 else 0)
    x2 = n2 + (sh if push == 2 else 0)
    o += T(20, y - 52, title, 16, INK, 'start', 'bold')
    o += vwall(wx, y, 64)
    o += spring(wx, y, x1 - 17, TEN)
    o += spring(x1 + 17, y, x2 - 17, TEN)
    for (x0, x, lab, ip) in ((n1, x1, '1', 1), (n2, x2, '2', 2)):
        if push == ip:
            o += R(x0 - 17, y - 13, 34, 26, 'none', MUT, 1.3, 4, dash='4 3')
            o += dim(x0, y + 34, x, y + 34, '1', AC, size=15, lab_off=10)
        o += roller_block(x, y)
        o += T(x, y + 6, lab, 15, INK, 'middle', 'bold')
        if push is not None and push != ip:
            o += lock(x, y - 24)
    if push is None:
        o += T((wx + n1) / 2, y - 18, '*k*_{1}', 16, TEN, 'middle', 'bold')
        o += T((n1 + n2) / 2, y - 18, '*k*_{2}', 16, TEN, 'middle', 'bold')
        o += A(n1 - 14, y - 30, n1 + 22, y - 30, AC, 2, 9) + T(n1 + 26, y - 26, '*d*_{1}', 15, AC)
        o += A(n2 - 14, y - 30, n2 + 22, y - 30, AC, 2, 9) + T(n2 + 26, y - 26, '*d*_{2}', 15, AC)
    elif push == 1:
        o += A(x1 - 6, y - 40, x1 + 46, y - 40, COMP, 3, 12)
        o += T(x1 + 52, y - 35, '*k*_{1} + *k*_{2}', 16, COMP, 'start', 'bold')
        o += A(x2 + 30, y - 40, x2 - 22, y - 40, COMP, 3, 12)
        o += T(x2 + 36, y - 35, '*k*_{2}（向左）', 15, COMP, 'start', 'bold')
    else:
        o += A(x1 + 30, y - 40, x1 - 22, y - 40, COMP, 3, 12)
        o += T(x1 - 26, y - 35, '*k*_{2}（向左）', 15, COMP, 'end', 'bold')
        o += A(x2 - 6, y - 40, x2 + 46, y - 40, COMP, 3, 12)
        o += T(x2 + 52, y - 35, '*k*_{2}', 16, COMP, 'start', 'bold')
    return o


def _col_box(x, y, title, a, b, c=COMP):
    o = R(x, y - 50, 230, 100, '#fff', c, 1.8, 10)
    o += T(x + 115, y - 24, title, 15, c, 'middle', 'bold')
    o += T(x + 50, y + 6, '第 1 列', 14, MUT, 'middle') + T(x + 160, y + 6, a, 16, INK, 'middle', 'bold')
    o += T(x + 50, y + 34, '第 2 列', 14, MUT, 'middle') + T(x + 160, y + 34, b, 16, INK, 'middle', 'bold')
    return o


def fig1_1():
    W, H = 900, 500
    o = ''
    ys = (100, 260, 420)
    o += _chain_row(ys[0], None, '(a) 原狀：兩支彈簧串接，兩個自由度')
    o += _chain_row(ys[1], 1, '(b) 只推節點 1 一單位，節點 2 鎖住')
    o += _chain_row(ys[2], 2, '(c) 只推節點 2 一單位，節點 1 鎖住')
    for y in (180, 340):
        o += L(16, y, 884, y, GRID, 1.2)
    o += R(650, ys[0] - 40, 230, 80, KEY2, KEY, 1.6, 10)
    o += T(765, ys[0] - 12, '每推一次', 15, KEY, 'middle', 'bold')
    o += T(765, ys[0] + 16, '＝填好 [*K*] 的一行', 15, KEY, 'middle', 'bold')
    o += _col_box(650, ys[1], '[*K*] 第 1 行', '*k*_{1} + *k*_{2}', '−*k*_{2}')
    o += _col_box(650, ys[2], '[*K*] 第 2 行', '−*k*_{2}', '*k*_{2}')
    return svg(W, H, o, '三格實驗：鎖住、推一下、量力')


def fig1_2():
    W, H = 900, 400
    o = ''
    pw = 292
    # (a) 軸向桿
    x0, y0 = 20, 120
    o += T(x0 + pw / 2, 34, '(a) 軸向：桁架桿', 16, TEN, 'middle', 'bold')
    o += vwall(x0 + 22, y0, 70)
    o += R(x0 + 22, y0 - 14, 190, 28, TEN2, TEN, 1.8)
    o += R(x0 + 22, y0 - 14, 226, 28, 'none', TEN, 1.3, dash='5 4')
    o += A(x0 + 250, y0, x0 + 280, y0, COMP, 3, 12)
    o += T(x0 + 268, y0 - 22, '*N*', 16, COMP, 'middle', 'bold')
    o += dim(x0 + 22, y0 + 34, x0 + 212, y0 + 34, '*L*', INK, size=15, lab_off=10)
    o += dim(x0 + 212, y0 - 34, x0 + 248, y0 - 34, 'δ', AC, size=15, lab_off=-12)
    lines = ['ε = δ / *L*　（相容）', 'σ = *E* ε　（材料律）', '*N* = σ *A*　（平衡）']
    for i, s in enumerate(lines):
        o += T(x0 + 10, 220 + i * 32, s, 15, INK)
    o += R(x0 + 6, 312, pw - 16, 50, KEY2, KEY, 1.6, 9)
    o += T(x0 + pw / 2 - 4, 344, '*k* = *N*/δ = *EA*/*L*', 17, KEY, 'middle', 'bold')
    # (b) 扭轉桿
    x0 = 20 + pw + 10
    o += T(x0 + pw / 2, 34, '(b) 扭轉：圓桿', 16, TEN, 'middle', 'bold')
    o += vwall(x0 + 22, y0, 70)
    o += R(x0 + 22, y0 - 18, 200, 36, TEN2, TEN, 1.8)
    for k in range(5):
        xx = x0 + 40 + k * 40
        sk = 6 * (k + 1) / 5
        o += L(xx - sk, y0 - 18, xx + sk, y0 + 18, TEN, 1.2)
    o += f'<ellipse cx="{f(x0 + 222)}" cy="{f(y0)}" rx="9" ry="18" fill="#fff" stroke="{TEN}" stroke-width="1.8"/>'
    o += arc_arrow(x0 + 244, y0, 26, -70, 230, COMP, 2.4, 11)
    o += T(x0 + 270, y0 - 30, '*T*', 16, COMP, 'start', 'bold')
    o += dim(x0 + 22, y0 + 38, x0 + 222, y0 + 38, '*L*', INK, size=15, lab_off=10)
    lines = ['γ = *r*φ / *L*　（相容）', 'τ = *G* γ　（材料律）', '*T* = ∫τ*r* d*A*　（平衡）']
    for i, s in enumerate(lines):
        o += T(x0 + 10, 220 + i * 32, s, 15, INK)
    o += R(x0 + 6, 312, pw - 16, 50, KEY2, KEY, 1.6, 9)
    o += T(x0 + pw / 2 - 4, 344, '*k* = *T*/φ = *GJ*/*L*', 17, KEY, 'middle', 'bold')
    # (c) 旋轉彈簧
    x0 = 20 + 2 * (pw + 10)
    cx, cy = x0 + 130, y0
    o += T(x0 + pw / 2 - 10, 34, '(c) 旋轉彈簧：半剛接', 16, TEN, 'middle', 'bold')
    pts = []
    for i in range(160):
        a = i / 159 * 3.2 * 2 * math.pi
        r = 4 + 24 * i / 159
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    o += P(pts, TEN, 2)
    o += L(x0 + 30, cy, cx - 4, cy, STEEL, 8) + L(cx + 28, cy, x0 + 250, cy, STEEL, 8)
    o += arc_arrow(cx, cy, 44, 20, 150, COMP, 2.4, 11)
    o += T(cx + 36, cy - 44, '*M*', 16, COMP, 'start', 'bold')
    lines = ['兩側轉角差 Δθ', '彎矩 *M* 與 Δθ 成正比', '（2019-4 給 10*EI*/*L*）']
    for i, s in enumerate(lines):
        o += T(x0 + 10, 220 + i * 32, s, 15, INK)
    o += R(x0 + 6, 312, pw - 26, 50, KEY2, KEY, 1.6, 9)
    o += T(x0 + pw / 2 - 10, 344, '*k*_{θ} = *M*/Δθ', 17, KEY, 'middle', 'bold')
    return svg(W, H, o, '三種彈簧：軸向、扭轉、旋轉')


def _bar_row(y, mode, title):
    o = T(20, y - 46, title, 16, INK, 'start', 'bold')
    xi, xj = 150, 470; sh = 54
    xa = xi + (sh if mode in ('i', 'both') else 0)
    xb = xj + (sh if mode in ('j', 'both') else 0)
    o += L(xa, y, xb, y, TEN, 9)
    if mode in ('i', 'both'):
        o += dim(xi, y + 26, xa, y + 26, '1', AC, size=15, lab_off=10)
    if mode in ('j', 'both'):
        o += C(xj, y, 7, 'none', MUT, 1.3)
        o += dim(xj, y + 26, xb, y + 26, '1', AC, size=15, lab_off=10)
    o += node(xa, y) + node(xb, y)
    o += T(xa, y + (56 if mode in ('i', 'both') else 30), '*i*', 16, INK, 'middle', 'bold')
    o += T(xb, y + (56 if mode in ('j', 'both') else 30), '*j*', 16, INK, 'middle', 'bold')
    if mode == 'i':
        o += lock(xb, y - 18)
        o += T((xa + xb) / 2, y - 16, '縮短 1 → 受壓 *k*', 15, TEN, 'middle')
        o += A(xa - 60, y, xa - 12, y, COMP, 3, 12) + T(xa - 64, y + 6, '+*k*', 17, COMP, 'end', 'bold')
        o += A(xb + 60, y, xb + 12, y, COMP, 3, 12) + T(xb + 64, y + 6, '−*k*', 17, COMP, 'start', 'bold')
    elif mode == 'j':
        o += lock(xa, y - 18)
        o += T((xa + xb) / 2, y - 16, '伸長 1 → 受拉 *k*', 15, TEN, 'middle')
        o += A(xa - 12, y, xa - 60, y, COMP, 3, 12) + T(xa - 64, y + 6, '−*k*', 17, COMP, 'end', 'bold')
        o += A(xb + 12, y, xb + 60, y, COMP, 3, 12) + T(xb + 64, y + 6, '+*k*', 17, COMP, 'start', 'bold')
    else:
        o += T((xa + xb) / 2, y - 16, '長度不變 → 桿力 0', 15, TEN, 'middle')
        o += T(xa - 30, y + 6, '0', 17, COMP, 'end', 'bold') + T(xb + 30, y + 6, '0', 17, COMP, 'start', 'bold')
    return o


def fig1_3():
    W, H = 900, 430
    o = ''
    o += _bar_row(90, 'i', '(a) 只推 *i* 端一單位（*j* 鎖住）→ 第 1 行')
    o += _bar_row(225, 'j', '(b) 只推 *j* 端一單位（*i* 鎖住）→ 第 2 行')
    o += _bar_row(360, 'both', '(c) 兩端一起推一單位（剛體平移）→ 兩行相加')
    for y in (158, 293):
        o += L(16, y, 884, y, GRID, 1.2)
    o += R(668, 40, 214, 110, KEY2, KEY, 1.6, 10)
    o += T(775, 64, '量到的力排成矩陣', 15, KEY, 'middle', 'bold')
    o += T(700, 112, '*k*', 18, INK, 'middle', 'bold')
    for bx_, sgn in ((722, 1), (838, -1)):
        o += P([(bx_ + 8 * sgn, 80), (bx_, 80), (bx_, 136), (bx_ + 8 * sgn, 136)], INK, 1.8)
    for r_, row in enumerate((('1', '−1'), ('−1', '1'))):
        for c_, v in enumerate(row):
            o += T(755 + c_ * 52, 102 + r_ * 28, v, 18, INK, 'middle', 'bold')
    o += R(668, 322, 214, 74, TEN2, TEN, 1.6, 10)
    o += T(775, 352, '每一列加起來 = 0', 15, TEN, 'middle', 'bold')
    o += T(775, 380, '（平移不產生力）', 15, INK, 'middle')
    return svg(W, H, o, '一根彈簧的 2×2 勁度矩陣')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3}
