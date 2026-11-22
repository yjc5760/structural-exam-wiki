# -*- coding: utf-8 -*-
"""第 7 章：細長柱彎矩放大（精簡）。"""
from figs_col import *  # noqa
from calcs import rc2006_2, rc2016_3
import math

A6 = rc2006_2(); A16 = rc2016_3()


def fig7_1():
    W, H = 900, 400
    o = T(450, 26, '種子 S6：軸力 × 側向撓度 ＝ 多出來的彎矩，而它又讓柱子更彎', 16, INK, 'middle', 'bold')
    xb, yt, yb = 200, 70, 330
    amp = 46
    pts = [(xb + amp * math.sin(math.pi * (y - yt) / (yb - yt)), y) for y in range(yt, yb + 1, 4)]
    o += L(xb, yt, xb, yb, MUT, 1.2, '5 4')
    o += P(pts, AC, 4)
    o += pin(xb, yb)
    o += C(xb, yt, 5, '#fff', INK, 1.5)
    o += A(xb, yt - 40, xb, yt - 4, COMP, 3, 12)
    o += T(xb + 10, yt - 22, '*P*', 16, COMP, 'start', 'bold')
    o += A(xb + 90, (yt + yb) / 2, xb + amp + 6, (yt + yb) / 2, KEY, 1.6, 9)
    o += T(xb + 96, (yt + yb) / 2 + 5, 'δ', 18, KEY, 'start', 'bold')
    o += T(xb, yb + 50, '(a) 微彎的柱', 14, INK, 'middle', 'bold')
    o += box(420, 70, 460, 270, '幾何級數', ['一階彎矩 *M*_{0} 造成撓度 δ_{0}', '*P*δ_{0} 再造成 δ_{0}·(*P*/*P*_{c})', '……再造成 δ_{0}·(*P*/*P*_{c})^{2}', 'δ = δ_{0}[1 + *P*/*P*_{c} + (*P*/*P*_{c})^{2} + …]', '= δ_{0} / (1 − *P*/*P*_{c})', '', '彎矩一樣被放大：*M* ≈ *M*_{0}/(1 − *P*/*P*_{c})'], KEY2, KEY, 15, 15)
    return svg(W, H, o, 'P-delta')


def fig7_2():
    W, H = 900, 420
    o = T(450, 26, 'δ_{ns} = *C*_{m}/(1 − *P*_{u}/0.75*P*_{c}) ≥ 1：雙曲率（*C*_{m} 小）比較不怕放大', 16, INK, 'middle', 'bold')
    pl = Plot(100, 60, 560, 300, 0, 0.9, 0, 4)
    o += pl.axes([0, 0.2, 0.4, 0.6, 0.8], [0, 1, 2, 3, 4], '*P*_{u}/(0.75*P*_{c})', 'δ_{ns}', size=14)
    for Cm, col, lab, ly in ((1.0, COMP, '*C*_{m} = 1.0（單曲率、等彎矩）', 3.6), (A6['Cm'], WARN, f"*C*_{{m}} = {A6['Cm']:.3f}（RC-2006-2）", 2.6), (A16['Cm'], TEN, '*C*_{m} = 0.25（RC-2016-3）', 0.55)):
        o += pl.curve(lambda x, Cm=Cm: Cm / (1 - x), 0, min(0.9, 1 - Cm / 4.0), col, 2.8)
        o += T(pl.X(0.02), pl.Y(ly), lab, 14, col, 'start', 'bold')
    o += pl.hline(1.0, 0, 0.9, INK, 1.8, '6 4')
    o += T(pl.X(0.55), pl.Y(1.0) + 20, '下限 1.0', 14, INK, 'middle', 'bold')
    x6 = A6['Pu'] / (0.75 * A6['Pc'])
    o += pl.dot(x6, A6['dns'], WARN, 7)
    o += T(pl.X(x6) + 10, pl.Y(A6['dns']) + 20, f"{A6['dns']:.3f}", 14, WARN, 'start', 'bold')
    x16 = A16['x']
    o += pl.dot(x16, A16['Cm'] / (1 - x16), TEN, 7)
    o += T(pl.X(x16) + 10, pl.Y(A16['Cm'] / (1 - x16)) + 5, f"{A16['dns_raw']:.2f} → 取 1.0", 14, TEN, 'start', 'bold')
    o += box(680, 80, 210, 240, '讀圖', ['橫軸越靠近 1', '→ 放大越劇烈', '', '*C*_{m} 是「等值均勻', '彎矩」的折減', '雙曲率兩端彎矩', '互相抵消一部分'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '彎矩放大')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
