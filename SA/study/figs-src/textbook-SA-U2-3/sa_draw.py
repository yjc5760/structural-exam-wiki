# -*- coding: utf-8 -*-
"""SA-U2-3 專用繪圖元件：彎矩弧形箭頭、角度弧、牆式固定端、滾支承、桿件彈性曲線。
全書顏色：藍＝變形與幾何（彈性曲線、θ、ψ、弦）；紅＝彎矩；綠＝力與平衡；橘＝載重與固端彎矩；紫＝種子與關鍵結果。"""
from plot import *  # noqa
import math

DEF = AC          # 變形
MOM = COMP        # 彎矩
FOR = TEN         # 力
LOAD = WARN       # 載重
PUR = '#7b1fa2'


def arc_pts(cx, cy, r, a0, a1, n=40):
    """螢幕座標的圓弧點（角度以度、螢幕座標下角度增加＝視覺上順時針）。"""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def moment(cx, cy, r=26, cw=True, c=MOM, w=2.2, start=None, span=250):
    """彎矩弧形箭頭。cw=True 畫順時針（視覺上）。start 為起始角（度，螢幕座標）。"""
    if start is None:
        start = 145 if cw else 35
    a1 = start + span if cw else start - span
    return curve_arrow(arc_pts(cx, cy, r, start, a1), c, w, 10)


def angle_arc(cx, cy, r, a0, a1, c=DEF, w=1.6):
    return P(arc_pts(cx, cy, r, a0, a1), c, w)


def wall(x, y, h=56, side='left', c=INK):
    """垂直牆固定端（給水平桿件）。side='left' 表示牆在桿件左側。"""
    o = L(x, y - h / 2, x, y + h / 2, c, 3)
    n = 7
    for i in range(n + 1):
        yy = y - h / 2 + h * i / n
        dx = -8 if side == 'left' else 8
        o += L(x, yy, x + dx, yy + 7, c, 1)
    return o


def roller(x, y, c=INK, s=10):
    o = P([(x, y), (x - s, y + s * 1.4), (x + s, y + s * 1.4)], c, 1.5, fill='#fff', close=True)
    o += C(x - s * 0.55, y + s * 1.4 + 4, 3.5, '#fff', c, 1.2) + C(x + s * 0.55, y + s * 1.4 + 4, 3.5, '#fff', c, 1.2)
    o += L(x - s * 1.5, y + s * 1.4 + 8, x + s * 1.5, y + s * 1.4 + 8, c, 1.5)
    return o


def udl(x1, x2, y, q=22, n=9, c=LOAD, label=''):
    """向下均布載重（箭頭尖端在 y）。"""
    o = L(x1, y - q, x2, y - q, c, 1.6)
    for i in range(n + 1):
        xx = x1 + (x2 - x1) * i / n
        o += A(xx, y - q, xx, y - 2, c, 1.4, 7)
    if label:
        o += T((x1 + x2) / 2, y - q - 8, label, 15, c, 'middle', 'bold')
    return o


def curve_pts(x0, y0, Lpx, fn, scale, n=80):
    """水平桿件：x 從 x0 到 x0+Lpx，fn(xi) 為向上為正的位移（以 L 為單位），scale 把位移換成像素。"""
    return [(x0 + Lpx * i / n, y0 - scale * fn(i / n)) for i in range(n + 1)]


def joint(x, y, c=INK, r=4.5):
    return C(x, y, r, c, c, 1)


def hinge(x, y, c=INK, r=5.5):
    return C(x, y, r, '#fff', c, 1.8)


def bmd(pl, fn, a=0.0, b=1.0, c=MOM, fill='#ef9a9a', n=160):
    """彎矩圖：曲線＋與基線之間塗色（一個多邊形，正負都對）。"""
    pts = [pl.pt(a + (b - a) * i / n, fn(a + (b - a) * i / n)) for i in range(n + 1)]
    poly = pts + [pl.pt(b, 0), pl.pt(a, 0)]
    o = P(poly, None, fill=fill, close=True, op=0.38)
    o += L(pl.X(a), pl.Y(0), pl.X(b), pl.Y(0), INK, 1.4)
    o += P(pts, c, 2.4)
    return o
