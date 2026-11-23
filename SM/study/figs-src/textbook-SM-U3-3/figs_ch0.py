# -*- coding: utf-8 -*-
"""第 0 章：種子家族樹、五步驟。"""
from common_figs import *  # noqa

SEEDS = [
    ('S1', '重量沿斜面拆：*W* sin θ 推、*W* cos θ 壓', COMP),
    ('S2', "破壞準則 τ_{f} = *c*′ + σ′ tan φ′", TEN),
    ('S3', "有效應力 σ′ = σ − *u*", AC),
    ('S4', 'FS = 抗力 ÷ 驅動力（同一個面）', KEY),
    ('S5', '水頭 *h* = *z* + *u*/γ_{w}；等勢線 ⊥ 流線', AC),
]

KIDS = [
    (0, '1', '楔體 *W* = ½γ*H*²(cot θ − cot α)'),
    (3, '1', '平面滑動 FS = (*cL* + *N* tan φ)/*T*'),
    (0, '2', '無限邊坡 τ = σ_{v} sin β cos β'),
    (1, '2', '乾坡＝浸水：FS = tan φ/tan β'),
    (2, '3', "滲流：FS 乘 γ′/γ_{sat} ≈ ½"),
    (4, '3', '*u* = γ_{w}*h*_{w} cos²β、*i* = sin θ'),
    (0, '4', '地震：*T* + *k*_{h}*W* cos、*N* − *k*_{h}*W* sin'),
    (3, '4', '地錨反算 *T*_{a} = *s*(FS·*T* − *cL* − *N* tan φ)/tan φ'),
    (1, '5', "Rankine 推力、*z*_{c} = 2*c*′/(γ√*K*_{a})"),
    (3, '5', '滑動塊體 FS = (*s*_{u}*L* + *P*_{P})/*P*_{A}'),
    (2, '6', 'Fellenius：(*W* cos α − *u*Δ*L*) tan φ′'),
    (3, '6', 'Bishop：*m*_{α} 迭代'),
]


def fig0_1():
    return seed_tree(SEEDS, KIDS, '5 顆種子（要記的）')


def fig0_2():
    return five_steps()


ALL = {'fig0_1': fig0_1, 'fig0_2': fig0_2}
