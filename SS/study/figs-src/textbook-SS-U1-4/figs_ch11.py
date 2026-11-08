# -*- coding: utf-8 -*-
"""第 11 章：銲接接合的破壞位置。"""
from plot import *  # noqa
import math


def _tag(x, y, n, c):
    return C(x, y, 13, c, '#fff', 1.6) + T(x, y + 5, str(n), 14, '#fff', 'middle', 'bold')


def fig11_1():
    W, H = 900, 470
    o = T(230, 28, '(a) 填角銲（T 形接合）', 16, INK, 'middle', 'bold')
    ox, oy, w = 140, 330, 150
    o += R(ox - 36, 60, 36, oy - 60, STEEL2, INK, 1.4)          # 豎板
    o += R(ox - 36 - 60, oy, 330, 40, STEEL2, INK, 1.4)          # 平板
    o += P([(ox, oy), (ox, oy - w), (ox + w, oy)], INK, 2, fill=WARN2, close=True)
    # HAZ 帶
    o += P([(ox + 2, oy - w - 18), (ox + 14, oy - w - 18), (ox + 14, oy - 2)], None, fill=COMP2, close=False)
    o += R(ox, oy - w - 18, 14, w + 18, COMP2, None, op=0.8)
    o += R(ox, oy, w + 18, 14, COMP2, None, op=0.8)
    o += L(ox, oy, ox + w / 2, oy - w / 2, COMP, 3.4)                  # 喉面
    o += _tag(ox + w / 2 + 10, oy - w / 2 - 22, 1, COMP)
    o += _tag(ox - 4, oy + 4, 2, KEY)                                  # 根部
    o += _tag(ox + w + 14, oy - 14, 3, WARN)                           # 趾部
    o += _tag(ox + 30, oy + 26, 4, AC)                                 # HAZ
    o += L(ox - 36, 120, ox - 36, 300, TEN, 3, '6 4')
    o += _tag(ox - 60, 210, 5, TEN)                                    # 母材
    o += T(230, 420, '豎板若是厚柱板：板厚方向受拉 → 層狀撕裂（⑥）', 14, MUT, 'middle')
    # (b) CJP
    o += T(680, 28, '(b) 全滲透開槽銲（CJP，單斜開槽）', 16, INK, 'middle', 'bold')
    bx, by = 600, 80
    o += R(bx - 150, by, 150, 60, STEEL2, INK, 1.4)
    o += R(bx + 40, by, 150, 60, STEEL2, INK, 1.4)
    o += P([(bx, by), (bx + 40, by), (bx + 40, by + 60), (bx + 8, by + 60), (bx, by)], INK, 1.6, fill=WARN2, close=True)
    o += R(bx - 6, by + 60, 56, 12, STEEL3, INK, 1)                    # 背襯板
    o += T(bx + 60, by + 76, '背襯板', 14, MUT, 'start')
    o += _tag(bx - 24, by + 66, 2, KEY)
    o += _tag(bx + 62, by - 14, 4, AC)
    o += _tag(bx + 22, by + 30, 7, COMP)
    rows = [('① 喉面剪斷', COMP), ('② 根部未熔合 → 裂縫起點', KEY), ('③ 趾部應力集中 → 疲勞裂縫', WARN),
            ('④ HAZ 脆化、氫致冷裂', AC), ('⑤ 母材沿銲道邊撕裂（塊剪）', TEN), ('⑥ 層狀撕裂（板厚方向）', INK), ('⑦ 銲道內部瑕疵（氣孔、夾渣）', COMP)]
    o += R(470, 210, 420, 240, '#fff', KEY, 1.6, 10)
    for i, (t, c) in enumerate(rows):
        o += T(490, 240 + i * 30, t, 15, c, 'start', 'bold' if i < 2 else None)
    return svg(W, H, o, '銲接破壞位置')


ALL = {'fig11_1': fig11_1}
