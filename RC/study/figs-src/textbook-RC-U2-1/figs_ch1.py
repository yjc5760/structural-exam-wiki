# -*- coding: utf-8 -*-
"""第 1 章：剪力破壞是拉裂——純剪微元素、莫爾圓、Vc ∝ √f'c。"""
from figs_common import *  # noqa
from calcs import demo, mohr
import math

D = demo()


def _square(cx, cy, s, ang_deg, fill=STEEL2):
    a = math.radians(ang_deg)
    pts = []
    for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x = dx * s / 2; y = dy * s / 2
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return P(pts, INK, 1.6, fill=fill, close=True)


def fig1_1():
    W, H = 900, 400
    o = T(450, 24, '剪力區的一個小方塊：剪應力 τ ＝ 45° 方向的拉應力 τ', 16, INK, 'middle', 'bold')
    # ── 左：梁端
    x0, y0, bl, bh = 30, 90, 270, 120
    o += R(x0, y0, bl, bh, STEEL2, INK, 1.6)
    o += pin(x0 + 25, y0 + bh, INK, 10)
    o += L(x0, y0 + bh / 2, x0 + bl, y0 + bh / 2, MUT, 1, '5 4')
    o += T(x0 + 6, y0 + bh / 2 - 6, '中性軸', 14, MUT, 'start')
    for i in range(4):
        xa = x0 + 110 + i * 32
        o += L(xa, y0 + bh - 4, xa + 62, y0 + 34, COMP, 2.2)
    o += R(x0 + 80 - 13, y0 + bh / 2 - 13, 26, 26, '#fff', AC, 2)
    o += A(x0 + 95, y0 + bh / 2 - 14, 372, 128, AC, 1.4, 8)
    o += A(x0 + 40, y0 - 40, x0 + 40, y0 - 4, INK, 1.8)
    o += A(x0 + 120, y0 - 40, x0 + 120, y0 - 4, INK, 1.8)
    o += A(x0 + 200, y0 - 40, x0 + 200, y0 - 4, INK, 1.8)
    o += T(x0 + 135, y0 + bh + 46, '支承附近：剪力大、彎矩小', 14, INK, 'middle')
    o += T(x0 + 135, y0 + bh + 68, '紅線＝45° 斜裂縫', 14, COMP, 'middle', 'bold')
    o += T(x0 + 80, y0 + bh / 2 + 34, '取一小塊', 14, AC, 'middle', 'bold')
    # ── 中：純剪方塊 & 轉 45°
    cx, cy, s = 420, 140, 70
    o += _square(cx, cy, s, 0, '#fff')
    o += A(cx + 28, cy - s / 2 - 8, cx - 28, cy - s / 2 - 8, WARN, 2, 8)
    o += A(cx - 28, cy + s / 2 + 8, cx + 28, cy + s / 2 + 8, WARN, 2, 8)
    o += A(cx + s / 2 + 8, cy - 28, cx + s / 2 + 8, cy + 28, WARN, 2, 8)
    o += A(cx - s / 2 - 8, cy + 28, cx - s / 2 - 8, cy - 28, WARN, 2, 8)
    o += T(cx, cy - s / 2 - 18, 'τ', 16, WARN, 'middle', 'bold', italic=True)
    o += T(cx, cy + 6, '純剪', 15, INK, 'middle', 'bold')
    o += A(cx, cy + 62, cx, cy + 100, MUT, 1.6)
    o += T(cx + 10, cy + 86, '轉 45° 看', 14, MUT, 'start')
    cy2 = 300
    o += _square(cx, cy2, s, 45, '#fff')
    r1 = s / math.sqrt(2) + 6
    for sg in (1, -1):
        ux, uy = math.cos(math.radians(45)) * sg, math.sin(math.radians(45)) * sg
        o += A(cx + ux * r1, cy2 + uy * r1, cx + ux * (r1 + 34), cy2 + uy * (r1 + 34), TEN, 2.4, 9)
        vx, vy = math.cos(math.radians(-45)) * sg, math.sin(math.radians(-45)) * sg
        o += A(cx + vx * (r1 + 34), cy2 + vy * (r1 + 34), cx + vx * r1, cy2 + vy * r1, COMP, 2.4, 9)
    o += T(cx + 74, cy2 + 56, 'σ_{1} = +τ', 15, TEN, 'start', 'bold')
    o += T(cx + 66, cy2 - 52, 'σ_{2} = −τ', 15, COMP, 'start', 'bold')
    o += L(cx - 26, cy2 + 26, cx + 26, cy2 - 26, COMP, 1.4, '3 3')
    # ── 右：莫爾圓
    pl = Plot(610, 90, 250, 250, -1.6, 1.6, -1.6, 1.6)
    o += L(pl.X(-1.6), pl.Y(0), pl.X(1.6) + 10, pl.Y(0), INK, 1.4)
    o += head(pl.X(1.6) + 14, pl.Y(0), 0, INK, 9)
    o += L(pl.X(0), pl.Y(1.6), pl.X(0), pl.Y(-1.6), INK, 1.4)
    o += head(pl.X(0), pl.Y(1.6) - 4, -math.pi / 2, INK, 9)
    o += T(pl.X(1.6) + 16, pl.Y(0) + 22, 'σ', 16, INK, 'middle', italic=True)
    o += T(pl.X(0) + 10, pl.Y(1.6) - 2, 'τ', 16, INK, 'start', italic=True)
    r = 1.0
    pts = [pl.pt(r * math.cos(t / 100 * 2 * math.pi), r * math.sin(t / 100 * 2 * math.pi)) for t in range(101)]
    o += P(pts, KEY, 2.6)
    s1, s2, th = mohr(0, 1)
    o += pl.dot(0, 1, WARN, 5) + pl.dot(0, -1, WARN, 5)
    o += L(pl.X(0), pl.Y(1), pl.X(0), pl.Y(-1), WARN, 1.6, '4 3')
    o += pl.dot(s1, 0, TEN, 6) + pl.dot(s2, 0, COMP, 6)
    o += T(pl.X(s1) + 8, pl.Y(0) + 24, 'σ_{1} = τ', 15, TEN, 'start', 'bold')
    o += T(pl.X(s2) - 8, pl.Y(0) + 24, 'σ_{2} = −τ', 15, COMP, 'end', 'bold')
    o += T(pl.X(0) + 10, pl.Y(1) - 8, '(0, τ)', 14, WARN, 'start')
    o += T(pl.X(0), pl.Y(-1.6) + 28, '圓心在原點、半徑 τ', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '純剪與莫爾圓')


def fig1_2():
    W, H = 900, 380
    pl = Plot(110, 50, 520, 270, 140, 560, 5, 13)
    o = pl.axes([140, 210, 280, 350, 420, 490, 560], [5, 7, 9, 11, 13], "*f*′_{c}", '*V*_{c}/*b*_{w}*d*', size=14)
    o += T(pl.X(560) + 18, pl.Y(5) + 26, '(kgf/cm²)', 14, MUT, 'start')
    o += pl.curve(lambda fc: 0.53 * math.sqrt(fc), 140, 560, COMP, 3.2)
    for fc in (210, 240, 280, 350, 420):
        v = 0.53 * math.sqrt(fc)
        o += pl.dot(fc, v, COMP, 5)
        o += T(pl.X(fc), pl.Y(v) - 12, f'{v:.2f}', 14, COMP, 'middle', 'bold')
    v1, v2 = 0.53 * math.sqrt(210), 0.53 * math.sqrt(420)
    o += pl.hline(v1, 210, 420, MUT, 1.2)
    o += L(pl.X(420), pl.Y(v1), pl.X(420), pl.Y(v2), KEY, 2)
    o += T(pl.X(420) + 8, pl.Y((v1 + v2) / 2) + 34, f'+{(v2 / v1 - 1) * 100:.0f}%', 16, KEY, 'start', 'bold')
    o += T(pl.X(315), pl.Y(v1) + 24, "*f*′_{c} 加倍（210 → 420）", 14, MUT, 'middle')
    o += box(665, 70, 220, 200, '記法', ['所有「裂開」的強度', '都是 √*f*′_{c}：', '*f*_{r} = 2.0√*f*′_{c}', '*V*_{c}：0.53√*f*′_{c}', '*V*_{cw}：0.93√*f*′_{c}', '*T*_{cr}：1.06√*f*′_{c}'], KEY2, KEY, 15, 14)
    o += T(pl.X(240) + 12, pl.Y(0.53 * math.sqrt(240)) + 24, '示範梁', 14, COMP, 'start')
    return svg(W, H, o, 'Vc 與 √fc')


ALL = {'fig1_1': fig1_1, 'fig1_2': fig1_2}
