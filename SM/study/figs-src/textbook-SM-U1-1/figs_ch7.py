# -*- coding: utf-8 -*-
"""第 7 章：種子樹（重繪）、三相題解題流程。"""
from common_figs import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig7_1():
    return seed_tree(SEEDS, KIDS, '4 顆種子', '考場上要重建的公式')


def fig7_2():
    return flow([
        ('① 畫三相圖', '左體積、右重量；令 *V*_{s} = 1（或依題目給的量）', KEY),
        ('② 寫錨點', '一個狀態？兩個狀態？壓縮鎖 *V*_{s}、運土加水鎖 *W*_{s}', TEN),
        ('③ 填格子', '題目每個數填進一格；*Se* = *wG*_{s} 補水那一格', AC),
        ('④ 單位換算', 'g/cm³ × 9.81 = kN/m³；kgf × 9.81 = N', WARN),
        ('⑤ 兩格相除', '要什麼指標就除什麼（記分母）', AC),
        ('⑥ 收尾檢查', '0 ≤ *S* ≤ 1；γ_{d} < γ_{t} < γ_{sat} < 26.5；*n* < 1', COMP),
    ], '三相題解題流程')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
