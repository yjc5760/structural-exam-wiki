# -*- coding: utf-8 -*-
"""影響線講義共用元件：梁簡圖（與影響線共用同一條 x 比例尺）、分段直線影響線、正負塗色。
所有座標由呼叫端以 m 為單位給定，換算一律走 Xm()。"""
from draw import *  # noqa
import math

POS, POS2 = AC, '#bbdefb'       # 影響線正值：藍
NEG, NEG2 = COMP, '#ffcdd2'     # 負值：紅
ILC = AC


class Ax:
    """一條水平 x 比例尺：x（m）→ px。梁與底下各條影響線共用，保證垂直對齊。"""
    def __init__(self, px0, s):
        self.px0, self.s = px0, s

    def __call__(self, x):
        return self.px0 + self.s * x


def beam(ax, y, x0, x1, supports=(), hinges=(), labels=(), c=INK, w=5, lab_dy=-16):
    """supports: [(x, 'pin'|'roller'|'fixL'|'fixR')]；labels: [(x, '名', dx)]。"""
    o = L(ax(x0), y, ax(x1), y, c, w)
    for x, k in supports:
        X = ax(x)
        if k == 'pin':
            o += pin(X, y + 3)
        elif k == 'roller':
            o += roller(X, y + 3)
        elif k == 'fixL':
            o += fixed_left(X, y, 50)
        elif k == 'fixR':
            o += L(X, y - 25, X, y + 25, c, 3) + ''.join(L(X, y - 25 + i * 50 / 7, X + 8, y - 25 + i * 50 / 7 - 7, c, 1) for i in range(8))
    for x in hinges:
        o += hinge(ax(x), y, 6.5)
    for lab in labels:
        x, s = lab[0], lab[1]
        dx = lab[2] if len(lab) > 2 else 0
        o += T(ax(x) + dx, y + lab_dy, s, 16, INK, 'middle', 'bold')
    return o


def il(ax, y0, sy, pts, c=ILC, w=2.6, fill=True, xr=None, axis_lab='', vals=(), name='', name_x=None,
       vsize=15, ticks=(), pfill=None, nfill=None):
    """畫一條分段直線影響線。
    pts：[(x, η), ...]，相同 x 重複兩次表示跳躍。y0＝基線 px，sy＝每單位縱距的 px。
    vals：[(x, η, 文字, 位置 'n'|'s'|'e'|'w'|(dx,dy))]。"""
    xr = xr or (pts[0][0], pts[-1][0])
    Y = lambda v: y0 - sy * v
    o = ''
    if fill:
        # 依正負號切塊塗色
        seg = []
        for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
            if xa == xb:
                continue
            if ya * yb < 0:
                xm = xa + (xb - xa) * ya / (ya - yb)
                seg += [((xa, ya), (xm, 0.0)), ((xm, 0.0), (xb, yb))]
            else:
                seg.append(((xa, ya), (xb, yb)))
        for (xa, ya), (xb, yb) in seg:
            sgn = ya + yb
            if abs(sgn) < 1e-12:
                continue
            col = (pfill or POS2) if sgn > 0 else (nfill or NEG2)
            o += P([(ax(xa), y0), (ax(xa), Y(ya)), (ax(xb), Y(yb)), (ax(xb), y0)], None, fill=col, close=True, op=0.8)
    o += L(ax(xr[0]) - 10, y0, ax(xr[1]) + 14, y0, MUT, 1.3)
    for t in ticks:
        o += L(ax(t), y0 - 4, ax(t), y0 + 4, MUT, 1.2)
    o += P([(ax(x), Y(v)) for x, v in pts], c, w)
    for item in vals:
        x, v, s = item[0], item[1], item[2]
        pos = item[3] if len(item) > 3 else ('n' if v >= 0 else 's')
        X, Yv = ax(x), Y(v)
        o += C(X, Yv, 4, c, '#fff', 1.4)
        if pos == 'n':
            o += T(X, Yv - 10, s, vsize, c, 'middle', 'bold')
        elif pos == 's':
            o += T(X, Yv + 22, s, vsize, c, 'middle', 'bold')
        elif pos == 'e':
            o += T(X + 9, Yv + 5, s, vsize, c, 'start', 'bold')
        elif pos == 'w':
            o += T(X - 9, Yv + 5, s, vsize, c, 'end', 'bold')
        else:
            o += T(X + pos[0], Yv + pos[1], s, vsize, c, 'middle', 'bold')
    if name:
        o += T(name_x if name_x is not None else 14, y0 + 5, name, 16, INK, 'start', 'bold')
    return o


def unit_load(X, y, c=COMP, label='1', h=40, lsize=16):
    """向下單位載重，箭頭尖端在 (X,y)。"""
    return A(X, y - h, X, y - 3, c, 2.8, 12) + T(X, y - h - 7, label, lsize, c, 'middle', 'bold')


def up_arrow(X, y, c=TEN, label='', h=38, lsize=15, ldx=0, anchor='middle'):
    """向上反力，箭頭尖端在 (X,y)。"""
    o = A(X, y + h, X, y + 3, c, 2.6, 11)
    if label:
        o += T(X + ldx, y + h + 18, label, lsize, c, anchor, 'bold')
    return o
