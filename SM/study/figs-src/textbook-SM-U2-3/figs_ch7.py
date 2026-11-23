# -*- coding: utf-8 -*-
"""第 7 章：天平、2017-4 上舉反算曲線。"""
from plot import *  # noqa
from calcs import *  # noqa


def fig7_1():
    W, H = 900, 380
    o = ''
    cx, cy = 450, 90
    o += P([(cx, cy), (cx - 30, 330), (cx + 30, 330)], INK, 2, fill=STEEL2, close=True)
    o += L(cx - 300, cy + 20, cx + 300, cy - 20, INK, 4)
    o += C(cx, cy, 8, KEY, '#fff', 2)
    for side, x, y, title, items, c, fill in ((-1, cx - 300, cy + 20, '驅動（分母）', ['*γH*', '超載 *q*', '受壓水頭 *h*_{w}', '水頭差 Δ*H*'], TEN, TEN2),
                                               (1, cx + 300, cy - 20, '抵抗（分子）', ['*S*_{u}（改良）', '不透水層 *t*', '貫入 *D*', '支撐、斷面'], COMP, COMP2)):
        o += L(x, y, x, y + 40, INK, 1.4)
        o += R(x - 120, y + 40, 240, 160, fill, c, 1.8, 10)
        o += T(x, y + 66, title, 16, c, 'middle', 'bold')
        for k, it in enumerate(items):
            o += T(x, y + 94 + k * 26, it, 15, INK, 'middle')
    o += T(cx - 300, 330, '① 先拿掉（便宜）', 15, TEN, 'middle', 'bold')
    o += T(cx + 300, 330, '② 再加上（貴）', 15, COMP, 'middle', 'bold')
    o += T(cx, 362, '反算：目標 *FS* 代入，解盤上的任一個量', 15, KEY, 'middle', 'bold')
    return svg(W, H, o, '天平')


def fig7_2():
    d = ex2017_4_water()
    W, H = 900, 400
    pl = Plot(90, 50, 560, 290, 0, 10, 0, 3)
    o = pl.axes([0, 2, 4, 6, 8, 10], [0, 1, 2, 3], '受壓水位 GL−(m)', '*FS*')
    f = lambda g: d['W'] / max(d['top_SM'] - g, 1e-6)
    o += pl.curve(lambda g: min(f(g), 3), 0, 9.0, KEY, 3)
    o += pl.hline(1.0, 0, 10, COMP, 1.3) + pl.hline(2.0, 0, 10, WARN, 1.3)
    o += T(pl.X(0.1), pl.Y(2.0) - 6, '目標 2.0', 14, WARN, 'start', 'bold') + T(pl.X(0.1), pl.Y(1.0) - 6, '1.0', 14, COMP, 'start')
    o += pl.dot(1.0, d['FSu'], COMP, 6.5) + T(pl.X(1.0) + 10, pl.Y(d['FSu']) + 20, f"設計水位 GL−1.0：{d['FSu']:.2f}", 14, COMP, 'start', 'bold')
    o += pl.dot(d['GL_req'], 2.0, KEY, 7) + pl.vline(d['GL_req'], 0, 2.0, KEY, 1.3)
    o += T(pl.X(d['GL_req']) - 10, pl.Y(2.0) - 10, f"GL−{d['GL_req']:.2f}", 15, KEY, 'end', 'bold')
    o += box(670, 70, 215, 150, '反算', ['*W*=1.86×2.32=4.315', '*h*_{w}=4.315/2=2.158', '10.32−2.158', '=8.16 m'], KEY2, KEY)
    return svg(W, H, o, '上舉反算')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
