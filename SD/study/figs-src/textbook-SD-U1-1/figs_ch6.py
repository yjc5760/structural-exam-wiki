# -*- coding: utf-8 -*-
"""第 6 章：總整理（種子樹、解題流程）。"""
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig6_1():
    return seed_tree(SEEDS, KIDS, kw=420, sw=345, title_l='全書 6 顆種子')


def fig6_2():
    rows = [('① 讀單位', '重量 ÷ *g* 變質量；Hz × 2π 變 rad/s；ξ 代小數', MUT),
            ('② 自由體圖', '*mü* + *cu̇* + *ku* = *p*；地震右端 −*mü*_{g}', AC),
            ('③ 基本參數', 'ω = √(*k*/*m*)、*T*、ξ = *c*/(2*m*ω)、ω_{D}', AC),
            ('④ 看外力型式', '無外力→第 2 章｜簡諧→第 3 章｜脈衝→第 4 章', KEY),
            ('⑤a 自由振動', '*A* = *u*_{0}、*B* = (*u̇*_{0}+ξω*u*_{0})/ω_{D}；每圈 e^{−2πξ}', TEN),
            ('⑤b 簡諧', '相量三角形 → *R*_{d}、φ；傳到地面 → *TR*', KEY),
            ('⑤c 脈衝', '*t*_{d}/*T* ≲ 0.25 衝量；否則分段＋自由振動找峰', WARN),
            ('⑥ 多自由度', '正交 → Γ、有效質量；Rayleigh 商；Rayleigh 阻尼', COMP),
            ('⑦ 極限檢查', '*r*→0 回靜力；*r* = 1 → 1/2ξ；Σ*M*^{eff} = Σ*m*', PUR)]
    return flow(rows, title='SD-U1-1 解題流程', bh=48, gap=20)


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
