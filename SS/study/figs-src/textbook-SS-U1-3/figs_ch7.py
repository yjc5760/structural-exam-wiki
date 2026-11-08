# -*- coding: utf-8 -*-
"""第 7 章：容量的兩條腿（柱 φcPn、梁 φbMn）、φ 排序、ASD 容許應力的來歷。"""
from plot import *  # noqa
from calcs import ex2014, ex2014_cap, W, Fcr_lrfd, lam_c, Fa_asd
import math


def fig7_1():
    d, c = ex2014(), ex2014_cap()
    w = W
    W_, H = 900, 430
    Py = w['Fy'] * w['A'] / 1000
    pl = Plot(80, 60, 330, 280, 0, 2.0, 0, 6500)
    o = T(245, 32, '(a) 柱：φ_{c}*P*_{n}（U1-1）', 16, COMP, 'middle', 'bold')
    o += pl.axes([0, 0.5, 1.0, 1.5, 2.0], [0, 2000, 4000, 6000], 'λ_{c}', 'kN', size=14)
    o += pl.hline(Py, c=TEN, dash='6 4')
    o += T(pl.X(2.0), pl.Y(Py) - 8, f'*P*_{{y}} = {Py:,.0f}', 14, TEN, 'end', 'bold')
    o += pl.curve(lambda l: 0.85 * Fcr_lrfd(l, w['Fy']) * w['A'] / 1000, 0, 2.0, COMP, 3.4)
    o += pl.dot(d['lc'], d['phiPn'], KEY, 6)
    o += L(pl.X(d['lc']), pl.Y(d['phiPn']), pl.X(0.78), pl.Y(5250), KEY, 1.1)
    o += T(pl.X(0.8), pl.Y(5400), f'2014-4：λ_{{c}} = {d["lc"]:.3f}', 14, KEY, 'start', 'bold')
    o += T(pl.X(0.8), pl.Y(5400) + 22, f'φ_{{c}}*P*_{{n}} = {d["phiPn"]:,.0f} kN', 14, KEY, 'start', 'bold')
    o += L(450, 20, 450, 420, GRID, 1.5)
    o += T(675, 32, '(b) 梁：φ_{b}*M*_{n}（U1-2）', 16, TEN, 'middle', 'bold')
    My = w['Fy'] * c['Sx'] / 1e6; Mp = w['Fy'] * w['Zx'] / 1e6
    items = [('*M*_{y} = *F*_{y}*S*_{x}', My, AC), ('*M*_{p} = *F*_{y}*Z*_{x}', Mp, TEN), ('φ_{b}*M*_{p}', d['phiMn'], KEY)]
    sc = 240 / 950
    for k, (lab, v, col) in enumerate(items):
        y = 80 + k * 72
        o += T(560, y + 22, lab, 15, col, 'end', 'bold')
        o += R(572, y, v * sc, 34, col, None, 0, 4, op=0.85)
        o += T(572 + v * sc + 8, y + 24, f'{v:.1f}', 15, col, 'start', 'bold')
    o += T(675, 330, f'*Z*/*S* = {c["ZS"]:.2f}（形狀因子）', 15, INK, 'middle')
    o += T(675, 358, '*L*_{b} ≤ *L*_{p}、結實斷面時 *M*_{n} = *M*_{p}', 14, MUT, 'middle')
    o += T(675, 384, '單位 kN·m；W14×90 強軸', 14, MUT, 'middle')
    return svg(W_, H, o, '容量兩條腿')


def fig7_2():
    W_, H = 900, 300
    pl = Plot(80, 120, 740, 40, 0.70, 0.95, 0, 1)
    o = T(450, 34, 'φ 的大小 ＝ 破壞前的預警有多明顯', 16, INK, 'middle', 'bold')
    o += L(pl.X(0.70), 160, pl.X(0.95), 160, INK, 2)
    for t in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
        o += L(pl.X(t), 160, pl.X(t), 168, INK, 1.4) + T(pl.X(t), 188, f'{t:.2f}', 14, MUT, 'middle')
    marks = [(0.75, '斷裂（淨斷面、螺栓）', '一斷就斷，沒預警', COMP2, COMP),
             (0.85, '柱挫屈 φ_{c}', '突然側彎，幾乎沒預警', WARN2, WARN),
             (0.90, '梁降伏 φ_{b}', '撓度變大，看得出來', TEN2, TEN)]
    for (v, t1, t2, fill, col), dx in zip(marks, (0, -70, 75)):
        x = pl.X(v); bx = x + dx
        o += C(x, 160, 8, col, '#fff', 2)
        o += L(x, 150, bx, 112, col, 1.6)
        o += R(bx - 100, 52, 200, 60, fill, col, 1.4, 8)
        o += T(bx, 76, t1, 15, col, 'middle', 'bold')
        o += T(bx, 100, t2, 14, INK, 'middle')
    o += A(pl.X(0.72), 230, pl.X(0.93), 230, KEY, 2.4, 11)
    o += T(450, 260, '越有預警、越可預測 → φ 越大', 15, KEY, 'middle', 'bold')
    o += T(450, 286, '同一個梁柱題裡同時有 0.85 和 0.90，不能統一用 0.9', 14, COMP, 'middle')
    return svg(W_, H, o, 'φ 排序')


def fig7_3():
    c = ex2014_cap()
    W_, H = 900, 340
    o = T(450, 32, 'ASD 的三個彎曲容許應力：都是「*F*_{y} × 形狀因子 ÷ 1.67」', 16, INK, 'middle', 'bold')
    rows = [('0.60*F*_{y}', '*F*_{y} ÷ 1.67', '只到初始降伏（非結實、或 LTB 上限）', 0.60, AC),
            ('0.66*F*_{y}', '*F*_{y} × 1.10 ÷ 1.67', '強軸結實：*Z*/*S* ≈ 1.1', 0.66, TEN),
            ('0.75*F*_{y}', '*F*_{y} × 1.25 ÷ 1.67', '弱軸結實：*Z*/*S* ≈ 1.5，打折取 1.25', 0.75, WARN)]
    for k, (a, b, cc, v, col) in enumerate(rows):
        y = 64 + k * 66
        o += R(30, y, 120, 44, col, None, 0, 6, op=0.9)
        o += T(90, y + 29, a, 17, '#fff', 'middle', 'bold')
        o += T(170, y + 29, '＝ ' + b, 16, col, 'start', 'bold')
        o += T(430, y + 29, cc, 14.5, INK, 'start')
    o += R(30, 270, 840, 54, KEY2, KEY, 1.4, 8)
    o += T(450, 295, f'自我檢查（W14×90）：LRFD φ_{{b}}*Z*/*S* ÷ 1.5 = 0.9 × {c["ZS"]:.3f} ÷ 1.5 = {c["Fbx_equiv"]:.3f} ≈ 0.66', 15, KEY, 'middle', 'bold')
    o += T(450, 316, '兩套規範在梁這條腿上幾乎一樣', 14, INK, 'middle')
    return svg(W_, H, o, 'ASD 彎曲容許應力')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2, 'fig7_3': fig7_3}
