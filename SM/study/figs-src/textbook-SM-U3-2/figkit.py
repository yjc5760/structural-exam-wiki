# -*- coding: utf-8 -*-
"""共用圖形工具：種子樹、推導樹、流程框。"""
from plot import *  # noqa


def seed_tree(seeds, W=900, title=''):
    """seeds: [(代號, 種子短句, 顏色, [長出的公式...]), ...]；兩欄排列。"""
    n = len(seeds)
    cols = 2
    rows = (n + 1) // 2
    rowh = 150
    H = 70 + rows * rowh + 10
    o = T(W / 2, 32, title, 18, KEY, 'middle', 'bold') if title else ''
    for i, (code, txt, c, kids) in enumerate(seeds):
        cx = 30 + (i % cols) * 440
        cy = 60 + (i // cols) * rowh
        o += R(cx, cy, 160, 58, KEY2, KEY, 2, 12)
        o += T(cx + 80, cy + 24, code, 16, KEY, 'middle', 'bold')
        o += T(cx + 80, cy + 47, txt, 14, INK, 'middle')
        for j, k in enumerate(kids[:4]):
            ky = cy - 8 + j * 34
            o += L(cx + 160, cy + 29, cx + 200, ky + 14, c, 1.6)
            o += R(cx + 200, ky, 220, 28, '#fff', c, 1.3, 7)
            o += T(cx + 310, ky + 20, k, 14, c, 'middle')
    return svg(W, H, o, title or '種子家族樹')


def tree_fig(seeds, leaves, links, W=900, H=430, title=''):
    """seeds: [(id, label, color)]；leaves: [(id, label, color)]；links: [(seed_id, leaf_id)]"""
    o = T(W / 2, 28, title, 17, KEY, 'middle', 'bold') if title else ''
    ns, nl = len(seeds), len(leaves)
    sw = (W - 40) / ns
    lw = (W - 40) / nl
    pos = {}
    for i, (k, lab, c) in enumerate(seeds):
        x = 20 + sw * (i + 0.5)
        pos[k] = (x, 92)
        o += R(x - sw / 2 + 6, 62, sw - 12, 60, KEY2, KEY, 2, 10)
        for j, line in enumerate(lab.split('\n')):
            o += T(x, 86 + j * 22, line, 15 if j == 0 else 14, KEY if j == 0 else INK, 'middle', 'bold' if j == 0 else None)
    for i, (k, lab, c) in enumerate(leaves):
        x = 20 + lw * (i + 0.5)
        pos[k] = (x, H - 80)
        lines = lab.split('\n')
        o += R(x - lw / 2 + 4, H - 110, lw - 8, 26 + 22 * len(lines), '#fff', c, 1.5, 8)
        for j, line in enumerate(lines):
            o += T(x, H - 90 + j * 22, line, 14, c, 'middle', 'bold' if j == 0 else None)
    for a, b in links:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        o += A(x1, y1 + 32, x2, y2 - 34, MUT, 1.3, 8)
    return svg(W, H, o, title or '種子樹')


def flow_box(x, y, w, h, txt, c=AC, fill=None, diamond=False):
    o = ''
    if diamond:
        o += P([(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)], c, 1.8, fill=fill or KEY2, close=True)
    else:
        o += R(x, y, w, h, fill or '#fff', c, 1.6, 8)
    lines = txt.split('\n')
    for j, line in enumerate(lines):
        o += T(x + w / 2, y + h / 2 + 6 + (j - (len(lines) - 1) / 2) * 20, line, 14, c, 'middle', 'bold' if j == 0 else None)
    return o


