# -*- coding: utf-8 -*-
"""第 12 章：開槽型式、NDT 對應。"""
from plot import *  # noqa


def fig12_1():
    W, H = 900, 300
    o = ''
    y0, t = 110, 60
    # Single V
    o += T(230, 40, '(a) Single V：兩片都開斜角', 16, INK, 'middle', 'bold')
    cx = 230
    o += P([(cx - 180, y0), (cx - 20, y0), (cx - 4, y0 + t), (cx - 180, y0 + t)], INK, 1.6, fill=STEEL2, close=True)
    o += P([(cx + 180, y0), (cx + 20, y0), (cx + 4, y0 + t), (cx + 180, y0 + t)], INK, 1.6, fill=STEEL2, close=True)
    o += P([(cx - 20, y0), (cx + 20, y0), (cx + 4, y0 + t), (cx - 4, y0 + t)], COMP, 1.4, fill=WARN2, close=True)
    o += T(cx, y0 + t + 34, '對接（Butt）；對稱，較易熔透', 14, INK, 'middle')
    # Single bevel
    o += T(670, 40, '(b) Single Bevel：只開一片', 16, INK, 'middle', 'bold')
    cx = 650
    o += P([(cx - 180, y0), (cx - 34, y0), (cx - 4, y0 + t), (cx - 180, y0 + t)], INK, 1.6, fill=STEEL2, close=True)
    o += R(cx + 4, y0 - 60, 40, t + 120, STEEL2, INK, 1.6)
    o += P([(cx - 34, y0), (cx + 4, y0), (cx + 4, y0 + t), (cx - 4, y0 + t)], COMP, 1.4, fill=WARN2, close=True)
    o += T(cx - 100, y0 + t + 34, 'T 形、角接；加工少，根部較難熔透', 14, INK, 'middle')
    o += R(110, 238, 680, 46, KEY2, KEY, 1.4, 8)
    o += T(450, 267, 'Single／Double＝單面／雙面開槽；字根 V＝兩片開斜角、Bevel＝一片開斜角', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '開槽型式')


ALL = {'fig12_1': fig12_1}
