# -*- coding: utf-8 -*-
"""第 7 章：種子樹（重繪）、判斷滑動型式流程。"""
from common_figs import *  # noqa
from figs_ch0 import SEEDS, KIDS


def fig7_1():
    return seed_tree(SEEDS, KIDS, '5 顆種子', '考場上要重建的公式')


def fig7_2():
    return flow([
        ('① 判斷滑動型式', '長而平行→無限｜弱面→平面｜夾層→三塊｜圓弧→切片', KEY),
        ('② 確認深度量法', '鉛直深度還是垂直坡面厚度？決定 cos β 乘幾次', AC),
        ('③ 缺的單位重', '三相：飽和段 *e* = *wG*_{s} → γ_{t}、γ_{sat}', AC),
        ('④ 水放哪裡', '靜水：浮力｜滲流：γ_{w}*h*_{w}cos²β｜切片：*u*Δ*L*｜塊體：水壓另加', AC),
        ('⑤ 拆每一個力', '*W*、*k*_{h}*W*、地錨：沿面 → 分母；垂直 → *N* tan φ', COMP),
        ('⑥ 算 FS', '(凝聚力項 + 有效正向力 × tan φ) ÷ 下滑力', TEN),
        ('⑦ 比門檻、下結論', '常時 1.5、地震／豪雨 1.1～1.2；不足就排水或反算地錨', WARN),
    ], '邊坡解題流程')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
