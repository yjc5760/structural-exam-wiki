# -*- coding: utf-8 -*-
"""第 1 章：內力為什麼會長大（P-δ 與 P-Δ）。幾何依解析形狀逐點計算；數字取自 calcs.py。"""
from plot import *  # noqa
from calcs import ex2014, W, LOAD
import math


def _moment_arc(cx, cy, r, a0, a1, c, w=2.6):
    """弧形箭頭（角度以度、螢幕座標，順時針為正）。"""
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / 24)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / 24))) for i in range(25)]
    return curve_arrow(pts, c, w, 11)


def fig1_1():
    W_, H = 900, 430
    o = ''
    x0, x1, yb = 80, 500, 120
    Lp = x1 - x0
    d0, d2 = 26, 44            # 示意：一階／二階中點撓度（px，放大顯示）
    shp = lambda u: 4 * u * (1 - u)          # 均勻彎矩 → 拋物線
    o += T(295, 30, '(a) 同一根梁柱：先只有 *M*，再加上 *P*', 16, INK, 'middle', 'bold')
    o += L(x0 - 10, yb, x1 + 10, yb, MUT, 1.2, '6 5')
    o += P([(x0 + Lp * i / 100, yb + d0 * shp(i / 100)) for i in range(101)], AC, 3, dash='8 5')
    o += P([(x0 + Lp * i / 100, yb + d2 * shp(i / 100)) for i in range(101)], COMP, 5)
    o += pin(x0, yb + 4) + pin(x1, yb + 4)
    # 端彎矩（單曲率：左端順時針、右端逆時針）
    o += _moment_arc(x0, yb, 30, 200, 330, INK) + _moment_arc(x1, yb, 30, -20, -150, INK)
    o += T(x0 - 6, yb - 40, '*M*', 17, INK, 'end', 'bold') + T(x1 + 6, yb - 40, '*M*', 17, INK, 'start', 'bold')
    # 軸力
    o += A(x0 - 56, yb, x0 - 14, yb, COMP, 3.2, 12) + A(x1 + 56, yb, x1 + 14, yb, COMP, 3.2, 12)
    o += T(x0 - 44, yb + 30, '*P*', 17, COMP, 'middle', 'bold') + T(x1 + 44, yb + 30, '*P*', 17, COMP, 'middle', 'bold')
    xm = (x0 + x1) / 2
    o += T(xm + 18, yb + d0 - 6, 'δ_{0}（只有 *M*）', 14, AC, 'start')
    o += T(xm, yb + d2 + 24, 'δ（加上 *P*，更彎）', 14, COMP, 'middle', 'bold')
    # 彎矩圖
    yd, hm = 250, 50
    o += T(x0 - 8, yd - 14, '彎矩圖', 15, INK, 'start', 'bold')
    o += L(x0, yd, x1, yd, INK, 1.5)
    o += R(x0, yd, Lp, hm, AC2, AC, 1.4)
    bulge = [(x0 + Lp * i / 100, yd + hm + 1.25 * d2 * shp(i / 100)) for i in range(101)]
    o += P([(x0, yd + hm)] + bulge + [(x1, yd + hm)], COMP, 2, fill=COMP2, close=True)
    o += T(xm, yd + 32, '*M*（一階，全長一樣）', 15, AC, 'middle', 'bold')
    o += T(xm, yd + hm + 34, '+ *P*·*y*(*x*)', 15, COMP, 'middle', 'bold')
    o += T(xm, yd + hm + 92, '二階多出來的：中間最多，兩端為 0', 14, COMP, 'middle')
    # (b) 自由體圖
    o += L(580, 20, 580, 415, GRID, 1.5)
    o += T(740, 30, '(b) 切開中點看左半', 16, INK, 'middle', 'bold')
    fx0, fx1, fy = 662, 790, 130
    dd = 46
    pts = [(fx0 + (fx1 - fx0) * i / 60, fy + dd * math.sin(math.pi / 2 * i / 60)) for i in range(61)]
    o += L(fx0 - 10, fy, fx1 + 30, fy, MUT, 1.2, '6 5')
    o += P(pts, COMP, 5)
    o += _moment_arc(fx0, fy, 28, 200, 330, INK)
    o += T(fx0 - 4, fy - 36, '*M*', 16, INK, 'end', 'bold')
    o += A(fx0 - 50, fy, fx0 - 12, fy, COMP, 3, 12)
    o += T(fx0 - 32, fy + 26, '*P*', 16, COMP, 'middle', 'bold')
    o += A(fx1 + 8, fy + dd, fx1 + 50, fy + dd, COMP, 3, 12)
    o += T(fx1 + 34, fy + dd + 26, '*P*', 16, COMP, 'middle', 'bold')
    o += _moment_arc(fx1, fy + dd, 26, -30, -160, KEY)
    o += T(fx1 - 10, fy + dd - 34, '*M*_{mid}', 16, KEY, 'end', 'bold')
    o += dim(fx1 + 66, fy, fx1 + 66, fy + dd, '', MUT) + T(fx1 + 78, fy + dd / 2 + 6, 'δ', 17, MUT, 'start', italic=True)
    o += R(600, 250, 285, 116, KEY2, KEY, 1.4, 9)
    o += T(742, 278, '對切口取力矩：', 15, KEY, 'middle', 'bold')
    o += T(742, 310, '*M*_{mid} = *M* + *P*·δ', 18, KEY, 'middle', 'bold')
    o += T(742, 343, '兩個 *P* 錯開了 δ，就是一個力偶', 14, INK, 'middle')
    return svg(W_, H, o, '一階與二階彎矩')


def _col(x, ytop, ybot, shape, amp, c=COMP, w=5):
    return P([(x + amp * shape(i / 80), ytop + (ybot - ytop) * i / 80) for i in range(81)], c, w)


def fig1_2():
    W_, H = 900, 470
    o = ''
    yt, yb = 120, 370
    # (a) P-δ：有側撐，兩端不動，中間鼓出
    o += T(225, 30, '(a) P-δ：構材內的彎曲', 16, COMP, 'middle', 'bold')
    o += T(225, 54, '兩端不能側移（有斜撐）', 14, MUT, 'middle')
    xc = 110
    o += L(xc, yt - 10, xc, yb + 10, MUT, 1.2, '6 5')
    o += _col(xc, yt, yb, lambda u: math.sin(math.pi * u), 34)
    o += P([(xc, yt), (xc - 10, yt - 15), (xc + 10, yt - 15)], INK, 1.5, '#fff', close=True)
    o += pin(xc, yb)
    o += A(xc, yt - 48, xc, yt - 18, COMP, 3.2, 12) + T(xc + 10, yt - 28, '*P*', 17, COMP, 'start', 'bold')
    o += dim(xc, (yt + yb) / 2 + 30, xc + 34, (yt + yb) / 2 + 30, '', MUT, size=14)
    o += T(xc + 17, (yt + yb) / 2 + 56, 'δ', 17, MUT, 'middle', italic=True)
    # 彎矩圖（一階線性 M2→M1；二階加 P·y）
    mx = 270
    M2, M1 = 70, 30
    o += L(mx, yt, mx, yb, INK, 1.4)
    lin = lambda u: M2 + (M1 - M2) * u
    o += P([(mx, yt)] + [(mx + lin(i / 80), yt + (yb - yt) * i / 80) for i in range(81)] + [(mx, yb)], AC, 1.6, AC2, close=True)
    o += P([(mx + lin(i / 80) + 50 * math.sin(math.pi * i / 80), yt + (yb - yt) * i / 80) for i in range(81)], COMP, 2.6)
    o += T(mx + M2 + 6, yt + 4, '*M*_{2}', 15, AC, 'start')
    o += T(mx + M1 + 6, yb + 4, '*M*_{1}', 15, AC, 'start')
    o += T(mx + 112, (yt + yb) / 2 + 4, '+*P*·δ', 15, COMP, 'start', 'bold')
    o += R(30, 400, 390, 52, COMP2, COMP, 1.4, 8)
    o += T(225, 422, '兩端沒變，中段變大', 15, COMP, 'middle', 'bold')
    o += T(225, 444, '→ 由 *B*_{1} 放大（第 2、3 章）', 14, INK, 'middle')
    o += L(450, 20, 450, 460, GRID, 1.5)
    # (b) P-Δ：整層側移
    o += T(675, 30, '(b) P-Δ：整層樓的側移', 16, AC, 'middle', 'bold')
    o += T(675, 54, '柱頂可以側移（無斜撐）', 14, MUT, 'middle')
    xb, Dl = 520, 56
    o += L(xb, yt - 10, xb, yb + 10, MUT, 1.2, '6 5')
    shp = lambda u: (1 - u) ** 2 * (2 + u) / 2   # 懸臂頂力的撓曲形狀（u 由頂往下 0→1），頂端 = 1
    o += _col(xb, yt, yb, shp, Dl, AC)
    o += fixed_wall(xb, yb, 70)
    o += A(xb + Dl, yt - 48, xb + Dl, yt - 6, COMP, 3.2, 12) + T(xb + Dl + 10, yt - 28, '*P*', 17, COMP, 'start', 'bold')
    o += A(xb - 50, yt, xb + Dl - 8, yt, AC, 3.2, 12) + T(xb - 50, yt - 12, '*H*', 17, AC, 'start', 'bold')
    o += dim(xb, yt + 26, xb + Dl, yt + 26, '', MUT)
    o += T(xb + Dl / 2, yt + 52, 'Δ', 17, MUT, 'middle', italic=True)
    # 彎矩圖：一階 H(L-x)（底部最大）＋ P·(Δ−y)
    mx = 700
    o += L(mx, yt, mx, yb, INK, 1.4)
    o += P([(mx, yt), (mx + 90, yb), (mx, yb)], AC, 1.6, AC2, close=True)
    o += P([(mx + 90 * u + 46 * (1 - shp(u)), yt + (yb - yt) * u) for u in [i / 80 for i in range(81)]], COMP, 2.6)
    o += T(mx + 98, yb + 4, '*HL*', 15, AC, 'start')
    o += T(mx + 112, yb - 34, '+*P*Δ', 15, COMP, 'start', 'bold')
    o += R(480, 400, 390, 52, AC2, AC, 1.4, 8)
    o += T(675, 422, '柱端（柱底）變大', 15, AC, 'middle', 'bold')
    o += T(675, 444, '→ 由 *B*_{2} 放大（第 2、4 章）', 14, INK, 'middle')
    return svg(W_, H, o, 'P-δ 與 P-Δ')


def fig1_3():
    d = ex2014()
    W_, H = 900, 330
    o = T(450, 30, 'SS-2014-4（W14×90）：第一輪多出來的彎矩有多少？', 16, INK, 'middle', 'bold')
    pl = Plot(250, 70, 520, 160, 0, 0.10, 0, 2)  # 只用來定比例
    items = [(d['Pdelta0_ratio'], 'P-δ（構材）', COMP,
              f'*P*_{{u}}δ_{{0}} = {d["Pu"]:.0f}×{d["delta0_uniform"]:.2f} mm = {d["Pdelta0"]:.2f} kN·m'),
             (d['alpha2'], 'P-Δ（整層樓）', AC,
              f'Σ*P*_{{u}}Δ = {LOAD["SumPu"]:.0f}×{d["Delta"]:.2f} mm = {d["SumPDelta"]:.2f} kN·m')]
    for k, (v, lab, c, eq) in enumerate(items):
        y = 92 + k * 92
        o += T(240, y + 21, lab, 15, c, 'end', 'bold')
        if k == 0:
            o += T(240, y + 44, '設兩端 110 kN·m', 14, MUT, 'end')
        o += R(250, y, 520 * v / 0.10, 32, c, None, 0, 4, op=0.85)
        o += T(250 + 520 * v / 0.10 + 10, y + 23, f'{v * 100:.1f}%', 17, c, 'start', 'bold')
        o += T(250, y + 56, eq, 14, INK, 'start')
    o += L(250, 82, 250, 270, INK, 1.4)
    o += R(120, 278, 660, 42, KEY2, KEY, 1.4, 8)
    o += T(450, 305, '單看一輪都不大——但它會一輪一輪疊下去（第 2 章）', 15, KEY, 'middle', 'bold')
    return svg(W_, H, o, '第一輪 P×變形')


def _euler(x, ytop, ybot, Lfac, amp, c, label, sub, val):
    """畫柱與有效長度：Lfac=1 半個正弦；Lfac>1 時正弦延伸到柱外（虛線）。"""
    o = ''
    Lp = ybot - ytop
    Le = Lp * Lfac
    y0 = ybot - Le        # 正弦的起點（可能在柱頂之上）
    pts_in, pts_out = [], []
    for i in range(121):
        yy = y0 + Le * i / 120
        xx = x + amp * math.sin(math.pi * i / 120)
        (pts_in if yy >= ytop - 0.5 else pts_out).append((xx, yy))
    if pts_out:
        o += P(pts_out + [pts_in[0]], c, 2, dash='6 5')
    o += P(pts_in, c, 5)
    o += L(x, ytop - 10, x, ybot + 10, MUT, 1.2, '6 5')
    o += pin(x, ybot)
    o += T(x, 36, label, 16, c, 'middle', 'bold')
    o += T(x, 58, sub, 14, MUT, 'middle')
    o += T(x + 10, ybot + 52, val, 15, c, 'middle', 'bold')
    return o


def fig1_4():
    d = ex2014()
    W_, H = 900, 420
    yt, yb = 180, 330
    o = _euler(140, yt, yb, 1.0, 40, COMP, '*K* = 1：兩端不側移', '給 *B*_{1} 用（第 3 章）', f'*P*_{{e1}} = {d["Pe1"]:,.0f} kN')
    o += dim(80, yt, 80, yb, '*L*', MUT, size=15)
    o += _euler(400, yt, yb, W['Kx'], 40, AC, f'*K*_{{x}} = {W["Kx"]}：可側移的強軸', '給 *B*_{2}／柱強度用（第 4、7 章）', f'*P*_{{eK}} = {d["PeKx"]:,.0f} kN')
    o += dim(340, yb - (yb - yt) * W['Kx'], 340, yb, '*KL*', MUT, size=15)
    o += L(560, 20, 560, 400, GRID, 1.5)
    o += R(580, 90, 300, 260, KEY2, KEY, 1.6, 10)
    o += T(730, 120, '同一個 *EI*、同一個 *L*', 15, KEY, 'middle', 'bold')
    o += T(730, 158, '*P*_{e} = π²*EI* / (*KL*)²', 18, KEY, 'middle', 'bold')
    o += T(730, 198, '*K* 變成 1.79 倍', 15, INK, 'middle')
    o += T(730, 224, '→ 挫屈載重除以 1.79² = 3.20', 15, INK, 'middle')
    o += T(730, 262, f'{d["Pe1"]:,.0f} ÷ 3.20 = {d["PeKx"]:,.0f} kN', 15, INK, 'middle')
    o += T(730, 300, '*K* 選錯，放大係數就錯', 15, COMP, 'middle', 'bold')
    o += T(730, 326, '（2014-4 最大的陷阱）', 14, COMP, 'middle')
    return svg(W_, H, o, 'Pe 與 K')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2, 'fig1_3': fig1_3, 'fig1_4': fig1_4}
