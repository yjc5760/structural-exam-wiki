# -*- coding: utf-8 -*-
"""第 8 章：種子 → 工具 → 考題 樹、解題流程圖。"""
from sa_draw import *  # noqa
import math

SEEDS = [('S1', '平衡', FOR), ('S2', '功＝三角形', PUR), ('S3', '材料律（含轉折）', LOAD),
         ('S4', '卡氏 ∂*U*/∂*P* = Δ', MOM), ('S5', '疊加 *M* = *M*_{0} + *Pm*', DEF), ('S6', '直線×任意', INK)]
# (名稱, 章, 來自哪些種子, 用在哪些考題)
TOOLS = [
    ('五種應變能', '1', [1, 2], ['2014-4', '2012-2', '2006-1', '2018-3']),
    ('卡氏定理＋虛設力', '2', [3], ['2013-2', '2014-4']),
    ('單位力法', '2', [3, 4], ['2016-3', '2006-1']),
    ('數 *n*、選多餘力', '3', [0], ['2017-2', '2019-1', '2013-2']),
    ('∂*U*/∂*R* = 0（沉陷 = δ）', '3', [3, 4], ['2005-1', '2008-3', '2014-4', '2013-2']),
    ('分段彎矩、開關〈〉', '4', [0], ['2005-1', '2013-2', '2017-2']),
    ('圖乘表、⅔、⅜、Simpson', '4', [5, 4], ['2016-3']),
    ('固端彎矩 *Pab*^{2}/*L*^{2}…', '5', [3, 4], ['2017-2']),
    ('桁架表格、彈簧＝桿', '6', [1, 2], ['2012-2', '2006-1', '2019-1']),
    ('纜索鬆弛、*n*+1 機構', '7', [2], ['2018-3', '2019-1']),
]
QS = ['2005-1', '2006-1', '2008-3', '2012-2', '2013-2', '2014-4', '2016-3', '2017-2', '2018-3', '2019-1']


def fig8_1():
    W = 900
    sx, sw, sh, sgap, sy0 = 10, 190, 46, 70, 70
    tx, tw, th, tgap, ty0 = 290, 300, 34, 44, 64
    qx, qw, qh, qgap, qy0 = 720, 120, 30, 44, 64
    H = ty0 + len(TOOLS) * tgap + 30
    o = T(sx + sw / 2, 34, '6 顆種子', 17, PUR, 'middle', 'bold')
    o += T(tx + tw / 2, 34, '10 件工具（第幾章）', 17, INK, 'middle', 'bold')
    o += T(qx + qw / 2, 34, '10 道考題', 17, MOM, 'middle', 'bold')
    sp = {}
    for i, (sid, txt, c) in enumerate(SEEDS):
        y = sy0 + i * sgap
        sp[i] = (sx + sw, y + sh / 2, c)
        o += R(sx, y, sw, sh, '#fff', c, 2.2, 9) + R(sx, y, 40, sh, c, None, 0, 9) + R(sx + 28, y, 12, sh, c, None)
        o += T(sx + 20, y + 29, sid, 15, '#fff', 'middle', 'bold') + T(sx + 48, y + 29, txt, 14, INK, 'start', 'bold')
    qp = {}
    for j, q in enumerate(QS):
        y = qy0 + j * qgap
        qp[q] = (qx, y + qh / 2)
        o += R(qx, y, qw, qh, '#ffebee', MOM, 1.4, 7) + T(qx + qw / 2, y + 21, q, 15, MOM, 'middle', 'bold')
    for k, (nm, ch, seeds, qs) in enumerate(TOOLS):
        y = ty0 + k * tgap
        x2, y2 = tx, y + th / 2
        for si in seeds:
            x1, y1, c = sp[si]
            mx = (x1 + x2) / 2
            o += f'<path d="M{f(x1)},{f(y1)} C{f(mx)},{f(y1)} {f(mx)},{f(y2)} {f(x2 - 6)},{f(y2)}" fill="none" stroke="{c}" stroke-width="1.7" opacity=".7"/>'
            o += head(x2, y2, 0, c, 7)
        for q in qs:
            x3, y3 = qp[q]
            mx = (tx + tw + x3) / 2
            o += f'<path d="M{f(tx + tw)},{f(y2)} C{f(mx)},{f(y2)} {f(mx)},{f(y3)} {f(x3)},{f(y3)}" fill="none" stroke="{STEEL}" stroke-width="1.2" opacity=".8"/>'
        o += R(tx, y, tw, th, '#fafafa', STEEL, 1.1, 7) + R(tx, y, 46, th, STEEL2, None, 0, 7)
        o += T(tx + 23, y + 23, f'第{ch}章', 14, MUT, 'middle', 'bold') + T(tx + 56, y + 23, nm, 14, INK, 'start', 'bold')
    return svg(W, int(H), o, '種子工具考題樹')


def fig8_2():
    W, H = 900, 560
    steps = [
        ('① 讀題', '指定方法？求反力／位移／轉角／彎矩圖？', INK),
        ('② 數 *n*、選多餘力', '拿掉後要站得住（S1）', FOR),
        ('③ 每根構件問一句', '有沒有 *M*？*N*？彈簧？纜索？', LOAD),
        ('④ 寫 *M*(*x*)', '分段＝開關；∂*M*/∂*R* = *m*（S5）', MOM),
        ('⑤ 列方程', '∂*U*/∂*R* = 0；沉陷 = δ；彈簧多一項', PUR),
        ('⑥ 積分', '圖乘表／Simpson（S6）', DEF),
        ('⑦ 檢查符號', '纜索、只能壓的支承：負值 → 拿掉重解', COMP),
        ('⑧ 求位移／轉角', '虛設力 *Q*：先微分、再令 0、後積分', MOM),
        ('⑨ 極限檢查', '5*P*/16、*PL*/8、*wL*^{2}/12、*k* → ∞', FOR),
    ]
    bw, bh = 400, 74
    o = ''
    pos = []
    for i, (t, s, c) in enumerate(steps):
        col = 0 if i < 5 else 1
        row = i if i < 5 else i - 5
        x = 30 if col == 0 else 470
        y = 30 + row * 104
        pos.append((x, y))
        o += R(x, y, bw, bh, '#fff', c, 2, 10) + R(x, y, 8, bh, c, None, 0, 4)
        o += T(x + 24, y + 30, t, 17, c, 'start', 'bold') + T(x + 24, y + 58, s, 15, INK, 'start')
    for i in range(len(steps) - 1):
        (x1, y1), (x2, y2) = pos[i], pos[i + 1]
        if i == 4:
            o += P([(x1 + bw, y1 + bh / 2), (450, y1 + bh / 2), (450, y2 + bh / 2), (x2 - 2, y2 + bh / 2)], INK, 1.8)
            o += head(x2, y2 + bh / 2, 0, INK, 9)
        else:
            o += A(x1 + 60, y1 + bh, x2 + 60, y2 - 2, INK, 1.8, 9)
    x, y = pos[6]
    o += T(x + bw - 8, y + bh + 22, '有負值 → 回 ②', 14, COMP, 'end', 'bold')
    return svg(W, H, o, '最小功法解題流程')


ALL = {'fig8_1': fig8_1, 'fig8_2': fig8_2}
