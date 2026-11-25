# -*- coding: utf-8 -*-
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig5_1():
    return seed_tree(SEEDS, KIDS, kw=420, sw=345, kfs=13.5, sfs=14, title_l='全書 4 顆種子')


def fig5_2():
    rows = [('① 計算方向', '縱向或橫向；支承在該方向擋不擋', MUT),
            ('② 振動單元', '該墩承擔的上構重量 *W*', AC),
            ('③ 勁度', '墩 3*EI*/*L*³（頂可轉）或 12*EI*/*L*³', TEN),
            ('④ 靜撓度', '沿計算方向施加 *w*(*x*)，求 *u*(*x*)', TEN),
            ('⑤ 積分', 'β = ∫*wu*、γ = ∫*wu*²', KEY),
            ('⑥ 週期', '*T* = 2π√(γ/β*g*)；剛性上構 2π√(*U*_{0}/*g*)', KEY),
            ('⑦ 譜與力', '*S*_{aD} → *V* = *I*/(1.2α_{y})·(·)_{m}·*W*', COMP)]
    return flow(rows, title='SD-U2-3 橋梁週期與地震力流程', bh=48, gap=18)


ALL = {'fig5_1': fig5_1, 'fig5_2': fig5_2}
