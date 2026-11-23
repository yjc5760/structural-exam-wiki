# -*- coding: utf-8 -*-
"""第 8 章：種子樹與解題流程圖。"""
from plot import *  # noqa
from figkit import tree_fig, flow_box


def fig8_1():
    seeds = [('S1', 'S1 Rankine\n相切', TEN), ('S2', 'S2 水 *K*=1\n分開算', AC), ('S3', 'S3 平衡\nΣ*M*=Σ*F*=0', WARN),
             ('S4', 'S4 倒過來的\n基礎', COMP), ('S5', 'S5 水的\n三種攻擊', AC), ('S6', 'S6 天平\n反算', KEY)]
    leaves = [('a', '*K*_{a}、*K*_{p}\n4*c*_{u}−*γH*', TEN), ('b', '懸臂\n*L*_{3}、簡化法', WARN), ('c', '自由端\nBlum', WARN), ('d', 'Peck\n鉸接法', COMP),
              ('e', '隆起\nB–E', COMP), ('f', '上舉\n砂湧', AC), ('g', '門檻\n對策', KEY)]
    links = [('S1', 'a'), ('S1', 'b'), ('S1', 'c'), ('S1', 'd'), ('S2', 'a'), ('S2', 'b'), ('S3', 'b'), ('S3', 'c'), ('S3', 'd'),
             ('S4', 'e'), ('S4', 'd'), ('S5', 'f'), ('S6', 'g'), ('S6', 'e'), ('S6', 'f')]
    return tree_fig(seeds, leaves, links, title='種子 → 公式（箭頭＝由誰推出）')


def fig8_2():
    W, H = 900, 640
    o = ''
    xs, w = 230, 360
    steps = [(30, '① 數橫桿：0 懸臂／1 錨定／多根 Peck', WARN, True),
             (130, '② 開挖面以下是砂還是黏土？\n砂：有效應力＋水；黏土：*φ*=0、先算 *N*_{s}', KEY, True),
             (240, '③ 擋土計算：土壓 → 取矩求 *D*、*T*／支撐力×*s*', WARN, False),
             (310, '④ 坑底黏土 → 隆起（有 *B*×*L* 用三維）', COMP, False),
             (375, '⑤ 有水位／受壓層？\n砂湧（最短流徑）／上舉（蓋子平衡）', KEY, True),
             (480, '⑥ 與門檻比較：1.2～1.5／1.5～2.0', KEY, False),
             (545, '⑦ 不足：反算 → 對策（先降驅動）→ 監測', KEY, False)]
    prev = None
    for y, txt, c, dia in steps:
        h = 86 if dia else 46
        o += flow_box(xs - 40, y, w + 80, h, txt, c, diamond=dia)
        if prev is not None:
            o += A(xs + w / 2, prev, xs + w / 2, y, MUT, 1.6, 9)
        prev = y + h
    o += box(20, 40, 160, 110, '最先寫', ['*γ*_{w} 取值', '單位'], KEY2, KEY)
    o += box(720, 150, 170, 90, '常見錯', ['*γ*_{sat}×*K*_{a}'], COMP2, COMP)
    o += box(720, 390, 170, 90, '常見錯', ['上舉寫加長壁'], COMP2, COMP)
    return svg(W, H, o, '解題流程圖')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
