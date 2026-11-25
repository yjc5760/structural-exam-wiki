# -*- coding: utf-8 -*-
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig7_1():
    return seed_tree(SEEDS, KIDS, kw=420, sw=345, kfs=13.5, sfs=13.5, title_l='全書 5 顆種子')


def fig7_2():
    rows = [('① 地震水準', '30／475／2475 年 ↔ 80%／10%／2%', KEY),
            ('② 工址譜', '*S*_{DS} = *F*_{a}*S*_{S}^{D}、*S*_{D1} = *F*_{v}*S*_{1}^{D}、四段', AC),
            ('③ 週期', '*T* = *C*_{t}*h*_{n}^{3/4}（或分析）→ *S*_{aD}', AC),
            ('④ 韌性', '*R*_{a} = 1+(*R*−1)/1.5 → *F*_{u}（依 *T*/*T*_{0}^{D}）→ (·)_{m}', TEN),
            ('⑤ 總橫力', '*V*、*V*^{*}、*V*_{M} 取最大', COMP),
            ('⑥ 豎向分配', '*F*_{t}（*T* > 0.7 s）＋ *wh* 比例；層剪力、*M*_{0}', WARN),
            ('⑦ 動力分析', '90% 質量；下限 90%／100%', AC),
            ('⑧ 檢核', '位移角 0.005（*V*^{*}）、扭轉 1.2、層強度 0.8', PUR)]
    return flow(rows, title='SD-U2-2 規範計算流程', bh=48, gap=18)


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
