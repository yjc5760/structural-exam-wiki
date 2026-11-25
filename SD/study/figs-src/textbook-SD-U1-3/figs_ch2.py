# -*- coding: utf-8 -*-
"""第 2 章：振態形狀、特性多項式、3DOF。"""
from sdfig import *  # noqa
from calcs import EX, EX3, K, M
import math
import numpy as np


def _modes(ox, phis, labels, cols, sh=90, scale=50, n=2, mass_lab=None):
    o = ''
    for j, (ph, lab, c) in enumerate(zip(phis, labels, cols)):
        x0 = ox + j * 250
        yb = 320
        o += T(x0 + 40, 30, lab, 15.5, c, 'middle', 'bold')
        o += L(x0 + 40, yb, x0 + 40, yb - n * sh, GRID, 1.4, '5 4')
        pts = [(x0 + 40, yb)] + [(x0 + 40 + scale * ph[i], yb - (i + 1) * sh) for i in range(n)]
        o += P(pts, c, 2.8)
        for i in range(n):
            o += C(pts[i + 1][0], pts[i + 1][1], 9, c, '#fff', 2)
            o += T(pts[i + 1][0] + (16 if ph[i] >= 0 else -16), pts[i + 1][1] + 5, f'{ph[i]:.3f}'.rstrip('0').rstrip('.') if abs(ph[i]) > 1e-9 else '0', 15, c, 'start' if ph[i] >= 0 else 'end', 'bold')
        o += hatch_ground(x0, yb, 80)
    return o


def fig2_1():
    W, H = 900, 380
    phi = EX['phi']
    o = _modes(30, [phi[:, 0], phi[:, 1]], [f'第 1 振態 ω = {EX["w"][0]:.3f}', f'第 2 振態 ω = {EX["w"][1]:.3f}'], [AC, COMP], scale=55)
    o += box(520, 50, 370, 300, '每一層都打平：*K*φ = ω²*M*φ', [
        '第 1 振態，一樓：',
        '3000(1) − 1500(1.618) = 573',
        f'ω²*m*φ = {EX["w2"][0]:.3f} × 100 × 1 = 573 ✔',
        '第 1 振態，二樓：',
        '−1500(1) + 1500(1.618) = 927',
        f'{EX["w2"][0]:.3f} × 100 × 1.618 = 927 ✔',
        '彈簧淨力 = 質量 × ω² × 位移',
        '（S1 的 ω² = *k*/*m* 在每一層成立）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '兩層樓的振態')


def fig2_2():
    W, H = 900, 340
    f_ = lambda x: np.linalg.det(K - x * M) / 1e5
    pl = Plot(90, 40, 520, 250, 0, 50, -30, 50)
    o = pl.axes([0, 10, 20, 30, 40, 50], [-25, 0, 25, 50], 'ω² (rad²/s²)', 'det(*K* − ω²*M*) (10^{5})')
    o += pl.curve(f_, 0, 50, AC, 2.8)
    o += pl.hline(0, c=MUT, dash=None, w=1.2)
    for v, c in ((EX['w2'][0], KEY), (EX['w2'][1], COMP)):
        o += pl.dot(v, 0, c, 6) + T(pl.X(v), pl.Y(0) + 26, f'{v:.3f}', 15, c, 'middle', 'bold')
    o += box(630, 50, 260, 250, '特徵值＝曲線過零的點', ['det = 0：存在非零 φ', '2DOF 是 ω² 的二次式', '(3000 − 100ω²)(1500 − 100ω²)', '− 1500² = 0', '⇒ ω⁴ − 45ω² + 225 = 0', 'ω² = 5.730、39.271'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '特性多項式')


def fig2_3():
    W, H = 900, 400
    ph = EX3['phi']
    lam = EX3['lam']
    o = ''
    cols = [AC, KEY, COMP]
    for j in range(3):
        x0 = 70 + j * 200
        yb = 340
        o += T(x0 + 50, 28, f'λ_{{{j+1}}} = {lam[j]:.3f}', 15.5, cols[j], 'middle', 'bold')
        o += L(x0 + 50, yb, x0 + 50, yb - 270, GRID, 1.4, '5 4')
        pts = [(x0 + 50, yb)] + [(x0 + 50 + 45 * ph[i, j], yb - (i + 1) * 90) for i in range(3)]
        o += P(pts, cols[j], 2.8)
        for i in range(3):
            o += C(pts[i + 1][0], pts[i + 1][1], 9 if i < 2 else 7, cols[j], '#fff', 2)
            v = ph[i, j]
            o += T(pts[i + 1][0] + (14 if v >= 0 else -14), pts[i + 1][1] + 5, f'{v:.3f}'.rstrip('0').rstrip('.') if abs(v) > 1e-9 else '0', 14.5, cols[j], 'start' if v >= 0 else 'end', 'bold')
        o += hatch_ground(x0 + 10, yb, 80)
    o += box(680, 50, 210, 300, '*m*、*m*、*m*/2', ['每層 *k*', 'λ = ω²*m*/*k*', 'λ³ − 6λ² + 9λ − 2 = 0', '= (λ − 2)(λ² − 4λ + 1)', 'λ = 2 − √3、2、2 + √3', '（2016-4、2024-1）', '頂層正規化為 1'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, '三層 m m m/2 的振態')


ALL = {'fig2_1': fig2_1, 'fig2_2': fig2_2, 'fig2_3': fig2_3}
