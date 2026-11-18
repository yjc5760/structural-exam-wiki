# -*- coding: utf-8 -*-
"""本單元共用的圖元：彈簧、彎矩弧箭頭、鎖、固定牆、梁變形曲線。"""
from plot import *  # noqa
import math
from calcs import hermite

TEAL = '#00838f'


def spring(x1, y, x2, c=TEN, w=2.2, n=7, amp=10, lead=14):
    """水平彈簧（鋸齒）。"""
    pts = [(x1, y), (x1 + lead, y)]
    seg = (x2 - x1 - 2 * lead) / (2 * n)
    for i in range(2 * n):
        pts.append((x1 + lead + seg * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts += [(x2 - lead, y), (x2, y)]
    return P(pts, c, w)


def vwall(x, y, h, c=INK, left=True):
    """垂直固定牆，斜線畫在左側（left=True）或右側。"""
    o = L(x, y - h / 2, x, y + h / 2, c, 3)
    n = max(4, int(h / 9))
    for i in range(n + 1):
        yy = y - h / 2 + h * i / n
        o += L(x, yy, x + (-8 if left else 8), yy + 7, c, 1)
    return o


def lock(x, y, c=WARN, s=11):
    """鎖住的符號（小鎖頭）。"""
    o = P([(x - s * 0.55, y - s * 0.2), (x - s * 0.55, y - s * 0.75)], c, 2.2)
    o += f'<path d="M{f(x - s * 0.55)},{f(y - s * 0.75)} A{f(s * 0.55)},{f(s * 0.55)} 0 0 1 {f(x + s * 0.55)},{f(y - s * 0.75)}" fill="none" stroke="{c}" stroke-width="2.2"/>'
    o += L(x + s * 0.55, y - s * 0.75, x + s * 0.55, y - s * 0.2, c, 2.2)
    o += R(x - s * 0.85, y - s * 0.25, s * 1.7, s * 1.25, c, None, 0, 2.5)
    return o


def arc_arrow(cx, cy, r, a0, a1, c=COMP, w=2.2, size=10):
    """圓弧箭頭；a0→a1 為數學角度（度，逆時針為正，0° 朝右）。a1>a0 表示逆時針。"""
    n = 24
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return curve_arrow(pts, c, w, size)


def beam_shape(x0, y0, Lpx, coeffs, scale, c=AC, w=3, dash=None, n=80):
    """以 Hermite 形狀畫梁的變形：coeffs=(v1, θ1L, v2, θ2L)，scale=像素/單位，向上為正。"""
    pts = []
    for i in range(n + 1):
        xi = i / n
        N = hermite(xi)
        v = sum(a * b for a, b in zip(coeffs, N))
        pts.append((x0 + Lpx * xi, y0 - scale * v))
    return P(pts, c, w, dash=dash)


def node(x, y, r=7, c=INK):
    return C(x, y, r, '#fff', c, 2)


def roller_block(x, y, w=34, h=26, fill='#fff', c=INK):
    """可滑動的節點塊（彈簧串接用）。"""
    return R(x - w / 2, y - h / 2, w, h, fill, c, 2, 4)


# ───────── 第 3～8 章共用：平面剛架的變形形狀（全部由節點位移＋Hermite 算出） ─────────
class Frame:
    """模型座標（y 向上）→ 畫面座標。nodes={名: (x, y)}，members=[(i, j)]。"""
    def __init__(self, nodes, members, X0, Y0, sc):
        self.n, self.m, self.X0, self.Y0, self.sc = nodes, members, X0, Y0, sc

    def S(self, x, y):
        return (self.X0 + x * self.sc, self.Y0 - y * self.sc)

    def P(self, name):
        return self.S(*self.n[name])

    def undeformed(self, c=STEEL, w=2, dash='6 5'):
        o = ''
        for i, j in self.m:
            o += L(*self.P(i), *self.P(j), c, w, dash)
        return o

    def solid(self, c=INK, w=5):
        o = ''
        for i, j in self.m:
            o += L(*self.P(i), *self.P(j), c, w)
        return o

    def deformed(self, D, amp=1.0, c=AC, w=3.2, n=60, rel=None):
        """D={名: (u, v, θ)}（缺者為 0）。rel={(i,j): (θi, θj)} 可覆寫桿端轉角（鉸接、彈簧）。"""
        o = ''
        for i, j in self.m:
            (x1, y1), (x2, y2) = self.n[i], self.n[j]
            Ln = math.hypot(x2 - x1, y2 - y1); cc, ss = (x2 - x1) / Ln, (y2 - y1) / Ln
            u1, v1, t1 = D.get(i, (0, 0, 0)); u2, v2, t2 = D.get(j, (0, 0, 0))
            if rel and (i, j) in rel:
                t1, t2 = rel[(i, j)]
            a1, a2 = cc * u1 + ss * v1, cc * u2 + ss * v2
            w1, w2 = -ss * u1 + cc * v1, -ss * u2 + cc * v2
            pts = []
            for k in range(n + 1):
                xi = k / n
                N = hermite(xi)
                tr = (w1 * N[0] + t1 * Ln * N[1] + w2 * N[2] + t2 * Ln * N[3]) * amp
                ax = (a1 * (1 - xi) + a2 * xi) * amp
                x = x1 + cc * (xi * Ln + ax) - ss * tr
                y = y1 + ss * (xi * Ln + ax) + cc * tr
                pts.append(self.S(x, y))
            o += P(pts, c, w)
        return o


def hinge(x, y, r=6, c=INK):
    return C(x, y, r, '#fff', c, 2)


def plastic_hinge(x, y, r=8):
    return C(x, y, r, COMP, '#fff', 2)


def mat_grid(x, y, cells, cw=78, ch=40, hdr=None, rowhdr=None, colors=None, size=15):
    """畫一個數字矩陣（cells[i][j] 字串），colors[i][j] 底色。"""
    o = ''
    n, m = len(cells), len(cells[0])
    for i in range(n):
        for j in range(m):
            fill = colors[i][j] if colors and colors[i][j] else '#fff'
            o += R(x + j * cw, y + i * ch, cw, ch, fill, STEEL, 1)
            o += T(x + j * cw + cw / 2, y + i * ch + ch / 2 + 5.5, cells[i][j], size, INK, 'middle', 'bold')
    if hdr:
        for j, hname in enumerate(hdr):
            o += T(x + j * cw + cw / 2, y - 10, hname, 14, MUT, 'middle', 'bold')
    if rowhdr:
        for i, hname in enumerate(rowhdr):
            o += T(x - 10, y + i * ch + ch / 2 + 5, hname, 14, MUT, 'end', 'bold')
    return o
