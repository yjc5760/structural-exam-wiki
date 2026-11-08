# -*- coding: utf-8 -*-
"""第 7 章：種子樹（沿用圖 0-1）、解題流程圖。"""
from plot import *  # noqa
from calcs import *  # noqa
import figs_ch0


def fig7_1():
    return figs_ch0.fig0_1()


def _node(x, y, w, h, t, sub, c, fill='#fff'):
    o = R(x - w / 2, y, w, h, fill, c, 2, 10)
    o += T(x, y + 26, t, 15, c, 'middle', 'bold')
    if sub:
        o += T(x, y + 50, sub, 14, INK, 'middle')
    return o


def _dia(x, y, w, h, t, c):
    o = P([(x, y), (x + w / 2, y + h / 2), (x, y + h), (x - w / 2, y + h / 2)], c, 2, fill=WARN2, close=True)
    o += T(x, y + h / 2 + 5, t, 14, c, 'middle', 'bold')
    return o


def fig7_2():
    W, H = 900, 1000
    o = ''
    cx = 300
    # 左欄：斷面
    o += T(cx, 30, '斷面（第 1–3 章）', 17, AC, 'middle', 'bold')
    o += _node(cx, 50, 380, 64, '① 切塊：每塊 *b*、*h*、*y*_{i}', '先確認上下順序（2010-1）', INK)
    o += A(cx, 116, cx, 142, INK, 2, 9)
    o += _dia(cx, 144, 300, 70, '上下對稱？', WARN)
    o += T(cx + 160, 172, '是', 15, TEN, 'start', 'bold')
    o += A(cx + 150, 179, 640, 179, TEN, 2, 9)
    o += _node(735, 150, 190, 64, '封閉式', 'H：*b*_{f}*t*_{f}(*d* − *t*_{f}) + *t*_{w}*h*_{w}^{2}/4', TEN)
    o += T(cx - 20, 236, '否', 15, COMP, 'end', 'bold')
    o += A(cx, 214, cx, 250, INK, 2, 9)
    # 兩條線
    o += _node(cx - 100, 252, 190, 120, '彈性線（藍）', '', AC, AC2)
    o += T(cx - 100, 302, 'ENA：Σ*Ay*/Σ*A*', 14, INK, 'middle')
    o += T(cx - 100, 326, '*I* = Σ(*bh*^{3}/12 + *Ad*^{2})', 14, INK, 'middle')
    o += T(cx - 100, 350, '*M*_{y} = *F*_{y}*I*/*c*_{max}', 14, INK, 'middle', 'bold')
    o += _node(cx + 100, 252, 190, 120, '塑性線（紫）', '', KEY, KEY2)
    o += T(cx + 100, 302, 'PNA：累加到 *A*/2', 14, INK, 'middle')
    o += T(cx + 100, 326, '*Z* = Σ*A*_{i}|*y*_{i} − *y*_{PNA}|', 14, INK, 'middle')
    o += T(cx + 100, 350, '*M*_{p} = *F*_{y}*Z*', 14, INK, 'middle', 'bold')
    o += A(cx - 100, 374, cx - 10, 410, INK, 1.8, 9) + A(cx + 100, 374, cx + 10, 410, INK, 1.8, 9)
    o += A(735, 216, cx + 192, 440, TEN, 1.6, 9)
    o += _node(cx, 412, 380, 64, '② 檢查 *f* = *Z*/*S*', 'H 1.1 多、矩形 1.5、圓 1.70、T 1.8', INK)
    o += A(cx, 478, cx, 510, INK, 2.4, 11)
    # 崩塌
    o += T(cx, 532, '崩塌（第 4–6 章）', 17, COMP, 'middle', 'bold')
    o += _node(cx, 548, 380, 64, '③ 靜不定度 *n* → 鉸數 *n* + 1', '說出前提：結實＋側撐', INK)
    o += A(cx, 614, cx, 640, INK, 2, 9)
    o += _dia(cx, 642, 300, 70, '集中載重？', WARN)
    o += T(cx + 160, 670, '是', 15, TEN, 'start', 'bold')
    o += A(cx + 150, 677, 640, 677, TEN, 2, 9)
    o += _node(735, 648, 190, 64, '鉸在載重點', '直接虛功，不必微分', TEN)
    o += T(cx - 20, 734, '否（均佈）', 15, COMP, 'end', 'bold')
    o += A(cx, 712, cx, 748, INK, 2, 9)
    o += _node(cx, 750, 380, 64, '④ 設 *x*，虛功 *w*_{u}(*x*)', '外功 *w*·面積；內功 Σ*M*_{p}*θ*', COMP)
    o += A(cx, 816, cx, 842, INK, 2, 9)
    o += A(735, 714, cx + 192, 948, TEN, 1.6, 9)
    o += _node(cx, 844, 380, 64, '⑤ d*w*_{u}/d*x* = 0，取最小', '固端-簡支：0.414*L*、11.66*M*_{p}/*L*^{2}', COMP)
    o += A(cx, 910, cx, 932, INK, 2, 9)
    o += _node(cx, 934, 380, 58, '⑥ 畫彎矩圖：|*M*| ≤ *M*_{p}？', '', KEY, KEY2)
    # 右欄：自我檢查
    bx = 600
    o += R(bx, 360, 290, 250, '#fff', STEEL, 1.4, 10)
    o += T(bx + 145, 388, '每一步的自我檢查', 16, INK, 'middle', 'bold')
    chk = ['上下面積各 *A*/2？', '*C* × 力臂 = *M*_{p}？', '*Z* ≥ *S*？', '答案在 8 與 16 之間？', '鉸不在跨中？', '最大正彎矩點 = 鉸位？']
    for i, s in enumerate(chk):
        o += T(bx + 20, 424 + i * 30, '□ ' + s, 15, INK, 'start')
    o += R(bx, 800, 290, 120, KEY2, KEY, 1.4, 10)
    o += T(bx + 145, 830, '是 → 唯一解，交卷', 15, KEY, 'middle', 'bold')
    o += T(bx + 145, 860, '否 → 還有更小的機構', 15, COMP, 'middle', 'bold')
    o += T(bx + 145, 888, '回到 ④ 再猜', 15, COMP, 'middle')
    o += A(cx + 192, 963, bx, 880, KEY, 1.6, 9)
    return svg(W, H, o, '塑性分析解題流程圖')


ALL = {'fig7_1': fig7_1, 'fig7_2': fig7_2}
