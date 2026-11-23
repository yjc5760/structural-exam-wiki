# -*- coding: utf-8 -*-
"""第 7 章：種子樹與解題流程圖。"""
from plot import *  # noqa
from figkit import tree_fig, flow_box


def fig7_1():
    seeds = [('S1', 'S1 Rankine\n相切', TEN), ('S2', 'S2 Coulomb\n三力閉合', WARN), ('S3', 'S3 剛體\n自由體圖', AC),
             ('S4', 'S4 摩擦塊\n底面', COMP), ('S5', 'S5 梯形\n底壓', WARN), ('S6', 'S6 加勁\n摩擦綁土', KEY)]
    leaves = [('a', '*K*_{a}、*z*_{c}\n水、超載', TEN), ('b', 'Coulomb\nM-O 0.6*H*', WARN), ('c', '分塊\n虛擬牆背', AC), ('d', '*FS*_{SL}\n*φ*=0', COMP),
              ('e', '*FS*_{OT}\n*P*_{av}', AC), ('f', '*e*、*q*_{max}\n*B*′、承載', WARN), ('g', '內穩定\n外穩定', KEY)]
    links = [('S1', 'a'), ('S1', 'c'), ('S2', 'b'), ('S3', 'c'), ('S3', 'd'), ('S3', 'e'), ('S3', 'f'), ('S4', 'd'), ('S5', 'f'), ('S6', 'g'), ('S6', 'd'), ('S6', 'f')]
    return tree_fig(seeds, leaves, links, title='種子 → 公式（箭頭＝由誰推出）')


def fig7_2():
    W, H = 900, 660
    o = ''
    xs, w = 230, 360
    steps = [(30, '① 土壓方向？\n水平／平行地表／偏法線 δ', KEY, True),
             (140, '② 懸臂式？→ 虛擬牆背過踵端；踵上土算牆重', KEY, True),
             (240, '③ 自由體圖：原點牆趾、分塊、Σ*V*、Σ*M*_{R}、Σ*M*_{O}', AC, False),
             (310, '④ 底土 *φ*=0？\n是：抗滑只剩 *S*_{u}*B*；否：Σ*V*tan*δ*+*c*_{a}*B*', KEY, True),
             (420, '⑤ *FS*_{SL}、*FS*_{OT}（*P*_{av} 進 *M*_{R}）', COMP, False),
             (485, '⑥ *x̄*、*e*≤*B*/6、*q*_{max}、*B*′、傾斜因數 → *FS*_{BC}', WARN, False),
             (555, '⑦ 比 1.5／2.0／3.0 → 結論 → 對症補救', KEY, False)]
    prev = None
    for y, txt, c, dia in steps:
        h = 90 if dia else 50
        o += flow_box(xs - 50, y, w + 100, h, txt, c, diamond=dia)
        if prev is not None:
            o += A(xs + w / 2, prev, xs + w / 2, y, MUT, 1.6, 9)
        prev = y + h
    o += box(20, 250, 150, 100, '先寫', ['*γ*_{w}、單位', '界面假設'], KEY2, KEY)
    o += box(730, 330, 160, 90, '常見錯', ['*φ*=0 算牆重'], COMP2, COMP)
    o += box(730, 470, 160, 90, '常見錯', ['漏傾斜因數'], COMP2, COMP)
    return svg(W, H, o, '解題流程圖')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
