# -*- coding: utf-8 -*-
"""第 5 章：峰值不同時、CQC 相關係數、等位移與等能量。"""
from sdfig import *  # noqa
from calcs import COMB_TH, COMB, COMB_STATS, EX, rho
import math
import numpy as np


def fig5_1():
    W, H = 900, 400
    t, (q1, q2) = COMB_TH
    s = q1 + q2
    pl = Plot(90, 40, 560, 300, 0, 20, -0.065, 0.065)
    o = pl.axes([0, 5, 10, 15, 20], [-0.06, -0.03, 0, 0.03, 0.06], '*t* (s)', '二樓層間位移 (m)', yfmt=lambda v: f'{v:.2f}')
    step = 4
    o += P([pl.pt(a, b) for a, b in zip(t[::step], q1[::step])], AC, 1.4, op=0.8)
    o += P([pl.pt(a, b) for a, b in zip(t[::step], q2[::step])], COMP, 1.4, op=0.9)
    for arr, c in ((q1, AC), (q2, COMP), (s, KEY)):
        i = int(np.abs(arr).argmax())
        o += pl.dot(t[i], arr[i], c, 6)
    c0 = COMB[0]
    o += box(670, 50, 220, 300, '同一場（合成）地震', [f'第 1 振態峰 {c0["p"][0]*100:.2f} cm', f'第 2 振態峰 {c0["p"][1]*100:.2f} cm', '兩個峰不同時（圓點）', f'真實合計峰 {c0["true"]*100:.2f} cm', f'SRSS {c0["srss"]*100:.2f} cm', f'絕對值和 {c0["absum"]*100:.2f} cm', '20 場平均：', f'SRSS/真實 = {COMB_STATS["srss_ratio"]:.2f}', f'絕對值和/真實 = {COMB_STATS["abs_ratio"]:.2f}'], KEY2, KEY, 15, 14)
    o += T(pl.X(10), pl.Y(-0.058), '藍：第 1 振態貢獻　紅：第 2 振態貢獻', 14, MUT, 'middle')
    return svg(W, H, o, '峰值不同時發生')


def fig5_2():
    W, H = 900, 330
    pl = Plot(90, 40, 520, 250, 0, 1, 0, 1)
    o = pl.axes([0, 0.2, 0.4, 0.6, 0.8, 1], [0, 0.25, 0.5, 0.75, 1], 'β = ω_{i}/ω_{j}', 'ρ_{ij}', yfmt=lambda v: f'{v:.2f}')
    o += pl.curve(lambda b: rho(b, 0.05), 0.01, 1, KEY, 3, n=500)
    o += pl.curve(lambda b: rho(b, 0.02), 0.01, 1, AC, 2.2, n=500, dash='6 4')
    o += pl.dot(EX['beta'], EX['rho12'], COMP, 6)
    o += T(pl.X(EX['beta']) - 20, pl.Y(EX['rho12']) - 40, f'範例 β = {EX["beta"]:.3f}：ρ = {EX["rho12"]:.4f}', 15, COMP, 'start', 'bold')
    o += T(pl.X(0.78), pl.Y(0.55), 'ξ = 5%', 15, KEY, 'end', 'bold')
    o += T(pl.X(0.93), pl.Y(0.25), 'ξ = 2%', 15, AC, 'start', 'bold')
    o += box(630, 50, 260, 250, 'CQC：頻率接近才要它', ['*r* = √(ΣΣρ_{ij}*r*_{i}*r*_{j})', 'ρ_{ii} = 1', '頻率分離（β < 0.8）', 'ρ ≈ 0 → 退化成 SRSS', f'範例：CQC {EX["u_top_cqc"]:.4f} m', f'SRSS {EX["u_top"]:.4f} m', '（2020-3 考卷印 CQC 式）'], KEY2, KEY, 15, 14.5)
    return svg(W, H, o, 'CQC 相關係數')


def fig5_3():
    W, H = 900, 360
    o = ''
    for j, (ttl, mu) in enumerate((('等位移（長週期）', 4), ('等能量（中週期）', 4))):
        ox = 40 + j * 440
        pl = Plot(ox + 50, 50, 330, 240, 0, 5, 0, 5)
        o += T(ox + 210, 28, ttl, 16, KEY if j == 0 else WARN, 'middle', 'bold')
        o += pl.axes([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], '*u*', '*F*', grid=False)
        if j == 0:
            Fe, uy, um = 4, 1, 4
            o += P([pl.pt(0, 0), pl.pt(4, 4)], AC, 2.6, dash='6 4')
            o += P([pl.pt(0, 0), pl.pt(uy, 1), pl.pt(um, 1)], COMP, 3)
            o += pl.dot(4, 4, AC, 5) + pl.dot(um, 1, COMP, 5)
            o += pl.vline(4, 0, 4, MUT)
            o += T(pl.X(4) - 8, pl.Y(4) - 8, '彈性 *F*_{e}', 15, AC, 'end', 'bold')
            o += T(pl.X(2.5), pl.Y(1) - 10, '*F*_{y} = *F*_{e}/*R*', 15, COMP, 'middle', 'bold')
            o += T(pl.X(2.5), pl.Y(0.4), '同一個最大位移 ⇒ μ = *R*', 15, KEY, 'middle', 'bold')
        else:
            R_ = 4
            mu_e = (R_ * R_ + 1) / 2
            Fy = 1
            ue = R_
            # 彈性三角形面積 = ½·R·R·（以 Fy=1、uy=1 為單位）；彈塑性面積 = μ − ½
            o += pl.area(lambda u: u if u <= ue else 0, lambda u: 0, 0, ue, ACM, 0.35)
            o += P([pl.pt(0, 0), pl.pt(ue, ue)], AC, 2.6, dash='6 4')
            o += P([pl.pt(0, 0), pl.pt(1, Fy), pl.pt(5, Fy)], COMP, 3)
            o += pl.area(lambda u: min(u, 1), lambda u: 0, 0, 5, COMPM, 0.35)
            o += T(pl.X(2.2), pl.Y(3.3), '兩塊面積相等', 15, KEY, 'middle', 'bold')
            o += T(pl.X(2.6), pl.Y(0.4), 'μ = (*R*² + 1)/2', 15, KEY, 'middle', 'bold')
            o += T(pl.X(4.9), pl.Y(1) - 10, f'*R* = 4 → μ = {mu_e:.1f}（超出圖外）', 14, COMP, 'end')
    o += T(450, 345, '等能量：*R* = √(2μ − 1)；同樣 *R* = 4，等能量要求的韌性 8.5 遠大於等位移的 4', 14.5, MUT, 'middle')
    return svg(W, H, o, '等位移與等能量')


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2, 'fig5_3': fig5_3}
