# -*- coding: utf-8 -*-
"""第 7 章：種子樹（由下而上推導關係）與解題流程圖。"""
from plot import *  # noqa
from calcs import *  # noqa


def tree_fig(seeds, leaves, links, W=900, H=430, title=''):
    """seeds: [(id, label, color)]；leaves: [(id, label, color)]；links: [(seed_id, leaf_id)]"""
    o = T(W / 2, 28, title, 17, KEY, 'middle', 'bold') if title else ''
    ns, nl = len(seeds), len(leaves)
    sw = (W - 40) / ns
    lw = (W - 40) / nl
    pos = {}
    for i, (k, lab, c) in enumerate(seeds):
        x = 20 + sw * (i + 0.5)
        pos[k] = (x, 92)
        o += R(x - sw / 2 + 6, 62, sw - 12, 60, KEY2, KEY, 2, 10)
        for j, line in enumerate(lab.split('\n')):
            o += T(x, 86 + j * 22, line, 15 if j == 0 else 14, KEY if j == 0 else INK, 'middle', 'bold' if j == 0 else None)
    for i, (k, lab, c) in enumerate(leaves):
        x = 20 + lw * (i + 0.5)
        pos[k] = (x, H - 80)
        lines = lab.split('\n')
        o += R(x - lw / 2 + 4, H - 110, lw - 8, 26 + 22 * len(lines), '#fff', c, 1.5, 8)
        for j, line in enumerate(lines):
            o += T(x, H - 90 + j * 22, line, 14, c, 'middle', 'bold' if j == 0 else None)
    for a, b in links:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        o += A(x1, y1 + 32, x2, y2 - 34, MUT, 1.3, 8)
    return svg(W, H, o, title or '種子樹')


def fig7_1():
    seeds = [('S1', 'S1 土粒不變\n柱子 1、*e*', AC), ('S6', 'S6 潤滑→佔位\n夯實曲線', COMP), ('S2', 'S2 *σ*′=*σ*−*u*\n三條線', TEN),
             ('S4', 'S4 力會擴散\n2:1 錐', WARN), ('S3', 'S3 兩條直線\n折點 *p*_{c}′', KEY), ('S5', 'S5 路徑平方\n擴散', WARN)]
    leaves = [('a', '三相組\n*D*_{r}、土方', AC), ('b', '*γ*_{zav}\n能量、R.C.', COMP), ('c', '*p*_{0}′\nΔ*σ*′', TEN),
              ('d', 'Δ*p*\n層平均', WARN), ('e', 'OCR、*m*_{v}\nCasagrande', KEY), ('f', '沉陷三式\n次壓密', KEY), ('g', '*T*_{v}、*H*_{dr}\n兩段式', WARN)]
    links = [('S1', 'a'), ('S1', 'b'), ('S6', 'b'), ('S2', 'c'), ('S4', 'd'), ('S3', 'e'), ('S1', 'e'),
             ('S1', 'f'), ('S3', 'f'), ('S2', 'f'), ('S4', 'f'), ('S5', 'g')]
    return tree_fig(seeds, leaves, links, title='種子 → 公式（箭頭＝由誰推出）')


def flow_box(x, y, w, h, txt, c=AC, fill=None, diamond=False):
    o = ''
    if diamond:
        o += P([(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)], c, 1.8, fill=fill or KEY2, close=True)
    else:
        o += R(x, y, w, h, fill or '#fff', c, 1.6, 8)
    lines = txt.split('\n')
    for j, line in enumerate(lines):
        o += T(x + w / 2, y + h / 2 + 6 + (j - (len(lines) - 1) / 2) * 20, line, 14, c, 'middle', 'bold' if j == 0 else None)
    return o


def fig7_2():
    W, H = 900, 640
    o = ''
    # 主線（右）
    xs, w = 330, 250
    steps = [(30, '① 畫剖面、水位、黏土中點', TEN, False),
             (100, '② *p*_{0}′＝Σ*γh*−*u*（水位上用 *γ*_{d}）', TEN, False),
             (170, '③ Δ*p*：大面積／2:1／水位變化', WARN, False),
             (240, '④ 三個數比大小\n*p*_{0}′、*p*_{c}′、*p*_{0}′+Δ*p*', KEY, True),
             (340, '⑤ 沉陷：每段 *C*log(終/起)×*H*/(1+*e*_{0})', KEY, False),
             (410, '⑥ 上下透水嗎？\n*H*_{dr}=*H* 或 *H*/2', WARN, True),
             (510, '⑦ *T*_{v}=*c*_{v}*t*/*H*_{dr}^{2} ↔ *U*（60% 換式）', WARN, False),
             (580, '⑧ *S*_{t}=*U*·*S*_{c}；或反求 *t*', WARN, False)]
    prev = None
    for y, txt, c, dia in steps:
        h = 80 if dia else 46
        ww = w + (70 if dia else 70)
        x = xs - 35
        o += flow_box(x, y, ww, h, txt, c, diamond=dia)
        if prev is not None:
            o += A(xs + w / 2, prev, xs + w / 2, y, MUT, 1.6, 9)
        prev = y + h
    # 夯實支線（左）
    o += flow_box(30, 30, 220, 46, '夯實／土方題', COMP)
    o += A(140, 76, 140, 110, MUT, 1.6, 9)
    o += flow_box(30, 110, 220, 46, '畫三相柱（S1）', AC)
    o += A(140, 156, 140, 190, MUT, 1.6, 9)
    o += flow_box(30, 190, 220, 66, '*D*_{r}／R.C.／*γ*_{zav}\n土粒重守恆', AC)
    o += A(140, 256, 140, 290, MUT, 1.6, 9)
    o += flow_box(30, 290, 220, 66, '說明題：能量、乾濕側\nCBR 取較高 *γ*_{d}', COMP)
    # 右側提醒
    o += box(660, 255, 225, 66, '④ 的結果', ['只淺／只陡／兩段'], KEY2, KEY)
    o += box(660, 425, 225, 66, '⑥ 的結果', ['試體與現場常不同'], WARN2, WARN)
    return svg(W, H, o, '解題流程圖')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
