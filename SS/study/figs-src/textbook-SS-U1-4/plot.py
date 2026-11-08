# -*- coding: utf-8 -*-
"""繪圖共用：座標軸、曲線（以 lib.py 的 SVG 原件為基礎）。字級比舊講義放大，方便年長讀者閱讀。"""
from lib import *  # noqa
import math

FS_BASE = 15   # 圖內基本字級


class Plot:
    def __init__(self, x0, y0, w, h, xmin, xmax, ymin, ymax):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax

    def X(self, v):
        return self.x0 + (v - self.xmin) / (self.xmax - self.xmin) * self.w

    def Y(self, v):
        return self.y0 + self.h - (v - self.ymin) / (self.ymax - self.ymin) * self.h

    def pt(self, x, y):
        return (self.X(x), self.Y(y))

    def axes(self, xticks, yticks, xlabel='', ylabel='', grid=True, xfmt=None, yfmt=None, size=13):
        o = ''
        xb, yb = self.x0, self.y0 + self.h
        if grid:
            for t in xticks:
                o += L(self.X(t), self.y0, self.X(t), yb, GRID, 1)
            for t in yticks:
                o += L(self.x0, self.Y(t), self.x0 + self.w, self.Y(t), GRID, 1)
        o += A(xb, yb, self.x0 + self.w + 14, yb, INK, 1.6, 9)
        o += A(xb, yb, xb, self.y0 - 14, INK, 1.6, 9)
        for t in xticks:
            o += L(self.X(t), yb, self.X(t), yb + 5, INK, 1.2)
            o += T(self.X(t), yb + 20, xfmt(t) if xfmt else f(t), size, MUT, 'middle')
        for t in yticks:
            o += L(xb - 5, self.Y(t), xb, self.Y(t), INK, 1.2)
            o += T(xb - 9, self.Y(t) + 4.5, yfmt(t) if yfmt else f(t), size, MUT, 'end')
        if xlabel:
            o += T(self.x0 + self.w + 18, yb + 5, xlabel, size + 2, INK, 'start')
        if ylabel:
            o += T(xb, self.y0 - 22, ylabel, size + 2, INK, 'middle')
        return o

    def curve(self, fn, a, b, c=INK, w=2.4, dash=None, n=240, clip=True, op=None):
        pts = []
        for i in range(n + 1):
            x = a + (b - a) * i / n
            y = fn(x)
            if clip:
                y = max(self.ymin, min(self.ymax, y))
            pts.append(self.pt(x, y))
        return P(pts, c, w, dash=dash, op=op)

    def area(self, fn_top, fn_bot, a, b, fill, op=0.5, n=200):
        top = [self.pt(a + (b - a) * i / n, min(self.ymax, fn_top(a + (b - a) * i / n))) for i in range(n + 1)]
        bot = [self.pt(a + (b - a) * i / n, max(self.ymin, fn_bot(a + (b - a) * i / n))) for i in range(n + 1)][::-1]
        return P(top + bot, None, fill=fill, close=True, op=op)

    def dot(self, x, y, c=INK, r=5):
        return C(self.X(x), self.Y(y), r, c, '#fff', 1.6)

    def hline(self, y, a=None, b=None, c=INK, w=1.4, dash='5 4'):
        a = self.xmin if a is None else a
        b = self.xmax if b is None else b
        return L(self.X(a), self.Y(y), self.X(b), self.Y(y), c, w, dash)

    def vline(self, x, a=None, b=None, c=INK, w=1.4, dash='5 4'):
        a = self.ymin if a is None else a
        b = self.ymax if b is None else b
        return L(self.X(x), self.Y(a), self.X(x), self.Y(b), c, w, dash)


def box(x, y, w, h, title, lines=(), fill=AC2, c=AC, tsize=15, lsize=13.5, rx=9, tcol=None):
    o = R(x, y, w, h, fill, c, 1.6, rx)
    o += T(x + w / 2, y + 22, title, tsize, tcol or c, 'middle', 'bold')
    for i, s in enumerate(lines):
        o += T(x + w / 2, y + 22 + (i + 1) * (lsize + 7), s, lsize, INK, 'middle')
    return o


def badge(x, y, txt, c, size=13):
    w = len(txt) * size * 0.95 + 14
    return R(x, y - size - 2, w, size + 9, c, None, 0, 6) + T(x + w / 2, y + 1, txt, size, '#fff', 'middle', 'bold')
