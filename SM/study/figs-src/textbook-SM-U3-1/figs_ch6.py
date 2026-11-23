# -*- coding: utf-8 -*-
"""第 6 章：種子樹（重繪）、土壓力題流程。"""
from common_figs import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig6_1():
    return seed_tree(SEEDS, KIDS, '5 顆種子', '考場上要重建的公式')


def fig6_2():
    return flow([
        ('① 牆往哪動', '被夾住 *K*_{0}｜離開 *K*_{a}｜推向 *K*_{p}（打折）', WARN),
        ('② Rankine 條件？', '鉛直、光滑、水平；不成立 → 傾斜式／虛擬牆背／Coulomb', KEY),
        ('③ 轉折點清單', '地表（超載）→ 水位 → 層界（兩值）→ *z*_{c} → 牆底', AC),
        ('④ 每層選法', '有效應力 *K*σ_{v}′ ＋ 水｜φ = 0 總應力 σ_{v} ± 2*S*_{u}', AC),
        ('⑤ 凝聚力與裂縫', '主動減 2*c*√*K*_{a}；負值歸零；積水 ½γ_{w}*z*_{c}²', WARN),
        ('⑥ 切方塊取矩', '*P* = Σ*P*_{i}；*ȳ* = Σ*P*_{i}*y*_{i}/*P*（對牆底）', TEN),
        ('⑦ 檢查', '*ȳ* 約 0.2*H*～0.4*H*；水位上升推力一定增加', COMP),
    ], '土壓力題解題流程')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2}
