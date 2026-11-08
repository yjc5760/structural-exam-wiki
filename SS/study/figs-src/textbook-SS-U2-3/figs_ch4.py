# -*- coding: utf-8 -*-
"""第 4 章：非破壞檢測。"""
from plot import *  # noqa
from calcs import *  # noqa
import math


def fig4_1():
    W, H = 900, 420
    o = T(450, 26, '瑕疵在哪裡 × 瑕疵長什麼樣 → 用哪一種方法', 16, INK, 'middle', 'bold')
    x0, y0, cw, ch = 220, 70, 320, 150
    o += T(x0 + cw / 2, y0 - 10, '體積型（有厚度）', 15, INK, 'middle', 'bold')
    o += T(x0 + cw * 1.5, y0 - 10, '面積型（幾乎沒厚度）', 15, INK, 'middle', 'bold')
    o += T(x0 - 14, y0 + ch / 2, '表面', 15, INK, 'end', 'bold') + T(x0 - 14, y0 + ch / 2 + 20, '（開口）', 14, MUT, 'end')
    o += T(x0 - 14, y0 + ch * 1.5, '內部', 15, INK, 'end', 'bold') + T(x0 - 14, y0 + ch * 1.5 + 20, '（封閉）', 14, MUT, 'end')
    cells = [
        (0, 0, TEN2, TEN, 'VT 目視', ['咬邊、重疊、餘高', '銲腳不足、凹坑']),
        (1, 0, AC2, AC, 'MT 磁粒／PT 液滲', ['表面裂縫', 'MT 限磁性、深約 3 mm']),
        (0, 1, WARN2, WARN, 'RT 放射線', ['氣孔、夾渣', '量「少掉的厚度」']),
        (1, 1, KEY2, KEY, 'UT 超音波', ['裂縫、未熔合、層狀撕裂', '量「界面的反射」']),
    ]
    for cx, cy, fl, c, title, lines in cells:
        x, y = x0 + cx * cw, y0 + cy * ch
        o += R(x, y, cw, ch, fl, c, 1.8)
        o += T(x + cw / 2, y + 48, title, 18, c, 'middle', 'bold')
        for i, s in enumerate(lines):
            o += T(x + cw / 2, y + 82 + i * 24, s, 14.5, INK, 'middle')
    o += T(450, 402, 'VT 是所有銲道的基本要求；其餘依瑕疵位置與形狀挑一種「最適合」的。', 14, MUT, 'middle')
    return svg(W, H, o, 'NDT 2x2')


def fig4_2():
    W, H = 900, 360
    o = ''
    # (a) RT
    o += T(220, 26, '(a) RT：射線穿過去，看「少掉的厚度」', 16, WARN, 'middle', 'bold')
    px, py, pw, ph = 60, 110, 320, 90
    o += R(px, py, pw, ph, STEEL2, INK, 1.4)
    o += C(150, py + 45, 14, '#fff', WARN, 2) + T(150, py + 75, '氣孔', 14, WARN, 'middle')
    o += L(290, py + 10, 290, py + 80, COMP, 3) + T(282, py + 30, '平行射線的裂縫', 14, COMP, 'end')
    for xx in (150, 290):
        o += A(xx, 58, xx, py - 4, WARN, 2, 9) + L(xx, py + ph + 4, xx, py + ph + 40, WARN, 2, '4 3')
    o += R(px, py + ph + 44, pw, 22, '#455a64', None, 0)
    o += R(140, py + ph + 44, 20, 22, '#eceff1', None, 0)
    o += T(150, py + ph + 90, '底片變亮', 14, TEN, 'middle', 'bold') + T(150, py + ph + 108, '→ 看得到', 14, TEN, 'middle', 'bold')
    o += T(300, py + ph + 90, '沒少厚度', 14, COMP, 'middle', 'bold') + T(300, py + ph + 108, '→ 看不到', 14, COMP, 'middle', 'bold')
    # (b) UT
    o += T(680, 26, '(b) UT：聲波撞到界面就反射', 16, KEY, 'middle', 'bold')
    qx = 500
    o += R(qx, py, 360, ph, STEEL2, INK, 1.4)
    o += R(qx + 30, py - 22, 50, 22, KEY, None, 0, 4) + T(qx + 55, py - 30, '探頭', 14, KEY, 'middle', 'bold')
    cx, cy = qx + 200, py + 55
    o += L(cx - 30, cy, cx + 30, cy, COMP, 3) + T(cx + 36, cy + 20, '裂縫（面積型）', 14, COMP, 'start')
    # 斜角入射與反射
    sx, sy = qx + 60, py
    o += A(sx, sy, cx - 5, cy - 2, KEY, 2.4, 10)
    o += A(cx - 8, cy + 6, sx + 14, sy + 16, KEY, 2.4, 10, dash='6 4')
    o += T(qx + 180, py + ph + 40, '平面缺陷正對聲波 → 回波最強', 14, TEN, 'middle', 'bold')
    o += T(qx + 180, py + ph + 62, '球形氣孔把聲波散開 → 回波弱', 14, MUT, 'middle')
    o += T(450, 345, '所以：氣孔、夾渣（體積型）→ RT；裂縫、未熔合（面積型）→ UT。', 15, INK, 'middle', 'bold')
    return svg(W, H, o, 'RT 與 UT')


def fig4_3():
    """SS-2021-1 圖一的示意重繪：T 形接頭兩道填角銲上的四種瑕疵 a～d（依題解判讀）。"""
    W, H = 900, 400
    o = T(450, 26, 'SS-2021-1 四處瑕疵（示意重繪，依題解判讀）', 16, INK, 'middle', 'bold')
    by, bt = 280, 50
    o += R(80, by, 740, bt, STEEL2, INK, 1.4)              # 底板
    sx0, sx1 = 420, 480
    o += R(sx0, 70, sx1 - sx0, by - 70, STEEL2, INK, 1.4)  # 立板
    w = 90
    # 左銲道
    o += P([(sx0, by), (sx0 - w, by), (sx0, by - w)], COMP, 1.4, fill=COMPM, close=True)
    # 右銲道
    o += P([(sx1, by), (sx1 + w, by), (sx1, by - w)], COMP, 1.4, fill=COMPM, close=True)
    # a 咬邊：左銲道上趾（立板）被熔蝕凹口
    o += P([(sx0 + 0.5, by - w - 2), (sx0 + 10, by - w - 10), (sx0 + 0.5, by - w - 20)], INK, 1.4, fill='#fff', close=True)
    # b 銲面裂縫：左銲道斜面開口鋸齒
    mx, my = sx0 - w / 2, by - w / 2
    o += P([(mx, my), (mx + 10, my + 10), (mx + 4, my + 18), (mx + 14, my + 28)], COMP, 2.4)
    # c 重疊：右銲道下趾翻捲外舖
    o += P([(sx1 + w, by), (sx1 + w + 26, by - 2), (sx1 + w + 30, by - 9), (sx1 + w - 6, by - 10)], COMP, 1.4, fill=COMPM, close=True)
    # d 母材裂縫：右銲道下趾往底板厚度方向
    dx = sx1 + w - 20
    o += P([(dx, by), (dx + 6, by + 12), (dx - 2, by + 24), (dx + 6, by + 38)], COMP, 2.4)
    labs = [(sx0 + 14, by - w - 10, 'a', '咬邊 → VT', 560, 100),
            (mx + 10, my + 14, 'b', '銲道裂縫 → MT', 300, 140),
            (sx1 + w + 18, by - 6, 'c', '重疊 → VT', 700, 200),
            (dx + 4, by + 20, 'd', '母材／HAZ 裂縫 → UT', 600, 370)]
    for px, py, k, s, lx, ly in labs:
        o += L(px, py, lx - 6 if lx > px else lx + 6, ly - 5, MUT, 1.2, '4 3')
        o += C(lx + (14 if lx > px else -14), ly - 6, 12, '#fff', COMP, 1.8) + T(lx + (14 if lx > px else -14), ly - 1, k, 15, COMP, 'middle', 'bold')
        o += T(lx + (32 if lx > px else -32), ly, s, 15, INK, 'start' if lx > px else 'end', 'bold')
    return svg(W, H, o, 'SS-2021-1 四瑕疵')


ALL = {'fig4_1': fig4_1, 'fig4_2': fig4_2, 'fig4_3': fig4_3}
