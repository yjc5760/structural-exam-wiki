# -*- coding: utf-8 -*-
"""第 6 章：總整理。"""
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig6_1():
    return seed_tree(SEEDS, KIDS, kw=410, sw=360, kfs=13.5, sfs=13.5, title_l='全書 6 顆種子')


def fig6_2():
    rows = [('① 組 *K*、*M*', '單位位移法；重量 ÷ *g*；自由度由下往上', MUT),
            ('② 特徵值', 'det(*K* − ω²*M*) = 0；代回一列求 φ', TEN),
            ('③ 驗振態', '正交；Σω² = tr(*M*^{−1}*K*)；寫明正規化', TEN),
            ('④ 參與', 'Γ = *L*/*M*、*M*^{eff} = *L*²/*M*；Σ*M*^{eff} = Σ*m*', KEY),
            ('⑤a 反應譜', '讀 *S*_{a}（×*g*）→ *S*_{d} = *S*_{a}/ω² → Γφ*S*_{d}、Γ*M*φ*S*_{a}', KEY),
            ('⑤b 歷時', '*q*_{n} 的台車方程：初值、衝量、簡諧', COMP),
            ('⑥ 每振態內', '層剪力、層間位移、內力先算好', AC),
            ('⑦ 組合', 'SRSS；頻率接近用 CQC；歷時直接相加', WARN),
            ('⑧ 非彈性', '長週期 *R* = μ；中週期 *R* = √(2μ−1)', PUR)]
    return flow(rows, title='SD-U1-3 MDOF 解題流水線', bh=48, gap=18)


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
