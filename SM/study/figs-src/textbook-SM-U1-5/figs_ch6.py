# -*- coding: utf-8 -*-
"""第 6 章：十字片剪、靈敏度、正規化強度剖面。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig6_1():
    W, H = 900, 420
    o = ''
    cx, top, h, rw, ry = 230, 110, 200, 90, 26
    # 圓柱
    o += P([(cx - rw, top), (cx - rw, top + h)], INK, 1.8) + P([(cx + rw, top), (cx + rw, top + h)], INK, 1.8)
    def ell(y, dash=None, fill='none'):
        pts = [(cx + rw * math.cos(t), y + ry * math.sin(t)) for t in [i * math.pi / 40 for i in range(81)]]
        return P(pts, INK, 1.6, fill=fill, dash=dash)
    o += ell(top, fill=COMP2) + ell(top + h, dash='5 4')
    o += R(cx - rw, top, 2 * rw, h, AC2, None, 0, op=0.5)
    o += ell(top, fill=COMP2)
    # 葉片
    o += L(cx, top - 70, cx, top + h, INK, 4)
    o += L(cx - rw, top + h / 2, cx + rw, top + h / 2, STEEL, 6) + L(cx - rw * 0.55, top + h / 2 + ry * 0.8, cx + rw * 0.55, top + h / 2 - ry * 0.8, STEEL, 6)
    o += curve_arrow([(cx + 40 * math.cos(t), top - 50 + 12 * math.sin(t)) for t in [math.pi * 0.2 + i * math.pi * 1.4 / 20 for i in range(21)]], COMP, 2.4, 11)
    o += T(cx + 50, top - 56, '扭力 *T*', 16, COMP, 'start', 'bold')
    o += dim(cx - rw, top + h + 46, cx + rw, top + h + 46, '*d*', INK, size=15)
    o += dim(cx + rw + 30, top, cx + rw + 30, top + h, '*h*', INK, size=15)
    o += T(cx - rw - 10, top + h / 2, '側面', 15, AC, 'end', 'bold')
    o += T(cx - rw - 10, top + h / 2 + 22, '*S*_{u}·*πdh*', 15, AC, 'end')
    o += T(cx - rw - 10, top - 4, '端面', 15, COMP, 'end', 'bold')
    o += box(440, 80, 440, 220, '扭力＝側面＋兩端', ['側面：*S*_{u}(*πdh*)·*d*/2 = *S*_{u}*πd*²*h*/2', '一端：∫ *S*_{u}·2*πr*·*r* d*r* = *S*_{u}*πd*³/12', '兩端：*S*_{u}*πd*³/6',
                                                    '⇒ *S*_{u}=*T* / *π*(*d*²*h*/2+*d*³/6)', '例 *d*=65、*h*=130 mm、*T*=50 N·m → 49.67 kPa'], KEY2, KEY, lsize=15)
    return svg(W, H, o, '十字片剪')


def fig6_2():
    W, H = 900, 400
    pl = Plot(90, 50, 560, 290, 0, 15, 0, 120)
    o = pl.axes([0, 3, 6, 9, 12, 15], [0, 40, 80, 120], '軸應變 (%)', '單壓應力 (kPa)')
    und = lambda e: 110 * (e / 2.5) * math.exp(1 - e / 2.5) if e > 0 else 0
    rem = lambda e: 14 * (1 - math.exp(-e / 4))
    o += pl.curve(lambda e: und(e) if e <= 2.5 else 40 + 70 * math.exp(-(e - 2.5) / 2.5), 0, 15, COMP, 3)
    o += pl.curve(rem, 0, 15, AC, 3)
    o += pl.dot(2.5, 110, COMP, 6) + T(pl.X(2.5) + 10, pl.Y(110) - 8, '不擾動 *q*_{u}≈110', 15, COMP, 'start', 'bold')
    o += T(pl.X(14.8), pl.Y(rem(14.8)) - 10, '重塑 ≈14（同含水量）', 15, AC, 'end', 'bold')
    o += box(670, 70, 215, 150, '靈敏度', ['*S*_{t}=*q*_{u}/*q*_{u,r}', '本例 ≈ 7.9', '>16：流黏土', '淋溶後結構一碰就塌'], KEY2, KEY)
    return svg(W, H, o, '靈敏度')


def fig6_3():
    W, H = 900, 430
    gp, S, m = 8.0, 0.22, 0.8
    zmax = 20
    x0, y0, w, h = 120, 50, 500, 330
    X = lambda v: x0 + v / 40 * w
    Y = lambda z: y0 + z / zmax * h
    o = A(x0, y0, x0 + w + 16, y0, INK, 1.5) + A(x0, y0, x0, y0 + h + 16, INK, 1.5)
    for v in (0, 10, 20, 30, 40):
        o += L(X(v), y0, X(v), y0 + h, GRID, 1) + T(X(v), y0 - 8, f'{v}', 14, MUT, 'middle')
    for z in (0, 5, 10, 15, 20):
        o += T(x0 - 8, Y(z) + 5, f'{z}', 14, MUT, 'end')
    o += T(x0 + w + 20, y0 + 5, '*S*_{u} (kPa)', 14, INK) + T(x0 - 8, y0 + h + 30, '深度 (m)', 14, INK, 'end')
    zs = [0.05 + i * 0.05 for i in range(400)]
    o += P([(X(S * gp * z), Y(z)) for z in zs], KEY, 2.2, dash='7 4')
    def su(z):
        sv = gp * z
        pc = max(sv, 50.0)
        return S * sv * (pc / sv) ** m
    o += P([(X(min(su(z), 40)), Y(z)) for z in zs if su(z) <= 40], COMP, 3)
    o += T(X(S * gp * 18) + 10, Y(18), 'NC：0.22*σ*_{v0}′', 15, KEY, 'start', 'bold')
    o += T(X(su(2.0)) + 12, Y(2.0), '乾縮硬殼（OCR 大）', 15, COMP, 'start', 'bold')
    o += L(x0, Y(50 / gp), x0 + w, Y(50 / gp), MUT, 1, '4 3') + T(x0 + w - 4, Y(50 / gp) - 6, '*σ*_{v0}′=*p*_{c}′', 14, MUT, 'end')
    o += box(650, 80, 235, 150, 'SHANSEP', ['*S*_{u}/*σ*_{v0}′=*S*·OCR^{*m*}', 'NC：*S*≈0.22、*m*≈0.8', '→ 隨深度線性增加', '表層硬殼偏高'], KEY2, KEY, lsize=14)
    return svg(W, H, o, '正規化強度剖面')


ALL = {'fig6_1': fig6_1, 'fig6_2': fig6_2, 'fig6_3': fig6_3}
