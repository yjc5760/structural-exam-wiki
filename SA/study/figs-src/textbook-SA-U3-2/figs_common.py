# -*- coding: utf-8 -*-
"""本單元共用圖元：彈簧、柱的變形曲線（由 calcs 的形狀函數算出）、剛性梁、固定端、彎矩弧箭頭。"""
from plot import *  # noqa
import math
from calcs import ff_shape

TEAL = '#00838f'
BROWN = '#6d4c41'


def spring(x1, y, x2, c=TEN, w=2.2, n=7, amp=10, lead=14):
    """水平彈簧（鋸齒）。"""
    pts = [(x1, y), (x1 + lead, y)]
    seg = (x2 - x1 - 2 * lead) / (2 * n)
    for i in range(2 * n):
        pts.append((x1 + lead + seg * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts += [(x2 - lead, y), (x2, y)]
    return P(pts, c, w)


def vspring(x, y1, y2, c=TEN, w=2.2, n=6, amp=10, lead=12):
    """垂直彈簧（y1 在上、y2 在下）。"""
    pts = [(x, y1), (x, y1 + lead)]
    seg = (y2 - y1 - 2 * lead) / (2 * n)
    for i in range(2 * n):
        pts.append((x + (amp if i % 2 == 0 else -amp), y1 + lead + seg * (i + 0.5)))
    pts += [(x, y2 - lead), (x, y2)]
    return P(pts, c, w)


def col_ff(x, yb, yt, d0, d1, c=AC, w=3, dash=None, n=60):
    """兩端不轉的柱：底端側移 d0、頂端側移 d1（像素），形狀 3ξ²−2ξ³。"""
    pts = []
    for i in range(n + 1):
        xi = i / n
        pts.append((x + d0 + (d1 - d0) * ff_shape(xi), yb + (yt - yb) * xi))
    return P(pts, c, w, dash=dash)


def col_pin_base(x, yb, yt, d1, c=AC, w=3, dash=None, n=60):
    """柱頂不轉、柱底鉸接（不動）：整根是一支從柱頂伸下來的懸臂。"""
    pts = []
    for i in range(n + 1):
        xi = i / n                    # 由下往上
        s = 1 - xi                    # 距柱頂（相對）
        pts.append((x + d1 - d1 * (3 * s ** 2 - s ** 3) / 2, yb + (yt - yb) * xi))
    return P(pts, c, w, dash=dash)


def rigid_beam(x1, x2, y, c=INK, t=9):
    """剛性梁（I＝∞）：粗實心條。"""
    return R(x1, y - t / 2, x2 - x1, t, c, None, 0, 2)


def base_fixed(x, y, w=44, c=INK):
    return fixed_wall(x, y, w, c)


def arc_arrow(cx, cy, r, a0, a1, c=COMP, w=2.2, size=10):
    """圓弧箭頭；a0→a1 為數學角度（度，逆時針為正，0° 朝右）。"""
    n = 24
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return curve_arrow(pts, c, w, size)


def node(x, y, r=6, c=INK, fill='#fff'):
    return C(x, y, r, fill, c, 2)


def roller_block(x, y, w=34, h=26, fill='#fff', c=INK):
    return R(x - w / 2, y - h / 2, w, h, fill, c, 2, 4)


def lock(x, y, c=WARN, s=11):
    """鎖住的符號（小鎖頭）。"""
    o = P([(x - s * 0.55, y - s * 0.2), (x - s * 0.55, y - s * 0.75)], c, 2.2)
    o += f'<path d="M{f(x - s * 0.55)},{f(y - s * 0.75)} A{f(s * 0.55)},{f(s * 0.55)} 0 0 1 {f(x + s * 0.55)},{f(y - s * 0.75)}" fill="none" stroke="{c}" stroke-width="2.2"/>'
    o += L(x + s * 0.55, y - s * 0.75, x + s * 0.55, y - s * 0.2, c, 2.2)
    o += R(x - s * 0.85, y - s * 0.25, s * 1.7, s * 1.25, c, None, 0, 2.5)
    return o
