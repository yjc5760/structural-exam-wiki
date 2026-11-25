# -*- coding: utf-8 -*-
from sdfig import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig7_1():
    return seed_tree(SEEDS, KIDS, kw=430, sw=330, kfs=13.5, sfs=14, title_l='全書 6 顆種子')


def fig7_2():
    rows = [('① 選保險絲', '梁端撓曲塑鉸（強柱弱梁、撓曲優先於剪力）', KEY),
            ('② 設計保險絲', '*R*_{n}、ρ；ρ ≤ 0.025；½、¼ 規定', TEN),
            ('③ 保險絲上限', '*M*_{pr} = 1.25*f*_{y}*A*_{s}(*d* − *a*/2)、φ = 1、實配', KEY),
            ('④ 梁剪力', '*V*_{e} = Σ*M*_{pr}/ℓ_{n} + *w*_{u}ℓ_{n}/2；*V*_{c} = 0 判斷', COMP),
            ('⑤ 柱', 'Σ*M*_{nc} ≥ 1.2Σ*M*_{nb}；剪力用 2*M*_{pr}/*h*_{eff}', COMP),
            ('⑥ 圍束', '塑鉸區箍筋 *d*/4、6*d*_{b}、15 cm；ρ_{s}', WARN),
            ('⑦ 整體', '側推、位移角 0.005、層剪力強度 0.8', MUT)]
    return flow(rows, title='SD-U3-1 容量設計流程', bh=48, gap=18)


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
