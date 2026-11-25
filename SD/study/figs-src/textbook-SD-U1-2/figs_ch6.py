# -*- coding: utf-8 -*-
"""第 6 章：總整理。"""
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig6_1():
    return seed_tree(SEEDS, KIDS, kw=420, sw=345, kfs=13.5, sfs=14, title_l='全書 5 顆種子')


def fig6_2():
    rows = [('① 數自由度', '每個有質量或轉動慣量的運動一個；沒慣量的要濃縮', MUT),
            ('② 選量測基準', '地震用相對座標；重力從靜平衡量（倒擺除外）', WARN),
            ('③ 選方法', '力好畫→自由體圖；剛體、幾何複雜→能量', AC),
            ('④ 寫 *M*', '集中質量對角；剛體用 ∂²*T*/∂*u̇*_{i}∂*u̇*_{j}', KEY),
            ('⑤ 寫 *K*', '單位位移法逐欄；柱 12、3 *EI*/*h*³；重力給 ∓*mgL*', TEN),
            ('⑥ 寫外力', '虛功 *Q* = δ*W*/δ*q*；地震 −*M*ι*ü*_{g}', COMP),
            ('⑦ 連續體', '猜 ψ → *m*^{*}、*k*^{*}、*p*^{*}；或解 PDE', COMP),
            ('⑧ 檢查', '*K* 對稱；剛體平移；*M* 總和＝總質量；上界', PUR)]
    return flow(rows, title='SD-U1-2 寫運動方程的流程', bh=48, gap=20)


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
