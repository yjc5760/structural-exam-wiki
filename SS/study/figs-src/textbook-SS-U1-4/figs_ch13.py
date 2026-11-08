# -*- coding: utf-8 -*-
"""第 13 章：概念題答題流程。"""
from plot import *  # noqa


def fig13_1():
    W, H = 900, 300
    steps = [('① 圈部位', '哪個接頭、哪道銲、哪顆螺栓', AC),
             ('② 會出什麼事', '沿換手鏈找會壞的站（S1）', COMP),
             ('③ 為什麼', '用種子講機制（S2～S7）', KEY),
             ('④ 規定（數字）', '本書數字卡', WARN),
             ('⑤ 怎麼驗', 'VT／MT／UT／試驗', TEN)]
    bw, gap = 160, 18
    o = T(450, 30, '概念題的五格答法：每一段都走一遍', 17, INK, 'middle', 'bold')
    for i, (t, s, c) in enumerate(steps):
        x = 12 + i * (bw + gap)
        o += R(x, 60, bw, 130, '#fff', c, 2.2, 12)
        o += R(x, 60, bw, 40, c, None, 0, 12) + R(x, 86, bw, 14, c, None)
        o += T(x + bw / 2, 87, t, 16, '#fff', 'middle', 'bold')
        words = s
        o += T(x + bw / 2, 132, words[:9], 14, INK, 'middle')
        if len(words) > 9:
            o += T(x + bw / 2, 156, words[9:], 14, INK, 'middle')
        if i < 4:
            o += A(x + bw + 2, 125, x + bw + gap - 2, 125, INK, 2.2, 9)
    o += R(110, 220, 680, 60, KEY2, KEY, 1.4, 10)
    o += T(450, 246, '開頭一句總論（保險絲／換手鏈），中間逐部位五格，', 15, KEY, 'middle', 'bold')
    o += T(450, 270, '結尾一句因果鏈（例：Northridge → 移除背襯板＋高韌性銲材＋UT＋塑鉸外移）', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '概念題答法')


ALL = {'fig13_1': fig13_1}
