# -*- coding: utf-8 -*-
"""結構簡圖共用元件（支承、內鉸、載重、力矩箭頭）。座標一律由呼叫端依比例換算。"""
from plot import *  # noqa
import math


class Frame:
    """結構座標（m，y 向上）→ SVG 座標。"""
    def __init__(self, x0, y0, s):
        self.x0, self.y0, self.s = x0, y0, s

    def __call__(self, x, y):
        return (self.x0 + self.s * x, self.y0 - self.s * y)


def member(p, q, c=INK, w=4.5):
    return L(p[0], p[1], q[0], q[1], c, w)


def hinge(x, y, r=7, c=INK):
    return C(x, y, r, '#fff', c, 2)


def roller(x, y, c=INK, s=10):
    """滾支承（反力垂直），頂點在 (x,y)。"""
    o = P([(x, y), (x - s, y + s * 1.3), (x + s, y + s * 1.3)], c, 1.5, fill='#fff', close=True)
    o += C(x - s * 0.55, y + s * 1.3 + 4, 3.6, '#fff', c, 1.3) + C(x + s * 0.55, y + s * 1.3 + 4, 3.6, '#fff', c, 1.3)
    o += hatch_ground(x - s * 1.6, y + s * 1.3 + 8, s * 3.2, c)
    return o


def roller_wall(x, y, c=INK, s=10):
    """貼右側垂直牆的滾支承（反力水平），頂點在 (x,y)。"""
    o = P([(x, y), (x + s * 1.3, y - s), (x + s * 1.3, y + s)], c, 1.5, fill='#fff', close=True)
    o += C(x + s * 1.3 + 4, y - s * 0.55, 3.6, '#fff', c, 1.3) + C(x + s * 1.3 + 4, y + s * 0.55, 3.6, '#fff', c, 1.3)
    xw = x + s * 1.3 + 8
    o += L(xw, y - s * 1.7, xw, y + s * 1.7, c, 1.5)
    for i in range(6):
        yy = y - s * 1.7 + i * s * 3.4 / 5
        o += L(xw, yy, xw + 7, yy - 6, c, 1)
    return o


def fixed_left(x, y, h=56, c=INK):
    """左側固定牆（梁的左端），牆面在 x。"""
    o = L(x, y - h / 2, x, y + h / 2, c, 3)
    n = 7
    for i in range(n + 1):
        yy = y - h / 2 + h * i / n
        o += L(x, yy, x - 8, yy + 7, c, 1)
    return o


def fixed_bottom(x, y, w=50, c=INK):
    """柱底固定（地面線在 y，剖線向下）。"""
    return fixed_wall(x, y, w, c, top=False)


def spring_v(x, y1, y2, c=INK, n=6, amp=8):
    """垂直彈簧，由 y1（上）到 y2（下），下端接地。"""
    pts = [(x, y1), (x, y1 + 8)]
    h = (y2 - y1 - 16) / n
    for i in range(n):
        pts.append((x + (amp if i % 2 == 0 else -amp), y1 + 8 + h * (i + 0.5)))
    pts += [(x, y2 - 8), (x, y2)]
    return P(pts, c, 1.6) + hatch_ground(x - 16, y2, 32, c)


def force(tip, ang_deg, length=46, c=COMP, w=2.6, label='', lsize=15, loff=(0, 0), anchor='middle'):
    """箭頭尖端在 tip，箭頭『從 ang_deg 方向來』：ang_deg=90 表示由上往下打（向下的力）。"""
    a = math.radians(ang_deg)
    sx, sy = tip[0] + length * math.cos(a), tip[1] - length * math.sin(a)
    o = A(sx, sy, tip[0], tip[1], c, w, 11)
    if label:
        o += T(sx + loff[0], sy + loff[1], label, lsize, c, anchor, 'bold')
    return o


def moment(x, y, r=20, cw=True, c=KEY, label='', lsize=15, start=200, span=250, loff=(0, 0), anchor='middle'):
    """弧形力矩箭頭（cw=True 順時針）。角度以數學方向（逆時針、y 向上）給。"""
    pts = []
    n = 30
    for i in range(n + 1):
        t = start + (span * i / n) * (-1 if cw else 1)
        pts.append((x + r * math.cos(math.radians(t)), y - r * math.sin(math.radians(t))))
    o = curve_arrow(pts, c, 2.2, 10)
    if label:
        o += T(x + loff[0], y - r - 8 + loff[1], label, lsize, c, anchor, 'bold')
    return o


def udl(x1, x2, y, c=COMP, h=26, n=None, label='', lsize=15):
    """向下均布載重，箭頭尖端落在 y。"""
    n = n or max(3, int((x2 - x1) / 26))
    o = L(x1, y - h, x2, y - h, c, 1.6)
    for i in range(n + 1):
        xx = x1 + (x2 - x1) * i / n
        o += A(xx, y - h, xx, y - 2, c, 1.4, 7)
    if label:
        o += T((x1 + x2) / 2, y - h - 8, label, lsize, c, 'middle', 'bold')
    return o


def udl_h(x, y1, y2, c=COMP, w=26, n=None, label='', to_left=True, lsize=15):
    """水平均布載重（作用在垂直桿上），箭頭尖端落在 x。"""
    n = n or max(3, int(abs(y2 - y1) / 22))
    s = 1 if to_left else -1
    o = L(x + s * w, y1, x + s * w, y2, c, 1.6)
    for i in range(n + 1):
        yy = y1 + (y2 - y1) * i / n
        o += A(x + s * w, yy, x + s * 2, yy, c, 1.4, 7)
    if label:
        o += T(x + s * (w + 6), (y1 + y2) / 2 + 5, label, lsize, c, 'start' if s > 0 else 'end', 'bold')
    return o
