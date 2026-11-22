# -*- coding: utf-8 -*-
"""第 4 章：臨界斷面——力要走路、三個例外。"""
from figs_common import *  # noqa
from calcs import demo
import math

D = demo()


def fig4_1():
    W, H = 900, 420
    o = T(450, 24, '距支承 *d* 以內的載重：沿短壓桿直接進支承，不過裂縫', 16, INK, 'middle', 'bold')
    sc = 2.6
    x0, y0 = 130, 110
    h, d = D['h'], D['d']
    Lb = 230
    # 柱
    o += R(x0 - 60, y0 - 30, 60, h * sc + 120, STEEL3, INK, 1.6)
    o += T(x0 - 30, y0 + h * sc + 116, '柱', 15, INK, 'middle', 'bold')
    o += R(x0, y0, Lb * sc, h * sc, STEEL2, INK, 1.6)
    ys = y0 + d * sc
    o += L(x0, ys, x0 + Lb * sc, ys, INK, 3)
    # 裂縫
    o += L(x0 + 4, ys, x0 + d * sc, y0 + 6, COMP, 3.2)
    o += T(x0 + d * sc * 0.55 + 14, y0 + d * sc * 0.55, '第一條斜裂縫', 15, COMP, 'start', 'bold')
    # 載重箭頭
    for i in range(12):
        xx = x0 + 10 + i * 20 * sc * 0.9
        if xx > x0 + Lb * sc - 10:
            break
        inside = xx - x0 < d * sc
        col = KEY if inside else MUT
        o += A(xx, y0 - 46, xx, y0 - 4, col, 2 if inside else 1.4, 9)
        if inside:
            o += L(xx, y0 + 4, x0 + 6, y0 + h * sc - 30, KEY, 1.6, '5 3')
    o += hdim(x0, x0 + d * sc, y0 - 62, f'*d* = {d:.0f} cm', KEY, -1, 15)
    o += L(x0 + d * sc, y0 - 6, x0 + d * sc, y0 + h * sc + 30, KEY, 1.6, '6 4')
    o += T(x0 + d * sc, y0 + h * sc + 50, '臨界斷面', 15, KEY, 'middle', 'bold')
    o += T(x0 + 4, y0 + h * sc + 50, '支承面', 15, INK, 'start', 'bold')
    o += T(x0 + 420, y0 - 54, '*d* 以外的載重要跨過裂縫', 15, MUT, 'middle')
    bx = x0 + Lb * sc - 10
    o += box(690, 140, 195, 200, '示範梁', [f'支承面 {D["Vsup"]/1000:.2f} tf', f'*x* = *d* 處 {D["Vu"]/1000:.2f} tf', '箍筋間距', f'{D["s_face"]:.2f} → {D["s_req"]:.2f} cm', '（三條件成立）'], KEY2, KEY, 15, 14)
    return svg(W, H, o, 'd 偏移的物理')


def _beam(x, y, w, h):
    return R(x, y, w, h, STEEL2, INK, 1.4)


def fig4_2():
    W, H = 900, 340
    o = T(450, 24, '三種不能偏移的情況：那根「短壓桿」不存在', 16, INK, 'middle', 'bold')
    bw_, bh_ = 230, 80
    # ① 吊掛支承
    x, y = 40, 120
    o += _beam(x, y, bw_, bh_)
    o += L(x + 20, y - 60, x + 20, y + bh_ - 6, TEN, 3.5)
    o += R(x + 8, y + bh_ - 8, 24, 8, INK, INK, 1)
    o += A(x + 20, y - 30, x + 20, y - 70, TEN, 2.2, 9)
    o += T(x + 30, y - 46, '吊桿受拉', 14, TEN, 'start', 'bold')
    o += L(x + 30, y + bh_ - 8, x + 110, y + 4, COMP, 2.4)
    for i in range(5):
        o += A(x + 60 + i * 34, y - 34, x + 60 + i * 34, y - 4, MUT, 1.4, 8)
    o += T(x + bw_ / 2, y + bh_ + 34, '① 支承把端區拉開', 15, COMP, 'middle', 'bold')
    o += T(x + bw_ / 2, y + bh_ + 58, '（吊掛、支承在拉力面）', 14, MUT, 'middle')
    # ② 倒 T 下翼板載重
    x = 335
    o += R(x, y, bw_, bh_ - 26, STEEL2, INK, 1.4)
    o += R(x - 0, y + bh_ - 26, bw_, 26, STEEL2, INK, 1.4)
    o += pin(x + 20, y + bh_, INK, 9)
    for i in range(5):
        xx = x + 60 + i * 34
        o += A(xx, y + bh_ - 70, xx, y + bh_ - 28, WARN, 2, 8)
    o += T(x + bw_ - 6, y - 10, '載重在下翼板頂面', 14, WARN, 'end', 'bold')
    o += L(x + 30, y + bh_ - 4, x + 110, y + 6, COMP, 2.4)
    o += T(x + bw_ / 2, y + bh_ + 34, '② 載重從拉力側進來', 15, COMP, 'middle', 'bold')
    o += T(x + bw_ / 2, y + bh_ + 58, '（RC-2020-2 倒 T 梁）', 14, MUT, 'middle')
    # ③ d 內集中載重
    x = 630
    o += _beam(x, y, bw_, bh_)
    o += pin(x + 20, y + bh_, INK, 9)
    o += A(x + 62, y - 70, x + 62, y - 4, COMP, 3.2, 11)
    o += T(x + 70, y - 46, '*P*', 17, COMP, 'start', 'bold')
    o += L(x + 100, y - 2, x + 100, y + bh_, KEY, 1.4, '5 3')
    o += A(x + 80, y + bh_ - 16, x + 100, y + bh_ - 16, KEY, 1.2, 7) + A(x + 40, y + bh_ - 16, x + 20, y + bh_ - 16, KEY, 1.2, 7)
    o += T(x + 60, y + bh_ - 11, '*d*', 15, KEY, 'middle', 'bold')
    for i in range(3):
        o += A(x + 140 + i * 30, y - 34, x + 140 + i * 30, y - 4, MUT, 1.4, 8)
    o += T(x + bw_ / 2, y + bh_ + 34, '③ *d* 以內有集中載重', 15, COMP, 'middle', 'bold')
    o += T(x + bw_ / 2, y + bh_ + 58, '（小梁、柱落在梁上）', 14, MUT, 'middle')
    o += T(450, 318, '三種情況都要在「支承面」取 *V*_{u}。', 16, INK, 'middle', 'bold')
    return svg(W, H, o, '不可偏移的三種情況')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2}
