# -*- coding: utf-8 -*-
"""第 7 章：種子樹與解題流程圖。"""
from plot import *  # noqa
from figkit import tree_fig, flow_box


def fig7_1():
    seeds = [('S1', 'S1 有效應力\n*σ*′=*σ*−*u*', TEN), ('S2', 'S2 莫爾圓\n圓心、半徑', COMP), ('S3', 'S3 摩擦塊\n*τ*=*c*+*σ*tan*φ*', WARN),
             ('S4', 'S4 相切\n直角三角形', KEY), ('S5', 'S5 水擠不出\n彈簧＋水', AC), ('S6', 'S6 應力路徑\n圓頂軌跡', TEN)]
    leaves = [('a', '選型\n*i*_{cr}', TEN), ('b', '任意面\n*σ*_{n}、*τ*', COMP), ('c', '主應力式\nsin*φ*′', KEY), ('d', '*θ*_{f}\n*σ*_{ff}、*τ*_{ff}', KEY),
              ('e', 'Skempton\n*φ*_{u}=0', AC), ('f', '由 *φ*′\n推 *S*_{u}', AC), ('g', '*K*_{f}\nAC／LE', TEN)]
    links = [('S1', 'a'), ('S1', 'e'), ('S2', 'b'), ('S2', 'd'), ('S3', 'c'), ('S4', 'c'), ('S4', 'd'), ('S4', 'f'), ('S4', 'g'),
             ('S5', 'e'), ('S5', 'f'), ('S6', 'g'), ('S1', 'f')]
    return tree_fig(seeds, leaves, links, title='種子 → 公式（箭頭＝由誰推出）')


def fig7_2():
    W, H = 900, 640
    o = ''
    xs, w = 250, 330
    steps = [(30, '① 題目給的是總應力還是有效應力？\n（CU 有 *u*_{f}、CD *u*=0、UU 只有 *S*_{u}）', KEY, True),
             (130, '② 換成主應力：*σ*_{1}=*σ*_{3}+軸差；需要時扣 *u*', TEN, False),
             (195, '③ *c*′ 是 0 嗎？', KEY, True),
             (280, '④a *c*=0：sin*φ*=(*σ*_{1}−*σ*_{3})/(*σ*_{1}+*σ*_{3})\n④b 有 *c*：兩點聯立 *σ*_{1}=*N*_{φ}*σ*_{3}+2*c*√*N*_{φ}', KEY, False),
             (370, '⑤ 問角度？量自哪個面（極點／大主應力面）', KEY, True),
             (465, '⑥ 破壞面應力 (*C*−*R*sin*φ*, *R*cos*φ*)；驗算 *τ*=*c*+*σ*tan*φ*', KEY, False),
             (535, '⑦ 孔壓：*A*_{f}=Δ*u*_{f}/Δ*q*_{f}；預測現地用 Skempton', AC, False)]
    prev = None
    for y, txt, c, dia in steps:
        h = 80 if dia else (66 if '\n' in txt else 46)
        o += flow_box(xs - 40, y, w + 80, h, txt, c, diamond=dia)
        if prev is not None:
            o += A(xs + w / 2, prev, xs + w / 2, y, MUT, 1.6, 9)
        prev = y + h
    o += box(30, 40, 170, 120, '先畫', ['一條線', '一個相切的圓', '一條半徑'], KEY2, KEY)
    o += box(700, 200, 190, 90, '常見錯', ['有 *c* 還用比例'], COMP2, COMP)
    o += box(700, 380, 190, 90, '常見錯', ['*θ* 用 *φ*_{cu}'], COMP2, COMP)
    return svg(W, H, o, '解題流程圖')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
