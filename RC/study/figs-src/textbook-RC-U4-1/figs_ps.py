# -*- coding: utf-8 -*-
"""預力教科書共用圖元：I 形斷面、應力分布塊、四聯疊加圖、梁立面。壓為正（畫在軸左側、紅），拉為負（右側、綠）。"""
from figs_common import *  # noqa
from calcs import tf, tfm

# 示範梁的 I 形尺寸：作者自訂，使 A = 1100、I ≈ 469,000（題目只給 A、I、c）
IB = dict(h=60.0, bf=30.0, tf=12.5, tw=10.0)


def ibeam(xc, y0, sc, col=INK, fill=STEEL2, d=IB):
    h, bf, tf_, tw = d['h'], d['bf'], d['tf'], d['tw']
    pts = [(-bf / 2, 0), (bf / 2, 0), (bf / 2, tf_), (tw / 2, tf_), (tw / 2, h - tf_), (bf / 2, h - tf_), (bf / 2, h),
           (-bf / 2, h), (-bf / 2, h - tf_), (-tw / 2, h - tf_), (-tw / 2, tf_), (-bf / 2, tf_)]
    return P([(xc + x * sc, y0 + y * sc) for x, y in pts], col, 1.6, fill=fill, close=True)


def rect_sec(xc, y0, sc, b, h, col=INK, fill=STEEL2):
    return R(xc - b * sc / 2, y0, b * sc, h * sc, fill, col, 1.6)


def sblock(xa, y0, hp, top, bot, k, label=True, size=14, fmt='{:.2f}', lab_top=None, lab_bot=None):
    """線性應力分布：xa 為零應力軸，壓（正）向左、拉（負）向右。k = px / (kgf/cm²)。"""
    yb = y0 + hp
    xt = xa - k * top; xb = xa - k * bot
    o = L(xa, y0 - 6, xa, yb + 6, MUT, 1.1, '4 3')
    if top * bot >= 0:
        fill = COMP2 if (top + bot) > 0 else TEN2
        o += P([(xa, y0), (xt, y0), (xb, yb), (xa, yb)], None, fill=fill, close=True)
    else:
        y0z = y0 + hp * top / (top - bot)
        o += P([(xa, y0), (xt, y0), (xa, y0z)], None, fill=COMP2 if top > 0 else TEN2, close=True)
        o += P([(xa, y0z), (xb, yb), (xa, yb)], None, fill=COMP2 if bot > 0 else TEN2, close=True)
    o += L(xt, y0, xb, yb, INK, 2)
    o += L(xa, y0, xt, y0, INK, 1.4) + L(xa, yb, xb, yb, INK, 1.4)
    if label:
        for v, yy, lab, dy in ((top, y0, lab_top, -7), (bot, yb, lab_bot, 19)):
            txt = lab if lab is not None else fmt.format(v).replace('-', '−')
            col = COMP if v > 0 else (TEN if v < 0 else MUT)
            xx = xa - k * v
            anc = 'start' if v > 0 else ('end' if v < 0 else 'middle')
            o += T(xx, yy + dy, txt, size, col, anc, 'bold')
    return o


def sum_panels(items, total, title, W=900, H=330, hp=170, y0=80, k=None, note=None, sec=None):
    """items = [(名稱, top, bot)]；total = (top, bot)。等號前各項、等號後合計。"""
    o = T(W / 2, 28, title, 16, INK, 'middle', 'bold')
    n = len(items) + 1
    big = max(abs(v) for it in items for v in it[1:]) if items else 1
    big = max(big, abs(total[0]), abs(total[1]))
    k = k or 80 / big
    x0 = 70 if sec is None else 150
    if sec is not None:
        o += sec(60, y0, hp)
    gap = (W - x0 - 40) / n
    for i, (name, t, b) in enumerate(items + [('合計', total[0], total[1])]):
        xa = x0 + gap * (i + 0.62)
        o += sblock(xa, y0, hp, t, b, k)
        o += T(xa, y0 + hp + 48, name, 15, KEY if i == n - 1 else INK, 'middle', 'bold')
        if i < n - 1:
            o += T(x0 + gap * (i + 1) + 6, y0 + hp / 2 + 8, '＝' if i == n - 2 else '＋', 22, INK, 'middle', 'bold')
    if note:
        o += T(W / 2, H - 12, note, 15, KEY, 'middle', 'bold')
    return svg(W, H, o, title)
