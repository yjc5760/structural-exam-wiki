# -*- coding: utf-8 -*-
"""RC-U1-1 共用圖元：斷面＋應變＋內力三聯圖、流程圖節點。所有尺寸依實際 cm 比例。"""
from plot import *  # noqa
import math


def section(x0, y0, sc, b, h, be=None, hf=None, flange_top=True, fill=STEEL2):
    """畫矩形或 T 形斷面，(x0,y0) 為斷面『腹板』中心線頂點的 x 與頂面 y。回傳 (svg, 左緣 x, 右緣 x)。"""
    o = ''
    if be and hf:
        if flange_top:
            o += R(x0 - be * sc / 2, y0, be * sc, hf * sc, fill, INK, 1.6)
            o += R(x0 - b * sc / 2, y0 + hf * sc, b * sc, (h - hf) * sc, fill, INK, 1.6)
            o += L(x0 - b * sc / 2 + 1, y0 + hf * sc, x0 + b * sc / 2 - 1, y0 + hf * sc, fill, 2.5)
        else:
            o += R(x0 - b * sc / 2, y0, b * sc, (h - hf) * sc, fill, INK, 1.6)
            o += R(x0 - be * sc / 2, y0 + (h - hf) * sc, be * sc, hf * sc, fill, INK, 1.6)
            o += L(x0 - b * sc / 2 + 1, y0 + (h - hf) * sc, x0 + b * sc / 2 - 1, y0 + (h - hf) * sc, fill, 2.5)
        return o
    o += R(x0 - b * sc / 2, y0, b * sc, h * sc, fill, INK, 1.6)
    return o


def bars(x0, y, sc, b, n, db, c=INK, cover=6.0, fill=None):
    """在深度 y（px）畫 n 根鋼筋，橫向均分於 b - 2*cover 範圍。"""
    o = ''
    if n == 1:
        xs = [x0]
    else:
        span = (b - 2 * cover) * sc
        xs = [x0 - span / 2 + span * i / (n - 1) for i in range(n)]
    r = max(db * sc / 2, 4.5)
    for xx in xs:
        o += C(xx, y, r, fill or c, '#fff', 1.2)
    return o


def strain_panel(xa, y0, sc, h, c, layers, emax_px=150, ecu=0.003, title=True, ecu_label='0.003'):
    """應變圖：xa 為零應變基準線，向左為壓、向右為拉。layers=[(深度cm, ε 拉為正, 標籤, 顏色)]。"""
    big = max([ecu] + [abs(e) for _, e, _, _ in layers])
    k = emax_px / big
    yc = y0 + c * sc
    yb = y0 + h * sc
    o = L(xa, y0 - 6, xa, yb + 6, MUT, 1.2, '4 3')
    # 線性應變：頂 -ecu、在 c 為 0
    def ex(depth):
        return xa + k * ecu * (depth - c) / c
    top = (xa - k * ecu, y0)
    bot_e = ecu * (h - c) / c
    pts = [top, (xa + k * bot_e, yb)]
    o += P([(xa, y0)] + [top] + [(xa, yc)], None, fill=COMP2, close=True)
    o += P([(xa, yc), (xa + k * bot_e, yb), (xa, yb)], None, fill=TEN2, close=True)
    o += L(top[0], top[1], pts[1][0], pts[1][1], INK, 2.2)
    o += T(top[0] - 4, y0 - 8, ecu_label, 15, COMP, 'middle', 'bold')
    o += L(xa - 8, yc, xa + 8, yc, INK, 1.5)
    for depth, e, lab, col in layers:
        xx = ex(depth)
        yy = y0 + depth * sc
        o += L(xa, yy, xx, yy, col, 2.4) + C(xx, yy, 4, col, '#fff', 1)
        if lab:
            anc = 'start' if xx >= xa else 'end'
            o += T(xx + (8 if xx >= xa else -8), yy + 5, lab, 14, col, anc, 'bold')
    return o, k, ex


def node(x, y, w, h, lines, fill=AC2, c=AC, size=15, shape='box', weight=None, tc=INK):
    """流程圖節點；(x,y) 為中心。shape：box／dia（菱形）／round。"""
    o = ''
    if shape == 'dia':
        o += P([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], c, 1.8, fill=fill, close=True)
    else:
        o += R(x - w / 2, y - h / 2, w, h, fill, c, 1.8, 14 if shape == 'round' else 8)
    n = len(lines)
    for i, s in enumerate(lines):
        o += T(x, y + (i - (n - 1) / 2) * (size + 6) + size * 0.35, s, size, tc, 'middle', weight)
    return o


def arrow_v(x, y1, y2, c=INK, label=None, side=1):
    o = A(x, y1, x, y2, c, 1.8, 10)
    if label:
        o += T(x + 8 * side, (y1 + y2) / 2 + 5, label, 14, c, 'start' if side > 0 else 'end', 'bold')
    return o


def arrow_path(pts, c=INK, label=None, lx=None, ly=None, anchor='middle'):
    o = P(pts[:-1] + [pts[-1]], c, 1.8)
    x1, y1 = pts[-2]; x2, y2 = pts[-1]
    o += head(x2, y2, math.atan2(y2 - y1, x2 - x1), c, 10)
    if label:
        o += T(lx, ly, label, 14, c, anchor, 'bold')
    return o


def vdim(x, y1, y2, label, c=INK, side=1, size=15, tick=6, weight=None, gap=8):
    """垂直尺寸線，標籤放在線的左（side=-1）或右（side=1），垂直置中。"""
    o = L(x, y1, x, y2, c, 1.2)
    o += L(x - tick, y1, x + tick, y1, c, 1.2) + L(x - tick, y2, x + tick, y2, c, 1.2)
    o += T(x + side * gap, (y1 + y2) / 2 + size * 0.35, label, size, c, 'start' if side > 0 else 'end', weight)
    return o


def hdim(x1, x2, y, label, c=INK, side=1, size=15, tick=6, weight=None, gap=8):
    """水平尺寸線，標籤在線下（side=1）或上（side=-1）。"""
    o = L(x1, y, x2, y, c, 1.2)
    o += L(x1, y - tick, x1, y + tick, c, 1.2) + L(x2, y - tick, x2, y + tick, c, 1.2)
    o += T((x1 + x2) / 2, y + (gap + size * 0.8 if side > 0 else -gap), label, size, c, 'middle', weight)
    return o
