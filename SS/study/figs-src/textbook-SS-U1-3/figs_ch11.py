# -*- coding: utf-8 -*-
"""第 11 章：全書種子樹（沿用圖 0-2）、梁柱題完整流程圖。"""
from plot import *  # noqa
from calcs import ex2014, ex2014_cap
import figs_ch0


def fig11_1():
    return figs_ch0.fig0_1()


def _box(x, y, w, h, t1, t2, c, fill):
    o = R(x, y, w, h, fill, c, 1.8, 9)
    o += T(x + w / 2, y + 24, t1, 15, c, 'middle', 'bold')
    if t2:
        o += T(x + w / 2, y + 47, t2, 14, INK, 'middle')
    return o


def fig11_2():
    d, c = ex2014(), ex2014_cap()
    W_, H = 900, 600
    o = T(225, 28, '需求（上冊）', 16, COMP, 'middle', 'bold') + T(675, 28, '容量（第 7 章）', 16, TEN, 'middle', 'bold')
    o += _box(30, 44, 390, 58, '① 一階分析 → *P*_{u}、*M*_{nt}、*M*_{lt}', '能側移就拆兩次（S4）', INK, '#fafafa')
    o += A(225, 104, 225, 124, INK, 2, 9)
    o += _box(30, 126, 390, 58, '② *B*_{1}：*C*_{m}/(1 − *P*_{u}/*P*_{e1}) ≥ 1', '曲率符號、*K* = 1（S2、S3）', COMP, COMP2)
    o += A(225, 186, 225, 206, INK, 2, 9)
    o += _box(30, 208, 390, 58, '③ *B*_{2}：1/(1 − Σ*P*_{u}/Σ*P*_{eK})', '整層、對位圖 *K*（S2、S5）', COMP, COMP2)
    o += A(225, 268, 225, 288, INK, 2, 9)
    o += _box(30, 290, 390, 58, '④ *M*_{u} = *B*_{1}*M*_{nt} + *B*_{2}*M*_{lt}', f'本例 {d["Mux"]:.1f} kN·m（兩端取大）', COMP, '#fff')
    o += _box(480, 44, 390, 58, '⑤ φ_{c}*P*_{n} = 0.85 *F*_{cr}*A*_{g}', f'*KL*/*r* 取兩軸大；本例 {d["phiPn"]:.0f} kN', TEN, TEN2)
    o += A(675, 104, 675, 124, INK, 2, 9)
    o += _box(480, 126, 390, 58, '⑥ φ_{b}*M*_{n} = 0.90 *F*_{y}*Z*', f'弱軸 ≤ 1.5*F*_{{y}}*S*_{{y}}；本例 {d["phiMn"]:.1f} kN·m', TEN, TEN2)
    o += A(675, 186, 675, 206, INK, 2, 9)
    o += _box(480, 208, 390, 58, 'ASD：*F*_{a}、*F*_{b}（0.66／0.75*F*_{y}）', '*F*′_{e} = *F*_{e}×12/23', WARN, WARN2)
    o += A(225, 350, 380, 392, COMP, 2.4, 10) + A(675, 268, 520, 392, TEN, 2.4, 10)
    o += R(150, 394, 600, 104, KEY2, KEY, 2.2, 12)
    o += T(450, 422, '⑦ LRFD：*P*_{u}/φ_{c}*P*_{n} ≥ 0.2 ？ 上段 *P* + (8/9)Σ*M* ； 下段 *P*/2 + Σ*M*', 15, KEY, 'middle', 'bold')
    o += T(450, 450, f'本例 {d["Pu_ratio"]:.3f} + (8/9)×{c["M_ratio"]:.3f} = {c["H1"]:.3f} ≤ 1.0　OK', 15, INK, 'middle')
    o += T(450, 478, 'ASD：穩定式（中段）＋強度式（端部）兩式都驗；*f*_{a}/*F*_{a} ≤ 0.15 用直線', 14.5, WARN, 'middle', 'bold')
    o += R(150, 516, 600, 66, '#fff', MUT, 1.2, 10)
    o += T(450, 542, '三個 *K*：柱強度用題給（兩軸大）、*B*_{1} 用 1、*B*_{2} 用對位圖', 14.5, INK, 'middle')
    o += T(450, 566, '兩個 φ：柱 0.85、梁 0.90', 14.5, INK, 'middle')
    return svg(W_, H, o, '梁柱完整流程')


ALL = {'fig11_1': fig11_1, 'fig11_2': fig11_2}
