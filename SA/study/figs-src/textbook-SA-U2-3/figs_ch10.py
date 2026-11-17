# -*- coding: utf-8 -*-
"""第 10 章：總整理。種子 → 工具 → 考題的家族樹、解題流程圖。"""
from sa_draw import *  # noqa
from figs_ch0 import SEEDS

TOOLS = [
    # (標籤, 章, 種子 index 清單, 代表考題)
    ('主式 4、2、½、−3ψ', '2', (1, 2, 3), '每一題'),
    ('固端彎矩 1/12、1/8、*Pab*^{2}/*L*^{2}', '3', (1, 3), '2017-3、2012-3、2020-1'),
    ('鉸端 3*EI*/*L* ＋ 修正固端彎矩', '4', (1, 3), '2017-3、2022-2、2023-3'),
    ('非均勻斷面 *k*_{AA}、*k*_{AB}', '5', (1,), '2025-3'),
    ('節點平衡、桿端剪力、彈簧沉陷', '6', (0,), '2019-3、2021-1、2023-3'),
    ('層剪力 Σ(*M*+*M*) ＝ −Σ*P*_{x}*y*', '7', (0,), '2017-3、2022-2、2024-3'),
    ('柱側移勁度 12、3（短柱）', '7', (1, 2), '2006-4、2024-3'),
    ('位移圖定 ψ ＋ 虛功', '8', (5, 0), '2014-3、2020-1'),
    ('鏡像：θ\' ＝ ∓θ、勁度 2 與 6', '9', (4,), '2015-3、2020-2、2021-2'),
]


def fig10_1():
    W = 900
    sx, sw, sh = 14, 300, 54
    tx, tw, th = 400, 486, 50
    sy0, sgap = 92, 96
    ty0, tgap = 70, 62
    H = 90 + max(len(SEEDS) * sgap, len(TOOLS) * tgap) + 10
    o = T(sx + sw / 2, 36, '6 顆種子', 18, PUR, 'middle', 'bold')
    o += T(tx + tw / 2, 36, '9 件工具（第幾章｜用在哪些考題）', 18, INK, 'middle', 'bold')
    spos = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        spos[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.4, 10)
        o += R(sx, y, 46, sh, c, None, 0, 10) + R(sx + 30, y, 16, sh, c, None)
        o += T(sx + 23, y + 33, sid, 16, '#fff', 'middle', 'bold')
        short = txt.split('：')[0]
        o += T(sx + 58, y + 24, short, 15, INK, 'start', 'bold')
        o += T(sx + 58, y + 45, txt.split('：', 1)[1] if '：' in txt else '', 14, MUT, 'start')
    for j, (lab, ch, seeds, ex) in enumerate(TOOLS):
        y = ty0 + j * tgap
        for si in seeds:
            x1, y1, c = spos[si]
            x2, y2 = tx, y + th / 2
            mx = (x1 + x2) / 2
            o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.8" opacity=".7"/>'
            o += head(x2, y2, 0, c, 8)
        o += R(tx, y, tw, th, '#fafafa', STEEL, 1.1, 8)
        o += R(tx, y, 58, th, STEEL2, None, 0, 8)
        o += T(tx + 29, y + 31, f'第{ch}章', 14, MUT, 'middle', 'bold')
        o += T(tx + 68, y + 22, lab, 15, INK, 'start', 'bold')
        o += T(tx + 68, y + 42, ex, 14, AC, 'start')
    return svg(W, int(H), o, '種子、工具與考題')


STEPS = [
    ('① 讀圖', '支承、內鉸、斜桿、桿上或節點載重', '題目正本的判讀清單', '1'),
    ('② 盤點未知數', '剛節點 θ；每層一個 Δ', '鉸端修正式先消掉；斜桿看位移圖', '1、4、8'),
    ('③ 能不能降維', '結構＋載重照鏡子：對稱／反對稱', '內鉸、支承不同就不行', '9'),
    ('④ 固端彎矩', '桿件攤平看載重朝上或朝下', '斜桿只取法向；節點載重不算', '3、4、8'),
    ('⑤ 桿端彎矩', '主式 2(2θ_{近}+θ_{遠}−3ψ)；鉸端 3(θ−ψ)', '非均勻斷面換成 *k*_{AA}、*k*_{AB}', '2、4、5'),
    ('⑥ 列方程', '每個 θ：節點 Σ*M* ＝ *M*_{外}', '每個 Δ：層剪力或虛功', '6、7、8'),
    ('⑦ 解、代回', '分數到底，最後才化小數', '代回節點與層剪力檢查', '7'),
    ('⑧ 驗算與反求', 'Σ*F* ＝ 0、方向合物理', '鉸端轉角、剪力、反力、彎矩圖', '4、6'),
]


def fig10_2():
    W = 900
    bw, bh = 400, 92
    xs = (30, 470)
    y0, gap = 84, 116
    rows = (len(STEPS) + 1) // 2
    H = y0 + rows * gap + 10
    o = T(W / 2, 34, '解題流程：八步，每一步對應一章', 18, INK, 'middle', 'bold')
    pos = []
    for i, (t, a, b, ch) in enumerate(STEPS):
        col = i // rows
        row = i % rows
        x, y = xs[col], y0 + row * gap
        pos.append((x, y))
        c = [DEF, INK, PUR, LOAD, MOM, FOR, INK, FOR][i]
        o += R(x, y, bw, bh, '#fff', c, 2, 10)
        o += R(x, y, 150, bh, c, None, 0, 10) + R(x + 130, y, 20, bh, c, None)
        o += T(x + 75, y + 42, t, 16, '#fff', 'middle', 'bold')
        o += T(x + 75, y + 70, f'第 {ch} 章', 14, '#fff', 'middle')
        o += T(x + 162, y + 34, a, 14, INK, 'start')
        o += T(x + 162, y + 62, b, 14, MUT, 'start')
    for i in range(len(STEPS) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if x1 == x2:
            o += A(x1 + 75, y1 + bh + 2, x2 + 75, y2 - 4, INK, 2, 10)
        else:
            o += curve_arrow([(x1 + bw, y1 + bh / 2), (x1 + bw + 20, y1 + bh / 2), (x2 - 20, y0 + bh / 2 - 60), (x2 + 75, y0 - 18), (x2 + 75, y2 - 4)], INK, 2, 10)
    return svg(W, int(H), o, '解題流程')


ALL = {'fig10_1': fig10_1, 'fig10_2': fig10_2}
